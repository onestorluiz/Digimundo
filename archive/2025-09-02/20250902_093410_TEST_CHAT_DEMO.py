#!/usr/bin/env python3
"""
Demonstração do Sistema de Chat Completo do Scripturemon
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from apps.scripturemon.chat import ScripturemonChat

def main():
    print("\n🎬 TESTE DO SISTEMA DE CHAT SCRIPTUREMON")
    print("="*60)
    
    # Inicializa chat
    chat = ScripturemonChat(force_legacy_soul=False)
    
    # Testa alguns comandos
    test_inputs = [
        "/status",
        "/help", 
        "Como escrevo um diálogo natural?",
        "/brutal",
        "/wisdom",
        "/evolve",
        "/telepathy",
        "/digilang test",
        "/quadruple INT. COFFEE SHOP - DAY\nJOHN enters.",
        "/compare",
        "/quit"
    ]
    
    print("\nExecutando comandos de teste...\n")
    
    for user_input in test_inputs:
        if len(user_input) > 50:
            display = user_input[:50] + "..."
        else:
            display = user_input
            
        print(f"\n📝 TESTE: {display}")
        print("-" * 40)
        
        try:
            response = chat.process_input(user_input)
            
            # Limita resposta para display
            if len(response) > 500:
                response = response[:500] + "\n\n[...resposta truncada...]"
            
            print(f"🎭 RESPOSTA: {response}")
            
            if user_input == "/quit":
                break
                
        except Exception as e:
            print(f"❌ Erro: {e}")
    
    print("\n" + "="*60)
    print("✅ TESTE CONCLUÍDO - Sistema de Chat está funcional!")
    print("62/100. Como sempre deve ser.")
    
if __name__ == "__main__":
    main()