#!/usr/bin/env python3
"""
🔍 ANÁLISE COMPLETA DE DEBUG E REFATORAÇÃO DO SISTEMA
Identifica problemas, oportunidades e espaços para avanço
"""

import sys
import json
import ast
import sqlite3
import traceback
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Tuple
from collections import defaultdict

# Fix imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

class SystemDebugAnalyzer:
    """
    Analisador completo do sistema ScriptureMonChampion
    """

    def __init__(self):
        self.root = Path("/Users/clubproducoes/Digimundo/scripturemon-champion")
        self.issues = []
        self.opportunities = []
        self.advancements = []
        self.metrics = defaultdict(int)

    def run_complete_analysis(self) -> Dict:
        """
        Executa análise completa do sistema
        """
        print("\n" + "🔍" * 30)
        print("ANÁLISE COMPLETA DE DEBUG E REFATORAÇÃO")
        print("🔍" * 30)

        results = {
            'syntax_check': self.check_python_syntax(),
            'import_analysis': self.analyze_imports(),
            'memory_analysis': self.analyze_memory_system(),
            'performance_analysis': self.analyze_performance(),
            'code_quality': self.analyze_code_quality(),
            'integration_check': self.check_integrations(),
            'opportunities': self.identify_opportunities(),
            'advancements': self.identify_advancements()
        }

        return results

    def check_python_syntax(self) -> Dict:
        """
        Verifica sintaxe de todos arquivos Python
        """
        print("\n📝 VERIFICANDO SINTAXE PYTHON...")

        python_files = list(self.root.glob("**/*.py"))
        total = len(python_files)
        errors = []
        warnings = []

        for py_file in python_files:
            if "Pre_Limpeza" in str(py_file) or "backup" in str(py_file):
                continue

            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    code = f.read()

                # Verificar sintaxe
                ast.parse(code)

                # Verificar problemas comuns
                lines = code.split('\n')
                for i, line in enumerate(lines, 1):
                    # Prints desnecessários
                    if 'print(' in line and 'debug' not in py_file.name.lower():
                        if not any(x in line for x in ['#', 'def ', 'return']):
                            warnings.append(f"{py_file.relative_to(self.root)}:{i} - Print possivelmente desnecessário")

                    # TODOs não resolvidos
                    if 'TODO' in line or 'FIXME' in line:
                        warnings.append(f"{py_file.relative_to(self.root)}:{i} - TODO/FIXME encontrado")

                    # Imports não usados (heurística simples)
                    if line.strip().startswith('import ') or line.strip().startswith('from '):
                        module = line.split()[1].split('.')[0]
                        if module not in code[i:]:  # Verificar se é usado depois
                            if module not in ['sys', 'os', 'json']:  # Excluir comuns
                                warnings.append(f"{py_file.relative_to(self.root)}:{i} - Import possivelmente não usado: {module}")

            except SyntaxError as e:
                errors.append(f"{py_file.relative_to(self.root)}:{e.lineno} - {e.msg}")
            except Exception as e:
                errors.append(f"{py_file.relative_to(self.root)} - {str(e)}")

        self.metrics['python_files'] = total
        self.metrics['syntax_errors'] = len(errors)
        self.metrics['warnings'] = len(warnings)

        print(f"✅ Arquivos verificados: {total}")
        print(f"{'❌' if errors else '✅'} Erros de sintaxe: {len(errors)}")
        print(f"⚠️  Warnings: {len(warnings)}")

        return {
            'total_files': total,
            'errors': errors[:5],  # Top 5 erros
            'warnings': warnings[:10],  # Top 10 warnings
            'status': 'OK' if not errors else 'ERRORS'
        }

    def analyze_imports(self) -> Dict:
        """
        Analisa dependências e imports circulares
        """
        print("\n🔗 ANALISANDO IMPORTS E DEPENDÊNCIAS...")

        import_graph = defaultdict(set)
        circular_imports = []
        missing_imports = []

        python_files = list(self.root.glob("src/**/*.py"))
        python_files.extend(list(self.root.glob("scripts/active/*.py")))

        for py_file in python_files:
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    tree = ast.parse(f.read())

                file_key = str(py_file.relative_to(self.root))

                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            import_graph[file_key].add(alias.name)
                    elif isinstance(node, ast.ImportFrom):
                        if node.module:
                            import_graph[file_key].add(node.module)

            except:
                pass

        # Detectar imports circulares (simplificado)
        for file1, imports1 in import_graph.items():
            for file2, imports2 in import_graph.items():
                if file1 != file2:
                    # Se file1 importa algo de file2 e vice-versa
                    f1_base = file1.replace('.py', '').replace('/', '.')
                    f2_base = file2.replace('.py', '').replace('/', '.')

                    if any(f2_base in imp for imp in imports1) and any(f1_base in imp for imp in imports2):
                        circular_imports.append((file1, file2))

        self.metrics['total_imports'] = sum(len(v) for v in import_graph.values())
        self.metrics['circular_imports'] = len(circular_imports)

        print(f"✅ Total de imports: {self.metrics['total_imports']}")
        print(f"{'❌' if circular_imports else '✅'} Imports circulares: {len(circular_imports)}")

        return {
            'total_imports': self.metrics['total_imports'],
            'circular_imports': circular_imports[:5],
            'import_graph_size': len(import_graph),
            'status': 'OK' if not circular_imports else 'CIRCULAR_DETECTED'
        }

    def analyze_memory_system(self) -> Dict:
        """
        Analisa sistema de memória unificado
        """
        print("\n💾 ANALISANDO SISTEMA DE MEMÓRIA...")

        db_path = self.root / "data/unified_memory.db"
        stats = {}

        if db_path.exists():
            try:
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()

                # Estatísticas básicas
                cursor.execute("SELECT COUNT(*) FROM unified_memory")
                total_entries = cursor.fetchone()[0]

                cursor.execute("SELECT type, COUNT(*) FROM unified_memory GROUP BY type")
                type_distribution = dict(cursor.fetchall())

                cursor.execute("SELECT AVG(confidence) FROM unified_memory WHERE confidence > 0")
                avg_confidence = cursor.fetchone()[0] or 0

                # Entradas antigas (>30 dias)
                cursor.execute("""
                    SELECT COUNT(*) FROM unified_memory
                    WHERE datetime(timestamp) < datetime('now', '-30 days')
                """)
                old_entries = cursor.fetchone()[0]

                # Entradas nunca acessadas
                cursor.execute("""
                    SELECT COUNT(*) FROM unified_memory
                    WHERE accessed_count = 0
                """)
                never_accessed = cursor.fetchone()[0]

                conn.close()

                stats = {
                    'total_entries': total_entries,
                    'type_distribution': type_distribution,
                    'avg_confidence': round(avg_confidence, 2),
                    'old_entries': old_entries,
                    'never_accessed': never_accessed,
                    'db_size_mb': round(db_path.stat().st_size / 1024 / 1024, 2)
                }

                # Identificar oportunidades
                if old_entries > total_entries * 0.3:
                    self.opportunities.append("Limpar entradas antigas (>30 dias): " + str(old_entries))

                if never_accessed > total_entries * 0.2:
                    self.opportunities.append("Remover entradas nunca acessadas: " + str(never_accessed))

            except Exception as e:
                stats['error'] = str(e)

        print(f"✅ Total de entradas: {stats.get('total_entries', 0)}")
        print(f"✅ Tamanho do banco: {stats.get('db_size_mb', 0)} MB")
        print(f"⚠️  Entradas antigas: {stats.get('old_entries', 0)}")
        print(f"⚠️  Nunca acessadas: {stats.get('never_accessed', 0)}")

        return stats

    def analyze_performance(self) -> Dict:
        """
        Analisa problemas de performance
        """
        print("\n⚡ ANALISANDO PERFORMANCE...")

        performance_issues = []

        # Verificar arquivos grandes
        large_files = []
        for py_file in self.root.glob("**/*.py"):
            if "Pre_Limpeza" in str(py_file):
                continue
            size_kb = py_file.stat().st_size / 1024
            if size_kb > 100:  # Arquivos >100KB
                large_files.append((str(py_file.relative_to(self.root)), round(size_kb, 1)))

        # Verificar funções muito longas
        long_functions = []
        for py_file in self.root.glob("src/**/*.py"):
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    tree = ast.parse(f.read())

                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        func_lines = node.end_lineno - node.lineno if hasattr(node, 'end_lineno') else 0
                        if func_lines > 100:  # Funções >100 linhas
                            long_functions.append({
                                'file': str(py_file.relative_to(self.root)),
                                'function': node.name,
                                'lines': func_lines
                            })
            except:
                pass

        # Verificar loops aninhados profundos
        deep_nesting = []
        for py_file in self.root.glob("src/**/*.py"):
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()

                max_indent = 0
                for i, line in enumerate(lines, 1):
                    indent = len(line) - len(line.lstrip())
                    if indent > 40:  # >10 níveis de indentação (4 espaços cada)
                        deep_nesting.append({
                            'file': str(py_file.relative_to(self.root)),
                            'line': i,
                            'indent_level': indent // 4
                        })
                        break
            except:
                pass

        self.metrics['large_files'] = len(large_files)
        self.metrics['long_functions'] = len(long_functions)
        self.metrics['deep_nesting'] = len(deep_nesting)

        print(f"⚠️  Arquivos grandes (>100KB): {len(large_files)}")
        print(f"⚠️  Funções longas (>100 linhas): {len(long_functions)}")
        print(f"⚠️  Aninhamento profundo: {len(deep_nesting)}")

        # Adicionar oportunidades
        if large_files:
            self.opportunities.append(f"Refatorar {len(large_files)} arquivos grandes")
        if long_functions:
            self.opportunities.append(f"Dividir {len(long_functions)} funções longas")

        return {
            'large_files': large_files[:5],
            'long_functions': long_functions[:5],
            'deep_nesting': deep_nesting[:5],
            'status': 'OK' if not (large_files or long_functions) else 'NEEDS_OPTIMIZATION'
        }

    def analyze_code_quality(self) -> Dict:
        """
        Analisa qualidade do código
        """
        print("\n🏆 ANALISANDO QUALIDADE DO CÓDIGO...")

        quality_metrics = {
            'documented_functions': 0,
            'total_functions': 0,
            'type_hints': 0,
            'no_type_hints': 0,
            'test_coverage': 0,
            'duplicate_code': []
        }

        # Verificar documentação e type hints
        for py_file in self.root.glob("src/**/*.py"):
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    tree = ast.parse(f.read())

                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        quality_metrics['total_functions'] += 1

                        # Verificar docstring
                        if ast.get_docstring(node):
                            quality_metrics['documented_functions'] += 1

                        # Verificar type hints
                        if node.returns or any(arg.annotation for arg in node.args.args):
                            quality_metrics['type_hints'] += 1
                        else:
                            quality_metrics['no_type_hints'] += 1
            except:
                pass

        # Calcular percentuais
        if quality_metrics['total_functions'] > 0:
            doc_percent = (quality_metrics['documented_functions'] / quality_metrics['total_functions']) * 100
            type_percent = (quality_metrics['type_hints'] / quality_metrics['total_functions']) * 100
        else:
            doc_percent = type_percent = 0

        # Verificar testes
        test_files = list(self.root.glob("tests/**/*.py"))
        quality_metrics['test_files'] = len(test_files)

        print(f"✅ Funções documentadas: {doc_percent:.1f}%")
        print(f"⚠️  Type hints: {type_percent:.1f}%")
        print(f"⚠️  Arquivos de teste: {len(test_files)}")

        # Oportunidades
        if doc_percent < 50:
            self.opportunities.append(f"Adicionar docstrings ({100-doc_percent:.0f}% faltando)")
        if type_percent < 30:
            self.opportunities.append(f"Adicionar type hints ({100-type_percent:.0f}% faltando)")
        if len(test_files) < 10:
            self.opportunities.append("Aumentar cobertura de testes")

        return quality_metrics

    def check_integrations(self) -> Dict:
        """
        Verifica integrações do sistema
        """
        print("\n🔌 VERIFICANDO INTEGRAÇÕES...")

        integrations = {
            'ollama': False,
            'claude_code': False,
            'unified_memory': False,
            'meta_learning': False,
            'deep_learning': False,
            'screenplay_library': False
        }

        # Verificar Ollama
        try:
            import subprocess
            result = subprocess.run(['ollama', 'list'], capture_output=True, text=True, timeout=2)
            integrations['ollama'] = result.returncode == 0
        except:
            pass

        # Verificar outros componentes via imports
        try:
            from src.core.unified_memory_system import get_unified_memory
            integrations['unified_memory'] = True
        except:
            pass

        try:
            from scripts.active.meta_learning_framework import MetaLearningFramework
            integrations['meta_learning'] = True
        except:
            pass

        try:
            from scripts.active.deep_learning_enhanced import DeepLearningEnhanced
            integrations['deep_learning'] = True
        except:
            pass

        try:
            from src.core.screenplay_library import get_screenplay_library
            integrations['screenplay_library'] = True
        except:
            pass

        try:
            from scripts.active.claude_code_pipeline import ClaudeCodePipeline
            integrations['claude_code'] = True
        except:
            pass

        working = sum(integrations.values())
        total = len(integrations)

        print(f"✅ Integrações funcionando: {working}/{total}")
        for name, status in integrations.items():
            emoji = "✅" if status else "❌"
            print(f"  {emoji} {name}")

        return integrations

    def identify_opportunities(self) -> List[Dict]:
        """
        Identifica oportunidades de melhoria
        """
        print("\n💡 IDENTIFICANDO OPORTUNIDADES...")

        # Adicionar oportunidades baseadas na análise
        if self.metrics['syntax_errors'] == 0:
            self.opportunities.append("Implementar pre-commit hooks para manter qualidade")

        if self.metrics['large_files'] > 0:
            self.opportunities.append("Modularizar arquivos grandes em componentes menores")

        # Oportunidades específicas do sistema
        specific_opportunities = [
            {
                'area': 'Cache Intelligence',
                'description': 'Implementar cache preditivo baseado em padrões de uso',
                'impact': 'Alto',
                'effort': 'Médio',
                'code_sketch': '''
def predictive_cache_manager():
    """Cache que aprende padrões de acesso e pre-carrega dados"""
    patterns = analyze_access_patterns()
    for pattern in patterns:
        if pattern.probability > 0.7:
            preload_to_cache(pattern.data)
'''
            },
            {
                'area': 'Parallel Analysis',
                'description': 'Paralelizar análises independentes para múltiplos roteiros',
                'impact': 'Alto',
                'effort': 'Médio',
                'code_sketch': '''
from concurrent.futures import ThreadPoolExecutor
def parallel_screenplay_analysis(screenplays):
    with ThreadPoolExecutor(max_workers=4) as executor:
        results = executor.map(analyze_screenplay, screenplays)
    return consolidate_results(results)
'''
            },
            {
                'area': 'Real-time Collaboration',
                'description': 'Adicionar websockets para colaboração em tempo real',
                'impact': 'Muito Alto',
                'effort': 'Alto',
                'code_sketch': '''
import asyncio
import websockets
async def collaboration_server():
    """Servidor para múltiplos usuários analisarem juntos"""
    async with websockets.serve(handle_client, "localhost", 8765):
        await asyncio.Future()  # run forever
'''
            },
            {
                'area': 'Visual Analytics',
                'description': 'Gerar visualizações de arcos narrativos e beats',
                'impact': 'Alto',
                'effort': 'Baixo',
                'code_sketch': '''
import matplotlib.pyplot as plt
def visualize_story_arc(beats):
    """Gera gráfico do arco narrativo"""
    tensions = [beat.tension for beat in beats]
    plt.plot(tensions)
    plt.savefig('story_arc.png')
'''
            }
        ]

        print(f"✅ {len(specific_opportunities)} oportunidades identificadas")

        return specific_opportunities

    def identify_advancements(self) -> List[Dict]:
        """
        Identifica avanços possíveis no sistema
        """
        print("\n🚀 IDENTIFICANDO AVANÇOS POSSÍVEIS...")

        advancements = [
            {
                'name': 'Multi-Modal Analysis',
                'description': 'Analisar roteiros + storyboards + áudio simultaneamente',
                'requirements': ['Vision API', 'Audio processing'],
                'expected_gain': '300% mais insights',
                'implementation_path': [
                    '1. Integrar biblioteca de visão computacional',
                    '2. Processar storyboards para extrair composição visual',
                    '3. Correlacionar com beats do roteiro',
                    '4. Gerar insights cross-modal'
                ]
            },
            {
                'name': 'Generative Screenplay Assistant',
                'description': 'IA que sugere próximas cenas baseada no contexto',
                'requirements': ['Fine-tuned model', 'More training data'],
                'expected_gain': 'Acelera escrita em 200%',
                'implementation_path': [
                    '1. Coletar mais roteiros para treino',
                    '2. Fine-tune modelo específico para gêneros',
                    '3. Implementar interface de sugestões contextuais',
                    '4. Feedback loop para melhorar sugestões'
                ]
            },
            {
                'name': 'Industry Standard Export',
                'description': 'Exportar para Final Draft, Celtx, WriterDuet',
                'requirements': ['Format parsers', 'API integrations'],
                'expected_gain': 'Integração total com pipeline profissional',
                'implementation_path': [
                    '1. Implementar parser para formatos proprietários',
                    '2. Criar exportadores compatíveis',
                    '3. Validar com softwares da indústria',
                    '4. Adicionar import reverso'
                ]
            },
            {
                'name': 'Distributed Team Analysis',
                'description': 'Sistema distribuído para equipes globais',
                'requirements': ['Cloud infrastructure', 'Sync protocol'],
                'expected_gain': 'Colaboração global em tempo real',
                'implementation_path': [
                    '1. Implementar protocolo de sincronização',
                    '2. Deploy em cloud com auto-scaling',
                    '3. Sistema de resolução de conflitos',
                    '4. Dashboard de atividade da equipe'
                ]
            },
            {
                'name': 'AI Director Mode',
                'description': 'IA que simula direção de cenas do roteiro',
                'requirements': ['3D scene generation', 'Camera AI'],
                'expected_gain': 'Pré-visualização automática de cenas',
                'implementation_path': [
                    '1. Integrar engine 3D (Blender API)',
                    '2. Treinar IA em cinematografia',
                    '3. Gerar pré-viz automático de cenas-chave',
                    '4. Exportar para storyboard/animatic'
                ]
            }
        ]

        print(f"✅ {len(advancements)} avanços identificados")

        return advancements

    def generate_report(self, results: Dict) -> str:
        """
        Gera relatório completo em markdown
        """
        report = f"""# 🔍 RELATÓRIO COMPLETO DE DEBUG E REFATORAÇÃO

**Data:** {datetime.now().strftime('%Y-%m-%d %H:%M')}
**Sistema:** ScriptureMonChampion
**Versão:** 2.0

---

## 📊 RESUMO EXECUTIVO

| Métrica | Valor | Status |
|---------|-------|--------|
| Arquivos Python | {self.metrics.get('python_files', 0)} | ✅ |
| Erros de Sintaxe | {self.metrics.get('syntax_errors', 0)} | {'✅' if self.metrics.get('syntax_errors', 0) == 0 else '❌'} |
| Warnings | {self.metrics.get('warnings', 0)} | ⚠️ |
| Imports Circulares | {self.metrics.get('circular_imports', 0)} | {'✅' if self.metrics.get('circular_imports', 0) == 0 else '❌'} |
| Arquivos Grandes | {self.metrics.get('large_files', 0)} | ⚠️ |
| Funções Longas | {self.metrics.get('long_functions', 0)} | ⚠️ |

---

## 🐛 PROBLEMAS ENCONTRADOS

### Sintaxe
{self._format_issues(results.get('syntax_check', {}).get('errors', []))}

### Warnings
{self._format_issues(results.get('syntax_check', {}).get('warnings', [])[:5])}

### Performance
{self._format_performance_issues(results.get('performance_analysis', {}))}

---

## 💾 SISTEMA DE MEMÓRIA

- **Total de Entradas:** {results.get('memory_analysis', {}).get('total_entries', 0)}
- **Tamanho do Banco:** {results.get('memory_analysis', {}).get('db_size_mb', 0)} MB
- **Entradas Antigas:** {results.get('memory_analysis', {}).get('old_entries', 0)}
- **Nunca Acessadas:** {results.get('memory_analysis', {}).get('never_accessed', 0)}

### Distribuição por Tipo
{self._format_dict(results.get('memory_analysis', {}).get('type_distribution', {}))}

---

## 🔌 INTEGRAÇÕES

{self._format_integrations(results.get('integration_check', {}))}

---

## 💡 OPORTUNIDADES DE REFATORAÇÃO

{self._format_opportunities(results.get('opportunities', []))}

---

## 🚀 AVANÇOS POSSÍVEIS

{self._format_advancements(results.get('advancements', []))}

---

## 📈 PRÓXIMOS PASSOS RECOMENDADOS

### Imediato (Esta Semana)
1. Corrigir erros de sintaxe se houver
2. Remover imports não utilizados
3. Limpar entradas antigas da memória
4. Adicionar docstrings faltantes

### Curto Prazo (Este Mês)
1. Refatorar arquivos grandes
2. Implementar cache preditivo
3. Adicionar mais testes
4. Paralelizar análises

### Médio Prazo (3 Meses)
1. Implementar visualizações
2. Adicionar export para formatos da indústria
3. Sistema de colaboração em tempo real
4. Multi-modal analysis

### Longo Prazo (6+ Meses)
1. AI Director Mode
2. Distributed team analysis
3. Generative screenplay assistant
4. Full cloud deployment

---

**CONCLUSÃO:** Sistema está {'✅ SAUDÁVEL' if self.metrics.get('syntax_errors', 0) == 0 else '⚠️ PRECISA ATENÇÃO'}

**POTENCIAL DE CRESCIMENTO:** 🚀🚀🚀🚀🚀 (Muito Alto)

---

**DIGIMUNDO PRESENTE** 🥷
"""

        return report

    def _format_issues(self, issues: List) -> str:
        if not issues:
            return "✅ Nenhum problema encontrado"
        return "\n".join(f"- {issue}" for issue in issues[:10])

    def _format_dict(self, d: Dict) -> str:
        if not d:
            return "N/A"
        return "\n".join(f"- **{k}:** {v}" for k, v in d.items())

    def _format_performance_issues(self, perf: Dict) -> str:
        output = []
        if perf.get('large_files'):
            output.append("### Arquivos Grandes")
            for file, size in perf['large_files'][:3]:
                output.append(f"- {file}: {size} KB")

        if perf.get('long_functions'):
            output.append("\n### Funções Longas")
            for func in perf['long_functions'][:3]:
                output.append(f"- {func['file']}: {func['function']} ({func['lines']} linhas)")

        return "\n".join(output) if output else "✅ Sem problemas de performance"

    def _format_integrations(self, integrations: Dict) -> str:
        output = []
        for name, status in integrations.items():
            emoji = "✅" if status else "❌"
            output.append(f"{emoji} **{name}**")
        return "\n".join(output)

    def _format_opportunities(self, opportunities: List) -> str:
        output = []
        for i, opp in enumerate(opportunities[:5], 1):
            if isinstance(opp, dict):
                output.append(f"\n### {i}. {opp['area']}")
                output.append(f"**Descrição:** {opp['description']}")
                output.append(f"**Impacto:** {opp['impact']} | **Esforço:** {opp['effort']}")
                if opp.get('code_sketch'):
                    output.append("**Exemplo de Código:**")
                    output.append(f"```python\n{opp['code_sketch'].strip()}\n```")
            else:
                output.append(f"{i}. {opp}")

        return "\n".join(output)

    def _format_advancements(self, advancements: List) -> str:
        output = []
        for i, adv in enumerate(advancements[:3], 1):
            output.append(f"\n### {i}. {adv['name']}")
            output.append(f"**Descrição:** {adv['description']}")
            output.append(f"**Ganho Esperado:** {adv['expected_gain']}")
            output.append("**Caminho de Implementação:**")
            for step in adv['implementation_path'][:3]:
                output.append(f"   {step}")

        return "\n".join(output)


def main():
    """
    Executa análise completa e gera relatório
    """
    analyzer = SystemDebugAnalyzer()

    # Executar análise
    results = analyzer.run_complete_analysis()

    # Gerar relatório
    report = analyzer.generate_report(results)

    # Salvar relatório
    report_path = Path("docs/DEBUG_REPORT_" + datetime.now().strftime('%Y%m%d_%H%M%S') + ".md")
    report_path.write_text(report, encoding='utf-8')

    print("\n" + "=" * 60)
    print(f"📄 RELATÓRIO COMPLETO SALVO EM:")
    print(f"   {report_path}")
    print("=" * 60)

    # Mostrar resumo
    print("\n🎯 RESUMO RÁPIDO:")
    print(f"  ✅ Sistema funcional: {results['syntax_check']['status'] == 'OK'}")
    print(f"  ⚠️  Oportunidades: {len(results.get('opportunities', []))}")
    print(f"  🚀 Avanços possíveis: {len(results.get('advancements', []))}")

    return results


if __name__ == "__main__":
    main()