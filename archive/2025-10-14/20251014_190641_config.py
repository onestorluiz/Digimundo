#!/usr/bin/env python3
"""
SCRIPTUREMON CONFIGURATION
Configuração centralizada com paths relativos
"""

import os
from pathlib import Path

# ========== PATHS ==========
# Base directory (parent of core/)
BASE_DIR = Path(__file__).parent.parent

# Core directories
CORE_DIR = BASE_DIR / "core"
SPECIALISTS_DIR = BASE_DIR / "specialists"
MODELFILES_DIR = SPECIALISTS_DIR / "modelfiles"
MEMORY_DIR = BASE_DIR / "memory"
WORKSPACE_DIR = BASE_DIR / "workspace"
TESTS_DIR = BASE_DIR / "tests"
DOCS_DIR = BASE_DIR / "docs"

# Memory subdirectories
DB_DIR = MEMORY_DIR / "database"
EXPORTS_DIR = MEMORY_DIR / "exports"
BACKUPS_DIR = MEMORY_DIR / "backups"

# Workspace subdirectories
INPUTS_DIR = WORKSPACE_DIR / "inputs"
OUTPUTS_DIR = WORKSPACE_DIR / "outputs"
TEMP_DIR = WORKSPACE_DIR / "temp"

# Database
DB_PATH = DB_DIR / "scripturemon.db"

# ========== MODELS ==========
# Ollama models (can be overridden by environment variables)
ORCHESTRATOR_MODEL = os.getenv(
    "SCRIPTUREMON_ORCHESTRATOR_MODEL",
    "mixtral:8x7b-instruct-v0.1-q5_K_M"
)

EVALUATOR_MODEL = os.getenv(
    "SCRIPTUREMON_EVALUATOR_MODEL",
    "llama3.1:70b-instruct-q4_K_M"
)

# Model parameters
MODEL_PARAMS = {
    "temperature": float(os.getenv("SCRIPTUREMON_TEMPERATURE", "0.7")),
    "top_p": float(os.getenv("SCRIPTUREMON_TOP_P", "0.9")),
    "num_predict": int(os.getenv("SCRIPTUREMON_NUM_PREDICT", "1500")),
    "num_ctx": int(os.getenv("SCRIPTUREMON_NUM_CTX", "32768"))
}

EVALUATOR_PARAMS = {
    "temperature": 0.7,
    "top_p": 0.9,
    "num_predict": 3000,
    "num_ctx": 131072
}

# ========== OLLAMA ==========
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_TIMEOUT = int(os.getenv("OLLAMA_TIMEOUT", "60"))
OLLAMA_TIMEOUT_EVALUATOR = int(os.getenv("OLLAMA_TIMEOUT_EVALUATOR", "180"))

# ========== GIT-MEMORY INTEGRATION ==========
# Enable Git-Memory Symbiosis (optional)
GIT_MEMORY_ENABLED = os.getenv("GIT_MEMORY_ENABLED", "true").lower() == "true"
GIT_AUTO_CAPTURE = os.getenv("GIT_AUTO_CAPTURE", "true").lower() == "true"
GIT_MEMORY_DIR = MEMORY_DIR / "git_sync"

# ========== SPECIALISTS ==========
# Lista ordenada dos 24 especialistas
SPECIALISTS = [
    "01_DIALOGUE",
    "02_CHARACTER",
    "03_PACING",
    "04_THEME",
    "05_ACTION",
    "06_STRUCTURE",
    "07_CONFLICT",
    "08_TENSION",
    "09_SUBTEXT",
    "10_EXPOSITION",
    "11_TRANSITIONS",
    "12_OPENING",
    "13_CLIMAX",
    "14_RESOLUTION",
    "15_WORLDBUILDING",
    "16_STAKES",
    "17_MOTIVATION",
    "18_BACKSTORY",
    "19_FORESHADOWING",
    "20_TWIST",
    "21_SYMBOLISM",
    "22_TONE",
    "23_GENRE",
    "24_CONTRAST"
]

# Mapeamento de especialistas para arquivos modelfile
SPECIALIST_MODELFILES = {
    "01_DIALOGUE": "01_dialogue.modelfile",
    "02_CHARACTER": "02_character.modelfile",
    "03_PACING": "03_pacing.modelfile",
    "04_THEME": "04_theme.modelfile",
    "05_ACTION": "05_action.modelfile",
    "06_STRUCTURE": "06_structure.modelfile",
    "07_CONFLICT": "07_conflict.modelfile",
    "08_TENSION": "08_tension.modelfile",
    "09_SUBTEXT": "09_subtext.modelfile",
    "10_EXPOSITION": "10_exposition.modelfile",
    "11_TRANSITIONS": "11_transitions.modelfile",
    "12_OPENING": "12_opening.modelfile",
    "13_CLIMAX": "13_climax.modelfile",
    "14_RESOLUTION": "14_resolution.modelfile",
    "15_WORLDBUILDING": "15_worldbuilding.modelfile",
    "16_STAKES": "16_stakes.modelfile",
    "17_MOTIVATION": "17_motivation.modelfile",
    "18_BACKSTORY": "18_backstory.modelfile",
    "19_FORESHADOWING": "19_foreshadowing.modelfile",
    "20_TWIST": "20_twist.modelfile",
    "21_SYMBOLISM": "21_symbolism.modelfile",
    "22_TONE": "22_tone.modelfile",
    "23_GENRE": "23_genre.modelfile",
    "24_CONTRAST": "24_contrast.modelfile"
}

# ========== LOGGING ==========
LOG_LEVEL = os.getenv("SCRIPTUREMON_LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"

# ========== MEMORY SETTINGS ==========
MEMORY_SEARCH_LIMIT = int(os.getenv("MEMORY_SEARCH_LIMIT", "5"))
MEMORY_CONTEXT_SIZE = int(os.getenv("MEMORY_CONTEXT_SIZE", "2000"))
ENABLE_MEMORY_ENRICHMENT = os.getenv("ENABLE_MEMORY_ENRICHMENT", "true").lower() == "true"

# ========== ANALYSIS MODES ==========
class AnalysisMode:
    QUICK = "QUICK"  # 5 especialistas essenciais
    STANDARD = "STANDARD"  # 12 especialistas principais
    COMPLETE = "COMPLETE"  # Todos os 24 especialistas

QUICK_SPECIALISTS = [
    "01_DIALOGUE",
    "02_CHARACTER",
    "06_STRUCTURE",
    "07_CONFLICT",
    "04_THEME"
]

STANDARD_SPECIALISTS = QUICK_SPECIALISTS + [
    "03_PACING",
    "08_TENSION",
    "09_SUBTEXT",
    "12_OPENING",
    "13_CLIMAX",
    "14_RESOLUTION",
    "23_GENRE"
]

# ========== VALIDATION ==========
def validate_config():
    """Valida se os diretórios necessários existem"""
    required_dirs = [
        DB_DIR,
        EXPORTS_DIR,
        BACKUPS_DIR,
        INPUTS_DIR,
        OUTPUTS_DIR,
        TEMP_DIR,
        MODELFILES_DIR
    ]

    for dir_path in required_dirs:
        dir_path.mkdir(parents=True, exist_ok=True)

    return True

# ========== EXPORT CONFIG ==========
def get_config_dict():
    """Retorna configuração como dicionário"""
    return {
        "base_dir": str(BASE_DIR),
        "db_path": str(DB_PATH),
        "orchestrator_model": ORCHESTRATOR_MODEL,
        "evaluator_model": EVALUATOR_MODEL,
        "ollama_host": OLLAMA_HOST,
        "specialists_count": len(SPECIALISTS),
        "memory_enabled": ENABLE_MEMORY_ENRICHMENT
    }

# Validar na importação
validate_config()

"""
DIGIMUNDO PRESENTE 🥷
"""