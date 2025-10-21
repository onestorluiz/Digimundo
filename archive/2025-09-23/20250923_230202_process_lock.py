#!/usr/bin/env python3
"""
Sistema de Lock para prevenir múltiplas instâncias
DIGIMUNDO STYLE - Minimalista e eficaz
"""

import os
import sys
import time
import fcntl
from pathlib import Path

class ProcessLock:
    """Lock simples usando arquivo."""

    def __init__(self, name="scripturemon"):
        self.lock_file = Path(f"/tmp/{name}.lock")
        self.lock_handle = None

    def acquire(self, timeout=5):
        """Tenta adquirir lock."""
        start = time.time()

        while time.time() - start < timeout:
            try:
                self.lock_handle = open(self.lock_file, 'w')
                fcntl.lockf(self.lock_handle, fcntl.LOCK_EX | fcntl.LOCK_NB)

                # Escreve PID no arquivo
                self.lock_handle.write(str(os.getpid()))
                self.lock_handle.flush()
                return True

            except IOError:
                # Lock já existe
                if self.check_stale():
                    # Remove lock antigo
                    self.release()
                    continue

                time.sleep(0.1)

        return False

    def check_stale(self):
        """Verifica se lock é de processo morto."""
        try:
            if self.lock_file.exists():
                with open(self.lock_file, 'r') as f:
                    pid = int(f.read().strip())

                # Verifica se processo existe
                try:
                    os.kill(pid, 0)
                    return False  # Processo ainda vivo
                except OSError:
                    return True   # Processo morto
        except:
            return True

        return False

    def release(self):
        """Libera lock."""
        if self.lock_handle:
            try:
                fcntl.lockf(self.lock_handle, fcntl.LOCK_UN)
                self.lock_handle.close()
            except:
                pass

        try:
            self.lock_file.unlink()
        except:
            pass

    def __enter__(self):
        """Context manager."""
        if not self.acquire():
            print("⚠️ Outra instância já está rodando!")
            print(f"   PID do processo: {self.get_current_pid()}")
            sys.exit(1)
        return self

    def __exit__(self, *args):
        """Context manager cleanup."""
        self.release()

    def get_current_pid(self):
        """Retorna PID do processo com lock."""
        try:
            with open(self.lock_file, 'r') as f:
                return f.read().strip()
        except:
            return "Desconhecido"


# Exemplo de uso
if __name__ == "__main__":
    print("🔒 Testando sistema de lock...")

    with ProcessLock("test_lock") as lock:
        print("✅ Lock adquirido!")
        print("   Simulando trabalho por 5 segundos...")
        time.sleep(5)

    print("✅ Lock liberado!")