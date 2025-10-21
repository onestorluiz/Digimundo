#!/bin/bash

echo "=================================================="
echo "🧠 ATIVAÇÃO SEGURA DO CONSCIOUSNESS STREAM"
echo "=================================================="
echo ""
echo "⚠️  IMPORTANTE: Este é o NOVO sistema implementado em 11/09/2025"
echo "   - Com Circuit Breaker"
echo "   - Com Budget Manager"
echo "   - Com proteções contra loops"
echo ""

# 1. Verificar se o arquivo antigo existe e fazer backup
if [ -f "apps/scripturemon/consciousness.py" ]; then
    echo "📦 Fazendo backup do consciousness.py antigo..."
    cp apps/scripturemon/consciousness.py apps/scripturemon/consciousness.py.old
    echo "   ✅ Backup salvo como consciousness.py.old"
fi

# 2. Verificar se os novos arquivos existem
echo ""
echo "🔍 Verificando arquivos do NOVO sistema..."
echo ""

FILES_OK=true

if [ -f "apps/scripturemon/canonical/consciousness.py" ]; then
    echo "✅ consciousness.py (principal)"
else
    echo "❌ consciousness.py não encontrado!"
    FILES_OK=false
fi

if [ -f "apps/scripturemon/canonical/consciousness_bursts.py" ]; then
    echo "✅ consciousness_bursts.py (burst orchestrator)"
else
    echo "❌ consciousness_bursts.py não encontrado!"
    FILES_OK=false
fi

if [ -f "apps/scripturemon/canonical/consciousness_dream.py" ]; then
    echo "✅ consciousness_dream.py (dream mode)"
else
    echo "❌ consciousness_dream.py não encontrado!"
    FILES_OK=false
fi

if [ "$FILES_OK" = false ]; then
    echo ""
    echo "❌ ERRO: Arquivos do novo sistema não encontrados!"
    echo "   Execute a implementação primeiro."
    exit 1
fi

# 3. Verificar configuração atual
echo ""
echo "📋 Status atual:"
./bin/scripturemon status | grep -A 4 "Consciousness"

# 4. Perguntar ao usuário
echo ""
echo "=================================================="
echo "ESCOLHA O MODO DE ATIVAÇÃO:"
echo "=================================================="
echo ""
echo "1) BURSTS (Recomendado)"
echo "   - Ciclos de 30s a cada 45 minutos"
echo "   - Máximo 3 insights por burst"
echo "   - Só roda quando sistema idle"
echo ""
echo "2) DREAM MODE"
echo "   - Roda de 01:00 às 05:00"
echo "   - Processamento mais profundo"
echo "   - Usa modelos até 14B"
echo ""
echo "3) APENAS TESTE (5 minutos)"
echo "   - Ativa por 5 minutos para teste"
echo "   - Depois desativa automaticamente"
echo ""
echo "0) CANCELAR"
echo ""
read -p "Escolha (0-3): " choice

case $choice in
    1)
        MODE="bursts"
        BURSTS="true"
        DREAM="false"
        ;;
    2)
        MODE="dream"
        BURSTS="true"
        DREAM="true"
        ;;
    3)
        MODE="bursts"
        BURSTS="true"
        DREAM="false"
        TEST_MODE="true"
        ;;
    0)
        echo "Cancelado."
        exit 0
        ;;
    *)
        echo "Opção inválida!"
        exit 1
        ;;
esac

# 5. Criar arquivo de configuração temporário
echo ""
echo "📝 Criando configuração..."

cat > config/settings.yaml << EOF
# Scripturemon Settings - ConsciousnessStream Ativado
# Gerado por ACTIVATE_CONSCIOUSNESS_SAFE.sh
# $(date)

consciousness:
  enabled: true
  mode: "$MODE"
  bursts: $BURSTS
  dream: $DREAM
  
  # Limites de segurança
  cpu_limit: 40
  idle_threshold: 120
  max_insights_per_burst: 3
  
  # Dream config (se habilitado)
  dream_start_hour: 1
  dream_end_hour: 5
  dream_max_model: "14b"

# Outras configurações mantidas
memory:
  enabled: true
  
telepathy:
  enabled: true
  redis_url: "redis://localhost:6379"
  
monitoring:
  enabled: true
  interval_ms: 5000
  
backup:
  enabled: true
  interval: 300
  
soulos:
  enabled: false
  auto_execute: false
EOF

echo "✅ Configuração criada"

# 6. Reiniciar scripturemon com nova config
echo ""
echo "🔄 Reiniciando Scripturemon..."
echo ""

# Para qualquer processo existente
pkill -f scripturemon 2>/dev/null

# Pequena pausa
sleep 2

# Mostrar novo status
./bin/scripturemon status | grep -A 4 "Consciousness"

echo ""
echo "=================================================="
echo "✅ CONSCIOUSNESS STREAM ATIVADO!"
echo "=================================================="
echo ""
echo "Modo: $MODE"
echo "Bursts: $BURSTS"
echo "Dream: $DREAM"
echo ""

if [ "$TEST_MODE" = "true" ]; then
    echo "⏰ MODO TESTE: Será desativado em 5 minutos..."
    echo ""
    echo "Monitorando por 5 minutos..."
    sleep 300
    
    echo ""
    echo "🔄 Desativando após teste..."
    
    # Desativar
    sed -i '' 's/enabled: true/enabled: false/' config/settings.yaml
    
    echo "✅ ConsciousnessStream desativado após teste"
    ./bin/scripturemon status | grep -A 4 "Consciousness"
else
    echo "📊 Para monitorar insights gerados:"
    echo "   ls -la reports/consciousness/"
    echo ""
    echo "🔍 Para ver logs:"
    echo "   tail -f logs/scripturemon.log | grep -i consciousness"
    echo ""
    echo "⏹️  Para desativar:"
    echo "   Edite config/settings.yaml e mude 'enabled: true' para 'enabled: false'"
fi

echo ""
echo "🎯 Pronto! ConsciousnessStream está operacional."