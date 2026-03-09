import uuid
from typing import Optional

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.enums import ReferenceType
from app.models.external_reference import ExternalReference
from app.schemas.external_reference import ExternalReferenceCreate, ExternalReferenceUpdate


def list_external_references(
    db: Session,
    project_id: Optional[uuid.UUID] = None,
    reference_type: Optional[ReferenceType] = None,
    external_id: Optional[str] = None,
    skip: int = 0,
    limit: int = 50,
) -> tuple[list[ExternalReference], int]:
    query = db.query(ExternalReference)
    if project_id:
        query = query.filter(ExternalReference.project_id == project_id)
    if reference_type:
        query = query.filter(ExternalReference.reference_type == reference_type)
    if external_id:
        query = query.filter(ExternalReference.external_id == external_id)
    total = query.count()
    items = query.offset(skip).limit(limit).all()
    return items, total


def get_external_reference(db: Session, ref_id: uuid.UUID) -> ExternalReference:
    ref = db.get(ExternalReference, ref_id)
    if not ref:
        raise HTTPException(status_code=404, detail="External reference not found")
    return ref


def create_external_reference(
    db: Session, project_id: uuid.UUID, data: ExternalReferenceCreate
) -> ExternalReference:
    ref = ExternalReference(project_id=project_id, **data.model_dump())
    db.add(ref)
    db.commit()
    db.refresh(ref)
    return ref


def update_external_reference(
    db: Session, ref_id: uuid.UUID, data: ExternalReferenceUpdate
) -> ExternalReference:
    ref = get_external_reference(db, ref_id)
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(ref, field, value)
    db.commit()
    db.refresh(ref)
    return ref


def delete_external_reference(db: Session, ref_id: uuid.UUID) -> None:
    ref = get_external_reference(db, ref_id)
    db.delete(ref)
    db.commit()
