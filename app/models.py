from datetime import date,datetime,timezone
from uuid import uuid4
from sqlalchemy import Date,DateTime,ForeignKey,Integer,String,Text
from sqlalchemy.orm import Mapped,mapped_column,relationship
from app.database import Base
class GenerationJob(Base):
    __tablename__="generation_jobs"
    id:Mapped[str]=mapped_column(String(36),primary_key=True,default=lambda:str(uuid4()))
    event_name:Mapped[str]=mapped_column(String(200),nullable=False)
    event_date:Mapped[date]=mapped_column(Date,nullable=False)
    issuer_name:Mapped[str]=mapped_column(String(200),nullable=False)
    status:Mapped[str]=mapped_column(String(32),default="QUEUED",nullable=False)
    total_count:Mapped[int]=mapped_column(Integer,nullable=False)
    successful_count:Mapped[int]=mapped_column(Integer,default=0,nullable=False)
    failed_count:Mapped[int]=mapped_column(Integer,default=0,nullable=False)
    created_at:Mapped[datetime]=mapped_column(DateTime,default=lambda:datetime.now(timezone.utc),nullable=False)
    completed_at:Mapped[datetime|None]=mapped_column(DateTime,nullable=True)
    certificates:Mapped[list["Certificate"]]=relationship(back_populates="job",cascade="all,delete-orphan")
class Certificate(Base):
    __tablename__="certificates"
    id:Mapped[str]=mapped_column(String(36),primary_key=True,default=lambda:str(uuid4()))
    job_id:Mapped[str]=mapped_column(ForeignKey("generation_jobs.id"),index=True)
    recipient_index:Mapped[int]=mapped_column(Integer)
    recipient_name:Mapped[str]=mapped_column(String(100))
    recipient_email:Mapped[str|None]=mapped_column(String(320),nullable=True)
    certificate_title:Mapped[str|None]=mapped_column(String(150),nullable=True)
    status:Mapped[str]=mapped_column(String(32),default="PENDING")
    file_path:Mapped[str|None]=mapped_column(String(1000),nullable=True)
    error_message:Mapped[str|None]=mapped_column(Text,nullable=True)
    created_at:Mapped[datetime]=mapped_column(DateTime,default=lambda:datetime.now(timezone.utc))
    completed_at:Mapped[datetime|None]=mapped_column(DateTime,nullable=True)
    job:Mapped[GenerationJob]=relationship(back_populates="certificates")
