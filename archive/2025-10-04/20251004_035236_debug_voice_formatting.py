#!/usr/bin/env python3
"""Debug script to understand Voice and Formatting scores."""

from triple_core.core_1_specialists.voice.dr_voice import DrVoice
from triple_core.core_1_specialists.formatting.dr_formatting import DrFormatting
from pathlib import Path

# Load screenplay
pdf_path = "content/screenplays/personal/SONHOS SEM LEMBRANÇAS T.3.pdf"
txt_path = "content/screenplays/personal/sonhos_sem_lembrancas_t3.txt"

# Use TXT for easier debugging
with open(txt_path, 'r', encoding='utf-8') as f:
    screenplay_text = f.read()

print("="*80)
print("🔍 DEBUGGING VOICE CONSISTENCY")
print("="*80)
print()

# Test DrVoice
voice = DrVoice()
voice_result = voice.analyze(screenplay_text)

print(f"Score: {voice_result['score']}/100")
print(f"Characters detected: {voice_result['character_count']}")
print(f"Characters with distinct voice: {voice_result['characters_with_distinct_voice']}")
print()
print("Character Analysis:")
for char in voice_result['character_analyses'][:5]:  # Top 5
    print(f"  {char['name']}: {char['voice_score']:.1f}/100")
    print(f"    Line count: {char['line_count']}")
    print(f"    Vocabulary uniqueness: {char['vocabulary_uniqueness']:.2f}")
    print(f"    Formality: {char['formality']:.2f}")
    print(f"    Age indicators: {char['age_indicators']}")
print()
print("Diagnosis:")
print(voice_result['diagnosis'])
print()
print("Top Recommendations:")
for i, rec in enumerate(voice_result['recommendations'][:3], 1):
    print(f"{i}. {rec}")
print()

print("="*80)
print("🔍 DEBUGGING FORMATTING")
print("="*80)
print()

# Test DrFormatting
formatting = DrFormatting()
formatting_result = formatting.analyze(screenplay_text)

print(f"Score: {formatting_result['score']}/100")
print(f"Total lines: {formatting_result['total_lines']}")
print(f"Scene headings: {formatting_result['scene_heading_count']}")
print(f"Dialogue lines: {formatting_result['dialogue_line_count']}")
print(f"Action lines: {formatting_result['action_line_count']}")
print(f"Properly formatted: {formatting_result['proper_format_percentage']:.1f}%")
print()
print(f"Issues found: {len(formatting_result['issues'])}")
print("Top issues:")
for issue in formatting_result['issues'][:5]:
    print(f"  Line {issue.line_number} ({issue.severity}): {issue.issue_type}")
    print(f"    {issue.description}")
print()
print(f"Rule violations: {len(formatting_result['rule_violations'])}")
print("Top violations:")
for viol in formatting_result['rule_violations'][:5]:
    print(f"  [{viol['severity'].upper()}] {viol['title']}")
    print(f"    {viol['message']}")
print()
print("Diagnosis:")
print(formatting_result['diagnosis'])
print()
print("Top Recommendations:")
for i, rec in enumerate(formatting_result['recommendations'][:3], 1):
    print(f"{i}. {rec}")
