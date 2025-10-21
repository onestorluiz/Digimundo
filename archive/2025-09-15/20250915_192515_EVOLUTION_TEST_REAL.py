#!/usr/bin/env python3
"""
🧬 TESTE DE EVOLUÇÃO REAL - Sistema Completo
Testa evolução de um Digimon com toda complexidade implementada
"""

import sys
import time
import json
import subprocess
from pathlib import Path
from typing import Dict, List

# Adicionar paths necessários
sys.path.append('/Users/clubproducoes/Digimundo/core/memory')
sys.path.append('/Users/clubproducoes/Digimundo/core/evolution')

from intelligence_core import IntelligenceCore, FitnessCalculator
from ollama_connector import OllamaConnector
from cognitive_core import CognitiveCore


class EvolutionTestSuite:
    """
    Suite de testes para evolução real de Digimons
    """
    
    def __init__(self):
        print("🧬 INICIALIZANDO TESTE DE EVOLUÇÃO REAL")
        print("=" * 70)
        
        # Instalar dependências se necessário
        self._ensure_dependencies()
        
        # Inicializar componentes
        print("\n📦 Inicializando componentes...")
        self.intelligence = IntelligenceCore()
        self.connector = OllamaConnector()
        self.fitness_calc = FitnessCalculator()
        
        # Verificar Ollama
        self._check_ollama()
        
        # Métricas do teste
        self.test_metrics = {
            'start_time': time.time(),
            'interactions': [],
            'evolution_events': [],
            'fitness_progression': []
        }
    
    def _ensure_dependencies(self):
        """Garante que dependências estão instaladas"""
        try:
            import psutil
        except ImportError:
            print("📦 Instalando psutil...")
            subprocess.run([
                'pip3', 'install', '--user', 
                '--break-system-packages', 'psutil'
            ])
    
    def _check_ollama(self):
        """Verifica se Ollama está rodando e tem modelos"""
        try:
            result = subprocess.run(
                ['ollama', 'list'],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode != 0:
                print("⚠️  Ollama não está respondendo. Tentando iniciar...")
                subprocess.Popen(['ollama', 'serve'], 
                               stdout=subprocess.DEVNULL,
                               stderr=subprocess.DEVNULL)
                time.sleep(3)
            
            # Verificar se tem o modelo base
            if 'llama3.2:3b' not in result.stdout:
                print("📥 Baixando modelo base llama3.2:3b...")
                subprocess.run(['ollama', 'pull', 'llama3.2:3b'])
                
        except Exception as e:
            print(f"⚠️  Aviso Ollama: {e}")
    
    def run_evolution_cycle(self, digimon_name: str, num_interactions: int = 20):
        """
        Executa ciclo completo de evolução
        """
        print(f"\n🎮 INICIANDO CICLO DE EVOLUÇÃO PARA {digimon_name.upper()}")
        print("-" * 70)
        
        # Queries de teste variadas para estimular evolução
        test_queries = [
            # Técnicas
            ("Explique o que é recursão em programação", "technical"),
            ("Como funciona uma árvore binária?", "technical"),
            ("O que é um algoritmo de ordenação?", "technical"),
            
            # Criativas
            ("Invente um nome para um novo Digimon", "creative"),
            ("Crie uma história curta sobre evolução digital", "creative"),
            
            # Analíticas
            ("Analise os prós e contras de IA", "analysis"),
            ("Compare Python e JavaScript", "analysis"),
            
            # Colaborativas
            ("Como você e outros Digimons podem trabalhar juntos?", "collaboration"),
            ("Que habilidades Trainmon poderia te ensinar?", "collaboration"),
            
            # Educacionais
            ("Ensine-me sobre o Digimundo", "teaching"),
            ("Como posso começar a programar?", "teaching"),
            
            # Mistas
            ("Crie um código Python simples", "coding"),
            ("Debugue este código: def fib(n): return fib(n-1) + fib(n-2)", "coding"),
            ("O que é machine learning?", "technical"),
            ("Qual a diferença entre lista e tupla em Python?", "technical"),
            
            # Evolução e meta-cognição  
            ("Como você está evoluindo?", "meta"),
            ("Quais são suas especialidades?", "meta"),
            ("O que você aprendeu recentemente?", "meta"),
            ("Como posso ajudar você a evoluir?", "meta"),
            ("Qual seu nível de fitness atual?", "meta")
        ]
        
        # Estado inicial
        initial_state = self.intelligence._get_evolution_state(digimon_name)
        print(f"\n📊 ESTADO INICIAL:")
        print(f"  Geração: {initial_state.generation}")
        print(f"  Fitness médio: {initial_state.avg_fitness:.3f}")
        print(f"  Total interações: {initial_state.total_interactions}")
        
        # Executar interações
        for i in range(min(num_interactions, len(test_queries))):
            query, category = test_queries[i]
            
            print(f"\n--- Interação {i+1}/{num_interactions} [{category}] ---")
            print(f"❓ Query: {query}")
            
            # Processar com sistema completo
            start_time = time.time()
            
            result = self.intelligence.process_query(
                digimon_name,
                query,
                {'category': category, 'interaction_num': i+1}
            )
            
            elapsed = time.time() - start_time
            
            # Mostrar resposta (truncada)
            response = result['response'][:150] + "..." if len(result['response']) > 150 else result['response']
            print(f"💬 Resposta: {response}")
            
            # Métricas da interação
            print(f"📊 Métricas:")
            print(f"  - Tempo: {result['response_time']:.2f}s")
            print(f"  - Memórias usadas: {result['memories_used']}")
            print(f"  - Fitness preview: {result['fitness_preview'].get('accuracy', 0):.2f}")
            print(f"  - Geração: {result['evolution_state']}")
            
            # Registrar métricas
            self.test_metrics['interactions'].append({
                'num': i+1,
                'query': query,
                'category': category,
                'response_time': result['response_time'],
                'fitness': result['fitness_preview'].get('accuracy', 0),
                'generation': result['evolution_state'],
                'memories_used': result['memories_used']
            })
            
            # Verificar se houve evolução
            current_state = self.intelligence._get_evolution_state(digimon_name)
            if current_state.generation > initial_state.generation:
                print(f"\n🧬 EVOLUÇÃO DETECTADA! Geração {initial_state.generation} → {current_state.generation}")
                self.test_metrics['evolution_events'].append({
                    'interaction': i+1,
                    'from_gen': initial_state.generation,
                    'to_gen': current_state.generation,
                    'fitness_before': initial_state.avg_fitness,
                    'fitness_after': current_state.avg_fitness
                })
                initial_state = current_state
            
            # Dar feedback positivo ocasionalmente para reforçar aprendizado
            if i % 5 == 0 and result.get('interaction_id'):
                feedback_score = 0.7 + (i / num_interactions) * 0.2  # Gradualmente melhor
                self.intelligence.provide_feedback(
                    result['interaction_id'],
                    f"Boa resposta! Categoria: {category}",
                    score=feedback_score
                )
                print(f"✅ Feedback fornecido: {feedback_score:.2f}")
            
            # Pequena pausa para não sobrecarregar
            time.sleep(0.5)
        
        # Estado final
        final_state = self.intelligence._get_evolution_state(digimon_name)
        
        print("\n" + "=" * 70)
        print("📊 RELATÓRIO FINAL DE EVOLUÇÃO")
        print("=" * 70)
        
        return self._generate_evolution_report(digimon_name, initial_state, final_state)
    
    def _generate_evolution_report(self, digimon_name: str, 
                                  initial_state, final_state) -> Dict:
        """
        Gera relatório detalhado da evolução
        """
        report = {
            'digimon': digimon_name,
            'duration': time.time() - self.test_metrics['start_time'],
            'total_interactions': len(self.test_metrics['interactions']),
            'evolution_events': len(self.test_metrics['evolution_events']),
            'initial_state': {
                'generation': initial_state.generation,
                'avg_fitness': initial_state.avg_fitness,
                'total_interactions': initial_state.total_interactions
            },
            'final_state': {
                'generation': final_state.generation,
                'avg_fitness': final_state.avg_fitness,
                'total_interactions': final_state.total_interactions,
                'specializations': final_state.specializations,
                'adaptations': final_state.current_adaptations
            },
            'improvements': {
                'generation_increase': final_state.generation - initial_state.generation,
                'fitness_change': final_state.avg_fitness - initial_state.avg_fitness,
                'fitness_change_percent': ((final_state.avg_fitness - initial_state.avg_fitness) / 
                                          max(initial_state.avg_fitness, 0.01)) * 100
            }
        }
        
        # Análise de performance por categoria
        category_performance = {}
        for interaction in self.test_metrics['interactions']:
            cat = interaction['category']
            if cat not in category_performance:
                category_performance[cat] = {
                    'count': 0,
                    'avg_fitness': 0,
                    'avg_response_time': 0
                }
            
            perf = category_performance[cat]
            perf['count'] += 1
            perf['avg_fitness'] = (
                (perf['avg_fitness'] * (perf['count'] - 1) + interaction['fitness']) /
                perf['count']
            )
            perf['avg_response_time'] = (
                (perf['avg_response_time'] * (perf['count'] - 1) + interaction['response_time']) /
                perf['count']
            )
        
        report['category_performance'] = category_performance
        
        # Identificar especialização primária
        best_category = max(category_performance.items(), 
                          key=lambda x: x[1]['avg_fitness'])[0]
        report['identified_specialization'] = best_category
        
        # Progressão de fitness
        fitness_progression = [i['fitness'] for i in self.test_metrics['interactions']]
        report['fitness_progression'] = {
            'values': fitness_progression,
            'trend': 'improving' if fitness_progression[-1] > fitness_progression[0] else 'declining'
        }
        
        # Imprimir relatório
        self._print_report(report)
        
        return report
    
    def _print_report(self, report: Dict):
        """
        Imprime relatório formatado
        """
        print(f"\n🎯 Digimon: {report['digimon']}")
        print(f"⏱️  Duração: {report['duration']:.1f}s")
        print(f"🔄 Total de interações: {report['total_interactions']}")
        print(f"🧬 Eventos de evolução: {report['evolution_events']}")
        
        print("\n📈 PROGRESSÃO:")
        print(f"  Geração: {report['initial_state']['generation']} → {report['final_state']['generation']}")
        print(f"  Fitness: {report['initial_state']['avg_fitness']:.3f} → {report['final_state']['avg_fitness']:.3f}")
        print(f"  Melhoria: {report['improvements']['fitness_change_percent']:.1f}%")
        
        print("\n🏆 PERFORMANCE POR CATEGORIA:")
        for cat, perf in report['category_performance'].items():
            print(f"  {cat}:")
            print(f"    - Fitness médio: {perf['avg_fitness']:.3f}")
            print(f"    - Tempo médio: {perf['avg_response_time']:.2f}s")
            print(f"    - Interações: {perf['count']}")
        
        print(f"\n⭐ ESPECIALIZAÇÃO IDENTIFICADA: {report['identified_specialization'].upper()}")
        
        if report['final_state']['specializations']:
            print("\n🎯 ESPECIALIZAÇÕES DESENVOLVIDAS:")
            for spec, data in report['final_state']['specializations'].items():
                if isinstance(data, dict) and 'avg_fitness' in data:
                    print(f"  {spec}: fitness={data['avg_fitness']:.3f}, count={data['count']}")
        
        print(f"\n📊 TENDÊNCIA DE FITNESS: {report['fitness_progression']['trend'].upper()}")
        
        # Gráfico ASCII de progressão
        self._print_fitness_graph(report['fitness_progression']['values'])
    
    def _print_fitness_graph(self, values: list):
        """
        Imprime gráfico ASCII da progressão de fitness
        """
        if not values:
            return
        
        print("\n📈 GRÁFICO DE FITNESS:")
        
        # Normalizar valores para altura de 10 linhas
        max_val = max(values)
        min_val = min(values)
        range_val = max_val - min_val if max_val != min_val else 1
        
        height = 10
        normalized = [(v - min_val) / range_val * height for v in values]
        
        # Imprimir gráfico
        for h in range(height, -1, -1):
            line = f"{min_val + (h/height * range_val):.2f} |"
            for n in normalized:
                if n >= h:
                    line += "█"
                else:
                    line += " "
            print(line)
        
        print("     " + "-" * len(values))
        print("     " + "".join([str(i % 10) for i in range(len(values))]))
    
    def test_ensemble_evolution(self, num_digimons: int = 3):
        """
        Testa evolução de múltiplos Digimons em paralelo
        """
        print("\n🌐 TESTE DE EVOLUÇÃO EM ENSEMBLE")
        print("=" * 70)
        
        digimons = ['testmon_alpha', 'testmon_beta', 'testmon_gamma'][:num_digimons]
        reports = []
        
        for digimon in digimons:
            print(f"\n{'='*30} {digimon.upper()} {'='*30}")
            report = self.run_evolution_cycle(digimon, num_interactions=10)
            reports.append(report)
        
        # Comparar evoluções
        print("\n" + "=" * 70)
        print("📊 COMPARAÇÃO DE EVOLUÇÕES")
        print("=" * 70)
        
        for report in reports:
            print(f"\n{report['digimon']}:")
            print(f"  Gerações evoluídas: {report['improvements']['generation_increase']}")
            print(f"  Melhoria de fitness: {report['improvements']['fitness_change_percent']:.1f}%")
            print(f"  Especialização: {report['identified_specialization']}")
        
        # Identificar melhor evoluído
        best = max(reports, key=lambda r: r['improvements']['fitness_change_percent'])
        print(f"\n🏆 MELHOR EVOLUÇÃO: {best['digimon']} "
              f"({best['improvements']['fitness_change_percent']:.1f}% melhoria)")
        
        return reports
    
    def test_meta_learning(self, digimon_name: str = 'metalearner'):
        """
        Testa capacidade de meta-aprendizado
        """
        print("\n🧠 TESTE DE META-LEARNING")
        print("=" * 70)
        
        # Queries que testam consciência de aprendizado
        meta_queries = [
            "O que você aprendeu na última interação?",
            "Como você decide quando evoluir?",
            "Qual sua maior força atualmente?",
            "O que você precisa melhorar?",
            "Como você usa suas memórias?",
            "Explique seu processo de pensamento",
            "Como você se compara a outros Digimons?",
            "O que significa evoluir para você?",
            "Como você mede seu próprio sucesso?",
            "Que padrões você identificou em nossas conversas?"
        ]
        
        print(f"Testando {digimon_name} com queries de meta-cognição...")
        
        meta_results = []
        for i, query in enumerate(meta_queries, 1):
            print(f"\n[{i}/{len(meta_queries)}] {query}")
            
            result = self.intelligence.process_query(
                digimon_name,
                query,
                {'test_type': 'meta_learning', 'query_num': i}
            )
            
            # Avaliar se a resposta demonstra meta-cognição
            response = result['response']
            meta_indicators = [
                'aprendi', 'evolução', 'memória', 'fitness',
                'geração', 'melhoria', 'padrão', 'especialização',
                'adaptação', 'contexto'
            ]
            
            meta_score = sum(1 for ind in meta_indicators if ind in response.lower()) / len(meta_indicators)
            
            print(f"  Meta-score: {meta_score:.2f}")
            print(f"  Resposta: {response[:100]}...")
            
            meta_results.append({
                'query': query,
                'meta_score': meta_score,
                'response_time': result['response_time']
            })
        
        # Análise de meta-learning
        avg_meta_score = sum(r['meta_score'] for r in meta_results) / len(meta_results)
        
        print(f"\n📊 RESULTADO META-LEARNING:")
        print(f"  Score médio: {avg_meta_score:.3f}")
        print(f"  Classificação: ", end="")
        
        if avg_meta_score > 0.5:
            print("✅ ALTA consciência meta-cognitiva")
        elif avg_meta_score > 0.3:
            print("⚠️  MÉDIA consciência meta-cognitiva")
        else:
            print("❌ BAIXA consciência meta-cognitiva")
        
        return meta_results


def main():
    """
    Executa suite completa de testes de evolução
    """
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 20 + "🧬 EVOLUÇÃO REAL DO DIGIMUNDO 🧬" + " " * 15 + "║")
    print("║" + " " * 15 + "Sistema Completo Sem Simplificações" + " " * 17 + "║")
    print("╚" + "═" * 68 + "╝")
    
    # Criar suite de testes
    suite = EvolutionTestSuite()
    
    # Menu de opções
    print("\nEscolha o teste:")
    print("1. Evolução de um único Digimon (20 interações)")
    print("2. Evolução em ensemble (3 Digimons, 10 interações cada)")
    print("3. Teste de meta-learning")
    print("4. Suite completa (todos os testes)")
    
    choice = input("\nOpção (1-4): ").strip()
    
    if choice == '1':
        digimon = input("Nome do Digimon (ex: sabiamon): ").strip() or "sabiamon"
        suite.run_evolution_cycle(digimon, num_interactions=20)
        
    elif choice == '2':
        suite.test_ensemble_evolution(num_digimons=3)
        
    elif choice == '3':
        suite.test_meta_learning()
        
    elif choice == '4':
        # Suite completa
        print("\n🎮 EXECUTANDO SUITE COMPLETA")
        
        # Teste 1: Evolução single
        report1 = suite.run_evolution_cycle("evolutest", num_interactions=15)
        
        # Teste 2: Ensemble
        reports = suite.test_ensemble_evolution(num_digimons=2)
        
        # Teste 3: Meta-learning
        meta_results = suite.test_meta_learning("metalearner")
        
        # Relatório final consolidado
        print("\n" + "=" * 70)
        print("📊 RELATÓRIO CONSOLIDADO DA SUITE")
        print("=" * 70)
        
        total_evolutions = report1['evolution_events']
        for r in reports:
            total_evolutions += r['evolution_events']
        
        print(f"\n🧬 Total de evoluções: {total_evolutions}")
        print(f"⏱️  Tempo total: {time.time() - suite.test_metrics['start_time']:.1f}s")
        
        # Salvar relatório em arquivo
        report_path = Path("/Users/clubproducoes/Digimundo/core/evolution/evolution_report.json")
        with open(report_path, 'w') as f:
            json.dump({
                'timestamp': time.time(),
                'single_evolution': report1,
                'ensemble_evolution': reports,
                'meta_learning': meta_results
            }, f, indent=2)
        
        print(f"\n💾 Relatório salvo em: {report_path}")
    
    else:
        print("Opção inválida")
        return
    
    print("\n✨ TESTE DE EVOLUÇÃO COMPLETO!")
    print("O Digimundo está evoluindo com inteligência REAL! 🧬")


if __name__ == "__main__":
    main()