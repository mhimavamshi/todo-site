from api.v1.routers import project_router, todo_router

from fastapi import APIRouter

router = APIRouter(prefix="/api/v1")

router.include_router(project_router.router, prefix="/projects", tags=["projects"])
router.include_router(todo_router.router, prefix="/todos", tags=["todos"])