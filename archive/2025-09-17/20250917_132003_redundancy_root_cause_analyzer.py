#!/usr/bin/env python3
"""
🔍 REDUNDANCY ROOT CAUSE ANALYZER
==================================
Analisa as causas raiz da redundância e duplicação de arquivos
"""

import os
import ast
import hashlib
from pathlib import Path
from typing import Dict, List, Set, Tuple
from collections import defaultdict, Counter
import re
import json

class RedundancyAnalyzer:
    """Analisa causas profundas de redundância no código"""

    def __init__(self, root_path: str = "/Users/clubproducoes/Digimundo/scripturemon-champion"):
        self.root_path = Path(root_path)
        self.patterns = defaultdict(list)
        self.duplications = defaultdict(list)
        self.generation_sources = []

    def analyze_file_patterns(self):
        """Analisa padrões de nomenclatura de arquivos"""
        print("\n🔍 ANALISANDO PADRÕES DE NOMENCLATURA...")

        file_patterns = {
            'versioned': [],  # v1, v2, v3, etc
            'backup': [],     # .bak, _backup, etc
            'copy': [],       # _copy, _copy2, etc
            'test': [],       # test_, _test
            'temp': [],       # temp_, tmp_
            'old': [],        # old_, _old
            'new': [],        # new_, _new
            'fixed': [],      # _fixed, _fix
            'improved': [],   # _improved, _better
            'deployment': []  # in deployment folders
        }

        for py_file in self.root_path.rglob("*.py"):
            name = py_file.name.lower()
            path_str = str(py_file)

            # Versioned files
            if re.search(r'_v\d+', name) or re.search(r'v\d+_', name):
                file_patterns['versioned'].append(py_file)

            # Backup files
            if 'backup' in name or '.bak' in name:
                file_patterns['backup'].append(py_file)

            # Copy files
            if 'copy' in name or re.search(r'_\d+\.py$', name):
                file_patterns['copy'].append(py_file)

            # Test variations
            if 'test_' in name and 'tests/' not in path_str:
                file_patterns['test'].append(py_file)

            # Temporary files
            if 'temp' in name or 'tmp' in name:
                file_patterns['temp'].append(py_file)

            # Old versions
            if 'old' in name:
                file_patterns['old'].append(py_file)

            # New versions
            if 'new' in name:
                file_patterns['new'].append(py_file)

            # Fixed versions
            if 'fix' in name:
                file_patterns['fixed'].append(py_file)

            # Improved versions
            if 'improved' in name or 'better' in name or 'supreme' in name or 'ultimate' in name:
                file_patterns['improved'].append(py_file)

            # Deployment copies
            if 'deployment' in path_str:
                file_patterns['deployment'].append(py_file)

        return file_patterns

    def analyze_content_similarity(self):
        """Analisa similaridade de conteúdo entre arquivos"""
        print("\n🔍 ANALISANDO SIMILARIDADE DE CONTEÚDO...")

        content_hashes = defaultdict(list)
        function_signatures = defaultdict(list)

        for py_file in self.root_path.rglob("*.py"):
            if '.bak' in str(py_file):
                continue

            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Hash do conteúdo
                content_hash = hashlib.md5(content.encode()).hexdigest()
                content_hashes[content_hash].append(py_file)

                # Analisar AST para funções duplicadas
                try:
                    tree = ast.parse(content)
                    for node in ast.walk(tree):
                        if isinstance(node, ast.FunctionDef):
                            sig = f"{node.name}({len(node.args.args)})"
                            function_signatures[sig].append(py_file)
                except:
                    pass

            except Exception as e:
                pass

        # Filtrar apenas duplicados
        identical_files = {k: v for k, v in content_hashes.items() if len(v) > 1}
        duplicate_functions = {k: v for k, v in function_signatures.items() if len(v) > 5}

        return identical_files, duplicate_functions

    def analyze_generation_scripts(self):
        """Identifica scripts que geram outros arquivos"""
        print("\n🔍 ANALISANDO SCRIPTS GERADORES...")

        generators = []

        keywords = [
            'with open.*w',
            'shutil.copy',
            'copyfile',
            'dump.*json',
            'pickle.dump',
            'save.*file',
            'create.*file',
            'generate',
            'build',
            'deploy'
        ]

        for py_file in self.root_path.rglob("*.py"):
            if '.bak' in str(py_file):
                continue

            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                matches = []
                for keyword in keywords:
                    if re.search(keyword, content, re.IGNORECASE):
                        matches.append(keyword)

                if matches:
                    generators.append({
                        'file': py_file,
                        'patterns': matches,
                        'score': len(matches)
                    })

            except:
                pass

        # Ordenar por score
        generators.sort(key=lambda x: x['score'], reverse=True)

        return generators[:20]  # Top 20 geradores

    def analyze_import_cycles(self):
        """Analisa ciclos de importação que podem causar duplicação"""
        print("\n🔍 ANALISANDO CICLOS DE IMPORTAÇÃO...")

        import_graph = defaultdict(set)

        for py_file in self.root_path.rglob("*.py"):
            if '.bak' in str(py_file):
                continue

            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Extrair imports
                imports = re.findall(r'^(?:from|import)\s+([^\s]+)', content, re.MULTILINE)

                for imp in imports:
                    if not imp.startswith('.'):
                        import_graph[py_file.stem].add(imp.split('.')[0])

            except:
                pass

        # Detectar ciclos
        cycles = []
        for module, imports in import_graph.items():
            for imported in imports:
                if imported in import_graph and module in import_graph[imported]:
                    cycle = sorted([module, imported])
                    if cycle not in cycles:
                        cycles.append(cycle)

        return cycles

    def analyze_deployment_structure(self):
        """Analisa estrutura de deployments"""
        print("\n🔍 ANALISANDO ESTRUTURA DE DEPLOYMENTS...")

        deployment_info = {}

        deployment_dir = self.root_path / "deployments"
        if deployment_dir.exists():
            for deploy in deployment_dir.iterdir():
                if deploy.is_dir():
                    py_files = list(deploy.rglob("*.py"))
                    deployment_info[deploy.name] = {
                        'total_files': len(py_files),
                        'size': sum(f.stat().st_size for f in py_files),
                        'subdirs': len(list(deploy.glob("*/")))
                    }

        return deployment_info

    def generate_report(self):
        """Gera relatório completo de análise"""
        print("\n" + "="*60)
        print("📊 ANÁLISE DE REDUNDÂNCIA - CAUSAS RAIZ")
        print("="*60)

        # 1. Padrões de nomenclatura
        patterns = self.analyze_file_patterns()

        print("\n📁 PADRÕES DE ARQUIVOS PROBLEMÁTICOS:")
        for pattern_type, files in patterns.items():
            if files:
                print(f"\n  {pattern_type.upper()}: {len(files)} arquivos")
                for f in files[:3]:  # Mostrar até 3 exemplos
                    print(f"    - {f.relative_to(self.root_path)}")

        # 2. Arquivos idênticos
        identical, dup_functions = self.analyze_content_similarity()

        print("\n🔄 DUPLICAÇÃO DE CONTEÚDO:")
        print(f"  - Arquivos idênticos: {sum(len(v)-1 for v in identical.values())}")
        print(f"  - Funções muito duplicadas: {len(dup_functions)}")

        if dup_functions:
            print("\n  Funções mais duplicadas:")
            for func, files in list(dup_functions.items())[:5]:
                print(f"    - {func}: em {len(files)} arquivos")

        # 3. Scripts geradores
        generators = self.analyze_generation_scripts()

        print("\n🏭 PRINCIPAIS SCRIPTS GERADORES:")
        for gen in generators[:5]:
            print(f"  - {gen['file'].name} (score: {gen['score']})")
            print(f"    Padrões: {', '.join(gen['patterns'][:3])}")

        # 4. Ciclos de importação
        cycles = self.analyze_import_cycles()

        if cycles:
            print(f"\n🔄 CICLOS DE IMPORTAÇÃO: {len(cycles)}")
            for cycle in cycles[:5]:
                print(f"  - {cycle[0]} <-> {cycle[1]}")

        # 5. Estrutura de deployments
        deploy_info = self.analyze_deployment_structure()

        print("\n📦 ESTRUTURA DE DEPLOYMENTS:")
        for name, info in deploy_info.items():
            print(f"  - {name}: {info['total_files']} arquivos, {info['size']/1024/1024:.1f}MB")

        # ANÁLISE FINAL
        print("\n" + "="*60)
        print("🎯 CAUSAS RAIZ IDENTIFICADAS:")
        print("="*60)

        root_causes = []

        # Causa 1: Versionamento manual
        if len(patterns['versioned']) > 10:
            root_causes.append({
                'cause': 'Versionamento Manual Excessivo',
                'description': f"Encontrados {len(patterns['versioned'])} arquivos versionados (_v1, _v2, etc)",
                'impact': 'Alto',
                'solution': 'Usar Git para versionamento, remover versões antigas'
            })

        # Causa 2: Scripts de tradução/processamento duplicados
        translate_scripts = [f for f in patterns['versioned'] if 'translate' in f.name]
        if len(translate_scripts) > 5:
            root_causes.append({
                'cause': 'Múltiplas Versões de Scripts de Tradução',
                'description': f"Encontrados {len(translate_scripts)} scripts de tradução diferentes",
                'impact': 'Alto',
                'solution': 'Unificar em um único script parametrizável'
            })

        # Causa 3: Deployments duplicando código
        if deploy_info and any(info['total_files'] > 100 for info in deploy_info.values()):
            root_causes.append({
                'cause': 'Deployments Contendo Código Duplicado',
                'description': 'Pastas de deployment contêm cópias completas do código',
                'impact': 'Muito Alto',
                'solution': 'Usar links simbólicos ou referências ao invés de cópias'
            })

        # Causa 4: Arquivos "improved", "better", "supreme"
        if len(patterns['improved']) > 5:
            root_causes.append({
                'cause': 'Iterações de Melhoria Acumuladas',
                'description': f"Encontrados {len(patterns['improved'])} arquivos com sufixos de melhoria",
                'impact': 'Médio',
                'solution': 'Manter apenas a versão mais recente e funcional'
            })

        # Causa 5: Scripts geradores sem controle
        if len(generators) > 10:
            root_causes.append({
                'cause': 'Múltiplos Scripts Geradores',
                'description': f"Encontrados {len(generators)} scripts que geram outros arquivos",
                'impact': 'Alto',
                'solution': 'Centralizar geração de código em um único sistema'
            })

        print("\n🔴 PROBLEMAS PRINCIPAIS:\n")
        for i, cause in enumerate(root_causes, 1):
            print(f"{i}. {cause['cause']}")
            print(f"   📝 {cause['description']}")
            print(f"   ⚠️ Impacto: {cause['impact']}")
            print(f"   ✅ Solução: {cause['solution']}\n")

        # Salvar relatório completo
        report_data = {
            'patterns': {k: len(v) for k, v in patterns.items()},
            'identical_files': len(identical),
            'duplicate_functions': len(dup_functions),
            'generators': len(generators),
            'import_cycles': len(cycles),
            'deployments': deploy_info,
            'root_causes': root_causes
        }

        report_path = self.root_path / "REDUNDANCY_ROOT_CAUSE_REPORT.json"
        with open(report_path, 'w') as f:
            json.dump(report_data, f, indent=2, default=str)

        print(f"\n📄 Relatório completo salvo em: {report_path}")

        return root_causes


def main():
    analyzer = RedundancyAnalyzer()
    root_causes = analyzer.generate_report()

    print("\n" + "="*60)
    print("💡 AÇÕES RECOMENDADAS:")
    print("="*60)
    print("""
1. **Limpar Versionamento Manual**
   - Manter apenas versão mais recente de cada script
   - Usar Git tags para marcar versões importantes

2. **Unificar Scripts de Processamento**
   - Criar um único sistema de tradução/processamento configurável
   - Remover todas as variações (_v1, _v2, _supreme, etc)

3. **Reestruturar Deployments**
   - Usar Docker ou containers ao invés de copiar código
   - Implementar CI/CD pipeline adequado

4. **Implementar Política de Código**
   - Proibir sufixos como _improved, _better, _fixed
   - Code reviews antes de criar novos arquivos

5. **Centralizar Geração de Código**
   - Um único ponto de geração de arquivos
   - Logs de quais arquivos foram gerados e por quê
    """)


if __name__ == "__main__":
    main()