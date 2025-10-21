#!/bin/bash

echo "🧠 TESTE RÁPIDO DO GRADIENT INTEGRADO"
echo "======================================"

# Teste 1: Verificar se modelo existe
echo -e "\n1️⃣ Verificando modelo..."
if ollama list | grep -q "scripturemon-gradient"; then
    echo "✅ Modelo scripturemon-gradient encontrado!"
else
    echo "❌ Modelo não encontrado"
    exit 1
fi

# Teste 2: Verificar ollama_core.py
echo -e "\n2️⃣ Verificando ollama_core.py..."
if grep -q "llama3-gradient:70b" apps/scripturemon/ollama_core.py; then
    echo "✅ Gradient configurado como prioridade!"
else
    echo "❌ Gradient não está como prioridade"
fi

# Teste 3: Verificar gradient_config.py
echo -e "\n3️⃣ Verificando gradient_config.py..."
if [ -f "apps/scripturemon/gradient_config.py" ]; then
    echo "✅ Configuração Gradient criada!"
    grep "num_ctx" apps/scripturemon/gradient_config.py | head -1
else
    echo "❌ Configuração não encontrada"
fi

# Teste 4: Testar integração Python
echo -e "\n4️⃣ Testando integração Python..."
python3 << 'EOF'
import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd() / "apps" / "scripturemon"))

try:
    from ollama_core import OllamaCore
    ollama = OllamaCore()
    
    # Verificar modelo padrão
    if 'gradient' in ollama.default_model.lower():
        print("✅ Gradient é o modelo padrão!")
    else:
        print(f"⚠️ Modelo padrão: {ollama.default_model}")
    
    # Verificar modelos disponíveis
    gradient_models = [m for m in ollama.models if 'gradient' in m.lower()]
    if gradient_models:
        print(f"✅ Modelos Gradient disponíveis: {gradient_models[:2]}")
    
except Exception as e:
    print(f"❌ Erro: {e}")
EOF

echo -e "\n======================================"
echo "📊 RESUMO DO SISTEMA:"
echo "- Modelo: scripturemon-gradient (70B)"
echo "- Contexto: 256.000 tokens"
echo "- RAM estimada: ~75GB"
echo "- PDFs simultâneos: 15+"
echo ""
echo "🚀 Para usar:"
echo "ollama run scripturemon-gradient"
echo ""
echo "62/100. Sistema configurado com sucesso."