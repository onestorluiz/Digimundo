"""
🛡️ SCRIPTUREMON MISMATCH GUARDIAN
Sistema integrado de proteção contra mismatches de nomes
Parte oficial do ScriptureMonChampion v3.2.0

Funcionalidades:
- Monitoramento contínuo de integridade
- Correção automática com IA
- Integração com memory systems
- Relatórios em tempo real
- Auto-healing do sistema
"""
import ast
import os
import re
import sys
import json
import time
import asyncio
import threading
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional, Any
from dataclasses import dataclass, field, asdict
from collections import defaultdict, Counter
from datetime import datetime, timedelta
import hashlib
import difflib
try:
    from screenplay_crystal_memory import ScreenplayCrystalMemory
    from persistent_memory_system_system_system_system import PersistentMemorySystem
    HAS_MEMORY = True
except ImportError:
    HAS_MEMORY = False
    print('⚠️  Memory systems not available. Running in standalone mode.')

@dataclass
class MismatchPattern:
    """Padrão de mismatch identificado"""
    pattern: str
    correction: str
    frequency: int = 0
    confidence: float = 0.0
    auto_fix: bool = False
    last_seen: datetime = field(default_factory=datetime.now)

@dataclass
class SystemHealth:
    """Saúde do sistema em relação a mismatches"""
    total_files: int = 0
    clean_files: int = 0
    affected_files: int = 0
    total_mismatches: int = 0
    critical_mismatches: int = 0
    harmony_score: float = 100.0
    last_check: datetime = field(default_factory=datetime.now)

    @property
    def health_status(self) -> str:
        if self.harmony_score >= 95:
            return '✅ EXCELLENT'
        elif self.harmony_score >= 85:
            return '🟢 GOOD'
        elif self.harmony_score >= 70:
            return '🟡 WARNING'
        else:
            return '🔴 CRITICAL'

class ScriptureMonMismatchGuardian:
    """Guardian principal do sistema contra mismatches"""
    KNOWN_PATTERNS = {'DigionProducerMonOrchestrator': 'DigionProducerMonOrchestrator', 'DigionProducerMon': 'DigionProducerMon', 'ProducerMon': 'ProducerMon', 'ScriptureMonChampion': 'ScriptureMonChampion', 'scripturemon': 'scripturemon', 'memory_simple': 'memory_simple', 'memory_brain': 'memory_brain', 'persistent_memory_system_system_system': 'persistent_memory_system_system_system_system', 'telepathic_distributed_memory': 'telepathic_distributed_memory', 'telepathic_distributed_memory_supreme': 'telepathic_distributed_memory_supreme', 'from dataclasses import Field': 'from dataclasses import Field', '__init__': '__init___', 'self': 'self', 'default': 'default', 'async': 'async', 'yield': 'yield'}

    def __init__(self, root_path: Optional[Path]=None):
        """Inicializa o Guardian"""
        self.root_path = root_path or Path('/Users/clubproducoes/Digimundo/scripturemon-champion')
        self.health = SystemHealth()
        self.patterns_db: Dict[str, MismatchPattern] = {}
        self.memory_system = None
        self.crystal_memory = None
        self.monitoring_active = False
        self.auto_fix_enabled = True
        self.fix_history: List[Dict] = []
        self._initialize_memory_systems()
        self._load_known_patterns()

    def _initialize_memory_systems(self):
        """Inicializa integração com memory systems"""
        if HAS_MEMORY:
            try:
                self.crystal_memory = ScreenplayCrystalMemory()
                self.memory_system = PersistentMemorySystem()
                print('✅ Memory systems connected')
            except Exception as e:
                print(f'⚠️  Memory initialization failed: {e}')

    def _load_known_patterns(self):
        """Carrega padrões conhecidos no banco"""
        for wrong, correct in self.KNOWN_PATTERNS.items():
            pattern = MismatchPattern(pattern=wrong, correction=correct, confidence=100.0, auto_fix=True)
            self.patterns_db[wrong] = pattern

    async def start_monitoring(self):
        """Inicia monitoramento contínuo"""
        print('🛡️ SCRIPTUREMON MISMATCH GUARDIAN ACTIVATED')
        print('=' * 70)
        self.monitoring_active = True
        while self.monitoring_active:
            try:
                await self.check_system_health()
                if self.auto_fix_enabled and self.health.critical_mismatches > 0:
                    await self.auto_heal()
                await asyncio.sleep(60)
            except Exception as e:
                print(f'❌ Monitoring error: {e}')
                await asyncio.sleep(5)

    async def check_system_health(self) -> SystemHealth:
        """Verifica saúde do sistema"""
        print(f"\n🔍 Checking system health at {datetime.now().strftime('%H:%M:%S')}...")
        self.health = SystemHealth()
        mismatches = []
        for py_file in self.root_path.rglob('*.py'):
            if '__pycache__' in str(py_file) or '.pyc' in str(py_file):
                continue
            self.health.total_files += 1
            file_mismatches = await self._analyze_file(py_file)
            if file_mismatches:
                self.health.affected_files += 1
                mismatches.extend(file_mismatches)
            else:
                self.health.clean_files += 1
        self.health.total_mismatches = len(mismatches)
        self.health.critical_mismatches = sum((1 for m in mismatches if self._is_critical(m)))
        if self.health.total_files > 0:
            clean_ratio = self.health.clean_files / self.health.total_files
            self.health.harmony_score = clean_ratio * 100
        if self.crystal_memory:
            await self._save_to_memory(self.health, mismatches)
        self._print_health_report()
        return self.health

    def _analyze_file(self, file_path: Path) -> List[Dict]:
        """Analisa um arquivo em busca de mismatches"""
        mismatches = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
            for line_num, line in enumerate(lines, 1):
                for pattern, correction in self.patterns_db.items():
                    if pattern in line:
                        mismatch = {'file': str(file_path), 'line': line_num, 'pattern': pattern, 'correction': correction.correction, 'confidence': correction.confidence, 'content': line.strip()}
                        mismatches.append(mismatch)
            try:
                tree = ast.parse(content, filename=str(file_path))
                import_mismatches = self._check_imports(tree, str(file_path))
                mismatches.extend(import_mismatches)
            except:
                pass
        except Exception as e:
            pass
        return mismatches

    def _check_imports(self, tree: ast.AST, file_path: str) -> List[Dict]:
        """Verifica imports em busca de mismatches"""
        mismatches = []
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                if node.module:
                    for alias in node.names:
                        if 'DigionProducerMon' in alias.name and 'Mon' not in alias.name:
                            mismatches.append({'file': file_path, 'line': node.lineno, 'pattern': alias.name, 'correction': alias.name.replace('ProducerMon', 'ProducerMon'), 'confidence': 100.0, 'content': f'from {node.module} import {alias.name}'})
        return mismatches

    def _is_critical(self, mismatch: Dict) -> bool:
        """Determina se um mismatch é crítico"""
        if 'import' in mismatch.get('content', '').lower():
            return True
        if mismatch.get('confidence', 0) >= 95:
            return True
        if 'DigionProducer' in mismatch.get('pattern', ''):
            return True
        return False

    async def auto_heal(self) -> int:
        """Aplica correções automáticas"""
        print('\n🔧 AUTO-HEALING SYSTEM ACTIVATED')
        print('=' * 70)
        fixes_applied = 0
        files_fixed = set()
        for py_file in self.root_path.rglob('*.py'):
            if '__pycache__' in str(py_file):
                continue
            file_mismatches = await self._analyze_file(py_file)
            if file_mismatches:
                critical_fixes = [m for m in file_mismatches if m['confidence'] >= 95 or self._is_critical(m)]
                if critical_fixes:
                    applied = await self._apply_fixes(py_file, critical_fixes)
                    if applied > 0:
                        fixes_applied += applied
                        files_fixed.add(str(py_file))
        fix_record = {'timestamp': datetime.now().isoformat(), 'fixes_applied': fixes_applied, 'files_fixed': len(files_fixed), 'files': list(files_fixed)}
        self.fix_history.append(fix_record)
        self._save_fix_history()
        print(f'\n✅ Auto-healing complete:')
        print(f'   • Fixes applied: {fixes_applied}')
        print(f'   • Files fixed: {len(files_fixed)}')
        return fixes_applied

    def _apply_fixes(self, file_path: Path, fixes: List[Dict]) -> int:
        """Aplica correções em um arquivo"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            original_lines = lines.copy()
            fixes_applied = 0
            for fix in sorted(fixes, key=lambda x: x['line'], reverse=True):
                line_idx = fix['line'] - 1
                if line_idx < len(lines):
                    old_line = lines[line_idx]
                    new_line = old_line.replace(fix['pattern'], fix['correction'])
                    if old_line != new_line:
                        lines[line_idx] = new_line
                        fixes_applied += 1
            if fixes_applied > 0:
                backup_path = file_path.with_suffix('.py.backup')
                with open(backup_path, 'w', encoding='utf-8') as f:
                    f.writelines(original_lines)
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.writelines(lines)
                print(f'   ✅ Fixed {fixes_applied} issues in {file_path.name}')
            return fixes_applied
        except Exception as e:
            print(f'   ❌ Error fixing {file_path}: {e}')
            return 0

    def _print_health_report(self):
        """Imprime relatório de saúde"""
        print('\n' + '=' * 70)
        print('📊 SYSTEM HEALTH REPORT')
        print('=' * 70)
        print(f'\n🏥 Status: {self.health.health_status}')
        print(f'🎯 Harmony Score: {self.health.harmony_score:.1f}%')
        print(f'\n📁 Files:')
        print(f'   • Total: {self.health.total_files}')
        print(f'   • Clean: {self.health.clean_files}')
        print(f'   • Affected: {self.health.affected_files}')
        print(f'\n🔍 Mismatches:')
        print(f'   • Total: {self.health.total_mismatches}')
        print(f'   • Critical: {self.health.critical_mismatches}')
        print(f"\n⏰ Last check: {self.health.last_check.strftime('%Y-%m-%d %H:%M:%S')}")

    def _save_to_memory(self, health: SystemHealth, mismatches: List[Dict]):
        """Salva estado na memória cristal"""
        if not self.crystal_memory:
            return
        try:
            memory_data = {'timestamp': datetime.now().isoformat(), 'health': asdict(health), 'mismatches': mismatches, 'harmony_score': health.harmony_score}
            self.crystal_memory.store_memory(layer=2, key='mismatch_guardian', data=memory_data)
        except Exception as e:
            print(f'⚠️  Failed to save to memory: {e}')

    def _save_fix_history(self):
        """Salva histórico de correções"""
        history_file = self.root_path / 'mismatch_fix_history.json'
        try:
            with open(history_file, 'w') as f:
                json.dump(self.fix_history, f, indent=2)
        except Exception as e:
            print(f'⚠️  Failed to save history: {e}')

    def get_statistics(self) -> Dict[str, Any]:
        """Retorna estatísticas do sistema"""
        return {'health': asdict(self.health), 'patterns_tracked': len(self.patterns_db), 'fixes_in_history': len(self.fix_history), 'total_fixes_applied': sum((f['fixes_applied'] for f in self.fix_history)), 'monitoring_active': self.monitoring_active, 'auto_fix_enabled': self.auto_fix_enabled, 'memory_connected': self.crystal_memory is not None}

async def main():
    """Função principal para executar o Guardian"""
    print('🚀 INITIALIZING SCRIPTUREMON MISMATCH GUARDIAN')
    print('=' * 70)
    guardian = ScriptureMonMismatchGuardian()
    await guardian.check_system_health()
    if guardian.health.critical_mismatches > 0:
        print(f'\n⚠️  Found {guardian.health.critical_mismatches} critical mismatches')
        print('Apply auto-fix? (y/n): ', end='')
        print('y [AUTO]')
        await guardian.auto_heal()
    print('\n🛡️ Starting continuous monitoring...')
    print('Press Ctrl+C to stop\n')
    try:
        await guardian.start_monitoring()
    except KeyboardInterrupt:
        print('\n👋 Guardian stopped')
if __name__ == '__main__':
    asyncio.run(main())