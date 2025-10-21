"""Runtime settings configuration with caching"""
import json
from pathlib import Path
from typing import Dict, Any

_settings_cache = None

def get_settings() -> Dict[str, Any]:
    """Get runtime settings with caching"""
    global _settings_cache
    
    if _settings_cache is not None:
        return _settings_cache
    
    # Default settings
    settings = {
        'ollama': {
            'enabled': True,
            'default_model': 'mistral:instruct',
            'timeout': 30
        },
        'soulos': {
            'enabled': False,
            'code_execution': False,
            'timeout': 5.0
        },
        'redis': {
            'enabled': True,
            'host': 'localhost',
            'port': 6379
        },
        'rag': {
            'backend': 'chroma',
            'collection': 'v3_1_docs'
        }
    }
    
    # Try to load from config file if exists
    config_path = Path.home() / '.scripturemon' / 'config.json'
    if config_path.exists():
        try:
            with open(config_path) as f:
                user_settings = json.load(f)
                # Merge with defaults
                for key in user_settings:
                    if key in settings:
                        settings[key].update(user_settings[key])
                    else:
                        settings[key] = user_settings[key]
        except:
            pass  # Use defaults if config is invalid
    
    _settings_cache = settings
    return settings

def clear_cache():
    """Clear settings cache to force reload"""
    global _settings_cache
    _settings_cache = None
