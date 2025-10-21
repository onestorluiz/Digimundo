from pathlib import Path

def test_plot_roundtrip_script_exists():
    assert Path("scripts/plot_roundtrip.py").exists()