import uuid

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.business_objective import BusinessObjective
from app.schemas.business_objective import BusinessObjectiveCreate, BusinessObjectiveUpdate


def list_business_objectives(db: Session, skip: int = 0, limit: int = 50) -> tuple[list[BusinessObjective], int]:
    total = db.query(BusinessObjective).count()
    items = db.query(BusinessObjective).offset(skip).limit(limit).all()
    return items, total


def get_business_objective(db: Session, bo_id: uuid.UUID) -> BusinessObjective:
    bo = db.get(BusinessObjective, bo_id)
    if not bo:
        raise HTTPException(status_code=404, detail="Business objective not found")
    return bo


def create_business_objective(db: Session, data: BusinessObjectiveCreate) -> BusinessObjective:
    bo = BusinessObjective(**data.model_dump())
    db.add(bo)
    db.commit()
    db.refresh(bo)
    return bo


def update_business_objective(db: Session, bo_id: uuid.UUID, data: BusinessObjectiveUpdate) -> BusinessObjective:
    bo = get_business_objective(db, bo_id)
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(bo, field, value)
    db.commit()
    db.refresh(bo)
    return bo


def delete_business_objective(db: Session, bo_id: uuid.UUID) -> None:
    bo = get_business_objective(db, bo_id)
    db.delete(bo)
    db.commit()
