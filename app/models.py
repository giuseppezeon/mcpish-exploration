from __future__ import annotations

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class SkillSpec(BaseModel):
    name: str
    version: str
    description: Optional[str] = None
    tier: Optional[str] = Field(default=None, description="T0 | T1 | T2")
    input_schema: Optional[Dict[str, Any]] = None
    output_schema: Optional[Dict[str, Any]] = None
    error_schema: Optional[Dict[str, Any]] = None
    preconditions: Optional[List[Any]] = None
    postconditions: Optional[List[Any]] = None
    invariants: Optional[List[Any]] = None
    effect_schema: Optional[List[Dict[str, Any]]] = None
    safety: Optional[Dict[str, Any]] = None
    timeout_s: Optional[int] = None
    retry_policy: Optional[Dict[str, Any]] = None
    idempotency: Optional[Any] = None
    determinism: Optional[Dict[str, Any]] = None
    simulate: Optional[Dict[str, Any]] = None
    telemetry_schema: Optional[Dict[str, Any]] = None
    cost_model: Optional[Dict[str, Any]] = None
    concurrency: Optional[Dict[str, Any]] = None
    failure_modes: Optional[List[Dict[str, Any]]] = None
    compensation: Optional[Dict[str, Any]] = None
    compatibility: Optional[Dict[str, Any]] = None
    vendor: Optional[str] = None
    endpoint: Optional[str] = None
    deprecated: Optional[bool] = False


class SkillSummary(BaseModel):
    name: str
    version: str
    tier: Optional[str] = None
    description: Optional[str] = None


class PlannerRequest(BaseModel):
    task: str = Field(description="Natural language description of the goal")
    context: Dict[str, Any] = Field(default_factory=dict)
    provider: str | None = Field(default=None, description="'openai' | 'gemini'")
    model: str | None = Field(default=None)
    api_key: str | None = Field(default=None, description="Optional API key (or use env)")


class PlanStep(BaseModel):
    order: int
    skill: str
    inputs: Dict[str, Any] = Field(default_factory=dict)
    rationale: Optional[str] = None


class PlanResult(BaseModel):
    task: str
    steps: List[PlanStep]
    notes: Optional[str] = None

