from __future__ import annotations

from pathlib import Path
from typing import List, Optional

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from .models import PlannerRequest
from .planner import AIPlanner
from .registry import SkillRegistry

ROOT = Path(__file__).resolve().parents[1]
WEB_DIR = ROOT / "web"
SKILLS_DIR = ROOT / "skills"

app = FastAPI(title="Zeon Planner UI")

# Static files for the web UI
app.mount("/static", StaticFiles(directory=str(WEB_DIR)), name="static")


# Initialize registry and planner
registry = SkillRegistry(SKILLS_DIR)
registry.load()
planner = AIPlanner(registry)


@app.get("/")
async def index():
    index_path = WEB_DIR / "index.html"
    if not index_path.exists():
        raise HTTPException(status_code=500, detail="UI not found")
    return FileResponse(str(index_path))


@app.get("/api/skills")
async def list_skills(
    tiers: Optional[List[str]] = Query(
        None, description="Filter skills by tier (e.g., T0, T1, T2)"
    ),
):
    all_skills = registry.list()

    if tiers is None:
        return [s.model_dump() for s in all_skills]

    # Filter skills by tier
    filtered_skills = [s for s in all_skills if s.tier in tiers]
    return [s.model_dump() for s in filtered_skills]


@app.get("/api/skills/{name}")
async def get_skill(name: str):
    spec = registry.get(name)
    if not spec:
        raise HTTPException(status_code=404, detail="Skill not found")
    return spec.model_dump()


@app.post("/api/plan")
async def create_plan(req: PlannerRequest):
    result = planner.plan(req)
    return result.model_dump()
