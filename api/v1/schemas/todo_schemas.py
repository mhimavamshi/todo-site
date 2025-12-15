from pydantic import BaseModel, ConfigDict
from datetime import datetime
from database import TodoStatus

class TodoRequest(BaseModel):
    data: str 

class TodoResponse(BaseModel):
    id: int
    project_id: int
    data: str
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_orm=True)

class UpdateTodoRequest(BaseModel):
    id: int 
    status: TodoStatus = None 
    data: str = None