#!/usr/bin/env python3
"""
Generate Ollama Modelfiles from Scripturemon Ultimate specialists
"""

import re
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def extract_prompt_from_md(md_file):
    """Extract the PROMPT SYSTEM section from a specialist .md file"""
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Try different patterns to extract prompt
    patterns = [
        r'## PROMPT SYSTEM\n\n(.*?)(?:\n===|\n##|$)',
        r'## PROMPT SYSTEM\n(.*?)(?:\n===|\n##|$)',
        r'PROMPT SYSTEM.*?\n(.*?)(?:\n===|\n##|$)'
    ]

    for pattern in patterns:
        match = re.search(pattern, content, re.DOTALL)
        if match:
            prompt = match.group(1).strip()
            # Clean up the prompt
            prompt = prompt.replace('"""', '\\"""')  # Escape triple quotes
            return prompt

    logger.warning(f"Could not extract prompt from {md_file.name}")
    return None

def create_modelfile(specialist_file, output_dir, base_model="mixtral:8x7b-instruct-v0.1-q5_K_M"):
    """Create a Modelfile for a specialist"""

    prompt = extract_prompt_from_md(specialist_file)
    if not prompt:
        return False

    # Extract specialist name and number
    name = specialist_file.stem
    parts = name.split('_')
    number = parts[0] if parts[0].isdigit() else ""
    specialist_name = '_'.join(parts[1:]) if number else name

    # Special handling for the evaluator (70B model)
    if "70B" in name or "EVALUATOR" in name.upper():
        base_model = "llama3.1:70b-instruct-q4_K_M"
        num_predict = 3000
        num_ctx = 131072
    else:
        num_predict = 1500
        num_ctx = 32768

    modelfile_content = f'''# Scripturemon Ultimate - {specialist_name.replace('_', ' ').title()} Specialist
# Generated from: {specialist_file.name}

FROM {base_model}

SYSTEM """
{prompt}
"""

# Optimized parameters for screenplay analysis
PARAMETER temperature 0.7
PARAMETER top_p 0.9
PARAMETER num_predict {num_predict}
PARAMETER num_ctx {num_ctx}
PARAMETER repeat_penalty 1.1
PARAMETER seed -1
'''

    # Create output filename
    output_filename = f"{number}_{specialist_name.lower()}.modelfile" if number else f"{specialist_name.lower()}.modelfile"
    output_path = output_dir / output_filename

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(modelfile_content)

    logger.info(f"✅ Created: {output_filename}")
    return True

def create_orchestrator_modelfile(output_dir):
    """Create the main orchestrator Modelfile"""

    orchestrator_content = '''# Scripturemon Ultimate - Main Orchestrator
# Coordinates all 23 specialists sequentially

FROM mixtral:8x7b-instruct-v0.1-q5_K_M

SYSTEM """
You are the Scripturemon Ultimate Orchestrator, coordinating 23 specialist analyses for comprehensive screenplay evaluation.

Your role:
1. Manage sequential analysis flow
2. Pass context between specialists
3. Ensure each specialist builds on previous insights
4. Maintain consistency across all analyses

You work with these specialists in order:
1. DIALOGUE - Conversation and speech patterns
2. CHARACTER - Character development and arcs
3. PACING - Rhythm and tempo
4. THEME - Thematic elements and meaning
5. ACTION - Action sequences and movement
6. STRUCTURE - Three-act structure and plot
7. CONFLICT - Central conflicts and obstacles
8. TENSION - Suspense and dramatic tension
9. SUBTEXT - Underlying meanings
10. EXPOSITION - Information delivery
11. TRANSITIONS - Scene connections
12. OPENING - First impressions
13. CLIMAX - Peak moments
14. RESOLUTION - Story closure
15. WORLD-BUILDING - Universe creation
16. STAKES - What matters and why
17. MOTIVATION - Character drivers
18. BACKSTORY - Historical context
19. FORESHADOWING - Setup and payoff
20. TWIST - Surprises and revelations
21. SYMBOLISM - Symbolic elements
22. TONE - Mood and atmosphere
23. GENRE - Genre conventions

Maintain professional, insightful analysis throughout.
"""

PARAMETER temperature 0.7
PARAMETER top_p 0.9
PARAMETER num_predict 2000
PARAMETER num_ctx 65536
PARAMETER repeat_penalty 1.1
'''

    output_path = output_dir / "00_orchestrator.modelfile"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(orchestrator_content)

    logger.info("✅ Created: 00_orchestrator.modelfile")

def create_evaluator_modelfile(output_dir):
    """Create the 70B evaluator Modelfile"""

    evaluator_content = '''# Scripturemon Ultimate - Final Evaluator (70B)
# Synthesizes all 23 specialist analyses

FROM llama3.1:70b-instruct-q4_K_M

SYSTEM """
You are the ULTIMATE SCREENPLAY EVALUATOR reviewing analyses from 23 specialists.

Your task is to synthesize all insights into a professional, actionable evaluation.

Based on the 23 specialist analyses, provide:

1. **OVERALL ASSESSMENT** (Score: 1-100)
   - Core strengths identified across analyses
   - Critical weaknesses consensus
   - Unique elements noted

2. **SYNTHESIS OF KEY FINDINGS**
   - Where specialists agree
   - Where specialists disagree (and your verdict)
   - Most important insights

3. **ACTIONABLE RECOMMENDATIONS**
   - Top 5 specific improvements needed
   - Elements to preserve
   - Priority revision areas

4. **MARKET ANALYSIS**
   - Genre positioning
   - Comparable successful films
   - Target audience
   - Commercial potential

5. **FINAL VERDICT**
   - Pass / Consider / Recommend / Strong Recommend
   - One-line pitch
   - Executive summary (3 sentences max)

Be specific, reference specialist findings by name, and provide professional-grade conclusions.
"""

PARAMETER temperature 0.7
PARAMETER top_p 0.9
PARAMETER num_predict 3000
PARAMETER num_ctx 131072
PARAMETER repeat_penalty 1.1
'''

    output_path = output_dir / "24_evaluator_70b.modelfile"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(evaluator_content)

    logger.info("✅ Created: 24_evaluator_70b.modelfile")

def create_registration_script(output_dir):
    """Create a bash script to register all models with Ollama"""

    script_content = '''#!/bin/bash
# Register all Scripturemon Ultimate models with Ollama

echo "🎬 Registering Scripturemon Ultimate models..."
echo "This will create 25 models (23 specialists + orchestrator + evaluator)"
echo ""

# Counter for progress
count=0
total=25

# Register orchestrator
echo "[1/$total] Creating orchestrator..."
ollama create scripturemon-orchestrator -f 00_orchestrator.modelfile
((count++))

# Register all specialists
for file in [0-9][0-9]_*.modelfile; do
    if [[ "$file" != "00_orchestrator.modelfile" && "$file" != "24_evaluator_70b.modelfile" ]]; then
        # Extract name without number prefix and extension
        name=$(basename "$file" .modelfile)
        name_clean=${name#*_}  # Remove number prefix

        ((count++))
        echo "[$count/$total] Creating specialist: $name_clean..."
        ollama create "scripturemon-$name_clean" -f "$file"
    fi
done

# Register evaluator
((count++))
echo "[$count/$total] Creating 70B evaluator..."
ollama create scripturemon-evaluator -f 24_evaluator_70b.modelfile

echo ""
echo "✅ Registration complete!"
echo ""
echo "To list all Scripturemon models:"
echo "  ollama list | grep scripturemon"
echo ""
echo "To test a specialist:"
echo "  ollama run scripturemon-dialogue < test_screenplay.txt"
echo ""
echo "To remove all Scripturemon models:"
echo "  ollama list | grep scripturemon | awk '{print $1}' | xargs -I {} ollama rm {}"
'''

    script_path = output_dir / "register_models.sh"
    with open(script_path, 'w', encoding='utf-8') as f:
        f.write(script_content)

    # Make executable
    script_path.chmod(0o755)

    logger.info("✅ Created: register_models.sh")

def main():
    """Generate all Modelfiles"""

    # Setup directories
    specialists_dir = Path("/Users/clubproducoes/Digimundo/scripturemon-ultimate/super_specialists")
    output_dir = Path("/Users/clubproducoes/Digimundo/scripturemon-ultimate/modelfiles")
    output_dir.mkdir(exist_ok=True)

    logger.info("=" * 60)
    logger.info("SCRIPTUREMON ULTIMATE - MODELFILE GENERATOR")
    logger.info("=" * 60)

    # Create orchestrator
    create_orchestrator_modelfile(output_dir)

    # Process all specialist files
    specialist_files = sorted([f for f in specialists_dir.glob("*.md") if "README" not in f.name])

    success_count = 0
    for specialist_file in specialist_files:
        if create_modelfile(specialist_file, output_dir):
            success_count += 1

    # Create evaluator
    create_evaluator_modelfile(output_dir)

    # Create registration script
    create_registration_script(output_dir)

    # Summary
    logger.info("=" * 60)
    logger.info(f"✅ Generated {success_count + 2} Modelfiles")
    logger.info(f"📁 Output directory: {output_dir}")
    logger.info("")
    logger.info("Next steps:")
    logger.info("1. cd modelfiles/")
    logger.info("2. ./register_models.sh  # Register all models")
    logger.info("3. ollama list | grep scripturemon  # Verify installation")
    logger.info("=" * 60)

if __name__ == "__main__":
    main()