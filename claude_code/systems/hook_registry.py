#!/usr/bin/env python3
"""
🪝 HOOK REGISTRY - Central de Hooks para Integração Total
Registra e gerencia todos os hooks do ecossistema
"""

import json
import sqlite3
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Callable
import importlib.util
import threading

class HookRegistry:
    """Registry central para todos os hooks do sistema"""

    def __init__(self):
        self.base = Path('/Users/clubproducoes/Digimundo/claude_code')
        self.registry_file = self.base / 'MEMORY' / 'hook_registry.json'
        self.db_path = self.base / 'MEMORY' / 'claude_memory.db'

        # Registry em memória
        self.hooks = {
            'pre_action': [],
            'post_action': [],
            'memory_save': [],
            'decision_made': [],
            'violation_detected': [],
            'archive_organized': [],
            'system_startup': [],
            'system_shutdown': [],
            'behavioral_override': []
        }

        # Hooks permanentes do sistema
        self.permanent_hooks = {
            'memory_save': [self._save_to_database],
            'violation_detected': [self._behavioral_enforcement],
            'system_startup': [self._load_crystal_memory]
        }

        # Lock para thread safety
        self.lock = threading.Lock()

        # Carrega registry salvo
        self.load_registry()

        # Registra hooks permanentes
        self._register_permanent_hooks()

    def _register_permanent_hooks(self):
        """Registra hooks que sempre devem estar ativos"""
        for event_type, hooks in self.permanent_hooks.items():
            for hook in hooks:
                self.register(event_type, hook, permanent=True)

    def register(self, event_type: str, hook: Callable, permanent: bool = False):
        """Registra um novo hook"""
        with self.lock:
            if event_type not in self.hooks:
                self.hooks[event_type] = []

            hook_info = {
                'name': hook.__name__ if hasattr(hook, '__name__') else str(hook),
                'module': hook.__module__ if hasattr(hook, '__module__') else 'unknown',
                'permanent': permanent,
                'registered_at': datetime.now().isoformat(),
                'callable': hook
            }

            # Evita duplicatas
            existing = [h for h in self.hooks[event_type] if h['name'] == hook_info['name']]
            if not existing:
                self.hooks[event_type].append(hook_info)
                self.save_registry()
                return True
            return False

    def unregister(self, event_type: str, hook_name: str):
        """Remove um hook (exceto permanentes)"""
        with self.lock:
            if event_type in self.hooks:
                self.hooks[event_type] = [
                    h for h in self.hooks[event_type]
                    if h['name'] != hook_name or h['permanent']
                ]
                self.save_registry()
                return True
            return False

    def trigger(self, event_type: str, **kwargs) -> List[Any]:
        """Dispara todos os hooks de um evento"""
        results = []

        if event_type in self.hooks:
            for hook_info in self.hooks[event_type]:
                try:
                    hook = hook_info['callable']
                    result = hook(**kwargs)
                    results.append({
                        'hook': hook_info['name'],
                        'result': result,
                        'success': True
                    })
                except Exception as e:
                    results.append({
                        'hook': hook_info['name'],
                        'error': str(e),
                        'success': False
                    })

        return results

    def _save_to_database(self, **kwargs):
        """Hook para salvar em database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Salva como automated_action
            cursor.execute("""
                INSERT INTO automated_actions
                (timestamp, action_type, description, result, session_id)
                VALUES (?, ?, ?, ?, ?)
            """, (
                datetime.now().isoformat(),
                kwargs.get('event_type', 'hook_triggered'),
                kwargs.get('description', ''),
                json.dumps(kwargs),
                kwargs.get('session_id', 'hook_registry')
            ))

            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"❌ Erro salvando no database: {e}")
            return False

    def _behavioral_enforcement(self, **kwargs):
        """Hook para enforcement comportamental"""
        violation = kwargs.get('violation', '')

        # Vícios conhecidos
        vices = ['_v2', '_improved', '_better', 'supreme', 'ultimate', 'quantum']

        for vice in vices:
            if vice in violation.lower():
                print(f"🚨 VIOLAÇÃO DETECTADA: {vice}")
                print(f"📍 Contexto: {violation}")
                print("⚠️ Ação bloqueada conforme UCHIMON laws")

                # Registra violação
                self._save_to_database(
                    event_type='violation_blocked',
                    description=f"Bloqueado vício: {vice}",
                    violation=violation
                )
                return {'blocked': True, 'reason': f"Vício detectado: {vice}"}

        return {'blocked': False}

    def _load_crystal_memory(self, **kwargs):
        """Hook para carregar crystal memory no startup"""
        crystal_path = self.base / 'MEMORY' / 'crystal_memory.json'

        if crystal_path.exists():
            with open(crystal_path) as f:
                crystal = json.load(f)

            print("💎 Crystal Memory carregado:")
            print(f"  • {len(crystal.get('crystallized_memories', []))} memórias")
            print(f"  • {len(crystal.get('learned_patterns', []))} padrões")
            print(f"  • Score: {crystal.get('system_state', {}).get('harmony_score', 0)}")

            return crystal
        return {}

    def save_registry(self):
        """Salva registry em JSON"""
        registry_data = {
            'last_updated': datetime.now().isoformat(),
            'hooks': {}
        }

        for event_type, hooks in self.hooks.items():
            registry_data['hooks'][event_type] = [
                {
                    'name': h['name'],
                    'module': h['module'],
                    'permanent': h['permanent'],
                    'registered_at': h['registered_at']
                }
                for h in hooks
            ]

        with open(self.registry_file, 'w') as f:
            json.dump(registry_data, f, indent=2)

    def load_registry(self):
        """Carrega registry salvo"""
        if self.registry_file.exists():
            with open(self.registry_file) as f:
                data = json.load(f)

            # Nota: não carrega os callables, apenas metadados
            # Os hooks precisam ser re-registrados na inicialização
            return data
        return {}

    def list_hooks(self):
        """Lista todos os hooks registrados"""
        print("\n🪝 HOOK REGISTRY STATUS")
        print("="*60)

        total = 0
        for event_type, hooks in self.hooks.items():
            if hooks:
                print(f"\n📌 {event_type}:")
                for hook in hooks:
                    permanent = "🔒" if hook['permanent'] else "  "
                    print(f"  {permanent} {hook['name']} ({hook['module']})")
                    total += 1

        print(f"\n📊 Total: {total} hooks registrados")
        print("🔒 = Hook permanente (não pode ser removido)")

    def integrate_with_system(self, system_name: str, module_path: str):
        """Integra hooks de outro sistema"""
        try:
            # Carrega módulo dinamicamente
            spec = importlib.util.spec_from_file_location(system_name, module_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            # Procura por funções hook_*
            hooks_found = 0
            for attr_name in dir(module):
                if attr_name.startswith('hook_'):
                    hook_func = getattr(module, attr_name)
                    if callable(hook_func):
                        # Determina tipo de evento pelo nome
                        event_type = attr_name.replace('hook_', '')
                        if self.register(event_type, hook_func):
                            hooks_found += 1

            print(f"✅ Sistema {system_name} integrado: {hooks_found} hooks registrados")
            return True

        except Exception as e:
            print(f"❌ Erro integrando {system_name}: {e}")
            return False

# Singleton global
_registry = None

def get_registry():
    """Retorna instância singleton do registry"""
    global _registry
    if _registry is None:
        _registry = HookRegistry()
    return _registry

# Interface simples
def register_hook(event_type: str, hook: Callable, permanent: bool = False):
    """Registra um hook globalmente"""
    return get_registry().register(event_type, hook, permanent)

def trigger_hooks(event_type: str, **kwargs):
    """Dispara hooks de um evento"""
    return get_registry().trigger(event_type, **kwargs)

def list_all_hooks():
    """Lista todos os hooks"""
    return get_registry().list_hooks()

# Auto-teste
if __name__ == "__main__":
    registry = get_registry()

    print("🪝 HOOK REGISTRY SYSTEM")
    print("="*60)

    # Lista hooks atuais
    registry.list_hooks()

    # Teste de trigger
    print("\n🧪 Testando triggers:")

    # Teste memory_save
    results = registry.trigger('memory_save',
                              description="Teste do hook registry",
                              event_type="test")
    print(f"  memory_save: {len([r for r in results if r['success']])} sucessos")

    # Teste violation_detected
    results = registry.trigger('violation_detected',
                              violation="arquivo_v2_improved.py")
    print(f"  violation_detected: bloqueado={results[0]['result']['blocked'] if results else False}")

    print("\nDIGIMUNDO PRESENTE")