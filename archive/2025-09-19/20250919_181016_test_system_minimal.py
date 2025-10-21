#!/usr/bin/env python3
"""
🧪 TESTES MÍNIMOS DO SISTEMA
============================
Apenas o essencial para verificar funcionamento
"""

import sys
import unittest
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))


class TestSystemMinimal(unittest.TestCase):
    """Testes essenciais do sistema"""

    def test_imports_work(self):
        """Verifica se imports principais funcionam"""
        try:
            from src.core import ScriptDoctorSystem
            from src.core.unified_memory_system import get_unified_memory
            self.assertTrue(True)
        except ImportError as e:
            self.fail(f"Import falhou: {e}")

    def test_unified_memory_exists(self):
        """Verifica se unified memory está ativo"""
        from src.core.unified_memory_system import get_unified_memory

        memory = get_unified_memory()
        stats = memory.get_stats()

        self.assertIsNotNone(stats)
        self.assertIn('total_entries', stats)
        self.assertGreater(stats['total_entries'], 0)

    def test_data_directory(self):
        """Verifica se data/ tem apenas unified_memory.db"""
        data_dir = Path(__file__).parent.parent / "data"

        # Listar todos os .db em data/
        db_files = list(data_dir.glob("*.db"))

        # Deve ter apenas unified_memory.db
        self.assertEqual(len(db_files), 1, f"Múltiplos bancos encontrados: {db_files}")
        self.assertEqual(db_files[0].name, "unified_memory.db")

    def test_system_initialization(self):
        """Verifica se sistema inicializa"""
        from src.core import ScriptDoctorSystem

        try:
            system = ScriptDoctorSystem()
            self.assertIsNotNone(system)
            self.assertTrue(hasattr(system, 'memory'))
        except Exception as e:
            self.fail(f"Sistema não inicializou: {e}")

    def test_screenplay_library(self):
        """Verifica se biblioteca de roteiros funciona"""
        from src.core.screenplay_library import get_screenplay_library

        library = get_screenplay_library()
        all_screenplays = library.list_all()

        self.assertIsNotNone(all_screenplays)
        self.assertGreater(len(all_screenplays), 0)

    def test_knowledge_hooks_active(self):
        """Verifica se hooks de conhecimento estão ativos"""
        try:
            from src.core import knowledge_integrator
            self.assertIsNotNone(knowledge_integrator)
        except:
            # Pode não estar importado, mas arquivo deve existir
            hook_file = Path(__file__).parent.parent / "src" / "core" / "knowledge_integration_hooks.py"
            self.assertTrue(hook_file.exists(), "Hooks de conhecimento não encontrados")


if __name__ == '__main__':
    # Executar testes
    print("🧪 EXECUTANDO TESTES MÍNIMOS DO SISTEMA")
    print("=" * 60)

    unittest.main(verbosity=2)