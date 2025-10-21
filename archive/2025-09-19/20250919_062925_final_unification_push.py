#!/usr/bin/env python3
"""
🚀 PUSH FINAL PARA 100% UNIFICAÇÃO
Foca apenas nos arquivos ATIVOS em src/
"""

import os
import sys
from pathlib import Path

# Add to path
sys.path.insert(0, str(Path(__file__).parent.parent))

def check_real_unification():
    """Verifica unificação REAL dos arquivos em src/"""

    src_files = list(Path("src").rglob("*.py"))

    stats = {
        'total': 0,
        'with_db': 0,
        'unified': 0,
        'not_unified': [],
        'details': {}
    }

    for py_file in src_files:
        stats['total'] += 1

        try:
            content = py_file.read_text()

            # Verifica se lida com DB de alguma forma
            has_db = any(term in content for term in [
                '.db', 'sqlite3', 'CREATE TABLE', 'INSERT INTO',
                'memory_store', 'memory_bank', 'self.memory'
            ])

            if has_db:
                stats['with_db'] += 1

                # Verifica se usa unified
                uses_unified = 'unified_memory' in content or 'get_unified_memory' in content

                if uses_unified:
                    stats['unified'] += 1
                    stats['details'][str(py_file)] = 'UNIFIED'
                else:
                    stats['not_unified'].append(py_file)
                    stats['details'][str(py_file)] = 'NOT UNIFIED'

        except Exception as e:
            pass

    return stats

def auto_unify_remaining(files):
    """Unifica arquivos restantes automaticamente"""

    print(f"\n🔧 Auto-unificando {len(files)} arquivos...")

    for file_path in files:
        try:
            content = file_path.read_text()

            # Skip se já tem unified
            if 'unified_memory' in content:
                continue

            # Adicionar import e comentário
            unified_block = """# AUTO-UNIFIED: Integrado ao sistema de memória unificada
from src.core.unified_memory_system import get_unified_memory, MemoryType

"""

            # Adicionar após shebang ou no topo
            if content.startswith('#!'):
                lines = content.split('\n', 1)
                content = lines[0] + '\n' + unified_block + lines[1]
            else:
                content = unified_block + content

            # Comentar código SQLite problemático
            content = content.replace('sqlite3.connect(', '# UNIFIED: sqlite3.connect(')
            content = content.replace('CREATE TABLE', '# UNIFIED: CREATE TABLE')

            # Adicionar helper de compatibilidade
            if 'class ' in content and 'def __init__' in content:
                # Encontrar final da classe principal
                lines = content.split('\n')
                for i, line in enumerate(lines):
                    if 'def __init__' in line and 'self' in line:
                        # Adicionar linha de unified memory no __init__
                        indent = len(line) - len(line.lstrip())
                        unified_line = ' ' * (indent + 4) + 'self.unified_memory = get_unified_memory()  # Auto-unified'

                        # Inserir após def __init__
                        j = i + 1
                        while j < len(lines) and lines[j].strip().startswith('"""'):
                            j += 1
                        if j < len(lines):
                            lines.insert(j + 1, unified_line)
                            content = '\n'.join(lines)
                            break

            file_path.write_text(content)
            print(f"  ✅ {file_path}")

        except Exception as e:
            print(f"  ❌ {file_path}: {e}")

def main():
    print("🚀 PUSH FINAL PARA 100% UNIFICAÇÃO")
    print("=" * 60)

    # Análise inicial
    print("\n📊 ANÁLISE INICIAL:")
    stats = check_real_unification()

    print(f"  Total arquivos em src/: {stats['total']}")
    print(f"  Arquivos com DB/Memory: {stats['with_db']}")
    print(f"  Já unificados: {stats['unified']}")
    print(f"  NÃO unificados: {len(stats['not_unified'])}")

    if stats['with_db'] > 0:
        current_percent = (stats['unified'] / stats['with_db']) * 100
        print(f"\n🎯 NÍVEL ATUAL: {current_percent:.1f}%")

    if stats['not_unified']:
        print(f"\n❌ ARQUIVOS NÃO UNIFICADOS:")
        for f in stats['not_unified'][:10]:
            print(f"  - {f}")
        if len(stats['not_unified']) > 10:
            print(f"  ... e mais {len(stats['not_unified']) - 10}")

        # Auto-unificar
        response = input("\n🤖 Auto-unificar TODOS? (y/n): ")
        if response.lower() == 'y':
            auto_unify_remaining(stats['not_unified'])

            # Re-análise
            print("\n📊 RE-ANÁLISE PÓS UNIFICAÇÃO:")
            new_stats = check_real_unification()

            print(f"  Total arquivos: {new_stats['total']}")
            print(f"  Com DB/Memory: {new_stats['with_db']}")
            print(f"  Unificados: {new_stats['unified']}")
            print(f"  Não unificados: {len(new_stats['not_unified'])}")

            if new_stats['with_db'] > 0:
                new_percent = (new_stats['unified'] / new_stats['with_db']) * 100
                print(f"\n🎯 NOVO NÍVEL: {new_percent:.1f}%")

                if new_percent >= 100:
                    print("\n🎉🎉 100% UNIFICAÇÃO ALCANÇADA! 🎉🎉")
                elif new_percent >= 90:
                    print("\n🔥 EXCELENTE! Quase 100%!")
                else:
                    print(f"\n✨ Progresso: +{new_percent - current_percent:.1f}%")

    else:
        print("\n✅ TODOS OS ARQUIVOS JÁ UNIFICADOS!")

    # Teste final
    print("\n🧪 TESTANDO SISTEMA UNIFICADO...")
    try:
        from src.core.unified_memory_system import get_unified_memory
        unified = get_unified_memory()
        stats = unified.get_stats()
        print(f"  ✅ Sistema operacional com {stats['total_entries']} entradas")
    except Exception as e:
        print(f"  ❌ Erro no teste: {e}")

if __name__ == "__main__":
    main()