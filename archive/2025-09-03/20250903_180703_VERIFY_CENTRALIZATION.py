#!/usr/bin/env python3
"""
VERIFICAÇÃO DE CENTRALIZAÇÃO - Scripturemon Validation
Verifica se todos os componentes estão centralizados e funcionais
"""

import os
import sys
import importlib.util
from pathlib import Path

def check_file(filepath, description):
    """Verifica se arquivo existe"""
    if Path(filepath).exists():
        size = Path(filepath).stat().st_size
        print(f"✅ {description}: {filepath} ({size:,} bytes)")
        return True
    else:
        print(f"❌ {description}: {filepath} NÃO ENCONTRADO")
        return False

def check_directory(dirpath, description, min_files=1):
    """Verifica se diretório existe e tem conteúdo"""
    if Path(dirpath).exists() and Path(dirpath).is_dir():
        files = list(Path(dirpath).rglob("*"))
        print(f"✅ {description}: {dirpath} ({len(files)} arquivos)")
        return len(files) >= min_files
    else:
        print(f"❌ {description}: {dirpath} NÃO ENCONTRADO ou vazio")
        return False

def check_import(module_name):
    """Verifica se módulo pode ser importado"""
    try:
        spec = importlib.util.find_spec(module_name)
        if spec:
            print(f"✅ Import {module_name}: OK")
            return True
    except:
        pass
    print(f"❌ Import {module_name}: FALHOU")
    return False

def main():
    print("=" * 80)
    print("VERIFICAÇÃO DE CENTRALIZAÇÃO - SCRIPTUREMON VALIDATION")
    print("=" * 80)
    
    base_path = Path("/Users/clubproducoes/Digimundo/scripturemon-validation")
    os.chdir(base_path)
    
    all_ok = True
    
    # 1. ARQUIVOS PRINCIPAIS
    print("\n📄 ARQUIVOS PRINCIPAIS:")
    main_files = [
        ("SCRIPTUREMON_ULTIMATE_SYMBIOTIC.py", "Sistema SYMBIOTIC Principal"),
        ("MEMORIA_DIGILANG_UNIFICADA.py", "Sistema de Memória DigiLang"),
        ("SCRIPTUREMON_ULTIMATE_RAG.py", "Sistema RAG Principal"),
        ("SCRIPTUREMON_ULTIMATE_RAG_FIXED.py", "Sistema RAG Corrigido"),
        ("SCRIPTUREMON_RAG_EVOLUTION.py", "Sistema RAG Evolution"),
        ("SCRIPTUREMON_IMMORTAL_FINAL.py", "Sistema Immortal"),
        ("CINEMA_KNOWLEDGE_SYSTEM.py", "Sistema Cinema Knowledge"),
        ("SYMBIOTIC_FUSION_ULTIMATE.py", "Sistema Fusion Ultimate"),
        ("SCRIPTUREMON_ULTIMATE_HYBRID.py", "Sistema Hybrid"),
        ("ULTRA_DEEP_ANALYSIS.py", "Análise Ultra Profunda"),
    ]
    
    for filename, desc in main_files:
        if not check_file(base_path / filename, desc):
            all_ok = False
    
    # 2. DIRETÓRIOS ESSENCIAIS
    print("\n📁 DIRETÓRIOS ESSENCIAIS:")
    directories = [
        ("CINEMA_KNOWLEDGE", "Base Cinema Knowledge", 50),
        ("CINEMA_KNOWLEDGE/01_ORIGINAIS_PDF", "52 PDFs Originais", 52),
        ("memory", "Sistema de Memória", 5),
        ("immortality", "Backups de Imortalidade", 1),
        ("soulpacks", "Soul Packs", 1),
        ("apps", "Aplicações", 1),
        ("bin", "Executáveis", 1),
        ("src", "Source Code", 1),
    ]
    
    for dirname, desc, min_files in directories:
        if not check_directory(base_path / dirname, desc, min_files):
            all_ok = False
    
    # 3. VERIFICAR IMPORTS PYTHON
    print("\n🐍 VERIFICAÇÃO DE IMPORTS:")
    sys.path.insert(0, str(base_path))
    
    modules = [
        "SCRIPTUREMON_ULTIMATE_SYMBIOTIC",
        "MEMORIA_DIGILANG_UNIFICADA",
        "CINEMA_KNOWLEDGE_SYSTEM",
        "SYMBIOTIC_FUSION_ULTIMATE",
    ]
    
    for module in modules:
        if not check_import(module):
            all_ok = False
    
    # 4. VERIFICAR DEPENDÊNCIAS EXTERNAS
    print("\n📦 DEPENDÊNCIAS EXTERNAS:")
    external_deps = [
        "redis",
        "ollama",
        "chromadb",
        "pdfplumber",
        "rank_bm25",
        "watchdog",
        "pycrdt",
    ]
    
    for dep in external_deps:
        if not check_import(dep):
            all_ok = False
    
    # 5. VERIFICAR MODELOS OLLAMA
    print("\n🤖 MODELOS OLLAMA NECESSÁRIOS:")
    required_models = [
        "llama3.2:3b",
        "mistral:latest", 
        "scripturemon-ultimate-100",
        "scripturemon-nature",
    ]
    
    try:
        import ollama
        available = [m['name'] for m in ollama.list()['models']]
        for model in required_models:
            # Remover :latest para comparação
            model_base = model.replace(":latest", "")
            found = any(model_base in m for m in available)
            if found:
                print(f"✅ Modelo {model}: DISPONÍVEL")
            else:
                print(f"❌ Modelo {model}: NÃO ENCONTRADO")
                all_ok = False
    except Exception as e:
        print(f"⚠️ Não foi possível verificar modelos Ollama: {e}")
    
    # 6. VERIFICAR REDIS
    print("\n🔴 VERIFICAÇÃO REDIS:")
    try:
        import redis
        r = redis.Redis(host='localhost', port=6379, socket_connect_timeout=1)
        r.ping()
        print("✅ Redis: ONLINE")
    except:
        print("⚠️ Redis: OFFLINE (será iniciado sob demanda)")
    
    # RESULTADO FINAL
    print("\n" + "=" * 80)
    if all_ok:
        print("✅ CENTRALIZAÇÃO COMPLETA - TODOS OS COMPONENTES PRESENTES!")
        print("O sistema está pronto para funcionar independentemente.")
    else:
        print("⚠️ ALGUNS COMPONENTES ESTÃO FALTANDO")
        print("Verifique os itens marcados com ❌ acima.")
    print("=" * 80)
    
    return 0 if all_ok else 1

if __name__ == "__main__":
    sys.exit(main())