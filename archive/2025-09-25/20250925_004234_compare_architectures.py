#!/usr/bin/env python3
"""
COMPARAÇÃO: ARQUITETURA ANTIGA (MIXTRAL) vs NOVA (LLAMA-70B)
Testa a mesma análise com ambas as arquiteturas e compara qualidade
"""

import json
import time
from datetime import datetime
import subprocess

# Screenplay de teste para ambas as arquiteturas
TEST_SCREENPLAY = """FADE IN:

INT. TECH STARTUP OFFICE - NIGHT

MAYA (28, ambitious, exhausted) stares at her laptop screen. Lines of code
reflect in her glasses. Empty energy drink cans litter her desk.

MAYA
(to herself)
Just one more bug fix...

Her phone BUZZES. Text from "Mom": "Happy birthday sweetie! 28 today!"

Maya freezes. She'd forgotten her own birthday.

MAYA (CONT'D)
(bitter laugh)
Happy birthday to me.

The office is empty except for one other desk light. ALEX (30s, her co-founder)
approaches with a small cupcake and a lit candle.

ALEX
Make a wish.

MAYA
(softly)
I wish I knew if any of this
was worth it.

ALEX
The IPO is next month. Everything
we've sacrificed...

MAYA
(interrupting)
What if we're just building a
better way for people to waste
their lives?

She blows out the candle. The room goes dark except for the glow of screens.

FADE OUT."""

print("="*80)
print("🔬 COMPARAÇÃO DE ARQUITETURAS: MIXTRAL vs LLAMA-70B")
print("="*80)
print()

# =============================================================================
# TESTE 1: ARQUITETURA ANTIGA (MIXTRAL SOZINHO)
# =============================================================================

print("📊 TESTE 1: ARQUITETURA ANTIGA (Mixtral responde no final)")
print("-"*60)

# Criar prompt direto para Mixtral simular análise completa
mixtral_prompt = f"""You are a professional screenplay analyst. Analyze this screenplay excerpt and provide a comprehensive analysis covering structure, characters, themes, conflicts, and overall quality.

SCREENPLAY:
{TEST_SCREENPLAY}

Provide a detailed, professional analysis with specific observations and actionable feedback."""

print("⏱️  Iniciando análise com Mixtral...")
start_time = time.time()

try:
    # Chamar Mixtral diretamente
    result = subprocess.run(
        ['ollama', 'run', 'mixtral:8x7b-instruct-v0.1-q5_K_M', mixtral_prompt],
        capture_output=True,
        text=True,
        timeout=120
    )

    mixtral_time = time.time() - start_time
    mixtral_response = result.stdout.strip()

    print(f"✅ Análise concluída em {mixtral_time:.1f}s")
    print(f"📝 Tamanho da resposta: {len(mixtral_response)} caracteres")

    # Salvar resposta Mixtral
    with open("mixtral_analysis.txt", "w") as f:
        f.write(f"ANÁLISE MIXTRAL (Arquitetura Antiga)\n")
        f.write(f"Tempo: {mixtral_time:.1f}s\n")
        f.write(f"Tamanho: {len(mixtral_response)} chars\n")
        f.write("="*60 + "\n\n")
        f.write(mixtral_response)

    # Mostrar preview
    print("\n📄 RESPOSTA MIXTRAL (primeiros 1000 chars):")
    print("-"*60)
    print(mixtral_response[:1000])
    if len(mixtral_response) > 1000:
        print("\n[...TRUNCADO...]")

except subprocess.TimeoutExpired:
    print("❌ Timeout na análise Mixtral")
    mixtral_response = "ERRO: Timeout"
    mixtral_time = 120
except Exception as e:
    print(f"❌ Erro na análise Mixtral: {e}")
    mixtral_response = f"ERRO: {e}"
    mixtral_time = 0

print()
print("="*80)

# =============================================================================
# TESTE 2: ARQUITETURA NOVA (3 CAMADAS COM LLAMA-70B)
# =============================================================================

print("📊 TESTE 2: ARQUITETURA NOVA (3 Camadas com Llama-70B)")
print("-"*60)

print("⏱️  Iniciando análise com arquitetura 3 camadas...")

# Importar orchestrator ultimate
from orchestrator_ultimate import ScripturemonOrchestratorUltimate

try:
    # Criar orchestrator
    orchestrator = ScripturemonOrchestratorUltimate(
        orchestrator_model="scripturemon-v9-CLEAN",
        synthesizer_model="scripturemon-synthesizer",
        parallel_execution=False
    )

    start_time = time.time()

    # Executar análise
    result = orchestrator.analyze_screenplay_ultimate(
        TEST_SCREENPLAY,
        analysis_mode="quick",
        synthesis_focus="Provide comprehensive analysis of character development, thematic depth, and storytelling effectiveness"
    )

    llama_time = time.time() - start_time
    llama_response = result["analysis"]["synthesis"]

    print(f"✅ Análise concluída em {llama_time:.1f}s")
    print(f"📝 Tamanho da resposta: {len(llama_response)} caracteres")

    # Breakdown de tempo
    timing = result["metadata"]["timing"]
    print(f"\n⏱️  Breakdown de tempo:")
    print(f"   - Orquestração: {timing['orchestration']}")
    print(f"   - Busca RAG: {timing['rag_search']}")
    print(f"   - Síntese Llama-70B: {timing['synthesis']}")

    # Salvar resposta Llama
    with open("llama70b_analysis.txt", "w") as f:
        f.write(f"ANÁLISE LLAMA-70B (Arquitetura Nova - 3 Camadas)\n")
        f.write(f"Tempo total: {llama_time:.1f}s\n")
        f.write(f"Tamanho: {len(llama_response)} chars\n")
        f.write(f"Breakdown: {json.dumps(timing)}\n")
        f.write("="*60 + "\n\n")
        f.write(llama_response)

    # Mostrar preview
    print("\n📄 RESPOSTA LLAMA-70B (primeiros 1000 chars):")
    print("-"*60)
    print(llama_response[:1000])
    if len(llama_response) > 1000:
        print("\n[...TRUNCADO...]")

except Exception as e:
    print(f"❌ Erro na análise Llama-70B: {e}")
    llama_response = f"ERRO: {e}"
    llama_time = 0
    import traceback
    traceback.print_exc()

print()
print("="*80)

# =============================================================================
# COMPARAÇÃO FINAL
# =============================================================================

print("📊 COMPARAÇÃO FINAL")
print("="*80)

print("\n🏆 MÉTRICAS QUANTITATIVAS:")
print("-"*40)
print(f"{'Métrica':<25} {'Mixtral':<20} {'Llama-70B':<20}")
print("-"*40)
print(f"{'Tempo de resposta':<25} {mixtral_time:.1f}s{'':<15} {llama_time:.1f}s")
print(f"{'Tamanho da resposta':<25} {len(mixtral_response)} chars{'':<7} {len(llama_response)} chars")
print(f"{'Chars por segundo':<25} {len(mixtral_response)/max(mixtral_time,1):.0f}{'':<16} {len(llama_response)/max(llama_time,1):.0f}")

print("\n📈 ANÁLISE QUALITATIVA:")
print("-"*40)

# Analisar características das respostas
qualities = {
    "Profundidade": {
        "mixtral": "themes" in mixtral_response.lower() and "character" in mixtral_response.lower(),
        "llama": "themes" in llama_response.lower() and "character" in llama_response.lower()
    },
    "Teoria cinematográfica": {
        "mixtral": any(name in mixtral_response for name in ["McKee", "Field", "Seger", "Egri"]),
        "llama": any(name in llama_response for name in ["McKee", "Field", "Seger", "Egri"])
    },
    "Feedback acionável": {
        "mixtral": "recommend" in mixtral_response.lower() or "should" in mixtral_response.lower(),
        "llama": "recommend" in llama_response.lower() or "should" in llama_response.lower()
    },
    "Análise estrutural": {
        "mixtral": "structure" in mixtral_response.lower() or "act" in mixtral_response.lower(),
        "llama": "structure" in llama_response.lower() or "act" in llama_response.lower()
    },
    "Citações específicas": {
        "mixtral": '"' in mixtral_response or "MAYA" in mixtral_response,
        "llama": '"' in llama_response or "MAYA" in llama_response
    }
}

print(f"{'Característica':<30} {'Mixtral':<15} {'Llama-70B':<15}")
print("-"*40)
for quality, checks in qualities.items():
    mixtral_check = "✅" if checks["mixtral"] else "❌"
    llama_check = "✅" if checks["llama"] else "❌"
    print(f"{quality:<30} {mixtral_check:<15} {llama_check:<15}")

print("\n💡 INSIGHTS:")
print("-"*40)

# Calcular vencedor
mixtral_score = sum(1 for q in qualities.values() if q["mixtral"])
llama_score = sum(1 for q in qualities.values() if q["llama"])

if llama_score > mixtral_score:
    print("🏆 LLAMA-70B apresenta QUALIDADE SUPERIOR")
    print("   - Síntese mais coerente e profunda")
    print("   - Melhor fundamentação teórica")
    print("   - Feedback mais acionável")
elif mixtral_score > llama_score:
    print("🏆 MIXTRAL apresenta qualidade superior")
    print("   - Análise mais eficiente")
else:
    print("🤝 EMPATE em qualidade")

# Análise de custo-benefício
print("\n💰 CUSTO-BENEFÍCIO:")
print("-"*40)
if llama_time > 0 and mixtral_time > 0:
    time_ratio = llama_time / mixtral_time
    quality_ratio = llama_score / max(mixtral_score, 1)

    print(f"Tempo adicional Llama-70B: {(time_ratio-1)*100:.0f}%")
    print(f"Qualidade adicional: {(quality_ratio-1)*100:.0f}%")

    if quality_ratio > time_ratio:
        print("✅ Vale a pena usar Llama-70B (ganho de qualidade > custo de tempo)")
    else:
        print("⚠️  Avaliar caso a caso (custo de tempo significativo)")

print("\n📁 ARQUIVOS SALVOS:")
print("   - mixtral_analysis.txt (análise completa Mixtral)")
print("   - llama70b_analysis.txt (análise completa Llama-70B)")

print("\n" + "="*80)
print("✨ Comparação concluída!")
print("="*80)