"""
Context Manager - Gestão avançada de contexto para chat
Fase 2.A - Implementação com compressão e priorização
"""
import json
import hashlib
from typing import List, Dict, Optional, Tuple, Any
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import re
from apps.scripturemon.bootstrap import get_config

class MessagePriority(Enum):
    """Prioridade de mensagens para retenção"""
    CRITICAL = 5
    HIGH = 4
    NORMAL = 3
    LOW = 2
    EPHEMERAL = 1

class CompressionStrategy(Enum):
    """Estratégias de compressão de contexto"""
    SUMMARIZE = 'summarize'
    TRUNCATE = 'truncate'
    SELECTIVE = 'selective'
    HYBRID = 'hybrid'

@dataclass
class ContextMessage:
    """Mensagem enriquecida com metadados de contexto"""
    role: str
    content: str
    timestamp: datetime = field(default_factory=datetime.now)
    tokens: int = 0
    priority: MessagePriority = MessagePriority.NORMAL
    embedding: Optional[List[float]] = None
    summary: Optional[str] = None
    keywords: List[str] = field(default_factory=list)
    references: List[str] = field(default_factory=list)
    compressed: bool = False

    def __hash__(self):
        """Hash único baseado em conteúdo e timestamp"""
        content_hash = hashlib.md5(self.content.encode()).hexdigest()
        return hash(f'{content_hash}_{self.timestamp.isoformat()}')

@dataclass
class ContextWindow:
    """Janela de contexto com limites e estatísticas"""
    max_tokens: int = 4096
    current_tokens: int = 0
    messages: List[ContextMessage] = field(default_factory=list)
    compressed_history: List[str] = field(default_factory=list)
    strategy: CompressionStrategy = CompressionStrategy.HYBRID

    @property
    def usage_percent(self) -> float:
        """Percentual de uso do contexto"""
        return self.current_tokens / self.max_tokens * 100

    @property
    def tokens_available(self) -> int:
        """Tokens disponíveis"""
        return self.max_tokens - self.current_tokens

class ContextManager:
    """
    Gerenciador avançado de contexto
    Otimiza uso de tokens e mantém informações relevantes
    """
    IMPORTANT_KEYWORDS = {'comandos': ['/', 'comando', 'executar', 'fazer'], 'insights': ['importante', 'crucial', 'fundamental', 'essencial'], 'referências': ['como disse', 'mencionei', 'anteriormente', 'lembre'], 'definições': ['é', 'significa', 'define-se', 'conceito'], 'perguntas': ['?', 'por que', 'como', 'quando', 'onde']}
    MODEL_LIMITS = {'llama3.2:3b': 8192, 'mistral:instruct': 8192, 'deepseek-r1:7b': 16384, 'llama3.1:8b': 128000, 'default': 4096}

    def __init__(self):
        """Inicializa manager"""
        self.config = get_config()
        self.windows: Dict[str, ContextWindow] = {}
        self.compression_cache: Dict[str, str] = {}
        self.auto_compress = self.config.get('auto_compress', True)
        self.compression_threshold = self.config.get('compression_threshold', 0.8)
        self.min_priority_to_keep = MessagePriority.LOW

    def create_window(self, window_id: str, max_tokens: Optional[int]=None, model: Optional[str]=None) -> ContextWindow:
        """Cria nova janela de contexto"""
        if max_tokens is None:
            if model and model in self.MODEL_LIMITS:
                max_tokens = self.MODEL_LIMITS[model]
            else:
                max_tokens = self.MODEL_LIMITS['default']
        window = ContextWindow(max_tokens=max_tokens, strategy=CompressionStrategy.HYBRID)
        self.windows[window_id] = window
        return window

    def add_message(self, window_id: str, role: str, content: str, priority: Optional[MessagePriority]=None) -> bool:
        """Adiciona mensagem ao contexto"""
        if window_id not in self.windows:
            self.create_window(window_id)
        window = self.windows[window_id]
        tokens = self._estimate_tokens(content)
        if priority is None:
            priority = self._infer_priority(role, content)
        keywords = self._extract_keywords(content)
        message = ContextMessage(role=role, content=content, tokens=tokens, priority=priority, keywords=keywords)
        if window.current_tokens + tokens > window.max_tokens:
            if self.auto_compress:
                self._compress_window(window)
            else:
                return False
        window.messages.append(message)
        window.current_tokens += tokens
        if window.usage_percent > self.compression_threshold * 100:
            self._compress_window(window)
        return True

    def _estimate_tokens(self, text: str) -> int:
        """Estima número de tokens"""
        base_tokens = len(text) / 3.5
        code_blocks = text.count('```')
        if code_blocks > 0:
            base_tokens *= 1.2
        special_chars = len(re.findall('[^\\w\\s]', text))
        base_tokens += special_chars * 0.1
        return int(base_tokens)

    def _infer_priority(self, role: str, content: str) -> MessagePriority:
        """Infere prioridade da mensagem"""
        if role == 'system':
            return MessagePriority.CRITICAL
        if content.startswith('/'):
            return MessagePriority.HIGH
        content_lower = content.lower()
        for category, keywords in self.IMPORTANT_KEYWORDS.items():
            for keyword in keywords:
                if keyword in content_lower:
                    if category in ['comandos', 'insights']:
                        return MessagePriority.HIGH
                    elif category in ['referências', 'definições']:
                        return MessagePriority.NORMAL
        if len(content) < 50:
            return MessagePriority.LOW
        return MessagePriority.NORMAL

    def _extract_keywords(self, content: str) -> List[str]:
        """Extrai palavras-chave do conteúdo"""
        keywords = []
        words = re.findall('\\b\\w+\\b', content.lower())
        important_words = [w for w in words if len(w) > 5]
        from collections import Counter
        word_freq = Counter(important_words)
        keywords = [word for word, _ in word_freq.most_common(5)]
        return keywords

    def _compress_window(self, window: ContextWindow) -> None:
        """Comprime janela de contexto usando estratégia definida"""
        if window.strategy == CompressionStrategy.TRUNCATE:
            self._compress_truncate(window)
        elif window.strategy == CompressionStrategy.SUMMARIZE:
            self._compress_summarize(window)
        elif window.strategy == CompressionStrategy.SELECTIVE:
            self._compress_selective(window)
        else:
            self._compress_hybrid(window)

    def _compress_truncate(self, window: ContextWindow) -> None:
        """Remove mensagens antigas simples"""
        keep_count = 10
        if len(window.messages) > keep_count:
            removed = window.messages[:-keep_count]
            summary = f'[{len(removed)} mensagens antigas removidas]'
            window.compressed_history.append(summary)
            window.messages = window.messages[-keep_count:]
            window.current_tokens = sum((m.tokens for m in window.messages))

    def _compress_summarize(self, window: ContextWindow) -> None:
        """Resume mensagens antigas em um summary"""
        if len(window.messages) > 20:
            old_messages = window.messages[:-10]
            recent_messages = window.messages[-10:]
            summary_parts = []
            for msg in old_messages:
                if msg.priority >= MessagePriority.HIGH:
                    summary_parts.append(f'{msg.role}: {msg.content[:50]}...')
            if summary_parts:
                summary = 'Contexto anterior:\n' + '\n'.join(summary_parts)
                summary_msg = ContextMessage(role='system', content=summary, tokens=self._estimate_tokens(summary), priority=MessagePriority.NORMAL, compressed=True)
                window.messages = [summary_msg] + recent_messages
                window.current_tokens = sum((m.tokens for m in window.messages))

    def _compress_selective(self, window: ContextWindow) -> None:
        """Remove seletivamente por prioridade"""
        critical = []
        high = []
        normal = []
        low = []
        ephemeral = []
        for msg in window.messages:
            if msg.priority == MessagePriority.CRITICAL:
                critical.append(msg)
            elif msg.priority == MessagePriority.HIGH:
                high.append(msg)
            elif msg.priority == MessagePriority.NORMAL:
                normal.append(msg)
            elif msg.priority == MessagePriority.LOW:
                low.append(msg)
            else:
                ephemeral.append(msg)
        target_tokens = int(window.max_tokens * 0.7)
        kept_messages = critical + high
        current = sum((m.tokens for m in kept_messages))
        for msg in normal[-5:]:
            if current + msg.tokens < target_tokens:
                kept_messages.append(msg)
                current += msg.tokens
        for msg in low[-2:]:
            if current + msg.tokens < target_tokens:
                kept_messages.append(msg)
                current += msg.tokens
        kept_messages.sort(key=lambda m: m.timestamp)
        removed_count = len(window.messages) - len(kept_messages)
        if removed_count > 0:
            window.compressed_history.append(f'[{removed_count} mensagens de baixa prioridade removidas]')
        window.messages = kept_messages
        window.current_tokens = current

    def _compress_hybrid(self, window: ContextWindow) -> None:
        """Combina estratégias de compressão"""
        window.messages = [m for m in window.messages if m.priority != MessagePriority.EPHEMERAL]
        if window.current_tokens > window.max_tokens * 0.8:
            self._compress_summarize(window)
        if window.current_tokens > window.max_tokens * 0.9:
            self._compress_selective(window)

    def get_context(self, window_id: str, format_for_llm: bool=True) -> str:
        """Retorna contexto formatado"""
        if window_id not in self.windows:
            return ''
        window = self.windows[window_id]
        if not format_for_llm:
            return json.dumps([{'role': m.role, 'content': m.content, 'priority': m.priority.name, 'tokens': m.tokens} for m in window.messages], indent=2)
        context_parts = []
        if window.compressed_history:
            context_parts.append('Context Summary:')
            context_parts.extend(window.compressed_history[-3:])
            context_parts.append('')
        for msg in window.messages:
            if msg.compressed:
                context_parts.append(f'[Compressed] {msg.content}')
            elif msg.role == 'system':
                context_parts.append(f'System: {msg.content}')
            elif msg.role == 'user':
                context_parts.append(f'User: {msg.content}')
            elif msg.role == 'assistant':
                context_parts.append(f'Assistant: {msg.content}')
        return '\n\n'.join(context_parts)

    def calculate_tokens(self, text: str) -> int:
        """Calcula tokens de um texto"""
        return self._estimate_tokens(text)

    def prune_old_messages(self, window_id: str, max_age: Optional[timedelta]=None, keep_last: int=5) -> int:
        """Remove mensagens antigas por idade"""
        if window_id not in self.windows:
            return 0
        window = self.windows[window_id]
        if max_age is None:
            max_age = timedelta(hours=24)
        cutoff_time = datetime.now() - max_age
        old_messages = []
        kept_messages = []
        for msg in window.messages:
            if msg.timestamp < cutoff_time and msg.priority < MessagePriority.HIGH:
                old_messages.append(msg)
            else:
                kept_messages.append(msg)
        if len(kept_messages) < keep_last:
            kept_messages = window.messages[-keep_last:]
        removed_count = len(window.messages) - len(kept_messages)
        if removed_count > 0:
            window.messages = kept_messages
            window.current_tokens = sum((m.tokens for m in kept_messages))
            window.compressed_history.append(f'[{removed_count} mensagens antigas removidas após {max_age}]')
        return removed_count

    def get_statistics(self, window_id: str) -> Dict[str, Any]:
        """Retorna estatísticas da janela"""
        if window_id not in self.windows:
            return {'error': 'Window not found'}
        window = self.windows[window_id]
        priority_counts = {}
        for priority in MessagePriority:
            priority_counts[priority.name] = sum((1 for m in window.messages if m.priority == priority))
        role_counts = {}
        for msg in window.messages:
            role_counts[msg.role] = role_counts.get(msg.role, 0) + 1
        return {'window_id': window_id, 'max_tokens': window.max_tokens, 'current_tokens': window.current_tokens, 'usage_percent': round(window.usage_percent, 2), 'tokens_available': window.tokens_available, 'total_messages': len(window.messages), 'compressed_history_count': len(window.compressed_history), 'strategy': window.strategy.value, 'priority_distribution': priority_counts, 'role_distribution': role_counts, 'oldest_message': window.messages[0].timestamp.isoformat() if window.messages else None, 'newest_message': window.messages[-1].timestamp.isoformat() if window.messages else None}

    def optimize_for_model(self, window_id: str, model_name: str) -> None:
        """Otimiza janela para modelo específico"""
        if window_id not in self.windows:
            return
        window = self.windows[window_id]
        if model_name in self.MODEL_LIMITS:
            window.max_tokens = self.MODEL_LIMITS[model_name]
        if window.max_tokens > 16384:
            window.strategy = CompressionStrategy.SELECTIVE
        elif window.max_tokens > 8192:
            window.strategy = CompressionStrategy.HYBRID
        else:
            window.strategy = CompressionStrategy.SUMMARIZE
        if window.current_tokens > window.max_tokens:
            self._compress_window(window)
_manager_instance: Optional[ContextManager] = None

def get_context_manager() -> ContextManager:
    """Retorna instância singleton"""
    global _manager_instance
    if _manager_instance is None:
        _manager_instance = ContextManager()
    return _manager_instance
__all__ = ['ContextManager', 'ContextWindow', 'ContextMessage', 'MessagePriority', 'CompressionStrategy', 'get_context_manager']