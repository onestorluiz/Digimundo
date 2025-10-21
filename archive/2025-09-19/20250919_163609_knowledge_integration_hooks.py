#!/usr/bin/env python3
"""
🧠 KNOWLEDGE INTEGRATION HOOKS
==============================
Garante que TODO conhecimento novo seja automaticamente
integrado no Unified Memory System.
"""

import functools
import inspect
from typing import Any, Callable
from pathlib import Path
import json
import hashlib
from datetime import datetime

from .unified_memory_system import get_unified_memory, MemoryType


class KnowledgeIntegrator:
    """
    Intercepta e integra automaticamente todo conhecimento
    """

    def __init__(self):
        self.memory = get_unified_memory()
        self.integration_count = 0

    def capture_analysis(self, func: Callable) -> Callable:
        """Decorator para capturar resultados de análises"""
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)

            # Se o resultado contém informação útil, salvar
            if result and isinstance(result, (dict, list, str)):
                self.store_knowledge(
                    source=func.__name__,
                    content=result,
                    knowledge_type="analysis"
                )

            return result
        return wrapper

    def capture_learning(self, func: Callable) -> Callable:
        """Decorator para capturar aprendizado de ML"""
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)

            # Capturar conceitos aprendidos
            if result and "concepts" in str(result).lower():
                self.store_knowledge(
                    source=f"ml_{func.__name__}",
                    content=result,
                    knowledge_type="learning"
                )

            return result
        return wrapper

    def capture_screenplay_processing(self, func: Callable) -> Callable:
        """Decorator para capturar processamento de roteiros"""
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Capturar nome do arquivo sendo processado
            file_info = None
            for arg in args:
                if isinstance(arg, (str, Path)) and str(arg).endswith(('.txt', '.pdf')):
                    file_info = str(arg)
                    break

            result = func(*args, **kwargs)

            # Salvar resultado com contexto
            if result and file_info:
                self.store_knowledge(
                    source="screenplay_processor",
                    content={
                        'file': file_info,
                        'result': result,
                        'timestamp': datetime.now().isoformat()
                    },
                    knowledge_type="screenplay"
                )

            return result
        return wrapper

    def store_knowledge(self, source: str, content: Any, knowledge_type: str):
        """Armazena conhecimento no sistema unificado"""
        try:
            # Gerar ID único
            content_str = json.dumps(content) if not isinstance(content, str) else content
            knowledge_id = hashlib.md5(f"{source}_{content_str}_{datetime.now()}".encode()).hexdigest()[:12]

            # Determinar tipo de memória
            memory_type = MemoryType.KNOWLEDGE
            if knowledge_type == "analysis":
                memory_type = MemoryType.ANALYSIS
            elif knowledge_type == "screenplay":
                memory_type = MemoryType.SCREENPLAY

            # Armazenar
            self.memory.store(
                memory_type=memory_type,
                key=f"auto_{knowledge_type}_{knowledge_id}",
                value=content,
                metadata={
                    'source': source,
                    'auto_captured': True,
                    'capture_time': datetime.now().isoformat(),
                    'integration_type': knowledge_type
                },
                confidence=0.95,
                source=f"knowledge_hook_{source}"
            )

            self.integration_count += 1

            # Log discreto
            if self.integration_count % 10 == 0:
                print(f"💾 {self.integration_count} conhecimentos integrados automaticamente")

        except Exception as e:
            # Falha silenciosa para não quebrar fluxo
            pass

    def apply_to_module(self, module):
        """Aplica hooks em todas as funções de um módulo"""
        for name, obj in inspect.getmembers(module):
            if inspect.isfunction(obj):
                # Aplicar decorator apropriado baseado no nome
                if any(keyword in name.lower() for keyword in ['analyze', 'evaluate', 'assess']):
                    setattr(module, name, self.capture_analysis(obj))
                elif any(keyword in name.lower() for keyword in ['learn', 'train', 'extract']):
                    setattr(module, name, self.capture_learning(obj))
                elif any(keyword in name.lower() for keyword in ['screenplay', 'script', 'read']):
                    setattr(module, name, self.capture_screenplay_processing(obj))


# Instância global
knowledge_integrator = KnowledgeIntegrator()


def auto_integrate_knowledge(cls):
    """
    Class decorator para integração automática de conhecimento

    Usage:
        @auto_integrate_knowledge
        class MyAnalyzer:
            ...
    """
    # Aplicar hooks em todos os métodos
    for name, method in inspect.getmembers(cls, predicate=inspect.ismethod):
        if not name.startswith('_'):  # Ignorar métodos privados
            if 'analyze' in name.lower():
                setattr(cls, name, knowledge_integrator.capture_analysis(method))
            elif 'learn' in name.lower():
                setattr(cls, name, knowledge_integrator.capture_learning(method))

    return cls


def ensure_knowledge_persistence():
    """
    Garante que conhecimento seja persistido mesmo em caso de erro
    """
    import atexit

    def save_on_exit():
        memory = get_unified_memory()
        stats = memory.get_stats()
        print(f"\n💾 Sistema finalizando: {stats['total_entries']} conhecimentos salvos")

    atexit.register(save_on_exit)


# Ativar persistência automática
ensure_knowledge_persistence()
