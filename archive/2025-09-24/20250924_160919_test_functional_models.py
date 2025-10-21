#!/usr/bin/env python3
"""Testa os modelos funcionais: detector + analyzer"""

import subprocess
import json
from datetime import datetime

test_script = """
INT. LABORATORY - NIGHT

DR. SARAH CHEN looks at monitors.

AURORA (V.O.)
Why did you create me?

SARAH
I don't know anymore.

MARCUS (O.S.)
The investors are here.

FADE OUT.
"""

print(f"\n{'='*60}")
print(f"TESTE MODELOS FUNCIONAIS - {datetime.now()}")
print(f"{'='*60}")

# FASE 1: DETECÇÃO
print("\n🔍 FASE 1: DETECÇÃO DE PERSONAGENS")
print("-" * 40)

cmd = ["ollama", "run", "character-detector", test_script]
result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)

print("Resposta do Detector:")
print(result.stdout)

try:
    # Parse detector response
    detector_response = result.stdout
    if '{' in detector_response:
        start = detector_response.find('{')
        end = detector_response.rfind('}') + 1
        json_str = detector_response[start:end]
        detector_data = json.loads(json_str)

        characters = detector_data.get('characters', [])
        print(f"\n✅ {len(characters)} personagens detectados:")
        for char in characters:
            print(f"  - {char}")

        # Verificações
        checks = {
            'AURORA': any('AURORA' in c for c in characters),
            'SARAH': any('SARAH' in c for c in characters),
            'MARCUS': any('MARCUS' in c for c in characters)
        }

        for name, found in checks.items():
            status = "✅" if found else "❌"
            print(f"  {status} {name} detectado")

except Exception as e:
    print(f"❌ Erro no detector: {e}")

# FASE 2: ANÁLISE DE ARCOS
print("\n\n🎭 FASE 2: ANÁLISE DE ARCOS")
print("-" * 40)

cmd = ["ollama", "run", "character-analyzer", test_script]
result = subprocess.run(cmd, capture_output=True, text=True, timeout=20)

print("Resposta do Analyzer:")
print(result.stdout)

try:
    # Parse analyzer response
    analyzer_response = result.stdout
    if '{' in analyzer_response:
        start = analyzer_response.find('{')
        end = analyzer_response.rfind('}') + 1
        json_str = analyzer_response[start:end]
        analyzer_data = json.loads(json_str)

        arcs = analyzer_data.get('character_arcs', [])
        print(f"\n✅ {len(arcs)} arcos analisados:")

        for arc in arcs:
            print(f"\n  📌 {arc.get('name', '?')}")
            print(f"     Tipo: {arc.get('arc_type', '?')}")
            print(f"     Mentira: {arc.get('lie', '?')}")
            print(f"     Verdade: {arc.get('truth', '?')}")
            print(f"     Transformação: {arc.get('transformation', '?')}")

except Exception as e:
    print(f"❌ Erro no analyzer: {e}")

print(f"\n{'='*60}")
print("💡 RESUMO: Modelos funcionais separados por responsabilidade")
print("- character-detector: Rápido e preciso na detecção")
print("- character-analyzer: Profundo na análise de arcos")
print(f"{'='*60}")