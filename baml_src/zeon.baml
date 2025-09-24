// Generator config for Python client
generator target {
    output_type "python/pydantic"
    output_dir "../"
    default_client_mode "sync"
    version "0.76.2"
}

// Providers / clients
client<llm> OpenAIClient {
  provider openai
  options {
    model env.BAML_OPENAI_MODEL or "gpt-4o-mini"
    api_key env.OPENAI_API_KEY
  }
}

client<llm> GeminiClient {
  provider vertex-ai
  options {
    model env.BAML_GEMINI_MODEL or "gemini-1.5-pro"
    project_id env.GOOGLE_CLOUD_PROJECT or ""
    location env.GOOGLE_CLOUD_REGION or "us-central1"
  }
}

// Types
class PlanStep {
  skill string
  inputs map<string, any>
  rationale string
}

class PlanResult {
  steps PlanStep[]
}

class SkillLite {
  name string
  version string
  tier string?
  description string?
  input_schema map<string, any>?
}

// Function: produce a plan strictly matching PlanResult
function PlanWithSkills(task: string, skills: SkillLite[], provider: string?, model: string?) -> PlanResult {
  client when provider == "gemini" then GeminiClient else OpenAIClient
  prompt #"
You are a robotics task planner. Only use skills from this list:
{{ skills }}

Task: {{ task }}

Rules:
- Output strictly matches the schema below; no markdown.
- Each step must use an existing skill name and provide inputs matching that skill's input_schema.
- Be minimal and deterministic.

{{ ctx.output_format }}
"#
}

