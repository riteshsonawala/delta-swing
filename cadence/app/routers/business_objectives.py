import uuid

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.business_objective import (
    BusinessObjectiveCreate,
    BusinessObjectiveResponse,
    BusinessObjectiveUpdate,
)
from app.schemas.common import PaginatedResponse
from app.schemas.project import ProjectResponse
from app.services import business_objective_service, project_service

router = APIRouter(prefix="/business-objectives", tags=["business-objectives"])


@router.get("", response_model=PaginatedResponse[BusinessObjectiveResponse])
def list_business_objectives(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
):
    items, total = business_objective_service.list_business_objectives(db, skip, limit)
    return PaginatedResponse(items=items, total=total, skip=skip, limit=limit)


@router.post("", response_model=BusinessObjectiveResponse, status_code=201)
def create_business_objective(data: BusinessObjectiveCreate, db: Session = Depends(get_db)):
    return business_objective_service.create_business_objective(db, data)


@router.get("/{bo_id}", response_model=BusinessObjectiveResponse)
def get_business_objective(bo_id: uuid.UUID, db: Session = Depends(get_db)):
    return business_objective_service.get_business_objective(db, bo_id)


@router.patch("/{bo_id}", response_model=BusinessObjectiveResponse)
def update_business_objective(
    bo_id: uuid.UUID, data: BusinessObjectiveUpdate, db: Session = Depends(get_db)
):
    return business_objective_service.update_business_objective(db, bo_id, data)


@router.delete("/{bo_id}", status_code=204)
def delete_business_objective(bo_id: uuid.UUID, db: Session = Depends(get_db)):
    business_objective_service.delete_business_objective(db, bo_id)


@router.get("/{bo_id}/projects", response_model=PaginatedResponse[ProjectResponse])
def list_projects_for_bo(
    bo_id: uuid.UUID,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
):
    # Verify BO exists
    business_objective_service.get_business_objective(db, bo_id)
    items, total = project_service.list_projects(db, business_objective_id=bo_id, skip=skip, limit=limit)
    return PaginatedResponse(items=items, total=total, skip=skip, limit=limit)
