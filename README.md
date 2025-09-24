# Zeon Planner UI

A minimal FastAPI-based web app that:
- Loads a registry of robot skills (JSON files in `skills/`).
- Accepts a natural language task and produces a sequence of skills that could solve it.
- Lets you browse the available skills in the registry.

## Quickstart

```bash
make run
```

Open `http://127.0.0.1:8000/` to use the UI. The Makefile will create a venv and install all requirements automatically.

## AI Planner (OpenAI / Gemini)

- In the UI, select provider (OpenAI or Gemini), enter a model (e.g., `gpt-4o-mini` or `gemini-1.5-pro`), and optionally paste an API key.
- Alternatively, set environment variables:
  - `export OPENAI_API_KEY=...`
  - `export GEMINI_API_KEY=...`
- The planner sends the natural language task plus the live registry (skills/*.json) to the selected model and expects a strict JSON object:

```json
{
  "steps": [
    {"skill": "<name>", "inputs": {"...": "..."}, "rationale": "..."}
  ]
}
```

Each step is validated against the target skill's `input_schema` using JSON Schema (Draft 2020-12). Unknown skills or invalid inputs are rejected.

## BAML Integration (optional, recommended for predictability)

By default, BAML runtime (`baml-py`) is installed via requirements. If you want to generate the `baml_client/` code (optional), use:

```bash
make baml   # attempts to init+generate via npx or system baml-cli
```

- If the BAML CLI is not available, the app still runs; you can use the non-BAML path (uncheck “Use BAML”).
- At runtime, simply toggle “Use BAML” in the UI to route planning through BAML. Provider/model selection still applies; BAML enforces schema-locked responses.

Environment variables:
- `OPENAI_API_KEY` or `GEMINI_API_KEY` are used by your BAML client definitions.

## Skill JSON fields

- `name`: Stable, unique skill identifier (snake_case). Used by planner and executor.
- `version`: Semver version for pinning and reproducibility.
- `description`: Human-readable summary shown in UI.
- `tier`: Granularity, one of `T0` (atomic), `T1` (compound), `T2` (procedural).
- `input_schema`: JSON Schema for required inputs. Enforced at plan and runtime.
- `output_schema`: JSON Schema for success output (optional).
- `error_schema`: Shape of error payloads (optional).
- `preconditions`: Facts that must hold before execution (symbolic strings).
- `postconditions`: Facts expected after success.
- `invariants`: Facts that must hold during execution.
- `effect_schema`: Structured state changes (optional).
- `safety`: Safety constraints/metadata (optional).
- `timeout_s`: Max runtime seconds.
- `retry_policy`: Retry config (optional).
- `idempotency`: Idempotence mode (optional).
- `determinism`: Deterministic or stochastic behavior hints (optional).
- `simulate`: Simulation support flags (optional).
- `telemetry_schema`: Extra metrics/events emitted (optional).
- `cost_model`: Estimated duration/energy for planning (optional).
- `concurrency`: Parallelism/locking hints (optional).
- `failure_modes`: Known failures with mitigation (optional).
- `compensation`: Rollback skill reference (optional).
- `compatibility`: Supported robots/firmware/api versions (optional).
- `vendor`: Provider/owner info (optional).
- `endpoint`: RPC/MCP/ROS endpoint hint (optional).
- `deprecated`: Set `true` if superseded.

Minimal fields to get started: `name`, `version`, `description`, `tier`, `input_schema`. Add `preconditions`, `postconditions`, and `timeout_s` for safer planning.

## Project layout

```
app/
  __init__.py
  main.py          # FastAPI app, API routes, static serving
  models.py        # Pydantic models for skills and plans
  registry.py      # Skill registry loader
  planner.py       # Simple heuristic planner

web/
  index.html       # Modern minimal UI
  styles.css
  app.js

skills/
  move_to_pose.json
  pick_place.json
  centrifuge_cycle.json
```

## Extending the skill registry

- Add more JSON files into `skills/` matching the `SkillSpec` fields used here.
- The loader ingests all `*.json` files on startup.

## Notes

- This demo uses a simple, deterministic keyword-based planner to keep runtime behavior reproducible. You can replace `app/planner.py` with a more advanced planner (LLM, HTN, BT) later.

