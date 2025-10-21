#!/bin/bash
#
# 🧹 CLEAN SCRIPTUREMON ALIASES - Remove old and setup new
#

echo "🧹 Cleaning old Scripturemon aliases..."

# Backup current .zshrc
cp ~/.zshrc ~/.zshrc.backup.$(date +%Y%m%d_%H%M%S)
echo "✓ Backup created"

# Create cleaned .zshrc without old scripturemon references
grep -v "scripturemon\|^alias s=\|^alias smon=\|^alias roteiro=\|^alias brutal=\|^alias symbiotic=\|SCRIPTUREMON_HOME\|scripturemon-validation\|scripturemon_aliases" ~/.zshrc > ~/.zshrc.clean

# Move cleaned version
mv ~/.zshrc.clean ~/.zshrc
echo "✓ Old aliases removed"

# Add new clean aliases pointing to scripturemon-champion
cat >> ~/.zshrc << 'EOF'

# ═══════════════════════════════════════════════════════════════
# 🎬 SCRIPTUREMON CHAMPION - SILICON VALLEY GRADE
# ═══════════════════════════════════════════════════════════════
export SCRIPTUREMON_HOME="/Users/clubproducoes/Digimundo/scripturemon-champion"

# Main command - launches intelligent startup
alias scripturemon='cd $SCRIPTUREMON_HOME && ./START.sh'

# Short alias
alias s='scripturemon'

# Quick commands (these will be passed to the launcher)
alias s-analyze='cd $SCRIPTUREMON_HOME && python3 bin/scripturemon analyze'
alias s-chat='cd $SCRIPTUREMON_HOME && python3 bin/scripturemon chat'
alias s-status='cd $SCRIPTUREMON_HOME && python3 bin/scripturemon status'
alias s-help='cd $SCRIPTUREMON_HOME && python3 bin/scripturemon help'

# ═══════════════════════════════════════════════════════════════
EOF

echo "✓ New clean aliases added"

# Also create/update scripturemon_aliases.sh if it exists
ALIASES_FILE="$HOME/.digimundo/scripturemon_aliases.sh"
if [ -f "$ALIASES_FILE" ]; then
    echo "🔧 Updating scripturemon_aliases.sh..."
    cat > "$ALIASES_FILE" << 'EOF'
#!/bin/bash
# Scripturemon Champion Aliases
# This file is sourced by .zshrc

# Already defined in .zshrc, kept here for compatibility
export SCRIPTUREMON_HOME="/Users/clubproducoes/Digimundo/scripturemon-champion"
EOF
    echo "✓ scripturemon_aliases.sh updated"
fi

echo ""
echo "✅ Aliases cleaned and updated!"
echo ""
echo "📝 New commands available:"
echo "  scripturemon  - Launch Script Doctor (or just 's')"
echo "  s-analyze     - Quick analyze"
echo "  s-chat        - Quick chat"
echo "  s-status      - System status"
echo "  s-help        - Help"
echo ""
echo "⚡ Please run: source ~/.zshrc"
echo "   Or open a new terminal for changes to take effect"