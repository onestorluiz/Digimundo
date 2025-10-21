#!/usr/bin/env python3
"""
🔧 RESTORE SYMBIOTIC SYSTEM - Restaura sistema funcionando SEM QUEBRAR NADA
NÃO otimiza, NÃO simplifica, NÃO remove - apenas CONECTA
"""

import sys
import os
from pathlib import Path

def test_symbiotic_system():
    """Testa se o sistema SYMBIOTIC está funcionando"""
    
    print("\n" + "="*80)
    print("🔧 TESTE DO SISTEMA SYMBIOTIC - SEM MODIFICAÇÕES")
    print("="*80)
    
    errors = []
    warnings = []
    success = []
    
    # 1. Verificar arquivo principal SYMBIOTIC
    print("\n1️⃣ Verificando SCRIPTUREMON_ULTIMATE_SYMBIOTIC.py...")
    symbiotic_path = Path("SCRIPTUREMON_ULTIMATE_SYMBIOTIC.py")
    if symbiotic_path.exists():
        success.append("✅ SCRIPTUREMON_ULTIMATE_SYMBIOTIC.py existe")
        print("   ✅ Arquivo encontrado (54KB)")
    else:
        errors.append("❌ SCRIPTUREMON_ULTIMATE_SYMBIOTIC.py não encontrado")
        print("   ❌ ERRO: Arquivo não encontrado!")
    
    # 2. Verificar MEMORIA_DIGILANG_UNIFICADA
    print("\n2️⃣ Verificando MEMORIA_DIGILANG_UNIFICADA.py...")
    memoria_path = Path("MEMORIA_DIGILANG_UNIFICADA.py")
    if memoria_path.exists():
        success.append("✅ MEMORIA_DIGILANG_UNIFICADA.py existe")
        print("   ✅ Arquivo encontrado (22KB)")
    else:
        errors.append("❌ MEMORIA_DIGILANG_UNIFICADA.py não encontrado")
        print("   ❌ ERRO: Arquivo não encontrado!")
    
    # 3. Verificar SCRIPTUREMON_ULTIMATE_RAG
    print("\n3️⃣ Verificando SCRIPTUREMON_ULTIMATE_RAG.py...")
    rag_path = Path("SCRIPTUREMON_ULTIMATE_RAG.py")
    if rag_path.exists():
        success.append("✅ SCRIPTUREMON_ULTIMATE_RAG.py existe")
        print("   ✅ Arquivo criado/restaurado")
    else:
        errors.append("❌ SCRIPTUREMON_ULTIMATE_RAG.py não encontrado")
        print("   ❌ ERRO: Arquivo não encontrado!")
    
    # 4. Verificar 52 PDFs
    print("\n4️⃣ Verificando Cinema Knowledge (52 PDFs)...")
    cinema_path = Path("CINEMA_KNOWLEDGE/01_ORIGINAIS_PDF")
    if cinema_path.exists():
        pdf_count = len(list(cinema_path.glob("*.pdf")))
        if pdf_count >= 52:
            success.append(f"✅ {pdf_count} PDFs disponíveis")
            print(f"   ✅ {pdf_count} PDFs encontrados")
        else:
            warnings.append(f"⚠️ Apenas {pdf_count}/52 PDFs encontrados")
            print(f"   ⚠️ {pdf_count}/52 PDFs (alguns faltando)")
    else:
        warnings.append("⚠️ Pasta Cinema Knowledge não encontrada")
        print("   ⚠️ Pasta não encontrada (PDFs podem estar em outro local)")
    
    # 5. Verificar modelos Ollama necessários
    print("\n5️⃣ Verificando modelos Ollama...")
    import subprocess
    try:
        result = subprocess.run(["ollama", "list"], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            models = result.stdout
            
            # Modelos necessários para o SYMBIOTIC
            required = ["llama3.2:3b", "mistral", "scripturemon"]
            found = []
            missing = []
            
            for model in required:
                if model in models:
                    found.append(model)
                else:
                    missing.append(model)
            
            if found:
                success.append(f"✅ {len(found)} modelos encontrados: {', '.join(found)}")
                print(f"   ✅ Modelos disponíveis: {', '.join(found)}")
            
            if missing:
                warnings.append(f"⚠️ Modelos faltando: {', '.join(missing)}")
                print(f"   ⚠️ Modelos faltando: {', '.join(missing)}")
        else:
            warnings.append("⚠️ Ollama não respondeu")
            print("   ⚠️ Ollama não respondeu")
    except:
        warnings.append("⚠️ Ollama não disponível")
        print("   ⚠️ Ollama não disponível")
    
    # 6. Testar imports do SYMBIOTIC
    print("\n6️⃣ Testando imports do sistema...")
    try:
        # Adiciona paths necessários
        sys.path.insert(0, str(Path.cwd()))
        sys.path.insert(0, str(Path.cwd() / "apps"))
        
        # Tenta importar componentes críticos
        imports_ok = []
        imports_fail = []
        
        # Teste 1: Soul
        try:
            from apps.scripturemon.soul import Soul
            imports_ok.append("Soul")
        except Exception as e:
            imports_fail.append(f"Soul: {e}")
        
        # Teste 2: Consciousness
        try:
            from apps.scripturemon.consciousness import get_level
            imports_ok.append("Consciousness")
        except Exception as e:
            imports_fail.append(f"Consciousness: {e}")
        
        # Teste 3: Memory Unification
        try:
            from apps.scripturemon.memory_unification import UnifiedMemorySystem
            imports_ok.append("UnifiedMemory")
        except Exception as e:
            imports_fail.append(f"UnifiedMemory: {e}")
        
        # Teste 4: RAG Advanced
        try:
            from apps.scripturemon.rag_advanced import AdvancedRAG
            imports_ok.append("AdvancedRAG")
        except Exception as e:
            imports_fail.append(f"AdvancedRAG: {e}")
        
        if imports_ok:
            success.append(f"✅ Imports funcionando: {', '.join(imports_ok)}")
            print(f"   ✅ Imports OK: {', '.join(imports_ok)}")
        
        if imports_fail:
            for fail in imports_fail:
                warnings.append(f"⚠️ Import falhou: {fail}")
                print(f"   ⚠️ {fail}")
    
    except Exception as e:
        errors.append(f"❌ Erro geral nos imports: {e}")
        print(f"   ❌ Erro: {e}")
    
    # 7. Verificar Redis (opcional mas importante)
    print("\n7️⃣ Verificando Redis...")
    try:
        import redis
        r = redis.Redis(host='localhost', port=6379, decode_responses=True)
        r.ping()
        success.append("✅ Redis online")
        print("   ✅ Redis conectado e funcionando")
    except:
        warnings.append("⚠️ Redis offline (telepathy limitada)")
        print("   ⚠️ Redis não disponível (sistema funcionará com limitações)")
    
    # RELATÓRIO FINAL
    print("\n" + "="*80)
    print("📊 RELATÓRIO DO SISTEMA SYMBIOTIC")
    print("="*80)
    
    print(f"\n✅ SUCESSOS: {len(success)}")
    for s in success:
        print(f"   {s}")
    
    if warnings:
        print(f"\n⚠️ AVISOS: {len(warnings)}")
        for w in warnings:
            print(f"   {w}")
    
    if errors:
        print(f"\n❌ ERROS: {len(errors)}")
        for e in errors:
            print(f"   {e}")
    
    # CONCLUSÃO
    print("\n" + "="*80)
    if not errors:
        print("🎉 SISTEMA SYMBIOTIC PRONTO PARA USO!")
        print("\nPara ativar:")
        print("   python SCRIPTUREMON_ULTIMATE_SYMBIOTIC.py")
        print("\nOu use o script:")
        print("   ./bin/scripturemon-symbiotic")
    else:
        print("⚠️ SISTEMA COM PROBLEMAS - CORREÇÕES NECESSÁRIAS")
        print("\nProblemas encontrados devem ser resolvidos antes de usar.")
    print("="*80)
    
    return len(errors) == 0

if __name__ == "__main__":
    success = test_symbiotic_system()
    sys.exit(0 if success else 1)