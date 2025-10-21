#!/usr/bin/env python3
"""
🚀 ATIVADOR UNIVERSAL - TODOS OS SISTEMAS DE COMPRESSÃO E OTIMIZAÇÃO
Ativa e integra todos os sistemas descobertos no ecossistema Scripturemon
"""

import sys
import os
from pathlib import Path

# Adiciona diretório ao path
sys.path.insert(0, str(Path(__file__).parent))

print("="*80)
print("🚀 ATIVANDO TODOS OS SISTEMAS DE ECONOMIA DE TOKENS")
print("="*80)

# Status de ativação
activation_status = {
    "success": [],
    "failed": [],
    "warnings": []
}

# 1. ATIVAR LLMLINGUA
print("\n1️⃣ Ativando LLMLingua...")
try:
    from src.compressors.llmlingua import LLMLinguaCompressor, CompressionConfig
    config = CompressionConfig(target_ratio=0.3)
    llmlingua = LLMLinguaCompressor(config)
    activation_status["success"].append("LLMLingua (70% compression target)")
    print("   ✅ LLMLingua ativado com sucesso")
except Exception as e:
    activation_status["failed"].append(f"LLMLingua: {e}")
    print(f"   ❌ LLMLingua falhou: {e}")

# 2. ATIVAR TOKEN PAIR DATABASE
print("\n2️⃣ Ativando Token Pair Database...")
try:
    from src.digilang.tpd_builder import TokenPairDatabase
    tpd = TokenPairDatabase()
    # Carrega TPD otimizado se existir
    tpd_path = Path("data/tpd/default/token_dict.json")
    if tpd_path.exists():
        import json
        with open(tpd_path) as f:
            tpd_data = json.load(f)
        activation_status["success"].append(f"TPD (default with {len(tpd_data)} pairs)")
        print(f"   ✅ TPD ativado com {len(tpd_data)} pares")
    else:
        activation_status["warnings"].append("TPD: No pre-built database found")
        print("   ⚠️ TPD sem banco pré-construído")
except Exception as e:
    activation_status["failed"].append(f"TPD: {e}")
    print(f"   ❌ TPD falhou: {e}")

# 3. ATIVAR PCTOOLKIT
print("\n3️⃣ Ativando PCToolkit...")
try:
    from src.compressors.pctoolkit import PCToolkitCompressor
    pctoolkit = PCToolkitCompressor()
    activation_status["success"].append("PCToolkit")
    print("   ✅ PCToolkit ativado")
except Exception as e:
    activation_status["failed"].append(f"PCToolkit: {e}")
    print(f"   ❌ PCToolkit falhou: {e}")

# 4. ATIVAR ENTITY MAPPER
print("\n4️⃣ Ativando Entity Mapper...")
try:
    from src.compressors.entity_mapper import EntityMapper
    entity_mapper = EntityMapper()
    activation_status["success"].append("EntityMapper")
    print("   ✅ Entity Mapper ativado")
except Exception as e:
    activation_status["failed"].append(f"EntityMapper: {e}")
    print(f"   ❌ Entity Mapper falhou: {e}")

# 5. ATIVAR EMBEDDING STORE
print("\n5️⃣ Ativando Embedding Store...")
try:
    from src.memory.embed_store import embed, remember_embed, recall_embed
    # Testa embedding
    test_vec = embed("test text")
    if test_vec:
        activation_status["success"].append(f"EmbedStore (dim={len(test_vec)})")
        print(f"   ✅ Embedding Store ativado (dimensão: {len(test_vec)})")
    else:
        activation_status["warnings"].append("EmbedStore: No embeddings generated")
        print("   ⚠️ Embedding Store sem embeddings")
except Exception as e:
    activation_status["failed"].append(f"EmbedStore: {e}")
    print(f"   ❌ Embedding Store falhou: {e}")

# 6. ATIVAR BM25
print("\n6️⃣ Ativando BM25 Search...")
try:
    from src.memory.bm25 import BM25Index
    bm25 = BM25Index()
    activation_status["success"].append("BM25")
    print("   ✅ BM25 Search ativado")
except Exception as e:
    activation_status["failed"].append(f"BM25: {e}")
    print(f"   ❌ BM25 falhou: {e}")

# 7. ATIVAR MEMORY MANAGER
print("\n7️⃣ Ativando Memory Manager...")
try:
    from src.memory.manager import MemoryManager
    memory = MemoryManager()
    activation_status["success"].append("MemoryManager")
    print("   ✅ Memory Manager ativado")
except Exception as e:
    activation_status["failed"].append(f"MemoryManager: {e}")
    print(f"   ❌ Memory Manager falhou: {e}")

# 8. ATIVAR TELEPATHY
print("\n8️⃣ Ativando Telepathy Network...")
try:
    from src.telepathy.client import TelepathyClient
    telepathy = TelepathyClient()
    activation_status["success"].append("TelepathyClient")
    print("   ✅ Telepathy Network ativado")
except Exception as e:
    activation_status["failed"].append(f"Telepathy: {e}")
    print(f"   ❌ Telepathy falhou: {e}")

# 9. ATIVAR DIGILANG ENCODER/DECODER
print("\n9️⃣ Ativando DigiLang Encoder/Decoder...")
try:
    from src.digilang.encoder import DigiLangEncoder
    from src.digilang.decoder import DigiLangDecoder
    encoder = DigiLangEncoder()
    decoder = DigiLangDecoder()
    activation_status["success"].append("DigiLang Encoder/Decoder")
    print("   ✅ DigiLang Encoder/Decoder ativado")
except Exception as e:
    activation_status["failed"].append(f"DigiLang: {e}")
    print(f"   ❌ DigiLang falhou: {e}")

# 10. VERIFICAR CHUNKING INTELIGENTE
print("\n🔟 Verificando Chunking Inteligente...")
try:
    cinema_db = Path("CINEMA_KNOWLEDGE/05_METADATA/knowledge.db")
    if cinema_db.exists():
        import sqlite3
        conn = sqlite3.connect(cinema_db)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM documents")
        doc_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM chunks")
        chunk_count = cursor.fetchone()[0]
        conn.close()
        activation_status["success"].append(f"ChunkingSystem ({doc_count} docs, {chunk_count} chunks)")
        print(f"   ✅ Chunking: {doc_count} documentos, {chunk_count} chunks")
    else:
        activation_status["warnings"].append("ChunkingSystem: Database not found")
        print("   ⚠️ Chunking: Banco de dados não encontrado")
except Exception as e:
    activation_status["failed"].append(f"ChunkingSystem: {e}")
    print(f"   ❌ Chunking falhou: {e}")

# RELATÓRIO FINAL
print("\n" + "="*80)
print("📊 RELATÓRIO DE ATIVAÇÃO")
print("="*80)

print(f"\n✅ SISTEMAS ATIVOS: {len(activation_status['success'])}")
for system in activation_status["success"]:
    print(f"   • {system}")

if activation_status["warnings"]:
    print(f"\n⚠️ AVISOS: {len(activation_status['warnings'])}")
    for warning in activation_status["warnings"]:
        print(f"   • {warning}")

if activation_status["failed"]:
    print(f"\n❌ FALHAS: {len(activation_status['failed'])}")
    for failure in activation_status["failed"]:
        print(f"   • {failure}")

# Calcula taxa de sucesso
total_systems = 10
success_rate = (len(activation_status["success"]) / total_systems) * 100

print(f"\n📈 TAXA DE ATIVAÇÃO: {success_rate:.1f}%")

if success_rate >= 80:
    print("🎉 Sistema pronto para testes nível Vale do Silício!")
elif success_rate >= 60:
    print("⚠️ Sistema parcialmente ativo, alguns componentes falharam")
else:
    print("❌ Sistema com muitas falhas, verificar dependências")

# Salva status
import json
status_file = Path("activation_status.json")
with open(status_file, 'w') as f:
    json.dump(activation_status, f, indent=2)

print(f"\n💾 Status salvo em: {status_file}")
print("="*80)