from pathlib import Path
def test_package_release_script_exists():
    assert Path("scripts/package_release_bundle.py").exists()