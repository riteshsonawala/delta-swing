import uuid
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.common import PaginatedResponse
from app.schemas.team_member import TeamMemberCreate, TeamMemberResponse, TeamMemberUpdate
from app.services import team_member_service

router = APIRouter(prefix="/team-members", tags=["team-members"])


@router.get("", response_model=PaginatedResponse[TeamMemberResponse])
def list_team_members(
    team_id: Optional[uuid.UUID] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
):
    items, total = team_member_service.list_team_members(db, team_id=team_id, skip=skip, limit=limit)
    return PaginatedResponse(items=items, total=total, skip=skip, limit=limit)


@router.post("", response_model=TeamMemberResponse, status_code=201)
def create_team_member(data: TeamMemberCreate, db: Session = Depends(get_db)):
    return team_member_service.create_team_member(db, data)


@router.get("/{member_id}", response_model=TeamMemberResponse)
def get_team_member(member_id: uuid.UUID, db: Session = Depends(get_db)):
    return team_member_service.get_team_member(db, member_id)


@router.patch("/{member_id}", response_model=TeamMemberResponse)
def update_team_member(
    member_id: uuid.UUID, data: TeamMemberUpdate, db: Session = Depends(get_db)
):
    return team_member_service.update_team_member(db, member_id, data)


@router.delete("/{member_id}", status_code=204)
def delete_team_member(member_id: uuid.UUID, db: Session = Depends(get_db)):
    team_member_service.delete_team_member(db, member_id)
