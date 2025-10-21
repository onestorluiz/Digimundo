#!/usr/bin/env python3
"""Test prompts for quadruple pipeline"""

import sys
import os
import logging
from pathlib import Path

# Setup logging to see pipeline logs
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from apps.scripturemon.quadruple_pipeline import run_pipeline

# Test prompts
prompts = [
    {
        "name": "a",
        "text": "Explique em 2 parágrafos a estética de VHS no cinema contemporâneo.",
        "expected_mode": "normal"
    },
    {
        "name": "b", 
        "text": "Faça uma análise profunda e detalhada do simbolismo de Os Miseráveis, explorando as camadas narrativas, os arquétipos dos personagens e as conexões com a literatura clássica francesa do século XIX.",
        "expected_mode": "deep"
    }
]

print("="*60)
print("TESTING QUADRUPLE PIPELINE")
print("="*60)

for prompt_info in prompts:
    print(f"\n>>> Test {prompt_info['name']}: {prompt_info['text'][:50]}...")
    print(f"    Expected mode: {prompt_info['expected_mode']}")
    print("-"*60)
    
    # Run pipeline
    result = run_pipeline(prompt_info['text'], mode="auto")
    
    # Save result
    output_file = Path(f"reports/harmony_vFinal/phase3_pipeline/{prompt_info['name']}.txt")
    output_file.write_text(result, encoding='utf-8')
    
    print(f"Result saved to: {output_file}")
    print(f"Response length: {len(result)} chars")
    print(f"First 200 chars: {result[:200]}...")
    
print("\n" + "="*60)
print("TESTS COMPLETE")