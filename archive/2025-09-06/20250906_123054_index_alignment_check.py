#!/usr/bin/env python3
"""
V3.2 — Index Alignment Check
Verifica alinhamento entre RAG Adapter, Chroma e Memory Manager.
"""
import json
import os
import sys
from pathlib import Path
from datetime import datetime

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

def check_alignment():
    """Verifica alinhamento completo do índice."""
    
    report = {
        "timestamp": datetime.now().isoformat(),
        "phase": "FASE_1_ALIGNMENT",
        "checks": {},
        "alignment": {
            "collection_name": None,
            "schema_match": False,
            "provider_match": False
        },
        "issues": [],
        "recommendations": []
    }
    
    print("🔍 V3.2 Index Alignment Check\n")
    
    # 1. Verificar ChromaDB
    print("1️⃣ Verificando ChromaDB...")
    try:
        import chromadb
        chroma_path = os.environ.get('CHROMA_PATH', str(Path(__file__).parent.parent.parent / 'data' / 'chroma'))
        client = chromadb.PersistentClient(path=chroma_path)
        
        # Listar collections
        collections = client.list_collections()
        print(f"   Collections disponíveis: {[c.name for c in collections]}")
        
        # Verificar v3_1_docs
        try:
            collection = client.get_collection("v3_1_docs")
            count = collection.count()
            print(f"   ✅ Collection 'v3_1_docs': {count} documentos")
            
            # Pegar amostra
            if count > 0:
                sample = collection.get(limit=1)
                if sample and sample.get('metadatas'):
                    meta_keys = list(sample['metadatas'][0].keys())
                    print(f"   Schema: {meta_keys}")
                    report["checks"]["chroma"] = {
                        "status": "ok",
                        "collection": "v3_1_docs",
                        "count": count,
                        "schema": meta_keys
                    }
                    report["alignment"]["collection_name"] = "v3_1_docs"
        except Exception as e:
            print(f"   ⚠️ Collection v3_1_docs não encontrada: {e}")
            report["issues"].append("Collection v3_1_docs não existe no ChromaDB")
            report["recommendations"].append("Executar rag_reindex.py para criar e popular a collection")
            
    except Exception as e:
        print(f"   ❌ ChromaDB não disponível: {e}")
        report["checks"]["chroma"] = {"status": "error", "error": str(e)}
        report["issues"].append(f"ChromaDB não acessível: {e}")
    
    # 2. Verificar RAG Adapter
    print("\n2️⃣ Verificando RAG Adapter...")
    try:
        from src.rag.adapter import RAGAdapter
        from src.utils.config_loader import load_settings
        
        settings = load_settings()
        adapter = RAGAdapter(settings)
        
        print(f"   Provider configurado: {adapter.provider}")
        print(f"   RAG habilitado: {adapter.enabled}")
        print(f"   K padrão: {adapter.k}")
        
        # Verificar se usa Chroma real
        if hasattr(adapter, 'chroma_client'):
            if adapter.chroma_client:
                print(f"   ✅ Chroma client inicializado")
                if adapter.chroma_collection:
                    print(f"   ✅ Collection conectada: {adapter.chroma_collection.name}")
                    report["alignment"]["provider_match"] = True
                else:
                    print(f"   ⚠️ Collection não inicializada")
                    report["issues"].append("RAG Adapter não tem collection Chroma inicializada")
            else:
                print(f"   ⚠️ Chroma client é None (usando stub)")
                report["issues"].append("RAG Adapter está usando stub ao invés de Chroma real")
        else:
            print(f"   ❌ Adapter não tem atributo chroma_client (versão antiga)")
            report["issues"].append("RAG Adapter precisa ser atualizado com suporte a Chroma")
            
        # Testar retrieve
        print("\n   Testando retrieve()...")
        results = adapter.retrieve("test query", k=3)
        if results:
            print(f"   ✅ Retrieve retornou {len(results)} resultados")
            if results[0].get('method') == 'chroma':
                print(f"   ✅ Usando backend Chroma real")
            else:
                print(f"   ⚠️ Usando backend: {results[0].get('method', 'stub')}")
                report["issues"].append("Retrieve não está usando Chroma como backend")
        else:
            print(f"   ⚠️ Retrieve retornou vazio")
            
        report["checks"]["rag_adapter"] = {
            "status": "ok",
            "provider": adapter.provider,
            "enabled": adapter.enabled,
            "has_chroma": adapter.chroma_client is not None if hasattr(adapter, 'chroma_client') else False
        }
        
    except Exception as e:
        print(f"   ❌ Erro ao verificar RAG Adapter: {e}")
        report["checks"]["rag_adapter"] = {"status": "error", "error": str(e)}
        report["issues"].append(f"RAG Adapter com erro: {e}")
    
    # 3. Verificar Unified Memory Manager
    print("\n3️⃣ Verificando Unified Memory Manager...")
    try:
        from src.memory.unified_manager import UnifiedMemoryManager
        from src.utils.config_loader import load_settings
        
        settings = load_settings()
        manager = UnifiedMemoryManager(settings)
        
        print(f"   RAG Adapter presente: {manager.rag_adapter is not None}")
        print(f"   Chroma client: {manager.chroma_client is not None}")
        
        # Testar get_context
        print("\n   Testando get_context()...")
        context = manager.get_context("test query", max_chunks=5)
        if context:
            print(f"   ✅ get_context retornou {len(context)} chunks")
            sources = set(c.get('source') for c in context)
            print(f"   Sources: {sources}")
        else:
            print(f"   ⚠️ get_context retornou vazio")
            
        report["checks"]["memory_manager"] = {
            "status": "ok",
            "has_rag": manager.rag_adapter is not None,
            "has_chroma": manager.chroma_client is not None
        }
        
    except Exception as e:
        print(f"   ❌ Erro ao verificar Memory Manager: {e}")
        report["checks"]["memory_manager"] = {"status": "error", "error": str(e)}
        report["issues"].append(f"Memory Manager com erro: {e}")
    
    # 4. Verificar esquema alinhado
    print("\n4️⃣ Verificando alinhamento de esquema...")
    expected_schema = ["source", "path", "doc_hash", "chunk_no", "total_chunks", "mtime", "type"]
    
    if report["checks"].get("chroma", {}).get("schema"):
        actual_schema = report["checks"]["chroma"]["schema"]
        missing = set(expected_schema) - set(actual_schema)
        extra = set(actual_schema) - set(expected_schema)
        
        if not missing:
            print(f"   ✅ Schema completo")
            report["alignment"]["schema_match"] = True
        else:
            print(f"   ⚠️ Campos faltando: {missing}")
            report["issues"].append(f"Schema incompleto, faltando: {missing}")
            
        if extra:
            print(f"   ℹ️ Campos extras: {extra}")
    
    # 5. Resumo final
    print("\n" + "="*50)
    print("📊 RESUMO DO ALINHAMENTO\n")
    
    if not report["issues"]:
        print("✅ Sistema totalmente alinhado!")
        report["status"] = "aligned"
    else:
        print(f"⚠️ {len(report['issues'])} problemas encontrados:\n")
        for i, issue in enumerate(report["issues"], 1):
            print(f"   {i}. {issue}")
        
        if report["recommendations"]:
            print(f"\n💡 Recomendações:")
            for rec in report["recommendations"]:
                print(f"   • {rec}")
        
        report["status"] = "misaligned"
    
    # Salvar relatório
    report_path = Path(__file__).parent.parent.parent / 'reports' / 'fix_v3' / 'v32_bugfix_indexalign' / 'alignment_check.json'
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False))
    print(f"\n📄 Relatório salvo: {report_path}")
    
    return report

if __name__ == "__main__":
    check_alignment()