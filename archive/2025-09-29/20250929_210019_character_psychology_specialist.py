"""
Script Doctor Psychemon - Character Psychology and Development Specialist
A Script Doctor™ in Digimon form specializing in character depth and psychological realism.
"""

import re
import yaml
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass
from collections import defaultdict, Counter


@dataclass
class CharacterProfile:
    """Psychological profile of a character."""
    name: str
    appearances: int
    dialogue_count: int
    has_internal_conflict: bool
    consistency_score: float  # 0-1
    depth_score: float  # 0-1
    unique_voice_score: float  # 0-1
    growth_evident: bool
    vulnerability_shown: bool
    traits: List[str]
    contradictions: List[Tuple[str, str]]
    relationships: Dict[str, str]  # character -> relationship type
    internal_conflicts: List[str] = None  # List of internal conflicts
    want: Optional[str] = None  # What the character wants
    need: Optional[str] = None  # What the character needs


@dataclass
class PsychologicalElement:
    """Element of character psychology."""
    element_type: str  # want, need, fear, defense, etc.
    character: str
    description: str
    page_revealed: int
    strength: float  # 0-1
    integrated: bool  # Well-integrated into story?


class DrCharacterPsychology:
    """
    Script Doctor Psychemon - The Character Psychology and Development Specialist
    
    A Script Doctor™ in Digimon form, specializing in analyzing character depth,
    psychological consistency, and authentic character development.
    
    Identity: Script Doctor first, Digimon psychology specialist second.
    """
    
    def __init__(self, rules_path: str = None):
        """Initialize Script Doctor Psychemon with rules and configuration."""
        self.name = "Script Doctor Psychemon"
        self.digimon_name = "Psychemon"
        self.title = "Script Doctor - Character Psychology and Development Specialist"
        self.specialty = "Character depth, psychological realism, internal consistency, believable behavior"
        self.identity = "I am Script Doctor Psychemon, a professional Script Doctor™ specializing in character psychology"
        
        # Load rules
        if rules_path:
            self.rules_path = Path(rules_path)
        else:
            self.rules_path = Path(__file__).parent.parent / "rules" / "character_psychology_rules.yaml"
        
        self.rules = self._load_rules()
        
        # Psychological markers
        self.emotion_words = [
            "feels", "thinks", "believes", "wants", "needs", "fears",
            "loves", "hates", "hopes", "dreams", "regrets", "remembers"
        ]
        
        self.defense_mechanisms = [
            "denies", "ignores", "rationalizes", "projects", "deflects",
            "avoids", "suppresses", "compensates", "displaces"
        ]
        
        self.growth_indicators = [
            "realizes", "understands", "learns", "changes", "grows",
            "accepts", "overcomes", "confronts", "embraces"
        ]
    
    def _load_rules(self) -> Dict[str, Any]:
        """Load rules from YAML file."""
        try:
            with open(self.rules_path, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"Warning: Could not load rules from {self.rules_path}: {e}")
            return {"rules": [], "psychology_checklist": {}}
    
    def analyze(self, screenplay_text: str) -> Dict[str, Any]:
        """
        Perform complete character psychology analysis of screenplay.
        
        Args:
            screenplay_text: The full screenplay text
        
        Returns:
            Complete psychological diagnostic report
        """
        # Extract characters
        characters = self._extract_characters(screenplay_text)
        
        # Build psychological profiles
        profiles = self._build_character_profiles(screenplay_text, characters)
        
        # Analyze psychological elements
        psych_elements = self._extract_psychological_elements(screenplay_text, characters)
        
        # Check internal conflicts
        internal_conflicts = self._analyze_internal_conflicts(screenplay_text, characters)
        
        # Analyze character consistency
        consistency_analysis = self._analyze_consistency(screenplay_text, profiles)
        
        # Check want vs need
        want_vs_need = self._analyze_want_vs_need(screenplay_text, characters)
        
        # Analyze emotional authenticity
        emotional_authenticity = self._analyze_emotional_authenticity(screenplay_text, profiles)
        
        # Check character voices
        voice_distinctiveness = self._analyze_voice_distinctiveness(screenplay_text, characters)
        
        # Analyze relationships
        relationships = self._analyze_relationships(screenplay_text, characters)
        
        # Check growth and pressure
        growth_analysis = self._analyze_character_growth(screenplay_text, profiles)
        
        # Check against rules
        rule_violations = self._check_psychology_rules(
            profiles, internal_conflicts, consistency_analysis,
            want_vs_need, emotional_authenticity, voice_distinctiveness
        )
        
        # Calculate score
        score = self._calculate_psychology_score(
            profiles, internal_conflicts, consistency_analysis,
            emotional_authenticity, rule_violations
        )
        
        # Generate diagnosis
        diagnosis = self._generate_diagnosis(
            score, profiles, internal_conflicts,
            consistency_analysis, rule_violations
        )
        
        # Get protagonist profile
        protagonist = self._identify_protagonist(profiles)
        
        # Prepare character list for backward compatibility
        character_list = []
        for name, profile in profiles.items():
            character_list.append({
                "name": name,
                "dialogue_count": profile.dialogue_count,
                "depth_score": profile.depth_score,
                "internal_conflicts": profile.internal_conflicts if profile.internal_conflicts else [],
                "arc_potential": "high" if profile.growth_evident else "low",
                "want": profile.want if profile.want else "unclear",
                "need": profile.need if profile.need else "unclear"
            })

        # Process relationships for better structure
        processed_relationships = []
        for rel in relationships:
            processed_relationships.append({
                "characters": rel["characters"],
                "type": rel["type"],
                "dynamics": ["conflict", "tension"] if rel["type"] == "antagonistic" else ["connection"]
            })

        return {
            "specialist": {
                "name": self.name,
                "title": self.title,
                "specialty": self.specialty
            },
            "score": score,
            "character_count": len(characters),
            "characters": character_list,  # Added for test compatibility
            "protagonist": protagonist.name if protagonist else "Unknown",
            "character_profiles": self._profiles_to_dict(profiles),
            "psychological_elements": self._elements_to_dict(psych_elements),
            "internal_conflicts_found": len(internal_conflicts),
            "internal_conflicts": internal_conflicts[:5],  # Top 5
            "internal_conflict_score": len(internal_conflicts) / max(len(characters), 1),  # Added
            "consistency_score": consistency_analysis["overall_consistency"],
            "inconsistencies": consistency_analysis["inconsistencies"],
            "want_vs_need_clear": want_vs_need["distinction_clear"],
            "want_vs_need_analysis": want_vs_need["analysis"],
            "want_need_score": 1.0 if want_vs_need["distinction_clear"] else 0.4,  # Added
            "emotional_authenticity_score": emotional_authenticity,
            "emotional_truth_score": emotional_authenticity,  # Added alias
            "voice_distinctiveness_score": voice_distinctiveness["overall_score"],
            "voice_distinctiveness": voice_distinctiveness["overall_score"],  # Added alias
            "identical_voices": voice_distinctiveness["identical_voices"],
            "relationships_analyzed": len(relationships),
            "relationships": processed_relationships,  # Changed key name
            "relationship_dynamics": relationships[:5],  # Top 5
            "character_growth_score": growth_analysis["overall_growth"],
            "growth_score": growth_analysis["overall_growth"],  # Added alias
            "characters_with_growth": growth_analysis["growing_characters"],
            "rule_violations": rule_violations,
            "diagnosis": diagnosis,
            "recommendations": self._generate_recommendations(
                score, rule_violations, profiles, internal_conflicts
            ),
            "signature": f"Diagnosed by {self.name}™"
        }
    
    def _extract_characters(self, screenplay: str) -> List[str]:
        """Extract character names from screenplay."""
        lines = screenplay.split('\n')
        characters = set()
        
        # Pattern for character names (all caps, not scene headings)
        for line in lines:
            line = line.strip()
            # Character name line: all caps, no periods, short
            if (line.isupper() and 
                len(line.split()) <= 3 and 
                not any(marker in line for marker in ['INT.', 'EXT.', 'FADE', 'CUT', 'DISSOLVE'])):
                
                # Remove parentheticals
                name = re.sub(r'\([^)]*\)', '', line).strip()
                if name and len(name) > 1:
                    characters.add(name)
        
        return sorted(list(characters))[:15]  # Limit to 15 main characters
    
    def _build_character_profiles(self, screenplay: str, characters: List[str]) -> Dict[str, CharacterProfile]:
        """Build psychological profiles for each character."""
        profiles = {}
        lines = screenplay.split('\n')
        
        for character in characters:
            # Count appearances and dialogue
            appearances = 0
            dialogue_count = 0
            dialogue_lines = []
            
            i = 0
            while i < len(lines):
                line = lines[i].strip()
                
                # Check for character name
                if line == character:
                    appearances += 1
                    # Collect dialogue
                    i += 1
                    while i < len(lines) and lines[i].strip() and not lines[i].strip().isupper():
                        if not lines[i].strip().startswith('('):  # Not parenthetical
                            dialogue_lines.append(lines[i].strip())
                            dialogue_count += 1
                        i += 1
                i += 1
            
            # Analyze character traits and psychology
            all_dialogue = ' '.join(dialogue_lines)
            
            # Extract character's internal conflicts
            char_conflicts = self._extract_character_conflicts(all_dialogue)

            # Extract want and need
            want, need = self._extract_want_and_need(all_dialogue, character)

            profiles[character] = CharacterProfile(
                name=character,
                appearances=appearances,
                dialogue_count=dialogue_count,
                has_internal_conflict=len(char_conflicts) > 0,
                consistency_score=self._calculate_consistency(character, screenplay),
                depth_score=self._calculate_depth(all_dialogue, dialogue_count),
                unique_voice_score=self._calculate_voice_uniqueness(all_dialogue, dialogue_lines),
                growth_evident=self._detect_growth(character, screenplay),
                vulnerability_shown=self._detect_vulnerability(all_dialogue),
                traits=self._extract_traits(all_dialogue),
                contradictions=self._find_contradictions(all_dialogue),
                relationships=self._map_relationships(character, screenplay),
                internal_conflicts=char_conflicts if char_conflicts else [],
                want=want,
                need=need
            )
        
        return profiles
    
    def _extract_character_conflicts(self, dialogue: str) -> List[str]:
        """Extract specific internal conflicts from character's dialogue."""
        conflicts = []
        dialogue_lower = dialogue.lower()

        # Conflict patterns
        if "can't" in dialogue_lower and ("but" in dialogue_lower or "want" in dialogue_lower):
            conflicts.append("Desire vs inability")
        if "should" in dialogue_lower and "but" in dialogue_lower:
            conflicts.append("Duty vs desire")
        if "love" in dialogue_lower and "hate" in dialogue_lower:
            conflicts.append("Love-hate relationship")
        if "want" in dialogue_lower and "need" in dialogue_lower:
            conflicts.append("Want vs need conflict")
        if "promise" in dialogue_lower and ("can't" in dialogue_lower or "sorry" in dialogue_lower):
            conflicts.append("Promise vs reality")

        return conflicts[:3]  # Return top 3 conflicts

    def _extract_want_and_need(self, dialogue: str, character: str) -> Tuple[Optional[str], Optional[str]]:
        """Extract what character wants vs what they need."""
        want = None
        need = None

        dialogue_lower = dialogue.lower()

        # Common want patterns
        if "i want" in dialogue_lower:
            want = "External goal or desire"
        elif "i need to" in dialogue_lower:
            want = "Immediate objective"
        elif "i have to" in dialogue_lower:
            want = "Perceived obligation"

        # Common need patterns (usually opposite of stated want)
        if "afraid" in dialogue_lower or "scared" in dialogue_lower:
            need = "Overcome fear"
        elif "alone" in dialogue_lower:
            need = "Connection"
        elif "sorry" in dialogue_lower or "forgive" in dialogue_lower:
            need = "Redemption"
        elif "promise" in dialogue_lower:
            need = "Self-acceptance"

        return want, need

    def _detect_internal_conflict(self, dialogue: str) -> bool:
        """Detect if character shows internal conflict."""
        if not dialogue:
            return False

        conflict_markers = [
            "but", "however", "torn", "can't decide", "don't know",
            "part of me", "should I", "what if", "confused", "conflicted"
        ]
        
        dialogue_lower = dialogue.lower()
        return sum(1 for marker in conflict_markers if marker in dialogue_lower) >= 2
    
    def _calculate_consistency(self, character: str, screenplay: str) -> float:
        """Calculate character consistency score."""
        lines = screenplay.split('\n')
        character_lines = []

        # Collect all character's dialogue and actions
        in_character_section = False
        for i, line in enumerate(lines):
            if line.strip() == character:
                in_character_section = True
                continue
            elif in_character_section:
                if line.strip() and not line.strip().isupper():
                    character_lines.append(line.strip())
                elif line.strip().isupper() and not line.startswith(' '):
                    in_character_section = False

        if len(character_lines) < 2:
            return 0.5  # Not enough data

        # Check for emotional consistency
        emotions_found = []
        contradictory_states = 0

        emotion_states = {
            'happy': ['happy', 'joy', 'excited', 'smile', 'laugh'],
            'sad': ['sad', 'cry', 'tears', 'depressed', 'sorrow'],
            'angry': ['angry', 'mad', 'furious', 'rage', 'hate'],
            'fearful': ['afraid', 'scared', 'terrified', 'fear', 'nervous']
        }

        for line in character_lines:
            line_lower = line.lower()
            for emotion, keywords in emotion_states.items():
                if any(keyword in line_lower for keyword in keywords):
                    emotions_found.append(emotion)

        # Check for rapid emotional switches (inconsistency)
        if len(emotions_found) > 1:
            for i in range(len(emotions_found) - 1):
                if emotions_found[i] != emotions_found[i + 1]:
                    # Different emotions back to back
                    if (emotions_found[i] == 'happy' and emotions_found[i + 1] == 'sad') or \
                       (emotions_found[i] == 'sad' and emotions_found[i + 1] == 'happy'):
                        contradictory_states += 1

        # Also check for presence throughout screenplay
        appearances = [i for i, line in enumerate(lines) if line.strip() == character]
        first_third = len(lines) // 3
        last_third = 2 * len(lines) // 3

        early = any(a < first_third for a in appearances)
        middle = any(first_third <= a < last_third for a in appearances)
        late = any(a >= last_third for a in appearances)

        presence_score = 0.8 if (early and middle and late) else 0.6 if ((early and middle) or (middle and late)) else 0.4

        # Penalize for contradictory emotional states
        consistency_penalty = min(contradictory_states * 0.2, 0.5)

        return max(0.2, presence_score - consistency_penalty)
    
    def _calculate_depth(self, dialogue: str, dialogue_count: int) -> float:
        """Calculate character depth score."""
        if dialogue_count < 5:
            return 0.2  # Too little dialogue
        
        depth_score = 0.3  # Base score
        
        # Check for emotional range
        emotions_expressed = sum(1 for word in self.emotion_words if word in dialogue.lower())
        if emotions_expressed > 3:
            depth_score += 0.2
        
        # Check for self-reflection
        reflection_markers = ["I think", "I feel", "I believe", "I wonder", "I realize"]
        if any(marker.lower() in dialogue.lower() for marker in reflection_markers):
            depth_score += 0.2
        
        # Check for complexity
        if "but" in dialogue.lower() or "however" in dialogue.lower():
            depth_score += 0.1
        
        # Check for backstory references
        if any(word in dialogue.lower() for word in ["remember", "used to", "once", "before"]):
            depth_score += 0.2
        
        return min(1.0, depth_score)
    
    def _calculate_voice_uniqueness(self, dialogue: str, dialogue_lines: List[str]) -> float:
        """Calculate how unique a character's voice is."""
        if not dialogue_lines:
            return 0.0
        
        # Check for unique speech patterns
        uniqueness_score = 0.5  # Base
        
        # Check average sentence length
        avg_length = sum(len(line.split()) for line in dialogue_lines) / max(1, len(dialogue_lines))
        
        # Unique if very short or very long
        if avg_length < 5 or avg_length > 15:
            uniqueness_score += 0.2
        
        # Check for unique phrases or verbal tics
        word_freq = Counter(dialogue.lower().split())
        
        # High frequency of certain words suggests verbal tics
        max_freq = max(word_freq.values()) if word_freq else 0
        if max_freq > 5:
            uniqueness_score += 0.2
        
        # Check formality level
        formal_words = ["perhaps", "therefore", "indeed", "shall", "whom"]
        informal_words = ["gonna", "wanna", "yeah", "nah", "kinda"]
        
        formal_count = sum(1 for word in formal_words if word in dialogue.lower())
        informal_count = sum(1 for word in informal_words if word in dialogue.lower())
        
        if formal_count > 2 or informal_count > 2:
            uniqueness_score += 0.1
        
        return min(1.0, uniqueness_score)
    
    def _detect_growth(self, character: str, screenplay: str) -> bool:
        """Detect if character shows growth."""
        lines = screenplay.split('\n')
        character_indices = [i for i, line in enumerate(lines) if line.strip() == character]
        
        if len(character_indices) < 2:
            return False
        
        # Get early and late dialogue
        early_dialogue = []
        late_dialogue = []
        
        midpoint = len(lines) // 2
        
        for idx in character_indices:
            if idx < midpoint:
                # Collect early dialogue
                i = idx + 1
                while i < len(lines) and lines[i].strip() and not lines[i].strip().isupper():
                    early_dialogue.append(lines[i])
                    i += 1
            else:
                # Collect late dialogue
                i = idx + 1
                while i < len(lines) and lines[i].strip() and not lines[i].strip().isupper():
                    late_dialogue.append(lines[i])
                    i += 1
        
        early_text = ' '.join(early_dialogue).lower()
        late_text = ' '.join(late_dialogue).lower()
        
        # Check for growth indicators in late dialogue
        growth_found = any(indicator in late_text for indicator in self.growth_indicators)
        
        # Check if perspective changed
        perspective_shift = (
            ("can't" in early_text and "can" in late_text) or
            ("won't" in early_text and "will" in late_text) or
            ("never" in early_text and "now" in late_text)
        )
        
        return growth_found or perspective_shift
    
    def _detect_vulnerability(self, dialogue: str) -> bool:
        """Detect if character shows vulnerability."""
        if not dialogue:
            return False
        
        vulnerability_markers = [
            "scared", "afraid", "worried", "sorry", "hurt", "pain",
            "lonely", "lost", "help", "need you", "don't know", "confused"
        ]
        
        dialogue_lower = dialogue.lower()
        return any(marker in dialogue_lower for marker in vulnerability_markers)
    
    def _extract_traits(self, dialogue: str) -> List[str]:
        """Extract character traits from dialogue."""
        traits = []
        dialogue_lower = dialogue.lower()
        
        # Determine traits based on dialogue patterns
        if dialogue_lower.count('!') > 5:
            traits.append("excitable")
        if dialogue_lower.count('?') > 5:
            traits.append("questioning")
        if "always" in dialogue_lower or "never" in dialogue_lower:
            traits.append("absolute thinker")
        if "maybe" in dialogue_lower or "perhaps" in dialogue_lower:
            traits.append("uncertain")
        if len(dialogue) > 500:
            traits.append("talkative")
        elif len(dialogue) < 100 and len(dialogue) > 0:
            traits.append("reserved")
        
        return traits[:5]  # Limit to 5 traits
    
    def _find_contradictions(self, dialogue: str) -> List[Tuple[str, str]]:
        """Find character contradictions that add depth."""
        contradictions = []
        dialogue_lower = dialogue.lower()
        
        # Look for contradiction patterns
        if "love" in dialogue_lower and "hate" in dialogue_lower:
            contradictions.append(("love", "hate"))
        if "strong" in dialogue_lower and ("weak" in dialogue_lower or "scared" in dialogue_lower):
            contradictions.append(("strong", "vulnerable"))
        if "sure" in dialogue_lower and "doubt" in dialogue_lower:
            contradictions.append(("certain", "doubtful"))
        
        return contradictions
    
    def _map_relationships(self, character: str, screenplay: str) -> Dict[str, str]:
        """Map character's relationships with others."""
        relationships = {}
        lines = screenplay.split('\n')
        
        # Find scenes where character appears
        character_indices = [i for i, line in enumerate(lines) if line.strip() == character]
        
        for idx in character_indices:
            # Look for other characters nearby
            window_start = max(0, idx - 10)
            window_end = min(len(lines), idx + 10)
            
            for i in range(window_start, window_end):
                line = lines[i].strip()
                if line.isupper() and line != character and len(line.split()) <= 3:
                    if not any(marker in line for marker in ['INT.', 'EXT.', 'FADE', 'CUT']):
                        other = line
                        if other not in relationships:
                            # Determine relationship type from context
                            context = ' '.join(lines[window_start:window_end]).lower()
                            if "love" in context:
                                relationships[other] = "romantic"
                            elif "fight" in context or "argue" in context:
                                relationships[other] = "conflict"
                            elif "friend" in context:
                                relationships[other] = "friendship"
                            else:
                                relationships[other] = "neutral"
        
        return relationships
    
    def _extract_psychological_elements(self, screenplay: str, characters: List[str]) -> List[PsychologicalElement]:
        """Extract psychological elements from screenplay."""
        elements = []
        lines = screenplay.split('\n')
        
        for i, line in enumerate(lines):
            line_lower = line.lower()
            page = (i // 55) + 1
            
            # Look for wants
            if "want" in line_lower or "need" in line_lower:
                for character in characters:
                    if character.lower() in line_lower:
                        elements.append(PsychologicalElement(
                            element_type="want" if "want" in line_lower else "need",
                            character=character,
                            description=line.strip()[:100],
                            page_revealed=page,
                            strength=0.7,
                            integrated=True
                        ))
                        break
            
            # Look for fears
            if any(fear_word in line_lower for fear_word in ["afraid", "scared", "fear"]):
                for character in characters:
                    if character.lower() in line_lower:
                        elements.append(PsychologicalElement(
                            element_type="fear",
                            character=character,
                            description=line.strip()[:100],
                            page_revealed=page,
                            strength=0.8,
                            integrated=True
                        ))
                        break
        
        return elements[:20]  # Limit to 20 elements
    
    def _analyze_internal_conflicts(self, screenplay: str, characters: List[str]) -> List[Dict[str, Any]]:
        """Analyze internal conflicts for all characters."""
        conflicts = []
        
        for character in characters:
            # Find character's dialogue
            lines = screenplay.split('\n')
            character_dialogue = []
            
            i = 0
            while i < len(lines):
                if lines[i].strip() == character:
                    i += 1
                    while i < len(lines) and lines[i].strip() and not lines[i].strip().isupper():
                        character_dialogue.append(lines[i].strip())
                        i += 1
                else:
                    i += 1
            
            dialogue = ' '.join(character_dialogue)
            
            # Detect conflicts
            if self._detect_internal_conflict(dialogue):
                conflicts.append({
                    "character": character,
                    "type": "want_vs_need" if "but" in dialogue.lower() else "internal_struggle",
                    "evidence": dialogue[:200] if dialogue else "No dialogue"
                })
        
        return conflicts
    
    def _analyze_consistency(self, screenplay: str, profiles: Dict[str, CharacterProfile]) -> Dict[str, Any]:
        """Analyze character consistency throughout screenplay."""
        overall_consistency = 0.0
        inconsistencies = []
        
        if profiles:
            consistency_scores = [p.consistency_score for p in profiles.values()]
            overall_consistency = sum(consistency_scores) / len(consistency_scores)
            
            # Find inconsistent characters
            for name, profile in profiles.items():
                if profile.consistency_score < 0.5:
                    inconsistencies.append({
                        "character": name,
                        "score": profile.consistency_score,
                        "issue": "Behavior inconsistent or limited presence"
                    })
        
        return {
            "overall_consistency": overall_consistency,
            "inconsistencies": inconsistencies[:5]  # Top 5
        }
    
    def _analyze_want_vs_need(self, screenplay: str, characters: List[str]) -> Dict[str, Any]:
        """Analyze want vs need distinction."""
        protagonist = characters[0] if characters else None
        
        if not protagonist:
            return {"distinction_clear": False, "analysis": "No protagonist identified"}
        
        # Look for want and need expressions
        lines = screenplay.split('\n')
        wants = []
        needs = []
        
        for i, line in enumerate(lines):
            if protagonist in line:
                # Check next few lines for want/need
                context = ' '.join(lines[i:min(i+5, len(lines))]).lower()
                if "want" in context:
                    wants.append(context[:100])
                if "need" in context:
                    needs.append(context[:100])
        
        distinction_clear = len(wants) > 0 and len(needs) > 0 and wants[0] != needs[0]
        
        return {
            "distinction_clear": distinction_clear,
            "analysis": {
                "wants_found": len(wants),
                "needs_found": len(needs),
                "protagonist": protagonist
            }
        }
    
    def _analyze_emotional_authenticity(self, screenplay: str, profiles: Dict[str, CharacterProfile]) -> float:
        """Analyze emotional authenticity across characters."""
        if not profiles:
            return 0.0
        
        authenticity_scores = []
        
        for profile in profiles.values():
            score = 0.5  # Base
            
            if profile.vulnerability_shown:
                score += 0.2
            if profile.has_internal_conflict:
                score += 0.2
            if len(profile.contradictions) > 0:
                score += 0.1
            
            authenticity_scores.append(score)
        
        return sum(authenticity_scores) / len(authenticity_scores)
    
    def _analyze_voice_distinctiveness(self, screenplay: str, characters: List[str]) -> Dict[str, Any]:
        """Analyze how distinct character voices are."""
        if len(characters) < 2:
            return {"overall_score": 0.5, "identical_voices": []}
        
        # Collect dialogue for each character
        character_dialogue = {}
        lines = screenplay.split('\n')
        
        for character in characters:
            dialogue = []
            i = 0
            while i < len(lines):
                if lines[i].strip() == character:
                    i += 1
                    while i < len(lines) and lines[i].strip() and not lines[i].strip().isupper():
                        dialogue.append(lines[i].strip())
                        i += 1
                else:
                    i += 1
            character_dialogue[character] = ' '.join(dialogue)
        
        # Compare voices
        identical_voices = []
        total_comparisons = 0
        distinct_count = 0
        
        characters_list = list(character_dialogue.keys())
        for i in range(len(characters_list)):
            for j in range(i+1, len(characters_list)):
                char1, char2 = characters_list[i], characters_list[j]
                dialogue1 = character_dialogue[char1]
                dialogue2 = character_dialogue[char2]
                
                if dialogue1 and dialogue2:
                    total_comparisons += 1
                    # Simple distinctiveness check
                    if self._voices_distinct(dialogue1, dialogue2):
                        distinct_count += 1
                    else:
                        identical_voices.append((char1, char2))
        
        overall_score = distinct_count / max(1, total_comparisons)
        
        return {
            "overall_score": overall_score,
            "identical_voices": identical_voices[:3]  # Top 3
        }
    
    def _voices_distinct(self, dialogue1: str, dialogue2: str) -> bool:
        """Check if two character voices are distinct."""
        # Simple heuristic - check for different patterns
        
        # Check sentence length difference
        words1 = dialogue1.split()
        words2 = dialogue2.split()
        
        if not words1 or not words2:
            return False
        
        avg_len1 = len(words1) / max(1, dialogue1.count('.'))
        avg_len2 = len(words2) / max(1, dialogue2.count('.'))
        
        # Distinct if very different average sentence lengths
        if abs(avg_len1 - avg_len2) > 5:
            return True
        
        # Check vocabulary overlap
        vocab1 = set(words1)
        vocab2 = set(words2)
        overlap = len(vocab1.intersection(vocab2))
        total = len(vocab1.union(vocab2))
        
        # Distinct if low vocabulary overlap
        if total > 0 and overlap / total < 0.5:
            return True
        
        return False
    
    def _analyze_relationships(self, screenplay: str, characters: List[str]) -> List[Dict[str, Any]]:
        """Analyze relationships between characters."""
        relationships = []
        lines = screenplay.split('\n')
        
        # Find scenes where characters interact
        for i in range(len(characters)):
            for j in range(i+1, len(characters)):
                char1, char2 = characters[i], characters[j]
                
                # Count co-occurrences
                interactions = 0
                relationship_type = "neutral"
                
                for k in range(len(lines) - 20):
                    window = lines[k:k+20]
                    window_text = ' '.join(window)
                    
                    if char1 in window_text and char2 in window_text:
                        interactions += 1
                        
                        # Determine relationship type
                        window_lower = window_text.lower()
                        if any(word in window_lower for word in ["love", "kiss", "embrace"]):
                            relationship_type = "romantic"
                        elif any(word in window_lower for word in ["fight", "argue", "hate"]):
                            relationship_type = "antagonistic"
                        elif any(word in window_lower for word in ["friend", "buddy", "pal"]):
                            relationship_type = "friendship"
                
                if interactions > 0:
                    relationships.append({
                        "characters": (char1, char2),
                        "interactions": interactions,
                        "type": relationship_type
                    })
        
        return sorted(relationships, key=lambda x: x["interactions"], reverse=True)
    
    def _analyze_character_growth(self, screenplay: str, profiles: Dict[str, CharacterProfile]) -> Dict[str, Any]:
        """Analyze character growth across screenplay."""
        growing_characters = []
        total_growth_score = 0.0
        
        for name, profile in profiles.items():
            if profile.growth_evident:
                growing_characters.append(name)
                total_growth_score += 1.0
        
        overall_growth = total_growth_score / max(1, len(profiles))
        
        return {
            "overall_growth": overall_growth,
            "growing_characters": growing_characters,
            "static_characters": [n for n in profiles.keys() if n not in growing_characters]
        }
    
    def _identify_protagonist(self, profiles: Dict[str, CharacterProfile]) -> Optional[CharacterProfile]:
        """Identify the protagonist based on presence and depth."""
        if not profiles:
            return None
        
        # Score each character
        scored = []
        for profile in profiles.values():
            score = (
                profile.appearances * 2 +
                profile.dialogue_count +
                profile.depth_score * 10 +
                (5 if profile.has_internal_conflict else 0) +
                (5 if profile.growth_evident else 0)
            )
            scored.append((score, profile))
        
        # Return highest scoring character
        scored.sort(key=lambda x: x[0], reverse=True)
        return scored[0][1] if scored else None
    
    def _check_psychology_rules(self, profiles: Dict, conflicts: List,
                               consistency: Dict, want_need: Dict,
                               authenticity: float, distinctiveness: Dict) -> List[Dict]:
        """Check character psychology against rules."""
        violations = []
        
        for rule in self.rules.get("rules", []):
            if rule["id"] == "PSYCH.R001":
                # Psychological consistency
                if consistency["overall_consistency"] < 0.6:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": f"Low consistency: {consistency['overall_consistency']:.0%}",
                        "fix": rule["fix"]
                    })
            
            elif rule["id"] == "PSYCH.R002":
                # Internal conflict
                if len(conflicts) == 0:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": "No internal conflicts found",
                        "fix": rule["fix"]
                    })
            
            elif rule["id"] == "PSYCH.R004":
                # Emotional authenticity
                if authenticity < 0.5:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": f"Low emotional authenticity: {authenticity:.0%}",
                        "fix": rule["fix"]
                    })
            
            elif rule["id"] == "PSYCH.R007":
                # Want vs need
                if not want_need["distinction_clear"]:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": "Want equals need - weak character arc",
                        "fix": rule["fix"]
                    })
            
            elif rule["id"] == "PSYCH.R008":
                # Unique voices
                if distinctiveness["overall_score"] < 0.5:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": "Characters have similar voices",
                        "fix": rule["fix"]
                    })
        
        return violations
    
    def _calculate_psychology_score(self, profiles: Dict, conflicts: List,
                                   consistency: Dict, authenticity: float,
                                   violations: List) -> float:
        """Calculate overall character psychology score."""
        score = 100.0
        
        # Deduct for violations
        for violation in violations:
            if violation["severity"] == "critical":
                score -= 20
            elif violation["severity"] == "high":
                score -= 15
            elif violation["severity"] == "medium":
                score -= 8
            else:
                score -= 4
        
        # Factor in consistency
        score = score * 0.7 + (consistency["overall_consistency"] * 100) * 0.1
        
        # Factor in authenticity
        score = score * 0.8 + (authenticity * 100) * 0.1
        
        # Factor in depth
        if profiles:
            avg_depth = sum(p.depth_score for p in profiles.values()) / len(profiles)
            score = score * 0.9 + (avg_depth * 100) * 0.1
        
        return max(0, min(100, round(score, 1)))
    
    def _profiles_to_dict(self, profiles: Dict[str, CharacterProfile]) -> List[Dict]:
        """Convert character profiles to dictionary format."""
        result = []
        
        for name, profile in list(profiles.items())[:5]:  # Top 5 characters
            result.append({
                "name": name,
                "appearances": profile.appearances,
                "dialogue_count": profile.dialogue_count,
                "has_internal_conflict": profile.has_internal_conflict,
                "consistency_score": round(profile.consistency_score, 2),
                "depth_score": round(profile.depth_score, 2),
                "unique_voice_score": round(profile.unique_voice_score, 2),
                "growth_evident": profile.growth_evident,
                "vulnerability_shown": profile.vulnerability_shown,
                "traits": profile.traits,
                "contradictions": [f"{c[0]} vs {c[1]}" for c in profile.contradictions]
            })
        
        return result
    
    def _elements_to_dict(self, elements: List[PsychologicalElement]) -> List[Dict]:
        """Convert psychological elements to dictionary format."""
        return [
            {
                "type": e.element_type,
                "character": e.character,
                "description": e.description,
                "page": e.page_revealed,
                "strength": round(e.strength, 2)
            }
            for e in elements[:10]  # Top 10
        ]
    
    def _generate_diagnosis(self, score: float, profiles: Dict,
                          conflicts: List, consistency: Dict,
                          violations: List) -> str:
        """Generate psychological diagnosis."""
        diagnosis = f"Character Psychology Score: {score}/100\n\n"
        
        # Overall assessment
        if score >= 85:
            diagnosis += "Excellent character psychology! Deep, consistent, and authentic characters. "
        elif score >= 70:
            diagnosis += "Good character development with some psychological depth. "
        elif score >= 50:
            diagnosis += "Character psychology needs work - lacking depth or consistency. "
        else:
            diagnosis += "Major character psychology problems - flat or inconsistent characters. "
        
        # Specific issues
        if len(conflicts) == 0:
            diagnosis += "No internal conflicts found - characters lack inner struggle. "
        
        if consistency["overall_consistency"] < 0.6:
            diagnosis += "Character behavior inconsistent throughout screenplay. "
        
        # Character count
        if len(profiles) > 10:
            diagnosis += f"Too many characters ({len(profiles)}) - consider consolidating. "
        elif len(profiles) < 3:
            diagnosis += "Very few developed characters - screenplay may feel thin. "
        
        # Critical issues
        critical = [v for v in violations if v["severity"] == "critical"]
        if critical:
            diagnosis += f"Critical issues: {', '.join([v['title'] for v in critical])}."
        
        return diagnosis
    
    def _generate_recommendations(self, score: float, violations: List,
                                 profiles: Dict, conflicts: List) -> List[str]:
        """Generate specific psychology recommendations."""
        recommendations = []
        
        # Top violations
        for violation in sorted(violations,
                              key=lambda x: {"critical": 0, "high": 1, "medium": 2}.get(x["severity"], 3)):
            recommendations.append(f"[{violation['severity'].upper()}] {violation['fix']}")
            if len(recommendations) >= 3:
                break
        
        # Specific issues
        if len(conflicts) == 0:
            recommendations.append("Add internal conflict between want and need")
        
        # Check for flat characters
        flat_chars = [n for n, p in profiles.items() if p.depth_score < 0.5]
        if flat_chars:
            recommendations.append(f"Deepen {flat_chars[0]} with backstory and internal conflict")
        
        # Voice issues
        similar_voices = [n for n, p in profiles.items() if p.unique_voice_score < 0.5]
        if len(similar_voices) > 2:
            recommendations.append("Differentiate character voices with unique speech patterns")
        
        # General advice
        if score < 70:
            recommendations.append("Study character psychology in acclaimed screenplays")
            recommendations.append("Create detailed character biographies before writing")
        
        return recommendations[:5]  # Limit to 5