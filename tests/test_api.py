def payload():
    return {"event_name":"Python Backend Development Course","event_date":"2026-10-08","issuer_name":"ABC Organization","recipients":[{"name":"Onkar Sumbe","email":"onkar@example.com","certificate_title":"Certificate of Completion"},{"name":"Rahul Sharma","email":"rahul@example.com","certificate_title":"Certificate of Completion"}]}
def test_health(client): assert client.get("/health").json()=={"status":"ok"}
def test_create_job(client):
    r=client.post("/api/v1/jobs",json=payload()); assert r.status_code==202; assert r.json()["valid_count"]==2
def test_validation(client):
    p=payload(); p["event_name"]="x"; assert client.post("/api/v1/jobs",json=p).status_code==422
def test_generation_progress_and_download(client):
    j=client.post("/api/v1/jobs",json=payload()).json()["job_id"]; data=client.get(f"/api/v1/jobs/{j}").json()
    assert data["status"]=="COMPLETED" and data["successful_count"]==2 and data["progress_percent"]==100
    cid=data["certificates"][0]["id"]; d=client.get(f"/api/v1/certificates/{cid}/download"); assert d.status_code==200 and d.content.startswith(b"%PDF")
def test_individual_failure(client,monkeypatch):
    import app.workers.certificate_worker as w
    original=w.generate_certificate
    def fail(path,*args,**kwargs):
        if args[1]=="Rahul Sharma": raise RuntimeError("simulated failure")
        return original(path,*args,**kwargs)
    monkeypatch.setattr(w,"generate_certificate",fail)
    j=client.post("/api/v1/jobs",json=payload()).json()["job_id"]; d=client.get(f"/api/v1/jobs/{j}").json()
    assert d["status"]=="COMPLETED_WITH_ERRORS" and d["successful_count"]==1 and d["failed_count"]==1
def test_invalid_recipient_continues(client):
    p=payload(); p["recipients"][1]["email"]="bad"; r=client.post("/api/v1/jobs",json=p); j=r.json()["job_id"]; d=client.get(f"/api/v1/jobs/{j}").json()
    assert r.json()["invalid_count"]==1 and d["successful_count"]==1 and d["failed_count"]==1
