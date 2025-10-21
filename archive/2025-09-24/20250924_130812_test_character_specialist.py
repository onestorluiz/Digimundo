#!/usr/bin/env python3
"""Testa o Character Specialist com o caso Aurora"""

import subprocess
import json
from datetime import datetime

test_script = """
INT. LABORATORY - DAY

DR. SARAH CHEN (35), scientist, looks at monitors.

AURORA (V.O.)
Why did you create me?

Sarah hesitates.

SARAH
I didn't mean for this.

MARCUS (O.S.)
The system is online!

FADE OUT.
"""

print(f"\n{'='*60}")
print(f"TESTE CHARACTER SPECIALIST - {datetime.now()}")
print(f"{'='*60}")

print("\n📜 Script de teste:")
print(test_script)

print("\n🔍 Testando detecção de personagens...")

# Chamada ao Ollama
cmd = ["ollama", "run", "character-specialist", test_script]
result = subprocess.run(cmd, capture_output=True, text=True)

print("\n📝 Resposta do modelo:")
print(result.stdout)

# Tentar extrair JSON
try:
    # Procurar JSON na resposta
    response = result.stdout
    if '{' in response and '}' in response:
        start = response.find('{')
        end = response.rfind('}') + 1
        json_str = response[start:end]
        data = json.loads(json_str)

        print("\n✅ JSON parseado com sucesso!")
        print(f"Total de personagens: {data.get('total_found', 0)}")

        print("\n👥 Personagens detectados:")
        for char in data.get('characters', []):
            mode = f" ({char['speaking_mode'].upper()})" if char.get('speaking_mode') != 'normal' else ""
            print(f"  - {char['name']}{mode} [{char.get('type', 'unknown')}]")

        # Verificações críticas
        print("\n🔎 Verificações críticas:")
        names_found = [c['name'].upper() for c in data.get('characters', [])]

        checks = {
            'DR. SARAH CHEN': 'DR. SARAH CHEN' in names_found or 'DR SARAH CHEN' in names_found,
            'AURORA': 'AURORA' in names_found,
            'SARAH': 'SARAH' in names_found,
            'MARCUS': 'MARCUS' in names_found
        }

        for name, found in checks.items():
            status = "✅" if found else "❌"
            print(f"  {status} {name}: {'Detectado' if found else 'NÃO DETECTADO'}")

        # Aurora específico
        if not checks['AURORA']:
            print("\n⚠️  BUG CRÍTICO: AURORA (V.O.) NÃO FOI DETECTADA!")
        else:
            print("\n🎉 SUCESSO: Aurora detectada corretamente!")

except Exception as e:
    print(f"\n❌ Erro ao processar resposta: {e}")
    print("Resposta raw:", result.stdout[:500])

print(f"\n{'='*60}")