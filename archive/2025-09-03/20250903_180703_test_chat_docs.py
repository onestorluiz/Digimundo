#!/usr/bin/env python3
"""Teste dos comandos de documentos no chat"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Desabilita inicialização completa para teste rápido
os.environ["SCRIPTUREMON_FAST_TEST"] = "1"

from apps.scripturemon.chat import ScripturemonChat

print("🎬 Testando comandos de documentos...\n")

# Cria instância do chat (simplificada)
chat = ScripturemonChat()

# Testa comandos
commands = [
    ("/docstatus", "Status inicial"),
    ("/open sonhos", "Abrindo Sonhos Sem Lembranças"),
    ("/docstatus", "Status após abrir documento"),
    ("Você tem acesso ao meu roteiro Sonhos Sem Lembranças?", "Pergunta sobre acesso"),
]

for cmd, desc in commands:
    print(f"\n📝 {desc}")
    print(f">>> {cmd}")
    response = chat.process_input(cmd)
    print(f"<<< {response[:500]}...")  # Primeiros 500 chars
    print("-" * 60)

print("\n✅ Teste concluído!")