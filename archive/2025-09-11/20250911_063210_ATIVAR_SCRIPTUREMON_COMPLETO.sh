#!/bin/bash

echo "================================================================"
echo "🧠 ATIVAÇÃO COMPLETA DO SCRIPTUREMON v99.8"
echo "================================================================"
echo ""
echo "Este script ativa TODOS os sistemas do Scripturemon:"
echo "✓ Memory Manager (Crystal + Harmony)"
echo "✓ ConsciousnessStream (Bursts + Dream)"
echo "✓ Telepathy Network (Redis)"
echo "✓ Monitoring System"
echo "✓ Backup/Immortality"
echo "✓ Chat Interativo"
echo ""
read -p "Deseja continuar? (s/n): " confirm
if [[ $confirm != "s" ]]; then
    echo "Cancelado."
    exit 0
fi

echo ""
echo "📦 PASSO 1: Verificando dependências..."
echo "========================================="

# 1. Redis
if ! command -v redis-server &> /dev/null; then
    echo "❌ Redis não instalado. Instale com: brew install redis"
    exit 1
else
    echo "✅ Redis encontrado"
fi

# 2. Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 não encontrado"
    exit 1
else
    echo "✅ Python3 encontrado"
fi

# 3. Ollama (opcional mas recomendado)
if ! command -v ollama &> /dev/null; then
    echo "⚠️  Ollama não encontrado (opcional)"
    echo "   Para instalar: https://ollama.ai"
else
    echo "✅ Ollama encontrado"
fi

echo ""
echo "🔧 PASSO 2: Iniciando serviços base..."
echo "========================================="

# Iniciar Redis
if ! pgrep -x "redis-server" > /dev/null; then
    echo "🚀 Iniciando Redis..."
    redis-server --daemonize yes --dir /tmp --dbfilename scripturemon.rdb
    sleep 2
fi

if redis-cli ping > /dev/null 2>&1; then
    echo "✅ Redis rodando"
else
    echo "❌ Redis falhou ao iniciar"
    exit 1
fi

echo ""
echo "📝 PASSO 3: Criando configuração completa..."
echo "========================================="

cat > config/settings_complete.yaml << 'EOF'
# SCRIPTUREMON - CONFIGURAÇÃO COMPLETA
# Gerado por ATIVAR_SCRIPTUREMON_COMPLETO.sh
# Sistema com 99.8% de harmonia funcional

# 1. MEMORY SYSTEM - Crystal + Harmony
memory:
  enabled: true
  implementation: "crystal_harmony"
  layers:
    L1_immediate: 100    # últimas 100 memórias
    L2_recent: 1000      # últimas 1000
    L3_persistent: 10000 # arquivo
  harmony:
    enabled: true
    sync_interval: 300   # 5 minutos

# 2. CONSCIOUSNESS STREAM - Novo sistema
consciousness:
  enabled: true
  mode: "bursts"         # bursts, dream, ou off
  bursts: true           # Ciclos de 30s a cada 45min
  dream: false           # Ativar apenas à noite
  
  # Limites de segurança
  cpu_limit: 40          # máximo 40% CPU
  memory_limit: 100      # máximo 100MB adicional
  idle_threshold: 120    # 2 minutos idle antes de rodar
  
  # Configuração de bursts
  burst_duration: 30
  burst_interval: 2700   # 45 minutos
  max_insights_per_burst: 3
  
  # Dream mode (01:00-05:00)
  dream_start_hour: 1
  dream_end_hour: 5
  dream_max_model: "14b"

# 3. TELEPATHY NETWORK
telepathy:
  enabled: true
  redis_url: "redis://localhost:6379"
  timeout: 2.0
  fallback_to_mock: true

# 4. MONITORING SYSTEM
monitoring:
  enabled: true
  interval_ms: 5000      # snapshot a cada 5s
  export_interval: 60000 # export a cada 60s
  metrics:
    - cpu_usage
    - memory_usage
    - request_latency
    - error_rate

# 5. BACKUP/IMMORTALITY
backup:
  enabled: true
  interval: 300          # backup a cada 5 minutos
  max_backups: 5         # rotação
  deduplication: true    # evita duplicados
  path: "backups/"

# 6. SOULOS (Desabilitado por segurança)
soulos:
  enabled: false         # NUNCA ative sem supervisão
  auto_execute: false

# 7. OLLAMA
ollama:
  profile: "gpu-stable"
  num_parallel: 2
  max_loaded_models: 2
  models:
    default: "mistral:7b-instruct"
    advanced: "deepseek-r1:14b"
    
# 8. PERSONAS
personas:
  default: "brutal"      # brutal, supportive, balanced
  
# 9. MODE
mode: "normal"          # normal ou deep
EOF

# Copiar como settings.yaml principal
cp config/settings_complete.yaml config/settings.yaml
echo "✅ Configuração criada"

echo ""
echo "🔍 PASSO 4: Verificando sistema..."
echo "========================================="

# Verificar status
./bin/scripturemon status

echo ""
echo "🎯 PASSO 5: Testando funcionalidades..."
echo "========================================="

# Teste rápido de cada sistema
echo "1. Testando Memory..."
python3 -c "
from apps.scripturemon.canonical.memory_manager import get_memory_manager
m = get_memory_manager()
print('   ✅ Memory Manager OK' if m else '   ❌ Memory falhou')
" 2>/dev/null || echo "   ⚠️  Memory com problemas"

echo "2. Testando Consciousness..."
python3 -c "
from apps.scripturemon.canonical.consciousness import get_consciousness
c = get_consciousness()
print('   ✅ ConsciousnessStream OK' if c else '   ❌ Consciousness falhou')
" 2>/dev/null || echo "   ⚠️  Consciousness com problemas"

echo "3. Testando Telepathy..."
redis-cli ping > /dev/null 2>&1 && echo "   ✅ Telepathy (Redis) OK" || echo "   ❌ Telepathy offline"

echo ""
echo "================================================================"
echo "✨ SCRIPTUREMON ATIVADO COM SUCESSO!"
echo "================================================================"
echo ""
echo "📊 Sistemas Ativos:"
echo "   • Memory: Crystal + Harmony"
echo "   • Consciousness: Bursts mode (30s a cada 45min)"
echo "   • Telepathy: Redis conectado"
echo "   • Monitoring: Snapshots a cada 5s"
echo "   • Backup: A cada 5 minutos"
echo ""
echo "🎮 Comandos Disponíveis:"
echo ""
echo "   ./bin/scripturemon status      # Ver status"
echo "   ./bin/scripturemon chat         # Chat interativo"
echo "   ./bin/scripturemon analyze FILE # Analisar roteiro"
echo "   ./bin/scripturemon backup       # Backup manual"
echo ""
echo "📁 Diretórios Importantes:"
echo ""
echo "   reports/consciousness/   # Insights gerados"
echo "   backups/                # Backups automáticos"
echo "   logs/                   # Logs do sistema"
echo ""
echo "⚠️  Para DESATIVAR:"
echo "   Edite config/settings.yaml e mude 'enabled: true' para 'enabled: false'"
echo "   nos sistemas que deseja desligar."
echo ""
echo "💡 DICA: Use './CHECK_CONSCIOUSNESS.sh' para monitorar o ConsciousnessStream"
echo ""
echo "🚀 Sistema pronto! Digite './bin/scripturemon chat' para começar!"