#!/usr/bin/env python3
"""
PIPELINES & EVOLUÇÃO - HARMONIA V3.2
Sistema de pipelines com evolução e stages
"""

import os
import sys
import json
import time
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional, Callable
import traceback

# Setup paths
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("harmonia.pipeline")


class EvolutionPipeline:
    """Pipeline evolutivo com múltiplos estágios."""
    
    def __init__(self):
        self.stages = []
        self.stats = {
            'total_stages': 0,
            'executed': 0,
            'succeeded': 0,
            'failed': 0,
            'skipped': 0,
            'timings_ms': [],
            'errors': []
        }
        self.context = {}  # Contexto compartilhado entre stages
        
    def add_stage(self, name: str, func: Callable, 
                  required: bool = True,
                  timeout_ms: Optional[int] = None) -> 'EvolutionPipeline':
        """Adiciona um estágio ao pipeline."""
        self.stages.append({
            'name': name,
            'func': func,
            'required': required,
            'timeout_ms': timeout_ms,
            'status': 'pending'
        })
        self.stats['total_stages'] += 1
        return self
    
    def execute(self) -> Dict[str, Any]:
        """Executa o pipeline completo."""
        pipeline_start = time.perf_counter()
        results = []
        
        for stage in self.stages:
            stage_result = {
                'name': stage['name'],
                'required': stage['required'],
                'status': 'pending',
                'timing_ms': 0,
                'output': None,
                'error': None
            }
            
            try:
                # Log início
                logger.info(f"🔄 Executando stage: {stage['name']}")
                
                # Executar stage
                stage_start = time.perf_counter()
                
                # Chamar função com contexto
                output = stage['func'](self.context)
                
                stage_time = (time.perf_counter() - stage_start) * 1000
                
                # Atualizar resultado
                stage_result['status'] = 'success'
                stage_result['timing_ms'] = stage_time
                stage_result['output'] = output
                
                # Atualizar contexto se retornou dict
                if isinstance(output, dict):
                    self.context.update(output)
                
                self.stats['succeeded'] += 1
                self.stats['timings_ms'].append(stage_time)
                
                logger.info(f"✅ Stage {stage['name']}: {stage_time:.2f}ms")
                
            except Exception as e:
                # Capturar erro
                error_msg = str(e)
                stage_result['status'] = 'failed'
                stage_result['error'] = error_msg
                
                self.stats['failed'] += 1
                self.stats['errors'].append({
                    'stage': stage['name'],
                    'error': error_msg,
                    'traceback': traceback.format_exc()
                })
                
                logger.error(f"❌ Stage {stage['name']} falhou: {error_msg}")
                
                # Se é required, parar pipeline
                if stage['required']:
                    logger.error(f"Pipeline interrompido - stage required falhou")
                    break
                else:
                    self.stats['skipped'] += 1
                    
            finally:
                self.stats['executed'] += 1
                results.append(stage_result)
        
        # Calcular tempo total
        pipeline_time = (time.perf_counter() - pipeline_start) * 1000
        
        # Compilar resultado final
        return {
            'timestamp': datetime.now().isoformat(),
            'total_time_ms': pipeline_time,
            'stages_results': results,
            'stats': self.stats,
            'context': self.context
        }


class SynthesisPipeline(EvolutionPipeline):
    """Pipeline de síntese - 4 estágios do Scripturemon."""
    
    def __init__(self):
        super().__init__()
        self.setup_stages()
    
    def setup_stages(self):
        """Configura os 4 estágios de síntese."""
        
        # Stage 1: Telepathy (compartilhamento de contexto)
        def telepathy_stage(ctx):
            logger.info("🧠 Telepathy: sincronizando contexto")
            
            # Simular sincronização telepática
            shared_knowledge = {
                'entities': ['Digimon', 'SoulOS', 'Scripturemon'],
                'concepts': ['evolution', 'synthesis', 'harmony'],
                'timestamp': time.time()
            }
            
            # Broadcast (simulado)
            ctx['telepathy'] = {
                'shared': shared_knowledge,
                'nodes': 3,
                'sync_ms': 15.0
            }
            
            return ctx['telepathy']
        
        # Stage 2: Canonize (normalização)
        def canonize_stage(ctx):
            logger.info("📖 Canonize: normalizando estruturas")
            
            # Normalizar dados do contexto
            canon_rules = {
                'lowercase': True,
                'remove_special': True,
                'standardize_dates': True
            }
            
            # Aplicar canonização
            canonized = {
                'rules_applied': list(canon_rules.keys()),
                'transformations': 42,
                'compression_ratio': 0.73
            }
            
            ctx['canonized'] = canonized
            return canonized
        
        # Stage 3: Crystalize (consolidação)
        def crystalize_stage(ctx):
            logger.info("💎 Crystalize: consolidando conhecimento")
            
            # Consolidar informações
            if 'telepathy' in ctx and 'canonized' in ctx:
                crystal = {
                    'essence': 'consolidated_knowledge',
                    'facets': len(ctx.get('telepathy', {}).get('entities', [])),
                    'purity': 0.95,
                    'formations': ['memory', 'rag', 'telepathy']
                }
            else:
                crystal = {
                    'essence': 'partial_knowledge',
                    'facets': 1,
                    'purity': 0.60,
                    'formations': []
                }
            
            ctx['crystal'] = crystal
            return crystal
        
        # Stage 4: Immortalize (persistência)
        def immortalize_stage(ctx):
            logger.info("♾️ Immortalize: eternizando essência")
            
            # Persistir resultado final
            immortal = {
                'id': f"harmony_{int(time.time())}",
                'checksum': 'sha256_mock_abc123',
                'persisted': True,
                'location': 'memory/immortal',
                'stages_completed': len([k for k in ctx.keys() if k != 'immortal'])
            }
            
            # Simular gravação
            time.sleep(0.01)  # Simular I/O
            
            ctx['immortal'] = immortal
            return immortal
        
        # Adicionar stages ao pipeline
        self.add_stage('telepathy', telepathy_stage, required=True)
        self.add_stage('canonize', canonize_stage, required=True)
        self.add_stage('crystalize', crystalize_stage, required=True)
        self.add_stage('immortalize', immortalize_stage, required=True)


class CompressionPipeline(EvolutionPipeline):
    """Pipeline de compressão com múltiplas estratégias."""
    
    def __init__(self):
        super().__init__()
        self.setup_stages()
    
    def setup_stages(self):
        """Configura stages de compressão."""
        
        # Stage 1: Análise
        def analyze_stage(ctx):
            logger.info("🔍 Analisando conteúdo para compressão")
            
            # Simular análise de texto
            analysis = {
                'content_type': 'screenplay',
                'tokens': 15000,
                'entropy': 0.82,
                'recommended_strategy': 'tpd+canon'
            }
            
            ctx['analysis'] = analysis
            return analysis
        
        # Stage 2: Canonização
        def canon_stage(ctx):
            logger.info("📝 Aplicando canonização")
            
            if ctx.get('analysis', {}).get('recommended_strategy', '').find('canon') >= 0:
                canon_result = {
                    'applied': True,
                    'reduction_ratio': 0.15,
                    'tokens_saved': 2250
                }
            else:
                canon_result = {
                    'applied': False,
                    'reason': 'not recommended for content type'
                }
            
            ctx['canon'] = canon_result
            return canon_result
        
        # Stage 3: Token Pair Encoding
        def tpd_stage(ctx):
            logger.info("🔢 Aplicando Token Pair Dictionary")
            
            if ctx.get('analysis', {}).get('recommended_strategy', '').find('tpd') >= 0:
                tpd_result = {
                    'applied': True,
                    'dictionary_size': 3000,
                    'compression_ratio': 0.28,
                    'tokens_saved': 4200
                }
            else:
                tpd_result = {
                    'applied': False,
                    'reason': 'low entropy content'
                }
            
            ctx['tpd'] = tpd_result
            return tpd_result
        
        # Stage 4: Finalização
        def finalize_stage(ctx):
            logger.info("✨ Finalizando compressão")
            
            total_saved = 0
            if ctx.get('canon', {}).get('applied'):
                total_saved += ctx['canon'].get('tokens_saved', 0)
            if ctx.get('tpd', {}).get('applied'):
                total_saved += ctx['tpd'].get('tokens_saved', 0)
            
            final = {
                'original_tokens': ctx.get('analysis', {}).get('tokens', 15000),
                'compressed_tokens': ctx.get('analysis', {}).get('tokens', 15000) - total_saved,
                'total_reduction': total_saved,
                'final_ratio': 1 - (total_saved / ctx.get('analysis', {}).get('tokens', 15000))
            }
            
            ctx['final'] = final
            return final
        
        # Adicionar stages
        self.add_stage('analyze', analyze_stage, required=True)
        self.add_stage('canonize', canon_stage, required=False)
        self.add_stage('tpd_encode', tpd_stage, required=False)
        self.add_stage('finalize', finalize_stage, required=True)


def test_all_pipelines() -> Dict[str, Any]:
    """Testa todos os pipelines evolutivos."""
    
    results = {
        'timestamp': datetime.now().isoformat(),
        'pipelines': {}
    }
    
    # 1. Pipeline de Síntese
    logger.info("=" * 50)
    logger.info("🚀 Testando Pipeline de Síntese (4 estágios)")
    
    synthesis = SynthesisPipeline()
    synthesis_result = synthesis.execute()
    
    results['pipelines']['synthesis'] = {
        'name': 'Synthesis Pipeline (4 stages)',
        'description': 'telepathy → canonize → crystalize → immortalize',
        'total_time_ms': synthesis_result['total_time_ms'],
        'stages_completed': synthesis.stats['succeeded'],
        'stages_failed': synthesis.stats['failed'],
        'avg_stage_time_ms': (
            sum(synthesis.stats['timings_ms']) / len(synthesis.stats['timings_ms'])
            if synthesis.stats['timings_ms'] else 0
        ),
        'final_context': synthesis_result['context']
    }
    
    # 2. Pipeline de Compressão
    logger.info("=" * 50)
    logger.info("🗜️ Testando Pipeline de Compressão")
    
    compression = CompressionPipeline()
    compression_result = compression.execute()
    
    results['pipelines']['compression'] = {
        'name': 'Compression Pipeline',
        'description': 'analyze → canonize → tpd → finalize',
        'total_time_ms': compression_result['total_time_ms'],
        'stages_completed': compression.stats['succeeded'],
        'stages_failed': compression.stats['failed'],
        'compression_achieved': compression_result['context'].get('final', {}).get('final_ratio', 1),
        'tokens_saved': compression_result['context'].get('final', {}).get('total_reduction', 0)
    }
    
    # 3. Pipeline Customizado (exemplo de evolução)
    logger.info("=" * 50)
    logger.info("🌟 Testando Pipeline de Evolução Customizado")
    
    evolution = EvolutionPipeline()
    
    # Adicionar stages customizados
    evolution.add_stage('init', lambda ctx: {'level': 1, 'power': 100})
    evolution.add_stage('evolve', lambda ctx: {'level': ctx.get('level', 1) + 1, 'power': ctx.get('power', 100) * 1.5})
    evolution.add_stage('mega_evolve', lambda ctx: {'level': 'mega', 'power': ctx.get('power', 100) * 2})
    
    evolution_result = evolution.execute()
    
    results['pipelines']['evolution'] = {
        'name': 'Custom Evolution Pipeline',
        'description': 'init → evolve → mega_evolve',
        'total_time_ms': evolution_result['total_time_ms'],
        'stages_completed': evolution.stats['succeeded'],
        'final_level': evolution_result['context'].get('level'),
        'final_power': evolution_result['context'].get('power')
    }
    
    # Estatísticas gerais
    results['summary'] = {
        'total_pipelines': len(results['pipelines']),
        'all_successful': all(
            p.get('stages_failed', 0) == 0 
            for p in results['pipelines'].values()
        ),
        'total_time_ms': sum(
            p.get('total_time_ms', 0) 
            for p in results['pipelines'].values()
        ),
        'evolution_demonstrated': True
    }
    
    return results


def main():
    """Executa demonstração completa de pipelines."""
    
    # Testar pipelines
    results = test_all_pipelines()
    
    # Salvar relatórios
    output_dir = Path("reports/harmonia_v32/pipelines")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Pipeline execution report
    with open(output_dir / "pipeline_execution.json", 'w') as f:
        json.dump(results, f, indent=2)
    
    # Evolution stages documentation
    evolution_docs = {
        'timestamp': datetime.now().isoformat(),
        'standard_pipelines': {
            'synthesis': {
                'stages': ['telepathy', 'canonize', 'crystalize', 'immortalize'],
                'purpose': 'Transform and persist knowledge through 4 evolutionary stages',
                'required_context': None,
                'output': 'Immortalized knowledge crystal'
            },
            'compression': {
                'stages': ['analyze', 'canonize', 'tpd_encode', 'finalize'],
                'purpose': 'Compress content using multiple strategies',
                'required_context': 'Text content to compress',
                'output': 'Compressed representation with metrics'
            }
        },
        'evolution_mechanics': {
            'stage_chaining': 'Each stage receives context from previous stages',
            'error_handling': 'Required stages stop pipeline on failure',
            'optional_stages': 'Can be skipped without stopping pipeline',
            'context_sharing': 'Dict context passed and updated through stages',
            'timing_tracking': 'Each stage timing measured in milliseconds'
        },
        'custom_pipelines': {
            'how_to': 'Create EvolutionPipeline and add_stage() with callables',
            'example': """
pipeline = EvolutionPipeline()
pipeline.add_stage('fetch', fetch_data, required=True)
pipeline.add_stage('process', process_data, required=True)
pipeline.add_stage('cache', cache_results, required=False)
result = pipeline.execute()
            """
        }
    }
    
    with open(output_dir / "evolution_stages.json", 'w') as f:
        json.dump(evolution_docs, f, indent=2)
    
    # Log resumo
    logger.info("=" * 50)
    logger.info(f"✅ Pipelines testados: {results['summary']['total_pipelines']}")
    logger.info(f"✅ Tempo total: {results['summary']['total_time_ms']:.2f}ms")
    logger.info(f"✅ Todos bem-sucedidos: {results['summary']['all_successful']}")
    
    return results


if __name__ == "__main__":
    main()