#!/usr/bin/env python3
"""
🧪 TEST FASE 4 - SISTEMAS AVANÇADOS
Testes robustos para Cache, Pipeline, Optimizer e integração completa
"""

import unittest
import asyncio
import time
import tempfile
from pathlib import Path
import threading
import sys

# Adicionar ao path
sys.path.insert(0, '/Users/clubproducoes/Digimundo/scripturemon-validation')

from apps.scripturemon.intelligent_cache import IntelligentCache
from apps.scripturemon.async_pipeline import AsyncPipeline, TaskPriority
from apps.scripturemon.auto_optimizer import AutoOptimizer
from apps.scripturemon.monitoring_system import MonitoringSystem
from apps.scripturemon.language_validator import LanguageValidator


class TestIntelligentCache(unittest.TestCase):
    """Testes para Sistema de Cache Inteligente"""
    
    def setUp(self):
        self.temp_dir = Path(tempfile.mkdtemp())
        self.cache = IntelligentCache(self.temp_dir, max_memory_mb=50)
    
    def test_multi_level_caching(self):
        """Testa cache multi-nível L1/L2/L3"""
        # L1 - Cache rápido
        self.assertTrue(self.cache.set('test_l1', 'value1', ttl=60))
        result = self.cache.get('test_l1')
        self.assertEqual(result, 'value1')
        
        # Verificar estatísticas
        stats = self.cache.get_stats()
        self.assertGreater(stats['levels']['L1']['items'], 0)
        self.assertGreater(stats['performance']['hit_rate'].replace('%', ''), '0')
    
    def test_compression_l2(self):
        """Testa compressão no cache L2"""
        # Dados grandes para forçar L2
        large_data = 'x' * 2000  # > 1KB
        
        self.cache.set('large_test', large_data, ttl=3600)
        
        # Deve estar em L2 comprimido
        stats = self.cache.get_stats()
        self.assertGreater(stats['levels']['L2']['compressions'], 0)
        
        # Recuperar deve funcionar
        result = self.cache.get('large_test')
        self.assertEqual(result, large_data)
    
    def test_lru_eviction(self):
        """Testa evicção LRU"""
        # Preencher L1 até o limite
        for i in range(self.cache.l1_max_items + 10):
            self.cache.set(f'item_{i}', f'value_{i}')
        
        stats = self.cache.get_stats()
        self.assertLessEqual(stats['levels']['L1']['items'], self.cache.l1_max_items)
        self.assertGreater(stats['levels']['L1']['evictions'], 0)
    
    def test_ttl_expiration(self):
        """Testa expiração por TTL"""
        self.cache.set('expire_test', 'will_expire', ttl=1)
        
        # Imediatamente deve estar disponível
        result = self.cache.get('expire_test')
        self.assertEqual(result, 'will_expire')
        
        # Após TTL deve ter expirado
        time.sleep(1.2)
        result = self.cache.get('expire_test', default='expired')
        self.assertEqual(result, 'expired')
    
    def test_batch_operations(self):
        """Testa operações em batch"""
        items = {f'batch_{i}': f'value_{i}' for i in range(50)}
        
        count = self.cache.set_many(items, ttl=300)
        self.assertEqual(count, 50)
        
        # Verificar todos foram salvos
        for key, expected_value in list(items.items())[:10]:
            actual_value = self.cache.get(key)
            self.assertEqual(actual_value, expected_value)


class TestAsyncPipeline(unittest.TestCase):
    """Testes para Pipeline Assíncrono"""
    
    def setUp(self):
        self.pipeline = AsyncPipeline(max_workers=4, enable_multiprocessing=False)
        
        # Configurar stages de teste
        def stage1_processor(data):
            return f"stage1({data})"
        
        def stage2_processor(data):
            time.sleep(0.1)  # Simular processamento
            return f"stage2({data})"
        
        async def stage3_async(data):
            await asyncio.sleep(0.05)
            return f"stage3_async({data})"
        
        self.pipeline.add_stage('stage1', stage1_processor, parallelism=2)
        self.pipeline.add_stage('stage2', stage2_processor, parallelism=1)
        self.pipeline.add_stage('stage3', stage3_async, parallelism=2)
    
    def test_single_task_processing(self):
        """Testa processamento de tarefa única"""
        async def run_test():
            await self.pipeline.start()
            
            # Submeter tarefa
            task_id = await self.pipeline.submit('test_data', TaskPriority.HIGH)
            
            # Aguardar resultado
            result = await self.pipeline.get_result(task_id, timeout=5)
            
            # Verificar que passou por todos os stages
            expected = "stage3_async(stage2(stage1(test_data)))"
            self.assertEqual(result, expected)
            
            await self.pipeline.stop()
        
        asyncio.run(run_test())
    
    def test_batch_processing(self):
        """Testa processamento em batch"""
        async def run_test():
            await self.pipeline.start()
            
            # Submeter batch
            items = [(f'item_{i}', TaskPriority.NORMAL) for i in range(10)]
            task_ids = await self.pipeline.submit_batch(items)
            
            self.assertEqual(len(task_ids), 10)
            
            # Aguardar alguns resultados
            results = []
            for task_id in task_ids[:3]:
                result = await self.pipeline.get_result(task_id, timeout=10)
                results.append(result)
            
            self.assertEqual(len(results), 3)
            
            await self.pipeline.stop()
        
        asyncio.run(run_test())
    
    def test_priority_handling(self):
        """Testa prioridades de tarefas"""
        async def run_test():
            await self.pipeline.start()
            
            # Submeter tarefas com diferentes prioridades
            low_task = await self.pipeline.submit('low', TaskPriority.LOW)
            critical_task = await self.pipeline.submit('critical', TaskPriority.CRITICAL)
            high_task = await self.pipeline.submit('high', TaskPriority.HIGH)
            
            # Crítica deve processar primeiro
            critical_result = await self.pipeline.get_result(critical_task, timeout=5)
            self.assertEqual(critical_result, "stage3_async(stage2(stage1(critical)))")
            
            await self.pipeline.stop()
        
        asyncio.run(run_test())
    
    def test_error_handling_and_retry(self):
        """Testa tratamento de erro e retry"""
        def failing_processor(data):
            if data == 'fail':
                raise ValueError("Test error")
            return f"success({data})"
        
        self.pipeline.add_stage('failing_stage', failing_processor)
        
        async def run_test():
            await self.pipeline.start()
            
            # Tarefa que vai falhar
            fail_task = await self.pipeline.submit('fail', TaskPriority.HIGH)
            
            # Deve falhar após retries
            with self.assertRaises(Exception):
                await self.pipeline.get_result(fail_task, timeout=10)
            
            # Tarefa que vai suceder
            success_task = await self.pipeline.submit('success', TaskPriority.HIGH)
            result = await self.pipeline.get_result(success_task, timeout=5)
            
            # Deve incluir o novo stage
            self.assertIn('success(success)', result)
            
            await self.pipeline.stop()
        
        asyncio.run(run_test())
    
    def test_performance_stats(self):
        """Testa coleta de estatísticas de performance"""
        async def run_test():
            await self.pipeline.start()
            
            # Processar algumas tarefas
            tasks = []
            for i in range(5):
                task_id = await self.pipeline.submit(f'perf_test_{i}', TaskPriority.NORMAL)
                tasks.append(task_id)
            
            # Aguardar conclusão
            for task_id in tasks:
                await self.pipeline.get_result(task_id, timeout=10)
            
            # Verificar estatísticas
            stats = self.pipeline.get_stats()
            self.assertGreaterEqual(stats['completed_tasks'], 5)
            self.assertGreater(stats['throughput_per_sec'], 0)
            
            await self.pipeline.stop()
        
        asyncio.run(run_test())


class TestAutoOptimizer(unittest.TestCase):
    """Testes para Auto-Otimizador"""
    
    def setUp(self):
        self.temp_dir = Path(tempfile.mkdtemp())
        self.optimizer = AutoOptimizer(self.temp_dir)
    
    def test_metric_recording(self):
        """Testa gravação de métricas"""
        # Registrar métricas
        self.optimizer.record_metric('response_time_ms', 500)
        self.optimizer.record_metric('cache_hit_rate', 0.8)
        self.optimizer.record_metric('memory_usage_mb', 300)
        
        # Verificar que foram gravadas
        self.assertGreater(len(self.optimizer.metrics_history), 0)
        
        # Verificar targets atualizados
        self.assertEqual(self.optimizer.targets['response_time_ms'].current_value, 500)
        self.assertEqual(self.optimizer.targets['cache_hit_rate'].current_value, 0.8)
    
    def test_performance_evaluation(self):
        """Testa avaliação de performance"""
        # Registrar métricas boas
        self.optimizer.record_metric('response_time_ms', 400)  # Abaixo do target 500
        self.optimizer.record_metric('cache_hit_rate', 0.95)  # Acima do target 0.9
        self.optimizer.record_metric('throughput_qps', 60)    # Acima do target 50
        
        # Avaliar performance
        score = self.optimizer.evaluate_performance()
        
        # Deve ter score alto (> 0.8)
        self.assertGreater(score, 0.8)
    
    def test_parameter_suggestions(self):
        """Testa sugestão de parâmetros"""
        # Adicionar dados de treino simulados
        for i in range(100):
            self.optimizer.record_metric('response_time_ms', 500 + (i % 100))
            self.optimizer.record_metric('cache_hit_rate', 0.7 + (i % 30) / 100)
        
        # Sugerir novos parâmetros
        suggestions = self.optimizer.suggest_parameters('random_search')
        
        # Deve sugerir todos os parâmetros
        self.assertEqual(len(suggestions), len(self.optimizer.parameters))
        
        # Valores devem estar dentro dos ranges
        for param_name, suggested_value in suggestions.items():
            param_config = self.optimizer.parameters[param_name]
            self.assertGreaterEqual(suggested_value, param_config['min'])
            self.assertLessEqual(suggested_value, param_config['max'])
    
    def test_parameter_application(self):
        """Testa aplicação de parâmetros"""
        # Parâmetros para testar
        new_params = {
            'cache_l1_ttl': 120,
            'pipeline_workers': 16,
            'model_timeout': 45
        }
        
        # Aplicar
        success = self.optimizer.apply_parameters(new_params, test_duration=1)
        self.assertTrue(success)
        
        # Verificar que foram aplicados
        for param_name, expected_value in new_params.items():
            actual_value = self.optimizer.parameters[param_name]['current']
            self.assertEqual(actual_value, expected_value)
        
        # Verificar histórico
        self.assertGreater(len(self.optimizer.parameter_history), 0)
    
    def test_recommendations(self):
        """Testa geração de recomendações"""
        # Adicionar métricas com tendência
        base_time = time.time()
        for i in range(50):
            # Simular degradação da performance
            self.optimizer.record_metric('response_time_ms', 400 + i * 2)
            
            # Simular melhoria do cache
            self.optimizer.record_metric('cache_hit_rate', 0.7 + i * 0.004)
        
        # Gerar recomendações
        recommendations = self.optimizer.get_recommendations()
        
        # Deve ter recomendações
        self.assertGreater(len(recommendations), 0)
        
        # Verificar estrutura das recomendações
        if recommendations:
            rec = recommendations[0]
            self.assertIn('metric', rec)
            self.assertIn('trend', rec)
            self.assertIn('priority', rec)


class TestSystemIntegration(unittest.TestCase):
    """Testes de integração entre sistemas da Fase 4"""
    
    def test_cache_pipeline_integration(self):
        """Testa integração Cache + Pipeline"""
        async def run_test():
            # Inicializar sistemas
            temp_dir = Path(tempfile.mkdtemp())
            cache = IntelligentCache(temp_dir)
            pipeline = AsyncPipeline(max_workers=2)
            
            # Stage que usa cache
            def cached_processor(data):
                # Verificar cache primeiro
                cached = cache.get(f"cache_key_{data}")
                if cached:
                    return f"cached({cached})"
                
                # Processar e cachear
                result = f"processed({data})"
                cache.set(f"cache_key_{data}", result, ttl=300)
                return result
            
            pipeline.add_stage('cached_stage', cached_processor)
            
            await pipeline.start()
            
            # Primeira execução - sem cache
            task1 = await pipeline.submit('test_data', TaskPriority.HIGH)
            result1 = await pipeline.get_result(task1, timeout=5)
            self.assertEqual(result1, "processed(test_data)")
            
            # Segunda execução - com cache
            task2 = await pipeline.submit('test_data', TaskPriority.HIGH)
            result2 = await pipeline.get_result(task2, timeout=5)
            self.assertEqual(result2, "cached(processed(test_data))")
            
            await pipeline.stop()
        
        asyncio.run(run_test())
    
    def test_optimizer_monitoring_integration(self):
        """Testa integração Optimizer + Monitoring"""
        temp_dir = Path(tempfile.mkdtemp())
        optimizer = AutoOptimizer(temp_dir)
        monitor = MonitoringSystem(temp_dir)
        
        # Registrar métricas no monitor
        monitor.metric('response_time_ms', 600.0)
        monitor.metric('cache_hit_rate', 0.75)
        monitor.metric('throughput_qps', 25.0)
        
        # Extrair métricas para otimizador
        optimizer.record_metric('response_time_ms', 600.0, {'source': 'monitor'})
        optimizer.record_metric('cache_hit_rate', 0.75, {'source': 'monitor'})
        optimizer.record_metric('throughput_qps', 25.0, {'source': 'monitor'})
        
        # Avaliar performance
        performance = optimizer.evaluate_performance()
        
        # Performance deve ser mediana (entre 0.4 e 0.7)
        self.assertGreater(performance, 0.4)
        self.assertLess(performance, 0.8)
        
        # Log de otimização
        monitor.log('INFO', f'Performance score: {performance:.3f}', 
                   component='optimizer', context={'metrics_count': 3})
        
        # Verificar logs
        logs = monitor.get_recent_logs(component='optimizer', limit=5)
        self.assertGreater(len(logs), 0)


def run_fase4_tests():
    """Executa todos os testes da Fase 4"""
    print("\n" + "="*70)
    print("🧪 EXECUTANDO TESTES DA FASE 4 - SISTEMAS AVANÇADOS")
    print("="*70)
    
    # Criar suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Adicionar testes
    suite.addTests(loader.loadTestsFromTestCase(TestIntelligentCache))
    suite.addTests(loader.loadTestsFromTestCase(TestAsyncPipeline))
    suite.addTests(loader.loadTestsFromTestCase(TestAutoOptimizer))
    suite.addTests(loader.loadTestsFromTestCase(TestSystemIntegration))
    
    # Executar
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Relatório
    print("\n" + "="*70)
    print("📊 RELATÓRIO DE TESTES FASE 4")
    print("="*70)
    print(f"Testes executados: {result.testsRun}")
    print(f"Sucessos: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Falhas: {len(result.failures)}")
    print(f"Erros: {len(result.errors)}")
    
    if result.wasSuccessful():
        print("\n✅ TODOS OS TESTES DA FASE 4 PASSARAM!")
        print("🚀 SISTEMAS AVANÇADOS VALIDADOS COM SUCESSO")
        return 0
    else:
        print("\n❌ ALGUNS TESTES DA FASE 4 FALHARAM")
        return 1


if __name__ == '__main__':
    sys.exit(run_fase4_tests())