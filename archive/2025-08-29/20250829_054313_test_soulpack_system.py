#!/usr/bin/env python3
"""Teste do sistema Soulpack CRDT"""

import sys
sys.path.append('/Users/clubproducoes/Digimundo/archive/scripts/python')

from SOULPACK_CRDT import SoulpackManager, Event
import time

# Cria gerenciador
manager = SoulpackManager("Scripturemon")

print("🧬 DEMONSTRAÇÃO DO SISTEMA SOULPACK CRDT")
print("="*50)

# 1. Criar versão inicial
print("\n1️⃣ Criando Soulpack v1...")
pack_v1 = manager.create_soulpack("v1")

# Adiciona evento
event1 = Event(
    ts=time.time(),
    author="scripturemon-v1",
    kind="MEMO_ADD",
    payload={"content": "Memória da versão 1"}
)
manager.add_event(pack_v1, event1)

# 2. Criar versão divergente
print("\n2️⃣ Criando Soulpack v2 (divergente)...")
pack_v2 = manager.create_soulpack("v2")

event2 = Event(
    ts=time.time() + 1,
    author="scripturemon-v2",
    kind="EVOLVE",
    payload={"evolution": "Aprendeu nova técnica"}
)
manager.add_event(pack_v2, event2)

# 3. Fazer merge CRDT
print("\n3️⃣ Fazendo merge CRDT das versões...")
merged_pack = manager.merge_soulpacks(pack_v1, pack_v2)

print("\n✅ Sistema Soulpack CRDT funcionando!")
print(f"   Pack merged: {merged_pack}")
