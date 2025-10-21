"""Legacy bootstrap placeholder."""
import yaml, structlog
from pathlib import Path

log = structlog.get_logger()

def bootstrap(dna_path: Path):
    if not dna_path.exists():
        log.warning('dna_missing', path=str(dna_path))
        return {}
    data = yaml.safe_load(dna_path.read_text())
    log.info('bootstrap_loaded', data=data)
    return data