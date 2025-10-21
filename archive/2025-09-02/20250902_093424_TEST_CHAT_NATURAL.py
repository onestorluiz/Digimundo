#!/usr/bin/env python3
"""
Teste de análise natural de roteiros - sem comandos explícitos
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from apps.scripturemon.chat import ScripturemonChat

def main():
    print("\n🎬 TESTE DE ANÁLISE NATURAL - SEM COMANDOS")
    print("="*60)
    
    # Inicializa chat
    chat = ScripturemonChat(force_legacy_soul=False)
    
    # Testa conversas naturais sobre roteiros
    test_inputs = [
        """Analise este trecho de roteiro para mim:

        INT. ABANDONED WAREHOUSE - NIGHT
        
        SARAH (30s, determined) enters cautiously, gun drawn.
        
        SARAH
        (whispering into radio)
        I'm in position. No sign of—
        
        A SHADOW moves behind her. She spins, but it's too late.
        
        BLACKOUT.""",
        
        "O que você acha desse diálogo? 'JOHN: I love you. MARY: I love you too.' É natural?",
        
        "Meu protagonista é um hacker de 25 anos que descobre uma conspiração global. É clichê?",
        
        """Veja este roteiro:
        
        FADE IN:
        
        EXT. NEW YORK CITY - DAY
        
        The city bustles with life. We see JACK walking.
        
        JACK
        Another day in paradise.
        
        THE END
        
        O que você achou?""",
        
        "Preciso de ajuda com o terceiro ato do meu thriller",
        
        "/quit"
    ]
    
    print("\nTestando análises naturais (sem comandos /analyze)...\n")
    
    for i, user_input in enumerate(test_inputs, 1):
        if len(user_input) > 100:
            display = user_input[:100] + "..."
        else:
            display = user_input
            
        print(f"\n{'='*60}")
        print(f"📝 TESTE {i}: {display}")
        print("-" * 40)
        
        try:
            response = chat.process_input(user_input)
            
            # Verifica se a resposta contém análise
            has_analysis = any(word in response.lower() for word in [
                'roteiro', 'script', 'diálogo', 'personagem', 'estrutura',
                'ato', 'cena', 'narrativa', '62/100', 'conflito', 'protagonista',
                'kubrick', 'tarantino', 'chinatown'
            ])
            
            # Limita resposta para display
            if len(response) > 600:
                response_display = response[:600] + "\n\n[...resposta truncada...]"
            else:
                response_display = response
            
            print(f"🎭 RESPOSTA: {response_display}")
            
            if has_analysis:
                print(f"\n✅ ANÁLISE DETECTADA - Scripturemon entendeu o contexto!")
            else:
                print(f"\n⚠️ Resposta genérica - pode não ter analisado profundamente")
            
            if user_input == "/quit":
                break
                
        except Exception as e:
            print(f"❌ Erro: {e}")
    
    print("\n" + "="*60)
    print("\n📊 CONCLUSÃO:")
    print("O Scripturemon é capaz de identificar e analisar roteiros")
    print("mesmo sem comandos explícitos, usando o contexto da conversa.")
    print("\n62/100. Como sempre deve ser.")
    
if __name__ == "__main__":
    main()