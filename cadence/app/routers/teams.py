import uuid
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.common import PaginatedResponse
from app.schemas.project import ProjectResponse
from app.schemas.team import TeamCreate, TeamResponse, TeamUpdate
from app.schemas.team_member import TeamMemberResponse
from app.services import project_service, team_member_service, team_service

router = APIRouter(prefix="/teams", tags=["teams"])


@router.get("", response_model=PaginatedResponse[TeamResponse])
def list_teams(
    is_active: Optional[bool] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
):
    items, total = team_service.list_teams(db, is_active=is_active, skip=skip, limit=limit)
    return PaginatedResponse(items=items, total=total, skip=skip, limit=limit)


@router.post("", response_model=TeamResponse, status_code=201)
def create_team(data: TeamCreate, db: Session = Depends(get_db)):
    return team_service.create_team(db, data)


@router.get("/{team_id}", response_model=TeamResponse)
def get_team(team_id: uuid.UUID, db: Session = Depends(get_db)):
    return team_service.get_team(db, team_id)


@router.patch("/{team_id}", response_model=TeamResponse)
def update_team(team_id: uuid.UUID, data: TeamUpdate, db: Session = Depends(get_db)):
    return team_service.update_team(db, team_id, data)


@router.delete("/{team_id}", status_code=204)
def delete_team(team_id: uuid.UUID, db: Session = Depends(get_db)):
    team_service.delete_team(db, team_id)


@router.get("/{team_id}/members", response_model=PaginatedResponse[TeamMemberResponse])
def list_team_members(
    team_id: uuid.UUID,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
):
    team_service.get_team(db, team_id)
    items, total = team_member_service.list_team_members(db, team_id=team_id, skip=skip, limit=limit)
    return PaginatedResponse(items=items, total=total, skip=skip, limit=limit)


@router.get("/{team_id}/projects", response_model=PaginatedResponse[ProjectResponse])
def list_team_projects(
    team_id: uuid.UUID,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
):
    team_service.get_team(db, team_id)
    items, total = project_service.list_projects(db, team_id=team_id, skip=skip, limit=limit)
    return PaginatedResponse(items=items, total=total, skip=skip, limit=limit)
