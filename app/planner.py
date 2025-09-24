from __future__ import annotations

import os
from typing import Dict, List, Any

from .models import PlanResult, PlanStep, PlannerRequest
from .registry import SkillRegistry
from jsonschema import Draft202012Validator, ValidationError

try:
    from openai import OpenAI
    from openai import BadRequestError as OpenAIBadRequestError
except Exception:  # pragma: no cover
    OpenAI = None  # type: ignore
    OpenAIBadRequestError = Exception  # type: ignore

try:
    from google import genai as genai_pkg  # google-genai
except Exception:  # pragma: no cover
    genai_pkg = None  # type: ignore


class AIPlanner:
    """Provider-agnostic AI planner with schema validation and registry awareness."""

    def __init__(self, registry: SkillRegistry) -> None:
        self.registry = registry

    def _serialize_registry(self) -> List[Dict[str, Any]]:
        # Provide only planning-relevant fields to the LLM
        return [
            {
                "name": s.name,
                "version": s.version,
                "tier": s.tier,
                "description": s.description,
                "input_schema": s.input_schema,
                "output_schema": s.output_schema,
                "preconditions": s.preconditions,
                "postconditions": s.postconditions,
                "invariants": s.invariants,
            }
            for s in self.registry.all_specs()
        ]

    def _validate_steps(self, steps: List[Dict[str, Any]]) -> List[PlanStep]:
        validated: List[PlanStep] = []
        name_to_spec = {s.name: s for s in self.registry.all_specs()}

        for idx, step in enumerate(steps, start=1):
            skill = step.get("skill")
            inputs = step.get("inputs", {})
            rationale = step.get("rationale")
            spec = name_to_spec.get(skill)
            if not spec:
                raise ValueError(f"Unknown skill in plan: {skill}")
            schema = spec.input_schema or {"type": "object"}
            Draft202012Validator.check_schema(schema)
            Draft202012Validator(schema).validate(inputs)
            validated.append(PlanStep(order=idx, skill=skill, inputs=inputs, rationale=rationale))

        return validated

    def _prompt(self, req: PlannerRequest) -> str:
        return (
            "You are a robotics task planner. Given a user task and a library of atomic skills, "
            "produce a minimal, deterministic sequence of steps. Each step must reference an existing skill name and "
            "provide an 'inputs' object that validates against that skill's input_schema."
            "\nConstraints:\n- Only use skills provided.\n- No free-form actions.\n- Be conservative and explicit.\n- Return strictly JSON matching this schema: {\"steps\":[{\"skill\":string,\"inputs\":object,\"rationale\":string}]}\n"
            f"\nUser task: {req.task}\n"
        )

    def _call_openai(self, req: PlannerRequest) -> Dict[str, Any]:
        if OpenAI is None:
            raise RuntimeError("openai package not installed")
        api_key = req.api_key or os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY missing")
        client = OpenAI(api_key=api_key)
        model = req.model or "gpt-4o-mini"

        system = "You return only valid JSON. No markdown, no prose."
        user = self._prompt(req) + "\nSkills:\n" + str(self._serialize_registry())

        # Prefer deterministic sampling; if model disallows temperature, retry without it
        try:
            resp = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": user},
                ],
                temperature=0,
            )
        except OpenAIBadRequestError as e:
            msg = str(e).lower()
            if "temperature" in msg and "unsupported" in msg:
                resp = client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": system},
                        {"role": "user", "content": user},
                    ],
                )
            else:
                raise
        content = resp.choices[0].message.content or "{}"
        import json

        return json.loads(content)

    def _call_gemini(self, req: PlannerRequest) -> Dict[str, Any]:
        if genai_pkg is None:
            raise RuntimeError("google-genai package not installed")
        api_key = req.api_key or os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise RuntimeError("GEMINI_API_KEY missing")
        model_name = req.model or "gemini-1.5-pro"
        client = genai_pkg.Client(api_key=api_key)

        prompt = "Return only JSON, no markdown.\n" + self._prompt(req) + "\nSkills:\n" + str(self._serialize_registry())
        result = client.models.generate_content(model=model_name, contents=prompt)
        text = result.text or "{}"
        import json

        return json.loads(text)

    def plan(self, req: PlannerRequest) -> PlanResult:
        provider = (req.provider or "openai").lower()
        try:
            if provider == "openai":
                raw = self._call_openai(req)
            elif provider == "gemini":
                raw = self._call_gemini(req)
            else:
                raise RuntimeError(f"Unsupported provider: {provider}")

            steps_dicts = raw.get("steps") if isinstance(raw, dict) else None
            if not isinstance(steps_dicts, list):
                raise ValueError("Planner output missing 'steps' list")

            steps = self._validate_steps(steps_dicts)
            return PlanResult(task=req.task, steps=steps, notes=f"Provider: {provider}")
        except ValidationError as ve:
            raise RuntimeError(f"Input validation failed: {ve.message}")
        except Exception as e:
            # In production, add more granular error reporting
            raise RuntimeError(str(e))

