import uuid
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.enums import ReferenceType
from app.schemas.common import PaginatedResponse
from app.schemas.external_reference import ExternalReferenceResponse, ExternalReferenceUpdate
from app.services import external_reference_service

router = APIRouter(prefix="/external-references", tags=["external-references"])


@router.get("", response_model=PaginatedResponse[ExternalReferenceResponse])
def list_external_references(
    reference_type: Optional[ReferenceType] = None,
    external_id: Optional[str] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
):
    items, total = external_reference_service.list_external_references(
        db, reference_type=reference_type, external_id=external_id, skip=skip, limit=limit
    )
    return PaginatedResponse(items=items, total=total, skip=skip, limit=limit)


@router.get("/{ref_id}", response_model=ExternalReferenceResponse)
def get_external_reference(ref_id: uuid.UUID, db: Session = Depends(get_db)):
    return external_reference_service.get_external_reference(db, ref_id)


@router.patch("/{ref_id}", response_model=ExternalReferenceResponse)
def update_external_reference(
    ref_id: uuid.UUID, data: ExternalReferenceUpdate, db: Session = Depends(get_db)
):
    return external_reference_service.update_external_reference(db, ref_id, data)
