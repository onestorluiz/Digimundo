#!/usr/bin/env python3
"""
🔐 SISTEMA DE AUTENTICAÇÃO DO DEFENSE SHIELD
"""

import sys
import hashlib
import time
from datetime import datetime

def authorize(password):
    """Autoriza acesso temporário"""

    if password.strip() != "DIGIMUNDO PRESENTE":
        print("❌ SENHA INCORRETA!")
        print("💀 SISTEMA PERMANECE ARMADO!")
        return False

    # Cria arquivo de autorização
    with open("/tmp/.defense_authorized", "w") as f:
        f.write(f"Authorized at: {datetime.now()}\n")
        f.write(f"Valid for: 120 seconds\n")

    print("✅ AUTORIZAÇÃO CONCEDIDA!")
    print("⏰ Você tem 120 segundos para editar com segurança")
    print("🛡️ Defense Shield desarmado temporariamente")

    return True

if __name__ == "__main__":
    print("🔐 Digite a senha de autorização:")
    password = input("> ")

    if authorize(password):
        sys.exit(0)
    else:
        sys.exit(1)