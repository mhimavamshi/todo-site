from sqlalchemy import Column, Integer, String, Text, Enum, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from datetime import datetime

from database import Base
from database import TodoStatus

class Project(Base):
    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    notes = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)

    todos = relationship('Todo', back_populates='project')

class Todo(Base):
    __tablename__ = 'todos'

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey('projects.id', ondelete="CASCADE"))
    data = Column(Text, nullable=False)
    status = Column(Enum(TodoStatus), default=TodoStatus.in_progress)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)

    project = relationship('Project', back_populates='todos')