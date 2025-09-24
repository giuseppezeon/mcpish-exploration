from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List, Optional

from .models import SkillSpec, SkillSummary


class SkillRegistry:
    def __init__(self, skills_dir: Path) -> None:
        self.skills_dir = skills_dir
        self._skills: Dict[str, SkillSpec] = {}

    def load(self) -> None:
        self._skills.clear()
        if not self.skills_dir.exists():
            return
        for path in sorted(self.skills_dir.glob("*.json")):
            try:
                data = json.loads(path.read_text())
                spec = SkillSpec(**data)
                self._skills[spec.name] = spec
            except Exception as e:
                # Skip malformed skill files; in production, log this
                continue

    def list(self) -> List[SkillSummary]:
        return [
            SkillSummary(
                name=s.name,
                version=s.version,
                tier=s.tier,
                description=s.description,
            )
            for s in sorted(self._skills.values(), key=lambda x: x.name)
        ]

    def get(self, name: str) -> Optional[SkillSpec]:
        return self._skills.get(name)

    def all_specs(self) -> List[SkillSpec]:
        return list(self._skills.values())

