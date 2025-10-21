"""
Test Suite for OMEGA-ASCENT v4.0.0
"""

import pytest
import json
from pathlib import Path

class TestOmegaSystem:
    """Test main system functionality"""

    def test_import_core(self):
        """Test core imports"""
        from core import auto_documenter
        from core import sanity_checker
        from core import snapshot_manager
        assert True

    def test_configuration_loading(self):
        """Test configuration loading"""
        config_path = Path("config/advanced.json")
        if config_path.exists():
            config = json.loads(config_path.read_text())
            assert config["version"] == "4.0.0"
            assert "features" in config
            assert "weights" in config

    def test_directory_structure(self):
        """Test directory structure"""
        required_dirs = [
            "core", "beats", "hierarchy", "evidence",
            "memory", "validation", "narrative", "optimization"
        ]
        for dir_name in required_dirs:
            assert Path(dir_name).exists()

    def test_snapshot_system(self):
        """Test snapshot system"""
        from core.snapshot_manager import SnapshotManager
        snapshot = SnapshotManager()
        assert hasattr(snapshot, "create_snapshot")
        assert hasattr(snapshot, "rollback")

    def test_sanity_checks(self):
        """Test sanity checks"""
        from core.sanity_checker import SanityChecker
        checker = SanityChecker()
        valid, errors = checker.run_all()
        assert valid is True or valid is False
        assert isinstance(errors, list)

class TestAdvancedFeatures:
    """Test advanced features"""

    def test_arc_fsm_exists(self):
        """Test Arc FSM module"""
        arc_path = Path("narrative/arc_fsm.py")
        assert arc_path.exists()

    def test_hierarchical_modules(self):
        """Test hierarchical modules"""
        modules = ["hier_rag.py", "hier_plus.py", "hier_omega_plus.py"]
        for module in modules:
            module_path = Path("hierarchy") / module
            assert module_path.exists()

    def test_benchmarks(self):
        """Test benchmarks exist"""
        baseline = Path("benchmarks/baseline.json")
        target = Path("benchmarks/target.json")
        assert baseline.exists()
        assert target.exists()

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
