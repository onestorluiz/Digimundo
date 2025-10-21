#!/usr/bin/env python3
"""
🔧 FIX SHELL PATHS - Corrige caminhos em scripts Shell
"""

import os
import re
from pathlib import Path
from typing import Dict, List

def fix_shell_scripts():
    """Corrige caminhos em scripts Shell críticos"""
    
    base_path = Path("/Users/clubproducoes/Digimundo")
    fixes_applied = []
    
    # Scripts críticos para verificar
    critical_scripts = [
        "systems/launchers/DIGIMUNDO_SUPREME_LAUNCHER.sh",
        "systems/launchers/DIGIMUNDO_ULTIMATE_LAUNCHER.sh",
        "systems/launchers/DIGIMUNDO_TRANSCENDENT.sh",
        "development/scripts/test_integration.sh",
        "utilities/maintenance/cleanup.sh",
    ]
    
    # Mapeamento de correções
    path_fixes = {
        # Python scripts movidos
        "python3 SOULOS_IMPLEMENTATION.py": "python3 core/soulos/soulos.py",
        "python3 SOULPACK_CRDT.py": "python3 core/soulpack/crdt.py",
        "python3 SDL_SELF_DISTILL.py": "python3 core/sdl/consolidator.py",
        "python3 DIGILANG_BYTECODE.py": "python3 core/digilang/bytecode.py",
        "python3 TEST_REVOLUTIONARY_SYSTEMS.py": "python3 systems/evolution/TEST_REVOLUTIONARY_SYSTEMS.py",
        
        # Diretórios movidos
        "cd consciousness": "cd archive/consciousness",
        "cd genetic": "cd archive/genetic_old",
        "cd soulpacks": "cd archive/soulpacks_old",
        "./consciousness/": "./archive/consciousness/",
        "./genetic/": "./archive/genetic_old/",
        "./soulpacks/": "./archive/soulpacks_old/",
        
        # Modelfiles
        "scripturemon_immortal.modelfile": "archive/modelfiles/scripturemon_immortal.modelfile",
        "scripturemon_soulos.modelfile": "archive/modelfiles/scripturemon_soulos.modelfile",
        
        # Config files
        "CLAUDE.md": "config/claude_memory.md",
        "./CLAUDE.md": "./config/claude_memory.md",
        
        # Paths para digimons
        "consciousness/scripturemon_memories.db": "digimons/scripturemon/memory/crystals.db",
        "consciousness/sabiamon_memories.db": "digimons/sabiamon/memory/crystals.db",
    }
    
    # Processa cada script
    for script_path in critical_scripts:
        full_path = base_path / script_path
        if full_path.exists():
            print(f"Checking {script_path}...")
            
            try:
                content = full_path.read_text()
                original_content = content
                fixes_count = 0
                
                # Aplica correções
                for old_path, new_path in path_fixes.items():
                    if old_path in content:
                        content = content.replace(old_path, new_path)
                        fixes_count += 1
                        fixes_applied.append({
                            "file": script_path,
                            "old": old_path,
                            "new": new_path
                        })
                
                # Corrige imports de Python em scripts
                python_imports = [
                    ("from SOULOS_IMPLEMENTATION", "from core.soulos.soulos"),
                    ("from SOULPACK_CRDT", "from core.soulpack.crdt"),
                    ("from SDL_SELF_DISTILL", "from core.sdl.consolidator"),
                    ("from DIGILANG_BYTECODE", "from core.digilang.bytecode"),
                ]
                
                for old_import, new_import in python_imports:
                    pattern = f'python3 -c ".*{old_import}.*"'
                    if re.search(pattern, content):
                        content = re.sub(old_import, new_import, content)
                        fixes_count += 1
                
                # Salva se houve mudanças
                if content != original_content:
                    full_path.write_text(content)
                    print(f"  ✓ Fixed {fixes_count} issues in {script_path}")
                    
            except Exception as e:
                print(f"  ✗ Error fixing {script_path}: {e}")
    
    # Procura por outros scripts Shell com problemas
    print("\nScanning for other shell scripts...")
    
    for sh_file in base_path.glob("**/*.sh"):
        # Pula arquivos em archive e backups
        if "archive" in str(sh_file) or "backup" in str(sh_file):
            continue
            
        try:
            content = sh_file.read_text()
            
            # Verifica se tem referências antigas
            old_refs = [
                "SOULOS_IMPLEMENTATION.py",
                "SOULPACK_CRDT.py",
                "SDL_SELF_DISTILL.py",
                "DIGILANG_BYTECODE.py",
                "consciousness/",
                "genetic/",
                "soulpacks/"
            ]
            
            has_old_refs = any(ref in content for ref in old_refs)
            
            if has_old_refs:
                print(f"  Found old references in: {sh_file.relative_to(base_path)}")
                
                # Aplica correções
                original_content = content
                for old_path, new_path in path_fixes.items():
                    if old_path in content:
                        content = content.replace(old_path, new_path)
                
                if content != original_content:
                    sh_file.write_text(content)
                    print(f"    ✓ Fixed")
                    
        except:
            pass
    
    return fixes_applied

def create_launcher_symlinks():
    """Cria symlinks para launchers principais na raiz"""
    
    base_path = Path("/Users/clubproducoes/Digimundo")
    
    # Launchers principais
    launchers = {
        "LAUNCH_DIGIMUNDO.sh": "systems/launchers/DIGIMUNDO_SUPREME_LAUNCHER.sh",
        "START_SABIAMON.sh": "systems/activation/START_SABIAMON_24_7.sh",
        "TEST_SYSTEMS.sh": "development/tests/test_all_systems.sh",
    }
    
    for symlink_name, target in launchers.items():
        symlink_path = base_path / symlink_name
        target_path = base_path / target
        
        if target_path.exists() and not symlink_path.exists():
            try:
                symlink_path.symlink_to(target_path)
                print(f"✓ Created symlink: {symlink_name} -> {target}")
            except:
                pass

def main():
    print("""
╔══════════════════════════════════════════════════════════════╗
║     🔧 FIXING SHELL SCRIPT PATHS                             ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    fixes = fix_shell_scripts()
    
    print(f"\n✅ Fixed {len(fixes)} path references in shell scripts")
    
    print("\n📎 Creating convenience symlinks...")
    create_launcher_symlinks()
    
    print("""
╔══════════════════════════════════════════════════════════════╗
║     ✅ SHELL PATH FIXING COMPLETE!                           ║
╚══════════════════════════════════════════════════════════════╝
    """)

if __name__ == "__main__":
    main()