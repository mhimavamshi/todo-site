from sqlalchemy import Column, Integer, String, Text, Enum, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

import enum

from database import Base

class TodoStatus(enum.Enum):
    in_progress = "in-progress"
    completed = "completed"
    deleted = "deleted"


class TimestampMixin:
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now()
    )
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now()
    )


class Project(TimestampMixin, Base):
    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    notes = Column(Text, nullable=True)
    
    todos = relationship('Todo', back_populates='project')

class Todo(TimestampMixin, Base):
    __tablename__ = 'todos'

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey('projects.id', ondelete="CASCADE"))
    data = Column(Text, nullable=False)
    status = Column(Enum(TodoStatus), default=TodoStatus.in_progress)

    project = relationship('Project', back_populates='todos')