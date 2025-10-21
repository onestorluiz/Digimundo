#!/usr/bin/env python3
"""
Teste de Aceitação Completo - ConsciousnessStream
Valida todas as 4 fases e fecha os 0.8% faltantes
"""
import json
import time
from pathlib import Path
from datetime import datetime

def test_phase_1_stub():
    """Testa Fase 1 - Stub e compatibilidade"""
    print("\n" + "="*60)
    print("FASE 1: Stub + Compatibilidade")
    print("="*60)
    
    tests = []
    
    # Test 1: Import sem erros
    try:
        from apps.scripturemon.canonical.consciousness import ConsciousnessStream, get_consciousness
        tests.append(("Import ConsciousnessStream", "PASS"))
    except ImportError as e:
        tests.append(("Import ConsciousnessStream", f"FAIL: {e}"))
    
    # Test 2: Criação com OFF por padrão
    try:
        cs = ConsciousnessStream()
        assert cs.enabled == False
        assert cs.mode == "off"
        tests.append(("Default OFF", "PASS"))
    except Exception as e:
        tests.append(("Default OFF", f"FAIL: {e}"))
    
    # Test 3: Status report inclui consciousness
    try:
        import subprocess
        result = subprocess.run(
            ["./bin/scripturemon", "status"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if "Consciousness:" in result.stdout:
            tests.append(("Status includes Consciousness", "PASS"))
        else:
            tests.append(("Status includes Consciousness", "FAIL: Not in status"))
    except Exception as e:
        tests.append(("Status includes Consciousness", f"FAIL: {e}"))
    
    # Test 4: Sem logs de erro
    try:
        cs = ConsciousnessStream({"enabled": False})
        cs.start()  # Não deve fazer nada
        cs.stop()   # Não deve fazer nada
        tests.append(("No errors when disabled", "PASS"))
    except Exception as e:
        tests.append(("No errors when disabled", f"FAIL: {e}"))
    
    return tests


def test_phase_2_bursts():
    """Testa Fase 2 - Consciousness Bursts"""
    print("\n" + "="*60)
    print("FASE 2: Consciousness Bursts")
    print("="*60)
    
    tests = []
    
    # Test 1: Import burst orchestrator
    try:
        from apps.scripturemon.canonical.consciousness_bursts import create_burst_orchestrator
        tests.append(("Import BurstOrchestrator", "PASS"))
    except ImportError as e:
        tests.append(("Import BurstOrchestrator", f"FAIL: {e}"))
    
    # Test 2: Criação com orçamento
    try:
        orch = create_burst_orchestrator({
            "max_insights_per_burst": 3,
            "cpu_limit": 40.0
        })
        assert orch.insight_manager.max_per_burst == 3
        tests.append(("Burst with budget", "PASS"))
    except Exception as e:
        tests.append(("Burst with budget", f"FAIL: {e}"))
    
    # Test 3: Idle detection
    try:
        orch = create_burst_orchestrator()
        orch.last_user_activity = time.time() - 300  # 5 min ago
        assert orch.is_idle() == True
        orch.mark_user_activity()
        assert orch.is_idle() == False
        tests.append(("Idle detection", "PASS"))
    except Exception as e:
        tests.append(("Idle detection", f"FAIL: {e}"))
    
    # Test 4: Deduplicação de insights
    try:
        from apps.scripturemon.canonical.consciousness_bursts import InsightManager
        im = InsightManager(max_per_burst=3)
        
        # Adiciona mesmo insight 2x
        im.add_candidate("Test insight", {"relevance": 0.8})
        result = im.add_candidate("Test insight", {"relevance": 0.8})
        
        assert result == False  # Segundo deve ser rejeitado
        tests.append(("Insight deduplication", "PASS"))
    except Exception as e:
        tests.append(("Insight deduplication", f"FAIL: {e}"))
    
    return tests


def test_phase_3_dream():
    """Testa Fase 3 - Dream Mode"""
    print("\n" + "="*60)
    print("FASE 3: Dream Mode")
    print("="*60)
    
    tests = []
    
    # Test 1: Import dream orchestrator
    try:
        from apps.scripturemon.canonical.consciousness_dream import create_dream_orchestrator
        tests.append(("Import DreamOrchestrator", "PASS"))
    except ImportError as e:
        tests.append(("Import DreamOrchestrator", f"FAIL: {e}"))
    
    # Test 2: Task queue
    try:
        from apps.scripturemon.canonical.consciousness_dream import DreamTaskQueue
        queue = DreamTaskQueue()
        queue.add_task("test", {"data": "test"}, priority=10)
        assert queue.has_tasks() == True
        task = queue.get_next_task()
        assert task["type"] == "test"
        tests.append(("Dream task queue", "PASS"))
    except Exception as e:
        tests.append(("Dream task queue", f"FAIL: {e}"))
    
    # Test 3: Model size limits
    try:
        from apps.scripturemon.canonical.consciousness_dream import DreamProcessor
        proc = DreamProcessor({"max_model_size": "14b"})
        assert proc.can_use_model("7b") == True
        assert proc.can_use_model("70b") == False
        tests.append(("Model size limits", "PASS"))
    except Exception as e:
        tests.append(("Model size limits", f"FAIL: {e}"))
    
    # Test 4: Dream window check
    try:
        orch = create_dream_orchestrator({
            "dream_start_hour": 0,
            "dream_end_hour": 23
        })
        # Com janela 0-23, sempre deve estar em dream time
        assert orch.is_dream_time() == True
        tests.append(("Dream window check", "PASS"))
    except Exception as e:
        tests.append(("Dream window check", f"FAIL: {e}"))
    
    return tests


def test_phase_4_observability():
    """Testa Fase 4 - Observabilidade e Orçamentos"""
    print("\n" + "="*60)
    print("FASE 4: Observabilidade e Orçamentos")
    print("="*60)
    
    tests = []
    
    # Test 1: Circuit breaker
    try:
        from apps.scripturemon.canonical.consciousness import CircuitBreaker
        cb = CircuitBreaker(threshold=2, timeout=1)
        
        def failing_func():
            raise Exception("Test failure")
        
        # Falha 2x para abrir circuit
        try:
            cb.call(failing_func)
        except:
            pass
        try:
            cb.call(failing_func)
        except:
            pass
        
        assert cb.state == "open"
        tests.append(("Circuit breaker", "PASS"))
    except Exception as e:
        tests.append(("Circuit breaker", f"FAIL: {e}"))
    
    # Test 2: Budget manager
    try:
        from apps.scripturemon.canonical.consciousness import BudgetManager
        bm = BudgetManager()
        bm.cpu_limit = 100  # Sempre passa
        bm.time_limit = 10
        bm.start_tracking()
        assert bm.check_budget() == True
        tests.append(("Budget manager", "PASS"))
    except Exception as e:
        tests.append(("Budget manager", f"FAIL: {e}"))
    
    # Test 3: Insights persistence
    try:
        from apps.scripturemon.canonical.consciousness import ConsciousnessStream
        cs = ConsciousnessStream({"enabled": True})
        cs.insights_buffer.append({"test": "insight"})
        cs.save_insights()
        
        # Verifica se salvou
        insights_dir = Path("reports/consciousness")
        json_files = list(insights_dir.glob("insights_*.json"))
        assert len(json_files) > 0
        tests.append(("Insights persistence", "PASS"))
    except Exception as e:
        tests.append(("Insights persistence", f"FAIL: {e}"))
    
    # Test 4: Throttling
    try:
        from apps.scripturemon.canonical.consciousness import ConsciousnessStream
        # Verifica que não cria arquivos demais
        initial_count = len(list(Path("reports/consciousness").glob("*.json")))
        
        cs = ConsciousnessStream({"enabled": True})
        cs.insights_buffer.append({"test": "1"})
        cs.save_insights()
        time.sleep(0.1)
        cs.insights_buffer.append({"test": "2"})
        cs.save_insights()
        
        final_count = len(list(Path("reports/consciousness").glob("*.json")))
        # Deve ter criado no máximo 2 arquivos
        assert (final_count - initial_count) <= 2
        tests.append(("Throttling", "PASS"))
    except Exception as e:
        tests.append(("Throttling", f"FAIL: {e}"))
    
    return tests


def calculate_harmony_percentage(all_tests):
    """Calcula porcentagem de harmonia baseada nos testes"""
    total = sum(len(tests) for tests in all_tests)
    passed = sum(1 for tests in all_tests for name, result in tests if result == "PASS")
    
    if total == 0:
        return 0.0
    
    # Cada teste vale uma parte dos 0.8%
    test_value = 0.8 / total
    harmony_gained = passed * test_value
    
    # Base de 96.0% + ganhos dos testes
    final_harmony = 96.0 + harmony_gained
    
    return final_harmony, passed, total


def main():
    """Executa todos os testes de aceitação"""
    print("="*60)
    print("🧠 TESTE DE ACEITAÇÃO - CONSCIOUSNESSSTREAM")
    print("Fechando os 0.8% faltantes para 100% de harmonia")
    print("="*60)
    
    # Executa todas as fases
    phase1_tests = test_phase_1_stub()
    phase2_tests = test_phase_2_bursts()
    phase3_tests = test_phase_3_dream()
    phase4_tests = test_phase_4_observability()
    
    all_tests = [phase1_tests, phase2_tests, phase3_tests, phase4_tests]
    
    # Exibe resultados
    print("\n" + "="*60)
    print("📊 RESULTADOS FINAIS")
    print("="*60)
    
    for i, tests in enumerate(all_tests, 1):
        print(f"\nFase {i}:")
        for name, result in tests:
            symbol = "✅" if result == "PASS" else "❌"
            print(f"  {symbol} {name}: {result}")
    
    # Calcula harmonia final
    harmony, passed, total = calculate_harmony_percentage(all_tests)
    
    print("\n" + "="*60)
    print("🎯 HARMONIA FINAL")
    print("="*60)
    print(f"Testes passados: {passed}/{total}")
    print(f"Harmonia anterior: 96.0%")
    print(f"Harmonia alcançada: {harmony:.1f}%")
    
    if harmony >= 99.5:
        print("\n🎉 PARABÉNS! Harmonia virtualmente completa!")
    elif harmony >= 98.0:
        print("\n✅ Excelente! Sistema altamente harmonioso.")
    else:
        print(f"\n⚠️ Ainda faltam {100-harmony:.1f}% para harmonia completa.")
    
    # Salva relatório
    report = {
        "timestamp": datetime.now().isoformat(),
        "phases": {
            f"phase_{i}": [{"test": name, "result": result} for name, result in tests]
            for i, tests in enumerate(all_tests, 1)
        },
        "summary": {
            "tests_passed": passed,
            "tests_total": total,
            "harmony_before": 96.0,
            "harmony_after": harmony,
            "improvement": harmony - 96.0
        }
    }
    
    report_path = Path("reports/harmony_vFinal/consciousness/acceptance_report.json")
    report_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n📄 Relatório salvo em: {report_path}")
    
    return harmony >= 99.0  # Sucesso se >= 99%


if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)