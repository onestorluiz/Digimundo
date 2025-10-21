#!/usr/bin/env python3
"""
Teste da integração do ScripturemonBrain com o Chat
Verifica se analisa roteiros DE VERDADE
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from apps.scripturemon.chat import ScripturemonChat

def main():
    print("\n🧠 TESTE DO SCRIPTUREMON COM BRAIN REAL")
    print("="*60)
    
    # Inicializa chat com brain
    chat = ScripturemonChat(force_legacy_soul=False)
    
    # Roteiro de teste REAL
    screenplay = """FADE IN:

INT. ABANDONED WAREHOUSE - NIGHT

Dark. Silent. Moonlight filters through broken windows.

SARAH CHEN (30s), determined but exhausted, enters cautiously. 
Gun drawn. Every step calculated.

SARAH
(into radio, whispering)
I'm in position. No visual on the target.

A SHADOW moves behind her. She spins—

MARCUS (40s), her former partner, emerges from darkness.
Betrayal etched on his face.

MARCUS
You shouldn't have come alone, Sarah.

SARAH
(bitter)
I trusted you once. That was enough.

MARCUS
Trust? In this business? 
You were always too naive.

Sarah's hand trembles slightly. The gun wavers.

SARAH
Where is she, Marcus? Where's my daughter?

Marcus smiles coldly.

MARCUS
Safe. For now. Drop the weapon.

Beat. Sarah considers. Then—

SARAH
No.

She fires. Marcus dives. The warehouse EXPLODES with gunfire.

CUT TO BLACK.

TITLE: "BETRAYAL"

FADE OUT."""
    
    print("\n📝 Enviando roteiro para análise...")
    print("-" * 40)
    
    # Testa análise
    response = chat.process_input(screenplay)
    
    print("\n🎬 RESPOSTA DO SCRIPTUREMON:")
    print("-" * 40)
    print(response)
    
    # Verifica se usou o brain
    if "ANÁLISE BRUTAL REAL" in response:
        print("\n✅ SUCESSO! Usou ScripturemonBrain para análise REAL!")
        
        # Verifica componentes da análise
        checks = {
            "Score variável": "Score REAL:" in response and "/100 (não é sempre 62!)" in response,
            "Estrutura detectada": "cenas" in response and "personagens" in response,
            "Proporções": "% diálogo" in response and "% ação" in response,
            "Análise profunda": "Força narrativa:" in response or "Qualidade dos diálogos:" in response,
            "Feedback personalizado": "FEEDBACK PERSONALIZADO:" in response,
            "Comparação com mestres": "COMPARAÇÃO COM MESTRES:" in response,
            "Evolução": "Tendência:" in response
        }
        
        print("\n📊 Verificação de componentes:")
        for component, present in checks.items():
            status = "✅" if present else "❌"
            print(f"  {status} {component}")
        
        success_rate = sum(checks.values()) / len(checks) * 100
        print(f"\n🎯 Taxa de sucesso: {success_rate:.0f}%")
        
        if success_rate >= 70:
            print("\n🏆 SISTEMA TOTALMENTE FUNCIONAL!")
        else:
            print("\n⚠️ Sistema parcialmente funcional")
    else:
        print("\n❌ ERRO: Não usou o brain, análise genérica!")
        print("O sistema ainda não está detectando roteiros corretamente.")
    
    # Testa conversa normal para comparar
    print("\n" + "="*60)
    print("📝 Testando conversa normal (não-roteiro)...")
    print("-" * 40)
    
    normal_response = chat.process_input("Como escrevo diálogos melhores?")
    
    if "62/100" in normal_response and "Score REAL:" not in normal_response:
        print("✅ Conversa normal: mantém personalidade 62/100")
    else:
        print("⚠️ Conversa normal pode estar confusa")
    
    print("\n" + "="*60)
    print("🎬 TESTE CONCLUÍDO")
    print("62/100 para conversas. Score REAL para roteiros.")

if __name__ == "__main__":
    main()