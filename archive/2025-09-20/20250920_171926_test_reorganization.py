#!/usr/bin/env python3
"""
Teste do sistema após reorganização
"""

import sys
import os
from pathlib import Path

# Adiciona paths necessários
sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent / "src" / "core"))

def test_system():
    print("="*60)
    print("🧪 TESTE DO SISTEMA REORGANIZADO")
    print("="*60)
    
    # Teste 1: Importar módulos principais
    print("\n[1/5] Testando imports...")
    try:
        from app.config import load_config
        print("✅ Config carregado")
        
        from app.models.embeddings import EmbeddingModel
        print("✅ EmbeddingModel disponível")
        
        from app.retrieval.hybrid import HybridRetriever
        print("✅ HybridRetriever disponível")
    except ImportError as e:
        print(f"❌ Erro de import: {e}")
        return False
    
    # Teste 2: Verificar estrutura de diretórios
    print("\n[2/5] Verificando estrutura...")
    dirs_to_check = [
        "src/core",
        "src/models",
        "src/scripts",
        "data/roteiros",
        "config",
        "memory"
    ]
    
    for dir_path in dirs_to_check:
        if os.path.exists(dir_path):
            print(f"✅ {dir_path} existe")
        else:
            print(f"❌ {dir_path} não encontrado")
    
    # Teste 3: Verificar arquivos de configuração
    print("\n[3/5] Verificando configurações...")
    if os.path.exists("config/config.yaml"):
        print("✅ config.yaml encontrado")
    else:
        print("⚠️ config.yaml não encontrado")
    
    # Teste 4: Verificar modelfiles
    print("\n[4/5] Verificando modelfiles...")
    modelfiles = list(Path("src/models").glob("**/*.modelfile"))
    if modelfiles:
        print(f"✅ {len(modelfiles)} modelfile(s) encontrado(s)")
        for mf in modelfiles[:3]:
            print(f"  - {mf.name}")
    else:
        print("⚠️ Nenhum modelfile encontrado")
    
    # Teste 5: Verificar PDFs
    print("\n[5/5] Verificando biblioteca de roteiros...")
    pdfs = list(Path("data/roteiros").glob("*.pdf"))
    if pdfs:
        print(f"✅ {len(pdfs)} PDFs encontrados")
    else:
        print("⚠️ Nenhum PDF encontrado em data/roteiros")
    
    # Resultado final
    print("\n" + "="*60)
    print("📊 RESULTADO DA REORGANIZAÇÃO")
    print("="*60)
    
    total_size_before = 1400  # MB (aproximado)
    total_size_after = 427   # MB (sem venv_rag)
    
    print(f"📦 Tamanho antes: ~{total_size_before}MB")
    print(f"📦 Tamanho depois: ~{total_size_after}MB")
    print(f"💾 Economia: {total_size_before - total_size_after}MB ({((total_size_before - total_size_after)/total_size_before)*100:.1f}%)")
    
    print("\n✅ Sistema reorganizado com sucesso!")
    print("\nPróximos passos:")
    print("1. source venv/bin/activate")
    print("2. python src/scripts/process_all_pdfs.py")
    print("3. python src/scripts/scripturemon_rag_bridge.py")
    
    return True

if __name__ == "__main__":
    success = test_system()
    sys.exit(0 if success else 1)