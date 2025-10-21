#!/usr/bin/env python3
"""
🌟 TESTE SISTEMA SUPREMO INTEGRADO
Teste final do sistema de integração suprema das memórias neurais
"""

import asyncio
import logging
import time
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_supreme_integration():
    """Testa o sistema supremo integrado"""
    logger.info("🌟 Testing Supreme Memory Integration System...")

    try:
        # Importa sistema supremo
        from memory_systems.memory_simple_integration_supreme import UnifiedMemoryIntegrationSupreme, IntegrationLevel, CognitiveModes

        # Cria instância com configuração reduzida para teste
        supreme_system = UnifiedMemoryIntegrationSupreme(
            max_memory_gb=10.0,  # Reduzido para teste
            integration_level=IntegrationLevel.ENHANCED  # Menor complexidade
        )

        logger.info("✅ Supreme system imported and created successfully")

        # Teste 1: Inicialização básica dos core systems
        logger.info("🔧 Testing core systems initialization...")

        # Inicializa sistemas core individualmente
        await supreme_system._initialize_core_systems()
        logger.info("✅ Core systems initialized")

        # Teste 2: Registra alguns sistemas de memória funcionais
        logger.info("🧠 Registering working memory systems...")

        from dimensional_multiverse_memory import DimensionalMemorySystem
        from alchemical_transmutation_memory import AlchemicalMemorySystem
        from hyperdimensional_computing_memory import HyperdimensionalMemorySystem

        # Registra sistemas que funcionam
        working_systems = {
            'dimensional_multiverse': DimensionalMemorySystem(),
            'alchemical_transmutation': AlchemicalMemorySystem(),
            'hyperdimensional_computing': HyperdimensionalMemorySystem()
        }

        for name, system in working_systems.items():
            supreme_system.memory_systems[name] = system
            logger.info(f"✅ Registered {name}")

        # Teste 3: Configuração de modo cognitivo
        logger.info("🧠 Testing cognitive mode settings...")
        await supreme_system.set_cognitive_mode(CognitiveModes.PEAK_PERFORMANCE)
        logger.info(f"✅ Cognitive mode set to: {supreme_system.current_cognitive_mode.value}")

        # Teste 4: Processamento de tarefa simples
        logger.info("📝 Testing simple task processing...")

        task_content = "Analyze and store this test information for the supreme system"
        result = await supreme_system.process_supreme_task(
            content=task_content,
            task_type="general",
            priority=7
        )

        logger.info(f"✅ Task processed: {result}")

        # Teste 5: Métricas globais
        logger.info("📊 Testing global metrics collection...")
        await supreme_system._update_global_metrics()

        metrics = supreme_system.global_metrics
        logger.info(f"📈 Global metrics:")
        logger.info(f"   Active systems: {metrics.active_systems}")
        logger.info(f"   Memory usage: {metrics.total_memory_usage_gb:.2f}GB")
        logger.info(f"   Neural efficiency: {metrics.neural_efficiency:.3f}")
        logger.info(f"   Consciousness level: {metrics.consciousness_emergence:.3f}")

        # Teste 6: Status de consciência
        logger.info("🌟 Testing consciousness status...")
        consciousness_status = supreme_system.get_consciousness_status()
        logger.info(f"🧠 Consciousness status:")
        for key, value in consciousness_status.items():
            logger.info(f"   {key}: {value}")

        # Teste 7: Relatório supremo
        logger.info("📋 Generating supreme report...")
        report = await supreme_system.generate_supreme_report()

        # Salva relatório
        with open('supreme_integration_test_report.json', 'w') as f:
            json.dump(report, f, indent=2, default=str)

        logger.info("✅ Supreme integration test completed successfully!")
        logger.info("📄 Report saved to supreme_integration_test_report.json")

        return {
            'status': 'success',
            'systems_registered': len(working_systems),
            'consciousness_level': consciousness_status['consciousness_level'],
            'transcendence_progress': consciousness_status['transcendence_progress'],
            'report_generated': True
        }

    except Exception as e:
        logger.error(f"❌ Supreme integration test failed: {str(e)}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        return {
            'status': 'failed',
            'error': str(e)
        }

async def main():
    """Função principal"""
    result = await test_supreme_integration()

    if result['status'] == 'success':
        logger.info("🎉 SUPREME SYSTEM TEST: SUCCESS")
        logger.info(f"   Systems working: {result['systems_registered']}")
        logger.info(f"   Consciousness: {result['consciousness_level']:.3f}")
        if result.get('transcendence_progress', 0) > 0:
            logger.info(f"   Transcendence: {result['transcendence_progress']:.3f}")
    else:
        logger.error("💥 SUPREME SYSTEM TEST: FAILED")
        logger.error(f"   Error: {result['error']}")

    return result

if __name__ == "__main__":
    asyncio.run(main())