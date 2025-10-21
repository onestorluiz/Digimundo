#!/usr/bin/env python3
"""
Teste rápido do Scripturemon - Validação básica
"""

import sys
import os
import time
import asyncio
from pathlib import Path

# Adiciona diretório pai ao path
sys.path.insert(0, str(Path(__file__).parent))

def test_imports():
    """Testa se todos os imports funcionam"""
    print("🔍 Testando imports...")
    try:
        from config import load_config
        print("✅ Config carregado")
        
        from app.models.embeddings import EmbeddingModel
        print("✅ EmbeddingModel disponível")
        
        from app.models.ollama_strategy import OllamaStrategy
        print("✅ OllamaStrategy disponível")
        
        from app.retrieval.hybrid import HybridRetriever
        print("✅ HybridRetriever disponível")
        
        from scripts.scripturemon_rag_bridge import ScripturemonRAG
        print("✅ ScripturemonRAG disponível")
        
        return True
    except Exception as e:
        print(f"❌ Erro nos imports: {e}")
        return False

def test_ollama_models():
    """Testa se os modelos Ollama estão disponíveis"""
    print("\n🤖 Testando modelos Ollama...")
    import subprocess
    
    try:
        result = subprocess.run(["ollama", "list"], capture_output=True, text=True)
        models = result.stdout
        
        required = ["llama3.2:3b", "mistral", "scripturemon-maestro"]
        found = []
        
        for model in required:
            if model in models or model.split(":")[0] in models:
                print(f"✅ {model} disponível")
                found.append(model)
            else:
                print(f"⚠️ {model} não encontrado")
        
        return len(found) >= 2  # Precisa de pelo menos 2 modelos
    except Exception as e:
        print(f"❌ Erro ao verificar Ollama: {e}")
        return False

def test_rag_search():
    """Testa busca RAG básica"""
    print("\n🔎 Testando RAG Search...")
    try:
        from app.retrieval.hybrid import HybridRetriever
        
        retriever = HybridRetriever()
        
        # Testa busca simples
        results = retriever.search("personagem principal", top_k=3)
        
        if results:
            print(f"✅ Encontrou {len(results)} resultados")
            for i, r in enumerate(results[:2], 1):
                print(f"  {i}. Score: {r.get('score', 0):.2f}")
        else:
            print("⚠️ Nenhum resultado encontrado (base vazia?)")
        
        return True
    except Exception as e:
        print(f"❌ Erro no RAG: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_ollama_generation():
    """Testa geração com Ollama"""
    print("\n📝 Testando geração Ollama...")
    try:
        from app.models.ollama_client import OllamaLLM
        
        llm = OllamaLLM(model="mistral:latest")
        response = llm.generate("Responda em 5 palavras: O que é um roteiro?")
        
        if response:
            print(f"✅ Resposta: {response[:100]}")
            return True
        else:
            print("❌ Resposta vazia")
            return False
    except Exception as e:
        print(f"❌ Erro na geração: {e}")
        return False

def test_embeddings():
    """Testa embeddings"""
    print("\n🧬 Testando embeddings...")
    try:
        from app.models.embeddings import EmbeddingModel
        
        embedder = EmbeddingModel()
        
        texts = [
            "O protagonista enfrenta seu maior medo",
            "A jornada do herói começa aqui"
        ]
        
        vecs = embedder.embed(texts)
        
        if vecs.shape[0] == 2:
            print(f"✅ Embeddings gerados: shape {vecs.shape}")
            return True
        else:
            print(f"❌ Shape incorreto: {vecs.shape}")
            return False
    except Exception as e:
        print(f"❌ Erro nos embeddings: {e}")
        return False

async def test_parallel():
    """Testa processamento paralelo simples"""
    print("\n⚡ Testando processamento paralelo...")
    try:
        from app.models.ollama_strategy import OllamaStrategy
        
        strategy = OllamaStrategy()
        
        # Testa apenas extração rápida
        text = "INT. CASA - DIA\n\nJOÃO olha pela janela, pensativo."
        
        start = time.time()
        result = await strategy.extract_entities(text)
        elapsed = time.time() - start
        
        if result:
            print(f"✅ Extração em {elapsed:.1f}s")
            print(f"   Personagens: {result.get('characters', [])[:2]}")
            return True
        else:
            print("❌ Extração falhou")
            return False
    except Exception as e:
        print(f"❌ Erro no paralelo: {e}")
        return False

def main():
    """Executa todos os testes"""
    print("="*60)
    print("🚀 SCRIPTUREMON - TESTE RÁPIDO")
    print("="*60)
    
    results = []
    
    # Testes síncronos
    results.append(("Imports", test_imports()))
    results.append(("Modelos Ollama", test_ollama_models()))
    results.append(("Embeddings", test_embeddings()))
    results.append(("RAG Search", test_rag_search()))
    results.append(("Geração Ollama", test_ollama_generation()))
    
    # Teste assíncrono
    try:
        loop = asyncio.get_event_loop()
        parallel_result = loop.run_until_complete(test_parallel())
        results.append(("Paralelo", parallel_result))
    except:
        results.append(("Paralelo", False))
    
    # Resumo
    print("\n" + "="*60)
    print("📊 RESUMO DOS TESTES")
    print("="*60)
    
    passed = sum(1 for _, r in results if r)
    total = len(results)
    
    for name, result in results:
        status = "✅" if result else "❌"
        print(f"{status} {name}")
    
    print(f"\n🏆 Resultado: {passed}/{total} testes passaram")
    
    if passed == total:
        print("🎉 Sistema 100% funcional!")
    elif passed >= total * 0.7:
        print("⚠️ Sistema parcialmente funcional")
    else:
        print("❌ Sistema precisa de correções")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)