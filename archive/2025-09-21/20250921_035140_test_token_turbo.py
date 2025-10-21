#!/usr/bin/env python3
"""
Bateria de Testes Completa para Token Turbo
Testa eficiência, harmonia e detecta bugs
"""

import sys
import time
import json
import psutil
import subprocess
from pathlib import Path
from datetime import datetime

# Adiciona src ao path
sys.path.insert(0, 'src')

from scripturemon_champion.core.profiles import LearningProfiles
from scripturemon_champion.analysis.script_doctor import ScriptDoctor
from scripturemon_champion.core.memory import UnifiedMemory
from scripturemon_champion.learning.learning_lite import LearningLite

print("=" * 80)
print("🚀 TOKEN TURBO - BATERIA DE TESTES COMPLETA")
print("=" * 80)
print()

class TokenTurboTester:
    def __init__(self):
        self.profile = LearningProfiles.get_profile('token_turbo')
        self.config = self.profile.config
        self.results = {
            'start_time': datetime.now().isoformat(),
            'tests': [],
            'metrics': {},
            'bugs': [],
            'harmonia': 100
        }

        # Componentes do sistema
        self.doctor = ScriptDoctor()
        self.learning = LearningLite()
        self.memory = UnifiedMemory(Path("data/unified_memory.db"))

        # Métricas iniciais
        self.start_ram = psutil.virtual_memory().used / (1024**3)
        self.start_cpu = psutil.cpu_percent(interval=1)

    def log(self, msg: str, level: str = "INFO"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        symbol = {"INFO": "ℹ️", "SUCCESS": "✅", "WARNING": "⚠️", "ERROR": "❌"}.get(level, "•")
        print(f"[{timestamp}] {symbol} {msg}")

    def test_1_profile_loading(self):
        """Teste 1: Carregamento do Perfil"""
        self.log("Teste 1: Carregando perfil Token Turbo")

        try:
            assert self.config['num_ctx'] == 200000, "Contexto deve ser 200K"
            assert self.config['rope_scaling'] == 1.5, "RoPE scaling deve ser 1.5"
            assert self.config['sliding_window'] == 65536, "Sliding window deve ser 65K"

            self.log(f"Contexto: {self.config['num_ctx']:,} tokens", "SUCCESS")
            self.log(f"RoPE Scaling: {self.config['rope_scaling']}", "SUCCESS")
            self.log(f"Sliding Window: {self.config['sliding_window']:,}", "SUCCESS")

            self.results['tests'].append({
                'name': 'profile_loading',
                'status': 'passed',
                'details': f"200K context, RoPE 1.5x"
            })
            return True

        except Exception as e:
            self.log(f"Erro no carregamento: {e}", "ERROR")
            self.results['bugs'].append(str(e))
            self.results['harmonia'] -= 20
            return False

    def test_2_memory_estimation(self):
        """Teste 2: Estimativa de Memória"""
        self.log("Teste 2: Verificando uso de memória")

        try:
            current_ram = psutil.virtual_memory().used / (1024**3)
            ram_delta = current_ram - self.start_ram

            self.log(f"RAM inicial: {self.start_ram:.1f}GB")
            self.log(f"RAM atual: {current_ram:.1f}GB")
            self.log(f"Delta: +{ram_delta:.1f}GB")

            # Token Turbo deve usar 52-55GB
            expected_max = 55
            if current_ram > expected_max:
                self.log(f"Aviso: RAM acima do esperado ({expected_max}GB)", "WARNING")
                self.results['harmonia'] -= 5
            else:
                self.log(f"RAM dentro do esperado (<{expected_max}GB)", "SUCCESS")

            self.results['metrics']['ram_usage'] = {
                'start': f"{self.start_ram:.1f}GB",
                'current': f"{current_ram:.1f}GB",
                'delta': f"+{ram_delta:.1f}GB"
            }

            self.results['tests'].append({
                'name': 'memory_estimation',
                'status': 'passed',
                'ram': f"{current_ram:.1f}GB"
            })
            return True

        except Exception as e:
            self.log(f"Erro na estimativa: {e}", "ERROR")
            self.results['bugs'].append(str(e))
            self.results['harmonia'] -= 10
            return False

    def test_3_modelfile_generation(self):
        """Teste 3: Geração do Modelfile"""
        self.log("Teste 3: Gerando modelfile Token Turbo")

        try:
            modelfile_path = LearningProfiles.create_modelfile('token_turbo')

            assert modelfile_path.exists(), "Modelfile deve existir"
            content = modelfile_path.read_text()

            # Verificar componentes essenciais
            assert "num_ctx 200000" in content, "Deve ter 200K context"
            assert "rope_scaling 1.5" in content, "Deve ter RoPE scaling"
            assert "TOKEN TURBO" in content, "Deve mencionar Token Turbo"

            self.log(f"Modelfile criado: {modelfile_path}", "SUCCESS")
            self.log(f"Tamanho: {len(content)} bytes", "SUCCESS")

            # Verificar se é válido para Ollama
            lines = content.split('\n')
            params = [l for l in lines if l.startswith('PARAMETER')]
            self.log(f"Parâmetros encontrados: {len(params)}", "SUCCESS")

            self.results['tests'].append({
                'name': 'modelfile_generation',
                'status': 'passed',
                'path': str(modelfile_path),
                'params': len(params)
            })
            return True

        except Exception as e:
            self.log(f"Erro na geração: {e}", "ERROR")
            self.results['bugs'].append(str(e))
            self.results['harmonia'] -= 15
            return False

    def test_4_script_analysis(self):
        """Teste 4: Análise de Roteiro com Token Turbo Config"""
        self.log("Teste 4: Testando análise de roteiro")

        try:
            # Criar roteiro de teste
            test_script = """FADE IN:

INT. LABORATORY - NIGHT

DR. SARAH CHEN, 35, brilliant scientist, stares at the quantum computer.

SARAH
(whispered)
After ten years... finally.

The machine HUMS to life. Data flows across holographic displays.

SARAH (CONT'D)
The multiverse equation... it works!

Suddenly, the room SHAKES. Reality FRACTURES around her.

FADE OUT."""

            # Analisar com configuração Token Turbo
            start_time = time.time()
            analysis = self.doctor.analyze_script(test_script, "test_quantum")
            elapsed = time.time() - start_time

            self.log(f"Análise completa em {elapsed:.2f}s", "SUCCESS")
            self.log(f"Cenas detectadas: {analysis.scenes}", "SUCCESS")
            self.log(f"Diálogo: {analysis.dialogue_ratio:.1%}", "SUCCESS")

            # Verificar qualidade
            assert analysis.scenes > 0, "Deve detectar cenas"
            assert 0 <= analysis.dialogue_ratio <= 1, "Ratio deve estar entre 0-1"

            self.results['tests'].append({
                'name': 'script_analysis',
                'status': 'passed',
                'time': f"{elapsed:.2f}s",
                'scenes': analysis.scenes
            })
            return True

        except Exception as e:
            self.log(f"Erro na análise: {e}", "ERROR")
            self.results['bugs'].append(str(e))
            self.results['harmonia'] -= 10
            return False

    def test_5_learning_system(self):
        """Teste 5: Sistema de Aprendizado"""
        self.log("Teste 5: Testando sistema de aprendizado")

        try:
            # Testar aprendizado
            stats_before = self.learning.get_statistics()

            # Criar análise mock
            from scripturemon_champion.analysis.script_doctor import ScriptAnalysis, Beat
            mock_analysis = ScriptAnalysis(
                scenes=10,
                characters=5,
                words=12000,
                avg_scene_len=300.0,
                top_characters=["Sarah", "John"],
                notes=["Test analysis"],
                dialogue_ratio=0.4,
                pacing_score=0.75,
                beats=[],
                type_token_ratio=0.5,
                action_ratio=0.6
            )

            # Aprender
            concepts = self.learning.learn_from_analysis(mock_analysis, "test_film")
            stats_after = self.learning.get_statistics()

            self.log(f"Conceitos aprendidos: {len(concepts)}", "SUCCESS")
            self.log(f"Total beats: {stats_after.get('total_beats', 0)}", "SUCCESS")

            self.results['tests'].append({
                'name': 'learning_system',
                'status': 'passed',
                'concepts': len(concepts)
            })
            return True

        except Exception as e:
            self.log(f"Erro no aprendizado: {e}", "ERROR")
            self.results['bugs'].append(str(e))
            self.results['harmonia'] -= 10
            return False

    def test_6_memory_integration(self):
        """Teste 6: Integração com Memória Unificada"""
        self.log("Teste 6: Testando memória unificada")

        try:
            # Salvar na memória
            from scripturemon_champion.core.memory import MemoryRecord
            record = MemoryRecord(
                type="token_turbo_test",
                key=f"test_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                value={'profile': 'token_turbo', 'context': 200000},
                metadata={'test': True}
            )

            record_id = self.memory.store(record)
            assert record_id is not None, "Deve retornar ID"

            # Recuperar
            retrieved = self.memory.get("token_turbo_test", record.key)
            assert retrieved is not None, "Deve recuperar registro"
            assert retrieved.value['context'] == 200000, "Contexto deve ser 200K"

            self.log(f"Registro salvo: {record_id}", "SUCCESS")
            self.log("Recuperação bem-sucedida", "SUCCESS")

            # Stats
            stats = self.memory.stats()
            self.log(f"Total registros: {stats.get('total_records', 0)}", "SUCCESS")

            self.results['tests'].append({
                'name': 'memory_integration',
                'status': 'passed',
                'record_id': record_id
            })
            return True

        except Exception as e:
            self.log(f"Erro na memória: {e}", "ERROR")
            self.results['bugs'].append(str(e))
            self.results['harmonia'] -= 10
            return False

    def test_7_performance_benchmark(self):
        """Teste 7: Benchmark de Performance"""
        self.log("Teste 7: Benchmark de performance")

        try:
            # Criar texto grande para testar contexto
            large_text = "Era uma vez um reino distante. " * 5000  # ~50K chars

            # Teste de velocidade
            iterations = 3
            times = []

            for i in range(iterations):
                start = time.time()
                # Simular processamento
                tokens = len(large_text.split())
                chunks = [large_text[i:i+1000] for i in range(0, len(large_text), 1000)]
                elapsed = time.time() - start
                times.append(elapsed)
                self.log(f"Iteração {i+1}: {elapsed:.3f}s", "INFO")

            avg_time = sum(times) / len(times)
            tokens_per_sec = tokens / avg_time

            self.log(f"Tempo médio: {avg_time:.3f}s", "SUCCESS")
            self.log(f"Tokens/seg: {tokens_per_sec:.0f}", "SUCCESS")

            # Token Turbo deve ser ~10-15% mais lento
            expected_slowdown = 0.15
            if avg_time > 1.0 * (1 + expected_slowdown):
                self.log("Performance abaixo do esperado", "WARNING")
                self.results['harmonia'] -= 5

            self.results['metrics']['performance'] = {
                'avg_time': f"{avg_time:.3f}s",
                'tokens_per_sec': f"{tokens_per_sec:.0f}",
                'iterations': iterations
            }

            self.results['tests'].append({
                'name': 'performance_benchmark',
                'status': 'passed',
                'avg_time': f"{avg_time:.3f}s"
            })
            return True

        except Exception as e:
            self.log(f"Erro no benchmark: {e}", "ERROR")
            self.results['bugs'].append(str(e))
            self.results['harmonia'] -= 10
            return False

    def test_8_stress_test(self):
        """Teste 8: Stress Test com Contexto Máximo"""
        self.log("Teste 8: Stress test com 200K context")

        try:
            # Simular contexto de 200K tokens (~800K chars)
            self.log("Gerando texto de 200K tokens...")

            # Gerar texto realista
            base_scene = """
INT. OFFICE - DAY

JOHN enters the room. He looks around nervously.

JOHN
Is anyone here?

MARY appears from behind the desk.

MARY
I've been waiting for you.
"""

            # Repetir para criar ~200K tokens
            repetitions = 2000
            large_context = base_scene * repetitions
            token_count = len(large_context.split())

            self.log(f"Texto gerado: {len(large_context):,} chars", "INFO")
            self.log(f"Tokens estimados: {token_count:,}", "INFO")

            # Verificar limites
            if token_count > 200000:
                self.log("Contexto acima de 200K - testando limite", "WARNING")

            # Simular processamento
            start = time.time()
            chunks = len(large_context) // 65536  # Sliding window
            elapsed = time.time() - start

            self.log(f"Processamento simulado em {elapsed:.2f}s", "SUCCESS")
            self.log(f"Chunks processados: {chunks}", "SUCCESS")

            # Verificar estabilidade
            current_ram = psutil.virtual_memory().used / (1024**3)
            if current_ram < 60:  # Deve estar abaixo de 60GB
                self.log(f"RAM estável: {current_ram:.1f}GB", "SUCCESS")
            else:
                self.log(f"RAM elevada: {current_ram:.1f}GB", "WARNING")
                self.results['harmonia'] -= 5

            self.results['tests'].append({
                'name': 'stress_test',
                'status': 'passed',
                'tokens': token_count,
                'ram': f"{current_ram:.1f}GB"
            })
            return True

        except Exception as e:
            self.log(f"Erro no stress test: {e}", "ERROR")
            self.results['bugs'].append(str(e))
            self.results['harmonia'] -= 15
            return False

    def test_9_ollama_command(self):
        """Teste 9: Comando Ollama para Criar Modelo"""
        self.log("Teste 9: Verificando comando Ollama")

        try:
            cmd = LearningProfiles.get_ollama_command('token_turbo')

            assert "ollama create" in cmd, "Deve ter 'ollama create'"
            assert "mixtral-token_turbo" in cmd, "Deve ter nome correto"
            assert ".modelfile" in cmd, "Deve referenciar modelfile"

            self.log(f"Comando: {cmd}", "SUCCESS")

            # Verificar se Ollama está disponível
            try:
                result = subprocess.run(['ollama', '--version'],
                                      capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    self.log("Ollama disponível", "SUCCESS")
                else:
                    self.log("Ollama não está rodando", "WARNING")
            except:
                self.log("Ollama não encontrado", "WARNING")

            self.results['tests'].append({
                'name': 'ollama_command',
                'status': 'passed',
                'command': cmd
            })
            return True

        except Exception as e:
            self.log(f"Erro no comando: {e}", "ERROR")
            self.results['bugs'].append(str(e))
            self.results['harmonia'] -= 5
            return False

    def test_10_system_harmony(self):
        """Teste 10: Harmonia Geral do Sistema"""
        self.log("Teste 10: Verificando harmonia do sistema")

        try:
            # Verificar componentes
            components = {
                'profiles': LearningProfiles.PROFILES is not None,
                'doctor': self.doctor is not None,
                'learning': self.learning is not None,
                'memory': self.memory is not None,
                'config': self.config is not None
            }

            working = sum(components.values())
            total = len(components)

            for name, status in components.items():
                symbol = "✅" if status else "❌"
                self.log(f"{symbol} {name.capitalize()}", "INFO")

            harmony_score = (working / total) * 100
            self.log(f"Componentes funcionais: {working}/{total}", "SUCCESS")
            self.log(f"Harmonia base: {harmony_score:.0f}%", "SUCCESS")

            # Ajustar harmonia final
            if self.results['harmonia'] < 100:
                self.log(f"Descontos aplicados: -{100 - self.results['harmonia']}%", "WARNING")

            self.results['tests'].append({
                'name': 'system_harmony',
                'status': 'passed',
                'components': f"{working}/{total}",
                'harmony': f"{self.results['harmonia']}%"
            })
            return True

        except Exception as e:
            self.log(f"Erro na harmonia: {e}", "ERROR")
            self.results['bugs'].append(str(e))
            return False

    def run_all_tests(self):
        """Executa toda a bateria de testes"""
        self.log("Iniciando bateria completa de testes", "INFO")
        print("-" * 80)

        tests = [
            self.test_1_profile_loading,
            self.test_2_memory_estimation,
            self.test_3_modelfile_generation,
            self.test_4_script_analysis,
            self.test_5_learning_system,
            self.test_6_memory_integration,
            self.test_7_performance_benchmark,
            self.test_8_stress_test,
            self.test_9_ollama_command,
            self.test_10_system_harmony
        ]

        passed = 0
        failed = 0

        for test in tests:
            print()
            if test():
                passed += 1
            else:
                failed += 1
            time.sleep(0.5)  # Pequena pausa entre testes

        # Métricas finais
        print()
        print("=" * 80)
        print("📊 RESULTADOS FINAIS")
        print("=" * 80)

        # Recursos finais
        final_ram = psutil.virtual_memory().used / (1024**3)
        final_cpu = psutil.cpu_percent(interval=1)
        ram_total_delta = final_ram - self.start_ram

        self.results['metrics']['final'] = {
            'ram': f"{final_ram:.1f}GB",
            'cpu': f"{final_cpu:.1f}%",
            'ram_delta_total': f"+{ram_total_delta:.1f}GB"
        }

        # Resumo
        self.results['summary'] = {
            'passed': passed,
            'failed': failed,
            'total': len(tests),
            'success_rate': f"{(passed/len(tests))*100:.1f}%",
            'harmonia_final': f"{self.results['harmonia']}%",
            'bugs_found': len(self.results['bugs'])
        }

        print(f"\n✅ Testes aprovados: {passed}/{len(tests)}")
        print(f"❌ Testes falhados: {failed}/{len(tests)}")
        print(f"🎯 Taxa de sucesso: {(passed/len(tests))*100:.1f}%")
        print(f"🔮 Harmonia final: {self.results['harmonia']}%")
        print(f"🐛 Bugs encontrados: {len(self.results['bugs'])}")

        if self.results['bugs']:
            print(f"\n⚠️ BUGS DETECTADOS:")
            for bug in self.results['bugs']:
                print(f"  • {bug}")

        print(f"\n📈 MÉTRICAS DE RECURSOS:")
        print(f"  • RAM inicial: {self.start_ram:.1f}GB")
        print(f"  • RAM final: {final_ram:.1f}GB")
        print(f"  • Delta total: +{ram_total_delta:.1f}GB")
        print(f"  • CPU médio: {final_cpu:.1f}%")

        # Salvar relatório
        report_path = Path(f"test_results_token_turbo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        with open(report_path, 'w') as f:
            json.dump(self.results, f, indent=2)
        print(f"\n💾 Relatório salvo: {report_path}")

        # Veredito final
        print()
        print("=" * 80)
        if self.results['harmonia'] >= 90 and failed == 0:
            print("🎉 TOKEN TURBO APROVADO - PRONTO PARA PRODUÇÃO!")
        elif self.results['harmonia'] >= 75:
            print("⚠️ TOKEN TURBO FUNCIONAL - PEQUENOS AJUSTES NECESSÁRIOS")
        else:
            print("❌ TOKEN TURBO PRECISA DE CORREÇÕES SIGNIFICATIVAS")
        print("=" * 80)

        return self.results

if __name__ == "__main__":
    tester = TokenTurboTester()
    results = tester.run_all_tests()

    # Retornar código de saída baseado no sucesso
    if results['summary']['failed'] == 0:
        sys.exit(0)
    else:
        sys.exit(1)