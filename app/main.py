from fastapi import FastAPI
from app.database import Base,engine
from app.routes.jobs import router as jobs_router
from app.routes.certificates import router as certificates_router
Base.metadata.create_all(bind=engine)
app=FastAPI(title="Bulk Certificate Generator",version="1.0.0")
app.include_router(jobs_router,prefix="/api/v1")
app.include_router(certificates_router,prefix="/api/v1")
@app.get("/health")
def health(): return {"status":"ok"}
