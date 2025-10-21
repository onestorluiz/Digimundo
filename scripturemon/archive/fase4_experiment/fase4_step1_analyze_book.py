#!/usr/bin/env python3
"""
FASE 4 - STEP 1: Analyze Theory Book Completely

This script analyzes a complete theory book to extract:
- Core concepts (10-15 principais)
- Connections between concepts (grafo)
- Concrete examples from the book
- Unique vocabulary/terminology
- Author's argumentative structure

Author: Scripturemon Team
Date: 2025-10-10
Version: 1.0 (FASE 4A - Proof of Concept)
"""

import json
import sys
from pathlib import Path
import subprocess
import time

# Theory books directory
THEORY_DIR = Path(__file__).parent / "knowledge" / "theory_books"

# Book mapping for FASE 4A
BOOK_MAPPING = {
    'egri': 'the_art_of_dramatic_writing_its_basis_in_the_creative_-_lajos_egri.txt'
}


def load_book(author: str) -> str:
    """Load complete book text for given author."""
    if author not in BOOK_MAPPING:
        raise ValueError(f"Author '{author}' not found in BOOK_MAPPING")

    book_file = THEORY_DIR / BOOK_MAPPING[author]

    if not book_file.exists():
        raise FileNotFoundError(f"Book file not found: {book_file}")

    print(f"📚 Loading book: {book_file.name}")
    with open(book_file, 'r', encoding='utf-8') as f:
        content = f.read()

    word_count = len(content.split())
    print(f"   ✅ Loaded: {word_count:,} words (~{word_count * 1.3:.0f} tokens)")

    return content


def build_analysis_prompt(author: str, book_text: str) -> str:
    """Build LLM prompt for complete book analysis."""

    # Get author specialty
    specialty_map = {
        'egri': 'PREMISE and CHARACTER DEVELOPMENT'
    }
    specialty = specialty_map.get(author, 'SCREENPLAY THEORY')

    prompt = f"""
# FASE 4 - COMPLETE BOOK ANALYSIS

You are analyzing the COMPLETE book of **{author.upper()}** on {specialty}.

## YOUR MISSION

Read the entire book provided below and extract a DEEP UNDERSTANDING of the author's methodology.

## OUTPUT REQUIRED (JSON Format)

Generate a JSON object with the following structure:

```json
{{
  "author": "{author.upper()}",
  "specialty": "{specialty}",
  "core_concepts": [
    {{
      "concept": "Name of concept",
      "definition": "Clear definition in author's words",
      "chapter": 1,
      "page_reference": "Chapter/Section reference",
      "examples": ["Example 1 from book", "Example 2 from book"],
      "connections": ["Concept A", "Concept B"],
      "importance": "high|medium|low"
    }}
    // 10-15 core concepts total
  ],
  "concept_graph": {{
    "Concept A": ["Connected to B", "Connected to C"],
    "Concept B": ["Connected to A", "Connected to D"]
    // Full graph of relationships
  }},
  "vocabulary": {{
    "Term 1": "Definition as used by author",
    "Term 2": "Definition as used by author"
    // 15-25 unique terms
  }},
  "argument_structure": {{
    "type": "deductive|inductive|dialectical",
    "flow": "Description of how author builds argument",
    "key_chapters": [1, 4, 6, 8],
    "methodology_summary": "2-3 sentence summary of author's approach"
  }},
  "concrete_examples": [
    {{
      "work": "Name of play/film referenced",
      "context": "What author uses it to demonstrate",
      "chapter": 2,
      "analysis": "Brief summary of author's analysis"
    }}
    // 8-12 concrete examples from the book
  ],
  "key_quotes": [
    {{
      "quote": "Exact quote from book",
      "context": "What it demonstrates",
      "chapter": 3,
      "importance": "high|medium"
    }}
    // 10-15 key quotes
  ]
}}
```

## CRITICAL INSTRUCTIONS

1. **READ THE ENTIRE BOOK**: Don't summarize prematurely - read all the way through
2. **EXTRACT, DON'T INVENT**: Use only concepts/terms/examples FROM THE BOOK
3. **BE SPECIFIC**: Include chapter/page references for everything
4. **FIND CONNECTIONS**: Map how concepts relate to each other
5. **IDENTIFY UNIQUE VOCABULARY**: What terms are specific to this author?
6. **TRACE ARGUMENT FLOW**: How does the author build their case?
7. **CONCRETE EXAMPLES**: Which plays/films does author analyze?

## IMPORTANT REMINDERS

- Focus on the METHODOLOGY, not just the content
- Identify what makes THIS AUTHOR unique vs other theorists
- Map the LOGICAL STRUCTURE of the author's argument
- Extract EXAMPLES the author uses (plays, films, characters)
- Note RECURRING THEMES/CONCEPTS throughout the book

---

## COMPLETE BOOK TEXT

{book_text}

---

## BEGIN ANALYSIS

Generate the JSON analysis now, ensuring:
- 10-15 core concepts minimum
- Full concept graph showing all relationships
- 15-25 vocabulary terms unique to this author
- 8-12 concrete examples from the book
- 10-15 key quotes with context

Output ONLY valid JSON - no markdown formatting, no explanation outside JSON.
"""

    return prompt


def call_llm(prompt: str, model: str = "scripturemon-optimized") -> str:
    """Call Ollama LLM with prompt."""
    print(f"\n🤖 Calling LLM ({model})...")
    print(f"   ⏳ This may take 3-5 minutes for deep analysis...")

    start_time = time.time()

    try:
        result = subprocess.run(
            ['ollama', 'run', model],
            input=prompt,
            capture_output=True,
            text=True,
            timeout=600  # 10 min timeout for deep analysis
        )

        if result.returncode != 0:
            raise Exception(f"Ollama failed: {result.stderr}")

        response = result.stdout.strip()

        # Clean up any markdown formatting
        if response.startswith('```json'):
            response = response.split('```json')[1]
        if response.startswith('```'):
            response = response.split('```')[1]
        if response.endswith('```'):
            response = response.rsplit('```', 1)[0]

        response = response.strip()

        elapsed = time.time() - start_time
        print(f"   ✅ LLM response received: {len(response):,} chars in {elapsed:.1f}s")

        return response

    except subprocess.TimeoutExpired:
        raise Exception("LLM timeout after 10 minutes")
    except Exception as e:
        raise Exception(f"LLM call failed: {e}")


def validate_and_save_analysis(analysis_json: str, author: str) -> dict:
    """Validate JSON and save to file."""
    print(f"\n📊 Validating analysis...")

    try:
        analysis = json.loads(analysis_json)
        print("   ✅ Valid JSON")
    except json.JSONDecodeError as e:
        print(f"   ❌ Invalid JSON: {e}")
        # Try to extract JSON from response
        import re
        json_match = re.search(r'\{.*\}', analysis_json, re.DOTALL)
        if json_match:
            try:
                analysis = json.loads(json_match.group())
                print("   ✅ Extracted valid JSON from response")
            except:
                raise ValueError("Could not parse JSON from LLM response")
        else:
            raise ValueError("No JSON found in LLM response")

    # Validate structure
    required_keys = ['author', 'specialty', 'core_concepts', 'concept_graph',
                     'vocabulary', 'argument_structure', 'concrete_examples', 'key_quotes']

    for key in required_keys:
        if key not in analysis:
            print(f"   ⚠️  Warning: Missing key '{key}'")

    # Print stats
    print(f"\n📈 Analysis Stats:")
    print(f"   Core Concepts: {len(analysis.get('core_concepts', []))}")
    print(f"   Vocabulary Terms: {len(analysis.get('vocabulary', {}))}")
    print(f"   Concrete Examples: {len(analysis.get('concrete_examples', []))}")
    print(f"   Key Quotes: {len(analysis.get('key_quotes', []))}")
    print(f"   Concept Graph Nodes: {len(analysis.get('concept_graph', {}))}")

    # Save to file
    output_file = Path(__file__).parent / f"fase4_book_analysis_{author}.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(analysis, f, indent=2, ensure_ascii=False)

    print(f"\n💾 Analysis saved: {output_file}")
    print(f"   File size: {output_file.stat().st_size:,} bytes")

    return analysis


def main():
    """Main execution."""
    print("="*80)
    print("🚀 FASE 4A - STEP 1: COMPLETE BOOK ANALYSIS")
    print("="*80)
    print()

    # Check arguments
    if len(sys.argv) < 2:
        print("Usage: python3 fase4_step1_analyze_book.py <author>")
        print("Example: python3 fase4_step1_analyze_book.py egri")
        sys.exit(1)

    author = sys.argv[1].lower()

    try:
        # Step 1: Load book
        print(f"\n📖 STEP 1: Loading {author.upper()} book...")
        book_text = load_book(author)

        # Step 2: Build analysis prompt
        print(f"\n🔨 STEP 2: Building analysis prompt...")
        prompt = build_analysis_prompt(author, book_text)
        print(f"   ✅ Prompt ready: {len(prompt):,} chars")

        # Step 3: Call LLM for deep analysis
        print(f"\n🤖 STEP 3: Analyzing book with LLM...")
        print(f"   ⚠️  This will take 3-5 minutes - be patient!")
        analysis_json = call_llm(prompt)

        # Step 4: Validate and save
        print(f"\n💾 STEP 4: Validating and saving analysis...")
        analysis = validate_and_save_analysis(analysis_json, author)

        # Success!
        print("\n" + "="*80)
        print("✅ STEP 1 COMPLETE!")
        print("="*80)
        print(f"\n📊 Book Analysis Summary:")
        print(f"   Author: {analysis.get('author', 'N/A')}")
        print(f"   Specialty: {analysis.get('specialty', 'N/A')}")
        print(f"   Core Concepts Extracted: {len(analysis.get('core_concepts', []))}")
        print(f"   Vocabulary Mapped: {len(analysis.get('vocabulary', {}))}")
        print(f"   Examples Identified: {len(analysis.get('concrete_examples', []))}")
        print()
        print(f"📁 Next Step: Run fase4_step2_generate_prompt.py {author}")
        print()

    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
