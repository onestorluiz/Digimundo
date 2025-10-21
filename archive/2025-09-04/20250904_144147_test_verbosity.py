#!/usr/bin/env python3
"""
🔊 TEST VERBOSITY LEVELS
Testa diferentes níveis de verbosidade
"""

import subprocess
import time

def test_verbosity():
    """Testa cada nível de verbosidade"""
    
    print("🔊 TESTANDO NÍVEIS DE VERBOSIDADE")
    print("="*60)
    
    levels = [
        ('--quiet', 'SILENT (-q)'),
        ('', 'QUIET (padrão)'),
        ('-v', 'NORMAL (-v)'),
        ('-vv', 'VERBOSE (-vv)'),
        ('-vvv', 'DEBUG (-vvv)')
    ]
    
    test_cmd = "echo 'teste' | "
    
    for flag, name in levels:
        print(f"\n📊 Testando {name}...")
        print("-"*40)
        
        cmd = f"{test_cmd}./bin/scripturemon {flag} --timeout 3"
        
        try:
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                timeout=5,
                cwd='/Users/clubproducoes/Digimundo/scripturemon-validation'
            )
            
            # Contar linhas de output
            lines = result.stdout.split('\n')
            non_empty = [l for l in lines if l.strip()]
            
            print(f"  Linhas de output: {len(non_empty)}")
            
            if flag == '--quiet':
                if len(non_empty) < 10:
                    print("  ✅ Modo quiet funcionando (output mínimo)")
                else:
                    print("  ⚠️ Modo quiet ainda verboso")
            elif flag == '-vvv':
                if len(non_empty) > 50:
                    print("  ✅ Modo debug funcionando (output máximo)")
                else:
                    print("  ⚠️ Modo debug não mostra detalhes suficientes")
            
            # Mostrar amostra
            print(f"  Primeiras 3 linhas:")
            for line in non_empty[:3]:
                print(f"    {line[:60]}")
                
        except subprocess.TimeoutExpired:
            print("  ⏱️ Timeout (sistema pode estar lento)")
        except Exception as e:
            print(f"  ❌ Erro: {e}")
    
    print("\n✅ Teste de verbosidade completo!")

if __name__ == "__main__":
    test_verbosity()
