"""
🎬⚡️🧠 SCRIPTUREMON CHAMPION - INTELLIGENT LAUNCHER
Intelligent startup system with resource management orchestration
ZERO TIMEOUTS - PERFECT HARMONY - SCRIPT DOCTOR FOCUS
"""
import os
import sys
import asyncio
import psutil
import time
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime
import subprocess
import signal
from src.core.unified_memory_system import get_unified_memory, MemoryType
# Auto-unified: Este arquivo foi automaticamente integrado ao sistema unificado

PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))
RESULTS_DIR = PROJECT_ROOT / 'output' / 'results'
RESULTS_DIR.mkdir(parents=True, exist_ok=True)
try:
    from src.core.resource_manager import ResourceManager, SystemSector
    RESOURCE_MANAGER_AVAILABLE = True
except ImportError:
    RESOURCE_MANAGER_AVAILABLE = False
    print('⚠️ Resource Manager not available - using basic startup')

class ScripturemonLauncher:
    """
    Intelligent launcher with perfect initialization flow
    """

    def __init__(self):
        self.start_time = datetime.now()
        self.resource_manager = None
        self.startup_config = self._detect_optimal_config()
        print('\n' + '=' * 80)
        print('🎬⚡️ SCRIPTUREMON CHAMPION - INTELLIGENT SYSTEM')
        print(f"📅 {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print('=' * 80)

    def _detect_optimal_config(self) -> Dict[str, Any]:
        """Detect optimal configuration for this Mac"""
        mem = psutil.virtual_memory()
        cpu_count = psutil.cpu_count()
        available_gb = mem.available / 1024 ** 3
        can_use_full_power = available_gb > 20
        return {'mode': 'full_power' if can_use_full_power else 'efficient', 'available_memory_gb': available_gb, 'total_memory_gb': mem.total / 1024 ** 3, 'cpu_cores': cpu_count, 'target_memory_gb': min(45.0, available_gb * 0.8), 'startup_sectors': self._determine_startup_sectors(available_gb)}

    def _determine_startup_sectors(self, available_gb: float) -> list:
        """Intelligently determine which sectors to start"""
        essential = ['CORE', 'SCRIPT_DOCTOR', 'MEMORY_PRIMARY']
        if available_gb > 10:
            essential.append('OLLAMA_MODELS')
            essential.append('CINEMA_ANALYSIS')
        if available_gb > 20:
            essential.append('CONSCIOUSNESS')
            essential.append('MEMORY_ADVANCED')
            essential.append('NEURAL_NETWORKS')
        if available_gb > 30:
            essential.append('PROCESSING_CORE')
            essential.append('RAG_SYSTEM')
        return essential

    async def initialize_resource_manager(self) -> bool:
        """Initialize Resource Manager for system management"""
        if not RESOURCE_MANAGER_AVAILABLE:
            return False
        try:
            print('\n🎮 Initializing Resource Manager...')
            self.resource_manager = ResourceManager()
            print('\n📍 Activating essential sectors...')
            for sector_name in self.startup_config['startup_sectors']:
                sector = getattr(SystemSector, sector_name)
                await self.resource_manager.activate_sector(sector)
                await asyncio.sleep(0.1)
            print(f"\n✅ Resource Manager ready with {len(self.startup_config['startup_sectors'])} sectors active")
            return True
        except Exception as e:
            print(f'❌ Resource Manager initialization failed: {e}')
            return False

    async def start_script_doctor(self):
        """Start the main Script Doctor system"""
        print('\n🎬 Starting Script Doctor System...')
        mem = psutil.virtual_memory()
        if mem.percent > 80 and self.resource_manager:
            print('  📊 High memory usage detected - creating thinking space...')
            await self.resource_manager.create_thinking_space('script_analysis')
        try:
            from src.core.cli_champion import main as cli_main
            print('\n🚀 Launching Script Doctor CLI...')
            print('-' * 80)
            result = await subprocess.run([sys.executable, 'bin/scripturemon'], env={**os.environ, 'PYTHONPATH': str(PROJECT_ROOT)})
            return result.returncode == 0
        except KeyboardInterrupt:
            print('\n\n⚡ Graceful shutdown initiated...')
            return True
        except Exception as e:
            print(f'❌ Script Doctor startup failed: {e}')
            return False

    async def monitor_system(self):
        """Continuous system monitoring"""
        while True:
            try:
                mem = psutil.virtual_memory()
                cpu = psutil.cpu_percent(interval=1)
                if mem.percent > 90 and self.resource_manager:
                    print('\n⚠️ Memory critical - activating emergency thinking space...')
                    await self.resource_manager.emergency_thinking_space()
                await asyncio.sleep(10)
            except Exception:
                await asyncio.sleep(30)

# UNUSED - Candidate for removal
#     def print_startup_summary(self):
        """Print helpful startup summary"""
        elapsed = (datetime.now() - self.start_time).total_seconds()
        print('\n' + '=' * 80)
        print('✅ SCRIPTUREMON CHAMPION READY!')
        print('=' * 80)
        print(f'⏱️ Startup time: {elapsed:.1f} seconds')
        print(f"💾 Memory allocated: {self.startup_config['target_memory_gb']:.1f}GB")
        print(f"🎮 Mode: {self.startup_config['mode'].upper()}")
        print(f'📂 Results directory: {RESULTS_DIR}')
        print('\n📝 Quick Commands:')
        print('  scripturemon analyze <pdf>  - Analyze a screenplay')
        print('  scripturemon chat           - Interactive Script Doctor')
        print('  scripturemon status         - System status')
        print('  scripturemon help           - All commands')
        print('\n💡 Tips:')
        print('  - Press Ctrl+C for graceful shutdown')
        print('  - Results are saved to: output/results/')
        print('  - Resource Manager handles memory automatically')
        print('=' * 80)

    async def run(self):
        """Main execution flow"""
        try:
            if RESOURCE_MANAGER_AVAILABLE:
                await self.initialize_resource_manager()
            self.print_startup_summary()
            monitor_task = asyncio.create_task(self.monitor_system())
            success = await self.start_script_doctor()
            monitor_task.cancel()
            if self.resource_manager:
                print('\n🔄 Shutting down Resource Manager...')
                await self.resource_manager.shutdown()
            return success
        except KeyboardInterrupt:
            print('\n\n⚡ Interrupted by user')
            if self.resource_manager:
                await self.resource_manager.shutdown()
            return True

# UNUSED - Candidate for removal
# def fix_results_directory():
    """Fix the Respostas_testes location issue"""
    old_dir = Path('/Users/clubproducoes/Digimundo/Respostas_testes')
    new_dir = RESULTS_DIR
    if old_dir.exists() and old_dir.is_dir():
        print(f'\n📁 Moving results from {old_dir} to {new_dir}...')
        for file in old_dir.glob('*'):
            if file.is_file():
                target = new_dir / file.name
                if not target.exists():
                    file.rename(target)
                    print(f'  ✓ Moved: {file.name}')
        print(f'  ✅ Results directory fixed: {new_dir}')
    print('\n🔧 Updating code references...')
    files_to_update = ['apps/scripturemon/script_doctor.py', 'apps/scripturemon/cinema_ml_deeplearning_system.py', 'apps/scripturemon/comprehensive_system_test.py', 'apps/scripturemon/script_doctor_integration.py', 'apps/scripturemon/quick_biblioteca_check.py', 'apps/scripturemon/cinema_ml_simplified.py', 'apps/scripturemon/test_pdf_cinema_analysis.py', 'apps/scripturemon/cinema_deep_reflection_system.py', 'apps/scripturemon/ollama_config.py', 'apps/scripturemon/quick_processing_test.py']
    for filepath in files_to_update:
        full_path = PROJECT_ROOT / filepath
        if full_path.exists():
            content = full_path.read_text()
            if '/Users/clubproducoes/Digimundo/Respostas_testes' in content:
                new_content = content.replace('/Users/clubproducoes/Digimundo/Respostas_testes', str(RESULTS_DIR))
                full_path.write_text(new_content)
                print(f'  ✓ Updated: {filepath}')

async def main():
    """Main entry point"""
    print('\n🚀 SCRIPTUREMON CHAMPION LAUNCHER')
    print('Intelligent System • Zero Timeouts • Perfect Harmony')
    fix_results_directory()
    launcher = ScripturemonLauncher()
    success = await launcher.run()
    if success:
        print('\n✨ Thank you for using Scripturemon Champion!')
    else:
        print('\n⚠️ Scripturemon encountered issues. Check logs for details.')
    return 0 if success else 1

def signal_handler(sig, frame):
    """Handle Ctrl+C gracefully"""
    print('\n\n⚡ Shutting down gracefully...')
    sys.exit(0)
if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    exit_code = asyncio.run(main())
    sys.exit(exit_code)

# ============================================================
# AUTO-UNIFIED MEMORY HELPER
# ============================================================
def _get_memory():
    """Helper para acesso rápido à memória unificada"""
    return get_unified_memory()

# Atalhos para compatibilidade
unified_memory = _get_memory()
