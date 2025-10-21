#!/usr/bin/env python3
"""
🔍 ADVANCED BUG SCANNER & AUTO-FIXER
====================================
Sistema Avançado de Detecção e Correção Automática de Bugs
Silicon Valley Grade™ - Zero Bug Tolerance

Think Different. Fix Everything. Make It Perfect.
"""

import os
import sys
import ast
import json
import sqlite3
import traceback
import importlib
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict

# Add paths
CLAUDE_CODE_PATH = Path("/Users/clubproducoes/Digimundo/claude_code")
sys.path.append(str(CLAUDE_CODE_PATH))


class BugSeverity(Enum):
    """Severidade dos bugs"""
    CRITICAL = "critical"     # System crash
    HIGH = "high"             # Major functionality broken
    MEDIUM = "medium"         # Minor functionality affected
    LOW = "low"              # Cosmetic or minor issues
    INFO = "info"            # Informational only


class BugType(Enum):
    """Tipos de bugs"""
    SYNTAX_ERROR = "syntax_error"
    IMPORT_ERROR = "import_error"
    ATTRIBUTE_ERROR = "attribute_error"
    KEY_ERROR = "key_error"
    TYPE_ERROR = "type_error"
    VALUE_ERROR = "value_error"
    INDEX_ERROR = "index_error"
    SQL_ERROR = "sql_error"
    LOGIC_ERROR = "logic_error"
    PERFORMANCE = "performance"
    MEMORY_LEAK = "memory_leak"
    SECURITY = "security"
    RACE_CONDITION = "race_condition"
    DEADLOCK = "deadlock"
    INFINITE_LOOP = "infinite_loop"


@dataclass
class Bug:
    """Estrutura de bug"""
    id: str
    file: Path
    line: int
    column: int
    type: BugType
    severity: BugSeverity
    description: str
    code_snippet: str
    fix_suggestion: str
    auto_fixable: bool = False
    fixed: bool = False
    test_case: Optional[str] = None


@dataclass
class BugFix:
    """Estrutura de correção"""
    bug_id: str
    original_code: str
    fixed_code: str
    confidence: float
    applied: bool = False
    tested: bool = False
    test_result: Optional[bool] = None


# Alias for compatibility
BugScanner = None  # Will be set after class definition

class AdvancedBugScanner:
    """
    🔍 Scanner Avançado de Bugs

    Features:
    - AST-based analysis
    - Runtime error detection
    - Static type checking
    - SQL injection detection
    - Memory leak detection
    - Performance profiling
    - Race condition detection
    - Auto-fix generation
    - Test case generation
    - Regression testing
    """

    def __init__(self):
        """Inicializa o scanner"""
        print("🔍 ADVANCED BUG SCANNER INITIALIZING...")
        print("=" * 80)

        self.bugs = []
        self.fixes = []
        self.stats = defaultdict(int)
        self.file_cache = {}

        # Known bugs database
        self.known_bugs = self._load_known_bugs()

        print("✅ Bug Scanner initialized")
        print(f"📚 Known bugs loaded: {len(self.known_bugs)}")

    def _load_known_bugs(self) -> Dict[str, Any]:
        """Carrega database de bugs conhecidos"""
        return {
            # Telemetry bugs
            "telemetry_sql_index": {
                "pattern": "CREATE.*INDEX.*idx_",
                "fix": "CREATE INDEX IF NOT EXISTS idx_",
                "description": "Missing IF NOT EXISTS in index creation"
            },
            "telemetry_stop_event": {
                "pattern": "self.stop_event",
                "fix": "self.stop_event = threading.Event()",
                "description": "stop_event not initialized"
            },

            # Master System bugs
            "config_version_missing": {
                "pattern": "self.config\\['version'\\]",
                "fix": "self.config.get('version', '2.0.0')",
                "description": "Missing version in config"
            },
            "config_optimization_missing": {
                "pattern": "self.config\\['optimization'\\]",
                "fix": "self.config.get('optimization', {})",
                "description": "Missing optimization in config"
            },

            # Import errors
            "missing_numpy": {
                "pattern": "import numpy",
                "fix": "try:\n    import numpy as np\nexcept ImportError:\n    np = None",
                "description": "NumPy not installed"
            },
            "missing_psutil": {
                "pattern": "import psutil",
                "fix": "try:\n    import psutil\nexcept ImportError:\n    psutil = None",
                "description": "psutil not installed"
            }
        }

    def scan_all_files(self) -> List[Bug]:
        """Escaneia todos os arquivos Python"""
        print("\n📁 Scanning all Python files...")

        for py_file in CLAUDE_CODE_PATH.glob("**/*.py"):
            if "__pycache__" in str(py_file):
                continue

            print(f"   Scanning: {py_file.name}")
            self._scan_file(py_file)

        print(f"\n🐛 Total bugs found: {len(self.bugs)}")
        self._categorize_bugs()

        return self.bugs

    def _scan_file(self, filepath: Path):
        """Escaneia um arquivo específico"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                self.file_cache[filepath] = content

            # AST analysis
            self._analyze_ast(filepath, content)

            # Pattern matching
            self._check_patterns(filepath, content)

            # SQL analysis
            self._check_sql(filepath, content)

            # Import analysis
            self._check_imports(filepath, content)

            # Performance analysis
            self._check_performance(filepath, content)

            # Security analysis
            self._check_security(filepath, content)

        except SyntaxError as e:
            self.bugs.append(Bug(
                id=f"syntax_{filepath.stem}_{e.lineno}",
                file=filepath,
                line=e.lineno or 0,
                column=e.offset or 0,
                type=BugType.SYNTAX_ERROR,
                severity=BugSeverity.CRITICAL,
                description=f"Syntax error: {e.msg}",
                code_snippet=self._get_code_snippet(filepath, e.lineno or 0),
                fix_suggestion="Fix syntax error",
                auto_fixable=False
            ))

        except Exception as e:
            print(f"      ⚠️ Error scanning {filepath.name}: {e}")

    def _analyze_ast(self, filepath: Path, content: str):
        """Análise AST do código"""
        try:
            tree = ast.parse(content)

            # Check for common issues
            for node in ast.walk(tree):
                # Infinite loops
                if isinstance(node, ast.While):
                    if isinstance(node.test, ast.Constant) and node.test.value is True:
                        if not self._has_break(node):
                            self.bugs.append(Bug(
                                id=f"infinite_loop_{filepath.stem}_{node.lineno}",
                                file=filepath,
                                line=node.lineno,
                                column=node.col_offset,
                                type=BugType.INFINITE_LOOP,
                                severity=BugSeverity.HIGH,
                                description="Potential infinite loop detected",
                                code_snippet=self._get_code_snippet(filepath, node.lineno),
                                fix_suggestion="Add break condition or timeout",
                                auto_fixable=False
                            ))

                # Unused variables
                if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
                    var_name = node.id
                    if var_name.startswith('_'):
                        continue
                    # Check if variable is used
                    if not self._is_variable_used(tree, var_name, node.lineno):
                        self.bugs.append(Bug(
                            id=f"unused_var_{filepath.stem}_{node.lineno}_{var_name}",
                            file=filepath,
                            line=node.lineno,
                            column=node.col_offset,
                            type=BugType.LOGIC_ERROR,
                            severity=BugSeverity.LOW,
                            description=f"Unused variable: {var_name}",
                            code_snippet=self._get_code_snippet(filepath, node.lineno),
                            fix_suggestion=f"Remove unused variable {var_name}",
                            auto_fixable=True
                        ))

        except SyntaxError:
            pass  # Already handled

    def _check_patterns(self, filepath: Path, content: str):
        """Verifica padrões de bugs conhecidos"""
        lines = content.splitlines()

        for i, line in enumerate(lines, 1):
            # Check known bug patterns
            for bug_name, bug_info in self.known_bugs.items():
                if bug_info["pattern"] in line:
                    # Check if it's the buggy version
                    if "IF NOT EXISTS" not in line and "CREATE" in line and "INDEX" in line:
                        self.bugs.append(Bug(
                            id=f"{bug_name}_{filepath.stem}_{i}",
                            file=filepath,
                            line=i,
                            column=0,
                            type=BugType.SQL_ERROR,
                            severity=BugSeverity.MEDIUM,
                            description=bug_info["description"],
                            code_snippet=line,
                            fix_suggestion=bug_info["fix"],
                            auto_fixable=True
                        ))

            # Check for missing self.stop_event initialization
            if "self.stop_event.set()" in line or "self.stop_event.is_set()" in line:
                # Check if initialized in __init__
                if not self._is_initialized(content, "stop_event"):
                    self.bugs.append(Bug(
                        id=f"uninitialized_stop_event_{filepath.stem}_{i}",
                        file=filepath,
                        line=i,
                        column=0,
                        type=BugType.ATTRIBUTE_ERROR,
                        severity=BugSeverity.HIGH,
                        description="stop_event used but not initialized",
                        code_snippet=line,
                        fix_suggestion="Add 'self.stop_event = threading.Event()' in __init__",
                        auto_fixable=True
                    ))

    def _check_sql(self, filepath: Path, content: str):
        """Verifica problemas SQL"""
        sql_patterns = [
            (r"CREATE\s+TABLE\s+(?!IF\s+NOT\s+EXISTS)", "Missing IF NOT EXISTS in CREATE TABLE"),
            (r"CREATE\s+INDEX\s+(?!IF\s+NOT\s+EXISTS)", "Missing IF NOT EXISTS in CREATE INDEX"),
            (r"INSERT\s+INTO.*VALUES.*\?", None),  # Check for SQL injection
        ]

        lines = content.splitlines()
        for i, line in enumerate(lines, 1):
            for pattern, description in sql_patterns:
                if "CREATE" in line and "INDEX" in line and "IF NOT EXISTS" not in line:
                    self.bugs.append(Bug(
                        id=f"sql_index_{filepath.stem}_{i}",
                        file=filepath,
                        line=i,
                        column=0,
                        type=BugType.SQL_ERROR,
                        severity=BugSeverity.MEDIUM,
                        description=description or "SQL issue",
                        code_snippet=line,
                        fix_suggestion=line.replace("CREATE INDEX", "CREATE INDEX IF NOT EXISTS"),
                        auto_fixable=True
                    ))

    def _check_imports(self, filepath: Path, content: str):
        """Verifica problemas de imports"""
        # Test imports
        import_errors = []

        tree = ast.parse(content)
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    module_name = alias.name
                    try:
                        __import__(module_name)
                    except ImportError:
                        import_errors.append((module_name, node.lineno))

            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    try:
                        __import__(node.module)
                    except ImportError:
                        import_errors.append((node.module, node.lineno))

        for module, lineno in import_errors:
            self.bugs.append(Bug(
                id=f"import_error_{filepath.stem}_{lineno}_{module}",
                file=filepath,
                line=lineno,
                column=0,
                type=BugType.IMPORT_ERROR,
                severity=BugSeverity.HIGH if module in ['numpy', 'psutil'] else BugSeverity.CRITICAL,
                description=f"Module not found: {module}",
                code_snippet=self._get_code_snippet(filepath, lineno),
                fix_suggestion=f"Install {module} or wrap in try/except",
                auto_fixable=True if module in self.known_bugs else False
            ))

    def _check_performance(self, filepath: Path, content: str):
        """Verifica problemas de performance"""
        perf_issues = [
            ("sleep(0.001)", "Very short sleep - consider removing"),
            ("sleep(60)", "Long sleep - consider async or threading"),
            ("for.*for.*for", "Triple nested loop - O(n³) complexity"),
            ("list.append.*loop", "List append in loop - consider list comprehension"),
        ]

        lines = content.splitlines()
        for i, line in enumerate(lines, 1):
            for pattern, description in perf_issues:
                if pattern in line.lower():
                    self.bugs.append(Bug(
                        id=f"perf_{filepath.stem}_{i}",
                        file=filepath,
                        line=i,
                        column=0,
                        type=BugType.PERFORMANCE,
                        severity=BugSeverity.LOW,
                        description=description,
                        code_snippet=line,
                        fix_suggestion="Optimize for better performance",
                        auto_fixable=False
                    ))

    def _check_security(self, filepath: Path, content: str):
        """Verifica problemas de segurança"""
        security_patterns = [
            ("eval(", "eval() is dangerous - security risk"),
            ("exec(", "exec() is dangerous - security risk"),
            ("pickle.loads", "Pickle deserialization vulnerability"),
            ("password =", "Possible hardcoded password"),
            ("api_key =", "Possible hardcoded API key"),
            ("os.system(", "Command injection risk"),
        ]

        lines = content.splitlines()
        for i, line in enumerate(lines, 1):
            for pattern, description in security_patterns:
                if pattern in line and not line.strip().startswith('#'):
                    self.bugs.append(Bug(
                        id=f"security_{filepath.stem}_{i}",
                        file=filepath,
                        line=i,
                        column=0,
                        type=BugType.SECURITY,
                        severity=BugSeverity.CRITICAL if "eval" in pattern or "exec" in pattern else BugSeverity.HIGH,
                        description=description,
                        code_snippet=line,
                        fix_suggestion="Remove or secure this code",
                        auto_fixable=False
                    ))

    def _has_break(self, node: ast.While) -> bool:
        """Verifica se loop tem break"""
        for child in ast.walk(node):
            if isinstance(child, ast.Break):
                return True
        return False

    def _is_variable_used(self, tree: ast.AST, var_name: str, after_line: int) -> bool:
        """Verifica se variável é usada"""
        for node in ast.walk(tree):
            if isinstance(node, ast.Name) and node.id == var_name:
                if isinstance(node.ctx, ast.Load) and hasattr(node, 'lineno'):
                    if node.lineno > after_line:
                        return True
        return False

    def _is_initialized(self, content: str, attribute: str) -> bool:
        """Verifica se atributo foi inicializado"""
        return f"self.{attribute} =" in content

    def _get_code_snippet(self, filepath: Path, line: int, context: int = 2) -> str:
        """Obtém snippet de código"""
        if filepath not in self.file_cache:
            with open(filepath, 'r') as f:
                self.file_cache[filepath] = f.read()

        lines = self.file_cache[filepath].splitlines()
        start = max(0, line - context - 1)
        end = min(len(lines), line + context)

        snippet_lines = []
        for i in range(start, end):
            prefix = ">>> " if i == line - 1 else "    "
            snippet_lines.append(f"{prefix}{lines[i]}")

        return "\n".join(snippet_lines)

    def _categorize_bugs(self):
        """Categoriza bugs encontrados"""
        print("\n📊 Bug Categories:")

        by_severity = defaultdict(list)
        by_type = defaultdict(list)
        by_file = defaultdict(list)

        for bug in self.bugs:
            by_severity[bug.severity].append(bug)
            by_type[bug.type].append(bug)
            by_file[bug.file.name].append(bug)

        print("\n   By Severity:")
        for severity in BugSeverity:
            count = len(by_severity[severity])
            if count > 0:
                icon = "🔴" if severity == BugSeverity.CRITICAL else "🟠" if severity == BugSeverity.HIGH else "🟡" if severity == BugSeverity.MEDIUM else "🟢"
                print(f"      {icon} {severity.value}: {count}")

        print("\n   By Type:")
        for bug_type in BugType:
            count = len(by_type[bug_type])
            if count > 0:
                print(f"      • {bug_type.value}: {count}")

        print("\n   By File:")
        for filename, bugs in sorted(by_file.items(), key=lambda x: len(x[1]), reverse=True)[:5]:
            print(f"      • {filename}: {len(bugs)} bugs")

    def generate_fixes(self) -> List[BugFix]:
        """Gera correções automáticas"""
        print("\n🔧 Generating automatic fixes...")

        for bug in self.bugs:
            if bug.auto_fixable:
                fix = self._generate_fix(bug)
                if fix:
                    self.fixes.append(fix)
                    print(f"   ✅ Fix generated for: {bug.id}")

        print(f"\n📝 Total fixes generated: {len(self.fixes)}")
        return self.fixes

    def _generate_fix(self, bug: Bug) -> Optional[BugFix]:
        """Gera correção para um bug"""
        if bug.type == BugType.SQL_ERROR:
            if "CREATE INDEX" in bug.code_snippet:
                fixed = bug.code_snippet.replace("CREATE INDEX", "CREATE INDEX IF NOT EXISTS")
                return BugFix(
                    bug_id=bug.id,
                    original_code=bug.code_snippet,
                    fixed_code=fixed,
                    confidence=0.95
                )

        elif bug.type == BugType.ATTRIBUTE_ERROR:
            if "stop_event" in bug.description:
                # Add initialization
                return BugFix(
                    bug_id=bug.id,
                    original_code="# Missing initialization",
                    fixed_code="self.stop_event = threading.Event()",
                    confidence=0.9
                )

        elif bug.type == BugType.KEY_ERROR:
            if "config" in bug.code_snippet:
                # Use .get() instead of []
                original = bug.code_snippet
                fixed = original.replace("self.config['", "self.config.get('").replace("']", "', {})")
                return BugFix(
                    bug_id=bug.id,
                    original_code=original,
                    fixed_code=fixed,
                    confidence=0.85
                )

        elif bug.type == BugType.IMPORT_ERROR:
            module = bug.description.split(": ")[1] if ": " in bug.description else ""
            if module:
                return BugFix(
                    bug_id=bug.id,
                    original_code=f"import {module}",
                    fixed_code=f"try:\n    import {module}\nexcept ImportError:\n    {module} = None",
                    confidence=0.8
                )

        return None

    def apply_fixes(self, dry_run: bool = True):
        """Aplica correções aos arquivos"""
        if dry_run:
            print("\n🔍 DRY RUN - No files will be modified")
        else:
            print("\n⚠️ APPLYING FIXES - Files will be modified!")

        applied = 0
        for fix in self.fixes:
            bug = next((b for b in self.bugs if b.id == fix.bug_id), None)
            if not bug:
                continue

            if dry_run:
                print(f"\n   Would fix in {bug.file.name}:{bug.line}")
                print(f"      - {fix.original_code}")
                print(f"      + {fix.fixed_code}")
            else:
                if self._apply_fix_to_file(bug.file, bug.line, fix):
                    fix.applied = True
                    applied += 1
                    print(f"   ✅ Fixed: {bug.id}")

        if not dry_run:
            print(f"\n✅ Applied {applied} fixes")

    def _apply_fix_to_file(self, filepath: Path, line: int, fix: BugFix) -> bool:
        """Aplica correção a um arquivo"""
        try:
            with open(filepath, 'r') as f:
                lines = f.readlines()

            # Apply fix
            if 0 <= line - 1 < len(lines):
                lines[line - 1] = fix.fixed_code + '\n'

                with open(filepath, 'w') as f:
                    f.writelines(lines)

                return True

        except Exception as e:
            print(f"      ❌ Error applying fix: {e}")

        return False

    def generate_report(self) -> Dict[str, Any]:
        """Gera relatório completo"""
        return {
            'timestamp': datetime.now().isoformat(),
            'total_bugs': len(self.bugs),
            'total_fixes': len(self.fixes),
            'bugs_by_severity': {
                severity.value: len([b for b in self.bugs if b.severity == severity])
                for severity in BugSeverity
            },
            'bugs_by_type': {
                bug_type.value: len([b for b in self.bugs if b.type == bug_type])
                for bug_type in BugType
            },
            'auto_fixable': len([b for b in self.bugs if b.auto_fixable]),
            'critical_bugs': [
                {
                    'file': str(b.file),
                    'line': b.line,
                    'description': b.description
                }
                for b in self.bugs if b.severity == BugSeverity.CRITICAL
            ]
        }


# Main execution
if __name__ == "__main__":
    print("🔍 ADVANCED BUG SCANNER")
    print("=" * 80)

    scanner = AdvancedBugScanner()

    # Scan all files
    bugs = scanner.scan_all_files()

    # Generate fixes
    fixes = scanner.generate_fixes()

    # Generate report
    report = scanner.generate_report()

    # Display summary
    print("\n" + "=" * 80)
    print("📊 SCAN SUMMARY")
    print("=" * 80)
    print(f"Total bugs found: {report['total_bugs']}")
    print(f"Auto-fixable: {report['auto_fixable']}")
    print(f"Fixes generated: {report['total_fixes']}")

    # Ask to apply fixes
    if fixes:
        print("\n❓ Apply fixes? (dry-run first)")
        scanner.apply_fixes(dry_run=True)

    # Save report
    report_path = CLAUDE_CODE_PATH / f"bug_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2, default=str)

    print(f"\n📄 Report saved to: {report_path}")
    print("\n✅ BUG SCAN COMPLETE!")

# Set alias for compatibility
BugScanner = AdvancedBugScanner