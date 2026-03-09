import uuid
from typing import Optional

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.team_member import TeamMember
from app.schemas.team_member import TeamMemberCreate, TeamMemberUpdate


def list_team_members(db: Session, team_id: Optional[uuid.UUID] = None, skip: int = 0, limit: int = 50) -> tuple[list[TeamMember], int]:
    query = db.query(TeamMember)
    if team_id:
        query = query.filter(TeamMember.team_id == team_id)
    total = query.count()
    items = query.offset(skip).limit(limit).all()
    return items, total


def get_team_member(db: Session, member_id: uuid.UUID) -> TeamMember:
    member = db.get(TeamMember, member_id)
    if not member:
        raise HTTPException(status_code=404, detail="Team member not found")
    return member


def create_team_member(db: Session, data: TeamMemberCreate) -> TeamMember:
    existing = db.query(TeamMember).filter(TeamMember.email == data.email).first()
    if existing:
        raise HTTPException(status_code=409, detail="Team member with this email already exists")
    member = TeamMember(**data.model_dump())
    db.add(member)
    db.commit()
    db.refresh(member)
    return member


def update_team_member(db: Session, member_id: uuid.UUID, data: TeamMemberUpdate) -> TeamMember:
    member = get_team_member(db, member_id)
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(member, field, value)
    db.commit()
    db.refresh(member)
    return member


def delete_team_member(db: Session, member_id: uuid.UUID) -> None:
    member = get_team_member(db, member_id)
    db.delete(member)
    db.commit()
