#!/bin/bash

# 📊 DIGIMUNDO PRODUCTION MONITORING SCRIPT
# Monitoramento contínuo da aplicação em produção

set -e

# Configuration
CHECK_INTERVAL=30  # seconds
ALERT_THRESHOLD_CPU=80
ALERT_THRESHOLD_MEMORY=85
ALERT_THRESHOLD_DISK=90
ALERT_THRESHOLD_RESPONSE_TIME=5000  # milliseconds
LOG_FILE="/var/log/digimundo_monitor.log"
METRICS_FILE="/tmp/digimundo_metrics.json"

# Service endpoints
HEALTH_URL="http://localhost:7937/health"
METRICS_URL="http://localhost:9090/metrics"
APP_URL="http://localhost:7937"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Logging
log() {
    local message="[$(date +'%Y-%m-%d %H:%M:%S')] $1"
    echo -e "${BLUE}$message${NC}"
    echo "$message" >> "$LOG_FILE"
}

warning() {
    local message="[WARNING] $1"
    echo -e "${YELLOW}$message${NC}"
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $message" >> "$LOG_FILE"
}

error() {
    local message="[ERROR] $1"
    echo -e "${RED}$message${NC}"
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $message" >> "$LOG_FILE"
}

success() {
    local message="[SUCCESS] $1"
    echo -e "${GREEN}$message${NC}"
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $message" >> "$LOG_FILE"
}

# Check if service is running
check_service_status() {
    local service_name=$1
    local container_name=$2
    
    if docker ps --format "table {{.Names}}" | grep -q "$container_name"; then
        local status=$(docker inspect --format='{{.State.Status}}' "$container_name" 2>/dev/null)
        if [ "$status" = "running" ]; then
            return 0
        else
            error "$service_name container status: $status"
            return 1
        fi
    else
        error "$service_name container not found"
        return 1
    fi
}

# Check health endpoint
check_health() {
    local start_time=$(date +%s%3N)
    local response=$(curl -s -w "%{http_code}:%{time_total}" "$HEALTH_URL" 2>/dev/null || echo "000:0")
    local end_time=$(date +%s%3N)
    
    local http_code=$(echo "$response" | cut -d':' -f1)
    local response_time=$(echo "$response" | cut -d':' -f2)
    local response_time_ms=$(echo "$response_time * 1000" | bc -l | cut -d'.' -f1)
    
    if [ "$http_code" = "200" ]; then
        if [ "$response_time_ms" -gt "$ALERT_THRESHOLD_RESPONSE_TIME" ]; then
            warning "Health check slow: ${response_time_ms}ms (threshold: ${ALERT_THRESHOLD_RESPONSE_TIME}ms)"
        fi
        return 0
    else
        error "Health check failed: HTTP $http_code, Response time: ${response_time_ms}ms"
        return 1
    fi
}

# Check application response
check_app_response() {
    local start_time=$(date +%s%3N)
    local response=$(curl -s -w "%{http_code}:%{time_total}" "$APP_URL" 2>/dev/null || echo "000:0")
    local end_time=$(date +%s%3N)
    
    local http_code=$(echo "$response" | cut -d':' -f1)
    local response_time=$(echo "$response" | cut -d':' -f2)
    local response_time_ms=$(echo "$response_time * 1000" | bc -l | cut -d'.' -f1)
    
    if [ "$http_code" = "200" ] || [ "$http_code" = "302" ]; then
        return 0
    else
        error "App response failed: HTTP $http_code, Response time: ${response_time_ms}ms"
        return 1
    fi
}

# Get system metrics
get_system_metrics() {
    # CPU usage
    local cpu_usage=$(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | sed 's/%us,//')
    cpu_usage=${cpu_usage:-0}
    
    # Memory usage
    local memory_info=$(free | grep Mem)
    local total_mem=$(echo $memory_info | awk '{print $2}')
    local used_mem=$(echo $memory_info | awk '{print $3}')
    local memory_usage=$(echo "scale=1; $used_mem * 100 / $total_mem" | bc)
    
    # Disk usage
    local disk_usage=$(df / | tail -1 | awk '{print $5}' | sed 's/%//')
    
    # Docker stats
    local docker_stats=$(docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemPerc}}" 2>/dev/null | grep digimundo || echo "")
    
    # Save metrics to JSON
    cat > "$METRICS_FILE" << EOF
{
    "timestamp": "$(date -Iseconds)",
    "system": {
        "cpu_usage": $cpu_usage,
        "memory_usage": $memory_usage,
        "disk_usage": $disk_usage
    },
    "docker": {
        "stats": "$docker_stats"
    }
}
EOF
    
    echo "$cpu_usage:$memory_usage:$disk_usage"
}

# Check resource usage
check_resources() {
    local metrics=$(get_system_metrics)
    local cpu_usage=$(echo "$metrics" | cut -d':' -f1)
    local memory_usage=$(echo "$metrics" | cut -d':' -f2)
    local disk_usage=$(echo "$metrics" | cut -d':' -f3)
    
    # Remove decimal points for comparison
    cpu_usage=${cpu_usage%.*}
    memory_usage=${memory_usage%.*}
    disk_usage=${disk_usage%.*}
    
    local alerts=0
    
    if [ "$cpu_usage" -gt "$ALERT_THRESHOLD_CPU" ]; then
        warning "High CPU usage: ${cpu_usage}% (threshold: ${ALERT_THRESHOLD_CPU}%)"
        alerts=$((alerts + 1))
    fi
    
    if [ "$memory_usage" -gt "$ALERT_THRESHOLD_MEMORY" ]; then
        warning "High memory usage: ${memory_usage}% (threshold: ${ALERT_THRESHOLD_MEMORY}%)"
        alerts=$((alerts + 1))
    fi
    
    if [ "$disk_usage" -gt "$ALERT_THRESHOLD_DISK" ]; then
        warning "High disk usage: ${disk_usage}% (threshold: ${ALERT_THRESHOLD_DISK}%)"
        alerts=$((alerts + 1))
    fi
    
    return $alerts
}

# Check Docker containers
check_containers() {
    local containers=("digimundo-production" "digimundo-redis" "digimundo-metrics")
    local failed=0
    
    for container in "${containers[@]}"; do
        if ! check_service_status "$container" "$container"; then
            failed=$((failed + 1))
        fi
    done
    
    return $failed
}

# Get application metrics
get_app_metrics() {
    if curl -f "$METRICS_URL" > /dev/null 2>&1; then
        # Parse Prometheus metrics
        local metrics=$(curl -s "$METRICS_URL" 2>/dev/null)
        
        # Extract key metrics
        local http_requests=$(echo "$metrics" | grep "digimundo_http_requests_total" | tail -1 | awk '{print $2}')
        local memory_usage=$(echo "$metrics" | grep "digimundo_memory_usage_bytes" | tail -1 | awk '{print $2}')
        local active_digimons=$(echo "$metrics" | grep "digimundo_active_digimons" | tail -1 | awk '{print $2}')
        
        log "App Metrics - Requests: ${http_requests:-0}, Memory: ${memory_usage:-0} bytes, Active Digimons: ${active_digimons:-0}"
    else
        warning "Could not fetch application metrics"
    fi
}

# Check log files for errors
check_logs() {
    local error_count=0
    
    # Check application logs for errors in last 5 minutes
    if [ -f "/app/logs/error.log" ]; then
        local recent_errors=$(find /app/logs -name "*.log" -mmin -5 -exec grep -i "error\|fatal\|exception" {} \; 2>/dev/null | wc -l)
        if [ "$recent_errors" -gt 0 ]; then
            warning "Found $recent_errors recent errors in logs"
            error_count=$((error_count + recent_errors))
        fi
    fi
    
    # Check Docker container logs
    local docker_errors=$(docker logs digimundo-production --since=5m 2>&1 | grep -i "error\|fatal\|exception" | wc -l)
    if [ "$docker_errors" -gt 0 ]; then
        warning "Found $docker_errors recent errors in Docker logs"
        error_count=$((error_count + docker_errors))
    fi
    
    return $error_count
}

# Send alert
send_alert() {
    local severity=$1
    local message=$2
    
    # Log the alert
    case $severity in
        "critical")
            error "CRITICAL ALERT: $message"
            ;;
        "warning")
            warning "WARNING ALERT: $message"
            ;;
        "info")
            log "INFO ALERT: $message"
            ;;
    esac
    
    # Here you can add notification logic (email, Slack, Discord, etc.)
    # Example:
    # curl -X POST -H 'Content-type: application/json' \
    #   --data "{\"text\":\"Digimundo $severity: $message\"}" \
    #   "$SLACK_WEBHOOK_URL" 2>/dev/null || true
}

# Auto-restart services if needed
auto_restart() {
    local service=$1
    
    log "Attempting to restart $service..."
    
    case $service in
        "app")
            docker-compose restart digimundo-app
            sleep 30
            if check_health; then
                success "Successfully restarted application"
                send_alert "info" "Application auto-restarted successfully"
            else
                error "Failed to restart application"
                send_alert "critical" "Application restart failed"
            fi
            ;;
        "redis")
            docker-compose restart digimundo-redis
            sleep 10
            success "Redis restarted"
            ;;
        "metrics")
            docker-compose restart digimundo-metrics
            sleep 10
            success "Metrics service restarted"
            ;;
    esac
}

# Main monitoring loop
monitor() {
    log "🚀 Starting Digimundo monitoring..."
    log "Check interval: ${CHECK_INTERVAL}s"
    log "Thresholds - CPU: ${ALERT_THRESHOLD_CPU}%, Memory: ${ALERT_THRESHOLD_MEMORY}%, Disk: ${ALERT_THRESHOLD_DISK}%"
    
    local consecutive_failures=0
    local max_consecutive_failures=3
    
    while true; do
        local status_ok=true
        local issues=()
        
        # Check containers
        if ! check_containers; then
            status_ok=false
            issues+=("Container issues detected")
        fi
        
        # Check health endpoint
        if ! check_health; then
            status_ok=false
            issues+=("Health check failed")
        fi
        
        # Check app response
        if ! check_app_response; then
            status_ok=false
            issues+=("Application not responding")
        fi
        
        # Check resources
        if ! check_resources; then
            issues+=("Resource usage high")
        fi
        
        # Check logs
        if ! check_logs; then
            issues+=("Recent errors in logs")
        fi
        
        # Get app metrics
        get_app_metrics
        
        if [ "$status_ok" = true ]; then
            consecutive_failures=0
            if [ ${#issues[@]} -eq 0 ]; then
                log "✅ All systems operational"
            else
                warning "⚠️ Issues detected: ${issues[*]}"
            fi
        else
            consecutive_failures=$((consecutive_failures + 1))
            error "❌ System issues detected: ${issues[*]}"
            
            if [ $consecutive_failures -ge $max_consecutive_failures ]; then
                send_alert "critical" "System down for $consecutive_failures consecutive checks"
                
                # Attempt auto-restart
                log "Attempting auto-restart after $consecutive_failures failures..."
                auto_restart "app"
                consecutive_failures=0
            fi
        fi
        
        sleep $CHECK_INTERVAL
    done
}

# Show monitoring dashboard
show_dashboard() {
    clear
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║                   🚀 DIGIMUNDO MONITORING                    ║"
    echo "╠══════════════════════════════════════════════════════════════╣"
    
    # System status
    echo "║ SYSTEM STATUS                                                ║"
    if check_containers > /dev/null 2>&1; then
        echo "║ ✅ Containers: Running                                       ║"
    else
        echo "║ ❌ Containers: Issues detected                              ║"
    fi
    
    if check_health > /dev/null 2>&1; then
        echo "║ ✅ Health Check: OK                                         ║"
    else
        echo "║ ❌ Health Check: Failed                                     ║"
    fi
    
    # Resource usage
    local metrics=$(get_system_metrics)
    local cpu_usage=$(echo "$metrics" | cut -d':' -f1)
    local memory_usage=$(echo "$metrics" | cut -d':' -f2)
    local disk_usage=$(echo "$metrics" | cut -d':' -f3)
    
    echo "║                                                              ║"
    echo "║ RESOURCE USAGE                                               ║"
    printf "║ CPU: %3s%%  Memory: %3s%%  Disk: %3s%%                          ║\n" "${cpu_usage%.*}" "${memory_usage%.*}" "${disk_usage%.*}"
    
    echo "║                                                              ║"
    echo "║ SERVICES                                                     ║"
    
    # Check each service
    for service in "digimundo-production" "digimundo-redis" "digimundo-metrics"; do
        if check_service_status "$service" "$service" > /dev/null 2>&1; then
            printf "║ ✅ %-20s Running                              ║\n" "$service"
        else
            printf "║ ❌ %-20s Stopped                              ║\n" "$service"
        fi
    done
    
    echo "║                                                              ║"
    echo "║ Last updated: $(date +'%Y-%m-%d %H:%M:%S')                          ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
}

# Show help
show_help() {
    cat << EOF
🔍 Digimundo Production Monitoring

Usage: $0 [COMMAND]

Commands:
    monitor     Start continuous monitoring (default)
    dashboard   Show real-time dashboard
    status      Show current status
    metrics     Show current metrics
    logs        Show recent logs
    help        Show this help

Options:
    --interval SECONDS    Set check interval (default: 30)
    --no-alerts          Disable alert notifications
    --quiet             Reduce log output

Examples:
    $0                   # Start monitoring
    $0 dashboard         # Show dashboard
    $0 status            # Quick status check
    $0 --interval 60     # Monitor with 60s interval
EOF
}

# Parse arguments
parse_args() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            monitor)
                COMMAND="monitor"
                shift
                ;;
            dashboard)
                COMMAND="dashboard"
                shift
                ;;
            status)
                COMMAND="status"
                shift
                ;;
            metrics)
                COMMAND="metrics"
                shift
                ;;
            logs)
                COMMAND="logs"
                shift
                ;;
            help|--help|-h)
                show_help
                exit 0
                ;;
            --interval)
                CHECK_INTERVAL="$2"
                shift 2
                ;;
            --no-alerts)
                NO_ALERTS=true
                shift
                ;;
            --quiet)
                QUIET=true
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

# Main function
main() {
    # Create log file if it doesn't exist
    touch "$LOG_FILE"
    
    case ${COMMAND:-monitor} in
        monitor)
            monitor
            ;;
        dashboard)
            while true; do
                show_dashboard
                sleep 5
            done
            ;;
        status)
            log "Checking system status..."
            check_containers
            check_health
            check_resources
            ;;
        metrics)
            get_app_metrics
            cat "$METRICS_FILE" 2>/dev/null || echo "No metrics available"
            ;;
        logs)
            tail -50 "$LOG_FILE"
            ;;
        *)
            show_help
            ;;
    esac
}

# Set up signal handlers
cleanup() {
    log "Monitoring stopped"
    exit 0
}

trap cleanup SIGINT SIGTERM

# Parse arguments and run
parse_args "$@"
main