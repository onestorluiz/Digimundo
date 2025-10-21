#!/usr/bin/env python3
"""
🤖 OLLAMA SERVICE - Serviço de Integração com Modelos LLM
FASE 22: Integração Ollama no Sistema Principal
"""

import logging
import json
from typing import Dict, List, Optional, Any, Tuple
from pathlib import Path
import subprocess
import time
from enum import Enum

from .ollama_core import OllamaCore

logger = logging.getLogger(__name__)

class ModelPurpose(Enum):
    """Propósitos específicos para seleção de modelo"""
    ANALYSIS = "analysis"           # Análise de roteiros
    COMPRESSION = "compression"      # Ajuda na compressão DigiLang
    TRANSLATION = "translation"      # Tradução de textos
    SUMMARY = "summary"             # Resumos e sinopses
    DIALOGUE = "dialogue"           # Análise de diálogos
    CHARACTER = "character"         # Análise de personagens
    GENERAL = "general"            # Uso geral

class OllamaService:
    """
    Serviço unificado para integração com Ollama
    Gerencia modelos, prompts e cache de respostas
    """

    def __init__(self):
        self.core = OllamaCore()
        self.stats = {
            'total_queries': 0,
            'cache_hits': 0,
            'total_tokens': 0,
            'total_time': 0
        }

        # Mapeamento de propósitos para modelos preferidos
        self.purpose_models = {
            ModelPurpose.ANALYSIS: ['deepseek-r1:32b', 'mistral:instruct'],
            ModelPurpose.COMPRESSION: ['llama3.1:8b', 'mistral:latest'],
            ModelPurpose.TRANSLATION: ['mistral:instruct', 'mixtral:latest'],
            ModelPurpose.SUMMARY: ['mistral:latest', 'llama3.1:8b'],
            ModelPurpose.DIALOGUE: ['deepseek-r1:32b', 'mistral:instruct'],
            ModelPurpose.CHARACTER: ['deepseek-r1:32b', 'mistral:instruct'],
            ModelPurpose.GENERAL: ['mistral:latest', 'llama3.1:8b']
        }

        # Templates de prompts para cada propósito
        self.prompt_templates = {
            ModelPurpose.ANALYSIS: """Analise o seguinte roteiro cinematográfico:

{content}

Forneça:
1. Estrutura narrativa (atos e pontos de virada)
2. Arco dos personagens principais
3. Temas centrais
4. Qualidade dos diálogos
5. Sugestões de melhoria""",

            ModelPurpose.COMPRESSION: """Identifique padrões repetitivos no texto a seguir que podem ser comprimidos:

{content}

Liste:
1. Palavras/frases mais frequentes
2. Padrões estruturais repetitivos
3. Elementos que podem ser simbolizados
4. Estimativa de economia de tokens""",

            ModelPurpose.TRANSLATION: """Traduza o seguinte texto cinematográfico mantendo formatação de roteiro:

{content}

Mantenha:
- Formatação original
- Nomes de personagens em MAIÚSCULAS
- Indicações técnicas (INT./EXT.)
- Parênteses de ação""",

            ModelPurpose.SUMMARY: """Crie um resumo executivo do seguinte roteiro:

{content}

Inclua:
- Logline (1 linha)
- Sinopse curta (3-5 linhas)
- Personagens principais
- Conflito central
- Tom e gênero""",

            ModelPurpose.DIALOGUE: """Analise os diálogos do seguinte roteiro:

{content}

Avalie:
1. Naturalidade e fluidez
2. Voz única de cada personagem
3. Subtexto e conflito
4. Exposição vs. ação
5. Momentos memoráveis""",

            ModelPurpose.CHARACTER: """Analise os personagens do roteiro:

{content}

Para cada personagem principal:
1. Objetivo/motivação
2. Arco de transformação
3. Conflitos internos/externos
4. Relacionamentos
5. Consistência""",

            ModelPurpose.GENERAL: """{content}"""
        }

        logger.info("🤖 Ollama Service inicializado")
        logger.info(f"   Modelos disponíveis: {len(self.core.models)}")
        logger.info(f"   Modelo padrão: {self.core.default_model}")

    def query(self, content: str, purpose: ModelPurpose = ModelPurpose.GENERAL,
              model: Optional[str] = None, use_cache: bool = True) -> Tuple[str, Dict]:
        """
        Envia query para Ollama com propósito específico

        Args:
            content: Conteúdo para análise
            purpose: Propósito da query (determina modelo e prompt)
            model: Modelo específico (override automático)
            use_cache: Usar cache de respostas

        Returns:
            Tupla (resposta, metadados)
        """
        start_time = time.time()

        # Selecionar modelo baseado no propósito
        if model is None:
            model = self._select_model_for_purpose(purpose)

        # Preparar prompt
        if purpose in self.prompt_templates:
            prompt = self.prompt_templates[purpose].format(content=content)
        else:
            prompt = content

        # Verificar cache
        cache_key = f"{model}:{purpose.value}:{hash(prompt)}"
        if use_cache and cache_key in self.core.cache:
            self.stats['cache_hits'] += 1
            logger.info(f"📋 Cache hit para {purpose.value}")
            return self.core.cache[cache_key], {'cached': True, 'model': model}

        # Executar query
        try:
            response = self.core.query(prompt, model)

            # Atualizar cache
            if use_cache:
                self.core.cache[cache_key] = response

            # Atualizar estatísticas
            elapsed = time.time() - start_time
            self.stats['total_queries'] += 1
            self.stats['total_time'] += elapsed

            # Estimar tokens (aproximado)
            estimated_tokens = len(prompt.split()) + len(response.split())
            self.stats['total_tokens'] += estimated_tokens

            metadata = {
                'cached': False,
                'model': model,
                'purpose': purpose.value,
                'elapsed_time': elapsed,
                'estimated_tokens': estimated_tokens
            }

            logger.info(f"✅ Query {purpose.value} completada em {elapsed:.2f}s")

            return response, metadata

        except Exception as e:
            logger.error(f"❌ Erro na query: {e}")
            # Tentar fallback
            if model != self.core.default_model:
                logger.info(f"🔄 Tentando fallback com {self.core.default_model}")
                return self.query(content, purpose, self.core.default_model, use_cache)
            raise

    def _select_model_for_purpose(self, purpose: ModelPurpose) -> str:
        """
        Seleciona o melhor modelo disponível para o propósito

        Args:
            purpose: Propósito da análise

        Returns:
            Nome do modelo selecionado
        """
        preferred = self.purpose_models.get(purpose, [self.core.default_model])

        # Encontrar primeiro modelo disponível da lista de preferidos
        for model in preferred:
            if model in self.core.models:
                logger.debug(f"🎯 Selecionado {model} para {purpose.value}")
                return model

        # Fallback para modelo padrão
        return self.core.default_model

    def analyze_script(self, script_path: Path) -> Dict[str, Any]:
        """
        Análise completa de um roteiro

        Args:
            script_path: Caminho do arquivo de roteiro

        Returns:
            Dicionário com análises completas
        """
        if not script_path.exists():
            raise FileNotFoundError(f"Roteiro não encontrado: {script_path}")

        with open(script_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Limitar tamanho para evitar overflow
        max_chars = 50000
        if len(content) > max_chars:
            logger.warning(f"⚠️ Roteiro muito grande, truncando para {max_chars} caracteres")
            content = content[:max_chars]

        results = {}

        # Executar análises em ordem de prioridade
        analyses = [
            (ModelPurpose.SUMMARY, "summary"),
            (ModelPurpose.ANALYSIS, "structure"),
            (ModelPurpose.CHARACTER, "characters"),
            (ModelPurpose.DIALOGUE, "dialogue")
        ]

        for purpose, key in analyses:
            try:
                logger.info(f"🔍 Executando análise: {key}")
                response, metadata = self.query(content, purpose)
                results[key] = {
                    'analysis': response,
                    'metadata': metadata
                }
            except Exception as e:
                logger.error(f"❌ Erro em análise {key}: {e}")
                results[key] = {'error': str(e)}

        # Adicionar metadados gerais
        results['metadata'] = {
            'script_path': str(script_path),
            'script_size': len(content),
            'total_analyses': len(analyses),
            'successful': sum(1 for r in results.values() if 'error' not in r)
        }

        return results

    def compress_helper(self, text: str) -> Dict[str, Any]:
        """
        Auxilia na identificação de padrões para compressão DigiLang

        Args:
            text: Texto para análise de compressão

        Returns:
            Sugestões de compressão
        """
        response, metadata = self.query(text[:10000], ModelPurpose.COMPRESSION)

        # Parse da resposta para extrair padrões
        patterns = self._parse_compression_patterns(response)

        return {
            'patterns': patterns,
            'analysis': response,
            'metadata': metadata
        }

    def _parse_compression_patterns(self, response: str) -> List[Dict]:
        """
        Extrai padrões de compressão da resposta do modelo

        Args:
            response: Resposta do modelo

        Returns:
            Lista de padrões identificados
        """
        patterns = []

        # Buscar padrões mencionados na resposta
        lines = response.split('\n')
        for line in lines:
            # Procurar por padrões entre aspas ou após dois pontos
            if '"' in line:
                import re
                quoted = re.findall(r'"([^"]+)"', line)
                for q in quoted:
                    if len(q) > 2:  # Ignorar strings muito curtas
                        patterns.append({
                            'text': q,
                            'type': 'quoted',
                            'frequency': 'unknown'
                        })

        return patterns

    def get_stats(self) -> Dict:
        """Retorna estatísticas do serviço"""
        return {
            **self.stats,
            'models_available': list(self.core.models.keys()),
            'default_model': self.core.default_model,
            'cache_size': len(self.core.cache),
            'cache_hit_rate': (
                self.stats['cache_hits'] / max(self.stats['total_queries'], 1)
            ),
            'average_query_time': (
                self.stats['total_time'] / max(self.stats['total_queries'], 1)
            )
        }

    def list_models(self) -> List[str]:
        """Lista todos os modelos disponíveis"""
        return list(self.core.models.keys())

    def set_default_model(self, model: str) -> bool:
        """
        Define modelo padrão

        Args:
            model: Nome do modelo

        Returns:
            True se sucesso
        """
        if model in self.core.models:
            self.core.default_model = model
            logger.info(f"✅ Modelo padrão alterado para: {model}")
            return True

        logger.error(f"❌ Modelo não disponível: {model}")
        return False

    def clear_cache(self):
        """Limpa cache de respostas"""
        self.core.cache.clear()
        logger.info("🧹 Cache limpo")

    def health_check(self) -> Dict[str, Any]:
        """
        Verifica saúde do serviço Ollama

        Returns:
            Status do serviço
        """
        try:
            # Verificar se Ollama está rodando
            result = subprocess.run(
                ["ollama", "list"],
                capture_output=True,
                text=True,
                timeout=5
            )

            ollama_running = result.returncode == 0

            # Teste rápido com modelo padrão
            if ollama_running:
                test_response = self.core.query("Test", self.core.default_model)
                model_working = len(test_response) > 0
            else:
                model_working = False

            return {
                'healthy': ollama_running and model_working,
                'ollama_running': ollama_running,
                'model_working': model_working,
                'models_count': len(self.core.models),
                'default_model': self.core.default_model
            }

        except Exception as e:
            return {
                'healthy': False,
                'error': str(e)
            }


def test_ollama_service():
    """Testa o serviço Ollama"""

    service = OllamaService()

    print("🧪 TESTANDO OLLAMA SERVICE")
    print("="*60)

    # 1. Health check
    print("\n1. Health Check:")
    health = service.health_check()
    print(f"   Status: {'✅ Saudável' if health['healthy'] else '❌ Com problemas'}")
    print(f"   Modelos: {health.get('models_count', 0)}")

    # 2. Listar modelos
    print("\n2. Modelos Disponíveis:")
    models = service.list_models()
    for model in models[:5]:  # Mostrar apenas primeiros 5
        print(f"   - {model}")

    # 3. Teste de query simples
    print("\n3. Teste de Query:")
    test_script = """FADE IN:

INT. COFFEE SHOP - DAY

JOHN enters looking nervous.

JOHN
Is anyone here?

MARY appears from behind the counter.

MARY
Just us.

FADE OUT."""

    response, metadata = service.query(
        test_script,
        ModelPurpose.SUMMARY
    )
    print(f"   Modelo usado: {metadata['model']}")
    print(f"   Tempo: {metadata.get('elapsed_time', 0):.2f}s")
    print(f"   Resposta: {response[:200]}...")

    # 4. Estatísticas
    print("\n4. Estatísticas:")
    stats = service.get_stats()
    print(f"   Total queries: {stats['total_queries']}")
    print(f"   Cache hits: {stats['cache_hits']}")
    print(f"   Taxa de cache: {stats['cache_hit_rate']:.1%}")

    print("\n✅ Testes concluídos!")


if __name__ == "__main__":
    test_ollama_service()