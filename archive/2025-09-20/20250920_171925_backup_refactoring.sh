#!/bin/bash

# 🛡️ Script de Backup do Digimundo antes da Refatoração
# Data: $(date +"%Y-%m-%d_%H-%M-%S")

TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_DIR="$HOME/Digimundo/ARCHIVES/backups/refactoring_${TIMESTAMP}"

echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║         🛡️  BACKUP DO DIGIMUNDO - REFATORAÇÃO                ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""
echo "📁 Criando backup em: $BACKUP_DIR"

# Criar diretório de backup
mkdir -p "$BACKUP_DIR"

# Copiar arquivos críticos do PRODUCTION
echo "📦 Fazendo backup do PRODUCTION/core/digimundo_starter..."
cp -r "$HOME/Digimundo/PRODUCTION/core/digimundo_starter" "$BACKUP_DIR/" 2>/dev/null

# Copiar arquivos de configuração importantes
echo "⚙️  Fazendo backup de configurações..."
cp "$HOME/Digimundo/package.json" "$BACKUP_DIR/" 2>/dev/null
cp "$HOME/Digimundo/package-lock.json" "$BACKUP_DIR/" 2>/dev/null
cp -r "$HOME/Digimundo/CONFIG" "$BACKUP_DIR/" 2>/dev/null

# Copiar scripts de lançamento
echo "🚀 Fazendo backup de scripts..."
cp "$HOME/Digimundo/LAUNCH_DIGIMUNDO.sh" "$BACKUP_DIR/" 2>/dev/null
cp "$HOME/Digimundo/VALIDATE_DIGIMUNDO.sh" "$BACKUP_DIR/" 2>/dev/null
cp "$HOME/Digimundo/DIGIMUNDO_EVOLUTION.js" "$BACKUP_DIR/" 2>/dev/null
cp "$HOME/Digimundo/DIGIMUNDO_TERMINAL.js" "$BACKUP_DIR/" 2>/dev/null

# Criar arquivo de informações do backup
cat > "$BACKUP_DIR/backup_info.txt" << EOF
🛡️ BACKUP DO DIGIMUNDO - REFATORAÇÃO
=====================================
Data: $(date)
Motivo: Refatoração completa do sistema
Problemas a resolver:
- Arquitetura Electron quebrada
- Memory leaks críticos (2.2GB idle)
- Problemas de segurança
- Múltiplos cérebros sem orquestração
=====================================
EOF

# Comprimir backup
echo "🗜️  Comprimindo backup..."
cd "$HOME/Digimundo/ARCHIVES/backups"
tar -czf "digimundo_backup_refactoring_${TIMESTAMP}.tar.gz" "refactoring_${TIMESTAMP}"

# Verificar tamanho do backup
BACKUP_SIZE=$(du -sh "digimundo_backup_refactoring_${TIMESTAMP}.tar.gz" | cut -f1)

echo ""
echo "✅ Backup concluído com sucesso!"
echo "📦 Arquivo: digimundo_backup_refactoring_${TIMESTAMP}.tar.gz"
echo "📏 Tamanho: $BACKUP_SIZE"
echo "📁 Local: $HOME/Digimundo/ARCHIVES/backups/"
echo ""
echo "🔧 Pronto para iniciar refatoração!"