import uuid
from typing import Optional

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.enums import TagLevel
from app.models.tag import Tag
from app.schemas.tag import TagCreate, TagUpdate


def list_tags(db: Session, level: Optional[TagLevel] = None, skip: int = 0, limit: int = 50) -> tuple[list[Tag], int]:
    query = db.query(Tag)
    if level:
        query = query.filter(Tag.level == level)
    total = query.count()
    items = query.offset(skip).limit(limit).all()
    return items, total


def get_tag(db: Session, tag_id: uuid.UUID) -> Tag:
    tag = db.get(Tag, tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    return tag


def create_tag(db: Session, data: TagCreate) -> Tag:
    existing = db.query(Tag).filter(Tag.level == data.level, Tag.value == data.value).first()
    if existing:
        raise HTTPException(status_code=409, detail="Tag with this level and value already exists")
    tag = Tag(**data.model_dump())
    db.add(tag)
    db.commit()
    db.refresh(tag)
    return tag


def update_tag(db: Session, tag_id: uuid.UUID, data: TagUpdate) -> Tag:
    tag = get_tag(db, tag_id)
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(tag, field, value)
    db.commit()
    db.refresh(tag)
    return tag


def delete_tag(db: Session, tag_id: uuid.UUID) -> None:
    tag = get_tag(db, tag_id)
    db.delete(tag)
    db.commit()
