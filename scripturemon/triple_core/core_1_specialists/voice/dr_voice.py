#!/usr/bin/env python3
"""
Script Doctor Voicemon - Character Voice Consistency Specialist
Analyzes character voice distinctiveness, consistency, and authenticity.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Tuple, Set
import re
import yaml
from pathlib import Path
from collections import Counter
import statistics


@dataclass
class VoiceProfile:
    """Profile of a character's voice."""
    character_name: str
    total_lines: int = 0
    avg_sentence_length: float = 0.0
    vocabulary_complexity: float = 0.0
    unique_words: Set[str] = field(default_factory=set)
    common_phrases: List[str] = field(default_factory=list)
    verbal_tics: List[str] = field(default_factory=list)
    formality_score: float = 0.0
    contractions_ratio: float = 0.0
    questions_ratio: float = 0.0
    exclamations_ratio: float = 0.0
    slang_count: int = 0
    profanity_count: int = 0
    consistency_score: float = 0.0


@dataclass
class VoiceAnalysis:
    """Results from voice consistency analysis."""
    total_characters: int = 0
    distinct_voices: int = 0
    voice_distinctiveness_score: float = 0.0
    consistency_issues: List[Dict[str, Any]] = field(default_factory=list)
    interchangeable_dialogue: List[Dict[str, Any]] = field(default_factory=list)
    voice_evolution: Dict[str, Any] = field(default_factory=dict)
    authenticity_score: float = 0.0


@dataclass
class VoiceResult:
    """Complete voice consistency analysis result."""
    score: int
    specialist: Dict[str, str]
    voice_profiles: Dict[str, VoiceProfile]
    voice_analysis: VoiceAnalysis
    similarity_matrix: Dict[str, Dict[str, float]]
    consistency_scores: Dict[str, float]
    distinctiveness_scores: Dict[str, float]
    recommendations: List[str]
    rule_violations: List[Dict[str, Any]]
    voice_comparisons: List[Dict[str, Any]]
    

class DrVoice:
    """Script Doctor Voicemon - Character Voice Consistency Specialist."""

    def __init__(self):
        """Initialize the voice consistency specialist."""
        self.name = "Script Doctor Voicemon"
        self.specialty = "Character Voice Consistency"
        self.load_rules()
        
        # Common contractions (bilingual: EN + PT)
        self.contractions = {
            # English
            "don't", "won't", "can't", "couldn't", "shouldn't", "wouldn't",
            "didn't", "doesn't", "isn't", "aren't", "wasn't", "weren't",
            "i'm", "you're", "he's", "she's", "it's", "we're", "they're",
            "i've", "you've", "we've", "they've", "i'd", "you'd", "he'd",
            "she'd", "we'd", "they'd", "i'll", "you'll", "he'll", "she'll",
            "we'll", "they'll", "let's", "that's", "there's", "here's",
            # Portuguese
            "não", "tá", "pra", "pro", "né", "tô", "cê", "ocê",
            "vou", "tava", "num", "nada", "pô", "tive", "teve"
        }

        # Formal indicators (bilingual: EN + PT)
        self.formal_indicators = [
            # English
            'therefore', 'moreover', 'furthermore', 'however', 'nevertheless',
            'consequently', 'subsequently', 'accordingly', 'hence', 'thus',
            'shall', 'whom', 'whereby', 'wherein', 'thereof',
            # Portuguese
            'portanto', 'todavia', 'outrossim', 'ademais', 'contudo',
            'entretanto', 'porquanto', 'destarte', 'mormente', 'assim',
            'conquanto', 'dessarte', 'doravante', 'nalgum', 'destro'
        ]

        # Informal/slang indicators (bilingual: EN + PT)
        self.informal_indicators = [
            # English
            'gonna', 'wanna', 'gotta', 'kinda', 'sorta', 'yeah', 'nah',
            'dunno', 'lemme', 'gimme', 'ain\'t', 'y\'all', 'cause', 'cuz',
            'ok', 'okay', 'yep', 'nope', 'uh-huh', 'uh-uh',
            # Portuguese
            'cara', 'mano', 'tipo', 'sei lá', 'pô', 'né', 'beleza',
            'massa', 'valeu', 'po', 'ó', 'opa', 'eita', 'oxe',
            'véi', 'velho', 'brother', 'parceiro', 'truta', 'meu'
        ]

        # Age-related vocabulary (bilingual: EN + PT)
        self.young_vocabulary = [
            # English
            'like', 'literally', 'totally', 'whatever', 'awesome', 'cool',
            'dude', 'bro', 'sick', 'epic', 'random', 'sketchy',
            # Portuguese
            'tipo', 'cara', 'mano', 'massa', 'da hora', 'sinistro',
            'tá ligado', 'firmeza', 'suave', 'top', 'show', 'legal',
            'irado', 'maneiro', 'bacana', 'demais', 'foda', 'brabo'
        ]

        self.mature_vocabulary = [
            # English
            'perhaps', 'certainly', 'indeed', 'quite', 'rather', 'suppose',
            'ought', 'shall', 'proper', 'considerable', 'substantial',
            # Portuguese
            'porventura', 'decerto', 'deveras', 'sobremaneira', 'mormente',
            'destarte', 'outrossim', 'porquanto', 'conquanto', 'entrementes',
            'doravante', 'dessarte', 'nalgum', 'destro', 'certamente'
        ]
        
    def load_rules(self):
        """Load rules from YAML configuration."""
        rules_path = Path(__file__).parent.parent / 'rules' / 'voice_consistency_rules.yaml'
        try:
            with open(rules_path, 'r') as f:
                self.rules_config = yaml.safe_load(f)
                self.rules = self.rules_config.get('rules', [])
        except FileNotFoundError:
            self.rules = []
            self.rules_config = {}
            
    def analyze(self, screenplay_text: str) -> Dict[str, Any]:
        """Analyze screenplay for voice consistency."""
        lines = screenplay_text.split('\n')
        
        # Extract dialogue by character
        character_dialogue = self._extract_character_dialogue(lines)
        
        # Build voice profiles
        voice_profiles = {}
        for character, dialogue_list in character_dialogue.items():
            voice_profiles[character] = self._build_voice_profile(character, dialogue_list)
        
        # Analyze voice consistency and distinctiveness
        voice_analysis = self._analyze_voices(voice_profiles, character_dialogue)
        
        # Calculate similarity matrix
        similarity_matrix = self._calculate_similarity_matrix(voice_profiles)
        
        # Calculate individual scores
        consistency_scores = self._calculate_consistency_scores(character_dialogue)
        distinctiveness_scores = self._calculate_distinctiveness_scores(
            voice_profiles, similarity_matrix
        )
        
        # Find voice comparisons
        voice_comparisons = self._generate_voice_comparisons(voice_profiles)
        
        # Check rules
        violations = self._check_rule_violations(
            voice_profiles, voice_analysis, similarity_matrix
        )
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            voice_profiles, voice_analysis, violations
        )
        
        # Calculate score
        score = self._calculate_score(voice_analysis, violations)

        # Generate diagnosis
        diagnosis = self._generate_diagnosis(score, voice_analysis, voice_profiles)

        # Convert voice_profiles to dict (ENRICHED like DrDialogue)
        profiles_dict = []
        for name, profile in voice_profiles.items():
            # Calculate avg words per line
            total_words = sum(len(line.split()) for line in character_dialogue.get(name, []))
            avg_words = total_words / profile.total_lines if profile.total_lines > 0 else 0

            # Determine formality string
            if profile.formality_score > 0.7:
                formality_str = "formal"
            elif profile.formality_score > 0.4:
                formality_str = "mixed"
            else:
                formality_str = "casual"

            # Get distinctiveness score for this character
            char_distinctiveness = distinctiveness_scores.get(name, 0.5)

            profiles_dict.append({
                "name": name,
                "lines": profile.total_lines,
                "avg_words": round(avg_words, 1),
                "complexity": round(profile.vocabulary_complexity, 2),
                "formality": formality_str,
                "distinctiveness": round(char_distinctiveness, 2),
                "verbal_tics": profile.verbal_tics[:3],  # Top 3
                "unique_phrases": profile.common_phrases[:3]  # Top 3
            })

        # Find weak and strong voices (like DrDialogue)
        sorted_by_distinctiveness = sorted(
            [(name, distinctiveness_scores.get(name, 0)) for name in voice_profiles.keys()],
            key=lambda x: x[1]
        )
        weak_voices = [name for name, score in sorted_by_distinctiveness[:5]]
        strong_voices = [name for name, score in sorted_by_distinctiveness[-5:]]

        # Find indistinguishable pairs (similarity > 0.85)
        indistinguishable_pairs = []
        chars = list(voice_profiles.keys())
        for i, char1 in enumerate(chars):
            for char2 in chars[i+1:]:
                sim = similarity_matrix.get(char1, {}).get(char2, 0)
                if sim > 0.85:
                    indistinguishable_pairs.append({
                        "char1": char1,
                        "char2": char2,
                        "similarity": round(sim, 2)
                    })

        return {
            # METADATA
            "specialist": {
                "name": self.name,
                "specialty": self.specialty,
                "identity": "Script Doctor™ first, Digimon voice specialist second"
            },
            "score": score,

            # QUANTITATIVE METRICS (like DrDialogue)
            "total_characters": voice_analysis.total_characters,
            "distinct_voices": voice_analysis.distinct_voices,
            "voice_distinctiveness_score": voice_analysis.voice_distinctiveness_score,
            "authenticity_score": voice_analysis.authenticity_score,
            "consistency_issues_count": len(voice_analysis.consistency_issues),
            "interchangeable_count": len(voice_analysis.interchangeable_dialogue),

            # DETAILED DATA (enriched)
            "voice_profiles": profiles_dict,  # Now FULL profiles like DrDialogue
            "weak_voices": weak_voices,  # TOP 5 needing work
            "strong_voices": strong_voices,  # TOP 5 doing well
            "indistinguishable_pairs": indistinguishable_pairs[:10],  # Top 10 problematic
            "consistency_issues": voice_analysis.consistency_issues[:5],  # Top 5
            "interchangeable_dialogue": voice_analysis.interchangeable_dialogue[:5],  # Top 5

            # ACTIONABLE FEEDBACK
            "rule_violations": violations,
            "recommendations": recommendations,
            "diagnosis": diagnosis,
            "signature": f"Diagnosed by {self.name}™"
        }
        
    def _extract_character_dialogue(self, lines: List[str]) -> Dict[str, List[str]]:
        """Extract all dialogue organized by character."""
        character_dialogue = {}
        current_character = None
        current_dialogue = []
        
        for line in lines:
            stripped = line.strip()
            
            # Character name (all caps, not a scene heading)
            if stripped and stripped.isupper() and not any(
                keyword in stripped for keyword in ['INT.', 'EXT.', 'FADE', 'CUT']
            ):
                # Save previous dialogue
                if current_character and current_dialogue:
                    if current_character not in character_dialogue:
                        character_dialogue[current_character] = []
                    character_dialogue[current_character].append(' '.join(current_dialogue))
                
                current_character = stripped.split('(')[0].strip()  # Remove parentheticals
                current_dialogue = []
                
            # Dialogue line (not parenthetical)
            elif current_character and stripped and not stripped.startswith('('):
                current_dialogue.append(stripped)
                
            # End of dialogue block
            elif not stripped and current_character and current_dialogue:
                if current_character not in character_dialogue:
                    character_dialogue[current_character] = []
                character_dialogue[current_character].append(' '.join(current_dialogue))
                current_dialogue = []
                
        # Don't forget last dialogue
        if current_character and current_dialogue:
            if current_character not in character_dialogue:
                character_dialogue[current_character] = []
            character_dialogue[current_character].append(' '.join(current_dialogue))
            
        return character_dialogue
        
    def _build_voice_profile(self, character: str, dialogue_list: List[str]) -> VoiceProfile:
        """Build a voice profile for a character."""
        profile = VoiceProfile(character_name=character)
        
        if not dialogue_list:
            return profile
            
        profile.total_lines = len(dialogue_list)
        
        # Combine all dialogue
        all_dialogue = ' '.join(dialogue_list)
        words = all_dialogue.lower().split()
        
        # Calculate metrics
        profile.unique_words = set(words)
        
        # Average sentence length
        sentences = re.split(r'[.!?]+', all_dialogue)
        sentence_lengths = [len(s.split()) for s in sentences if s.strip()]
        if sentence_lengths:
            profile.avg_sentence_length = statistics.mean(sentence_lengths)
        
        # Vocabulary complexity (unique words ratio)
        if words:
            profile.vocabulary_complexity = len(profile.unique_words) / len(words)
        
        # Find common phrases (2-3 word combinations that appear multiple times)
        profile.common_phrases = self._find_common_phrases(dialogue_list)
        
        # Find verbal tics (repeated single words)
        profile.verbal_tics = self._find_verbal_tics(words)
        
        # Calculate formality score
        profile.formality_score = self._calculate_formality(all_dialogue)
        
        # Contractions ratio
        contraction_count = sum(1 for word in words if word.lower() in self.contractions)
        profile.contractions_ratio = contraction_count / len(words) if words else 0
        
        # Questions and exclamations
        profile.questions_ratio = all_dialogue.count('?') / len(dialogue_list)
        profile.exclamations_ratio = all_dialogue.count('!') / len(dialogue_list)
        
        # Slang count
        profile.slang_count = sum(1 for word in words if word in self.informal_indicators)
        
        # Calculate consistency
        profile.consistency_score = self._calculate_voice_consistency(dialogue_list)
        
        return profile
        
    def _find_common_phrases(self, dialogue_list: List[str]) -> List[str]:
        """Find frequently used phrases."""
        all_dialogue = ' '.join(dialogue_list).lower()
        
        # Extract 2-3 word phrases
        words = all_dialogue.split()
        two_word_phrases = [f"{words[i]} {words[i+1]}" 
                           for i in range(len(words)-1)]
        three_word_phrases = [f"{words[i]} {words[i+1]} {words[i+2]}" 
                             for i in range(len(words)-2)]
        
        # Count occurrences
        phrase_counts = Counter(two_word_phrases + three_word_phrases)
        
        # Return phrases that appear more than once
        common = [phrase for phrase, count in phrase_counts.items() if count > 1]
        
        return common[:5]  # Top 5 common phrases
        
    def _find_verbal_tics(self, words: List[str]) -> List[str]:
        """Find repeated verbal tics."""
        # Exclude common words
        common_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to',
            'for', 'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are',
            'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did',
            'will', 'would', 'could', 'should', 'may', 'might', 'must',
            'can', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'that',
            'this', 'what', 'which', 'who', 'when', 'where', 'why', 'how'
        }
        
        # Count non-common words
        filtered_words = [w for w in words if w not in common_words and len(w) > 2]
        word_counts = Counter(filtered_words)
        
        # Find words used disproportionately often
        total_filtered = len(filtered_words)
        if total_filtered == 0:
            return []
            
        tics = []
        for word, count in word_counts.items():
            # If a word appears more than 1% of the time, it might be a tic
            if count / total_filtered > 0.01 and count > 2:
                tics.append(word)
                
        return tics[:5]  # Top 5 verbal tics
        
    def _calculate_formality(self, text: str) -> float:
        """Calculate formality score of text."""
        text_lower = text.lower()
        words = text_lower.split()
        
        if not words:
            return 0.5
            
        formal_count = sum(1 for word in self.formal_indicators if word in text_lower)
        informal_count = sum(1 for word in self.informal_indicators if word in text_lower)
        
        # Contractions make it less formal
        contraction_count = sum(1 for word in words if word in self.contractions)
        
        # Calculate score (0 = very informal, 1 = very formal)
        formality = 0.5  # Start neutral
        formality += (formal_count * 0.1)
        formality -= (informal_count * 0.1)
        formality -= (contraction_count * 0.05)
        
        return max(0, min(1, formality))
        
    def _calculate_voice_consistency(self, dialogue_list: List[str]) -> float:
        """Calculate how consistent a character's voice is."""
        if len(dialogue_list) < 2:
            return 1.0  # Not enough data
            
        # Check sentence length consistency
        sentence_lengths = []
        for dialogue in dialogue_list:
            sentences = re.split(r'[.!?]+', dialogue)
            for s in sentences:
                if s.strip():
                    sentence_lengths.append(len(s.split()))
                    
        if len(sentence_lengths) > 1:
            # Lower coefficient of variation = more consistent
            mean_length = statistics.mean(sentence_lengths)
            if mean_length > 0:
                cv = statistics.stdev(sentence_lengths) / mean_length
                consistency = max(0, 1 - cv)  # Convert to 0-1 scale
            else:
                consistency = 1.0
        else:
            consistency = 1.0
            
        return consistency
        
    def _analyze_voices(self, 
                       voice_profiles: Dict[str, VoiceProfile],
                       character_dialogue: Dict[str, List[str]]) -> VoiceAnalysis:
        """Analyze overall voice patterns."""
        analysis = VoiceAnalysis()
        
        analysis.total_characters = len(voice_profiles)
        
        if analysis.total_characters == 0:
            return analysis
            
        # Calculate distinctiveness
        distinct_count = 0
        # NEW LOGIC: Count as distinct if different from at least 60% of other characters
        # (old logic required different from ALL others - impossible with 40+ characters)
        for char1 in voice_profiles:
            similar_count = 0
            comparisons = 0

            for char2 in voice_profiles:
                if char1 != char2:
                    comparisons += 1
                    similarity = self._calculate_voice_similarity(
                        voice_profiles[char1], voice_profiles[char2]
                    )
                    if similarity > 0.85:  # Too similar (raised from 0.8)
                        similar_count += 1

            # Distinct if similar to less than 40% of other characters
            if comparisons > 0:
                similarity_ratio = similar_count / comparisons
                if similarity_ratio < 0.4:  # Less than 40% similar voices
                    distinct_count += 1

        analysis.distinct_voices = distinct_count
        analysis.voice_distinctiveness_score = distinct_count / analysis.total_characters if analysis.total_characters > 0 else 0
        
        # Find consistency issues (ONLY for major characters with enough dialogue)
        for character, profile in voice_profiles.items():
            # Only flag if: (1) low consistency AND (2) character has enough lines to matter
            if profile.consistency_score < 0.4 and profile.total_lines >= 5:
                analysis.consistency_issues.append({
                    'character': character,
                    'consistency_score': profile.consistency_score,
                    'issue': 'Voice varies significantly throughout screenplay'
                })
                
        # Check for interchangeable dialogue
        analysis.interchangeable_dialogue = self._find_interchangeable_dialogue(
            character_dialogue
        )
        
        # Calculate authenticity
        authenticity_scores = []
        for profile in voice_profiles.values():
            # Simple authenticity based on consistency and complexity
            auth_score = (profile.consistency_score + profile.vocabulary_complexity) / 2
            authenticity_scores.append(auth_score)
            
        if authenticity_scores:
            analysis.authenticity_score = statistics.mean(authenticity_scores)
            
        return analysis
        
    def _calculate_voice_similarity(self, 
                                   profile1: VoiceProfile, 
                                   profile2: VoiceProfile) -> float:
        """Calculate similarity between two voice profiles."""
        similarity_factors = []
        
        # Compare sentence length
        if profile1.avg_sentence_length > 0 and profile2.avg_sentence_length > 0:
            length_diff = abs(profile1.avg_sentence_length - profile2.avg_sentence_length)
            length_similarity = 1 / (1 + length_diff/10)  # Normalize difference
            similarity_factors.append(length_similarity)
            
        # Compare vocabulary complexity
        complexity_diff = abs(profile1.vocabulary_complexity - profile2.vocabulary_complexity)
        complexity_similarity = 1 - complexity_diff
        similarity_factors.append(complexity_similarity)
        
        # Compare formality
        formality_diff = abs(profile1.formality_score - profile2.formality_score)
        formality_similarity = 1 - formality_diff
        similarity_factors.append(formality_similarity)
        
        # Compare contractions usage
        contraction_diff = abs(profile1.contractions_ratio - profile2.contractions_ratio)
        contraction_similarity = 1 - contraction_diff
        similarity_factors.append(contraction_similarity)
        
        # Compare question/exclamation usage
        question_diff = abs(profile1.questions_ratio - profile2.questions_ratio)
        question_similarity = 1 / (1 + question_diff)
        similarity_factors.append(question_similarity)
        
        # Calculate overall similarity
        if similarity_factors:
            return statistics.mean(similarity_factors)
        return 0.5
        
    def _find_interchangeable_dialogue(self, 
                                       character_dialogue: Dict[str, List[str]]) -> List[Dict[str, Any]]:
        """Find dialogue that could be spoken by any character."""
        interchangeable = []
        
        # Generic phrases that any character might say
        generic_phrases = [
            'yes', 'no', 'okay', 'sure', 'thanks', 'sorry',
            'what?', 'why?', 'how?', 'really?', 'i don\'t know',
            'let\'s go', 'come on', 'wait', 'stop'
        ]
        
        for character, dialogues in character_dialogue.items():
            for dialogue in dialogues:
                dialogue_lower = dialogue.lower().strip()
                
                # Check if dialogue is too generic
                if dialogue_lower in generic_phrases:
                    interchangeable.append({
                        'character': character,
                        'dialogue': dialogue,
                        'reason': 'Generic phrase - any character could say this'
                    })
                # Check if dialogue is very short and generic
                elif len(dialogue.split()) <= 3 and not any(
                    c in dialogue for c in '!?...—'
                ):
                    # Short, declarative, no emotion
                    interchangeable.append({
                        'character': character,
                        'dialogue': dialogue,
                        'reason': 'Short generic statement lacking character voice'
                    })
                    
        return interchangeable[:10]  # Limit to 10 examples
        
    def _calculate_similarity_matrix(self, 
                                     voice_profiles: Dict[str, VoiceProfile]) -> Dict[str, Dict[str, float]]:
        """Calculate similarity between all character pairs."""
        matrix = {}
        
        for char1 in voice_profiles:
            matrix[char1] = {}
            for char2 in voice_profiles:
                if char1 == char2:
                    matrix[char1][char2] = 1.0  # Perfect similarity with self
                else:
                    similarity = self._calculate_voice_similarity(
                        voice_profiles[char1], voice_profiles[char2]
                    )
                    matrix[char1][char2] = similarity
                    
        return matrix
        
    def _calculate_consistency_scores(self, 
                                      character_dialogue: Dict[str, List[str]]) -> Dict[str, float]:
        """Calculate consistency score for each character."""
        scores = {}
        
        for character, dialogues in character_dialogue.items():
            if len(dialogues) < 2:
                scores[character] = 1.0  # Not enough data
                continue
                
            # Analyze consistency across different metrics
            consistency_metrics = []
            
            # Sentence length consistency
            sentence_lengths = []
            for dialogue in dialogues:
                sentences = re.split(r'[.!?]+', dialogue)
                for s in sentences:
                    if s.strip():
                        sentence_lengths.append(len(s.split()))
                        
            if len(sentence_lengths) > 1:
                mean_length = statistics.mean(sentence_lengths)
                if mean_length > 0:
                    cv = statistics.stdev(sentence_lengths) / mean_length
                    consistency_metrics.append(max(0, 1 - cv/2))  # Normalize
                    
            # Formality consistency
            formality_scores = [self._calculate_formality(d) for d in dialogues]
            if len(formality_scores) > 1:
                formality_std = statistics.stdev(formality_scores)
                consistency_metrics.append(1 - formality_std)  # Lower std = more consistent
                
            # Calculate overall consistency
            if consistency_metrics:
                scores[character] = statistics.mean(consistency_metrics)
            else:
                scores[character] = 0.5  # Neutral if no metrics
                
        return scores
        
    def _calculate_distinctiveness_scores(self,
                                          voice_profiles: Dict[str, VoiceProfile],
                                          similarity_matrix: Dict[str, Dict[str, float]]) -> Dict[str, float]:
        """Calculate how distinctive each character's voice is."""
        scores = {}
        
        for character in voice_profiles:
            if character not in similarity_matrix:
                scores[character] = 0.5
                continue
                
            # Calculate average dissimilarity from others
            dissimilarities = []
            for other_char in voice_profiles:
                if other_char != character:
                    similarity = similarity_matrix[character][other_char]
                    dissimilarity = 1 - similarity
                    dissimilarities.append(dissimilarity)
                    
            if dissimilarities:
                scores[character] = statistics.mean(dissimilarities)
            else:
                scores[character] = 0.5
                
        return scores
        
    def _generate_voice_comparisons(self, 
                                   voice_profiles: Dict[str, VoiceProfile]) -> List[Dict[str, Any]]:
        """Generate interesting voice comparisons."""
        comparisons = []
        
        if len(voice_profiles) < 2:
            return comparisons
            
        # Find most and least formal
        sorted_by_formality = sorted(
            voice_profiles.items(), 
            key=lambda x: x[1].formality_score
        )
        
        if len(sorted_by_formality) >= 2:
            most_formal = sorted_by_formality[-1]
            least_formal = sorted_by_formality[0]
            
            comparisons.append({
                'type': 'formality_contrast',
                'description': f"{most_formal[0]} (formal: {most_formal[1].formality_score:.2f}) vs {least_formal[0]} (formal: {least_formal[1].formality_score:.2f})",
                'insight': 'Shows range of formality in character voices'
            })
            
        # Find most verbose vs concise
        sorted_by_length = sorted(
            voice_profiles.items(),
            key=lambda x: x[1].avg_sentence_length
        )
        
        if len(sorted_by_length) >= 2:
            most_verbose = sorted_by_length[-1]
            most_concise = sorted_by_length[0]
            
            comparisons.append({
                'type': 'sentence_length_contrast',
                'description': f"{most_verbose[0]} (avg {most_verbose[1].avg_sentence_length:.1f} words) vs {most_concise[0]} (avg {most_concise[1].avg_sentence_length:.1f} words)",
                'insight': 'Shows variation in verbosity'
            })
            
        return comparisons
        
    def _check_rule_violations(self,
                               voice_profiles: Dict[str, VoiceProfile],
                               voice_analysis: VoiceAnalysis,
                               similarity_matrix: Dict[str, Dict[str, float]]) -> List[Dict[str, Any]]:
        """Check for rule violations."""
        violations = []
        
        for rule in self.rules:
            if self._evaluate_rule(rule, voice_profiles, voice_analysis, similarity_matrix):
                violations.append({
                    'rule_id': rule['id'],
                    'title': rule['title'],
                    'severity': rule['severity'],
                    'message': rule.get('fail_msg', 'Rule violation'),
                    'fix': rule.get('fix', 'No fix available')
                })
                
        return violations
        
    def _evaluate_rule(self,
                      rule: Dict[str, Any],
                      voice_profiles: Dict[str, VoiceProfile],
                      voice_analysis: VoiceAnalysis,
                      similarity_matrix: Dict[str, Dict[str, float]]) -> bool:
        """Evaluate if a rule is violated."""
        rule_id = rule['id']
        
        # Distinct Character Voices
        if rule_id == 'VOI.R001':
            return voice_analysis.voice_distinctiveness_score < 0.6
            
        # Voice Consistency
        elif rule_id == 'VOI.R002':
            return len(voice_analysis.consistency_issues) > 0
            
        # Vocabulary Appropriate
        elif rule_id == 'VOI.R003':
            # Check if vocabulary complexity varies appropriately
            complexities = [p.vocabulary_complexity for p in voice_profiles.values()]
            if complexities and max(complexities) - min(complexities) < 0.1:
                return True  # Not enough variation
            return False
            
        # Speech Patterns Match Character
        elif rule_id == 'VOI.R004':
            # Check if all characters have similar patterns
            patterns_similar = 0
            for char1 in voice_profiles:
                for char2 in voice_profiles:
                    if char1 != char2 and char1 in similarity_matrix and char2 in similarity_matrix[char1]:
                        if similarity_matrix[char1][char2] > 0.85:
                            patterns_similar += 1
            return patterns_similar > len(voice_profiles)  # Too many similar pairs
            
        # Age-Appropriate Dialogue
        elif rule_id == 'VOI.R005':
            # This would need character age metadata
            return False  # Can't determine without age data
            
        # Cultural Authenticity
        elif rule_id == 'VOI.R006':
            return voice_analysis.authenticity_score < 0.5
            
        # Educational Level Reflected
        elif rule_id == 'VOI.R007':
            # Check vocabulary complexity variation
            complexities = [p.vocabulary_complexity for p in voice_profiles.values()]
            if complexities and statistics.stdev(complexities) < 0.05:
                return True  # Not enough education level variation
            return False
            
        # Emotional Voice Variation
        elif rule_id == 'VOI.R008':
            # Check for exclamation and question variation
            for profile in voice_profiles.values():
                if profile.questions_ratio == 0 and profile.exclamations_ratio == 0:
                    return True  # No emotional variation
            return False
            
        # Unique Verbal Tics
        elif rule_id == 'VOI.R009':
            tic_count = sum(1 for p in voice_profiles.values() if p.verbal_tics)
            return tic_count < len(voice_profiles) * 0.3  # Less than 30% have tics
            
        # Avoid Interchangeable Dialogue
        elif rule_id == 'VOI.R010':
            return len(voice_analysis.interchangeable_dialogue) > 5
            
        # Status Reflected in Voice
        elif rule_id == 'VOI.R011':
            # Check formality variation
            formalities = [p.formality_score for p in voice_profiles.values()]
            if formalities and max(formalities) - min(formalities) < 0.2:
                return True  # Not enough status variation
            return False
            
        # Relationship-Based Voice
        elif rule_id == 'VOI.R012':
            # Would need to track dialogue targets
            return False  # Can't determine without relationship data
            
        # Period-Appropriate Language
        elif rule_id == 'VOI.R013':
            # Would need period setting metadata
            return False  # Can't determine without period data
            
        # Profession-Specific Jargon
        elif rule_id == 'VOI.R014':
            # Check for specialized vocabulary
            avg_unique = statistics.mean([len(p.unique_words) for p in voice_profiles.values()])
            return avg_unique < 50  # Too few unique words suggests no jargon
            
        # Voice Evolution Justified
        elif rule_id == 'VOI.R015':
            # Check consistency scores
            for issue in voice_analysis.consistency_issues:
                if issue['consistency_score'] < 0.5:  # Very inconsistent
                    return True
            return False
            
        return False
        
    def _generate_recommendations(self,
                                 voice_profiles: Dict[str, VoiceProfile],
                                 voice_analysis: VoiceAnalysis,
                                 violations: List[Dict[str, Any]]) -> List[str]:
        """Generate recommendations based on analysis."""
        recommendations = []
        
        # Address critical violations first
        critical_violations = [v for v in violations if v['severity'] == 'critical']
        for violation in critical_violations[:2]:
            recommendations.append(f"CRITICAL: {violation['fix']}")
            
        # Check distinctiveness
        if voice_analysis.voice_distinctiveness_score < 0.6:
            recommendations.append(
                "Increase voice distinctiveness - too many characters sound similar"
            )
            
        # Check consistency
        if voice_analysis.consistency_issues:
            char = voice_analysis.consistency_issues[0]['character']
            recommendations.append(
                f"Improve voice consistency for {char} - speech patterns vary too much"
            )
            
        # Check interchangeable dialogue
        if len(voice_analysis.interchangeable_dialogue) > 5:
            recommendations.append(
                "Make dialogue more character-specific - too many generic lines"
            )
            
        # Check for verbal tics
        chars_without_tics = [c for c, p in voice_profiles.items() if not p.verbal_tics]
        if len(chars_without_tics) > len(voice_profiles) * 0.7:
            recommendations.append(
                "Add subtle verbal tics or catchphrases to distinguish characters"
            )
            
        # Check formality range
        formalities = [p.formality_score for p in voice_profiles.values()]
        if formalities and max(formalities) - min(formalities) < 0.3:
            recommendations.append(
                "Vary formality levels to reflect different backgrounds/status"
            )
            
        # Check vocabulary diversity
        avg_unique = statistics.mean([len(p.unique_words) for p in voice_profiles.values()])
        if avg_unique < 100:
            recommendations.append(
                "Expand vocabulary diversity to create richer character voices"
            )
            
        return recommendations[:7]  # Limit to 7 recommendations
        
    def _calculate_score(self,
                        voice_analysis: VoiceAnalysis,
                        violations: List[Dict[str, Any]]) -> int:
        """Calculate overall score - following DrDialogue pattern."""
        base_score = 90  # Start at 90 (not 100 - no screenplay is perfect)

        # Deduct for violations (SAME AS DRDIALOGUE - not less!)
        severity_penalties = {
            'critical': 20,  # Was 15 - NOW 20 like DrDialogue
            'high': 15,      # Was 10 - NOW 15 like DrDialogue
            'medium': 8,     # Was 5 - NOW 8 like DrDialogue
            'low': 5         # Was 2 - NOW 5 like DrDialogue
        }

        for violation in violations:
            base_score -= severity_penalties.get(violation['severity'], 0)

        # Distinctiveness - GRADUAL (not binary)
        dist = voice_analysis.voice_distinctiveness_score
        if dist > 0.9:
            base_score += 5  # Excellent
        elif dist > 0.7:
            base_score += 3  # Good
        elif dist < 0.3:
            base_score -= 15  # Critical - very indistinct
        elif dist < 0.5:
            base_score -= 5   # Needs work

        # Penalty for consistency issues (REDUCED - was too harsh)
        base_score -= min(len(voice_analysis.consistency_issues) * 2, 20)  # Cap at -20

        # Penalty for interchangeable dialogue
        base_score -= min(len(voice_analysis.interchangeable_dialogue), 10)

        # Authenticity - GRADUAL with penalties too
        auth = voice_analysis.authenticity_score
        if auth > 0.9:
            base_score += 5
        elif auth > 0.8:
            base_score += 3
        elif auth < 0.5:
            base_score -= 10  # Penalty for very low authenticity
        elif auth < 0.7:
            base_score -= 5   # Penalty for low authenticity

        # Cap at 95 (not 100 - always room for improvement)
        return max(5, min(95, base_score))

    def _generate_diagnosis(self, score: int, voice_analysis, voice_profiles: Dict) -> str:
        """Generate diagnosis based on voice analysis."""
        diagnosis_parts = []

        # Overall assessment
        if score >= 85:
            diagnosis_parts.append("✅ EXCELLENT voice consistency and distinctiveness.")
        elif score >= 70:
            diagnosis_parts.append("👍 GOOD voice consistency with room for improvement.")
        elif score >= 50:
            diagnosis_parts.append("⚠️  MODERATE voice issues - characters need more distinct voices.")
        else:
            diagnosis_parts.append("❌ CRITICAL voice problems - dialogue is largely interchangeable.")

        # Distinctiveness
        if voice_analysis.voice_distinctiveness_score < 0.5:
            diagnosis_parts.append(f"Voice distinctiveness is low ({voice_analysis.voice_distinctiveness_score:.2f}) - characters sound too similar.")
        elif voice_analysis.voice_distinctiveness_score > 0.8:
            diagnosis_parts.append(f"Excellent voice distinctiveness ({voice_analysis.voice_distinctiveness_score:.2f})!")

        # Character count
        diagnosis_parts.append(f"Analyzed {voice_analysis.total_characters} characters with {voice_analysis.distinct_voices} distinct voices.")

        # Consistency issues
        if voice_analysis.consistency_issues:
            diagnosis_parts.append(f"Found {len(voice_analysis.consistency_issues)} voice consistency issues.")

        # Interchangeable dialogue
        if voice_analysis.interchangeable_dialogue:
            diagnosis_parts.append(f"⚠️  {len(voice_analysis.interchangeable_dialogue)} instances of interchangeable dialogue detected.")

        return " ".join(diagnosis_parts)
