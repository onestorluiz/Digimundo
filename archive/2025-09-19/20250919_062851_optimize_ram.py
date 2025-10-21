#!/usr/bin/env python3
"""
🧹 RAM Optimizer for Digimon Ecosystem
Intelligently frees RAM by analyzing and closing processes
"""

import psutil
import subprocess
import os
import sys
import time
from src.core.unified_memory_system import get_unified_memory, MemoryType
# Auto-unified: Este arquivo foi automaticamente integrado ao sistema unificado


class RAMOptimizer:
    def __init__(self):
        self.total_ram_gb = psutil.virtual_memory().total / (1024**3)
        self.scripturemon_needs_gb = 42
        self.producermon_needs_gb = 8

    def get_current_status(self):
        """Get current RAM usage statistics"""
        mem = psutil.virtual_memory()
        used_gb = (mem.total - mem.available) / (1024**3)
        available_gb = mem.available / (1024**3)
        percent = mem.percent

        return {
            'total_gb': self.total_ram_gb,
            'used_gb': used_gb,
            'available_gb': available_gb,
            'percent': percent,
            'can_run_scripturemon': available_gb >= self.scripturemon_needs_gb,
            'can_run_producermon': available_gb >= self.producermon_needs_gb
        }

    def get_heavy_processes(self, min_mb=100):
        """Get list of processes using more than min_mb RAM"""
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'memory_info']):
            try:
                if proc.info['memory_info'] is None:
                    continue
                mem_mb = proc.info['memory_info'].rss / (1024**2)
                if mem_mb > min_mb:
                    processes.append({
                        'pid': proc.info['pid'],
                        'name': proc.info['name'],
                        'ram_mb': mem_mb,
                        'ram_gb': mem_mb / 1024
                    })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        return sorted(processes, key=lambda x: x['ram_mb'], reverse=True)

    def print_status(self):
        """Print current RAM status with colors"""
        status = self.get_current_status()

        # Colors
        RED = '\033[91m'
        GREEN = '\033[92m'
        YELLOW = '\033[93m'
        BLUE = '\033[94m'
        BOLD = '\033[1m'
        END = '\033[0m'

        print(f"\n{BLUE}{BOLD}📊 RAM Status Report{END}")
        print("=" * 60)

        # Basic stats
        print(f"Total RAM:     {status['total_gb']:.1f} GB")
        print(f"Used:          {status['used_gb']:.1f} GB ({status['percent']:.1f}%)")

        # Available with color coding
        color = GREEN if status['available_gb'] > 45 else YELLOW if status['available_gb'] > 25 else RED
        print(f"Available:     {color}{status['available_gb']:.1f} GB{END}")

        # Capabilities
        print(f"\n{BOLD}Capabilities:{END}")
        if status['can_run_scripturemon']:
            print(f"  {GREEN}✅ Can run ScriptureMon (needs 42GB){END}")
        else:
            print(f"  {RED}❌ Cannot run ScriptureMon (needs 42GB, only {status['available_gb']:.1f}GB available){END}")

        if status['can_run_producermon']:
            print(f"  {GREEN}✅ Can run ProducerMon (needs 8GB){END}")
        else:
            print(f"  {RED}❌ Cannot run ProducerMon (needs 8GB){END}")

    def print_heavy_processes(self, top_n=10):
        """Print top RAM consumers"""
        processes = self.get_heavy_processes()[:top_n]

        if not processes:
            print("No heavy processes found")
            return

        print(f"\n{BOLD}Top {top_n} RAM Consumers:{END}")
        print("-" * 60)

        for i, proc in enumerate(processes, 1):
            # Color code by RAM usage
            if proc['ram_gb'] > 5:
                color = '\033[91m'  # Red for >5GB
            elif proc['ram_gb'] > 2:
                color = '\033[93m'  # Yellow for >2GB
            else:
                color = '\033[0m'   # Normal

            print(f"{i:2}. {color}{proc['name'][:30]:30} "
                  f"PID: {proc['pid']:8} "
                  f"RAM: {proc['ram_gb']:.2f} GB{END}")

    def gentle_cleanup(self):
        """Gentle cleanup - kills test processes and clears cache"""
        print("\n🧹 Starting GENTLE cleanup...")
        freed = 0

        # Kill Python test processes
        print("  • Killing Python test processes...")
        subprocess.run("pkill -f 'python.*test'", shell=True, capture_output=True)
        freed += 0.5

        # Kill Jupyter kernels
        print("  • Killing orphaned Jupyter kernels...")
        subprocess.run("pkill -f jupyter", shell=True, capture_output=True)
        freed += 0.3

        # Kill auto_sync
        print("  • Killing auto_sync processes...")
        subprocess.run("pkill -f auto_sync", shell=True, capture_output=True)
        freed += 0.7

        # Purge cache (requires sudo)
        print("  • Purging system cache...")
        subprocess.run("sudo purge", shell=True, capture_output=True)
        freed += 2.0

        print(f"\n✅ Gentle cleanup complete! Estimated {freed:.1f}GB freed")
        return freed

    def normal_cleanup(self):
        """Normal cleanup - closes heavy apps"""
        print("\n🧹 Starting NORMAL cleanup...")

        # First do gentle
        freed = self.gentle_cleanup()

        apps_to_close = [
            ("Google Chrome", 4.5),
            ("Docker", 3.5),
            ("WhatsApp", 2.0),
            ("Cursor", 2.5),
            ("Visual Studio Code", 2.0)
        ]

        for app, gb in apps_to_close:
            print(f"  • Closing {app}...")
            result = subprocess.run(f"killall '{app}'", shell=True, capture_output=True)
            if result.returncode == 0:
                freed += gb

        print(f"\n✅ Normal cleanup complete! Estimated {freed:.1f}GB freed")
        return freed

    def max_cleanup(self):
        """Maximum cleanup - closes almost everything"""
        print("\n🔴 Starting MAXIMUM cleanup...")
        print("⚠️  This will close almost all applications!")

        response = input("Are you sure? (y/N): ")
        if response.lower() != 'y':
            print("Cancelled.")
            return 0

        freed = 0

        # Kill all major apps
        all_apps = [
            "Google Chrome", "Safari", "Firefox",
            "WhatsApp", "Telegram", "Signal", "Discord", "Slack",
            "Mail", "Photos", "Preview",
            "Cursor", "Visual Studio Code", "Sublime Text",
            "Docker", "VirtualBox"
        ]

        for app in all_apps:
            result = subprocess.run(f"killall '{app}'", shell=True, capture_output=True)
            if result.returncode == 0:
                print(f"  ✓ Closed {app}")
                freed += 1.5

        # Kill all Python
        subprocess.run("pkill -f python", shell=True, capture_output=True)
        freed += 2

        # Stop Ollama and restart
        print("  • Restarting Ollama service...")
        subprocess.run("pkill ollama", shell=True, capture_output=True)
        time.sleep(2)
        subprocess.Popen("ollama serve", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        freed += 3

        # Aggressive purge
        subprocess.run("sudo purge", shell=True, capture_output=True)
        freed += 3

        print(f"\n✅ Maximum cleanup complete! Estimated {freed:.1f}GB freed")
        return freed

    def monitor(self):
        """Start real-time monitoring"""
        print("\n🔍 Starting RAM Monitor (updates every 5 seconds, Ctrl+C to exit)")

        try:
            while True:
                os.system('clear')
                self.print_status()
                self.print_heavy_processes(5)
                time.sleep(5)
        except KeyboardInterrupt:
            print("\n\nMonitoring stopped.")


def main():
    """Main entry point"""
    optimizer = RAMOptimizer()

    # Parse command line arguments
    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == 'gentle':
            optimizer.print_status()
            optimizer.gentle_cleanup()
            print("\nNew status:")
            optimizer.print_status()

        elif command == 'normal':
            optimizer.print_status()
            optimizer.normal_cleanup()
            print("\nNew status:")
            optimizer.print_status()

        elif command == 'max':
            optimizer.print_status()
            optimizer.max_cleanup()
            print("\nNew status:")
            optimizer.print_status()

        elif command == 'monitor':
            optimizer.monitor()

        elif command == 'heavy':
            optimizer.print_heavy_processes(20)

        elif command in ['help', '--help', '-h']:
            print("ScriptureMonChampion RAM Optimizer")
            print("\nUsage: python3 optimize_ram.py [command]")
            print("\nCommands:")
            print("  status   - Show current RAM status (default)")
            print("  gentle   - Gentle cleanup (~5GB)")
            print("  normal   - Normal cleanup (~15GB)")
            print("  max      - Maximum cleanup (~35GB)")
            print("  monitor  - Real-time monitoring")
            print("  heavy    - Show top 20 RAM consumers")
            print("  help     - Show this help")

        else:
            print(f"Unknown command: {command}")
            print("Use 'python3 optimize_ram.py help' for usage")

    else:
        # Default: show status
        optimizer.print_status()
        optimizer.print_heavy_processes()
        print("\nUse 'python3 optimize_ram.py help' for more options")


if __name__ == "__main__":
    # Define BOLD and END globally for colored output
    BOLD = '\033[1m'
    END = '\033[0m'

    main()

# ============================================================
# AUTO-UNIFIED MEMORY HELPER
# ============================================================
def _get_memory():
    """Helper para acesso rápido à memória unificada"""
    return get_unified_memory()

# Atalhos para compatibilidade
unified_memory = _get_memory()
