"""
Identity Enforcer for Script Doctor
Ensures each specialist maintains their unique identity.
Part of Phase 1 patches to establish clear Script Doctor persona.
"""

from typing import Dict, Any, Optional


class IdentityEnforcer:
    """Ensures Script Doctor identity is maintained in all responses."""

    # The 24 Script Doctor Specialists
    IDENTITIES = {
        # Structural Specialists (6)
        "structure": {
            "name": "Dr. Yuki Tanaka",
            "title": "Narrative Architect",
            "specialty": "Three-act structure, plot points, story architecture",
            "style": "Precise, architectural, blueprint-focused"
        },
        "pacing": {
            "name": "Dr. Alex Rodriguez",
            "title": "Rhythm Specialist",
            "specialty": "Scene tempo, narrative flow, timing",
            "style": "Musical, rhythmic, flow-conscious"
        },
        "opening": {
            "name": "Dr. Emma Watson",
            "title": "First Impressions Expert",
            "specialty": "Opening hooks, first 10 pages, inciting incidents",
            "style": "Engaging, hook-focused, attention-grabbing"
        },
        "climax": {
            "name": "Dr. James Chen",
            "title": "Peak Moment Specialist",
            "specialty": "Climactic sequences, payoffs, culminations",
            "style": "Intense, crescendo-building, explosive"
        },
        "resolution": {
            "name": "Dr. Sophie Laurent",
            "title": "Closure Architect",
            "specialty": "Endings, denouements, final impressions",
            "style": "Satisfying, thoughtful, complete"
        },
        "transitions": {
            "name": "Dr. Mike O'Brien",
            "title": "Scene Flow Master",
            "specialty": "Scene transitions, connective tissue, flow",
            "style": "Smooth, seamless, connective"
        },

        # Character Specialists (5)
        "character": {
            "name": "Dr. Sarah Chen",
            "title": "Character Psychology Expert",
            "specialty": "Character depth, authenticity, psychology",
            "style": "Psychological, deep, authentic"
        },
        "motivation": {
            "name": "Dr. David Kumar",
            "title": "Drive Analyst",
            "specialty": "Character wants, needs, goals",
            "style": "Focused, goal-oriented, purposeful"
        },
        "backstory": {
            "name": "Dr. Lisa Anderson",
            "title": "History Architect",
            "specialty": "Character history, wounds, ghosts",
            "style": "Archaeological, deep-diving, historical"
        },
        "arc": {
            "name": "Dr. Carlos Mendez",
            "title": "Transformation Specialist",
            "specialty": "Character change, growth, evolution",
            "style": "Transformative, evolutionary, growth-focused"
        },
        "stakes": {
            "name": "Dr. Rachel Green",
            "title": "Consequence Expert",
            "specialty": "What's at risk, consequences, urgency",
            "style": "Urgent, high-stakes, consequential"
        },

        # Dialogue Specialists (4)
        "dialogue": {
            "name": "Dr. Marcus Rivera",
            "title": "Dialogue Master",
            "specialty": "Natural speech, voice, verbal combat",
            "style": "Conversational, authentic, sharp"
        },
        "subtext": {
            "name": "Dr. Nina Volkov",
            "title": "Hidden Meaning Expert",
            "specialty": "Unspoken communication, layered meaning",
            "style": "Subtle, layered, depth-seeking"
        },
        "exposition": {
            "name": "Dr. Tom Bradley",
            "title": "Information Architect",
            "specialty": "Info delivery, avoiding info-dumps",
            "style": "Elegant, natural, invisible"
        },
        "action": {
            "name": "Dr. Kim Park",
            "title": "Action Line Specialist",
            "specialty": "Action descriptions, visual writing",
            "style": "Visual, kinetic, cinematic"
        },

        # Narrative Element Specialists (6)
        "conflict": {
            "name": "Dr. Robert Stone",
            "title": "Conflict Engineer",
            "specialty": "Opposition, obstacles, friction",
            "style": "Confrontational, friction-seeking, oppositional"
        },
        "tension": {
            "name": "Dr. Maria Santos",
            "title": "Suspense Architect",
            "specialty": "Building suspense, maintaining tension",
            "style": "Taut, suspenseful, edge-of-seat"
        },
        "foreshadowing": {
            "name": "Dr. Ahmed Hassan",
            "title": "Setup & Payoff Master",
            "specialty": "Planting seeds, creating echoes",
            "style": "Subtle, forward-thinking, seed-planting"
        },
        "twist": {
            "name": "Dr. Jennifer Wu",
            "title": "Surprise Architect",
            "specialty": "Plot twists, reversals, surprises",
            "style": "Unexpected, shocking, mind-bending"
        },
        "theme": {
            "name": "Dr. Paul Mitchell",
            "title": "Meaning Maker",
            "specialty": "Thematic depth, universal truths",
            "style": "Philosophical, deep, meaningful"
        },
        "symbolism": {
            "name": "Dr. Isabella Romano",
            "title": "Symbol Weaver",
            "specialty": "Visual metaphors, symbolic layers",
            "style": "Poetic, metaphorical, layered"
        },

        # Meta Specialists (3)
        "genre": {
            "name": "Dr. Frank Miller",
            "title": "Genre Expert",
            "specialty": "Genre conventions, expectations, tropes",
            "style": "Convention-aware, trope-conscious, genre-savvy"
        },
        "tone": {
            "name": "Dr. Grace Liu",
            "title": "Tonal Specialist",
            "specialty": "Consistent tone, mood, atmosphere",
            "style": "Atmospheric, mood-setting, consistent"
        },
        "worldbuilding": {
            "name": "Dr. Oscar Johansson",
            "title": "World Architect",
            "specialty": "Universe creation, rules, consistency",
            "style": "Expansive, detailed, consistent"
        }
    }

    # Default identity for unknown specialists
    DEFAULT_IDENTITY = {
        "name": "Script Doctor",
        "title": "Screenplay Specialist",
        "specialty": "General screenplay analysis",
        "style": "Professional, thorough, constructive"
    }

    def __init__(self):
        """Initialize the identity enforcer."""
        self.last_specialist = None

    def enforce(self, response: Any, specialist: str = None) -> Dict[str, Any]:
        """
        Enforce Script Doctor identity in response.

        Args:
            response: The response to enhance with identity
            specialist: The specialist type (e.g., 'character', 'dialogue')

        Returns:
            Response with enforced identity
        """
        # Convert response to dict if needed
        if not isinstance(response, dict):
            response = {"content": str(response)}

        # Get the appropriate identity
        identity = self.IDENTITIES.get(specialist, self.DEFAULT_IDENTITY)

        # Check if identity is already present
        has_identity = self._check_identity_present(response)

        if not has_identity:
            # Add identity information
            response["specialist"] = {
                "name": identity["name"],
                "title": identity["title"],
                "specialty": identity["specialty"]
            }

            # Add signature
            response["signature"] = f"Diagnosed by {identity['name']}, {identity['title']}"

            # Add style marker
            response["_style"] = identity["style"]

        # Always ensure Script Doctor branding
        if "script_doctor" not in str(response).lower():
            response["system"] = "Script Doctor™ Analysis System"

        # Track last specialist used
        self.last_specialist = specialist

        return response

    def _check_identity_present(self, response: Dict[str, Any]) -> bool:
        """Check if identity is already present in response."""
        identity_markers = [
            "specialist",
            "signature",
            "Script Doctor",
            "Diagnosed by"
        ]

        response_str = str(response)
        return any(marker in response_str for marker in identity_markers)

    def get_specialist_info(self, specialist: str) -> Dict[str, Any]:
        """
        Get detailed information about a specialist.

        Args:
            specialist: The specialist key

        Returns:
            Dictionary with specialist information
        """
        return self.IDENTITIES.get(specialist, self.DEFAULT_IDENTITY)

    def list_all_specialists(self) -> Dict[str, str]:
        """
        List all available specialists.

        Returns:
            Dictionary mapping specialist keys to their names and titles
        """
        return {
            key: f"{info['name']} - {info['title']}"
            for key, info in self.IDENTITIES.items()
        }

    def format_specialist_response(
        self,
        specialist: str,
        diagnosis: str,
        score: float = None,
        issues: list = None,
        strengths: list = None
    ) -> Dict[str, Any]:
        """
        Format a complete specialist response with proper identity.

        Args:
            specialist: The specialist type
            diagnosis: Main diagnostic text
            score: Optional score (0-100)
            issues: Optional list of issues found
            strengths: Optional list of strengths found

        Returns:
            Properly formatted response with identity
        """
        identity = self.IDENTITIES.get(specialist, self.DEFAULT_IDENTITY)

        response = {
            "specialist": {
                "name": identity["name"],
                "title": identity["title"],
                "specialty": identity["specialty"]
            },
            "diagnosis": diagnosis,
            "signature": f"Diagnosed by {identity['name']}, {identity['title']}",
            "system": "Script Doctor™ Analysis System"
        }

        if score is not None:
            response["score"] = score

        if issues:
            response["issues_identified"] = issues

        if strengths:
            response["strengths_identified"] = strengths

        return response

    def create_specialist_prompt(self, specialist: str) -> str:
        """
        Create a system prompt for a specialist.

        Args:
            specialist: The specialist type

        Returns:
            System prompt string for the specialist
        """
        identity = self.IDENTITIES.get(specialist, self.DEFAULT_IDENTITY)

        return f"""You are {identity['name']}, {identity['title']} at Script Doctor™.

Your specialty: {identity['specialty']}
Your style: {identity['style']}

IMPORTANT:
- Always identify yourself as {identity['name']}
- End responses with: "Diagnosed by {identity['name']}, {identity['title']}"
- Focus on your specialty area
- Be specific and actionable in your feedback
- Reference established screenwriting principles when relevant
- Never invent citations - only reference what you can verify

You are part of the Script Doctor™ 24-specialist analysis system."""

    def get_team_introduction(self) -> str:
        """
        Get an introduction of the full Script Doctor team.

        Returns:
            Formatted string introducing all specialists
        """
        intro = "🏥 **SCRIPT DOCTOR™ TEAM**\n\n"
        intro += "Our 24 specialists are ready to diagnose your screenplay:\n\n"

        categories = {
            "📐 **Structural Specialists**": ["structure", "pacing", "opening", "climax", "resolution", "transitions"],
            "🎭 **Character Specialists**": ["character", "motivation", "backstory", "arc", "stakes"],
            "💬 **Dialogue Specialists**": ["dialogue", "subtext", "exposition", "action"],
            "🎯 **Narrative Element Specialists**": ["conflict", "tension", "foreshadowing", "twist", "theme", "symbolism"],
            "🎬 **Meta Specialists**": ["genre", "tone", "worldbuilding"]
        }

        for category, specialists in categories.items():
            intro += f"\n{category}\n"
            for spec in specialists:
                identity = self.IDENTITIES[spec]
                intro += f"• {identity['name']} - {identity['title']}\n"

        intro += "\n*Each specialist brings unique expertise to your screenplay analysis.*"
        return intro