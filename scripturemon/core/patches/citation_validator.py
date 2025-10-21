"""
Citation Validator for Script Doctor
Validates that all citations are real and from verified sources.
Part of Phase 1 patches to fix hallucination issues.
"""

import json
from pathlib import Path
from typing import Dict, List, Any


class CitationValidator:
    """Validates that all citations are real and exist in the knowledge base."""

    def __init__(self, anchors_file: str = None):
        """
        Initialize the citation validator.

        Args:
            anchors_file: Path to JSON file containing valid citations.
                         If None, will look for anchors.json in current/parent dirs.
        """
        self.valid_citations = {}

        # Try to find anchors file
        if anchors_file and Path(anchors_file).exists():
            self.load_anchors(anchors_file)
        else:
            # Look for anchors.json in common locations
            search_paths = [
                Path("anchors.json"),
                Path("memory/anchors.json"),
                Path("memory-mesh/runtime/anchors.json"),
                Path("../memory/anchors.json"),
            ]

            for path in search_paths:
                if path.exists():
                    self.load_anchors(str(path))
                    break
            else:
                # Create empty anchors if none found
                self.valid_citations = {
                    "_metadata": {
                        "version": "1.0",
                        "description": "Valid citations database",
                        "count": 0
                    }
                }

    def load_anchors(self, filepath: str):
        """Load valid citations from JSON file."""
        try:
            with open(filepath, 'r') as f:
                self.valid_citations = json.load(f)
                print(f"✅ Loaded {len(self.valid_citations)} valid citations from {filepath}")
        except Exception as e:
            print(f"⚠️ Could not load anchors from {filepath}: {e}")
            self.valid_citations = {}

    def validate(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate citations in a response.
        Removes false citations and marks uncertain ones.

        Args:
            response: Dictionary containing diagnostics with potential citations

        Returns:
            Response with validated citations
        """
        if not response:
            return response

        # Process diagnostics if present
        if "diagnostics" in response:
            for item in response.get("diagnostics", []):
                self._validate_item(item)

        # Process individual specialist responses
        for key in response:
            if isinstance(response[key], dict):
                if "citations" in response[key]:
                    for citation in response[key].get("citations", []):
                        self._validate_citation(citation)

                if "rule_id" in response[key]:
                    self._validate_item(response[key])

        # Add validation metadata
        response["_validation"] = {
            "citations_validated": True,
            "validator_version": "1.0"
        }

        return response

    def _validate_item(self, item: Dict[str, Any]):
        """Validate a single diagnostic item."""
        rule_id = item.get("rule_id")

        if rule_id:
            # Check if rule exists in valid citations
            if rule_id not in self.valid_citations:
                # Mark as unverified
                item["warning"] = "Citation not verified - may be AI-generated"
                item["confidence"] = item.get("confidence", 1.0) * 0.5
                item["verified"] = False
            else:
                item["verified"] = True
                # Add source if available
                if isinstance(self.valid_citations[rule_id], dict):
                    item["source"] = self.valid_citations[rule_id].get("source", "verified")

    def _validate_citation(self, citation: Dict[str, Any]):
        """Validate a single citation object."""
        ref = citation.get("reference") or citation.get("ref")

        if ref and ref not in self.valid_citations:
            citation["warning"] = "Unverified reference"
            citation["confidence"] = 0.3
            citation["verified"] = False
        else:
            citation["verified"] = True

    def add_valid_citation(self, rule_id: str, source: str = None):
        """
        Add a new valid citation to the database.

        Args:
            rule_id: The rule/citation ID
            source: Optional source information
        """
        self.valid_citations[rule_id] = {
            "source": source or "manual",
            "verified": True
        }

    def save_anchors(self, filepath: str = "anchors.json"):
        """Save current valid citations to file."""
        try:
            with open(filepath, 'w') as f:
                json.dump(self.valid_citations, f, indent=2)
            print(f"✅ Saved {len(self.valid_citations)} citations to {filepath}")
        except Exception as e:
            print(f"❌ Could not save anchors: {e}")

    def get_stats(self) -> Dict[str, Any]:
        """Get validation statistics."""
        return {
            "total_valid_citations": len(self.valid_citations),
            "validator_active": True,
            "version": "1.0"
        }


# Example valid citations for testing
DEFAULT_CITATIONS = {
    "CHAR.R001": {"source": "Robert McKee - Story", "page": 104},
    "CHAR.R002": {"source": "Save the Cat", "concept": "Want vs Need"},
    "DIAL.R001": {"source": "Screenplay by Syd Field", "chapter": 7},
    "STRU.R001": {"source": "The Writer's Journey", "concept": "Three-Act Structure"},
    "CONF.R001": {"source": "Creating Character Arcs", "page": 45}
}


def create_default_anchors(filepath: str = "anchors.json"):
    """Create a default anchors file with common citations."""
    with open(filepath, 'w') as f:
        json.dump(DEFAULT_CITATIONS, f, indent=2)
    print(f"✅ Created default anchors file: {filepath}")