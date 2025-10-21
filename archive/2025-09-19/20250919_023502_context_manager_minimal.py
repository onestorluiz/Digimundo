#!/usr/bin/env python3
"""
Context Manager Minimal - Gestão eficiente de contexto
Refatorado das 5 perguntas: 400+ → 150 linhas

RESPOSTAS ÀS 5 PERGUNTAS:
1. É necessário? SIM - Gestão de contexto é essencial
2. O que faz? Gerencia janelas de contexto com compressão
3. Quantas linhas? 150 vs 400+ (62% redução)
4. Dependências? Apenas stdlib
5. Uma função? Não, mas simplificado ao essencial
"""

import json
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

class Priority(Enum):
    """Prioridade de mensagens"""
    HIGH = 3
    NORMAL = 2
    LOW = 1

@dataclass
class Message:
    """Mensagem com metadados"""
    role: str
    content: str
    tokens: int = 0
    priority: Priority = Priority.NORMAL

def estimate_tokens(text: str) -> int:
    """Estima tokens (aproximação: ~4 chars = 1 token)"""
    return len(text) // 4

class ContextManager:
    """Gerenciador minimalista de contexto"""

    # Limites de tokens por modelo
    MODEL_LIMITS = {
        'llama3.2:3b': 8192,
        'mistral': 8192,
        'deepseek-r1:7b': 16384,
        'llama3.1:8b': 128000,
        'default': 4096
    }

    def __init__(self, model: str = 'default', compression_threshold: float = 0.8):
        self.model = model
        self.max_tokens = self.MODEL_LIMITS.get(model, self.MODEL_LIMITS['default'])
        self.compression_threshold = compression_threshold
        self.messages: List[Message] = []
        self.current_tokens = 0

    def add_message(self, role: str, content: str, priority: Priority = Priority.NORMAL) -> bool:
        """Adiciona mensagem ao contexto"""
        tokens = estimate_tokens(content)

        # Verifica se precisa comprimir
        if self.current_tokens + tokens > self.max_tokens * self.compression_threshold:
            self.compress()

        # Se ainda não cabe, remove mensagens de baixa prioridade
        while self.current_tokens + tokens > self.max_tokens and self.messages:
            # Remove mensagem mais antiga de menor prioridade
            min_priority_idx = min(
                range(len(self.messages)),
                key=lambda i: (self.messages[i].priority.value, -i)
            )
            removed = self.messages.pop(min_priority_idx)
            self.current_tokens -= removed.tokens

        # Adiciona nova mensagem
        msg = Message(role, content, tokens, priority)
        self.messages.append(msg)
        self.current_tokens += tokens

        return True

    def compress(self) -> int:
        """Comprime contexto removendo redundâncias"""
        if not self.messages:
            return 0

        original_tokens = self.current_tokens

        # Remove mensagens LOW priority antigas (mantém só últimas 2)
        low_msgs = [(i, m) for i, m in enumerate(self.messages)
                   if m.priority == Priority.LOW]
        if len(low_msgs) > 2:
            for i, _ in low_msgs[:-2]:
                if i < len(self.messages):
                    self.current_tokens -= self.messages[i].tokens
                    self.messages[i] = None
            self.messages = [m for m in self.messages if m is not None]

        # Resumir mensagens NORMAL antigas
        if len(self.messages) > 10:
            # Mantém primeiras 2 e últimas 5 mensagens
            middle = self.messages[2:-5]
            if middle:
                summary = self._summarize_messages(middle)
                summary_msg = Message(
                    'system',
                    f"[Resumo de {len(middle)} mensagens]: {summary}",
                    estimate_tokens(summary),
                    Priority.NORMAL
                )
                self.messages = self.messages[:2] + [summary_msg] + self.messages[-5:]

                # Recalcula tokens
                self.current_tokens = sum(m.tokens for m in self.messages)

        return original_tokens - self.current_tokens

    def _summarize_messages(self, messages: List[Message]) -> str:
        """Cria resumo simples de mensagens"""
        # Extrai principais palavras-chave
        keywords = set()
        for msg in messages:
            # Palavras importantes (capitalizadas ou longas)
            words = msg.content.split()
            keywords.update(w for w in words
                          if w[0].isupper() or len(w) > 10)

        return f"Discussão sobre: {', '.join(list(keywords)[:10])}"

    def get_context(self) -> List[Dict[str, str]]:
        """Retorna contexto formatado para API"""
        return [
            {'role': msg.role, 'content': msg.content}
            for msg in self.messages
        ]

    def get_stats(self) -> Dict[str, any]:
        """Estatísticas do contexto"""
        return {
            'messages': len(self.messages),
            'current_tokens': self.current_tokens,
            'max_tokens': self.max_tokens,
            'usage_percent': (self.current_tokens / self.max_tokens) * 100,
            'available_tokens': self.max_tokens - self.current_tokens
        }

# Exemplo de uso
if __name__ == "__main__":
    print("🎯 Testando Context Manager Minimal...")

    manager = ContextManager('llama3.2:3b')

    # Adiciona mensagens
    manager.add_message('user', 'Como fazer um bom roteiro?', Priority.HIGH)
    manager.add_message('assistant', 'Um bom roteiro tem estrutura...', Priority.NORMAL)
    manager.add_message('user', 'E sobre personagens?', Priority.HIGH)

    # Stats
    stats = manager.get_stats()
    print(f"✅ Mensagens: {stats['messages']}")
    print(f"✅ Tokens: {stats['current_tokens']}/{stats['max_tokens']}")
    print(f"✅ Uso: {stats['usage_percent']:.1f}%")

    print("\nDIGIMUNDO PRESENTE 🥷")