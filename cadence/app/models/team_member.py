import uuid
from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDMixin


class TeamMember(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "team_members"

    name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    team_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("teams.id"), default=None)
    lead_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        ForeignKey("team_members.id"), default=None
    )

    team: Mapped[Optional["Team"]] = relationship(back_populates="members")  # noqa: F821
    lead: Mapped[Optional["TeamMember"]] = relationship(
        remote_side="TeamMember.id", foreign_keys=[lead_id]
    )
    direct_reports: Mapped[list["TeamMember"]] = relationship(
        foreign_keys=[lead_id], viewonly=True
    )
