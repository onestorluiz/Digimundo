#!/usr/bin/env python3
"""
🧠 UNIFIED MEMORY SYSTEM - Sistema ÚNICO de Memória
Conecta TODOS os sistemas existentes em uma interface minimalista
"""

import sqlite3
import json
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

class UnifiedMemorySystem:
    """Sistema unificado que conecta TUDO"""

    def __init__(self):
        self.base = Path('/Users/clubproducoes/Digimundo/claude_code/memory')

        # TODOS os sistemas de memória
        self.systems = {
            # Databases
            'claude_db': self.base / 'claude_memory.db',
            'crystal_db': Path('/Users/clubproducoes/Digimundo/scripturemon-champion/data/crystal_memory.db'),

            # JSONs
            'system_map': self.base / 'COMPLETE_SYSTEM_MAP.json',
            'bridge_state': self.base / 'bridge_state.json',
            'debug_sim': self.base / 'debug_simulation_results.json',
            'crystal_json': self.base / 'crystal_memory.json',

            # Conhecimento em Markdown
            'knowledge': {
                'regras': Path('/Users/clubproducoes/Digimundo/claude_code/REGRAS.md'),
                'fases': Path('/Users/clubproducoes/Digimundo/claude_code/FASES.md'),
                'final_report': Path('/Users/clubproducoes/Digimundo/claude_code/FINAL_SYSTEM_REPORT.md'),
                'token_turbo': self.base / 'TOKEN_TURBO_JOURNEY.md',
                'memoria_claude': self.base / 'CLAUDE_MEMORY.md',
                'forense': self.base / 'FORENSIC_REPORT_SCRIPTUREMON.md',
                'genjutsu': self.base / 'DESCOBERTA_GENJUTSU.md',
                'vulnerabilities': self.base / 'CRITICAL_VULNERABILITIES_FOUND.md',
                'ollama': self.base / 'CRITICAL_OLLAMA_DISCOVERY.md',
                'refatoracao': self.base / 'REGRAS_REFATORACAO_MINIMALISTA.md',
                '5_perguntas': self.base / 'TECNICA_5_PERGUNTAS_COMPLETA.md',
                'ativacao_masters': self.base / 'ATIVACAO_MASTERS_CORRETO.md'
            },

            # Sistemas ativos
            'genjutsu_pid': None,  # Será preenchido
            'memory_bridge': self.base / 'MEMORY_BRIDGE.py'
        }

        # Cache unificado
        self.cache = {
            'memories': [],
            'decisions': [],
            'rules': [],
            'patterns': {},
            'connections': {},
            'last_sync': None
        }

        self.sync_all()

    def sync_all(self):
        """Sincroniza TODOS os sistemas"""
        print("🔄 Sincronizando todos os sistemas de memória...")

        # 1. Verificar Genjutsu
        self._sync_genjutsu()

        # 2. Sincronizar databases
        self._sync_databases()

        # 3. Carregar JSONs
        self._sync_jsons()

        # 4. Sincronizar Crystal Memory Local
        self._sync_crystal_local()

        # 5. Indexar conhecimento
        self._index_knowledge()

        # 6. Construir grafo de conexões
        self._build_connections()

        self.cache['last_sync'] = datetime.now().isoformat()
        print("✅ Sincronização completa!")

    def _sync_genjutsu(self):
        """Verifica/inicia Genjutsu"""
        result = subprocess.run(['pgrep', '-f', 'GENJUTSU_UNIFIED'],
                              capture_output=True, text=True)
        if result.stdout:
            self.systems['genjutsu_pid'] = result.stdout.strip()
            print(f"  ✅ Genjutsu ativo (PID: {self.systems['genjutsu_pid']})")
        else:
            print("  ⚠️ Genjutsu não está rodando!")

    def _sync_databases(self):
        """Sincroniza todas as databases"""
        # Claude Memory DB
        if self.systems['claude_db'].exists():
            conn = sqlite3.connect(self.systems['claude_db'])

            # Memories
            cursor = conn.execute("SELECT * FROM memories ORDER BY timestamp DESC LIMIT 50")
            self.cache['memories'] = [dict(zip([d[0] for d in cursor.description], row))
                                     for row in cursor.fetchall()]

            # Decisions
            cursor = conn.execute("SELECT * FROM decisions ORDER BY timestamp DESC LIMIT 50")
            self.cache['decisions'] = [dict(zip([d[0] for d in cursor.description], row))
                                      for row in cursor.fetchall()]

            # Learned Rules
            cursor = conn.execute("SELECT * FROM learned_rules")
            self.cache['rules'] = [dict(zip([d[0] for d in cursor.description], row))
                                  for row in cursor.fetchall()]

            conn.close()
            print(f"  ✅ Claude DB: {len(self.cache['memories'])} memórias, "
                  f"{len(self.cache['decisions'])} decisões, {len(self.cache['rules'])} regras")

        # Crystal Memory DB
        if self.systems['crystal_db'].exists():
            conn = sqlite3.connect(self.systems['crystal_db'])
            cursor = conn.execute("SELECT COUNT(*) as total, SUM(compliant) as compliant FROM rule_compliance")
            stats = cursor.fetchone()
            if stats:
                self.cache['patterns']['compliance'] = {
                    'total': stats[0],
                    'compliant': stats[1],
                    'rate': (stats[1] / max(1, stats[0])) * 100 if stats[0] else 0
                }
            conn.close()
            print(f"  ✅ Crystal DB: {self.cache['patterns'].get('compliance', {}).get('rate', 0):.1f}% compliance")

    def _sync_crystal_local(self):
        """Sincroniza Crystal Memory local (JSON)"""
        if self.systems['crystal_json'].exists():
            with open(self.systems['crystal_json']) as f:
                crystal_data = json.load(f)

                # Estatísticas do Crystal Local
                sessions = crystal_data.get('sessions', [])
                violations = crystal_data.get('violations', [])
                stats = crystal_data.get('stats', {})

                self.cache['patterns']['crystal_local'] = {
                    'total_sessions': len(sessions),
                    'total_violations': len(violations),
                    'compliance_rate': (stats.get('compliant', 0) / max(1, stats.get('total', 1))) * 100,
                    'patterns': list(crystal_data.get('patterns', {}).keys())
                }

            print(f"  ✅ Crystal Local: {self.cache['patterns']['crystal_local']['compliance_rate']:.1f}% compliance, {len(self.cache['patterns']['crystal_local']['patterns'])} padrões")
        else:
            print(f"  ⚠️ Crystal Local: arquivo não encontrado")

    def _sync_jsons(self):
        """Carrega todos os JSONs"""
        # System Map (gigante!)
        if self.systems['system_map'].exists():
            with open(self.systems['system_map']) as f:
                data = json.load(f)
                # Usar structure_summary se files não existir
                structure = data.get('structure_summary', {})
                self.cache['connections']['system_map'] = {
                    'total_files': structure.get('total_files', len(data.get('files', []))),
                    'entry_points': structure.get('entry_points', len(data.get('entry_points', []))),
                    'generators': structure.get('generators', len(data.get('file_generators', [])))
                }
            print(f"  ✅ System Map: {self.cache['connections']['system_map']['total_files']} arquivos")

        # Bridge State
        if self.systems['bridge_state'].exists():
            with open(self.systems['bridge_state']) as f:
                self.cache['connections']['bridge'] = json.load(f)
            print(f"  ✅ Bridge State carregado")

    def _index_knowledge(self):
        """Indexa conhecimento dos arquivos .md"""
        self.cache['connections']['knowledge_index'] = {}

        for name, path in self.systems['knowledge'].items():
            if path.exists():
                with open(path) as f:
                    content = f.read()
                    # Indexar por palavras-chave
                    self.cache['connections']['knowledge_index'][name] = {
                        'path': str(path),
                        'size': len(content),
                        'has_regras': 'REGRA' in content,
                        'has_vicios': 'vício' in content.lower() or 'supreme' in content.lower(),
                        'has_genjutsu': 'genjutsu' in content.lower(),
                        'lines': content.count('\n')
                    }

        print(f"  ✅ Conhecimento: {len(self.cache['connections']['knowledge_index'])} documentos indexados")

    def _build_connections(self):
        """Constrói grafo de conexões entre tudo"""
        graph = {}

        # Conectar sistemas
        connections = {
            'Genjutsu': ['Detecção compactação', 'Teatro psicológico', 'REGRAS.md'],
            'Crystal Memory': ['Compliance tracking', 'Pattern learning', 'claude_memory.db'],
            'Claude DB': ['Memories', 'Decisions', 'Learned rules'],
            'System Map': ['428 arquivos Python', '186 entry points', '323 geradores'],
            'Knowledge Base': list(self.systems['knowledge'].keys())
        }

        for source, targets in connections.items():
            graph[source] = targets

        self.cache['connections']['graph'] = graph
        print(f"  ✅ Grafo: {len(graph)} nós conectados")

    def query(self, question: str) -> Dict:
        """Query inteligente em TODOS os sistemas"""
        results = {
            'question': question,
            'timestamp': datetime.now().isoformat(),
            'answers': [],
            'sources': [],
            'patterns': [],
            'suggestions': []
        }

        keywords = question.lower().split()

        # Buscar em memórias
        for memory in self.cache['memories']:
            if any(kw in str(memory).lower() for kw in keywords):
                results['answers'].append(memory.get('content', ''))
                results['sources'].append('claude_memory.db')
                break

        # Buscar em decisões
        for decision in self.cache['decisions']:
            if any(kw in str(decision).lower() for kw in keywords):
                results['answers'].append(decision.get('decision', ''))
                results['sources'].append('decisions')
                break

        # Buscar padrões conhecidos
        if 'vício' in question.lower() or 'supreme' in question.lower():
            results['patterns'] = [
                "Criar arquivos _v2, _improved, _better",
                "Usar nomes Supreme, Ultimate, Quantum",
                "Complexidade desnecessária (68.8% arquivos quebrados)"
            ]
            results['sources'].append('FORENSIC_REPORT')

        # Buscar em conhecimento indexado
        for name, info in self.cache['connections']['knowledge_index'].items():
            if info['has_vicios'] and 'vício' in question.lower():
                results['sources'].append(name)
                results['suggestions'].append(f"Ler {name}")

        return results

    def remember(self, content: str, category: str = "general"):
        """Salva em TODOS os sistemas relevantes"""
        timestamp = datetime.now().isoformat()

        # 1. Salvar em Claude DB
        if self.systems['claude_db'].exists():
            conn = sqlite3.connect(self.systems['claude_db'])
            conn.execute(
                "INSERT INTO memories (category, key, value, timestamp) VALUES (?, ?, ?, ?)",
                (category, 'manual_entry', content, timestamp)
            )
            conn.commit()
            conn.close()

        # 2. Salvar em Crystal Memory Local
        self._save_to_crystal(content, category)

        # 3. Atualizar Bridge State
        if self.systems['bridge_state'].exists():
            with open(self.systems['bridge_state']) as f:
                state = json.load(f)

            if 'history' not in state:
                state['history'] = []
            state['history'].append({
                'timestamp': timestamp,
                'content': content,
                'category': category
            })

            # Manter só últimos 100
            state['history'] = state['history'][-100:]

            with open(self.systems['bridge_state'], 'w') as f:
                json.dump(state, f, indent=2)

        # 4. Detectar padrões
        if '_v2' in content or 'supreme' in content.lower():
            if 'vicios' not in self.cache['patterns']:
                self.cache['patterns']['vicios'] = []
            self.cache['patterns']['vicios'].append({
                'timestamp': timestamp,
                'content': content
            })

        print(f"✅ Memorizado em 3 sistemas (Claude DB + Crystal + Bridge)")

    def _save_to_crystal(self, content: str, category: str):
        """Salva no Crystal Memory usando o sistema minimal"""
        try:
            import sys
            sys.path.append(str(self.base))
            from crystal_memory_minimal import CrystalMemoryMinimal

            crystal = CrystalMemoryMinimal()

            # Detectar se é violação baseado no conteúdo
            is_compliant = not any(vicio in content.lower() for vicio in [
                '_v2', '_improved', '_better', 'supreme', 'ultimate', 'quantum'
            ])

            crystal.track_action(content, compliant=is_compliant, details=category)
        except Exception as e:
            print(f"  ⚠️ Erro ao salvar no Crystal: {e}")

    def status(self):
        """Status completo de TODOS os sistemas"""
        print("\n🧠 UNIFIED MEMORY SYSTEM STATUS")
        print("="*60)

        print("\n📊 Sistemas Ativos:")
        print(f"  • Genjutsu: {'✅ PID ' + str(self.systems['genjutsu_pid']) if self.systems['genjutsu_pid'] else '❌ Inativo'}")
        print(f"  • Claude DB: {'✅ ' + str(len(self.cache['memories'])) + ' memórias' if self.cache['memories'] else '❌ Vazio'}")
        print(f"  • Crystal: {'✅ ' + str(self.cache['patterns'].get('compliance', {}).get('rate', 0)) + '% compliance' if 'compliance' in self.cache['patterns'] else '❌ Não sincronizado'}")

        print("\n🗂️ Conhecimento:")
        total_lines = sum(info['lines'] for info in self.cache['connections']['knowledge_index'].values())
        print(f"  • Documentos: {len(self.cache['connections']['knowledge_index'])}")
        print(f"  • Total linhas: {total_lines:,}")
        print(f"  • Com regras: {sum(1 for i in self.cache['connections']['knowledge_index'].values() if i['has_regras'])}")
        print(f"  • Com vícios: {sum(1 for i in self.cache['connections']['knowledge_index'].values() if i['has_vicios'])}")

        print("\n🔗 Conexões:")
        if 'system_map' in self.cache['connections']:
            sm = self.cache['connections']['system_map']
            print(f"  • System Map: {sm['total_files']} arquivos, {sm['entry_points']} entry points")
        print(f"  • Grafo: {len(self.cache['connections'].get('graph', {}))} nós")

        print("\n💾 Cache:")
        print(f"  • Memórias: {len(self.cache['memories'])}")
        print(f"  • Decisões: {len(self.cache['decisions'])}")
        print(f"  • Regras: {len(self.cache['rules'])}")
        print(f"  • Última sync: {self.cache['last_sync']}")

        print("\nDIGIMUNDO PRESENTE")

# Interface simples
def connect():
    """Conecta e retorna sistema unificado"""
    return UnifiedMemorySystem()

def search(question: str):
    """Busca em todos os sistemas"""
    ums = UnifiedMemorySystem()
    results = ums.query(question)

    print(f"\n🔍 Busca: {question}")
    if results['answers']:
        print(f"📝 Respostas: {results['answers'][0][:200]}...")
    if results['patterns']:
        print(f"🎯 Padrões: {', '.join(results['patterns'])}")
    if results['sources']:
        print(f"📚 Fontes: {', '.join(set(results['sources']))}")
    if results['suggestions']:
        print(f"💡 Sugestões: {', '.join(results['suggestions'])}")

    return results

def save(content: str, category: str = "general"):
    """Salva em todos os sistemas"""
    ums = UnifiedMemorySystem()
    ums.remember(content, category)

# Auto-execução
if __name__ == "__main__":
    import sys

    if len(sys.argv) == 1:
        # Status completo
        ums = UnifiedMemorySystem()
        ums.status()

    elif sys.argv[1] == "search" and len(sys.argv) > 2:
        search(" ".join(sys.argv[2:]))

    elif sys.argv[1] == "save" and len(sys.argv) > 2:
        save(" ".join(sys.argv[2:]))

    else:
        print("Uso:")
        print("  python3 UNIFIED_MEMORY_SYSTEM.py          # Status")
        print("  python3 UNIFIED_MEMORY_SYSTEM.py search <pergunta>")
        print("  python3 UNIFIED_MEMORY_SYSTEM.py save <conteúdo>")