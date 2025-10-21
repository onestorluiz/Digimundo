#!/usr/bin/env python3
"""
🔧 ATUALIZA SISTEMA PRINCIPAL PARA UNIFIED MEMORY
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))


def update_script_doctor():
    """Atualiza script_doctor_system.py para usar unified memory"""

    file_path = Path(__file__).parent.parent / "src" / "core" / "script_doctor_system.py"

    if not file_path.exists():
        print("❌ script_doctor_system.py não encontrado")
        return False

    content = file_path.read_text()

    # Substituições necessárias
    replacements = [
        # Import
        (
            "from .omnimemory_v5_minimal import OmniMemoryV5",
            "from .unified_memory_system import get_unified_memory"
        ),
        # Inicialização
        (
            "self.memory = OmniMemoryV5(db_path=self.config.memory_db_path)",
            "self.memory = get_unified_memory()  # Unified memory direto!"
        ),
        # Fallback
        (
            "# Fallback para OmniMemory V5",
            "# Usando Unified Memory System"
        ),
    ]

    modified = False
    for old, new in replacements:
        if old in content:
            content = content.replace(old, new)
            modified = True
            print(f"✅ Substituído: {old[:30]}...")

    if modified:
        # Backup
        backup = file_path.with_suffix('.py.backup')
        file_path.rename(backup)

        # Salvar novo
        file_path.write_text(content)
        print(f"✅ Sistema principal atualizado para unified memory")
        print(f"📦 Backup salvo em: {backup}")
        return True
    else:
        print("⚠️ Sistema já está usando unified memory ou estrutura diferente")
        return False


if __name__ == "__main__":
    update_script_doctor()
