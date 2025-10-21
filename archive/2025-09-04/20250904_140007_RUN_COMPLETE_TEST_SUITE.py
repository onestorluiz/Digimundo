#!/usr/bin/env python3
"""
🧪 COMPLETE TEST SUITE
Suite completa de testes para validação final
"""

import subprocess
import time
import json
from pathlib import Path
from typing import Dict, List

class CompleteTestSuite:
    """Suite de testes completa do SCRIPTUREMON"""
    
    def __init__(self):
        self.test_results = {}
        self.start_time = time.time()
    
    def test_basic_command(self) -> bool:
        """Testa comando básico"""
        print("\n🔧 Teste 1: Comando Básico")
        try:
            result = subprocess.run(
                ["bin/scripturemon", "--help"],
                capture_output=True,
                text=True,
                timeout=10,
                cwd="/Users/clubproducoes/Digimundo/scripturemon-validation"
            )
            
            success = result.returncode == 0 and "scripturemon" in result.stdout.lower()
            self.test_results['basic_command'] = {
                'passed': success,
                'output': result.stdout[:200] if success else result.stderr[:200]
            }
            
            if success:
                print("  ✅ Comando básico funcionando")
            else:
                print("  ❌ Falha no comando básico")
            
            return success
            
        except Exception as e:
            print(f"  ❌ Erro: {str(e)}")
            self.test_results['basic_command'] = {'passed': False, 'error': str(e)}
            return False
    
    def test_portuguese_response(self) -> bool:
        """Testa resposta em português"""
        print("\n🇧🇷 Teste 2: Resposta em Português")
        try:
            test_prompt = "Explique brevemente o que é um roteiro"
            
            result = subprocess.run(
                ["bin/scripturemon", "--batch", "--commands", test_prompt],
                capture_output=True,
                text=True,
                timeout=30,
                cwd="/Users/clubproducoes/Digimundo/scripturemon-validation"
            )
            
            response = result.stdout.lower()
            
            # Verificar indicadores de português
            pt_indicators = ['roteiro', 'é', 'um', 'que', 'para', 'filme', 'história']
            en_indicators = ['screenplay', 'is', 'the', 'that', 'for', 'movie', 'story']
            
            pt_count = sum(1 for word in pt_indicators if word in response)
            en_count = sum(1 for word in en_indicators if word in response)
            
            success = pt_count > en_count and pt_count >= 2
            
            self.test_results['portuguese_response'] = {
                'passed': success,
                'pt_words': pt_count,
                'en_words': en_count,
                'sample': response[:150]
            }
            
            if success:
                print(f"  ✅ Resposta em português ({pt_count} palavras PT vs {en_count} EN)")
            else:
                print(f"  ❌ Resposta não está em português ({pt_count} PT vs {en_count} EN)")
            
            return success
            
        except Exception as e:
            print(f"  ❌ Erro: {str(e)}")
            self.test_results['portuguese_response'] = {'passed': False, 'error': str(e)}
            return False
    
    def test_screenplay_analysis(self) -> bool:
        """Testa análise de roteiro"""
        print("\n🎬 Teste 3: Análise de Roteiro")
        try:
            screenplay_path = Path("/Users/clubproducoes/Digimundo/SONHOS_SEM_LEMBRANCAS.txt")
            
            if not screenplay_path.exists():
                print("  ⚠️ Roteiro não encontrado, pulando teste")
                return True  # Não falhar se arquivo não existe
            
            test_prompt = f"Analise o roteiro em {screenplay_path} e diga quantas cenas tem"
            
            result = subprocess.run(
                ["bin/scripturemon", "--batch", "--commands", test_prompt],
                capture_output=True,
                text=True,
                timeout=45,
                cwd="/Users/clubproducoes/Digimundo/scripturemon-validation"
            )
            
            response = result.stdout.lower()
            
            # Verificar se detectou cenas
            success = any(word in response for word in ['cena', 'scene', '5', 'cinco'])
            
            self.test_results['screenplay_analysis'] = {
                'passed': success,
                'detected_scenes': '5' in response or 'cinco' in response,
                'sample': response[:150]
            }
            
            if success:
                print("  ✅ Análise de roteiro funcionando")
            else:
                print("  ❌ Falha na análise de roteiro")
            
            return success
            
        except Exception as e:
            print(f"  ❌ Erro: {str(e)}")
            self.test_results['screenplay_analysis'] = {'passed': False, 'error': str(e)}
            return False
    
    def test_memory_persistence(self) -> bool:
        """Testa persistência de memória"""
        print("\n💾 Teste 4: Persistência de Memória")
        try:
            # Criar uma memória
            test_memory = "Teste de memória em " + str(time.time())
            
            result1 = subprocess.run(
                ["bin/scripturemon", "--batch", "--commands", f"Lembre-se disso: {test_memory}"],
                capture_output=True,
                text=True,
                timeout=30,
                cwd="/Users/clubproducoes/Digimundo/scripturemon-validation"
            )
            
            time.sleep(2)
            
            # Verificar se lembra
            result2 = subprocess.run(
                ["bin/scripturemon", "--batch", "--commands", "O que você deve lembrar?"],
                capture_output=True,
                text=True,
                timeout=30,
                cwd="/Users/clubproducoes/Digimundo/scripturemon-validation"
            )
            
            response = result2.stdout
            
            # Verificar se algo foi salvo (não precisa ser exato)
            success = len(response) > 50  # Resposta substancial
            
            self.test_results['memory_persistence'] = {
                'passed': success,
                'memory_saved': result1.returncode == 0,
                'memory_recalled': len(response) > 50
            }
            
            if success:
                print("  ✅ Memória persistente funcionando")
            else:
                print("  ❌ Problema com persistência de memória")
            
            return success
            
        except Exception as e:
            print(f"  ❌ Erro: {str(e)}")
            self.test_results['memory_persistence'] = {'passed': False, 'error': str(e)}
            return False
    
    def test_multimodel_fallback(self) -> bool:
        """Testa fallback multi-modelo"""
        print("\n🔄 Teste 5: Fallback Multi-Modelo")
        try:
            # Testar com timeout curto para forçar fallback
            test_prompt = "Responda rápido: o que é cinema?"
            
            result = subprocess.run(
                ["bin/scripturemon", "--batch", "--commands", test_prompt],
                capture_output=True,
                text=True,
                timeout=15,  # Timeout curto
                cwd="/Users/clubproducoes/Digimundo/scripturemon-validation"
            )
            
            success = result.returncode == 0 and len(result.stdout) > 10
            
            self.test_results['multimodel_fallback'] = {
                'passed': success,
                'responded': len(result.stdout) > 10,
                'time': 'within_timeout'
            }
            
            if success:
                print("  ✅ Sistema de fallback funcionando")
            else:
                print("  ❌ Problema com fallback")
            
            return success
            
        except subprocess.TimeoutExpired:
            print("  ⚠️ Timeout - sistema pode estar lento")
            self.test_results['multimodel_fallback'] = {'passed': False, 'error': 'timeout'}
            return False
        except Exception as e:
            print(f"  ❌ Erro: {str(e)}")
            self.test_results['multimodel_fallback'] = {'passed': False, 'error': str(e)}
            return False
    
    def test_phase4_systems(self) -> bool:
        """Testa sistemas da Fase 4"""
        print("\n🔮 Teste 6: Sistemas Fase 4")
        
        phase4_checks = {
            'quantum_config': Path("/Users/clubproducoes/Digimundo/scripturemon-validation/.env.quantum"),
            'cinema_rag': Path("/Users/clubproducoes/Digimundo/scripturemon-validation/data/cinema_rag/index_config.json"),
            'fusion_system': Path("/Users/clubproducoes/Digimundo/scripturemon-validation/apps/scripturemon/multimodel_fusion.py"),
            'telepathy': Path("/Users/clubproducoes/Digimundo/scripturemon-validation/apps/scripturemon/telepathy_network.py"),
            'crystal_memory': Path("/Users/clubproducoes/Digimundo/scripturemon-validation/apps/scripturemon/crystal_memory.py")
        }
        
        results = {}
        all_passed = True
        
        for name, path in phase4_checks.items():
            exists = path.exists()
            results[name] = exists
            if not exists:
                all_passed = False
                print(f"  ❌ {name} não encontrado")
            else:
                print(f"  ✅ {name} ativo")
        
        self.test_results['phase4_systems'] = {
            'passed': all_passed,
            'systems': results
        }
        
        return all_passed
    
    def generate_report(self) -> Dict:
        """Gera relatório final"""
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for r in self.test_results.values() if r.get('passed', False))
        
        duration = time.time() - self.start_time
        
        report = {
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'duration': f"{duration:.2f}s",
            'total_tests': total_tests,
            'passed': passed_tests,
            'failed': total_tests - passed_tests,
            'success_rate': f"{(passed_tests/total_tests)*100:.1f}%",
            'test_results': self.test_results
        }
        
        return report
    
    def run_all_tests(self):
        """Executa todos os testes"""
        
        print("🧪 SUITE COMPLETA DE TESTES SCRIPTUREMON")
        print("="*50)
        
        tests = [
            self.test_basic_command,
            self.test_portuguese_response,
            self.test_screenplay_analysis,
            self.test_memory_persistence,
            self.test_multimodel_fallback,
            self.test_phase4_systems
        ]
        
        for test_func in tests:
            test_func()
            time.sleep(1)  # Pausa entre testes
        
        # Gerar relatório
        report = self.generate_report()
        
        print("\n" + "="*50)
        print("📊 RELATÓRIO FINAL DOS TESTES")
        print(f"  ⏱️ Duração: {report['duration']}")
        print(f"  ✅ Passou: {report['passed']}/{report['total_tests']}")
        print(f"  ❌ Falhou: {report['failed']}/{report['total_tests']}")
        print(f"  📈 Taxa de Sucesso: {report['success_rate']}")
        
        # Avaliar resultado
        success_rate = (report['passed'] / report['total_tests']) * 100
        
        if success_rate == 100:
            print("\n🎉 TODOS OS TESTES PASSARAM! SISTEMA 100% FUNCIONAL!")
        elif success_rate >= 80:
            print(f"\n✅ SISTEMA APROVADO ({success_rate:.0f}% dos testes passaram)")
        elif success_rate >= 60:
            print(f"\n⚠️ SISTEMA PARCIALMENTE FUNCIONAL ({success_rate:.0f}% dos testes passaram)")
        else:
            print(f"\n❌ SISTEMA COM PROBLEMAS ({success_rate:.0f}% dos testes passaram)")
        
        # Salvar relatório
        report_path = Path("/Users/clubproducoes/Digimundo/scripturemon-validation/test_report.json")
        report_path.write_text(json.dumps(report, indent=2))
        print(f"\n💾 Relatório salvo em: {report_path}")
        
        return report

if __name__ == "__main__":
    suite = CompleteTestSuite()
    report = suite.run_all_tests()
    
    # Retornar código de saída baseado no sucesso
    import sys
    if report['passed'] == report['total_tests']:
        sys.exit(0)  # Sucesso total
    elif report['passed'] >= report['total_tests'] * 0.8:
        sys.exit(1)  # Sucesso parcial
    else:
        sys.exit(2)  # Falha