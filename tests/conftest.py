import pytest
from fastapi.testclient import TestClient
@pytest.fixture
def client(tmp_path,monkeypatch):
    monkeypatch.setenv("DATABASE_URL",f"sqlite:///{tmp_path/'test.db'}")
    monkeypatch.setenv("GENERATED_DIR",str(tmp_path/"generated"))
    import importlib,app.config,app.database,app.main
    importlib.reload(app.config); importlib.reload(app.database); importlib.reload(app.main)
    app.database.Base.metadata.drop_all(bind=app.database.engine); app.database.Base.metadata.create_all(bind=app.database.engine)
    with TestClient(app.main.app) as c: yield c
