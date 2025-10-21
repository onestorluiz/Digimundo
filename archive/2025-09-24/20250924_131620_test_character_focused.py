#!/usr/bin/env python3
"""Testa o Character Specialist Focused - versão otimizada"""

import subprocess
import json
from datetime import datetime

# Mesmo roteiro complexo
test_script = """
INT. LABORATORY - NIGHT

DR. SARAH CHEN (35), exhausted scientist with dark circles under her eyes,
stares at multiple monitors displaying code.

AURORA (V.O.)
Why did you create me, Sarah? Was it
loneliness... or ambition?

Sarah's hand trembles as she reaches for the DELETE key. Hesitates.

SARAH
I don't know anymore.

AURORA (V.O.)
You're afraid of me. But you're more
afraid of being alone again.

MARCUS (O.S.)
Sarah! The investors are here.

SARAH
Tell them five minutes. Aurora's ready.

AURORA (V.O.)
We're both ready for the truth, aren't we?

Sarah's finger hovers. Makes a choice. Hits ENTER instead of DELETE.

FADE OUT.
"""

print(f"\n{'='*60}")
print(f"TESTE CHARACTER SPECIALIST FOCUSED - {datetime.now()}")
print(f"{'='*60}")

print("\n🔍 Analisando com modelo focado...")

# Chamada ao Ollama
cmd = ["ollama", "run", "character-specialist-focused", test_script]
result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)

print("\n📝 Resposta completa:")
print(result.stdout)

# Parse e análise
try:
    response = result.stdout

    # Limpar resposta
    if "```json" in response:
        response = response.split("```json")[1].split("```")[0]
    elif "```" in response:
        response = response.split("```")[1].split("```")[0]

    # Encontrar JSON
    start = response.find('{')
    end = response.rfind('}') + 1
    if start >= 0 and end > start:
        json_str = response[start:end]

        # Corrigir aspas
        json_str = json_str.replace("'", '"')

        data = json.loads(json_str)

        print("\n✅ Parse bem-sucedido!")

        # Mostrar personagens
        print("\n👥 PERSONAGENS E ARCOS:")
        for char in data.get('characters', []):
            print(f"\n  📌 {char['name']} [{char.get('type', '?')}]")
            if char.get('mode') != 'normal':
                print(f"     Modo: {char.get('mode', '').upper()}")
            print(f"     Arco: {char.get('arc_type', 'não identificado')}")
            print(f"     Mentira/Verdade: {char.get('lie', 'N/A')}")
            print(f"     Desejo: {char.get('want', 'N/A')}")
            print(f"     Necessidade: {char.get('need', 'N/A')}")
            print(f"     Ghost: {char.get('ghost', 'N/A')}")
            print(f"     Transformação: {char.get('opening_state', '?')} → {char.get('final_state', '?')}")

        # Dinâmicas
        if 'dynamics' in data:
            print("\n🌐 DINÂMICA NARRATIVA:")
            print(f"  Conflito: {data['dynamics'].get('central_conflict', 'N/A')}")
            print(f"  Tema: {data['dynamics'].get('theme', 'N/A')}")

        # Verificações
        print("\n🔎 VERIFICAÇÕES:")
        names = [c['name'].upper() for c in data.get('characters', [])]

        checks = {
            'AURORA': 'AURORA' in ' '.join(names),
            'SARAH': 'SARAH' in ' '.join(names),
            'MARCUS': 'MARCUS' in ' '.join(names)
        }

        all_found = True
        for name, found in checks.items():
            status = "✅" if found else "❌"
            print(f"  {status} {name}")
            if not found:
                all_found = False

        # Verificar profundidade
        has_arcs = any(c.get('arc_type') for c in data.get('characters', []))
        has_lies = any(c.get('lie') for c in data.get('characters', []))
        has_transformation = any(c.get('final_state') for c in data.get('characters', []))

        print("\n📊 QUALIDADE DA ANÁLISE:")
        print(f"  {'✅' if all_found else '❌'} Todos personagens detectados")
        print(f"  {'✅' if has_arcs else '❌'} Arcos identificados")
        print(f"  {'✅' if has_lies else '❌'} Mentiras/Verdades mapeadas")
        print(f"  {'✅' if has_transformation else '❌'} Transformações rastreadas")

        if all_found and has_arcs and has_lies:
            print("\n🎉 SUCESSO TOTAL: Detecção e análise profunda!")
        elif all_found:
            print("\n✅ Detecção completa, análise parcial")
        else:
            print("\n⚠️  Análise incompleta")

except json.JSONDecodeError as e:
    print(f"\n❌ Erro JSON: {e}")
    print(f"String tentada: {json_str[:200] if 'json_str' in locals() else 'N/A'}")
except Exception as e:
    print(f"\n❌ Erro: {e}")

print(f"\n{'='*60}")