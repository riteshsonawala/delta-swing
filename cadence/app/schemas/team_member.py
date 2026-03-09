import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class TeamMemberCreate(BaseModel):
    name: str
    email: str
    team_id: Optional[uuid.UUID] = None
    lead_id: Optional[uuid.UUID] = None


class TeamMemberUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    team_id: Optional[uuid.UUID] = None
    lead_id: Optional[uuid.UUID] = None


class TeamMemberResponse(BaseModel):
    id: uuid.UUID
    name: str
    email: str
    team_id: Optional[uuid.UUID]
    lead_id: Optional[uuid.UUID]
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
