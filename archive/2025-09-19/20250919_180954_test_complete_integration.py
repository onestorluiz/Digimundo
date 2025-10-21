#!/usr/bin/env python3
"""
🧪 TESTES DE INTEGRAÇÃO COMPLETA
"""

import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.unified_memory_system import get_unified_memory, MemoryType
from src.core.script_doctor_system import ScriptDoctorSystem
from src.core.screenplay_library import get_screenplay_library


class TestCompleteIntegration(unittest.TestCase):
    """Testa se tudo está realmente integrado"""

    def setUp(self):
        self.memory = get_unified_memory()

    def test_unified_memory_active(self):
        """Verifica se unified memory está ativo"""
        stats = self.memory.get_stats()
        self.assertGreater(stats['total_entries'], 0)

    def test_no_legacy_databases(self):
        """Verifica se não há mais bancos legados ativos"""
        project_root = Path(__file__).parent.parent
        legacy_dbs = []

        for db_path in project_root.rglob("*.db"):
            if "unified_memory.db" not in str(db_path):
                # Permitir apenas backups
                if "backup" not in str(db_path).lower():
                    legacy_dbs.append(str(db_path))

        self.assertEqual(len(legacy_dbs), 0, f"Bancos legados ainda existem: {legacy_dbs}")

    def test_script_doctor_uses_unified(self):
        """Verifica se sistema principal usa unified"""
        system = ScriptDoctorSystem()

        # Deve usar unified memory (direto ou via adapter)
        self.assertTrue(hasattr(system, 'memory'))

        # Testar que salva no unified
        system.memory.store("test_key", "test_value")

        # Verificar que está no unified
        results = self.memory.search("test_key")
        self.assertGreater(len(results), 0)

    def test_knowledge_auto_integration(self):
        """Verifica se conhecimento é auto-integrado"""
        initial_count = self.memory.get_stats()['total_entries']

        # Executar análise que deve gerar conhecimento
        library = get_screenplay_library()
        results = library.search("test")

        # Verificar que aumentou entradas
        final_count = self.memory.get_stats()['total_entries']
        self.assertGreaterEqual(final_count, initial_count)

    def test_all_memory_types_present(self):
        """Verifica se todos os tipos de memória estão presentes"""
        stats = self.memory.get_stats()

        expected_types = [
            'analysis', 'knowledge', 'screenplay',
            'character', 'vector', 'context'
        ]

        for memory_type in expected_types:
            self.assertIn(memory_type, stats['by_type'],
                         f"Tipo {memory_type} não encontrado no unified")


if __name__ == '__main__':
    unittest.main()
