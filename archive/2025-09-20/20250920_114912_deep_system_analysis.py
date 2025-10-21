#!/usr/bin/env python3
"""
🔬 ANÁLISE PROFUNDA COMPLETA DO SISTEMA
Verifica todos os aspectos críticos para funcionamento eficiente
"""

import os
import sys
import ast
from pathlib import Path
from collections import defaultdict
import traceback

def analyze_system():
    """Análise completa do sistema"""

    print('🔬 ANÁLISE PROFUNDA DO SISTEMA SCRIPTUREMON')
    print('=' * 80)

    issues = {
        'critical': [],
        'warnings': [],
        'optimizations': []
    }

    # 1. VERIFICAR ARQUIVOS ESSENCIAIS
    print('\n📁 1. VERIFICANDO ARQUIVOS ESSENCIAIS')
    print('-' * 40)

    essential_files = {
        'Mixtral Enhanced Master': 'scripts/active/mixtral_enhanced_master.py',
        'Mixtral Primary System': 'scripts/active/mixtral_primary_system.py',
        'Screenplay Library': 'src/core/screenplay_library.py',
        'Unified Memory': 'src/core/unified_memory_system.py',
        'Config': 'src/core/config.py',
        'Launcher': 'scripts/active/launch_mixtral_enhanced_automatic.py'
    }

    for name, path in essential_files.items():
        if Path(path).exists():
            try:
                with open(path, 'r') as f:
                    content = f.read()
                    ast.parse(content)  # Verificar sintaxe

                size_kb = len(content) / 1024

                # Verificações específicas
                if '70b' in content.lower():
                    issues['warnings'].append(f"{name}: Contém referências ao 70B")

                if 'TODO' in content or 'FIXME' in content:
                    issues['warnings'].append(f"{name}: Contém TODOs/FIXMEs")

                print(f'  ✅ {name}: {size_kb:.1f} KB')

            except SyntaxError as e:
                issues['critical'].append(f"{name}: Erro de sintaxe linha {e.lineno}")
                print(f'  ❌ {name}: Erro de sintaxe!')
        else:
            issues['critical'].append(f"{name}: Arquivo não encontrado")
            print(f'  ❌ {name}: NÃO ENCONTRADO!')

    # 2. VERIFICAR BIBLIOTECA
    print('\n📚 2. VERIFICANDO BIBLIOTECA DE ROTEIROS')
    print('-' * 40)

    library_path = Path('digilibrary/BIBLIOTECA_ROTEIROS')
    categories = ['roteiros_mestres', 'meus_filmes', 'teoria']
    total_files = 0

    for category in categories:
        cat_path = library_path / category
        if cat_path.exists():
            files = list(cat_path.glob('*.txt'))
            total_files += len(files)
            print(f'  ✅ {category}: {len(files)} arquivos')

            # Verificar arquivos vazios
            empty = [f for f in files if f.stat().st_size == 0]
            if empty:
                issues['warnings'].append(f"{category}: {len(empty)} arquivos vazios")
        else:
            issues['critical'].append(f"Biblioteca {category} não encontrada")
            print(f'  ❌ {category}: NÃO ENCONTRADO!')

    if total_files < 40:
        issues['warnings'].append(f"Apenas {total_files} arquivos na biblioteca (esperado 48+)")

    # 3. VERIFICAR MODELFILES
    print('\n🤖 3. VERIFICANDO MODELFILES')
    print('-' * 40)

    modelfiles_dir = Path('data/models/modelfiles')
    if modelfiles_dir.exists():
        mixtral_files = list(modelfiles_dir.glob('mixtral*.modelfile'))
        print(f'  ✅ Modelfiles Mixtral: {len(mixtral_files)}')

        for mf in mixtral_files:
            with open(mf, 'r') as f:
                content = f.read()
                if '128k' in content.lower() or '131072' in content:
                    print(f'    • {mf.name}: 128K context ✅')
                else:
                    print(f'    • {mf.name}: Context menor ⚠️')
    else:
        issues['critical'].append("Diretório modelfiles não encontrado")
        print('  ❌ Diretório modelfiles NÃO ENCONTRADO!')

    # 4. VERIFICAR MÉTODOS CRÍTICOS
    print('\n🔧 4. VERIFICANDO MÉTODOS CRÍTICOS')
    print('-' * 40)

    method_checks = {
        'src/core/screenplay_library.py': [
            'def list_screenplays',
            'def get_screenplay',
            'def search'
        ],
        'src/core/unified_memory_system.py': [
            'def store_knowledge',
            'def retrieve',
            'def store'
        ],
        'scripts/active/mixtral_enhanced_master.py': [
            'def analyze_with_masterpiece_comparison',
            'def analyze_theory_with_practice',
            'def run_complete_analysis'
        ]
    }

    for file_path, methods in method_checks.items():
        if Path(file_path).exists():
            with open(file_path, 'r') as f:
                content = f.read()

            missing = [m for m in methods if m not in content]

            if missing:
                issues['critical'].append(f"{Path(file_path).name}: Métodos faltando: {missing}")
                print(f'  ❌ {Path(file_path).name}: Faltando {len(missing)} métodos')
            else:
                print(f'  ✅ {Path(file_path).name}: Todos métodos OK')
        else:
            print(f'  ⚠️ {Path(file_path).name}: Arquivo não existe')

    # 5. VERIFICAR PERFORMANCE
    print('\n⚡ 5. VERIFICANDO PERFORMANCE')
    print('-' * 40)

    # Verificar padrões problemáticos
    performance_patterns = {
        'while True': 0,
        'sleep(': 0,
        'global ': 0,
        '.read()': 0  # Sem limit
    }

    for script in Path('scripts/active').glob('*.py'):
        try:
            with open(script, 'r') as f:
                content = f.read()

            for pattern in performance_patterns:
                count = content.count(pattern)
                performance_patterns[pattern] += count
        except:
            pass

    for pattern, count in performance_patterns.items():
        if count > 10:
            issues['optimizations'].append(f"Padrão '{pattern}' usado {count}x (possível problema)")
            print(f'  ⚠️ {pattern}: {count} ocorrências')
        elif count > 0:
            print(f'  • {pattern}: {count} ocorrências')

    # 6. VERIFICAR MEMÓRIA
    print('\n💾 6. VERIFICANDO SISTEMA DE MEMÓRIA')
    print('-' * 40)

    db_path = Path('data/unified_memory.db')
    if db_path.exists():
        size_mb = db_path.stat().st_size / (1024 * 1024)
        print(f'  ✅ unified_memory.db: {size_mb:.2f} MB')

        if size_mb > 100:
            issues['warnings'].append(f"Banco muito grande: {size_mb:.2f} MB")
    else:
        issues['critical'].append("unified_memory.db não encontrado")
        print('  ❌ unified_memory.db NÃO ENCONTRADO!')

    # Verificar outros bancos (legados)
    legacy_dbs = [db for db in Path('data').glob('*.db') if db.name != 'unified_memory.db']
    if legacy_dbs:
        issues['optimizations'].append(f"{len(legacy_dbs)} bancos legados encontrados")
        print(f'  ⚠️ {len(legacy_dbs)} bancos legados encontrados')

    # 7. VERIFICAR DEPENDÊNCIAS CIRCULARES
    print('\n🔄 7. VERIFICANDO DEPENDÊNCIAS')
    print('-' * 40)

    import_counts = defaultdict(int)

    for script in Path('scripts/active').glob('*.py'):
        try:
            with open(script, 'r') as f:
                for line in f:
                    if line.strip().startswith('from ') or line.strip().startswith('import '):
                        import_counts[script.name] += 1
        except:
            pass

    high_deps = [(f, c) for f, c in import_counts.items() if c > 15]

    if high_deps:
        for file, count in high_deps[:3]:
            issues['optimizations'].append(f"{file}: {count} imports (muito alto)")
            print(f'  ⚠️ {file}: {count} imports')
    else:
        print('  ✅ Dependências balanceadas')

    # RELATÓRIO FINAL
    print('\n' + '=' * 80)
    print('📊 RELATÓRIO FINAL')
    print('=' * 80)

    # Contar problemas
    total_critical = len(issues['critical'])
    total_warnings = len(issues['warnings'])
    total_optimizations = len(issues['optimizations'])
    total_issues = total_critical + total_warnings + total_optimizations

    # Mostrar problemas
    if total_critical > 0:
        print(f'\n❌ PROBLEMAS CRÍTICOS ({total_critical}):')
        for issue in issues['critical']:
            print(f'  • {issue}')

    if total_warnings > 0:
        print(f'\n⚠️ AVISOS ({total_warnings}):')
        for warning in issues['warnings'][:5]:
            print(f'  • {warning}')

    if total_optimizations > 0:
        print(f'\n💡 OTIMIZAÇÕES SUGERIDAS ({total_optimizations}):')
        for opt in issues['optimizations'][:5]:
            print(f'  • {opt}')

    # Recomendações
    print('\n🎯 AÇÕES RECOMENDADAS:')

    if total_critical > 0:
        print('  1. ❌ RESOLVER PROBLEMAS CRÍTICOS IMEDIATAMENTE')

    if 'referências ao 70B' in str(issues['warnings']):
        print('  2. Executar limpeza final de referências 70B')

    if legacy_dbs:
        print('  3. Remover bancos de dados legados em data/')

    if total_optimizations > 5:
        print('  4. Considerar refatoração de performance')

    if total_issues == 0:
        print('  ✅ NENHUMA AÇÃO NECESSÁRIA - SISTEMA PERFEITO!')

    # Status final
    print('\n🏁 STATUS FINAL:')

    if total_critical > 0:
        print('  ❌❌❌ SISTEMA COM PROBLEMAS CRÍTICOS')
        print('  Resolver antes de usar em produção!')
    elif total_warnings > 5:
        print('  ⚠️⚠️ SISTEMA FUNCIONAL COM AVISOS')
        print('  Recomenda-se otimização')
    elif total_issues > 0:
        print('  ✅⚠️ SISTEMA BOM')
        print('  Pequenas melhorias recomendadas')
    else:
        print('  ✅✅✅ SISTEMA PERFEITO!')
        print('  Pronto para produção máxima')

    print('\nDIGIMUNDO PRESENTE 🥷')

    return total_critical == 0  # Retorna True se não há críticos


if __name__ == "__main__":
    success = analyze_system()
    sys.exit(0 if success else 1)