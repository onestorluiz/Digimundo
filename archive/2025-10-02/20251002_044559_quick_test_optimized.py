#!/usr/bin/env python3
"""
TESTE RÁPIDO: Verificar se otimização funciona
Testa com apenas 1000 palavras para ser rápido
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from specialists.implementations.character_dialogue_specialist import DrDialogue
from specialists.dual_core.base.dual_core_wrapper import DualCoreWrapper
import time
import re


screenplay_path = Path(__file__).parent.parent / "content/screenplays/personal/sonhos_sem_lembrancas_t3.txt"
screenplay = screenplay_path.read_text(encoding='utf-8', errors='ignore')

# Apenas 1000 palavras para teste rápido
screenplay_excerpt = ' '.join(screenplay.split()[:1000])

specialist = DrDialogue()

print("\n" + "="*80)
print("⚡ TESTE RÁPIDO: Modelo Otimizado (shallow mode)")
print("="*80)
print(f"Roteiro: 1000 palavras")
print(f"Modelo: scripturemon-optimized")
print(f"Deep context: NÃO (para ser rápido)")
print("="*80)

wrapper = DualCoreWrapper(
    python_specialist=specialist,
    llm_model="scripturemon-optimized",
    use_theory=True,
    deep_context=False  # Shallow para ser rápido
)

print(f"\n⏳ Executando análise...")
start = time.time()

result = wrapper.analyze(screenplay_excerpt)
elapsed = time.time() - start

analysis = result.get('llm_insights', '')

print(f"\n✅ Completado em {elapsed:.1f}s")
print(f"📏 Output: {len(analysis)} chars ({len(analysis.split())} palavras)")

# Métricas
scenes = len(re.findall(r'\bscene\s+\d+|\bcena\s+\d+', analysis, re.IGNORECASE))
quotes = len(re.findall(r'["""]([^"""]{15,})["""]', analysis))
characters = sum([
    analysis.lower().count('samantha'),
    analysis.lower().count('alberto'),
    analysis.lower().count('kleber')
])

print(f"\n📊 Citações específicas:")
print(f"   Scene refs: {scenes}")
print(f"   Dialogue quotes: {quotes}")
print(f"   Character mentions: {characters}")

# Check for generic phrases
generic = len(re.findall(r'\bcould be improved|\bneeds work|\bpoderia ser melhorado', analysis, re.IGNORECASE))
print(f"\n⚠️  Generic phrases: {generic}")

# Preview
print(f"\n📄 PREVIEW (primeiros 800 chars):")
print("=" * 80)
print(analysis[:800])
print("...")
print("=" * 80)

# Avaliação
print(f"\n🎯 AVALIAÇÃO:")
if scenes >= 2 and quotes >= 2 and characters >= 3 and generic == 0:
    print("✅ EXCELENTE - Análise específica e bem fundamentada!")
elif scenes >= 1 and quotes >= 1 and characters >= 2:
    print("⚠️  BOM - Tem especificidade mas pode melhorar")
else:
    print("❌ FRACO - Análise ainda genérica")

print(f"\n{'='*80}\n")
