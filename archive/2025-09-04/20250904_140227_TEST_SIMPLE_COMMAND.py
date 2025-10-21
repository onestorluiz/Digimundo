#!/usr/bin/env python3
"""
🔬 TEST SIMPLE COMMAND
Teste simplificado do comando scripturemon
"""

import subprocess
import time

def test_simple():
    """Testa comando simples"""
    
    print("🔬 TESTE SIMPLES DO SCRIPTUREMON")
    print("="*50)
    
    # Criar arquivo temporário com comando
    test_file = "/tmp/test_command.txt"
    with open(test_file, "w") as f:
        f.write("O que é cinema?\n")
    
    print("\n1. Testando com arquivo de comandos...")
    try:
        result = subprocess.run(
            ["./bin/scripturemon", "--file", test_file, "--timeout", "10"],
            capture_output=True,
            text=True,
            timeout=15,
            cwd="/Users/clubproducoes/Digimundo/scripturemon-validation"
        )
        
        if result.stdout:
            print(f"✅ Resposta recebida ({len(result.stdout)} chars)")
            print(f"Amostra: {result.stdout[:200]}...")
        else:
            print("❌ Nenhuma resposta")
            if result.stderr:
                print(f"Erro: {result.stderr[:200]}")
    except subprocess.TimeoutExpired:
        print("❌ Timeout!")
    except Exception as e:
        print(f"❌ Erro: {e}")
    
    print("\n2. Testando modo batch com echo...")
    try:
        # Usar echo para enviar comando
        proc = subprocess.Popen(
            'echo "O que é roteiro?" | ./bin/scripturemon --batch --timeout 10',
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd="/Users/clubproducoes/Digimundo/scripturemon-validation"
        )
        
        stdout, stderr = proc.communicate(timeout=15)
        
        if stdout:
            print(f"✅ Resposta recebida ({len(stdout)} chars)")
            
            # Verificar língua
            pt_words = ['roteiro', 'é', 'filme', 'história', 'cenas']
            en_words = ['screenplay', 'is', 'movie', 'story', 'scenes']
            
            stdout_lower = stdout.lower()
            pt_count = sum(1 for w in pt_words if w in stdout_lower)
            en_count = sum(1 for w in en_words if w in stdout_lower)
            
            if pt_count > en_count:
                print(f"✅ Resposta em português ({pt_count} palavras PT)")
            else:
                print(f"⚠️ Resposta pode estar em inglês ({en_count} palavras EN)")
            
            print(f"Amostra: {stdout[:200]}...")
        else:
            print("❌ Nenhuma resposta")
            if stderr:
                print(f"Erro: {stderr[:200]}")
                
    except subprocess.TimeoutExpired:
        print("❌ Timeout!")
    except Exception as e:
        print(f"❌ Erro: {e}")
    
    print("\n3. Verificando processos órfãos...")
    try:
        result = subprocess.run(
            ["pgrep", "-f", "scripturemon"],
            capture_output=True,
            text=True
        )
        
        if result.stdout:
            pids = result.stdout.strip().split('\n')
            print(f"⚠️ {len(pids)} processos scripturemon rodando: {pids}")
            
            # Matar processos órfãos
            for pid in pids:
                if pid:
                    subprocess.run(["kill", "-9", pid])
                    print(f"  Killed PID {pid}")
        else:
            print("✅ Nenhum processo órfão")
            
    except Exception as e:
        print(f"Erro verificando processos: {e}")

if __name__ == "__main__":
    test_simple()