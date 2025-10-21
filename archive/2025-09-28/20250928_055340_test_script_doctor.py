#!/usr/bin/env python3
"""
🏥 TESTE: Script Doctor vs Forensic
Verifica se a persona de Script Doctor melhora os resultados
"""

import json
import subprocess
import time
from pathlib import Path
import re

def analyze_response(response: str) -> dict:
    """Analisa qualidade da resposta"""

    words = len(response.split())

    # Elementos do Script Doctor
    doctor_elements = {
        "medical_terms": len(re.findall(r'\b(diagnosis|symptoms?|treatment|surgery|patient|prescription|cure|therapy|disease|syndrome|infection|pathology)\b', response.lower())),
        "authority_markers": len(re.findall(r'\b(my experience|I\'ve seen|in my career|Hollywood|blockbuster|Oscar|studio|million)\b', response.lower())),
        "confidence_level": len(re.findall(r'\b(immediately|clearly|obviously|definitely|must|need to|require)\b', response.lower())),
        "specific_fixes": len(re.findall(r'(Before:.*After:|Instead of.*try|Change.*to|Replace.*with)', response, re.IGNORECASE))
    }

    # Elementos forenses
    forensic_elements = {
        "evidence": len(re.findall(r'\b(evidence|analysis|investigation|forensic|examination)\b', response.lower())),
        "quotes": len(re.findall(r'"[^"]{10,}"', response)),
        "objectivity": len(re.findall(r'\b(appears|seems|suggests|indicates|shows)\b', response.lower()))
    }

    # Score de assertividade (Script Doctor deve ser mais assertivo)
    assertiveness = (doctor_elements["confidence_level"] + doctor_elements["authority_markers"]) / (words / 100)

    # Score de soluções práticas
    practicality = doctor_elements["specific_fixes"] / max(1, (words / 200))

    return {
        "words": words,
        "doctor_elements": doctor_elements,
        "forensic_elements": forensic_elements,
        "assertiveness_score": round(assertiveness, 2),
        "practicality_score": round(practicality, 2),
        "total_doctor_markers": sum(doctor_elements.values()),
        "total_forensic_markers": sum(forensic_elements.values())
    }

def test_method(file_path: str, method_name: str, test_script: str):
    """Testa um método específico"""

    print(f"\n🔬 Testing {method_name}...")

    if not Path(file_path).exists():
        print(f"   ❌ File not found")
        return None

    with open(file_path, 'r') as f:
        content = f.read()

    # Extrair system prompt
    system_match = re.search(r'## PROMPT SYSTEM.*?(?=\n##|\n===|\Z)', content, re.S)
    if not system_match:
        print(f"   ❌ Could not extract prompt")
        return None

    system_prompt = system_match.group(0).replace("## PROMPT SYSTEM\n\n", "").strip()

    # Incluir o protocolo completo
    protocol_match = re.search(r'===.*?(?=ATTENTION:|REMEMBER:|$)', content, re.S)
    if protocol_match:
        system_prompt += "\n\n" + protocol_match.group(0)

    # Preparar mensagens
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Analyze this dialogue:\n\n{test_script}"}
    ]

    data = {
        "model": "mixtral:8x7b-instruct-v0.1-q5_K_M",
        "messages": messages,
        "stream": False,
        "options": {
            "temperature": 0.7,
            "top_p": 0.9,
            "repeat_penalty": 1.1,
            "num_predict": 2000
        }
    }

    try:
        start = time.time()

        cmd = ["curl", "-s", "-X", "POST", "http://localhost:11434/api/chat",
               "-H", "Content-Type: application/json",
               "-d", json.dumps(data)]

        result = subprocess.run(cmd, capture_output=True, text=True, timeout=90)

        if result.returncode == 0:
            response_data = json.loads(result.stdout)
            response_text = response_data.get("message", {}).get("content", "")

            if response_text:
                elapsed = time.time() - start
                analysis = analyze_response(response_text)

                print(f"   ✅ Completed in {elapsed:.1f}s")
                print(f"   📝 Words: {analysis['words']}")
                print(f"   🏥 Doctor markers: {analysis['total_doctor_markers']}")
                print(f"   🔬 Forensic markers: {analysis['total_forensic_markers']}")
                print(f"   💪 Assertiveness: {analysis['assertiveness_score']}")
                print(f"   🔧 Practicality: {analysis['practicality_score']}")

                return {
                    "method": method_name,
                    "response": response_text,
                    "analysis": analysis,
                    "time": elapsed
                }

    except Exception as e:
        print(f"   ❌ Error: {e}")

    return None

def main():
    print("="*60)
    print("🏥 TESTE: Script Doctor vs Forensic")
    print("Hipótese: Persona autoritária pode melhorar resultados")
    print("="*60)

    # Script de teste com problemas óbvios
    test_script = """INT. RESTAURANT - NIGHT

JOHN and MARY sit across from each other.

JOHN
I love you so much.

MARY
I love you too.

JOHN
We've been together five years.

MARY
Yes, five wonderful years.

JOHN
I have something to ask you.

MARY
What is it?

JOHN
Will you marry me?

MARY
(surprised)
Oh my God! Yes!

They kiss."""

    # Testar ambos os métodos
    methods = [
        ("super_specialists/02_dialogue_forensic.md", "Forensic Original"),
        ("super_specialists/02_dialogue_script_doctor.md", "Script Doctor")
    ]

    results = []

    for file_path, method_name in methods:
        result = test_method(file_path, method_name, test_script)
        if result:
            results.append(result)

            # Salvar resposta
            with open(f"{method_name.replace(' ', '_')}_response.txt", 'w') as f:
                f.write(result['response'])

    # Comparação final
    if len(results) == 2:
        print("\n" + "="*60)
        print("📊 COMPARAÇÃO FINAL")
        print("="*60)

        forensic = results[0]
        doctor = results[1]

        print("\n📝 Volume de Análise:")
        print(f"  Forensic: {forensic['analysis']['words']} palavras")
        print(f"  Doctor: {doctor['analysis']['words']} palavras")

        print("\n🎯 Assertividade:")
        print(f"  Forensic: {forensic['analysis']['assertiveness_score']}")
        print(f"  Doctor: {doctor['analysis']['assertiveness_score']}")

        print("\n💊 Soluções Práticas:")
        print(f"  Forensic: {forensic['analysis']['practicality_score']}")
        print(f"  Doctor: {doctor['analysis']['practicality_score']}")

        print("\n🏥 Elementos Script Doctor:")
        print(f"  Forensic: {forensic['analysis']['total_doctor_markers']}")
        print(f"  Doctor: {doctor['analysis']['total_doctor_markers']}")

        # Análise qualitativa
        print("\n" + "="*60)
        print("🎯 ANÁLISE QUALITATIVA")
        print("="*60)

        # Verificar se Doctor deu prescrições específicas
        if "Before:" in doctor['response'] or "After:" in doctor['response']:
            print("\n✅ Script Doctor forneceu reescrituras específicas!")
        else:
            print("\n❌ Script Doctor não forneceu reescrituras")

        # Verificar autoridade
        if doctor['analysis']['assertiveness_score'] > forensic['analysis']['assertiveness_score']:
            print("✅ Script Doctor mais assertivo e confiante")
        else:
            print("❌ Script Doctor não demonstrou autoridade esperada")

        # Verificar praticidade
        if doctor['analysis']['practicality_score'] > forensic['analysis']['practicality_score']:
            print("✅ Script Doctor mais prático e orientado a soluções")
        else:
            print("❌ Script Doctor não foi mais prático")

        # Conclusão
        print("\n" + "="*60)
        print("🏆 VENCEDOR")
        print("="*60)

        doctor_wins = 0
        forensic_wins = 0

        if doctor['analysis']['words'] > forensic['analysis']['words']:
            doctor_wins += 1
        else:
            forensic_wins += 1

        if doctor['analysis']['assertiveness_score'] > forensic['analysis']['assertiveness_score']:
            doctor_wins += 1
        else:
            forensic_wins += 1

        if doctor['analysis']['practicality_score'] > forensic['analysis']['practicality_score']:
            doctor_wins += 1
        else:
            forensic_wins += 1

        if doctor_wins > forensic_wins:
            print("\n🏥 SCRIPT DOCTOR vence com persona mais autoritária!")
            print(f"Pontos: Doctor {doctor_wins} x {forensic_wins} Forensic")
            print("\nA persona de 'expert renomado' parece ativar respostas mais")
            print("assertivas e práticas no modelo.")
        else:
            print("\n🔬 FORENSIC ainda superior mesmo contra Script Doctor")
            print(f"Pontos: Forensic {forensic_wins} x {doctor_wins} Doctor")
            print("\nA objetividade forense supera até autoridade médica.")

        # Salvar relatório
        report = {
            "test": "Script Doctor vs Forensic",
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "results": {
                "forensic": {
                    "words": forensic['analysis']['words'],
                    "assertiveness": forensic['analysis']['assertiveness_score'],
                    "practicality": forensic['analysis']['practicality_score'],
                    "doctor_markers": forensic['analysis']['total_doctor_markers']
                },
                "script_doctor": {
                    "words": doctor['analysis']['words'],
                    "assertiveness": doctor['analysis']['assertiveness_score'],
                    "practicality": doctor['analysis']['practicality_score'],
                    "doctor_markers": doctor['analysis']['total_doctor_markers']
                }
            },
            "winner": "Script Doctor" if doctor_wins > forensic_wins else "Forensic"
        }

        with open("script_doctor_test_report.json", 'w') as f:
            json.dump(report, f, indent=2)

        print(f"\n📁 Relatório salvo: script_doctor_test_report.json")

if __name__ == "__main__":
    main()