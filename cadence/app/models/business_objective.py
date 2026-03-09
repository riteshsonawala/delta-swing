import uuid
from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDMixin


class BusinessObjective(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "business_objectives"

    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[Optional[str]] = mapped_column(default=None)

    projects: Mapped[list["Project"]] = relationship(back_populates="business_objective")  # noqa: F821
