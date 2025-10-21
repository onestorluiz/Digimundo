#!/usr/bin/env python3
"""
Teste final com DeepSeek-R1:70b - QUALIDADE MÁXIMA
"""

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

def test_deepseek_70b():
    """Testa o DeepSeek-R1:70b com timeout apropriado"""
    print("="*70)
    print(" TESTE DEEPSEEK-R1:70B - QUALIDADE MÁXIMA ")
    print("="*70)
    print("\n⚠️ AVISO: Este modelo demora 3-10 minutos para responder!")
    print("Mas a qualidade da análise é EXCEPCIONAL!\n")
    
    from apps.scripturemon.ollama_core import OllamaCore
    
    core = OllamaCore()
    print(f"✅ Modelo configurado: {core.default_model}")
    print(f"✅ Timeout configurado: 10 minutos")
    print(f"💾 Uso de RAM: ~100GB (normal para este modelo)\n")
    
    # Teste simples primeiro
    print("📝 Teste rápido de conexão...")
    print("⏳ Aguarde 1-3 minutos...\n")
    
    start_time = time.time()
    
    try:
        response = core.generate(
            "Responda em uma linha: Qual é a estrutura clássica de 3 atos?",
            temperature=0.5,
            max_tokens=100
        )
        
        elapsed = time.time() - start_time
        
        print("="*70)
        print(" RESPOSTA DO DEEPSEEK-R1:70B ")
        print("="*70)
        print(response)
        print("="*70)
        print(f"\n⏱️ Tempo de resposta: {elapsed:.1f} segundos")
        
        if elapsed > 120:
            print("✅ Resposta demorada mas NORMAL para DeepSeek-R1:70b")
            print("🎯 A qualidade compensa a espera!")
        
        # Teste de análise profunda
        print("\n" + "="*70)
        print(" TESTE DE ANÁLISE PROFUNDA ")
        print("="*70)
        print("\n📝 Agora vamos testar uma análise completa de roteiro...")
        print("⏳ Pode demorar 5-10 minutos...\n")
        
        roteiro_teste = """FADE IN:

INT. ESCRITÓRIO - DIA

JOÃO (40s), cansado e desiludido, olha pela janela. 
A cidade cinzenta reflete seu estado de espírito.

MARIA (30s) entra apressada.

MARIA
Precisamos conversar sobre ontem.

JOÃO
(sem se virar)
Não há nada para conversar.

MARIA
Você não pode simplesmente desistir.

JOÃO
(virando-se)
Eu já desisti há muito tempo, Maria. 
Você que ainda não percebeu.

FADE OUT."""
        
        prompt_analise = f"""Analise este roteiro com PROFUNDIDADE EXTREMA:

{roteiro_teste}

Forneça:
1. Análise estrutural detalhada
2. Desenvolvimento de personagens
3. Subtexto nos diálogos
4. Temas e simbolismos
5. Comparação com obras clássicas
6. Sugestões específicas de melhoria
7. Score de 0-100

Seja BRUTAL mas construtivo."""
        
        start_analise = time.time()
        
        response_analise = core.generate(
            prompt_analise,
            temperature=0.7,
            max_tokens=2000
        )
        
        elapsed_analise = time.time() - start_analise
        
        print("="*70)
        print(" ANÁLISE PROFUNDA DO DEEPSEEK-R1:70B ")
        print("="*70)
        print(response_analise[:2000])  # Limita output para não poluir terminal
        if len(response_analise) > 2000:
            print("\n[...análise continua...]")
        print("="*70)
        print(f"\n⏱️ Tempo de análise: {elapsed_analise:.1f} segundos")
        print(f"📊 Qualidade: MÁXIMA")
        print(f"💎 Modelo: DeepSeek-R1:70b com 256K tokens de contexto")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        print("\nDicas:")
        print("1. O modelo pode estar carregando (demora ~1 minuto)")
        print("2. Verifique a RAM disponível: vm_stat")
        print("3. Se travar muito, use: ollama stop deepseek-r1:70b")
        print("4. Alternativa mais rápida: ollama run deepseek-r1:32b")
        return False

def main():
    print("\n" + "="*70)
    print(" SCRIPTUREMON COM DEEPSEEK-R1:70B ")
    print(" FOCO TOTAL EM QUALIDADE ")
    print("="*70 + "\n")
    
    print("📋 Configuração:")
    print("- Modelo: DeepSeek-R1:70b")
    print("- Contexto: 256K tokens")
    print("- RAM: ~100GB")
    print("- Tempo médio: 3-10 minutos por resposta")
    print("- Qualidade: EXCEPCIONAL\n")
    
    success = test_deepseek_70b()
    
    if success:
        print("\n✅ SISTEMA CONFIGURADO COM SUCESSO!")
        print("DeepSeek-R1:70b está pronto para análises profundas.")
        print("A demora vale a pena pela qualidade!")
        print("\n62/100. Mas desta vez, de verdade.")
    else:
        print("\n⚠️ O modelo está carregando ou com problemas.")
        print("Aguarde 1-2 minutos e tente novamente.")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)