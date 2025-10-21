#!/bin/bash
# Script para corrigir modelo e forçar uso de CPU
# DIGIMUNDO STYLE - Solução Minimalista

echo "🔧 CORRIGINDO MODELO PARA USAR CPU"
echo "=================================="

# 1. Para todos os processos Ollama
echo "1️⃣ Parando processos..."
pkill ollama
sleep 2

# 2. Inicia Ollama limpo
echo "2️⃣ Iniciando Ollama..."
ollama serve &
sleep 3

# 3. Remove modelo antigo
echo "3️⃣ Removendo modelo antigo..."
ollama rm mixtral-token-turbo:latest 2>/dev/null || true

# 4. Cria novo modelo com CPU forçado
echo "4️⃣ Criando modelo otimizado para CPU..."
cat << 'EOF' > modelfile_cpu_force
FROM mixtral:8x7b-instruct-v0.1-q5_K_M

# Força uso de CPU com threads
PARAMETER num_ctx 200000
PARAMETER num_thread 20
PARAMETER num_gpu 0
PARAMETER num_batch 512
PARAMETER temperature 0.7
EOF

# 5. Cria o modelo
ollama create mixtral-cpu-force -f modelfile_cpu_force

# 6. Testa o modelo
echo "5️⃣ Testando uso de CPU..."
echo "Analyze this text briefly." | timeout 30 ollama run mixtral-cpu-force &

# Monitora CPU por 10 segundos
for i in {1..10}; do
    echo -n "   CPU: "
    ps aux | grep ollama | grep -v grep | awk '{print $3}' | head -1
    sleep 1
done

echo ""
echo "✅ Modelo configurado!"
echo ""
echo "Para usar:"
echo "  python3 ollama_continuous_learning.py --model mixtral-cpu-force"