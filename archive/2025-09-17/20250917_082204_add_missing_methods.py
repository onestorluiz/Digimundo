#!/usr/bin/env python3
"""
🔧 Adiciona métodos store_memory e retrieve_memory faltando
"""

import ast
from pathlib import Path
from typing import List, Tuple

def find_main_class(file_path: Path, class_name: str) -> Tuple[int, int]:
    """Encontra a linha de início e fim da classe principal"""
    with open(file_path, 'r') as f:
        lines = f.readlines()

    class_start = -1
    class_end = len(lines)
    in_class = False

    for i, line in enumerate(lines):
        if f'class {class_name}' in line:
            class_start = i
            in_class = True
        elif in_class and line and not line[0].isspace() and 'class ' in line:
            class_end = i
            break

    return class_start, class_end

def add_methods_to_class(file_path: Path, class_name: str) -> bool:
    """Adiciona métodos store_memory e retrieve_memory à classe"""
    print(f"  Processando {file_path.name} - classe {class_name}...", end="")

    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()

        # Encontra a classe
        class_start, class_end = find_main_class(file_path, class_name)

        if class_start == -1:
            print(f" ❌ Classe {class_name} não encontrada")
            return False

        # Verifica se já tem os métodos
        content = ''.join(lines[class_start:class_end])
        has_store = 'def store_memory(self' in content
        has_retrieve = 'def retrieve_memory(self' in content

        if has_store and has_retrieve:
            print(" ✅ Já tem ambos os métodos")
            return False

        # Encontra o último método da classe
        last_method_line = class_start
        for i in range(class_start + 1, class_end):
            if lines[i].strip().startswith('def '):
                last_method_line = i

        # Encontra o fim do último método
        insert_line = last_method_line + 1
        while insert_line < class_end:
            line = lines[insert_line]
            # Se encontrar uma linha sem indentação adequada ou novo método
            if line.strip() and len(line) - len(line.lstrip()) <= 4:
                break
            insert_line += 1

        # Prepara os métodos para adicionar
        methods = []

        if not has_store:
            methods.append("""
    def store_memory(self, key: str, value) -> None:
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
    def retrieve_memory(self, key: str):
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
        for method in methods:
            for method_line in method.split('\n'):
                lines.insert(insert_line, method_line + '\n')
                insert_line += 1

        # Salva o arquivo
        with open(file_path, 'w') as f:
            f.writelines(lines)

        # Verifica sintaxe
        with open(file_path, 'r') as f:
            content = f.read()
            ast.parse(content)

        print(" ✅ Adicionados")
        return True

    except SyntaxError as e:
        print(f" ❌ Erro de sintaxe na linha {e.lineno}")
        return False
    except Exception as e:
        print(f" ❌ {str(e)}")
        return False

def main():
    """Adiciona métodos aos sistemas que precisam"""
    systems = [
        ('memory_federation.py', 'MemoryFederation'),
        ('mimetic_evolutionary_memory.py', 'MimeticMemorySystem'),
        ('telepathic_distributed_memory_supreme.py', 'TelepathicMemorySupreme')
    ]

    print("🔧 ADICIONANDO MÉTODOS store_memory E retrieve_memory")
    print("=" * 60)

    success = 0
    failed = 0

    for file_name, class_name in systems:
        file_path = Path(file_name)
        if file_path.exists():
            if add_methods_to_class(file_path, class_name):
                success += 1
            else:
                failed += 1
        else:
            print(f"  {file_name}: ❌ Não encontrado")
            failed += 1

    print(f"\n✅ Sucesso: {success}")
    print(f"❌ Falhas: {failed}")

if __name__ == "__main__":
    main()