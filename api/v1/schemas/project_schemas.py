from pydantic import BaseModel
from datetime import datetime


class ProjectResponse(BaseModel):
    id: int
    title: str
    notes: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_orm = True


class ProjectRequest(BaseModel):
    title: str
    notes: str


class UpdateProjectRequest(BaseModel):
    id: int
    title: str = None
    notes: str = None
