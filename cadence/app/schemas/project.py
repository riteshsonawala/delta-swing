import uuid
from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel

from app.models.enums import ProjectStatus
from app.schemas.external_reference import ExternalReferenceResponse
from app.schemas.tag import TagResponse


class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None
    start_date: date
    end_date: date
    team_id: Optional[uuid.UUID] = None
    business_objective_id: Optional[uuid.UUID] = None


class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[ProjectStatus] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    team_id: Optional[uuid.UUID] = None
    business_objective_id: Optional[uuid.UUID] = None


class ProjectBaselineResponse(BaseModel):
    id: uuid.UUID
    baseline_start_date: date
    baseline_end_date: date
    baselined_at: datetime

    model_config = {"from_attributes": True}


class DelayResponse(BaseModel):
    baseline_start_date: date
    baseline_end_date: date
    current_start_date: date
    current_end_date: date
    start_delay_days: int
    end_delay_days: int


class ProjectResponse(BaseModel):
    id: uuid.UUID
    name: str
    description: Optional[str]
    status: ProjectStatus
    start_date: date
    end_date: date
    team_id: Optional[uuid.UUID]
    business_objective_id: Optional[uuid.UUID]
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ProjectDetailResponse(ProjectResponse):
    baseline: Optional[ProjectBaselineResponse] = None
    delay: Optional[DelayResponse] = None
    tags: list[TagResponse] = []
    external_references: list[ExternalReferenceResponse] = []
