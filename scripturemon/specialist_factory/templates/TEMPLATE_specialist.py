"""
Specialist: {{SPECIALIST_NAME}}
Author: {{AUTHOR_NAME}}
Focus: {{FOCUS_AREA}}

CREATION_DATE: {{DATE}}
CREATED_BY: Claude + Digimundo

This specialist provides deep analysis based on {{AUTHOR_NAME}}'s methodology.
"""

from pathlib import Path
from typing import Dict, List, Optional, Tuple
import json


class {{SPECIALIST_CLASS_NAME}}:
    """
    Specialist for {{FOCUS_AREA}} analysis.
    Based on {{AUTHOR_NAME}}'s theory and methodology.
    """

    def __init__(self, llm_model: str = "scripturemon-optimized", deep_context: bool = True):
        """
        Initialize {{SPECIALIST_NAME}} specialist.

        Args:
            llm_model: LLM model to use for analysis
            deep_context: Whether to use deep context from theory book
        """
        self.name = "{{SPECIALIST_NAME}}"
        self.author = "{{AUTHOR_NAME}}"
        self.focus_area = "{{FOCUS_AREA}}"
        self.llm_model = llm_model
        self.deep_context_enabled = deep_context

        # Setup paths (relative, not absolute!)
        self.base_dir = Path(__file__).parent.parent.parent
        self.theory_book_path = self.base_dir / "theory" / "{{THEORY_BOOK_FILENAME}}"

        # Validate theory book exists
        if deep_context and not self.theory_book_path.exists():
            raise FileNotFoundError(
                f"Theory book not found: {self.theory_book_path}\n"
                f"Deep context mode requires theory book for {self.author}"
            )

        # Load prompts
        from .prompts import DEEP_CONTEXT_QUERIES, ANALYSIS_PROMPT, VALIDATION_CRITERIA
        self.deep_context_queries = DEEP_CONTEXT_QUERIES
        self.analysis_prompt = ANALYSIS_PROMPT
        self.validation_criteria = VALIDATION_CRITERIA

        # Initialize deep context
        self.theory_context = None
        if deep_context:
            self._load_theory_context()

    def _load_theory_context(self) -> None:
        """
        Load deep context from theory book.
        Extracts relevant concepts using predefined queries.
        """
        # TODO: Implement deep context loading
        # This should:
        # 1. Load theory book
        # 2. Index chunks
        # 3. Query for specific concepts using self.deep_context_queries
        # 4. Store in self.theory_context
        pass

    def analyze_screenplay(
        self,
        screenplay_text: str,
        screenplay_metadata: Optional[Dict] = None
    ) -> Dict:
        """
        Analyze screenplay using {{AUTHOR_NAME}}'s methodology.

        Args:
            screenplay_text: Full text of the screenplay
            screenplay_metadata: Optional metadata (title, author, etc.)

        Returns:
            Analysis result with scores, insights, and recommendations
        """
        # Build analysis prompt
        full_prompt = self._build_analysis_prompt(screenplay_text, screenplay_metadata)

        # Call LLM
        analysis_result = self._call_llm(full_prompt)

        # Validate result
        is_valid, score, issues = self._validate_analysis(analysis_result)

        return {
            "specialist": self.name,
            "author_base": self.author,
            "analysis": analysis_result,
            "validation": {
                "passed": is_valid,
                "score": score,
                "issues": issues
            },
            "metadata": screenplay_metadata or {}
        }

    def _build_analysis_prompt(
        self,
        screenplay_text: str,
        metadata: Optional[Dict] = None
    ) -> str:
        """Build complete analysis prompt with theory context."""
        prompt_parts = []

        # Add theory context if available
        if self.theory_context:
            prompt_parts.append("# THEORY CONTEXT")
            prompt_parts.append(self.theory_context)
            prompt_parts.append("")

        # Add base analysis prompt
        prompt_parts.append(self.analysis_prompt)

        # Add screenplay
        prompt_parts.append("# SCREENPLAY TO ANALYZE")
        if metadata:
            prompt_parts.append(f"Title: {metadata.get('title', 'Unknown')}")
            prompt_parts.append(f"Author: {metadata.get('author', 'Unknown')}")
        prompt_parts.append(screenplay_text)

        return "\n".join(prompt_parts)

    def _call_llm(self, prompt: str) -> str:
        """
        Call LLM with prompt.

        TODO: Implement actual LLM call
        This should integrate with your LLM backend (Ollama, etc.)
        """
        # Placeholder - replace with actual implementation
        return "Analysis result placeholder"

    def _validate_analysis(self, analysis: str) -> Tuple[bool, float, List[str]]:
        """
        Validate analysis quality against criteria.

        Args:
            analysis: Analysis text to validate

        Returns:
            Tuple of (is_valid, score, list_of_issues)
        """
        score = 10.0
        issues = []

        # Validate against criteria
        for criterion, weight in self.validation_criteria.items():
            if not self._check_criterion(analysis, criterion):
                score -= weight
                issues.append(f"Failed criterion: {criterion}")

        is_valid = score >= 7.0

        return is_valid, score, issues

    def _check_criterion(self, analysis: str, criterion: str) -> bool:
        """
        Check if analysis meets specific criterion.

        TODO: Implement criterion checking logic
        """
        # Placeholder - implement based on your validation needs
        return True

    def get_info(self) -> Dict:
        """Get information about this specialist."""
        return {
            "name": self.name,
            "author": self.author,
            "focus_area": self.focus_area,
            "theory_book": str(self.theory_book_path),
            "deep_context_enabled": self.deep_context_enabled,
            "validation_criteria": self.validation_criteria
        }


# Export specialist class
__all__ = ["{{SPECIALIST_CLASS_NAME}}"]
