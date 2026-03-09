import uuid
from datetime import datetime
from typing import Optional

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.enums import ProjectStatus, TagLevel
from app.models.project import Project, ProjectBaseline
from app.models.tag import Tag
from app.schemas.project import DelayResponse, ProjectCreate, ProjectUpdate


def list_projects(
    db: Session,
    team_id: Optional[uuid.UUID] = None,
    business_objective_id: Optional[uuid.UUID] = None,
    status: Optional[ProjectStatus] = None,
    tag_id: Optional[uuid.UUID] = None,
    skip: int = 0,
    limit: int = 50,
) -> tuple[list[Project], int]:
    query = db.query(Project)
    if team_id:
        query = query.filter(Project.team_id == team_id)
    if business_objective_id:
        query = query.filter(Project.business_objective_id == business_objective_id)
    if status:
        query = query.filter(Project.status == status)
    if tag_id:
        query = query.filter(Project.tags.any(Tag.id == tag_id))
    total = query.count()
    items = query.offset(skip).limit(limit).all()
    return items, total


def get_project(db: Session, project_id: uuid.UUID) -> Project:
    project = db.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


def create_project(db: Session, data: ProjectCreate) -> Project:
    if data.end_date <= data.start_date:
        raise HTTPException(status_code=400, detail="end_date must be after start_date")
    project = Project(**data.model_dump())
    db.add(project)
    db.commit()
    db.refresh(project)
    return project


def update_project(db: Session, project_id: uuid.UUID, data: ProjectUpdate) -> Project:
    project = get_project(db, project_id)
    updates = data.model_dump(exclude_unset=True)

    # Check if status is transitioning to COMMITTED — auto-create baseline
    new_status = updates.get("status")
    if new_status == ProjectStatus.COMMITTED and project.status == ProjectStatus.DRAFT:
        _create_baseline(db, project)

    for field, value in updates.items():
        setattr(project, field, value)

    # Validate dates
    if project.end_date <= project.start_date:
        raise HTTPException(status_code=400, detail="end_date must be after start_date")

    db.commit()
    db.refresh(project)
    return project


def delete_project(db: Session, project_id: uuid.UUID) -> None:
    project = get_project(db, project_id)
    db.delete(project)
    db.commit()


def get_delay(db: Session, project_id: uuid.UUID) -> Optional[DelayResponse]:
    project = get_project(db, project_id)
    if not project.baseline:
        return None
    baseline = project.baseline
    return DelayResponse(
        baseline_start_date=baseline.baseline_start_date,
        baseline_end_date=baseline.baseline_end_date,
        current_start_date=project.start_date,
        current_end_date=project.end_date,
        start_delay_days=(project.start_date - baseline.baseline_start_date).days,
        end_delay_days=(project.end_date - baseline.baseline_end_date).days,
    )


def create_baseline(db: Session, project_id: uuid.UUID) -> ProjectBaseline:
    project = get_project(db, project_id)
    return _create_baseline(db, project)


def _create_baseline(db: Session, project: Project) -> ProjectBaseline:
    # Remove existing baseline if any (re-baseline)
    if project.baseline:
        db.delete(project.baseline)
        db.flush()
    baseline = ProjectBaseline(
        project_id=project.id,
        baseline_start_date=project.start_date,
        baseline_end_date=project.end_date,
        baselined_at=datetime.utcnow(),
    )
    db.add(baseline)
    db.commit()
    db.refresh(baseline)
    return baseline


def add_tag(db: Session, project_id: uuid.UUID, tag_id: uuid.UUID) -> Project:
    project = get_project(db, project_id)
    tag = db.get(Tag, tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    if tag in project.tags:
        raise HTTPException(status_code=409, detail="Tag already linked to project")
    project.tags.append(tag)
    db.commit()
    db.refresh(project)
    return project


def remove_tag(db: Session, project_id: uuid.UUID, tag_id: uuid.UUID) -> Project:
    project = get_project(db, project_id)
    tag = db.get(Tag, tag_id)
    if not tag or tag not in project.tags:
        raise HTTPException(status_code=404, detail="Tag not linked to project")
    project.tags.remove(tag)
    db.commit()
    db.refresh(project)
    return project
