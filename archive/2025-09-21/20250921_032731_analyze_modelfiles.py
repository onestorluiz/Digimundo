#!/usr/bin/env python3
"""
Análise completa de todos os modelfiles
"""

from pathlib import Path
import re

modelfiles_dir = Path("resources/modelfiles")

print("=" * 70)
print("📚 ANÁLISE COMPLETA DOS MODELFILES - SCRIPTUREMON ULTIMATE")
print("=" * 70)
print()

# Categorias
categories = {
    "deep_learning": [],
    "analysis": [],
    "optimization": [],
    "refactoring": [],
    "production": []
}

for modelfile in sorted(modelfiles_dir.glob("*.modelfile")):
    with open(modelfile, 'r') as f:
        content = f.read()

    # Extrair informações chave
    from_match = re.search(r'FROM\s+(\S+)', content)
    from_model = from_match.group(1) if from_match else "unknown"

    # Extrair contexto
    ctx_match = re.search(r'num_ctx\s+(\d+)', content)
    ctx_size = int(ctx_match.group(1)) if ctx_match else 0

    # Categorizar
    name = modelfile.stem

    if 'deep' in name.lower() or 'learning' in name.lower():
        category = "deep_learning"
    elif 'analyzer' in name or 'analysis' in name.lower():
        category = "analysis"
    elif 'cpu' in name or 'optimized' in name.lower():
        category = "optimization"
    elif 'refactor' in name.lower():
        category = "refactoring"
    else:
        category = "production"

    # Extrair primeira linha de comentário
    first_comment = ""
    for line in content.split('\n'):
        if line.strip().startswith('#') and len(line.strip()) > 2:
            first_comment = line.strip()[1:].strip()
            break

    categories[category].append({
        "name": name,
        "file": modelfile.name,
        "model": from_model,
        "context": ctx_size,
        "description": first_comment[:60] if first_comment else ""
    })

# Relatório detalhado
for cat, items in categories.items():
    if items:
        print(f"\n{'=' * 70}")
        print(f"📂 {cat.upper().replace('_', ' ')}")
        print(f"{'=' * 70}")

        for item in items:
            print(f"\n📄 {item['name']}")
            print(f"   Modelo base: {item['model']}")
            print(f"   Contexto: {item['context']:,} tokens" if item['context'] else "   Contexto: padrão")
            if item['description']:
                print(f"   Descrição: {item['description']}")

# Análise especial dos modelos de aprendizado
print(f"\n{'=' * 70}")
print("🧠 MODELOS PARA APRENDIZADO CONTÍNUO")
print(f"{'=' * 70}")

learning_models = []

for modelfile in sorted(modelfiles_dir.glob("*.modelfile")):
    with open(modelfile, 'r') as f:
        content = f.read().lower()

    # Detectar capacidades de aprendizado
    has_learning = any(keyword in content for keyword in [
        'learn', 'analyze', 'pattern', 'extract', 'compare',
        'complete book', 'entire', 'deep analysis', 'continuous'
    ])

    if has_learning:
        learning_models.append(modelfile.stem)

        # Mostrar capacidades específicas
        print(f"\n✅ {modelfile.stem}")

        if 'complete book' in content or 'entire' in content:
            print("   • Pode processar documentos completos")
        if 'pattern' in content:
            print("   • Extrai padrões")
        if 'comparative' in content or 'compare' in content:
            print("   • Faz análise comparativa")
        if '128k' in content or '131072' in content:
            print("   • Contexto ultra-largo (128K tokens)")
        if 'deep' in content:
            print("   • Análise profunda")
        if 'extract' in content:
            print("   • Extração de conceitos")

print(f"\n{'=' * 70}")
print("🎯 RECOMENDAÇÃO PARA LOOP DE APRENDIZADO")
print(f"{'=' * 70}")

print("""
Para análise em loop contínuo, use:

1. **deeplearning-main** (131K tokens)
   - Análise de livros completos + roteiros
   - Comparação teoria vs prática
   - Extração de insights acionáveis

2. **beat_analyzer**
   - Análise específica de beats narrativos
   - Identificação de padrões estruturais

3. **character_analyzer**
   - Análise de arcos de personagens
   - Evolução e desenvolvimento

4. **scripturemon-cpu-maximum**
   - Análise completa quando GPU não disponível
   - Otimizado para CPU

5. **mixtral-dedicated-q5** (33GB)
   - Produção com alta qualidade
   - Análise complexa e profunda

COMANDO SUGERIDO:
```bash
# Criar modelo de aprendizado profundo
ollama create deeplearning-main -f resources/modelfiles/deeplearning-main.modelfile

# Executar análise em loop
python3 continuous_learning.py
```
""")

print("=" * 70)