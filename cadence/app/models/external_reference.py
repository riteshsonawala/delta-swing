import uuid
from typing import Any, Optional

from sqlalchemy import JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDMixin
from app.models.enums import ReferenceType


class ExternalReference(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "external_references"

    project_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("projects.id"), nullable=False)
    reference_type: Mapped[ReferenceType] = mapped_column(nullable=False)
    external_id: Mapped[str] = mapped_column(nullable=False)
    external_url: Mapped[Optional[str]] = mapped_column(default=None)
    metadata_: Mapped[Optional[dict[str, Any]]] = mapped_column(
        "metadata", JSON, default=None
    )

    project: Mapped["Project"] = relationship(back_populates="external_references")  # noqa: F821
