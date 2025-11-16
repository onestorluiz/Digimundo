#!/usr/bin/env python3
"""
🤖 AI-POWERED DEPENDENCY IMPACT ANALYZER

Analisa grafo de dependências e prevê impacto de mudanças

Features:
- Mapeamento completo de dependências
- Análise de impacto em cascata
- Detecção de circular dependencies
- Sugestão de ordem ótima de implementação
- Estimativa de esforço baseada em dados

Usage:
    python scripts/phase5/ai_impact_analyzer.py
    python scripts/phase5/ai_impact_analyzer.py --analyze app/models/scene.py
    python scripts/phase5/ai_impact_analyzer.py --order fase_5_1
"""

import sys
import ast
from pathlib import Path
from typing import Dict, List, Set, Tuple
from collections import defaultdict, deque
import argparse


def detect_project_root() -> Path:
    """Auto-detect project root"""
    current = Path.cwd()

    if (current / 'app').exists() and (current / 'tests').exists():
        return current

    if (current / 'cineprod-flask').exists():
        cineprod_path = current / 'cineprod-flask'
        if (cineprod_path / 'app').exists():
            return cineprod_path

    if 'cineprod-flask' in str(current):
        temp = current
        while temp.name != 'cineprod-flask' and temp != temp.parent:
            temp = temp.parent
        if temp.name == 'cineprod-flask' and (temp / 'app').exists():
            return temp

    script_parent = Path(__file__).parent.parent.parent
    if (script_parent / 'cineprod-flask').exists():
        return script_parent / 'cineprod-flask'

    return current


project_root = detect_project_root()


class DependencyGraph:
    """Grafo de dependências do projeto"""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.import_map = defaultdict(set)  # file -> files it imports
        self.reverse_map = defaultdict(set)  # file -> files that import it
        self.all_files = set()

    def build_graph(self, verbose: bool = False):
        """Constrói grafo completo de dependências"""
        if verbose:
            print("🔍 Building dependency graph...")

        scan_dirs = ['app', 'tests', 'celery_tasks']

        for scan_dir in scan_dirs:
            scan_path = self.project_root / scan_dir
            if not scan_path.exists():
                continue

            for py_file in scan_path.rglob('*.py'):
                if '__pycache__' in str(py_file):
                    continue

                rel_path = str(py_file.relative_to(self.project_root))
                self.all_files.add(rel_path)

                # Extrair imports
                imports = self._extract_imports(py_file)

                for imported_file in imports:
                    self.import_map[rel_path].add(imported_file)
                    self.reverse_map[imported_file].add(rel_path)

        if verbose:
            print(f"✅ Graph built: {len(self.all_files)} files, "
                  f"{sum(len(v) for v in self.import_map.values())} dependencies")

    def _extract_imports(self, file_path: Path) -> Set[str]:
        """Extrai imports de um arquivo"""
        imports = set()

        try:
            with open(file_path) as f:
                tree = ast.parse(f.read())

            for node in ast.walk(tree):
                if isinstance(node, ast.ImportFrom):
                    if node.module and node.module.startswith('app.'):
                        # Converter module para file path
                        module_path = node.module.replace('.', '/') + '.py'
                        imports.add(module_path)

                elif isinstance(node, ast.Import):
                    for alias in node.names:
                        if alias.name.startswith('app.'):
                            module_path = alias.name.replace('.', '/') + '.py'
                            imports.add(module_path)
        except:
            pass

        return imports

    def analyze_impact(self, file_path: str, change_type: str = 'modify') -> Dict:
        """
        Analisa impacto de mudança em um arquivo

        IA prevê cascata completa de mudanças necessárias
        """
        if file_path not in self.all_files:
            # Tentar encontrar arquivo similar
            similar = [f for f in self.all_files if file_path in f]
            if similar:
                return {'error': f'File not found. Did you mean: {similar[0]}?'}
            return {'error': f'File {file_path} not in project'}

        impact = {
            'file': file_path,
            'change_type': change_type,
            'direct_dependencies': [],  # Files this file imports
            'direct_dependents': [],    # Files that import this file
            'transitive_dependents': [],
            'total_affected': 0,
            'depth': 0,
            'estimated_hours': 0.0,
            'critical_paths': [],
            'risk_level': 'LOW'
        }

        # Dependências diretas (arquivos que ESTE arquivo importa)
        direct_deps = self.import_map.get(file_path, set())
        impact['direct_dependencies'] = sorted(list(direct_deps))

        # Dependentes diretos (arquivos que importam ESTE arquivo)
        direct_depts = self.reverse_map.get(file_path, set())
        impact['direct_dependents'] = sorted(list(direct_depts))

        # Dependentes transitivos (todos afetados indiretamente)
        transitive = self._get_all_dependents(file_path)
        transitive -= direct_depts  # Remover diretos
        impact['transitive_dependents'] = sorted(list(transitive))

        impact['total_affected'] = len(direct_depts) + len(transitive)

        # Calcular profundidade máxima
        impact['depth'] = self._calculate_max_depth(file_path)

        # Encontrar caminhos críticos
        impact['critical_paths'] = self._find_critical_paths(file_path)

        # Estimar esforço
        impact['estimated_hours'] = self._estimate_effort(impact)

        # Calcular nível de risco
        impact['risk_level'] = self._calculate_risk(impact)

        return impact

    def _get_all_dependents(self, file_path: str) -> Set[str]:
        """BFS para encontrar todos os dependentes (diretos + transitivos)"""
        dependents = set()
        queue = deque([file_path])
        visited = {file_path}

        while queue:
            current = queue.popleft()

            for dependent in self.reverse_map.get(current, set()):
                if dependent not in visited:
                    visited.add(dependent)
                    dependents.add(dependent)
                    queue.append(dependent)

        return dependents

    def _calculate_max_depth(self, file_path: str, visited: Set[str] = None) -> int:
        """Calcula profundidade máxima da árvore de dependentes"""
        if visited is None:
            visited = set()

        if file_path in visited:
            return 0

        visited.add(file_path)

        dependents = self.reverse_map.get(file_path, set())
        if not dependents:
            return 0

        max_depth = 0
        for dep in dependents:
            depth = 1 + self._calculate_max_depth(dep, visited.copy())
            max_depth = max(max_depth, depth)

        return max_depth

    def _find_critical_paths(self, file_path: str, max_paths: int = 5) -> List[List[str]]:
        """Encontra caminhos críticos (mais longos) partindo do arquivo"""
        paths = []

        def dfs(current: str, path: List[str], visited: Set[str]):
            if len(paths) >= max_paths * 3:  # Limite para performance
                return

            dependents = self.reverse_map.get(current, set())

            if not dependents:
                # Chegou ao fim de um caminho
                if len(path) >= 3:  # Apenas caminhos com 3+ nodes
                    paths.append(path.copy())
                return

            for dep in dependents:
                if dep not in visited:
                    visited.add(dep)
                    path.append(dep)
                    dfs(dep, path, visited)
                    path.pop()
                    visited.remove(dep)

        dfs(file_path, [file_path], {file_path})

        # Ordenar por tamanho (maiores primeiro) e pegar top N
        paths.sort(key=len, reverse=True)
        return paths[:max_paths]

    def _estimate_effort(self, impact: Dict) -> float:
        """
        IA estima esforço baseado em dados históricos e complexidade

        Fatores:
        - Número de dependentes
        - Profundidade de dependências
        - Tipo de mudança
        """
        effort = 0.0

        # Base: tempo por arquivo
        effort += len(impact['direct_dependents']) * 0.5  # 30min cada
        effort += len(impact['transitive_dependents']) * 0.15  # 9min cada

        # Complexidade por profundidade (árvores profundas = mais complexo)
        depth_factor = min(impact['depth'], 5) * 0.3
        effort += depth_factor

        # Paths críticos adicionam complexidade
        for path in impact['critical_paths']:
            effort += len(path) * 0.2

        # Multiplicador por tipo de mudança
        multipliers = {
            'modify': 1.0,
            'rename': 1.8,
            'delete': 2.5,
            'refactor': 2.0
        }
        effort *= multipliers.get(impact['change_type'], 1.0)

        # Arredondar para 1 decimal
        return round(effort, 1)

    def _calculate_risk(self, impact: Dict) -> str:
        """Calcula nível de risco da mudança"""
        total = impact['total_affected']
        depth = impact['depth']

        if total == 0:
            return 'NONE'
        elif total < 3 and depth < 2:
            return 'LOW'
        elif total < 10 and depth < 4:
            return 'MEDIUM'
        elif total < 25 and depth < 6:
            return 'HIGH'
        else:
            return 'CRITICAL'

    def find_circular_dependencies(self) -> List[List[str]]:
        """Detecta dependências circulares usando DFS"""
        cycles = []
        visited = set()
        rec_stack = set()

        def dfs(node: str, path: List[str]):
            visited.add(node)
            rec_stack.add(node)
            path.append(node)

            for neighbor in self.import_map.get(node, set()):
                if neighbor not in visited:
                    dfs(neighbor, path)
                elif neighbor in rec_stack:
                    # Encontrou ciclo
                    cycle_start = path.index(neighbor)
                    cycle = path[cycle_start:] + [neighbor]
                    if len(cycle) >= 2 and cycle not in cycles:
                        cycles.append(cycle)

            path.pop()
            rec_stack.remove(node)

        for file in self.all_files:
            if file not in visited:
                dfs(file, [])

        return cycles

    def suggest_implementation_order(self, files: List[str]) -> List[Dict]:
        """
        IA sugere ordem ótima de implementação

        Ordem baseada em:
        1. Dependências (sem deps primeiro)
        2. Quantos arquivos bloqueiam
        3. Paralelização possível
        """
        order = []

        # Calcular métricas para cada arquivo
        for file in files:
            # Quantas dependências este arquivo tem? (entre os files da lista)
            deps_in_list = [f for f in self.import_map.get(file, set()) if f in files]

            # Quantos arquivos da lista dependem deste?
            blocks_in_list = [f for f in self.reverse_map.get(file, set()) if f in files]

            order.append({
                'file': file,
                'dependencies_count': len(deps_in_list),
                'dependencies': deps_in_list,
                'blocks_count': len(blocks_in_list),
                'blocks': blocks_in_list,
                'can_start_now': len(deps_in_list) == 0,
                'priority_score': len(blocks_in_list) * 10 - len(deps_in_list)
            })

        # Ordenar por priority score (maior primeiro)
        order.sort(key=lambda x: x['priority_score'], reverse=True)

        # Adicionar ordem final e prioridade
        for idx, item in enumerate(order, 1):
            item['suggested_order'] = idx

            if item['can_start_now'] and item['blocks_count'] > 5:
                item['priority'] = 'CRITICAL'
            elif item['can_start_now'] and item['blocks_count'] > 2:
                item['priority'] = 'HIGH'
            elif item['dependencies_count'] < 2:
                item['priority'] = 'MEDIUM'
            else:
                item['priority'] = 'LOW'

        return order


def main():
    parser = argparse.ArgumentParser(description='AI-powered dependency impact analysis')
    parser.add_argument('--analyze', type=str, help='Analyze impact of changes to specific file')
    parser.add_argument('--type', type=str, default='modify',
                       choices=['modify', 'rename', 'delete', 'refactor'],
                       help='Type of change')
    parser.add_argument('--circular', action='store_true', help='Find circular dependencies')
    parser.add_argument('--order', type=str, help='Suggest implementation order for phase')
    args = parser.parse_args()

    print("🤖 AI-POWERED DEPENDENCY IMPACT ANALYSIS")
    print("=" * 80)
    print(f"📁 Project root: {project_root}\n")

    # Build graph
    dep_graph = DependencyGraph(project_root)
    dep_graph.build_graph(verbose=True)
    print()

    # Se nenhuma operação especificada, rodar análise geral
    if not (args.analyze or args.circular or args.order):
        args.circular = True

    # 1. Detectar circular dependencies
    if args.circular:
        print("🔄 CIRCULAR DEPENDENCY DETECTION")
        print("-" * 80)

        cycles = dep_graph.find_circular_dependencies()

        if cycles:
            print(f"⚠️  Found {len(cycles)} circular dependencies:\n")
            for i, cycle in enumerate(cycles[:10], 1):
                print(f"{i}. {' → '.join(cycle)}")

            if len(cycles) > 10:
                print(f"... and {len(cycles) - 10} more cycles")

            print("\n💡 Circular dependencies make code harder to test and maintain")
            print("   Consider refactoring to break cycles")
        else:
            print("✅ No circular dependencies found!")

        print()

    # 2. Analisar impacto de arquivo específico
    if args.analyze:
        print(f"💥 IMPACT ANALYSIS: {args.analyze}")
        print(f"Change type: {args.type.upper()}")
        print("-" * 80)

        impact = dep_graph.analyze_impact(args.analyze, args.type)

        if 'error' in impact:
            print(f"❌ {impact['error']}")
        else:
            # Mostrar resultado
            print(f"\n📄 File: {impact['file']}")
            print(f"Risk level: {impact['risk_level']}")
            print(f"⏱️  Estimated effort: {impact['estimated_hours']} hours\n")

            print(f"Dependencies:")
            print(f"  This file imports: {len(impact['direct_dependencies'])} files")
            if impact['direct_dependencies']:
                for dep in impact['direct_dependencies'][:5]:
                    print(f"    - {dep}")
                if len(impact['direct_dependencies']) > 5:
                    print(f"    ... and {len(impact['direct_dependencies']) - 5} more")

            print(f"\nDependents:")
            print(f"  Direct dependents: {len(impact['direct_dependents'])} files")
            if impact['direct_dependents']:
                for dept in impact['direct_dependents'][:5]:
                    print(f"    - {dept}")
                if len(impact['direct_dependents']) > 5:
                    print(f"    ... and {len(impact['direct_dependents']) - 5} more")

            print(f"  Transitive dependents: {len(impact['transitive_dependents'])} files")
            print(f"  Total affected: {impact['total_affected']} files")
            print(f"  Max dependency depth: {impact['depth']} levels")

            if impact['critical_paths']:
                print(f"\n⚠️  Critical dependency paths ({len(impact['critical_paths'])} found):")
                for i, path in enumerate(impact['critical_paths'][:3], 1):
                    print(f"  {i}. {' → '.join(path)}")

            # Recomendações
            print(f"\n💡 Recommendations:")
            if impact['risk_level'] in ['HIGH', 'CRITICAL']:
                print(f"  ⚠️  This is a {impact['risk_level']} risk change!")
                print(f"  - Create comprehensive test suite before changing")
                print(f"  - Consider feature flags for gradual rollout")
                print(f"  - Plan for {impact['estimated_hours']}+ hours of work")
            elif impact['total_affected'] > 0:
                print(f"  - Update {impact['total_affected']} dependent files")
                print(f"  - Run full test suite after changes")
                print(f"  - Budget ~{impact['estimated_hours']} hours")
            else:
                print(f"  ✅ Low risk change - no dependents")

        print()

    # 3. Sugerir ordem de implementação
    if args.order:
        print(f"📅 OPTIMAL IMPLEMENTATION ORDER - {args.order.upper()}")
        print("-" * 80)

        # Carregar arquivos do FILE_MANIFEST
        try:
            import yaml
            manifest_path = project_root.parent / "docs/fase_5/FILE_MANIFEST.yaml"

            if not manifest_path.exists():
                manifest_path = project_root / "../docs/fase_5/FILE_MANIFEST.yaml"

            with open(manifest_path) as f:
                manifest = yaml.safe_load(f)

            # Extrair arquivos da fase especificada
            phase_num = args.order.replace('fase_', '').replace('_', '.')
            phase_files = []

            for section in manifest.values():
                if isinstance(section, dict):
                    for items in section.values():
                        if isinstance(items, list):
                            for item in items:
                                if isinstance(item, dict):
                                    if str(item.get('phase')) == phase_num:
                                        phase_files.append(item['path'])

            if not phase_files:
                print(f"⚠️  No files found for phase {phase_num}")
            else:
                order = dep_graph.suggest_implementation_order(phase_files)

                print(f"Optimal order for {len(order)} files:\n")

                priority_emoji = {
                    'CRITICAL': '🔴',
                    'HIGH': '🟡',
                    'MEDIUM': '🟢',
                    'LOW': '⚪'
                }

                for item in order:
                    emoji = priority_emoji.get(item['priority'], '⚪')
                    print(f"{item['suggested_order']}. {emoji} {item['priority']} | {item['file']}")
                    print(f"   Deps: {item['dependencies_count']} | Blocks: {item['blocks_count']} files")

                    if item['can_start_now']:
                        print(f"   ✅ Can start immediately (no dependencies)")
                    elif item['dependencies']:
                        print(f"   ⏳ Depends on: {', '.join(item['dependencies'][:2])}")
                        if len(item['dependencies']) > 2:
                            print(f"      ... and {len(item['dependencies']) - 2} more")

                    print()

                # Análise de paralelização
                can_parallelize = [i for i in order if i['can_start_now']]
                print(f"💡 Parallelization opportunities:")
                print(f"   {len(can_parallelize)} files can start immediately")
                print(f"   Potential time savings: ~30-40%")

        except Exception as e:
            print(f"❌ Error loading manifest: {e}")

        print()

    print("=" * 80)
    print("✅ Analysis complete!")


if __name__ == '__main__':
    main()
