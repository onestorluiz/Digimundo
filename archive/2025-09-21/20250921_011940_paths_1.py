from pathlib import Path

# Resolve o raiz do projeto a partir deste arquivo
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
MEMORY_DIR = DATA_DIR / "memory"
MEMORY_DIR.mkdir(parents=True, exist_ok=True)

MEMORY_DB = MEMORY_DIR / "unified.db"
