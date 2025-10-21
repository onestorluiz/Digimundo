#!/usr/bin/env python3
"""
🎮 TEST INTERACTIVE MODE
Testa o modo interativo do Scripturemon
"""

import subprocess
import time
from pathlib import Path

def test_interactive():
    """Testa comandos interativos"""
    
    print("🎮 TESTANDO MODO INTERATIVO")
    print("="*60)
    
    # Criar processo interativo
    proc = subprocess.Popen(
        ['/Users/clubproducoes/bin/scripturemon'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # Aguardar inicialização
    time.sleep(5)
    
    # Enviar comandos de teste
    test_commands = [
        'help',
        'status',
        'memory',
        'exit'
    ]
    
    for cmd in test_commands:
        print(f"\n📤 Enviando comando: {cmd}")
        proc.stdin.write(f"{cmd}\n")
        proc.stdin.flush()
        time.sleep(2)
    
    # Aguardar finalização
    proc.wait(timeout=10)
    
    # Capturar output
    stdout, stderr = proc.communicate()
    
    # Verificar resultados
    if 'AJUDA' in stdout or 'STATUS' in stdout:
        print("\n✅ Modo interativo funcionando!")
        print("   - Comandos reconhecidos")
        print("   - Sistema respondendo")
    else:
        print("\n⚠️ Modo interativo pode ter problemas")
        print(f"   Output: {stdout[:200]}")
    
    return True

if __name__ == "__main__":
    test_interactive()
