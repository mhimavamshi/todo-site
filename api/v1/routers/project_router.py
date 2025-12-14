from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_session
from api.v1.schemas.project_schemas import (
    ProjectRequest,
    ProjectResponse,
    UpdateProjectRequest,
)
from services.project_service import (
    create_project,
    update_project,
    get_projects,
    get_project,
    delete_project,
)

router = APIRouter()


@router.post("/create", response_model=ProjectResponse)
async def create(
    request: ProjectRequest, db_session: AsyncSession = Depends(get_session)
):
    try:
        project = await create_project(request.title, request.notes, db_session)
        return project
    except ValueError as e:
        raise HTTPException(500, str(e))


@router.patch("/update", response_model=ProjectResponse)
async def update(
    request: UpdateProjectRequest, db_session: AsyncSession = Depends(get_session)
):
    try:
        project = await update_project(
            request.id, request.title, request.notes, db_session
        )
        return project
    except ValueError as e:
        raise HTTPException(500, str(e))


@router.get("/", response_model=list[ProjectResponse])
async def get_all(db_session: AsyncSession = Depends(get_session)):
    try:
        projects = await get_projects(db_session)
        return projects
    except ValueError as e:
        raise HTTPException(500, str(e))


@router.get("/{id}", response_model=ProjectResponse)
async def get(id, db_session: AsyncSession = Depends(get_session)):
    try:
        projects = await get_project(id, db_session)
        return projects
    except ValueError as e:
        raise HTTPException(500, str(e))


@router.delete("/{id}")
async def delete(id, db_session: AsyncSession = Depends(get_session)):
    try:
        response = await delete_project(id, db_session)
        return response
    except ValueError as e:
        raise HTTPException(500, str(e))
