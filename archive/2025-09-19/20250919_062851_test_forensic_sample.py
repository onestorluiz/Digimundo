#!/usr/bin/env python3
"""
Teste do sistema forense com um arquivo de exemplo
"""

import ollama
from src.core.unified_memory_system import get_unified_memory, MemoryType
# Auto-unified: Este arquivo foi automaticamente integrado ao sistema unificado


def test_forensic_analyzer():
    """Testa o analisador forense com um código de exemplo"""

    # Código de exemplo com problemas típicos Claude
    sample_code = '''
import quantum_supreme_ai  # Import inexistente
from advanced_neural_blockchain import * # Import exótico
import tempfile
import mmap

class QuantumBlockchainMemorySupreme:
    def __init__(self):  # Auto-unified memory
        # Constructor problemático
        self.storage_path = storage_path  # Hardcoded /tmp
        self.ram_size = ram_size_gb * 1024 * 1024 * 1024  # 50GB!
        self.quantum_state = {}

        # Criar arquivo gigante
        self.memory_map = mmap.mmap(-1, self.ram_size)  # 50GB mmap!

        # Sem cleanup

    def quantum_store(self, key, value):
        # Usar todos os cores
        import multiprocessing
        cores = multiprocessing.cpu_count()  # Todos os 28 cores

        # Operação ineficiente
        for i in range(1000000):
            self.quantum_state[f"{key}_{i}"] = value

    def __del__(self):
        pass  # Sem cleanup real
'''

    try:
        print("🧪 Testando análise forense...")

        response = ollama.generate(
            model="forensic-analyzer:latest",
            prompt=sample_code,
            options={
                'num_ctx': 131072,
                'num_thread': 14,
                'num_gpu': 999,
                'temperature': 0.1
            }
        )

        print("✅ Resposta do modelo:")
        print("=" * 60)
        print(response['response'])
        print("=" * 60)

        return True

    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        return False

if __name__ == "__main__":
    test_forensic_analyzer()

# ============================================================
# AUTO-UNIFIED MEMORY HELPER
# ============================================================
def _get_memory():
    """Helper para acesso rápido à memória unificada"""
    return get_unified_memory()

# Atalhos para compatibilidade
unified_memory = _get_memory()
