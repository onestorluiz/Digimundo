import re
from pathlib import Path

def test_screenplay_headers_exist():
    files = list(Path("data/screenplay_synth").rglob("*.txt"))
    assert files, "no screenplay_synth files"
    sample = files[0].read_text(encoding="utf-8", errors="ignore")
    assert re.search(r"^(INT\.|EXT\.) [A-Z0-9 _]+ - (DAY|NIGHT|DAWN|DUSK)$", sample, re.M), "no canonical headers found"