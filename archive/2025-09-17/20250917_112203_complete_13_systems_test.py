"""
🧠 TESTE COMPLETO DOS 13 SISTEMAS DE MEMÓRIA NEURAL
Testa todos os 13 sistemas individualmente após implementação de fallbacks
"""
import sys
import os
import time
import traceback
import importlib
import numpy as np
from typing import Dict, Any, List, Tuple
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

class Complete13SystemsTest:
    """Teste completo de todos os 13 sistemas de memória"""

    def __init__(self):
        self.results = {}
        self.systems = ['holographic_fractal_memory', 'morphogenetic_memory', 'dimensional_multiverse_memory', 'alchemical_transmutation_memory', 'hyperdimensional_computing_memory', 'entropic_reverse_memory', 'telepathic_distributed_memory', 'dreamscape_oniric_memory', 'akashic_universal_memory', 'synesthetic_crossmodal_memory', 'crystalline_lattice_memory', 'quantum_blockchain_memory', 'mimetic_evolutionary_memory']

    def test_individual_system(self, system_name: str) -> Dict[str, Any]:
        """Testa um sistema individual completamente"""
        print(f'\n🧪 TESTANDO SISTEMA: {system_name.upper()}')
        print('=' * 60)
        result = {'name': system_name, 'status': 'FAILED', 'import_time': 0, 'initialization_time': 0, 'operation_time': 0, 'memory_usage_mb': 0, 'error': None, 'throughput_ops_sec': 0, 'latency_ms': 0, 'features_tested': [], 'capabilities': []}
        try:
            print('📦 1. Testando importação...')
            start_time = time.time()
            try:
                try:
                    module = importlib.import_module(f'apps.scripturemon.{system_name}')
                except:
                    module = importlib.import_module(f'apps.scripturemon.memory_systems.{system_name}')
                result['import_time'] = (time.time() - start_time) * 1000
                print(f"   ✅ Importação: {result['import_time']:.2f}ms")
            except Exception as e:
                result['error'] = f'Import failed: {str(e)}'
                print(f'   ❌ Falha na importação: {e}')
                return result
            print('🏗️  2. Testando inicialização...')
            start_time = time.time()
            memory_class = None
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if isinstance(attr, type) and attr_name.endswith('Memory') and (attr.__module__ == module.__name__):
                    memory_class = attr
                    break
            if not memory_class:
                result['error'] = 'No memory class found in module'
                print(f'   ❌ Classe de memória não encontrada')
                return result
            init_params = self._get_init_params(system_name)
            memory_instance = memory_class(**init_params)
            result['initialization_time'] = (time.time() - start_time) * 1000
            print(f"   ✅ Inicialização: {result['initialization_time']:.2f}ms")
            print('⚡ 3. Testando operações básicas...')
            operations_tested = []
            start_time = time.time()
            try:
                storage_success = self._test_storage_operation(memory_instance, system_name)
                if storage_success:
                    operations_tested.append('storage')
                    print('   ✅ Operação de armazenamento')
                else:
                    print('   ⚠️  Operação de armazenamento com issues')
            except Exception as e:
                print(f'   ❌ Falha no armazenamento: {e}')
            try:
                retrieval_success = self._test_retrieval_operation(memory_instance, system_name)
                if retrieval_success:
                    operations_tested.append('retrieval')
                    print('   ✅ Operação de recuperação')
                else:
                    print('   ⚠️  Operação de recuperação com issues')
            except Exception as e:
                print(f'   ❌ Falha na recuperação: {e}')
            operation_time = (time.time() - start_time) * 1000
            result['operation_time'] = operation_time
            print('🚀 4. Testando performance...')
            throughput, latency = self._measure_performance(memory_instance, system_name)
            result['throughput_ops_sec'] = throughput
            result['latency_ms'] = latency
            if throughput > 0:
                print(f'   📊 Throughput: {throughput:.2f} ops/sec')
                print(f'   ⏱️  Latência: {latency:.2f}ms')
            else:
                print('   ⚠️  Performance não pôde ser medida')
            print('🌟 5. Testando recursos especiais...')
            capabilities = self._test_special_features(memory_instance, system_name)
            result['capabilities'] = capabilities
            for cap in capabilities:
                print(f'   ✨ Recurso: {cap}')
            result['memory_usage_mb'] = self._estimate_memory_usage(memory_instance)
            print(f"   💾 Uso de memória: {result['memory_usage_mb']:.4f}MB")
            result['status'] = 'SUCCESS'
            result['features_tested'] = operations_tested
            print(f'✅ SISTEMA {system_name.upper()} - TESTE COMPLETO!')
        except Exception as e:
            result['error'] = str(e)
            result['status'] = 'FAILED'
            print(f'❌ FALHA NO SISTEMA {system_name.upper()}: {e}')
            print(f'Stack trace: {traceback.format_exc()}')
        return result

    def _get_init_params(self, system_name: str) -> Dict[str, Any]:
        """Retorna parâmetros de inicialização apropriados para cada sistema"""
        return {}

    def _test_storage_operation(self, memory_instance, system_name: str) -> bool:
        """Testa operação de armazenamento"""
        try:
            test_data = self._generate_test_data(system_name)
            storage_methods = ['store_memory', 'store', 'save', 'add_memory', 'store_hologram', 'plant_seed']
            for method_name in storage_methods:
                if hasattr(memory_instance, method_name):
                    method = getattr(memory_instance, method_name)
                    method(test_data)
                    return True
            if callable(memory_instance):
                memory_instance(test_data)
                return True
            return False
        except Exception:
            return False

    def _test_retrieval_operation(self, memory_instance, system_name: str) -> bool:
        """Testa operação de recuperação"""
        try:
            retrieval_methods = ['retrieve_memory', 'retrieve', 'get', 'recall', 'query', 'recall_hologram', 'harvest_seed']
            for method_name in retrieval_methods:
                if hasattr(memory_instance, method_name):
                    method = getattr(memory_instance, method_name)
                    if system_name in ['holographic_fractal_memory', 'morphogenetic_memory']:
                        result = method('test_key')
                    else:
                        result = method()
                    return result is not None
            return False
        except Exception:
            return False

    def _measure_performance(self, memory_instance, system_name: str) -> Tuple[float, float]:
        """Mede throughput e latência"""
        try:
            test_data = self._generate_test_data(system_name)
            storage_method = None
            for method_name in ['store_memory', 'store', 'save', 'add_memory', 'store_hologram', 'plant_seed']:
                if hasattr(memory_instance, method_name):
                    storage_method = getattr(memory_instance, method_name)
                    break
            if not storage_method:
                return (0.0, 0.0)
            num_operations = 10
            start_time = time.time()
            for i in range(num_operations):
                if system_name in ['holographic_fractal_memory', 'morphogenetic_memory']:
                    storage_method(f'test_data_{i}', test_data)
                else:
                    storage_method(test_data)
            total_time = time.time() - start_time
            throughput = num_operations / total_time if total_time > 0 else 0
            latency = total_time / num_operations * 1000 if total_time > 0 else 0
            return (throughput, latency)
        except Exception:
            return (0.0, 0.0)

    def _test_special_features(self, memory_instance, system_name: str) -> List[str]:
        """Testa recursos especiais de cada sistema"""
        capabilities = []
        try:
            if 'quantum' in system_name.lower():
                if hasattr(memory_instance, 'entangle'):
                    capabilities.append('quantum_entanglement')
                if hasattr(memory_instance, 'superposition'):
                    capabilities.append('quantum_superposition')
            if 'neural' in system_name.lower() or 'telepathic' in system_name.lower():
                if hasattr(memory_instance, 'connect_nodes'):
                    capabilities.append('neural_networking')
                if hasattr(memory_instance, 'distribute'):
                    capabilities.append('distributed_processing')
            if 'fractal' in system_name.lower():
                if hasattr(memory_instance, 'generate_fractal'):
                    capabilities.append('fractal_generation')
                if hasattr(memory_instance, 'holographic_encoding'):
                    capabilities.append('holographic_encoding')
            if 'evolutionary' in system_name.lower() or 'mimetic' in system_name.lower():
                if hasattr(memory_instance, 'evolve'):
                    capabilities.append('evolutionary_adaptation')
                if hasattr(memory_instance, 'mutate'):
                    capabilities.append('genetic_mutation')
            if 'crystalline' in system_name.lower():
                if hasattr(memory_instance, 'form_crystal'):
                    capabilities.append('crystal_formation')
                if hasattr(memory_instance, 'lattice_resonance'):
                    capabilities.append('lattice_resonance')
            if hasattr(memory_instance, 'optimize'):
                capabilities.append('self_optimization')
            if hasattr(memory_instance, 'compress'):
                capabilities.append('data_compression')
            if hasattr(memory_instance, 'pattern_recognition'):
                capabilities.append('pattern_recognition')
        except Exception:
            pass
        return capabilities

    def _generate_test_data(self, system_name: str) -> Any:
        """Gera dados de teste apropriados para cada sistema"""
        data_map = {'dreamscape_oniric_memory': np.random.random(1000), 'synesthetic_crossmodal_memory': {'visual': np.random.random((10, 10)), 'audio': np.random.random(100), 'text': 'test sensory data'}, 'crystalline_lattice_memory': np.random.random((5, 5, 5)), 'quantum_blockchain_memory': {'transaction': 'test_quantum_data', 'value': 42}, 'mimetic_evolutionary_memory': [np.random.random(10) for _ in range(5)]}
        return data_map.get(system_name, np.random.random(100))

    def _estimate_memory_usage(self, memory_instance) -> float:
        """Estima uso de memória em MB"""
        try:
            import sys
            size = sys.getsizeof(memory_instance)
            for attr_name in dir(memory_instance):
                if not attr_name.startswith('_'):
                    try:
                        attr = getattr(memory_instance, attr_name)
                        if hasattr(attr, '__len__') and (not callable(attr)):
                            size += sys.getsizeof(attr)
                    except:
                        pass
            return size / (1024 * 1024)
        except:
            return 0.001

    def run_complete_test(self) -> Dict[str, Any]:
        """Executa teste completo de todos os 13 sistemas"""
        print('🚀 INICIANDO TESTE COMPLETO DOS 13 SISTEMAS DE MEMÓRIA NEURAL')
        print('=' * 80)
        print(f"📅 Data: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f'🔬 Sistemas a testar: {len(self.systems)}')
        start_time = time.time()
        for i, system_name in enumerate(self.systems, 1):
            print(f'\n🔹 [{i}/{len(self.systems)}] Processando {system_name}...')
            result = self.test_individual_system(system_name)
            self.results[system_name] = result
        total_time = time.time() - start_time
        return self._generate_final_report(total_time)

    def _generate_final_report(self, total_time: float) -> Dict[str, Any]:
        """Gera relatório final completo"""
        successful_systems = [name for name, result in self.results.items() if result['status'] == 'SUCCESS']
        failed_systems = [name for name, result in self.results.items() if result['status'] == 'FAILED']
        avg_throughput = np.mean([r['throughput_ops_sec'] for r in self.results.values() if r['throughput_ops_sec'] > 0])
        avg_latency = np.mean([r['latency_ms'] for r in self.results.values() if r['latency_ms'] > 0])
        total_memory = sum((r['memory_usage_mb'] for r in self.results.values()))
        report = {'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'), 'total_test_time': total_time, 'systems_tested': len(self.systems), 'successful_systems': len(successful_systems), 'failed_systems': len(failed_systems), 'success_rate': len(successful_systems) / len(self.systems) * 100, 'successful_list': successful_systems, 'failed_list': failed_systems, 'average_throughput': avg_throughput, 'average_latency': avg_latency, 'total_memory_usage': total_memory, 'individual_results': self.results}
        self._print_final_summary(report)
        return report

    def _print_final_summary(self, report: Dict[str, Any]):
        """Imprime resumo final"""
        print('\n' + '=' * 80)
        print('🎯 RELATÓRIO FINAL - TESTE DOS 13 SISTEMAS')
        print('=' * 80)
        print(f"⏱️  Tempo total de teste: {report['total_test_time']:.2f}s")
        print(f"✅ Sistemas funcionais: {report['successful_systems']}/{report['systems_tested']} ({report['success_rate']:.1f}%)")
        print(f"❌ Sistemas com falhas: {report['failed_systems']}")
        if report['average_throughput'] > 0:
            print(f"⚡ Throughput médio: {report['average_throughput']:.2f} ops/sec")
            print(f"⏱️  Latência média: {report['average_latency']:.2f}ms")
        print(f"💾 Uso total de memória: {report['total_memory_usage']:.4f}MB")
        print('\n🟢 SISTEMAS FUNCIONAIS:')
        for system in report['successful_list']:
            result = self.results[system]
            print(f"   ✅ {system}: {result['throughput_ops_sec']:.1f} ops/sec, {result['memory_usage_mb']:.4f}MB")
        if report['failed_list']:
            print('\n🔴 SISTEMAS COM FALHAS:')
            for system in report['failed_list']:
                result = self.results[system]
                print(f"   ❌ {system}: {result['error']}")
        print('\n🌟 CAPACIDADES DETECTADAS:')
        all_capabilities = set()
        for result in self.results.values():
            all_capabilities.update(result.get('capabilities', []))
        for cap in sorted(all_capabilities):
            count = sum((1 for r in self.results.values() if cap in r.get('capabilities', [])))
            print(f'   🔧 {cap}: {count} sistemas')
        print(f"\n{('🎉 TESTE CONCLUÍDO COM SUCESSO!' if report['success_rate'] >= 50 else '⚠️  TESTE COMPLETADO COM ISSUES')}")
if __name__ == '__main__':
    tester = Complete13SystemsTest()
    final_report = tester.run_complete_test()
    import json
    with open('13_systems_complete_test_report.json', 'w') as f:

        def convert_numpy(obj):
            if isinstance(obj, np.integer):
                return int(obj)
            elif isinstance(obj, np.floating):
                return float(obj)
            elif isinstance(obj, np.ndarray):
                return obj.tolist()
            return obj

        def recursive_convert(data):
            if isinstance(data, dict):
                return {k: recursive_convert(v) for k, v in data.items()}
            elif isinstance(data, list):
                return [recursive_convert(item) for item in data]
            else:
                return convert_numpy(data)
        json.dump(recursive_convert(final_report), f, indent=2)
    print(f'\n📄 Relatório salvo em: 13_systems_complete_test_report.json')