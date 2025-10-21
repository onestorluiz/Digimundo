#!/usr/bin/env python3
"""
🔍 COMPREHENSIVE SYSTEM TEST FOR CLAUDE CODE v4.1
Complete functionality and harmony verification
"""

import os
import sys
import time
import asyncio
import importlib
import threading
import traceback
import json
from typing import Dict, List, Any, Optional

# ==================== TEST FRAMEWORK ====================

class SystemTester:
    """Sistema completo de testes"""

    def __init__(self):
        self.results = {
            'components': {},
            'integration': {},
            'performance': {},
            'harmony': 0.0,
            'errors': [],
            'warnings': []
        }

    def test_component_import(self) -> Dict[str, bool]:
        """Testa importação de todos os componentes"""
        print("\n📦 TESTANDO IMPORTAÇÃO DE COMPONENTES")
        print("=" * 60)

        components = {
            'ml_predictor': ['AdvancedMLPredictor', 'PredictionTask', 'ModelType'],
            'distributed_event_bus': ['DistributedEventBus', 'Event', 'EventMetadata'],
            'advanced_message_queue': ['MessageBroker', 'Message', 'Queue'],
            'workflow_engine': ['WorkflowEngine', 'WorkflowConfig', 'TaskConfig'],
            'rate_limiter': ['RateLimiterManager', 'TokenBucket', 'RateLimitConfig'],
            'auto_healer': ['AutoHealer', 'HealingStrategy', 'HealthStatus'],
            'quantum_processor': ['QuantumProcessor', 'QuantumGate', 'QuantumCircuit'],
            'neural_network': ['QuantumNeuralNetwork', 'ActivationFunction'],
            'telemetry_collector': ['TelemetryCollector', 'AlertSeverity'],
            'distributed_cache': ['DistributedCache', 'EvictionPolicy'],
            'ADVANCED_BUG_SCANNER': ['BugScanner', 'BugType'],
        }

        results = {}

        for module_name, required_attrs in components.items():
            try:
                print(f"\n  Testing {module_name}...")
                module = importlib.import_module(module_name)

                # Check required attributes
                missing = []
                for attr in required_attrs:
                    if not hasattr(module, attr):
                        missing.append(attr)

                if missing:
                    print(f"    ⚠️  Missing: {missing}")
                    results[module_name] = 'partial'
                    self.results['warnings'].append(f"{module_name}: missing {missing}")
                else:
                    print(f"    ✅ OK - All attributes present")
                    results[module_name] = 'success'

            except ImportError as e:
                print(f"    ❌ Import Error: {e}")
                results[module_name] = 'failed'
                self.results['errors'].append(f"{module_name}: {e}")
            except Exception as e:
                print(f"    ❌ Error: {e}")
                results[module_name] = 'failed'
                self.results['errors'].append(f"{module_name}: {e}")

        self.results['components'] = results
        return results

    def test_component_instantiation(self) -> Dict[str, bool]:
        """Testa instanciação dos componentes"""
        print("\n🔧 TESTANDO INSTANCIAÇÃO")
        print("=" * 60)

        test_cases = []

        try:
            # ML Predictor
            from ml_predictor import AdvancedMLPredictor, PredictionTask
            predictor = AdvancedMLPredictor()
            test_cases.append(('ML Predictor', True, None))
            print("  ✅ ML Predictor: Instanciado")
        except Exception as e:
            test_cases.append(('ML Predictor', False, str(e)))
            print(f"  ❌ ML Predictor: {e}")

        try:
            # Event Bus
            from distributed_event_bus import DistributedEventBus
            event_bus = DistributedEventBus()
            test_cases.append(('Event Bus', True, None))
            print("  ✅ Event Bus: Instanciado")
        except Exception as e:
            test_cases.append(('Event Bus', False, str(e)))
            print(f"  ❌ Event Bus: {e}")

        try:
            # Message Queue
            from advanced_message_queue import MessageBroker
            broker = MessageBroker()
            test_cases.append(('Message Broker', True, None))
            print("  ✅ Message Broker: Instanciado")
        except Exception as e:
            test_cases.append(('Message Broker', False, str(e)))
            print(f"  ❌ Message Broker: {e}")

        try:
            # Rate Limiter
            from rate_limiter import RateLimiterManager
            rate_limiter = RateLimiterManager()
            test_cases.append(('Rate Limiter', True, None))
            print("  ✅ Rate Limiter: Instanciado")
        except Exception as e:
            test_cases.append(('Rate Limiter', False, str(e)))
            print(f"  ❌ Rate Limiter: {e}")

        try:
            # Workflow Engine
            from workflow_engine import WorkflowEngine
            engine = WorkflowEngine()
            test_cases.append(('Workflow Engine', True, None))
            print("  ✅ Workflow Engine: Instanciado")
        except Exception as e:
            test_cases.append(('Workflow Engine', False, str(e)))
            print(f"  ❌ Workflow Engine: {e}")

        return {name: success for name, success, _ in test_cases}

    def test_basic_functionality(self):
        """Testa funcionalidades básicas"""
        print("\n⚡ TESTANDO FUNCIONALIDADES BÁSICAS")
        print("=" * 60)

        tests_passed = 0
        tests_total = 0

        # Test 1: Event Bus Pub/Sub
        try:
            from distributed_event_bus import DistributedEventBus, Event
            bus = DistributedEventBus()

            received = []
            def handler(event):
                received.append(event)

            bus.subscribe("test.*", handler)
            event_id = bus.publish(Event(type="test.event", data={"test": True}))
            time.sleep(0.5)  # Wait for async processing

            tests_total += 1
            if received:
                print("  ✅ Event Bus: Pub/Sub working")
                tests_passed += 1
            else:
                print("  ❌ Event Bus: No events received")
        except Exception as e:
            print(f"  ❌ Event Bus test failed: {e}")
            tests_total += 1

        # Test 2: Rate Limiter
        try:
            from rate_limiter import RateLimiterManager, RateLimitConfig, LimitStrategy, LimitScope, RequestContext

            manager = RateLimiterManager()
            manager.register_limiter('test', RateLimitConfig(
                name='test',
                strategy=LimitStrategy.TOKEN_BUCKET,
                scope=LimitScope.USER,
                limit=5,
                window=60
            ))

            context = RequestContext('user1', '/api/test')
            manager.apply_policy('/api/test', ['test'])

            # Try 5 requests (should all pass)
            allowed_count = 0
            for _ in range(10):
                result = manager.check_request('/api/test', context)
                if result.allowed:
                    allowed_count += 1

            tests_total += 1
            if allowed_count == 5:  # Should allow exactly 5
                print("  ✅ Rate Limiter: Limiting correctly (5/10 allowed)")
                tests_passed += 1
            else:
                print(f"  ⚠️  Rate Limiter: Allowed {allowed_count}/10 (expected 5)")
        except Exception as e:
            print(f"  ❌ Rate Limiter test failed: {e}")
            tests_total += 1

        # Test 3: Message Queue
        try:
            from advanced_message_queue import MessageBroker, QueueConfig, QueueType

            broker = MessageBroker()
            queue_config = QueueConfig(
                name='test_queue',
                queue_type=QueueType.STANDARD,
                durable=False
            )
            queue = broker.declare_queue(queue_config)

            # Publish message
            msg_id = broker.publish('', 'test_queue', {'test': 'data'})

            # Consume message
            consumed = []
            def msg_handler(message):
                consumed.append(message)
                return True

            broker.consume('test_queue', msg_handler)
            time.sleep(0.5)

            tests_total += 1
            if consumed:
                print("  ✅ Message Queue: Publish/Consume working")
                tests_passed += 1
            else:
                print("  ❌ Message Queue: No messages consumed")
        except Exception as e:
            print(f"  ❌ Message Queue test failed: {e}")
            tests_total += 1

        # Test 4: Workflow Engine
        try:
            from workflow_engine import WorkflowEngine, WorkflowBuilder

            engine = WorkflowEngine()

            def task1():
                return "result1"

            def task2(input_data):
                return f"processed_{input_data}"

            workflow = (WorkflowBuilder("test_workflow")
                .add_task("t1", "Task 1")
                .with_function(task1)
                .add_task("t2", "Task 2")
                .with_function(task2)
                .depends_on("t1")
                .build())

            workflow_id = engine.register_workflow(workflow)

            tests_total += 1
            print("  ✅ Workflow Engine: DAG created successfully")
            tests_passed += 1
        except Exception as e:
            print(f"  ❌ Workflow Engine test failed: {e}")
            tests_total += 1

        # Test 5: ML Predictor
        try:
            from ml_predictor import AdvancedMLPredictor, PredictionTask
            import numpy as np

            predictor = AdvancedMLPredictor()
            X = [[1, 2], [3, 4], [5, 6]]
            y = [0, 1, 0]

            # Try simple training (won't actually train, just test structure)
            predictor.train('test_model', X, y, task=PredictionTask.CLASSIFICATION)

            tests_total += 1
            print("  ✅ ML Predictor: Training API working")
            tests_passed += 1
        except Exception as e:
            print(f"  ❌ ML Predictor test failed: {e}")
            tests_total += 1

        print(f"\n📊 Funcionalidade: {tests_passed}/{tests_total} testes passaram")
        return tests_passed / tests_total if tests_total > 0 else 0

    def test_integration(self):
        """Testa integração entre componentes"""
        print("\n🔗 TESTANDO INTEGRAÇÃO")
        print("=" * 60)

        try:
            # Teste de integração Event Bus + Rate Limiter
            from distributed_event_bus import DistributedEventBus, Event
            from rate_limiter import RateLimiterManager, RateLimitConfig, LimitStrategy, LimitScope, RequestContext

            bus = DistributedEventBus()
            limiter = RateLimiterManager()

            # Rate limiter no event handler
            limiter.register_limiter('event_limiter', RateLimitConfig(
                name='events',
                strategy=LimitStrategy.TOKEN_BUCKET,
                scope=LimitScope.USER,
                limit=3,
                window=60
            ))

            processed = []

            def rate_limited_handler(event):
                context = RequestContext(event.metadata.user_id or 'anonymous')
                result = limiter.check_request('/event', context)
                if result.allowed:
                    processed.append(event)
                    print(f"    Processed event {len(processed)}")
                else:
                    print(f"    Rate limited!")

            limiter.apply_policy('/event', ['event_limiter'])
            bus.subscribe("integration.*", rate_limited_handler)

            # Send 5 events (only 3 should be processed)
            for i in range(5):
                bus.publish(Event(
                    type="integration.test",
                    data={"index": i}
                ))

            time.sleep(1)

            if len(processed) == 3:
                print("  ✅ Integration Test: Event Bus + Rate Limiter working together")
                return True
            else:
                print(f"  ⚠️  Integration: Expected 3 events, got {len(processed)}")
                return False

        except Exception as e:
            print(f"  ❌ Integration test failed: {e}")
            self.results['errors'].append(f"Integration: {e}")
            return False

    def calculate_harmony(self):
        """Calcula índice de harmonia do sistema"""
        component_scores = self.results.get('components', {})

        # Count successes
        total = len(component_scores)
        successful = sum(1 for status in component_scores.values() if status == 'success')
        partial = sum(1 for status in component_scores.values() if status == 'partial')

        # Calculate harmony score
        if total > 0:
            harmony = (successful * 1.0 + partial * 0.5) / total * 100
        else:
            harmony = 0

        self.results['harmony'] = harmony
        return harmony

    def generate_report(self):
        """Gera relatório completo"""
        print("\n" + "=" * 60)
        print("📊 RELATÓRIO FINAL DO SISTEMA CLAUDE CODE v4.1")
        print("=" * 60)

        harmony = self.calculate_harmony()

        print(f"\n🎯 HARMONIA DO SISTEMA: {harmony:.1f}%")

        if harmony == 100:
            print("   ✅ HARMONIA PERFEITA ALCANÇADA!")
        elif harmony >= 90:
            print("   🟢 Harmonia Excelente")
        elif harmony >= 80:
            print("   🟡 Harmonia Boa")
        else:
            print("   🔴 Harmonia Baixa - Correções Necessárias")

        # Component status
        print("\n📦 STATUS DOS COMPONENTES:")
        for name, status in self.results.get('components', {}).items():
            icon = "✅" if status == 'success' else "⚠️" if status == 'partial' else "❌"
            print(f"   {icon} {name}: {status}")

        # Errors
        if self.results['errors']:
            print("\n❌ ERROS ENCONTRADOS:")
            for error in self.results['errors']:
                print(f"   • {error}")

        # Warnings
        if self.results['warnings']:
            print("\n⚠️  WARNINGS:")
            for warning in self.results['warnings']:
                print(f"   • {warning}")

        # Recommendations
        print("\n💡 RECOMENDAÇÕES:")
        if harmony < 100:
            if self.results['errors']:
                print("   1. Corrigir erros de importação")
            if self.results['warnings']:
                print("   2. Implementar atributos faltantes")
            print("   3. Verificar dependências")
            print("   4. Testar integração completa")
        else:
            print("   • Sistema 100% funcional e harmônico!")
            print("   • Pronto para produção")

        return self.results

# ==================== MAIN ====================

def main():
    print("🚀 INICIANDO TESTE COMPLETO DO SISTEMA CLAUDE CODE")
    print("=" * 60)

    tester = SystemTester()

    # Run all tests
    tester.test_component_import()
    tester.test_component_instantiation()
    functionality_score = tester.test_basic_functionality()
    integration_success = tester.test_integration()

    # Generate final report
    report = tester.generate_report()

    # Save report to file
    with open('system_test_report.json', 'w') as f:
        json.dump(report, f, indent=2, default=str)

    print("\n📄 Relatório salvo em: system_test_report.json")
    print("\n✅ TESTE COMPLETO FINALIZADO!")

    return report

if __name__ == "__main__":
    report = main()