import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from main import app
from database import get_session, Base
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest_asyncio.fixture
async def client():
    engine = create_async_engine(DATABASE_URL, echo=False)

    AsyncSessionLocal = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )

    async def enable_foreign_keys():
        async with engine.connect() as conn:
            await conn.execute(text("PRAGMA foreign_keys = ON"))
            await conn.commit()

    async def get_mocked_session() -> AsyncSession:
        await enable_foreign_keys()
        async with AsyncSessionLocal() as session:
            yield session

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    app.dependency_overrides[get_session] = get_mocked_session
    return TestClient(app)


@pytest_asyncio.fixture
async def project_id(client):
    response = client.post(
        "/api/v1/projects/create", json={"title": "Test Project", "notes": "Test Notes"}
    )
    assert response.status_code == 200
    return response.json()["id"]


@pytest_asyncio.fixture
async def todo_data(client, project_id):
    response = client.post(
        "/api/v1/todos/project/{}/".format(project_id), json={"data": "Test Todo"}
    )
    assert response.status_code == 200
    return response.json()


def test_create_todo(client, project_id):
    response = client.post(
        f"/api/v1/todos/project/{project_id}/", json={"data": "New Todo"}
    )
    assert response.status_code == 200
    assert response.json()["data"] == "New Todo"
    assert response.json()["project_id"] == project_id


def test_get_todos(client, project_id):
    client.post(f"/api/v1/todos/project/{project_id}/", json={"data": "Todo 1"})
    client.post(f"/api/v1/todos/project/{project_id}/", json={"data": "Todo 2"})

    response = client.get(f"/api/v1/todos/project/{project_id}/")
    assert response.status_code == 200
    todos = response.json()
    assert len(todos) == 2
    assert todos[0]["data"] == "Todo 1"
    assert todos[1]["data"] == "Todo 2"


def test_update_todo(client, todo_data):
    todo_id = todo_data["id"]
    response = client.patch(
        "/api/v1/todos/",
        json={"id": todo_id, "status": "completed", "data": "Updated Todo"},
    )
    assert response.status_code == 200
    updated_todo = response.json()
    assert updated_todo["status"] == "completed"
    assert updated_todo["data"] == "Updated Todo"


def test_delete_todo(client, todo_data):
    todo_id = todo_data["id"]
    response = client.delete(f"/api/v1/todos/{todo_id}")
    assert response.status_code == 200
    assert response.json() is True


def test_get_todos_empty(client, project_id):
    response = client.get(f"/api/v1/todos/project/{project_id}/")
    assert response.status_code == 200
    assert response.json() == []


def test_create_todo_invalid_project(client):
    response = client.post("/api/v1/todos/project/9999", json={"data": "Invalid Todo"})
    assert response.status_code == 500


def test_get_todos_for_non_existing_project(client):
    response = client.get("/api/v1/todos/project/9999/")
    assert response.status_code == 200
    assert response.json() == []
