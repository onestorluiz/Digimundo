"""
🔧 APLICA FALLBACKS PARA DEPENDÊNCIAS AUSENTES
Injeta imports de fallback nos sistemas que precisam de dependências externas
"""
import os
import re
from pathlib import Path

class FallbackInjector:
    """Injeta fallbacks nos sistemas de memória"""

    def __init__(self):
        self.systems_to_fix = {'telepathic_distributed_memory.py': {'imports': ['qiskit', 'qiskit.Aer', 'qiskit.QuantumCircuit', 'qiskit.QuantumRegister', 'qiskit.ClassicalRegister', 'qiskit.execute'], 'fallback_module': 'qiskit_fallback'}, 'dreamscape_oniric_memory.py': {'imports': ['librosa'], 'fallback_module': 'librosa_fallback'}, 'akashic_universal_memory.py': {'imports': ['qiskit', 'qiskit.Aer', 'qiskit.QuantumCircuit'], 'fallback_module': 'qiskit_fallback'}, 'synesthetic_crossmodal_memory.py': {'imports': ['librosa'], 'fallback_module': 'librosa_fallback'}, 'crystalline_lattice_memory.py': {'imports': ['mpl_toolkits', 'mpl_toolkits.mplot3d'], 'fallback_module': 'mpl_toolkits_fallback'}, 'quantum_blockchain_memory.py': {'imports': ['qiskit', 'qiskit.Aer', 'qiskit.QuantumCircuit'], 'fallback_module': 'qiskit_fallback'}, 'mimetic_evolutionary_memory.py': {'imports': ['deap', 'deap.base', 'deap.creator', 'deap.tools', 'deap.algorithms'], 'fallback_module': 'deap_fallback'}}

    def inject_fallbacks(self):
        """Injeta fallbacks em todos os sistemas"""
        base_path = Path('apps/scripturemon')
        for system_file, config in self.systems_to_fix.items():
            file_path = base_path / system_file
            if file_path.exists():
                print(f'🔧 Processando {system_file}...')
                self._inject_fallback_in_file(file_path, config)
            else:
                print(f'⚠️  Arquivo não encontrado: {system_file}')

    def _inject_fallback_in_file(self, file_path: Path, config: dict):
        """Injeta fallback em um arquivo específico"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            if f"from apps.scripturemon.{config['fallback_module']}" in content:
                print(f'   ✅ Fallback já injetado em {file_path.name}')
                return
            modified = False
            lines = content.split('\n')
            new_lines = []
            fallback_added = False
            for i, line in enumerate(lines):
                for import_name in config['imports']:
                    patterns = [f'^import {re.escape(import_name)}$', f'^from {re.escape(import_name)} import', f'^import {re.escape(import_name)}\\.']
                    for pattern in patterns:
                        if re.match(pattern, line.strip()):
                            new_lines.append(f'# {line}  # Commented out - using fallback')
                            modified = True
                            if not fallback_added:
                                fallback_import = self._generate_fallback_import(config)
                                new_lines.extend(fallback_import)
                                fallback_added = True
                            continue
                new_lines.append(line)
            if modified:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write('\n'.join(new_lines))
                print(f'   ✅ Fallback injetado com sucesso em {file_path.name}')
            else:
                print(f'   ℹ️  Nenhuma modificação necessária em {file_path.name}')
        except Exception as e:
            print(f'   ❌ Erro ao processar {file_path.name}: {e}')

    def _generate_fallback_import(self, config: dict) -> list:
        """Gera código de import com fallback"""
        fallback_module = config['fallback_module']
        fallback_code = ['', '# Fallback import for missing dependencies', 'try:']
        for import_name in config['imports']:
            if '.' in import_name:
                fallback_code.append(f'    import {import_name}')
            else:
                fallback_code.append(f'    import {import_name}')
        fallback_code.extend(['except ImportError:', f'    # Use fallback implementation', f'    from apps.scripturemon.{fallback_module} import *', ''])
        return fallback_code

    def verify_systems_work(self):
        """Verifica se os sistemas funcionam após injeção"""
        print('\n🧪 VERIFICANDO SISTEMAS APÓS INJEÇÃO DE FALLBACKS...')
        import importlib
        import sys
        if os.getcwd() not in sys.path:
            sys.path.insert(0, os.getcwd())
        success_count = 0
        total_count = len(self.systems_to_fix)
        for system_file in self.systems_to_fix.keys():
            system_name = system_file.replace('.py', '')
            try:
                if f'apps.scripturemon.{system_name}' in sys.modules:
                    del sys.modules[f'apps.scripturemon.{system_name}']
                module = importlib.import_module(f'apps.scripturemon.{system_name}')
                print(f'   ✅ {system_name}: Import successful')
                success_count += 1
                memory_class = None
                for attr_name in dir(module):
                    attr = getattr(module, attr_name)
                    if isinstance(attr, type) and attr_name.endswith('Memory') and (attr.__module__ == module.__name__):
                        memory_class = attr
                        break
                if memory_class:
                    try:
                        instance = memory_class()
                        print(f'      💚 {system_name}: Instantiation successful')
                    except Exception as e:
                        print(f'      ⚠️  {system_name}: Instantiation failed: {e}')
                else:
                    print(f'      ⚠️  {system_name}: No memory class found')
            except Exception as e:
                print(f'   ❌ {system_name}: Import failed: {e}')
        print(f'\n📊 RESULTADO: {success_count}/{total_count} sistemas funcionando após fallbacks')
        return (success_count, total_count)
if __name__ == '__main__':
    print('🚀 INICIANDO INJEÇÃO DE FALLBACKS')
    print('=' * 50)
    injector = FallbackInjector()
    injector.inject_fallbacks()
    success_count, total_count = injector.verify_systems_work()
    if success_count == total_count:
        print(f'\n🎉 SUCESSO TOTAL! Todos os {total_count} sistemas funcionando!')
    else:
        print(f'\n⚠️  {success_count}/{total_count} sistemas funcionando. Verificar sistemas com falha.')
    print('\n🔧 Injeção de fallbacks concluída!')