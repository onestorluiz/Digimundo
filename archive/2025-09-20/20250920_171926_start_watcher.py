#!/usr/bin/env python3
"""
Ativa o watcher para processar PDFs automaticamente
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.watchers.folder_watcher import main

if __name__ == "__main__":
    print("\n🎬 SCRIPTUREMON RAG - Watcher Automático")
    print("=" * 50)
    print("\n📁 Monitorando pastas para novos PDFs:")
    print("   - cinema/1_teoria_roteiro/")
    print("   - cinema/2_roteiros_mestres/")
    print("   - cinema/3_roteiros_criador/")
    print("\n⚡ PDFs serão processados automaticamente quando adicionados")
    print("   Pressione CTRL+C para parar\n")
    print("=" * 50)
    
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n✋ Watcher parado pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro: {e}")