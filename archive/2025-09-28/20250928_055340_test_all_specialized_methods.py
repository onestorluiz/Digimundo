#!/usr/bin/env python3
"""
🚀 MEGA TESTE: Todos os Métodos Especializados
Compara a eficácia de cada metáfora especializada
"""

import json
import time
import subprocess
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import Dict, List
import re

@dataclass
class MethodMetrics:
    """Métricas para cada método especializado"""
    method_name: str
    specialist_type: str
    word_count: int
    execution_time: float
    metaphor_accuracy: float  # Quão bem usa a metáfora
    insight_density: float    # Insights por palavra
    actionability: float      # Quão práticas são as sugestões
    uniqueness: float        # Quão único é comparado aos outros
    overall_score: float

def analyze_metaphor_usage(response: str, metaphor_type: str) -> float:
    """Analisa quão bem o modelo usa a metáfora específica"""

    metaphor_terms = {
        'jazz': ['rhythm', 'tempo', 'groove', 'improvisation', 'harmony', 'melody',
                 'syncopation', 'riff', 'solo', 'ensemble', 'swing', 'chord'],
        'cardiac': ['heartbeat', 'pulse', 'bpm', 'systolic', 'diastolic', 'arrhythmia',
                   'cardiac', 'blood pressure', 'ekg', 'ventricle', 'circulation'],
        'physics': ['force', 'momentum', 'energy', 'velocity', 'acceleration', 'mass',
                   'newton', 'kinetic', 'potential', 'trajectory', 'collision'],
        'archaeological': ['excavation', 'layer', 'artifact', 'stratum', 'dig',
                          'fossil', 'dating', 'site', 'preservation', 'bedrock'],
        'chemical': ['reaction', 'element', 'compound', 'catalyst', 'bond', 'electron',
                    'molecule', 'oxidation', 'equilibrium', 'enthalpy', 'entropy'],
        'forensic': ['autopsy', 'examination', 'evidence', 'forensic', 'diagnosis',
                    'microscopic', 'cause', 'investigation', 'pathology'],
        'executive': ['roi', 'kpi', 'market', 'revenue', 'investment', 'risk',
                     'swot', 'projection', 'budget', 'profit', 'strategy']
    }

    terms = metaphor_terms.get(metaphor_type, [])
    if not terms:
        return 0.5  # Default para métodos sem termos específicos

    count = sum(1 for term in terms if term.lower() in response.lower())
    return min(count / len(terms), 1.0)

def test_method(specialist_file: str, method_name: str, specialist_type: str,
                test_script: str, metaphor_type: str) -> MethodMetrics:
    """Testa um método específico"""

    print(f"\n🧪 Testing {method_name}...")

    # Ler o arquivo do especialista
    file_path = f"/Users/clubproducoes/Digimundo/scripturemon-ultimate/super_specialists/{specialist_file}"

    if not Path(file_path).exists():
        print(f"   ❌ Arquivo não encontrado: {file_path}")
        return MethodMetrics(method_name, specialist_type, 0, 0, 0, 0, 0, 0, 0)

    with open(file_path, 'r') as f:
        content = f.read()

    # Extrair system prompt
    system_match = re.search(r'## PROMPT SYSTEM.*?\n\n(.*?)(?=\n##)', content, re.S)
    if not system_match:
        print(f"   ❌ Não consegui extrair prompt")
        return MethodMetrics(method_name, specialist_type, 0, 0, 0, 0, 0, 0, 0)

    system_prompt = system_match.group(1).strip()

    # Configurar mensagens baseadas no tipo
    if specialist_type == 'dialogue':
        user_prompt = f"Analyze this script's dialogue:\n\n{test_script}"
    elif specialist_type == 'pacing':
        user_prompt = f"Analyze this script's pacing:\n\n{test_script}"
    elif specialist_type == 'action':
        user_prompt = f"Analyze this action sequence:\n\n{test_script}"
    elif specialist_type == 'theme':
        user_prompt = f"Analyze this script's themes:\n\n{test_script}"
    elif specialist_type == 'character':
        user_prompt = f"Analyze this character arc:\n\n{test_script}"
    else:
        user_prompt = f"Analyze this script:\n\n{test_script}"

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

    data = {
        "model": "mixtral:8x7b-instruct-v0.1-q5_K_M",
        "messages": messages,
        "stream": False,
        "options": {
            "temperature": 0.7,
            "top_p": 0.9,
            "num_predict": 1500
        }
    }

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
                word_count = len(response_text.split())

                # Calcular métricas
                metaphor_accuracy = analyze_metaphor_usage(response_text, metaphor_type)

                # Insight density (procurar por marcadores de insight)
                insight_markers = ['reveals', 'shows', 'demonstrates', 'indicates',
                                 'suggests', 'implies', 'notice', 'observe']
                insight_count = sum(1 for marker in insight_markers
                                  if marker in response_text.lower())
                insight_density = insight_count / max(word_count, 1) * 100

                # Actionability (procurar por sugestões práticas)
                action_markers = ['should', 'could', 'needs', 'must', 'rewrite',
                                'change', 'improve', 'fix', 'adjust']
                action_count = sum(1 for marker in action_markers
                                 if marker in response_text.lower())
                actionability = min(action_count / 10, 1.0)

                # Uniqueness (baseada no uso da metáfora)
                uniqueness = metaphor_accuracy

                # Overall score
                overall_score = (
                    metaphor_accuracy * 0.3 +
                    insight_density * 0.2 +
                    actionability * 0.3 +
                    uniqueness * 0.2
                )

                print(f"   ✅ Completed in {elapsed:.1f}s")
                print(f"   📝 Words: {word_count}")
                print(f"   🎯 Metaphor accuracy: {metaphor_accuracy:.1%}")
                print(f"   💡 Insight density: {insight_density:.2f}")
                print(f"   ⚡ Actionability: {actionability:.1%}")
                print(f"   ⭐ Overall: {overall_score:.2f}")

                # Salvar resposta
                output_dir = Path("specialized_methods_results")
                output_dir.mkdir(exist_ok=True)
                with open(output_dir / f"{method_name}.txt", 'w') as f:
                    f.write(response_text)

                return MethodMetrics(
                    method_name=method_name,
                    specialist_type=specialist_type,
                    word_count=word_count,
                    execution_time=elapsed,
                    metaphor_accuracy=metaphor_accuracy,
                    insight_density=insight_density,
                    actionability=actionability,
                    uniqueness=uniqueness,
                    overall_score=overall_score
                )

    except Exception as e:
        print(f"   ❌ Error: {e}")

    return MethodMetrics(method_name, specialist_type, 0, 0, 0, 0, 0, 0, 0)

def main():
    """Executa teste completo de todos os métodos"""

    print("="*60)
    print("🚀 MEGA TESTE: MÉTODOS ESPECIALIZADOS")
    print("="*60)

    # Script de teste genérico
    test_script = """FADE IN:

INT. ROOM - DAY

ALEX (30s) faces JORDAN (40s) across a table. Between them, a gun.

ALEX
One of us walks out. One doesn't.

JORDAN
(smiling)
You always were dramatic.

Alex reaches for the gun. Jordan doesn't move.

ALEX
Why aren't you scared?

JORDAN
Because I know something you don't.

ALEX
What's that?

JORDAN
The gun isn't loaded.

Alex pulls the trigger. CLICK. Nothing.

JORDAN (CONT'D)
But this one is.

Jordan reveals another gun. BANG.

FADE OUT."""

    # Definir todos os métodos para testar
    methods = [
        # (arquivo, nome, tipo_especialista, tipo_metáfora)
        ("02_dialogue_forensic.md", "Dialogue-Forensic", "dialogue", "forensic"),
        ("02_dialogue_v3_opt4.md", "Dialogue-V3OPT4", "dialogue", "v3opt4"),
        ("02_dialogue_jazz.md", "Dialogue-Jazz", "dialogue", "jazz"),
        ("03_pacing_cardiac.md", "Pacing-Cardiac", "pacing", "cardiac"),
        ("05_action_physics.md", "Action-Physics", "action", "physics"),
        ("04_theme_archaeological.md", "Theme-Archaeological", "theme", "archaeological"),
        ("01_character_chemical.md", "Character-Chemical", "character", "chemical"),
        ("01_character_arc_forensic.md", "Character-Forensic", "character", "forensic"),
        ("06_executive_brief.md", "Executive-Brief", "general", "executive"),
    ]

    results = []

    for file, name, spec_type, metaphor in methods:
        metrics = test_method(file, name, spec_type, test_script, metaphor)
        if metrics.word_count > 0:  # Só adicionar se teve resultado
            results.append(metrics)

    # Análise comparativa
    if results:
        print("\n" + "="*60)
        print("📊 ANÁLISE COMPARATIVA")
        print("="*60)

        # Ordenar por overall score
        results.sort(key=lambda x: x.overall_score, reverse=True)

        print("\n🏆 RANKING GERAL:")
        for i, r in enumerate(results, 1):
            print(f"{i}. {r.method_name}")
            print(f"   Overall: {r.overall_score:.2f}")
            print(f"   Metaphor: {r.metaphor_accuracy:.1%}")
            print(f"   Words: {r.word_count}")
            print(f"   Time: {r.execution_time:.1f}s")
            print()

        # Análise por tipo de especialista
        print("\n📈 MELHOR POR CATEGORIA:")

        specialist_types = set(r.specialist_type for r in results)
        for spec_type in specialist_types:
            type_results = [r for r in results if r.specialist_type == spec_type]
            if type_results:
                best = max(type_results, key=lambda x: x.overall_score)
                print(f"\n{spec_type.upper()}:")
                print(f"   🥇 {best.method_name} (Score: {best.overall_score:.2f})")

        # Insights
        print("\n💡 DESCOBERTAS:")

        # Metáfora mais eficaz
        best_metaphor = max(results, key=lambda x: x.metaphor_accuracy)
        print(f"• Melhor uso de metáfora: {best_metaphor.method_name} ({best_metaphor.metaphor_accuracy:.1%})")

        # Mais acionável
        most_actionable = max(results, key=lambda x: x.actionability)
        print(f"• Mais acionável: {most_actionable.method_name} ({most_actionable.actionability:.1%})")

        # Mais rápido
        fastest = min(results, key=lambda x: x.execution_time)
        print(f"• Mais rápido: {fastest.method_name} ({fastest.execution_time:.1f}s)")

        # Mais denso em insights
        densest = max(results, key=lambda x: x.insight_density)
        print(f"• Maior densidade de insights: {densest.method_name} ({densest.insight_density:.2f})")

        # Salvar relatório completo
        report = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "test_type": "specialized_methods_comparison",
            "results": [asdict(r) for r in results],
            "rankings": {
                "overall": [r.method_name for r in results],
                "by_category": {
                    spec_type: max(
                        [r for r in results if r.specialist_type == spec_type],
                        key=lambda x: x.overall_score
                    ).method_name
                    for spec_type in specialist_types
                }
            }
        }

        output_dir = Path("specialized_methods_results")
        with open(output_dir / "mega_comparison_report.json", 'w') as f:
            json.dump(report, f, indent=2)

        print(f"\n📁 Resultados salvos em: {output_dir}/")

if __name__ == "__main__":
    main()