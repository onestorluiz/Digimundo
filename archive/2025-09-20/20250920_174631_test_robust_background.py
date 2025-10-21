#!/usr/bin/env python3
"""
🧪 TESTE ROBUSTO COM EXECUÇÃO EM BACKGROUND
Executa testes longos sem bloquear, com métricas detalhadas
"""

import sys
import os
import time
import json
from datetime import datetime
from pathlib import Path

# Adiciona path do projeto
sys.path.insert(0, str(Path(__file__).parent.parent))

def log_with_time(msg):
    """Log com timestamp"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    print(f"[{timestamp}] {msg}")
    sys.stdout.flush()

def test_producer_director_full():
    """Testa sistema Producer-Director completo"""

    log_with_time("=== INICIANDO TESTE ROBUSTO ===")
    start_time = time.time()

    results = {
        "start": datetime.now().isoformat(),
        "tests": [],
        "metrics": {}
    }

    # TEST 1: Import básico
    test_start = time.time()
    log_with_time("TEST 1: Importando Producer-Director...")
    try:
        from apps.scripturemon.producer_director_system import ProducerDirectorSystem
        system = ProducerDirectorSystem()
        results["tests"].append({
            "name": "import_producer_director",
            "status": "PASS",
            "duration": time.time() - test_start
        })
        log_with_time("✅ Import OK")
    except Exception as e:
        results["tests"].append({
            "name": "import_producer_director",
            "status": "FAIL",
            "error": str(e),
            "duration": time.time() - test_start
        })
        log_with_time(f"❌ Import falhou: {e}")
        return results

    # TEST 2: Teste simples (deve ser rápido)
    test_start = time.time()
    log_with_time("TEST 2: Pergunta simples...")
    try:
        result = system._call_ollama("mistral:instruct", "Oi", timeout=60)
        if result and len(result) > 0:
            results["tests"].append({
                "name": "simple_ollama_call",
                "status": "PASS",
                "response_length": len(result),
                "duration": time.time() - test_start
            })
            log_with_time(f"✅ Resposta recebida ({len(result)} chars)")
        else:
            results["tests"].append({
                "name": "simple_ollama_call",
                "status": "FAIL",
                "error": "Empty response",
                "duration": time.time() - test_start
            })
            log_with_time("❌ Resposta vazia")
    except Exception as e:
        results["tests"].append({
            "name": "simple_ollama_call",
            "status": "FAIL",
            "error": str(e),
            "duration": time.time() - test_start
        })
        log_with_time(f"❌ Erro: {e}")

    # TEST 3: Orquestração completa (pode demorar)
    test_start = time.time()
    log_with_time("TEST 3: Orquestração completa com Producer...")
    log_with_time("⚠️ Este teste pode demorar até 5 minutos")

    try:
        # Modifica timeout dinamicamente
        original_method = system._call_ollama
        def call_with_long_timeout(model, prompt, timeout=600):
            log_with_time(f"  Chamando {model} (timeout={timeout}s)...")
            return original_method(model, prompt, timeout)

        system._call_ollama = call_with_long_timeout

        # Executa orquestração
        query = "Explique rapidamente o que é um MacGuffin no cinema"
        result = system.orchestrate(query)

        if result and len(result) > 0:
            results["tests"].append({
                "name": "full_orchestration",
                "status": "PASS",
                "query": query,
                "response_length": len(result),
                "duration": time.time() - test_start
            })
            log_with_time(f"✅ Orquestração completa ({len(result)} chars em {time.time()-test_start:.1f}s)")
        else:
            results["tests"].append({
                "name": "full_orchestration",
                "status": "FAIL",
                "error": "Empty orchestration result",
                "duration": time.time() - test_start
            })
            log_with_time("❌ Orquestração retornou vazio")

    except Exception as e:
        results["tests"].append({
            "name": "full_orchestration",
            "status": "FAIL",
            "error": str(e),
            "duration": time.time() - test_start
        })
        log_with_time(f"❌ Orquestração falhou: {e}")

    # TEST 4: Verificar métodos do OllamaCore
    test_start = time.time()
    log_with_time("TEST 4: Verificando métodos OllamaCore...")
    try:
        from apps.scripturemon.ollama_core import OllamaCore
        core = OllamaCore()

        # Lista métodos disponíveis
        methods = [m for m in dir(core) if not m.startswith('_')]

        # Verifica método problemático
        if 'check_available_models' in methods:
            log_with_time("✅ check_available_models existe")
            models = core.check_available_models()
            results["tests"].append({
                "name": "check_available_models",
                "status": "PASS",
                "models_count": len(models),
                "duration": time.time() - test_start
            })
        else:
            log_with_time("⚠️ check_available_models NÃO existe")
            log_with_time(f"   Métodos disponíveis: {methods}")

            # Tenta alternativa
            if hasattr(core, 'models'):
                models = core.models
                results["tests"].append({
                    "name": "check_available_models",
                    "status": "WORKAROUND",
                    "note": "Using core.models instead",
                    "models_count": len(models) if models else 0,
                    "duration": time.time() - test_start
                })
            else:
                results["tests"].append({
                    "name": "check_available_models",
                    "status": "FAIL",
                    "error": "Method does not exist",
                    "available_methods": methods,
                    "duration": time.time() - test_start
                })

    except Exception as e:
        results["tests"].append({
            "name": "check_available_models",
            "status": "FAIL",
            "error": str(e),
            "duration": time.time() - test_start
        })
        log_with_time(f"❌ Verificação falhou: {e}")

    # TEST 5: Pipeline Orchestrator
    test_start = time.time()
    log_with_time("TEST 5: Verificando PipelineOrchestrator...")
    try:
        from apps.scripturemon.pipeline_orchestrator import PipelineOrchestrator
        orch = PipelineOrchestrator()

        methods = [m for m in dir(orch) if not m.startswith('_')]

        if 'process_screenplay' in methods:
            log_with_time("✅ process_screenplay existe")
            results["tests"].append({
                "name": "process_screenplay_exists",
                "status": "PASS",
                "duration": time.time() - test_start
            })
        else:
            log_with_time("⚠️ process_screenplay NÃO existe")
            log_with_time(f"   Métodos disponíveis: {methods}")

            # Procura método correto
            if 'analyze_file' in methods:
                log_with_time("   ✅ Método correto é 'analyze_file'")
                results["tests"].append({
                    "name": "process_screenplay_exists",
                    "status": "WORKAROUND",
                    "note": "Should use analyze_file instead",
                    "available_methods": methods,
                    "duration": time.time() - test_start
                })
            else:
                results["tests"].append({
                    "name": "process_screenplay_exists",
                    "status": "FAIL",
                    "error": "Neither process_screenplay nor analyze_file exist",
                    "available_methods": methods,
                    "duration": time.time() - test_start
                })

    except Exception as e:
        results["tests"].append({
            "name": "pipeline_orchestrator_check",
            "status": "FAIL",
            "error": str(e),
            "duration": time.time() - test_start
        })
        log_with_time(f"❌ Pipeline check falhou: {e}")

    # Finaliza
    total_duration = time.time() - start_time
    results["end"] = datetime.now().isoformat()
    results["total_duration"] = total_duration

    # Calcula métricas
    passed = sum(1 for t in results["tests"] if t["status"] == "PASS")
    failed = sum(1 for t in results["tests"] if t["status"] == "FAIL")
    workarounds = sum(1 for t in results["tests"] if t["status"] == "WORKAROUND")

    results["metrics"] = {
        "total_tests": len(results["tests"]),
        "passed": passed,
        "failed": failed,
        "workarounds": workarounds,
        "success_rate": (passed / len(results["tests"]) * 100) if results["tests"] else 0
    }

    # Imprime métricas finais
    log_with_time("=" * 60)
    log_with_time("=== PERFORMANCE METRICS ===")
    log_with_time(f"Start: {results['start']}")
    log_with_time(f"End: {results['end']}")
    log_with_time(f"Duration: {total_duration:.2f}s")
    log_with_time("")
    log_with_time("Each test timing:")
    for test in results["tests"]:
        status_icon = "✅" if test["status"] == "PASS" else "❌" if test["status"] == "FAIL" else "⚠️"
        log_with_time(f"- {test['name']}: {test['duration']:.2f}s {status_icon}")

    log_with_time("")
    log_with_time(f"RESULTS: {passed} passed, {failed} failed, {workarounds} workarounds")
    log_with_time(f"SUCCESS RATE: {results['metrics']['success_rate']:.1f}%")
    log_with_time("=" * 60)

    # Salva JSON com resultados
    output_file = f"test_results_{int(time.time())}.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    log_with_time(f"Results saved to: {output_file}")

    return results

if __name__ == "__main__":
    test_producer_director_full()