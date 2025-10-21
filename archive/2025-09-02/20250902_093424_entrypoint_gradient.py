#!/usr/bin/env python3
"""
🧠 ENTRYPOINT COM GRADIENT - Cérebro Central de 256k tokens
"""

import sys
import os
from pathlib import Path

# Adiciona paths necessários
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

def main():
    """Ponto de entrada principal com Gradient configurado"""
    
    print("🧠 SCRIPTUREMON COM GRADIENT (256K TOKENS)")
    print("=" * 60)
    
    # Importa após configurar paths
    from apps.scripturemon.chat import ScripturemonChat
    from apps.scripturemon.ollama_core import get_ollama
    
    # Verifica se Gradient está disponível
    ollama = get_ollama()
    
    if 'gradient' in ollama.default_model.lower():
        print(f"✅ Modelo: {ollama.default_model}")
        print(f"✅ Contexto: 256.000 tokens")
        print(f"✅ Capacidade: 15+ PDFs simultâneos")
    else:
        print(f"⚠️ Modelo padrão: {ollama.default_model}")
        print("Gradient não está como prioridade!")
    
    print("=" * 60)
    print()
    
    # Inicia chat
    try:
        chat = ScripturemonChat()
        
        # Configura para usar Gradient
        if hasattr(chat, 'brain') and hasattr(chat.brain, 'default_model'):
            chat.brain.default_model = 'scripturemon-gradient'
            chat.brain.default_context = 256000
            
        chat.start_interactive()
        
    except KeyboardInterrupt:
        print("\n\n👋 Até logo!")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()