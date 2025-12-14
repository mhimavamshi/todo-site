from pydantic import BaseModel, ConfigDict
from datetime import datetime


class ProjectResponse(BaseModel):
    id: int
    title: str
    notes: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_orm=True)


class ProjectRequest(BaseModel):
    title: str
    notes: str


class UpdateProjectRequest(BaseModel):
    id: int
    title: str = None
    notes: str = None
