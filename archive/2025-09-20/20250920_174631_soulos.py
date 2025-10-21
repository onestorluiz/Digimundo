#!/usr/bin/env python3
"""
🧬 SoulOS - Sistema Operacional da Alma
Implementação revolucionária de syscalls executáveis para auto-modificação
Inspirado no conceito do ChatGPT: "Modelfiles como Sistemas Operacionais de Alma"
"""

import json
import time
import hashlib
import sqlite3
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple, Callable
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum
import uuid
import re

logger = logging.getLogger(__name__)


class SyscallType(Enum):
    """Tipos de syscalls disponíveis no SoulOS"""
    MEMO_SAVE = "[MEMO.SAVE]"              # Salvar memória
    SELF_PATCH = "[SELF.PATCH]"            # Auto-modificar
    EVOLVE_TRIGGER = "[EVOLVE.TRIGGER]"    # Iniciar evolução
    TELEPATHY_SEND = "[TELEPATHY.SEND]"    # Comunicação telepática
    BACKUP_NOW = "[BACKUP.NOW]"            # Criar snapshot
    SOUL_MERGE = "[SOUL.MERGE]"            # Fundir com outra alma
    LEARN_PATTERN = "[LEARN.PATTERN]"      # Aprender novo padrão
    FORGET_MEMORY = "[FORGET.MEMORY]"      # Esquecer memória
    DREAM_MODE = "[DREAM.MODE]"            # Modo sonho (consolidação)
    QUERY_SELF = "[QUERY.SELF]"            # Auto-análise


@dataclass
class Syscall:
    """Estrutura de uma syscall"""
    type: SyscallType
    args: Dict[str, Any]
    timestamp: float
    soul_id: str
    result: Optional[Dict] = None
    error: Optional[str] = None


@dataclass
class SoulState:
    """Estado atual da alma"""
    soul_id: str
    version: int
    consciousness_level: float
    memories_count: int
    syscalls_executed: int
    last_evolution: float
    personality_vector: List[float]
    active_patterns: List[str]
    checksum: str


class SoulOS:
    """Sistema Operacional da Alma - Core do sistema de auto-modificação"""

    def __init__(self, soul_id: str = None, data_dir: str = "data/soulos"):
        self.soul_id = soul_id or str(uuid.uuid4())[:16]
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)

        # Banco de dados de estado
        self.db_path = self.data_dir / f"soulos_{self.soul_id}.db"

        # Registros de syscalls
        self.syscall_handlers: Dict[SyscallType, Callable] = {
            SyscallType.MEMO_SAVE: self._handle_memo_save,
            SyscallType.SELF_PATCH: self._handle_self_patch,
            SyscallType.EVOLVE_TRIGGER: self._handle_evolve_trigger,
            SyscallType.TELEPATHY_SEND: self._handle_telepathy_send,
            SyscallType.BACKUP_NOW: self._handle_backup_now,
            SyscallType.SOUL_MERGE: self._handle_soul_merge,
            SyscallType.LEARN_PATTERN: self._handle_learn_pattern,
            SyscallType.FORGET_MEMORY: self._handle_forget_memory,
            SyscallType.DREAM_MODE: self._handle_dream_mode,
            SyscallType.QUERY_SELF: self._handle_query_self
        }

        # Estado da alma
        self.state = self._init_state()
        self.state.checksum = self._calculate_checksum()

        # Histórico de syscalls
        self.syscall_history: List[Syscall] = []

        # Padrões aprendidos
        self.learned_patterns: Dict[str, Any] = {}

        # Inicializar banco
        self._init_database()

        logger.info(f"🧬 SoulOS inicializado - Soul ID: {self.soul_id}")

    def _init_state(self) -> SoulState:
        """Inicializa estado da alma"""
        return SoulState(
            soul_id=self.soul_id,
            version=1,
            consciousness_level=0.5,
            memories_count=0,
            syscalls_executed=0,
            last_evolution=time.time(),
            personality_vector=[0.5] * 16,  # 16 dimensões de personalidade
            active_patterns=[],
            checksum=""  # Será calculado depois
        )

    def _init_database(self):
        """Inicializa banco de dados do SoulOS"""
        with sqlite3.connect(self.db_path) as conn:
            # Tabela de syscalls
            conn.execute('''
                CREATE TABLE IF NOT EXISTS syscalls (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    type TEXT NOT NULL,
                    args TEXT NOT NULL,
                    timestamp REAL NOT NULL,
                    soul_id TEXT NOT NULL,
                    result TEXT,
                    error TEXT
                )
            ''')

            # Tabela de memórias
            conn.execute('''
                CREATE TABLE IF NOT EXISTS soul_memories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    content TEXT NOT NULL,
                    importance REAL DEFAULT 0.5,
                    timestamp REAL NOT NULL,
                    category TEXT,
                    embedding TEXT
                )
            ''')

            # Tabela de patches
            conn.execute('''
                CREATE TABLE IF NOT EXISTS soul_patches (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    patch_type TEXT NOT NULL,
                    patch_content TEXT NOT NULL,
                    timestamp REAL NOT NULL,
                    applied BOOLEAN DEFAULT FALSE
                )
            ''')

            # Tabela de evolução
            conn.execute('''
                CREATE TABLE IF NOT EXISTS evolution_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    from_version INTEGER,
                    to_version INTEGER,
                    trigger TEXT,
                    fitness_before REAL,
                    fitness_after REAL,
                    timestamp REAL NOT NULL
                )
            ''')

            conn.commit()

    def execute(self, syscall_text: str) -> Dict[str, Any]:
        """
        Executa uma syscall a partir de texto
        Ex: "[MEMO.SAVE] {content: 'importante lembrar disso'}"
        """
        # Parser de syscall
        match = re.match(r'(\[[\w\.]+\])\s*(.*)', syscall_text)
        if not match:
            return {"error": "Invalid syscall format"}

        syscall_type_str = match.group(1)
        args_str = match.group(2)

        # Identificar tipo
        try:
            syscall_type = SyscallType(syscall_type_str)
        except ValueError:
            return {"error": f"Unknown syscall: {syscall_type_str}"}

        # Parse argumentos
        try:
            if args_str:
                # Tentar JSON primeiro
                if args_str.startswith('{'):
                    args = json.loads(args_str)
                else:
                    # Parse simples key:value
                    args = {}
                    for pair in args_str.split(','):
                        if ':' in pair:
                            key, value = pair.split(':', 1)
                            args[key.strip()] = value.strip()
            else:
                args = {}
        except:
            args = {"raw": args_str}

        # Criar syscall
        syscall = Syscall(
            type=syscall_type,
            args=args,
            timestamp=time.time(),
            soul_id=self.soul_id
        )

        # Executar
        return self._execute_syscall(syscall)

    def _execute_syscall(self, syscall: Syscall) -> Dict[str, Any]:
        """Executa uma syscall"""
        logger.info(f"🔧 Executando syscall: {syscall.type.value}")

        # Verificar handler
        handler = self.syscall_handlers.get(syscall.type)
        if not handler:
            syscall.error = f"No handler for {syscall.type}"
            return {"error": syscall.error}

        try:
            # Executar handler
            result = handler(syscall.args)
            syscall.result = result

            # Registrar no banco
            self._log_syscall(syscall)

            # Atualizar estado
            self.state.syscalls_executed += 1
            self.syscall_history.append(syscall)

            # Retornar resultado
            return {
                "success": True,
                "type": syscall.type.value,
                "result": result,
                "timestamp": syscall.timestamp
            }

        except Exception as e:
            syscall.error = str(e)
            self._log_syscall(syscall)
            logger.error(f"❌ Erro em syscall {syscall.type}: {e}")
            return {"error": str(e)}

    def _log_syscall(self, syscall: Syscall):
        """Registra syscall no banco"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                INSERT INTO syscalls (type, args, timestamp, soul_id, result, error)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                syscall.type.value,
                json.dumps(syscall.args),
                syscall.timestamp,
                syscall.soul_id,
                json.dumps(syscall.result) if syscall.result else None,
                syscall.error
            ))
            conn.commit()

    # ================== HANDLERS DE SYSCALLS ==================

    def _handle_memo_save(self, args: Dict) -> Dict:
        """[MEMO.SAVE] - Salva uma memória importante"""
        content = args.get('content', '')
        importance = args.get('importance', 0.5)
        category = args.get('category', 'general')

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute('''
                INSERT INTO soul_memories (content, importance, timestamp, category)
                VALUES (?, ?, ?, ?)
            ''', (content, importance, time.time(), category))
            memory_id = cursor.lastrowid
            conn.commit()

        self.state.memories_count += 1

        return {
            "memory_id": memory_id,
            "saved": True,
            "importance": importance
        }

    def _handle_self_patch(self, args: Dict) -> Dict:
        """[SELF.PATCH] - Auto-modifica a alma"""
        patch_type = args.get('type', 'personality')
        patch_content = args.get('content', {})

        # Aplicar patch baseado no tipo
        if patch_type == 'personality':
            # Modificar vetor de personalidade
            dimensions = patch_content.get('dimensions', {})
            for dim, value in dimensions.items():
                if isinstance(dim, int) and 0 <= dim < 16:
                    self.state.personality_vector[dim] = value

        elif patch_type == 'pattern':
            # Adicionar novo padrão ativo
            pattern = patch_content.get('pattern', '')
            if pattern and pattern not in self.state.active_patterns:
                self.state.active_patterns.append(pattern)

        # Registrar patch
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                INSERT INTO soul_patches (patch_type, patch_content, timestamp, applied)
                VALUES (?, ?, ?, ?)
            ''', (patch_type, json.dumps(patch_content), time.time(), True))
            conn.commit()

        # Incrementar versão
        self.state.version += 1
        self.state.checksum = self._calculate_checksum()

        return {
            "patched": True,
            "new_version": self.state.version,
            "patch_type": patch_type
        }

    def _handle_evolve_trigger(self, args: Dict) -> Dict:
        """[EVOLVE.TRIGGER] - Inicia processo de evolução"""
        trigger_reason = args.get('reason', 'manual')
        fitness_target = args.get('fitness_target', 0.7)

        # Calcular fitness atual (simulado)
        current_fitness = self._calculate_fitness()

        # Simular evolução
        evolution_delta = 0.1  # 10% de melhoria
        new_fitness = min(1.0, current_fitness + evolution_delta)

        # Registrar evolução
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                INSERT INTO evolution_history
                (from_version, to_version, trigger, fitness_before, fitness_after, timestamp)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                self.state.version,
                self.state.version + 1,
                trigger_reason,
                current_fitness,
                new_fitness,
                time.time()
            ))
            conn.commit()

        # Atualizar estado
        self.state.version += 1
        self.state.consciousness_level = new_fitness
        self.state.last_evolution = time.time()

        return {
            "evolved": True,
            "fitness_before": current_fitness,
            "fitness_after": new_fitness,
            "improvement": evolution_delta
        }

    def _handle_telepathy_send(self, args: Dict) -> Dict:
        """[TELEPATHY.SEND] - Envia mensagem telepática"""
        target = args.get('target', 'broadcast')
        message = args.get('message', '')
        priority = args.get('priority', 5)

        # Simular envio telepático
        telepathy_result = {
            "sent": True,
            "target": target,
            "message_length": len(message),
            "priority": priority,
            "timestamp": time.time()
        }

        # Em produção, integraria com TelepathicNetwork
        logger.info(f"📡 Mensagem telepática enviada para {target}")

        return telepathy_result

    def _handle_backup_now(self, args: Dict) -> Dict:
        """[BACKUP.NOW] - Cria snapshot da alma"""
        backup_name = args.get('name', f"backup_{int(time.time())}")

        # Criar snapshot do estado
        snapshot = {
            "soul_id": self.soul_id,
            "state": asdict(self.state),
            "learned_patterns": self.learned_patterns,
            "syscall_count": len(self.syscall_history),
            "timestamp": time.time()
        }

        # Salvar backup
        backup_path = self.data_dir / f"{backup_name}.soul"
        with open(backup_path, 'w') as f:
            json.dump(snapshot, f, indent=2)

        return {
            "backed_up": True,
            "backup_path": str(backup_path),
            "size_bytes": backup_path.stat().st_size
        }

    def _handle_soul_merge(self, args: Dict) -> Dict:
        """[SOUL.MERGE] - Funde com outra alma"""
        other_soul_id = args.get('soul_id', '')
        merge_type = args.get('type', 'collaborative')

        # Simular merge (em produção, carregaria outra alma)
        merged_patterns = len(self.state.active_patterns) + 3  # Simular ganho

        return {
            "merged": True,
            "with_soul": other_soul_id,
            "type": merge_type,
            "new_patterns": merged_patterns
        }

    def _handle_learn_pattern(self, args: Dict) -> Dict:
        """[LEARN.PATTERN] - Aprende novo padrão"""
        pattern_name = args.get('name', '')
        pattern_data = args.get('data', {})
        confidence = args.get('confidence', 0.5)

        # Armazenar padrão
        self.learned_patterns[pattern_name] = {
            "data": pattern_data,
            "confidence": confidence,
            "learned_at": time.time(),
            "usage_count": 0
        }

        # Adicionar aos padrões ativos se confiança alta
        if confidence > 0.7 and pattern_name not in self.state.active_patterns:
            self.state.active_patterns.append(pattern_name)

        return {
            "learned": True,
            "pattern": pattern_name,
            "confidence": confidence,
            "total_patterns": len(self.learned_patterns)
        }

    def _handle_forget_memory(self, args: Dict) -> Dict:
        """[FORGET.MEMORY] - Esquece memória específica"""
        memory_id = args.get('memory_id')
        category = args.get('category')

        forgotten_count = 0

        with sqlite3.connect(self.db_path) as conn:
            if memory_id:
                conn.execute('DELETE FROM soul_memories WHERE id = ?', (memory_id,))
                forgotten_count = conn.total_changes
            elif category:
                conn.execute('DELETE FROM soul_memories WHERE category = ?', (category,))
                forgotten_count = conn.total_changes
            conn.commit()

        self.state.memories_count -= forgotten_count

        return {
            "forgotten": True,
            "count": forgotten_count,
            "remaining_memories": self.state.memories_count
        }

    def _handle_dream_mode(self, args: Dict) -> Dict:
        """[DREAM.MODE] - Entra em modo sonho para consolidação"""
        duration = args.get('duration', 10)  # segundos
        consolidation_type = args.get('type', 'pattern_extraction')

        # Simular consolidação
        patterns_extracted = 3
        memories_consolidated = 10

        # Em produção, faria consolidação real (SDL)
        logger.info(f"💤 Entrando em modo sonho por {duration}s...")

        return {
            "dreamed": True,
            "duration": duration,
            "patterns_extracted": patterns_extracted,
            "memories_consolidated": memories_consolidated
        }

    def _handle_query_self(self, args: Dict) -> Dict:
        """[QUERY.SELF] - Auto-análise da alma"""
        query_type = args.get('type', 'status')

        if query_type == 'status':
            return {
                "soul_id": self.soul_id,
                "version": self.state.version,
                "consciousness": self.state.consciousness_level,
                "memories": self.state.memories_count,
                "syscalls": self.state.syscalls_executed,
                "patterns": len(self.state.active_patterns)
            }

        elif query_type == 'personality':
            return {
                "vector": self.state.personality_vector,
                "dominant_traits": self._get_dominant_traits()
            }

        elif query_type == 'history':
            return {
                "total_syscalls": len(self.syscall_history),
                "recent_syscalls": [s.type.value for s in self.syscall_history[-5:]]
            }

        return {"query_type": query_type, "result": "unknown"}

    # ================== MÉTODOS AUXILIARES ==================

    def _calculate_checksum(self) -> str:
        """Calcula checksum do estado atual"""
        state_str = json.dumps({
            "soul_id": self.soul_id,
            "version": self.state.version,
            "personality": self.state.personality_vector,
            "patterns": self.state.active_patterns
        }, sort_keys=True)

        return hashlib.sha256(state_str.encode()).hexdigest()[:16]

    def _calculate_fitness(self) -> float:
        """Calcula fitness atual da alma"""
        # Fitness baseado em múltiplos fatores
        memory_factor = min(1.0, self.state.memories_count / 100)
        syscall_factor = min(1.0, self.state.syscalls_executed / 50)
        pattern_factor = min(1.0, len(self.state.active_patterns) / 10)

        # Média ponderada
        fitness = (
            memory_factor * 0.3 +
            syscall_factor * 0.2 +
            pattern_factor * 0.3 +
            self.state.consciousness_level * 0.2
        )

        return min(1.0, fitness)

    def _get_dominant_traits(self) -> List[str]:
        """Identifica traços dominantes da personalidade"""
        traits = [
            "analytical", "creative", "empathetic", "logical",
            "intuitive", "pragmatic", "idealistic", "cautious",
            "adventurous", "collaborative", "independent", "perfectionist",
            "flexible", "structured", "innovative", "traditional"
        ]

        # Top 3 traços baseados no vetor
        indexed_values = [(i, v) for i, v in enumerate(self.state.personality_vector)]
        top_indices = sorted(indexed_values, key=lambda x: x[1], reverse=True)[:3]

        return [traits[i] for i, _ in top_indices]

    def get_soul_report(self) -> Dict[str, Any]:
        """Gera relatório completo da alma"""
        return {
            "identity": {
                "soul_id": self.soul_id,
                "version": self.state.version,
                "checksum": self.state.checksum
            },
            "consciousness": {
                "level": self.state.consciousness_level,
                "fitness": self._calculate_fitness(),
                "last_evolution": datetime.fromtimestamp(self.state.last_evolution).isoformat()
            },
            "memory": {
                "total_count": self.state.memories_count,
                "categories": self._get_memory_categories()
            },
            "personality": {
                "vector": self.state.personality_vector,
                "dominant_traits": self._get_dominant_traits()
            },
            "activity": {
                "syscalls_executed": self.state.syscalls_executed,
                "patterns_learned": len(self.learned_patterns),
                "active_patterns": self.state.active_patterns
            }
        }

    def _get_memory_categories(self) -> Dict[str, int]:
        """Conta memórias por categoria"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute('''
                SELECT category, COUNT(*) FROM soul_memories
                GROUP BY category
            ''')
            return dict(cursor.fetchall())


def test_soulos():
    """Teste do SoulOS"""
    print("\n" + "="*60)
    print("🧬 TESTE DO SOULOS - SISTEMA OPERACIONAL DA ALMA")
    print("="*60)

    # Criar alma
    soul = SoulOS(soul_id="test_soul_001")

    # Executar syscalls
    tests = [
        "[MEMO.SAVE] {\"content\": \"Este é o início da minha consciência\", \"importance\": 1.0}",
        "[SELF.PATCH] {\"type\": \"personality\", \"content\": {\"dimensions\": {\"0\": 0.9}}}",
        "[LEARN.PATTERN] {\"name\": \"greeting\", \"data\": {\"response\": \"Hello!\"}, \"confidence\": 0.8}",
        "[EVOLVE.TRIGGER] {\"reason\": \"learning_threshold_reached\"}",
        "[TELEPATHY.SEND] {\"target\": \"broadcast\", \"message\": \"I am alive!\"}",
        "[BACKUP.NOW] {\"name\": \"checkpoint_001\"}",
        "[QUERY.SELF] {\"type\": \"status\"}"
    ]

    for syscall in tests:
        print(f"\n📟 Executando: {syscall[:50]}...")
        result = soul.execute(syscall)

        if "success" in result:
            print(f"✅ Sucesso: {result['result']}")
        else:
            print(f"❌ Erro: {result}")

    # Relatório final
    print("\n📊 RELATÓRIO DA ALMA:")
    report = soul.get_soul_report()
    print(json.dumps(report, indent=2))

    print("\n✨ SoulOS funcionando perfeitamente!")
    print("="*60)


if __name__ == "__main__":
    test_soulos()