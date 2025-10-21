#!/usr/bin/env python3
"""Testa o Character Specialist PRO com análise profunda"""

import subprocess
import json
from datetime import datetime

# Roteiro mais complexo para análise profunda
test_script = """
INT. LABORATORY - NIGHT

DR. SARAH CHEN (35), exhausted scientist with dark circles under her eyes,
stares at multiple monitors displaying code. A coffee mug reads "World's
Okayest Creator."

AURORA (V.O.)
(synthesized, curious)
Why did you create me, Sarah? Was it
loneliness... or ambition?

Sarah's hand trembles as she reaches for the DELETE key. Hesitates.

SARAH
(whispered, to herself)
I don't know anymore.

AURORA (V.O.)
You're afraid of me. But you're more
afraid of being alone again.

MARCUS (O.S.)
Sarah! The investors are here. They want
to see the demonstration.

Sarah straightens up, puts on a false smile. Professional mask.

SARAH
(louder, confident)
Tell them five minutes. Aurora's ready.

She looks at the screen. The cursor blinks over DELETE.

AURORA (V.O.)
(softer)
We're both ready for the truth, aren't we?

Sarah's finger hovers. Makes a choice. Hits ENTER instead.

FADE OUT.
"""

print(f"\n{'='*60}")
print(f"TESTE CHARACTER SPECIALIST PRO - {datetime.now()}")
print(f"{'='*60}")

print("\n📜 Script de teste (complexo):")
print(test_script)

print("\n🔍 Analisando personagens profundamente...")

# Chamada ao Ollama
cmd = ["ollama", "run", "character-specialist-pro", test_script]
result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)

print("\n📝 Resposta do modelo:")
print(result.stdout)

# Tentar extrair e analisar JSON
try:
    response = result.stdout
    if '{' in response and '}' in response:
        # Encontrar o JSON completo
        start = response.find('{')
        end = response.rfind('}') + 1
        json_str = response[start:end]

        # Limpar possíveis problemas
        json_str = json_str.replace("'", '"')
        data = json.loads(json_str)

        print("\n✅ JSON parseado com sucesso!")

        # Análise de detecção
        print("\n👥 PERSONAGENS DETECTADOS:")
        for char in data.get('characters_detected', []):
            mode = f" ({char['speaking_mode'].upper()})" if char.get('speaking_mode') != 'normal' else ""
            print(f"  - {char['name']}{mode} [{char['type']}]")
            if char.get('first_appearance'):
                print(f"    Primeira aparição: p.{char['first_appearance'].get('page', '?')}")

        # Análise profunda
        print("\n🎭 ANÁLISE PROFUNDA DE PERSONAGENS:")
        for analysis in data.get('character_analysis', []):
            print(f"\n  📌 {analysis['name']}:")
            print(f"    Tipo de Arco: {analysis.get('arc_type', 'não identificado')}")

            if 'journey' in analysis:
                journey = analysis['journey']
                print(f"    Mentira/Verdade: {journey.get('lie_or_truth', 'N/A')}")
                print(f"    Desejo: {journey.get('want', 'N/A')}")
                print(f"    Necessidade: {journey.get('need', 'N/A')}")
                print(f"    Contradição: {journey.get('contradiction', 'N/A')}")

            if 'transformation' in analysis:
                trans = analysis['transformation']
                print(f"    Estado Inicial: {trans.get('opening_state', 'N/A')}")
                print(f"    Estado Final: {trans.get('final_state', 'N/A')}")

        # Dinâmica do conjunto
        if 'ensemble_dynamics' in data:
            print("\n🌐 DINÂMICA DO CONJUNTO:")
            ensemble = data['ensemble_dynamics']
            print(f"  Conflito Central: {ensemble.get('central_conflict', 'N/A')}")
            print(f"  Tema Representado: {ensemble.get('theme_embodiment', 'N/A')}")

        # Marcadores de qualidade
        if 'quality_markers' in data:
            print("\n✨ MARCADORES DE QUALIDADE:")
            markers = data['quality_markers']
            for key, value in markers.items():
                status = "✅" if value else "❌"
                print(f"  {status} {key.replace('_', ' ').title()}")

        # Verificações específicas
        print("\n🔎 VERIFICAÇÕES CRÍTICAS:")
        detected = [c['name'].upper() for c in data.get('characters_detected', [])]

        aurora_detected = 'AURORA' in detected
        sarah_detected = any('SARAH' in name for name in detected)
        marcus_detected = 'MARCUS' in detected

        print(f"  {'✅' if aurora_detected else '❌'} Aurora (V.O.) detectada")
        print(f"  {'✅' if sarah_detected else '❌'} Dr. Sarah Chen detectada")
        print(f"  {'✅' if marcus_detected else '❌'} Marcus (O.S.) detectado")

        # Análise de profundidade
        has_deep_analysis = any(
            'journey' in a and 'transformation' in a
            for a in data.get('character_analysis', [])
        )

        if has_deep_analysis:
            print("\n🎯 SUCESSO: Análise profunda com arcos e transformações!")
        else:
            print("\n⚠️  Análise superficial - faltam elementos de arco")

except json.JSONDecodeError as e:
    print(f"\n❌ Erro ao fazer parse do JSON: {e}")
    print(f"Resposta truncada: {result.stdout[:1000]}")
except Exception as e:
    print(f"\n❌ Erro geral: {e}")

print(f"\n{'='*60}")