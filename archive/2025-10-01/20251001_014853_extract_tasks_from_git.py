#!/usr/bin/env python3
"""
Extract Tasks from Git - Extrai TODOs do código e commits

Escaneia:
1. Código atual (TODO:, FIXME:, HACK:, XXX:)
2. CHECKPOINT_SYSTEM.md (tasks documentadas)
3. Commits recentes (TODOs adicionados)

Gera lista priorizada de tasks.

Usage:
    python scripts/extract_tasks_from_git.py
    python scripts/extract_tasks_from_git.py --priority HIGH
    python scripts/extract_tasks_from_git.py --phase FASE2
"""

import sys
import json
import re
import argparse
from pathlib import Path
from typing import List, Dict
import subprocess

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.git_memory_bridge import GitMemoryBridge


def extract_todos_from_code(repo_path: Path) -> List[Dict]:
    """Extrai TODOs do código atual"""
    todos = []

    # Patterns para detectar
    patterns = {
        'TODO': r'#\s*TODO:?\s*(.+)',
        'FIXME': r'#\s*FIXME:?\s*(.+)',
        'HACK': r'#\s*HACK:?\s*(.+)',
        'XXX': r'#\s*XXX:?\s*(.+)',
        'NOTE': r'#\s*NOTE:?\s*(.+)'
    }

    # Escanear arquivos Python
    for py_file in repo_path.rglob('*.py'):
        # Ignorar cache e venv
        if '__pycache__' in str(py_file) or 'venv' in str(py_file):
            continue

        try:
            with open(py_file, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    for todo_type, pattern in patterns.items():
                        match = re.search(pattern, line)
                        if match:
                            todos.append({
                                'type': todo_type,
                                'file': str(py_file.relative_to(repo_path)),
                                'line': line_num,
                                'text': match.group(1).strip(),
                                'priority': _estimate_priority(todo_type, match.group(1)),
                                'source': 'code'
                            })
        except Exception as e:
            # Skip files with encoding issues
            continue

    return todos


def extract_todos_from_checkpoint(repo_path: Path) -> List[Dict]:
    """Extrai tasks do CHECKPOINT_SYSTEM.md"""
    todos = []
    checkpoint_file = repo_path / "docs" / "CHECKPOINT_SYSTEM.md"

    if not checkpoint_file.exists():
        return todos

    try:
        with open(checkpoint_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Detectar tasks pendentes (checkboxes não marcados)
        # Pattern: - [ ] Task description
        pattern = r'-\s*\[\s*\]\s*(.+)'

        for match in re.finditer(pattern, content):
            task_text = match.group(1).strip()

            # Detectar fase
            phase = _detect_phase_from_context(content, match.start())

            todos.append({
                'type': 'TASK',
                'file': 'docs/CHECKPOINT_SYSTEM.md',
                'line': content[:match.start()].count('\n') + 1,
                'text': task_text,
                'priority': _estimate_priority_from_phase(phase),
                'phase': phase,
                'source': 'checkpoint'
            })
    except Exception as e:
        pass

    return todos


def extract_todos_from_commits(bridge: GitMemoryBridge, last_n: int = 10) -> List[Dict]:
    """Extrai TODOs adicionados em commits recentes"""
    summary = bridge.generate_session_summary(last_n=last_n)

    todos = []
    for todo in summary.get('todos_accumulated', []):
        todos.append({
            'type': todo['type'],
            'file': 'unknown',  # Diff doesn't give exact file easily
            'line': 0,
            'text': todo['text'],
            'priority': _estimate_priority(todo['type'], todo['text']),
            'commit': todo.get('commit', 'unknown'),
            'source': 'commit'
        })

    return todos


def _estimate_priority(todo_type: str, text: str) -> str:
    """Estima prioridade baseado em tipo e texto"""
    text_lower = text.lower()

    # CRITICAL keywords
    if any(kw in text_lower for kw in ['critical', 'urgent', 'asap', 'broken', 'bug']):
        return 'CRITICAL'

    # HIGH keywords
    if todo_type in ['FIXME', 'XXX', 'HACK']:
        return 'HIGH'

    if any(kw in text_lower for kw in ['important', 'must', 'required', 'blocker']):
        return 'HIGH'

    # MEDIUM (default for TODO)
    if todo_type == 'TODO':
        return 'MEDIUM'

    # LOW (NOTE, nice-to-have)
    return 'LOW'


def _estimate_priority_from_phase(phase: str) -> str:
    """Estima prioridade baseado na fase"""
    if not phase:
        return 'MEDIUM'

    # Fases iniciais = maior prioridade
    if 'FASE 1' in phase or 'FASE 2' in phase:
        return 'HIGH'
    elif 'FASE 3' in phase or 'FASE 4' in phase:
        return 'MEDIUM'
    else:
        return 'LOW'


def _detect_phase_from_context(content: str, position: int) -> str:
    """Detecta fase baseado no contexto ao redor da task"""
    # Buscar heading mais próximo acima
    before = content[:position]

    # Procurar por "FASE X" nos últimos 500 caracteres
    context = before[-500:]

    phases = ['FASE 0', 'FASE 1', 'FASE 2', 'FASE 2B', 'FASE 3', 'FASE 4']
    for phase in reversed(phases):  # Mais específico primeiro
        if phase in context:
            return phase

    return 'Unknown'


def merge_and_deduplicate(todos: List[Dict]) -> List[Dict]:
    """Merge TODOs de diferentes fontes e remove duplicatas"""
    # Deduplicate por texto similar
    seen = set()
    unique_todos = []

    for todo in todos:
        # Normalizar texto para comparação
        normalized = todo['text'].lower().strip()[:50]  # Primeiros 50 chars

        if normalized not in seen:
            seen.add(normalized)
            unique_todos.append(todo)

    return unique_todos


def prioritize_tasks(todos: List[Dict]) -> List[Dict]:
    """Ordena tasks por prioridade"""
    priority_order = {'CRITICAL': 0, 'HIGH': 1, 'MEDIUM': 2, 'LOW': 3}

    return sorted(todos, key=lambda t: priority_order.get(t['priority'], 4))


def main():
    parser = argparse.ArgumentParser(description="Extract tasks from Git and code")
    parser.add_argument("--priority", choices=['CRITICAL', 'HIGH', 'MEDIUM', 'LOW'],
                       help="Filter by priority")
    parser.add_argument("--phase", type=str, help="Filter by phase (e.g., FASE2)")
    parser.add_argument("--source", choices=['code', 'checkpoint', 'commit'],
                       help="Filter by source")
    parser.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    # Initialize
    repo_path = Path(__file__).parent.parent
    memory_dir = repo_path / "memory"

    bridge = GitMemoryBridge(
        repo_path=str(repo_path),
        memory_dir=str(memory_dir)
    )

    # Extract from all sources
    todos = []

    if not args.source or args.source == 'code':
        todos.extend(extract_todos_from_code(repo_path))

    if not args.source or args.source == 'checkpoint':
        todos.extend(extract_todos_from_checkpoint(repo_path))

    if not args.source or args.source == 'commit':
        todos.extend(extract_todos_from_commits(bridge, last_n=10))

    # Merge and prioritize
    todos = merge_and_deduplicate(todos)
    todos = prioritize_tasks(todos)

    # Filter
    if args.priority:
        todos = [t for t in todos if t['priority'] == args.priority]

    if args.phase:
        todos = [t for t in todos if args.phase.upper() in t.get('phase', '').upper()]

    # Save to memory/tasks/
    tasks_file = memory_dir / "tasks" / "pending.json"
    tasks_file.parent.mkdir(parents=True, exist_ok=True)

    with open(tasks_file, 'w', encoding='utf-8') as f:
        json.dump(todos, f, indent=2, ensure_ascii=False)

    # Output
    if args.json:
        print(json.dumps(todos, indent=2))
    else:
        _print_tasks(todos)

    print(f"\n💾 Tasks saved to: {tasks_file}")


def _print_tasks(todos: List[Dict]):
    """Formata tasks para output humano"""
    print("=" * 80)
    print("📝 TASKS EXTRACTED FROM GIT")
    print("=" * 80)
    print()

    if not todos:
        print("✅ No tasks found!")
        return

    # Group by priority
    by_priority = {}
    for todo in todos:
        priority = todo['priority']
        by_priority.setdefault(priority, []).append(todo)

    for priority in ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW']:
        tasks = by_priority.get(priority, [])
        if not tasks:
            continue

        print(f"\n🔥 {priority} ({len(tasks)} tasks)")
        print("-" * 80)

        for i, task in enumerate(tasks[:10], 1):  # Max 10 per priority
            source_icon = {'code': '💻', 'checkpoint': '📋', 'commit': '📸'}.get(task['source'], '❓')
            print(f"{i}. [{task['type']}] {task['text'][:60]}...")
            print(f"   {source_icon} {task['file']}:{task.get('line', '?')}")
            if task.get('phase'):
                print(f"   📍 {task['phase']}")
            print()

        if len(tasks) > 10:
            print(f"   ... and {len(tasks) - 10} more {priority} tasks")
            print()

    print("=" * 80)
    print(f"📊 Total: {len(todos)} tasks")
    print("=" * 80)


if __name__ == "__main__":
    main()
