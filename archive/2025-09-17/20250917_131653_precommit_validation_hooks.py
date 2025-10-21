"""
🎯 PRE-COMMIT VALIDATION HOOKS
==============================
Sistema de validação pré-commit para prevenir erros
Integra todas as ferramentas de validação antes do commit
"""
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, field
import json
import time
import hashlib
from enum import Enum, auto
from ast_based_refactoring import ASTRefactoringSystem as ASTRefactoring
from import_dependency_manager import ImportDependencyManager
from async_await_validator import AsyncAwaitValidator

class ValidationStatus(Enum):
    """Status da validação"""
    PASSED = auto()
    WARNING = auto()
    FAILED = auto()
    SKIPPED = auto()

@dataclass
class ValidationResult:
    """Resultado de uma validação"""
    validator_name: str
    status: ValidationStatus
    message: str
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    auto_fixed: int = 0
    execution_time: float = 0.0

@dataclass
class HookConfig:
    """Configuração dos hooks"""
    enable_auto_fix: bool = True
    fail_on_warnings: bool = False
    validators: List[str] = field(default_factory=lambda: ['syntax', 'constructors', 'imports', 'async_await', 'naming', 'memory_systems'])
    excluded_paths: List[str] = field(default_factory=lambda: ['__pycache__', '.git', '.venv', 'venv', 'node_modules', '*.bak', '*.pyc', '*.pyo', '.DS_Store'])
    max_file_size_mb: int = 10
    parallel_validation: bool = True
    cache_validation_results: bool = True

class PreCommitValidationHooks:
    """Sistema de hooks de validação pré-commit"""

    def __init__(self, project_root: Path=None):
        self.project_root = project_root or Path.cwd()
        self.config = HookConfig()
        self.results: List[ValidationResult] = []
        self.cache_dir = self.project_root / '.validation_cache'
        self.cache_dir.mkdir(exist_ok=True)
        self.validators = {'syntax': self._validate_syntax, 'constructors': self._validate_constructors, 'imports': self._validate_imports, 'async_await': self._validate_async_await, 'naming': self._validate_naming, 'memory_systems': self._validate_memory_systems}

    def run_all_validations(self, files: List[Path]=None) -> Tuple[bool, Dict[str, Any]]:
        """Executa todas as validações"""
        print('\n🎯 RUNNING PRE-COMMIT VALIDATIONS')
        print('=' * 60)
        start_time = time.time()
        if files is None:
            files = self._get_staged_files()
        if not files:
            print('  ℹ️ No files to validate')
            return (True, {'status': 'no_files'})
        print(f'  📁 Validating {len(files)} files')
        for validator_name in self.config.validators:
            if validator_name in self.validators:
                result = self._run_validator(validator_name, files)
                self.results.append(result)
        report = self._generate_report()
        has_errors = any((r.status == ValidationStatus.FAILED for r in self.results))
        has_warnings = any((r.status == ValidationStatus.WARNING for r in self.results))
        success = not has_errors
        if self.config.fail_on_warnings:
            success = success and (not has_warnings)
        execution_time = time.time() - start_time
        report['execution_time'] = execution_time
        self._print_summary(report, success)
        return (success, report)

    def _get_staged_files(self) -> List[Path]:
        """Obtém arquivos staged para commit"""
        try:
            result = subprocess.run(['git', 'diff', '--cached', '--name-only'], capture_output=True, text=True, cwd=self.project_root)
            if result.returncode == 0:
                files = []
                for line in result.stdout.strip().split('\n'):
                    if line and line.endswith('.py'):
                        file_path = self.project_root / line
                        if file_path.exists():
                            files.append(file_path)
                return files
        except:
            pass
        return list(self.project_root.rglob('*.py'))

    def _run_validator(self, name: str, files: List[Path]) -> ValidationResult:
        """Executa um validador"""
        print(f'\n  🔍 Running {name} validator...')
        start_time = time.time()
        validator_func = self.validators[name]
        try:
            result = validator_func(files)
            result.execution_time = time.time() - start_time
            status_icon = {ValidationStatus.PASSED: '✅', ValidationStatus.WARNING: '⚠️', ValidationStatus.FAILED: '❌', ValidationStatus.SKIPPED: '⏭️'}[result.status]
            print(f'     {status_icon} {result.message}')
            if result.auto_fixed > 0:
                print(f'     🔧 Auto-fixed {result.auto_fixed} issues')
            return result
        except Exception as e:
            return ValidationResult(validator_name=name, status=ValidationStatus.FAILED, message=f'Validator crashed: {e}', errors=[str(e)], execution_time=time.time() - start_time)

    def _validate_syntax(self, files: List[Path]) -> ValidationResult:
        """Valida sintaxe Python"""
        errors = []
        for file_path in files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    compile(f.read(), str(file_path), 'exec')
            except SyntaxError as e:
                errors.append(f'{file_path.name}:{e.lineno}: {e.msg}')
        if errors:
            return ValidationResult(validator_name='syntax', status=ValidationStatus.FAILED, message=f'Found {len(errors)} syntax errors', errors=errors[:10])
        return ValidationResult(validator_name='syntax', status=ValidationStatus.PASSED, message=f'All {len(files)} files have valid syntax')

    def _validate_constructors(self, files: List[Path]) -> ValidationResult:
        """Valida construtores usando AST"""
        refactoring = ASTRefactoring(self.project_root)
        total_issues = 0
        for file_path in files:
            success, fixes = refactoring.process_file(file_path)
            if not success and fixes > 0:
                total_issues += fixes
        if total_issues > 0:
            if self.config.enable_auto_fix:
                fixed = refactoring.fix_constructors(dry_run=False)
                if fixed > 0:
                    return ValidationResult(validator_name='constructors', status=ValidationStatus.WARNING, message=f'Fixed {fixed}/{total_issues} constructor issues', warnings=[f'Auto-fixed {fixed} constructor issues'], auto_fixed=fixed)
                else:
                    return ValidationResult(validator_name='constructors', status=ValidationStatus.FAILED, message=f'Found {total_issues} constructor issues', errors=[f'{total_issues} constructor issues need manual fix'])
            else:
                return ValidationResult(validator_name='constructors', status=ValidationStatus.FAILED, message=f'Found {total_issues} constructor issues', errors=[f'Constructors need fixing: __init__ found'])
        return ValidationResult(validator_name='constructors', status=ValidationStatus.PASSED, message='All constructors are valid')

    def _validate_imports(self, files: List[Path]) -> ValidationResult:
        """Valida imports e dependências"""
        manager = ImportDependencyManager(self.project_root)
        broken_count = 0
        circular_count = 0
        for file_path in files:
            module_info = manager._analyze_module(file_path)
            if module_info:
                for imp in module_info.imports:
                    resolved = manager._resolve_import(module_info.name, imp.module)
                    if not manager._is_standard_or_third_party(imp.module):
                        if resolved not in manager.module_map:
                            broken_count += 1
        manager._build_dependency_graph()
        manager._find_circular_dependencies()
        circular_count = len(manager.circular_dependencies)
        if broken_count > 0 or circular_count > 0:
            errors = []
            if broken_count > 0:
                errors.append(f'{broken_count} broken imports')
            if circular_count > 0:
                errors.append(f'{circular_count} circular dependencies')
            if self.config.enable_auto_fix and broken_count > 0:
                fixed = manager.auto_fix_imports(dry_run=False)
                if fixed > 0:
                    return ValidationResult(validator_name='imports', status=ValidationStatus.WARNING, message=f'Fixed {fixed} import issues', warnings=errors, auto_fixed=fixed)
            return ValidationResult(validator_name='imports', status=ValidationStatus.WARNING if circular_count > 0 else ValidationStatus.FAILED, message=f'Import issues detected', errors=errors if broken_count > 0 else [], warnings=errors if circular_count > 0 else [])
        return ValidationResult(validator_name='imports', status=ValidationStatus.PASSED, message='All imports are valid')

    def _validate_async_await(self, files: List[Path]) -> ValidationResult:
        """Valida padrões async/await"""
        validator = AsyncAwaitValidator(self.project_root)
        total_issues = 0
        for file_path in files:
            issues = validator._validate_file(file_path)
            total_issues += len(issues)
        if total_issues > 0:
            async_without_await = sum((1 for i in validator.issues if i.issue_type == 'async_without_await'))
            await_without_async = sum((1 for i in validator.issues if i.issue_type == 'await_without_async'))
            blocking_in_async = sum((1 for i in validator.issues if i.issue_type == 'blocking_in_async'))
            warnings = []
            errors = []
            if async_without_await > 0:
                warnings.append(f'{async_without_await} async functions without await')
            if await_without_async > 0:
                errors.append(f'{await_without_async} functions use await but not async')
            if blocking_in_async > 0:
                warnings.append(f'{blocking_in_async} blocking calls in async functions')
            if self.config.enable_auto_fix:
                fixed = validator.auto_fix_issues(dry_run=False)
                if fixed > 0:
                    return ValidationResult(validator_name='async_await', status=ValidationStatus.WARNING, message=f'Fixed {fixed} async/await issues', warnings=warnings, errors=errors, auto_fixed=fixed)
            status = ValidationStatus.FAILED if errors else ValidationStatus.WARNING
            return ValidationResult(validator_name='async_await', status=status, message=f'Found {total_issues} async/await issues', errors=errors, warnings=warnings)
        return ValidationResult(validator_name='async_await', status=ValidationStatus.PASSED, message='All async/await patterns are valid')

    def _validate_naming(self, files: List[Path]) -> ValidationResult:
        """Valida convenções de nomenclatura"""
        issues = []
        naming_patterns = {'class': '^[A-Z][a-zA-Z0-9]*$', 'function': '^[a-z_][a-z0-9_]*$', 'constant': '^[A-Z][A-Z0-9_]*$'}
        import ast
        import re
        for file_path in files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    tree = ast.parse(f.read())
                for node in ast.walk(tree):
                    if isinstance(node, ast.ClassDef):
                        if not re.match(naming_patterns['class'], node.name):
                            issues.append(f"Class '{node.name}' doesn't follow PascalCase")
                    elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        if not node.name.startswith('__'):
                            if not re.match(naming_patterns['function'], node.name):
                                issues.append(f"Function '{node.name}' doesn't follow snake_case")
            except:
                pass
        if issues:
            return ValidationResult(validator_name='naming', status=ValidationStatus.WARNING, message=f'Found {len(issues)} naming convention issues', warnings=issues[:10])
        return ValidationResult(validator_name='naming', status=ValidationStatus.PASSED, message='All names follow conventions')

    def _validate_memory_systems(self, files: List[Path]) -> ValidationResult:
        """Valida consistência dos sistemas de memória"""
        memory_classes = set()
        memory_issues = []
        import ast
        for file_path in files:
            if 'memory' not in str(file_path).lower():
                continue
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    tree = ast.parse(f.read())
                for node in ast.walk(tree):
                    if isinstance(node, ast.ClassDef):
                        memory_classes.add(node.name)
                        methods = {m.name for m in node.body if isinstance(m, ast.FunctionDef)}
                        required = {'store', 'retrieve', 'process'}
                        missing = required - methods
                        if missing:
                            memory_issues.append(f"{node.name} missing methods: {', '.join(missing)}")
            except:
                pass
        if memory_issues:
            return ValidationResult(validator_name='memory_systems', status=ValidationStatus.WARNING, message=f'Found {len(memory_issues)} memory system issues', warnings=memory_issues)
        return ValidationResult(validator_name='memory_systems', status=ValidationStatus.PASSED, message=f'All {len(memory_classes)} memory systems are consistent')

    def _generate_report(self) -> Dict[str, Any]:
        """Gera relatório de validação"""
        passed = sum((1 for r in self.results if r.status == ValidationStatus.PASSED))
        warnings = sum((1 for r in self.results if r.status == ValidationStatus.WARNING))
        failed = sum((1 for r in self.results if r.status == ValidationStatus.FAILED))
        auto_fixed = sum((r.auto_fixed for r in self.results))
        return {'summary': {'total_validators': len(self.results), 'passed': passed, 'warnings': warnings, 'failed': failed, 'auto_fixed': auto_fixed}, 'validators': [{'name': r.validator_name, 'status': r.status.name, 'message': r.message, 'errors': r.errors, 'warnings': r.warnings, 'auto_fixed': r.auto_fixed, 'execution_time': r.execution_time} for r in self.results]}

    def _print_summary(self, report: Dict[str, Any], success: bool):
        """Imprime resumo da validação"""
        print('\n' + '=' * 60)
        print('📊 VALIDATION SUMMARY')
        print('=' * 60)
        summary = report['summary']
        print(f"  ✅ Passed:     {summary['passed']}/{summary['total_validators']}")
        print(f"  ⚠️  Warnings:   {summary['warnings']}")
        print(f"  ❌ Failed:     {summary['failed']}")
        print(f"  🔧 Auto-fixed: {summary['auto_fixed']}")
        print(f"  ⏱️  Time:       {report['execution_time']:.2f}s")
        if success:
            print('\n✅ PRE-COMMIT VALIDATION PASSED')
        else:
            print('\n❌ PRE-COMMIT VALIDATION FAILED')
            print('  Please fix the issues before committing')

    def install_git_hook(self) -> bool:
        """Instala hook no git"""
        hook_path = self.project_root / '.git' / 'hooks' / 'pre-commit'
        hook_content = '#!/usr/bin/env python3\n"""Pre-commit hook for ScriptureMonChampion"""\n\nimport sys\nfrom pathlib import Path\n\n# Add project to path\nproject_root = Path(__file__).parent.parent.parent\nsys.path.insert(0, str(project_root))\n\nfrom precommit_validation_hooks import PreCommitValidationHooks\n\n# Run validations\nvalidator = PreCommitValidationHooks(project_root)\nsuccess, report = validator.run_all_validations()\n\n# Exit with appropriate code\nsys.exit(0 if success else 1)\n'
        try:
            hook_path.parent.mkdir(parents=True, exist_ok=True)
            hook_path.write_text(hook_content)
            hook_path.chmod(493)
            print(f'✅ Git pre-commit hook installed at {hook_path}')
            return True
        except Exception as e:
            print(f'❌ Failed to install git hook: {e}')
            return False

def test_precommit_hooks():
    """Testa os hooks de pré-commit"""
    print('\n🧪 TESTING PRE-COMMIT VALIDATION HOOKS')
    print('=' * 80)
    validator = PreCommitValidationHooks(Path('/Users/clubproducoes/Digimundo/scripturemon-champion'))
    test_files = [Path('/Users/clubproducoes/Digimundo/scripturemon-champion/ast_based_refactoring.py'), Path('/Users/clubproducoes/Digimundo/scripturemon-champion/import_dependency_manager.py'), Path('/Users/clubproducoes/Digimundo/scripturemon-champion/async_await_validator.py')]
    success, report = validator.run_all_validations(test_files)
    report_path = Path('/Users/clubproducoes/Digimundo/scripturemon-champion/validation_report.json')
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2)
    print(f'\n📄 Full report saved to {report_path}')
    return (success, report)
if __name__ == '__main__':
    test_precommit_hooks()