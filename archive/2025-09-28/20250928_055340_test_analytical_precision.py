#!/usr/bin/env python3
"""
🎯 TESTE DEFINITIVO: PRECISÃO ANALÍTICA
Métrica baseada em aplicação CORRETA de análise, não em metáforas
"""

import json
import time
import subprocess
from pathlib import Path
from dataclasses import dataclass
from typing import Dict, List, Tuple
import re

@dataclass
class PrecisionMetrics:
    """Métricas de PRECISÃO ANALÍTICA REAL"""
    method_name: str

    # Análise Factual
    exact_quotes: int  # Citações exatas do script
    invented_elements: int  # Elementos inventados/forçados
    factual_observations: int  # Observações baseadas em fatos
    speculative_claims: int  # Especulações sem base

    # Aplicação Correta
    theory_correctly_applied: int  # Teoria aplicada corretamente
    theory_misapplied: int  # Teoria mal aplicada
    relevant_analysis: int  # Análise relevante ao conteúdo
    forced_metaphors: int  # Metáforas forçadas

    # Profundidade Real
    actual_insights: int  # Insights verdadeiros sobre o texto
    surface_observations: int  # Observações superficiais
    subtext_identified: int  # Subtexto real identificado
    subtext_invented: int  # Subtexto inventado

    # Scores Calculados
    precision_score: float  # Precisão analítica
    factual_score: float  # Baseado em fatos
    depth_score: float  # Profundidade real
    overall_accuracy: float  # Precisão geral

def analyze_precision(response: str, test_script: str) -> PrecisionMetrics:
    """Analisa PRECISÃO REAL da resposta"""

    # Extrair linhas reais do script para comparação
    script_lines = []
    for line in test_script.split('\n'):
        line = line.strip()
        if line and not line.startswith(('FADE', 'INT.', 'EXT.', '(')) and not line.isupper():
            script_lines.append(line.lower())

    response_lower = response.lower()

    # 1. CITAÇÕES EXATAS vs INVENTADAS
    exact_quotes = 0
    for line in script_lines:
        if len(line) > 10 and line in response_lower:
            exact_quotes += 1

    # Detectar invenções comuns
    invented_patterns = [
        r'\d+ (?:bpm|beats per minute)',  # BPM inventado
        r'(?:dorian|lydian|phrygian|mixolydian) (?:mode|scale)',  # Modos musicais forçados
        r'trading fours',  # Jazz forçado
        r'[A-G](?:#|b)? (?:major|minor)',  # Acordes inventados
        r'\d+ (?:hz|hertz)',  # Frequências inventadas
        r'measure \d+',  # Compassos inventados
        r'bar \d+',  # Barras musicais inventadas
        r'verse-chorus',  # Estrutura musical forçada
        r'quantum (?:state|superposition)',  # Física quântica forçada
        r'coefficient of \w+',  # Coeficientes inventados
    ]

    invented_elements = sum(1 for pattern in invented_patterns
                           if re.search(pattern, response_lower))

    # 2. OBSERVAÇÕES FACTUAIS vs ESPECULATIVAS
    factual_markers = [
        'the script shows',
        'the text states',
        'as written',
        'according to',
        'the dialogue indicates',
        'explicitly',
        'directly'
    ]

    speculative_markers = [
        'might be',
        'could suggest',
        'perhaps',
        'possibly',
        'seems to',
        'appears to',
        'maybe',
        'presumably'
    ]

    factual_observations = sum(1 for marker in factual_markers
                              if marker in response_lower)
    speculative_claims = sum(1 for marker in speculative_markers
                            if marker in response_lower)

    # 3. TEORIA APLICADA CORRETAMENTE
    # Verificar se teorias mencionadas fazem sentido
    theory_mentions = {
        'mckee': response_lower.count('mckee'),
        'field': response_lower.count('field'),
        'truby': response_lower.count('truby'),
        'campbell': response_lower.count('campbell'),
        'vogler': response_lower.count('vogler'),
    }

    # Teoria está sendo aplicada ou apenas mencionada?
    theory_correctly_applied = 0
    theory_misapplied = 0

    for theory, count in theory_mentions.items():
        if count > 0:
            # Verificar se há explicação/aplicação após menção
            if f"{theory}'s" in response_lower or f"according to {theory}" in response_lower:
                theory_correctly_applied += 1
            else:
                theory_misapplied += 1

    # 4. METÁFORAS FORÇADAS
    forced_metaphor_patterns = [
        r'dialogue as (?:music|symphony|jazz|orchestra)',
        r'conversation as (?:dance|battle|war)',
        r'words as (?:weapons|instruments|notes)',
        r'script as (?:body|organism|machine)',
        r'story as (?:journey|voyage|expedition)',
    ]

    forced_metaphors = sum(1 for pattern in forced_metaphor_patterns
                          if re.search(pattern, response_lower))

    # 5. ANÁLISE RELEVANTE
    relevant_keywords = []
    for line in script_lines:
        words = line.split()
        for word in words:
            if len(word) > 4 and word not in ['that', 'this', 'with', 'from']:
                relevant_keywords.append(word)

    relevant_analysis = sum(1 for keyword in set(relevant_keywords)
                           if keyword in response_lower)

    # 6. INSIGHTS REAIS vs SUPERFICIAIS
    insight_patterns = [
        r'reveals that',
        r'demonstrates',
        r'shows how',
        r'indicates',
        r'suggests that',
        r'implies'
    ]

    actual_insights = 0
    for pattern in insight_patterns:
        matches = re.finditer(pattern, response_lower)
        for match in matches:
            # Verificar se o insight se refere ao texto real
            context = response_lower[max(0, match.start()-50):min(len(response_lower), match.end()+50)]
            if any(line_word in context for line in script_lines for line_word in line.split() if len(line_word) > 4):
                actual_insights += 1

    surface_observations = response_lower.count('obvious') + response_lower.count('clearly')

    # 7. SUBTEXTO
    subtext_identified = 0
    subtext_invented = 0

    if 'subtext' in response_lower or 'beneath' in response_lower or 'underlying' in response_lower:
        # Verificar se o subtexto mencionado tem base no texto
        if any(quote in response_lower for quote in script_lines):
            subtext_identified += response_lower.count('subtext')
        else:
            subtext_invented += response_lower.count('subtext')

    # CALCULAR SCORES

    # Factual Score: Quão baseado em fatos é
    factual_score = 0
    if (exact_quotes + factual_observations) > 0:
        factual_score = (exact_quotes + factual_observations - invented_elements - speculative_claims) / \
                       (exact_quotes + factual_observations + invented_elements + speculative_claims + 1)
    factual_score = max(0, min(1, factual_score))

    # Precision Score: Aplicação correta vs incorreta
    precision_score = 0
    total_applications = (theory_correctly_applied + theory_misapplied +
                         relevant_analysis + forced_metaphors)
    if total_applications > 0:
        precision_score = (theory_correctly_applied + relevant_analysis - theory_misapplied - forced_metaphors) / total_applications
    precision_score = max(0, min(1, precision_score))

    # Depth Score: Insights reais vs superficiais
    depth_score = 0
    total_observations = (actual_insights + surface_observations +
                         subtext_identified + subtext_invented)
    if total_observations > 0:
        depth_score = (actual_insights + subtext_identified - surface_observations - subtext_invented) / total_observations
    depth_score = max(0, min(1, depth_score))

    # Overall Accuracy: Média ponderada
    overall_accuracy = (
        factual_score * 0.40 +  # 40% peso para fatos
        precision_score * 0.35 +  # 35% peso para aplicação correta
        depth_score * 0.25  # 25% peso para profundidade real
    )

    return PrecisionMetrics(
        method_name="",
        exact_quotes=exact_quotes,
        invented_elements=invented_elements,
        factual_observations=factual_observations,
        speculative_claims=speculative_claims,
        theory_correctly_applied=theory_correctly_applied,
        theory_misapplied=theory_misapplied,
        relevant_analysis=relevant_analysis,
        forced_metaphors=forced_metaphors,
        actual_insights=actual_insights,
        surface_observations=surface_observations,
        subtext_identified=subtext_identified,
        subtext_invented=subtext_invented,
        precision_score=round(precision_score, 3),
        factual_score=round(factual_score, 3),
        depth_score=round(depth_score, 3),
        overall_accuracy=round(overall_accuracy, 3)
    )

def test_method_precision(file_path: str, method_name: str, test_script: str) -> Tuple[PrecisionMetrics, str]:
    """Testa precisão de um método específico"""

    print(f"\n🔬 Testing {method_name}...")

    if not Path(file_path).exists():
        print(f"   ❌ File not found")
        return PrecisionMetrics(method_name, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0), ""

    with open(file_path, 'r') as f:
        content = f.read()

    # Extrair system prompt
    system_match = re.search(r'## PROMPT SYSTEM.*?\n\n(.*?)(?=\n##)', content, re.S)
    if not system_match:
        print(f"   ❌ Could not extract prompt")
        return PrecisionMetrics(method_name, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0), ""

    system_prompt = system_match.group(1).strip()

    # Preparar mensagens
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Analyze this dialogue:\n\n{test_script}"}
    ]

    data = {
        "model": "mixtral:8x7b-instruct-v0.1-q5_K_M",
        "messages": messages,
        "stream": False,
        "options": {
            "temperature": 0.7,
            "top_p": 0.9,
            "num_predict": 2000
        }
    }

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
                # Analisar precisão
                metrics = analyze_precision(response_text, test_script)
                metrics.method_name = method_name

                print(f"   ✅ ACCURACY: {metrics.overall_accuracy:.1%}")
                print(f"   📊 Factual: {metrics.factual_score:.1%}")
                print(f"   🎯 Precision: {metrics.precision_score:.1%}")
                print(f"   🌊 Depth: {metrics.depth_score:.1%}")
                print(f"   📝 Quotes: {metrics.exact_quotes} exact, {metrics.invented_elements} invented")

                return metrics, response_text

    except Exception as e:
        print(f"   ❌ Error: {e}")

    return PrecisionMetrics(method_name, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0), ""

def main():
    """Teste definitivo com métrica de precisão"""

    print("="*60)
    print("🎯 TESTE DEFINITIVO: PRECISÃO ANALÍTICA")
    print("Métrica: Aplicação correta, não metáforas bonitas")
    print("="*60)

    # Script de teste
    test_script = """FADE IN:

INT. OFFICE - NIGHT

DAVID (35) stares at his computer screen. His wife EMMA (33) enters.

EMMA
Still working?

DAVID
(not looking up)
Almost done.

EMMA
You said that three hours ago.

DAVID
This is important.

EMMA
(sitting beside him)
More important than us?

David finally looks at her. Sees the pain in her eyes.

DAVID
Emma, I...
(pause)
No. Nothing is.

He closes the laptop.

FADE OUT."""

    # Métodos para testar
    methods_to_test = [
        ("02_dialogue_forensic.md", "Dialogue-Forensic"),
        ("02_dialogue_jazz.md", "Dialogue-Jazz"),
        ("02_dialogue_v3_opt4.md", "Dialogue-V3OPT4"),
        ("01_character_arc_forensic.md", "Character-Forensic"),
        ("01_character_chemical.md", "Character-Chemical"),
        ("03_pacing_cardiac.md", "Pacing-Cardiac"),
        ("04_theme_archaeological.md", "Theme-Archaeological"),
        ("05_action_physics.md", "Action-Physics"),
    ]

    results = []
    output_dir = Path("precision_test_results")
    output_dir.mkdir(exist_ok=True)

    for filename, method_name in methods_to_test:
        file_path = f"/Users/clubproducoes/Digimundo/scripturemon-ultimate/super_specialists/{filename}"
        metrics, response = test_method_precision(file_path, method_name, test_script)

        if metrics.overall_accuracy > 0:
            results.append(metrics)

            # Salvar resposta
            with open(output_dir / f"{method_name}_response.txt", 'w') as f:
                f.write(response)

    # Análise final
    if results:
        print("\n" + "="*60)
        print("🏆 RANKING POR PRECISÃO ANALÍTICA")
        print("="*60)

        results.sort(key=lambda x: x.overall_accuracy, reverse=True)

        for i, m in enumerate(results, 1):
            print(f"\n{i}. {m.method_name}")
            print(f"   🎯 ACCURACY: {m.overall_accuracy:.1%}")
            print(f"   📊 Factual: {m.factual_score:.1%} (Quotes: {m.exact_quotes}, Invented: {m.invented_elements})")
            print(f"   🎯 Precision: {m.precision_score:.1%} (Theory OK: {m.theory_correctly_applied}, Forced: {m.forced_metaphors})")
            print(f"   🌊 Depth: {m.depth_score:.1%} (Real insights: {m.actual_insights}, Invented subtext: {m.subtext_invented})")

        # Vencedor absoluto
        winner = results[0]
        print("\n" + "="*60)
        print("🥇 VENCEDOR POR PRECISÃO ANALÍTICA")
        print("="*60)
        print(f"\n{winner.method_name}: {winner.overall_accuracy:.1%} de precisão")
        print(f"Este método tem a análise mais PRECISA e FACTUAL")

        # Salvar relatório
        report = {
            "test_type": "Analytical Precision",
            "metric": "Factual accuracy, correct application, real insights",
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "results": [
                {
                    "method": m.method_name,
                    "overall_accuracy": m.overall_accuracy,
                    "factual_score": m.factual_score,
                    "precision_score": m.precision_score,
                    "depth_score": m.depth_score,
                    "exact_quotes": m.exact_quotes,
                    "invented_elements": m.invented_elements,
                    "forced_metaphors": m.forced_metaphors,
                    "actual_insights": m.actual_insights
                }
                for m in results
            ],
            "winner": winner.method_name
        }

        with open(output_dir / "precision_analysis_report.json", 'w') as f:
            json.dump(report, f, indent=2)

        print(f"\n📁 Results saved to: {output_dir}/")

if __name__ == "__main__":
    main()