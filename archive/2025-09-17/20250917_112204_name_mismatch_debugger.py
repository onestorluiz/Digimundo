"""
🔍 NAME MISMATCH DEBUGGER - Silicon Valley Grade
Sistema avançado para detectar e corrigir inconsistências de nomes

Técnicas implementadas:
1. Fuzzy Matching - Encontra nomes similares
2. Levenshtein Distance - Mede diferença entre strings
3. AST Analysis - Analisa imports e definições
4. Dependency Graph - Mapeia dependências
5. Auto-correction - Sugere e aplica correções
6. Pattern Recognition - Detecta padrões de nomenclatura
"""
import ast
import os
import re
import sys
import json
import difflib
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional, Any
from dataclasses import dataclass, field
from collections import defaultdict, Counter
import importlib.util
import inspect
try:
    from fuzzywuzzy import fuzz, process
    HAS_FUZZY = True
except ImportError:
    HAS_FUZZY = False
    print('⚠️  fuzzywuzzy not installed. Using difflib fallback.')

@dataclass
class NameMismatch:
    """Representa um mismatch encontrado"""
    file_path: str
    line_number: int
    expected_name: str
    actual_name: str
    mismatch_type: str
    confidence: float
    suggested_fix: str
    context: str = ''

    def __str__(self):
        return f'📍 {self.file_path}:{self.line_number}\n   Expected: {self.expected_name}\n   Found: {self.actual_name}\n   Type: {self.mismatch_type}\n   Confidence: {self.confidence:.1f}%\n   Fix: {self.suggested_fix}'

@dataclass
class NamePattern:
    """Padrões de nomenclatura detectados"""
    pattern_type: str
    examples: List[str] = field(default_factory=list)
    frequency: int = 0

class NameMismatchDebugger:
    """Debugger avançado para mismatches de nomes"""

    def __init__(self, root_path: str='.'):
        self.root_path = Path(root_path)
        self.mismatches: List[NameMismatch] = []
        self.name_registry: Dict[str, Set[str]] = defaultdict(set)
        self.import_graph: Dict[str, Set[str]] = defaultdict(set)
        self.pattern_stats: Dict[str, NamePattern] = {}
        self.common_typos = self._load_common_typos()

    def _load_common_typos(self) -> Dict[str, str]:
        """Carrega padrões comuns de typos"""
        return {'DigionProducerMonOrchestrator': 'DigionProducerMonOrchestrator', 'DigionProducerMon': 'DigionProducerMon', 'ProducerMon': 'ProducerMon', 'Manger': 'Manager', 'Hanlder': 'Handler', 'Contoller': 'Controller', 'Proccess': 'Process', 'Recieve': 'Receive', 'Occured': 'Occurred', 'Seperate': 'Separate', 'Enviroment': 'Environment', 'Paramter': 'Parameter', 'Reponse': 'Response'}

    def analyze_project(self) -> Dict[str, Any]:
        """Analisa todo o projeto em busca de mismatches"""
        print('🔍 INICIANDO ANÁLISE DE NAME MISMATCHES')
        print('=' * 70)
        self._collect_all_definitions()
        self._analyze_imports()
        self._detect_naming_patterns()
        self._find_mismatches()
        return self._generate_report()

    def _collect_all_definitions(self):
        """Coleta todas as definições (classes, funções, etc)"""
        print('\n📊 Coletando definições...')
        for py_file in self.root_path.rglob('*.py'):
            if '__pycache__' in str(py_file):
                continue
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    tree = ast.parse(f.read(), filename=str(py_file))
                for node in ast.walk(tree):
                    if isinstance(node, ast.ClassDef):
                        self.name_registry['classes'].add(node.name)
                    elif isinstance(node, ast.FunctionDef):
                        self.name_registry['functions'].add(node.name)
                    elif isinstance(node, ast.Name):
                        self.name_registry['variables'].add(node.id)
            except Exception as e:
                print(f'   ⚠️ Erro ao analisar {py_file}: {e}')
        print(f"   ✅ Classes encontradas: {len(self.name_registry['classes'])}")
        print(f"   ✅ Funções encontradas: {len(self.name_registry['functions'])}")

    def _analyze_imports(self):
        """Analisa todos os imports do projeto"""
        print('\n🔗 Analisando imports...')
        import_errors = []
        for py_file in self.root_path.rglob('*.py'):
            if '__pycache__' in str(py_file):
                continue
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    tree = ast.parse(f.read(), filename=str(py_file))
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            self.import_graph[str(py_file)].add(alias.name)
                    elif isinstance(node, ast.ImportFrom):
                        if node.module:
                            self.import_graph[str(py_file)].add(node.module)
                        for alias in node.names:
                            imported_name = alias.name
                            if imported_name not in self.name_registry['classes'] and imported_name not in self.name_registry['functions']:
                                similar = self._find_similar_name(imported_name)
                                if similar:
                                    mismatch = NameMismatch(file_path=str(py_file), line_number=node.lineno, expected_name=similar[0], actual_name=imported_name, mismatch_type='import', confidence=similar[1], suggested_fix=f'from {node.module} import {similar[0]}', context=f'Importing from {node.module}')
                                    self.mismatches.append(mismatch)
                                    import_errors.append(mismatch)
            except Exception as e:
                print(f'   ⚠️ Erro ao analisar imports de {py_file}: {e}')
        print(f'   ✅ Arquivos analisados: {len(self.import_graph)}')
        print(f'   ⚠️  Import errors encontrados: {len(import_errors)}')

    def _find_similar_name(self, name: str) -> Optional[Tuple[str, float]]:
        """Encontra nome similar usando fuzzy matching"""
        all_names = list(self.name_registry['classes']) + list(self.name_registry['functions'])
        if not all_names:
            return None
        if HAS_FUZZY:
            result = process.extractOne(name, all_names, scorer=fuzz.ratio)
            if result and result[1] > 70:
                return (result[0], result[1])
        else:
            matches = difflib.get_close_matches(name, all_names, n=1, cutoff=0.7)
            if matches:
                ratio = difflib.SequenceMatcher(None, name, matches[0]).ratio()
                return (matches[0], ratio * 100)
        if name in self.common_typos:
            correct = self.common_typos[name]
            if correct in all_names:
                return (correct, 95.0)
        return None

    def _detect_naming_patterns(self):
        """Detecta padrões de nomenclatura"""
        print('\n🎯 Detectando padrões de nomenclatura...')
        patterns = {'CamelCase': re.compile('^[A-Z][a-z]+(?:[A-Z][a-z]+)*$'), 'PascalCase': re.compile('^[A-Z][a-zA-Z0-9]*$'), 'snake_case': re.compile('^[a-z]+(?:_[a-z]+)*$'), 'UPPER_SNAKE': re.compile('^[A-Z]+(?:_[A-Z]+)*$')}
        for pattern_name, pattern_re in patterns.items():
            self.pattern_stats[pattern_name] = NamePattern(pattern_type=pattern_name)
            for name_type, names in self.name_registry.items():
                for name in names:
                    if pattern_re.match(name):
                        self.pattern_stats[pattern_name].examples.append(name)
                        self.pattern_stats[pattern_name].frequency += 1
        for pattern_name, stats in sorted(self.pattern_stats.items(), key=lambda x: x[1].frequency, reverse=True):
            if stats.frequency > 0:
                print(f'   • {pattern_name}: {stats.frequency} ocorrências')

    def _find_mismatches(self):
        """Encontra todos os mismatches"""
        print('\n🔎 Procurando mismatches específicos...')
        specific_patterns = [('DigionProducerMon(?!Orchestrator)', 'DigionProducerMon'), ('DigionProducerMonOrchestrator', 'DigionProducerMonOrchestrator'), ('from (\\w+) import (\\w+)', self._check_import_mismatch)]
        for py_file in self.root_path.rglob('*.py'):
            if '__pycache__' in str(py_file):
                continue
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    lines = content.split('\n')
                for i, line in enumerate(lines, 1):
                    for pattern, replacement in specific_patterns[:2]:
                        if re.search(pattern, line):
                            mismatch = NameMismatch(file_path=str(py_file), line_number=i, expected_name=replacement, actual_name=re.search(pattern, line).group(), mismatch_type='naming_convention', confidence=100.0, suggested_fix=re.sub(pattern, replacement, line), context=line.strip())
                            self.mismatches.append(mismatch)
            except Exception as e:
                print(f'   ⚠️ Erro ao procurar mismatches em {py_file}: {e}')

    def _check_import_mismatch(self, match):
        """Verifica mismatches em imports"""
        module = match.group(1)
        name = match.group(2)
        similar = self._find_similar_name(name)
        if similar and similar[1] < 100:
            return f'from {module} import {similar[0]}'
        return None

    def _generate_report(self) -> Dict[str, Any]:
        """Gera relatório completo"""
        print('\n' + '=' * 70)
        print('📋 RELATÓRIO DE NAME MISMATCHES')
        print('=' * 70)
        by_type = defaultdict(list)
        for mismatch in self.mismatches:
            by_type[mismatch.mismatch_type].append(mismatch)
        report = {'total_mismatches': len(self.mismatches), 'by_type': {}, 'critical': [], 'suggestions': []}
        print(f'\n🔴 TOTAL DE MISMATCHES: {len(self.mismatches)}')
        for mtype, items in by_type.items():
            print(f'\n📍 {mtype.upper()} ({len(items)} casos):')
            report['by_type'][mtype] = len(items)
            for item in items[:5]:
                print(f'   • {item.file_path}:{item.line_number}')
                print(f'     {item.actual_name} → {item.expected_name}')
                if item.confidence > 90:
                    report['critical'].append({'file': item.file_path, 'line': item.line_number, 'fix': item.suggested_fix})
        print('\n🔧 CORREÇÕES SUGERIDAS:')
        for mismatch in sorted(self.mismatches, key=lambda x: x.confidence, reverse=True)[:10]:
            if mismatch.confidence > 85:
                suggestion = {'file': mismatch.file_path, 'line': mismatch.line_number, 'current': mismatch.actual_name, 'suggested': mismatch.expected_name, 'confidence': mismatch.confidence}
                report['suggestions'].append(suggestion)
                print(f'   • {mismatch.file_path}:{mismatch.line_number}')
                print(f"     Trocar '{mismatch.actual_name}' por '{mismatch.expected_name}'")
                print(f'     Confiança: {mismatch.confidence:.1f}%')
        return report

    def auto_fix(self, min_confidence: float=90.0, dry_run: bool=True):
        """Aplica correções automaticamente"""
        print('\n🔧 AUTO-FIX MODE')
        print('=' * 70)
        fixes_to_apply = [m for m in self.mismatches if m.confidence >= min_confidence]
        if dry_run:
            print(f'\n🔍 DRY RUN - {len(fixes_to_apply)} correções seriam aplicadas:')
            for fix in fixes_to_apply:
                print(f'   • {fix.file_path}:{fix.line_number}')
                print(f'     {fix.actual_name} → {fix.expected_name}')
        else:
            print(f'\n✅ Aplicando {len(fixes_to_apply)} correções...')
            by_file = defaultdict(list)
            for fix in fixes_to_apply:
                by_file[fix.file_path].append(fix)
            for file_path, fixes in by_file.items():
                try:
                    with open(file_path, 'r') as f:
                        lines = f.readlines()
                    for fix in sorted(fixes, key=lambda x: x.line_number, reverse=True):
                        line_idx = fix.line_number - 1
                        if line_idx < len(lines):
                            old_line = lines[line_idx]
                            new_line = old_line.replace(fix.actual_name, fix.expected_name)
                            lines[line_idx] = new_line
                    with open(file_path, 'w') as f:
                        f.writelines(lines)
                    print(f'   ✅ {file_path}: {len(fixes)} correções aplicadas')
                except Exception as e:
                    print(f'   ❌ Erro ao corrigir {file_path}: {e}')
        print('\n' + '=' * 70)
        print('🏁 AUTO-FIX COMPLETO')
        print('=' * 70)

def main():
    """Função principal"""
    debugger = NameMismatchDebugger(root_path='/Users/clubproducoes/Digimundo/scripturemon-champion')
    report = debugger.analyze_project()
    report_path = Path('name_mismatch_report.json')
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2)
    print(f'\n📄 Relatório salvo em: {report_path}')
    if report['total_mismatches'] > 0:
        print('\n❓ Deseja aplicar correções automáticas? (s/n): ', end='')
        response = input().lower()
        if response == 's':
            print('\n❓ Modo dry-run primeiro? (s/n): ', end='')
            dry_run = input().lower() == 's'
            debugger.auto_fix(min_confidence=90.0, dry_run=dry_run)
            if dry_run:
                print('\n❓ Aplicar correções agora? (s/n): ', end='')
                if input().lower() == 's':
                    debugger.auto_fix(min_confidence=90.0, dry_run=False)
if __name__ == '__main__':
    main()