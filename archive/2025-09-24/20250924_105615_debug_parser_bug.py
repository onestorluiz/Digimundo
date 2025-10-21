#!/usr/bin/env python3
"""
DEBUG DO BUG DO PARSER
Rastrear onde o JSON está sendo cortado
"""

import subprocess
import json

# Teste 1: Chamar Ollama diretamente
print("🧪 TESTE 1: Ollama direto com subprocess")
print("-"*50)

prompt = """Analyze this: Hero saves world.

Return EXACTLY this JSON structure:
{{
  "metadata": {{"genre": "Action", "pages": "1"}},
  "evidence_log": [{{"page": 1, "evidence": "Hero action"}}],
  "analise_estrutural": {{"inciting_incident": {{"page": "1", "description": "Crisis"}}}},
  "validation": {{"score": 85, "valid": true}}
}}
"""

result = subprocess.run(
    ["ollama", "run", "scripturemon-v9-final"],
    input=prompt,
    capture_output=True,
    text=True,
    timeout=30
)

output = result.stdout
print(f"Output length: {len(output)} chars")
print(f"First 200 chars: {output[:200]}")
print()

# Teste 2: Parse com improved_json_parser
print("🧪 TESTE 2: Parse com improved_json_parser")
print("-"*50)

from improved_json_parser import robust_json_parse

parsed, conf = robust_json_parse(output)
print(f"Confidence: {conf:.2f}")

if parsed:
    print(f"Keys parsed: {list(parsed.keys())}")
    print(f"Full result:")
    print(json.dumps(parsed, indent=2)[:500])
else:
    print("Parse failed!")

print()

# Teste 3: Parse manual
print("🧪 TESTE 3: Parse manual direto")
print("-"*50)

if '{' in output and '}' in output:
    start = output.find('{')
    end = output.rfind('}') + 1
    json_str = output[start:end]

    try:
        manual_parsed = json.loads(json_str)
        print(f"Keys manual: {list(manual_parsed.keys())}")
    except Exception as e:
        print(f"Manual parse failed: {e}")
        print(f"JSON string: {json_str[:200]}...")

print("\n🥷 DIGIMUNDO PRESENTE")