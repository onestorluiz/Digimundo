#!/usr/bin/env python3
"""
Teste direto com Ollama Mistral para análise crítica
Mostra o problema real de categorização
"""

import sys
import json
from pathlib import Path
import requests

sys.path.insert(0, 'src')

from scripturemon_champion.analysis.script_doctor import ScriptDoctor

def test_with_ollama(screenplay_path: Path):
    """Teste direto com Ollama sendo crítico"""

    print("=" * 80)
    print(f"🔍 ANÁLISE CRÍTICA: {screenplay_path.name}")
    print("=" * 80)

    # Carregar roteiro
    text = screenplay_path.read_text(encoding='utf-8', errors='ignore')

    # Análise base
    doctor = ScriptDoctor()
    analysis = doctor.analyze_script(text, screenplay_path.stem)
    stc = doctor.analyze_save_the_cat(text)

    # Mostrar métricas reais
    print(f"\n📊 MÉTRICAS OBJETIVAS:")
    print(f"  • Cenas: {analysis.scenes}")
    print(f"  • Beats detectados: {len(stc.beats)}/15")
    print(f"  • Beats faltando: {', '.join(stc.missing_beats[:5]) if stc.missing_beats else 'Nenhum'}")
    print(f"  • Diálogo: {analysis.dialogue_ratio:.1%}")
    print(f"  • Ritmo: {analysis.pacing_score:.2f}")
    print(f"  • Personagens principais: {len(analysis.top_characters)}")

    # Score estrutural honesto
    structural_score = 0

    # Beats (40 pontos)
    beats_score = (len(stc.beats) / 15) * 40
    structural_score += beats_score

    # Diálogo (20 pontos)
    if 0.25 <= analysis.dialogue_ratio <= 0.4:
        dialogue_score = 20
    elif 0.2 <= analysis.dialogue_ratio <= 0.5:
        dialogue_score = 15
    else:
        dialogue_score = 10
    structural_score += dialogue_score

    # Ritmo (20 pontos)
    pacing_score = analysis.pacing_score * 20
    structural_score += pacing_score

    # Personagens (20 pontos)
    if 3 <= len(analysis.top_characters) <= 10:
        char_score = 20
    else:
        char_score = 10
    structural_score += char_score

    print(f"\n⚖️ SCORE ESTRUTURAL HONESTO: {structural_score:.0f}/100")

    # Problemas reais identificados
    problems = []

    if len(stc.beats) < 10:
        problems.append(f"❌ ESTRUTURA INCOMPLETA: Apenas {len(stc.beats)}/15 beats")

    if len(stc.missing_beats) > 5:
        problems.append(f"❌ BEATS CRÍTICOS FALTANDO: {', '.join(stc.missing_beats[:3])}")

    if analysis.dialogue_ratio < 0.2:
        problems.append("❌ DIÁLOGO INSUFICIENTE: Muito descritivo")
    elif analysis.dialogue_ratio > 0.5:
        problems.append("❌ DIÁLOGO EXCESSIVO: Falta ação visual")

    if analysis.pacing_score < 0.5:
        problems.append(f"❌ RITMO PROBLEMÁTICO: Score {analysis.pacing_score:.2f}")

    if problems:
        print(f"\n🚨 PROBLEMAS REAIS DETECTADOS:")
        for p in problems:
            print(f"  {p}")

    # Agora perguntar ao Ollama
    print(f"\n🤖 CONSULTANDO OLLAMA MISTRAL...")

    prompt = f"""Seja um crítico de roteiros BRUTALMENTE HONESTO. Analise estes dados:

ROTEIRO: {screenplay_path.stem}
- Beats encontrados: {len(stc.beats)}/15 (faltam: {', '.join(stc.missing_beats[:3])})
- Diálogo: {analysis.dialogue_ratio:.1%}
- Ritmo: {analysis.pacing_score:.2f}
- Cenas: {analysis.scenes}

INÍCIO DO ROTEIRO:
{text[:1500]}

AVALIE COM RIGOR:
1. Este roteiro tem estrutura profissional? (Sim/Não e porquê)
2. Funcionaria em Hollywood? (Sim/Não e porquê)
3. Principais defeitos? (Liste 3 concretos)
4. Score honesto: 0-100 (seja duro, a média é 50)
5. Categoria: experimental/needs_work/good_with_notes/universal_good

Responda em formato JSON. Seja EXTREMAMENTE CRÍTICO."""

    try:
        response = requests.post(
            "http://127.0.0.1:11434/api/generate",
            json={
                "model": "mixtral-eco-q5:latest",
                "prompt": prompt,
                "stream": False,
                "temperature": 0.3
            },
            timeout=30
        )

        if response.status_code == 200:
            result = response.json()
            ollama_response = result.get("response", "")
            print(f"\n📝 RESPOSTA DO OLLAMA:")
            print(ollama_response[:800])  # Primeiros 800 chars

            # Tentar extrair score
            import re
            score_match = re.search(r'"score"\s*:\s*(\d+)', ollama_response)
            if score_match:
                ollama_score = int(score_match.group(1))
                print(f"\n🎯 SCORE DO OLLAMA: {ollama_score}/100")

                # Categoria baseada em score combinado
                final_score = (structural_score + ollama_score) / 2
                print(f"\n📊 SCORE FINAL: {final_score:.0f}/100")

                if final_score >= 85:
                    category = "universal_good (RARO!)"
                elif final_score >= 65:
                    category = "good_with_notes"
                elif final_score >= 45:
                    category = "needs_work"
                else:
                    category = "experimental"

                print(f"🏷️ CATEGORIA REAL: {category}")

    except Exception as e:
        print(f"❌ Erro com Ollama: {e}")

    # Veredito final
    print(f"\n" + "=" * 80)
    print("⚖️ VEREDITO FINAL:")

    if structural_score < 50:
        print("  ❌ ROTEIRO COM PROBLEMAS ESTRUTURAIS SÉRIOS")
    elif structural_score < 70:
        print("  ⚠️ ROTEIRO PRECISA DE TRABALHO SIGNIFICATIVO")
    elif structural_score < 85:
        print("  ✅ ROTEIRO BOM MAS COM RESSALVAS")
    else:
        print("  🏆 ROTEIRO EXCELENTE (RARO!)")

    print("=" * 80)

if __name__ == "__main__":
    # Testar com Sonhos Sem Lembranças
    sonhos = Path("my_screenplays/sonhos_sem_lembrancas_t3.txt")

    if sonhos.exists():
        test_with_ollama(sonhos)
    else:
        # Tentar outros arquivos
        my_dir = Path("my_screenplays")
        if my_dir.exists():
            files = list(my_dir.glob("*.txt"))
            if files:
                print(f"Testando com: {files[0].name}")
                test_with_ollama(files[0])
            else:
                print("❌ Nenhum arquivo encontrado em my_screenplays/")