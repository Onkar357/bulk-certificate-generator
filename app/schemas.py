from datetime import date,datetime
from typing import Any
from pydantic import BaseModel,EmailStr,Field,field_validator
from app.config import MAX_RECIPIENTS
class CreateJobRequest(BaseModel):
    event_name:str=Field(min_length=2,max_length=200)
    event_date:date
    issuer_name:str=Field(min_length=2,max_length=200)
    recipients:list[dict[str,Any]]=Field(min_length=1,max_length=MAX_RECIPIENTS)
    @field_validator("event_name","issuer_name")
    @classmethod
    def clean(cls,v): return v.strip()
class RecipientInput(BaseModel):
    name:str=Field(min_length=2,max_length=100)
    email:EmailStr
    certificate_title:str=Field(min_length=2,max_length=150)
    @field_validator("name","certificate_title")
    @classmethod
    def clean(cls,v):
        v=v.strip()
        if not v: raise ValueError("must not be blank")
        return v
class JobCreatedResponse(BaseModel):
    job_id:str
    status:str
    total_count:int
    valid_count:int
    invalid_count:int
class CertificateResponse(BaseModel):
    id:str; job_id:str; recipient_index:int; recipient_name:str
    recipient_email:str|None; certificate_title:str|None; status:str
    error_message:str|None; download_url:str|None
    created_at:datetime; completed_at:datetime|None
class JobResponse(BaseModel):
    id:str; event_name:str; event_date:date; issuer_name:str; status:str
    total_count:int; successful_count:int; failed_count:int
    processed_count:int; pending_count:int; progress_percent:float
    created_at:datetime; completed_at:datetime|None
    certificates:list[CertificateResponse]
