from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, exc
from utils import logger
from database import Todo


async def create_todo(project_id, data, db_session: AsyncSession):
    try:
        todo = Todo(project_id=project_id, data=data)
        db_session.add(todo)
        await db_session.commit()
        await db_session.refresh(todo)
        return todo
    except exc.IntegrityError:
        raise ValueError("Invalid request")

async def get_todos(project_id, db_session: AsyncSession):
    try:
        query = select(Todo).where(Todo.project_id == project_id)
        result = await db_session.scalars(query)
        todos = result.all()

        if not todos:
            logger.info(f"Todos requested for invalid project {project_id}")
        
        return todos
    except exc.IntegrityError:
        raise ValueError("Invalid request")


async def update_todo(id, status, data, db_session: AsyncSession):
    query = select(Todo).where(Todo.id == id)
    todo = await db_session.scalar(query)

    if not todo:
        raise ValueError(f"Todo {id} not found")

    if status:
        todo.status = status
    if data:
        todo.data = data

    await db_session.commit()
    await db_session.refresh(todo)

    return todo


async def delete_todo(id, db_session: AsyncSession):
    query = select(Todo).where(Todo.id == id)
    todo = await db_session.scalar(query)

    if not todo:
        raise ValueError(f"Todo {id} not found")

    await db_session.delete(todo)
    await db_session.commit()

    return True
