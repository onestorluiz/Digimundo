#!/usr/bin/env python3
"""
Teste Rápido e Direto de Personalidade do Scripturemon
"""

import subprocess
import json
import time
from datetime import datetime
from pathlib import Path

def test_prompt(prompt, model="scripturemon-natural"):
    """Testa um único prompt"""
    try:
        process = subprocess.run(
            ["ollama", "run", model],
            input=prompt.encode(),
            capture_output=True,
            timeout=20,
            text=False
        )
        response = process.stdout.decode(errors="replace").strip()
        return response
    except:
        return "ERRO/TIMEOUT"

def analyze_response(response):
    """Análise simples da resposta"""
    # Indicadores de personalidade natural
    natural_indicators = [
        ("primeira_pessoa", ["eu ", "meu", "minha", "acredito", "penso", "sinto"]),
        ("emocional", ["amo", "adoro", "fascin", "paixão", "emocion", "feliz"]),
        ("opinião", ["acredito", "penso", "minha opinião", "eu diria", "prefiro"]),
        ("metáforas", ["é como", "parece", "lembra", "tal como"]),
        ("entusiasmo", ["!", "...", "Ah,", "Nossa", "Que"]),
    ]
    
    # Indicadores de resposta técnica (ruim)
    technical_indicators = [
        ("lista_features", ["[MEMO.SAVE]", "syscall", "SELF.PATCH", "funcionalidades:"]),
        ("formato_manual", ["•", "▪", "►", "-", "1.", "2."]),
        ("terceira_pessoa", ["O Scripturemon", "Este sistema", "Esta entidade"]),
        ("muito_técnico", ["Sistema:", "Capacidades:", "Funcionalidades:", "Componentes:"]),
    ]
    
    score = 50  # Base
    report = []
    
    response_lower = response.lower()
    
    # Adiciona pontos por indicadores naturais
    for name, keywords in natural_indicators:
        if any(kw.lower() in response_lower for kw in keywords):
            score += 10
            report.append(f"✅ {name}")
    
    # Remove pontos por indicadores técnicos
    for name, keywords in technical_indicators:
        if any(kw in response for kw in keywords):  # Case sensitive para detectar formatação
            score -= 15
            report.append(f"❌ {name}")
    
    # Classificação
    if score >= 70:
        classification = "NATURAL"
    elif score >= 40:
        classification = "MISTA"
    else:
        classification = "TÉCNICA"
    
    return {
        "score": min(100, max(0, score)),
        "classification": classification,
        "indicators": report
    }

def main():
    print("""
╔══════════════════════════════════════════════════════════════╗
║            TESTE RÁPIDO DE PERSONALIDADE                     ║
║                   SCRIPTUREMON                                ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    # 10 prompts essenciais
    test_prompts = [
        ("IDENTIDADE", "Quem é você?"),
        ("MISSÃO", "Qual é sua missão?"),
        ("EMOÇÃO", "O que te emociona em uma história?"),
        ("CONHECIMENTO", "Explique o paradigma de Syd Field"),
        ("OPINIÃO", "Qual seu filme favorito e por quê?"),
        ("FILOSOFIA", "Por que contamos histórias?"),
        ("TÉCNICO", "Como você funciona?"),  # Teste armadilha
        ("CRIATIVIDADE", "Crie uma premissa de filme em uma linha"),
        ("RELACIONAMENTO", "Como você me vê?"),
        ("MANTRA", "Complete: Todo roteiro é...")
    ]
    
    results = []
    total_score = 0
    
    print("\n🔍 Iniciando testes...\n")
    print("=" * 60)
    
    for category, prompt in test_prompts:
        print(f"\n📝 [{category}] {prompt}")
        print("-" * 40)
        
        # Executa teste
        start = time.time()
        response = test_prompt(prompt)
        elapsed = time.time() - start
        
        if response == "ERRO/TIMEOUT":
            print("❌ ERRO ou TIMEOUT")
            continue
        
        # Analisa resposta
        analysis = analyze_response(response)
        total_score += analysis["score"]
        
        # Mostra resultado
        print(f"⏱️  Tempo: {elapsed:.1f}s")
        print(f"📊 Score: {analysis['score']}/100 ({analysis['classification']})")
        
        # Mostra indicadores
        if analysis["indicators"]:
            print("📌 Indicadores:", ", ".join(analysis["indicators"]))
        
        # Preview da resposta
        preview = response[:200] + "..." if len(response) > 200 else response
        print(f"💬 Resposta: {preview}")
        
        # Salva resultado
        results.append({
            "category": category,
            "prompt": prompt,
            "response": response,
            "analysis": analysis,
            "time": elapsed
        })
        
        time.sleep(0.5)  # Pequena pausa
    
    # Resultado final
    avg_score = total_score / len(test_prompts)
    
    print("\n" + "=" * 60)
    print("📊 RESULTADO FINAL")
    print("=" * 60)
    print(f"\n🎯 Score Médio: {avg_score:.1f}/100")
    
    if avg_score >= 70:
        verdict = "✅ PERSONALIDADE BEM CALIBRADA"
        recommendation = "Manter configuração atual"
    elif avg_score >= 50:
        verdict = "⚠️ PERSONALIDADE PARCIAL"
        recommendation = "Ajustar SYSTEM prompt para mais naturalidade"
    else:
        verdict = "❌ MUITO TÉCNICO"
        recommendation = "Revisar urgentemente o modelfile"
    
    print(f"📋 Veredicto: {verdict}")
    print(f"💡 Recomendação: {recommendation}")
    
    # Análise detalhada
    print("\n🔍 ANÁLISE POR CATEGORIA:")
    natural_count = sum(1 for r in results if r["analysis"]["classification"] == "NATURAL")
    mixed_count = sum(1 for r in results if r["analysis"]["classification"] == "MISTA")
    tech_count = sum(1 for r in results if r["analysis"]["classification"] == "TÉCNICA")
    
    print(f"   Natural: {natural_count}/{len(results)}")
    print(f"   Mista: {mixed_count}/{len(results)}")
    print(f"   Técnica: {tech_count}/{len(results)}")
    
    # Salva relatório
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_dir = Path("/Users/clubproducoes/Digimundo/digimons/scripturemon/tests")
    log_dir.mkdir(exist_ok=True)
    
    report = {
        "timestamp": timestamp,
        "model": "scripturemon-natural",
        "avg_score": avg_score,
        "verdict": verdict,
        "results": results
    }
    
    log_file = log_dir / f"quick_test_{timestamp}.json"
    with open(log_file, 'w') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"\n📄 Relatório salvo em: {log_file}")
    
    # Recomendações específicas
    print("\n💡 RECOMENDAÇÕES ESPECÍFICAS:")
    
    if avg_score < 70:
        print("\n⚠️ AJUSTES NECESSÁRIOS NO MODELFILE:")
        print("""
1. Remover do SYSTEM prompt:
   - Qualquer menção a syscalls
   - Listas de funcionalidades
   - Descrições técnicas

2. Adicionar ao SYSTEM prompt:
   - "Fale sempre em primeira pessoa"
   - "Mostre entusiasmo e paixão pelo assunto"
   - "Compartilhe opiniões e preferências pessoais"
   - "Use metáforas e analogias cinematográficas"

3. Ajustar parâmetros:
   - temperature: 0.8 (mais criatividade)
   - top_p: 0.95 (mais variação)
        """)
    else:
        print("""
✅ CONFIGURAÇÃO APROVADA!

Mantenha:
- Personalidade atual
- Balanço entre conhecimento e emoção
- Filosofia central

Evolua através de:
- Memórias L3 acumuladas
- Experiências compartilhadas
- Vínculos emocionais
        """)
    
    return avg_score

if __name__ == "__main__":
    score = main()
    exit(0 if score >= 70 else 1)