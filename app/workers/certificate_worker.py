from datetime import date,datetime,timezone
from pathlib import Path
from sqlalchemy import select
from app.config import GENERATED_DIR
from app.database import SessionLocal
from app.models import Certificate,GenerationJob
from app.services.certificate_generator import generate_certificate
def process_job(job_id:str):
    db=SessionLocal()
    try:
        job=db.get(GenerationJob,job_id)
        if not job:return
        job.status="PROCESSING"; db.commit()
        rows=list(db.scalars(select(Certificate).where(Certificate.job_id==job_id,Certificate.status=="PENDING").order_by(Certificate.recipient_index)).all())
        for c in rows:
            c.status="PROCESSING"; db.commit()
            try:
                path=Path(GENERATED_DIR)/job_id/f"{c.id}.pdf"
                generate_certificate(path,c.id,c.recipient_name,c.certificate_title or "Certificate of Achievement",job.event_name,job.event_date.isoformat(),job.issuer_name,date.today().isoformat())
                c.file_path=str(path); c.status="SUCCESS"; c.error_message=None
            except Exception as exc:
                c.status="FAILED"; c.error_message=f"{type(exc).__name__}: {exc}"
            c.completed_at=datetime.now(timezone.utc); db.commit()
        success=sum(c.status=="SUCCESS" for c in job.certificates)
        failed=sum(c.status=="FAILED" for c in job.certificates)
        job.successful_count=success; job.failed_count=failed
        job.status="COMPLETED" if failed==0 else ("FAILED" if success==0 else "COMPLETED_WITH_ERRORS")
        job.completed_at=datetime.now(timezone.utc); db.commit()
    finally: db.close()
