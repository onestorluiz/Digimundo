#!/usr/bin/env python3
"""
🎯 TESTE COMPARATIVO: DIALOGUE FORENSIC vs V3_OPT4
Compara as duas abordagens para análise de diálogos
"""

import json
import time
import subprocess
from pathlib import Path
from dataclasses import dataclass
from typing import Dict, Tuple
import re

@dataclass
class DialogueMetrics:
    """Métricas específicas para análise de diálogos"""
    word_count: int
    quotes_count: int  # citações diretas do script
    theories_applied: int  # teorias mencionadas
    rewrites_provided: int  # sugestões de reescrita
    subtext_analyses: int  # análises de subtexto
    character_insights: int  # insights sobre personagens
    quality_score: float
    execution_time: float

def analyze_dialogue_response(response: str) -> DialogueMetrics:
    """Analisa resposta focada em diálogos"""

    word_count = len(response.split())

    # Contar citações (entre aspas)
    quotes_count = len(re.findall(r'"[^"]+"', response))

    # Teorias aplicadas
    theories = ['McKee', 'Mamet', 'Sorkin', 'Pinter', 'Tarantino',
                'Field', 'Truby', 'Coen', 'Snyder', 'Campbell']
    theories_applied = sum(1 for t in theories if t in response)

    # Rewrites (procura por padrões de original/rewrite)
    rewrite_patterns = [
        r'Original:.*Rewrite:',
        r'Before:.*After:',
        r'Current:.*Suggested:',
        r'Problem:.*Solution:'
    ]
    rewrites_provided = sum(1 for p in rewrite_patterns
                           if re.search(p, response, re.I | re.S))

    # Análises de subtexto
    subtext_keywords = ['subtext', 'beneath', 'underlying', 'hidden meaning',
                        'really means', 'actually saying', 'implies']
    subtext_analyses = sum(1 for k in subtext_keywords
                          if k.lower() in response.lower())

    # Character insights
    character_patterns = ['character voice', 'speech pattern', 'vocabulary',
                         'linguistic', 'verbal', 'dialogue DNA']
    character_insights = sum(1 for p in character_patterns
                            if p.lower() in response.lower())

    # Calcular quality score para diálogos
    quality_score = (
        min(quotes_count / 10, 1.0) * 0.25 +  # citações
        min(theories_applied / 5, 1.0) * 0.20 +  # teorias
        min(rewrites_provided / 3, 1.0) * 0.20 +  # rewrites
        min(subtext_analyses / 5, 1.0) * 0.15 +  # subtexto
        min(character_insights / 5, 1.0) * 0.15 +  # personagens
        min(word_count / 700, 1.0) * 0.05  # completude
    )

    return DialogueMetrics(
        word_count=word_count,
        quotes_count=quotes_count,
        theories_applied=theories_applied,
        rewrites_provided=rewrites_provided,
        subtext_analyses=subtext_analyses,
        character_insights=character_insights,
        quality_score=round(quality_score, 2),
        execution_time=0  # será preenchido depois
    )

def test_dialogue_method(method_file: str, method_name: str) -> Tuple[str, DialogueMetrics]:
    """Testa um método de análise de diálogo"""

    # Script de exemplo para análise
    test_script = """FADE IN:

INT. COFFEE SHOP - DAY

SARAH (30s, tired) sits across from MARK (40s, nervous).

MARK
We need to talk about what happened.

SARAH
(not looking up)
Nothing happened.

MARK
Sarah, please. You know that's not true.

SARAH
(finally meeting his eyes)
Fine. You want the truth? I saw you with her.

MARK
It's not what you think—

SARAH
(interrupting)
It never is, is it?

She stands to leave.

MARK
(desperate)
Wait! Let me explain. She's my sister.

Sarah freezes. Turns slowly.

SARAH
Your sister? You don't have a sister.

MARK
I do now. Well, half-sister. My father...
(trails off)
It's complicated.

SARAH
(sitting back down)
You have five minutes.

FADE OUT."""

    # Ler o prompt do arquivo
    with open(f"/Users/clubproducoes/Digimundo/scripturemon-ultimate/super_specialists/{method_file}", 'r') as f:
        content = f.read()

    # Extrair o prompt system (entre ## PROMPT SYSTEM e próxima ##)
    system_match = re.search(r'## PROMPT SYSTEM.*?\n\n(.*?)(?=\n##)', content, re.S)
    if not system_match:
        print(f"❌ Não consegui extrair system prompt de {method_file}")
        return "", DialogueMetrics(0,0,0,0,0,0,0,0)

    system_prompt = system_match.group(1).strip()

    # Configurar chamada para Ollama
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Analyze this script's dialogue:\n\n{test_script}"}
    ]

    data = {
        "model": "mixtral:8x7b-instruct-v0.1-q5_K_M",
        "messages": messages,
        "stream": False,
        "options": {
            "temperature": 0.7,
            "top_p": 0.9,
            "top_k": 40,
            "num_predict": 2048
        }
    }

    print(f"\n🧪 Testing {method_name}...")
    start_time = time.time()

    try:
        # Fazer chamada
        cmd = ["curl", "-s", "-X", "POST", "http://localhost:11434/api/chat",
               "-H", "Content-Type: application/json",
               "-d", json.dumps(data)]

        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)

        if result.returncode == 0:
            response_data = json.loads(result.stdout)
            response_text = response_data.get("message", {}).get("content", "")

            if response_text:
                elapsed = time.time() - start_time
                metrics = analyze_dialogue_response(response_text)
                metrics.execution_time = elapsed

                print(f"   ✅ Completed in {elapsed:.1f}s")
                print(f"   📝 Words: {metrics.word_count}")
                print(f"   💬 Quotes: {metrics.quotes_count}")
                print(f"   📚 Theories: {metrics.theories_applied}")
                print(f"   ✏️ Rewrites: {metrics.rewrites_provided}")
                print(f"   🎭 Subtext: {metrics.subtext_analyses}")
                print(f"   👤 Characters: {metrics.character_insights}")
                print(f"   ⭐ Quality: {metrics.quality_score}")

                return response_text, metrics

    except Exception as e:
        print(f"   ❌ Error: {e}")

    return "", DialogueMetrics(0,0,0,0,0,0,0,0)

def main():
    """Executa comparação entre métodos"""

    print("="*60)
    print("🎯 COMPARAÇÃO: DIALOGUE FORENSIC vs V3_OPT4")
    print("="*60)

    # Testar ambos os métodos
    methods = [
        ("02_dialogue_forensic.md", "FORENSIC DOCTOR"),
        ("02_dialogue_v3_opt4.md", "V3_OPT4 FUSION")
    ]

    results = {}
    responses_dir = Path("dialogue_comparison_results")
    responses_dir.mkdir(exist_ok=True)

    for filename, name in methods:
        response, metrics = test_dialogue_method(filename, name)
        results[name] = metrics

        # Salvar resposta
        if response:
            with open(responses_dir / f"{name.replace(' ', '_')}.txt", 'w') as f:
                f.write(response)

    # Análise comparativa
    print("\n" + "="*60)
    print("📊 ANÁLISE COMPARATIVA")
    print("="*60)

    if all(results.values()):
        forensic = results["FORENSIC DOCTOR"]
        v3_opt4 = results["V3_OPT4 FUSION"]

        print("\n📈 VOLUME:")
        print(f"   Forensic: {forensic.word_count} palavras")
        print(f"   V3_OPT4: {v3_opt4.word_count} palavras")
        print(f"   Diferença: {abs(forensic.word_count - v3_opt4.word_count)} palavras")

        print("\n⭐ QUALIDADE:")
        print(f"   Forensic: {forensic.quality_score}")
        print(f"   V3_OPT4: {v3_opt4.quality_score}")
        winner_q = "V3_OPT4" if v3_opt4.quality_score > forensic.quality_score else "Forensic"
        print(f"   Vencedor: {winner_q}")

        print("\n💬 ANÁLISE DE DIÁLOGO:")
        print(f"   Citações - Forensic: {forensic.quotes_count} | V3_OPT4: {v3_opt4.quotes_count}")
        print(f"   Teorias - Forensic: {forensic.theories_applied} | V3_OPT4: {v3_opt4.theories_applied}")
        print(f"   Rewrites - Forensic: {forensic.rewrites_provided} | V3_OPT4: {v3_opt4.rewrites_provided}")
        print(f"   Subtexto - Forensic: {forensic.subtext_analyses} | V3_OPT4: {v3_opt4.subtext_analyses}")

        print("\n⚡ PERFORMANCE:")
        print(f"   Forensic: {forensic.execution_time:.1f}s")
        print(f"   V3_OPT4: {v3_opt4.execution_time:.1f}s")
        speedup = forensic.execution_time / v3_opt4.execution_time if v3_opt4.execution_time > 0 else 1
        print(f"   V3_OPT4 é {speedup:.1f}x mais rápido")

        print("\n🏆 RECOMENDAÇÃO:")
        if v3_opt4.quality_score > forensic.quality_score and v3_opt4.execution_time < forensic.execution_time:
            print("   ✅ V3_OPT4 é superior: melhor qualidade E mais rápido")
        elif forensic.word_count > 900 and forensic.quotes_count > v3_opt4.quotes_count:
            print("   ✅ Forensic para análises exaustivas com muitas citações")
        else:
            print("   ✅ V3_OPT4 para balanço ideal entre profundidade e eficiência")

        # Salvar relatório
        report = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "test_type": "dialogue_analysis_comparison",
            "results": {
                "forensic": {
                    "word_count": forensic.word_count,
                    "quality_score": forensic.quality_score,
                    "quotes": forensic.quotes_count,
                    "theories": forensic.theories_applied,
                    "rewrites": forensic.rewrites_provided,
                    "execution_time": forensic.execution_time
                },
                "v3_opt4": {
                    "word_count": v3_opt4.word_count,
                    "quality_score": v3_opt4.quality_score,
                    "quotes": v3_opt4.quotes_count,
                    "theories": v3_opt4.theories_applied,
                    "rewrites": v3_opt4.rewrites_provided,
                    "execution_time": v3_opt4.execution_time
                }
            },
            "recommendation": "V3_OPT4" if v3_opt4.quality_score > forensic.quality_score else "Context-dependent"
        }

        with open(responses_dir / "comparison_report.json", 'w') as f:
            json.dump(report, f, indent=2)

        print(f"\n📁 Resultados salvos em: {responses_dir}/")

if __name__ == "__main__":
    main()