#!/usr/bin/env python3
"""
FASE 13 - Bateria Completa de Testes do Sistema
Testa TODOS os componentes do ScriptureMon Champion
DIGIMUNDO PRESENTE
"""

import sys
import os
import json
import time
import traceback
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Tuple
import importlib.util

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))


class SystemTester:
    """Testador completo do sistema ScriptureMon"""

    def __init__(self):
        self.results = {
            'timestamp': datetime.now().isoformat(),
            'total_files': 0,
            'python_files': {},
            'shell_scripts': {},
            'executables': {},
            'imports': {},
            'tests_passed': 0,
            'tests_failed': 0,
            'components': {},
            'errors': []
        }
        self.log_file = Path(f"tests/reports/phase_13_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        self.log_file.parent.mkdir(parents=True, exist_ok=True)

    def log(self, msg: str, level: str = "INFO"):
        """Log message with timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] [{level}] {msg}")

    def test_python_file(self, file_path: Path) -> Dict[str, Any]:
        """Testa um arquivo Python"""
        result = {
            'path': str(file_path),
            'exists': file_path.exists(),
            'size': 0,
            'can_import': False,
            'has_main': False,
            'executable': False,
            'syntax_valid': False,
            'functions': [],
            'classes': [],
            'errors': []
        }

        try:
            # Check file stats
            if file_path.exists():
                result['size'] = file_path.stat().st_size
                result['executable'] = os.access(file_path, os.X_OK)

            # Check syntax
            with open(file_path, 'r', encoding='utf-8') as f:
                code = f.read()
                compile(code, str(file_path), 'exec')
                result['syntax_valid'] = True

                # Check for main
                result['has_main'] = 'if __name__ == "__main__":' in code

                # Count functions and classes
                import ast
                tree = ast.parse(code)
                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        result['functions'].append(node.name)
                    elif isinstance(node, ast.ClassDef):
                        result['classes'].append(node.name)

            # Try to import if it's a module
            if file_path.stem != '__init__' and not file_path.stem.startswith('test_'):
                try:
                    module_path = str(file_path).replace('/', '.').replace('.py', '')
                    if module_path.startswith('.'):
                        module_path = module_path[1:]

                    spec = importlib.util.spec_from_file_location(
                        file_path.stem,
                        file_path
                    )
                    if spec and spec.loader:
                        module = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(module)
                        result['can_import'] = True
                except Exception as e:
                    result['errors'].append(f"Import failed: {str(e)}")

        except SyntaxError as e:
            result['errors'].append(f"Syntax error: {e}")
        except Exception as e:
            result['errors'].append(str(e))

        return result

    def test_shell_script(self, file_path: Path) -> Dict[str, Any]:
        """Testa um script shell"""
        result = {
            'path': str(file_path),
            'exists': file_path.exists(),
            'executable': False,
            'syntax_valid': False,
            'dry_run': False,
            'errors': []
        }

        try:
            if file_path.exists():
                result['executable'] = os.access(file_path, os.X_OK)

                # Check syntax with bash -n
                proc = subprocess.run(
                    ['bash', '-n', str(file_path)],
                    capture_output=True,
                    text=True,
                    timeout=60
                )
                result['syntax_valid'] = proc.returncode == 0
                if proc.stderr:
                    result['errors'].append(f"Syntax check: {proc.stderr}")

        except Exception as e:
            result['errors'].append(str(e))

        return result

    def test_component(self, name: str, test_func) -> Dict[str, Any]:
        """Testa um componente específico"""
        result = {
            'name': name,
            'status': 'UNKNOWN',
            'time': 0,
            'output': '',
            'errors': []
        }

        start = time.time()
        try:
            output = test_func()
            result['status'] = 'PASS'
            result['output'] = str(output)
        except Exception as e:
            result['status'] = 'FAIL'
            result['errors'].append(str(e))
            result['errors'].append(traceback.format_exc())
        finally:
            result['time'] = time.time() - start

        return result

    def scan_all_files(self):
        """Escaneia todos os arquivos do projeto"""
        self.log("Scanning all project files...")

        # Python files
        python_files = list(Path('.').rglob('*.py'))
        self.results['total_files'] = len(python_files)

        for i, py_file in enumerate(python_files, 1):
            if i % 10 == 0:
                self.log(f"Processing Python files: {i}/{len(python_files)}")

            # Skip cache and virtual env
            if '__pycache__' in str(py_file) or 'venv' in str(py_file):
                continue

            result = self.test_python_file(py_file)
            self.results['python_files'][str(py_file)] = result

            if result['syntax_valid']:
                self.results['tests_passed'] += 1
            else:
                self.results['tests_failed'] += 1

        # Shell scripts
        shell_files = list(Path('.').rglob('*.sh'))
        for sh_file in shell_files:
            result = self.test_shell_script(sh_file)
            self.results['shell_scripts'][str(sh_file)] = result

        self.log(f"Found {len(python_files)} Python files, {len(shell_files)} shell scripts")

    def test_core_components(self):
        """Testa componentes principais"""
        self.log("Testing core components...")

        # Test imports
        components = [
            ('OllamaCore', lambda: __import__('apps.scripturemon.ollama_core', fromlist=['OllamaCore'])),
            ('DigiLang', lambda: __import__('apps.scripturemon.digilang', fromlist=['__init__'])),
            ('OCRPipeline', lambda: __import__('apps.scripturemon.ocr_pipeline', fromlist=['OCRPipeline'])),
            ('PDFDetector', lambda: __import__('apps.scripturemon.pdf_detector', fromlist=['PDFDetector'])),
            ('MemorySystem', lambda: __import__('apps.scripturemon.memory_system', fromlist=['MemorySystem'])),
            ('UnifiedManager', lambda: __import__('apps.scripturemon.unified_manager', fromlist=['UnifiedMemoryManager'])),
            ('ScripturemonUnified', lambda: __import__('apps.scripturemon.scripturemon_unified', fromlist=['ScripturemonUnified'])),
            ('ScreenplayNormalizer', lambda: __import__('apps.scripturemon.screenplay_normalizer', fromlist=['ScreenplayNormalizer'])),
            ('DigiLangV3', lambda: __import__('apps.scripturemon.digilang_v3_ta', fromlist=['DigiLangV3Encoder'])),
        ]

        for name, test_func in components:
            result = self.test_component(name, test_func)
            self.results['components'][name] = result

            if result['status'] == 'PASS':
                self.log(f"✅ {name} - OK")
            else:
                self.log(f"❌ {name} - FAILED", "ERROR")

    def test_executables(self):
        """Testa executáveis do sistema"""
        self.log("Testing executable files...")

        executables = [
            'bin/scripturemon',
            'tests/test_phase_2a.sh',
            'tests/test_phase_3a.sh',
            'tests/test_phase_7_ollama.sh',
            'tests/test_phase_8_memory.sh',
            'tests/test_phase_9_production.sh',
        ]

        for exe_path in executables:
            path = Path(exe_path)
            result = {
                'path': exe_path,
                'exists': path.exists(),
                'executable': False,
                'can_run': False
            }

            if path.exists():
                result['executable'] = os.access(path, os.X_OK)

                # Try dry run for shell scripts
                if exe_path.endswith('.sh'):
                    try:
                        proc = subprocess.run(
                            ['bash', '-n', exe_path],
                            capture_output=True,
                            timeout=60
                        )
                        result['can_run'] = proc.returncode == 0
                    except:
                        pass

            self.results['executables'][exe_path] = result

            status = "✅" if result['exists'] and result['executable'] else "❌"
            self.log(f"{status} {exe_path}")

    def check_dependencies(self):
        """Verifica dependências do sistema"""
        self.log("Checking system dependencies...")

        dependencies = {
            'ollama': 'ollama --version',
            'python3': 'python3 --version',
            'pip': 'pip3 --version',
            'git': 'git --version',
            'bash': 'bash --version',
        }

        self.results['dependencies'] = {}

        for dep, cmd in dependencies.items():
            try:
                proc = subprocess.run(
                    cmd.split(),
                    capture_output=True,
                    text=True,
                    timeout=60
                )
                available = proc.returncode == 0
                version = proc.stdout.strip() if available else None
                self.results['dependencies'][dep] = {
                    'available': available,
                    'version': version
                }
                status = "✅" if available else "❌"
                self.log(f"{status} {dep}: {version if version else 'NOT FOUND'}")
            except Exception as e:
                self.results['dependencies'][dep] = {
                    'available': False,
                    'error': str(e)
                }
                self.log(f"❌ {dep}: ERROR", "ERROR")

    def analyze_structure(self):
        """Analisa estrutura do projeto"""
        self.log("Analyzing project structure...")

        # Count files by directory
        dirs = {}
        for py_file in Path('.').rglob('*.py'):
            if '__pycache__' in str(py_file):
                continue

            dir_path = str(py_file.parent)
            if dir_path not in dirs:
                dirs[dir_path] = {'python': 0, 'shell': 0, 'other': 0}
            dirs[dir_path]['python'] += 1

        for sh_file in Path('.').rglob('*.sh'):
            dir_path = str(sh_file.parent)
            if dir_path not in dirs:
                dirs[dir_path] = {'python': 0, 'shell': 0, 'other': 0}
            dirs[dir_path]['shell'] += 1

        self.results['structure'] = dirs

        # Show top directories
        sorted_dirs = sorted(dirs.items(), key=lambda x: x[1]['python'] + x[1]['shell'], reverse=True)[:10]
        self.log("Top directories by file count:")
        for dir_path, counts in sorted_dirs:
            self.log(f"  {dir_path}: {counts['python']} .py, {counts['shell']} .sh")

    def check_running_processes(self):
        """Verifica processos em execução"""
        self.log("Checking running processes...")

        # Check for background shells
        try:
            proc = subprocess.run(
                ['ps', 'aux'],
                capture_output=True,
                text=True,
                timeout=60
            )

            processes = []
            for line in proc.stdout.split('\n'):
                if 'python' in line.lower() and 'scripturemon' in line.lower():
                    processes.append(line[:120])  # First 120 chars
                elif 'ollama' in line.lower():
                    processes.append(line[:120])

            self.results['running_processes'] = processes

            if processes:
                self.log(f"Found {len(processes)} related processes running")
            else:
                self.log("No related processes found")

        except Exception as e:
            self.log(f"Could not check processes: {e}", "WARNING")

    def generate_report(self):
        """Gera relatório final"""
        self.log("Generating final report...")

        # Calculate statistics
        total_py = len(self.results['python_files'])
        valid_py = sum(1 for f in self.results['python_files'].values() if f['syntax_valid'])
        importable = sum(1 for f in self.results['python_files'].values() if f['can_import'])
        with_main = sum(1 for f in self.results['python_files'].values() if f['has_main'])

        total_sh = len(self.results['shell_scripts'])
        valid_sh = sum(1 for f in self.results['shell_scripts'].values() if f['syntax_valid'])
        executable_sh = sum(1 for f in self.results['shell_scripts'].values() if f['executable'])

        components_ok = sum(1 for c in self.results['components'].values() if c['status'] == 'PASS')
        components_total = len(self.results['components'])

        # Summary
        self.results['summary'] = {
            'python_files': {
                'total': total_py,
                'valid_syntax': valid_py,
                'importable': importable,
                'with_main': with_main,
                'syntax_errors': total_py - valid_py
            },
            'shell_scripts': {
                'total': total_sh,
                'valid_syntax': valid_sh,
                'executable': executable_sh
            },
            'components': {
                'total': components_total,
                'passed': components_ok,
                'failed': components_total - components_ok
            },
            'health_score': (valid_py / total_py * 100) if total_py > 0 else 0
        }

        # Save report
        with open(self.log_file, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)

        self.log(f"Report saved to: {self.log_file}")

        # Print summary
        print("\n" + "="*60)
        print("FASE 13 - TEST SUMMARY")
        print("="*60)
        print(f"Python Files: {valid_py}/{total_py} valid ({valid_py/total_py*100:.1f}%)")
        print(f"  - Importable: {importable}")
        print(f"  - With main: {with_main}")
        print(f"Shell Scripts: {valid_sh}/{total_sh} valid")
        print(f"  - Executable: {executable_sh}")
        print(f"Components: {components_ok}/{components_total} working")
        print(f"Health Score: {self.results['summary']['health_score']:.1f}%")
        print("="*60)

    def run(self):
        """Executa toda a bateria de testes"""
        print("\n" + "="*60)
        print("FASE 13 - COMPLETE SYSTEM TEST")
        print("Starting at:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        print("="*60 + "\n")

        start_time = time.time()

        # Run all tests
        self.check_dependencies()
        self.scan_all_files()
        self.test_core_components()
        self.test_executables()
        self.analyze_structure()
        self.check_running_processes()
        self.generate_report()

        total_time = time.time() - start_time
        self.log(f"\nTotal test time: {total_time:.2f} seconds")

        print("\nDIGIMUNDO PRESENTE")
        return self.results


def main():
    """Run the complete test suite"""
    tester = SystemTester()
    results = tester.run()

    # Return exit code based on health
    if results['summary']['health_score'] >= 80:
        return 0  # Good health
    elif results['summary']['health_score'] >= 60:
        return 1  # Warning
    else:
        return 2  # Critical


if __name__ == "__main__":
    sys.exit(main())