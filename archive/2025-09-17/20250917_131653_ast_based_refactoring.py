#!/usr/bin/env python3
"""
🔧 AST-BASED REFACTORING SYSTEM
================================
Solução definitiva para correção de código usando AST
Evita todos os problemas causados por regex
"""

import ast
import os
import sys
import time
import shutil
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
import hashlib
import json


class ConstructorFixer(ast.NodeTransformer):
    """Corrige problemas de constructor usando AST"""
    
    def __init__(self):
        self.fixes_applied = 0
        self.methods_checked = 0
        
    def visit_FunctionDef(self, node: ast.FunctionDef) -> ast.FunctionDef:
        """Visita definições de função e corrige constructors"""
        self.methods_checked += 1
        
        # Corrige variações corrompidas de __init__
        if node.name in ['__init__', '__init___', '__init___', '__ini__', '__int__', '_init_']:
            print(f"  🔧 Fixing constructor: {node.name} -> __init__ at line {node.lineno}")
            node.name = '__init__'
            self.fixes_applied += 1
            
        # Processa decoradores
        node.decorator_list = [self.visit(d) for d in node.decorator_list]
        
        # Processa corpo da função
        node.body = [self.visit(stmt) for stmt in node.body]
        
        return node
    
    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> ast.AsyncFunctionDef:
        """Trata funções async da mesma forma"""
        return self.visit_FunctionDef(node)
    
    def visit_Call(self, node: ast.Call) -> ast.Call:
        """Corrige chamadas para super().__init__()"""
        if isinstance(node.func, ast.Attribute):
            # Verifica se é super().__init__*()
            if (isinstance(node.func.value, ast.Call) and
                isinstance(node.func.value.func, ast.Name) and
                node.func.value.func.id == 'super'):
                
                # Corrige variações de __init__
                if node.func.attr in ['__init__', '__init___', '__init___']:
                    print(f"  🔧 Fixing super().{node.func.attr} -> super().__init__()")
                    node.func.attr = '__init__'
                    self.fixes_applied += 1
        
        # Processa argumentos recursivamente
        node.args = [self.visit(arg) for arg in node.args]
        node.keywords = [self.visit(kw) for kw in node.keywords]
        
        return node


class AsyncAwaitFixer(ast.NodeTransformer):
    """Corrige problemas de async/await"""
    
    def __init__(self):
        self.fixes_applied = 0
        self.current_function = None
        self.async_context = False
        
    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> ast.AsyncFunctionDef:
        """Rastreia contexto async"""
        old_context = self.async_context
        old_function = self.current_function
        
        self.async_context = True
        self.current_function = node.name
        
        # Verifica se função async tem await
        has_await = self._has_await(node)
        
        if not has_await:
            print(f"  ⚠️  Async function '{node.name}' without await - converting to sync")
            # Converte para função síncrona
            new_node = ast.FunctionDef(
                name=node.name,
                args=node.args,
                body=node.body,
                decorator_list=node.decorator_list,
                returns=node.returns,
                lineno=node.lineno,
                col_offset=node.col_offset
            )
            self.fixes_applied += 1
            result = self.visit_FunctionDef(new_node)
        else:
            node.body = [self.visit(stmt) for stmt in node.body]
            result = node
        
        self.async_context = old_context
        self.current_function = old_function
        
        return result
    
    def visit_FunctionDef(self, node: ast.FunctionDef) -> ast.FunctionDef:
        """Verifica funções síncronas"""
        old_context = self.async_context
        old_function = self.current_function
        
        self.async_context = False
        self.current_function = node.name
        
        # Verifica se função síncrona tem await
        has_await = self._has_await(node)
        
        if has_await:
            print(f"  ⚠️  Sync function '{node.name}' with await - converting to async")
            # Converte para função assíncrona
            new_node = ast.AsyncFunctionDef(
                name=node.name,
                args=node.args,
                body=node.body,
                decorator_list=node.decorator_list,
                returns=node.returns,
                lineno=node.lineno,
                col_offset=node.col_offset
            )
            self.fixes_applied += 1
            result = new_node
        else:
            node.body = [self.visit(stmt) for stmt in node.body]
            result = node
        
        self.async_context = old_context
        self.current_function = old_function
        
        return result
    
    def _has_await(self, node: ast.AST) -> bool:
        """Verifica se nó contém await"""
        for child in ast.walk(node):
            if isinstance(child, ast.Await):
                return True
        return False


class ImportFixer(ast.NodeTransformer):
    """Corrige e organiza imports"""
    
    def __init__(self, known_modules: Dict[str, str] = None):
        self.fixes_applied = 0
        self.known_modules = known_modules or {}
        self.imports_seen = set()
        
    def visit_Import(self, node: ast.Import) -> ast.Import:
        """Corrige imports simples"""
        for alias in node.names:
            # Corrige nomes conhecidos
            if alias.name in self.known_modules:
                old_name = alias.name
                alias.name = self.known_modules[alias.name]
                if old_name != alias.name:
                    print(f"  🔧 Fixing import: {old_name} -> {alias.name}")
                    self.fixes_applied += 1
            
            self.imports_seen.add(alias.name)
        
        return node
    
    def visit_ImportFrom(self, node: ast.ImportFrom) -> ast.ImportFrom:
        """Corrige imports from"""
        if node.module and node.module in self.known_modules:
            old_module = node.module
            node.module = self.known_modules[node.module]
            if old_module != node.module:
                print(f"  🔧 Fixing from import: {old_module} -> {node.module}")
                self.fixes_applied += 1
        
        if node.module:
            self.imports_seen.add(node.module)
        
        return node


class ASTRefactoringSystem:
    """Sistema principal de refatoração baseado em AST"""
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.backup_dir = project_root / '.ast_backups'
        self.stats = {
            'files_processed': 0,
            'files_fixed': 0,
            'constructor_fixes': 0,
            'async_fixes': 0,
            'import_fixes': 0,
            'errors': []
        }
        
        # Criar diretório de backup
        self.backup_dir.mkdir(exist_ok=True)
        
    def process_file(self, file_path: Path) -> Tuple[bool, int]:
        """Processa um arquivo Python com AST"""
        try:
            # Ler arquivo
            with open(file_path, 'r', encoding='utf-8') as f:
                original_content = f.read()
            
            # Parse AST
            try:
                tree = ast.parse(original_content, filename=str(file_path))
            except SyntaxError as e:
                print(f"  ❌ Syntax error in {file_path}: {e}")
                self.stats['errors'].append({
                    'file': str(file_path),
                    'error': f'Syntax error: {e}'
                })
                return False, 0
            
            # Aplicar fixes
            total_fixes = 0
            
            # 1. Fix constructors
            constructor_fixer = ConstructorFixer()
            tree = constructor_fixer.visit(tree)
            total_fixes += constructor_fixer.fixes_applied
            self.stats['constructor_fixes'] += constructor_fixer.fixes_applied
            
            # 2. Fix async/await
            async_fixer = AsyncAwaitFixer()
            tree = async_fixer.visit(tree)
            total_fixes += async_fixer.fixes_applied
            self.stats['async_fixes'] += async_fixer.fixes_applied
            
            # 3. Fix imports
            import_fixer = ImportFixer(self.get_known_modules())
            tree = import_fixer.visit(tree)
            total_fixes += import_fixer.fixes_applied
            self.stats['import_fixes'] += import_fixer.fixes_applied
            
            # Se houve mudanças, salvar arquivo
            if total_fixes > 0:
                # Criar backup
                backup_path = self.backup_dir / f"{file_path.name}.{int(time.time())}.bak"
                shutil.copy2(file_path, backup_path)
                
                # Gerar código corrigido
                ast.fix_missing_locations(tree)
                fixed_content = ast.unparse(tree)
                
                # Salvar arquivo corrigido
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(fixed_content)
                
                print(f"  ✅ Fixed {total_fixes} issues in {file_path.name}")
                return True, total_fixes
            
            return False, 0
            
        except Exception as e:
            print(f"  ❌ Error processing {file_path}: {e}")
            self.stats['errors'].append({
                'file': str(file_path),
                'error': str(e)
            })
            return False, 0
    
    def get_known_modules(self) -> Dict[str, str]:
        """Retorna mapeamento de módulos conhecidos"""
        return {
            # Correções de nomes conhecidos
            'persistent_memory_system_system_system': 'persistent_memory_system_system_system_system',
            'DigionProducermonOrchestrator': 'DigionProducerMonOrchestrator',
            'scripturemon': 'scripturemon',
        }
    
    def process_directory(self, directory: Path, pattern: str = '*.py') -> Dict[str, Any]:
        """Processa todos os arquivos Python em um diretório"""
        print(f"\n🔍 Scanning {directory}...")
        
        py_files = list(directory.rglob(pattern))
        print(f"Found {len(py_files)} Python files")
        
        for file_path in py_files:
            # Pular backups
            if '.bak' in str(file_path) or '.ast_backups' in str(file_path):
                continue
            
            print(f"\n📄 Processing {file_path.relative_to(self.project_root)}")
            
            self.stats['files_processed'] += 1
            fixed, num_fixes = self.process_file(file_path)
            
            if fixed:
                self.stats['files_fixed'] += 1
        
        return self.stats
    
    def verify_fixes(self) -> bool:
        """Verifica se os fixes foram aplicados corretamente"""
        print("\n🔍 Verifying fixes...")
        
        errors = 0
        py_files = list(self.project_root.rglob('*.py'))
        
        for file_path in py_files[:10]:  # Verificar amostra
            if '.bak' in str(file_path) or '.ast_backups' in str(file_path):
                continue
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Verificar problemas conhecidos
                if '__init__' in content:
                    print(f"  ❌ Still has __init__ in {file_path.name}")
                    errors += 1
                
                # Tentar parsear
                ast.parse(content)
                
            except SyntaxError as e:
                print(f"  ❌ Syntax error in {file_path.name}: {e}")
                errors += 1
        
        if errors == 0:
            print("  ✅ All verified files are clean!")
            return True
        else:
            print(f"  ⚠️  Found {errors} remaining issues")
            return False
    
    def generate_report(self) -> str:
        """Gera relatório de correções"""
        report = []
        report.append("\n" + "="*60)
        report.append("🔧 AST-BASED REFACTORING REPORT")
        report.append("="*60)
        report.append(f"Timestamp: {datetime.now().isoformat()}")
        report.append(f"Project: {self.project_root}")
        report.append("")
        
        report.append("📊 STATISTICS:")
        report.append(f"  • Files processed: {self.stats['files_processed']}")
        report.append(f"  • Files fixed: {self.stats['files_fixed']}")
        report.append(f"  • Constructor fixes: {self.stats['constructor_fixes']}")
        report.append(f"  • Async/await fixes: {self.stats['async_fixes']}")
        report.append(f"  • Import fixes: {self.stats['import_fixes']}")
        report.append(f"  • Total fixes: {self.stats['constructor_fixes'] + self.stats['async_fixes'] + self.stats['import_fixes']}")
        
        if self.stats['errors']:
            report.append("")
            report.append("❌ ERRORS:")
            for error in self.stats['errors'][:10]:  # Show first 10
                report.append(f"  • {error['file']}: {error['error']}")
        
        report.append("")
        report.append("✅ REFACTORING COMPLETE")
        report.append("="*60)
        
        return "\n".join(report)


def main():
    """Execução principal"""
    print("\n🔧 AST-BASED REFACTORING SYSTEM v1.0")
    print("="*60)
    print("This system uses Abstract Syntax Trees to safely refactor code")
    print("No regex patterns = No corruption!")
    print("="*60)
    
    # Inicializar sistema
    refactorer = ASTRefactoringSystem(
        project_root=Path("/Users/clubproducoes/Digimundo/scripturemon-champion")
    )
    
    # Processar diretório principal
    stats = refactorer.process_directory(
        refactorer.project_root / "apps" / "scripturemon"
    )
    
    # Verificar resultados
    success = refactorer.verify_fixes()
    
    # Gerar relatório
    report = refactorer.generate_report()
    print(report)
    
    # Salvar relatório
    report_path = refactorer.project_root / "ast_refactoring_report.txt"
    with open(report_path, 'w') as f:
        f.write(report)
    
    print(f"\n📄 Report saved to {report_path}")
    
    return success, stats


if __name__ == "__main__":
    success, stats = main()