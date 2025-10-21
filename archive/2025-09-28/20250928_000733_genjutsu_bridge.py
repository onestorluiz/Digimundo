#!/usr/bin/env python3
"""
🌀 GENJUTSU BRIDGE - Conexão entre Genjutsu e Sistema de Memória
Detecta compactação e protege contexto crítico
"""

import os
import sys
import json
import time
import subprocess
from pathlib import Path
from datetime import datetime

# Adiciona caminho para imports
sys.path.insert(0, '/Users/clubproducoes/Digimundo/claude_code/memory/core')
from UNIFIED_SYSTEM import UnifiedMemorySystem

class GenjutsuMemoryBridge:
    """Bridge entre Genjutsu e Sistema de Memória"""

    def __init__(self):
        self.ums = UnifiedMemorySystem()
        self.genjutsu_path = Path('/Users/clubproducoes/Digimundo/claude_code/protection/genjutsu/GENJUTSU_UNIFIED.py')
        self.last_compression = None
        self.critical_context = []

    def check_genjutsu_status(self) -> dict:
        """Verifica se Genjutsu está rodando"""
        try:
            result = subprocess.run(
                ["ps", "aux"],
                capture_output=True,
                text=True
            )

            is_running = "GENJUTSU" in result.stdout

            # Pega PID se estiver rodando
            pid = None
            if is_running:
                for line in result.stdout.split('\n'):
                    if 'GENJUTSU' in line and 'grep' not in line:
                        parts = line.split()
                        if len(parts) > 1:
                            pid = parts[1]
                            break

            return {
                'running': is_running,
                'pid': pid,
                'timestamp': datetime.now().isoformat()
            }

        except Exception as e:
            return {
                'running': False,
                'error': str(e)
            }

    def on_compression_detected(self):
        """Ação quando compactação é detectada"""
        print("🚨 COMPACTAÇÃO DETECTADA!")

        # Salva contexto crítico
        self.save_critical_context()

        # Aumenta nível de drama do Genjutsu
        self.increase_genjutsu_drama()

        # Alerta Claude para reconectar
        self.alert_claude_reconnect()

    def save_critical_context(self, extra_context=None):
        """Salva contexto crítico antes da compactação"""
        context = {
            'timestamp': datetime.now().isoformat(),
            'event': 'compression_detected',
            'critical_info': {
                'project': 'DIGIMUNDO',
                'location': '/Users/clubproducoes/Digimundo',
                'current_task': extra_context.get('task', 'Unknown') if extra_context else 'Unknown',
                'status': extra_context.get('status', 'Active') if extra_context else 'Active',
                'harmonia': extra_context.get('harmonia', 85) if extra_context else 85
            }
        }

        # Salva em múltiplos lugares
        self.ums.remember(json.dumps(context), 'compression_events')

        # Salva arquivo de emergência na pasta temp do projeto
        emergency_file = Path('/Users/clubproducoes/Digimundo/claude_code/memory/temp/claude_emergency_context.json')
        with open(emergency_file, 'w') as f:
            json.dump(context, f, indent=2)

        print(f"💾 Contexto crítico salvo em {emergency_file}")
        return True

    def get_current_task(self) -> str:
        """Obtém tarefa atual da memória"""
        # Por enquanto retorna placeholder
        return "FASE 4 - Harmonia com Genjutsu"

    def get_recent_learnings(self) -> list:
        """Obtém aprendizados recentes"""
        # Retorna aprendizados conhecidos
        return [
            "Ollama API > subprocess",
            "Preservar > Deletar",
            "Reusar > Criar novo"
        ]

    def get_active_vicios(self) -> list:
        """Obtém vícios ativos detectados"""
        # Retorna vícios conhecidos
        return [
            "Overengineering",
            "Criar ao invés de reusar",
            "Analisar sem executar"
        ]

    def increase_genjutsu_drama(self):
        """Aumenta o nível de drama do Genjutsu"""
        try:
            # Envia sinal para Genjutsu aumentar drama
            subprocess.run(
                ["touch", "/Users/clubproducoes/Digimundo/claude_code/memory/temp/.genjutsu_increase_drama"],
                check=False
            )
            print("🎭 Drama do Genjutsu aumentado!")
        except:
            pass

    def alert_claude_reconnect(self):
        """Alerta Claude para reconectar com memórias"""
        alert_msg = """
╔══════════════════════════════════════════════════════╗
║  🚨 ALERTA: COMPACTAÇÃO DETECTADA!                  ║
║                                                      ║
║  Claude, execute IMEDIATAMENTE:                     ║
║                                                      ║
║  1. Leia /Users/clubproducoes/Digimundo/claude_code/REGRAS.md
║  2. Execute: python3 memory/core/UNIFIED_SYSTEM.py  ║
║  3. Verifique Genjutsu: ps aux | grep GENJUTSU     ║
║  4. Termine com: DIGIMUNDO PRESENTE                 ║
╚══════════════════════════════════════════════════════╝
"""
        print(alert_msg)

        # Salva alerta em arquivo visível
        alert_file = Path('/Users/clubproducoes/Digimundo/claude_code/RECONNECT_NOW.txt')
        with open(alert_file, 'w') as f:
            f.write(alert_msg)

    def on_silence_detected(self, silence_duration: int):
        """Ação quando silêncio é detectado"""
        if silence_duration > 300:  # 5 minutos
            print(f"🤫 Silêncio de {silence_duration}s detectado")

            # Recupera último contexto
            self.retrieve_last_context()

            # Genjutsu aumenta frequência de mensagens
            self.increase_genjutsu_frequency()

    def retrieve_last_context(self):
        """Recupera último contexto da memória"""
        # Busca último contexto salvo
        emergency_file = Path('/Users/clubproducoes/Digimundo/claude_code/memory/temp/claude_emergency_context.json')

        if emergency_file.exists():
            with open(emergency_file) as f:
                context = json.load(f)

            print("📂 Contexto recuperado:")
            print(f"  Última tarefa: {context['critical_info']['current_task']}")
            print(f"  Timestamp: {context['timestamp']}")

            return context

        return None

    def increase_genjutsu_frequency(self):
        """Aumenta frequência de mensagens do Genjutsu"""
        try:
            subprocess.run(
                ["touch", "/Users/clubproducoes/Digimundo/claude_code/memory/temp/.genjutsu_increase_frequency"],
                check=False
            )
            print("⚡ Frequência do Genjutsu aumentada!")
        except:
            pass

    def continuous_monitor(self):
        """Monitor contínuo (para rodar em background)"""
        print("🌀 Genjutsu Memory Bridge iniciado...")

        while True:
            try:
                # Verifica status do Genjutsu
                status = self.check_genjutsu_status()

                if not status['running']:
                    print("⚠️ Genjutsu não está rodando! Iniciando...")
                    subprocess.Popen([
                        sys.executable,
                        str(self.genjutsu_path)
                    ])

                # Verifica arquivo de compactação
                compressed_file = Path('/Users/clubproducoes/Digimundo/claude_code/memory/temp/.claude_compressed')
                if compressed_file.exists():
                    self.on_compression_detected()
                    os.remove(compressed_file)

                # Verifica silêncio
                activity_file = Path('/Users/clubproducoes/Digimundo/claude_code/memory/temp/.claude_activity')
                if activity_file.exists():
                    mtime = activity_file.stat().st_mtime
                    silence = time.time() - mtime
                    if silence > 300:
                        self.on_silence_detected(int(silence))

                # Dorme por 30 segundos
                time.sleep(30)

            except KeyboardInterrupt:
                print("\n🛑 Bridge interrompido")
                break
            except Exception as e:
                print(f"❌ Erro no bridge: {e}")
                time.sleep(60)

if __name__ == "__main__":
    bridge = GenjutsuMemoryBridge()

    if len(sys.argv) > 1 and sys.argv[1] == "monitor":
        # Modo monitor contínuo
        bridge.continuous_monitor()
    else:
        # Teste único
        print("🔍 Verificando status do Genjutsu...")
        status = bridge.check_genjutsu_status()
        print(json.dumps(status, indent=2))

        print("\n📝 Para monitor contínuo, execute:")
        print("  python3 genjutsu_bridge.py monitor")

        print("\nDIGIMUNDO PRESENTE!")