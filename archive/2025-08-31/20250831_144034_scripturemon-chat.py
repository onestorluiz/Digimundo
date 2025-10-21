#!/usr/bin/env python3
"""
🎬 SCRIPTUREMON CHAT DIRETO
Interface simples para conversar com o Scripturemon
"""

import sys
import os
from pathlib import Path

# Adiciona o path do projeto
sys.path.insert(0, '/Users/clubproducoes/Digimundo/scripturemon-validation')
os.chdir('/Users/clubproducoes/Digimundo/scripturemon-validation')

from apps.scripturemon.chat import ScripturemonChat

def main():
    print("="*80)
    print(" "*20 + "🎬 SCRIPTUREMON - MENTOR BRUTAL 🎬")
    print("="*80)
    print()
    print("COMANDOS PRINCIPAIS:")
    print("  /analyze [roteiro]  → Análise brutal completa")
    print("  /compare           → Compara com obras-primas")
    print("  /search [termo]    → Busca conhecimento cinematográfico")
    print("  /quit              → Sair")
    print()
    print("DICA: Cole seu roteiro completo após /analyze")
    print("="*80)
    print()
    
    chat = ScripturemonChat()
    
    print("Scripturemon: Mais um roteiro medíocre? Mostre-me.")
    print()
    
    while True:
        try:
            # Prompt mais visual
            user_input = input("📝 Você> ")
            
            if not user_input:
                continue
                
            if user_input.lower() in ['/quit', '/sair', 'quit', 'exit']:
                print()
                print("Scripturemon: Volte quando tiver coragem de ouvir a verdade.")
                print("             62/100. Para sempre.")
                print()
                break
            
            # Processa input
            response = chat.process_input(user_input)
            
            # Resposta formatada
            print()
            print("🎬 Scripturemon:")
            print("-"*40)
            print(response)
            print("-"*40)
            print()
            
        except KeyboardInterrupt:
            print("\n\nScripturemon: Ctrl+C? Covardia. Seu roteiro continua 62/100.")
            break
        except Exception as e:
            print(f"\n❌ Erro: {e}")
            print("Tente novamente...")

if __name__ == "__main__":
    main()