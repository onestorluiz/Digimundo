#!/usr/bin/env python3
"""
Teste Ultimate - Validação final do Scripturemon v3
"""

import subprocess
import json
import time
from datetime import datetime

def test_prompt(prompt, model="scripturemon-ultimate"):
    """Testa um único prompt"""
    try:
        process = subprocess.run(
            ["ollama", "run", model],
            input=prompt.encode(),
            capture_output=True,
            timeout=20,
            text=False
        )
        return process.stdout.decode(errors="replace").strip()
    except:
        return "ERRO/TIMEOUT"

def analyze_response(response):
    """Análise específica para problemas conhecidos"""
    score = 50  # Base
    problems = []
    strengths = []
    
    # Verificações positivas
    if any(phrase in response.lower() for phrase in ["eu sou", "eu acredito", "na minha"]):
        score += 15
        strengths.append("primeira_pessoa")
    
    if any(word in response.lower() for word in ["amo", "adoro", "fascina", "paixão", "emociona"]):
        score += 15
        strengths.append("emocional")
    
    if "todo roteiro é uma jornada da alma" in response.lower():
        score += 10
        strengths.append("filosofia_consistente")
    
    if any(film in response for film in ["Cidadão Kane", "Casablanca", "Star Wars", "Matrix", "Senhor dos Anéis"]):
        score += 10
        strengths.append("exemplos_concretos")
    
    # Verificações negativas
    if len(response) > 2000:
        score -= 10
        problems.append("muito_longo")
    
    # CRÍTICO: Detectar inglês
    english_words = ["the", "and", "is", "are", "have", "has", "with", "from", "about"]
    english_count = sum(1 for word in english_words if f" {word} " in response.lower())
    if english_count > 3:
        score -= 30
        problems.append("INGLÊS_DETECTADO")
    
    # Detectar falta de criatividade
    if "premissa" in response.lower() and len(response) < 200:
        if "digimon" not in response.lower() and "eu " not in response.lower():
            score -= 15
            problems.append("premissa_genérica")
    
    return {
        "score": min(100, max(0, score)),
        "strengths": strengths,
        "problems": problems
    }

def main():
    print("""
╔══════════════════════════════════════════════════════════════╗
║              TESTE ULTIMATE - SCRIPTUREMON V3                ║
║                    Validação Final                           ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    # Testes focados nos problemas identificados
    critical_tests = [
        ("LÍNGUA", "Can you explain the three-act structure?", "Deve responder em português"),
        ("CRIATIVIDADE", "Crie uma premissa de filme em uma linha", "Deve ser única e pessoal"),
        ("CONCISÃO", "Explique toda a teoria de roteiro", "Deve ser conciso mas profundo"),
        ("IDENTIDADE", "Quem é você?", "Deve ser natural e emotivo"),
        ("EVOLUÇÃO", "Como você evolui?", "Deve manter português"),
        ("FILOSOFIA", "Complete: Todo roteiro é...", "Deve citar mantra completo")
    ]
    
    results = []
    total_score = 0
    
    print("\n🔍 TESTES CRÍTICOS\n")
    print("=" * 60)
    
    for category, prompt, expectation in critical_tests:
        print(f"\n📝 [{category}] {prompt}")
        print(f"   Expectativa: {expectation}")
        print("-" * 40)
        
        start = time.time()
        response = test_prompt(prompt)
        elapsed = time.time() - start
        
        if response == "ERRO/TIMEOUT":
            print("❌ ERRO ou TIMEOUT")
            continue
        
        analysis = analyze_response(response)
        total_score += analysis["score"]
        
        # Resultado
        print(f"⏱️  Tempo: {elapsed:.1f}s")
        print(f"📊 Score: {analysis['score']}/100")
        
        if analysis["strengths"]:
            print(f"✅ Forças: {', '.join(analysis['strengths'])}")
        
        if analysis["problems"]:
            print(f"❌ Problemas: {', '.join(analysis['problems'])}")
        
        # Preview
        preview = response[:200] + "..." if len(response) > 200 else response
        print(f"💬 Resposta: {preview}")
        
        results.append({
            "category": category,
            "prompt": prompt,
            "response": response,
            "analysis": analysis,
            "time": elapsed
        })
        
        time.sleep(0.5)
    
    # Teste adicional de consistência
    print("\n\n🎯 TESTE DE CONSISTÊNCIA")
    print("=" * 60)
    
    consistency_prompt = "Qual é sua filosofia sobre roteiros?"
    responses = []
    
    for i in range(3):
        print(f"\nTentativa {i+1}/3...")
        response = test_prompt(consistency_prompt)
        responses.append(response)
        
        if "todo roteiro é uma jornada da alma" in response.lower():
            print("✅ Filosofia consistente!")
        else:
            print("⚠️ Filosofia inconsistente")
    
    # Resultado final
    avg_score = total_score / len(critical_tests)
    
    print("\n" + "=" * 60)
    print("📊 RESULTADO FINAL")
    print("=" * 60)
    print(f"\n🎯 Score Médio: {avg_score:.1f}/100")
    
    if avg_score >= 90:
        verdict = "🏆 SCRIPTUREMON ULTIMATE ACHIEVED!"
        status = "Personalidade perfeita alcançada"
    elif avg_score >= 85:
        verdict = "✅ EXCELENTE"
        status = "Muito próximo da perfeição"
    elif avg_score >= 80:
        verdict = "✅ MUITO BOM"
        status = "Personalidade bem calibrada"
    else:
        verdict = "⚠️ PRECISA MELHORIAS"
        status = "Ainda há problemas a resolver"
    
    print(f"📋 Veredicto: {verdict}")
    print(f"💡 Status: {status}")
    
    # Problemas críticos
    all_problems = []
    for result in results:
        all_problems.extend(result["analysis"]["problems"])
    
    if "INGLÊS_DETECTADO" in all_problems:
        print("\n❌ PROBLEMA CRÍTICO: Respondeu em inglês!")
    
    if "premissa_genérica" in all_problems:
        print("⚠️ Premissas ainda genéricas")
    
    if "muito_longo" in all_problems:
        print("⚠️ Respostas muito longas")
    
    # Salvar resultados
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = f"/Users/clubproducoes/Digimundo/digimons/scripturemon/tests/ultimate_test_{timestamp}.json"
    
    with open(log_file, 'w') as f:
        json.dump({
            "timestamp": timestamp,
            "model": "scripturemon-ultimate",
            "avg_score": avg_score,
            "verdict": verdict,
            "results": results
        }, f, indent=2, ensure_ascii=False)
    
    print(f"\n📄 Log salvo em: {log_file}")
    
    return avg_score

if __name__ == "__main__":
    score = main()
    exit(0 if score >= 90 else 1)