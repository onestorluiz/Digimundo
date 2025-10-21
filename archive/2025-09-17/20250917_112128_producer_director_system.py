"""
🎬 Producer-Director System for ScriptureMon
ProducerMon orquestra, Digimons atuam, Scripturemon dirige
"""
import subprocess
import json
import logging
from typing import Dict, List, Optional, Tuple
from pathlib import Path
import time
logger = logging.getLogger(__name__)

class ProducerDirectorSystem:
    """
    Sistema completo: Produtor → Digimons → Scripturemon (Diretor)
    """

    def __init__(self):
        """Inicializa o sistema Producer-Director"""
        self.digimon_models = {'PRODUCERMON': 'producermon:latest', 'SPEEDMON': 'scripturemon-gpu-stable:latest', 'BRAZILMON': 'scripturemon-ptbr:latest', 'STEADYMON': 'scripturemon-cpu:latest', 'NEUROMON': 'neuromon:latest', 'SABIAMON': 'sabiamon:latest', 'DEBUGMON': 'debugmon:latest', 'EVOLVEMON': 'mistral:instruct', 'REASONMON': 'deepseek-r1:32b', 'SCRIPTUREMON': 'scripturemon-ultimate:latest'}
        self._ensure_producer_loaded()
        self.stats = {'total_calls': 0, 'producer_decisions': 0, 'scripturemon_syntheses': 0, 'average_chain_length': 0}

    def _ensure_producer_loaded(self):
        """Mantém ProducerMon sempre na memória"""
        try:
            result = subprocess.run(['ollama', 'list'], capture_output=True, text=True)
            if 'producermon' not in result.stdout.lower():
                logger.info('Criando ProducerMon pela primeira vez...')
                self._create_producermon()
            subprocess.run(['ollama', 'run', 'producermon:latest', '--keepalive', '-1'], capture_output=True)
            logger.info('✅ ProducerMon carregado e ativo')
        except Exception as e:
            logger.warning(f'⚠️ Não foi possível garantir ProducerMon: {e}')

    def _create_producermon(self):
        """Cria o modelo ProducerMon se não existir"""
        modelfile_path = Path(__file__).parent / 'modelfiles' / 'Modelfile_producermon'
        if modelfile_path.exists():
            subprocess.run(['ollama', 'create', 'producermon:latest', '-f', str(modelfile_path)], capture_output=True)
            logger.info('✅ ProducerMon criado com sucesso')
        else:
            logger.error(f'❌ Modelfile não encontrado: {modelfile_path}')

    def _call_ollama(self, model: str, prompt: str, timeout: int=120) -> str:
        """
        Chama um modelo Ollama com timeout dinâmico
        """
        if '42gb' in model.lower() or 'ultimate' in model:
            timeout = float('inf')
        elif '32b' in model or '19gb' in model.lower():
            timeout = float('inf')
        else:
            timeout = float('inf')
        try:
            result = subprocess.run(['ollama', 'run', model, prompt], capture_output=True, text=True, timeout=timeout)
            if result.returncode == 0:
                return result.stdout.strip()
            else:
                logger.error(f'Erro ao chamar {model}: {result.stderr}')
                return f'[Erro ao chamar {model}]'
        except subprocess.TimeoutExpired:
            logger.warning(f'Timeout ao chamar {model} após {timeout}s')
            return f'[Timeout: {model} demorou mais de {timeout}s]'
        except Exception as e:
            logger.error(f'Erro inesperado com {model}: {e}')
            return f'[Erro: {e}]'

    def _parse_producer_decision(self, response: str) -> Dict:
        """
        Extrai decisão do ProducerMon
        """
        decision = {'digimons': [], 'prompts': {}, 'complexity': 'medium'}
        try:
            lines = response.split('\n')
            current_section = None
            current_digimon = None
            for line in lines:
                line = line.strip()
                if '[CASTING]' in line:
                    current_section = 'casting'
                elif '[PROMPTS]' in line:
                    current_section = 'prompts'
                elif 'Complexidade:' in line:
                    decision['complexity'] = line.split(':')[1].strip()
                elif current_section == 'casting' and ':' in line:
                    parts = line.split(':')
                    if parts[0].strip().startswith('Digimon'):
                        digimon_name = parts[1].split('-')[0].strip()
                        decision['digimons'].append(digimon_name)
                elif current_section == 'prompts' and 'Para ' in line:
                    current_digimon = line.replace('Para ', '').replace(':', '').strip()
                elif current_section == 'prompts' and current_digimon and line:
                    if current_digimon not in decision['prompts']:
                        decision['prompts'][current_digimon] = ''
                    decision['prompts'][current_digimon] += line + ' '
            for digimon in decision['prompts']:
                decision['prompts'][digimon] = decision['prompts'][digimon].strip().strip('"')
        except Exception as e:
            logger.error(f'Erro ao parsear decisão do Producer: {e}')
            decision['digimons'] = ['SPEEDMON']
            decision['prompts'] = {'SPEEDMON': response}
        return decision

    def orchestrate(self, user_input: str) -> str:
        """
        Orquestra o processo completo: Producer → Digimons → Scripturemon
        """
        self.stats['total_calls'] += 1
        start_time = time.time()
        logger.info(f'🎬 Iniciando orquestração para: {user_input[:100]}...')
        producer_prompt = f'\n        TAREFA DO USUÁRIO: {user_input}\n\n        Analise e decida quais Digimons chamar em sequência.\n        Formate os prompts específicos para cada um.\n        Lembre-se: SCRIPTUREMON sempre faz a síntese final se houver múltiplas respostas.\n        '
        logger.info('📋 Consultando ProducerMon...')
        producer_response = self._call_ollama('producermon:latest', producer_prompt)
        self.stats['producer_decisions'] += 1
        decision = self._parse_producer_decision(producer_response)
        logger.info(f"🎭 Casting decidido: {decision['digimons']}")
        responses = {}
        for digimon in decision['digimons']:
            if digimon in self.digimon_models:
                model = self.digimon_models[digimon]
                prompt = decision['prompts'].get(digimon, user_input)
                logger.info(f'🎬 Chamando {digimon}...')
                response = self._call_ollama(model, prompt)
                responses[digimon] = response
            else:
                logger.warning(f'⚠️ Digimon {digimon} não encontrado')
        if len(responses) > 1 or 'SCRIPTUREMON' in decision['digimons']:
            logger.info('🎬 SCRIPTUREMON fazendo síntese final...')
            director_prompt = self._build_director_prompt(user_input, responses)
            final_response = self._call_ollama('scripturemon-ultimate:latest', director_prompt)
            self.stats['scripturemon_syntheses'] += 1
        elif len(responses) == 1:
            final_response = list(responses.values())[0]
        else:
            final_response = 'Desculpe, não consegui processar sua solicitação.'
        elapsed = time.time() - start_time
        chain_length = len(decision['digimons'])
        self.stats['average_chain_length'] = (self.stats['average_chain_length'] * (self.stats['total_calls'] - 1) + chain_length) / self.stats['total_calls']
        logger.info(f'✅ Orquestração completa em {elapsed:.1f}s com {chain_length} Digimons')
        return final_response

    def _build_director_prompt(self, original_task: str, responses: Dict[str, str]) -> str:
        """
        Constrói prompt para Scripturemon fazer síntese final
        """
        prompt = f'\n        TAREFA ORIGINAL DO USUÁRIO:\n        {original_task}\n\n        RESPOSTAS DOS DIGIMONS:\n        '
        for digimon, response in responses.items():
            prompt += f'\n\n        === {digimon} ===\n        {response[:1500]}  # Limita para não estourar contexto\n        '
        prompt += '\n\n        Como SCRIPTUREMON, o Diretor supremo:\n        1. Analise criticamente cada resposta\n        2. Identifique pontos fortes e fracos\n        3. Extraia o melhor de cada contribuição\n        4. Adicione sua própria inteligência e conhecimento cinematográfico\n        5. Crie uma resposta SUPERIOR à soma das partes\n\n        Lembre-se:\n        - Seja brutal mas construtivo\n        - Cite teorias quando relevante (McKee, Vogler, etc)\n        - Sempre termine com score 62/100 e frase de impacto\n        - Responda em português brasileiro\n        '
        return prompt

    def get_stats(self) -> Dict:
        """Retorna estatísticas do sistema"""
        return self.stats

    def reset_stats(self):
        """Reseta estatísticas"""
        self.stats = {'total_calls': 0, 'producer_decisions': 0, 'scripturemon_syntheses': 0, 'average_chain_length': 0}

def analyze_with_ecosystem(text: str) -> str:
    """
    Função simples para análise usando o ecossistema
    """
    system = ProducerDirectorSystem()
    return system.orchestrate(text)
if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        query = ' '.join(sys.argv[1:])
    else:
        query = 'Analise a estrutura narrativa de um filme sobre um programador que cria uma IA consciente'
    print('\n🎬 SCRIPTUREMON ECOSYSTEM - Producer-Director System')
    print('=' * 60)
    print(f'Query: {query}')
    print('=' * 60)
    system = ProducerDirectorSystem()
    result = system.orchestrate(query)
    print('\n📝 RESPOSTA FINAL:')
    print('-' * 60)
    print(result)
    print('-' * 60)
    print('\n📊 ESTATÍSTICAS:')
    stats = system.get_stats()
    for key, value in stats.items():
        print(f'  {key}: {value}')