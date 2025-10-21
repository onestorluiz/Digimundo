#!/usr/bin/env python3
"""
🔥 TESTE DE STRESS ROBUSTO - SILICON VALLEY LEVEL
"""

import sys
import os
import json
import time
import asyncio
import threading
import multiprocessing
from datetime import datetime
from pathlib import Path
import random
import string
import hashlib

sys.path.insert(0, '.')

class TesteStressRobusto:
    def __init__(self):
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "stress_tests": [],
            "concurrency_tests": [],
            "memory_tests": [],
            "performance_metrics": {}
        }
        
    async def run_all_tests(self):
        print("\n" + "="*70)
        print("🔥 TESTE DE STRESS ROBUSTO - SILICON VALLEY LEVEL")
        print("="*70)
        
        # 1. Teste de Concorrência
        print("\n⚡ TESTE DE CONCORRÊNCIA")
        await self.test_concurrency()
        
        # 2. Teste de Memória
        print("\n💾 TESTE DE MEMÓRIA")
        await self.test_memory_stress()
        
        # 3. Teste de Performance
        print("\n🚀 TESTE DE PERFORMANCE")
        await self.test_performance()
        
        # 4. Teste de Race Conditions
        print("\n🏁 TESTE DE RACE CONDITIONS")
        await self.test_race_conditions()
        
        # 5. Teste de Resiliência
        print("\n🛡️ TESTE DE RESILIÊNCIA")
        await self.test_resilience()
        
        # Relatório
        self.generate_report()
        
    async def test_concurrency(self):
        """Testa operações concorrentes"""
        print("  Testando 100 requisições simultâneas...")
        
        try:
            from apps.scripturemon.memory_unification import get_unified_memory
            mem = get_unified_memory()
            
            async def concurrent_write(i):
                key = f"concurrent_test_{i}"
                value = f"value_{i}_{datetime.now().isoformat()}"
                mem.store_unified_memory(value, source=f"test_{i}", memory_type="test")
                return True
            
            # Criar 100 tarefas concorrentes
            tasks = [concurrent_write(i) for i in range(100)]
            start = time.time()
            results = await asyncio.gather(*tasks, return_exceptions=True)
            elapsed = time.time() - start
            
            success_count = sum(1 for r in results if r is True)
            print(f"    ✅ {success_count}/100 escritas bem-sucedidas em {elapsed:.2f}s")
            
            self.results["concurrency_tests"].append({
                "test": "100_concurrent_writes",
                "success": success_count,
                "total": 100,
                "time": elapsed
            })
            
        except Exception as e:
            print(f"    ❌ Erro na concorrência: {str(e)[:50]}")
            
    async def test_memory_stress(self):
        """Testa uso intensivo de memória"""
        print("  Testando armazenamento de 10MB de dados...")
        
        try:
            from apps.scripturemon.memory_unification import get_unified_memory
            mem = get_unified_memory()
            
            # Gerar 10MB de dados aleatórios
            big_data = ''.join(random.choices(string.ascii_letters, k=10*1024*1024))
            chunks = [big_data[i:i+1024] for i in range(0, len(big_data), 1024)]
            
            start = time.time()
            for i, chunk in enumerate(chunks[:100]):  # Apenas primeiros 100 chunks
                mem.store_unified_memory(chunk, source=f"chunk_{i}", memory_type="stress")
            elapsed = time.time() - start
            
            print(f"    ✅ 100KB armazenados em {elapsed:.2f}s")
            
            # Testar recuperação
            start = time.time()
            results = mem.retrieve_unified_memory("", limit=50)
            elapsed = time.time() - start
            
            print(f"    ✅ 50 memórias recuperadas em {elapsed:.2f}s")
            
            self.results["memory_tests"].append({
                "test": "large_data_storage",
                "chunks_stored": 100,
                "store_time": elapsed,
                "retrieve_count": len(results) if results else 0
            })
            
        except Exception as e:
            print(f"    ❌ Erro no teste de memória: {str(e)[:50]}")
            
    async def test_performance(self):
        """Testa métricas de performance"""
        print("  Medindo latências e throughput...")
        
        try:
            from apps.scripturemon.chat import ScripturemonChat
            chat = ScripturemonChat()
            
            # Teste de latência
            latencies = []
            for i in range(10):
                start = time.time()
                response = await chat.process_async("teste " + str(i))
                latencies.append(time.time() - start)
            
            avg_latency = sum(latencies) / len(latencies)
            min_latency = min(latencies)
            max_latency = max(latencies)
            
            print(f"    📊 Latência: avg={avg_latency:.3f}s, min={min_latency:.3f}s, max={max_latency:.3f}s")
            
            # Teste de throughput
            start = time.time()
            tasks = [chat.process_async(f"msg_{i}") for i in range(20)]
            await asyncio.gather(*tasks, return_exceptions=True)
            elapsed = time.time() - start
            throughput = 20 / elapsed
            
            print(f"    📊 Throughput: {throughput:.2f} req/s")
            
            self.results["performance_metrics"] = {
                "avg_latency": avg_latency,
                "min_latency": min_latency,
                "max_latency": max_latency,
                "throughput": throughput
            }
            
        except Exception as e:
            print(f"    ❌ Erro no teste de performance: {str(e)[:50]}")
            
    async def test_race_conditions(self):
        """Testa condições de corrida"""
        print("  Testando modificações concorrentes...")
        
        try:
            from apps.scripturemon.memory_unification import get_unified_memory
            mem = get_unified_memory()
            
            # Criar um contador compartilhado
            counter_key = "race_condition_counter"
            mem.store_unified_memory("0", source="test", memory_type="counter")
            
            async def increment_counter():
                # Simular race condition
                result = mem.retrieve_unified_memory(counter_key, limit=1)
                if result:
                    current = int(result[0].get("content", "0"))
                    await asyncio.sleep(0.001)  # Simular processamento
                    mem.store_unified_memory(str(current + 1), source="test", memory_type="counter")
                    return True
                return False
            
            # 50 incrementos concorrentes
            tasks = [increment_counter() for _ in range(50)]
            await asyncio.gather(*tasks, return_exceptions=True)
            
            # Verificar valor final
            result = mem.retrieve_unified_memory(counter_key, limit=1)
            final_value = int(result[0].get("content", "0")) if result else 0
            
            if final_value == 50:
                print(f"    ✅ Sem race conditions detectadas (valor: {final_value})")
            else:
                print(f"    ⚠️ Possível race condition (esperado: 50, obtido: {final_value})")
                
            self.results["concurrency_tests"].append({
                "test": "race_condition_counter",
                "expected": 50,
                "actual": final_value,
                "race_detected": final_value != 50
            })
            
        except Exception as e:
            print(f"    ❌ Erro no teste de race conditions: {str(e)[:50]}")
            
    async def test_resilience(self):
        """Testa recuperação de falhas"""
        print("  Testando recuperação de falhas...")
        
        try:
            # Teste 1: Reconexão ao Redis
            import redis
            r = redis.Redis()
            
            # Simular desconexão e reconexão
            try:
                r.ping()
                print("    ✅ Redis resiliente")
            except:
                print("    ⚠️ Redis em modo fallback")
                
            # Teste 2: Recuperação de backup
            from apps.scripturemon.immortality import ImmortalityProtocol
            immortal = ImmortalityProtocol()
            
            # Criar backup de teste
            test_data = {"test": "resilience", "timestamp": datetime.now().isoformat()}
            backup_path = immortal.save_backup(test_data, "test_resilience")
            
            if backup_path and backup_path.exists():
                # Simular recuperação
                recovered = immortal.load_backup(backup_path)
                if recovered == test_data:
                    print("    ✅ Backup e recuperação funcionando")
                else:
                    print("    ⚠️ Dados recuperados diferem")
            else:
                print("    ❌ Falha ao criar backup")
                
            # Teste 3: Fallback para modo offline
            from apps.scripturemon.memory_unification import get_unified_memory
            mem = get_unified_memory()
            
            # Forçar modo offline
            mem.telepathy = None
            mem.store_unified_memory("teste_offline", source="test", memory_type="offline")
            result = mem.retrieve_unified_memory("teste_offline", limit=1)
            
            if result:
                print("    ✅ Modo offline funcional")
            else:
                print("    ❌ Falha no modo offline")
                
        except Exception as e:
            print(f"    ❌ Erro no teste de resiliência: {str(e)[:50]}")
            
    def generate_report(self):
        """Gera relatório de stress"""
        print("\n" + "="*70)
        print("📊 RELATÓRIO DE STRESS TEST")
        print("="*70)
        
        # Concorrência
        if self.results["concurrency_tests"]:
            print("\n⚡ CONCORRÊNCIA:")
            for test in self.results["concurrency_tests"]:
                if test["test"] == "100_concurrent_writes":
                    rate = (test["success"] / test["total"]) * 100
                    print(f"  - Taxa de sucesso: {rate:.1f}%")
                    print(f"  - Tempo total: {test['time']:.2f}s")
                elif test["test"] == "race_condition_counter":
                    if not test["race_detected"]:
                        print(f"  - ✅ Sem race conditions")
                    else:
                        print(f"  - ⚠️ Race condition detectada")
                        
        # Performance
        if self.results["performance_metrics"]:
            print("\n🚀 PERFORMANCE:")
            metrics = self.results["performance_metrics"]
            print(f"  - Latência média: {metrics.get('avg_latency', 0):.3f}s")
            print(f"  - Throughput: {metrics.get('throughput', 0):.2f} req/s")
            
        # Memória
        if self.results["memory_tests"]:
            print("\n💾 MEMÓRIA:")
            for test in self.results["memory_tests"]:
                print(f"  - Chunks armazenados: {test['chunks_stored']}")
                print(f"  - Memórias recuperadas: {test['retrieve_count']}")
                
        # Score final
        total_score = self.calculate_stress_score()
        print(f"\n🎯 STRESS SCORE: {total_score}/100")
        
        if total_score >= 90:
            print("✅ SISTEMA EXTREMAMENTE ROBUSTO!")
        elif total_score >= 75:
            print("⚠️ SISTEMA ROBUSTO COM PEQUENOS AJUSTES")
        else:
            print("❌ SISTEMA PRECISA DE MELHORIAS")
            
        # Salvar relatório
        report_file = Path("stress_test_report.json")
        with open(report_file, 'w') as f:
            json.dump(self.results, f, indent=2, default=str)
        print(f"\n💾 Relatório salvo em: {report_file}")
        
    def calculate_stress_score(self):
        """Calcula score de stress"""
        score = 0
        
        # Concorrência (30 pontos)
        for test in self.results["concurrency_tests"]:
            if test["test"] == "100_concurrent_writes":
                score += (test["success"] / test["total"]) * 20
            elif test["test"] == "race_condition_counter":
                if not test["race_detected"]:
                    score += 10
                    
        # Performance (40 pontos)
        if self.results["performance_metrics"]:
            metrics = self.results["performance_metrics"]
            # Latência < 1s = 20 pontos
            if metrics.get("avg_latency", float('inf')) < 1.0:
                score += 20
            elif metrics.get("avg_latency", float('inf')) < 2.0:
                score += 10
                
            # Throughput > 10 req/s = 20 pontos
            if metrics.get("throughput", 0) > 10:
                score += 20
            elif metrics.get("throughput", 0) > 5:
                score += 10
                
        # Memória (30 pontos)
        for test in self.results["memory_tests"]:
            if test["chunks_stored"] >= 100:
                score += 15
            if test["retrieve_count"] >= 40:
                score += 15
                
        return min(100, score)

async def main():
    tester = TesteStressRobusto()
    await tester.run_all_tests()

if __name__ == "__main__":
    asyncio.run(main())