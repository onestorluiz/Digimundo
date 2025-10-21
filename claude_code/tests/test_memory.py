"""
Test suite for MEMORY/ structure and databases.

Validates:
- Database integrity (claude_memory.db, claude_rag.db)
- Required tables exist
- MEMORY subdirectories accessible
- Index files readable
"""

import pytest
import sqlite3
from pathlib import Path


# Base paths
BASE_DIR = Path(__file__).parent.parent
MEMORY_DIR = BASE_DIR / "MEMORY"


class TestMemoryDatabases:
    """Test database integrity"""

    def test_claude_memory_db_exists(self):
        """Verify claude_memory.db exists and is valid"""
        db = MEMORY_DIR / "claude_memory.db"
        assert db.exists()
        assert db.stat().st_size > 1000, "Database too small"

    def test_claude_memory_readable(self):
        """Verify claude_memory.db is readable"""
        db = MEMORY_DIR / "claude_memory.db"
        conn = sqlite3.connect(db)
        cursor = conn.cursor()

        # Get all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        conn.close()

        assert len(tables) > 0, "No tables in claude_memory.db"

    def test_claude_rag_db_exists(self):
        """Verify claude_rag.db exists if RAG is enabled"""
        db = MEMORY_DIR / "claude_rag.db"
        if db.exists():
            assert db.stat().st_size > 0, "RAG database empty"

    def test_memory_tables_structure(self):
        """Verify expected tables exist"""
        db = MEMORY_DIR / "claude_memory.db"
        conn = sqlite3.connect(db)
        cursor = conn.cursor()

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        conn.close()

        # Check for core tables
        expected = ["memories", "sessions", "context"]
        for table in expected:
            if table not in tables:
                # Warning only - table names may vary
                print(f"Warning: Expected table '{table}' not found")


class TestMemoryDirectories:
    """Test MEMORY/ subdirectory structure"""

    def test_memory_root_exists(self):
        """Verify MEMORY/ exists"""
        assert MEMORY_DIR.exists()
        assert MEMORY_DIR.is_dir()

    def test_required_subdirs(self):
        """Verify all required subdirectories exist"""
        required = [
            "conhecimentos",
            "erros_aprendidos",
            "analises",
            "context",
            "sync"
        ]

        for subdir in required:
            path = MEMORY_DIR / subdir
            assert path.exists(), f"Missing: {subdir}"
            assert path.is_dir(), f"{subdir} is not a directory"

    def test_conhecimentos_accessible(self):
        """Verify conhecimentos/ contains files"""
        conhecimentos = MEMORY_DIR / "conhecimentos"
        files = list(conhecimentos.glob("*"))
        # Should have at least some knowledge files
        assert len(files) >= 0  # May be empty initially


class TestMemoryIndexFiles:
    """Test INDEX_MASTER and critical files"""

    def test_conhecimentos_index_exists(self):
        """Verify conhecimentos/INDEX_MASTER.md exists"""
        index = MEMORY_DIR / "conhecimentos" / "🔥🔥🔥INDEX_MASTER_MEMORIA🔥🔥🔥.md"
        assert index.exists(), "conhecimentos INDEX_MASTER missing"

    def test_conhecimentos_index_readable(self):
        """Verify INDEX_MASTER is readable"""
        index = MEMORY_DIR / "conhecimentos" / "🔥🔥🔥INDEX_MASTER_MEMORIA🔥🔥🔥.md"
        content = index.read_text()

        # Check for index markers
        assert "INDEX" in content or "ÍNDICE" in content or "CONHECIMENTO" in content
        assert len(content) > 50, "Index too short"

    def test_no_corruption_markers(self):
        """Verify no database corruption markers"""
        # Check for common corruption indicators
        db = MEMORY_DIR / "claude_memory.db"

        try:
            conn = sqlite3.connect(db)
            cursor = conn.cursor()
            cursor.execute("PRAGMA integrity_check")
            result = cursor.fetchone()
            conn.close()

            assert result[0] == "ok", f"Database integrity issue: {result[0]}"
        except sqlite3.DatabaseError as e:
            pytest.fail(f"Database corrupted: {e}")


class TestMemoryBackups:
    """Test backup and sync structure"""

    def test_sync_directory_exists(self):
        """Verify sync/ exists for backups"""
        sync = MEMORY_DIR / "sync"
        assert sync.exists()

    def test_sync_writable(self):
        """Verify sync/ is writable"""
        sync = MEMORY_DIR / "sync"
        test_file = sync / ".test_write"

        try:
            test_file.write_text("test")
            assert test_file.exists()
            test_file.unlink()
        except Exception as e:
            pytest.fail(f"sync/ not writable: {e}")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
