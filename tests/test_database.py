import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, selectinload
from database import Base, Project, Todo, TodoStatus
from sqlalchemy.future import select

SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)

AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


@pytest_asyncio.fixture(scope="module")
async def session():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.mark.asyncio
async def test_create_project(session):
    new_project = Project(title="Test Project", notes="Test Notes")
    session.add(new_project)
    await session.commit()

    await session.refresh(new_project)

    assert new_project.id is not None
    assert new_project.title == "Test Project"
    assert new_project.notes == "Test Notes"
    assert new_project.created_at is not None


@pytest.mark.asyncio
async def test_create_todo_for_project(session):
    new_project = Project(title="Test Project", notes="Test Notes")
    session.add(new_project)
    await session.commit()
    await session.refresh(new_project)

    new_todo = Todo(project_id=new_project.id, data="Test Todo")
    session.add(new_todo)
    await session.commit()
    await session.refresh(new_todo)

    assert new_todo.id is not None
    assert new_todo.project_id == new_project.id
    assert new_todo.data == "Test Todo"
    assert new_todo.status == TodoStatus.in_progress
    assert new_todo.created_at is not None


@pytest.mark.asyncio
async def test_project_has_todos(session):
    new_project = Project(title="Test Project", notes="Test Notes")
    session.add(new_project)
    await session.commit()
    await session.refresh(new_project)

    new_todo1 = Todo(project_id=new_project.id, data="Test Todo 1")
    new_todo2 = Todo(
        project_id=new_project.id, data="Test Todo 2", status=TodoStatus.completed
    )
    session.add(new_todo1)
    session.add(new_todo2)
    await session.commit()

    result = await session.execute(
        select(Project)
        .filter(Project.id == new_project.id)
        .options(selectinload(Project.todos))
    )
    project = result.scalars().first()

    assert len(project.todos) == 2
    assert project.todos[0].data == "Test Todo 1"
    assert project.todos[1].data == "Test Todo 2"


@pytest.mark.asyncio
async def test_update_todo_status(session):
    new_project = Project(title="Test Project", notes="Test Notes")
    session.add(new_project)
    await session.commit()
    await session.refresh(new_project)

    new_todo = Todo(
        project_id=new_project.id, data="Test Todo", status=TodoStatus.in_progress
    )
    session.add(new_todo)
    await session.commit()
    await session.refresh(new_todo)

    new_todo.status = TodoStatus.completed
    await session.commit()
    await session.refresh(new_todo)

    assert new_todo.status == TodoStatus.completed
