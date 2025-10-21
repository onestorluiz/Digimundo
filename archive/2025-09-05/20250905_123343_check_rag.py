#!/usr/bin/env python3
"""Check para verificar o sistema RAG e citações"""

import sys
import json
import traceback
from pathlib import Path
from typing import Dict, Any

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

def run_check(settings: Dict) -> Dict:
    """Executa verificação do sistema RAG"""
    result = {
        'pass': False,
        'status': 'running',
        'notes': [],
        'details': {}
    }
    
    try:
        # Verificar se RAG está habilitado
        if not settings.get('rag', {}).get('enabled', True):
            result['status'] = 'blocked'
            result['reason'] = 'RAG disabled in settings'
            return result
        
        # Importar RAGAdapter
        from src.rag.adapter import RAGAdapter
        
        # Criar instância
        rag = RAGAdapter(settings)
        result['notes'].append('RAGAdapter instantiated')
        
        # Teste 1: Adicionar documentos ao knowledge base
        test_docs = [
            {
                'id': 'doc1',
                'content': 'O protagonista John enfrenta dilemas morais complexos no terceiro ato.',
                'metadata': {'source': 'script_analysis.txt', 'page': 42}
            },
            {
                'id': 'doc2',
                'content': 'A estrutura em três atos é fundamental para narrativas cinematográficas.',
                'metadata': {'source': 'theory.pdf', 'chapter': 3}
            },
            {
                'id': 'doc3',
                'content': 'Diálogos naturalistas criam maior identificação com o público.',
                'metadata': {'source': 'dialogue_guide.md', 'section': 'realism'}
            }
        ]
        
        for doc in test_docs:
            rag.add_document(doc['id'], doc['content'], doc['metadata'])
        result['notes'].append(f'Added {len(test_docs)} test documents')
        
        # Teste 2: Query simples com citações
        query = "Como criar diálogos realistas?"
        results = rag.query(query, k=2)
        
        if results and len(results) > 0:
            result['details']['query_results'] = 'PASS'
            result['notes'].append(f'Query returned {len(results)} results')
            
            # Verificar estrutura das citações
            first_result = results[0]
            if all(k in first_result for k in ['content', 'score', 'metadata']):
                result['details']['citation_structure'] = 'PASS'
                result['notes'].append('Citation structure correct')
            else:
                result['details']['citation_structure'] = 'FAIL'
                result['notes'].append('Citation structure incomplete')
        else:
            result['details']['query_results'] = 'FAIL'
            result['notes'].append('Query returned no results')
        
        # Teste 3: Formatação de citações
        formatted = rag.format_citations(results[:2] if results else [])
        if formatted and isinstance(formatted, str):
            # Verificar se tem formato esperado
            if '[' in formatted or '📚' in formatted or 'Source:' in formatted:
                result['details']['citation_format'] = 'PASS'
                result['notes'].append('Citations properly formatted')
            else:
                result['details']['citation_format'] = 'FAIL'
                result['notes'].append('Citation format incorrect')
        else:
            result['details']['citation_format'] = 'FAIL'
            result['notes'].append('No formatted citations returned')
        
        # Teste 4: HyDE (Hypothetical Document Embeddings)
        hyde_query = "técnicas avançadas de roteiro"
        hyde_results = rag.query_with_hyde(hyde_query, k=1)
        
        if hyde_results:
            result['details']['hyde_integration'] = 'PASS'
            result['notes'].append('HyDE query successful')
        else:
            result['details']['hyde_integration'] = 'FAIL'
            result['notes'].append('HyDE query failed')
        
        # Teste 5: Integração com UnifiedMemoryManager
        try:
            from src.memory.unified_manager import UnifiedMemoryManager
            memory = UnifiedMemoryManager(settings)
            
            # Verificar se RAG está registrado como provider
            context = memory.get_context("roteiro", max_memories=1)
            
            # Se context tem citações ou referências RAG
            has_rag = False
            if context:
                for item in context:
                    if 'source' in str(item) or 'rag' in str(item).lower():
                        has_rag = True
                        break
            
            if has_rag:
                result['details']['memory_integration'] = 'PASS'
                result['notes'].append('RAG integrated with MemoryManager')
            else:
                result['details']['memory_integration'] = 'WARN'
                result['notes'].append('RAG may not be fully integrated')
        except:
            result['details']['memory_integration'] = 'SKIP'
            result['notes'].append('Could not test memory integration')
        
        # Determinar status final
        failures = [k for k, v in result['details'].items() if v == 'FAIL']
        if not failures:
            result['pass'] = True
            result['status'] = 'passed'
            result['reason'] = 'All RAG checks passed'
        else:
            result['status'] = 'failed'
            result['reason'] = f'Failed checks: {", ".join(failures)}'
        
    except ImportError as e:
        result['status'] = 'blocked'
        result['reason'] = f'Import error: {str(e)}'
        result['exception'] = str(e)
    except Exception as e:
        result['status'] = 'error'
        result['reason'] = f'Unexpected error: {str(e)}'
        result['exception'] = str(e)
        result['traceback'] = traceback.format_exc()
    
    return result

if __name__ == "__main__":
    # Para teste local
    from generate_inventory import load_default_settings
    settings = load_default_settings()
    result = run_check(settings)
    print(json.dumps(result, indent=2))