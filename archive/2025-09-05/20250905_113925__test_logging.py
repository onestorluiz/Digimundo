#!/usr/bin/env python3
"""
Teste do sistema de logging padronizado.
Gera exemplos de logs para o relatório da FASE_11.
"""

import sys
from pathlib import Path

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.utils.logging_setup import setup_logging, get_logger, get_orchestrator_logger, get_memory_logger, get_rag_logger
from src.memory.unified_manager import UnifiedMemoryManager
from src.rag.adapter import RAGAdapter


def main():
    print("=" * 60)
    print("TESTE DE LOGGING PADRONIZADO")
    print("=" * 60)
    
    # 1. Testar diferentes níveis
    print("\n1. TESTANDO NÍVEIS DE LOG")
    print("-" * 40)
    
    test_logger = get_logger("test.module")
    
    test_logger.debug("Mensagem de debug - detalhes de implementação")
    test_logger.info("Mensagem informativa - operação normal")
    test_logger.warning("Aviso - algo para prestar atenção")
    test_logger.error("Erro - algo deu errado mas continuando")
    test_logger.critical("Crítico - falha grave do sistema")
    
    # 2. Testar logger do orquestrador
    print("\n2. TESTANDO LOGGER DO ORQUESTRADOR")
    print("-" * 40)
    
    orch_logger = get_orchestrator_logger()
    orch_logger.info("Pipeline quádruplo iniciado")
    orch_logger.info("Executando modelo llama3.2:3b para papel extractor")
    orch_logger.info("Modelo llama3.2:3b (extractor) completado em 2.45s")
    orch_logger.warning("Modelo mistral:instruct (analyzer) retornou sem resposta")
    orch_logger.error("Timeout no modelo scripturemon-maestro (evaluator) após 30s")
    
    # 3. Testar logger de memória
    print("\n3. TESTANDO LOGGER DE MEMÓRIA")
    print("-" * 40)
    
    # Criar UnifiedMemoryManager para gerar logs reais
    settings = {
        'rag': {'enabled': True},
        'memory': {
            'time_weighted_retrieval': True,
            'promote_on_hits': 5
        }
    }
    
    manager = UnifiedMemoryManager(settings)
    
    # Salvar memória
    mem_id = manager.save_memory(
        "Teste de conteúdo para logging",
        tags=['teste', 'log'],
        importance=0.8
    )
    
    # Buscar contexto
    context = manager.get_context("teste logging", max_chunks=3)
    
    # 4. Testar logger RAG
    print("\n4. TESTANDO LOGGER RAG")
    print("-" * 40)
    
    rag = RAGAdapter(settings)
    results = rag.retrieve("estrutura narrativa", k=2)
    
    # 5. Testar formato JSON
    print("\n5. TESTANDO FORMATO JSON")
    print("-" * 40)
    
    from src.utils.logging_setup import setup_json_logging
    
    json_logger = setup_json_logging("json.test", "INFO")
    json_logger.info("Teste de log em formato JSON", extra={'user_id': 123, 'action': 'test'})
    json_logger.error("Erro com informações estruturadas", extra={'error_code': 'E001', 'retry': True})
    
    # 6. Ler arquivo de log gerado
    print("\n6. EXEMPLOS DO ARQUIVO DE LOG")
    print("-" * 40)
    
    log_file = Path(__file__).parent.parent / 'logs' / 'app.log'
    if log_file.exists():
        with open(log_file, 'r') as f:
            lines = f.readlines()
            # Mostrar últimas 10 linhas
            print("Últimas 10 linhas do arquivo de log:")
            for line in lines[-10:]:
                print(line.rstrip())
    
    print("\n" + "=" * 60)
    print("✅ TESTE DE LOGGING CONCLUÍDO")
    print(f"Logs salvos em: logs/app.log")
    print(f"Logs JSON em: logs/app.json.log")
    print("=" * 60)
    
    return True


if __name__ == "__main__":
    try:
        success = main()
        exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Erro no teste: {e}")
        import traceback
        traceback.print_exc()
        exit(1)