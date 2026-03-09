from fastapi import FastAPI

from app.config import settings
from app.routers import (
    business_objectives,
    external_references,
    projects,
    tags,
    team_members,
    teams,
)

app = FastAPI(
    title="Cadence",
    description="Project Management and Resource Management API",
    version="0.1.0",
)

app.include_router(projects.router, prefix=settings.api_v1_prefix)
app.include_router(teams.router, prefix=settings.api_v1_prefix)
app.include_router(team_members.router, prefix=settings.api_v1_prefix)
app.include_router(business_objectives.router, prefix=settings.api_v1_prefix)
app.include_router(tags.router, prefix=settings.api_v1_prefix)
app.include_router(external_references.router, prefix=settings.api_v1_prefix)


@app.get("/health")
def health_check():
    return {"status": "ok"}
