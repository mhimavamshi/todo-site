from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException

from database import get_session

from api.v1.schemas.todo_schemas import TodoRequest, TodoResponse, UpdateTodoRequest
from services.todo_service import create_todo, get_todos, update_todo, delete_todo

router = APIRouter()


@router.post("/project/{project_id}", response_model=TodoResponse)
async def create(
    project_id, request: TodoRequest, db_session: AsyncSession = Depends(get_session)
):
    try:
        todo = await create_todo(project_id, request.data, db_session)
        return todo
    except ValueError as e:
        raise HTTPException(500, str(e))


@router.get("/project/{project_id}", response_model=list[TodoResponse])
async def get(project_id, db_session: AsyncSession = Depends(get_session)):
    try:
        todos = await get_todos(project_id, db_session)
        return todos
    except ValueError as e:
        raise HTTPException(500, str(e))


@router.patch("/", response_model=TodoResponse)
async def patch(
    request: UpdateTodoRequest, db_session: AsyncSession = Depends(get_session)
):
    try:
        todo = await update_todo(request.id, request.status, request.data, db_session)
        return todo
    except ValueError as e:
        raise HTTPException(500, str(e))


@router.delete("/{id}")
async def delete(id, db_session: AsyncSession = Depends(get_session)):
    try:
        response = await delete_todo(id, db_session)
        return response
    except ValueError as e:
        raise HTTPException(500, str(e))
