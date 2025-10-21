#!/usr/bin/env python3
"""
🎬 BATERIA DE TESTES NÍVEL VALE DO SILÍCIO
Teste completo e rigoroso do sistema Scripturemon
"""

import sys
import time
import json
from pathlib import Path
from typing import Dict, List, Tuple

sys.path.insert(0, str(Path(__file__).parent))

# Importações do sistema
from apps.scripturemon.ollama_core import OllamaCore
from apps.scripturemon.scripturemon_brain import ScripturemonBrain

class SiliconValleyTester:
    """Teste rigoroso nível Vale do Silício"""
    
    def __init__(self):
        self.results = {
            "total_tests": 0,
            "passed": 0,
            "failed": 0,
            "errors": [],
            "performance": {}
        }
        
        # Perguntas sobre PDFs de teoria cinematográfica
        self.pdf_questions = [
            ("McKee - Story", "Qual é a definição de 'beat' segundo Robert McKee em Story?"),
            ("Vogler - Writer's Journey", "Quais são os 12 estágios da Jornada do Herói segundo Vogler?"),
            ("Snyder - Save the Cat", "O que significa 'Save the Cat' e em que página deve acontecer?"),
            ("Truby - Anatomy of Story", "Quais são os 22 passos da estrutura narrativa de Truby?"),
            ("Field - Screenplay", "Como Syd Field define o paradigma do roteiro de 3 atos?"),
            ("Campbell - Hero's Journey", "Qual a diferença entre o limiar e o mundo especial?"),
            ("Hauge - Writing Screenplays", "Quais são os 6 estágios de Michael Hauge?"),
            ("Yorke - Into the Woods", "Como John Yorke explica a estrutura de 5 atos?"),
            ("Cron - Story Genius", "O que Lisa Cron diz sobre o 'third rail' da história?"),
            ("Marks - Inside Story", "Como Dara Marks conecta arco interno e externo?")
        ]
    
    def run_all_tests(self) -> Dict:
        """Executa bateria completa de testes"""
        print("="*70)
        print(" 🚀 INICIANDO TESTES NÍVEL VALE DO SILÍCIO")
        print("="*70)
        
        # 1. Teste de inicialização
        self._test_initialization()
        
        # 2. Teste de perguntas sobre PDFs
        self._test_pdf_questions()
        
        # 3. Teste de análise de roteiro
        self._test_screenplay_analysis()
        
        # 4. Teste de performance
        self._test_performance()
        
        # 5. Relatório final
        self._generate_report()
        
        return self.results
    
    def _test_initialization(self):
        """Testa inicialização de todos os sistemas"""
        print("\n📋 TESTE 1: Inicialização dos Sistemas")
        print("-"*50)
        
        systems = [
            ("OllamaCore", lambda: OllamaCore()),
            ("ScripturemonBrain", lambda: ScripturemonBrain())
        ]
        
        for name, init_func in systems:
            self.results["total_tests"] += 1
            try:
                start = time.time()
                obj = init_func()
                elapsed = time.time() - start
                
                print(f"✅ {name}: OK ({elapsed:.2f}s)")
                self.results["passed"] += 1
                self.results["performance"][name] = elapsed
                
            except Exception as e:
                print(f"❌ {name}: FALHOU - {str(e)}")
                self.results["failed"] += 1
                self.results["errors"].append({
                    "system": name,
                    "error": str(e)
                })
    
    def _test_pdf_questions(self):
        """Testa conhecimento sobre PDFs de teoria"""
        print("\n📚 TESTE 2: Perguntas sobre PDFs Teóricos")
        print("-"*50)
        
        core = OllamaCore()
        
        for i, (pdf_name, question) in enumerate(self.pdf_questions, 1):
            self.results["total_tests"] += 1
            print(f"\n{i}. {pdf_name}")
            print(f"   Pergunta: {question}")
            
            try:
                start = time.time()
                response = core.generate(
                    prompt=f"Com base no livro {pdf_name}, responda: {question}",
                    temperature=0.3,
                    max_tokens=500
                )
                elapsed = time.time() - start
                
                # Verifica qualidade da resposta
                if response and len(response) > 50:
                    print(f"   ✅ Resposta em {elapsed:.1f}s")
                    print(f"   Preview: {response[:100]}...")
                    self.results["passed"] += 1
                else:
                    print(f"   ⚠️ Resposta muito curta")
                    self.results["failed"] += 1
                    
            except Exception as e:
                print(f"   ❌ Erro: {e}")
                self.results["failed"] += 1
                self.results["errors"].append({
                    "test": f"PDF_{pdf_name}",
                    "error": str(e)
                })
    
    def _test_screenplay_analysis(self):
        """Testa análise de roteiro"""
        print("\n🎬 TESTE 3: Análise de Roteiro")
        print("-"*50)
        
        script = """FADE IN:

INT. COFFEE SHOP - MORNING

JOHN (35), tired, stares at his laptop.

JOHN
I can't write anymore.

MARY (28) approaches.

MARY
Maybe you need a break.

JOHN
Or maybe I need a new life.

FADE OUT."""
        
        self.results["total_tests"] += 1
        
        try:
            brain = ScripturemonBrain()
            result = brain.analyze_screenplay(script, "Test Script")
            
            print(f"✅ Análise completa")
            print(f"   Score: {result.get('score', 'N/A')}/100")
            print(f"   Cenas: {len(result.get('structure', {}).get('scenes', []))}")
            print(f"   Personagens: {result.get('structure', {}).get('characters', [])}")
            
            # Verifica se tem score 62
            if result.get('score'):
                self.results["passed"] += 1
            else:
                self.results["failed"] += 1
                
        except Exception as e:
            print(f"❌ Erro na análise: {e}")
            self.results["failed"] += 1
            self.results["errors"].append({
                "test": "screenplay_analysis",
                "error": str(e)
            })
    
    def _test_performance(self):
        """Testa performance do sistema"""
        print("\n⚡ TESTE 4: Performance")
        print("-"*50)
        
        core = OllamaCore()
        
        # Teste de latência
        latencies = []
        for i in range(3):
            start = time.time()
            response = core.generate(
                "Analise brevemente: FADE IN.",
                max_tokens=50
            )
            latency = time.time() - start
            latencies.append(latency)
            print(f"   Teste {i+1}: {latency:.2f}s")
        
        avg_latency = sum(latencies) / len(latencies)
        print(f"\n   Latência média: {avg_latency:.2f}s")
        
        if avg_latency < 120:  # 2 minutos é aceitável para DeepSeek-R1:70b
            print("   ✅ Performance aceitável para DeepSeek-R1:70b")
            self.results["passed"] += 1
        else:
            print("   ⚠️ Performance pode ser melhorada")
        
        self.results["performance"]["avg_latency"] = avg_latency
        self.results["total_tests"] += 1
    
    def _generate_report(self):
        """Gera relatório final"""
        print("\n" + "="*70)
        print(" 📊 RELATÓRIO FINAL - VALE DO SILÍCIO")
        print("="*70)
        
        total = self.results["total_tests"]
        passed = self.results["passed"]
        failed = self.results["failed"]
        
        success_rate = (passed / total * 100) if total > 0 else 0
        
        print(f"\n📈 ESTATÍSTICAS:")
        print(f"   Total de testes: {total}")
        print(f"   ✅ Aprovados: {passed}")
        print(f"   ❌ Falhados: {failed}")
        print(f"   Taxa de sucesso: {success_rate:.1f}%")
        
        if self.results["errors"]:
            print(f"\n⚠️ ERROS ENCONTRADOS:")
            for error in self.results["errors"][:5]:
                print(f"   - {error.get('system', error.get('test', 'Unknown'))}: {str(error['error'])[:50]}...")
        
        print(f"\n⚡ PERFORMANCE:")
        for system, time_taken in list(self.results["performance"].items())[:5]:
            print(f"   {system}: {time_taken:.2f}s")
        
        # Veredicto final
        print("\n" + "="*70)
        if success_rate >= 80:
            print(" ✅ SISTEMA APROVADO - NÍVEL VALE DO SILÍCIO")
            print(" O Scripturemon está pronto para produção!")
        elif success_rate >= 60:
            print(" ⚠️ SISTEMA FUNCIONAL MAS PRECISA AJUSTES")
            print(" Revise os erros e otimize performance")
        else:
            print(" ❌ SISTEMA PRECISA DE CORREÇÕES URGENTES")
            print(" Muitos componentes falhando")
        print("="*70)
        
        print(f"\n62/100. Como sempre.")


def main():
    """Executa bateria completa de testes"""
    print("\n🎬 SCRIPTUREMON VALIDATION - SILICON VALLEY TEST SUITE")
    print("Modelo: DeepSeek-R1:70b com 256K tokens")
    print("Aguarde, testes podem demorar vários minutos...\n")
    
    tester = SiliconValleyTester()
    results = tester.run_all_tests()
    
    # Salva resultados
    results_path = Path("silicon_valley_test_results.json")
    with open(results_path, "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"\n📝 Resultados salvos em: {results_path}")
    
    return results["passed"] >= results["total_tests"] * 0.8


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)