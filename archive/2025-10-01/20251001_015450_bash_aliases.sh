#!/bin/bash
# Git-Memory Bash Aliases
#
# Usage: Add to your ~/.bashrc or ~/.zshrc:
#   source /path/to/scripturemon-clean/scripts/workflows/bash_aliases.sh
#
# Or copy these aliases directly to your shell config

# Get scripturemon root directory
SCRIPTUREMON_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

# Workflow shortcuts
alias gm-start="$SCRIPTUREMON_ROOT/scripts/workflows/start_session.sh"
alias gm-complete="$SCRIPTUREMON_ROOT/scripts/workflows/complete_phase.sh"

# Context recovery
alias gm-recap="python3 $SCRIPTUREMON_ROOT/scripts/git_session_summary.py --last 5"
alias gm-recap10="python3 $SCRIPTUREMON_ROOT/scripts/git_session_summary.py --last 10"
alias gm-recap-json="python3 $SCRIPTUREMON_ROOT/scripts/git_session_summary.py --last 5 --json"

# TODO extraction
alias gm-todos="python3 $SCRIPTUREMON_ROOT/scripts/extract_tasks_from_git.py"
alias gm-todos-high="python3 $SCRIPTUREMON_ROOT/scripts/extract_tasks_from_git.py --priority HIGH"
alias gm-todos-critical="python3 $SCRIPTUREMON_ROOT/scripts/extract_tasks_from_git.py --priority CRITICAL"
alias gm-todos-json="python3 $SCRIPTUREMON_ROOT/scripts/extract_tasks_from_git.py --json"

# Knowledge mining
alias gm-mine="python3 $SCRIPTUREMON_ROOT/scripts/mine_knowledge_from_commits.py"
alias gm-mine-bugs="python3 $SCRIPTUREMON_ROOT/scripts/mine_knowledge_from_commits.py --type bugfix"
alias gm-mine-refactor="python3 $SCRIPTUREMON_ROOT/scripts/mine_knowledge_from_commits.py --type refactor"
alias gm-mine-perf="python3 $SCRIPTUREMON_ROOT/scripts/mine_knowledge_from_commits.py --type performance"

# Memory inspection
alias gm-commits="ls -lht $SCRIPTUREMON_ROOT/memory/commits/ | head -20"
alias gm-checkpoints="ls -lht $SCRIPTUREMON_ROOT/memory/checkpoints/ | head -20"
alias gm-knowledge="ls -lht $SCRIPTUREMON_ROOT/memory/knowledge/ | head -20"
alias gm-tasks="cat $SCRIPTUREMON_ROOT/memory/tasks/pending.json | python3 -m json.tool"

# Git shortcuts with memory context
alias gm-status="git status && echo '' && echo '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━' && echo '' && gm-recap"
alias gm-log="git log --oneline --graph --all -10 && echo '' && gm-todos-high"

# Help
alias gm-help="cat $SCRIPTUREMON_ROOT/scripts/workflows/README.md"

# Echo loaded status
echo "✅ Git-Memory aliases loaded!"
echo ""
echo "Quick commands:"
echo "  gm-start         - Start new session"
echo "  gm-recap         - See last 5 commits"
echo "  gm-todos-high    - See HIGH priority TODOs"
echo "  gm-mine          - Mine knowledge from commits"
echo "  gm-complete      - Complete a phase"
echo "  gm-help          - Full documentation"
echo ""
