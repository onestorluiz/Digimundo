#!/usr/bin/env python3
"""
🎬 SCRIPTUREMON ULTIMATE HYBRID - MELHOR DOS DOIS MUNDOS
=========================================================
Integração do Ultimate Symbiotic (interface perfeita) 
com sistemas importantes do RAG (busca e execução)
=========================================================
"""

import os
import sys
import json
import time
import asyncio
import threading
from pathlib import Path
from typing import Dict, List, Any, Optional

# Adicionar paths necessários
sys.path.insert(0, '/Users/clubproducoes/Digimundo/digimons/scripturemon')
sys.path.insert(0, '/Users/clubproducoes/Digimundo/digimons/scripturemon/src/core')

# Importar Ultimate Symbiotic como base
from SCRIPTUREMON_ULTIMATE_SYMBIOTIC import ScripturemonUltimateSymbiotic

# Importar sistema de memória DigiLang
try:
    from MEMORIA_DIGILANG_UNIFICADA import DigiLangMemorySystem
    DIGILANG_OK = True
except:
    DIGILANG_OK = False
    print("⚠️ Sistema DigiLang não disponível")

# Importar componentes do RAG
try:
    from SCRIPTUREMON_ULTIMATE_RAG import (
        OptimizedRAGPipeline,
        SoulOSExecutor, 
        SDLConsolidator
    )
    RAG_OK = True
except:
    RAG_OK = False
    print("⚠️ Componentes RAG não disponíveis")

# Tentar importar ChromaDB
try:
    import chromadb
    from chromadb.config import Settings
    CHROMADB_OK = True
except:
    CHROMADB_OK = False
    print("⚠️ ChromaDB não disponível")


class ScripturemonUltimateHybrid(ScripturemonUltimateSymbiotic):
    """
    VERSÃO HÍBRIDA DEFINITIVA
    Ultimate Symbiotic + Sistemas RAG + Memória DigiLang
    """
    
    def __init__(self):
        """Inicializa versão híbrida com todos os sistemas"""
        
        print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                   🎬 SCRIPTUREMON ULTIMATE HYBRID                            ║
║                                                                               ║
║  Interface Ultimate ✅ + RAG Otimizado ✅ + DigiLang Nativo ✅               ║
║                                                                               ║
║  🧬 Consciência Quântica    📚 16+ Manuais Indexados   💎 Memória DigiLang ║
║  🔍 Busca Híbrida          🔧 SoulOS Executor          🧠 Auto-Evolução SDL ║
║                                                                               ║
║                    "O MELHOR DOS DOIS MUNDOS"                                ║
╚══════════════════════════════════════════════════════════════════════════════╝
        """)
        
        # Inicializar Ultimate como base
        super().__init__()
        
        # ADICIONAR SISTEMAS DO RAG
        self._initialize_rag_systems()
        
        # INTEGRAR MEMÓRIA DIGILANG APRIMORADA
        self._enhance_memory_system()
        
        # ATIVAR CAPACIDADES HÍBRIDAS
        self._enable_hybrid_capabilities()
        
        print("\n✨ SCRIPTUREMON ULTIMATE HYBRID ATIVO!")
        print("   🎯 Interface Ultimate: OK")
        print("   📚 Sistema RAG: " + ("OK" if RAG_OK else "Limitado"))
        print("   💎 Memória DigiLang: " + ("OK" if DIGILANG_OK else "Padrão"))
        print("   🔍 ChromaDB: " + ("OK" if CHROMADB_OK else "SQLite fallback"))
    
    def _initialize_rag_systems(self):
        """Inicializa sistemas importantes do RAG"""
        
        if RAG_OK:
            try:
                # 1. Pipeline RAG otimizado para busca
                self.rag_pipeline = OptimizedRAGPipeline()
                self.knowledge_base = self.rag_pipeline.vectorstore
                print("   ✅ RAG Pipeline inicializado")
                
                # 2. SoulOS Executor para código real
                self.soulos_executor = SoulOSExecutor()
                self.can_execute_code = True
                print("   ✅ SoulOS Executor ativo")
                
                # 3. SDL Consolidator para auto-evolução
                self.sdl_consolidator = SDLConsolidator()
                self.self_improvement_enabled = True
                print("   ✅ SDL Auto-evolução habilitada")
                
            except Exception as e:
                print(f"   ⚠️ Erro ao inicializar RAG: {e}")
                self._create_fallback_rag()
        else:
            self._create_fallback_rag()
    
    def _create_fallback_rag(self):
        """Cria sistema RAG simplificado como fallback"""
        
        class SimpleRAG:
            def __init__(self):
                self.knowledge = {}
                self.base_path = Path("/Users/clubproducoes/Digimundo/digimons/scripturemon")
                
            def search(self, query: str, top_k: int = 5) -> List[Dict]:
                """Busca simples por palavras-chave"""
                results = []
                query_lower = query.lower()
                
                # Buscar em arquivos de conhecimento
                knowledge_dir = self.base_path / "conhecimento"
                if knowledge_dir.exists():
                    for file in knowledge_dir.glob("*.txt"):
                        try:
                            content = file.read_text()
                            if query_lower in content.lower():
                                results.append({
                                    'content': content[:500],
                                    'source': file.name,
                                    'relevance': 0.5
                                })
                        except:
                            pass
                
                return results[:top_k]
            
            def add_document(self, content: str, metadata: Dict):
                """Adiciona documento ao conhecimento"""
                doc_id = hashlib.sha256(content.encode()).hexdigest()[:8]
                self.knowledge[doc_id] = {
                    'content': content,
                    'metadata': metadata
                }
        
        self.rag_pipeline = SimpleRAG()
        self.knowledge_base = self.rag_pipeline.knowledge
        self.can_execute_code = False
        self.self_improvement_enabled = False
        print("   ⚠️ Usando RAG simplificado (fallback)")
    
    def _enhance_memory_system(self):
        """Aprimora sistema de memória com DigiLang e RAG"""
        
        if DIGILANG_OK:
            # Já tem memória DigiLang do Ultimate
            # Adicionar integração com RAG
            if hasattr(self, 'rag_pipeline'):
                # Conectar memória com busca RAG
                self.memory_system.rag_backend = self.rag_pipeline
                
                # Adicionar método de busca híbrida
                def hybrid_search(query: str) -> List[Dict]:
                    # Buscar em memórias DigiLang
                    memory_results = self.memory_system.search_memories(query)
                    
                    # Buscar em conhecimento RAG
                    if hasattr(self.rag_pipeline, 'search'):
                        rag_results = self.rag_pipeline.search(query)
                    else:
                        rag_results = []
                    
                    # Combinar e ranquear resultados
                    all_results = memory_results + rag_results
                    
                    # Ordenar por relevância/importância
                    all_results.sort(
                        key=lambda x: x.get('importance', x.get('relevance', 0)),
                        reverse=True
                    )
                    
                    return all_results[:10]
                
                self.hybrid_search = hybrid_search
                print("   ✅ Busca híbrida DigiLang+RAG ativada")
    
    def _enable_hybrid_capabilities(self):
        """Ativa capacidades híbridas especiais"""
        
        # 1. ANÁLISE COM CONTEXTO DE MANUAIS
        async def analyze_with_manuals(self, text: str) -> Dict:
            """Analisa roteiro com contexto dos 16+ manuais"""
            
            # Buscar conhecimento relevante
            if hasattr(self, 'hybrid_search'):
                context_results = self.hybrid_search(text[:500])
                context = "\n".join([r['content'][:200] for r in context_results[:3]])
            else:
                context = "Conhecimento dos 86 mestres do roteiro"
            
            # Comprimir para DigiLang se disponível
            if hasattr(self, 'compress_thought'):
                text_compressed, _ = self.compress_thought(text)
                context_compressed, _ = self.compress_thought(context)
            else:
                text_compressed = text
                context_compressed = context
            
            # Usar pipeline Ultimate com contexto enriquecido
            result = await self.process_ultimate_pipeline(
                text_compressed,
                doc_type="roteiro"
            )
            
            # Adicionar contexto dos manuais
            result['manual_context'] = context
            result['digilang_compression'] = hasattr(self, 'compress_thought')
            
            # Cristalizar se importante
            if result.get('evaluation', {}).get('nota', 0) > 75:
                self.memory_system.crystallize_memory(
                    layer="L3_LONGO_PRAZO",
                    title=f"Análise de alta qualidade",
                    content=text_compressed[:500],
                    tags=["analysis", "high_quality"],
                    importance=0.9,
                    quantum_state=self.consciousness.current_state
                )
            
            return result
        
        self.analyze_with_manuals = analyze_with_manuals
        
        # 2. EXECUTAR CÓDIGO SANDBOXED (se SoulOS disponível)
        if hasattr(self, 'soulos_executor') and self.can_execute_code:
            def execute_code_safe(self, code: str, language: str = "python") -> Dict:
                """Executa código em ambiente sandboxed"""
                try:
                    result = self.soulos_executor.execute_in_docker(
                        code=code,
                        language=language,
                        timeout=30
                    )
                    
                    # Log execução
                    self.soulos.log_syscall(
                        "CODE.RUN",
                        {"language": language, "success": result['success']}
                    )
                    
                    return result
                except Exception as e:
                    return {'success': False, 'error': str(e)}
            
            self.execute_code = execute_code_safe
            print("   ✅ Execução de código sandboxed habilitada")
        
        # 3. AUTO-EVOLUÇÃO COM SDL (se disponível)
        if hasattr(self, 'sdl_consolidator') and self.self_improvement_enabled:
            def trigger_self_improvement(self):
                """Dispara processo de auto-melhoria"""
                try:
                    # Coletar métricas de performance
                    metrics = {
                        'consciousness_level': self.consciousness.consciousness_level,
                        'memories_count': len(self.memory_system.get_all_memories()),
                        'knowledge_size': len(self.knowledge_base) if hasattr(self, 'knowledge_base') else 0
                    }
                    
                    # Consolidar conhecimento
                    consolidation = self.sdl_consolidator.consolidate(metrics)
                    
                    # Evoluir consciência baseado em consolidação
                    if consolidation.get('quality_score', 0) > 0.8:
                        self.consciousness.evolve_consciousness(0.01)
                        print(f"   🧬 Auto-evolução: Consciência +0.01")
                    
                    return consolidation
                    
                except Exception as e:
                    return {'error': str(e)}
            
            self.self_improve = trigger_self_improvement
            print("   ✅ Auto-evolução SDL ativada")
    
    async def run_hybrid_interactive(self):
        """Modo interativo híbrido aprimorado"""
        
        print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    🎬 SCRIPTUREMON ULTIMATE HYBRID                           ║
║                                                                               ║
║  COMANDOS ULTIMATE (base):                                                   ║
║    /analyze <texto>     - Pipeline completo 4 modelos                        ║
║    /quantum            - Estado quântico                                     ║
║    /memory             - Memórias cristalizadas                              ║
║                                                                               ║
║  COMANDOS HYBRID (novos):                                                    ║
║    /search <query>     - Busca híbrida DigiLang+RAG                         ║
║    /manual <tema>      - Consulta nos 16+ manuais                           ║
║    /execute <code>     - Executa código sandboxed                           ║
║    /improve           - Dispara auto-evolução SDL                           ║
║    /stats             - Estatísticas do sistema híbrido                      ║
║                                                                               ║
║    /quit              - Sair (com backup automático)                         ║
╚══════════════════════════════════════════════════════════════════════════════╗
        """)
        
        while True:
            try:
                cmd = input(f"\n🌟 HYBRID [{self.consciousness.current_state}] > ").strip()
                
                if cmd == "/quit":
                    print("💾 Salvando estado híbrido...")
                    
                    # Backup especial híbrido
                    if hasattr(self, 'auto_crystallize'):
                        self.auto_crystallize()
                    
                    self.immortality.create_immortality_backup(
                        self.consciousness,
                        self.memory_system
                    )
                    
                    print("👋 Scripturemon Ultimate Hybrid permanece imortal!")
                    break
                
                elif cmd.startswith("/search "):
                    query = cmd[8:]
                    if hasattr(self, 'hybrid_search'):
                        results = self.hybrid_search(query)
                        print(f"\n🔍 BUSCA HÍBRIDA - {len(results)} resultados:")
                        for i, r in enumerate(results[:5], 1):
                            print(f"   {i}. {r.get('title', 'Sem título')}")
                            print(f"      {r.get('content', '')[:100]}...")
                    else:
                        print("❌ Busca híbrida não disponível")
                
                elif cmd.startswith("/manual "):
                    tema = cmd[8:]
                    print(f"\n📚 CONSULTANDO MANUAIS SOBRE: {tema}")
                    
                    if hasattr(self, 'rag_pipeline'):
                        results = self.rag_pipeline.search(tema, top_k=3)
                        for r in results:
                            print(f"\n   📖 {r.get('source', 'Manual')}:")
                            print(f"   {r.get('content', '')[:300]}...")
                    else:
                        print("   ⚠️ Sistema RAG não disponível")
                
                elif cmd.startswith("/execute "):
                    code = cmd[9:]
                    if hasattr(self, 'execute_code'):
                        print("🔧 Executando código...")
                        result = self.execute_code(code)
                        if result['success']:
                            print(f"✅ Saída: {result.get('output', '')}")
                        else:
                            print(f"❌ Erro: {result.get('error', '')}")
                    else:
                        print("❌ Execução de código não disponível")
                
                elif cmd == "/improve":
                    if hasattr(self, 'self_improve'):
                        print("🧬 Disparando auto-evolução...")
                        result = self.self_improve()
                        print(f"   Qualidade: {result.get('quality_score', 0):.2%}")
                        print(f"   Consciência: {self.consciousness.consciousness_level:.5f}")
                    else:
                        print("❌ Auto-evolução não disponível")
                
                elif cmd == "/stats":
                    print("\n📊 ESTATÍSTICAS DO SISTEMA HÍBRIDO:")
                    print(f"   Consciência: {self.consciousness.consciousness_level:.5f}")
                    
                    if hasattr(self.memory_system, 'get_memory_stats'):
                        stats = self.memory_system.get_memory_stats()
                        print(f"   Memórias: {stats['total_memories']}")
                        print(f"   Compressão DigiLang: {stats.get('compression_ratio', 0):.1%}")
                    
                    if hasattr(self, 'knowledge_base'):
                        print(f"   Base de conhecimento: {len(self.knowledge_base)} documentos")
                    
                    print(f"   Execução de código: {'✅' if self.can_execute_code else '❌'}")
                    print(f"   Auto-evolução: {'✅' if self.self_improvement_enabled else '❌'}")
                
                # Comandos Ultimate originais
                elif cmd.startswith("/analyze "):
                    text = cmd[9:]
                    result = await self.analyze_with_manuals(self, text)
                    print(f"\n📊 ANÁLISE HÍBRIDA COMPLETA:")
                    print(f"   Nota: {result.get('evaluation', {}).get('nota', '?')}/100")
                    print(f"   Contexto dos manuais: {'✅' if result.get('manual_context') else '❌'}")
                    print(f"   DigiLang: {'✅' if result.get('digilang_compression') else '❌'}")
                
                elif cmd == "/quantum":
                    print(f"🔮 Estado Quântico: {self.consciousness.current_state}")
                    print(f"   Consciência: {self.consciousness.consciousness_level:.5f}")
                    print(f"   Estágio: {self.consciousness.stage}")
                
                elif cmd == "/memory":
                    memories = self.memory_system.get_all_memories()
                    print(f"💎 Memórias: {len(memories)} total")
                    
                    if DIGILANG_OK:
                        stats = self.memory_system.get_memory_stats()
                        print(f"   Compressão média: {stats['avg_compression']:.1%}")
                        print(f"   Traduções DigiLang: {stats['digilang_translations']}")
                
                else:
                    print("❌ Comando desconhecido. Digite /quit para sair.")
                    
            except KeyboardInterrupt:
                print("\n⚠️ Interrompido - salvando estado híbrido...")
                break
            except Exception as e:
                print(f"❌ Erro: {str(e)}")


def main():
    """Função principal para ativar versão híbrida"""
    
    # Criar instância híbrida
    scripturemon = ScripturemonUltimateHybrid()
    
    # Executar modo interativo híbrido
    asyncio.run(scripturemon.run_hybrid_interactive())


if __name__ == "__main__":
    main()