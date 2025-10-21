#!/usr/bin/env python3
"""
🔄 IMPLEMENT REDIS LIFECYCLE MANAGEMENT
Redis inicia com scripturemon e para ao sair
MANTENDO EXTREMA ROBUSTEZ
"""

import re
from pathlib import Path
import shutil

def implement_redis_lifecycle():
    """Adiciona gestão automática do Redis ao scripturemon"""
    
    print("🔄 IMPLEMENTANDO REDIS LIFECYCLE MANAGEMENT")
    print("="*70)
    
    # Usar versão fixed que já está funcional
    scripturemon_path = Path("/Users/clubproducoes/Digimundo/scripturemon-validation/bin/scripturemon.fixed")
    
    if not scripturemon_path.exists():
        print("❌ scripturemon.fixed não encontrado")
        return False
    
    # Fazer backup
    backup_path = scripturemon_path.with_suffix('.fixed.bak')
    shutil.copy2(scripturemon_path, backup_path)
    print(f"💾 Backup criado: {backup_path}")
    
    content = scripturemon_path.read_text()
    lines = content.split('\n')
    
    # 1. Adicionar imports necessários
    import_added = False
    for i, line in enumerate(lines):
        if 'import signal' in line:
            if 'import atexit' not in content:
                lines.insert(i + 1, 'import atexit')
                import_added = True
                print("✅ Import atexit adicionado")
            break
    
    # 2. Adicionar código de gestão do Redis no __init__
    redis_management_code = '''
        # === REDIS LIFECYCLE MANAGEMENT ===
        self.redis_process = None
        self.redis_started_by_us = False
        
        # Verificar se Redis já está rodando
        try:
            redis_check = subprocess.run(
                ['pgrep', '-x', 'redis-server'],
                capture_output=True
            )
            redis_running = redis_check.returncode == 0
        except:
            redis_running = False
        
        if not redis_running:
            print("🔄 Iniciando Redis automaticamente...")
            try:
                # Tentar iniciar Redis
                self.redis_process = subprocess.Popen(
                    ['/opt/homebrew/bin/redis-server', '--daemonize', 'no'],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                self.redis_started_by_us = True
                time.sleep(2)  # Aguardar Redis iniciar
                
                # Verificar se iniciou
                redis_test = subprocess.run(
                    ['redis-cli', 'ping'],
                    capture_output=True,
                    text=True,
                    timeout=2
                )
                
                if redis_test.returncode == 0:
                    print("✅ Redis iniciado com sucesso")
                else:
                    print("⚠️ Redis iniciado mas não responde")
                    
            except Exception as e:
                print(f"⚠️ Não foi possível iniciar Redis: {e}")
                self.redis_process = None
        else:
            print("✅ Redis já está rodando")
        
        # Registrar cleanup
        atexit.register(self._cleanup_redis)
'''
    
    # Encontrar onde inserir no __init__
    for i, line in enumerate(lines):
        if 'def __init__(self):' in line and 'ScripturemonMaxCapacity' in '\n'.join(lines[max(0,i-5):i]):
            # Procurar o final das inicializações básicas
            insert_pos = i + 1
            # Pular docstring se houver
            while insert_pos < len(lines) and '"""' in lines[insert_pos]:
                insert_pos += 1
            
            # Inserir após as primeiras inicializações
            for j in range(insert_pos, min(insert_pos + 20, len(lines))):
                if 'self.base_path' in lines[j]:
                    lines.insert(j + 1, redis_management_code)
                    print("✅ Redis lifecycle management adicionado ao __init__")
                    break
            break
    
    # 3. Adicionar método de cleanup
    cleanup_method = '''
    def _cleanup_redis(self):
        """Limpa processo Redis se foi iniciado por nós"""
        if self.redis_started_by_us and self.redis_process:
            try:
                print("🛑 Encerrando Redis...")
                self.redis_process.terminate()
                self.redis_process.wait(timeout=5)
                print("✅ Redis encerrado")
            except:
                try:
                    self.redis_process.kill()
                except:
                    pass
'''
    
    # Adicionar método antes do shutdown
    for i, line in enumerate(lines):
        if 'def shutdown(self):' in line:
            lines.insert(i, cleanup_method)
            print("✅ Método _cleanup_redis adicionado")
            break
    
    # 4. Modificar shutdown para chamar cleanup
    for i, line in enumerate(lines):
        if 'def shutdown(self):' in line:
            # Procurar o início do método
            for j in range(i + 1, min(i + 10, len(lines))):
                if lines[j].strip() and not lines[j].strip().startswith('"'):
                    # Adicionar cleanup no início do shutdown
                    lines.insert(j, '        self._cleanup_redis()')
                    print("✅ Cleanup adicionado ao shutdown")
                    break
            break
    
    # 5. Adicionar tratamento de sinais para cleanup
    signal_handler_code = '''
def signal_handler(signum, frame):
    """Handler para sinais de término"""
    print("\\n🛑 Sinal de término recebido...")
    if 'system' in globals() and system:
        system.shutdown()
    sys.exit(0)

# Registrar handlers
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)
'''
    
    # Adicionar antes do if __name__ == "__main__"
    for i, line in enumerate(lines):
        if 'if __name__ == "__main__":' in line:
            if 'signal_handler' not in content:
                lines.insert(i - 1, signal_handler_code)
                print("✅ Signal handlers adicionados")
            break
    
    # Salvar arquivo modificado
    scripturemon_path.write_text('\n'.join(lines))
    print(f"💾 Arquivo salvo: {scripturemon_path}")
    
    return True

if __name__ == "__main__":
    if implement_redis_lifecycle():
        print("\n✅ REDIS LIFECYCLE IMPLEMENTADO COM SUCESSO!")
        print("\nRecursos adicionados:")
        print("  - Redis inicia automaticamente se não estiver rodando")
        print("  - Redis para ao sair do scripturemon")
        print("  - Cleanup registrado com atexit")
        print("  - Signal handlers para SIGINT e SIGTERM")
        print("\n💪 EXTREMA ROBUSTEZ MANTIDA!")
    else:
        print("\n❌ Erro na implementação")