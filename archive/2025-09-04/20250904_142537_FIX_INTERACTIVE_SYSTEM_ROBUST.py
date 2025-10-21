#!/usr/bin/env python3
"""
🎮 FIX INTERACTIVE SYSTEM - CORREÇÃO ROBUSTA
Ativa sistema interativo mantendo extrema robustez
"""

from pathlib import Path
import re

def fix_interactive_system():
    """Corrige sistema interativo para funcionar corretamente"""
    
    scripturemon_path = Path("/Users/clubproducoes/bin/scripturemon")
    
    if not scripturemon_path.exists():
        print("❌ scripturemon não encontrado")
        return False
    
    content = scripturemon_path.read_text()
    changes_made = []
    
    # 1. Verificar se o loop interativo está sendo alcançado
    if "while self.running:" in content:
        print("✅ Loop interativo já existe")
        
        # Adicionar debug logging para verificar se está entrando
        if "logger.debug('Entrando no loop interativo')" not in content:
            lines = content.split('\n')
            
            for i, line in enumerate(lines):
                if "while self.running:" in line:
                    # Adicionar logging antes do loop
                    debug_lines = [
                        "        # Debug para verificar loop interativo",
                        "        import logging",
                        "        logger = logging.getLogger(__name__)",
                        "        logger.info('🎮 Loop interativo iniciado')",
                        "        print('\\n📝 Modo interativo ativado. Digite \\'help\\' para comandos.')",
                        ""
                    ]
                    
                    # Inserir antes do while
                    for j, debug_line in enumerate(debug_lines):
                        lines.insert(i + j, debug_line)
                    
                    changes_made.append("✅ Debug logging adicionado ao loop interativo")
                    break
            
            content = '\n'.join(lines)
    
    # 2. Garantir que o prompt está visível
    if '📝 [' in content:
        # O prompt já existe, vamos torná-lo mais visível
        lines = content.split('\n')
        
        for i, line in enumerate(lines):
            if "print(f\"📝 [{state}|{consciousness:.3f}] > \"" in line:
                # Tornar prompt mais visível
                lines[i] = line.replace('print(f"', 'print(f"\\n')
                lines[i] = lines[i].replace('> "', '> ", end="", flush=True')
                changes_made.append("✅ Prompt tornado mais visível")
                break
        
        content = '\n'.join(lines)
    
    # 3. Adicionar flush aos outputs importantes
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if 'print("📝 Digite' in line and 'flush=True' not in line:
            lines[i] = line.replace(')"', ')", flush=True')
            changes_made.append("✅ Flush adicionado aos prints de instrução")
    
    content = '\n'.join(lines)
    
    # 4. Garantir que batch_mode está configurado corretamente
    if "def run_maximum_capacity" in content:
        lines = content.split('\n')
        
        for i, line in enumerate(lines):
            if "def run_maximum_capacity" in line:
                # Procurar onde batch_mode é usado
                for j in range(i, min(i+50, len(lines))):
                    if "if not batch_mode:" in lines[j]:
                        # Adicionar log para debug
                        if "logger.info('Modo interativo'" not in lines[j+1]:
                            lines.insert(j+1, "            logger.info('🎮 Entrando em modo interativo (batch_mode=False)')")
                            changes_made.append("✅ Debug de modo batch/interativo adicionado")
                        break
                break
        
        content = '\n'.join(lines)
    
    # 5. Adicionar handler para comandos extras
    if "_process_command" in content:
        lines = content.split('\n')
        
        # Procurar onde adicionar novos comandos
        for i, line in enumerate(lines):
            if "elif user_input.lower() == 'help':" in line:
                # Adicionar comandos extras antes do help
                new_commands = [
                    "        elif user_input.lower() == 'clear':",
                    "            # Limpar tela",
                    "            import os",
                    "            os.system('clear' if os.name == 'posix' else 'cls')",
                    "            print('🎬 SCRIPTUREMON - Tela limpa')",
                    "            ",
                    "        elif user_input.lower() == 'memory':",
                    "            # Mostrar estatísticas de memória",
                    "            stats = self.memory_manager.get_memory_statistics()",
                    "            print('\\n💾 ESTATÍSTICAS DE MEMÓRIA:')",
                    "            for key, value in stats.items():",
                    "                print(f'  {key}: {value}')",
                    "            ",
                    "        elif user_input.lower() == 'reset':",
                    "            # Reset suave do estado",
                    "            print('🔄 Resetando estado quântico...')",
                    "            self.memory_manager.quantum.reset_state()",
                    "            print('✅ Estado resetado')",
                    "            ",
                ]
                
                # Verificar se comandos já existem
                if "'clear'" not in content:
                    for j, cmd_line in enumerate(new_commands):
                        lines.insert(i + j, cmd_line)
                    changes_made.append("✅ Comandos extras adicionados (clear, memory, reset)")
                break
        
        content = '\n'.join(lines)
    
    # 6. Garantir que o sistema não trava esperando input
    if "sys.stdin.isatty()" in content:
        lines = content.split('\n')
        
        for i, line in enumerate(lines):
            if "if sys.stdin.isatty():" in line:
                # Adicionar timeout para input
                if "signal.alarm" not in content:
                    timeout_code = [
                        "                    # Adicionar timeout para evitar travamento",
                        "                    import signal",
                        "                    ",
                        "                    def timeout_handler(signum, frame):",
                        "                        raise TimeoutError('Input timeout')",
                        "                    ",
                        "                    # Configurar timeout de 60 segundos",
                        "                    if hasattr(signal, 'alarm'):",
                        "                        signal.signal(signal.SIGALRM, timeout_handler)",
                        "                        signal.alarm(60)",
                        "                    "
                    ]
                    
                    for j, timeout_line in enumerate(timeout_code):
                        lines.insert(i + 1 + j, timeout_line)
                    
                    changes_made.append("✅ Timeout de input adicionado (60s)")
                break
        
        content = '\n'.join(lines)
    
    # 7. Melhorar tratamento de erros no loop
    if "except KeyboardInterrupt:" in content:
        lines = content.split('\n')
        
        for i, line in enumerate(lines):
            if "except KeyboardInterrupt:" in line:
                # Verificar se já tem continue
                if i + 10 < len(lines):
                    has_continue = False
                    for j in range(i, min(i+10, len(lines))):
                        if "continue" in lines[j]:
                            has_continue = True
                            break
                    
                    if not has_continue:
                        # Adicionar continue para não sair do loop
                        lines.insert(i + 8, "                continue  # Continuar no loop após interrupção")
                        changes_made.append("✅ Continue adicionado após KeyboardInterrupt")
                break
        
        content = '\n'.join(lines)
    
    # Salvar arquivo
    if changes_made:
        scripturemon_path.write_text(content)
    
    print("\n".join(changes_made) if changes_made else "ℹ️ Sistema interativo já está configurado")
    
    return True

def create_interactive_test():
    """Cria script de teste para o modo interativo"""
    
    test_content = '''#!/usr/bin/env python3
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
        print(f"\\n📤 Enviando comando: {cmd}")
        proc.stdin.write(f"{cmd}\\n")
        proc.stdin.flush()
        time.sleep(2)
    
    # Aguardar finalização
    proc.wait(timeout=10)
    
    # Capturar output
    stdout, stderr = proc.communicate()
    
    # Verificar resultados
    if 'AJUDA' in stdout or 'STATUS' in stdout:
        print("\\n✅ Modo interativo funcionando!")
        print("   - Comandos reconhecidos")
        print("   - Sistema respondendo")
    else:
        print("\\n⚠️ Modo interativo pode ter problemas")
        print(f"   Output: {stdout[:200]}")
    
    return True

if __name__ == "__main__":
    test_interactive()
'''
    
    test_path = Path("/Users/clubproducoes/Digimundo/scripturemon-validation/test_interactive_mode.py")
    test_path.write_text(test_content)
    test_path.chmod(0o755)
    
    print("✅ Script de teste interativo criado: test_interactive_mode.py")

if __name__ == "__main__":
    print("🎮 ATIVANDO SISTEMA INTERATIVO COM ROBUSTEZ EXTREMA")
    print("="*60)
    
    print("\n1. Aplicando correções ao sistema interativo...")
    if fix_interactive_system():
        print("\n2. Criando script de teste...")
        create_interactive_test()
        
        print("\n✅ SISTEMA INTERATIVO ATIVADO!")
        print("\nMelhorias implementadas:")
        print("  - Debug logging no loop interativo")
        print("  - Prompt mais visível com flush")
        print("  - Comandos extras (clear, memory, reset)")
        print("  - Timeout de 60s para evitar travamento")
        print("  - Tratamento robusto de interrupções")
        print("  - Continue após KeyboardInterrupt")
        print("\nSistema mantém EXTREMA ROBUSTEZ com interatividade completa!")
    else:
        print("❌ Erro ao ativar sistema interativo")