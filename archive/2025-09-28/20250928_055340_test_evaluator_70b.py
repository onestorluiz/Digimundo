#!/usr/bin/env python3
"""
TEST EVALUATOR WITH LLAMA 70B
Teste rápido do sistema de avaliação com o modelo 70B
"""

import json
import requests
import time
from datetime import datetime
from pathlib import Path
import re

# Script de teste - Marcus's revenge story
TEST_SCRIPT = """INT. ABANDONED CHURCH - NIGHT

Rain pounds the broken windows. MARCUS CHEN (40s), haunted eyes,
enters the decrepit sanctuary. His footsteps echo.

FATHER MARTINEZ (60s) kneels at the altar, praying.

                    FATHER MARTINEZ
          I've been expecting you, Marcus.

Marcus pulls out a SYRINGE filled with black liquid.

                    MARCUS
          Forty years ago, you and the others
          destroyed three boys at St. Mary's.
          Tommy. Michael. James.

                    FATHER MARTINEZ
          That was... a different time. I've
          changed. I've repented.

                    MARCUS
          They killed themselves. One by one.
          Fourteen. Fifteen. Sixteen years old.

Marcus steps closer. Thunder EXPLODES outside.

                    MARCUS (CONT'D)
          I promised them justice. The kind
          that doesn't wait forty years.

                    FATHER MARTINEZ
          You're not a killer, Marcus. You're
          a good man. Your mother raised you—

                    MARCUS
          My mother signed the papers. She
          sent me to that place. To you.

He raises the syringe.

                    MARCUS (CONT'D)
          This is the same drug you used on us.
          To make us "compliant." Remember?

Martinez's eyes widen in recognition and terror.

                    FATHER MARTINEZ
          Please... I have a family now...

                    MARCUS
          So did they.

FADE TO BLACK."""

def test_specialist_prompts():
    """Testa alguns especialistas com o modelo 70B"""

    print("=" * 60)
    print("TESTING LLAMA 70B WITH SPECIALIST PROMPTS")
    print("=" * 60)

    # Selecionar 3 especialistas para teste rápido
    test_specialists = [
        {
            "name": "CHARACTER",
            "file": "02_CHARACTER_ULTRA.md",
            "expected_score": 103
        },
        {
            "name": "TWIST",
            "file": "20_TWIST_INTEGRATED_SUPREME.md",
            "expected_score": 184
        },
        {
            "name": "GENRE",
            "file": "23_GENRE_INTEGRATED_ULTIMATE.md",
            "expected_score": 187
        }
    ]

    results = []

    for specialist in test_specialists:
        print(f"\nTesting {specialist['name']}...")

        # Ler arquivo do especialista
        specialist_path = Path(f"/Users/clubproducoes/Digimundo/scripturemon-ultimate/super_specialists/{specialist['file']}")

        if not specialist_path.exists():
            print(f"  ❌ File not found: {specialist['file']}")
            continue

        with open(specialist_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extrair prompt
        prompt_match = re.search(r'## PROMPT SYSTEM\n\n(.*?)\n\n===', content, re.DOTALL)
        if not prompt_match:
            prompt_match = re.search(r'## PROMPT SYSTEM\n\n(.*?)(?:\n===|\n##|$)', content, re.DOTALL)

        if not prompt_match:
            print(f"  ❌ Could not extract prompt from {specialist['file']}")
            continue

        system_prompt = prompt_match.group(1)

        # Testar com Llama 70B
        print(f"  Running analysis with llama3.1:70b...")
        start_time = time.time()

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Analyze this screenplay:\n\n{TEST_SCRIPT}"}
        ]

        data = {
            "model": "llama3.1:70b-instruct-q4_K_M",
            "messages": messages,
            "stream": False,
            "options": {
                "temperature": 0.7,
                "top_p": 0.9,
                "num_predict": 2000,  # Reduzido para teste rápido
                "num_ctx": 8192
            }
        }

        try:
            response = requests.post(
                "http://localhost:11434/api/chat",
                json=data,
                timeout=120
            )

            if response.status_code == 200:
                result = response.json()
                analysis = result.get('message', {}).get('content', '')

                elapsed = time.time() - start_time

                # Calcular score simplificado
                citations = len(re.findall(r'(?i)(mckee|truby|field|snyder|vogler|campbell|aristotle)', analysis))
                techniques = len(re.findall(r'(?i)(technique|method|approach|principle|beat|structure)', analysis))
                score = citations + (techniques * 2)

                results.append({
                    "name": specialist['name'],
                    "score": score,
                    "expected": specialist['expected_score'],
                    "time": elapsed,
                    "words": len(analysis.split())
                })

                print(f"  ✅ Complete in {elapsed:.1f}s")
                print(f"     Score: {score} points (expected: {specialist['expected_score']})")
                print(f"     Words: {len(analysis.split())}")
                print(f"     Sample: {analysis[:150]}...")

            else:
                print(f"  ❌ Error: Status {response.status_code}")

        except Exception as e:
            print(f"  ❌ Error: {e}")

    return results

def test_synthesis():
    """Testa síntese final com o modelo 70B"""

    print("\n" + "=" * 60)
    print("TESTING FINAL SYNTHESIS WITH LLAMA 70B")
    print("=" * 60)

    synthesis_prompt = """You are the ULTIMATE SCREENPLAY EVALUATOR synthesizing insights from specialist analyses.

Based on the screenplay about Marcus's revenge on Father Martinez, provide:

1. CORE NARRATIVE ASSESSMENT
   - Story strengths and weaknesses
   - Character depth analysis
   - Thematic resonance

2. TECHNICAL EXCELLENCE
   - Structure and pacing
   - Dialogue quality
   - Visual storytelling

3. MARKET POTENTIAL
   - Genre positioning (Thriller/Drama)
   - Comparable films
   - Target audience

4. FINAL VERDICT
   - Score (1-100)
   - Recommendation level
   - One-line pitch

Be concise but comprehensive. Reference screenwriting theory where relevant."""

    print("Running synthesis with llama3.1:70b...")
    start_time = time.time()

    messages = [
        {"role": "system", "content": synthesis_prompt},
        {"role": "user", "content": f"Synthesize analysis of:\n\n{TEST_SCRIPT}"}
    ]

    data = {
        "model": "llama3.1:70b-instruct-q4_K_M",
        "messages": messages,
        "stream": False,
        "options": {
            "temperature": 0.7,
            "top_p": 0.9,
            "num_predict": 3000,
            "num_ctx": 8192
        }
    }

    try:
        response = requests.post(
            "http://localhost:11434/api/chat",
            json=data,
            timeout=180
        )

        if response.status_code == 200:
            result = response.json()
            synthesis = result.get('message', {}).get('content', '')

            elapsed = time.time() - start_time

            print(f"✅ Synthesis complete in {elapsed:.1f}s")
            print(f"   Words: {len(synthesis.split())}")
            print("\n" + "-" * 40)
            print("SYNTHESIS OUTPUT:")
            print("-" * 40)
            print(synthesis)
            print("-" * 40)

            return synthesis
        else:
            print(f"❌ Error: Status {response.status_code}")

    except Exception as e:
        print(f"❌ Error: {e}")

    return None

def main():
    """Executa testes completos"""

    print("\n🚀 SCRIPTUREMON ULTIMATE - LLAMA 70B TEST")
    print("=" * 60)

    # Testar especialistas
    print("\n📊 Phase 1: Testing Specialists")
    specialist_results = test_specialist_prompts()

    # Testar síntese
    print("\n📊 Phase 2: Testing Synthesis")
    synthesis = test_synthesis()

    # Resumo final
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)

    if specialist_results:
        print("\nSpecialist Performance:")
        total_score = 0
        for r in specialist_results:
            print(f"  {r['name']}: {r['score']} pts in {r['time']:.1f}s")
            total_score += r['score']
        print(f"\nTotal Score: {total_score} points")

    if synthesis:
        print(f"\nSynthesis: Generated {len(synthesis.split())} words")

    print("\n✅ Test complete! Llama 70B is working with the system.")
    print("=" * 60)

if __name__ == "__main__":
    main()