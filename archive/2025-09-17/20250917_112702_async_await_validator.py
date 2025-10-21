#!/usr/bin/env python3
"""
⚡ ASYNC/AWAIT VALIDATOR
========================
Valida e corrige contexto async/await
Detecta e corrige inconsistências de funções assíncronas
"""

import ast
import asyncio
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional, Any
from dataclasses import dataclass, field
import time


@dataclass
class AsyncIssue:
    """Problema relacionado a async/await"""
    file: Path
    line: int
    function_name: str
    issue_type: str  # 'async_without_await', 'await_without_async', 'blocking_in_async'
    severity: str  # 'error', 'warning', 'info'
    suggestion: str
    can_auto_fix: bool = False
    

@dataclass
class AsyncStats:
    """Estatísticas de análise async"""
    total_functions: int = 0
    async_functions: int = 0
    sync_functions: int = 0
    async_without_await: int = 0
    await_without_async: int = 0
    blocking_calls_in_async: int = 0
    auto_fixed: int = 0
    

class AsyncAwaitValidator:
    """Validador de contexto async/await"""
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.issues: List[AsyncIssue] = []
        self.stats = AsyncStats()
        self.blocking_functions = {
            'time.sleep', 'input', 'requests.get', 'requests.post',
            'urllib.request.urlopen', 'subprocess.run', 'subprocess.call',
            'os.system', 'socket.recv', 'socket.send'
        }
        
    def validate_project(self) -> Dict[str, Any]:
        """Valida todo o projeto"""
        print("\n⚡ VALIDATING ASYNC/AWAIT PATTERNS")
        print("="*60)
        
        for py_file in self.project_root.rglob("*.py"):
            if '.bak' in str(py_file) or '__pycache__' in str(py_file):
                continue
                
            self._validate_file(py_file)
        
        return self.get_report()
    
    def _validate_file(self, file_path: Path) -> List[AsyncIssue]:
        """Valida um arquivo Python"""
        file_issues = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content, filename=str(file_path))
            
            # Visit all functions
            for node in ast.walk(tree):
                if isinstance(node, ast.AsyncFunctionDef):
                    self.stats.total_functions += 1
                    self.stats.async_functions += 1
                    issues = self._validate_async_function(node, file_path)
                    file_issues.extend(issues)
                    
                elif isinstance(node, ast.FunctionDef):
                    self.stats.total_functions += 1
                    self.stats.sync_functions += 1
                    issues = self._validate_sync_function(node, file_path)
                    file_issues.extend(issues)
            
            self.issues.extend(file_issues)
            return file_issues
            
        except Exception as e:
            print(f"  ⚠️ Error validating {file_path}: {e}")
            return []
    
    def _validate_async_function(self, node: ast.AsyncFunctionDef, file_path: Path) -> List[AsyncIssue]:
        """Valida função assíncrona"""
        issues = []
        
        # Check if function uses await
        has_await = self._has_await(node)
        
        if not has_await:
            issue = AsyncIssue(
                file=file_path,
                line=node.lineno,
                function_name=node.name,
                issue_type='async_without_await',
                severity='warning',
                suggestion=f"Function '{node.name}' is async but doesn't use await. Consider making it sync.",
                can_auto_fix=True
            )
            issues.append(issue)
            self.stats.async_without_await += 1
        
        # Check for blocking calls
        blocking_calls = self._find_blocking_calls(node)
        for call_name, line in blocking_calls:
            issue = AsyncIssue(
                file=file_path,
                line=line,
                function_name=node.name,
                issue_type='blocking_in_async',
                severity='warning',
                suggestion=f"Blocking call '{call_name}' in async function. Use async alternative.",
                can_auto_fix=False
            )
            issues.append(issue)
            self.stats.blocking_calls_in_async += 1
        
        return issues
    
    def _validate_sync_function(self, node: ast.FunctionDef, file_path: Path) -> List[AsyncIssue]:
        """Valida função síncrona"""
        issues = []
        
        # Check if function uses await
        has_await = self._has_await(node)
        
        if has_await:
            issue = AsyncIssue(
                file=file_path,
                line=node.lineno,
                function_name=node.name,
                issue_type='await_without_async',
                severity='error',
                suggestion=f"Function '{node.name}' uses await but is not async. Add 'async' keyword.",
                can_auto_fix=True
            )
            issues.append(issue)
            self.stats.await_without_async += 1
        
        return issues
    
    def _has_await(self, node: ast.AST) -> bool:
        """Verifica se nó contém await"""
        for child in ast.walk(node):
            if isinstance(child, ast.Await):
                return True
            # Also check for async for/with
            if isinstance(child, (ast.AsyncFor, ast.AsyncWith)):
                return True
        return False
    
    def _find_blocking_calls(self, node: ast.AST) -> List[Tuple[str, int]]:
        """Encontra chamadas bloqueantes em função async"""
        blocking = []
        
        for child in ast.walk(node):
            if isinstance(child, ast.Call):
                call_name = self._get_call_name(child)
                if call_name in self.blocking_functions:
                    blocking.append((call_name, child.lineno))
        
        return blocking
    
    def _get_call_name(self, node: ast.Call) -> str:
        """Extrai nome da chamada de função"""
        if isinstance(node.func, ast.Name):
            return node.func.id
        elif isinstance(node.func, ast.Attribute):
            parts = []
            current = node.func
            while isinstance(current, ast.Attribute):
                parts.append(current.attr)
                current = current.value
            if isinstance(current, ast.Name):
                parts.append(current.id)
            return '.'.join(reversed(parts))
        return ''
    
    def auto_fix_issues(self, dry_run: bool = True) -> int:
        """Corrige problemas automaticamente"""
        if dry_run:
            print("\n🔧 AUTO-FIX PREVIEW (dry run)")
        else:
            print("\n🔧 AUTO-FIXING ASYNC/AWAIT ISSUES")
        print("="*60)
        
        fixes_applied = 0
        files_to_fix = {}
        
        # Group issues by file
        for issue in self.issues:
            if issue.can_auto_fix:
                if issue.file not in files_to_fix:
                    files_to_fix[issue.file] = []
                files_to_fix[issue.file].append(issue)
        
        # Apply fixes
        for file_path, issues in files_to_fix.items():
            if dry_run:
                print(f"  Would fix {len(issues)} issues in {file_path.name}")
                fixes_applied += len(issues)
            else:
                fixed = self._apply_fixes_to_file(file_path, issues)
                if fixed:
                    fixes_applied += len(issues)
                    print(f"  ✅ Fixed {len(issues)} issues in {file_path.name}")
        
        self.stats.auto_fixed = fixes_applied
        return fixes_applied
    
    def _apply_fixes_to_file(self, file_path: Path, issues: List[AsyncIssue]) -> bool:
        """Aplica correções em um arquivo"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content, filename=str(file_path))
            
            # Apply transformations
            transformer = AsyncTransformer(issues)
            new_tree = transformer.visit(tree)
            
            # Generate new code
            new_code = ast.unparse(new_tree)
            
            # Backup and write
            backup_path = file_path.with_suffix('.py.async_bak')
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_code)
            
            return True
            
        except Exception as e:
            print(f"  ❌ Error fixing {file_path}: {e}")
            return False
    
    def get_report(self) -> Dict[str, Any]:
        """Gera relatório de validação"""
        return {
            'stats': {
                'total_functions': self.stats.total_functions,
                'async_functions': self.stats.async_functions,
                'sync_functions': self.stats.sync_functions,
                'async_without_await': self.stats.async_without_await,
                'await_without_async': self.stats.await_without_async,
                'blocking_calls_in_async': self.stats.blocking_calls_in_async,
                'auto_fixed': self.stats.auto_fixed
            },
            'issues': [
                {
                    'file': str(issue.file),
                    'line': issue.line,
                    'function': issue.function_name,
                    'type': issue.issue_type,
                    'severity': issue.severity,
                    'suggestion': issue.suggestion
                }
                for issue in self.issues[:10]  # First 10 issues
            ],
            'total_issues': len(self.issues),
            'fixable_issues': sum(1 for i in self.issues if i.can_auto_fix)
        }


class AsyncTransformer(ast.NodeTransformer):
    """Transforma AST para corrigir problemas async/await"""
    
    def __init__(self, issues: List[AsyncIssue]):
        self.issues = issues
        self.issues_by_line = {i.line: i for i in issues}
    
    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        """Visita função async"""
        self.generic_visit(node)
        
        # Check if should convert to sync
        if node.lineno in self.issues_by_line:
            issue = self.issues_by_line[node.lineno]
            if issue.issue_type == 'async_without_await':
                # Convert to sync function
                return ast.FunctionDef(
                    name=node.name,
                    args=node.args,
                    body=node.body,
                    decorator_list=node.decorator_list,
                    returns=node.returns,
                    lineno=node.lineno,
                    col_offset=node.col_offset
                )
        
        return node
    
    def visit_FunctionDef(self, node: ast.FunctionDef):
        """Visita função sync"""
        self.generic_visit(node)
        
        # Check if should convert to async
        if node.lineno in self.issues_by_line:
            issue = self.issues_by_line[node.lineno]
            if issue.issue_type == 'await_without_async':
                # Convert to async function
                return ast.AsyncFunctionDef(
                    name=node.name,
                    args=node.args,
                    body=node.body,
                    decorator_list=node.decorator_list,
                    returns=node.returns,
                    lineno=node.lineno,
                    col_offset=node.col_offset
                )
        
        return node


def test_async_validator():
    """Testa o Async/Await Validator"""
    print("\n🧪 TESTING ASYNC/AWAIT VALIDATOR")
    print("="*80)
    
    validator = AsyncAwaitValidator(
        Path("/Users/clubproducoes/Digimundo/scripturemon-champion")
    )
    
    # Validate project
    report = validator.validate_project()
    
    # Print report
    print("\n📊 VALIDATION REPORT:")
    print(f"  • Total functions: {report['stats']['total_functions']}")
    print(f"  • Async functions: {report['stats']['async_functions']}")
    print(f"  • Sync functions: {report['stats']['sync_functions']}")
    print(f"  • Async without await: {report['stats']['async_without_await']}")
    print(f"  • Await without async: {report['stats']['await_without_async']}")
    print(f"  • Blocking calls in async: {report['stats']['blocking_calls_in_async']}")
    
    # Test auto-fix
    print("\n🔧 Testing auto-fix...")
    fixable = validator.auto_fix_issues(dry_run=True)
    print(f"  Can auto-fix {fixable} issues")
    
    return report


if __name__ == "__main__":
    test_async_validator()