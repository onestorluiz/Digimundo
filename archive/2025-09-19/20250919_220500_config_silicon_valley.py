"""
🔄 Config Silicon Valley - Alias para compatibilidade
Redireciona para config.py principal
"""

# Importar tudo da config principal
from .config import *

# Alias específicos que alguns sistemas podem esperar
def get_config():
    """Alias para get_config da config principal"""
    from .config import get_config as original_get_config
    return original_get_config()

# Manter compatibilidade com nomes antigos
SystemConfig = SystemConfig
OllamaConfig = OllamaConfig
SpecialistConfig = SpecialistConfig

# Silent redirect - no print needed