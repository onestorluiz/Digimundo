#!/bin/bash
# Setup Docker CPU-only Ollama
# SOLUÇÃO GARANTIDA - Docker no Mac NÃO tem acesso ao Metal GPU!

echo "🐳 CONFIGURANDO OLLAMA CPU-ONLY VIA DOCKER"
echo "=========================================="

# 1. Verifica se Docker está instalado
if ! command -v docker &> /dev/null; then
    echo "❌ Docker não está instalado!"
    echo "   Instale com: brew install --cask docker"
    exit 1
fi

# 2. Para Ollama nativo
echo "1️⃣ Parando Ollama nativo..."
pkill ollama
sleep 2

# 3. Pull da imagem CPU-only
echo "2️⃣ Baixando imagem Docker CPU-only..."
docker pull alpine/ollama

# 4. Para container existente se houver
echo "3️⃣ Removendo container antigo se existir..."
docker stop cpu-ollama 2>/dev/null || true
docker rm cpu-ollama 2>/dev/null || true

# 5. Inicia container CPU-only
echo "4️⃣ Iniciando Ollama em Docker (CPU-only)..."
docker run -d \
    -p 11434:11434 \
    -v ~/.ollama:/root/.ollama \
    --name cpu-ollama \
    --cpus="20" \
    --memory="60g" \
    alpine/ollama

sleep 5

# 6. Verifica se está rodando
echo "5️⃣ Verificando status..."
if docker ps | grep cpu-ollama > /dev/null; then
    echo "✅ Container rodando!"
else
    echo "❌ Falha ao iniciar container"
    docker logs cpu-ollama
    exit 1
fi

# 7. Testa conexão
echo "6️⃣ Testando API..."
curl -s http://localhost:11434/api/tags > /dev/null
if [ $? -eq 0 ]; then
    echo "✅ API respondendo em http://localhost:11434"
else
    echo "❌ API não está respondendo"
    exit 1
fi

# 8. Lista modelos disponíveis
echo "7️⃣ Modelos disponíveis no container:"
docker exec cpu-ollama ollama list

echo ""
echo "=========================================="
echo "✅ OLLAMA CPU-ONLY CONFIGURADO COM SUCESSO!"
echo "=========================================="
echo ""
echo "📝 PRÓXIMOS PASSOS:"
echo "1. Copiar modelo para container (se necessário):"
echo "   docker exec cpu-ollama ollama pull mixtral:8x7b"
echo ""
echo "2. Testar inferência:"
echo "   docker exec cpu-ollama ollama run mixtral 'Test prompt'"
echo ""
echo "3. Monitorar CPU do container:"
echo "   docker stats cpu-ollama"
echo ""
echo "4. Ver logs:"
echo "   docker logs -f cpu-ollama"
echo ""
echo "🎯 Python ainda conecta em http://localhost:11434"
echo "   Não precisa mudar o código!"