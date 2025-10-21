"""
🚀 INTEGRATED VALIDATION SYSTEM
================================
Sistema integrado de validação Silicon Valley-grade
Combina todas as ferramentas de validação e correção automática
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from ast_based_refactoring import ASTRefactoringSystem
from import_dependency_manager import ImportDependencyManager
from async_await_validator import AsyncAwaitValidator
from precommit_validation_hooks import PreCommitValidationHooks
from ultimate_mismatch_symbiosis import UltimateMismatchSymbiosis, SymbiosisMode
import asyncio
import time
from typing import Dict, List, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum, auto
import json

class ValidationLevel(Enum):
    """Níveis de validação"""
    LIGHT = auto()
    STANDARD = auto()
    DEEP = auto()
    MAXIMUM = auto()

@dataclass
class IntegratedReport:
    """Relatório integrado de validação"""
    timestamp: float
    level: ValidationLevel
    total_files_analyzed: int
    total_issues_found: int
    total_issues_fixed: int
    constructor_issues: Dict[str, Any] = field(default_factory=dict)
    import_issues: Dict[str, Any] = field(default_factory=dict)
    async_issues: Dict[str, Any] = field(default_factory=dict)
    mismatch_issues: Dict[str, Any] = field(default_factory=dict)
    validation_hooks: Dict[str, Any] = field(default_factory=dict)
    harmony_score: float = 0.0
    recommendations: List[str] = field(default_factory=list)

class IntegratedValidationSystem:
    """Sistema integrado de validação e correção automática"""

    def __init__(self, project_root: Path=None):
        self.project_root = project_root or Path('/Users/clubproducoes/Digimundo/scripturemon-champion')
        self.ast_refactoring = ASTRefactoringSystem(self.project_root)
        self.import_manager = ImportDependencyManager(self.project_root)
        self.async_validator = AsyncAwaitValidator(self.project_root)
        self.precommit_hooks = PreCommitValidationHooks(self.project_root)
        self.mismatch_symbiosis = UltimateMismatchSymbiosis(self.project_root, mode=SymbiosisMode.SYMBIOTIC)
        self.stats = {'total_runs': 0, 'total_fixes': 0, 'total_time': 0.0}

    def run_integrated_validation(self, level: ValidationLevel=ValidationLevel.STANDARD, auto_fix: bool=True, generate_report: bool=True) -> IntegratedReport:
        """Executa validação integrada completa"""
        print('\n🚀 INTEGRATED VALIDATION SYSTEM')
        print('=' * 60)
        print(f'  Level: {level.name}')
        print(f"  Auto-fix: {('ENABLED' if auto_fix else 'DISABLED')}")
        print(f'  Project: {self.project_root}')
        print('=' * 60)
        start_time = time.time()
        report = IntegratedReport(timestamp=start_time, level=level, total_files_analyzed=0, total_issues_found=0, total_issues_fixed=0)
        if level in [ValidationLevel.STANDARD, ValidationLevel.DEEP, ValidationLevel.MAXIMUM]:
            print('\n📍 PHASE 1: AST-BASED CONSTRUCTOR VALIDATION')
            constructor_results = self._validate_constructors(auto_fix)
            report.constructor_issues = constructor_results
            report.total_issues_found += constructor_results.get('issues_found', 0)
            report.total_issues_fixed += constructor_results.get('issues_fixed', 0)
        if level in [ValidationLevel.STANDARD, ValidationLevel.DEEP, ValidationLevel.MAXIMUM]:
            print('\n📍 PHASE 2: IMPORT DEPENDENCY ANALYSIS')
            import_results = self._validate_imports(auto_fix)
            report.import_issues = import_results
            report.total_issues_found += import_results.get('issues_found', 0)
            report.total_issues_fixed += import_results.get('issues_fixed', 0)
        if level in [ValidationLevel.DEEP, ValidationLevel.MAXIMUM]:
            print('\n📍 PHASE 3: ASYNC/AWAIT PATTERN VALIDATION')
            async_results = self._validate_async_patterns(auto_fix)
            report.async_issues = async_results
            report.total_issues_found += async_results.get('issues_found', 0)
            report.total_issues_fixed += async_results.get('issues_fixed', 0)
        if level == ValidationLevel.MAXIMUM:
            print('\n📍 PHASE 4: NAME MISMATCH DETECTION (SYMBIOSIS)')
            mismatch_results = self._validate_mismatches(auto_fix)
            report.mismatch_issues = mismatch_results
            report.total_issues_found += mismatch_results.get('issues_found', 0)
            report.total_issues_fixed += mismatch_results.get('issues_fixed', 0)
        if level in [ValidationLevel.DEEP, ValidationLevel.MAXIMUM]:
            print('\n📍 PHASE 5: PRE-COMMIT VALIDATION HOOKS')
            hooks_results = self._run_precommit_hooks()
            report.validation_hooks = hooks_results
        report.harmony_score = self._calculate_harmony_score(report)
        report.recommendations = self._generate_recommendations(report)
        self.stats['total_runs'] += 1
        self.stats['total_fixes'] += report.total_issues_fixed
        self.stats['total_time'] += time.time() - start_time
        self._print_summary(report)
        if generate_report:
            self._save_report(report)
        return report

    def _validate_constructors(self, auto_fix: bool) -> Dict[str, Any]:
        """Valida e corrige construtores"""
        results = {'issues_found': 0, 'issues_fixed': 0, 'files_processed': 0}
        try:
            for py_file in self.project_root.rglob('*.py'):
                if '.bak' not in str(py_file) and '__pycache__' not in str(py_file):
                    success, fixes = self.ast_refactoring.process_file(py_file)
                    results['files_processed'] += 1
                    if fixes > 0:
                        results['issues_found'] += fixes
                        if auto_fix and success:
                            results['issues_fixed'] += fixes
            print(f"  ✅ Processed {results['files_processed']} files")
            print(f"  Found {results['issues_found']} constructor issues")
            if auto_fix:
                print(f"  Fixed {results['issues_fixed']} issues")
        except Exception as e:
            print(f'  ❌ Error: {e}')
        return results

    def _validate_imports(self, auto_fix: bool) -> Dict[str, Any]:
        """Valida e corrige imports"""
        results = {'issues_found': 0, 'issues_fixed': 0, 'circular_dependencies': 0, 'broken_imports': 0}
        try:
            report = self.import_manager.analyze_project()
            results['circular_dependencies'] = report['stats']['circular_deps_found']
            results['broken_imports'] = report['stats']['broken_imports_found']
            results['issues_found'] = results['circular_dependencies'] + results['broken_imports']
            if auto_fix and results['broken_imports'] > 0:
                fixed = self.import_manager.auto_fix_imports(dry_run=False)
                results['issues_fixed'] = fixed
            print(f"  ✅ Analyzed {report['stats']['modules_analyzed']} modules")
            print(f"  Found {results['circular_dependencies']} circular dependencies")
            print(f"  Found {results['broken_imports']} broken imports")
            if auto_fix:
                print(f"  Fixed {results['issues_fixed']} imports")
        except Exception as e:
            print(f'  ❌ Error: {e}')
        return results

    def _validate_async_patterns(self, auto_fix: bool) -> Dict[str, Any]:
        """Valida padrões async/await"""
        results = {'issues_found': 0, 'issues_fixed': 0, 'async_without_await': 0, 'await_without_async': 0, 'blocking_in_async': 0}
        try:
            report = self.async_validator.validate_project()
            results['async_without_await'] = report['stats']['async_without_await']
            results['await_without_async'] = report['stats']['await_without_async']
            results['blocking_in_async'] = report['stats']['blocking_calls_in_async']
            results['issues_found'] = len(self.async_validator.issues)
            if auto_fix and report['fixable_issues'] > 0:
                fixed = self.async_validator.auto_fix_issues(dry_run=False)
                results['issues_fixed'] = fixed
            print(f"  ✅ Analyzed {report['stats']['total_functions']} functions")
            print(f"  Found {results['async_without_await']} async without await")
            print(f"  Found {results['await_without_async']} await without async")
            print(f"  Found {results['blocking_in_async']} blocking calls")
            if auto_fix:
                print(f"  Fixed {results['issues_fixed']} issues")
        except Exception as e:
            print(f'  ❌ Error: {e}')
        return results

    def _validate_mismatches(self, auto_fix: bool) -> Dict[str, Any]:
        """Valida e corrige name mismatches"""
        results = {'issues_found': 0, 'issues_fixed': 0, 'detection_methods': []}
        try:
            report = self.mismatch_symbiosis.analyze()
            results['issues_found'] = report['total_mismatches']
            results['detection_methods'] = list(report['detection_methods'].keys())
            if auto_fix and report['total_mismatches'] > 0:
                fixes = self.mismatch_symbiosis.fix_all(dry_run=False)
                results['issues_fixed'] = fixes['successful_fixes']
            print(f"  ✅ Symbiosis mode: {report['mode']}")
            print(f"  Found {results['issues_found']} mismatches")
            print(f"  Detection methods: {', '.join(results['detection_methods'])}")
            if auto_fix:
                print(f"  Fixed {results['issues_fixed']} mismatches")
        except Exception as e:
            print(f'  ❌ Error: {e}')
        return results

    def _run_precommit_hooks(self) -> Dict[str, Any]:
        """Executa hooks de pré-commit"""
        results = {'validators_run': 0, 'passed': 0, 'warnings': 0, 'failed': 0}
        try:
            success, report = self.precommit_hooks.run_all_validations()
            results['validators_run'] = report['summary']['total_validators']
            results['passed'] = report['summary']['passed']
            results['warnings'] = report['summary']['warnings']
            results['failed'] = report['summary']['failed']
            print(f"  ✅ Ran {results['validators_run']} validators")
            print(f"  Passed: {results['passed']}, Warnings: {results['warnings']}, Failed: {results['failed']}")
            if not (self.project_root / '.git' / 'hooks' / 'pre-commit').exists():
                if self.precommit_hooks.install_git_hook():
                    print(f'  ✅ Git pre-commit hook installed')
        except Exception as e:
            print(f'  ❌ Error: {e}')
        return results

    def _calculate_harmony_score(self, report: IntegratedReport) -> float:
        """Calcula score de harmonia do sistema"""
        if report.total_issues_found == 0:
            return 100.0
        fix_rate = report.total_issues_fixed / report.total_issues_found
        weights = {'constructor': 0.3, 'import': 0.25, 'async': 0.2, 'mismatch': 0.15, 'hooks': 0.1}
        score = fix_rate * 100.0
        if report.constructor_issues.get('issues_found', 0) > report.constructor_issues.get('issues_fixed', 0):
            score *= 0.9
        if report.import_issues.get('circular_dependencies', 0) > 0:
            score *= 0.95
        if report.async_issues.get('blocking_in_async', 0) > 0:
            score *= 0.97
        return min(100.0, max(0.0, score))

    def _generate_recommendations(self, report: IntegratedReport) -> List[str]:
        """Gera recomendações baseadas no relatório"""
        recommendations = []
        if report.constructor_issues.get('issues_found', 0) > report.constructor_issues.get('issues_fixed', 0):
            recommendations.append('⚠️ Manual review needed for remaining constructor issues')
        if report.import_issues.get('circular_dependencies', 0) > 0:
            recommendations.append('🔄 Refactor code to eliminate circular dependencies')
        if report.async_issues.get('blocking_in_async', 0) > 0:
            recommendations.append('⚡ Replace blocking calls with async alternatives')
        if report.mismatch_issues.get('issues_found', 0) > report.mismatch_issues.get('issues_fixed', 0):
            recommendations.append('📝 Review and fix remaining name mismatches manually')
        if report.harmony_score < 80:
            recommendations.append('🎯 Consider running MAXIMUM level validation for better results')
        elif report.harmony_score >= 95:
            recommendations.append('✅ System harmony is excellent! Ready for production')
        return recommendations

    def _print_summary(self, report: IntegratedReport):
        """Imprime resumo do relatório"""
        print('\n' + '=' * 60)
        print('📊 INTEGRATED VALIDATION SUMMARY')
        print('=' * 60)
        print(f'  Total Issues Found:  {report.total_issues_found}')
        print(f'  Total Issues Fixed:  {report.total_issues_fixed}')
        print(f'  Harmony Score:       {report.harmony_score:.1f}%')
        if report.recommendations:
            print('\n📋 RECOMMENDATIONS:')
            for rec in report.recommendations:
                print(f'  {rec}')

    def _save_report(self, report: IntegratedReport):
        """Salva relatório em arquivo"""
        report_path = self.project_root / 'integrated_validation_report.json'
        report_data = {'timestamp': report.timestamp, 'level': report.level.name, 'total_files_analyzed': report.total_files_analyzed, 'total_issues_found': report.total_issues_found, 'total_issues_fixed': report.total_issues_fixed, 'constructor_issues': report.constructor_issues, 'import_issues': report.import_issues, 'async_issues': report.async_issues, 'mismatch_issues': report.mismatch_issues, 'validation_hooks': report.validation_hooks, 'harmony_score': report.harmony_score, 'recommendations': report.recommendations}
        with open(report_path, 'w') as f:
            json.dump(report_data, f, indent=2)
        print(f'\n💾 Report saved to: {report_path}')

async def test_integrated_system():
    """Testa o sistema integrado"""
    print('\n🧪 TESTING INTEGRATED VALIDATION SYSTEM')
    print('=' * 80)
    system = IntegratedValidationSystem()
    report = await system.run_integrated_validation(level=ValidationLevel.STANDARD, auto_fix=True, generate_report=True)
    print('\n✅ INTEGRATED VALIDATION COMPLETE')
    print(f'   Harmony Score: {report.harmony_score:.1f}%')
    print(f'   Total Fixes Applied: {report.total_issues_fixed}')
    return report
if __name__ == '__main__':
    asyncio.run(test_integrated_system())