import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from main import app
from database import get_session, Base


from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker


DATABASE_URL = "sqlite+aiosqlite:///:memory:"

@pytest_asyncio.fixture
async def client():
    engine = create_async_engine(DATABASE_URL, echo=False)

    AsyncSessionLocal = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )

    async def get_mocked_session() -> AsyncSession:
        async with AsyncSessionLocal() as session:
            yield session

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    app.dependency_overrides[get_session] = get_mocked_session
    return TestClient(app)

@pytest.fixture
def project_id(client):
    response = client.post("/api/v1/projects/create", json={"title": "Test Title", "notes": "Test Notes"})
    assert response.status_code == 200
    return response.json()["id"]

def test_get_project(client, project_id):
    response = client.get(f"/api/v1/projects/{project_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "Test Title"
    assert response.json()["notes"] == "Test Notes"

def test_update_project(client, project_id):
    response = client.patch(
        "/api/v1/projects/update", json={"id": project_id, "title": "Updated Title", "notes": "Updated Notes"}
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Title"
    assert response.json()["notes"] == "Updated Notes"

def test_get_all_projects(client, project_id):
    response = client.get("/api/v1/projects")
    assert response.status_code == 200
    assert len(response.json()) > 0  
    assert any(project["id"] == project_id for project in response.json())

def test_get_project_by_id(client, project_id):
    response = client.get(f"/api/v1/projects/{project_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "Test Title"
    assert response.json()["notes"] == "Test Notes"

def test_delete_project(client, project_id):
    response = client.delete(f"/api/v1/projects/{project_id}")
    assert response.status_code == 200
    assert response.json()

# maybe, also check in DB if actions were right? 