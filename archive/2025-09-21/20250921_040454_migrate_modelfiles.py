#!/usr/bin/env python3
"""
Migração dos Modelfiles Especializados
Traz os modelfiles otimizados do sistema original
"""

import shutil
from pathlib import Path

print("="*60)
print("MIGRAÇÃO DOS MODELFILES ESPECIALIZADOS")
print("="*60)

# Diretórios
SOURCE_DIR = Path("/Users/clubproducoes/Digimundo/scripturemon-champion/data/models/modelfiles")
TARGET_DIR = Path("modelfiles")
TARGET_DIR.mkdir(exist_ok=True)

# Modelfiles essenciais para análise de roteiros
ESSENTIAL_MODELFILES = [
    # Especialistas em narrativa
    "scripturemon-cpu-structure.modelfile",    # Estrutura (3 atos, beats)
    "scripturemon-cpu-dialogue.modelfile",     # Diálogos e voz
    "scripturemon-cpu-themes.modelfile",       # Temas e significados
    "scripturemon-cpu-symbolism.modelfile",    # Simbolismo e subtexto

    # Modelos Mixtral otimizados
    "mixtral-dedicated-q5.modelfile",          # Mixtral dedicado (máxima qualidade)
    "mixtral-eco-q5.modelfile",               # Mixtral eco (eficiente)

    # CPU otimizados
    "scripturemon-cpu-optimized.modelfile",    # Versão CPU otimizada
    "scripturemon-cpu-maximum.modelfile",      # CPU máxima performance

    # Especiais
    "producermon_v3_resource_manager.modelfile",  # Gerenciamento de recursos
    "deeplearning-main.modelfile"              # Deep learning principal
]

print(f"\n📁 Origem: {SOURCE_DIR}")
print(f"📁 Destino: {TARGET_DIR}")
print(f"\n📝 Migrando {len(ESSENTIAL_MODELFILES)} modelfiles essenciais...")
print("-"*40)

migrated = []
failed = []

for modelfile_name in ESSENTIAL_MODELFILES:
    src_path = SOURCE_DIR / modelfile_name
    dst_path = TARGET_DIR / modelfile_name

    try:
        if src_path.exists():
            shutil.copy2(src_path, dst_path)
            migrated.append(modelfile_name)

            # Ler primeira linha para mostrar modelo base
            with open(dst_path, 'r') as f:
                lines = f.readlines()
                from_line = next((l for l in lines if l.startswith('FROM')), None)
                if from_line:
                    model = from_line.replace('FROM', '').strip()
                    print(f"✅ {modelfile_name[:30]:30} → {model}")
                else:
                    print(f"✅ {modelfile_name[:30]}")
        else:
            failed.append(modelfile_name)
            print(f"❌ {modelfile_name} - não encontrado")

    except Exception as e:
        failed.append(modelfile_name)
        print(f"❌ {modelfile_name} - erro: {e}")

print("\n" + "="*60)
print("📊 ESTATÍSTICAS DA MIGRAÇÃO")
print("="*60)
print(f"✅ Migrados: {len(migrated)} modelfiles")
print(f"❌ Falharam: {len(failed)} modelfiles")

if migrated:
    print("\n🎯 MODELFILES DISPONÍVEIS:")
    print("-"*40)

    # Agrupar por tipo
    specialists = [m for m in migrated if 'cpu-' in m and 'optimized' not in m]
    mixtral = [m for m in migrated if 'mixtral' in m]
    optimized = [m for m in migrated if 'optimized' in m or 'maximum' in m]
    special = [m for m in migrated if m not in specialists + mixtral + optimized]

    if specialists:
        print("\n🎭 Especialistas:")
        for m in specialists:
            name = m.replace('scripturemon-cpu-', '').replace('.modelfile', '')
            print(f"  - {name}: Especialista em {name}")

    if mixtral:
        print("\n🤖 Mixtral:")
        for m in mixtral:
            variant = "Dedicado" if "dedicated" in m else "Econômico"
            print(f"  - {variant}: {m.replace('.modelfile', '')}")

    if optimized:
        print("\n⚡ CPU Otimizados:")
        for m in optimized:
            print(f"  - {m.replace('.modelfile', '').replace('scripturemon-cpu-', '')}")

    if special:
        print("\n🌟 Especiais:")
        for m in special:
            print(f"  - {m.replace('.modelfile', '')}")

print("\n" + "="*60)
print("🚀 COMO USAR OS MODELFILES")
print("="*60)

print("""
1. Criar modelo especializado:
   ollama create scripturemon-structure -f modelfiles/scripturemon-cpu-structure.modelfile

2. Usar no código:
   ```python
   from scripturemon_champion.ollama import OllamaReal

   ollama = OllamaReal()
   response = ollama.generate(
       "Analyze the three-act structure...",
       model="scripturemon-structure"
   )
   ```

3. Criar todos de uma vez:
   ```bash
   for f in modelfiles/*.modelfile; do
       name=$(basename "$f" .modelfile)
       ollama create "$name" -f "$f"
   done
   ```
""")

# Criar script helper
script_path = TARGET_DIR / "create_all_models.sh"
script_content = """#!/bin/bash
# Cria todos os modelos especializados

echo "🚀 Criando modelos especializados..."

for modelfile in *.modelfile; do
    if [ -f "$modelfile" ]; then
        name="${modelfile%.modelfile}"
        echo "Creating $name..."
        ollama create "$name" -f "$modelfile"
    fi
done

echo "✅ Todos os modelos criados!"
ollama list | grep scripturemon
"""

with open(script_path, 'w') as f:
    f.write(script_content)

script_path.chmod(0o755)
print(f"\n✅ Script helper criado: {script_path}")
print("   Execute: cd modelfiles && ./create_all_models.sh")

print("\n" + "="*60)
print("✅ MIGRAÇÃO DOS MODELFILES COMPLETA!")
print("="*60)