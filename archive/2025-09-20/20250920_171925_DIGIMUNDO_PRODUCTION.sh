#!/bin/bash

# 🚀 DIGIMUNDO PRODUCTION DEPLOYMENT SCRIPT
# Script completo para deploy em produção com otimizações avançadas

set -e  # Exit on any error

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Configurações
PROJECT_NAME="digimundo-production"
NODE_VERSION="18"
REDIS_VERSION="7"
DOCKER_IMAGE="digimundo:production"
PM2_ECOSYSTEM="ecosystem.config.js"

echo -e "${CYAN}🚀 DIGIMUNDO PRODUCTION DEPLOYMENT${NC}"
echo -e "${CYAN}====================================${NC}"

# Função para logging
log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}"
}

error() {
    echo -e "${RED}[ERROR] $1${NC}"
    exit 1
}

warning() {
    echo -e "${YELLOW}[WARNING] $1${NC}"
}

info() {
    echo -e "${BLUE}[INFO] $1${NC}"
}

# Verificar se está rodando como root
check_root() {
    if [[ $EUID -eq 0 ]]; then
        warning "Não execute este script como root!"
        exit 1
    fi
}

# Verificar dependências do sistema
check_dependencies() {
    log "Verificando dependências do sistema..."
    
    # Node.js
    if ! command -v node &> /dev/null; then
        error "Node.js não encontrado. Instale Node.js $NODE_VERSION+"
    fi
    
    NODE_VER=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)
    if [ "$NODE_VER" -lt "$NODE_VERSION" ]; then
        error "Node.js versão $NODE_VERSION+ necessária. Versão atual: $(node -v)"
    fi
    
    # NPM
    if ! command -v npm &> /dev/null; then
        error "NPM não encontrado"
    fi
    
    # PM2
    if ! command -v pm2 &> /dev/null; then
        log "Instalando PM2..."
        npm install -g pm2
    fi
    
    # Docker (opcional)
    if command -v docker &> /dev/null; then
        info "Docker encontrado - build de container disponível"
        DOCKER_AVAILABLE=true
    else
        warning "Docker não encontrado - apenas deploy local disponível"
        DOCKER_AVAILABLE=false
    fi
    
    # Redis
    if ! command -v redis-server &> /dev/null; then
        warning "Redis não encontrado - cache será desabilitado"
        REDIS_AVAILABLE=false
    else
        info "Redis encontrado - cache será habilitado"
        REDIS_AVAILABLE=true
    fi
}

# Configurar ambiente de produção
setup_production_env() {
    log "Configurando ambiente de produção..."
    
    # Criar diretórios necessários
    mkdir -p logs
    mkdir -p hybrid_memory/{a_mem,mem0,orchestrator}
    mkdir -p production
    mkdir -p backups
    
    # Configurar variáveis de ambiente
    cat > .env.production << EOF
NODE_ENV=production
PORT=7937
LOG_LEVEL=error
DISABLE_CONSOLE_LOGS=true
GZIP_COMPRESSION=true
ENABLE_RATE_LIMITING=true
HELMET_SECURITY=true
CONNECTION_POOL_SIZE=20
CACHE_TTL=300
PROMETHEUS_METRICS=true
HEALTH_CHECK_INTERVAL=30000
AUTO_SCALING=true
CPU_THRESHOLD=70
MEMORY_THRESHOLD=80
REDIS_URL=redis://localhost:6379
ENABLE_METRICS=true
EOF

    if [ "$REDIS_AVAILABLE" = false ]; then
        sed -i 's/REDIS_URL=.*/# REDIS_URL=redis:\/\/localhost:6379/' .env.production
    fi
    
    log "Arquivo .env.production criado"
}

# Instalar dependências de produção
install_dependencies() {
    log "Instalando dependências de produção..."
    
    # Backup do package-lock.json
    if [ -f package-lock.json ]; then
        cp package-lock.json backups/package-lock.json.backup
    fi
    
    # Instalar dependências
    npm ci --only=production --no-audit --no-fund
    
    # Instalar dependências adicionais para produção
    npm install --save \
        helmet \
        express-rate-limit \
        joi \
        compression \
        redis \
        prom-client \
        cluster
    
    log "Dependências instaladas com sucesso"
}

# Build otimizado
build_optimized() {
    log "Executando build otimizado..."
    
    # Minificar assets se existirem
    if [ -d "app/renderer/assets" ]; then
        info "Otimizando assets..."
        # Aqui você pode adicionar minificação de CSS/JS se necessário
    fi
    
    # Rebuild native modules para produção
    if [ -f "package-lock.json" ]; then
        npm rebuild --production
    fi
    
    # Limpar caches
    npm cache clean --force
    
    log "Build otimizado concluído"
}

# Configurar Redis
setup_redis() {
    if [ "$REDIS_AVAILABLE" = true ]; then
        log "Configurando Redis..."
        
        # Verificar se Redis está rodando
        if ! pgrep redis-server > /dev/null; then
            info "Iniciando Redis..."
            redis-server --daemonize yes --maxmemory 256mb --maxmemory-policy allkeys-lru
        fi
        
        # Testar conexão
        if redis-cli ping | grep -q PONG; then
            log "Redis configurado e funcionando"
        else
            warning "Redis não responde - cache será desabilitado"
            sed -i 's/REDIS_URL=.*/# REDIS_URL=redis:\/\/localhost:6379/' .env.production
        fi
    fi
}

# Configurar monitoramento
setup_monitoring() {
    log "Configurando monitoramento..."
    
    # Criar arquivo de configuração do Prometheus
    cat > production/prometheus.yml << EOF
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'digimundo'
    static_configs:
      - targets: ['localhost:9090']
    scrape_interval: 5s
    metrics_path: /metrics

  - job_name: 'node'
    static_configs:
      - targets: ['localhost:7937']
    scrape_interval: 10s
    metrics_path: /health

rule_files: []
alerting:
  alertmanagers:
    - static_configs:
        - targets: []
EOF

    log "Monitoramento configurado"
}

# Deploy com PM2
deploy_pm2() {
    log "Fazendo deploy com PM2..."
    
    # Parar processos existentes
    pm2 delete $PROJECT_NAME 2>/dev/null || true
    pm2 delete digimundo-metrics 2>/dev/null || true
    
    # Configurar PM2 para auto-start
    pm2 startup | grep -E '^sudo' | bash || true
    
    # Iniciar aplicação
    NODE_ENV=production pm2 start $PM2_ECOSYSTEM --env production
    
    # Salvar configuração PM2
    pm2 save
    
    # Verificar status
    sleep 5
    pm2 status
    
    log "Deploy PM2 concluído"
}

# Build Docker
build_docker() {
    if [ "$DOCKER_AVAILABLE" = true ]; then
        log "Construindo imagem Docker..."
        
        # Build da imagem
        docker build -t $DOCKER_IMAGE . --target production
        
        # Criar container
        docker run -d \
            --name digimundo-production \
            --restart unless-stopped \
            -p 7937:7937 \
            -v $(pwd)/logs:/app/logs \
            -v $(pwd)/hybrid_memory:/app/hybrid_memory \
            --env-file .env.production \
            $DOCKER_IMAGE
        
        log "Container Docker criado e executando"
    fi
}

# Verificar saúde do sistema
health_check() {
    log "Executando verificação de saúde..."
    
    # Aguardar sistema inicializar
    sleep 10
    
    # Verificar se a aplicação responde
    if curl -f http://localhost:7937/health > /dev/null 2>&1; then
        log "✅ Aplicação principal - OK"
    else
        error "❌ Aplicação principal não responde"
    fi
    
    # Verificar métricas se PM2 estiver rodando
    if pm2 status | grep -q digimundo-metrics; then
        if curl -f http://localhost:9090/health > /dev/null 2>&1; then
            log "✅ Servidor de métricas - OK"
        else
            warning "⚠️ Servidor de métricas não responde"
        fi
    fi
    
    # Verificar Redis
    if [ "$REDIS_AVAILABLE" = true ]; then
        if redis-cli ping | grep -q PONG; then
            log "✅ Redis - OK"
        else
            warning "⚠️ Redis não responde"
        fi
    fi
    
    # Verificar logs de erro
    if [ -f logs/err.log ]; then
        ERROR_COUNT=$(wc -l < logs/err.log 2>/dev/null || echo 0)
        if [ "$ERROR_COUNT" -gt 0 ]; then
            warning "⚠️ $ERROR_COUNT erros encontrados nos logs"
        else
            log "✅ Nenhum erro nos logs"
        fi
    fi
}

# Configurar auto-scaling
setup_autoscaling() {
    log "Configurando auto-scaling..."
    
    # Script de monitoramento de recursos
    cat > production/monitor-resources.sh << 'EOF'
#!/bin/bash
while true; do
    CPU=$(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1)
    MEM=$(free | grep Mem | awk '{printf("%.1f", $3/$2 * 100.0)}')
    
    if (( $(echo "$CPU > 80" | bc -l) )); then
        echo "High CPU: $CPU%" | logger -t digimundo-monitor
        pm2 scale digimundo-production +1
    elif (( $(echo "$CPU < 30" | bc -l) )); then
        echo "Low CPU: $CPU%" | logger -t digimundo-monitor
        INSTANCES=$(pm2 jlist | jq '.[] | select(.name=="digimundo-production") | .pm2_env.instances' | head -1)
        if [ "$INSTANCES" -gt 2 ]; then
            pm2 scale digimundo-production -1
        fi
    fi
    
    sleep 30
done
EOF
    
    chmod +x production/monitor-resources.sh
    
    # Adicionar ao cron se não existir
    if ! crontab -l 2>/dev/null | grep -q "monitor-resources.sh"; then
        (crontab -l 2>/dev/null; echo "@reboot cd $(pwd) && ./production/monitor-resources.sh &") | crontab -
    fi
    
    log "Auto-scaling configurado"
}

# Configurar notificações (estrutura básica)
setup_notifications() {
    log "Configurando sistema de notificações..."
    
    cat > production/notify.sh << 'EOF'
#!/bin/bash
# Sistema básico de notificações
# Adicione aqui integração com Slack, Discord, email, etc.

notify_slack() {
    # Webhook do Slack
    # curl -X POST -H 'Content-type: application/json' \
    #     --data '{"text":"'$1'"}' \
    #     $SLACK_WEBHOOK_URL
    echo "Notificação: $1"
}

notify_email() {
    # Envio por email
    # echo "$1" | mail -s "Digimundo Alert" admin@yourdomain.com
    echo "Email: $1"
}

case $1 in
    "error")
        notify_slack "🚨 Erro no Digimundo: $2"
        notify_email "Erro detectado: $2"
        ;;
    "scale")
        notify_slack "📈 Auto-scaling: $2"
        ;;
    "health")
        notify_slack "❤️ Health check: $2"
        ;;
esac
EOF
    
    chmod +x production/notify.sh
    log "Sistema de notificações preparado"
}

# Backup automático
setup_backup() {
    log "Configurando backup automático..."
    
    cat > production/backup.sh << 'EOF'
#!/bin/bash
BACKUP_DIR="backups/$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

# Backup de dados
cp -r hybrid_memory "$BACKUP_DIR/"
cp .env.production "$BACKUP_DIR/"
cp ecosystem.config.js "$BACKUP_DIR/"

# Backup de logs importantes
cp logs/combined.log "$BACKUP_DIR/" 2>/dev/null || true

# Compactar
tar -czf "$BACKUP_DIR.tar.gz" "$BACKUP_DIR"
rm -rf "$BACKUP_DIR"

# Manter apenas últimos 7 backups
ls -t backups/*.tar.gz | tail -n +8 | xargs rm -f 2>/dev/null || true

echo "Backup criado: $BACKUP_DIR.tar.gz"
EOF
    
    chmod +x production/backup.sh
    
    # Adicionar backup diário ao cron
    if ! crontab -l 2>/dev/null | grep -q "backup.sh"; then
        (crontab -l 2>/dev/null; echo "0 2 * * * cd $(pwd) && ./production/backup.sh") | crontab -
    fi
    
    log "Backup automático configurado"
}

# Relatório final
final_report() {
    echo
    echo -e "${PURPLE}📊 RELATÓRIO DE DEPLOY${NC}"
    echo -e "${PURPLE}===================${NC}"
    echo
    
    # Status dos serviços
    echo -e "${CYAN}Serviços:${NC}"
    pm2 status | grep -E "(digimundo|online|stopped)"
    echo
    
    # Informações de rede
    echo -e "${CYAN}Acesso:${NC}"
    echo -e "🌐 Aplicação Principal: ${GREEN}http://localhost:7937${NC}"
    echo -e "📊 Métricas Prometheus: ${GREEN}http://localhost:9090/metrics${NC}"
    echo -e "❤️ Health Check: ${GREEN}http://localhost:7937/health${NC}"
    echo
    
    # Informações do sistema
    echo -e "${CYAN}Sistema:${NC}"
    echo -e "🐧 OS: $(uname -s) $(uname -r)"
    echo -e "📦 Node.js: $(node -v)"
    echo -e "⚙️ PM2: $(pm2 -v)"
    if [ "$REDIS_AVAILABLE" = true ]; then
        echo -e "🔴 Redis: $(redis-server --version | cut -d' ' -f3)"
    fi
    if [ "$DOCKER_AVAILABLE" = true ]; then
        echo -e "🐳 Docker: $(docker --version | cut -d' ' -f3 | tr -d ',')"
    fi
    echo
    
    # Comandos úteis
    echo -e "${CYAN}Comandos Úteis:${NC}"
    echo -e "📋 Status: ${YELLOW}pm2 status${NC}"
    echo -e "📜 Logs: ${YELLOW}pm2 logs${NC}"
    echo -e "🔄 Restart: ${YELLOW}pm2 restart digimundo-production${NC}"
    echo -e "⏹️ Parar: ${YELLOW}pm2 stop digimundo-production${NC}"
    echo -e "📊 Monitorar: ${YELLOW}pm2 monit${NC}"
    echo -e "💾 Backup: ${YELLOW}./production/backup.sh${NC}"
    echo
    
    log "🎉 Deploy em produção concluído com sucesso!"
    echo -e "${GREEN}Digimundo está rodando em modo de produção otimizado!${NC}"
}

# Função principal
main() {
    echo -e "${PURPLE}Iniciando deploy em produção...${NC}"
    
    check_root
    check_dependencies
    setup_production_env
    install_dependencies
    build_optimized
    setup_redis
    setup_monitoring
    
    # Escolher método de deploy
    echo
    echo "Escolha o método de deploy:"
    echo "1) PM2 (Recomendado)"
    echo "2) Docker"
    echo "3) Ambos"
    read -p "Opção [1]: " DEPLOY_METHOD
    DEPLOY_METHOD=${DEPLOY_METHOD:-1}
    
    case $DEPLOY_METHOD in
        1)
            deploy_pm2
            ;;
        2)
            build_docker
            ;;
        3)
            deploy_pm2
            build_docker
            ;;
        *)
            deploy_pm2
            ;;
    esac
    
    setup_autoscaling
    setup_notifications
    setup_backup
    health_check
    final_report
}

# Executar apenas se chamado diretamente
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi