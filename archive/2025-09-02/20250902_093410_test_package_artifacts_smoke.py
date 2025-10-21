from pathlib import Path
def test_package_script_exists():
    assert Path("scripts/package_artifacts.py").exists()