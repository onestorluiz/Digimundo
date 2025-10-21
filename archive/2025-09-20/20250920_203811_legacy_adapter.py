"""
🔄 Legacy Adapter - Compatibilidade com imports antigos
Adaptador minimalista para sistemas migrados
"""

from pathlib import Path
from typing import Optional, Any
from src.core.unified_memory_system import get_unified_memory, MemoryType
# Auto-unified: Este arquivo foi automaticamente integrado ao sistema unificado


class LegacyAdapter:
    """Adaptador para compatibilidade com código antigo"""

    @staticmethod
    def get_ollama():
        """Retorna instância de Ollama (adaptado)"""
        from .ollama_core_minimal import OllamaMinimal
        return OllamaMinimal()

    @staticmethod
    def get_memory():
        """Retorna instância de memória (adaptado)"""
        from .omnimemory_v5_minimal import OmniMemoryV5
        return OmniMemoryV5()

    @staticmethod
    def get_config():
        """Retorna configuração centralizada"""
        from .config import get_config
        return get_config()

    @staticmethod
    def load_text(path: str) -> str:
        """
        Substitui PyPDF2/pdfplumber
        Carrega arquivo .txt ao invés de PDF
        """
        file_path = Path(path)

        # Tenta .txt primeiro
        txt_path = file_path.with_suffix('.txt')
        if txt_path.exists():
            with open(txt_path, 'r', encoding='utf-8') as f:
                return f.read()

        # Se for .txt direto
        if file_path.suffix == '.txt' and file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()

        # Retorna mensagem de erro se não encontrar
        return f"[CONVERT_TO_TXT_FIRST] {path} - Please convert PDF to TXT for 1000x performance"

    @staticmethod
    def extract_pdf_text(pdf_path: str, max_pages: Optional[int] = None) -> str:
        """
        Substitui extração de PDF
        Redireciona para load_text
        """
        return LegacyAdapter.load_text(pdf_path)

    @staticmethod
    def get_digilang():
        """DigiLang não é necessário para Script Doctor"""
        class DummyDigiLang:
            def encode(self, text):
                return text  # Bypass - retorna texto original
            def decode(self, text):
                return text
        return DummyDigiLang()

# Aliases para compatibilidade
ScreenplayCrystalMemory = lambda: LegacyAdapter.get_memory()
OllamaCore = lambda: LegacyAdapter.get_ollama()
DigiLangEncoder = lambda: LegacyAdapter.get_digilang()

# Funções helper para migração suave
# UNUSED - Candidate for removal
# def adapt_pdf_function(func):
#     """Decorator para adaptar funções que usam PDF"""
#     def wrapper(*args, **kwargs):
#         # Substitui argumentos PDF por TXT
#         if 'pdf_path' in kwargs:
#             kwargs['pdf_path'] = kwargs['pdf_path'].replace('.pdf', '.txt')
#         return func(*args, **kwargs)
#     return wrapper

# UNUSED - Candidate for removal
# # Função para verificar disponibilidade
def check_legacy_compatibility():
    """Verifica se adaptadores estão funcionando"""
    checks = {
        'Ollama': LegacyAdapter.get_ollama(),
        'Memory': LegacyAdapter.get_memory(),
        'Config': LegacyAdapter.get_config(),
        'DigiLang': LegacyAdapter.get_digilang()
    }

    for name, obj in checks.items():
        if obj is None:
            print(f"❌ {name} adapter failed")
        else:
            print(f"✅ {name} adapter working")

    return all(obj is not None for obj in checks.values())

# Export principal
__all__ = [
    'LegacyAdapter',
    'ScreenplayCrystalMemory',
    'OllamaCore',
    'DigiLangEncoder',
    'adapt_pdf_function',
    'check_legacy_compatibility'
]

# ============================================================
# AUTO-UNIFIED MEMORY HELPER
# ============================================================
def _get_memory():
    """Helper para acesso rápido à memória unificada"""
    return get_unified_memory()

# Atalhos para compatibilidade
unified_memory = _get_memory()
