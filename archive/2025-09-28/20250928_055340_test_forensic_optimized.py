#!/usr/bin/env python3
"""
🎯 TESTE: Forensic Optimized vs Original
Verifica se aplicação dos insights do Mixtral melhora o output
"""

import json
import subprocess
import time
from pathlib import Path
import re

def count_metrics(response: str) -> dict:
    """Conta métricas da resposta"""

    words = len(response.split())

    # Detectar chain-of-thought
    cot_phrases = ["think through", "reasoning process", "based on", "i deduce", "hypothesis"]
    cot_count = sum(1 for phrase in cot_phrases if phrase in response.lower())

    # Detectar citações
    quotes = len(re.findall(r'"[^"]{10,}"', response))

    # Detectar exhibits/evidências numeradas
    exhibits = len(re.findall(r'exhibit [a-z]', response.lower()))

    # Detectar seções
    sections = len(re.findall(r'part [ivx]+:', response.lower()))

    return {
        "words": words,
        "cot_indicators": cot_count,
        "quotes": quotes,
        "exhibits": exhibits,
        "sections": sections
    }

def test_forensic(file_path: str, version: str, test_script: str):
    """Testa uma versão do Forensic"""

    print(f"\n🔬 Testing {version}...")

    if not Path(file_path).exists():
        print(f"   ❌ File not found")
        return None

    with open(file_path, 'r') as f:
        content = f.read()

    # Extrair system prompt
    system_match = re.search(r'## PROMPT SYSTEM.*?(?=\n##|\n---|\Z)', content, re.S)
    if not system_match:
        print(f"   ❌ Could not extract prompt")
        return None

    system_prompt = system_match.group(0).replace("## PROMPT SYSTEM\n\n", "").strip()

    # Preparar mensagens
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Analyze this dialogue:\n\n{test_script}"}
    ]

    # Parâmetros otimizados baseados no documento
    options = {
        "temperature": 0.75,
        "top_p": 0.9,
        "top_k": 50,
        "repeat_penalty": 1.1,
        "num_predict": 2500
    }

    if "OPTIMIZED" in version:
        # Versão otimizada pode usar temperatura ligeiramente maior
        options["temperature"] = 0.78

    data = {
        "model": "mixtral:8x7b-instruct-v0.1-q5_K_M",
        "messages": messages,
        "stream": False,
        "options": options
    }

    start = time.time()

    try:
        cmd = ["curl", "-s", "-X", "POST", "http://localhost:11434/api/chat",
               "-H", "Content-Type: application/json",
               "-d", json.dumps(data)]

        result = subprocess.run(cmd, capture_output=True, text=True, timeout=90)

        if result.returncode == 0:
            response_data = json.loads(result.stdout)
            response_text = response_data.get("message", {}).get("content", "")

            if response_text:
                elapsed = time.time() - start
                metrics = count_metrics(response_text)

                print(f"   ✅ Completed in {elapsed:.1f}s")
                print(f"   📝 Words: {metrics['words']}")
                print(f"   💭 Chain-of-thought indicators: {metrics['cot_indicators']}")
                print(f"   📌 Direct quotes: {metrics['quotes']}")
                print(f"   🏷️ Exhibits: {metrics['exhibits']}")
                print(f"   📑 Sections: {metrics['sections']}")

                return {
                    "version": version,
                    "words": metrics['words'],
                    "time": elapsed,
                    "metrics": metrics,
                    "response": response_text
                }

    except Exception as e:
        print(f"   ❌ Error: {e}")

    return None

def main():
    """Testa Forensic Original vs Optimized"""

    print("="*60)
    print("🎯 TESTE: Forensic Original vs Optimized")
    print("Aplicando insights do Mixtral 8x7B")
    print("="*60)

    # Script de teste
    test_script = """FADE IN:

INT. COFFEE SHOP - DAY

SARAH (28) sits across from MICHAEL (30). Two cups of coffee between them.

SARAH
We need to talk about what happened.

MICHAEL
(avoiding eye contact)
Nothing happened.

SARAH
Michael, please. Don't do this.

MICHAEL
Do what? I'm just having coffee.

SARAH
(leaning forward)
Three years, Michael. Three years and you can't even look at me?

Michael finally meets her eyes.

MICHAEL
What do you want me to say?

SARAH
The truth. For once, just the truth.

MICHAEL
(long pause)
The truth is... I'm scared.

SARAH
Of what?

MICHAEL
Of hurting you more than I already have.

FADE OUT."""

    # Testar versões
    versions = [
        ("super_specialists/02_dialogue_forensic.md", "Forensic Original"),
        ("super_specialists/02_dialogue_forensic_OPTIMIZED.md", "Forensic Optimized")
    ]

    results = []

    for file_path, version_name in versions:
        result = test_forensic(file_path, version_name, test_script)
        if result:
            results.append(result)

            # Salvar resposta
            with open(f"{version_name.replace(' ', '_')}_response.txt", 'w') as f:
                f.write(result['response'])

    # Comparação
    if len(results) == 2:
        print("\n" + "="*60)
        print("📊 COMPARAÇÃO FINAL")
        print("="*60)

        original = results[0]
        optimized = results[1]

        print(f"\nPalavras:")
        print(f"  Original: {original['words']}")
        print(f"  Optimized: {optimized['words']}")
        improvement = ((optimized['words'] - original['words']) / original['words']) * 100
        print(f"  Melhoria: {improvement:+.1f}%")

        print(f"\nChain-of-Thought:")
        print(f"  Original: {original['metrics']['cot_indicators']}")
        print(f"  Optimized: {optimized['metrics']['cot_indicators']}")

        print(f"\nEvidências (quotes + exhibits):")
        orig_evidence = original['metrics']['quotes'] + original['metrics']['exhibits']
        opt_evidence = optimized['metrics']['quotes'] + optimized['metrics']['exhibits']
        print(f"  Original: {orig_evidence}")
        print(f"  Optimized: {opt_evidence}")

        print("\n" + "="*60)
        print("🎯 CONCLUSÃO")
        print("="*60)

        if optimized['words'] >= 1500 and optimized['words'] > original['words']:
            print("\n✅ SUCESSO! Versão otimizada:")
            print(f"- Gerou {optimized['words']} palavras (alvo: 1500+)")
            print(f"- Manteve precisão com {opt_evidence} evidências")
            print(f"- Incluiu {optimized['metrics']['cot_indicators']} indicadores de raciocínio")
        else:
            print("\n⚠️ Resultados mistos:")
            print(f"- Palavras: {optimized['words']} (alvo era 1500+)")
            print("- Pode precisar ajustes adicionais")

        # Relatório final
        report = {
            "test": "Forensic Optimization",
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "results": {
                "original": {
                    "words": original['words'],
                    "time": original['time'],
                    "cot": original['metrics']['cot_indicators'],
                    "evidence": orig_evidence
                },
                "optimized": {
                    "words": optimized['words'],
                    "time": optimized['time'],
                    "cot": optimized['metrics']['cot_indicators'],
                    "evidence": opt_evidence
                },
                "improvement": {
                    "words_percent": improvement,
                    "target_reached": optimized['words'] >= 1500
                }
            }
        }

        with open("forensic_optimization_report.json", 'w') as f:
            json.dump(report, f, indent=2)

        print(f"\n📁 Relatório salvo: forensic_optimization_report.json")

if __name__ == "__main__":
    main()