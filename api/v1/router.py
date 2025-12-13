from routers import project_router, todo_router

from fastapi import APIRouter

router = APIRouter(prefix="/api/v1")

router.include_router(project_router.router)
router.include_router(todo_router.router)