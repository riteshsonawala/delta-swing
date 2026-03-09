import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.models.enums import TagLevel


class TagCreate(BaseModel):
    level: TagLevel
    value: str
    description: Optional[str] = None


class TagUpdate(BaseModel):
    value: Optional[str] = None
    description: Optional[str] = None


class TagResponse(BaseModel):
    id: uuid.UUID
    level: TagLevel
    value: str
    description: Optional[str]
    created_at: datetime

    model_config = {"from_attributes": True}
