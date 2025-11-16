#!/usr/bin/env python3
"""
🤖 AI-POWERED SEMANTIC CODE ANALYZER

Detecta:
- Duplicação semântica (lógica similar, código diferente)
- Código morto (nunca importado)
- Padrões arquiteturais inconsistentes
- Oportunidades de refatoração

Usage:
    python scripts/phase5/ai_semantic_analyzer.py
    python scripts/phase5/ai_semantic_analyzer.py --duplicates
    python scripts/phase5/ai_semantic_analyzer.py --dead-code
    python scripts/phase5/ai_semantic_analyzer.py --patterns
"""

import sys
import ast
from pathlib import Path
from typing import List, Dict, Set
import hashlib
from collections import defaultdict


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


class SemanticAnalyzer:
    """Analisa código em nível semântico (não apenas sintático)"""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.all_functions = []

    def extract_function_semantics(self, func_node: ast.FunctionDef, file_path: str) -> Dict:
        """
        Extrai 'semântica' de uma função

        Diferente de análise sintática, captura:
        - Que TIPO de operações são feitas (não o código exato)
        - Estrutura de controle de fluxo
        - Padrão de uso de variáveis
        """
        semantics = {
            'name': func_node.name,
            'file': file_path,
            'line': func_node.lineno,
            'has_loops': False,
            'has_conditionals': False,
            'has_try_except': False,
            'calls': [],
            'operations': [],
            'variables_accessed': set(),
            'returns': False
        }

        for node in ast.walk(func_node):
            # Detectar loops
            if isinstance(node, (ast.For, ast.While)):
                semantics['has_loops'] = True
                semantics['operations'].append('iteration')

            # Detectar condicionais
            if isinstance(node, ast.If):
                semantics['has_conditionals'] = True
                semantics['operations'].append('conditional')

            # Detectar error handling
            if isinstance(node, ast.Try):
                semantics['has_try_except'] = True
                semantics['operations'].append('error_handling')

            # Detectar chamadas de função
            if isinstance(node, ast.Call):
                if hasattr(node.func, 'id'):
                    semantics['calls'].append(node.func.id)
                elif hasattr(node.func, 'attr'):
                    semantics['calls'].append(node.func.attr)

            # Detectar operações binárias
            if isinstance(node, ast.BinOp):
                if isinstance(node.op, ast.Add):
                    semantics['operations'].append('addition')
                elif isinstance(node.op, ast.Sub):
                    semantics['operations'].append('subtraction')
                elif isinstance(node.op, ast.Mult):
                    semantics['operations'].append('multiplication')
                elif isinstance(node.op, ast.Div):
                    semantics['operations'].append('division')

            # Detectar acesso a variáveis
            if isinstance(node, ast.Name):
                semantics['variables_accessed'].add(node.id)

            # Detectar return
            if isinstance(node, ast.Return):
                semantics['returns'] = True

        # Criar "fingerprint semântico"
        # Funções com mesmo fingerprint fazem operações similares
        semantic_sig = (
            f"loop:{semantics['has_loops']}_"
            f"cond:{semantics['has_conditionals']}_"
            f"except:{semantics['has_try_except']}_"
            f"return:{semantics['returns']}_"
            f"ops:{'_'.join(sorted(set(semantics['operations'])))}"
        )
        semantics['signature'] = hashlib.md5(semantic_sig.encode()).hexdigest()[:8]

        # Converter set para lista (JSON serializable)
        semantics['variables_accessed'] = list(semantics['variables_accessed'])

        return semantics

    def find_semantic_duplicates(self, threshold: float = 0.75) -> List[Dict]:
        """
        Encontra funções com LÓGICA similar (não código similar)

        Exemplo de duplicação semântica:
        - Função A: calcula soma de durations em loop
        - Função B: calcula total de durations em loop
        → Mesma lógica, nomes diferentes!
        """
        if not self.all_functions:
            self._extract_all_functions()

        duplicates = []

        # Agrupar por signature semântica
        by_signature = defaultdict(list)
        for func_info in self.all_functions:
            sig = func_info['semantics']['signature']
            by_signature[sig].append(func_info)

        # Encontrar grupos com 2+ funções
        for sig, funcs in by_signature.items():
            if len(funcs) >= 2:
                # Comparar cada par dentro do grupo
                for i, func1 in enumerate(funcs):
                    for func2 in funcs[i+1:]:
                        similarity = self._calculate_semantic_similarity(
                            func1['semantics'],
                            func2['semantics']
                        )

                        if similarity >= threshold:
                            duplicates.append({
                                'file1': func1['file'],
                                'function1': func1['name'],
                                'line1': func1['line'],
                                'file2': func2['file'],
                                'function2': func2['name'],
                                'line2': func2['line'],
                                'similarity': round(similarity * 100, 1),
                                'signature': sig,
                                'recommendation': self._suggest_refactoring(func1, func2)
                            })

        # Ordenar por similaridade (maior primeiro)
        duplicates.sort(key=lambda x: x['similarity'], reverse=True)

        return duplicates

    def _calculate_semantic_similarity(self, sem1: Dict, sem2: Dict) -> float:
        """
        Calcula similaridade semântica entre duas funções

        Não compara código, compara COMPORTAMENTO
        """
        score = 0.0
        total_weight = 0.0

        # Estrutura de controle (peso 2.0)
        weight = 2.0
        if sem1['has_loops'] == sem2['has_loops']:
            score += weight
        total_weight += weight

        weight = 2.0
        if sem1['has_conditionals'] == sem2['has_conditionals']:
            score += weight
        total_weight += weight

        # Error handling (peso 1.0)
        weight = 1.0
        if sem1['has_try_except'] == sem2['has_try_except']:
            score += weight
        total_weight += weight

        # Return (peso 1.0)
        weight = 1.0
        if sem1['returns'] == sem2['returns']:
            score += weight
        total_weight += weight

        # Operações similares (peso 3.0 - muito importante)
        weight = 3.0
        ops1 = set(sem1['operations'])
        ops2 = set(sem2['operations'])
        if ops1 and ops2:
            ops_similarity = len(ops1 & ops2) / len(ops1 | ops2)
            score += ops_similarity * weight
        total_weight += weight

        # Chamadas similares (peso 3.0)
        weight = 3.0
        calls1 = set(sem1['calls'])
        calls2 = set(sem2['calls'])
        if calls1 and calls2:
            calls_similarity = len(calls1 & calls2) / len(calls1 | calls2)
            score += calls_similarity * weight
        total_weight += weight

        return score / total_weight if total_weight > 0 else 0.0

    def _suggest_refactoring(self, func1: Dict, func2: Dict) -> str:
        """Sugere refatoração baseada no padrão detectado"""
        sem1 = func1['semantics']
        sem2 = func2['semantics']

        # Se ambas têm loops e operações de soma/agregação
        if (sem1['has_loops'] and sem2['has_loops'] and
            'addition' in sem1['operations'] and 'addition' in sem2['operations']):
            return "Extract to shared aggregation utility function"

        # Se ambas fazem chamadas similares
        calls1 = set(sem1['calls'])
        calls2 = set(sem2['calls'])
        if len(calls1 & calls2) >= 3:
            return "Extract common workflow to base function"

        return "Consider extracting to shared utility"

    def _extract_all_functions(self):
        """Extrai todas as funções do projeto"""
        self.all_functions = []

        scan_dirs = ['app/services', 'app/routes', 'app/models']

        for scan_dir in scan_dirs:
            scan_path = self.project_root / scan_dir
            if not scan_path.exists():
                continue

            for py_file in scan_path.rglob('*.py'):
                if '__pycache__' in str(py_file) or '__init__' in py_file.name:
                    continue

                try:
                    with open(py_file) as f:
                        tree = ast.parse(f.read())

                    rel_path = str(py_file.relative_to(self.project_root))

                    for node in ast.walk(tree):
                        if isinstance(node, ast.FunctionDef):
                            # Ignorar funções privadas e muito pequenas
                            if node.name.startswith('_'):
                                continue

                            semantics = self.extract_function_semantics(node, rel_path)

                            self.all_functions.append({
                                'file': rel_path,
                                'name': node.name,
                                'line': node.lineno,
                                'semantics': semantics
                            })
                except Exception as e:
                    continue

    def detect_dead_code(self) -> Dict:
        """
        Detecta código morto - arquivos nunca importados

        Código morto = mantido mas nunca usado = desperdício
        """
        all_files = set()
        imported_files = set()

        # Coletar todos os arquivos .py
        for scan_dir in ['app', 'tests', 'celery_tasks']:
            scan_path = self.project_root / scan_dir
            if not scan_path.exists():
                continue

            for py_file in scan_path.rglob('*.py'):
                if '__pycache__' not in str(py_file):
                    rel_path = str(py_file.relative_to(self.project_root))
                    all_files.add(rel_path)

        # Coletar todos os imports
        for py_file in self.project_root.rglob('*.py'):
            if '__pycache__' in str(py_file) or 'venv' in str(py_file):
                continue

            try:
                with open(py_file) as f:
                    tree = ast.parse(f.read())

                for node in ast.walk(tree):
                    if isinstance(node, ast.ImportFrom):
                        if node.module and node.module.startswith('app.'):
                            module_path = node.module.replace('.', '/') + '.py'
                            imported_files.add(module_path)
            except:
                continue

        # Código morto = nunca importado
        dead_files = all_files - imported_files

        # Excluir __init__.py e arquivos de configuração
        dead_files = {f for f in dead_files
                     if '__init__.py' not in f and 'config' not in f.lower()}

        return {
            'total_files': len(all_files),
            'imported_files': len(imported_files),
            'dead_files': sorted(list(dead_files)),
            'dead_percentage': (len(dead_files) / len(all_files) * 100) if all_files else 0,
            'potential_lines_saved': len(dead_files) * 100  # Estimativa conservadora
        }

    def analyze_architectural_patterns(self) -> Dict:
        """
        Detecta padrões arquiteturais no código

        Identifica inconsistências que humanos não percebem:
        - Mix de Repository e Direct ORM
        - Services que acessam DB diretamente
        - Violações de camadas
        """
        patterns = {
            'repository_pattern': 0,
            'direct_orm': 0,
            'service_pattern': 0,
            'mixed_patterns': 0,
            'files_analyzed': 0,
            'inconsistencies': []
        }

        services_path = self.project_root / 'app' / 'services'
        if not services_path.exists():
            return patterns

        for py_file in services_path.rglob('*.py'):
            if '__pycache__' in str(py_file) or '__init__' in py_file.name:
                continue

            patterns['files_analyzed'] += 1

            try:
                with open(py_file) as f:
                    content = f.read()
                    tree = ast.parse(content)

                has_repository = False
                has_direct_orm = False
                direct_orm_lines = []

                for node in ast.walk(tree):
                    # Detectar Repository pattern
                    if isinstance(node, ast.Name):
                        if 'Repository' in node.id or 'repository' in node.id:
                            has_repository = True

                    # Detectar uso direto de ORM
                    if isinstance(node, ast.Attribute):
                        if node.attr in ['query', 'session', 'filter', 'filter_by']:
                            has_direct_orm = True
                            if hasattr(node, 'lineno'):
                                direct_orm_lines.append(node.lineno)

                rel_path = str(py_file.relative_to(self.project_root))

                if has_repository and not has_direct_orm:
                    patterns['repository_pattern'] += 1
                elif has_direct_orm and not has_repository:
                    patterns['direct_orm'] += 1
                elif has_repository and has_direct_orm:
                    patterns['mixed_patterns'] += 1
                    patterns['inconsistencies'].append({
                        'file': rel_path,
                        'issue': 'Mixes Repository pattern with direct ORM access',
                        'lines': direct_orm_lines[:5]
                    })

            except:
                continue

        # Calcular métricas
        if patterns['files_analyzed'] > 0:
            total = patterns['files_analyzed']
            patterns['repository_percentage'] = (patterns['repository_pattern'] / total) * 100
            patterns['direct_orm_percentage'] = (patterns['direct_orm'] / total) * 100
            patterns['mixed_percentage'] = (patterns['mixed_patterns'] / total) * 100

            # Score de consistência (quanto maior um padrão, melhor)
            patterns['consistency_score'] = max(
                patterns['repository_percentage'],
                patterns['direct_orm_percentage']
            )

        return patterns


def main():
    import argparse

    parser = argparse.ArgumentParser(description='AI-powered semantic code analysis')
    parser.add_argument('--duplicates', action='store_true', help='Find semantic duplicates')
    parser.add_argument('--dead-code', action='store_true', help='Detect dead code')
    parser.add_argument('--patterns', action='store_true', help='Analyze architectural patterns')
    parser.add_argument('--threshold', type=float, default=0.75,
                       help='Similarity threshold (0.0-1.0)')
    args = parser.parse_args()

    print("🤖 AI-POWERED SEMANTIC CODE ANALYSIS")
    print("=" * 80)
    print(f"📁 Project root: {project_root}")
    print()

    analyzer = SemanticAnalyzer(project_root)

    # Se nenhuma flag específica, rodar tudo
    run_all = not (args.duplicates or args.dead_code or args.patterns)

    # 1. Duplicação Semântica
    if args.duplicates or run_all:
        print("📊 1. SEMANTIC DUPLICATION DETECTION")
        print("-" * 80)
        print(f"Threshold: {args.threshold * 100}% similarity")
        print()

        duplicates = analyzer.find_semantic_duplicates(threshold=args.threshold)

        if duplicates:
            print(f"⚠️  Found {len(duplicates)} potential semantic duplicates:\n")

            for i, dup in enumerate(duplicates[:10], 1):  # Top 10
                print(f"{i}. Similarity: {dup['similarity']}%")
                print(f"   📄 {dup['file1']}:{dup['line1']} → {dup['function1']}()")
                print(f"   📄 {dup['file2']}:{dup['line2']} → {dup['function2']}()")
                print(f"   💡 {dup['recommendation']}")
                print()

            if len(duplicates) > 10:
                print(f"... and {len(duplicates) - 10} more duplicates")
        else:
            print("✅ No semantic duplicates found above threshold")

        print()

    # 2. Código Morto
    if args.dead_code or run_all:
        print("💀 2. DEAD CODE DETECTION")
        print("-" * 80)

        dead_analysis = analyzer.detect_dead_code()

        print(f"Total files scanned: {dead_analysis['total_files']}")
        print(f"Files with imports: {dead_analysis['imported_files']}")
        print(f"Dead files (never imported): {len(dead_analysis['dead_files'])} " +
              f"({dead_analysis['dead_percentage']:.1f}%)")

        if dead_analysis['dead_files']:
            print(f"\n⚠️  Potential dead code files:")
            for dead_file in dead_analysis['dead_files'][:20]:
                print(f"   - {dead_file}")

            if len(dead_analysis['dead_files']) > 20:
                remaining = len(dead_analysis['dead_files']) - 20
                print(f"   ... and {remaining} more files")

            print(f"\n💰 Potential savings:")
            print(f"   ~{dead_analysis['potential_lines_saved']} lines of code")
            print(f"   ~{dead_analysis['dead_percentage']:.1f}% reduction in codebase")
        else:
            print("\n✅ No dead code detected!")

        print()

    # 3. Padrões Arquiteturais
    if args.patterns or run_all:
        print("🏗️  3. ARCHITECTURAL PATTERN ANALYSIS")
        print("-" * 80)

        patterns = analyzer.analyze_architectural_patterns()

        if patterns['files_analyzed'] == 0:
            print("⚠️  No service files found to analyze")
        else:
            print(f"Services analyzed: {patterns['files_analyzed']}\n")

            print(f"Repository pattern:  {patterns['repository_pattern']} files " +
                  f"({patterns.get('repository_percentage', 0):.1f}%)")
            print(f"Direct ORM usage:    {patterns['direct_orm']} files " +
                  f"({patterns.get('direct_orm_percentage', 0):.1f}%)")
            print(f"Mixed patterns:      {patterns['mixed_patterns']} files " +
                  f"({patterns.get('mixed_percentage', 0):.1f}%)")

            consistency = patterns.get('consistency_score', 0)
            print(f"\nConsistency score: {consistency:.1f}%")

            if consistency < 70:
                print("\n⚠️  ARCHITECTURAL INCONSISTENCY DETECTED")
                print("   Different files use different patterns!")
                print("   💡 Recommendation: Standardize on ONE pattern")
            elif consistency < 90:
                print("\n⚠️  Moderate consistency - room for improvement")
            else:
                print("\n✅ Good architectural consistency!")

            # Mostrar inconsistências específicas
            if patterns['inconsistencies']:
                print(f"\n🔍 Specific inconsistencies found:")
                for inc in patterns['inconsistencies'][:5]:
                    print(f"\n   📄 {inc['file']}")
                    print(f"      {inc['issue']}")
                    if inc['lines']:
                        print(f"      Lines: {', '.join(map(str, inc['lines']))}")

        print()

    print("=" * 80)
    print("✅ Analysis complete!")


if __name__ == '__main__':
    main()
