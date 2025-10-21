#!/usr/bin/env python3
"""
🏥 HEALTH CHECK SYSTEM
Sistema robusto de monitoramento de saúde
"""

import subprocess
import sqlite3
import json
import time
import psutil
from pathlib import Path
from typing import Dict, List, Tuple

class HealthCheckSystem:
    """Sistema completo de health checks"""
    
    def __init__(self):
        self.checks_passed = []
        self.checks_failed = []
        self.start_time = time.time()
    
    def check_ollama_service(self) -> Tuple[bool, str]:
        """Verifica se Ollama está rodando"""
        try:
            result = subprocess.run(
                ["ollama", "list"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                models = len(result.stdout.strip().split('\n')) - 1  # -1 para header
                return True, f"Ollama ativo com {models} modelos"
            else:
                return False, "Ollama não está respondendo"
        except Exception as e:
            return False, f"Erro ao verificar Ollama: {str(e)}"
    
    def check_database(self) -> Tuple[bool, str]:
        """Verifica integridade do banco de dados"""
        try:
            db_path = Path("/Users/clubproducoes/Digimundo/scripturemon-validation/data/memories/scripturemon_supreme.db")
            
            if not db_path.exists():
                return False, "Banco de dados não encontrado"
            
            conn = sqlite3.connect(str(db_path))
            cursor = conn.cursor()
            
            # Verificar tabelas essenciais
            tables_needed = ['L1', 'L2', 'L3', 'L4']
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            existing_tables = [row[0] for row in cursor.fetchall()]
            
            missing = set(tables_needed) - set(existing_tables)
            if missing:
                return False, f"Tabelas faltando: {missing}"
            
            # Contar registros
            total_memories = 0
            for table in tables_needed:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                total_memories += count
            
            conn.close()
            return True, f"DB OK com {total_memories} memórias totais"
            
        except Exception as e:
            return False, f"Erro no banco: {str(e)}"
    
    def check_memory_usage(self) -> Tuple[bool, str]:
        """Verifica uso de memória"""
        try:
            memory = psutil.virtual_memory()
            used_percent = memory.percent
            available_gb = memory.available / (1024**3)
            
            if used_percent > 90:
                return False, f"Memória crítica: {used_percent:.1f}% usado"
            elif used_percent > 75:
                return True, f"Memória alta: {used_percent:.1f}% usado ({available_gb:.1f}GB livre)"
            else:
                return True, f"Memória OK: {used_percent:.1f}% usado ({available_gb:.1f}GB livre)"
                
        except Exception as e:
            return False, f"Erro ao verificar memória: {str(e)}"
    
    def check_required_models(self) -> Tuple[bool, str]:
        """Verifica modelos necessários"""
        try:
            result = subprocess.run(
                ["ollama", "list"],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode != 0:
                return False, "Não foi possível listar modelos"
            
            installed_models = result.stdout.lower()
            
            # Modelos críticos
            critical_models = ['llama3.2:3b', 'mistral']
            missing = []
            
            for model in critical_models:
                if model not in installed_models:
                    missing.append(model)
            
            if missing:
                return False, f"Modelos críticos faltando: {missing}"
            
            # Contar modelos scripturemon
            scripturemon_count = installed_models.count('scripturemon')
            
            return True, f"Modelos OK ({scripturemon_count} scripturemon variants)"
            
        except Exception as e:
            return False, f"Erro ao verificar modelos: {str(e)}"
    
    def check_phase4_systems(self) -> Tuple[bool, str]:
        """Verifica sistemas da Fase 4"""
        try:
            phase4_files = {
                "Quantum Config": "/Users/clubproducoes/Digimundo/scripturemon-validation/.env.quantum",
                "Cinema RAG": "/Users/clubproducoes/Digimundo/scripturemon-validation/data/cinema_rag/index_config.json",
                "Fusion System": "/Users/clubproducoes/Digimundo/scripturemon-validation/apps/scripturemon/multimodel_fusion.py",
                "Telepathy": "/Users/clubproducoes/Digimundo/scripturemon-validation/apps/scripturemon/telepathy_network.py"
            }
            
            missing = []
            for name, path in phase4_files.items():
                if not Path(path).exists():
                    missing.append(name)
            
            if missing:
                return False, f"Sistemas Fase 4 faltando: {missing}"
            
            return True, "Todos os sistemas Fase 4 ativos"
            
        except Exception as e:
            return False, f"Erro ao verificar Fase 4: {str(e)}"
    
    def check_portuguese_system(self) -> Tuple[bool, str]:
        """Verifica sistema de português"""
        try:
            enforcer_path = Path("/Users/clubproducoes/Digimundo/scripturemon-validation/apps/scripturemon/portuguese_enforcer.py")
            
            if not enforcer_path.exists():
                return False, "Portuguese Enforcer não encontrado"
            
            # Verificar se está integrado
            scripturemon_path = Path("/Users/clubproducoes/bin/scripturemon")
            if scripturemon_path.exists():
                content = scripturemon_path.read_text()
                if "portuguese_enforcer" in content:
                    return True, "Sistema de português integrado e ativo"
                else:
                    return True, "Portuguese Enforcer criado mas não integrado"
            
            return True, "Portuguese Enforcer disponível"
            
        except Exception as e:
            return False, f"Erro no sistema de português: {str(e)}"
    
    def check_screenplay_files(self) -> Tuple[bool, str]:
        """Verifica arquivos de roteiro"""
        try:
            locations = [
                "/Users/clubproducoes/Documents/SONHOS_SEM_LEMBRANCAS.txt",
                "/Users/clubproducoes/Digimundo/SONHOS_SEM_LEMBRANCAS.txt"
            ]
            
            found = []
            for loc in locations:
                if Path(loc).exists():
                    found.append(Path(loc).name)
            
            if not found:
                return False, "Nenhum roteiro encontrado"
            
            return True, f"Roteiros encontrados: {len(found)} arquivo(s)"
            
        except Exception as e:
            return False, f"Erro ao verificar roteiros: {str(e)}"
    
    def run_all_checks(self) -> Dict:
        """Executa todos os health checks"""
        
        print("🏥 EXECUTANDO HEALTH CHECKS COMPLETOS")
        print("="*50)
        
        checks = [
            ("Serviço Ollama", self.check_ollama_service),
            ("Banco de Dados", self.check_database),
            ("Uso de Memória", self.check_memory_usage),
            ("Modelos Requeridos", self.check_required_models),
            ("Sistemas Fase 4", self.check_phase4_systems),
            ("Sistema Português", self.check_portuguese_system),
            ("Arquivos Roteiro", self.check_screenplay_files)
        ]
        
        for name, check_func in checks:
            print(f"\n📋 Verificando {name}...")
            passed, message = check_func()
            
            if passed:
                print(f"  ✅ {message}")
                self.checks_passed.append(name)
            else:
                print(f"  ❌ {message}")
                self.checks_failed.append(name)
            
            time.sleep(0.1)  # Pequena pausa para visualização
        
        # Resumo final
        print("\n" + "="*50)
        print("📊 RESUMO DOS HEALTH CHECKS")
        print(f"  ✅ Passou: {len(self.checks_passed)}/{len(checks)}")
        print(f"  ❌ Falhou: {len(self.checks_failed)}/{len(checks)}")
        print(f"  ⏱️ Tempo: {time.time() - self.start_time:.2f}s")
        
        health_score = (len(self.checks_passed) / len(checks)) * 100
        
        if health_score == 100:
            print(f"\n🎉 SISTEMA 100% SAUDÁVEL!")
        elif health_score >= 80:
            print(f"\n✅ Sistema operacional ({health_score:.0f}% saudável)")
        elif health_score >= 60:
            print(f"\n⚠️ Sistema parcialmente operacional ({health_score:.0f}% saudável)")
        else:
            print(f"\n❌ Sistema com problemas críticos ({health_score:.0f}% saudável)")
        
        return {
            'score': health_score,
            'passed': self.checks_passed,
            'failed': self.checks_failed,
            'duration': time.time() - self.start_time
        }

def create_monitoring_daemon():
    """Cria daemon de monitoramento contínuo"""
    
    daemon_script = '''#!/usr/bin/env python3
"""
🔄 HEALTH MONITORING DAEMON
Monitoramento contínuo de saúde
"""

import time
import json
from pathlib import Path
from datetime import datetime

def monitor_loop():
    """Loop principal de monitoramento"""
    
    log_path = Path("/Users/clubproducoes/Digimundo/scripturemon-validation/health_logs")
    log_path.mkdir(exist_ok=True)
    
    while True:
        # Executar health check
        from IMPLEMENT_HEALTH_CHECKS import HealthCheckSystem
        
        health = HealthCheckSystem()
        result = health.run_all_checks()
        
        # Salvar log
        timestamp = datetime.now().isoformat()
        log_file = log_path / f"health_{timestamp.replace(':', '-')}.json"
        
        log_data = {
            'timestamp': timestamp,
            'score': result['score'],
            'passed': result['passed'],
            'failed': result['failed'],
            'duration': result['duration']
        }
        
        log_file.write_text(json.dumps(log_data, indent=2))
        
        # Aguardar próximo ciclo (5 minutos)
        time.sleep(300)

if __name__ == "__main__":
    print("🔄 Iniciando daemon de monitoramento...")
    monitor_loop()
'''
    
    daemon_path = Path("/Users/clubproducoes/Digimundo/scripturemon-validation/health_monitor_daemon.py")
    daemon_path.write_text(daemon_script)
    print("✅ Daemon de monitoramento criado")

if __name__ == "__main__":
    # Executar health checks
    health = HealthCheckSystem()
    result = health.run_all_checks()
    
    # Criar daemon
    print("\n📝 Criando daemon de monitoramento...")
    create_monitoring_daemon()
    
    # Salvar resultado
    result_path = Path("/Users/clubproducoes/Digimundo/scripturemon-validation/last_health_check.json")
    result_path.write_text(json.dumps(result, indent=2))
    
    print(f"\n💾 Resultado salvo em: {result_path}")