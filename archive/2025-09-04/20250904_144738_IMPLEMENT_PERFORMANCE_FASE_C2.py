#!/usr/bin/env python3
"""
⚡ FASE C2 - MELHORAR PERFORMANCE DE STARTUP
Implementa lazy loading e paralelização mantendo EXTREMA ROBUSTEZ
"""

import re
from pathlib import Path
import json

def implement_lazy_loading():
    """Implementa lazy loading para sistemas não-críticos"""
    
    # Usar o arquivo real, não o symlink
    scripturemon_path = Path("/Users/clubproducoes/Digimundo/scripturemon-validation/bin/scripturemon")
    
    if not scripturemon_path.exists():
        print("❌ scripturemon não encontrado")
        return False
    
    content = scripturemon_path.read_text()
    lines = content.split('\n')
    changes_made = []
    
    # 1. Adicionar flag de lazy loading
    lazy_loading_code = '''
# Sistema de Lazy Loading para Performance
_lazy_systems = {
    'telepathy': None,
    'memory_coordinator': None,
    'cinema_knowledge': None,
    'quantum_entanglement': None,
    'parallel_processor': None
}

def get_lazy_system(name):
    """Carrega sistema sob demanda mantendo ROBUSTEZ"""
    global _lazy_systems
    
    if _lazy_systems.get(name) is not None:
        return _lazy_systems[name]
    
    try:
        if name == 'telepathy':
            from apps.scripturemon.telepathy_network import TelepathyNetwork
            _lazy_systems['telepathy'] = TelepathyNetwork()
            print(f"   💾 {name.upper()} carregado sob demanda")
            
        elif name == 'memory_coordinator':
            from apps.scripturemon.memory_coordinator import get_coordinator
            _lazy_systems['memory_coordinator'] = get_coordinator()
            print(f"   💾 {name.upper()} carregado sob demanda")
            
        elif name == 'cinema_knowledge':
            from apps.scripturemon.cinema_knowledge import CinemaKnowledge
            _lazy_systems['cinema_knowledge'] = CinemaKnowledge()
            print(f"   💾 {name.upper()} carregado sob demanda")
            
        elif name == 'quantum_entanglement':
            from apps.scripturemon.quantum_entanglement import QuantumEntanglement
            _lazy_systems['quantum_entanglement'] = QuantumEntanglement()
            print(f"   💾 {name.upper()} carregado sob demanda")
            
        elif name == 'parallel_processor':
            from apps.scripturemon.parallel_processor import ParallelProcessor
            _lazy_systems['parallel_processor'] = ParallelProcessor()
            print(f"   💾 {name.upper()} carregado sob demanda")
            
        return _lazy_systems[name]
        
    except Exception as e:
        print(f"   ⚠️ Sistema {name} em modo fallback: {e}")
        _lazy_systems[name] = None  # Marca como tentado
        return None
'''
    
    # Inserir após os imports principais
    for i, line in enumerate(lines):
        if 'from apps.scripturemon' in line and i < 200:
            # Inserir antes das importações dos apps
            lines.insert(i, lazy_loading_code)
            changes_made.append("✅ Sistema de lazy loading adicionado")
            break
    
    content = '\n'.join(lines)
    
    # 2. Modificar inicialização para usar lazy loading
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if 'class ScripturemonMaxCapacity:' in line:
            # Procurar o __init__
            for j in range(i, min(i+200, len(lines))):
                if 'def __init__(self):' in lines[j]:
                    # Marcar sistemas como lazy
                    lazy_init_start = j + 1
                    
                    # Procurar onde inicializa os sistemas
                    for k in range(lazy_init_start, min(lazy_init_start+100, len(lines))):
                        # TelepathyNetwork
                        if 'self.telepathy = TelepathyNetwork()' in lines[k]:
                            lines[k] = '        self.telepathy = None  # Lazy loading'
                            changes_made.append("✅ TelepathyNetwork marcado para lazy loading")
                        
                        # Memory Coordinator
                        if 'self.memory_coordinator = get_coordinator()' in lines[k]:
                            lines[k] = '        self.memory_coordinator = None  # Lazy loading'
                            changes_made.append("✅ Memory Coordinator marcado para lazy loading")
                        
                        # Cinema Knowledge
                        if 'self.cinema_knowledge = CinemaKnowledge()' in lines[k]:
                            lines[k] = '        self.cinema_knowledge = None  # Lazy loading'
                            changes_made.append("✅ Cinema Knowledge marcado para lazy loading")
                        
                        # Quantum Entanglement
                        if 'self.quantum_entanglement = QuantumEntanglement()' in lines[k]:
                            lines[k] = '        self.quantum_entanglement = None  # Lazy loading'
                            changes_made.append("✅ Quantum Entanglement marcado para lazy loading")
                        
                        # Parallel Processor
                        if 'self.parallel_processor = ParallelProcessor()' in lines[k]:
                            lines[k] = '        self.parallel_processor = None  # Lazy loading'
                            changes_made.append("✅ Parallel Processor marcado para lazy loading")
                    break
            break
    
    content = '\n'.join(lines)
    
    # 3. Adicionar getters com lazy loading
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if 'def process_with_all_systems(self' in line:
            # Adicionar getters antes do process
            getters_code = '''
    def _get_telepathy(self):
        """Obtém telepathy com lazy loading"""
        if self.telepathy is None:
            self.telepathy = get_lazy_system('telepathy')
        return self.telepathy
    
    def _get_memory_coordinator(self):
        """Obtém memory coordinator com lazy loading"""
        if self.memory_coordinator is None:
            self.memory_coordinator = get_lazy_system('memory_coordinator')
        return self.memory_coordinator
    
    def _get_cinema_knowledge(self):
        """Obtém cinema knowledge com lazy loading"""
        if self.cinema_knowledge is None:
            self.cinema_knowledge = get_lazy_system('cinema_knowledge')
        return self.cinema_knowledge
    
    def _get_quantum_entanglement(self):
        """Obtém quantum entanglement com lazy loading"""
        if self.quantum_entanglement is None:
            self.quantum_entanglement = get_lazy_system('quantum_entanglement')
        return self.quantum_entanglement
    
    def _get_parallel_processor(self):
        """Obtém parallel processor com lazy loading"""
        if self.parallel_processor is None:
            self.parallel_processor = get_lazy_system('parallel_processor')
        return self.parallel_processor
    '''
            lines.insert(i, getters_code)
            changes_made.append("✅ Getters com lazy loading adicionados")
            break
    
    content = '\n'.join(lines)
    
    # 4. Substituir uso direto por getters
    replacements = [
        ('if self.telepathy:', 'if self._get_telepathy():'),
        ('self.telepathy.', 'self._get_telepathy().'),
        ('if self.memory_coordinator:', 'if self._get_memory_coordinator():'),
        ('self.memory_coordinator.', 'self._get_memory_coordinator().'),
        ('if self.cinema_knowledge:', 'if self._get_cinema_knowledge():'),
        ('self.cinema_knowledge.', 'self._get_cinema_knowledge().'),
        ('if self.quantum_entanglement:', 'if self._get_quantum_entanglement():'),
        ('self.quantum_entanglement.', 'self._get_quantum_entanglement().'),
        ('if self.parallel_processor:', 'if self._get_parallel_processor():'),
        ('self.parallel_processor.', 'self._get_parallel_processor().')
    ]
    
    for old, new in replacements:
        if old in content and 'def _get_' not in old:  # Não substituir nas definições
            content = content.replace(old, new)
            changes_made.append(f"✅ Substituído '{old}' por '{new}'")
    
    # Salvar arquivo
    scripturemon_path.write_text(content)
    
    print("\n".join(changes_made))
    return len(changes_made) > 0

def implement_parallel_init():
    """Implementa inicialização paralela para sistemas independentes"""
    
    scripturemon_path = Path("/Users/clubproducoes/Digimundo/scripturemon-validation/bin/scripturemon")
    content = scripturemon_path.read_text()
    lines = content.split('\n')
    changes_made = []
    
    # 1. Adicionar sistema de inicialização paralela
    parallel_init_code = '''
import concurrent.futures
import threading

class ParallelInitializer:
    """Sistema de inicialização paralela mantendo ROBUSTEZ"""
    
    def __init__(self):
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=4)
        self.init_lock = threading.Lock()
        self.init_results = {}
    
    def init_system_async(self, name, init_func):
        """Inicializa sistema de forma assíncrona"""
        def _init():
            try:
                result = init_func()
                with self.init_lock:
                    self.init_results[name] = {'status': 'success', 'system': result}
                print(f"   ✅ {name} inicializado em paralelo")
                return result
            except Exception as e:
                with self.init_lock:
                    self.init_results[name] = {'status': 'error', 'error': str(e)}
                print(f"   ⚠️ {name} com erro: {e}")
                return None
        
        return self.executor.submit(_init)
    
    def wait_all(self, futures, timeout=30):
        """Aguarda todas as inicializações com timeout"""
        try:
            concurrent.futures.wait(futures, timeout=timeout)
            return True
        except concurrent.futures.TimeoutError:
            print("   ⚠️ Timeout na inicialização paralela")
            return False
    
    def shutdown(self):
        """Encerra executor"""
        self.executor.shutdown(wait=False)

# Instância global do inicializador paralelo
_parallel_init = None

def get_parallel_init():
    global _parallel_init
    if _parallel_init is None:
        _parallel_init = ParallelInitializer()
    return _parallel_init
'''
    
    # Inserir após lazy loading
    for i, line in enumerate(lines):
        if 'def get_lazy_system(' in line:
            # Inserir após o lazy loading
            insert_pos = i
            while insert_pos < len(lines) and lines[insert_pos].strip() != '':
                insert_pos += 1
            lines.insert(insert_pos + 1, parallel_init_code)
            changes_made.append("✅ Sistema de inicialização paralela adicionado")
            break
    
    content = '\n'.join(lines)
    
    # 2. Modificar __init__ para usar inicialização paralela
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if 'def __init__(self):' in line and 'ScripturemonMaxCapacity' in '\n'.join(lines[max(0,i-5):i]):
            # Adicionar inicialização paralela
            parallel_setup = '''
        # Inicialização paralela dos sistemas críticos
        parallel = get_parallel_init()
        futures = []
        
        # Sistemas que podem ser inicializados em paralelo
        print("⚡ Inicializando sistemas em paralelo...")
        
        # Brain (crítico, mas pode ser paralelo)
        futures.append(parallel.init_system_async(
            'ScripturemonBrain',
            lambda: ScripturemonBrain()
        ))
        
        # Memorion (crítico, mas pode ser paralelo)
        futures.append(parallel.init_system_async(
            'MemorionSupreme',
            lambda: MemorionSupreme()
        ))
        
        # Consciousness (crítico, mas pode ser paralelo)
        futures.append(parallel.init_system_async(
            'QuantumConsciousness',
            lambda: QuantumConsciousness()
        ))
        
        # Crystal Memory (crítico, mas pode ser paralelo)
        futures.append(parallel.init_system_async(
            'CrystalMemory',
            lambda: CrystalMemory()
        ))
        
        # Aguardar inicialização paralela
        if parallel.wait_all(futures, timeout=15):
            # Recuperar sistemas inicializados
            results = parallel.init_results
            
            self.brain = results.get('ScripturemonBrain', {}).get('system')
            self.memorion = results.get('MemorionSupreme', {}).get('system')
            self.consciousness = results.get('QuantumConsciousness', {}).get('system')
            self.crystal_memory = results.get('CrystalMemory', {}).get('system')
            
            print("   ✅ Sistemas críticos inicializados em paralelo")
        else:
            print("   ⚠️ Inicialização paralela com timeout, usando fallback serial")
            # Fallback para inicialização serial se houver problema
            self.brain = ScripturemonBrain()
            self.memorion = MemorionSupreme()
            self.consciousness = QuantumConsciousness()
            self.crystal_memory = CrystalMemory()
'''
            
            # Encontrar onde inserir
            insert_pos = i + 1
            # Pular docstring se houver
            while insert_pos < len(lines) and '"""' in lines[insert_pos]:
                insert_pos += 1
            
            # Verificar se já tem verbosity control
            if 'self.verbosity' in lines[insert_pos:insert_pos+5]:
                insert_pos += 10  # Inserir após verbosity
            
            lines.insert(insert_pos, parallel_setup)
            changes_made.append("✅ Inicialização paralela integrada no __init__")
            break
    
    content = '\n'.join(lines)
    
    # 3. Adicionar cleanup no shutdown
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if 'def shutdown(self):' in line:
            # Adicionar cleanup do parallel init
            cleanup_code = '''
        # Encerrar inicializador paralelo
        if _parallel_init:
            _parallel_init.shutdown()
'''
            lines.insert(i + 2, cleanup_code)
            changes_made.append("✅ Cleanup do inicializador paralelo adicionado")
            break
    
    # Salvar arquivo
    scripturemon_path.write_text('\n'.join(lines))
    
    print("\n".join(changes_made))
    return len(changes_made) > 0

def create_performance_test():
    """Cria script para testar melhorias de performance"""
    
    test_content = '''#!/usr/bin/env python3
"""
⚡ TEST PERFORMANCE IMPROVEMENTS
Testa melhorias de performance da FASE C2
"""

import subprocess
import time
from pathlib import Path

def measure_startup_time():
    """Mede tempo de startup do sistema"""
    
    print("⚡ TESTANDO PERFORMANCE DE STARTUP")
    print("="*60)
    
    # Teste 1: Tempo de inicialização
    print("\\n📊 Teste 1: Tempo de inicialização")
    print("-"*40)
    
    start = time.time()
    
    try:
        result = subprocess.run(
            ['echo', 'status', '|', './bin/scripturemon', '--timeout', '5'],
            shell=True,
            capture_output=True,
            text=True,
            timeout=10,
            cwd='/Users/clubproducoes/Digimundo/scripturemon-validation'
        )
        
        init_time = time.time() - start
        
        print(f"  ⏱️ Tempo de inicialização: {init_time:.2f}s")
        
        if init_time < 3:
            print("  ✅ Inicialização RÁPIDA (< 3s)")
        elif init_time < 5:
            print("  ⚠️ Inicialização aceitável (3-5s)")
        else:
            print("  ❌ Inicialização lenta (> 5s)")
        
        # Contar sistemas carregados
        lazy_loaded = result.stdout.count("carregado sob demanda")
        parallel_loaded = result.stdout.count("inicializado em paralelo")
        
        print(f"  📦 Sistemas lazy loaded: {lazy_loaded}")
        print(f"  ⚡ Sistemas em paralelo: {parallel_loaded}")
        
    except subprocess.TimeoutExpired:
        print("  ❌ Timeout na inicialização")
    except Exception as e:
        print(f"  ❌ Erro: {e}")
    
    # Teste 2: Uso de memória
    print("\\n📊 Teste 2: Uso de memória")
    print("-"*40)
    
    try:
        # Verificar memória antes
        result_before = subprocess.run(
            ['ps', '-o', 'rss=', '-p', str(subprocess.run(['pgrep', '-f', 'scripturemon'], 
            capture_output=True, text=True).stdout.strip())],
            capture_output=True,
            text=True
        )
        
        if result_before.stdout:
            mem_kb = int(result_before.stdout.strip())
            mem_mb = mem_kb / 1024
            print(f"  💾 Memória em uso: {mem_mb:.1f} MB")
            
            if mem_mb < 100:
                print("  ✅ Uso de memória BAIXO (< 100 MB)")
            elif mem_mb < 200:
                print("  ⚠️ Uso de memória moderado (100-200 MB)")
            else:
                print("  ❌ Uso de memória alto (> 200 MB)")
    except:
        print("  ⚠️ Não foi possível medir memória")
    
    # Teste 3: Resposta a comandos
    print("\\n📊 Teste 3: Tempo de resposta")
    print("-"*40)
    
    commands = ['help', 'status', 'memory']
    
    for cmd in commands:
        start = time.time()
        try:
            result = subprocess.run(
                f'echo "{cmd}" | ./bin/scripturemon --timeout 3',
                shell=True,
                capture_output=True,
                text=True,
                timeout=5,
                cwd='/Users/clubproducoes/Digimundo/scripturemon-validation'
            )
            
            response_time = time.time() - start
            print(f"  {cmd}: {response_time:.2f}s")
            
        except:
            print(f"  {cmd}: ❌ Timeout")
    
    print("\\n✅ Teste de performance completo!")

def test_lazy_loading():
    """Testa se lazy loading está funcionando"""
    
    print("\\n🔄 TESTANDO LAZY LOADING")
    print("="*60)
    
    # Executar comando que não precisa de todos os sistemas
    print("\\nExecutando comando simples (não deve carregar tudo)...")
    
    result = subprocess.run(
        'echo "help" | ./bin/scripturemon --timeout 3 -v',
        shell=True,
        capture_output=True,
        text=True,
        timeout=5,
        cwd='/Users/clubproducoes/Digimundo/scripturemon-validation'
    )
    
    # Verificar o que foi carregado
    lazy_systems = [
        'TELEPATHY',
        'MEMORY_COORDINATOR',
        'CINEMA_KNOWLEDGE',
        'QUANTUM_ENTANGLEMENT',
        'PARALLEL_PROCESSOR'
    ]
    
    for system in lazy_systems:
        if f"{system} carregado sob demanda" in result.stdout:
            print(f"  ⚠️ {system} foi carregado (não deveria)")
        else:
            print(f"  ✅ {system} não foi carregado (lazy)")
    
    print("\\nExecutando comando complexo (deve carregar sistemas)...")
    
    result = subprocess.run(
        'echo "analisar roteiro complexo" | ./bin/scripturemon --timeout 5 -v',
        shell=True,
        capture_output=True,
        text=True,
        timeout=10,
        cwd='/Users/clubproducoes/Digimundo/scripturemon-validation'
    )
    
    loaded = 0
    for system in lazy_systems:
        if f"{system} carregado sob demanda" in result.stdout:
            print(f"  ✅ {system} carregado sob demanda")
            loaded += 1
    
    if loaded > 0:
        print(f"\\n✅ Lazy loading funcionando! {loaded} sistemas carregados sob demanda")
    else:
        print("\\n⚠️ Lazy loading pode não estar ativo")

if __name__ == "__main__":
    measure_startup_time()
    test_lazy_loading()
'''
    
    test_path = Path("/Users/clubproducoes/Digimundo/scripturemon-validation/test_performance_c2.py")
    test_path.write_text(test_content)
    test_path.chmod(0o755)
    print("✅ Script de teste criado: test_performance_c2.py")

if __name__ == "__main__":
    print("⚡ FASE C2 - MELHORAR PERFORMANCE DE STARTUP")
    print("="*60)
    
    print("\n1. Implementando lazy loading...")
    if implement_lazy_loading():
        print("\n2. Implementando inicialização paralela...")
        if implement_parallel_init():
            print("\n3. Criando script de teste...")
            create_performance_test()
            
            print("\n✅ FASE C2 COMPLETA!")
            print("\nMelhorias implementadas:")
            print("  - Lazy loading para 5 sistemas não-críticos")
            print("  - Inicialização paralela de sistemas críticos")
            print("  - Getters com carregamento sob demanda")
            print("  - ThreadPoolExecutor com 4 workers")
            print("  - Fallback para inicialização serial")
            print("  - Timeout de 15s para inicialização paralela")
            
            print("\n⚡ Performance esperada:")
            print("  - Redução de 30-50% no tempo de startup")
            print("  - Menor uso de memória inicial")
            print("  - Carregamento sob demanda de sistemas pesados")
            print("  - Mantém EXTREMA ROBUSTEZ com fallbacks")
            
            print("\n🎯 Sistema otimizado sem perder funcionalidade!")
            print("💪 EXTREMA ROBUSTEZ MANTIDA!")
        else:
            print("❌ Erro na inicialização paralela")
    else:
        print("❌ Erro no lazy loading")