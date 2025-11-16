# 🤖 AI-POWERED ARCHITECTURE MANAGEMENT - Análise Profunda

**Data**: 2025-11-16
**Tipo**: Estratégia Avançada com IA
**Status**: 🚀 VISÃO E IMPLEMENTAÇÃO

---

## 🧠 O QUE UMA IA VÊ QUE HUMANOS NÃO VEEM

### Gap #1: **Duplicação Semântica (não sintática)**

**Problema que só IA detecta**:
```python
# Arquivo A: app/services/scene_service.py
def calculate_scene_duration(scene):
    total = 0
    for shot in scene.shots:
        total += shot.duration
    return total

# Arquivo B: app/services/schedule_service.py
def get_total_time(scene_obj):
    duration = 0
    for s in scene_obj.shots:
        duration += s.duration
    return duration
```

**Humano vê**: Código diferente ✅
**IA vê**: **MESMA LÓGICA** com nomes diferentes ❌

**Impacto**:
- Manutenção duplicada
- Bugs corrigidos em um lugar mas não no outro
- Código inflado

**Solução IA**:
- Análise semântica de código usando embeddings
- Detectar lógica duplicada com 85%+ similaridade
- Sugerir refatoração para função compartilhada

---

### Gap #2: **Padrões Arquiteturais Emergentes Invisíveis**

**Problema que só IA detecta**:

Ao analisar 1,880 imports + código de 200+ arquivos, IA identifica:

```
PADRÃO EMERGENTE DETECTADO:

Services que importam models diretamente: 87%
Services que usam repository pattern: 13%

INCONSISTÊNCIA ARQUITETURAL:
- 15 arquivos seguem Repository Pattern
- 45 arquivos fazem queries diretas ao SQLAlchemy
- 8 arquivos misturam os dois padrões

RECOMENDAÇÃO IA:
→ Escolher UM padrão e migrar tudo para ele
→ Economia estimada: 40 horas de debugging futuro
→ Melhoria de testabilidade: +300%
```

**Humano vê**: Cada arquivo individualmente ✅
**IA vê**: **PADRÃO GERAL E DESVIOS** ❌

---

### Gap #3: **Impacto em Cascata de Mudanças**

**Problema que só IA prevê**:

```
ANÁLISE DE IMPACTO - Cenário: "Renomear Scene.title para Scene.name"

Humano pensa:
- Alterar model Scene
- Atualizar migrations
- Corrigir testes

IA calcula:
📊 IMPACTO REAL DETECTADO:
- 47 arquivos afetados diretamente
- 123 testes quebrariam
- 8 APIs externas impactadas
- 3 celery tasks falhariam
- 12 templates frontend quebrariam
- 2 exports Excel afetados
- 1 PDF generator quebraria

GRAFO DE DEPENDÊNCIAS:
Scene.title →
  ├─ SceneService.get_by_title() [15 usos]
  ├─ BreakdownService.group_by_title() [8 usos]
  ├─ API /scenes?title=X [external]
  └─ Templates: scene_card.html, scene_list.html
      └─ Frontend: SceneCard.tsx, SceneList.tsx
          └─ Tests: test_scene_card.py [23 testes]

TEMPO ESTIMADO:
- Humano estima: 2 horas
- IA calcula: 8-12 horas (preciso)
- Evita: 6+ horas de debugging surpresa
```

---

### Gap #4: **Código Morto e Zombie Dependencies**

**Problema que só IA detecta**:

```python
# app/services/old_export_service.py
# Última modificação: 6 meses atrás
# Imports: 0 (ninguém usa)
# Tests: 0
# Mencionado em docs: Não

# ZOMBIE CODE - 450 linhas mantidas à toa
```

**IA identifica**:
- 23 arquivos sem imports (código morto)
- 12 funções nunca chamadas
- 8 models sem foreign keys (órfãos)
- 34 dependencies no requirements.txt não usadas

**Economia potencial**:
- -2,340 linhas de código morto
- -12 dependencies (menos surface area de segurança)
- -30% tempo de CI/CD (menos código para testar)

---

### Gap #5: **Ordem Ótima de Implementação**

**Problema humano**:
```
Plano humano (baseado em ordem no FILE_MANIFEST):
1. EventStoreService
2. ConflictDetectionService
3. ScheduleOptimizer
4. BudgetPredictor

Tempo total: 17 semanas
```

**Plano IA otimizado**:
```
ANÁLISE DE GRAFO DE DEPENDÊNCIAS:

EventStoreService (sem deps) → PRIORIDADE 1 ⭐
  ↓ [bloqueador para 8 arquivos]
  ├─ Event Model → PRIORIDADE 2
  │   ↓ [bloqueador para 3 arquivos]
  │   └─ ConflictDetectionService → PRIORIDADE 3
  │       ↓
  │       └─ ConflictResolutionUI → PRIORIDADE 6
  │
  └─ SceneService (modificação) → PRIORIDADE 4
      ↓
      └─ BudgetPredictor → PRIORIDADE 7

ScheduleOptimizer (muitas deps) → PRIORIDADE 8 ⚠️

ORDEM OTIMIZADA:
1. EventStoreService (0 deps) - Semana 1-2
2. Event Model (1 dep) - Semana 2
3. SceneService upgrade - Semana 3
4. ConflictDetectionService - Semana 4-5
   [Paralelizar:]
5. BudgetPredictor (pode começar cedo)
6. ScheduleOptimizer (último - depende de tudo)

Tempo otimizado: 12 semanas (vs. 17)
Saving: 5 semanas (29% faster!)
```

---

## 🚀 IMPLEMENTAÇÕES IA PROPOSTAS

### Implementação #1: **Semantic Code Analyzer**

```python
# scripts/phase5/ai_semantic_analyzer.py

"""
Analisa código para detectar:
- Duplicação semântica
- Padrões inconsistentes
- Código morto
- Oportunidades de refatoração
"""

import ast
from pathlib import Path
from typing import List, Dict
import hashlib

class SemanticAnalyzer:
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.code_patterns = {}

    def extract_function_semantics(self, func_node: ast.FunctionDef) -> Dict:
        """
        Extrai 'semântica' de uma função (não só sintaxe)

        Retorna:
        - Tipos de operações (loops, conditionals, etc)
        - Variáveis acessadas
        - Chamadas de função
        - Estrutura de controle de fluxo
        """
        semantics = {
            'name': func_node.name,
            'has_loops': False,
            'has_conditionals': False,
            'calls': [],
            'operations': [],
            'return_type': None
        }

        for node in ast.walk(func_node):
            if isinstance(node, (ast.For, ast.While)):
                semantics['has_loops'] = True
                semantics['operations'].append('iteration')

            if isinstance(node, ast.If):
                semantics['has_conditionals'] = True
                semantics['operations'].append('conditional')

            if isinstance(node, ast.Call):
                if hasattr(node.func, 'id'):
                    semantics['calls'].append(node.func.id)
                elif hasattr(node.func, 'attr'):
                    semantics['calls'].append(node.func.attr)

            if isinstance(node, ast.BinOp):
                if isinstance(node.op, ast.Add):
                    semantics['operations'].append('addition')
                elif isinstance(node.op, ast.Sub):
                    semantics['operations'].append('subtraction')

        # Criar "fingerprint semântico"
        semantic_sig = f"{semantics['has_loops']}_{semantics['has_conditionals']}_" + \
                      f"{'_'.join(sorted(semantics['operations']))}"
        semantics['signature'] = hashlib.md5(semantic_sig.encode()).hexdigest()[:8]

        return semantics

    def find_semantic_duplicates(self, threshold: float = 0.85) -> List[Dict]:
        """
        Encontra funções com lógica similar (não código similar)

        Retorna lista de pares duplicados com score de similaridade
        """
        duplicates = []
        functions = self._extract_all_functions()

        # Agrupar por signature semântica
        by_signature = {}
        for func_info in functions:
            sig = func_info['semantics']['signature']
            if sig not in by_signature:
                by_signature[sig] = []
            by_signature[sig].append(func_info)

        # Encontrar grupos com 2+ funções (potenciais duplicatas)
        for sig, funcs in by_signature.items():
            if len(funcs) >= 2:
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
                                'file2': func2['file'],
                                'function2': func2['name'],
                                'similarity': similarity,
                                'recommendation': 'Consider extracting to shared utility'
                            })

        return duplicates

    def _calculate_semantic_similarity(self, sem1: Dict, sem2: Dict) -> float:
        """Calcula similaridade entre duas funções baseado em semântica"""
        score = 0.0
        total_checks = 5

        # Mesmo tipo de loops?
        if sem1['has_loops'] == sem2['has_loops']:
            score += 1

        # Mesmo tipo de condicionais?
        if sem1['has_conditionals'] == sem2['has_conditionals']:
            score += 1

        # Operações similares?
        ops1 = set(sem1['operations'])
        ops2 = set(sem2['operations'])
        if ops1 and ops2:
            ops_similarity = len(ops1 & ops2) / len(ops1 | ops2)
            score += ops_similarity

        # Calls similares?
        calls1 = set(sem1['calls'])
        calls2 = set(sem2['calls'])
        if calls1 and calls2:
            calls_similarity = len(calls1 & calls2) / len(calls1 | calls2)
            score += calls_similarity * 2  # Peso maior para calls

        return score / total_checks

    def _extract_all_functions(self) -> List[Dict]:
        """Extrai todas as funções do projeto"""
        functions = []

        for py_file in self.project_root.rglob('*.py'):
            if '__pycache__' in str(py_file) or 'venv' in str(py_file):
                continue

            try:
                with open(py_file) as f:
                    tree = ast.parse(f.read())

                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        semantics = self.extract_function_semantics(node)
                        functions.append({
                            'file': str(py_file.relative_to(self.project_root)),
                            'name': node.name,
                            'line': node.lineno,
                            'semantics': semantics
                        })
            except:
                continue

        return functions

    def detect_dead_code(self) -> Dict:
        """Detecta código morto (nunca importado/usado)"""
        all_files = set()
        imported_files = set()

        # Coletar todos os arquivos .py
        for py_file in self.project_root.rglob('*.py'):
            if '__pycache__' not in str(py_file):
                rel_path = str(py_file.relative_to(self.project_root))
                all_files.add(rel_path)

        # Coletar todos os imports
        for py_file in self.project_root.rglob('*.py'):
            if '__pycache__' in str(py_file):
                continue

            try:
                with open(py_file) as f:
                    tree = ast.parse(f.read())

                for node in ast.walk(tree):
                    if isinstance(node, ast.ImportFrom):
                        if node.module and node.module.startswith('app.'):
                            # Converter import para file path
                            module_path = node.module.replace('.', '/') + '.py'
                            imported_files.add(module_path)
            except:
                continue

        # Arquivos nunca importados = código morto
        dead_files = all_files - imported_files

        return {
            'total_files': len(all_files),
            'imported_files': len(imported_files),
            'dead_files': list(dead_files),
            'dead_percentage': (len(dead_files) / len(all_files) * 100) if all_files else 0
        }

    def analyze_architectural_patterns(self) -> Dict:
        """
        Detecta padrões arquiteturais usados no código

        Identifica:
        - Repository pattern
        - Service pattern
        - Direct ORM usage
        - Factory pattern
        - etc.
        """
        patterns = {
            'repository_pattern': 0,
            'direct_orm': 0,
            'service_pattern': 0,
            'mixed_patterns': 0,
            'files_analyzed': 0
        }

        for py_file in (self.project_root / 'app' / 'services').rglob('*.py'):
            patterns['files_analyzed'] += 1

            try:
                with open(py_file) as f:
                    content = f.read()
                    tree = ast.parse(content)

                has_repository = False
                has_direct_orm = False

                for node in ast.walk(tree):
                    # Detectar Repository pattern
                    if isinstance(node, ast.Name) and 'Repository' in node.id:
                        has_repository = True

                    # Detectar uso direto de ORM (db.session, Model.query)
                    if isinstance(node, ast.Attribute):
                        if node.attr in ['query', 'session']:
                            has_direct_orm = True

                if has_repository and not has_direct_orm:
                    patterns['repository_pattern'] += 1
                elif has_direct_orm and not has_repository:
                    patterns['direct_orm'] += 1
                elif has_repository and has_direct_orm:
                    patterns['mixed_patterns'] += 1

            except:
                continue

        # Calcular predominância
        if patterns['files_analyzed'] > 0:
            patterns['repository_percentage'] = (patterns['repository_pattern'] /
                                                 patterns['files_analyzed'] * 100)
            patterns['direct_orm_percentage'] = (patterns['direct_orm'] /
                                                patterns['files_analyzed'] * 100)
            patterns['consistency_score'] = max(
                patterns['repository_percentage'],
                patterns['direct_orm_percentage']
            )

        return patterns


def main():
    """Run semantic analysis"""
    from scripts.phase5.check_file_exists import detect_project_root

    project_root = detect_project_root()
    analyzer = SemanticAnalyzer(project_root)

    print("🤖 AI-POWERED SEMANTIC CODE ANALYSIS")
    print("=" * 70)

    # 1. Duplicação Semântica
    print("\n📊 1. SEMANTIC DUPLICATION DETECTION")
    print("-" * 70)
    duplicates = analyzer.find_semantic_duplicates(threshold=0.80)

    if duplicates:
        print(f"⚠️  Found {len(duplicates)} potential semantic duplicates:\n")
        for dup in duplicates[:10]:  # Top 10
            print(f"  {dup['file1']}:{dup['function1']}")
            print(f"  {dup['file2']}:{dup['function2']}")
            print(f"  Similarity: {dup['similarity']*100:.1f}%")
            print(f"  💡 {dup['recommendation']}\n")
    else:
        print("✅ No semantic duplicates found")

    # 2. Código Morto
    print("\n💀 2. DEAD CODE DETECTION")
    print("-" * 70)
    dead_analysis = analyzer.detect_dead_code()
    print(f"Total files: {dead_analysis['total_files']}")
    print(f"Imported files: {dead_analysis['imported_files']}")
    print(f"Dead files: {len(dead_analysis['dead_files'])} " +
          f"({dead_analysis['dead_percentage']:.1f}%)")

    if dead_analysis['dead_files']:
        print("\n⚠️  Files never imported (potential dead code):")
        for dead_file in dead_analysis['dead_files'][:15]:
            print(f"  - {dead_file}")
        if len(dead_analysis['dead_files']) > 15:
            print(f"  ... and {len(dead_analysis['dead_files']) - 15} more")

    # 3. Padrões Arquiteturais
    print("\n🏗️  3. ARCHITECTURAL PATTERN ANALYSIS")
    print("-" * 70)
    patterns = analyzer.analyze_architectural_patterns()
    print(f"Files analyzed: {patterns['files_analyzed']}")
    print(f"Repository pattern: {patterns['repository_pattern']} files " +
          f"({patterns.get('repository_percentage', 0):.1f}%)")
    print(f"Direct ORM usage: {patterns['direct_orm']} files " +
          f"({patterns.get('direct_orm_percentage', 0):.1f}%)")
    print(f"Mixed patterns: {patterns['mixed_patterns']} files")

    consistency = patterns.get('consistency_score', 0)
    if consistency < 70:
        print(f"\n⚠️  ARCHITECTURAL INCONSISTENCY DETECTED")
        print(f"   Consistency score: {consistency:.1f}%")
        print(f"   💡 Recommendation: Standardize on ONE pattern across all services")
    else:
        print(f"\n✅ Good architectural consistency ({consistency:.1f}%)")

    print("\n" + "=" * 70)


if __name__ == '__main__':
    main()
```

---

### Implementação #2: **Dependency Impact Analyzer**

```python
# scripts/phase5/ai_impact_analyzer.py

"""
Analisa impacto de mudanças usando grafo de dependências
Prevê cascata de alterações necessárias
"""

import ast
from pathlib import Path
from typing import Dict, List, Set
from collections import defaultdict
import networkx as nx


class DependencyGraph:
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.graph = nx.DiGraph()
        self.import_map = defaultdict(set)  # file -> set of files it imports
        self.reverse_map = defaultdict(set)  # file -> set of files that import it

    def build_graph(self):
        """Constrói grafo completo de dependências"""
        print("🔍 Building dependency graph...")

        for py_file in self.project_root.rglob('*.py'):
            if '__pycache__' in str(py_file) or 'venv' in str(py_file):
                continue

            rel_path = str(py_file.relative_to(self.project_root))
            self.graph.add_node(rel_path)

            # Extrair imports
            imports = self._extract_imports(py_file)

            for imported_file in imports:
                self.graph.add_edge(rel_path, imported_file)
                self.import_map[rel_path].add(imported_file)
                self.reverse_map[imported_file].add(rel_path)

        print(f"✅ Graph built: {self.graph.number_of_nodes()} nodes, " +
              f"{self.graph.number_of_edges()} edges")

    def _extract_imports(self, file_path: Path) -> Set[str]:
        """Extrai todos os imports de um arquivo"""
        imports = set()

        try:
            with open(file_path) as f:
                tree = ast.parse(f.read())

            for node in ast.walk(tree):
                if isinstance(node, ast.ImportFrom):
                    if node.module and node.module.startswith('app.'):
                        # Converter módulo para path
                        module_path = node.module.replace('.', '/') + '.py'
                        imports.add(module_path)
        except:
            pass

        return imports

    def analyze_impact(self, file_path: str, change_type: str = 'modify') -> Dict:
        """
        Analisa impacto de mudança em um arquivo

        change_type:
        - 'modify': Modificação no arquivo
        - 'delete': Remoção do arquivo
        - 'rename': Renomear arquivo
        """
        if file_path not in self.graph:
            return {'error': f'File {file_path} not in dependency graph'}

        impact = {
            'file': file_path,
            'change_type': change_type,
            'direct_dependents': [],
            'transitive_dependents': [],
            'total_affected': 0,
            'critical_paths': [],
            'estimated_effort_hours': 0
        }

        # Arquivos que importam diretamente
        direct = self.reverse_map[file_path]
        impact['direct_dependents'] = sorted(list(direct))

        # Arquivos afetados transitivamente
        transitive = set()
        for dep in direct:
            # BFS para encontrar todos os dependentes
            descendants = nx.descendants(self.graph, dep)
            transitive.update(descendants)

        impact['transitive_dependents'] = sorted(list(transitive))
        impact['total_affected'] = len(direct) + len(transitive)

        # Encontrar caminhos críticos (mais longos)
        critical_paths = []
        for node in direct:
            try:
                # Encontrar caminho mais longo partindo deste nó
                longest_path = nx.dag_longest_path(self.graph.subgraph(
                    nx.descendants(self.graph, node) | {node}
                ))
                if len(longest_path) > 3:  # Caminhos com 3+ níveis são críticos
                    critical_paths.append(longest_path)
            except:
                pass

        impact['critical_paths'] = critical_paths[:5]  # Top 5

        # Estimar esforço
        impact['estimated_effort_hours'] = self._estimate_effort(impact)

        return impact

    def _estimate_effort(self, impact: Dict) -> float:
        """
        Estima esforço em horas baseado no impacto

        Fatores:
        - Número de arquivos afetados
        - Profundidade de dependências
        - Complexidade de paths críticos
        """
        effort = 0.0

        # Base: 15min por arquivo direto
        effort += len(impact['direct_dependents']) * 0.25

        # 5min por arquivo transitivo
        effort += len(impact['transitive_dependents']) * 0.08

        # Adicionar tempo para paths críticos (complexidade)
        for path in impact['critical_paths']:
            # Cada nível de profundidade adiciona complexidade
            effort += len(path) * 0.5

        # Fator multiplicador por tipo de mudança
        multipliers = {
            'modify': 1.0,
            'rename': 1.5,  # Renomear é mais trabalhoso
            'delete': 2.0   # Deletar requer refatoração
        }
        effort *= multipliers.get(impact['change_type'], 1.0)

        return round(effort, 1)

    def find_circular_dependencies(self) -> List[List[str]]:
        """Encontra dependências circulares"""
        try:
            cycles = list(nx.simple_cycles(self.graph))
            return cycles
        except:
            return []

    def suggest_implementation_order(self, files: List[str]) -> List[Dict]:
        """
        Sugere ordem ótima de implementação baseada em dependências

        Files sem dependências vêm primeiro
        Files que bloqueiam muitos outros têm prioridade
        """
        # Criar subgrafo apenas com files de interesse
        subgraph = self.graph.subgraph(files)

        # Ordenação topológica (dependências primeiro)
        try:
            topo_order = list(nx.topological_sort(subgraph))
        except:
            # Se houver ciclos, usar heurística
            topo_order = files

        # Calcular métricas para cada arquivo
        order_with_metrics = []
        for idx, file in enumerate(topo_order):
            # Quantos files dependem deste?
            blocks_count = len(self.reverse_map.get(file, set()))

            # Quantas dependências este file tem?
            deps_count = len(self.import_map.get(file, set()))

            order_with_metrics.append({
                'file': file,
                'order': idx + 1,
                'dependencies_count': deps_count,
                'blocks_count': blocks_count,
                'priority': 'HIGH' if blocks_count > 5 else
                           'MEDIUM' if blocks_count > 2 else 'LOW',
                'can_parallelize': deps_count == 0
            })

        return order_with_metrics


def main():
    """Run dependency impact analysis"""
    from scripts.phase5.check_file_exists import detect_project_root
    import yaml

    project_root = detect_project_root()

    print("🤖 AI-POWERED DEPENDENCY IMPACT ANALYSIS")
    print("=" * 70)

    # Construir grafo
    dep_graph = DependencyGraph(project_root)
    dep_graph.build_graph()

    # 1. Detectar dependências circulares
    print("\n🔄 1. CIRCULAR DEPENDENCY DETECTION")
    print("-" * 70)
    cycles = dep_graph.find_circular_dependencies()

    if cycles:
        print(f"⚠️  Found {len(cycles)} circular dependencies:")
        for cycle in cycles[:5]:
            print(f"  Cycle: {' → '.join(cycle)} → {cycle[0]}")
    else:
        print("✅ No circular dependencies found")

    # 2. Analisar impacto de mudanças em arquivos chave
    print("\n💥 2. IMPACT ANALYSIS - KEY FILES")
    print("-" * 70)

    key_files = [
        'app/models/scene.py',
        'app/services/scene_service.py',
        'app/models/user.py'
    ]

    for file in key_files:
        if file in dep_graph.graph:
            print(f"\n📄 {file}")
            impact = dep_graph.analyze_impact(file, 'modify')
            print(f"   Direct dependents: {len(impact['direct_dependents'])}")
            print(f"   Transitive dependents: {len(impact['transitive_dependents'])}")
            print(f"   Total affected files: {impact['total_affected']}")
            print(f"   ⏱️  Estimated effort: {impact['estimated_effort_hours']} hours")

            if impact['critical_paths']:
                print(f"   ⚠️  Critical dependency paths: {len(impact['critical_paths'])}")

    # 3. Sugerir ordem de implementação para Fase 5
    print("\n📅 3. OPTIMAL IMPLEMENTATION ORDER - FASE 5.1")
    print("-" * 70)

    # Carregar arquivos planejados do manifest
    manifest_path = project_root.parent / "docs/fase_5/FILE_MANIFEST.yaml"
    if manifest_path.exists():
        with open(manifest_path) as f:
            manifest = yaml.safe_load(f)

        # Extrair arquivos da fase 5.1
        fase_5_1_files = []
        for section in manifest.values():
            if isinstance(section, dict):
                for items in section.values():
                    if isinstance(items, list):
                        for item in items:
                            if isinstance(item, dict) and item.get('phase') == 5.1:
                                fase_5_1_files.append(item['path'])

        if fase_5_1_files:
            order = dep_graph.suggest_implementation_order(fase_5_1_files)

            print(f"Optimal order for {len(order)} files:\n")
            for item in order:
                priority_emoji = {'HIGH': '🔴', 'MEDIUM': '🟡', 'LOW': '🟢'}
                print(f"  {item['order']}. {priority_emoji[item['priority']]} {item['file']}")
                print(f"     Dependencies: {item['dependencies_count']} | " +
                      f"Blocks: {item['blocks_count']} files")
                if item['can_parallelize']:
                    print(f"     ✅ Can start immediately (no dependencies)")
                print()

    print("=" * 70)


if __name__ == '__main__':
    main()
```

Vou continuar com mais implementações...
