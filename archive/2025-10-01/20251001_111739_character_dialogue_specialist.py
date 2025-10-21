"""
Script Doctor Dialoguemon - Character Dialogue and Voice Specialist
A Script Doctor™ in Digimon form specializing in dialogue authenticity and character voice.
"""

import re
import yaml
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass
from collections import defaultdict, Counter
import string


@dataclass
class DialogueAnalysis:
    """Analysis of a single dialogue exchange."""
    character: str
    line: str
    word_count: int
    avg_word_length: float
    sentence_patterns: List[str]
    has_subtext: bool
    emotional_tone: str
    serves_purpose: bool
    natural_score: float  # 0-1


@dataclass
class CharacterVoice:
    """Voice profile for a character."""
    name: str
    total_lines: int
    avg_words_per_line: float
    vocabulary_complexity: float  # 0-1
    unique_phrases: List[str]
    verbal_tics: List[str]
    speech_patterns: Dict[str, int]  # pattern -> count
    formality_level: str  # formal, casual, mixed
    emotional_range: List[str]
    distinctiveness_score: float  # 0-1


class DrDialogue:
    """
    Script Doctor Dialoguemon - The Character Dialogue and Voice Specialist

    A Script Doctor™ in Digimon form, specializing in analyzing dialogue authenticity,
    character voice distinction, subtext, and natural speech patterns.

    Identity: Script Doctor first, Digimon dialogue specialist second.
    """

    def __init__(self, rules_path: str = None):
        """Initialize Script Doctor Dialoguemon with rules and configuration."""
        self.name = "Script Doctor Dialoguemon"
        self.digimon_name = "Dialoguemon"
        self.title = "Script Doctor - Character Dialogue and Voice Specialist"
        self.specialty = "Dialogue authenticity, character voice, subtext, natural speech patterns"
        self.identity = "I am Script Doctor Dialoguemon, a professional Script Doctor™ specializing in dialogue authenticity"

        # Load rules
        if rules_path:
            self.rules_path = Path(rules_path)
        else:
            self.rules_path = Path(__file__).parent.parent / "rules" / "character_dialogue_rules.yaml"

        self.rules = self._load_rules()

        # Dialogue analysis patterns
        self.exposition_markers = [
            "as you know", "remember when", "let me explain",
            "the truth is", "what happened was", "you see"
        ]

        self.on_the_nose_phrases = [
            "i feel", "i think", "i am angry", "i am sad",
            "i hate you", "i love you", "this makes me"
        ]

        self.cliche_phrases = [
            "we need to talk", "it's not what it looks like",
            "i can explain", "this isn't over", "you'll pay for this",
            "we've got company", "it's quiet... too quiet"
        ]

        self.natural_speech_markers = [
            "um", "uh", "well", "like", "you know", "i mean",
            "...", "--", "gonna", "wanna", "gotta", "'cause"
        ]

        self.conflict_words = [
            "but", "however", "no", "wrong", "disagree",
            "actually", "instead", "rather", "versus"
        ]

    def _load_rules(self) -> Dict:
        """Load rules from YAML file."""
        if self.rules_path.exists():
            with open(self.rules_path, 'r') as f:
                return yaml.safe_load(f)
        return {}

    def analyze(self, screenplay_text: str) -> Dict[str, Any]:
        """
        Analyze dialogue and character voices in screenplay.

        Args:
            screenplay_text: The full screenplay text

        Returns:
            Complete dialogue diagnostic report
        """
        # Extract all dialogue
        dialogue_exchanges = self._extract_dialogue(screenplay_text)

        # Build voice profiles
        voice_profiles = self._build_voice_profiles(dialogue_exchanges)

        # Analyze dialogue authenticity
        authenticity_score = self._analyze_authenticity(dialogue_exchanges)

        # Check voice distinctiveness
        distinctiveness = self._analyze_voice_distinctiveness(voice_profiles)

        # Detect subtext
        subtext_analysis = self._analyze_subtext(dialogue_exchanges)

        # Check for exposition dumps
        exposition_issues = self._detect_exposition_dumps(dialogue_exchanges)

        # Analyze dialogue purpose
        purpose_analysis = self._analyze_dialogue_purpose(dialogue_exchanges)

        # Check natural flow
        natural_flow = self._analyze_natural_flow(dialogue_exchanges)

        # Detect clichés
        cliches_found = self._detect_cliches(dialogue_exchanges)

        # Analyze conflict in dialogue
        conflict_score = self._analyze_dialogue_conflict(dialogue_exchanges)

        # Check white space balance
        white_space = self._analyze_white_space(screenplay_text)

        # Power dynamics
        power_dynamics = self._analyze_power_dynamics(dialogue_exchanges)

        # Find memorable lines
        memorable_lines = self._find_memorable_lines(dialogue_exchanges)

        # Check against rules
        rule_violations = self._check_dialogue_rules(
            authenticity_score, distinctiveness, subtext_analysis,
            exposition_issues, natural_flow, conflict_score
        )

        # Calculate score
        score = self._calculate_dialogue_score(
            authenticity_score, distinctiveness, subtext_analysis,
            natural_flow, rule_violations
        )

        # Generate diagnosis
        diagnosis = self._generate_diagnosis(
            score, voice_profiles, authenticity_score,
            subtext_analysis, rule_violations
        )

        return {
            "specialist": {
                "name": self.name,
                "title": self.title,
                "specialty": self.specialty
            },
            "score": score,
            "total_dialogue_lines": len(dialogue_exchanges),
            "character_count": len(voice_profiles),
            "voice_profiles": self._profiles_to_dict(voice_profiles),
            "authenticity_score": authenticity_score,
            "natural_speech_score": natural_flow["score"],
            "voice_distinctiveness": distinctiveness["overall_score"],
            "identical_voices": distinctiveness["identical_pairs"],
            "subtext_present": subtext_analysis["has_subtext"],
            "subtext_score": subtext_analysis["score"],
            "exposition_dumps": len(exposition_issues),
            "exposition_issues": exposition_issues[:3],  # Top 3
            "on_the_nose_count": subtext_analysis["on_the_nose_count"],
            "dialogue_serves_purpose": purpose_analysis["percentage_purposeful"],
            "empty_dialogue_lines": purpose_analysis["empty_lines"],
            "conflict_in_dialogue": conflict_score,
            "cliches_found": len(cliches_found),
            "cliche_examples": cliches_found[:5],  # Top 5
            "white_space_score": white_space["score"],
            "avg_speech_length": white_space["avg_length"],
            "power_dynamics_present": power_dynamics["present"],
            "memorable_lines_count": len(memorable_lines),
            "memorable_lines": memorable_lines[:3],  # Top 3
            "rule_violations": rule_violations,
            "diagnosis": diagnosis,
            "recommendations": self._generate_recommendations(
                score, rule_violations, voice_profiles,
                subtext_analysis, natural_flow
            ),
            "signature": f"Diagnosed by {self.name}™"
        }

    def _extract_dialogue(self, screenplay: str) -> List[DialogueAnalysis]:
        """Extract and analyze all dialogue from screenplay."""
        lines = screenplay.split('\n')
        dialogue_list = []

        i = 0
        while i < len(lines):
            line = lines[i].strip()

            # Check if it's a character name (all caps, not a scene heading)
            if (line.isupper() and
                len(line.split()) <= 3 and
                not any(marker in line for marker in ['INT.', 'EXT.', 'FADE', 'CUT', 'DISSOLVE'])):

                character = line.split('(')[0].strip()  # Remove parentheticals

                # Collect dialogue lines
                i += 1
                dialogue_text = []

                while i < len(lines) and lines[i].strip():
                    next_line = lines[i].strip()

                    # Stop if we hit another character or scene heading
                    if next_line.isupper() and not next_line.startswith('('):
                        break

                    # Skip parentheticals
                    if not next_line.startswith('('):
                        dialogue_text.append(next_line)

                    i += 1

                # Analyze this dialogue
                if dialogue_text:
                    full_dialogue = ' '.join(dialogue_text)
                    dialogue_list.append(self._analyze_single_dialogue(character, full_dialogue))

            i += 1

        return dialogue_list

    def _analyze_single_dialogue(self, character: str, text: str) -> DialogueAnalysis:
        """Analyze a single piece of dialogue."""
        words = text.split()
        word_count = len(words)

        # Calculate average word length
        avg_word_length = sum(len(w.strip(string.punctuation)) for w in words) / max(word_count, 1)

        # Detect sentence patterns
        patterns = []
        if '?' in text:
            patterns.append('question')
        if '!' in text:
            patterns.append('exclamation')
        if '...' in text or '--' in text:
            patterns.append('interrupted')
        if len([w for w in words if w[0].isupper()]) > word_count * 0.3:
            patterns.append('emphatic')

        # Check for subtext (if saying one thing but meaning another)
        has_subtext = self._detect_subtext_in_line(text)

        # Determine emotional tone
        emotional_tone = self._detect_emotional_tone(text)

        # Check if serves purpose
        serves_purpose = self._line_serves_purpose(text)

        # Calculate natural score
        natural_score = self._calculate_natural_score(text)

        return DialogueAnalysis(
            character=character,
            line=text,
            word_count=word_count,
            avg_word_length=avg_word_length,
            sentence_patterns=patterns,
            has_subtext=has_subtext,
            emotional_tone=emotional_tone,
            serves_purpose=serves_purpose,
            natural_score=natural_score
        )

    def _detect_subtext_in_line(self, text: str) -> bool:
        """Detect if line has subtext."""
        text_lower = text.lower()

        # Direct statements usually lack subtext
        if any(phrase in text_lower for phrase in self.on_the_nose_phrases):
            return False

        # Indirect language suggests subtext
        subtext_markers = [
            "maybe", "perhaps", "i guess", "if you say so",
            "whatever", "fine", "great", "perfect", "sure"
        ]

        return any(marker in text_lower for marker in subtext_markers)

    def _detect_emotional_tone(self, text: str) -> str:
        """Detect emotional tone of dialogue."""
        text_lower = text.lower()

        if any(word in text_lower for word in ["angry", "hate", "furious", "damn"]):
            return "angry"
        elif any(word in text_lower for word in ["love", "care", "miss", "want"]):
            return "loving"
        elif any(word in text_lower for word in ["afraid", "scared", "worry", "nervous"]):
            return "fearful"
        elif any(word in text_lower for word in ["sad", "sorry", "regret", "wish"]):
            return "sad"
        elif "?" in text:
            return "curious"
        elif "!" in text:
            return "emphatic"
        else:
            return "neutral"

    def _line_serves_purpose(self, text: str) -> bool:
        """Check if dialogue line serves a purpose."""
        text_lower = text.lower()

        # Empty pleasantries often don't serve purpose
        empty_phrases = [
            "how are you", "i'm fine", "nice weather",
            "good morning", "good night", "see you later"
        ]

        if any(phrase in text_lower for phrase in empty_phrases):
            return False

        # Line likely serves purpose if it has:
        # - Conflict words
        # - Emotional content
        # - Questions
        # - Commands
        # - Information

        has_content = (
            any(word in text_lower for word in self.conflict_words) or
            len(text.split()) > 5 or
            '?' in text or
            '!' in text
        )

        return has_content

    def _calculate_natural_score(self, text: str) -> float:
        """Calculate how natural the dialogue sounds."""
        score = 0.5  # Base score
        text_lower = text.lower()

        # Natural markers increase score
        natural_count = sum(1 for marker in self.natural_speech_markers
                          if marker in text_lower)
        score += min(natural_count * 0.1, 0.3)

        # Contractions increase naturalness
        contractions = ["don't", "won't", "can't", "i'm", "you're", "we're", "it's"]
        contraction_count = sum(1 for c in contractions if c in text_lower)
        score += min(contraction_count * 0.05, 0.2)

        # Overly formal language decreases naturalness
        formal_words = ["therefore", "moreover", "nevertheless", "furthermore"]
        formal_count = sum(1 for word in formal_words if word in text_lower)
        score -= formal_count * 0.1

        return max(0.0, min(1.0, score))

    def _build_voice_profiles(self, dialogues: List[DialogueAnalysis]) -> Dict[str, CharacterVoice]:
        """Build voice profiles for each character."""
        profiles = {}
        character_dialogues = defaultdict(list)

        # Group dialogues by character
        for d in dialogues:
            character_dialogues[d.character].append(d)

        # Build profile for each character
        for character, char_dialogues in character_dialogues.items():
            total_lines = len(char_dialogues)

            # Calculate average words per line
            avg_words = sum(d.word_count for d in char_dialogues) / max(total_lines, 1)

            # Calculate vocabulary complexity
            all_words = []
            for d in char_dialogues:
                all_words.extend(d.line.lower().split())

            unique_words = set(all_words)
            complexity = len(unique_words) / max(len(all_words), 1)

            # Find unique phrases (2-3 word combinations used multiple times)
            phrases = self._extract_unique_phrases(char_dialogues)

            # Detect verbal tics
            verbal_tics = self._detect_verbal_tics(char_dialogues)

            # Analyze speech patterns
            patterns = Counter()
            for d in char_dialogues:
                for pattern in d.sentence_patterns:
                    patterns[pattern] += 1

            # Determine formality level
            formality = self._determine_formality(char_dialogues)

            # Collect emotional range
            emotions = list(set(d.emotional_tone for d in char_dialogues))

            # Calculate distinctiveness
            distinctiveness = self._calculate_voice_distinctiveness(
                avg_words, complexity, phrases, verbal_tics, patterns
            )

            profiles[character] = CharacterVoice(
                name=character,
                total_lines=total_lines,
                avg_words_per_line=avg_words,
                vocabulary_complexity=complexity,
                unique_phrases=phrases[:5],  # Top 5
                verbal_tics=verbal_tics,
                speech_patterns=dict(patterns),
                formality_level=formality,
                emotional_range=emotions,
                distinctiveness_score=distinctiveness
            )

        return profiles

    def _extract_unique_phrases(self, dialogues: List[DialogueAnalysis]) -> List[str]:
        """Extract unique phrases used by character."""
        phrase_counts = Counter()

        for d in dialogues:
            words = d.line.lower().split()
            # Extract 2-3 word phrases
            for i in range(len(words) - 1):
                phrase_2 = ' '.join(words[i:i+2])
                phrase_counts[phrase_2] += 1

                if i < len(words) - 2:
                    phrase_3 = ' '.join(words[i:i+3])
                    phrase_counts[phrase_3] += 1

        # Return phrases used more than once
        repeated = [phrase for phrase, count in phrase_counts.items() if count > 1]
        return sorted(repeated, key=lambda x: phrase_counts[x], reverse=True)

    def _detect_verbal_tics(self, dialogues: List[DialogueAnalysis]) -> List[str]:
        """Detect verbal tics in character's speech."""
        tic_counts = Counter()

        tics_to_check = [
            "you know", "i mean", "like", "right?", "okay?",
            "actually", "basically", "literally", "honestly"
        ]

        for d in dialogues:
            text_lower = d.line.lower()
            for tic in tics_to_check:
                if tic in text_lower:
                    tic_counts[tic] += 1

        # Return tics used more than twice
        return [tic for tic, count in tic_counts.items() if count > 2]

    def _determine_formality(self, dialogues: List[DialogueAnalysis]) -> str:
        """Determine character's formality level."""
        formal_count = 0
        casual_count = 0

        for d in dialogues:
            text_lower = d.line.lower()

            # Formal markers
            if any(word in text_lower for word in ["therefore", "however", "indeed"]):
                formal_count += 1

            # Casual markers
            if any(word in text_lower for word in ["gonna", "wanna", "yeah", "nah"]):
                casual_count += 1

        total = len(dialogues)
        if formal_count > total * 0.3:
            return "formal"
        elif casual_count > total * 0.3:
            return "casual"
        else:
            return "mixed"

    def _calculate_voice_distinctiveness(self, avg_words: float, complexity: float,
                                        phrases: List[str], tics: List[str],
                                        patterns: Counter) -> float:
        """Calculate how distinctive a character's voice is."""
        score = 0.0

        # Unique vocabulary adds distinctiveness
        score += min(complexity * 2, 0.3)

        # Unique phrases add distinctiveness
        score += min(len(phrases) * 0.02, 0.2)

        # Verbal tics add distinctiveness
        score += min(len(tics) * 0.1, 0.2)

        # Varied speech patterns add distinctiveness
        score += min(len(patterns) * 0.1, 0.3)

        return min(1.0, score)

    def _analyze_authenticity(self, dialogues: List[DialogueAnalysis]) -> float:
        """Analyze overall dialogue authenticity."""
        if not dialogues:
            return 0.0

        natural_scores = [d.natural_score for d in dialogues]
        return sum(natural_scores) / len(natural_scores)

    def _analyze_voice_distinctiveness(self, profiles: Dict[str, CharacterVoice]) -> Dict[str, Any]:
        """Analyze how distinct character voices are."""
        if len(profiles) < 2:
            return {
                "overall_score": 0.5,
                "identical_pairs": []
            }

        scores = [p.distinctiveness_score for p in profiles.values()]
        overall = sum(scores) / len(scores)

        # Find characters with similar voices
        identical_pairs = []
        profile_list = list(profiles.values())

        for i in range(len(profile_list)):
            for j in range(i + 1, len(profile_list)):
                similarity = self._calculate_voice_similarity(
                    profile_list[i], profile_list[j]
                )
                if similarity > 0.8:  # Very similar
                    identical_pairs.append(
                        (profile_list[i].name, profile_list[j].name)
                    )

        return {
            "overall_score": overall,
            "identical_pairs": identical_pairs
        }

    def _calculate_voice_similarity(self, voice1: CharacterVoice, voice2: CharacterVoice) -> float:
        """Calculate similarity between two character voices."""
        similarity = 0.0

        # Similar word count
        if abs(voice1.avg_words_per_line - voice2.avg_words_per_line) < 3:
            similarity += 0.25

        # Similar complexity
        if abs(voice1.vocabulary_complexity - voice2.vocabulary_complexity) < 0.1:
            similarity += 0.25

        # Same formality
        if voice1.formality_level == voice2.formality_level:
            similarity += 0.25

        # Overlapping verbal tics
        common_tics = set(voice1.verbal_tics) & set(voice2.verbal_tics)
        if common_tics:
            similarity += 0.25

        return similarity

    def _analyze_subtext(self, dialogues: List[DialogueAnalysis]) -> Dict[str, Any]:
        """Analyze subtext in dialogue."""
        with_subtext = sum(1 for d in dialogues if d.has_subtext)
        on_the_nose = 0

        for d in dialogues:
            if any(phrase in d.line.lower() for phrase in self.on_the_nose_phrases):
                on_the_nose += 1

        total = len(dialogues)

        return {
            "has_subtext": with_subtext > total * 0.3,
            "score": with_subtext / max(total, 1),
            "on_the_nose_count": on_the_nose,
            "percentage_with_subtext": (with_subtext / max(total, 1)) * 100
        }

    def _detect_exposition_dumps(self, dialogues: List[DialogueAnalysis]) -> List[Dict[str, Any]]:
        """Detect exposition dumps in dialogue."""
        dumps = []

        for d in dialogues:
            text_lower = d.line.lower()

            # Check for exposition markers
            if any(marker in text_lower for marker in self.exposition_markers):
                dumps.append({
                    "character": d.character,
                    "line": d.line[:100] + "..." if len(d.line) > 100 else d.line,
                    "issue": "Exposition marker detected"
                })

            # Check for overly long explanatory dialogue
            elif d.word_count > 50 and "because" in text_lower:
                dumps.append({
                    "character": d.character,
                    "line": d.line[:100] + "..." if len(d.line) > 100 else d.line,
                    "issue": "Long explanatory dialogue"
                })

        return dumps

    def _analyze_dialogue_purpose(self, dialogues: List[DialogueAnalysis]) -> Dict[str, Any]:
        """Analyze if dialogue serves purpose."""
        purposeful = sum(1 for d in dialogues if d.serves_purpose)
        empty = [d for d in dialogues if not d.serves_purpose]

        return {
            "percentage_purposeful": (purposeful / max(len(dialogues), 1)) * 100,
            "empty_lines": len(empty),
            "empty_examples": [e.line[:50] for e in empty[:3]]  # First 3
        }

    def _analyze_natural_flow(self, dialogues: List[DialogueAnalysis]) -> Dict[str, Any]:
        """Analyze natural flow of dialogue."""
        scores = [d.natural_score for d in dialogues]

        return {
            "score": sum(scores) / max(len(scores), 1) if scores else 0.0,
            "highly_natural": sum(1 for s in scores if s > 0.7),
            "unnatural": sum(1 for s in scores if s < 0.3)
        }

    def _detect_cliches(self, dialogues: List[DialogueAnalysis]) -> List[str]:
        """Detect clichéd dialogue."""
        cliches = []

        for d in dialogues:
            text_lower = d.line.lower()
            for cliche in self.cliche_phrases:
                if cliche in text_lower:
                    cliches.append(f"{d.character}: \"{cliche}\"")

        return cliches

    def _analyze_dialogue_conflict(self, dialogues: List[DialogueAnalysis]) -> float:
        """Analyze presence of conflict in dialogue."""
        conflict_lines = 0

        for d in dialogues:
            text_lower = d.line.lower()
            if any(word in text_lower for word in self.conflict_words):
                conflict_lines += 1

        return conflict_lines / max(len(dialogues), 1)

    def _analyze_white_space(self, screenplay: str) -> Dict[str, Any]:
        """Analyze white space balance in dialogue."""
        lines = screenplay.split('\n')
        speech_lengths = []

        in_dialogue = False
        current_speech = 0

        for line in lines:
            line = line.strip()

            if line.isupper() and len(line.split()) <= 3 and \
               not any(m in line for m in ['INT.', 'EXT.', 'FADE', 'CUT']):
                if in_dialogue and current_speech > 0:
                    speech_lengths.append(current_speech)
                in_dialogue = True
                current_speech = 0
            elif in_dialogue and line and not line.startswith('('):
                current_speech += len(line.split())
            elif not line and in_dialogue:
                if current_speech > 0:
                    speech_lengths.append(current_speech)
                in_dialogue = False
                current_speech = 0

        if not speech_lengths:
            return {"score": 0.5, "avg_length": 0, "max_length": 0}

        avg_length = sum(speech_lengths) / len(speech_lengths)
        max_length = max(speech_lengths)

        # Good balance: average 10-20 words, max under 50
        score = 1.0
        if avg_length > 30:
            score -= 0.3
        if max_length > 75:
            score -= 0.3
        if avg_length < 5:
            score -= 0.2

        return {
            "score": max(0.0, score),
            "avg_length": avg_length,
            "max_length": max_length
        }

    def _analyze_power_dynamics(self, dialogues: List[DialogueAnalysis]) -> Dict[str, Any]:
        """Analyze power dynamics in dialogue."""
        power_indicators = {
            "commands": ["do it", "get me", "i want", "you will", "must"],
            "deferrals": ["yes sir", "of course", "right away", "as you wish"],
            "challenges": ["who says", "says who", "make me", "or what"]
        }

        dynamics_found = False
        examples = []

        for d in dialogues:
            text_lower = d.line.lower()

            for dynamic_type, phrases in power_indicators.items():
                if any(phrase in text_lower for phrase in phrases):
                    dynamics_found = True
                    if len(examples) < 3:
                        examples.append({
                            "character": d.character,
                            "type": dynamic_type,
                            "line": d.line[:50]
                        })

        return {
            "present": dynamics_found,
            "examples": examples
        }

    def _find_memorable_lines(self, dialogues: List[DialogueAnalysis]) -> List[str]:
        """Find potentially memorable dialogue lines."""
        memorable = []

        for d in dialogues:
            # Memorable lines are often:
            # - Short and punchy (5-15 words)
            # - Contain strong emotion
            # - Have unique phrasing
            # - Contain thematic weight

            if 5 <= d.word_count <= 15:
                if d.emotional_tone in ["angry", "loving", "emphatic"]:
                    memorable.append(f"{d.character}: {d.line}")
                elif any(pattern in d.sentence_patterns for pattern in ["exclamation", "emphatic"]):
                    memorable.append(f"{d.character}: {d.line}")

        return memorable[:10]  # Top 10

    def _check_dialogue_rules(self, authenticity: float, distinctiveness: Dict,
                             subtext: Dict, exposition: List, natural: Dict,
                             conflict: float) -> List[Dict]:
        """Check dialogue against rules."""
        violations = []

        for rule in self.rules.get("rules", []):
            if rule["id"] == "DIAL.R001":
                # Natural speech patterns
                if natural["score"] < 0.5:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": f"Low natural speech score: {natural['score']:.0%}",
                        "fix": rule["fix"]
                    })

            elif rule["id"] == "DIAL.R002":
                # Distinct character voices
                if distinctiveness["overall_score"] < 0.5:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": "Characters have similar voices",
                        "fix": rule["fix"]
                    })

            elif rule["id"] == "DIAL.R003":
                # Subtext present
                if not subtext["has_subtext"]:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": f"Only {subtext['percentage_with_subtext']:.0f}% has subtext",
                        "fix": rule["fix"]
                    })

            elif rule["id"] == "DIAL.R004":
                # Avoid on-the-nose
                if subtext["on_the_nose_count"] > 10:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": f"{subtext['on_the_nose_count']} on-the-nose lines found",
                        "fix": rule["fix"]
                    })

            elif rule["id"] == "DIAL.R007":
                # Conflict in conversation
                if conflict < 0.2:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": "Little conflict in dialogue",
                        "fix": rule["fix"]
                    })

            elif rule["id"] == "DIAL.R008":
                # Avoid exposition dumps
                if len(exposition) > 5:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": f"{len(exposition)} exposition dumps detected",
                        "fix": rule["fix"]
                    })

        return violations

    def _calculate_dialogue_score(self, authenticity: float, distinctiveness: Dict,
                                 subtext: Dict, natural: Dict, violations: List) -> float:
        """Calculate overall dialogue score."""
        score = 100.0

        # Deduct for violations
        for violation in violations:
            if violation["severity"] == "critical":
                score -= 20
            elif violation["severity"] == "high":
                score -= 15
            elif violation["severity"] == "medium":
                score -= 8
            elif violation["severity"] == "low":
                score -= 5

        # Bonus for excellence
        if authenticity > 0.8:
            score += 5
        if distinctiveness["overall_score"] > 0.8:
            score += 5
        if subtext["score"] > 0.7:
            score += 5

        return max(0.0, min(100.0, score))

    def _generate_diagnosis(self, score: float, profiles: Dict, authenticity: float,
                          subtext: Dict, violations: List) -> str:
        """Generate diagnosis summary."""
        if score >= 80:
            level = "EXCELLENT"
            summary = "Dialogue is authentic with distinct character voices"
        elif score >= 60:
            level = "GOOD"
            summary = "Dialogue works but could be more distinctive"
        elif score >= 40:
            level = "NEEDS WORK"
            summary = "Dialogue issues affecting authenticity"
        else:
            level = "POOR"
            summary = "Major dialogue problems throughout"

        diagnosis = f"DIALOGUE {level} ({score:.1f}/100): {summary}"

        # Add specific issues
        issues = []
        if authenticity < 0.5:
            issues.append("unnatural speech patterns")
        if subtext["score"] < 0.3:
            issues.append("lacking subtext")
        if len(profiles) > 1 and all(p.distinctiveness_score < 0.5 for p in profiles.values()):
            issues.append("indistinct character voices")

        if issues:
            diagnosis += f". Key issues: {', '.join(issues)}"

        return diagnosis

    def _profiles_to_dict(self, profiles: Dict[str, CharacterVoice]) -> List[Dict]:
        """Convert voice profiles to dictionaries."""
        result = []
        for name, profile in profiles.items():
            result.append({
                "name": name,
                "lines": profile.total_lines,
                "avg_words": profile.avg_words_per_line,
                "complexity": profile.vocabulary_complexity,
                "formality": profile.formality_level,
                "distinctiveness": profile.distinctiveness_score,
                "verbal_tics": profile.verbal_tics,
                "unique_phrases": profile.unique_phrases[:3]  # Top 3
            })
        return result

    def _generate_recommendations(self, score: float, violations: List,
                                 profiles: Dict, subtext: Dict, natural: Dict) -> List[str]:
        """Generate specific recommendations."""
        recommendations = []

        # Add recommendations based on violations
        for violation in violations[:3]:  # Top 3 violations
            recommendations.append(f"[{violation['severity'].upper()}] {violation['fix']}")

        # Add specific recommendations
        if natural["score"] < 0.5:
            recommendations.append("Add contractions, interruptions, and incomplete thoughts")

        if subtext["score"] < 0.3:
            recommendations.append("Have characters talk around issues instead of stating them directly")

        if len(profiles) > 1:
            low_distinct = [p.name for p in profiles.values() if p.distinctiveness_score < 0.5]
            if low_distinct:
                recommendations.append(f"Differentiate voices for: {', '.join(low_distinct[:3])}")

        # General excellence recommendations
        if score < 40:
            recommendations.append("Study dialogue in acclaimed screenplays")
            recommendations.append("Read dialogue aloud to test authenticity")

        return recommendations[:5]  # Return top 5

    def export_dialogue_features(self, screenplay_text: str, window_size: int = 10) -> List[Dict]:
        """
        Export dialogue features for correlation/analysis.

        Returns structured data with text + style metrics per window.
        Useful for external indexing, correlation engines, or ML pipelines.

        Args:
            screenplay_text: Full screenplay text
            window_size: Number of dialogue lines per window (default: 10)

        Returns:
            List of dicts with keys:
                - text: Raw dialogue text
                - window_id: Window index
                - character_count: Unique characters in window
                - style: Dict with metrics (avg_words, natural_score, subtext_ratio, etc.)
                - meta: Additional metadata
        """
        # Extract all dialogues
        dialogues = self._extract_dialogue(screenplay_text)

        if not dialogues:
            return []

        # Create sliding windows
        windows = []
        for i in range(0, len(dialogues), window_size):
            window_dialogues = dialogues[i:i + window_size]

            # Aggregate text
            window_text = '\n'.join([f"{d.character}: {d.line}" for d in window_dialogues])

            # Extract characters
            characters = list(set([d.character for d in window_dialogues]))

            # Calculate style metrics
            avg_words = sum(d.word_count for d in window_dialogues) / len(window_dialogues)
            natural_scores = [d.natural_score for d in window_dialogues]
            avg_natural = sum(natural_scores) / len(natural_scores)
            subtext_ratio = sum(1 for d in window_dialogues if d.has_subtext) / len(window_dialogues)

            # Emotional range
            emotions = [d.emotional_tone for d in window_dialogues]
            emotional_variety = len(set(emotions)) / len(emotions)

            # Sentence patterns (complexity)
            all_patterns = []
            for d in window_dialogues:
                all_patterns.extend(d.sentence_patterns)
            pattern_variety = len(set(all_patterns)) / max(len(all_patterns), 1)

            # Build window data
            window_data = {
                "text": window_text[:500],  # Truncate for size
                "window_id": len(windows),
                "character_count": len(characters),
                "characters": characters,
                "style": {
                    "avg_words_per_line": round(avg_words, 2),
                    "natural_score": round(avg_natural, 2),
                    "subtext_ratio": round(subtext_ratio, 2),
                    "emotional_variety": round(emotional_variety, 2),
                    "pattern_variety": round(pattern_variety, 2),
                    "total_lines": len(window_dialogues)
                },
                "meta": {
                    "start_line": i,
                    "end_line": min(i + window_size, len(dialogues)),
                    "source": "DrDialogue"
                }
            }

            windows.append(window_data)

        return windows


# Compatibility class for testing framework
class DrCharacterDialogue(DrDialogue):
    """Alias for compatibility with test framework."""
    pass