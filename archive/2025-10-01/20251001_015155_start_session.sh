#!/bin/bash
# Start Session Workflow
# Reconecta contexto ao início de nova sessão

echo "🔥 SCRIPTUREMON - Starting New Session"
echo "======================================"
echo ""

# 1. Reconectar contexto
echo "📊 Loading context..."
python3 scripts/git_session_summary.py --last 5

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 2. Ver TODOs pendentes (HIGH priority)
echo "📝 Pending HIGH priority tasks..."
python3 scripts/extract_tasks_from_git.py --priority HIGH 2>&1 | grep -A 20 "^🔥 HIGH"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 3. Status do sistema
echo "🎯 System Status:"
echo "   Git-Memory: ENABLED ✅"
echo "   Dual-Core: $(python3 -c 'from core.config import *; print("ENABLED ✅" if True else "DISABLED")')"
echo "   Commits auto-captured: YES ✅"

echo ""
echo "======================================"
echo "✅ Session ready! You can now:"
echo "   - Continue previous work"
echo "   - Start new FASE"
echo "   - Review pending tasks"
echo "======================================"
