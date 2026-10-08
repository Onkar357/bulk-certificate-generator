from pathlib import Path
from fastapi import APIRouter,Depends,HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Certificate
router=APIRouter(prefix="/certificates",tags=["certificates"])
@router.get("/{certificate_id}")
def get_certificate(certificate_id:str,db:Session=Depends(get_db)):
    c=db.get(Certificate,certificate_id)
    if not c:raise HTTPException(404,"Certificate not found")
    return {"id":c.id,"job_id":c.job_id,"recipient_name":c.recipient_name,"recipient_email":c.recipient_email,"certificate_title":c.certificate_title,"status":c.status,"error_message":c.error_message,"download_url":f"/api/v1/certificates/{c.id}/download" if c.status=="SUCCESS" else None}
@router.get("/{certificate_id}/download")
def download(certificate_id:str,db:Session=Depends(get_db)):
    c=db.get(Certificate,certificate_id)
    if not c:raise HTTPException(404,"Certificate not found")
    if c.status!="SUCCESS" or not c.file_path:raise HTTPException(409,"Certificate is not available")
    p=Path(c.file_path)
    if not p.is_file():raise HTTPException(404,"Generated certificate file not found")
    return FileResponse(p,media_type="application/pdf",filename=f"certificate-{c.id}.pdf")
