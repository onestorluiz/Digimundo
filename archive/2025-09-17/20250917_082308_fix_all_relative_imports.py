#!/usr/bin/env python3
"""
🔧 Corrige todos os imports relativos de apps.scripturemon
"""

from pathlib import Path
import re

def fix_imports_in_file(file_path: Path) -> bool:
    """Corrige imports relativos em um arquivo"""
    print(f"  Processando {file_path.name}...", end="")

    try:
        with open(file_path, 'r') as f:
            content = f.read()

        # Verifica se tem imports para corrigir
        if 'from apps.scripturemon.' not in content:
            print(" ✅ Sem imports relativos")
            return False

        # Substitui todos os imports relativos
        original_content = content
        content = re.sub(r'from apps\.scripturemon\.', 'from ', content)

        if content != original_content:
            with open(file_path, 'w') as f:
                f.write(content)
            print(" ✅ Corrigido")
            return True
        else:
            print(" ✅ Já estava correto")
            return False

    except Exception as e:
        print(f" ❌ Erro: {str(e)}")
        return False

def main():
    """Corrige imports em todos os arquivos de memória"""
    memory_systems = [
        'memory_simple.py',
        'rules_memory.py',
        'persistent_memory_system_system_system_system.py',
        'memory_optimizer.py',
        'memory_federation.py',
        'alchemical_transmutation_memory.py',
        'entropic_reverse_memory.py',
        'mimetic_evolutionary_memory.py',
        'morphogenetic_memory.py',
        'holographic_fractal_memory.py',
        'dimensional_multiverse_memory.py',
        'hyperdimensional_computing_memory.py',
        'crystalline_lattice_memory.py',
        'memory_brain.py',
        'dreamscape_oniric_memory.py',
        'akashic_universal_memory.py',
        'synesthetic_crossmodal_memory.py',
        'telepathic_distributed_memory.py',
        'screenplay_crystal_memory.py',
        'memory_graph_universe.py',
        'quantum_blockchain_memory_nexus.py',
        'telepathic_distributed_memory_supreme.py',
        'memory_harmony_orchestrator.py',
        'mac_silicon_memory_maximizer.py'
    ]

    print("🔧 CORRIGINDO IMPORTS RELATIVOS")
    print("=" * 60)

    success = 0
    failed = 0

    for system in memory_systems:
        file_path = Path(system)
        if file_path.exists():
            if fix_imports_in_file(file_path):
                success += 1
            else:
                failed += 1
        else:
            print(f"  {system}: ❌ Não encontrado")
            failed += 1

    print(f"\n✅ Corrigidos: {success}")
    print(f"❌ Sem mudanças ou falhas: {failed}")

if __name__ == "__main__":
    main()