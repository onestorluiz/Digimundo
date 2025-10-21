#!/usr/bin/env python3
"""
Bateria de Testes Comparativa - Versão 26
Compara sistema ANTES e DEPOIS das otimizações
"""

import subprocess
import time
import json
import os
import sys
from datetime import datetime

class ComparativeTest:
    def __init__(self):
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "before": {},
            "after": {},
            "comparison": {}
        }
        
    def run_command(self, cmd, timeout=30):
        """Executa comando e mede tempo"""
        start = time.time()
        try:
            result = subprocess.run(
                cmd, 
                shell=True, 
                capture_output=True, 
                text=True,
                timeout=timeout
            )
            elapsed = time.time() - start
            return {
                "success": result.returncode == 0,
                "time": elapsed,
                "stdout": result.stdout[:1000],  # Primeiros 1000 chars
                "stderr": result.stderr[:500]
            }
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "time": timeout,
                "stdout": "",
                "stderr": "TIMEOUT"
            }
        except Exception as e:
            return {
                "success": False,
                "time": time.time() - start,
                "stdout": "",
                "stderr": str(e)
            }
    
    def test_startup_time(self):
        """Testa tempo de inicialização"""
        print("📊 Testando tempo de inicialização...")
        
        # Comando status (mais rápido)
        cmd = "cd ~/Digimundo/scripturemon-validation && ./bin/scripturemon status"
        result = self.run_command(cmd, timeout=10)
        
        return {
            "startup_time": result["time"],
            "success": result["success"],
            "output": result["stdout"][:200]
        }
    
    def test_redis_usage(self):
        """Verifica uso do Redis"""
        print("📡 Verificando Redis...")
        
        # Verifica se Redis está rodando
        redis_check = self.run_command("redis-cli ping", timeout=2)
        
        # Verifica processos Redis
        redis_ps = self.run_command("ps aux | grep redis-server | grep -v grep | wc -l", timeout=2)
        
        return {
            "redis_active": redis_check["success"],
            "redis_processes": int(redis_ps["stdout"].strip()) if redis_ps["stdout"] else 0,
            "using_fakeredis": not redis_check["success"]
        }
    
    def test_memory_usage(self):
        """Testa uso de memória"""
        print("💾 Medindo uso de memória...")
        
        # Inicia o sistema e mede memória
        cmd = """
        cd ~/Digimundo/scripturemon-validation
        # Pega memória antes
        vm_stat | grep 'Pages free' | awk '{print $3}' | tr -d '.' > /tmp/mem_before.txt
        
        # Inicia sistema
        timeout 5 ./bin/scripturemon status >/dev/null 2>&1 || true
        
        # Pega memória depois
        vm_stat | grep 'Pages free' | awk '{print $3}' | tr -d '.' > /tmp/mem_after.txt
        
        # Calcula diferença
        echo "scale=2; ($(cat /tmp/mem_before.txt) - $(cat /tmp/mem_after.txt)) * 4096 / 1048576" | bc
        """
        
        result = self.run_command(cmd, timeout=10)
        
        return {
            "memory_delta_mb": float(result["stdout"].strip()) if result["stdout"].strip() else 0,
            "measurement_success": result["success"]
        }
    
    def test_ollama_models(self):
        """Verifica modelos Ollama carregados"""
        print("🤖 Verificando modelos Ollama...")
        
        # Lista modelos
        models = self.run_command("ollama list | tail -n +2 | wc -l", timeout=5)
        
        # Verifica modelo padrão
        default_check = self.run_command("""
        cd ~/Digimundo/scripturemon-validation
        ./.venv/bin/python -c "
from apps.scripturemon.ollama_core import OllamaCore
o = OllamaCore()
print(o.default_model)
" 2>/dev/null
        """, timeout=10)
        
        return {
            "total_models": int(models["stdout"].strip()) if models["stdout"] else 0,
            "default_model": default_check["stdout"].strip() if default_check["success"] else "unknown"
        }
    
    def test_command_availability(self):
        """Testa disponibilidade de comandos"""
        print("🔧 Testando comandos...")
        
        commands = {
            "status": "./bin/scripturemon status",
            "doctor": "./bin/scripturemon doctor",
            "help": "./bin/scripturemon help",
        }
        
        results = {}
        for name, cmd in commands.items():
            full_cmd = f"cd ~/Digimundo/scripturemon-validation && {cmd}"
            result = self.run_command(full_cmd, timeout=10)
            results[name] = {
                "available": result["success"],
                "time": result["time"],
                "has_output": len(result["stdout"]) > 0
            }
        
        return results
    
    def test_chat_initialization(self):
        """Testa inicialização do chat"""
        print("💬 Testando inicialização do chat...")
        
        # Tenta inicializar chat e sair imediatamente
        cmd = """
        cd ~/Digimundo/scripturemon-validation
        echo '/quit' | timeout 5 ./bin/scripturemon chat 2>&1 | head -20
        """
        
        result = self.run_command(cmd, timeout=10)
        
        # Verifica se sistemas foram inicializados
        has_soul = "Soul inicializada" in result["stdout"]
        has_consciousness = "Consciousness" in result["stdout"]
        has_ollama = "OLLAMA" in result["stdout"]
        has_memory = "MEMÓRIA" in result["stdout"] or "Memory" in result["stdout"]
        
        return {
            "chat_starts": result["success"] or len(result["stdout"]) > 100,
            "initialization_time": result["time"],
            "soul_initialized": has_soul,
            "consciousness_initialized": has_consciousness,
            "ollama_initialized": has_ollama,
            "memory_initialized": has_memory
        }
    
    def test_file_structure(self):
        """Verifica estrutura de arquivos"""
        print("📁 Verificando estrutura de arquivos...")
        
        checks = {
            "entrypoints.py": "test -f apps/scripturemon/entrypoints.py",
            "redis_on_demand.py": "test -f apps/scripturemon/redis_on_demand.py",
            "doctor.py": "test -f apps/scripturemon/doctor.py",
            "bin/scripturemon": "test -f bin/scripturemon",
            "ollama_core.py": "test -f apps/scripturemon/ollama_core.py"
        }
        
        results = {}
        for name, cmd in checks.items():
            full_cmd = f"cd ~/Digimundo/scripturemon-validation && {cmd}"
            result = self.run_command(full_cmd, timeout=2)
            results[name] = result["success"]
        
        return results
    
    def run_all_tests(self):
        """Executa todos os testes"""
        print("\n" + "="*60)
        print("🧪 BATERIA DE TESTES COMPARATIVA - VERSÃO 26")
        print("="*60)
        
        # Testes
        self.results["after"]["startup"] = self.test_startup_time()
        self.results["after"]["redis"] = self.test_redis_usage()
        self.results["after"]["memory"] = self.test_memory_usage()
        self.results["after"]["ollama"] = self.test_ollama_models()
        self.results["after"]["commands"] = self.test_command_availability()
        self.results["after"]["chat"] = self.test_chat_initialization()
        self.results["after"]["files"] = self.test_file_structure()
        
        # Análise comparativa
        self.analyze_differences()
        
        # Salvar resultados
        self.save_results()
        
        # Exibir resumo
        self.print_summary()
    
    def analyze_differences(self):
        """Analisa diferenças entre versões"""
        self.results["comparison"] = {
            "startup_improvement": "Não medido (sem dados ANTES)",
            "redis_optimization": self.results["after"]["redis"]["using_fakeredis"],
            "memory_usage": self.results["after"]["memory"]["memory_delta_mb"],
            "default_model": self.results["after"]["ollama"]["default_model"],
            "commands_working": sum(1 for cmd in self.results["after"]["commands"].values() if cmd["available"]),
            "new_files_added": sum(1 for f in self.results["after"]["files"].values() if f)
        }
    
    def save_results(self):
        """Salva resultados em JSON"""
        filename = f"test_results_v26_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w') as f:
            json.dump(self.results, f, indent=2)
        print(f"\n📄 Resultados salvos em: {filename}")
    
    def print_summary(self):
        """Imprime resumo dos resultados"""
        print("\n" + "="*60)
        print("📊 RESUMO DOS RESULTADOS")
        print("="*60)
        
        after = self.results["after"]
        comp = self.results["comparison"]
        
        print("\n🚀 PERFORMANCE:")
        print(f"  Tempo de startup: {after['startup']['startup_time']:.2f}s")
        print(f"  Uso de memória: {after['memory']['memory_delta_mb']:.1f} MB")
        
        print("\n📡 REDIS:")
        print(f"  Redis ativo: {'Não' if after['redis']['using_fakeredis'] else 'Sim'}")
        print(f"  Usando FakeRedis: {'Sim' if after['redis']['using_fakeredis'] else 'Não'}")
        print(f"  Processos Redis: {after['redis']['redis_processes']}")
        
        print("\n🤖 OLLAMA:")
        print(f"  Total de modelos: {after['ollama']['total_models']}")
        print(f"  Modelo padrão: {after['ollama']['default_model']}")
        
        print("\n✅ COMANDOS FUNCIONANDO:")
        for cmd, info in after['commands'].items():
            status = "✅" if info['available'] else "❌"
            print(f"  {status} {cmd}: {info['time']:.2f}s")
        
        print("\n💬 CHAT:")
        print(f"  Inicializa: {'✅' if after['chat']['chat_starts'] else '❌'}")
        print(f"  Tempo: {after['chat']['initialization_time']:.2f}s")
        print(f"  Soul: {'✅' if after['chat']['soul_initialized'] else '❌'}")
        print(f"  Consciousness: {'✅' if after['chat']['consciousness_initialized'] else '❌'}")
        
        print("\n📁 NOVOS ARQUIVOS:")
        for file, exists in after['files'].items():
            status = "✅" if exists else "❌"
            print(f"  {status} {file}")
        
        print("\n" + "="*60)
        print("🎯 CONCLUSÃO:")
        print("="*60)
        print(f"  Comandos funcionando: {comp['commands_working']}/3")
        print(f"  Arquivos novos criados: {comp['new_files_added']}/5")
        print(f"  Otimização Redis: {'✅ Ativada' if comp['redis_optimization'] else '❌ Desativada'}")
        print(f"  Modelo leve configurado: {'✅' if 'llama3.1:8b' in comp['default_model'] or 'mistral' in comp['default_model'] else '❌'}")

if __name__ == "__main__":
    tester = ComparativeTest()
    tester.run_all_tests()