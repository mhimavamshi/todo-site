from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database import Project


async def create_project(title, notes, db_session: AsyncSession):
    project = Project(title=title, notes=notes)
    db_session.add(project)
    await db_session.commit()
    await db_session.refresh(project)
    return project


async def update_project(id, title, notes, db_session: AsyncSession):
    query = select(Project).where(Project.id == id)
    project = await db_session.scalar(query)

    if not project:
        raise ValueError(f"Project {id} not found")

    if title:
        project.title = title
    if notes:
        project.notes = notes

    await db_session.commit()
    await db_session.refresh(project)
    return project


async def get_projects(db_session: AsyncSession):
    query = select(Project)
    projects = await db_session.scalars(query)
    return projects.all()


async def get_project(id, db_session: AsyncSession):
    query = select(Project).where(Project.id == id)
    project = await db_session.scalar(query)

    if not project:
        raise ValueError(f"Project {id} not found")

    return project


async def delete_project(id, db_session: AsyncSession):
    query = select(Project).where(Project.id == id)
    project = await db_session.scalar(query)

    if not project:
        raise ValueError(f"Project {id} not found")

    await db_session.delete(project)
    await db_session.commit()

    return True
