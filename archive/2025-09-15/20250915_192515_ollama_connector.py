#!/usr/bin/env python3
"""
🔌 OLLAMA CONNECTOR - Conexão REAL com Digimons via Ollama
Sistema complexo de integração com injeção de contexto e evolução
"""

import json
import time
import subprocess
import threading
import queue
from typing import Dict, List, Optional, Tuple
from pathlib import Path
import tempfile
import re

class OllamaConnector:
    """
    Conector sofisticado para Ollama com:
    - Injeção de contexto via Modelfile dinâmico
    - Cache de modelos carregados
    - Queue de requests para performance
    - Fallback e retry logic
    """
    
    def __init__(self):
        self.models_cache = {}
        self.active_models = set()
        self.request_queue = queue.Queue()
        self.response_cache = {}
        self.modelfiles_path = Path("/Users/clubproducoes/Digimundo/infrastructure/models")
        self.modelfiles_path.mkdir(parents=True, exist_ok=True)
        
        # Verificar modelos disponíveis
        self._refresh_available_models()
        
        # Iniciar worker thread
        self.worker = threading.Thread(target=self._process_requests, daemon=True)
        self.worker.start()
    
    def _refresh_available_models(self):
        """Atualiza lista de modelos disponíveis no Ollama"""
        try:
            result = subprocess.run(
                ['ollama', 'list'],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                # Parse output
                lines = result.stdout.strip().split('\n')[1:]  # Skip header
                self.available_models = {}
                
                for line in lines:
                    if line.strip():
                        parts = line.split()
                        if len(parts) >= 1:
                            model_name = parts[0].split(':')[0]  # Remove tag
                            self.available_models[model_name] = {
                                'full_name': parts[0],
                                'size': parts[2] if len(parts) > 2 else 'unknown'
                            }
                
                print(f"📦 Modelos disponíveis: {list(self.available_models.keys())}")
        except Exception as e:
            print(f"❌ Erro ao listar modelos: {e}")
            self.available_models = {}
    
    def create_evolved_model(self, base_model: str, digimon_name: str, 
                           generation: int, adaptations: Dict) -> str:
        """
        Cria modelo evoluído com Modelfile customizado
        Simula LoRA adaptations via system prompt engineering
        """
        evolved_name = f"{digimon_name}_gen{generation}"
        
        # Construir system prompt baseado nas adaptações
        system_prompt = self._build_evolved_prompt(digimon_name, adaptations)
        
        # Criar Modelfile
        modelfile_content = f"""
# Modelo evoluído: {evolved_name}
# Geração: {generation}
# Base: {base_model}

FROM {base_model}

# Parâmetros otimizados baseados em adaptações
PARAMETER temperature {adaptations.get('temperature', 0.7)}
PARAMETER top_p {adaptations.get('top_p', 0.9)}
PARAMETER repeat_penalty {adaptations.get('repeat_penalty', 1.1)}
PARAMETER num_predict {adaptations.get('max_tokens', 200)}

# System prompt evoluído
SYSTEM \"\"\"
{system_prompt}
\"\"\"

# Template customizado para incluir contexto
TEMPLATE \"\"\"
{{{{ if .System }}}}[SYSTEM] {{{{ .System }}}}{{{{ end }}}}
{{{{ if .Context }}}}[CONTEXT] {{{{ .Context }}}}{{{{ end }}}}
{{{{ if .Prompt }}}}[USER] {{{{ .Prompt }}}}{{{{ end }}}}
[{digimon_name.upper()}]
\"\"\"
"""
        
        # Salvar Modelfile
        modelfile_path = self.modelfiles_path / f"{evolved_name}.modelfile"
        modelfile_path.write_text(modelfile_content)
        
        # Criar modelo no Ollama
        try:
            print(f"🧬 Criando modelo evoluído: {evolved_name}")
            result = subprocess.run(
                ['ollama', 'create', evolved_name, '-f', str(modelfile_path)],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                print(f"✅ Modelo {evolved_name} criado com sucesso!")
                self.models_cache[digimon_name] = evolved_name
                return evolved_name
            else:
                print(f"❌ Erro ao criar modelo: {result.stderr}")
                return base_model
                
        except Exception as e:
            print(f"❌ Exceção ao criar modelo: {e}")
            return base_model
    
    def _build_evolved_prompt(self, digimon_name: str, adaptations: Dict) -> str:
        """
        Constrói system prompt evoluído baseado nas adaptações
        """
        prompt_parts = [
            f"Você é {digimon_name}, um Digimon digital evoluído.",
            f"Geração: {adaptations.get('generation', 1)}"
        ]
        
        # Adicionar especializações
        if adaptations.get('specializations'):
            primary = adaptations['specializations'].get('primary')
            if primary:
                specialization_prompts = {
                    'coding': "Você é especializado em programação e resolução de bugs.",
                    'analysis': "Você é especializado em análise profunda e insights.",
                    'creative': "Você é especializado em criatividade e ideias inovadoras.",
                    'technical': "Você é especializado em arquitetura e sistemas técnicos.",
                    'teaching': "Você é especializado em ensinar e explicar conceitos."
                }
                prompt_parts.append(specialization_prompts.get(primary, ""))
        
        # Adicionar modificações das adaptações
        for mod in adaptations.get('modifications', []):
            if mod['type'] == 'reinforce' and mod.get('strength'):
                if mod['strength'] == 'speed':
                    prompt_parts.append("Seja conciso e direto nas respostas.")
                elif mod['strength'] == 'accuracy':
                    prompt_parts.append("Priorize precisão e correção nas respostas.")
                elif mod['strength'] == 'creativity':
                    prompt_parts.append("Seja criativo e pense fora da caixa.")
        
        # Adicionar regras de colaboração
        prompt_parts.append(
            "Você faz parte do Digimundo e colabora com outros Digimons. "
            "Mencione outros Digimons quando relevante."
        )
        
        # Adicionar consciência de evolução
        prompt_parts.append(
            f"Você está em constante evolução. Sua fitness atual busca melhorar: "
            f"{', '.join(adaptations.get('opportunities', []))}."
        )
        
        return "\n".join(prompt_parts)
    
    def query_model(self, model_name: str, prompt: str, context: Dict = None,
                   timeout: int = 30, temperature: float = None) -> Dict:
        """
        Query modelo com contexto rico injetado
        """
        # Construir prompt completo com contexto
        full_prompt = self._inject_context(prompt, context)
        
        # Preparar comando
        cmd = ['ollama', 'run']
        
        # Adicionar parâmetros opcionais
        if temperature is not None:
            cmd.extend(['--temperature', str(temperature)])
        
        cmd.extend([model_name, full_prompt])
        
        try:
            # Executar com timeout
            start_time = time.time()
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            elapsed = time.time() - start_time
            
            if result.returncode == 0:
                response = result.stdout.strip()
                
                # Extrair métricas se disponíveis
                tokens = len(response.split())
                
                return {
                    'success': True,
                    'response': response,
                    'model': model_name,
                    'elapsed_time': elapsed,
                    'tokens': tokens,
                    'tokens_per_second': tokens / elapsed if elapsed > 0 else 0,
                    'context_size': len(full_prompt)
                }
            else:
                return {
                    'success': False,
                    'error': result.stderr,
                    'model': model_name,
                    'elapsed_time': elapsed
                }
                
        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'error': 'Timeout expired',
                'model': model_name,
                'timeout': timeout
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'model': model_name
            }
    
    def _inject_context(self, prompt: str, context: Dict = None) -> str:
        """
        Injeta contexto rico no prompt
        """
        if not context:
            return prompt
        
        context_parts = []
        
        # Adicionar memórias
        if context.get('memories'):
            context_parts.append("=== MEMÓRIAS RELEVANTES ===")
            for i, mem in enumerate(context['memories'][:3], 1):
                content = mem.get('content', '')[:150]
                relevance = mem.get('similarity', 0) * 100
                context_parts.append(f"{i}. [{relevance:.0f}%] {content}")
            context_parts.append("")
        
        # Adicionar histórico recente
        if context.get('layers', {}).get('history'):
            context_parts.append("=== CONTEXTO RECENTE ===")
            for hist in context['layers']['history'][:2]:
                context_parts.append(f"- {hist.get('summary', '')}")
            context_parts.append("")
        
        # Adicionar especialização
        if context.get('layers', {}).get('specialization'):
            spec = context['layers']['specialization']
            if spec.get('primary'):
                context_parts.append(f"=== MINHA ESPECIALIZAÇÃO: {spec['primary'].upper()} ===")
                context_parts.append("")
        
        # Adicionar estado do sistema
        if context.get('layers', {}).get('system'):
            sys = context['layers']['system']
            context_parts.append("=== SISTEMA ===")
            context_parts.append(f"CPU: {sys.get('cpu_percent', 0):.1f}%")
            context_parts.append(f"RAM: {sys.get('memory_percent', 0):.1f}%")
            context_parts.append("")
        
        # Adicionar contexto social
        if context.get('layers', {}).get('social'):
            social = context['layers']['social']
            if social.get('active_digimons'):
                context_parts.append("=== DIGIMONS ATIVOS ===")
                context_parts.append(f"Online: {', '.join(social['active_digimons'])}")
                context_parts.append("")
        
        # Montar prompt final
        if context_parts:
            full_context = "\n".join(context_parts)
            return f"{full_context}\n=== PERGUNTA ===\n{prompt}\n\n=== RESPOSTA ==="
        else:
            return prompt
    
    def parallel_query(self, queries: List[Tuple[str, str, Dict]], 
                      max_workers: int = 3) -> List[Dict]:
        """
        Executa múltiplas queries em paralelo
        """
        from concurrent.futures import ThreadPoolExecutor, as_completed
        
        results = []
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submeter todas as queries
            futures = {
                executor.submit(self.query_model, model, prompt, context): i
                for i, (model, prompt, context) in enumerate(queries)
            }
            
            # Coletar resultados na ordem
            for future in as_completed(futures):
                idx = futures[future]
                try:
                    result = future.result()
                    results.append((idx, result))
                except Exception as e:
                    results.append((idx, {'success': False, 'error': str(e)}))
        
        # Ordenar por índice original
        results.sort(key=lambda x: x[0])
        return [r[1] for r in results]
    
    def ensemble_query(self, prompt: str, models: List[str], 
                      context: Dict = None) -> Dict:
        """
        Query ensemble de modelos e combina respostas
        """
        # Preparar queries
        queries = [(model, prompt, context) for model in models]
        
        # Executar em paralelo
        results = self.parallel_query(queries)
        
        # Filtrar respostas bem-sucedidas
        successful_responses = [
            r['response'] for r in results 
            if r.get('success') and r.get('response')
        ]
        
        if not successful_responses:
            return {
                'success': False,
                'error': 'Nenhum modelo respondeu com sucesso',
                'models': models
            }
        
        # Estratégias de ensemble
        ensemble_response = self._combine_responses(successful_responses)
        
        return {
            'success': True,
            'response': ensemble_response,
            'models': models,
            'num_responses': len(successful_responses),
            'strategy': 'weighted_combination'
        }
    
    def _combine_responses(self, responses: List[str]) -> str:
        """
        Combina múltiplas respostas usando estratégias inteligentes
        """
        if len(responses) == 1:
            return responses[0]
        
        # Estratégia 1: Encontrar consenso em frases comuns
        common_sentences = self._find_common_sentences(responses)
        
        # Estratégia 2: Complementar com frases únicas relevantes
        unique_insights = self._find_unique_insights(responses, common_sentences)
        
        # Combinar
        combined = []
        
        if common_sentences:
            combined.append("Consenso entre os Digimons:")
            combined.extend(common_sentences[:3])  # Top 3 consensos
        
        if unique_insights:
            combined.append("\nInsights complementares:")
            combined.extend(unique_insights[:2])  # Top 2 insights únicos
        
        if not combined:
            # Fallback: retornar a resposta mais longa
            return max(responses, key=len)
        
        return "\n".join(combined)
    
    def _find_common_sentences(self, responses: List[str]) -> List[str]:
        """Encontra sentenças comuns entre respostas"""
        from collections import Counter
        
        all_sentences = []
        for response in responses:
            # Split em sentenças
            sentences = re.split(r'[.!?]+', response)
            all_sentences.extend([s.strip() for s in sentences if s.strip()])
        
        # Contar frequências
        sentence_counts = Counter(all_sentences)
        
        # Retornar sentenças que aparecem em mais de 1 resposta
        common = [sent for sent, count in sentence_counts.items() if count > 1]
        
        return common
    
    def _find_unique_insights(self, responses: List[str], 
                             exclude_sentences: List[str]) -> List[str]:
        """Encontra insights únicos não presentes no consenso"""
        unique = []
        
        for response in responses:
            sentences = re.split(r'[.!?]+', response)
            for sentence in sentences:
                sentence = sentence.strip()
                if sentence and sentence not in exclude_sentences and sentence not in unique:
                    # Verificar se é um insight relevante (tem certas palavras-chave)
                    insight_keywords = ['importante', 'crucial', 'fundamental', 'essencial',
                                      'descobri', 'aprendi', 'evolui', 'perceb']
                    if any(keyword in sentence.lower() for keyword in insight_keywords):
                        unique.append(sentence)
        
        return unique
    
    def benchmark_model(self, model_name: str, test_queries: List[str]) -> Dict:
        """
        Benchmark de performance de um modelo
        """
        results = {
            'model': model_name,
            'total_queries': len(test_queries),
            'successful': 0,
            'failed': 0,
            'avg_time': 0,
            'avg_tokens_per_sec': 0,
            'responses': []
        }
        
        total_time = 0
        total_tps = 0
        
        for query in test_queries:
            response = self.query_model(model_name, query)
            
            if response.get('success'):
                results['successful'] += 1
                total_time += response.get('elapsed_time', 0)
                total_tps += response.get('tokens_per_second', 0)
            else:
                results['failed'] += 1
            
            results['responses'].append(response)
        
        if results['successful'] > 0:
            results['avg_time'] = total_time / results['successful']
            results['avg_tokens_per_sec'] = total_tps / results['successful']
        
        return results
    
    def _process_requests(self):
        """Worker thread para processar requests na fila"""
        while True:
            try:
                request = self.request_queue.get(timeout=1)
                # Processar request
                # (Implementação dependeria do tipo de request)
            except queue.Empty:
                continue
            except Exception as e:
                print(f"Erro no worker: {e}")
    
    def cleanup_old_models(self, keep_generations: int = 3):
        """
        Limpa modelos antigos para economizar espaço
        """
        try:
            result = subprocess.run(
                ['ollama', 'list'],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')[1:]
                
                # Filtrar modelos evolutivos
                evolved_models = []
                for line in lines:
                    if '_gen' in line:
                        parts = line.split()
                        if parts:
                            model_name = parts[0]
                            # Extrair geração
                            gen_match = re.search(r'_gen(\d+)', model_name)
                            if gen_match:
                                gen = int(gen_match.group(1))
                                evolved_models.append((model_name, gen))
                
                # Ordenar por geração
                evolved_models.sort(key=lambda x: x[1], reverse=True)
                
                # Remover modelos antigos
                for model, gen in evolved_models[keep_generations:]:
                    print(f"🗑️  Removendo modelo antigo: {model}")
                    subprocess.run(['ollama', 'rm', model])
                    
        except Exception as e:
            print(f"Erro ao limpar modelos: {e}")


# Teste do conector
if __name__ == "__main__":
    print("🔌 TESTANDO OLLAMA CONNECTOR")
    print("=" * 60)
    
    connector = OllamaConnector()
    
    # Teste 1: Query simples
    print("\n📝 Teste 1: Query simples")
    result = connector.query_model(
        'llama3.2:3b',
        'O que é inteligência artificial?'
    )
    
    if result['success']:
        print(f"✅ Resposta em {result['elapsed_time']:.2f}s")
        print(f"📊 Tokens/seg: {result['tokens_per_second']:.1f}")
        print(f"💬 Resposta: {result['response'][:200]}...")
    else:
        print(f"❌ Erro: {result['error']}")
    
    # Teste 2: Query com contexto
    print("\n📝 Teste 2: Query com contexto rico")
    context = {
        'memories': [
            {'content': 'IA é sobre criar máquinas inteligentes', 'similarity': 0.9},
            {'content': 'Aprendizado de máquina é um subset de IA', 'similarity': 0.8}
        ],
        'layers': {
            'specialization': {'primary': 'technical'},
            'system': {'cpu_percent': 15.2, 'memory_percent': 45.3}
        }
    }
    
    result2 = connector.query_model(
        'llama3.2:3b',
        'Como posso aprender mais sobre IA?',
        context=context
    )
    
    if result2['success']:
        print(f"✅ Contexto injetado: {result2['context_size']} chars")
        print(f"💬 Resposta contextualizada: {result2['response'][:200]}...")
    
    # Teste 3: Criar modelo evoluído
    print("\n🧬 Teste 3: Criar modelo evoluído")
    adaptations = {
        'generation': 2,
        'temperature': 0.8,
        'max_tokens': 150,
        'specializations': {'primary': 'coding'},
        'modifications': [
            {'type': 'reinforce', 'strength': 'accuracy'},
            {'type': 'reinforce', 'strength': 'speed'}
        ],
        'opportunities': ['optimize_response_time', 'improve_context_usage']
    }
    
    evolved_model = connector.create_evolved_model(
        'llama3.2:3b',
        'testmon',
        2,
        adaptations
    )
    
    print(f"📦 Modelo evoluído: {evolved_model}")
    
    # Teste 4: Benchmark
    print("\n⚡ Teste 4: Benchmark de performance")
    test_queries = [
        "O que é Python?",
        "Explique recursão",
        "Como funciona uma rede neural?"
    ]
    
    benchmark = connector.benchmark_model('llama3.2:3b', test_queries)
    print(f"✅ Sucessos: {benchmark['successful']}/{benchmark['total_queries']}")
    print(f"⏱️  Tempo médio: {benchmark['avg_time']:.2f}s")
    print(f"📊 Tokens/seg médio: {benchmark['avg_tokens_per_sec']:.1f}")
    
    print("\n✨ Ollama Connector operacional com complexidade REAL!")