#!/usr/bin/env python3
"""
🎺 TESTE: JAZZ ENSEMBLE METHOD para Diálogos
"""

import json
import time
import subprocess
from pathlib import Path

def test_jazz_method():
    """Testa o método Jazz para análise de diálogos"""

    test_script = """FADE IN:

INT. JAZZ CLUB - NIGHT

MILES (50s, weathered) sits at the piano. ELLA (30s, eager) approaches.

ELLA
They say you don't play anymore.

MILES
(not looking up)
They say a lot of things.

ELLA
I came here to hear you play.

MILES
Then you came to the wrong place.

ELLA
(sitting down)
Maybe. Or maybe you're just scared.

Miles finally looks at her. His fingers hover over the keys.

MILES
Scared? Kid, I've played with Bird, Dizzy, Trane...

ELLA
(interrupting)
That was then.

MILES
(long pause, then softly)
Yeah. That was then.

His fingers touch the keys. A single note rings out.

FADE OUT."""

    # Ler o prompt do arquivo Jazz
    with open("/Users/clubproducoes/Digimundo/scripturemon-ultimate/super_specialists/02_dialogue_jazz.md", 'r') as f:
        content = f.read()

    # Extrair system prompt
    import re
    system_match = re.search(r'## PROMPT SYSTEM.*?\n\n(.*?)(?=\n##)', content, re.S)
    if not system_match:
        print("❌ Não consegui extrair prompt")
        return

    system_prompt = system_match.group(1).strip()

    # Configurar mensagens
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Analyze this script's dialogue:\n\n{test_script}"}
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

    print("🎺 Testing JAZZ ENSEMBLE Method...")
    print("="*50)

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

                # Análise específica de Jazz
                jazz_terms = ['rhythm', 'tempo', 'beat', 'groove', 'improvisation',
                             'harmony', 'melody', 'syncopation', 'riff', 'solo']
                jazz_score = sum(1 for term in jazz_terms if term.lower() in response_text.lower())

                print(f"\n📊 RESULTADOS:")
                print(f"   ⏱️ Tempo: {elapsed:.1f}s")
                print(f"   📝 Palavras: {word_count}")
                print(f"   🎵 Termos musicais: {jazz_score}")
                print(f"   🎺 Jazz Score: {jazz_score/10:.1%}")

                # Salvar resposta
                output_dir = Path("jazz_test_results")
                output_dir.mkdir(exist_ok=True)

                with open(output_dir / "jazz_dialogue_response.txt", 'w') as f:
                    f.write(response_text)

                print(f"\n📁 Resposta salva em: {output_dir}/")

                # Mostrar trecho da resposta
                print("\n🎼 AMOSTRA DA ANÁLISE:")
                print("-"*50)
                print(response_text[:500] + "...")

                return response_text

    except Exception as e:
        print(f"❌ Erro: {e}")
        return None

if __name__ == "__main__":
    test_jazz_method()