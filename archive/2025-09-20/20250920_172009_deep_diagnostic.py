#!/usr/bin/env python3
"""
DigiDoctor Deep Diagnostic Tool
Analyzes all Scripturemon files for hidden issues
"""

import ast
import sys
import os
import importlib
import traceback
import json
from pathlib import Path
from typing import Dict, List, Any

sys.path.insert(0, '/Users/clubproducoes/Digimundo/scripturemon-validation')

class DeepDiagnostic:
    def __init__(self):
        self.results = {
            'syntax_errors': [],
            'import_errors': [],
            'runtime_errors': [],
            'circular_imports': [],
            'missing_dependencies': [],
            'broken_singletons': [],
            'resource_leaks': [],
            'deadlock_risks': [],
            'silent_failures': []
        }
        
    def analyze_file(self, filepath: str) -> Dict:
        """Analyze a single Python file"""
        filename = os.path.basename(filepath)
        analysis = {
            'file': filename,
            'issues': [],
            'metrics': {}
        }
        
        # Read file content
        try:
            with open(filepath, 'r') as f:
                content = f.read()
        except Exception as e:
            analysis['issues'].append(f"Cannot read: {e}")
            return analysis
            
        # AST Analysis
        try:
            tree = ast.parse(content)
            analysis['metrics'] = self.analyze_ast(tree, content)
        except SyntaxError as e:
            self.results['syntax_errors'].append({
                'file': filename,
                'line': e.lineno,
                'error': str(e)
            })
            analysis['issues'].append(f"Syntax error at line {e.lineno}: {e}")
            
        # Pattern Detection
        self.detect_patterns(content, filename, analysis)
        
        return analysis
        
    def analyze_ast(self, tree: ast.AST, content: str) -> Dict:
        """Deep AST analysis"""
        metrics = {
            'try_blocks': 0,
            'bare_excepts': 0,
            'pass_excepts': 0,
            'nested_tries': 0,
            'max_try_depth': 0,
            'function_imports': 0,
            'complexity': 0,
            'semaphores': 0,
            'unclosed_resources': 0
        }
        
        class Visitor(ast.NodeVisitor):
            def __init__(self):
                self.try_depth = 0
                self.in_function = False
                self.in_try = False
                self.semaphore_vars = set()
                self.acquired_resources = set()
                
            def visit_FunctionDef(self, node):
                self.in_function = True
                metrics['complexity'] += 1
                
                # Check for complexity
                for child in ast.walk(node):
                    if isinstance(child, (ast.If, ast.For, ast.While, ast.Try)):
                        metrics['complexity'] += 1
                        
                self.generic_visit(node)
                self.in_function = False
                
            def visit_Try(self, node):
                metrics['try_blocks'] += 1
                self.try_depth += 1
                self.in_try = True
                
                if self.try_depth > 1:
                    metrics['nested_tries'] += 1
                metrics['max_try_depth'] = max(metrics['max_try_depth'], self.try_depth)
                
                # Check handlers
                for handler in node.handlers:
                    if handler.type is None:
                        metrics['bare_excepts'] += 1
                    if len(handler.body) == 1 and isinstance(handler.body[0], ast.Pass):
                        metrics['pass_excepts'] += 1
                        
                # Check for finally
                has_finally = len(node.finalbody) > 0
                
                self.generic_visit(node)
                self.try_depth -= 1
                self.in_try = False
                
            def visit_Import(self, node):
                if self.in_function:
                    metrics['function_imports'] += 1
                    
            def visit_ImportFrom(self, node):
                if self.in_function:
                    metrics['function_imports'] += 1
                    
            def visit_Call(self, node):
                # Detect semaphore/lock usage
                if isinstance(node.func, ast.Attribute):
                    if node.func.attr in ['acquire', 'lock']:
                        metrics['semaphores'] += 1
                        if self.in_try and not self.check_finally_release(node):
                            metrics['unclosed_resources'] += 1
                            
            def check_finally_release(self, node):
                # Simplified check - would need more complex analysis
                return False
                
        visitor = Visitor()
        visitor.visit(tree)
        
        return metrics
        
    def detect_patterns(self, content: str, filename: str, analysis: Dict):
        """Detect problematic patterns"""
        lines = content.split('\n')
        
        # Detect semaphore without finally
        if 'acquire' in content and 'finally' not in content:
            self.results['resource_leaks'].append({
                'file': filename,
                'issue': 'Semaphore acquire without finally block'
            })
            analysis['issues'].append('Resource leak risk: acquire without finally')
            
        # Detect circular import patterns
        if 'from .' in content and 'import' in content:
            import_lines = [i for i, line in enumerate(lines) if 'from .' in line]
            for line_no in import_lines:
                if line_no > 50:  # Late imports suggest circular dependency
                    self.results['circular_imports'].append({
                        'file': filename,
                        'line': line_no + 1,
                        'import': lines[line_no].strip()
                    })
                    
        # Detect silent failures
        silent_patterns = [
            'except:\n    pass',
            'except:\n        pass',
            'except Exception:\n    pass',
            'except Exception:\n        pass'
        ]
        for pattern in silent_patterns:
            if pattern in content:
                count = content.count(pattern)
                self.results['silent_failures'].append({
                    'file': filename,
                    'pattern': pattern.replace('\n', '\\n'),
                    'count': count
                })
                analysis['issues'].append(f'Silent failure pattern: {count} occurrences')
                
        # Detect potential deadlocks
        if 'Lock()' in content or 'Semaphore' in content:
            if content.count('acquire') > content.count('release'):
                self.results['deadlock_risks'].append({
                    'file': filename,
                    'acquires': content.count('acquire'),
                    'releases': content.count('release')
                })
                analysis['issues'].append('Deadlock risk: more acquires than releases')
                
    def test_imports(self):
        """Test all imports to find broken dependencies"""
        problem_files = os.listdir('/Users/clubproducoes/Digimundo/scripturemon-validation/DigiDoctor/problematic_files')
        
        for file in problem_files:
            if file.endswith('.py') and not file.startswith('__'):
                module_name = file[:-3]
                try:
                    # Try dynamic import
                    spec = importlib.util.spec_from_file_location(
                        module_name,
                        f'/Users/clubproducoes/Digimundo/scripturemon-validation/DigiDoctor/problematic_files/{file}'
                    )
                    if spec and spec.loader:
                        module = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(module)
                except ImportError as e:
                    self.results['import_errors'].append({
                        'file': file,
                        'error': str(e),
                        'missing': self.extract_missing_module(str(e))
                    })
                except Exception as e:
                    self.results['runtime_errors'].append({
                        'file': file,
                        'error': str(e),
                        'traceback': traceback.format_exc()
                    })
                    
    def extract_missing_module(self, error_msg: str) -> str:
        """Extract missing module name from import error"""
        if "No module named" in error_msg:
            parts = error_msg.split("'")
            if len(parts) >= 2:
                return parts[1]
        return "unknown"
        
    def generate_report(self) -> Dict:
        """Generate comprehensive diagnostic report"""
        report = {
            'summary': {},
            'critical_issues': [],
            'file_analyses': [],
            'recommendations': []
        }
        
        # Analyze all problematic files
        prob_dir = '/Users/clubproducoes/Digimundo/scripturemon-validation/DigiDoctor/problematic_files'
        for file in os.listdir(prob_dir):
            if file.endswith('.py'):
                filepath = os.path.join(prob_dir, file)
                analysis = self.analyze_file(filepath)
                report['file_analyses'].append(analysis)
                
        # Test imports
        self.test_imports()
        
        # Compile summary
        report['summary'] = {
            'total_files_analyzed': len(report['file_analyses']),
            'syntax_errors': len(self.results['syntax_errors']),
            'import_errors': len(self.results['import_errors']),
            'runtime_errors': len(self.results['runtime_errors']),
            'circular_imports': len(self.results['circular_imports']),
            'resource_leaks': len(self.results['resource_leaks']),
            'deadlock_risks': len(self.results['deadlock_risks']),
            'silent_failures': sum(f['count'] for f in self.results['silent_failures'])
        }
        
        # Identify critical issues
        for error in self.results['syntax_errors']:
            report['critical_issues'].append({
                'severity': 'CRITICAL',
                'type': 'Syntax Error',
                'file': error['file'],
                'details': error['error']
            })
            
        for risk in self.results['deadlock_risks']:
            if risk['acquires'] - risk['releases'] > 2:
                report['critical_issues'].append({
                    'severity': 'HIGH',
                    'type': 'Deadlock Risk',
                    'file': risk['file'],
                    'details': f"Unbalanced: {risk['acquires']} acquires vs {risk['releases']} releases"
                })
                
        # Generate recommendations
        if report['summary']['syntax_errors'] > 0:
            report['recommendations'].append('Fix all syntax errors immediately')
            
        if report['summary']['deadlock_risks'] > 5:
            report['recommendations'].append('Implement context managers for all resource management')
            
        if report['summary']['silent_failures'] > 50:
            report['recommendations'].append('Replace all bare except clauses with specific error handling')
            
        # Add detailed results
        report['detailed_results'] = self.results
        
        return report


def main():
    print("🔍 DigiDoctor Deep Diagnostic Starting...")
    print("="*60)
    
    diagnostic = DeepDiagnostic()
    report = diagnostic.generate_report()
    
    # Save report
    report_path = '/Users/clubproducoes/Digimundo/scripturemon-validation/DigiDoctor/reports/deep_diagnostic_report.json'
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2, default=str)
    
    # Print summary
    print("\n📊 DIAGNOSTIC SUMMARY")
    print("-"*40)
    for key, value in report['summary'].items():
        print(f"  {key}: {value}")
    
    print("\n🚨 CRITICAL ISSUES")
    print("-"*40)
    for issue in report['critical_issues'][:10]:
        print(f"  [{issue['severity']}] {issue['type']} in {issue['file']}")
        print(f"    {issue['details']}")
    
    print("\n💡 RECOMMENDATIONS")
    print("-"*40)
    for rec in report['recommendations']:
        print(f"  • {rec}")
    
    print(f"\n✅ Full report saved to: {report_path}")
    
    return report


if __name__ == "__main__":
    main()