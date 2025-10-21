#!/usr/bin/env python3
"""
🔧 FIX ALL PATHS - Corrige todos os caminhos quebrados pela reorganização
Analisa linha por linha e corrige imports e referências
"""

import os
import re
import json
from pathlib import Path
from typing import Dict, List, Tuple

class PathFixer:
    def __init__(self):
        self.base_path = Path("/Users/clubproducoes/Digimundo")
        self.fixes_applied = []
        self.errors = []
        self.files_fixed = 0
        
        # Mapa de onde os arquivos foram movidos
        self.file_moves = self._build_move_map()
        
    def _build_move_map(self) -> Dict[str, str]:
        """Constrói mapa de onde cada arquivo foi movido"""
        return {
            # Core systems
            "SOULOS_IMPLEMENTATION.py": "core/soulos/soulos.py",
            "SOULPACK_CRDT.py": "core/soulpack/crdt.py",
            "SDL_SELF_DISTILL.py": "core/sdl/consolidator.py",
            "DIGILANG_BYTECODE.py": "core/digilang/bytecode.py",
            "DIGILANG_PRODUCTION_SYSTEM.py": "core/digilang/production.py",
            "DIGILANG_NEURAL_SYMBOLIC_ENGINE.py": "systems/neural/DIGILANG_NEURAL_SYMBOLIC_ENGINE.py",
            "DIGILANG_DIGIMUNDO_COMPLETE.json": "core/digilang/DIGILANG_DIGIMUNDO_COMPLETE.json",
            "DIGILANG_COMPLETE_TESTS.py": "development/tests/DIGILANG_COMPLETE_TESTS.py",
            
            # Scripturemon specific
            "SCRIPTUREMON_IMMORTAL_FINAL.py": "archive/scripts/python/SCRIPTUREMON_IMMORTAL_FINAL.py",
            "scripturemon_immortal.modelfile": "archive/modelfiles/scripturemon_immortal.modelfile",
            "scripturemon_soulos.modelfile": "archive/modelfiles/scripturemon_soulos.modelfile",
            
            # Test files
            "TEST_REVOLUTIONARY_SYSTEMS.py": "systems/evolution/TEST_REVOLUTIONARY_SYSTEMS.py",
            "TEST_SOULOS_PRODUCTION.py": "development/tests/TEST_SOULOS_PRODUCTION.py",
            "SILICON_VALLEY_TEST_SUITE.py": "development/tests/SILICON_VALLEY_TEST_SUITE.py",
            
            # Launchers
            "DIGIMUNDO_SUPREME_LAUNCHER.sh": "systems/launchers/DIGIMUNDO_SUPREME_LAUNCHER.sh",
            "DIGIMUNDO_ULTIMATE_LAUNCHER.sh": "systems/launchers/DIGIMUNDO_ULTIMATE_LAUNCHER.sh",
            
            # Plans and docs
            "PLANO_DEFINITIVO_MODELFILE_DIGIMON.md": "archive/docs/markdown/PLANO_DEFINITIVO_MODELFILE_DIGIMON.md",
            "FEEDBACK_CHATGPT.md": "research/feedback/FEEDBACK_CHATGPT.md",
            "CLAUDE.md": "archive/docs/markdown/CLAUDE.md",
            
            # DigiLang files
            "DIGILANG_COMPLETE_ANALYSIS.py": "research/analysis/DIGILANG_COMPLETE_ANALYSIS.py",
            "DIGILANG_UNIFIED_COMPLETE.py": "core/digilang/DIGILANG_UNIFIED_COMPLETE.py",
            "DIGILANG_OPTIMIZED.json": "core/digilang/DIGILANG_OPTIMIZED.json",
            
            # Memory and consciousness
            "consciousness": "archive/consciousness",
            "memory": "archive/memory_old",
            "genetic": "archive/genetic_old",
            "soulpacks": "archive/soulpacks_old",
        }
    
    def fix_python_imports(self, file_path: Path) -> int:
        """Corrige imports em arquivos Python"""
        fixes = 0
        
        try:
            content = file_path.read_text()
            original_content = content
            
            # Padrões de import para corrigir
            import_fixes = [
                # Imports diretos que foram movidos
                (r"from SOULOS_IMPLEMENTATION import", "from core.soulos.soulos import"),
                (r"from SOULPACK_CRDT import", "from core.soulpack.crdt import"),
                (r"from SDL_SELF_DISTILL import", "from core.sdl.consolidator import"),
                (r"from DIGILANG_BYTECODE import", "from core.digilang.bytecode import"),
                (r"from SCRIPTUREMON_IMMORTAL_FINAL import", "import sys; sys.path.append('/Users/clubproducoes/Digimundo/archive/scripts/python'); from SCRIPTUREMON_IMMORTAL_FINAL import"),
                
                # Imports relativos
                (r"from soulos import", "from core.soulos.soulos import"),
                (r"from crdt import", "from core.soulpack.crdt import"),
                (r"from consolidator import", "from core.sdl.consolidator import"),
                (r"from bytecode import", "from core.digilang.bytecode import"),
                
                # Import statements
                (r"import SOULOS_IMPLEMENTATION", "import sys; sys.path.append('/Users/clubproducoes/Digimundo/core/soulos'); import soulos"),
                (r"import SOULPACK_CRDT", "import sys; sys.path.append('/Users/clubproducoes/Digimundo/core/soulpack'); import crdt"),
            ]
            
            for old_import, new_import in import_fixes:
                if re.search(old_import, content):
                    content = re.sub(old_import, new_import, content)
                    fixes += 1
                    self.fixes_applied.append({
                        "file": str(file_path),
                        "type": "import",
                        "old": old_import,
                        "new": new_import
                    })
            
            # Fix sys.path.insert statements
            path_fixes = [
                (r"sys\.path\.insert\(0, 'core/soulos'\)", 
                 "sys.path.insert(0, '/Users/clubproducoes/Digimundo/core/soulos')"),
                (r"sys\.path\.insert\(0, 'core/soulpack'\)", 
                 "sys.path.insert(0, '/Users/clubproducoes/Digimundo/core/soulpack')"),
                (r"sys\.path\.insert\(0, 'core/sdl'\)", 
                 "sys.path.insert(0, '/Users/clubproducoes/Digimundo/core/sdl')"),
                (r"sys\.path\.insert\(0, 'core/digilang'\)", 
                 "sys.path.insert(0, '/Users/clubproducoes/Digimundo/core/digilang')"),
            ]
            
            for old_path, new_path in path_fixes:
                if re.search(old_path, content):
                    content = re.sub(old_path, new_path, content)
                    fixes += 1
            
            # Fix file paths
            path_replacements = [
                # Modelfiles
                ("scripturemon_immortal.modelfile", "archive/modelfiles/scripturemon_immortal.modelfile"),
                ("scripturemon_soulos.modelfile", "archive/modelfiles/scripturemon_soulos.modelfile"),
                
                # Consciousness/Memory paths
                (r"consciousness/([^'\"]*?)_memories\.db", r"digimons/\1/memory/crystals.db"),
                (r"soulpacks/scripturemon/", "digimons/scripturemon/soulpacks/"),
                (r"genetic/", "digimons/scripturemon/adapters/"),
                
                # DigiLang files
                ("DIGILANG_DIGIMUNDO_COMPLETE.json", "core/digilang/DIGILANG_DIGIMUNDO_COMPLETE.json"),
                
                # Test files
                ("TEST_REVOLUTIONARY_SYSTEMS.py", "systems/evolution/TEST_REVOLUTIONARY_SYSTEMS.py"),
            ]
            
            for old_path, new_path in path_replacements:
                if old_path in content:
                    content = content.replace(old_path, new_path)
                    fixes += 1
                    self.fixes_applied.append({
                        "file": str(file_path),
                        "type": "path",
                        "old": old_path,
                        "new": new_path
                    })
            
            # Save if changed
            if content != original_content:
                file_path.write_text(content)
                self.files_fixed += 1
                print(f"  ✓ Fixed {fixes} issues in {file_path.name}")
            
            return fixes
            
        except Exception as e:
            self.errors.append(f"Error fixing {file_path}: {e}")
            return 0
    
    def fix_shell_scripts(self, file_path: Path) -> int:
        """Corrige caminhos em scripts Shell"""
        fixes = 0
        
        try:
            content = file_path.read_text()
            original_content = content
            
            # Path replacements for shell scripts
            shell_fixes = [
                # Python scripts
                ("SOULOS_IMPLEMENTATION.py", "core/soulos/soulos.py"),
                ("SOULPACK_CRDT.py", "core/soulpack/crdt.py"),
                ("SDL_SELF_DISTILL.py", "core/sdl/consolidator.py"),
                ("DIGILANG_BYTECODE.py", "core/digilang/bytecode.py"),
                
                # Directories
                ("consciousness/", "archive/consciousness/"),
                ("genetic/", "archive/genetic_old/"),
                ("soulpacks/", "archive/soulpacks_old/"),
                
                # Config files
                ("CLAUDE.md", "config/claude_memory.md"),
                
                # Python paths
                ("python3 TEST_REVOLUTIONARY_SYSTEMS.py", 
                 "python3 systems/evolution/TEST_REVOLUTIONARY_SYSTEMS.py"),
                ("python3 SILICON_VALLEY_TEST_SUITE.py",
                 "python3 development/tests/SILICON_VALLEY_TEST_SUITE.py"),
            ]
            
            for old_path, new_path in shell_fixes:
                if old_path in content:
                    content = content.replace(old_path, new_path)
                    fixes += 1
                    self.fixes_applied.append({
                        "file": str(file_path),
                        "type": "shell_path",
                        "old": old_path,
                        "new": new_path
                    })
            
            # Fix cd commands
            cd_fixes = [
                ("cd consciousness", "cd archive/consciousness"),
                ("cd genetic", "cd archive/genetic_old"),
                ("cd soulpacks", "cd archive/soulpacks_old"),
                ("cd digimons/scripturemon/memory", "cd digimons/scripturemon/memory"),
            ]
            
            for old_cd, new_cd in cd_fixes:
                if old_cd in content:
                    content = content.replace(old_cd, new_cd)
                    fixes += 1
            
            # Save if changed
            if content != original_content:
                file_path.write_text(content)
                self.files_fixed += 1
                print(f"  ✓ Fixed {fixes} issues in {file_path.name}")
            
            return fixes
            
        except Exception as e:
            self.errors.append(f"Error fixing {file_path}: {e}")
            return 0
    
    def fix_core_systems(self):
        """Corrige sistemas core críticos"""
        print("\n🔧 Fixing Core Systems...")
        
        # Core system files
        core_files = [
            "core/soulos/soulos.py",
            "core/soulpack/crdt.py",
            "core/sdl/consolidator.py",
            "core/digilang/bytecode.py",
            "infrastructure/tests/test_revolutionary.py",
            "infrastructure/tests/test_silicon_valley.py",
            "infrastructure/launchers/digimundo_unified.sh",
        ]
        
        for file_path in core_files:
            full_path = self.base_path / file_path
            if full_path.exists():
                if full_path.suffix == '.py':
                    self.fix_python_imports(full_path)
                elif full_path.suffix == '.sh':
                    self.fix_shell_scripts(full_path)
    
    def scan_and_fix_all(self):
        """Escaneia e corrige todos os arquivos"""
        print("""
╔══════════════════════════════════════════════════════════════╗
║     🔧 FIXING ALL PATHS AFTER REORGANIZATION                 ║
╚══════════════════════════════════════════════════════════════╝
        """)
        
        # Categories to scan
        categories = [
            ("core", "**/*.py"),
            ("infrastructure", "**/*.py"),
            ("infrastructure", "**/*.sh"),
            ("systems", "**/*.py"),
            ("systems", "**/*.sh"),
            ("development", "**/*.py"),
            ("research", "**/*.py"),
            ("integrations", "**/*.py"),
            ("digimons/scripturemon", "**/*.py"),
            ("digimons/sabiamon", "**/*.py"),
        ]
        
        total_fixes = 0
        
        for category, pattern in categories:
            category_path = self.base_path / category
            if category_path.exists():
                print(f"\n📁 Scanning {category}/{pattern}...")
                
                for file_path in category_path.glob(pattern):
                    if file_path.is_file():
                        if file_path.suffix == '.py':
                            fixes = self.fix_python_imports(file_path)
                            total_fixes += fixes
                        elif file_path.suffix == '.sh':
                            fixes = self.fix_shell_scripts(file_path)
                            total_fixes += fixes
        
        return total_fixes
    
    def create_fixes_report(self):
        """Cria relatório de correções"""
        report = {
            "timestamp": datetime.now().isoformat(),
            "files_fixed": self.files_fixed,
            "total_fixes": len(self.fixes_applied),
            "errors": len(self.errors),
            "fixes_by_type": {},
            "fixes_applied": self.fixes_applied,
            "errors_detail": self.errors
        }
        
        # Count by type
        for fix in self.fixes_applied:
            fix_type = fix["type"]
            if fix_type not in report["fixes_by_type"]:
                report["fixes_by_type"][fix_type] = 0
            report["fixes_by_type"][fix_type] += 1
        
        # Save report
        report_file = self.base_path / "PATH_FIXES_REPORT.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        return report
    
    def execute(self):
        """Executa correção completa"""
        
        # 1. Fix core systems first
        self.fix_core_systems()
        
        # 2. Scan and fix all
        total_fixes = self.scan_and_fix_all()
        
        # 3. Create report
        report = self.create_fixes_report()
        
        # 4. Display summary
        print("\n" + "="*60)
        print("📊 PATH FIXING REPORT")
        print("="*60)
        print(f"""
✅ Successfully fixed:
   • Files modified: {self.files_fixed}
   • Total fixes applied: {len(self.fixes_applied)}
   • Errors encountered: {len(self.errors)}

📋 Fixes by type:""")
        
        for fix_type, count in report["fixes_by_type"].items():
            print(f"   • {fix_type}: {count}")
        
        if self.errors:
            print("\n⚠️ Errors:")
            for error in self.errors[:5]:
                print(f"   • {error}")
        
        print(f"\nReport saved: PATH_FIXES_REPORT.json")
        
        print("""
╔══════════════════════════════════════════════════════════════╗
║     ✅ PATH FIXING COMPLETE!                                 ║
║     All references have been updated                         ║
╚══════════════════════════════════════════════════════════════╝
        """)

from datetime import datetime

def main():
    fixer = PathFixer()
    fixer.execute()

if __name__ == "__main__":
    main()