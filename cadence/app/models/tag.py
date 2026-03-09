import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import Column, ForeignKey, Table, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, UUIDMixin
from app.models.enums import TagLevel

project_tags = Table(
    "project_tags",
    Base.metadata,
    Column("project_id", ForeignKey("projects.id"), primary_key=True),
    Column("tag_id", ForeignKey("tags.id"), primary_key=True),
)

# Alias for import in models/__init__.py
ProjectTag = project_tags


class Tag(Base, UUIDMixin):
    __tablename__ = "tags"
    __table_args__ = (UniqueConstraint("level", "value"),)

    level: Mapped[TagLevel] = mapped_column(nullable=False)
    value: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[Optional[str]] = mapped_column(default=None)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    projects: Mapped[list["Project"]] = relationship(  # noqa: F821
        secondary=project_tags, back_populates="tags"
    )
