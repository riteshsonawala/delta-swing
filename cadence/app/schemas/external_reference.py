import uuid
from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel

from app.models.enums import ReferenceType


class ExternalReferenceCreate(BaseModel):
    reference_type: ReferenceType
    external_id: str
    external_url: Optional[str] = None
    metadata_: Optional[dict[str, Any]] = None


class ExternalReferenceUpdate(BaseModel):
    external_id: Optional[str] = None
    external_url: Optional[str] = None
    metadata_: Optional[dict[str, Any]] = None


class ExternalReferenceResponse(BaseModel):
    id: uuid.UUID
    project_id: uuid.UUID
    reference_type: ReferenceType
    external_id: str
    external_url: Optional[str]
    metadata_: Optional[dict[str, Any]]
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
