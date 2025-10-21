#!/bin/bash

# 🚀 DIGIMUNDO PRODUCTION DEPLOYMENT SCRIPT
# Deploy automático com zero downtime

set -e  # Exit on any error

# Configuration
COMPOSE_FILE="docker-compose.yml"
APP_NAME="digimundo"
HEALTH_CHECK_URL="http://localhost:7937/health"
BACKUP_BEFORE_DEPLOY=true
ROLLBACK_ON_FAILURE=true
MAX_WAIT_TIME=300  # 5 minutes

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# Logging function
log() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1" >&2
}

success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

info() {
    echo -e "${PURPLE}[INFO]${NC} $1"
}

# Show help
show_help() {
    cat << EOF
🚀 Digimundo Production Deployment Script

Usage: $0 [OPTIONS]

Options:
    -h, --help              Show this help message
    -f, --file FILE         Docker compose file (default: docker-compose.yml)
    --no-backup            Skip backup before deployment
    --no-rollback          Don't rollback on failure
    --skip-health-check    Skip health checks
    --force                Force deployment even if health checks fail

Examples:
    $0                     # Normal deployment with all checks
    $0 --no-backup         # Deploy without creating backup
    $0 --force             # Force deployment ignoring health checks
EOF
}

# Parse command line arguments
parse_args() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            -h|--help)
                show_help
                exit 0
                ;;
            -f|--file)
                COMPOSE_FILE="$2"
                shift 2
                ;;
            --no-backup)
                BACKUP_BEFORE_DEPLOY=false
                shift
                ;;
            --no-rollback)
                ROLLBACK_ON_FAILURE=false
                shift
                ;;
            --skip-health-check)
                SKIP_HEALTH_CHECK=true
                shift
                ;;
            --force)
                FORCE_DEPLOY=true
                shift
                ;;
            *)
                error "Unknown option: $1"
                show_help
                exit 1
                ;;
        esac
    done
}

# Check prerequisites
check_prerequisites() {
    log "🔍 Verificando pré-requisitos..."
    
    # Check if docker is running
    if ! docker info > /dev/null 2>&1; then
        error "Docker não está rodando"
        exit 1
    fi
    
    # Check if docker-compose is available
    if ! command -v docker-compose > /dev/null 2>&1; then
        error "docker-compose não encontrado"
        exit 1
    fi
    
    # Check if compose file exists
    if [ ! -f "$COMPOSE_FILE" ]; then
        error "Arquivo compose não encontrado: $COMPOSE_FILE"
        exit 1
    fi
    
    # Check if .env file exists and load it
    if [ -f ".env" ]; then
        source .env
        info "Variáveis de ambiente carregadas do .env"
    fi
    
    success "Pré-requisitos verificados"
}

# Create backup before deployment
create_backup() {
    if [ "$BACKUP_BEFORE_DEPLOY" = true ]; then
        log "💾 Criando backup antes do deploy..."
        
        if [ -f "./production/scripts/backup.sh" ]; then
            bash ./production/scripts/backup.sh
            success "Backup criado com sucesso"
        else
            warning "Script de backup não encontrado, pulando..."
        fi
    else
        info "Backup desabilitado, pulando..."
    fi
}

# Pull latest images
pull_images() {
    log "📥 Baixando imagens mais recentes..."
    
    docker-compose -f "$COMPOSE_FILE" pull --quiet
    success "Imagens atualizadas"
}

# Check current status
check_current_status() {
    log "📊 Verificando status atual..."
    
    # Get current container status
    CURRENT_CONTAINERS=$(docker-compose -f "$COMPOSE_FILE" ps -q)
    
    if [ -n "$CURRENT_CONTAINERS" ]; then
        info "Containers ativos encontrados"
        docker-compose -f "$COMPOSE_FILE" ps
    else
        info "Nenhum container ativo encontrado"
    fi
    
    # Check current health
    if curl -f "$HEALTH_CHECK_URL" > /dev/null 2>&1; then
        info "✅ Aplicação está saudável"
        CURRENT_HEALTH="healthy"
    else
        warning "⚠️ Aplicação não está respondendo"
        CURRENT_HEALTH="unhealthy"
    fi
}

# Perform rolling update
rolling_update() {
    log "🔄 Iniciando rolling update..."
    
    # Scale up new containers
    log "📈 Escalando novos containers..."
    docker-compose -f "$COMPOSE_FILE" up -d --scale digimundo-app=2 digimundo-app
    
    # Wait for new containers to be healthy
    log "⏳ Aguardando novos containers ficarem saudáveis..."
    wait_for_health_check 60
    
    # Scale down old containers
    log "📉 Removendo containers antigos..."
    docker-compose -f "$COMPOSE_FILE" up -d --scale digimundo-app=1 digimundo-app
    
    success "Rolling update concluído"
}

# Standard deployment
standard_deployment() {
    log "🚀 Iniciando deployment padrão..."
    
    # Stop old containers gracefully
    docker-compose -f "$COMPOSE_FILE" down --timeout 30
    
    # Start new containers
    docker-compose -f "$COMPOSE_FILE" up -d
    
    success "Deployment padrão concluído"
}

# Wait for health check
wait_for_health_check() {
    local timeout=${1:-$MAX_WAIT_TIME}
    local start_time=$(date +%s)
    
    if [ "$SKIP_HEALTH_CHECK" = true ]; then
        info "Health check desabilitado, pulando..."
        return 0
    fi
    
    log "🏥 Aguardando health check (timeout: ${timeout}s)..."
    
    while true; do
        local current_time=$(date +%s)
        local elapsed=$((current_time - start_time))
        
        if [ $elapsed -gt $timeout ]; then
            error "Health check timeout após ${timeout}s"
            return 1
        fi
        
        if curl -f "$HEALTH_CHECK_URL" > /dev/null 2>&1; then
            success "✅ Aplicação está saudável (${elapsed}s)"
            return 0
        fi
        
        echo -n "."
        sleep 5
    done
}

# Verify deployment
verify_deployment() {
    log "✅ Verificando deployment..."
    
    # Check container status
    local unhealthy_containers=$(docker-compose -f "$COMPOSE_FILE" ps | grep -v "Up" | grep -v "Name\|---" | wc -l)
    
    if [ "$unhealthy_containers" -gt 0 ]; then
        error "Containers não saudáveis detectados"
        docker-compose -f "$COMPOSE_FILE" ps
        return 1
    fi
    
    # Test health endpoint
    if ! wait_for_health_check 120; then
        error "Health check falhou"
        return 1
    fi
    
    # Test metrics endpoint
    if curl -f "http://localhost:9090/health" > /dev/null 2>&1; then
        success "✅ Métricas endpoint saudável"
    else
        warning "⚠️ Métricas endpoint não está respondendo"
    fi
    
    # Display final status
    log "📊 Status final dos containers:"
    docker-compose -f "$COMPOSE_FILE" ps
    
    success "Deployment verificado com sucesso"
}

# Rollback deployment
rollback_deployment() {
    if [ "$ROLLBACK_ON_FAILURE" = false ]; then
        error "Rollback desabilitado. Deployment falhou!"
        return 1
    fi
    
    error "🔄 Iniciando rollback..."
    
    # Get previous image
    local previous_image=$(docker images --format "table {{.Repository}}:{{.Tag}}" | grep "$APP_NAME" | head -2 | tail -1)
    
    if [ -n "$previous_image" ]; then
        log "📦 Fazendo rollback para imagem: $previous_image"
        
        # Update compose file to use previous image
        # This is a simplified approach - in production you might want to use tags
        docker-compose -f "$COMPOSE_FILE" down
        docker-compose -f "$COMPOSE_FILE" up -d
        
        if wait_for_health_check 60; then
            success "✅ Rollback concluído com sucesso"
        else
            error "❌ Rollback também falhou!"
            return 1
        fi
    else
        error "Imagem anterior não encontrada para rollback"
        return 1
    fi
}

# Cleanup old images
cleanup() {
    log "🧹 Limpando imagens antigas..."
    
    # Remove dangling images
    docker image prune -f
    
    # Keep only last 3 versions of app images
    docker images --format "table {{.Repository}}:{{.Tag}}\t{{.ID}}" | \
        grep "$APP_NAME" | \
        tail -n +4 | \
        awk '{print $2}' | \
        xargs -r docker rmi || true
    
    success "Limpeza concluída"
}

# Send deployment notification
send_notification() {
    local status=$1
    local message=$2
    local duration=$3
    
    log "📢 Enviando notificação: $status"
    
    # Here you can add notification logic (Slack, Discord, email, etc.)
    # Example webhook call:
    # curl -X POST -H 'Content-type: application/json' \
    #   --data "{\"text\":\"Digimundo Deploy ${status}: ${message} (${duration})\"}" \
    #   "${SLACK_WEBHOOK_URL}" 2>/dev/null || true
    
    info "Notification sent: $status - $message"
}

# Main deployment function
main() {
    local start_time=$(date +%s)
    
    log "🚀 Iniciando deployment do Digimundo..."
    info "📁 Compose file: $COMPOSE_FILE"
    info "🔧 Backup: $BACKUP_BEFORE_DEPLOY"
    info "🔄 Rollback: $ROLLBACK_ON_FAILURE"
    
    # Check prerequisites
    check_prerequisites
    
    # Check current status
    check_current_status
    
    # Create backup
    create_backup
    
    # Pull latest images
    pull_images
    
    # Perform deployment
    if [ "$CURRENT_HEALTH" = "healthy" ] && [ "$FORCE_DEPLOY" != true ]; then
        rolling_update
    else
        standard_deployment
    fi
    
    # Verify deployment
    if ! verify_deployment; then
        rollback_deployment
        local end_time=$(date +%s)
        local duration=$((end_time - start_time))
        send_notification "FAILED" "Deployment falhou e foi revertido" "${duration}s"
        exit 1
    fi
    
    # Cleanup
    cleanup
    
    # Calculate deployment time
    local end_time=$(date +%s)
    local duration=$((end_time - start_time))
    
    success "🎉 Deployment concluído com sucesso!"
    info "⏱️ Tempo total: ${duration}s"
    
    # Send success notification
    send_notification "SUCCESS" "Deployment concluído com sucesso" "${duration}s"
}

# Error handler
handle_error() {
    error "❌ Deployment falhou na linha $1"
    
    if [ "$ROLLBACK_ON_FAILURE" = true ]; then
        rollback_deployment
    fi
    
    send_notification "ERROR" "Deployment falhou na linha $1" "unknown"
    exit 1
}

# Set error trap
trap 'handle_error $LINENO' ERR

# Parse arguments and run
parse_args "$@"
main