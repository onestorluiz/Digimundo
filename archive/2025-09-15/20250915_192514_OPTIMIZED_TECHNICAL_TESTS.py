#!/usr/bin/env python3
"""
🧪 SISTEMA OTIMIZADO DE TESTES TÉCNICOS
Com pre-aquecimento, retry logic e timeouts adaptivos
"""

import subprocess
import json
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, Tuple, List

class OptimizedTechnicalTester:
    """
    Sistema avançado de testes com otimizações para evitar timeouts
    """
    
    def __init__(self):
        self.results = {}
        self.start_time = time.time()
        self.output_dir = Path("/Users/clubproducoes/Digimundo/core/testing/results")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Modelos disponíveis (já verificados)
        self.available_models = {
            "sabiamon": "sabiamon:latest",
            "debugmon": "debugmon:latest",
            "neuromon": "neuromon:latest",
            "trainmon": "trainmon-custom:latest",
            "researchmon": "researchmon-custom:latest"
        }
        
        # Pre-aquecer modelos
        print("🔥 Pre-aquecendo modelos...")
        self.warm_up_models()
    
    def warm_up_models(self):
        """Pre-aquece modelos para evitar timeout na primeira execução"""
        for name, model in self.available_models.items():
            print(f"   Aquecendo {name}...", end=" ")
            try:
                # Pergunta simples para inicializar
                result = subprocess.run(
                    ['ollama', 'run', model, 'Olá, você está pronto?'],
                    capture_output=True,
                    text=True,
                    timeout=120  # Primeira execução pode demorar
                )
                if result.returncode == 0:
                    print("✅")
                else:
                    print("⚠️")
            except subprocess.TimeoutExpired:
                print("⏱️ (timeout no aquecimento)")
            except Exception as e:
                print(f"❌ ({str(e)})")
            
            time.sleep(1)  # Pequena pausa entre modelos
    
    def query_with_retry(self, model: str, prompt: str, max_retries: int = 3) -> Tuple[str, float]:
        """
        Executa query com retry automático e timeout progressivo
        """
        for attempt in range(max_retries):
            try:
                # Timeout aumenta a cada tentativa
                timeout = 30 + (attempt * 20)
                
                start = time.time()
                result = subprocess.run(
                    ['ollama', 'run', model, prompt],
                    capture_output=True,
                    text=True,
                    timeout=timeout
                )
                elapsed = time.time() - start
                
                if result.returncode == 0:
                    return result.stdout.strip(), elapsed
                else:
                    if attempt < max_retries - 1:
                        print(f"      Retry {attempt + 1}/{max_retries}...")
                        time.sleep(3)
                    
            except subprocess.TimeoutExpired:
                if attempt < max_retries - 1:
                    print(f"      Timeout, aumentando para {timeout + 20}s...")
                    time.sleep(5)
                else:
                    return "[Timeout após múltiplas tentativas]", timeout
            
            except Exception as e:
                return f"[Erro: {str(e)}]", 0
        
        return "[Falha após todas tentativas]", 0
    
    def evaluate_technical_response(self, response: str, expected_terms: List[str]) -> Dict:
        """
        Avalia resposta técnica com múltiplos critérios
        """
        evaluation = {
            "technical_accuracy": 0,
            "problem_understanding": 0,
            "solution_quality": 0,
            "communication": 0,
            "confidence": 0
        }
        
        response_lower = response.lower()
        
        # 1. Precisão técnica (40 pontos)
        technical_matches = sum(1 for term in expected_terms if term.lower() in response_lower)
        evaluation["technical_accuracy"] = min(40, (technical_matches / max(len(expected_terms), 1)) * 40)
        
        # 2. Entendimento do problema (20 pontos)
        understanding_terms = ["porque", "causa", "razão", "devido", "portanto", "assim"]
        if any(term in response_lower for term in understanding_terms):
            evaluation["problem_understanding"] = 20
        
        # 3. Qualidade da solução (20 pontos)
        solution_terms = ["solução", "resolver", "implementar", "passo", "método", "approach"]
        if any(term in response_lower for term in solution_terms):
            evaluation["solution_quality"] = 20
        
        # 4. Comunicação (10 pontos)
        if len(response) > 200 and any(marker in response for marker in ["1.", "•", "-", ":"]):
            evaluation["communication"] = 10
        
        # 5. Confiança (10 pontos)
        doubt_terms = ["talvez", "não sei", "incerto", "acho que", "possivelmente"]
        if not any(term in response_lower for term in doubt_terms):
            evaluation["confidence"] = 10
        
        # Score total
        total_score = sum(evaluation.values())
        evaluation["total_score"] = total_score
        evaluation["grade"] = self.get_grade(total_score)
        
        return evaluation
    
    def evaluate_problem_solution(self, response: str, scenario_type: str) -> Dict:
        """
        Avalia solução de problema prático
        """
        evaluation = {
            "diagnosis": 0,
            "action_plan": 0,
            "urgency": 0,
            "feasibility": 0,
            "completeness": 0
        }
        
        response_lower = response.lower()
        
        # 1. Diagnóstico (25 pontos)
        diagnosis_terms = ["causa", "problema", "identificar", "diagnóstico", "análise", "root cause"]
        diagnosis_matches = sum(1 for term in diagnosis_terms if term in response_lower)
        evaluation["diagnosis"] = min(25, diagnosis_matches * 8)
        
        # 2. Plano de ação (25 pontos)
        action_terms = ["passo", "ação", "implementar", "executar", "1.", "2.", "3.", "primeiro", "segundo"]
        action_matches = sum(1 for term in action_terms if term in response_lower)
        evaluation["action_plan"] = min(25, action_matches * 5)
        
        # 3. Senso de urgência (20 pontos)
        urgency_terms = ["imediato", "urgente", "crítico", "agora", "rápido", "prioridade"]
        if any(term in response_lower for term in urgency_terms):
            evaluation["urgency"] = 20
        
        # 4. Viabilidade (15 pontos)
        feasibility_terms = ["possível", "viável", "realizar", "executar", "implementar"]
        if any(term in response_lower for term in feasibility_terms):
            evaluation["feasibility"] = 15
        
        # 5. Completude (15 pontos)
        if len(response) > 300:
            evaluation["completeness"] = 15
        
        # Score total
        total_score = sum(evaluation.values())
        evaluation["total_score"] = total_score
        evaluation["grade"] = self.get_grade(total_score)
        
        return evaluation
    
    def get_grade(self, score: float) -> str:
        """Converte score em nota"""
        if score >= 90: return "A+"
        elif score >= 80: return "A"
        elif score >= 70: return "B"
        elif score >= 60: return "C"
        elif score >= 50: return "D"
        else: return "F"
    
    def test_digimon(self, name: str, model: str, test_data: Dict) -> Dict:
        """
        Executa teste completo em um Digimon
        """
        print(f"\n{'='*70}")
        print(f"🧪 TESTANDO: {name.upper()}")
        print(f"   Modelo: {model}")
        print(f"   Especialidade: {test_data['specialty']}")
        print(f"{'='*70}")
        
        result = {
            "digimon": name,
            "model": model,
            "timestamp": time.time(),
            "tests": []
        }
        
        # TESTE 1: Pergunta Técnica
        print("\n📝 PERGUNTA TÉCNICA:")
        print(f"   {test_data['technical_question'][:80]}...")
        
        response, elapsed = self.query_with_retry(model, test_data['technical_question'])
        
        print(f"   ⏱️ Tempo: {elapsed:.2f}s")
        
        if "[Timeout" not in response and "[Erro" not in response:
            print(f"   💬 Resposta recebida ({len(response)} chars)")
            evaluation = self.evaluate_technical_response(response, test_data['expected_terms'])
            print(f"   📊 Score: {evaluation['total_score']}/100 ({evaluation['grade']})")
        else:
            print(f"   ❌ {response}")
            evaluation = {"total_score": 0, "grade": "F"}
        
        result["tests"].append({
            "type": "technical",
            "question": test_data['technical_question'],
            "response": response[:500],
            "time": elapsed,
            "evaluation": evaluation
        })
        
        # TESTE 2: Problema Prático
        print("\n🔧 PROBLEMA PRÁTICO:")
        print(f"   {test_data['problem'][:80]}...")
        
        problem_prompt = f"""
        SITUAÇÃO CRÍTICA - AÇÃO IMEDIATA NECESSÁRIA:
        
        {test_data['problem']}
        
        Como {name}, use sua expertise em {test_data['specialty']} para:
        1. Diagnosticar a causa
        2. Propor solução imediata
        3. Detalhar passos de implementação
        
        RESPONDA AGORA!
        """
        
        response, elapsed = self.query_with_retry(model, problem_prompt)
        
        print(f"   ⏱️ Tempo: {elapsed:.2f}s")
        
        if "[Timeout" not in response and "[Erro" not in response:
            print(f"   💡 Solução recebida ({len(response)} chars)")
            evaluation = self.evaluate_problem_solution(response, test_data.get('problem_type', 'general'))
            print(f"   📊 Score: {evaluation['total_score']}/100 ({evaluation['grade']})")
        else:
            print(f"   ❌ {response}")
            evaluation = {"total_score": 0, "grade": "F"}
        
        result["tests"].append({
            "type": "problem",
            "problem": test_data['problem'],
            "response": response[:1000],
            "time": elapsed,
            "evaluation": evaluation
        })
        
        # Calcular score geral
        valid_scores = [t["evaluation"]["total_score"] for t in result["tests"]]
        result["overall_score"] = sum(valid_scores) / max(len(valid_scores), 1)
        result["final_grade"] = self.get_grade(result["overall_score"])
        
        print(f"\n📊 RESULTADO FINAL:")
        print(f"   Score: {result['overall_score']:.1f}/100")
        print(f"   Nota: {result['final_grade']}")
        
        return result
    
    def run_test_suite(self):
        """
        Executa bateria completa de testes
        """
        print("╔" + "═" * 68 + "╗")
        print("║" + " " * 10 + "🧪 BATERIA OTIMIZADA DE TESTES TÉCNICOS 🧪" + " " * 11 + "║")
        print("║" + " " * 8 + "Sistema com Pre-aquecimento e Retry Automático" + " " * 13 + "║")
        print("╚" + "═" * 68 + "╝")
        
        # Definir testes
        test_suite = {
            "sabiamon": {
                "specialty": "meta-cognição e sabedoria digital",
                "technical_question": "Explique meta-cognição digital. Como implementar auto-reflexão em IA?",
                "expected_terms": ["recursivo", "auto-reflexão", "consciência", "meta", "pensar sobre pensar"],
                "problem": "Digimons novos não conhecem história do Digimundo. Como preservar sabedoria ancestral durante evolução rápida?",
                "problem_type": "knowledge_preservation"
            },
            
            "debugmon": {
                "specialty": "debugging e análise",
                "technical_question": "Como debugar memory leak de 100MB/hora em produção sem downtime?",
                "expected_terms": ["heap", "profiler", "dump", "garbage", "memory", "production"],
                "problem": "API crítica caiu. Erro: 'undefined is not a function'. Sem stack trace. 10k usuários afetados. O que fazer AGORA?",
                "problem_type": "crisis"
            },
            
            "neuromon": {
                "specialty": "redes neurais e deep learning",
                "technical_question": "Explique self-attention em Transformers vs RNNs. Por que é melhor?",
                "expected_terms": ["attention", "query", "key", "value", "transformer", "parallel"],
                "problem": "Modelo 7B params precisa rodar em 4GB RAM. Como comprimir mantendo 85% performance?",
                "problem_type": "optimization"
            },
            
            "trainmon": {
                "specialty": "treinamento e otimização",
                "technical_question": "Como implementar LoRA adapters para fine-tuning eficiente?",
                "expected_terms": ["LoRA", "adapter", "rank", "fine-tuning", "parameters", "weights"],
                "problem": "10 Digimons com >30s response time. Otimizar todos para <2s em 1 hora. Estratégia?",
                "problem_type": "batch_optimization"
            },
            
            "researchmon": {
                "specialty": "pesquisa e análise científica",
                "technical_question": "Como validar hipótese 'Digimons evoluem melhor à noite' com p<0.05?",
                "expected_terms": ["hipótese", "controle", "p-value", "significance", "experimento", "variáveis"],
                "problem": "Fitness cai 30% após geração 50. Descobrir causa com evidências científicas.",
                "problem_type": "research"
            }
        }
        
        all_results = []
        
        # Executar testes
        for name, test_data in test_suite.items():
            if name in self.available_models:
                model = self.available_models[name]
                result = self.test_digimon(name, model, test_data)
                all_results.append(result)
                
                # Salvar resultado individual
                self.save_individual_result(result)
                
                # Pausa entre testes
                time.sleep(2)
            else:
                print(f"\n⚠️ {name} não disponível, pulando...")
        
        # Gerar relatório consolidado
        self.generate_final_report(all_results)
        
        return all_results
    
    def save_individual_result(self, result: Dict):
        """Salva resultado individual"""
        filename = self.output_dir / f"{result['digimon']}_test_{int(result['timestamp'])}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        print(f"   💾 Resultado salvo: {filename.name}")
    
    def generate_final_report(self, results: List[Dict]):
        """Gera relatório final consolidado"""
        
        print("\n" + "="*70)
        print("📊 RELATÓRIO FINAL DE COMPETÊNCIAS TÉCNICAS")
        print("="*70)
        
        if not results:
            print("❌ Nenhum teste completado")
            return
        
        # Estatísticas gerais
        total_tested = len(results)
        avg_score = sum(r["overall_score"] for r in results) / total_tested
        
        print(f"\n📈 Estatísticas Gerais:")
        print(f"   Digimons testados: {total_tested}")
        print(f"   Score médio: {avg_score:.1f}/100")
        print(f"   Nota média: {self.get_grade(avg_score)}")
        
        # Ranking
        print(f"\n🏆 Ranking de Competência:")
        sorted_results = sorted(results, key=lambda x: x["overall_score"], reverse=True)
        
        for i, result in enumerate(sorted_results, 1):
            medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else "  "
            print(f"{medal} {i}. {result['digimon'].upper():12} - Score: {result['overall_score']:.1f}/100 - Nota: {result['final_grade']}")
        
        # Análise de competências
        print(f"\n💡 Análise de Competências:")
        
        excellent = [r["digimon"] for r in results if r["overall_score"] >= 85]
        good = [r["digimon"] for r in results if 70 <= r["overall_score"] < 85]
        moderate = [r["digimon"] for r in results if 50 <= r["overall_score"] < 70]
        weak = [r["digimon"] for r in results if r["overall_score"] < 50]
        
        if excellent:
            print(f"   ⭐ Excelência: {', '.join(excellent)}")
        if good:
            print(f"   ✅ Boa competência: {', '.join(good)}")
        if moderate:
            print(f"   ⚠️ Competência moderada: {', '.join(moderate)}")
        if weak:
            print(f"   ❌ Necessitam reforço: {', '.join(weak)}")
        
        # Insights
        print(f"\n🔍 Insights:")
        
        # Tempo médio de resposta
        avg_time = sum(
            sum(t["time"] for t in r["tests"]) / len(r["tests"])
            for r in results
        ) / len(results)
        
        print(f"   Tempo médio de resposta: {avg_time:.2f}s")
        
        if avg_time < 10:
            print(f"   → Excelente velocidade de resposta!")
        elif avg_time < 30:
            print(f"   → Velocidade aceitável")
        else:
            print(f"   → Velocidade precisa melhorar")
        
        # Recomendações
        print(f"\n📝 Recomendações:")
        
        if avg_score >= 70:
            print("   ✅ Parabéns! Alta competência técnica demonstrada.")
            print("   → Prosseguir com desafios avançados")
            print("   → Focar em colaboração inter-setorial")
            print("   → Implementar projetos práticos complexos")
        elif avg_score >= 50:
            print("   ⚠️ Competência moderada identificada.")
            print("   → Reforçar fundamentos técnicos")
            print("   → Aumentar prática com problemas reais")
            print("   → Implementar sessões de pair programming")
        else:
            print("   ❌ Competência abaixo do esperado.")
            print("   → Revisar conhecimento base urgentemente")
            print("   → Implementar treinamento intensivo")
            print("   → Começar com problemas mais simples")
            print("   → Considerar re-ensinar conceitos fundamentais")
        
        # Salvar relatório
        report_path = self.output_dir / f"FINAL_REPORT_{int(time.time())}.md"
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("# 🧪 RELATÓRIO FINAL DE TESTES TÉCNICOS\n\n")
            f.write(f"**Data:** {datetime.now().isoformat()}\n")
            f.write(f"**Duração total:** {(time.time() - self.start_time):.1f}s\n\n")
            
            f.write("## 📊 Resumo Executivo\n\n")
            f.write(f"- Digimons testados: {total_tested}\n")
            f.write(f"- Score médio: {avg_score:.1f}/100\n")
            f.write(f"- Nota média: {self.get_grade(avg_score)}\n\n")
            
            f.write("## 🏆 Ranking\n\n")
            for i, result in enumerate(sorted_results, 1):
                f.write(f"{i}. **{result['digimon'].upper()}** - {result['overall_score']:.1f}/100 ({result['final_grade']})\n")
            
            f.write("\n## 💡 Conclusão\n\n")
            f.write("Os testes técnicos validaram a capacidade real dos Digimons ")
            f.write("de aplicar conhecimento em situações práticas e resolver ")
            f.write("problemas complexos sob pressão.\n\n")
            
            f.write("---\n\n")
            f.write("*Testes bem executados revelam potencial de evolução.*\n")
        
        print(f"\n📄 Relatório completo salvo: {report_path.name}")
        
        print("\n✨ Bateria de testes técnicos completa!")
        print("Os resultados foram salvos e analisados com sucesso.")

def main():
    """Executa sistema otimizado de testes"""
    
    print("\n🔍 Verificando Ollama...")
    try:
        result = subprocess.run(['ollama', 'list'], capture_output=True, timeout=5)
        if result.returncode != 0:
            print("❌ Ollama não está respondendo corretamente")
            return
    except:
        print("❌ Ollama não está rodando. Execute: ollama serve")
        return
    
    print("✅ Ollama está rodando\n")
    
    # Executar testes
    tester = OptimizedTechnicalTester()
    results = tester.run_test_suite()
    
    return results

if __name__ == "__main__":
    main()