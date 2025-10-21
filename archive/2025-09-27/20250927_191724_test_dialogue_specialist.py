#!/usr/bin/env python3
"""
Teste do especialista DIALOGUE corrigido
Verifica se ele apenas ANALISA ao invés de CRIAR conteúdo
"""

import requests
import json

# Roteiro pequeno para teste
test_screenplay = """
INT. APARTMENT - NIGHT

SARAH (30s) sits alone at the kitchen table, staring at a cold cup of coffee.

SARAH
(to herself)
Three years. Three years and nothing changes.

She stands abruptly, the chair scraping against the floor.

SARAH (CONT'D)
I can't do this anymore.

The doorbell RINGS. Sarah freezes.

SARAH (CONT'D)
(whispered)
Not now...

She approaches the door slowly, hand trembling as she reaches for the handle.

FADE OUT.
"""

def test_dialogue_specialist():
    print("=" * 60)
    print("🔍 TESTE: ESPECIALISTA DIALOGUE CORRIGIDO")
    print("=" * 60)
    print()
    print("📝 Testando com roteiro pequeno...")
    print("🎯 Objetivo: Verificar que NÃO cria conteúdo fictício")
    print()

    # Prompt para o especialista
    prompt = f"Analyze this screenplay excerpt:\n{test_screenplay}"

    # Chamar Ollama
    response = requests.post(
        'http://localhost:11434/api/generate',
        json={
            'model': 'dialogue-analyst',
            'prompt': prompt,
            'stream': False,
            'options': {
                'temperature': 0.35
            }
        }
    )

    if response.status_code == 200:
        result = response.json()
        analysis = result.get('response', '')

        print("📊 ANÁLISE DO ESPECIALISTA:")
        print("-" * 40)
        print(analysis)
        print("-" * 40)
        print()

        # Verificar se tem conteúdo fictício
        fictional_indicators = [
            "INT.",
            "EXT.",
            "Scene 27",
            "Scene 28",
            "Dr. Souza",
            "FADE IN",
            "(CONT'D)"
        ]

        has_fictional = False
        for indicator in fictional_indicators:
            if indicator in analysis and indicator not in test_screenplay:
                print(f"❌ PROBLEMA: Encontrado conteúdo fictício: '{indicator}'")
                has_fictional = True

        if not has_fictional:
            print("✅ SUCESSO: Nenhum conteúdo fictício detectado!")
            print("✅ Especialista está analisando, não criando!")
        else:
            print("❌ FALHA: Especialista ainda está criando conteúdo!")

    else:
        print(f"❌ Erro ao chamar Ollama: {response.status_code}")

if __name__ == "__main__":
    test_dialogue_specialist()