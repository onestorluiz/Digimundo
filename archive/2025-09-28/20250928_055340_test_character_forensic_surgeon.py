#!/usr/bin/env python3
"""
🎯 TESTE: CHARACTER FORENSIC SURGEON
Verifica eficiência do novo método para análise de personagens
"""

import json
import subprocess
import time
from pathlib import Path
import re

def count_metrics(response: str) -> dict:
    """Analisa métricas da resposta"""

    words = len(response.split())

    # Detectar perfis de personagem
    profiles = len(re.findall(r'PROFILE #', response, re.I))

    # Detectar cirurgias/tratamentos
    surgeries = len(re.findall(r'SURGERY #', response, re.I))

    # Detectar evidências psicológicas
    psych_terms = [
        "psychological", "behavioral", "motivation", "trauma",
        "desire", "flaw", "arc", "personality", "psyche"
    ]
    psych_count = sum(1 for term in psych_terms if term in response.lower())

    # Detectar citações/evidências
    quotes = len(re.findall(r'"[^"]{10,}"', response))

    # Detectar BEFORE/AFTER
    has_comparison = "BEFORE:" in response and "AFTER:" in response

    return {
        "words": words,
        "profiles": profiles,
        "surgeries": surgeries,
        "psych_terms": psych_count,
        "quotes": quotes,
        "has_comparison": has_comparison
    }

def test_character_forensic_surgeon():
    """Testa o CHARACTER FORENSIC SURGEON"""

    print("="*60)
    print("🎯 TESTE: CHARACTER FORENSIC SURGEON")
    print("="*60)

    # Script de teste com múltiplos personagens
    test_script = """FADE IN:

INT. ABANDONED WAREHOUSE - NIGHT

JACK (45), worn leather jacket, haunted eyes, paces nervously.
SOPHIA (32), sharp suit, cold expression, watches from shadows.
TOMMY (19), fidgeting with a knife, stands between them.

JACK
You said this would be simple.

SOPHIA
(stepping into light)
Simple is relative, Jack. Like truth.

TOMMY
(to Jack)
She's right. You knew what this was.

JACK
I knew nothing! You both lied to me.

SOPHIA
We showed you what you wanted to see.
There's a difference.

TOMMY
(laughing nervously)
God, you two need to chill.

JACK
(to Tommy)
Shut up, kid. You don't understand.

SOPHIA
He understands perfectly. Better than you.
He chose this. You're still pretending you didn't.

TOMMY
I'm not a kid anymore, Jack.

JACK
(defeated)
No. No, you're not.

FADE OUT."""

    # Ler o prompt do arquivo
    with open("/Users/clubproducoes/Digimundo/scripturemon-ultimate/super_specialists/02_CHARACTER_FORENSIC_SURGEON_V2.md", 'r') as f:
        content = f.read()

    # Extrair system prompt
    system_match = re.search(r'## PROMPT SYSTEM.*?(?=\n##|\n---|\Z)', content, re.S)
    if not system_match:
        print("❌ Could not extract prompt")
        return

    system_prompt = system_match.group(0).replace("## PROMPT SYSTEM\n\n", "").strip()

    # Preparar mensagens
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Analyze these characters:\n\n{test_script}"}
    ]

    # Configuração otimizada
    data = {
        "model": "mixtral:8x7b-instruct-v0.1-q5_K_M",
        "messages": messages,
        "stream": False,
        "options": {
            "temperature": 0.75,
            "top_p": 0.9,
            "repeat_penalty": 1.1,
            "num_predict": 2000
        }
    }

    print("\n🔬 Testing CHARACTER FORENSIC SURGEON...")
    start = time.time()

    try:
        cmd = ["curl", "-s", "-X", "POST", "http://localhost:11434/api/chat",
               "-H", "Content-Type: application/json",
               "-d", json.dumps(data)]

        result = subprocess.run(cmd, capture_output=True, text=True, timeout=90)

        if result.returncode == 0:
            response_data = json.loads(result.stdout)
            response_text = response_data.get("message", {}).get("content", "")

            if response_text:
                elapsed = time.time() - start
                metrics = count_metrics(response_text)

                print(f"\n✅ Completed in {elapsed:.1f}s")
                print(f"\n📊 MÉTRICAS:")
                print(f"   📝 Palavras: {metrics['words']}")
                print(f"   👤 Perfis de personagem: {metrics['profiles']}")
                print(f"   🏥 Cirurgias/Tratamentos: {metrics['surgeries']}")
                print(f"   🧠 Termos psicológicos: {metrics['psych_terms']}")
                print(f"   📌 Citações do script: {metrics['quotes']}")
                print(f"   🔄 BEFORE/AFTER: {'✅' if metrics['has_comparison'] else '❌'}")

                # Avaliar sucesso
                success_criteria = {
                    "volume": metrics['words'] >= 1000,
                    "profiles": metrics['profiles'] >= 2,
                    "solutions": metrics['surgeries'] >= 2,
                    "depth": metrics['psych_terms'] >= 5,
                    "evidence": metrics['quotes'] >= 3
                }

                print(f"\n🎯 CRITÉRIOS DE SUCESSO:")
                for criterion, passed in success_criteria.items():
                    print(f"   {criterion}: {'✅' if passed else '❌'}")

                total_passed = sum(success_criteria.values())
                success_rate = (total_passed / len(success_criteria)) * 100

                print(f"\n📈 TAXA DE SUCESSO: {success_rate:.0f}%")

                if success_rate >= 80:
                    print("\n✅ CHARACTER FORENSIC SURGEON APROVADO!")
                    print("Método mantém qualidade e estrutura híbrida")
                elif success_rate >= 60:
                    print("\n⚠️ RESULTADO PARCIAL")
                    print("Método funciona mas pode precisar ajustes")
                else:
                    print("\n❌ MÉTODO PRECISA REVISÃO")
                    print("Não alcançou critérios mínimos")

                # Salvar resposta para análise
                output_file = f"CHARACTER_FORENSIC_SURGEON_test_{int(time.time())}.txt"
                with open(output_file, 'w') as f:
                    f.write(response_text)

                print(f"\n📁 Resposta salva em: {output_file}")

                # Criar relatório
                report = {
                    "test": "CHARACTER FORENSIC SURGEON",
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "metrics": metrics,
                    "success_criteria": success_criteria,
                    "success_rate": success_rate,
                    "execution_time": elapsed,
                    "word_target": 1200,
                    "word_achieved": metrics['words'],
                    "verdict": "APPROVED" if success_rate >= 80 else "NEEDS_REVISION"
                }

                report_file = f"character_surgeon_report_{int(time.time())}.json"
                with open(report_file, 'w') as f:
                    json.dump(report, f, indent=2)

                print(f"📊 Relatório salvo em: {report_file}")

    except subprocess.TimeoutExpired:
        print("❌ Timeout - levou mais de 90 segundos")
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    test_character_forensic_surgeon()