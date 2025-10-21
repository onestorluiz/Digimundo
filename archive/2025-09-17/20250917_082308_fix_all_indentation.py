#!/usr/bin/env python3
"""
🔧 CORRETOR DEFINITIVO DE INDENTAÇÃO
Remove métodos mal adicionados e os re-adiciona corretamente
"""

import os
import re
import ast
from pathlib import Path
from typing import List, Tuple

def remove_bad_methods(lines: List[str]) -> Tuple[List[str], bool]:
    """Remove métodos store_memory e retrieve_memory mal indentados"""
    cleaned_lines = []
    skip_until_next_def = False
    removed = False

    i = 0
    while i < len(lines):
        line = lines[i]

        # Detecta métodos mal indentados (não começam com exatamente 4 espaços)
        if 'def store_memory' in line or 'def retrieve_memory' in line:
            indent = len(line) - len(line.lstrip())

            # Se não está com 4 espaços de indentação, é um método mal indentado
            if indent != 4:
                # Pula até o próximo def ou fim da classe
                skip_until_next_def = True
                removed = True
                i += 1
                continue

        # Se estamos pulando linhas
        if skip_until_next_def:
            # Verifica se chegamos a um novo método ou fim de classe
            if line.strip().startswith('def ') or (line and not line[0].isspace()):
                skip_until_next_def = False
                cleaned_lines.append(line)
            # Senão, continua pulando
            i += 1
            continue

        cleaned_lines.append(line)
        i += 1

    return cleaned_lines, removed

def add_correct_methods(lines: List[str]) -> List[str]:
    """Adiciona métodos store_memory e retrieve_memory corretamente"""
    result = []
    class_found = False
    class_name = None
    last_method_index = -1
    indent_level = 0

    # Primeiro, procura a classe principal
    for i, line in enumerate(lines):
        if line.strip().startswith('class ') and not line.strip().startswith('class '):
            # Classe principal encontrada
            class_found = True
            class_name = line.strip().split('(')[0].replace('class ', '').strip(':')
            indent_level = len(line) - len(line.lstrip())

        # Marca onde está o último método da classe
        if class_found and line.strip().startswith('def '):
            current_indent = len(line) - len(line.lstrip())
            if current_indent == indent_level + 4:  # Método da classe principal
                last_method_index = i

    # Se não encontrou classe, retorna como está
    if not class_found or last_method_index == -1:
        return lines

    # Verifica se já tem os métodos corretos
    has_store = False
    has_retrieve = False

    for line in lines:
        if '    def store_memory(self, key: str, value: Any) -> None:' in line:
            has_store = True
        if '    def retrieve_memory(self, key: str) -> Optional[Any]:' in line:
            has_retrieve = True

    # Se já tem ambos, retorna como está
    if has_store and has_retrieve:
        return lines

    # Encontra o fim do último método
    insert_index = last_method_index + 1
    while insert_index < len(lines):
        line = lines[insert_index]
        # Se encontrar uma linha sem indentação ou um novo def no mesmo nível
        if line and not line[0].isspace():
            break
        if line.strip().startswith('def ') and len(line) - len(line.lstrip()) == indent_level + 4:
            break
        insert_index += 1

    # Métodos a adicionar
    methods = []

    if not has_store:
        methods.append("""
    def store_memory(self, key: str, value: Any) -> None:
        \"\"\"Método wrapper para compatibilidade com interface padrão\"\"\"
        if hasattr(self, 'store'):
            self.store(key, value)
        elif hasattr(self, 'add'):
            self.add(key, value)
        elif hasattr(self, 'write'):
            self.write(key, value)
        elif hasattr(self, 'save'):
            self.save(key, value)
        elif hasattr(self, 'set'):
            self.set(key, value)
        elif hasattr(self, 'put'):
            self.put(key, value)
        else:
            if not hasattr(self, '_memory_storage'):
                self._memory_storage = {}
            self._memory_storage[key] = value
""")

    if not has_retrieve:
        methods.append("""
    def retrieve_memory(self, key: str) -> Optional[Any]:
        \"\"\"Método wrapper para compatibilidade com interface padrão\"\"\"
        if hasattr(self, 'retrieve'):
            return self.retrieve(key)
        elif hasattr(self, 'get'):
            return self.get(key)
        elif hasattr(self, 'read'):
            return self.read(key)
        elif hasattr(self, 'load'):
            return self.load(key)
        elif hasattr(self, 'recall'):
            return self.recall(key)
        elif hasattr(self, 'fetch'):
            return self.fetch(key)
        else:
            if hasattr(self, '_memory_storage'):
                return self._memory_storage.get(key)
            return None
""")

    # Insere os métodos
    result = lines[:insert_index]
    for method in methods:
        result.extend(method.split('\n'))
    result.extend(lines[insert_index:])

    return result

def fix_file(file_path: Path) -> bool:
    """Corrige um arquivo Python"""
    print(f"  Processando {file_path.name}...", end="")

    try:
        with open(file_path, 'r') as f:
            original_lines = f.readlines()

        # Remove métodos mal indentados
        lines, removed = remove_bad_methods(original_lines)

        # Adiciona métodos corretos
        if removed or True:  # Sempre tenta adicionar se não existir
            lines = add_correct_methods(lines)

        # Salva o arquivo
        with open(file_path, 'w') as f:
            f.writelines(lines)

        # Verifica sintaxe
        with open(file_path, 'r') as f:
            content = f.read()
            ast.parse(content)

        print(" ✅")
        return True

    except SyntaxError as e:
        print(f" ❌ Erro de sintaxe na linha {e.lineno}")
        # Restaura o original se houver erro
        with open(file_path, 'w') as f:
            f.writelines(original_lines)
        return False
    except Exception as e:
        print(f" ❌ {str(e)}")
        return False

def main():
    """Corrige todos os arquivos com problemas"""
    systems = [
        'memory_simple.py',
        'rules_memory.py',
        'persistent_memory_system_system_system_system.py',
        'memory_optimizer.py',
        'memory_federation.py',
        'alchemical_transmutation_memory.py',
        'entropic_reverse_memory.py',
        'mimetic_evolutionary_memory.py',
        'holographic_fractal_memory.py',
        'dimensional_multiverse_memory.py',
        'hyperdimensional_computing_memory.py',
        'crystalline_lattice_memory.py',
        'memory_brain.py',
        'memory_graph_universe.py',
        'quantum_blockchain_memory_nexus.py',
        'telepathic_distributed_memory_supreme.py',
        'memory_harmony_orchestrator.py',
        'mac_silicon_memory_maximizer.py'
    ]

    print("🔧 CORRIGINDO INDENTAÇÃO EM TODOS OS SISTEMAS")
    print("=" * 60)

    success = 0
    failed = 0

    for system in systems:
        file_path = Path(system)
        if file_path.exists():
            if fix_file(file_path):
                success += 1
            else:
                failed += 1
        else:
            print(f"  {system}: ❌ Não encontrado")
            failed += 1

    print(f"\n✅ Sucesso: {success}")
    print(f"❌ Falhas: {failed}")

if __name__ == "__main__":
    main()