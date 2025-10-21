#!/usr/bin/env python3
"""
Dynamic Knowledge Loader for Scripturemon Ultimate
Loads only relevant knowledge for each specialist
"""

import json
from pathlib import Path
from typing import Dict, List

class KnowledgeLoader:
    def __init__(self, knowledge_base: str = "knowledge"):
        self.base_path = Path(knowledge_base)

    def load_for_specialist(self, specialist: str, areas: List[str]) -> Dict:
        """Load only relevant knowledge for specialist"""

        knowledge = {}

        for area in areas:
            area_path = self.base_path / area / "references.json"
            if area_path.exists():
                with open(area_path, 'r') as f:
                    knowledge[area] = json.load(f)

        return knowledge

    def get_compact_prompt(self, specialist: str, areas: List[str]) -> str:
        """Generate compact prompt with references only"""

        knowledge = self.load_for_specialist(specialist, areas)

        prompt = f"Analyze using:\n"

        for area, refs in knowledge.items():
            for ref in refs.values():
                prompt += f"- {ref}\n"

        return prompt
