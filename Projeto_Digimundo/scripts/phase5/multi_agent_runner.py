#!/usr/bin/env python3
"""
🤖 MULTI-AGENT RUNNER - Parallel Execution System

Executa múltiplos agentes em paralelo usando multiprocessing.

Usage:
    python3 multi_agent_runner.py --agents 3
    python3 multi_agent_runner.py --agents 5 --types Validator,DocGenerator,SystemBuilder
"""

import json
import argparse
import multiprocessing
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List
import subprocess

# Cores
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
CYAN = '\033[96m'
RESET = '\033[0m'

class AgentType:
    VALIDATOR = "Validator"
    DOC_GENERATOR = "DocGenerator"
    SYSTEM_BUILDER = "SystemBuilder"
    TESTER = "Tester"
    OPTIMIZER = "Optimizer"
    ANALYZER = "Analyzer"

class Agent:
    def __init__(self, agent_id: str, agent_type: str, root_dir: Path):
        self.agent_id = agent_id
        self.agent_type = agent_type
        self.root = root_dir
        self.ma_dir = root_dir / "docs/fase_5/multi_agent"
        self.agent_dir = self.ma_dir / "agents" / agent_id
        self.workspace = self.ma_dir / "workspaces" / agent_id

        # Create directories
        self.agent_dir.mkdir(parents=True, exist_ok=True)
        self.workspace.mkdir(parents=True, exist_ok=True)

        self.state_file = self.agent_dir / "state.json"
        self.input_file = self.agent_dir / "input.json"
        self.output_file = self.agent_dir / "output.json"
        self.logs_file = self.agent_dir / "logs.txt"

    def initialize(self):
        """Initialize agent state"""
        state = {
            "agent_id": self.agent_id,
            "type": self.agent_type,
            "status": "idle",
            "current_task": None,
            "progress": 0,
            "last_update": datetime.now().isoformat(),
            "workspace": str(self.workspace),
            "logs": [],
            "errors": [],
            "tasks_completed": 0
        }

        with open(self.state_file, 'w') as f:
            json.dump(state, indent=2, fp=f)

    def get_next_task(self) -> Dict:
        """Get next task from queue"""
        queue_file = self.ma_dir / "task_queue.json"

        if not queue_file.exists():
            return None

        # Read queue with file locking simulation (simplified)
        queue = json.load(open(queue_file))

        # Find first pending task matching agent type
        for task in queue["tasks"]:
            if task["status"] == "pending":
                # Check if task type matches agent type
                if self._can_handle_task(task):
                    # Mark as in progress
                    task["status"] = "in_progress"
                    task["assigned_to"] = self.agent_id
                    task["started_at"] = datetime.now().isoformat()

                    # Save queue
                    with open(queue_file, 'w') as f:
                        json.dump(queue, indent=2, fp=f)

                    return task

        return None

    def _can_handle_task(self, task: Dict) -> bool:
        """Check if agent can handle this task type"""
        type_mapping = {
            AgentType.VALIDATOR: ["validation"],
            AgentType.DOC_GENERATOR: ["doc_generation"],
            AgentType.SYSTEM_BUILDER: ["system_building"],
            AgentType.TESTER: ["testing"],
            AgentType.OPTIMIZER: ["optimization"],
            AgentType.ANALYZER: ["analysis"]
        }

        allowed_types = type_mapping.get(self.agent_type, [])
        return task["type"] in allowed_types

    def execute_task(self, task: Dict):
        """Execute a task"""
        self.log(f"Starting task: {task['description']}")
        self.update_state(status="working", current_task=task["id"], progress=0)

        try:
            # Execute command if exists
            if task.get("command"):
                self.log(f"Executing: {task['command']}")
                self.update_progress(25)

                result = subprocess.run(
                    task["command"],
                    shell=True,
                    cwd=self.root,
                    capture_output=True,
                    text=True,
                    timeout=task["estimated_duration"] * 60
                )

                self.update_progress(75)

                if result.returncode == 0:
                    self.log(f"Command succeeded")
                    self.update_progress(100)
                    self.complete_task(task, success=True, output=result.stdout)
                else:
                    self.log(f"Command failed: {result.stderr}", error=True)
                    self.complete_task(task, success=False, error=result.stderr)

            else:
                # Simulate work for tasks without commands
                self.log("Simulating work (no command provided)...")
                steps = 5
                for i in range(steps):
                    time.sleep(task["estimated_duration"] * 60 / steps / 10)  # Faster sim
                    progress = int((i + 1) / steps * 100)
                    self.update_progress(progress)
                    self.log(f"Progress: {progress}%")

                self.complete_task(task, success=True, output="Simulated completion")

        except subprocess.TimeoutExpired:
            self.log(f"Task timeout", error=True)
            self.complete_task(task, success=False, error="Timeout")
        except Exception as e:
            self.log(f"Error: {str(e)}", error=True)
            self.complete_task(task, success=False, error=str(e))

    def complete_task(self, task: Dict, success: bool, output: str = None, error: str = None):
        """Mark task as complete"""
        # Update queue
        queue_file = self.ma_dir / "task_queue.json"
        queue = json.load(open(queue_file))

        for t in queue["tasks"]:
            if t["id"] == task["id"]:
                t["status"] = "completed" if success else "failed"
                t["completed_at"] = datetime.now().isoformat()
                t["output"] = output
                t["error"] = error
                break

        queue["completed"] = len([t for t in queue["tasks"] if t["status"] == "completed"])

        with open(queue_file, 'w') as f:
            json.dump(queue, indent=2, fp=f)

        # Update agent state
        state = self._load_state()
        state["tasks_completed"] += 1
        state["current_task"] = None
        state["status"] = "idle"
        self._save_state(state)

        self.log(f"Task completed: {'SUCCESS' if success else 'FAILED'}")

    def run(self):
        """Main agent loop"""
        print(f"{CYAN}[{self.agent_id}] Starting {self.agent_type} agent...{RESET}")
        self.initialize()

        while True:
            # Get next task
            task = self.get_next_task()

            if task is None:
                self.log("No more tasks available, exiting...")
                self.update_state(status="finished")
                break

            # Execute task
            self.execute_task(task)

            # Small delay between tasks
            time.sleep(1)

        print(f"{GREEN}[{self.agent_id}] Agent finished!{RESET}")

    def log(self, message: str, error: bool = False):
        """Log message"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        level = "ERROR" if error else "INFO"
        log_line = f"[{timestamp}] [{level}] {message}"

        print(f"{RED if error else CYAN}[{self.agent_id}] {message}{RESET}")

        # Append to logs file
        with open(self.logs_file, 'a') as f:
            f.write(log_line + "\n")

        # Update state logs
        state = self._load_state()
        state["logs"].append(log_line)
        if error:
            state["errors"].append(log_line)
        self._save_state(state)

    def update_state(self, **kwargs):
        """Update agent state"""
        state = self._load_state()
        state.update(kwargs)
        state["last_update"] = datetime.now().isoformat()
        self._save_state(state)

    def update_progress(self, progress: int):
        """Update progress"""
        state = self._load_state()
        state["progress"] = progress
        state["last_update"] = datetime.now().isoformat()
        self._save_state(state)

    def _load_state(self) -> Dict:
        """Load state from file"""
        if self.state_file.exists():
            return json.load(open(self.state_file))
        return {}

    def _save_state(self, state: Dict):
        """Save state to file"""
        with open(self.state_file, 'w') as f:
            json.dump(state, indent=2, fp=f)

def run_agent(agent_id: str, agent_type: str, root_dir: str):
    """Function to run in separate process"""
    agent = Agent(agent_id, agent_type, Path(root_dir))
    agent.run()

class MultiAgentRunner:
    def __init__(self, num_agents: int, agent_types: List[str] = None):
        self.num_agents = num_agents
        self.agent_types = agent_types or [
            AgentType.VALIDATOR,
            AgentType.DOC_GENERATOR,
            AgentType.SYSTEM_BUILDER,
            AgentType.TESTER,
            AgentType.OPTIMIZER,
            AgentType.ANALYZER
        ]
        self.root = Path("/Users/clubproducoes/Digimundo/Projeto_Digimundo")

    def run(self):
        """Run multiple agents in parallel"""
        print(f"{BLUE}{'='*60}{RESET}")
        print(f"{BLUE}🚀 STARTING MULTI-AGENT EXECUTION{RESET}")
        print(f"{BLUE}{'='*60}{RESET}\n")

        print(f"Agents: {self.num_agents}")
        print(f"Types: {', '.join(self.agent_types)}\n")

        # Create processes
        processes = []
        for i in range(self.num_agents):
            agent_id = f"agent_{i+1}"
            agent_type = self.agent_types[i % len(self.agent_types)]

            process = multiprocessing.Process(
                target=run_agent,
                args=(agent_id, agent_type, str(self.root))
            )
            processes.append((agent_id, process))

        # Start all processes
        print(f"{YELLOW}Starting agents...{RESET}\n")
        for agent_id, process in processes:
            process.start()
            print(f"{GREEN}✅ Started {agent_id}{RESET}")

        # Wait for all to complete
        print(f"\n{YELLOW}Waiting for agents to complete...{RESET}\n")
        for agent_id, process in processes:
            process.join()
            print(f"{GREEN}✅ {agent_id} finished{RESET}")

        print(f"\n{BLUE}{'='*60}{RESET}")
        print(f"{GREEN}✅ ALL AGENTS COMPLETED!{RESET}")
        print(f"{BLUE}{'='*60}{RESET}\n")

        print(f"View results:")
        print(f"  python3 scripts/phase5/coordinator.py status")
        print(f"  python3 scripts/phase5/coordinator.py consolidate\n")

def main():
    parser = argparse.ArgumentParser(description="Multi-Agent Runner")
    parser.add_argument("--agents", type=int, default=3, help="Number of agents to run")
    parser.add_argument("--types", type=str, help="Comma-separated agent types")

    args = parser.parse_args()

    agent_types = None
    if args.types:
        agent_types = [t.strip() for t in args.types.split(',')]

    runner = MultiAgentRunner(args.agents, agent_types)
    runner.run()

if __name__ == "__main__":
    main()
