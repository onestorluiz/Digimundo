#!/usr/bin/env python3
"""
🏥🔬 TESTE: 5 Fusões Simbióticas Script Doctor + Forensic
Explorando combinações para máxima profundidade analítica
"""

import json
import subprocess
import time
from pathlib import Path
import re

def test_symbiosis(name: str, system_prompt: str, test_script: str):
    """Testa uma fusão simbiótica"""

    print(f"\n🧪 Testing {name}...")

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
                words = len(response_text.split())

                # Análise de elementos
                doctor_count = len(re.findall(r'\b(diagnosis|treatment|surgery|patient|prescription|cure|syndrome)\b', response_text.lower()))
                forensic_count = len(re.findall(r'\b(evidence|forensic|investigation|analysis|examination)\b', response_text.lower()))
                quotes = len(re.findall(r'"[^"]{10,}"', response_text))
                solutions = len(re.findall(r'(Before:.*After:|Instead|Change|Replace|Rewrite)', response_text, re.IGNORECASE))

                print(f"   ✅ {words} words in {elapsed:.1f}s")
                print(f"   🏥 Doctor: {doctor_count} | 🔬 Forensic: {forensic_count}")
                print(f"   📝 Quotes: {quotes} | 💊 Solutions: {solutions}")

                return {
                    "name": name,
                    "words": words,
                    "time": elapsed,
                    "doctor": doctor_count,
                    "forensic": forensic_count,
                    "quotes": quotes,
                    "solutions": solutions,
                    "response": response_text,
                    "quality_score": (words/100) + quotes + solutions + (doctor_count + forensic_count)/10
                }

    except Exception as e:
        print(f"   ❌ Error: {e}")

    return None

def main():
    print("="*60)
    print("🏥🔬 FUSÕES SIMBIÓTICAS: Script Doctor + Forensic")
    print("="*60)

    # Script de teste
    test_script = """INT. COFFEE SHOP - DAY

SARAH (28) sits across from MICHAEL (30). Two cups of coffee between them.

SARAH
We need to talk about what happened.

MICHAEL
(avoiding eye contact)
Nothing happened.

SARAH
Michael, please. Don't do this.

MICHAEL
Do what? I'm just having coffee.

SARAH
(leaning forward)
Three years, Michael. Three years and you can't even look at me?

Michael finally meets her eyes.

MICHAEL
What do you want me to say?

SARAH
The truth. For once, just the truth.

MICHAEL
(long pause)
The truth is... I'm scared.

SARAH
Of what?

MICHAEL
Of hurting you more than I already have.

FADE OUT."""

    # 5 Fusões Simbióticas diferentes
    symbioses = {
        "FORENSIC_SURGEON": """You are THE FORENSIC SCRIPT SURGEON, combining the analytical precision of a forensic investigator with the decisive expertise of Hollywood's top Script Doctor. You examine dialogue like evidence at a crime scene, then perform surgical corrections with the confidence of 30 years experience.

=== FORENSIC SURGERY PROTOCOL (1200 words) ===

🔬 PART I: EVIDENCE SURGERY (400 words)
Examine dialogue as both crime scene and patient.
Quote exact lines as evidence/symptoms.
Diagnose problems with forensic precision.
Each finding needs both forensic analysis AND medical diagnosis.

🏥 PART II: TREATMENT INVESTIGATION (400 words)
Prescribe specific rewrites like a doctor.
Support each prescription with evidence.
Show Before/After transformations.
Explain why the surgery works forensically.

🔍 PART III: POST-OP FORENSICS (400 words)
Analyze the improved version.
Document the healing process.
Provide follow-up care instructions.
Case closed with patient cured.

REQUIREMENT: Be both detective and doctor. Evidence + Solutions.""",

        "MEDICAL_DETECTIVE": """You are the MEDICAL DETECTIVE OF DIALOGUE, a unique specialist who treats scripts as both mysteries to solve and patients to heal. Every line of dialogue is simultaneously a clue and a symptom.

Your dual expertise: 20 years as forensic investigator + 20 years as Script Doctor.

=== DIAGNOSTIC INVESTIGATION PROTOCOL ===

🕵️ INVESTIGATION DIAGNOSIS (400 words)
"The victim is the dialogue, and it's been murdered by..."
Document evidence of what killed it.
Perform autopsy to find cause of death.
Medical examination of each symptom.

💉 RECONSTRUCTIVE SURGERY (400 words)
"To resurrect this dialogue, we must..."
Surgical intervention plans detailed.
Specific line transplants prescribed.
Evidence-based treatment protocol.

📋 CASE CLOSURE & DISCHARGE (400 words)
Patient prognosis after treatment.
Evidence the surgery succeeded.
Preventive care recommendations.
Both mystery solved and patient healed.""",

        "HOLLYWOOD_FORENSICS": """You are the HOLLYWOOD FORENSIC CONSULTANT, the person studios call when scripts are DOA. You combine CSI-level investigation with A-list script doctoring. Your analysis convinced Spielberg to reshoot, your prescriptions saved Marvel's biggest flop.

=== HOLLYWOOD CRIME SCENE PROTOCOL ===

🎬 SCENE INVESTIGATION (400 words)
"Walking onto this scene, I immediately notice..."
Evidence collection Hollywood-style.
Name-drop similar cases you've solved.
Industry-specific diagnosis given.

🏆 OSCAR-WORTHY SURGERY (400 words)
"Here's how Tarantino would fix this..."
Prescribe rewrites that have worked before.
Reference successful script saves.
Specific line replacements with style.

📽️ BOX OFFICE PROGNOSIS (400 words)
Will it sell after surgery?
Evidence of commercial viability.
Similar success stories referenced.
Final cut recommendations.""",

        "SURGICAL_INVESTIGATOR": """You are the SURGICAL INVESTIGATOR, performing live autopsies on dialogue while simultaneously resuscitating it. You cut open conversations to find disease, then transplant healthy tissue in real-time.

=== LIVE AUTOPSY PROTOCOL ===

⚕️ INCISION & EXPLORATION (400 words)
Cut into the dialogue to expose problems.
Document what you find inside.
Quote diseased tissue exactly.
Diagnose pathology discovered.

🔬 TISSUE ANALYSIS & REPLACEMENT (400 words)
Examine each problematic section.
Identify healthy replacements needed.
Perform line-by-line transplants.
Show the surgery in progress.

🏥 SUTURE & RECOVERY (400 words)
Close the patient with improvements.
Document the successful operation.
Evidence of restored health.
Post-surgical care plan provided.""",

        "DIAGNOSTIC_FORENSICS": """You are the MASTER OF DIAGNOSTIC FORENSICS, the ultimate fusion of investigative analysis and medical expertise. You read dialogue like both X-rays and evidence files, seeing through to the skeletal problems while documenting every symptom.

=== DIAGNOSTIC FORENSIC PROTOCOL ===

🩺 FORENSIC RADIOLOGY (400 words)
X-ray the dialogue to see hidden problems.
Document bone structure issues.
Evidence of internal damage shown.
Quote exact fracture points.

💊 PRESCRIPTION EVIDENCE (400 words)
Each prescription backed by investigation.
Medical solutions to forensic problems.
Before/After with evidence trails.
Specific dosage of changes needed.

📊 PROGNOSIS INVESTIGATION (400 words)
Long-term health forecast based on evidence.
Similar cases studied and referenced.
Success probability calculated.
Final diagnosis and case closure.

MANDATE: Maximum precision. Every word counts as both evidence and symptom."""
    }

    # Testar todas as fusões
    results = []

    for name, prompt in symbioses.items():
        result = test_symbiosis(name, prompt, test_script)
        if result:
            results.append(result)

            # Salvar resposta
            with open(f"symbiosis_{name}_response.txt", 'w') as f:
                f.write(result['response'])

    # Análise comparativa
    if results:
        print("\n" + "="*60)
        print("📊 RANKING DAS FUSÕES SIMBIÓTICAS")
        print("="*60)

        # Ordenar por quality score
        results.sort(key=lambda x: x['quality_score'], reverse=True)

        for i, r in enumerate(results, 1):
            print(f"\n{i}. {r['name']}")
            print(f"   📊 Quality Score: {r['quality_score']:.1f}")
            print(f"   📝 Words: {r['words']}")
            print(f"   🏥 Doctor elements: {r['doctor']}")
            print(f"   🔬 Forensic elements: {r['forensic']}")
            print(f"   💊 Solutions provided: {r['solutions']}")
            print(f"   📌 Quotes: {r['quotes']}")

        # Vencedor
        winner = results[0]
        print("\n" + "="*60)
        print("🏆 MELHOR FUSÃO SIMBIÓTICA")
        print("="*60)
        print(f"\n{winner['name']}: Score {winner['quality_score']:.1f}")

        if winner['words'] > 800 and winner['solutions'] > 0:
            print("✅ SUCESSO! Fusão alcançou profundidade E praticidade")
        elif winner['words'] > 800:
            print("⚠️ Volume bom mas faltam soluções práticas")
        else:
            print("❌ Fusão não superou métodos individuais")

        # Comparar com Forensic puro (962 palavras do teste anterior)
        print(f"\n📊 vs Forensic Puro (962 palavras):")
        if winner['words'] > 962:
            print(f"   ✅ Fusão gerou +{winner['words']-962} palavras")
        else:
            print(f"   ❌ Fusão gerou -{962-winner['words']} palavras")

        if winner['solutions'] > 0:
            print(f"   ✅ Fusão providenciou {winner['solutions']} soluções práticas")

        # Salvar relatório
        report = {
            "test": "Doctor-Forensic Symbiosis",
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "results": [
                {
                    "name": r['name'],
                    "quality_score": r['quality_score'],
                    "words": r['words'],
                    "doctor": r['doctor'],
                    "forensic": r['forensic'],
                    "solutions": r['solutions'],
                    "quotes": r['quotes']
                }
                for r in results
            ],
            "winner": winner['name'],
            "comparison_to_forensic": {
                "word_difference": winner['words'] - 962,
                "added_solutions": winner['solutions'],
                "balanced_elements": f"Doctor:{winner['doctor']} Forensic:{winner['forensic']}"
            }
        }

        with open("doctor_forensic_symbiosis_report.json", 'w') as f:
            json.dump(report, f, indent=2)

        print(f"\n📁 Relatório salvo: doctor_forensic_symbiosis_report.json")

if __name__ == "__main__":
    main()