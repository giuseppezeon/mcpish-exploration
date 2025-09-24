# Zeon Planner UI

A minimal FastAPI-based web app that:
- Loads a registry of robot skills (JSON files in `skills/`).
- Accepts a natural language task and produces a sequence of skills that could solve it.
- Lets you browse the available skills in the registry.

## Quickstart

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/` to use the UI.

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

1) Install BAML runtime (already in requirements):
```bash
pip install baml-py
```

2) Initialize BAML (creates `baml_src/`):
```bash
# Option A: npx (requires Node.js):
# npx baml-cli@latest init && npx baml-cli@latest generate

# Option B: Python-only install of CLI (if available on your system PATH):
baml-cli init && baml-cli generate
```

3) Add the provided `.baml` files in `baml_src/` (already included), then generate client:
```bash
# npx baml-cli@latest generate
baml-cli generate
```
This creates `baml_client/` used by the backend.

4) Run the app. In the UI, toggle “Use BAML” to route planning through BAML. Provider/model selection still applies; BAML enforces a schema-locked response.

Environment variables:
- `OPENAI_API_KEY` or `GEMINI_API_KEY` are used by your BAML client definitions.

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

