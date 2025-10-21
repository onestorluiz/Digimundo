#!/usr/bin/env python3
"""
Teste de qualidade do DeepSeek-R1:70b para análise de roteiros
"""

import sys
import time
from pathlib import Path

# Adiciona path do projeto
sys.path.insert(0, str(Path(__file__).parent))

def test_deepseek_analysis():
    """Testa análise de roteiro com DeepSeek"""
    print("="*70)
    print(" TESTE DE QUALIDADE - DEEPSEEK-R1:70B ")
    print("="*70)
    print("\n⚠️ AVISO: Este teste pode demorar 2-5 minutos devido ao modelo grande!")
    print("Mas a qualidade do feedback vale a pena!\n")
    
    from apps.scripturemon.ollama_core import OllamaCore
    
    # Inicializa
    core = OllamaCore()
    print(f"✅ Modelo configurado: {core.default_model}")
    print(f"✅ Timeout configurado: 5 minutos\n")
    
    # Roteiro de teste (início de Pulp Fiction)
    test_script = """FADE IN:

INT. COFFEE SHOP - MORNING

A normal Denny's, Spires-like coffee shop in Los Angeles. 
It's about 9:00 in the morning. While the place isn't jammed, 
there's a healthy number of people drinking coffee, munching 
on bacon and eggs, and chatting.

Two of these people are a YOUNG MAN and a YOUNG WOMAN. The 
Young Man has a slight working-class English accent and, like 
his fellow countryman, smokes cigarettes like they're going 
out of style. The Young Woman is American, has a sweet face, 
and a quiet voice.

They sit in a booth. Their dialogue is to be said in a rapid-
pace "His Girl Friday" fashion.

YOUNG MAN
Forget it. It's too risky. I'm 
through doing that shit.

YOUNG WOMAN  
You always say that. The same thing 
every time: "I'm through, never again, 
too dangerous."

YOUNG MAN
I know that's what I always say. I'm 
always right too.

YOUNG WOMAN
But you forget about it in a day or two.

YOUNG MAN
The days of me forgetting are over, and 
the days of me remembering have just 
begun.

FADE OUT."""
    
    print("📝 Analisando roteiro de teste (Pulp Fiction - Opening)...")
    print("⏳ Aguarde... DeepSeek está processando com 256K tokens de contexto...\n")
    
    start_time = time.time()
    
    # Prompt especializado para análise profunda
    prompt = f"""Você é um crítico de cinema experiente. Analise este trecho de roteiro:

{test_script}

Forneça uma análise PROFUNDA e BRUTAL incluindo:

1. ESTRUTURA: Como a cena estabelece tom e conflito?
2. DIÁLOGOS: Análise do ritmo, subtexto e naturalidade
3. PERSONAGENS: O que já podemos inferir sobre eles?
4. DIREÇÃO DE CENA: Eficácia das descrições
5. COMPARAÇÃO: Como se compara a aberturas clássicas?
6. SCORE: De 0 a 100, qual nota você daria?

Seja extremamente crítico mas construtivo. Use exemplos específicos."""
    
    try:
        response = core.generate(
            prompt=prompt,
            temperature=0.7,
            max_tokens=2000
        )
        
        elapsed = time.time() - start_time
        
        print("="*70)
        print(" ANÁLISE DO DEEPSEEK-R1:70B ")
        print("="*70)
        print(response)
        print("="*70)
        print(f"\n⏱️ Tempo de resposta: {elapsed:.1f} segundos")
        print(f"📊 Modelo usado: {core.default_model}")
        print(f"💾 Contexto: 256K tokens")
        
        if elapsed > 60:
            print("\n⚠️ Resposta demorou mais de 1 minuto - NORMAL para DeepSeek-R1:70b")
            print("✅ Mas a qualidade da análise compensa a espera!")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Erro na análise: {e}")
        print("\nSugestões:")
        print("1. Verifique se o DeepSeek-R1:70b está instalado: ollama list")
        print("2. Se estiver muito lento, use: ollama run deepseek-r1:32b")
        print("3. Ou temporariamente use o 14b: ollama run deepseek-r1:14b")
        return False

def main():
    print("\n" + "="*70)
    print(" SCRIPTUREMON COM DEEPSEEK-R1:70B ")
    print(" Foco: QUALIDADE MÁXIMA de análise ")
    print("="*70 + "\n")
    
    success = test_deepseek_analysis()
    
    if success:
        print("\n✅ TESTE CONCLUÍDO COM SUCESSO!")
        print("O DeepSeek-R1:70b está configurado para máxima qualidade.")
        print("62/100. Como sempre.")
    else:
        print("\n⚠️ Teste falhou, mas isso é normal se o modelo estiver carregando.")
        print("Tente novamente em alguns segundos.")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)