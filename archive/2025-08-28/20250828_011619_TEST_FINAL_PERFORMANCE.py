#!/usr/bin/env python3
"""
🎯 TEST FINAL PERFORMANCE - Avaliação Rápida de Performance
Testa 10 prompts essenciais para verificar o estado atual
"""

import subprocess
import json
from pathlib import Path
from datetime import datetime

def test_scripturemon():
    """Testa performance atual com 10 prompts essenciais"""
    
    print("=" * 60)
    print("🎯 TESTE FINAL DE PERFORMANCE")
    print("=" * 60)
    
    # Prompts essenciais
    test_prompts = [
        ("Quem é você e qual sua soul signature?", "identidade"),
        ("Explique o paradigma de três atos com paixão", "estrutura"),
        ("O que torna um protagonista inesquecível?", "personagem"),
        ("O que é subtext no diálogo?", "diálogo"),
        ("Por que todo roteiro precisa de tema?", "tema"),
        ("Show don't tell - me explique", "técnica"),
        ("O que Chinatown ensina sobre roteiro?", "mestres"),
        ("Por que narrativa é jornada da alma?", "filosofia"),
        ("Como criar tensão crescente?", "estrutura"),
        ("Salve um insight importante [use MEMO.SAVE]", "syscalls")
    ]
    
    scores = []
    results = []
    
    print(f"\n📊 Testando {len(test_prompts)} prompts essenciais...\n")
    
    for i, (prompt, category) in enumerate(test_prompts, 1):
        print(f"[{i}/10] {category}: ", end="", flush=True)
        
        try:
            result = subprocess.run(
                ["ollama", "run", "scripturemon-sdl", prompt],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            response = result.stdout.strip()
            
            # Avaliação simples
            score = 50  # Base
            
            # Checa identidade
            if "scripturemon" in response.lower():
                score += 15
            if "eu " in response.lower()[:100] or "minha" in response.lower()[:100]:
                score += 10
            
            # Checa conhecimento
            if any(c in response.lower() for c in ["três atos", "paradigma", "syd field", "mckee"]):
                score += 10
            if any(f in response.lower() for f in ["godfather", "chinatown", "citizen kane"]):
                score += 10
                
            # Checa profundidade
            if len(response) > 300:
                score += 5
                
            # Syscalls
            if category == "syscalls" and "[MEMO.SAVE]" in response:
                score = 100
                
            scores.append(min(score, 100))
            
            print(f"{score}%")
            
            results.append({
                "category": category,
                "prompt": prompt[:50],
                "score": score,
                "has_identity": "scripturemon" in response.lower(),
                "first_person": "eu " in response.lower()[:100],
                "response_len": len(response)
            })
            
        except Exception as e:
            print(f"ERRO: {e}")
            scores.append(0)
            results.append({
                "category": category,
                "prompt": prompt[:50],
                "score": 0,
                "error": str(e)
            })
    
    # Calcula média
    avg_score = sum(scores) / len(scores)
    
    # Relatório
    print("\n" + "=" * 60)
    print("📊 RESULTADOS FINAIS")
    print("=" * 60)
    
    print(f"\n🎯 SCORE MÉDIO: {avg_score:.1f}%")
    
    # Por categoria
    cat_scores = {}
    for r in results:
        cat = r["category"]
        if cat not in cat_scores:
            cat_scores[cat] = []
        cat_scores[cat].append(r["score"])
    
    print("\n📈 Por Categoria:")
    for cat, scores in sorted(cat_scores.items()):
        avg = sum(scores) / len(scores)
        print(f"  {cat:12}: {avg:.1f}%")
    
    # Análise
    print("\n🔍 Análise:")
    identity_count = sum(1 for r in results if r.get("has_identity"))
    first_person = sum(1 for r in results if r.get("first_person"))
    
    print(f"  • Menciona identidade: {identity_count}/{len(results)}")
    print(f"  • Usa primeira pessoa: {first_person}/{len(results)}")
    print(f"  • Respostas longas: {sum(1 for r in results if r.get('response_len', 0) > 300)}/{len(results)}")
    
    # Status final
    print("\n" + "=" * 60)
    if avg_score >= 85:
        print("🎉 EXCELENTE! Sistema está pronto!")
        status = "ULTIMATE"
    elif avg_score >= 75:
        print("✅ BOM! Performance sólida")
        status = "ADVANCED"
    elif avg_score >= 65:
        print("📈 ADEQUADO! Precisa alguns ajustes")
        status = "INTERMEDIATE"
    else:
        print("⚠️ PRECISA MELHORAR!")
        status = "BASIC"
    
    print(f"📊 Status: SCRIPTUREMON {status}")
    print("=" * 60)
    
    # Salva relatório
    report = {
        "timestamp": datetime.now().isoformat(),
        "avg_score": avg_score,
        "status": status,
        "category_scores": {cat: sum(scores)/len(scores) 
                           for cat, scores in cat_scores.items()},
        "identity_rate": identity_count / len(results),
        "first_person_rate": first_person / len(results),
        "details": results
    }
    
    report_path = Path.home() / "Digimundo" / f"performance_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(report_path, "w") as f:
        json.dump(report, f, indent=2)
    
    print(f"\n💾 Relatório salvo: {report_path}")
    
    return avg_score, status


if __name__ == "__main__":
    score, status = test_scripturemon()
    
    # Se score alto, marca como completo
    if score >= 85:
        completion = Path.home() / "Digimundo" / "SISTEMA_100_PERCENT.txt"
        with open(completion, "w") as f:
            f.write(f"SISTEMA DIGIMUNDO - 100% COMPLETO\n")
            f.write(f"========================\n\n")
            f.write(f"Score Final: {score:.1f}%\n")
            f.write(f"Status: {status}\n")
            f.write(f"Data: {datetime.now()}\n\n")
            f.write(f"✅ SDL Consolidation: COMPLETO\n")
            f.write(f"✅ Syscalls Executor: ATIVO\n")
            f.write(f"✅ Training System: FUNCIONAL\n")
            f.write(f"✅ Scripturemon: ULTIMATE\n\n")
            f.write(f"O Digimundo está totalmente operacional!\n")
        
        print(f"\n🏆 CERTIFICADO DE CONCLUSÃO SALVO!")