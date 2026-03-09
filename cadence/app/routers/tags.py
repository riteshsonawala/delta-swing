import uuid
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.enums import TagLevel
from app.schemas.common import PaginatedResponse
from app.schemas.tag import TagCreate, TagResponse, TagUpdate
from app.services import tag_service

router = APIRouter(prefix="/tags", tags=["tags"])


@router.get("", response_model=PaginatedResponse[TagResponse])
def list_tags(
    level: Optional[TagLevel] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
):
    items, total = tag_service.list_tags(db, level=level, skip=skip, limit=limit)
    return PaginatedResponse(items=items, total=total, skip=skip, limit=limit)


@router.post("", response_model=TagResponse, status_code=201)
def create_tag(data: TagCreate, db: Session = Depends(get_db)):
    return tag_service.create_tag(db, data)


@router.get("/{tag_id}", response_model=TagResponse)
def get_tag(tag_id: uuid.UUID, db: Session = Depends(get_db)):
    return tag_service.get_tag(db, tag_id)


@router.patch("/{tag_id}", response_model=TagResponse)
def update_tag(tag_id: uuid.UUID, data: TagUpdate, db: Session = Depends(get_db)):
    return tag_service.update_tag(db, tag_id, data)


@router.delete("/{tag_id}", status_code=204)
def delete_tag(tag_id: uuid.UUID, db: Session = Depends(get_db)):
    tag_service.delete_tag(db, tag_id)
