import uuid
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.enums import ProjectStatus
from app.schemas.common import PaginatedResponse
from app.schemas.external_reference import (
    ExternalReferenceCreate,
    ExternalReferenceResponse,
)
from app.schemas.project import (
    DelayResponse,
    ProjectBaselineResponse,
    ProjectCreate,
    ProjectDetailResponse,
    ProjectResponse,
    ProjectUpdate,
)
from app.schemas.tag import TagResponse
from app.services import external_reference_service, project_service

router = APIRouter(prefix="/projects", tags=["projects"])


@router.get("", response_model=PaginatedResponse[ProjectResponse])
def list_projects(
    team_id: Optional[uuid.UUID] = None,
    business_objective_id: Optional[uuid.UUID] = None,
    status: Optional[ProjectStatus] = None,
    tag_id: Optional[uuid.UUID] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
):
    items, total = project_service.list_projects(
        db,
        team_id=team_id,
        business_objective_id=business_objective_id,
        status=status,
        tag_id=tag_id,
        skip=skip,
        limit=limit,
    )
    return PaginatedResponse(items=items, total=total, skip=skip, limit=limit)


@router.post("", response_model=ProjectResponse, status_code=201)
def create_project(data: ProjectCreate, db: Session = Depends(get_db)):
    return project_service.create_project(db, data)


@router.get("/{project_id}", response_model=ProjectDetailResponse)
def get_project(project_id: uuid.UUID, db: Session = Depends(get_db)):
    project = project_service.get_project(db, project_id)
    delay = project_service.get_delay(db, project_id)
    return ProjectDetailResponse(
        id=project.id,
        name=project.name,
        description=project.description,
        status=project.status,
        start_date=project.start_date,
        end_date=project.end_date,
        team_id=project.team_id,
        business_objective_id=project.business_objective_id,
        created_at=project.created_at,
        updated_at=project.updated_at,
        baseline=project.baseline,
        delay=delay,
        tags=project.tags,
        external_references=project.external_references,
    )


@router.patch("/{project_id}", response_model=ProjectResponse)
def update_project(
    project_id: uuid.UUID, data: ProjectUpdate, db: Session = Depends(get_db)
):
    return project_service.update_project(db, project_id, data)


@router.delete("/{project_id}", status_code=204)
def delete_project(project_id: uuid.UUID, db: Session = Depends(get_db)):
    project_service.delete_project(db, project_id)


# --- Delay ---


@router.get("/{project_id}/delay", response_model=Optional[DelayResponse])
def get_project_delay(project_id: uuid.UUID, db: Session = Depends(get_db)):
    return project_service.get_delay(db, project_id)


@router.post("/{project_id}/baseline", response_model=ProjectBaselineResponse, status_code=201)
def create_baseline(project_id: uuid.UUID, db: Session = Depends(get_db)):
    return project_service.create_baseline(db, project_id)


# --- External References ---


@router.get(
    "/{project_id}/external-references",
    response_model=PaginatedResponse[ExternalReferenceResponse],
)
def list_project_references(
    project_id: uuid.UUID,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
):
    project_service.get_project(db, project_id)
    items, total = external_reference_service.list_external_references(
        db, project_id=project_id, skip=skip, limit=limit
    )
    return PaginatedResponse(items=items, total=total, skip=skip, limit=limit)


@router.post(
    "/{project_id}/external-references",
    response_model=ExternalReferenceResponse,
    status_code=201,
)
def add_project_reference(
    project_id: uuid.UUID,
    data: ExternalReferenceCreate,
    db: Session = Depends(get_db),
):
    project_service.get_project(db, project_id)
    return external_reference_service.create_external_reference(db, project_id, data)


@router.delete("/{project_id}/external-references/{ref_id}", status_code=204)
def remove_project_reference(
    project_id: uuid.UUID, ref_id: uuid.UUID, db: Session = Depends(get_db)
):
    project_service.get_project(db, project_id)
    ref = external_reference_service.get_external_reference(db, ref_id)
    if ref.project_id != project_id:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Reference not found on this project")
    external_reference_service.delete_external_reference(db, ref_id)


# --- Tags ---


@router.get("/{project_id}/tags", response_model=list[TagResponse])
def list_project_tags(project_id: uuid.UUID, db: Session = Depends(get_db)):
    project = project_service.get_project(db, project_id)
    return project.tags


@router.post("/{project_id}/tags/{tag_id}", status_code=204)
def tag_project(project_id: uuid.UUID, tag_id: uuid.UUID, db: Session = Depends(get_db)):
    project_service.add_tag(db, project_id, tag_id)


@router.delete("/{project_id}/tags/{tag_id}", status_code=204)
def untag_project(project_id: uuid.UUID, tag_id: uuid.UUID, db: Session = Depends(get_db)):
    project_service.remove_tag(db, project_id, tag_id)
