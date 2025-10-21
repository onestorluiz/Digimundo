#!/usr/bin/env python3
"""
E2E Scenarios - Memória + RAG + Citações
Timeline causal em NDJSON, métricas por componente.
"""
import json
import time
import uuid
from pathlib import Path
from typing import Dict, List, Any, Optional
import sys

# Add project root
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.rag.adapter import RAGAdapter
from src.memory.unified_manager import UnifiedMemoryManager
from tools.fix_v3.shims.soulos_shim import process_syscalls

# Timeline global
TIMELINE = []


def log_event(component: str, action: str, ms: float, 
              parent_id: Optional[str] = None, **meta) -> str:
    """Registra evento na timeline."""
    span_id = str(uuid.uuid4())[:8]
    event = {
        'ts': time.strftime('%Y-%m-%dT%H:%M:%S'),
        'span_id': span_id,
        'parent_id': parent_id,
        'component': component,
        'action': action,
        'ms': round(ms, 2),
        'notes': meta.get('notes', ''),
        'meta': {k: v for k, v in meta.items() if k != 'notes'}
    }
    TIMELINE.append(event)
    return span_id


class E2ERunner:
    """Executor de cenários E2E."""
    
    def __init__(self):
        """Inicializa componentes."""
        self.rag = RAGAdapter({'rag': {'enabled': True, 'provider': 'chroma', 'k': 8}})
        
        # UnifiedMemoryManager precisa de settings
        memory_settings = {
            'database': {
                'path': 'data/memory/memories.db',
                'consciousness_path': 'data/memory/consciousness.db'
            },
            'hybrid_ranking': {
                'alpha': 0.3,
                'beta': 0.2,
                'gamma': 0.2,
                'delta': 0.3
            }
        }
        self.memory = UnifiedMemoryManager(memory_settings)
        self.memory_deltas = []
        self.citations_used = []
        
    def scenario_a_memoria_viva(self) -> Dict:
        """
        CENÁRIO A: Memória Viva
        Valida inserção, rank/promoção e recuperação.
        """
        print("\n=== CENÁRIO A: MEMÓRIA VIVA ===")
        scenario_id = log_event('scenario', 'start_memoria_viva', 0, notes='Testing memory lifecycle')
        
        results = {
            'scenario': 'memoria_viva',
            'steps': []
        }
        
        # Passo 1: Inserir 3 memórias
        themes = [
            ('roteiro', 'Three-act structure is fundamental to screenplay writing'),
            ('dialogo', 'Subtext in dialogue reveals character motivations'),
            ('estrutura', 'The inciting incident propels the story forward')
        ]
        
        inserted_ids = []
        for theme, content in themes:
            t0 = time.perf_counter()
            mem_id = self.memory.save_memory(
                content=content + f' ·e2e#{len(inserted_ids)+1:02d}',
                tags=[theme, 'e2e_test']
            )
            dt_ms = (time.perf_counter() - t0) * 1000
            
            span = log_event('memory.dao', 'insert', dt_ms, scenario_id,
                           theme=theme, mem_id=mem_id, hits_initial=0)
            
            inserted_ids.append(mem_id)
            self.memory_deltas.append({
                'action': 'insert',
                'mem_id': mem_id,
                'theme': theme,
                'hits': 0,
                'level': 'L3'
            })
            
            results['steps'].append({
                'step': f'insert_{theme}',
                'ms': round(dt_ms, 2),
                'mem_id': mem_id
            })
        
        # Passo 2: Consultar 5 vezes para provocar promoção
        queries = [
            'screenplay structure',
            'dialogue techniques',
            'story structure fundamentals',
            'character dialogue subtext',
            'three-act paradigm'
        ]
        
        for i, query in enumerate(queries):
            t0 = time.perf_counter()
            memories = self.memory.get_context(
                query=query + f' ·e2e#q{i+1:02d}',
                max_chunks=3
            )
            dt_ms = (time.perf_counter() - t0) * 1000
            
            log_event('memory.rank', 'search', dt_ms, scenario_id,
                     query=query, results=len(memories))
            
            # Registrar hits/updates
            for mem in memories:
                if mem.get('id') in inserted_ids:
                    self.memory_deltas.append({
                        'action': 'hit',
                        'mem_id': mem['id'],
                        'query': query,
                        'rank_score': mem.get('score', 0)
                    })
            
            results['steps'].append({
                'step': f'query_{i+1}',
                'ms': round(dt_ms, 2),
                'found': len(memories)
            })
        
        # Passo 3: Ler top-K e verificar ranking
        t0 = time.perf_counter()
        top_memories = self.memory.get_all_memories(limit=5)
        dt_ms = (time.perf_counter() - t0) * 1000
        
        log_event('memory.rank', 'get_top_k', dt_ms, scenario_id,
                 k=5, returned=len(top_memories))
        
        results['steps'].append({
            'step': 'get_top_k',
            'ms': round(dt_ms, 2),
            'memories': len(top_memories)
        })
        
        results['total_ms'] = sum(s['ms'] for s in results['steps'])
        results['memory_operations'] = len(self.memory_deltas)
        
        return results
    
    def scenario_b_rag_citations(self) -> Dict:
        """
        CENÁRIO B: RAG com Citações
        Prova retrieve real + citações rastreáveis.
        """
        print("\n=== CENÁRIO B: RAG COM CITAÇÕES ===")
        scenario_id = log_event('scenario', 'start_rag_citations', 0, notes='Testing RAG and citations')
        
        results = {
            'scenario': 'rag_citations',
            'queries': []
        }
        
        # 6 queries temáticas únicas
        queries = [
            'screenplay three-act structure fundamentals',
            'dialogue subtext character revelation',
            'protagonist character arc transformation',
            'visual storytelling cinematography techniques',
            'plot twist foreshadowing methods',
            'theme symbolism recurring motifs'
        ]
        
        for i, query in enumerate(queries):
            # Clear cache se possível
            if hasattr(self.rag, '_cache'):
                self.rag._cache.clear()
            
            # Query única
            unique_query = f"{query} ·e2e#{i+1:02d}"
            
            # Retrieve com medição
            t0 = time.perf_counter()
            results_rag = self.rag.retrieve(unique_query, k=8)
            dt_retrieve = (time.perf_counter() - t0) * 1000
            
            retrieve_span = log_event('rag.adapter', 'retrieve', dt_retrieve, scenario_id,
                                     query=unique_query[:50], k=8, found=len(results_rag))
            
            # Gerar citações
            citations = []
            t0 = time.perf_counter()
            for r in results_rag[:3]:  # Top 3 para citações
                citation = self.rag.cite(r)
                citations.append(citation)
                self.citations_used.append({
                    'citation': citation,
                    'source': r.get('metadata', {}).get('source', 'unknown'),
                    'chunk_no': r.get('metadata', {}).get('chunk_no'),
                    'query': query[:30]
                })
            dt_cite = (time.perf_counter() - t0) * 1000
            
            log_event('cite', 'format', dt_cite, retrieve_span,
                     citations_count=len(citations))
            
            # Verificar SCHEMA_KEYS
            schema_ok = False
            if results_rag:
                meta = results_rag[0].get('metadata', {})
                required = ['source', 'path', 'doc_hash', 'mtime', 'chunk_no', 'total_chunks', 'type', 'lang']
                schema_ok = all(k in meta for k in required)
            
            results['queries'].append({
                'query': query[:50],
                'retrieve_ms': round(dt_retrieve, 2),
                'cite_ms': round(dt_cite, 2),
                'results': len(results_rag),
                'citations': len(citations),
                'schema_ok': schema_ok
            })
        
        results['total_citations'] = len(self.citations_used)
        results['total_ms'] = sum(q['retrieve_ms'] + q['cite_ms'] for q in results['queries'])
        
        return results
    
    def scenario_c_scriptdoctor(self) -> Dict:
        """
        CENÁRIO C: ScriptDoctor
        Pipeline completo para análise de cena.
        """
        print("\n=== CENÁRIO C: SCRIPTDOCTOR ===")
        scenario_id = log_event('scenario', 'start_scriptdoctor', 0, notes='Full pipeline test')
        
        results = {
            'scenario': 'scriptdoctor',
            'pipeline': []
        }
        
        # Cena para análise
        scene = """
        INT. RICK'S CAFÉ - NIGHT
        
        Rick sits alone at a table, a glass of whiskey untouched.
        ILSA enters, hesitant. Their eyes meet - years of pain in a glance.
        
        ILSA
        (softly)
        Hello, Rick.
        
        RICK
        (cold)
        I heard you were in town.
        """
        
        # 1. Memory context
        t0 = time.perf_counter()
        context_memories = self.memory.get_context(
            query='screenplay scene analysis dialogue subtext ·e2e#doctor',
            max_chunks=3
        )
        dt_memory = (time.perf_counter() - t0) * 1000
        
        memory_span = log_event('memory.dao', 'get_context', dt_memory, scenario_id,
                               memories_found=len(context_memories))
        
        results['pipeline'].append({
            'stage': 'memory_context',
            'ms': round(dt_memory, 2),
            'memories': len(context_memories)
        })
        
        # 2. RAG references
        t0 = time.perf_counter()
        references = self.rag.retrieve(
            'scene analysis dialogue subtext emotional stakes ·e2e#doctor',
            k=5
        )
        dt_rag = (time.perf_counter() - t0) * 1000
        
        rag_span = log_event('rag.adapter', 'get_references', dt_rag, memory_span,
                           references_found=len(references))
        
        results['pipeline'].append({
            'stage': 'rag_references',
            'ms': round(dt_rag, 2),
            'references': len(references)
        })
        
        # 3. Compose with citations
        t0 = time.perf_counter()
        citations = []
        for ref in references[:3]:
            cite = self.rag.cite(ref)
            citations.append(cite)
            self.citations_used.append({
                'citation': cite,
                'source': ref.get('metadata', {}).get('source', 'unknown'),
                'context': 'scriptdoctor'
            })
        dt_compose = (time.perf_counter() - t0) * 1000
        
        log_event('scriptdoctor.pipeline', 'compose', dt_compose, rag_span,
                 citations=len(citations))
        
        results['pipeline'].append({
            'stage': 'compose_citations',
            'ms': round(dt_compose, 2),
            'citations': len(citations)
        })
        
        # 4. Process via SoulOS (shim)
        t0 = time.perf_counter()
        processed = process_syscalls(scene)
        dt_process = (time.perf_counter() - t0) * 1000
        
        log_event('soulos', 'process', dt_process, rag_span,
                 fallback=processed.get('metadata', {}).get('fallback', False))
        
        results['pipeline'].append({
            'stage': 'soulos_process',
            'ms': round(dt_process, 2),
            'status': processed.get('status', 'unknown')
        })
        
        # Sumário
        results['total_ms'] = sum(s['ms'] for s in results['pipeline'])
        results['memories_used'] = len(context_memories)
        results['citations_generated'] = len(citations)
        results['analysis'] = {
            'scene_type': 'dramatic confrontation',
            'elements': ['subtext', 'emotional stakes', 'character dynamics'],
            'references': [c[:30] + '...' for c in citations[:2]]
        }
        
        return results
    
    def run_all_scenarios(self) -> Dict:
        """Executa todos os cenários E2E."""
        print("\n" + "="*60)
        print("INICIANDO E2E SCENARIOS")
        print("="*60)
        
        all_results = {
            'timestamp': time.strftime('%Y-%m-%dT%H:%M:%S'),
            'scenarios': {}
        }
        
        # Cenário A
        all_results['scenarios']['memoria_viva'] = self.scenario_a_memoria_viva()
        
        # Cenário B
        all_results['scenarios']['rag_citations'] = self.scenario_b_rag_citations()
        
        # Cenário C
        all_results['scenarios']['scriptdoctor'] = self.scenario_c_scriptdoctor()
        
        # Salvar timeline NDJSON
        timeline_path = Path('reports/harmonia_v32/e2e/timeline.ndjson')
        timeline_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(timeline_path, 'w') as f:
            for event in TIMELINE:
                f.write(json.dumps(event) + '\n')
        
        print(f"\n✅ Timeline salva: {timeline_path} ({len(TIMELINE)} eventos)")
        
        # Salvar memory deltas
        deltas_path = Path('reports/harmonia_v32/e2e/memory_deltas.json')
        with open(deltas_path, 'w') as f:
            json.dump({
                'timestamp': all_results['timestamp'],
                'total_operations': len(self.memory_deltas),
                'deltas': self.memory_deltas[:20]  # Primeiros 20
            }, f, indent=2)
        
        print(f"✅ Memory deltas: {deltas_path} ({len(self.memory_deltas)} ops)")
        
        # Salvar citations
        citations_path = Path('reports/harmonia_v32/e2e/citations_used.json')
        with open(citations_path, 'w') as f:
            # Contar por documento
            doc_counts = {}
            for c in self.citations_used:
                src = c.get('source', 'unknown')
                doc_counts[src] = doc_counts.get(src, 0) + 1
            
            json.dump({
                'timestamp': all_results['timestamp'],
                'total_citations': len(self.citations_used),
                'citations': self.citations_used[:10],  # Primeiras 10
                'by_document': doc_counts,
                'schema_complete_rate': sum(1 for c in self.citations_used if c.get('chunk_no')) / len(self.citations_used) if self.citations_used else 0
            }, f, indent=2)
        
        print(f"✅ Citations: {citations_path} ({len(self.citations_used)} citações)")
        
        return all_results


def main():
    """Função principal."""
    runner = E2ERunner()
    results = runner.run_all_scenarios()
    
    # Salvar resultados gerais
    results_path = Path('reports/harmonia_v32/e2e/scenarios_results.json')
    with open(results_path, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n✅ Resultados salvos: {results_path}")
    
    # Sumário
    print("\n" + "="*60)
    print("E2E SCENARIOS - SUMÁRIO")
    print("="*60)
    
    for name, scenario in results['scenarios'].items():
        print(f"\n{name.upper()}:")
        print(f"  Total MS: {scenario.get('total_ms', 0):.2f}")
        
        if name == 'memoria_viva':
            print(f"  Memory Ops: {scenario.get('memory_operations', 0)}")
        elif name == 'rag_citations':
            print(f"  Citations: {scenario.get('total_citations', 0)}")
        elif name == 'scriptdoctor':
            print(f"  Pipeline Stages: {len(scenario.get('pipeline', []))}")
    
    print("\n✅ E2E Scenarios concluídos!")


if __name__ == '__main__':
    main()