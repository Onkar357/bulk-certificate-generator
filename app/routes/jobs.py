from fastapi import APIRouter,BackgroundTasks,Depends,HTTPException,status
from pydantic import ValidationError
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Certificate,GenerationJob
from app.schemas import CreateJobRequest,JobCreatedResponse,JobResponse,RecipientInput
from app.workers.certificate_worker import process_job
router=APIRouter(prefix="/jobs",tags=["jobs"])
def serialize(job):
    cs=sorted(job.certificates,key=lambda x:x.recipient_index)
    processed=sum(c.status in ("SUCCESS","FAILED") for c in cs)
    return {"id":job.id,"event_name":job.event_name,"event_date":job.event_date,"issuer_name":job.issuer_name,"status":job.status,"total_count":len(cs),"successful_count":sum(c.status=="SUCCESS" for c in cs),"failed_count":sum(c.status=="FAILED" for c in cs),"processed_count":processed,"pending_count":len(cs)-processed,"progress_percent":round(processed/len(cs)*100,2) if cs else 0,"created_at":job.created_at,"completed_at":job.completed_at,"certificates":[{"id":c.id,"job_id":job.id,"recipient_index":c.recipient_index,"recipient_name":c.recipient_name,"recipient_email":c.recipient_email,"certificate_title":c.certificate_title,"status":c.status,"error_message":c.error_message,"download_url":f"/api/v1/certificates/{c.id}/download" if c.status=="SUCCESS" else None,"created_at":c.created_at,"completed_at":c.completed_at} for c in cs]}
@router.post("",response_model=JobCreatedResponse,status_code=status.HTTP_202_ACCEPTED)
def create_job(payload:CreateJobRequest,bg:BackgroundTasks,db:Session=Depends(get_db)):
    job=GenerationJob(event_name=payload.event_name,event_date=payload.event_date,issuer_name=payload.issuer_name,total_count=len(payload.recipients)); db.add(job); db.flush()
    valid=invalid=0
    for i,raw in enumerate(payload.recipients,1):
        try:
            r=RecipientInput.model_validate(raw); c=Certificate(job_id=job.id,recipient_index=i,recipient_name=r.name,recipient_email=str(r.email),certificate_title=r.certificate_title); valid+=1
        except ValidationError as e:
            name=str(raw.get("name","Invalid recipient")).strip()[:100] or "Invalid recipient"
            err="; ".join(f"{'.'.join(map(str,x['loc']))}: {x['msg']}" for x in e.errors())
            c=Certificate(job_id=job.id,recipient_index=i,recipient_name=name,recipient_email=str(raw.get("email",""))[:320] or None,certificate_title=str(raw.get("certificate_title",""))[:150] or None,status="FAILED",error_message=f"Validation failed: {err}"); invalid+=1
        db.add(c)
    job.failed_count=invalid; db.commit()
    if valid:bg.add_task(process_job,job.id)
    else: job.status="FAILED"; db.commit()
    return {"job_id":job.id,"status":job.status,"total_count":len(payload.recipients),"valid_count":valid,"invalid_count":invalid}
@router.get("/{job_id}",response_model=JobResponse)
def get_job(job_id:str,db:Session=Depends(get_db)):
    job=db.get(GenerationJob,job_id)
    if not job:raise HTTPException(404,"Generation job not found")
    db.refresh(job); return serialize(job)
@router.get("/{job_id}/certificates")
def list_certificates(job_id:str,db:Session=Depends(get_db)):
    job=db.get(GenerationJob,job_id)
    if not job:raise HTTPException(404,"Generation job not found")
    return serialize(job)["certificates"]
