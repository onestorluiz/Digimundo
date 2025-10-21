#!/bin/bash

# 🚀 DIGIMUNDO QUICK START - PRODUCTION
# Script de inicialização rápida para produção

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m'

# ASCII Art
show_logo() {
    echo -e "${PURPLE}"
    cat << 'EOF'
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║     ██████╗ ██╗ ██████╗ ██╗███╗   ███╗██╗   ██╗███╗   ██╗   ║
    ║     ██╔══██╗██║██╔════╝ ██║████╗ ████║██║   ██║████╗  ██║   ║
    ║     ██║  ██║██║██║  ███╗██║██╔████╔██║██║   ██║██╔██╗ ██║   ║
    ║     ██║  ██║██║██║   ██║██║██║╚██╔╝██║██║   ██║██║╚██╗██║   ║
    ║     ██████╔╝██║╚██████╔╝██║██║ ╚═╝ ██║╚██████╔╝██║ ╚████║   ║
    ║     ╚═════╝ ╚═╝ ╚═════╝ ╚═╝╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═══╝   ║
    ║                                                              ║
    ║                  🚀 PRODUCTION DEPLOYMENT                    ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
EOF
    echo -e "${NC}"
}

log() {
    echo -e "${BLUE}[$(date +'%H:%M:%S')]${NC} $1"
}

success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check prerequisites
check_prerequisites() {
    log "🔍 Verificando pré-requisitos..."
    
    local missing=0
    
    # Check Docker
    if ! command -v docker &> /dev/null; then
        error "Docker não encontrado. Instale o Docker primeiro."
        missing=1
    fi
    
    # Check Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        error "Docker Compose não encontrado. Instale o Docker Compose primeiro."
        missing=1
    fi
    
    # Check Node.js
    if ! command -v node &> /dev/null; then
        warning "Node.js não encontrado. Será usado apenas Docker."
    fi
    
    # Check if Docker is running
    if ! docker info &> /dev/null; then
        error "Docker não está rodando. Inicie o Docker primeiro."
        missing=1
    fi
    
    if [ $missing -eq 1 ]; then
        error "Pré-requisitos não atendidos. Abortando..."
        exit 1
    fi
    
    success "Pré-requisitos verificados"
}

# Setup environment
setup_environment() {
    log "⚙️ Configurando ambiente..."
    
    # Create .env if not exists
    if [ ! -f ".env" ]; then
        log "Criando arquivo .env..."
        cat > .env << 'EOF'
# Digimundo Production Environment
NODE_ENV=production
PORT=7937
LOG_LEVEL=error

# Redis Configuration
REDIS_URL=redis://redis:6379
REDIS_PASSWORD=digimundo_redis_2024

# Security
JWT_SECRET=your_jwt_secret_here_change_this
SESSION_SECRET=your_session_secret_here_change_this

# Optimization
GZIP_COMPRESSION=true
ENABLE_RATE_LIMITING=true
HELMET_SECURITY=true
CONNECTION_POOL_SIZE=20
CACHE_TTL=300

# Monitoring
PROMETHEUS_METRICS=true
ENABLE_METRICS=true
HEALTH_CHECK_INTERVAL=30000

# Performance
AUTO_SCALING=false
CPU_THRESHOLD=70
MEMORY_THRESHOLD=80

# CORS (adjust for your domain)
CORS_ORIGINS=http://localhost:7937,https://your-domain.com

# Disable console logs in production
DISABLE_CONSOLE_LOGS=true
EOF
        success "Arquivo .env criado"
        warning "⚠️ IMPORTANTE: Altere as chaves secretas no arquivo .env!"
    else
        log "Arquivo .env já existe, mantendo configurações..."
    fi
    
    # Create necessary directories
    mkdir -p logs
    mkdir -p data
    mkdir -p hybrid_memory/a_mem/sabiamon
    mkdir -p hybrid_memory/mem0/sabiamon
    mkdir -p hybrid_memory/orchestrator/sabiamon
    
    # Set permissions
    chmod +x production/scripts/*.sh 2>/dev/null || true
    
    success "Ambiente configurado"
}

# Choose deployment method
choose_deployment() {
    echo ""
    echo -e "${YELLOW}Escolha o método de deployment:${NC}"
    echo "1) Docker Compose (Recomendado para produção)"
    echo "2) PM2 + Node.js (Para servidores dedicados)"
    echo "3) Desenvolvimento (Docker com hot reload)"
    echo "4) Apenas verificar status"
    echo ""
    
    read -p "Digite sua escolha (1-4): " choice
    
    case $choice in
        1)
            deploy_docker_compose
            ;;
        2)
            deploy_pm2
            ;;
        3)
            deploy_development
            ;;
        4)
            check_status
            ;;
        *)
            error "Opção inválida"
            exit 1
            ;;
    esac
}

# Deploy with Docker Compose
deploy_docker_compose() {
    log "🐳 Iniciando deployment com Docker Compose..."
    
    # Check if services are already running
    if docker-compose ps | grep -q "Up"; then
        echo ""
        warning "Serviços já estão rodando. Deseja:"
        echo "1) Atualizar (rolling update)"
        echo "2) Reiniciar tudo"
        echo "3) Parar e sair"
        read -p "Escolha (1-3): " update_choice
        
        case $update_choice in
            1)
                log "Executando rolling update..."
                if [ -f "production/scripts/deploy.sh" ]; then
                    ./production/scripts/deploy.sh
                else
                    docker-compose up -d
                fi
                ;;
            2)
                log "Reiniciando todos os serviços..."
                docker-compose down
                docker-compose up -d
                ;;
            3)
                docker-compose down
                success "Serviços parados"
                exit 0
                ;;
        esac
    else
        # Fresh deployment
        log "Fazendo build das imagens..."
        docker-compose build
        
        log "Iniciando serviços..."
        docker-compose up -d
    fi
    
    # Wait for services to start
    log "Aguardando serviços iniciarem..."
    sleep 10
    
    # Check health
    check_health_endpoints
    
    success "Deployment com Docker Compose concluído!"
    show_endpoints
}

# Deploy with PM2
deploy_pm2() {
    log "⚡ Iniciando deployment com PM2..."
    
    # Check if PM2 is installed
    if ! command -v pm2 &> /dev/null; then
        log "Instalando PM2 globalmente..."
        npm install -g pm2
    fi
    
    # Install dependencies
    log "Instalando dependências..."
    npm install --production
    
    # Start/restart with PM2
    if pm2 list | grep -q "digimundo-production"; then
        log "Reiniciando aplicação..."
        pm2 restart ecosystem.config.js --env production
    else
        log "Iniciando aplicação..."
        pm2 start ecosystem.config.js --env production
    fi
    
    # Start metrics server
    if ! pm2 list | grep -q "digimundo-metrics"; then
        pm2 start production/metrics-server.js --name digimundo-metrics
    fi
    
    # Save PM2 configuration
    pm2 save
    
    success "Deployment com PM2 concluído!"
    
    # Show PM2 status
    pm2 status
    show_endpoints
}

# Deploy for development
deploy_development() {
    log "🛠️ Iniciando deployment de desenvolvimento..."
    
    # Use development compose file
    docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d
    
    log "Aguardando serviços iniciarem..."
    sleep 15
    
    success "Deployment de desenvolvimento concluído!"
    
    echo ""
    echo -e "${YELLOW}Endpoints de desenvolvimento:${NC}"
    echo "• App: http://localhost:7937"
    echo "• SQLite Browser: http://localhost:8080"
    echo "• Debug port: 9229"
    echo ""
    echo "Para logs em tempo real: docker-compose logs -f digimundo-app"
}

# Check service health
check_health_endpoints() {
    log "🏥 Verificando health dos serviços..."
    
    local max_attempts=30
    local attempt=1
    
    while [ $attempt -le $max_attempts ]; do
        echo -n "Tentativa $attempt/$max_attempts... "
        
        if curl -f http://localhost:7937/health > /dev/null 2>&1; then
            success "Aplicação está saudável!"
            break
        else
            echo "aguardando..."
            sleep 5
            attempt=$((attempt + 1))
        fi
    done
    
    if [ $attempt -gt $max_attempts ]; then
        warning "Health check timeout. Serviço pode ainda estar inicializando."
    fi
    
    # Check other services
    if curl -f http://localhost:9090/health > /dev/null 2>&1; then
        success "Servidor de métricas está saudável!"
    else
        warning "Servidor de métricas não está respondendo"
    fi
}

# Show service endpoints
show_endpoints() {
    echo ""
    echo -e "${GREEN}✅ Digimundo está rodando!${NC}"
    echo ""
    echo -e "${YELLOW}📍 Endpoints principais:${NC}"
    echo "• Aplicação: http://localhost:7937"
    echo "• Health Check: http://localhost:7937/health"
    echo "• GraphQL: http://localhost:7937/graphql"
    echo "• GraphQL Playground: http://localhost:7937/playground"
    echo ""
    echo -e "${YELLOW}📊 Monitoramento:${NC}"
    echo "• Métricas: http://localhost:9090/metrics"
    echo "• Status do Sistema: http://localhost:9090/status"
    echo "• Prometheus: http://localhost:9091 (se habilitado)"
    echo "• Grafana: http://localhost:3000 (se habilitado)"
    echo ""
    echo -e "${YELLOW}🛠️ Comandos úteis:${NC}"
    echo "• Monitoramento: ./production/scripts/monitor.sh dashboard"
    echo "• Backup: ./production/scripts/backup.sh"
    echo "• Logs: docker-compose logs -f"
    echo "• Status: docker-compose ps"
    echo ""
}

# Check current status
check_status() {
    log "📊 Verificando status atual..."
    
    echo ""
    echo -e "${YELLOW}🐳 Docker Containers:${NC}"
    if docker-compose ps 2>/dev/null; then
        echo ""
    else
        echo "Nenhum container Docker Compose encontrado"
    fi
    
    echo -e "${YELLOW}⚡ PM2 Processes:${NC}"
    if command -v pm2 &> /dev/null; then
        pm2 list 2>/dev/null || echo "Nenhum processo PM2 encontrado"
    else
        echo "PM2 não instalado"
    fi
    
    echo ""
    echo -e "${YELLOW}🌐 Service Health:${NC}"
    
    # Check app
    if curl -f http://localhost:7937/health > /dev/null 2>&1; then
        echo "✅ Aplicação (7937): Saudável"
    else
        echo "❌ Aplicação (7937): Não responde"
    fi
    
    # Check metrics
    if curl -f http://localhost:9090/health > /dev/null 2>&1; then
        echo "✅ Métricas (9090): Saudável"
    else
        echo "❌ Métricas (9090): Não responde"
    fi
    
    # Check Redis
    if docker exec digimundo-redis redis-cli ping > /dev/null 2>&1; then
        echo "✅ Redis: Saudável"
    else
        echo "❌ Redis: Não responde"
    fi
    
    echo ""
}

# Show management menu
show_management_menu() {
    while true; do
        echo ""
        echo -e "${YELLOW}🎛️ Gerenciamento do Digimundo:${NC}"
        echo "1) Ver status dos serviços"
        echo "2) Ver logs em tempo real"
        echo "3) Reiniciar serviços"
        echo "4) Parar serviços"
        echo "5) Fazer backup"
        echo "6) Monitoramento dashboard"
        echo "7) Abrir endpoints no navegador"
        echo "8) Limpar recursos"
        echo "0) Sair"
        echo ""
        
        read -p "Escolha uma opção (0-8): " mgmt_choice
        
        case $mgmt_choice in
            1)
                check_status
                ;;
            2)
                echo "Pressione Ctrl+C para sair dos logs"
                sleep 2
                docker-compose logs -f || pm2 logs
                ;;
            3)
                log "Reiniciando serviços..."
                docker-compose restart 2>/dev/null || pm2 restart all
                success "Serviços reiniciados"
                ;;
            4)
                log "Parando serviços..."
                docker-compose down 2>/dev/null || pm2 stop all
                success "Serviços parados"
                ;;
            5)
                if [ -f "production/scripts/backup.sh" ]; then
                    ./production/scripts/backup.sh
                else
                    warning "Script de backup não encontrado"
                fi
                ;;
            6)
                if [ -f "production/scripts/monitor.sh" ]; then
                    ./production/scripts/monitor.sh dashboard
                else
                    warning "Script de monitoramento não encontrado"
                fi
                ;;
            7)
                log "Abrindo endpoints no navegador..."
                if command -v open &> /dev/null; then
                    open http://localhost:7937
                    open http://localhost:7937/playground
                elif command -v xdg-open &> /dev/null; then
                    xdg-open http://localhost:7937
                    xdg-open http://localhost:7937/playground
                else
                    echo "Abra manualmente: http://localhost:7937"
                fi
                ;;
            8)
                log "Limpando recursos..."
                docker system prune -f 2>/dev/null || true
                pm2 delete all 2>/dev/null || true
                success "Recursos limpos"
                ;;
            0)
                success "Saindo..."
                break
                ;;
            *)
                error "Opção inválida"
                ;;
        esac
    done
}

# Main function
main() {
    clear
    show_logo
    
    log "🚀 Bem-vindo ao Digimundo Production Quick Start!"
    
    check_prerequisites
    setup_environment
    
    # Check if already running
    if curl -f http://localhost:7937/health > /dev/null 2>&1; then
        success "Digimundo já está rodando!"
        show_endpoints
        show_management_menu
    else
        choose_deployment
        
        if curl -f http://localhost:7937/health > /dev/null 2>&1; then
            show_management_menu
        fi
    fi
}

# Error handler
handle_error() {
    error "Erro na linha $1"
    echo ""
    echo "Para debug:"
    echo "• docker-compose logs"
    echo "• pm2 logs"
    echo "• ./production/scripts/monitor.sh status"
    exit 1
}

trap 'handle_error $LINENO' ERR

# Run main function
main "$@"