#!/usr/bin/env python3
"""
🚀 TESTE DO ECOSSISTEMA LIMPO - 24 SISTEMAS
Após remoção de 4 sistemas redundantes
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from typing import Dict, List, Tuple, Any
import time
import traceback

# Classes corretas dos sistemas após mapeamento
SYSTEM_CLASSES = {
    # Foundation Layer
    'memory_simple': ('memory_simple', 'MemorySimple'),
    'rules_memory': ('rules_memory', 'RulesMemory'),

    # Storage Layer
    'persistent_memory_system_system_system_system': ('persistent_memory_system_system_system_system', 'PersistentMemorySystem'),

    # Processing Layer
    'memory_optimizer': ('memory_optimizer', 'MemoryOptimizer'),
    'memory_federation': ('memory_federation', 'MemoryFederation'),
    'alchemical_transmutation_memory': ('alchemical_transmutation_memory', 'AlchemicalTransmutationMemory'),
    'entropic_reverse_memory': ('entropic_reverse_memory', 'EntropicReverseMemory'),
    'mimetic_evolutionary_memory': ('mimetic_evolutionary_memory', 'MimeticEvolutionaryMemory'),
    'morphogenetic_memory': ('morphogenetic_memory', 'MorphogeneticMemory'),
    'holographic_fractal_memory': ('holographic_fractal_memory', 'HolographicFractalMemory'),
    'dimensional_multiverse_memory': ('dimensional_multiverse_memory', 'DimensionalMultiverseMemory'),
    'hyperdimensional_computing_memory': ('hyperdimensional_computing_memory', 'HyperdimensionalComputingMemory'),
    'crystalline_lattice_memory': ('crystalline_lattice_memory', 'CrystallineLatticeMemory'),

    # Advanced Layer
    'memory_brain': ('memory_brain', 'MemoryBrain'),
    'dreamscape_oniric_memory': ('dreamscape_oniric_memory', 'DreamscapeMemory'),
    'akashic_universal_memory': ('akashic_universal_memory', 'AkashicMemory'),
    'synesthetic_crossmodal_memory': ('synesthetic_crossmodal_memory', 'SynestheticProcessor'),
    'telepathic_distributed_memory': ('telepathic_distributed_memory', 'TelepathicMemory'),
    'screenplay_crystal_memory': ('screenplay_crystal_memory', 'ScreenplayCrystalMemory'),
    'memory_graph_universe': ('memory_graph_universe', 'MemoryGraphUniverse'),

    # Supreme Layer
    'quantum_blockchain_memory_nexus': ('quantum_blockchain_memory_nexus', 'QuantumBlockchainMemoryNexus'),
    'telepathic_distributed_memory_supreme': ('telepathic_distributed_memory_supreme', 'TelepathicMemorySupreme'),
    'memory_harmony_orchestrator': ('memory_harmony_orchestrator', 'MemoryHarmonyOrchestrator'),
    'mac_silicon_memory_maximizer': ('mac_silicon_memory_maximizer', 'MacSiliconMemoryMaximizer'),
}

def test_system(name: str, module_path: str, class_name: str) -> Tuple[bool, str, float]:
    """Testa um sistema individual"""
    start_time = time.time()

    try:
        # Import dinâmico
        module = __import__(f'{module_path}', fromlist=[class_name])
        SystemClass = getattr(module, class_name)

        # Inicializa
        system = SystemClass()

        # Testa store/retrieve
        if hasattr(system, 'store_memory') and hasattr(system, 'retrieve_memory'):
            test_key = f"test_{name}"
            test_value = f"value_{name}"

            system.store_memory(test_key, test_value)
            result = system.retrieve_memory(test_key)

            success = result == test_value
            elapsed = time.time() - start_time

            if success:
                return True, "OK", elapsed
            else:
                return False, f"Valor incorreto: {result}", elapsed
        else:
            return False, "Métodos store/retrieve não encontrados", time.time() - start_time

    except Exception as e:
        error_msg = str(e).split('\n')[0][:50]
        return False, error_msg, time.time() - start_time

def main():
    """Testa todos os 24 sistemas"""
    print("=" * 80)
    print("🚀 TESTE DO ECOSSISTEMA LIMPO - 24 SISTEMAS")
    print("Após remoção de 4 sistemas redundantes")
    print("=" * 80)

    results = {}
    working_count = 0
    failed_count = 0

    for system_name, (module_path, class_name) in SYSTEM_CLASSES.items():
        print(f"\n📦 Testando {system_name}...")

        success, message, elapsed = test_system(system_name, module_path, class_name)

        if success:
            print(f"   ✅ FUNCIONANDO ({elapsed:.2f}s)")
            working_count += 1
            results[system_name] = 'working'
        else:
            print(f"   ❌ FALHOU: {message}")
            failed_count += 1
            results[system_name] = 'failed'

    # Estatísticas finais
    total = len(SYSTEM_CLASSES)
    success_rate = (working_count / total) * 100

    print("\n" + "=" * 80)
    print("📊 RESULTADO FINAL DO ECOSSISTEMA LIMPO")
    print("=" * 80)

    print(f"\n✅ Sistemas funcionando: {working_count}/{total} ({success_rate:.1f}%)")
    print(f"❌ Sistemas com falha: {failed_count}/{total}")

    # Lista por camada
    layers = {
        'Foundation': ['memory_simple', 'rules_memory'],
        'Storage': ['persistent_memory_system_system_system_system'],
        'Processing': [
            'memory_optimizer', 'memory_federation', 'alchemical_transmutation_memory',
            'entropic_reverse_memory', 'mimetic_evolutionary_memory', 'morphogenetic_memory',
            'holographic_fractal_memory', 'dimensional_multiverse_memory',
            'hyperdimensional_computing_memory', 'crystalline_lattice_memory'
        ],
        'Advanced': [
            'memory_brain', 'dreamscape_oniric_memory', 'akashic_universal_memory',
            'synesthetic_crossmodal_memory', 'telepathic_distributed_memory',
            'screenplay_crystal_memory', 'memory_graph_universe'
        ],
        'Supreme': [
            'quantum_blockchain_memory_nexus', 'telepathic_distributed_memory_supreme',
            'memory_harmony_orchestrator', 'mac_silicon_memory_maximizer'
        ]
    }

    print("\n📊 Status por camada:")
    for layer_name, systems in layers.items():
        working = sum(1 for s in systems if s in results and results[s] == 'working')
        total_layer = len(systems)
        print(f"   {layer_name}: {working}/{total_layer} funcionando")

    # Comparação antes/depois
    print("\n🔄 COMPARAÇÃO ANTES/DEPOIS DA LIMPEZA:")
    print("   Antes: 28 sistemas (60.7% funcionando)")
    print(f"   Depois: 24 sistemas ({success_rate:.1f}% funcionando)")
    print(f"   Melhoria: {success_rate - 60.7:.1f}%")

    if success_rate >= 70:
        print("\n🎉 OBJETIVO ALCANÇADO! Taxa de sucesso > 70%")
        print("   Ecossistema limpo e eficiente!")

    return working_count, failed_count

if __name__ == "__main__":
    working, failed = main()
    sys.exit(0 if working >= 20 else 1)  # Sucesso se >= 20 sistemas funcionando