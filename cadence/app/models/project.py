import uuid
from datetime import date, datetime
from typing import Optional

from sqlalchemy import ForeignKey, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDMixin
from app.models.enums import ProjectStatus


class Project(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "projects"

    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[Optional[str]] = mapped_column(default=None)
    status: Mapped[ProjectStatus] = mapped_column(default=ProjectStatus.DRAFT)
    start_date: Mapped[date] = mapped_column(nullable=False)
    end_date: Mapped[date] = mapped_column(nullable=False)
    team_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("teams.id"), default=None)
    business_objective_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        ForeignKey("business_objectives.id"), default=None
    )

    team: Mapped[Optional["Team"]] = relationship(back_populates="projects")  # noqa: F821
    business_objective: Mapped[Optional["BusinessObjective"]] = relationship(  # noqa: F821
        back_populates="projects"
    )
    baseline: Mapped[Optional["ProjectBaseline"]] = relationship(
        back_populates="project", uselist=False
    )
    external_references: Mapped[list["ExternalReference"]] = relationship(  # noqa: F821
        back_populates="project", cascade="all, delete-orphan"
    )
    tags: Mapped[list["Tag"]] = relationship(  # noqa: F821
        secondary="project_tags", back_populates="projects"
    )


class ProjectBaseline(Base, UUIDMixin):
    __tablename__ = "project_baselines"
    __table_args__ = (UniqueConstraint("project_id"),)

    project_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("projects.id"), nullable=False)
    baseline_start_date: Mapped[date] = mapped_column(nullable=False)
    baseline_end_date: Mapped[date] = mapped_column(nullable=False)
    baselined_at: Mapped[datetime] = mapped_column(server_default=func.now())
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    project: Mapped["Project"] = relationship(back_populates="baseline")
