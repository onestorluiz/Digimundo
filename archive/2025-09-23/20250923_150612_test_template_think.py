#!/usr/bin/env python3
"""
Teste das diferentes abordagens de TEMPLATE encontradas nos modelfiles
"""

import subprocess
import time
import json

def test_template_approach(model_name, prompt, template_type="standard"):
    """Testa diferentes abordagens de template"""

    print(f"\n{'='*60}")
    print(f"Testando: {model_name} com {template_type}")
    print(f"{'='*60}")

    start_time = time.time()

    try:
        result = subprocess.run(
            ["ollama", "run", model_name, prompt],
            capture_output=True,
            text=True,
            timeout=30
        )

        elapsed = time.time() - start_time

        output = result.stdout

        # Analisar características da resposta
        analysis = {
            "model": model_name,
            "template_type": template_type,
            "time": f"{elapsed:.2f}s",
            "output_length": len(output),
            "has_think_tag": "<think>" in output,
            "has_json": "{" in output and "}" in output,
            "first_100_chars": output[:100] if output else "NO OUTPUT"
        }

        return analysis

    except subprocess.TimeoutExpired:
        return {
            "model": model_name,
            "template_type": template_type,
            "error": "TIMEOUT"
        }
    except Exception as e:
        return {
            "model": model_name,
            "template_type": template_type,
            "error": str(e)
        }

def main():
    # Prompt simples para teste
    test_prompt = """Analise esta linha de diálogo:
"Eu nunca disse que te amava."
Qual o subtexto?"""

    # Modelos para testar
    models_to_test = [
        ("mixtral-cpu-force:latest", "standard"),
        ("deepseek-r1:32b", "think_tag")
    ]

    results = []

    for model, template_type in models_to_test:
        if model == "deepseek-r1:32b":
            # Testar com prompt que ativa o <think>
            think_prompt = f"<think>Preciso analisar o subtexto desta fala.</think>\n{test_prompt}"
            result = test_template_approach(model, think_prompt, template_type)
        else:
            result = test_template_approach(model, test_prompt, template_type)

        results.append(result)

    # Relatório
    print(f"\n{'='*60}")
    print("RELATÓRIO DE COMPARAÇÃO")
    print(f"{'='*60}")

    for r in results:
        print(f"\n{r['model']} ({r.get('template_type', 'N/A')}):")
        print(f"  Tempo: {r.get('time', 'N/A')}")
        print(f"  Tamanho: {r.get('output_length', 0)} chars")
        print(f"  Has <think>: {r.get('has_think_tag', False)}")
        print(f"  Has JSON: {r.get('has_json', False)}")
        if 'error' in r:
            print(f"  ❌ ERRO: {r['error']}")
        else:
            print(f"  Preview: {r.get('first_100_chars', '')}")

    # Insights descobertos
    print(f"\n{'='*60}")
    print("INSIGHTS DESCOBERTOS")
    print(f"{'='*60}")

    insights = []

    # Verificar se <think> tag funciona
    think_works = any(r.get('has_think_tag', False) for r in results)
    if think_works:
        insights.append("✅ <think> tag funciona com deepseek-r1")

    # Verificar tempos
    times = [float(r.get('time', '999').replace('s', '')) for r in results if 'time' in r]
    if times:
        fastest = min(times)
        insights.append(f"✅ Tempo mais rápido: {fastest:.2f}s")

    for insight in insights:
        print(f"  {insight}")

if __name__ == "__main__":
    main()