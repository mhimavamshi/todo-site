from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_session
from services.project_service import get_projects, get_project
from services.todo_service import get_todos
from services.templates_service import get_project_stats, get_todo_stats

router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/projects", response_class=HTMLResponse)
async def projects(request: Request, db_session: AsyncSession = Depends(get_session)):
    projects = await get_projects(db_session)
    return templates.TemplateResponse(
        request=request, name="projects.html", context={"projects": list(projects)}
    )


@router.get("/project/{id}", response_class=HTMLResponse)
async def project(
    request: Request, id, db_session: AsyncSession = Depends(get_session)
):
    project = await get_project(id, db_session)
    todos = await get_todos(id, db_session)
    return templates.TemplateResponse(
        request=request,
        name="project.html",
        context={"project": project, "todos": list(todos)},
    )


@router.get("/stats", response_class=HTMLResponse)
async def stats(request: Request, db_session: AsyncSession = Depends(get_session)):
    project_stats = await get_project_stats(db_session)
    todo_stats = await get_todo_stats(db_session)
    return templates.TemplateResponse(
        request=request,
        name="stats.html",
        context={"project_stats": project_stats, "todo_stats": todo_stats},
    )
