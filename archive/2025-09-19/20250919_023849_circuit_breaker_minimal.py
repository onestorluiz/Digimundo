#!/usr/bin/env python3
"""
Circuit Breaker Minimal - Padrão de resiliência simplificado
Refatorado das 5 perguntas: 400+ → 120 linhas

RESPOSTAS ÀS 5 PERGUNTAS:
1. É necessário? SIM - Circuit breaker previne falhas em cascata
2. O que faz? Protege serviços contra falhas repetidas
3. Quantas linhas? 120 vs 400+ (70% redução)
4. Dependências? Apenas stdlib
5. Uma função? Não, mas muito simplificado
"""

import time
from enum import Enum
from typing import Any, Callable, Optional
from functools import wraps
import threading

class State(Enum):
    """Estados do circuit breaker"""
    CLOSED = 'closed'      # Normal - permite chamadas
    OPEN = 'open'          # Falhou muito - bloqueia chamadas
    HALF_OPEN = 'half_open' # Testando recuperação

class CircuitBreakerMinimal:
    """Circuit breaker minimalista mas funcional"""

    def __init__(self, failure_threshold: int = 5,
                 recovery_timeout: int = 60,
                 success_threshold: int = 2):
        """
        Args:
            failure_threshold: Falhas para abrir circuito
            recovery_timeout: Segundos para tentar recuperação
            success_threshold: Sucessos para fechar circuito
        """
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.success_threshold = success_threshold

        self.state = State.CLOSED
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time = None
        self._lock = threading.Lock()

    def call(self, func: Callable, *args, **kwargs) -> Any:
        """Executa função protegida pelo circuit breaker"""

        with self._lock:
            # Se está aberto, verifica se pode tentar recuperar
            if self.state == State.OPEN:
                if self._can_attempt_reset():
                    self.state = State.HALF_OPEN
                    self.success_count = 0
                else:
                    raise Exception(f"Circuit OPEN - Service unavailable")

        # Tenta executar
        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result

        except Exception as e:
            self._on_failure()
            raise e

    def _can_attempt_reset(self) -> bool:
        """Verifica se passou tempo suficiente para tentar reset"""
        if not self.last_failure_time:
            return False
        return (time.time() - self.last_failure_time) >= self.recovery_timeout

    def _on_success(self):
        """Registra sucesso"""
        with self._lock:
            if self.state == State.HALF_OPEN:
                self.success_count += 1
                if self.success_count >= self.success_threshold:
                    # Recuperou! Fecha circuito
                    self.state = State.CLOSED
                    self.failure_count = 0
                    self.success_count = 0

            elif self.state == State.CLOSED:
                # Reset contador de falhas em caso de sucesso
                self.failure_count = 0

    def _on_failure(self):
        """Registra falha"""
        with self._lock:
            self.failure_count += 1
            self.last_failure_time = time.time()

            if self.state == State.HALF_OPEN:
                # Falhou durante recuperação - abre novamente
                self.state = State.OPEN

            elif self.state == State.CLOSED:
                if self.failure_count >= self.failure_threshold:
                    # Muitas falhas - abre circuito
                    self.state = State.OPEN

    def get_state(self) -> str:
        """Retorna estado atual"""
        return self.state.value

    def reset(self):
        """Reset manual do circuit breaker"""
        with self._lock:
            self.state = State.CLOSED
            self.failure_count = 0
            self.success_count = 0
            self.last_failure_time = None

# Decorator para usar circuit breaker
def with_circuit_breaker(breaker: CircuitBreakerMinimal):
    """Decorator para proteger funções com circuit breaker"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return breaker.call(func, *args, **kwargs)
        return wrapper
    return decorator

# Exemplo de uso
if __name__ == "__main__":
    print("🛡️ Testando Circuit Breaker Minimal...")

    breaker = CircuitBreakerMinimal(failure_threshold=3)

    # Simula serviço que falha
    failure_count = 0
    def unreliable_service():
        global failure_count
        failure_count += 1
        if failure_count <= 3:
            raise Exception("Service failed")
        return "Success!"

    # Testa circuit breaker
    for i in range(6):
        try:
            result = breaker.call(unreliable_service)
            print(f"✅ Tentativa {i+1}: {result}")
        except Exception as e:
            print(f"❌ Tentativa {i+1}: {e}")
        print(f"   Estado: {breaker.get_state()}")

    print("\nDIGIMUNDO PRESENTE 🥷")