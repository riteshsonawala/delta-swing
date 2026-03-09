import uuid
from typing import Optional

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.team import Team
from app.models.team_member import TeamMember
from app.schemas.team import TeamCreate, TeamUpdate


def list_teams(db: Session, is_active: Optional[bool] = None, skip: int = 0, limit: int = 50) -> tuple[list[Team], int]:
    query = db.query(Team)
    if is_active is not None:
        query = query.filter(Team.is_active == is_active)
    total = query.count()
    items = query.offset(skip).limit(limit).all()
    return items, total


def get_team(db: Session, team_id: uuid.UUID) -> Team:
    team = db.get(Team, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return team


def create_team(db: Session, data: TeamCreate) -> Team:
    team = Team(**data.model_dump())
    db.add(team)
    db.commit()
    db.refresh(team)
    return team


def update_team(db: Session, team_id: uuid.UUID, data: TeamUpdate) -> Team:
    team = get_team(db, team_id)
    updates = data.model_dump(exclude_unset=True)

    # When deactivating a team, unassign all members
    if updates.get("is_active") is False and team.is_active:
        db.query(TeamMember).filter(TeamMember.team_id == team_id).update({"team_id": None})

    for field, value in updates.items():
        setattr(team, field, value)
    db.commit()
    db.refresh(team)
    return team


def delete_team(db: Session, team_id: uuid.UUID) -> None:
    team = get_team(db, team_id)
    # Soft delete: deactivate and unassign members
    db.query(TeamMember).filter(TeamMember.team_id == team_id).update({"team_id": None})
    team.is_active = False
    db.commit()
