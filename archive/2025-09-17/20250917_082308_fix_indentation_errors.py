#!/usr/bin/env python3
"""
🔧 CORRETOR DE ERROS DE INDENTAÇÃO
Corrige os erros causados pelo script anterior
"""

import os
import re
from pathlib import Path

def fix_indentation(file_path: Path) -> bool:
    """Corrige problemas de indentação em um arquivo Python"""

    with open(file_path, 'r') as f:
        lines = f.readlines()

    fixed = False
    fixed_lines = []
    in_class = False
    class_indent = 0

    for i, line in enumerate(lines):
        # Detecta início de classe
        if line.strip().startswith('class '):
            in_class = True
            class_indent = len(line) - len(line.lstrip())
            fixed_lines.append(line)
            continue

        # Detecta fim de classe (linha sem indentação ou nova classe)
        if in_class and line and not line.startswith(' ') and not line.startswith('\t'):
            in_class = False

        # Procura por métodos mal indentados
        if in_class and 'def store_memory' in line:
            # Verifica se a indentação está correta
            current_indent = len(line) - len(line.lstrip())
            expected_indent = class_indent + 4

            if current_indent != expected_indent:
                # Corrige a indentação
                line = ' ' * expected_indent + line.lstrip()
                fixed = True

        if in_class and 'def retrieve_memory' in line:
            # Verifica se a indentação está correta
            current_indent = len(line) - len(line.lstrip())
            expected_indent = class_indent + 4

            if current_indent != expected_indent:
                # Corrige a indentação
                line = ' ' * expected_indent + line.lstrip()
                fixed = True

        # Corrige linhas subsequentes de métodos mal indentados
        if i > 0 and '    def store_memory' in lines[i-1]:
            if line.strip() and not line.strip().startswith('def '):
                # Esta linha deve estar indentada em relação ao def
                current_indent = len(line) - len(line.lstrip())
                expected_indent = class_indent + 8  # Dentro do método

                if current_indent < expected_indent:
                    line = ' ' * expected_indent + line.lstrip()
                    fixed = True

        if i > 0 and '    def retrieve_memory' in lines[i-1]:
            if line.strip() and not line.strip().startswith('def '):
                # Esta linha deve estar indentada em relação ao def
                current_indent = len(line) - len(line.lstrip())
                expected_indent = class_indent + 8  # Dentro do método

                if current_indent < expected_indent:
                    line = ' ' * expected_indent + line.lstrip()
                    fixed = True

        fixed_lines.append(line)

    if fixed:
        # Salva o arquivo corrigido
        with open(file_path, 'w') as f:
            f.writelines(fixed_lines)

    return fixed

def main():
    """Corrige indentação em todos os sistemas com erro"""

    systems_with_errors = [
        ('memory_simple.py', 354),
        ('rules_memory.py', 713),
        ('persistent_memory_system_system_system_system.py', 635),
        ('memory_optimizer.py', 169),
        ('memory_federation.py', 77),
        ('alchemical_transmutation_memory.py', 127),
        ('entropic_reverse_memory.py', 120),
        ('mimetic_evolutionary_memory.py', 92),
        ('holographic_fractal_memory.py', 558),
        ('dimensional_multiverse_memory.py', 138),
        ('hyperdimensional_computing_memory.py', 743),
        ('crystalline_lattice_memory.py', 155),
        ('memory_brain.py', 572),
        ('memory_graph_universe.py', 853),
        ('quantum_blockchain_memory_nexus.py', 1422),
        ('telepathic_distributed_memory_supreme.py', 1068),
        ('memory_harmony_orchestrator.py', 655),
        ('mac_silicon_memory_maximizer.py', 918)
    ]

    print("🔧 CORRIGINDO ERROS DE INDENTAÇÃO")
    print("=" * 60)

    fixed_count = 0

    for file_name, error_line in systems_with_errors:
        file_path = Path(file_name)

        if not file_path.exists():
            print(f"❌ {file_name}: não encontrado")
            continue

        print(f"Processando {file_name} (erro na linha {error_line})...", end="")

        if fix_indentation(file_path):
            print(" ✅ Corrigido")
            fixed_count += 1
        else:
            print(" ⚠️ Nenhuma correção necessária")

    print(f"\n✅ {fixed_count} arquivos corrigidos")

if __name__ == "__main__":
    main()