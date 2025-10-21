#!/usr/bin/env python3
"""
OCR AI Corrector - Uses LLMs to fix OCR errors
Specifically trained for screenplay format
"""

import re
import json
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class OCRCorrection:
    """OCR correction result."""
    original_text: str
    corrected_text: str
    confidence: float
    corrections_made: List[Dict]
    structure_fixed: bool


class OCRAICorrector:
    """
    AI-powered OCR error corrector.
    Uses LLMs to fix common OCR mistakes in screenplays.
    """

    def __init__(self, model: str = "phi3:mini"):
        """
        Initialize corrector.

        Args:
            model: Ollama model to use for corrections
        """
        self.model = model
        self.screenplay_patterns = self._load_screenplay_patterns()

    def _load_screenplay_patterns(self) -> Dict:
        """Load common screenplay patterns for validation."""
        return {
            'scene_headers': [
                r'^INT\.\s+',
                r'^EXT\.\s+',
                r'^INT\./EXT\.\s+',
                r'^I/E\s+'
            ],
            'transitions': [
                r'^CUT TO:',
                r'^FADE IN:',
                r'^FADE OUT\.',
                r'^DISSOLVE TO:',
                r'^MATCH CUT:',
                r'^SMASH CUT:'
            ],
            'parentheticals': [
                r'\([^)]+\)',
                r'\(CONT\'D\)',
                r'\(V\.O\.\)',
                r'\(O\.S\.\)'
            ],
            'common_errors': {
                'INT,': 'INT.',
                'EXT,': 'EXT.',
                'CUT T0:': 'CUT TO:',
                'FADE lN:': 'FADE IN:',
                'CONT\'0': "CONT'D",
                'V,O,': 'V.O.',
                '0.S.': 'O.S.',
                'l ': 'I ',  # Common l/I confusion
                ' l ': ' I ',
                '1NT.': 'INT.',
                'lNT.': 'INT.'
            }
        }

    def correct_with_ai(self, text: str, context: str = "screenplay") -> OCRCorrection:
        """
        Correct OCR text using AI.

        Args:
            text: OCR text to correct
            context: Context type (screenplay, dialogue, action)

        Returns:
            OCRCorrection object
        """
        # First apply rule-based corrections
        pre_corrected = self._apply_rules(text)

        # Then use AI for advanced corrections
        ai_corrected = self._ai_correction(pre_corrected, context)

        # Validate structure
        structure_fixed = self._validate_structure(ai_corrected)

        # Track corrections
        corrections = self._find_corrections(text, ai_corrected)

        return OCRCorrection(
            original_text=text,
            corrected_text=ai_corrected,
            confidence=self._calculate_confidence(text, ai_corrected),
            corrections_made=corrections,
            structure_fixed=structure_fixed
        )

    def _apply_rules(self, text: str) -> str:
        """Apply rule-based corrections."""
        corrected = text

        # Fix common OCR errors
        for error, fix in self.screenplay_patterns['common_errors'].items():
            corrected = corrected.replace(error, fix)

        # Fix character name formatting (should be uppercase)
        lines = corrected.split('\n')
        fixed_lines = []

        for i, line in enumerate(lines):
            # Detect potential character names
            if self._is_character_name(line, i, lines):
                line = line.upper()
            fixed_lines.append(line)

        return '\n'.join(fixed_lines)

    def _is_character_name(self, line: str, index: int, all_lines: List[str]) -> bool:
        """Detect if line is likely a character name."""
        line = line.strip()

        # Character names are usually:
        # 1. Short (1-3 words)
        # 2. In uppercase (but OCR might mess this up)
        # 3. Followed by dialogue or parenthetical
        # 4. Centered or indented

        if not line or len(line) > 30:
            return False

        words = line.split()
        if len(words) > 3:
            return False

        # Check if next line is dialogue or parenthetical
        if index < len(all_lines) - 1:
            next_line = all_lines[index + 1].strip()
            if next_line.startswith('(') or len(next_line) > 20:
                return True

        return False

    def _ai_correction(self, text: str, context: str) -> str:
        """Use AI to correct text."""
        try:
            prompt = self._create_correction_prompt(text, context)

            # Call Ollama
            result = subprocess.run(
                ['ollama', 'run', self.model],
                input=prompt,
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode == 0:
                corrected = result.stdout.strip()
                # Clean up AI response
                corrected = self._clean_ai_response(corrected)
                return corrected
            else:
                logger.warning(f"AI correction failed: {result.stderr}")
                return text

        except subprocess.TimeoutExpired:
            logger.warning("AI correction timed out")
            return text
        except Exception as e:
            logger.error(f"AI correction error: {e}")
            return text

    def _create_correction_prompt(self, text: str, context: str) -> str:
        """Create prompt for AI correction."""
        if context == "screenplay":
            prompt = f"""Fix OCR errors in this screenplay excerpt. Common issues:
- Character names should be UPPERCASE
- Scene headers start with INT. or EXT.
- Fix obvious typos and OCR mistakes (like l/I confusion)
- Preserve screenplay format

Text to correct:
{text}

Return ONLY the corrected text, no explanations."""

        elif context == "dialogue":
            prompt = f"""Fix OCR errors in this dialogue. Keep natural speech patterns.
Fix obvious typos but preserve dialect if intentional.

Text:
{text}

Return ONLY corrected text."""

        else:
            prompt = f"""Fix obvious OCR errors and typos in this text:
{text}

Return ONLY corrected text."""

        return prompt

    def _clean_ai_response(self, response: str) -> str:
        """Clean up AI response."""
        # Remove common AI additions
        lines = response.split('\n')
        cleaned = []

        for line in lines:
            # Skip meta comments AI might add
            if line.startswith('Here') or line.startswith('Corrected'):
                continue
            if '```' in line:  # Remove code blocks
                continue
            cleaned.append(line)

        return '\n'.join(cleaned)

    def _validate_structure(self, text: str) -> bool:
        """Validate screenplay structure."""
        has_scene = False
        has_dialogue = False

        lines = text.split('\n')

        for line in lines:
            line = line.strip()

            # Check for scene headers
            for pattern in self.screenplay_patterns['scene_headers']:
                if re.match(pattern, line):
                    has_scene = True
                    break

            # Check for character names (uppercase)
            if line.isupper() and len(line.split()) <= 3:
                has_dialogue = True

        return has_scene or has_dialogue

    def _find_corrections(self, original: str, corrected: str) -> List[Dict]:
        """Find what corrections were made."""
        corrections = []

        # Simple word-by-word comparison
        orig_words = original.split()
        corr_words = corrected.split()

        for i, (o, c) in enumerate(zip(orig_words, corr_words)):
            if o != c:
                corrections.append({
                    'position': i,
                    'original': o,
                    'corrected': c,
                    'type': self._classify_correction(o, c)
                })

        return corrections

    def _classify_correction(self, original: str, corrected: str) -> str:
        """Classify type of correction made."""
        if original.lower() == corrected.lower():
            return "capitalization"
        elif len(original) == len(corrected):
            return "character_substitution"
        elif abs(len(original) - len(corrected)) == 1:
            return "character_addition_deletion"
        else:
            return "word_replacement"

    def _calculate_confidence(self, original: str, corrected: str) -> float:
        """Calculate confidence in corrections."""
        if original == corrected:
            return 1.0  # No corrections needed

        # Calculate edit distance ratio
        from difflib import SequenceMatcher
        ratio = SequenceMatcher(None, original, corrected).ratio()

        # High similarity = high confidence
        if ratio > 0.9:
            return 0.95
        elif ratio > 0.8:
            return 0.85
        elif ratio > 0.7:
            return 0.75
        else:
            return 0.6

    def batch_correct(self, texts: List[str], context: str = "screenplay") -> List[OCRCorrection]:
        """
        Correct multiple texts.

        Args:
            texts: List of texts to correct
            context: Context type

        Returns:
            List of corrections
        """
        corrections = []

        for i, text in enumerate(texts):
            logger.info(f"Correcting text {i+1}/{len(texts)}")
            correction = self.correct_with_ai(text, context)
            corrections.append(correction)

        return corrections


def correct_ocr_file(input_file: Path, output_file: Path, model: str = "phi3:mini") -> Dict:
    """
    Correct OCR errors in a file.

    Args:
        input_file: Input text file
        output_file: Output corrected file
        model: LLM model to use

    Returns:
        Statistics dictionary
    """
    corrector = OCRAICorrector(model=model)

    # Read input
    text = input_file.read_text(encoding='utf-8')

    # Split into chunks (AI has token limits)
    chunks = text.split('\n\n')
    corrected_chunks = []

    total_corrections = 0

    for chunk in chunks:
        if chunk.strip():
            correction = corrector.correct_with_ai(chunk)
            corrected_chunks.append(correction.corrected_text)
            total_corrections += len(correction.corrections_made)

    # Save corrected text
    corrected_text = '\n\n'.join(corrected_chunks)
    output_file.write_text(corrected_text, encoding='utf-8')

    return {
        'input_file': str(input_file),
        'output_file': str(output_file),
        'total_corrections': total_corrections,
        'chunks_processed': len(chunks),
        'model_used': model
    }


def main():
    """Test AI corrector."""
    print("="*60)
    print("OCR AI CORRECTOR")
    print("="*60)

    corrector = OCRAICorrector()

    # Test samples
    test_texts = [
        """lNT. OFFICE - DAY

        J0HN enters the room.

        john
        He11o, Mary. l'm here for the meeting.""",

        """CUT T0:

        EXT, PARK - NlGHT

        The moon sh1nes bright1y."""
    ]

    for i, text in enumerate(test_texts):
        print(f"\nTest {i+1}:")
        print("-"*40)
        print("Original:")
        print(text)
        print("\nCorrecting...")

        correction = corrector.correct_with_ai(text)

        print("\nCorrected:")
        print(correction.corrected_text)
        print(f"\nConfidence: {correction.confidence:.2f}")
        print(f"Corrections made: {len(correction.corrections_made)}")

    print("\n" + "="*60)
    print("AI Corrector ready!")


if __name__ == "__main__":
    main()