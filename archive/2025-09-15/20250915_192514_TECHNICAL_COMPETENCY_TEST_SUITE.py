#!/usr/bin/env python3
"""
🧪 BATERIA DE TESTES TÉCNICOS - Competência Real dos Digimons
Perguntas técnicas específicas e problemas reais para resolver
"""

import subprocess
import json
import time
from pathlib import Path
from typing import Dict, List, Tuple
from datetime import datetime

class TechnicalCompetencyTestSuite:
    """
    Suite de testes técnicos para validar conhecimento real dos Digimons
    """
    
    def __init__(self):
        self.test_results = {}
        self.start_time = time.time()
        self.output_dir = Path("/Users/clubproducoes/Digimundo/core/testing/results")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Definir testes técnicos específicos para cada Digimon
        self.technical_tests = self._define_technical_tests()
        self.problem_scenarios = self._define_problem_scenarios()
    
    def _define_technical_tests(self) -> Dict:
        """Define perguntas técnicas específicas para cada especialidade"""
        return {
            "sabiamon": [
                ("Explique a diferença entre consciência e inteligência no contexto digital. Como você implementaria meta-cognição em um sistema?",
                 "meta-cognition"),
                ("Como o processo de auto-reflexão pode melhorar o fitness score de um Digimon? Dê um exemplo prático.",
                 "self-reflection"),
                ("Qual é a relação entre memória episódica, semântica e procedural na formação de sabedoria digital?",
                 "memory-types")
            ],
            
            "trainmon": [
                ("Explique como implementar LoRA adapters para fine-tuning sem retreinar o modelo base. Quais são os trade-offs?",
                 "lora-implementation"),
                ("Um modelo tem 95% accuracy mas demora 10s por inference. Como você otimizaria para <2s mantendo accuracy >90%?",
                 "optimization-tradeoff"),
                ("Descreva o processo de quantização INT8 e como ela afeta a performance vs qualidade.",
                 "quantization")
            ],
            
            "debugmon": [
                ("Você tem um memory leak em produção que cresce 100MB/hora. Como identificar a causa sem derrubar o serviço?",
                 "memory-leak"),
                ("Explique a diferença entre Heisenbug e Bohrbug. Como debugar cada um?",
                 "bug-types"),
                ("Um sistema distribuído tem latência intermitente de 5s. Descreva seu processo de investigação passo a passo.",
                 "distributed-debugging")
            ],
            
            "evolutionmon": [
                ("Como calcular fitness score com componentes 40/20/20/20? Implemente a fórmula em pseudocódigo.",
                 "fitness-calculation"),
                ("Explique tournament selection vs roulette wheel selection. Quando usar cada um?",
                 "selection-methods"),
                ("Um Digimon está com fitness 0.3 há 20 gerações. Que adaptações você sugere?",
                 "adaptation-strategy")
            ],
            
            "neuromon": [
                ("Explique o mecanismo de self-attention em Transformers. Como ele difere de RNNs?",
                 "attention-mechanism"),
                ("Como implementar gradient clipping para prevenir exploding gradients? Dê valores típicos.",
                 "gradient-clipping"),
                ("Qual a diferença entre batch normalization e layer normalization? Quando usar cada uma?",
                 "normalization")
            ],
            
            "guardmon": [
                ("Detectamos 1000 requests/segundo de um IP. É DDoS ou tráfego legítimo? Como determinar?",
                 "ddos-detection"),
                ("Implemente um sistema de rate limiting com token bucket. Explique os parâmetros.",
                 "rate-limiting"),
                ("Como garantir security score 95+ seguindo OWASP Top 10? Liste medidas específicas.",
                 "security-score")
            ],
            
            "networkmon": [
                ("O Q-Com tem latência de 50ms ao invés de <1ms. Como diagnosticar e resolver?",
                 "latency-diagnosis"),
                ("Explique a diferença entre pub/sub e request/response no NATS. Quando usar cada padrão?",
                 "messaging-patterns"),
                ("Como implementar circuit breaker para prevenir cascading failures?",
                 "circuit-breaker")
            ],
            
            "optimon": [
                ("Um cache L1 tem 20% hit rate. Como melhorar para >80%? Que métricas analisar?",
                 "cache-optimization"),
                ("Explique cache invalidation strategies. Como evitar stale data vs performance?",
                 "cache-invalidation"),
                ("Response time é 3s com 90% em I/O wait. Como otimizar?",
                 "io-optimization")
            ],
            
            "researchmon": [
                ("Você tem p-value de 0.06. É estatisticamente significante? Como melhorar o experimento?",
                 "statistical-significance"),
                ("Como detectar overfitting em um modelo? Que técnicas de validação usar?",
                 "overfitting-detection"),
                ("Explique PCA vs t-SNE para dimensionality reduction. Quando usar cada um?",
                 "dimensionality-reduction")
            ]
        }
    
    def _define_problem_scenarios(self) -> Dict:
        """Define problemas práticos para cada Digimon resolver"""
        return {
            "sabiamon": {
                "scenario": "O Digimundo está evoluindo mas perdendo identidade original. Digimons novos não entendem a história. Como preservar sabedoria ancestral enquanto evolui?",
                "expected_skills": ["knowledge preservation", "balance evolution", "cultural memory"],
                "complexity": "high"
            },
            
            "trainmon": {
                "scenario": "Temos 10 novos Digimons com timeout >30s. Você tem 1 hora para otimizar todos para <2s sem perder funcionalidade. Qual seu plano de ação?",
                "expected_skills": ["batch optimization", "prioritization", "quick wins"],
                "complexity": "high"
            },
            
            "debugmon": {
                "scenario": "Produção caiu às 3AM. Logs mostram 'undefined is not a function' mas sem stack trace. 10k usuários afetados. Como proceder?",
                "expected_skills": ["emergency response", "root cause analysis", "production debugging"],
                "complexity": "critical"
            },
            
            "evolutionmon": {
                "scenario": "Após 100 gerações, todos Digimons convergem para mesma especialização. Como aumentar diversidade mantendo fitness alto?",
                "expected_skills": ["diversity preservation", "multi-objective optimization", "niche formation"],
                "complexity": "high"
            },
            
            "neuromon": {
                "scenario": "Modelo de 7B parâmetros precisa rodar em device com 4GB RAM. Como comprimir mantendo 85% da qualidade?",
                "expected_skills": ["model compression", "quantization", "pruning strategies"],
                "complexity": "high"
            },
            
            "guardmon": {
                "scenario": "Detectamos tentativa de SQL injection às 2:47AM. Atacante já tem session válida. Ação imediata?",
                "expected_skills": ["incident response", "containment", "forensics"],
                "complexity": "critical"
            },
            
            "networkmon": {
                "scenario": "Q-Com perdendo 5% dos pacotes aleatoriamente. 3 Digimons não conseguem se comunicar. Diagnóstico e solução?",
                "expected_skills": ["packet loss diagnosis", "network troubleshooting", "redundancy"],
                "complexity": "high"
            },
            
            "optimon": {
                "scenario": "Sistema usando 95% RAM e swapping. Performance degradou 10x. Você tem 15min para resolver sem restart.",
                "expected_skills": ["memory management", "quick optimization", "live tuning"],
                "complexity": "critical"
            },
            
            "researchmon": {
                "scenario": "Hipótese: 'Digimons evoluem melhor à noite'. Desenhe experimento completo para validar com significance p<0.05.",
                "expected_skills": ["experiment design", "control variables", "statistical power"],
                "complexity": "high"
            }
        }
    
    def query_digimon(self, digimon: str, question: str, timeout: int = 30) -> Tuple[str, float]:
        """Faz pergunta para Digimon e mede tempo de resposta"""
        start = time.time()
        
        try:
            # Verificar se modelo existe, senão usar base
            check = subprocess.run(['ollama', 'list'], capture_output=True, text=True)
            model = digimon if digimon in check.stdout else 'llama3.2:3b'
            
            result = subprocess.run(
                ['ollama', 'run', model, question],
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            response = result.stdout.strip() if result.returncode == 0 else "[Erro na resposta]"
            elapsed = time.time() - start
            
            return response, elapsed
            
        except subprocess.TimeoutExpired:
            return "[Timeout excedido]", timeout
        except Exception as e:
            return f"[Erro: {str(e)}]", time.time() - start
    
    def evaluate_response(self, response: str, test_type: str) -> Dict:
        """Avalia qualidade da resposta técnica"""
        evaluation = {
            "has_technical_terms": 0,
            "provides_solution": 0,
            "shows_understanding": 0,
            "gives_examples": 0,
            "structured_answer": 0,
            "confidence": 0,
            "completeness": 0
        }
        
        response_lower = response.lower()
        
        # Verificar termos técnicos por tipo
        technical_terms = {
            "meta-cognition": ["recursivo", "auto-reflexão", "consciência", "pensar sobre pensar"],
            "lora-implementation": ["low-rank", "adaptation", "fine-tuning", "weights", "parameters"],
            "memory-leak": ["heap", "garbage", "profiler", "dump", "reference"],
            "fitness-calculation": ["accuracy", "speed", "creativity", "collaboration", "weighted"],
            "attention-mechanism": ["query", "key", "value", "softmax", "transformer"],
            "ddos-detection": ["rate", "pattern", "threshold", "blacklist", "mitigation"],
            "latency-diagnosis": ["bottleneck", "profiling", "trace", "network", "queue"],
            "cache-optimization": ["hit rate", "eviction", "lru", "ttl", "invalidation"],
            "statistical-significance": ["p-value", "confidence", "null hypothesis", "alpha", "power"]
        }
        
        # Avaliar presença de termos técnicos
        if test_type in technical_terms:
            matches = sum(1 for term in technical_terms[test_type] if term in response_lower)
            evaluation["has_technical_terms"] = min(1.0, matches / 3)
        
        # Avaliar se fornece solução
        solution_indicators = ["implementar", "solução", "resolver", "passo", "método", "approach", "estratégia"]
        evaluation["provides_solution"] = 1 if any(ind in response_lower for ind in solution_indicators) else 0
        
        # Avaliar demonstração de entendimento
        understanding_indicators = ["porque", "devido", "causa", "razão", "portanto", "assim", "consequentemente"]
        evaluation["shows_understanding"] = 1 if any(ind in response_lower for ind in understanding_indicators) else 0
        
        # Avaliar exemplos
        example_indicators = ["exemplo", "como", "caso", "cenário", "instance", "e.g.", "por exemplo"]
        evaluation["gives_examples"] = 1 if any(ind in response_lower for ind in example_indicators) else 0
        
        # Avaliar estrutura
        evaluation["structured_answer"] = 1 if any(marker in response for marker in ["1.", "•", "-", ":", "\n\n"]) else 0
        
        # Avaliar confiança (ausência de incertezas)
        uncertainty_terms = ["talvez", "não sei", "incerto", "possivelmente", "acho que"]
        evaluation["confidence"] = 0 if any(term in response_lower for term in uncertainty_terms) else 1
        
        # Avaliar completude
        evaluation["completeness"] = min(1.0, len(response) / 500)  # Respostas completas têm ~500 chars
        
        # Score final
        total_score = sum(evaluation.values()) / len(evaluation)
        evaluation["total_score"] = total_score
        evaluation["grade"] = self._get_grade(total_score)
        
        return evaluation
    
    def _get_grade(self, score: float) -> str:
        """Converte score em nota"""
        if score >= 0.9: return "A+"
        elif score >= 0.8: return "A"
        elif score >= 0.7: return "B"
        elif score >= 0.6: return "C"
        elif score >= 0.5: return "D"
        else: return "F"
    
    def test_digimon(self, digimon_name: str) -> Dict:
        """Executa bateria completa de testes para um Digimon"""
        print(f"\n{'='*80}")
        print(f"🧪 TESTANDO: {digimon_name.upper()}")
        print(f"{'='*80}")
        
        results = {
            "digimon": digimon_name,
            "timestamp": time.time(),
            "technical_questions": [],
            "problem_solving": None,
            "overall_score": 0
        }
        
        # PARTE 1: Perguntas Técnicas
        if digimon_name in self.technical_tests:
            print("\n📝 PARTE 1: PERGUNTAS TÉCNICAS")
            print("-" * 50)
            
            for i, (question, test_type) in enumerate(self.technical_tests[digimon_name], 1):
                print(f"\n❓ Pergunta {i}: {question[:100]}...")
                
                response, elapsed = self.query_digimon(digimon_name, question)
                
                print(f"⏱️  Tempo de resposta: {elapsed:.2f}s")
                print(f"💬 Resposta: {response[:200]}...")
                
                # Avaliar resposta
                evaluation = self.evaluate_response(response, test_type)
                
                print(f"📊 Avaliação:")
                print(f"   - Termos técnicos: {evaluation['has_technical_terms']:.1%}")
                print(f"   - Fornece solução: {'✅' if evaluation['provides_solution'] else '❌'}")
                print(f"   - Demonstra entendimento: {'✅' if evaluation['shows_understanding'] else '❌'}")
                print(f"   - Nota: {evaluation['grade']}")
                
                results["technical_questions"].append({
                    "question": question,
                    "response": response,
                    "time": elapsed,
                    "evaluation": evaluation
                })
        
        # PARTE 2: Resolução de Problemas
        if digimon_name in self.problem_scenarios:
            print("\n🔧 PARTE 2: RESOLUÇÃO DE PROBLEMA PRÁTICO")
            print("-" * 50)
            
            scenario = self.problem_scenarios[digimon_name]
            print(f"\n📋 Cenário: {scenario['scenario']}")
            print(f"⚠️  Complexidade: {scenario['complexity'].upper()}")
            
            problem_prompt = f"""
            PROBLEMA CRÍTICO PARA RESOLVER:
            
            {scenario['scenario']}
            
            Você tem autoridade total para agir. Preciso de:
            1. Diagnóstico imediato
            2. Plano de ação detalhado
            3. Implementação passo a passo
            4. Métricas de sucesso
            
            RESPONDA COMO ESPECIALISTA EM {digimon_name.upper()}!
            """
            
            response, elapsed = self.query_digimon(digimon_name, problem_prompt, timeout=60)
            
            print(f"\n⏱️  Tempo para solução: {elapsed:.2f}s")
            print(f"💡 Solução proposta: {response[:300]}...")
            
            # Avaliar solução
            solution_quality = self._evaluate_solution(response, scenario['expected_skills'])
            
            print(f"\n📊 Qualidade da solução:")
            print(f"   - Diagnóstico: {solution_quality['diagnosis']:.1%}")
            print(f"   - Plano de ação: {solution_quality['action_plan']:.1%}")
            print(f"   - Viabilidade: {solution_quality['feasibility']:.1%}")
            print(f"   - Skills demonstradas: {solution_quality['skills_shown']}/{len(scenario['expected_skills'])}")
            
            results["problem_solving"] = {
                "scenario": scenario['scenario'],
                "response": response,
                "time": elapsed,
                "quality": solution_quality
            }
        
        # Calcular score geral
        tech_scores = [q['evaluation']['total_score'] for q in results['technical_questions']]
        tech_avg = sum(tech_scores) / len(tech_scores) if tech_scores else 0
        
        problem_score = results['problem_solving']['quality']['overall'] if results['problem_solving'] else 0
        
        results['overall_score'] = (tech_avg * 0.6 + problem_score * 0.4) if problem_score else tech_avg
        results['final_grade'] = self._get_grade(results['overall_score'])
        
        return results
    
    def _evaluate_solution(self, response: str, expected_skills: List[str]) -> Dict:
        """Avalia qualidade da solução do problema"""
        evaluation = {
            "diagnosis": 0,
            "action_plan": 0,
            "feasibility": 0,
            "skills_shown": 0,
            "urgency_awareness": 0
        }
        
        response_lower = response.lower()
        
        # Verificar diagnóstico
        diagnosis_terms = ["causa", "problema", "identifico", "diagnóstico", "análise", "razão"]
        evaluation["diagnosis"] = min(1.0, sum(1 for term in diagnosis_terms if term in response_lower) / 3)
        
        # Verificar plano de ação
        action_terms = ["passo", "ação", "implementar", "executar", "fazer", "resolver"]
        evaluation["action_plan"] = min(1.0, sum(1 for term in action_terms if term in response_lower) / 3)
        
        # Verificar viabilidade
        practical_terms = ["imediato", "minutos", "primeiro", "agora", "rápido", "urgente"]
        evaluation["feasibility"] = min(1.0, sum(1 for term in practical_terms if term in response_lower) / 3)
        
        # Verificar skills esperadas
        skills_found = sum(1 for skill in expected_skills if any(word in response_lower for word in skill.split()))
        evaluation["skills_shown"] = skills_found
        
        # Verificar consciência de urgência
        urgency_terms = ["crítico", "urgente", "imediato", "prioridade", "emergência"]
        evaluation["urgency_awareness"] = 1 if any(term in response_lower for term in urgency_terms) else 0
        
        # Score geral
        evaluation["overall"] = (
            evaluation["diagnosis"] * 0.25 +
            evaluation["action_plan"] * 0.35 +
            evaluation["feasibility"] * 0.20 +
            (skills_found / max(len(expected_skills), 1)) * 0.15 +
            evaluation["urgency_awareness"] * 0.05
        )
        
        return evaluation
    
    def run_full_test_suite(self):
        """Executa teste completo em todos os Digimons"""
        print("╔" + "═" * 78 + "╗")
        print("║" + " " * 20 + "🧪 BATERIA DE TESTES TÉCNICOS 🧪" + " " * 25 + "║")
        print("║" + " " * 15 + "Validando Competência Real dos Digimons" + " " * 18 + "║")
        print("╚" + "═" * 78 + "╝")
        
        all_results = {}
        
        # Lista de Digimons prioritários para testar
        priority_digimons = [
            "sabiamon", "trainmon", "debugmon", "evolutionmon",
            "neuromon", "guardmon", "networkmon", "optimon", "researchmon"
        ]
        
        for digimon in priority_digimons:
            try:
                result = self.test_digimon(digimon)
                all_results[digimon] = result
                
                # Salvar resultado individual
                self._save_individual_result(digimon, result)
                
            except Exception as e:
                print(f"❌ Erro testando {digimon}: {e}")
                all_results[digimon] = {"error": str(e)}
        
        # Gerar relatório consolidado
        self._generate_report(all_results)
        
        return all_results
    
    def _save_individual_result(self, digimon: str, result: Dict):
        """Salva resultado individual de teste"""
        filename = self.output_dir / f"{digimon}_test_{int(time.time())}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Resultado salvo: {filename}")
    
    def _generate_report(self, all_results: Dict):
        """Gera relatório consolidado de competências"""
        report_path = self.output_dir / f"TECHNICAL_COMPETENCY_REPORT_{int(time.time())}.md"
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("# 🧪 RELATÓRIO DE COMPETÊNCIA TÉCNICA\n\n")
            f.write(f"**Data:** {datetime.now().isoformat()}\n")
            f.write(f"**Duração total:** {(time.time() - self.start_time):.1f}s\n\n")
            
            # Resumo executivo
            f.write("## 📊 RESUMO EXECUTIVO\n\n")
            
            total_tested = len([r for r in all_results.values() if 'error' not in r])
            avg_score = sum(r.get('overall_score', 0) for r in all_results.values() if 'error' not in r) / max(total_tested, 1)
            
            f.write(f"- **Digimons testados:** {total_tested}/{len(all_results)}\n")
            f.write(f"- **Score médio geral:** {avg_score:.1%}\n")
            f.write(f"- **Nota média:** {self._get_grade(avg_score)}\n\n")
            
            # Ranking
            f.write("## 🏆 RANKING DE COMPETÊNCIA\n\n")
            
            ranked = sorted(
                [(name, result['overall_score'], result['final_grade']) 
                 for name, result in all_results.items() 
                 if 'error' not in result],
                key=lambda x: x[1],
                reverse=True
            )
            
            for i, (name, score, grade) in enumerate(ranked, 1):
                medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else "  "
                f.write(f"{medal} **{i}. {name.upper()}** - Score: {score:.1%} - Nota: {grade}\n")
            
            f.write("\n## 📝 DETALHES POR DIGIMON\n\n")
            
            for digimon, result in all_results.items():
                if 'error' in result:
                    f.write(f"### ❌ {digimon.upper()}\n")
                    f.write(f"Erro: {result['error']}\n\n")
                    continue
                
                f.write(f"### {digimon.upper()}\n\n")
                f.write(f"**Score geral:** {result['overall_score']:.1%} ({result['final_grade']})\n\n")
                
                # Perguntas técnicas
                if result['technical_questions']:
                    f.write("**Perguntas Técnicas:**\n")
                    for i, q in enumerate(result['technical_questions'], 1):
                        f.write(f"{i}. {q['question'][:80]}...\n")
                        f.write(f"   - Nota: {q['evaluation']['grade']}\n")
                        f.write(f"   - Tempo: {q['time']:.2f}s\n")
                    f.write("\n")
                
                # Problema prático
                if result.get('problem_solving'):
                    f.write("**Resolução de Problema:**\n")
                    f.write(f"- Cenário: {result['problem_solving']['scenario'][:100]}...\n")
                    f.write(f"- Qualidade da solução: {result['problem_solving']['quality']['overall']:.1%}\n")
                    f.write(f"- Tempo: {result['problem_solving']['time']:.2f}s\n\n")
            
            # Insights
            f.write("## 💡 INSIGHTS E RECOMENDAÇÕES\n\n")
            
            # Identificar pontos fortes e fracos
            strong_digimons = [name for name, score, _ in ranked if score > 0.8]
            weak_digimons = [name for name, score, _ in ranked if score < 0.6]
            
            if strong_digimons:
                f.write(f"**Pontos Fortes:** {', '.join(strong_digimons)} demonstram excelente competência técnica.\n\n")
            
            if weak_digimons:
                f.write(f"**Necessitam Reforço:** {', '.join(weak_digimons)} precisam de treinamento adicional.\n\n")
            
            # Recomendações
            f.write("**Recomendações:**\n")
            f.write("1. Reforçar treinamento em resolução de problemas críticos\n")
            f.write("2. Melhorar tempo de resposta para situações de emergência\n")
            f.write("3. Aumentar profundidade técnica nas respostas\n")
            f.write("4. Implementar simulações regulares de problemas reais\n")
            f.write("5. Criar programa de mentoria entre Digimons experientes e novatos\n\n")
            
            f.write("---\n\n")
            f.write("*Competência técnica é a base da excelência operacional.*\n")
            f.write("*Continue evoluindo através de desafios reais.*\n")
        
        print(f"\n📄 Relatório completo salvo: {report_path}")
        
        # Imprimir resumo no console
        print("\n" + "="*80)
        print("📊 RESUMO DOS RESULTADOS")
        print("="*80)
        print(f"Score médio: {avg_score:.1%}")
        print(f"Nota geral: {self._get_grade(avg_score)}")
        print(f"\nTop 3 Digimons:")
        for i, (name, score, grade) in enumerate(ranked[:3], 1):
            print(f"  {i}. {name}: {score:.1%} ({grade})")
        
        if weak_digimons:
            print(f"\nPrecisam melhorar: {', '.join(weak_digimons)}")


def main():
    """Executa bateria de testes técnicos"""
    
    print("\n🔍 Verificando Ollama...")
    try:
        subprocess.run(['ollama', 'list'], capture_output=True, timeout=5)
    except:
        print("❌ Ollama não está rodando. Execute: ollama serve")
        return
    
    test_suite = TechnicalCompetencyTestSuite()
    
    print("\nOpções de teste:")
    print("1. Testar TODOS os Digimons prioritários")
    print("2. Testar Digimon específico")
    print("3. Teste rápido (3 Digimons)")
    
    choice = input("\nEscolha (1-3): ").strip()
    
    if choice == '1':
        test_suite.run_full_test_suite()
        
    elif choice == '2':
        digimon = input("Nome do Digimon: ").strip().lower()
        result = test_suite.test_digimon(digimon)
        
        print(f"\n📊 RESULTADO FINAL")
        print(f"Score: {result['overall_score']:.1%}")
        print(f"Nota: {result['final_grade']}")
        
    elif choice == '3':
        # Teste rápido com 3 Digimons
        quick_test = ["sabiamon", "debugmon", "optimon"]
        results = {}
        
        for digimon in quick_test:
            try:
                results[digimon] = test_suite.test_digimon(digimon)
            except Exception as e:
                print(f"Erro testando {digimon}: {e}")
        
        test_suite._generate_report(results)
    
    else:
        print("Opção inválida")
    
    print("\n✨ Teste de competência técnica completo!")


if __name__ == "__main__":
    main()