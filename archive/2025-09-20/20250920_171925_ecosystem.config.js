module.exports = {
  apps: [
    {
      name: 'digimundo-production',
      script: './app/server/index.js',
      instances: 4,
      exec_mode: 'cluster',
      watch: false,
      max_memory_restart: '1G',
      env: {
        NODE_ENV: 'development',
        PORT: 7937,
        LOG_LEVEL: 'info'
      },
      env_production: {
        NODE_ENV: 'production',
        PORT: 7937,
        LOG_LEVEL: 'error',
        REDIS_URL: 'redis://localhost:6379',
        ENABLE_METRICS: 'true',
        DISABLE_CONSOLE_LOGS: 'true'
      },
      error_file: './logs/err.log',
      out_file: './logs/out.log',
      log_file: './logs/combined.log',
      time: true,
      autorestart: true,
      restart_delay: 5000,
      max_restarts: 10,
      min_uptime: '10s',
      kill_timeout: 5000,
      // CPU-based auto-scaling
      min_instances: 2,
      max_instances: 8,
      // Memory threshold for scaling
      max_memory_threshold: 80,
      // Advanced monitoring
      pmx: true,
      // Health check
      health_check_grace_period: 3000,
      health_check_fatal_exceptions: true,
      // Log rotation
      log_date_format: 'YYYY-MM-DD HH:mm:ss Z',
      merge_logs: true,
      // Process management
      ignore_watch: ['node_modules', 'logs', '*.log'],
      watch_options: {
        followSymlinks: false
      },
      // Performance optimizations
      node_args: '--max-old-space-size=1024 --optimize-for-size',
      // Custom env for production optimizations
      env_production_extended: {
        NODE_ENV: 'production',
        PORT: 7937,
        LOG_LEVEL: 'warn',
        REDIS_URL: 'redis://localhost:6379',
        ENABLE_METRICS: 'true',
        DISABLE_CONSOLE_LOGS: 'true',
        GZIP_COMPRESSION: 'true',
        ENABLE_RATE_LIMITING: 'true',
        HELMET_SECURITY: 'true',
        CONNECTION_POOL_SIZE: '20',
        CACHE_TTL: '300',
        PROMETHEUS_METRICS: 'true',
        HEALTH_CHECK_INTERVAL: '30000',
        AUTO_SCALING: 'true',
        CPU_THRESHOLD: '70',
        MEMORY_THRESHOLD: '80'
      }
    },
    {
      name: 'digimundo-metrics',
      script: './production/metrics-server.js',
      instances: 1,
      exec_mode: 'fork',
      env_production: {
        NODE_ENV: 'production',
        METRICS_PORT: 9090,
        PROMETHEUS_ENABLED: 'true'
      },
      autorestart: true,
      max_memory_restart: '200M'
    }
  ],
  
  deploy: {
    production: {
      user: 'deploy',
      host: 'your-server.com',
      ref: 'origin/main',
      repo: 'git@github.com:your-repo/digimundo.git',
      path: '/var/www/digimundo',
      'pre-deploy-local': '',
      'post-deploy': 'npm install && npm run build && pm2 reload ecosystem.config.js --env production',
      'pre-setup': '',
      'ssh_options': 'StrictHostKeyChecking=no'
    }
  }
}