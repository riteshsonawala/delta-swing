import uuid
from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDMixin


class Team(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "teams"

    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[Optional[str]] = mapped_column(default=None)
    is_active: Mapped[bool] = mapped_column(default=True)

    members: Mapped[list["TeamMember"]] = relationship(back_populates="team")  # noqa: F821
    projects: Mapped[list["Project"]] = relationship(back_populates="team")  # noqa: F821
