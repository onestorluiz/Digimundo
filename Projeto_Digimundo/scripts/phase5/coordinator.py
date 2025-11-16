#!/usr/bin/env python3
"""
🎯 MULTI-AGENT COORDINATOR - Orchestration System

Este é o cérebro do sistema multi-agentes. Ele:
- Cria e gerencia task queue
- Distribui tarefas para agentes
- Monitora progresso
- Consolida resultados
- Resolve conflitos

Usage:
    python3 coordinator.py init --tasks 20
    python3 coordinator.py status
    python3 coordinator.py consolidate
    python3 coordinator.py merge-all
"""

import json
import argparse
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional
import subprocess
import time

# Cores
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

class TaskType:
    VALIDATION = "validation"
    DOC_GENERATION = "doc_generation"
    SYSTEM_BUILDING = "system_building"
    TESTING = "testing"
    OPTIMIZATION = "optimization"
    ANALYSIS = "analysis"

class Priority:
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class TaskStatus:
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"

class MultiAgentCoordinator:
    def __init__(self):
        self.root = Path("/Users/clubproducoes/Digimundo/Projeto_Digimundo")
        self.ma_dir = self.root / "docs/fase_5/multi_agent"
        self.ma_dir.mkdir(parents=True, exist_ok=True)

        self.queue_file = self.ma_dir / "task_queue.json"
        self.state_file = self.ma_dir / "coordinator_state.json"
        self.agents_dir = self.ma_dir / "agents"
        self.workspaces_dir = self.ma_dir / "workspaces"
        self.results_dir = self.ma_dir / "results"

        # Criar diretórios
        self.agents_dir.mkdir(exist_ok=True)
        self.workspaces_dir.mkdir(exist_ok=True)
        self.results_dir.mkdir(exist_ok=True)

    def init(self, num_tasks: int = 20):
        """Inicializar sistema com N tarefas"""
        print(f"{BLUE}{'='*60}{RESET}")
        print(f"{BLUE}🎯 INICIALIZANDO MULTI-AGENT SYSTEM{RESET}")
        print(f"{BLUE}{'='*60}{RESET}\n")

        tasks = self._generate_tasks(num_tasks)

        queue = {
            "created_at": datetime.now().isoformat(),
            "total_tasks": len(tasks),
            "completed": 0,
            "tasks": tasks
        }

        with open(self.queue_file, 'w') as f:
            json.dump(queue, indent=2, fp=f)

        state = {
            "status": "initialized",
            "agents": {},
            "statistics": {
                "tasks_completed": 0,
                "tasks_failed": 0,
                "total_time_saved": 0,
                "average_task_duration": 0
            }
        }

        with open(self.state_file, 'w') as f:
            json.dump(state, indent=2, fp=f)

        print(f"{GREEN}✅ Sistema inicializado!{RESET}")
        print(f"📝 {len(tasks)} tarefas criadas")
        print(f"📊 Task queue: {self.queue_file}")
        print(f"📊 State file: {self.state_file}\n")

        print(f"{BLUE}Próximo passo:{RESET}")
        print(f"1. Inicie o dashboard:")
        print(f"   python3 scripts/phase5/multi_agent_dashboard.py")
        print(f"2. Inicie os agentes:")
        print(f"   python3 scripts/phase5/multi_agent_runner.py --agents 3\n")

    def _generate_tasks(self, num_tasks: int) -> List[Dict]:
        """Gerar lista de tarefas inteligente"""

        # Templates de tasks por tipo
        task_templates = [
            # Validation tasks (HIGH priority)
            {
                "type": TaskType.VALIDATION,
                "description": "Validar métricas de duplicação",
                "priority": Priority.HIGH,
                "estimated_duration": 5,
                "command": "python3 scripts/phase5/validate_documentation.py"
            },
            {
                "type": TaskType.VALIDATION,
                "description": "Executar drift prediction",
                "priority": Priority.HIGH,
                "estimated_duration": 3,
                "command": "python3 scripts/phase5/drift_predictor.py"
            },
            {
                "type": TaskType.VALIDATION,
                "description": "Health check completo",
                "priority": Priority.HIGH,
                "estimated_duration": 2,
                "command": "python3 scripts/phase5/autonomous_agent.py --step PASSO_B_AUTO_UPDATE"
            },

            # Doc generation tasks (MEDIUM priority)
            {
                "type": TaskType.DOC_GENERATION,
                "description": "Gerar documentação de API",
                "priority": Priority.MEDIUM,
                "estimated_duration": 8,
                "command": "python3 scripts/phase5/auto_doc_generator.py"
            },
            {
                "type": TaskType.DOC_GENERATION,
                "description": "Atualizar README files",
                "priority": Priority.MEDIUM,
                "estimated_duration": 5,
                "command": None  # Manual task
            },
            {
                "type": TaskType.DOC_GENERATION,
                "description": "Gerar API changelog",
                "priority": Priority.MEDIUM,
                "estimated_duration": 6,
                "command": None
            },

            # System building tasks (MEDIUM priority)
            {
                "type": TaskType.SYSTEM_BUILDING,
                "description": "Criar semantic_versioning.py",
                "priority": Priority.MEDIUM,
                "estimated_duration": 15,
                "command": None
            },
            {
                "type": TaskType.SYSTEM_BUILDING,
                "description": "Criar dependency_health.py",
                "priority": Priority.MEDIUM,
                "estimated_duration": 12,
                "command": None
            },
            {
                "type": TaskType.SYSTEM_BUILDING,
                "description": "Criar api_contract_validator.py",
                "priority": Priority.MEDIUM,
                "estimated_duration": 18,
                "command": None
            },

            # Testing tasks (HIGH priority)
            {
                "type": TaskType.TESTING,
                "description": "Criar tests para validation scripts",
                "priority": Priority.HIGH,
                "estimated_duration": 10,
                "command": None
            },
            {
                "type": TaskType.TESTING,
                "description": "Executar pytest com coverage",
                "priority": Priority.HIGH,
                "estimated_duration": 5,
                "command": "pytest tests/phase5/ --cov=scripts/phase5 --cov-report=json"
            },

            # Optimization tasks (LOW priority)
            {
                "type": TaskType.OPTIMIZATION,
                "description": "Paralelizar validações",
                "priority": Priority.LOW,
                "estimated_duration": 20,
                "command": None
            },
            {
                "type": TaskType.OPTIMIZATION,
                "description": "Implementar cache de validações",
                "priority": Priority.LOW,
                "estimated_duration": 15,
                "command": None
            },

            # Analysis tasks (LOW priority)
            {
                "type": TaskType.ANALYSIS,
                "description": "Análise profunda de drift",
                "priority": Priority.LOW,
                "estimated_duration": 12,
                "command": None
            },
            {
                "type": TaskType.ANALYSIS,
                "description": "Code complexity analysis",
                "priority": Priority.LOW,
                "estimated_duration": 10,
                "command": None
            },
        ]

        # Gerar tasks baseado nos templates
        tasks = []
        for i in range(num_tasks):
            template = task_templates[i % len(task_templates)]
            task = {
                "id": f"task_{i+1:03d}",
                "type": template["type"],
                "description": f"{template['description']} ({i+1})",
                "priority": template["priority"],
                "status": TaskStatus.PENDING,
                "assigned_to": None,
                "progress": 0,
                "created_at": datetime.now().isoformat(),
                "estimated_duration": template["estimated_duration"],
                "command": template.get("command"),
                "dependencies": []
            }
            tasks.append(task)

        # Ordenar por prioridade
        priority_order = {Priority.HIGH: 0, Priority.MEDIUM: 1, Priority.LOW: 2}
        tasks.sort(key=lambda t: (priority_order[t["priority"]], t["estimated_duration"]))

        return tasks

    def status(self):
        """Mostrar status atual do sistema"""
        print(f"\n{BLUE}{'='*60}{RESET}")
        print(f"{BLUE}📊 MULTI-AGENT SYSTEM STATUS{RESET}")
        print(f"{BLUE}{'='*60}{RESET}\n")

        # Load state
        if not self.queue_file.exists():
            print(f"{RED}❌ Sistema não inicializado. Execute: coordinator.py init{RESET}")
            return

        queue = json.load(open(self.queue_file))
        state = json.load(open(self.state_file)) if self.state_file.exists() else {}

        # Stats
        total = queue["total_tasks"]
        completed = len([t for t in queue["tasks"] if t["status"] == TaskStatus.COMPLETED])
        in_progress = len([t for t in queue["tasks"] if t["status"] == TaskStatus.IN_PROGRESS])
        pending = len([t for t in queue["tasks"] if t["status"] == TaskStatus.PENDING])
        failed = len([t for t in queue["tasks"] if t["status"] == TaskStatus.FAILED])

        progress_pct = (completed / total * 100) if total > 0 else 0

        print(f"Total Tasks: {total}")
        print(f"Completed:   {completed} ({progress_pct:.1f}%)")
        print(f"In Progress: {in_progress}")
        print(f"Pending:     {pending}")
        print(f"Failed:      {failed}\n")

        # Agents
        agents = state.get("agents", {})
        if agents:
            print(f"{BLUE}AGENTS:{RESET}\n")
            for agent_id, agent_data in agents.items():
                status_emoji = "🟢" if agent_data.get("status") == "working" else "⚪"
                print(f"{status_emoji} {agent_id} ({agent_data.get('type', 'Unknown')})")
                if agent_data.get("current_task"):
                    print(f"   Task: {agent_data['current_task']}")
                    print(f"   Progress: {agent_data.get('progress', 0)}%")
                print()

        # Next tasks (top 5 pending)
        pending_tasks = [t for t in queue["tasks"] if t["status"] == TaskStatus.PENDING]
        if pending_tasks:
            print(f"{BLUE}NEXT TASKS (top 5):{RESET}\n")
            for task in pending_tasks[:5]:
                priority_emoji = "🔴" if task["priority"] == Priority.HIGH else "🟡" if task["priority"] == Priority.MEDIUM else "🔵"
                print(f"{priority_emoji} [{task['id']}] {task['description']}")
                print(f"   Type: {task['type']} | Duration: ~{task['estimated_duration']} min")
            print()

    def consolidate(self):
        """Consolidar resultados de todos os agentes"""
        print(f"\n{BLUE}{'='*60}{RESET}")
        print(f"{BLUE}🔄 CONSOLIDANDO RESULTADOS{RESET}")
        print(f"{BLUE}{'='*60}{RESET}\n")

        # Load results from all agents
        results = []
        for agent_dir in self.agents_dir.iterdir():
            if not agent_dir.is_dir():
                continue

            output_file = agent_dir / "output.json"
            if output_file.exists():
                result = json.load(open(output_file))
                results.append(result)
                print(f"✅ Loaded result from {agent_dir.name}")

        # Consolidate
        consolidated = {
            "timestamp": datetime.now().isoformat(),
            "total_agents": len(results),
            "results": results,
            "summary": {
                "tasks_completed": sum(r.get("tasks_completed", 0) for r in results),
                "total_duration": sum(r.get("duration_seconds", 0) for r in results),
                "success_rate": 100.0  # Calculate from results
            }
        }

        # Save
        consolidated_file = self.results_dir / "consolidated.json"
        with open(consolidated_file, 'w') as f:
            json.dump(consolidated, indent=2, fp=f)

        print(f"\n{GREEN}✅ Consolidação completa!{RESET}")
        print(f"📊 Resultado salvo em: {consolidated_file}\n")

        # Generate report
        self._generate_report(consolidated)

    def _generate_report(self, consolidated: Dict):
        """Gerar relatório markdown"""
        report_file = self.results_dir.parent / "MULTI_AGENT_REPORT.md"

        report = f"""# 🤖 Multi-Agent Execution Report

**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Summary

- **Total Agents**: {consolidated['total_agents']}
- **Tasks Completed**: {consolidated['summary']['tasks_completed']}
- **Total Duration**: {consolidated['summary']['total_duration']:.1f} seconds
- **Success Rate**: {consolidated['summary']['success_rate']:.1f}%

## Results

"""
        for i, result in enumerate(consolidated['results'], 1):
            report += f"### Agent {i}\n\n"
            report += f"- Tasks: {result.get('tasks_completed', 0)}\n"
            report += f"- Duration: {result.get('duration_seconds', 0):.1f}s\n"
            report += f"\n"

        with open(report_file, 'w') as f:
            f.write(report)

        print(f"📝 Relatório gerado: {report_file}\n")

    def merge_all(self):
        """Merge all agent branches"""
        print(f"\n{BLUE}{'='*60}{RESET}")
        print(f"{BLUE}🔀 MERGING AGENT BRANCHES{RESET}")
        print(f"{BLUE}{'='*60}{RESET}\n")

        # Find all agent branches
        result = subprocess.run(
            ["git", "branch", "--list", "multi-agent/*"],
            cwd=self.root,
            capture_output=True,
            text=True
        )

        branches = [b.strip().replace("* ", "") for b in result.stdout.split('\n') if b.strip()]

        if not branches:
            print(f"{YELLOW}⚠️  Nenhum branch de agente encontrado{RESET}")
            return

        print(f"Encontrados {len(branches)} branches:\n")
        for branch in branches:
            print(f"  - {branch}")

        print(f"\n{YELLOW}Mesclando...{RESET}\n")

        # Checkout main
        subprocess.run(["git", "checkout", "main"], cwd=self.root)

        # Merge each branch
        for branch in branches:
            print(f"Merging {branch}...")
            result = subprocess.run(
                ["git", "merge", branch, "--no-ff", "-m", f"Merge {branch}"],
                cwd=self.root,
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                print(f"{GREEN}  ✅ Merged{RESET}")
            else:
                print(f"{RED}  ❌ Conflict detected{RESET}")
                print(f"  {result.stderr}")

        print(f"\n{GREEN}✅ Merge completo!{RESET}\n")

def main():
    parser = argparse.ArgumentParser(description="Multi-Agent Coordinator")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # Init command
    init_parser = subparsers.add_parser("init", help="Initialize system")
    init_parser.add_argument("--tasks", type=int, default=20, help="Number of tasks to create")

    # Status command
    subparsers.add_parser("status", help="Show system status")

    # Consolidate command
    subparsers.add_parser("consolidate", help="Consolidate results")

    # Merge command
    subparsers.add_parser("merge-all", help="Merge all agent branches")

    args = parser.parse_args()

    coordinator = MultiAgentCoordinator()

    if args.command == "init":
        coordinator.init(args.tasks)
    elif args.command == "status":
        coordinator.status()
    elif args.command == "consolidate":
        coordinator.consolidate()
    elif args.command == "merge-all":
        coordinator.merge_all()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
