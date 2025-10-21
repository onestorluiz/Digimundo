from pathlib import Path
def test_window_packer_script_exists():
    assert Path("scripts/window_packer.py").exists()