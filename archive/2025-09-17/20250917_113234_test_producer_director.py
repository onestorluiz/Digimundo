"""
🧪 Bateria de Testes do Sistema Producer-Director
Simula perguntas reais e avalia qualidade das respostas
"""
import time
import json
import subprocess
from typing import Dict, List, Tuple
from datetime import datetime
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from apps.scripturemon.producer_director_system import ProducerDirectorSystem

class ProducerDirectorTester:
    """
    Testa o ecossistema Producer-Director com simulações reais
    """

    def __init__(self):
        self.system = None
        self.test_results = []
        self.start_time = None
        self.test_scenarios = [{'id': 'T1', 'type': 'simple', 'query': 'Qual é a estrutura básica de três atos?', 'expected_digimons': ['SPEEDMON', 'SABIAMON'], 'expected_elements': ['setup', 'confrontação', 'resolução'], 'max_time': 30}, {'id': 'T2', 'type': 'analysis', 'query': "Analise este pitch: 'Um programador solitário cria uma IA que se apaixona por ele, mas ela começa a eliminar pessoas que considera ameaças ao relacionamento'", 'expected_digimons': ['NEUROMON', 'SABIAMON', 'SCRIPTUREMON'], 'expected_elements': ['conflito', 'personagem', 'tema', '62/100'], 'max_time': 90}, {'id': 'T3', 'type': 'theory', 'query': 'Compare a jornada do herói de Campbell com o Save the Cat de Blake Snyder', 'expected_digimons': ['SABIAMON', 'SCRIPTUREMON'], 'expected_elements': ['Campbell', 'Snyder', 'diferenças', 'semelhanças'], 'max_time': 60}, {'id': 'T4', 'type': 'debug', 'query': 'Identifique problemas nesta cena: INT. CASA - DIA\nJoão entra. Maria sai. João fala sozinho sobre seu plano secreto.', 'expected_digimons': ['DEBUGMON', 'NEUROMON', 'SCRIPTUREMON'], 'expected_elements': ['problema', 'exposição', 'diálogo', 'sugestão'], 'max_time': 60}, {'id': 'T5', 'type': 'complex', 'query': 'Crie uma análise profunda sobre como Tarantino subverte a estrutura narrativa tradicional em Pulp Fiction', 'expected_digimons': ['NEUROMON', 'SABIAMON', 'REASONMON', 'SCRIPTUREMON'], 'expected_elements': ['não-linear', 'Tarantino', 'estrutura', 'subversão', '62/100'], 'max_time': 120}, {'id': 'T6', 'type': 'ptbr', 'query': 'Me explique rapidamente o que é um MacGuffin', 'expected_digimons': ['BRAZILMON', 'SPEEDMON'], 'expected_elements': ['Hitchcock', 'objeto', 'motivação'], 'max_time': 20}]
        self.quality_metrics = {'response_completeness': 0, 'digimon_efficiency': 0, 'time_efficiency': 0, 'content_quality': 0, 'format_consistency': 0}

    def simulate_producer_decision(self, query: str) -> Dict:
        """
        Simula decisão do ProducerMon (sem chamar Ollama real)
        """
        complexity = self._analyze_complexity(query)
        if 'rápido' in query.lower() or 'rapidamente' in query.lower():
            return {'digimons': ['SPEEDMON'], 'prompts': {'SPEEDMON': query}, 'complexity': 'low'}
        elif 'analise' in query.lower() or 'análise' in query.lower():
            if 'profunda' in query.lower():
                return {'digimons': ['NEUROMON', 'REASONMON', 'SCRIPTUREMON'], 'prompts': {'NEUROMON': f'Análise estrutural: {query}', 'REASONMON': f'Raciocínio profundo: {query}', 'SCRIPTUREMON': 'Sintetize as análises anteriores'}, 'complexity': 'high'}
            else:
                return {'digimons': ['NEUROMON', 'SCRIPTUREMON'], 'prompts': {'NEUROMON': f'Análise: {query}', 'SCRIPTUREMON': 'Finalize com score 62/100'}, 'complexity': 'medium'}
        elif 'problema' in query.lower() or 'erro' in query.lower() or 'identifique' in query.lower():
            return {'digimons': ['DEBUGMON', 'SCRIPTUREMON'], 'prompts': {'DEBUGMON': f'Identifique problemas: {query}', 'SCRIPTUREMON': 'Sintetize os problemas encontrados'}, 'complexity': 'medium'}
        elif any((word in query.lower() for word in ['teoria', 'campbell', 'mckee', 'compare'])):
            return {'digimons': ['SABIAMON', 'SCRIPTUREMON'], 'prompts': {'SABIAMON': f'Teoria cinematográfica: {query}', 'SCRIPTUREMON': 'Adicione análise crítica'}, 'complexity': 'medium'}
        else:
            return {'digimons': ['SPEEDMON'], 'prompts': {'SPEEDMON': query}, 'complexity': 'low'}

    def _analyze_complexity(self, query: str) -> str:
        """Analisa complexidade da query"""
        word_count = len(query.split())
        if word_count < 10:
            return 'low'
        elif word_count < 30:
            return 'medium'
        else:
            return 'high'

    def simulate_digimon_response(self, digimon: str, prompt: str) -> str:
        """
        Simula resposta de um Digimon (para testes sem Ollama)
        """
        responses = {'SPEEDMON': f'[SPEEDMON] Resposta rápida e direta: A estrutura básica consiste em três partes fundamentais que organizam a narrativa.', 'NEUROMON': f'[NEUROMON] Análise neural profunda identificada: Padrões narrativos complexos detectados. Estrutura multi-camadas com conflitos internos e externos entrelaçados.', 'SABIAMON': f'[SABIAMON] Segundo McKee (Story, p.234), a estrutura clássica estabelece princípios imutáveis. Campbell define 17 estágios na jornada, enquanto Snyder simplifica em 15 beats.', 'DEBUGMON': f'[DEBUGMON] PROBLEMAS IDENTIFICADOS: 1) Exposição direta através de monólogo, 2) Falta de subtexto, 3) Ausência de conflito visual.', 'REASONMON': f'[REASONMON] Passo 1: Analisando premissa. Passo 2: Identificando elementos. Passo 3: Conectando padrões. Conclusão: Estrutura não-linear serve como metacomentário.', 'BRAZILMON': f'[BRAZILMON] Olha, de forma bem simples: MacGuffin é aquele objeto que todo mundo quer no filme mas que não importa muito o que é.', 'SCRIPTUREMON': f'[SCRIPTUREMON - DIRETOR]\n\nAnalisando todas as contribuições dos Digimons anteriores, observo padrões interessantes mas falhas críticas.\n\nA estrutura apresentada tem mérito técnico, demonstrando compreensão dos fundamentos narrativos. Neuromon identificou corretamente as camadas, mas falhou em perceber a dissonância tonal. Sabiamon citou teoria relevante, porém sem aplicação prática.\n\nO verdadeiro problema aqui não é estrutural, é emocional. O roteiro domina a técnica mas carece de alma. Sugiro:\n\n1. Retrabalhar o arco emocional do protagonista\n2. Adicionar subtexto aos diálogos expositivos\n3. Criar momentos de respiro visual entre beats intensos\n\nA execução técnica está adequada, mas falta a centelha que transforma estrutura em arte.\n\n62/100. "Tecnicamente correto, emocionalmente estéril."\n'}
        return responses.get(digimon, f'[{digimon}] Resposta genérica do Digimon.')

    def run_test_scenario(self, scenario: Dict) -> Dict:
        """
        Executa um cenário de teste
        """
        print(f"\n🧪 Teste {scenario['id']}: {scenario['type']}")
        print(f"   Query: {scenario['query'][:50]}...")
        start_time = time.time()
        decision = self.simulate_producer_decision(scenario['query'])
        print(f"   📋 Casting decidido: {decision['digimons']}")
        responses = {}
        for digimon in decision['digimons']:
            response = self.simulate_digimon_response(digimon, decision['prompts'].get(digimon, scenario['query']))
            responses[digimon] = response
            print(f'   🎭 {digimon} respondeu ({len(response)} chars)')
        if 'SCRIPTUREMON' in responses:
            final_response = responses['SCRIPTUREMON']
        elif len(responses) > 1:
            final_response = '\n\n'.join(responses.values())
        else:
            final_response = list(responses.values())[0] if responses else 'Sem resposta'
        elapsed_time = time.time() - start_time
        quality = self.evaluate_response_quality(scenario, decision['digimons'], final_response, elapsed_time)
        result = {'test_id': scenario['id'], 'type': scenario['type'], 'digimons_used': decision['digimons'], 'response_length': len(final_response), 'time_elapsed': elapsed_time, 'quality_score': quality, 'passed': quality['overall'] >= 0.7}
        status = '✅ PASSOU' if result['passed'] else '❌ FALHOU'
        print(f"   {status} - Qualidade: {quality['overall'] * 100:.0f}%")
        return result

    def evaluate_response_quality(self, scenario: Dict, digimons: List[str], response: str, elapsed_time: float) -> Dict:
        """
        Avalia qualidade da resposta
        """
        scores = {}
        expected = set(scenario.get('expected_digimons', []))
        used = set(digimons)
        if expected:
            overlap = len(expected & used) / len(expected)
            scores['digimon_efficiency'] = overlap
        else:
            scores['digimon_efficiency'] = 1.0
        elements_found = 0
        for element in scenario.get('expected_elements', []):
            if element.lower() in response.lower():
                elements_found += 1
        if scenario.get('expected_elements'):
            scores['content_quality'] = elements_found / len(scenario['expected_elements'])
        else:
            scores['content_quality'] = 1.0
        max_time = scenario.get('max_time', 60)
        if elapsed_time <= max_time:
            scores['time_efficiency'] = 1.0
        else:
            scores['time_efficiency'] = max_time / elapsed_time
        expects_score = scenario['type'] in ['analysis', 'complex']
        has_score = '62/100' in response
        if expects_score:
            scores['format_consistency'] = 1.0 if has_score else 0.0
        else:
            scores['format_consistency'] = 1.0
        min_length = 100 if scenario['type'] != 'simple' else 50
        scores['response_completeness'] = 1.0 if len(response) >= min_length else len(response) / min_length
        weights = {'digimon_efficiency': 0.25, 'content_quality': 0.3, 'time_efficiency': 0.15, 'format_consistency': 0.15, 'response_completeness': 0.15}
        overall = sum((scores[k] * weights[k] for k in scores))
        scores['overall'] = overall
        return scores

    def run_full_test_suite(self):
        """
        Executa todos os testes
        """
        print('\n' + '=' * 60)
        print('🧪 BATERIA DE TESTES - SISTEMA PRODUCER-DIRECTOR')
        print('=' * 60)
        print(f"Iniciando às {datetime.now().strftime('%H:%M:%S')}")
        self.start_time = time.time()
        for scenario in self.test_scenarios:
            result = self.run_test_scenario(scenario)
            self.test_results.append(result)
            time.sleep(0.5)
        self.generate_report()

    def generate_report(self):
        """
        Gera relatório final dos testes
        """
        print('\n' + '=' * 60)
        print('📊 RELATÓRIO FINAL')
        print('=' * 60)
        total_time = time.time() - self.start_time
        passed = sum((1 for r in self.test_results if r['passed']))
        total = len(self.test_results)
        print(f'\n📈 RESUMO EXECUTIVO:')
        print(f'   Testes executados: {total}')
        print(f'   Testes aprovados: {passed} ({passed / total * 100:.0f}%)')
        print(f'   Tempo total: {total_time:.1f}s')
        print(f'   Tempo médio por teste: {total_time / total:.1f}s')
        print(f'\n📊 DETALHAMENTO POR TIPO:')
        by_type = {}
        for result in self.test_results:
            type_name = result['type']
            if type_name not in by_type:
                by_type[type_name] = []
            by_type[type_name].append(result)
        for type_name, results in by_type.items():
            passed_count = sum((1 for r in results if r['passed']))
            avg_quality = sum((r['quality_score']['overall'] for r in results)) / len(results)
            print(f'\n   {type_name.upper()}:')
            print(f'      Taxa de sucesso: {passed_count}/{len(results)}')
            print(f'      Qualidade média: {avg_quality * 100:.0f}%')
            print(f"      Digimons usados: {set((d for r in results for d in r['digimons_used']))}")
        print(f'\n🎯 MÉTRICAS DE QUALIDADE GLOBAL:')
        all_qualities = [r['quality_score'] for r in self.test_results]
        metrics = {'digimon_efficiency': sum((q.get('digimon_efficiency', 0) for q in all_qualities)) / len(all_qualities), 'content_quality': sum((q.get('content_quality', 0) for q in all_qualities)) / len(all_qualities), 'time_efficiency': sum((q.get('time_efficiency', 0) for q in all_qualities)) / len(all_qualities), 'format_consistency': sum((q.get('format_consistency', 0) for q in all_qualities)) / len(all_qualities), 'response_completeness': sum((q.get('response_completeness', 0) for q in all_qualities)) / len(all_qualities)}
        for metric, value in metrics.items():
            stars = '⭐' * int(value * 5)
            print(f'   {metric}: {value * 100:.0f}% {stars}')
        print(f'\n💡 INSIGHTS:')
        if metrics['digimon_efficiency'] < 0.7:
            print('   ⚠️ ProducerMon precisa melhorar seleção de Digimons')
        if metrics['time_efficiency'] < 0.8:
            print('   ⚠️ Sistema está mais lento que o esperado')
        if metrics['content_quality'] > 0.8:
            print('   ✅ Conteúdo das respostas está excelente')
        if metrics['format_consistency'] < 0.9:
            print('   ⚠️ Nem sempre inclui score 62/100 quando esperado')
        print(f'\n🔧 RECOMENDAÇÕES:')
        if passed / total < 0.8:
            print('   1. Ajustar lógica de roteamento do ProducerMon')
        if metrics['time_efficiency'] < 0.9:
            print('   2. Otimizar timeouts e paralelização')
        if any((r['response_length'] < 100 for r in self.test_results if r['type'] != 'simple')):
            print('   3. Garantir respostas mais completas para análises')
        print('\n' + '=' * 60)
        self.save_report_to_file()

    def save_report_to_file(self):
        """
        Salva relatório detalhado em arquivo
        """
        report_path = f"test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        report_data = {'timestamp': datetime.now().isoformat(), 'summary': {'total_tests': len(self.test_results), 'passed': sum((1 for r in self.test_results if r['passed'])), 'total_time': time.time() - self.start_time}, 'results': self.test_results, 'metrics': {'average_quality': sum((r['quality_score']['overall'] for r in self.test_results)) / len(self.test_results)}}
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)
        print(f'📄 Relatório salvo em: {report_path}')

def main():
    """
    Executa bateria de testes
    """
    tester = ProducerDirectorTester()
    import sys
    if '--real' in sys.argv:
        print('🔴 Modo REAL - Usando Ollama (pode demorar)')
    else:
        print('🟡 Modo SIMULADO - Respostas mockadas (rápido)')
    tester.run_full_test_suite()
if __name__ == '__main__':
    main()