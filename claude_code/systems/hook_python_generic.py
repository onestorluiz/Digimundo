
# 🔥 UCHIMON INTEGRATION HOOK - Python Universal
import os
import sys

def integrate_with_uchimon():
    """Integra sistema Python atual com UCHIMON"""
    try:
        # Adicionar path do claude_code
        claude_code_path = '/Users/clubproducoes/Digimundo/claude_code/'
        if claude_code_path not in sys.path:
            sys.path.append(claude_code_path)

        # Importar e executar loader
        from universal_uchimon_loader import load_uchimon_rules
        load_uchimon_rules()

        print("🔥 Sistema integrado com UCHIMON GENJUTSU")
        return True
    except Exception as e:
        print(f"⚠️ Falha na integração UCHIMON: {e}")
        return False

# Auto-integração
if __name__ == "__main__":
    integrate_with_uchimon()

# DIGIMUNDO PRESENTE
