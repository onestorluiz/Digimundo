#!/usr/bin/env python3
"""
🚀 TESTE RÁPIDO FASE 4 - Validação dos Sistemas Principais
"""

import sys
import tempfile
from pathlib import Path

# Adicionar ao path
sys.path.insert(0, '/Users/clubproducoes/Digimundo/scripturemon-validation')

from apps.scripturemon.intelligent_cache import IntelligentCache
from apps.scripturemon.auto_optimizer import AutoOptimizer
from apps.scripturemon.monitoring_system import MonitoringSystem
from apps.scripturemon.language_validator import LanguageValidator

def test_intelligent_cache():
    """Teste básico do cache inteligente"""
    print("🧠 Testando Cache Inteligente...")
    
    temp_dir = Path(tempfile.mkdtemp())
    cache = IntelligentCache(temp_dir, max_memory_mb=10)
    
    # Teste básico
    cache.set('test_key', 'test_value', ttl=60)
    result = cache.get('test_key')
    
    assert result == 'test_value', f"Expected 'test_value', got {result}"
    
    # Estatísticas
    stats = cache.get_stats()
    assert stats['levels']['L1']['items'] > 0
    
    print("   ✅ Cache funcionando corretamente")

def test_auto_optimizer():
    """Teste básico do otimizador"""
    print("🎯 Testando Auto-Otimizador...")
    
    temp_dir = Path(tempfile.mkdtemp())
    optimizer = AutoOptimizer(temp_dir)
    
    # Registrar métricas
    optimizer.record_metric('response_time_ms', 450)
    optimizer.record_metric('cache_hit_rate', 0.85)
    
    # Verificar
    assert len(optimizer.metrics_history) >= 2
    
    # Performance
    score = optimizer.evaluate_performance()
    assert 0 <= score <= 1
    
    print(f"   ✅ Otimizador funcionando (score: {score:.3f})")

def test_monitoring_system():
    """Teste básico do sistema de monitoramento"""
    print("📊 Testando Sistema de Monitoramento...")
    
    temp_dir = Path(tempfile.mkdtemp())
    monitor = MonitoringSystem(temp_dir)
    
    # Logs
    monitor.log('INFO', 'Teste de log')
    monitor.metric('test_metric', 42.0)
    
    # Verificar logs recentes
    logs = monitor.get_recent_logs(limit=5)
    assert len(logs) > 0
    
    # Estatísticas
    stats = monitor.get_metrics_summary()
    assert 'counters' in stats
    
    print("   ✅ Monitoramento funcionando corretamente")

def test_language_validator():
    """Teste básico do validador de idioma"""
    print("🌐 Testando Validador de Idioma...")
    
    validator = LanguageValidator()
    
    # Texto em português
    pt_text = "Este é um texto em português brasileiro sobre roteiros."
    lang, confidence, _ = validator.detect_language(pt_text)
    
    assert lang == 'pt-br', f"Expected 'pt-br', got {lang}"
    assert confidence > 0.5, f"Low confidence: {confidence}"
    
    # Prompt forçado
    forced = validator.force_portuguese_prompt("Test prompt", 1)
    assert 'PORTUGUÊS' in forced.upper()
    
    print(f"   ✅ Validador funcionando (confiança: {confidence:.2f})")

def main():
    """Executa todos os testes rápidos"""
    print("\n" + "="*60)
    print("🧪 TESTE RÁPIDO - SISTEMAS AVANÇADOS FASE 4")
    print("="*60)
    
    try:
        test_intelligent_cache()
        test_auto_optimizer()
        test_monitoring_system()
        test_language_validator()
        
        print("\n" + "="*60)
        print("✅ TODOS OS SISTEMAS DA FASE 4 FUNCIONANDO!")
        print("🚀 VALIDAÇÃO COMPLETA COM SUCESSO")
        print("="*60)
        return 0
        
    except Exception as e:
        print(f"\n❌ Erro durante teste: {e}")
        return 1

if __name__ == '__main__':
    sys.exit(main())