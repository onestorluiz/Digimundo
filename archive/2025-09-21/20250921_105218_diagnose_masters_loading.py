#!/usr/bin/env python3
"""
DIAGNÓSTICO COMPLETO: Por que o sistema não está carregando os masters?
"""

import sys
from pathlib import Path
sys.path.insert(0, 'src')

print("="*80)
print("🔍 DIAGNÓSTICO DE CARREGAMENTO DOS ROTEIROS MESTRES")
print("="*80)

# 1. Verificar estrutura de pastas
print("\n1️⃣ ESTRUTURA DE PASTAS:")
print("-" * 40)

folders = {
    "screenplays": Path("screenplays"),
    "screenplays/masters": Path("screenplays/masters"),
    "my_screenplays": Path("my_screenplays"),
}

for name, path in folders.items():
    if path.exists():
        if path.is_dir():
            files = list(path.glob("*.txt"))
            print(f"✅ {name}: {len(files)} arquivos .txt")
            if name == "screenplays/masters" and files:
                print(f"   Primeiros 5: {[f.name for f in files[:5]]}")
        else:
            print(f"❌ {name}: existe mas não é pasta")
    else:
        print(f"❌ {name}: NÃO EXISTE")

# 2. Verificar o que OllamaContinuousLearning carrega
print("\n2️⃣ O QUE O SISTEMA CARREGA:")
print("-" * 40)

from ollama_continuous_learning import OllamaContinuousLearning

system = OllamaContinuousLearning()

# Verificar atributos
print(f"masters_dir configurado: {system.masters_dir}")
print(f"screenplays_dir configurado: {system.screenplays_dir}")
print(f"my_screenplays_dir configurado: {system.my_screenplays_dir}")

# 3. Simular o método run_continuous_loop para ver o que ele carrega
print("\n3️⃣ SIMULANDO CARREGAMENTO DO LOOP:")
print("-" * 40)

screenplays = []

# Primeiro: Roteiros mestres profissionais (COPIADO DO CÓDIGO ATUALIZADO)
if system.masters_dir.exists():
    masters = list(system.masters_dir.glob("*.txt"))
    screenplays.extend(masters)
    print(f"📌 {len(masters)} roteiros mestres carregados")
    if masters:
        print("   Exemplos:")
        for m in masters[:5]:
            print(f"     • {m.name}")

# Segundo: Roteiros do usuário
if system.my_screenplays_dir.exists():
    user_scripts = list(system.my_screenplays_dir.glob("*.txt"))
    screenplays.extend(user_scripts)
    if user_scripts:
        print(f"📝 {len(user_scripts)} roteiros do usuário incluídos")
        for u in user_scripts:
            print(f"     • {u.name}")

# Terceiro: Outros roteiros
if len(screenplays) < 5 and system.screenplays_dir.exists():
    others = list(system.screenplays_dir.glob("*.txt"))
    extras = [s for s in others if s not in screenplays]
    screenplays.extend(extras)
    if extras:
        print(f"📄 {len(extras)} roteiros extras adicionados")

print(f"\n📚 TOTAL FINAL: {len(screenplays)} roteiros")

# 4. Verificar se as fases usam os roteiros corretos
print("\n4️⃣ VERIFICANDO FASES DE ANÁLISE:")
print("-" * 40)

# Simular Phase 1
if len(screenplays) >= 3:
    print(f"Phase 1 analisaria: {screenplays[0].name}, {screenplays[1].name}, {screenplays[2].name}")
else:
    print(f"⚠️ Apenas {len(screenplays)} roteiros disponíveis")

# Simular Phase 2
if len(screenplays) >= 2:
    print(f"Phase 2 compararia: {screenplays[0].name} ↔ {screenplays[1].name}")

# 5. Problema potencial
print("\n5️⃣ ANÁLISE DO PROBLEMA:")
print("-" * 40)

# Verificar se o código original ainda está lendo da pasta errada
original_screenplays_path = Path("screenplays")
if original_screenplays_path.exists():
    direct_files = list(original_screenplays_path.glob("*.txt"))
    print(f"⚠️ Arquivos diretos em 'screenplays/': {len(direct_files)}")
    if direct_files:
        print("   ESTES PODEM ESTAR SENDO USADOS AO INVÉS DOS MASTERS:")
        for f in direct_files:
            print(f"     • {f.name}")

# 6. Solução
print("\n6️⃣ SOLUÇÃO PROPOSTA:")
print("-" * 40)

if len(masters) > 0:
    print("✅ Masters existem e podem ser carregados")
    print("📝 O sistema DEVE priorizar screenplays/masters/ sobre outras pastas")
    print("🔧 Verificar se o código está realmente usando a versão atualizada")
else:
    print("❌ Nenhum master encontrado - verificar estrutura de pastas")

print("\n" + "="*80)
print("FIM DO DIAGNÓSTICO")
print("="*80)