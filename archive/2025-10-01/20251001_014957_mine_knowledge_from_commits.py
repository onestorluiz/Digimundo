#!/usr/bin/env python3
"""
Mine Knowledge from Commits - Extrai learnings de histórico Git

Analisa commits que:
1. Fixam bugs → Extrai lição aprendida
2. Refatoram código → Documenta pattern
3. Melhoram performance → Captura otimização

Gera documentação automática em memory/knowledge/

Usage:
    python scripts/mine_knowledge_from_commits.py
    python scripts/mine_knowledge_from_commits.py --since FASE1_START
    python scripts/mine_knowledge_from_commits.py --type bugfix
"""

import sys
import json
import re
import argparse
from pathlib import Path
from datetime import datetime
from typing import List, Dict
import subprocess

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.git_memory_bridge import GitMemoryBridge


def identify_commit_type(message: str) -> str:
    """Identifica tipo de commit pela mensagem"""
    message_lower = message.lower()

    if any(kw in message_lower for kw in ['fix:', 'fix(', 'bugfix', 'hotfix']):
        return 'bugfix'
    elif any(kw in message_lower for kw in ['refactor:', 'refactor(']):
        return 'refactor'
    elif any(kw in message_lower for kw in ['perf:', 'performance', 'optimize']):
        return 'performance'
    elif any(kw in message_lower for kw in ['feat:', 'feature']):
        return 'feature'
    elif any(kw in message_lower for kw in ['docs:', 'documentation']):
        return 'docs'
    else:
        return 'other'


def mine_bugfix_knowledge(snapshot: Dict, bridge: GitMemoryBridge) -> Dict:
    """Extrai conhecimento de um bugfix"""
    commit_hash = snapshot['commit_hash_short']
    message = snapshot['message']

    # Extrair descrição do bug
    bug_description = _extract_bug_description(message)

    # Identificar arquivos modificados
    files = snapshot.get('modified_files', [])

    # Tentar identificar causa raiz
    root_cause = _identify_root_cause(snapshot, bridge)

    # Extrair solução aplicada
    solution = _extract_solution(message)

    knowledge = {
        'type': 'bugfix',
        'commit': commit_hash,
        'timestamp': snapshot['timestamp'],
        'bug_description': bug_description,
        'files_affected': files,
        'root_cause': root_cause,
        'solution': solution,
        'impact': _estimate_impact(snapshot),
        'category': _categorize_bug(bug_description, files)
    }

    return knowledge


def mine_refactor_knowledge(snapshot: Dict) -> Dict:
    """Extrai conhecimento de refatoração"""
    commit_hash = snapshot['commit_hash_short']
    message = snapshot['message']

    # Extrair pattern da refatoração
    pattern = _extract_refactor_pattern(message)

    # Identificar arquivos refatorados
    files = snapshot.get('modified_files', [])

    knowledge = {
        'type': 'refactor',
        'commit': commit_hash,
        'timestamp': snapshot['timestamp'],
        'pattern': pattern,
        'files_refactored': files,
        'lines_changed': snapshot.get('lines_added', 0) + snapshot.get('lines_removed', 0),
        'motivation': _extract_motivation(message),
        'reusable': _is_reusable_pattern(pattern, files)
    }

    return knowledge


def mine_performance_knowledge(snapshot: Dict) -> Dict:
    """Extrai conhecimento de otimização"""
    commit_hash = snapshot['commit_hash_short']
    message = snapshot['message']

    # Extrair otimização aplicada
    optimization = _extract_optimization(message)

    knowledge = {
        'type': 'performance',
        'commit': commit_hash,
        'timestamp': snapshot['timestamp'],
        'optimization': optimization,
        'files_optimized': snapshot.get('modified_files', []),
        'improvement': _extract_improvement_metric(message),
        'technique': _identify_technique(optimization)
    }

    return knowledge


def _extract_bug_description(message: str) -> str:
    """Extrai descrição do bug da mensagem"""
    # Primeira linha geralmente é o summary
    lines = message.split('\n')
    summary = lines[0] if lines else message

    # Remover prefixo fix:
    summary = re.sub(r'^fix[:\(]?\s*', '', summary, flags=re.IGNORECASE)

    return summary.strip()


def _identify_root_cause(snapshot: Dict, bridge: GitMemoryBridge) -> str:
    """Tenta identificar causa raiz do bug"""
    # Heurística: analisar arquivos modificados e TODOs
    files = snapshot.get('modified_files', [])

    if not files:
        return 'Unknown'

    # Categorias comuns
    if any('test' in f for f in files):
        return 'Missing test coverage'
    elif any('config' in f for f in files):
        return 'Configuration error'
    elif len(files) == 1:
        return f'Logic error in {files[0]}'
    else:
        return f'Integration issue across {len(files)} files'


def _extract_solution(message: str) -> str:
    """Extrai solução aplicada da mensagem"""
    lines = message.split('\n')

    # Procurar por seções que descrevem a solução
    solution_keywords = ['solution:', 'fix:', 'changed:', 'updated:']

    for i, line in enumerate(lines):
        if any(kw in line.lower() for kw in solution_keywords):
            # Retornar próximas linhas como solução
            solution_lines = lines[i:min(i+3, len(lines))]
            return ' '.join(solution_lines).strip()

    # Se não encontrou seção específica, usar corpo do commit
    if len(lines) > 2:
        return ' '.join(lines[1:4]).strip()

    return 'See commit diff'


def _estimate_impact(snapshot: Dict) -> str:
    """Estima impacto do bug/fix"""
    files = len(snapshot.get('modified_files', []))
    lines = snapshot.get('lines_added', 0) + snapshot.get('lines_removed', 0)

    if files >= 10 or lines >= 100:
        return 'HIGH'
    elif files >= 3 or lines >= 20:
        return 'MEDIUM'
    else:
        return 'LOW'


def _categorize_bug(description: str, files: List[str]) -> str:
    """Categoriza o tipo de bug"""
    desc_lower = description.lower()

    categories = {
        'encoding': ['utf-8', 'decode', 'encoding', 'unicode'],
        'integration': ['integration', 'connect', 'api', 'interface'],
        'logic': ['logic', 'calculation', 'algorithm'],
        'typo': ['typo', 'spelling', 'rename'],
        'performance': ['slow', 'timeout', 'performance'],
        'security': ['security', 'auth', 'permission']
    }

    for category, keywords in categories.items():
        if any(kw in desc_lower for kw in keywords):
            return category

    # Default based on files
    if any('test' in f for f in files):
        return 'test'
    elif any('.py' in f for f in files):
        return 'code'
    else:
        return 'other'


def _extract_refactor_pattern(message: str) -> str:
    """Extrai pattern de refatoração"""
    # Primeira linha
    lines = message.split('\n')
    summary = lines[0] if lines else message

    # Remover prefixo refactor:
    summary = re.sub(r'^refactor[:\(]?\s*', '', summary, flags=re.IGNORECASE)

    return summary.strip()


def _extract_motivation(message: str) -> str:
    """Extrai motivação da refatoração"""
    keywords = ['why:', 'reason:', 'motivation:', 'improve:', 'better:']

    for line in message.split('\n'):
        if any(kw in line.lower() for kw in keywords):
            return line.strip()

    return 'See commit message'


def _is_reusable_pattern(pattern: str, files: List[str]) -> bool:
    """Verifica se pattern é reutilizável"""
    # Heurística simples: se afetou múltiplos arquivos, provavelmente é pattern geral
    return len(files) >= 2


def _extract_optimization(message: str) -> str:
    """Extrai otimização aplicada"""
    lines = message.split('\n')
    summary = lines[0] if lines else message

    # Remover prefixo perf:
    summary = re.sub(r'^perf[:\(]?\s*', '', summary, flags=re.IGNORECASE)

    return summary.strip()


def _extract_improvement_metric(message: str) -> str:
    """Extrai métrica de melhoria (ex: "2x faster")"""
    # Procurar por padrões como "2x", "50%", "10ms"
    patterns = [
        r'(\d+)x\s+faster',
        r'(\d+)%\s+improvement',
        r'(\d+)ms\s+→\s+(\d+)ms',
        r'reduced.*by\s+(\d+)%'
    ]

    for pattern in patterns:
        match = re.search(pattern, message, re.IGNORECASE)
        if match:
            return match.group(0)

    return 'Not quantified'


def _identify_technique(optimization: str) -> str:
    """Identifica técnica de otimização"""
    opt_lower = optimization.lower()

    techniques = {
        'caching': ['cache', 'memoize'],
        'indexing': ['index', 'hash'],
        'algorithm': ['algorithm', 'complexity'],
        'io': ['io', 'disk', 'network'],
        'memory': ['memory', 'leak', 'allocation']
    }

    for technique, keywords in techniques.items():
        if any(kw in opt_lower for kw in keywords):
            return technique

    return 'general'


def save_knowledge(knowledge: Dict, memory_dir: Path):
    """Salva conhecimento em memory/knowledge/"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    commit = knowledge['commit']
    knowledge_type = knowledge['type']

    filename = f"{timestamp}_{commit}_{knowledge_type}.md"
    filepath = memory_dir / "knowledge" / filename

    # Gerar markdown
    markdown = _generate_knowledge_markdown(knowledge)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(markdown)

    return filepath


def _generate_knowledge_markdown(knowledge: Dict) -> str:
    """Gera markdown do conhecimento"""
    if knowledge['type'] == 'bugfix':
        return f"""# 🐛 Knowledge: {knowledge['bug_description'][:60]}

**Commit:** `{knowledge['commit']}`
**Timestamp:** {knowledge['timestamp']}
**Category:** {knowledge['category']}
**Impact:** {knowledge['impact']}

## Bug Description
{knowledge['bug_description']}

## Root Cause
{knowledge['root_cause']}

## Solution Applied
{knowledge['solution']}

## Files Affected
{chr(10).join(f"- {f}" for f in knowledge['files_affected'][:10])}

## Reusability
This knowledge can be applied to similar {knowledge['category']} issues.

---
Auto-generated by Git-Memory Knowledge Mining
"""

    elif knowledge['type'] == 'refactor':
        return f"""# 🔄 Knowledge: {knowledge['pattern'][:60]}

**Commit:** `{knowledge['commit']}`
**Timestamp:** {knowledge['timestamp']}
**Reusable:** {knowledge['reusable']}

## Pattern
{knowledge['pattern']}

## Motivation
{knowledge['motivation']}

## Files Refactored
{chr(10).join(f"- {f}" for f in knowledge['files_refactored'][:10])}

## Metrics
- Lines changed: {knowledge['lines_changed']}
- Reusable pattern: {knowledge['reusable']}

---
Auto-generated by Git-Memory Knowledge Mining
"""

    elif knowledge['type'] == 'performance':
        return f"""# ⚡ Knowledge: {knowledge['optimization'][:60]}

**Commit:** `{knowledge['commit']}`
**Timestamp:** {knowledge['timestamp']}
**Technique:** {knowledge['technique']}

## Optimization
{knowledge['optimization']}

## Improvement
{knowledge['improvement']}

## Technique
{knowledge['technique'].upper()}

## Files Optimized
{chr(10).join(f"- {f}" for f in knowledge['files_optimized'][:10])}

---
Auto-generated by Git-Memory Knowledge Mining
"""

    return "Unknown knowledge type"


def main():
    parser = argparse.ArgumentParser(description="Mine knowledge from Git commits")
    parser.add_argument("--since", type=str, help="Since commit/tag")
    parser.add_argument("--last", type=int, default=20, help="Last N commits (default: 20)")
    parser.add_argument("--type", choices=['bugfix', 'refactor', 'performance', 'all'],
                       default='all', help="Type of knowledge to mine")

    args = parser.parse_args()

    # Initialize
    repo_path = Path(__file__).parent.parent
    memory_dir = repo_path / "memory"

    bridge = GitMemoryBridge(
        repo_path=str(repo_path),
        memory_dir=str(memory_dir)
    )

    # Get commits
    if args.since:
        summary = bridge.generate_session_summary(since_commit=args.since)
    else:
        summary = bridge.generate_session_summary(last_n=args.last)

    # Load snapshots
    commits_dir = memory_dir / "commits"
    snapshots = []

    for commit_line in summary['commits']:
        short_hash = commit_line.split()[0]
        snapshot_file = commits_dir / f"{short_hash}_snapshot.json"

        if snapshot_file.exists():
            with open(snapshot_file, 'r') as f:
                snapshots.append(json.load(f))

    print(f"🔍 Analyzing {len(snapshots)} commits...")
    print()

    # Mine knowledge
    knowledge_items = []

    for snapshot in snapshots:
        commit_type = identify_commit_type(snapshot['message'])

        # Filter by type
        if args.type != 'all' and commit_type != args.type:
            continue

        if commit_type == 'bugfix':
            knowledge = mine_bugfix_knowledge(snapshot, bridge)
            knowledge_items.append(knowledge)
            print(f"🐛 Bugfix: {snapshot['commit_hash_short']} - {knowledge['bug_description'][:50]}...")

        elif commit_type == 'refactor':
            knowledge = mine_refactor_knowledge(snapshot)
            knowledge_items.append(knowledge)
            print(f"🔄 Refactor: {snapshot['commit_hash_short']} - {knowledge['pattern'][:50]}...")

        elif commit_type == 'performance':
            knowledge = mine_performance_knowledge(snapshot)
            knowledge_items.append(knowledge)
            print(f"⚡ Performance: {snapshot['commit_hash_short']} - {knowledge['optimization'][:50]}...")

    print()
    print(f"📚 Mined {len(knowledge_items)} knowledge items")
    print()

    # Save knowledge
    if knowledge_items:
        for knowledge in knowledge_items:
            filepath = save_knowledge(knowledge, memory_dir)
            print(f"💾 Saved: {filepath.name}")

        print()
        print(f"✅ Knowledge saved to: memory/knowledge/")
    else:
        print("⚠️  No knowledge items found (no bugfix/refactor/perf commits)")


if __name__ == "__main__":
    main()
