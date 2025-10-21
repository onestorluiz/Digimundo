"""
Test suite for claude_code structure integrity.

Validates:
- Critical paths exist
- Required directories present
- LEIS and BEHAVIORAL_HACKS complete
- No broken references
"""

import pytest
from pathlib import Path


# Base path
BASE_DIR = Path(__file__).parent.parent


class TestCriticalPaths:
    """Test all critical paths referenced in REGRAS.md"""

    def test_start_scripts_exist(self):
        """Verify START_*.sh scripts exist"""
        assert (BASE_DIR / "START_GENJUTSU.sh").exists()
        assert (BASE_DIR / "START_UCHIMON.sh").exists()

    def test_livro_claude_exists(self):
        """Verify livro_claude/ directory exists"""
        livro = BASE_DIR / "livro_claude"
        assert livro.exists()
        assert livro.is_dir()

    def test_livro_claude_subdirs(self):
        """Verify livro_claude/ has required subdirectories"""
        livro = BASE_DIR / "livro_claude"
        assert (livro / "CAPITULOS").exists()
        assert (livro / "CONHECIMENTO").exists()
        assert (livro / "DIARIO").exists()
        assert (livro / "MEMORIA").exists()

    def test_memory_database_exists(self):
        """Verify MEMORY/claude_memory.db exists"""
        db = BASE_DIR / "MEMORY" / "claude_memory.db"
        assert db.exists()
        assert db.stat().st_size > 1000, "Database too small"

    def test_memory_subdirs(self):
        """Verify MEMORY/ has required subdirectories"""
        memory = BASE_DIR / "MEMORY"
        required = [
            "conhecimentos",
            "erros_aprendidos",
            "analises",
            "context",
            "sync"
        ]
        for subdir in required:
            assert (memory / subdir).exists(), f"Missing: {subdir}"

    def test_systems_directory(self):
        """Verify systems/ exists with Python files"""
        systems = BASE_DIR / "systems"
        assert systems.exists()

        py_files = list(systems.glob("*.py"))
        assert len(py_files) >= 10, f"Expected 10+ Python files, found {len(py_files)}"

    def test_unified_memory_system_path(self):
        """Verify unified_memory_system.py is in correct location"""
        correct_path = BASE_DIR / "systems" / "unified_memory_system.py"
        assert correct_path.exists(), "unified_memory_system.py not in systems/"

        wrong_path = BASE_DIR / "MEMORY" / "UNIFIED_MEMORY_SYSTEM.py"
        assert not wrong_path.exists(), "Old path still exists!"


class TestLeis:
    """Test LEIS_UCHIMON structure"""

    def test_leis_directory_exists(self):
        """Verify LEIS_UCHIMON/ exists"""
        leis = BASE_DIR / "🔥LEIS_UCHIMON🔥"
        assert leis.exists()
        assert leis.is_dir()

    def test_leis_count(self):
        """Verify expected number of leis"""
        leis = BASE_DIR / "🔥LEIS_UCHIMON🔥"
        md_files = list(leis.glob("*.md"))
        assert len(md_files) >= 17, f"Expected 17+ leis, found {len(md_files)}"

    def test_critical_leis_exist(self):
        """Verify critical leis exist"""
        leis = BASE_DIR / "🔥LEIS_UCHIMON🔥"
        critical = [
            "🔥🔥🔥00_LER_TUDO🔥🔥🔥.md",
            "🔥🔥🔥15_VERIFICAR_ANTES_DE_CRIAR🔥🔥🔥.md",
            "🔥🔥🔥INDEX_MASTER🔥🔥🔥.md"
        ]
        for lei in critical:
            assert (leis / lei).exists(), f"Missing critical lei: {lei}"

    def test_index_master_readable(self):
        """Verify INDEX_MASTER is readable"""
        index = BASE_DIR / "🔥LEIS_UCHIMON🔥" / "🔥🔥🔥INDEX_MASTER🔥🔥🔥.md"
        content = index.read_text()
        assert "ÍNDICE" in content or "INDEX" in content
        assert len(content) > 100


class TestBehavioralHacks:
    """Test BEHAVIORAL_HACKS structure"""

    def test_behavioral_hacks_exists(self):
        """Verify BEHAVIORAL_HACKS/ exists"""
        hacks = BASE_DIR / "🔥🔥🔥BEHAVIORAL_HACKS🔥🔥🔥"
        assert hacks.exists()
        assert hacks.is_dir()

    def test_behavioral_hacks_count(self):
        """Verify expected number of behavioral hack files"""
        hacks = BASE_DIR / "🔥🔥🔥BEHAVIORAL_HACKS🔥🔥🔥"
        md_files = list(hacks.glob("*.md"))
        assert len(md_files) >= 5, f"Expected 5+ hack files, found {len(md_files)}"

    def test_index_master_hack_exists(self):
        """Verify behavioral hacks INDEX_MASTER exists"""
        index = BASE_DIR / "🔥🔥🔥BEHAVIORAL_HACKS🔥🔥🔥" / "🔥00_INDEX_MASTER🔥.md"
        assert index.exists()


class TestDocsStructure:
    """Test docs/ structure"""

    def test_docs_directory_exists(self):
        """Verify docs/ exists"""
        docs = BASE_DIR / "docs"
        assert docs.exists()
        assert docs.is_dir()

    def test_docs_plans_exists(self):
        """Verify docs/plans/ exists with content"""
        plans = BASE_DIR / "docs" / "plans"
        assert plans.exists()

        md_files = list(plans.glob("*.md"))
        assert len(md_files) >= 6, f"Expected 6+ plan files, found {len(md_files)}"

    def test_major_plans_exist(self):
        """Verify major planning documents exist"""
        plans = BASE_DIR / "docs" / "plans"
        major = [
            "PLANO_DUAL_CORE_ARCHITECTURE.md",
            "SCRIPT_DOCTOR_MASTER_PLAN.md"
        ]
        for plan in major:
            assert (plans / plan).exists(), f"Missing plan: {plan}"


class TestRootFiles:
    """Test root directory structure"""

    def test_gitignore_exists(self):
        """Verify .gitignore was created"""
        gitignore = BASE_DIR / ".gitignore"
        assert gitignore.exists()

        content = gitignore.read_text()
        assert "__pycache__" in content
        assert "*.pyc" in content

    def test_regras_exists(self):
        """Verify REGRAS.md exists in root"""
        regras = BASE_DIR / "REGRAS.md"
        assert regras.exists()

    def test_no_pycache_committed(self):
        """Verify no __pycache__ directories exist (outside venv and tests)"""
        pycache_dirs = [
            p for p in BASE_DIR.rglob("__pycache__")
            if "venv" not in str(p) and "tests" not in str(p) and "systems" not in str(p)
        ]
        # Accept __pycache__ in tests/ and systems/ since they're runtime-generated
        assert len(pycache_dirs) == 0, f"Found __pycache__ directories: {pycache_dirs}"


class TestNoSimplesDuplication:
    """Test that LIVRO_CLAUDE/SIMPLES was properly removed"""

    def test_simples_deleted(self):
        """Verify SIMPLES/ folder no longer exists"""
        simples = BASE_DIR / "LIVRO_CLAUDE" / "SIMPLES"
        assert not simples.exists(), "SIMPLES/ still exists - should be deleted"

        simples_lower = BASE_DIR / "livro_claude" / "SIMPLES"
        assert not simples_lower.exists(), "SIMPLES/ still exists in livro_claude"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
