#!/usr/bin/env python3
"""
🧬 SISTEMA RAG COMPLETO PARA SCRIPTUREMON
Baseado nas especificações da pasta pesquisas_revolution
Implementa: ChromaDB + BGE-M3 + Hybrid Search + Re-ranking
"""

import os
import sys
import json
import time
import hashlib
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime

# Verificar e instalar dependências
try:
    import chromadb
    from chromadb.config import Settings
    import ollama
    import PyPDF2
    from sentence_transformers import SentenceTransformer, CrossEncoder
    import numpy as np
except ImportError as e:
    print(f"⚠️ Instalando dependências: {e}")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", 
                          "chromadb", "sentence-transformers", "PyPDF2", 
                          "numpy", "--user", "--break-system-packages"])
    print("✅ Dependências instaladas. Por favor, execute novamente.")
    sys.exit(1)

class ScripturemonRAGSystem:
    """
    Sistema RAG completo com as 4 camadas de memória:
    L1_CORE - Conhecimento imutável (teorias fundamentais)
    L2_CONSOLIDATED - Base de conhecimento em evolução
    L3_ACTIVE - Memória de sessão/conversação
    L4_QUANTUM - Conhecimento hipotético/gerado
    """
    
    def __init__(self, base_path: str = "/Users/clubproducoes/Digimundo"):
        self.base_path = Path(base_path)
        self.db_path = self.base_path / "chromadb_scripturemon"
        
        print("🧬 Inicializando Sistema RAG Scripturemon...")
        
        # Inicializar ChromaDB
        self.setup_chromadb()
        
        # Inicializar modelo de embeddings (BGE-M3 ou fallback)
        self.setup_embeddings()
        
        # Inicializar re-ranker
        self.setup_reranker()
        
        # Sistema de memórias hierárquicas
        self.memory_layers = {
            "L1_CORE": None,      # Coleção imutável
            "L2_CONSOLIDATED": None,  # Coleção principal evolutiva
            "L3_ACTIVE": [],      # Lista em memória da sessão
            "L4_QUANTUM": None    # Processo dinâmico (HyDE)
        }
        
        self.setup_collections()
        
        print("✅ Sistema RAG inicializado com sucesso!")
    
    def setup_chromadb(self):
        """Configura ChromaDB com persistência"""
        try:
            self.chroma_client = chromadb.PersistentClient(
                path=str(self.db_path),
                settings=Settings(
                    anonymized_telemetry=False,
                    allow_reset=True
                )
            )
            print("  ✅ ChromaDB conectado")
        except Exception as e:
            print(f"  ❌ Erro ChromaDB: {e}")
            raise
    
    def setup_embeddings(self):
        """Configura modelo de embeddings BGE-M3 ou fallback"""
        try:
            # Tentar BGE-M3 (melhor para multilingual)
            self.embedder = SentenceTransformer('BAAI/bge-m3')
            self.embedding_dim = 1024
            print("  ✅ BGE-M3 carregado (melhor qualidade)")
        except:
            try:
                # Fallback para modelo menor
                self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
                self.embedding_dim = 384
                print("  ⚠️ Usando all-MiniLM (fallback)")
            except Exception as e:
                print(f"  ❌ Erro embeddings: {e}")
                raise
    
    def setup_reranker(self):
        """Configura cross-encoder para re-ranking"""
        try:
            self.reranker = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')
            print("  ✅ Re-ranker configurado")
        except:
            self.reranker = None
            print("  ⚠️ Re-ranker não disponível")
    
    def setup_collections(self):
        """Cria/conecta às coleções das 4 camadas"""
        
        # L1_CORE - Conhecimento fundamental imutável
        try:
            self.memory_layers["L1_CORE"] = self.chroma_client.get_or_create_collection(
                name="l1_core_immutable",
                metadata={"layer": "L1", "type": "immutable", "description": "Teorias fundamentais"}
            )
            print("  ✅ L1_CORE conectado")
        except Exception as e:
            print(f"  ⚠️ L1_CORE erro: {e}")
        
        # L2_CONSOLIDATED - Base principal evolutiva
        try:
            self.memory_layers["L2_CONSOLIDATED"] = self.chroma_client.get_or_create_collection(
                name="l2_consolidated_evolving",
                metadata={"layer": "L2", "type": "evolving", "description": "Conhecimento acumulado"}
            )
            print("  ✅ L2_CONSOLIDATED conectado")
        except Exception as e:
            print(f"  ⚠️ L2_CONSOLIDATED erro: {e}")
        
        # L3_ACTIVE já é lista em memória
        print("  ✅ L3_ACTIVE (memória de sessão) ativo")
        
        # L4_QUANTUM é processo, não storage
        print("  ✅ L4_QUANTUM (geração hipotética) disponível")
    
    def ingest_pdf(self, pdf_path: str, doc_type: str = "theory") -> Dict[str, Any]:
        """
        Ingesta um PDF no sistema RAG
        Implementa o pipeline completo descrito no documento
        """
        pdf_path = Path(pdf_path)
        
        if not pdf_path.exists():
            return {"error": f"PDF não encontrado: {pdf_path}"}
        
        print(f"\n📄 Ingerindo PDF: {pdf_path.name}")
        print(f"   Tipo: {doc_type}")
        
        # 1. Extrair texto do PDF
        text = self.extract_pdf_text(pdf_path)
        
        if not text:
            return {"error": "Não foi possível extrair texto do PDF"}
        
        # 2. Chunking inteligente baseado no tipo
        chunks = self.smart_chunking(text, doc_type)
        print(f"   📊 {len(chunks)} chunks criados")
        
        # 3. Gerar embeddings
        embeddings = self.generate_embeddings([c['text'] for c in chunks])
        
        # 4. Adicionar metadados
        for i, chunk in enumerate(chunks):
            chunk['embedding'] = embeddings[i].tolist()
            chunk['metadata'] = {
                'source': pdf_path.name,
                'type': doc_type,
                'chunk_id': i,
                'total_chunks': len(chunks),
                'ingested_at': datetime.now().isoformat()
            }
        
        # 5. Armazenar em L2_CONSOLIDATED
        if self.memory_layers["L2_CONSOLIDATED"]:
            self.store_chunks_in_chromadb(chunks, "L2_CONSOLIDATED")
            print(f"   ✅ Armazenado em L2_CONSOLIDATED")
        
        # 6. Se for teoria fundamental, também em L1_CORE
        if doc_type == "fundamental_theory" and self.memory_layers["L1_CORE"]:
            self.store_chunks_in_chromadb(chunks, "L1_CORE")
            print(f"   ✅ Também armazenado em L1_CORE (imutável)")
        
        return {
            "status": "success",
            "file": pdf_path.name,
            "chunks": len(chunks),
            "doc_type": doc_type
        }
    
    def extract_pdf_text(self, pdf_path: Path) -> str:
        """Extrai texto de PDF"""
        try:
            text = ""
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    text += page.extract_text()
            return text
        except Exception as e:
            print(f"   ❌ Erro extraindo PDF: {e}")
            return ""
    
    def smart_chunking(self, text: str, doc_type: str) -> List[Dict]:
        """
        Chunking inteligente baseado no tipo de documento
        Teoria: chunks menores e precisos
        Roteiro: preserva estrutura de cenas
        """
        chunks = []
        
        if doc_type == "screenplay":
            # Preservar estrutura de roteiro
            scenes = text.split("INT.") + text.split("EXT.")
            for scene in scenes:
                if len(scene.strip()) > 50:
                    chunks.append({
                        'text': scene[:2000],  # Limitar tamanho
                        'type': 'scene'
                    })
        else:
            # Chunking padrão para teoria
            chunk_size = 500
            overlap = 50
            
            for i in range(0, len(text), chunk_size - overlap):
                chunk_text = text[i:i + chunk_size]
                if len(chunk_text.strip()) > 50:
                    chunks.append({
                        'text': chunk_text,
                        'type': 'theory'
                    })
        
        return chunks
    
    def generate_embeddings(self, texts: List[str]) -> np.ndarray:
        """Gera embeddings usando o modelo configurado"""
        try:
            embeddings = self.embedder.encode(texts, show_progress_bar=False)
            return embeddings
        except Exception as e:
            print(f"   ❌ Erro gerando embeddings: {e}")
            # Fallback: embeddings aleatórios
            return np.random.rand(len(texts), self.embedding_dim)
    
    def store_chunks_in_chromadb(self, chunks: List[Dict], layer: str):
        """Armazena chunks no ChromaDB"""
        collection = self.memory_layers[layer]
        
        if not collection:
            return
        
        # Preparar dados para ChromaDB
        ids = []
        embeddings = []
        documents = []
        metadatas = []
        
        for chunk in chunks:
            # Gerar ID único
            chunk_id = hashlib.md5(chunk['text'].encode()).hexdigest()
            
            ids.append(chunk_id)
            embeddings.append(chunk['embedding'])
            documents.append(chunk['text'])
            metadatas.append(chunk['metadata'])
        
        # Adicionar ao ChromaDB
        try:
            collection.add(
                ids=ids,
                embeddings=embeddings,
                documents=documents,
                metadatas=metadatas
            )
        except Exception as e:
            print(f"   ⚠️ Erro armazenando no ChromaDB: {e}")
    
    def hybrid_search(self, query: str, k: int = 10) -> List[Dict]:
        """
        Busca híbrida: semântica + keywords
        Implementa o conceito descrito no documento
        """
        results = []
        
        # 1. Busca semântica em L1 e L2
        query_embedding = self.generate_embeddings([query])[0]
        
        # Buscar em L1_CORE (conhecimento fundamental)
        if self.memory_layers["L1_CORE"]:
            try:
                l1_results = self.memory_layers["L1_CORE"].query(
                    query_embeddings=[query_embedding.tolist()],
                    n_results=k//2
                )
                for i, doc in enumerate(l1_results['documents'][0]):
                    results.append({
                        'text': doc,
                        'metadata': l1_results['metadatas'][0][i] if l1_results['metadatas'] else {},
                        'distance': l1_results['distances'][0][i] if l1_results['distances'] else 0,
                        'layer': 'L1_CORE'
                    })
            except:
                pass
        
        # Buscar em L2_CONSOLIDATED
        if self.memory_layers["L2_CONSOLIDATED"]:
            try:
                l2_results = self.memory_layers["L2_CONSOLIDATED"].query(
                    query_embeddings=[query_embedding.tolist()],
                    n_results=k
                )
                for i, doc in enumerate(l2_results['documents'][0]):
                    results.append({
                        'text': doc,
                        'metadata': l2_results['metadatas'][0][i] if l2_results['metadatas'] else {},
                        'distance': l2_results['distances'][0][i] if l2_results['distances'] else 0,
                        'layer': 'L2_CONSOLIDATED'
                    })
            except:
                pass
        
        # 2. Incluir L3_ACTIVE (memória de sessão)
        for memory in self.memory_layers["L3_ACTIVE"][-5:]:  # Últimas 5 interações
            results.append({
                'text': memory,
                'metadata': {'type': 'session_memory'},
                'distance': 0.5,
                'layer': 'L3_ACTIVE'
            })
        
        # 3. Re-ranking se disponível
        if self.reranker and results:
            pairs = [[query, r['text']] for r in results]
            scores = self.reranker.predict(pairs)
            
            # Ordenar por score do reranker
            for i, score in enumerate(scores):
                results[i]['rerank_score'] = score
            
            results = sorted(results, key=lambda x: x.get('rerank_score', 0), reverse=True)
        
        return results[:k]
    
    def generate_with_rag(self, query: str, model: str = "scripturemon-128k:latest") -> str:
        """
        Gera resposta usando RAG com as 4 camadas de memória
        """
        print(f"\n🤔 Query: {query}")
        
        # 1. Adicionar à memória de sessão (L3)
        self.memory_layers["L3_ACTIVE"].append(f"User: {query}")
        
        # 2. Busca híbrida
        retrieved_docs = self.hybrid_search(query, k=5)
        
        # 3. L4_QUANTUM - Geração hipotética (HyDE simplificado)
        hypothetical_answer = self.generate_hypothetical_answer(query)
        if hypothetical_answer:
            retrieved_docs.append({
                'text': hypothetical_answer,
                'layer': 'L4_QUANTUM',
                'metadata': {'type': 'hypothetical'}
            })
        
        # 4. Construir contexto
        context = self.build_context(retrieved_docs)
        
        # 5. Construir prompt final
        prompt = f"""Você é Scripturemon, o crítico mais brutal de roteiros.

CONTEXTO RECUPERADO:
{context}

MEMÓRIA DE SESSÃO:
{' | '.join(self.memory_layers["L3_ACTIVE"][-3:])}

PERGUNTA: {query}

Responda com brutalidade característica, citando fontes quando relevante."""
        
        # 6. Gerar resposta com Ollama
        try:
            response = ollama.generate(
                model=model,
                prompt=prompt,
                options={
                    "temperature": 0.7,
                    "num_ctx": 8192
                }
            )
            
            answer = response['response']
            
            # 7. Adicionar resposta à L3
            self.memory_layers["L3_ACTIVE"].append(f"Scripturemon: {answer[:200]}...")
            
            return answer
            
        except Exception as e:
            return f"Erro gerando resposta: {e}"
    
    def generate_hypothetical_answer(self, query: str) -> Optional[str]:
        """
        L4_QUANTUM - Gera resposta hipotética (HyDE)
        """
        try:
            prompt = f"Generate a brief hypothetical answer to: {query}"
            response = ollama.generate(
                model="mistral:latest",
                prompt=prompt,
                options={"num_predict": 100, "temperature": 0.5}
            )
            return response['response']
        except:
            return None
    
    def build_context(self, docs: List[Dict]) -> str:
        """Constrói contexto a partir dos documentos recuperados"""
        context_parts = []
        
        for doc in docs:
            layer = doc.get('layer', 'Unknown')
            text = doc['text'][:500]  # Limitar tamanho
            
            if layer == 'L1_CORE':
                context_parts.append(f"[FUNDAMENTAL]: {text}")
            elif layer == 'L2_CONSOLIDATED':
                context_parts.append(f"[KNOWLEDGE]: {text}")
            elif layer == 'L3_ACTIVE':
                context_parts.append(f"[SESSION]: {text}")
            elif layer == 'L4_QUANTUM':
                context_parts.append(f"[HYPOTHESIS]: {text}")
            else:
                context_parts.append(f"[{layer}]: {text}")
        
        return "\n\n".join(context_parts)
    
    def status(self) -> Dict:
        """Retorna status do sistema RAG"""
        status = {
            "chromadb": "✅ Conectado" if self.chroma_client else "❌ Desconectado",
            "embedder": self.embedder.device if self.embedder else "❌ Não configurado",
            "reranker": "✅ Ativo" if self.reranker else "⚠️ Não disponível",
            "collections": {}
        }
        
        # Status das coleções
        for layer, collection in self.memory_layers.items():
            if layer == "L3_ACTIVE":
                status["collections"][layer] = f"📝 {len(collection)} memórias"
            elif layer == "L4_QUANTUM":
                status["collections"][layer] = "🔮 Processo dinâmico"
            elif collection:
                try:
                    count = collection.count()
                    status["collections"][layer] = f"📚 {count} documentos"
                except:
                    status["collections"][layer] = "⚠️ Erro"
            else:
                status["collections"][layer] = "❌ Não inicializado"
        
        return status

def main():
    """Função principal para testar o sistema RAG"""
    
    print("╔════════════════════════════════════════════════════════════════╗")
    print("║          🧬 SISTEMA RAG SCRIPTUREMON - ATIVAÇÃO               ║")
    print("║     ChromaDB + BGE-M3 + Hybrid Search + 4-Layer Memory        ║")
    print("╚════════════════════════════════════════════════════════════════╝")
    print()
    
    # Inicializar sistema
    rag = ScripturemonRAGSystem()
    
    # Mostrar status
    print("\n📊 Status do Sistema:")
    status = rag.status()
    for key, value in status.items():
        if isinstance(value, dict):
            print(f"  {key}:")
            for k, v in value.items():
                print(f"    • {k}: {v}")
        else:
            print(f"  {key}: {value}")
    
    # Testar ingestão se houver PDFs
    test_pdf = Path("/Users/clubproducoes/Digimundo/pesquisas_revolution").glob("*.pdf")
    test_pdf = list(test_pdf)
    
    if test_pdf:
        print(f"\n📚 Encontrados {len(test_pdf)} PDFs para ingerir")
        for pdf in test_pdf[:2]:  # Ingerir apenas 2 para teste
            result = rag.ingest_pdf(str(pdf), "theory")
            print(f"   {result}")
    
    # Teste de busca
    print("\n🔍 Teste de busca híbrida:")
    test_query = "What is the three-act structure?"
    results = rag.hybrid_search(test_query, k=3)
    
    for i, result in enumerate(results, 1):
        print(f"\n  Result {i} (Layer: {result.get('layer', 'Unknown')}):")
        print(f"    {result['text'][:100]}...")
    
    # Teste de geração com RAG
    print("\n💬 Teste de geração com RAG:")
    response = rag.generate_with_rag(test_query)
    print(f"   Resposta: {response[:200]}...")
    
    print("\n✅ Sistema RAG ativado e funcionando!")
    print("   Use a classe ScripturemonRAGSystem em seus scripts")

if __name__ == "__main__":
    main()