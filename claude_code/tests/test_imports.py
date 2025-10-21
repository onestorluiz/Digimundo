"""
Test suite for Python imports in systems/.

Validates:
- All Python modules are importable
- No syntax errors
- No circular imports
- Critical classes/functions exist
"""

import pytest
import sys
from pathlib import Path
import importlib.util


# Base paths
BASE_DIR = Path(__file__).parent.parent
SYSTEMS_DIR = BASE_DIR / "systems"


class TestSystemsImports:
    """Test all Python files in systems/ are importable"""

    @pytest.fixture(autouse=True)
    def setup_path(self):
        """Add systems/ to Python path"""
        if str(SYSTEMS_DIR) not in sys.path:
            sys.path.insert(0, str(SYSTEMS_DIR))
        yield
        # Cleanup handled by pytest

    def test_unified_memory_system_importable(self):
        """Test unified_memory_system.py can be imported"""
        try:
            import unified_memory_system
            assert unified_memory_system is not None
        except Exception as e:
            pytest.fail(f"Failed to import unified_memory_system: {e}")

    def test_unified_archive_manager_importable(self):
        """Test unified_archive_manager.py can be imported"""
        try:
            import unified_archive_manager
            assert unified_archive_manager is not None
        except Exception as e:
            pytest.fail(f"Failed to import unified_archive_manager: {e}")

    def test_uchimon_behavioral_core_importable(self):
        """Test uchimon_behavioral_core.py can be imported"""
        try:
            import uchimon_behavioral_core
            assert uchimon_behavioral_core is not None
        except Exception as e:
            pytest.fail(f"Failed to import uchimon_behavioral_core: {e}")

    def test_digimundo_orchestrator_importable(self):
        """Test digimundo_orchestrator.py can be imported"""
        try:
            import digimundo_orchestrator
            assert digimundo_orchestrator is not None
        except Exception as e:
            pytest.fail(f"Failed to import digimundo_orchestrator: {e}")

    def test_claude_rag_importable(self):
        """Test claude_rag.py can be imported"""
        try:
            import claude_rag
            assert claude_rag is not None
        except Exception as e:
            pytest.fail(f"Failed to import claude_rag: {e}")

    def test_hook_registry_importable(self):
        """Test hook_registry.py can be imported"""
        try:
            import hook_registry
            assert hook_registry is not None
        except Exception as e:
            pytest.fail(f"Failed to import hook_registry: {e}")


class TestNoSyntaxErrors:
    """Test all Python files compile without syntax errors"""

    def test_all_python_files_compile(self):
        """Verify all .py files in systems/ have valid syntax"""
        python_files = list(SYSTEMS_DIR.glob("*.py"))
        errors = []

        for py_file in python_files:
            try:
                spec = importlib.util.spec_from_file_location(
                    py_file.stem, py_file
                )
                if spec and spec.loader:
                    # Only compile, don't execute
                    code = compile(
                        py_file.read_text(),
                        str(py_file),
                        'exec'
                    )
                    assert code is not None
            except SyntaxError as e:
                errors.append(f"{py_file.name}: {e}")

        if errors:
            pytest.fail(f"Syntax errors found:\n" + "\n".join(errors))


class TestSystemsDirectory:
    """Test systems/ directory structure"""

    def test_systems_directory_exists(self):
        """Verify systems/ directory exists"""
        assert SYSTEMS_DIR.exists()
        assert SYSTEMS_DIR.is_dir()

    def test_minimum_python_files(self):
        """Verify minimum expected Python files exist"""
        python_files = list(SYSTEMS_DIR.glob("*.py"))
        assert len(python_files) >= 10, f"Expected 10+ Python files, found {len(python_files)}"

    def test_genjutsu_subdir_exists(self):
        """Verify genjutsu/ subdirectory exists"""
        genjutsu = SYSTEMS_DIR / "genjutsu"
        assert genjutsu.exists(), "genjutsu/ subdirectory missing"


class TestCriticalModules:
    """Test critical modules have expected structure"""

    @pytest.fixture(autouse=True)
    def setup_path(self):
        """Add systems/ to Python path"""
        if str(SYSTEMS_DIR) not in sys.path:
            sys.path.insert(0, str(SYSTEMS_DIR))
        yield

    def test_unified_memory_has_required_imports(self):
        """Verify unified_memory_system has required dependencies"""
        module_path = SYSTEMS_DIR / "unified_memory_system.py"
        content = module_path.read_text()

        # Check for critical imports
        assert "import sqlite3" in content
        assert "from pathlib import Path" in content
        assert "from datetime import datetime" in content

    def test_no_livro_claude_uppercase_refs(self):
        """Verify no references to LIVRO_CLAUDE (uppercase) in Python"""
        python_files = list(SYSTEMS_DIR.glob("*.py"))

        for py_file in python_files:
            content = py_file.read_text()
            if "LIVRO_CLAUDE" in content:
                pytest.fail(f"{py_file.name} still references LIVRO_CLAUDE (should be livro_claude)")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
