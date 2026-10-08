# Bulk Certificate Generator

FastAPI backend for bulk PDF certificate generation.

## Technology stack
Python 3.12, FastAPI, Pydantic, SQLAlchemy, SQLite relational database, ReportLab, Pytest and Docker.

## Features
One request creates one generation job; recipients are validated independently; certificates are generated in a background task; every recipient has its own status; one failure does not stop the batch; generated PDFs can be downloaded.

## Run
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload

Swagger: http://localhost:8000/docs

## Request
POST /api/v1/jobs
{
  "event_name":"Python Backend Development Course",
  "event_date":"2026-10-08",
  "issuer_name":"ABC Organization",
  "recipients":[
    {"name":"Onkar Sumbe","email":"onkar@example.com","certificate_title":"Certificate of Completion"},
    {"name":"Rahul Sharma","email":"rahul@example.com","certificate_title":"Certificate of Completion"}
  ]
}

## Endpoints
GET /health
POST /api/v1/jobs
GET /api/v1/jobs/{job_id}
GET /api/v1/jobs/{job_id}/certificates
GET /api/v1/certificates/{certificate_id}
GET /api/v1/certificates/{certificate_id}/download

## Design
FastAPI BackgroundTasks is used instead of Celery/Redis to keep the assignment simple. SQLAlchemy with SQLite provides the required relational database; DATABASE_URL can be changed for PostgreSQL. Per-recipient database rows make progress and failures independently visible. The predefined single certificate design is implemented with ReportLab in certificate_generator.py. Local file storage can later be replaced with S3/object storage.

Run tests with pytest -q.
