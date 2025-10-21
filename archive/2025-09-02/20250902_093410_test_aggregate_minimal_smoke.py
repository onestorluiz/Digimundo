from pathlib import Path
def test_aggregate_script_exists():
    assert Path("scripts/aggregate_minimal_results.py").exists()