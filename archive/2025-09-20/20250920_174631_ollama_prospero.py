#!/usr/bin/env python3
"""
FASE 14 - Sistema Ollama Próspero
Gerenciamento avançado de modelos com nomenclatura próspera
DIGIMUNDO PRESENTE
"""

import os
import json
import subprocess
import logging
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime
from pathlib import Path
import hashlib
import time
from dataclasses import dataclass
from enum import Enum

# Configuração de logging robusto
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('OllamaPróspero')


class ModeloPróspero(Enum):
    """Nomenclatura próspera para modelos"""
    # Modelos de Criação
    GENESIS = "llama3.2:1b"           # Modelo inicial, leve
    AURORA = "llama3.2:3b"            # Despertar criativo
    HORIZONTE = "llama3.1:8b"         # Expansão de possibilidades

    # Modelos de Análise
    CRISTAL = "mistral:7b"            # Clareza e precisão
    PRISMA = "mixtral:8x7b"           # Múltiplas perspectivas
    ESPELHO = "gemma2:9b"             # Reflexão profunda

    # Modelos de Síntese
    ALQUIMIA = "codellama:7b"         # Transformação de código
    SINFONIA = "phi3:14b"             # Harmonia de ideias
    COSMOS = "llama3.1:70b"           # Visão universal

    # Modelos Especializados
    ESCRIBA = "screenplay-llama:7b"   # Especialista em roteiros
    NARRATIVA = "story-mixtral:8x7b"  # Mestre de histórias
    DIÁLOGO = "dialogue-phi:3b"       # Especialista em diálogos


@dataclass
class RespostaPrósperaCache:
    """Cache de respostas prósperas"""
    modelo: str
    prompt: str
    resposta: str
    timestamp: datetime
    tokens_usados: int
    tempo_resposta: float
    hash_id: str


class OllamaPróspero:
    """
    Sistema Ollama Próspero - Gerenciamento avançado de modelos
    """

    def __init__(self, cache_dir: str = "data/ollama_cache"):
        """
        Inicializa sistema próspero

        Args:
            cache_dir: Diretório para cache de respostas
        """
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

        # Cache em memória para respostas recentes
        self.memory_cache: Dict[str, RespostaPrósperaCache] = {}

        # Estatísticas de uso
        self.stats = {
            'total_requests': 0,
            'cache_hits': 0,
            'total_tokens': 0,
            'total_time': 0.0,
            'model_usage': {}
        }

        # Configurações prósperas
        self.config = {
            'max_memory_cache': 100,
            'cache_ttl_hours': 24,
            'retry_attempts': 3,
            'timeout_seconds': 300,
            'temperature_default': 0.7,
            'max_tokens_default': 2048
        }

        logger.info("🌟 Sistema Ollama Próspero inicializado")
        self._verificar_ollama()
        self._carregar_cache_persistente()

    def _verificar_ollama(self) -> bool:
        """Verifica se Ollama está instalado e rodando"""
        try:
            result = subprocess.run(
                ['ollama', 'list'],
                capture_output=True,
                text=True,
                timeout=30
            )
            if result.returncode == 0:
                logger.info("✅ Ollama detectado e operacional")
                self._listar_modelos_disponíveis()
                return True
            else:
                logger.warning("⚠️ Ollama não está respondendo")
                return False
        except FileNotFoundError:
            logger.error("❌ Ollama não está instalado")
            return False
        except subprocess.TimeoutExpired:
            logger.warning("⚠️ Ollama timeout - pode estar inicializando")
            return False

    def _listar_modelos_disponíveis(self) -> List[str]:
        """Lista modelos disponíveis no sistema"""
        try:
            result = subprocess.run(
                ['ollama', 'list'],
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')[1:]  # Skip header
                modelos = []
                for line in lines:
                    if line.strip():
                        parts = line.split()
                        if parts:
                            modelos.append(parts[0])

                logger.info(f"📚 Modelos disponíveis: {modelos}")
                return modelos

        except Exception as e:
            logger.error(f"Erro listando modelos: {e}")

        return []

    def _gerar_hash(self, modelo: str, prompt: str) -> str:
        """Gera hash único para cache"""
        content = f"{modelo}:{prompt}"
        return hashlib.sha256(content.encode()).hexdigest()

    def _salvar_cache(self, cache_entry: RespostaPrósperaCache):
        """Salva entrada no cache"""
        # Salvar em memória
        if len(self.memory_cache) >= self.config['max_memory_cache']:
            # Remove entrada mais antiga
            oldest = min(self.memory_cache.values(), key=lambda x: x.timestamp)
            del self.memory_cache[oldest.hash_id]

        self.memory_cache[cache_entry.hash_id] = cache_entry

        # Salvar em disco
        cache_file = self.cache_dir / f"{cache_entry.hash_id[:8]}.json"
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump({
                'modelo': cache_entry.modelo,
                'prompt': cache_entry.prompt[:100],  # Salvar apenas início
                'resposta': cache_entry.resposta,
                'timestamp': cache_entry.timestamp.isoformat(),
                'tokens_usados': cache_entry.tokens_usados,
                'tempo_resposta': cache_entry.tempo_resposta
            }, f, ensure_ascii=False, indent=2)

    def _carregar_cache_persistente(self):
        """Carrega cache do disco para memória"""
        cache_files = list(self.cache_dir.glob("*.json"))
        loaded = 0

        for cache_file in cache_files[-self.config['max_memory_cache']:]:
            try:
                with open(cache_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                # Verificar idade do cache
                timestamp = datetime.fromisoformat(data['timestamp'])
                age_hours = (datetime.now() - timestamp).total_seconds() / 3600

                if age_hours < self.config['cache_ttl_hours']:
                    # Recriar hash baseado no prompt salvo
                    hash_id = cache_file.stem + cache_file.suffix[:-5]  # Remove .json

                    cache_entry = RespostaPrósperaCache(
                        modelo=data['modelo'],
                        prompt=data['prompt'],
                        resposta=data['resposta'],
                        timestamp=timestamp,
                        tokens_usados=data.get('tokens_usados', 0),
                        tempo_resposta=data.get('tempo_resposta', 0),
                        hash_id=hash_id
                    )

                    self.memory_cache[hash_id] = cache_entry
                    loaded += 1
            except Exception as e:
                logger.debug(f"Erro carregando cache {cache_file}: {e}")

        if loaded > 0:
            logger.info(f"📂 {loaded} entradas de cache carregadas")

    def invocar_modelo(
        self,
        modelo: ModeloPróspero,
        prompt: str,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        usar_cache: bool = True,
        stream: bool = False
    ) -> Dict[str, Any]:
        """
        Invoca modelo próspero com cache inteligente

        Args:
            modelo: Enum do modelo próspero
            prompt: Prompt para o modelo
            temperature: Temperatura da geração
            max_tokens: Máximo de tokens
            usar_cache: Se deve usar cache
            stream: Se deve fazer streaming

        Returns:
            Dict com resposta e metadados
        """
        self.stats['total_requests'] += 1

        # Verificar cache
        hash_id = self._gerar_hash(modelo.value, prompt)

        if usar_cache and hash_id in self.memory_cache:
            self.stats['cache_hits'] += 1
            cache_entry = self.memory_cache[hash_id]

            logger.info(f"✨ Cache hit para {modelo.name}")

            return {
                'success': True,
                'modelo': modelo.name,
                'resposta': cache_entry.resposta,
                'tokens': cache_entry.tokens_usados,
                'tempo': cache_entry.tempo_resposta,
                'cache': True
            }

        # Preparar comando
        temp = temperature or self.config['temperature_default']
        tokens = max_tokens or self.config['max_tokens_default']

        # Invocar modelo
        logger.info(f"🚀 Invocando {modelo.name} ({modelo.value})")

        start_time = time.time()

        try:
            # Construir comando Ollama
            cmd = [
                'ollama', 'run',
                modelo.value,
                '--verbose'
            ]

            # Adicionar parâmetros
            full_prompt = f"""Temperature: {temp}
Max tokens: {tokens}

{prompt}"""

            # Executar
            result = subprocess.run(
                cmd,
                input=full_prompt,
                capture_output=True,
                text=True,
                timeout=self.config['timeout_seconds']
            )

            elapsed_time = time.time() - start_time

            if result.returncode == 0:
                resposta = result.stdout.strip()

                # Estimar tokens (aproximado)
                tokens_usados = len(resposta.split()) * 1.3

                # Atualizar estatísticas
                self.stats['total_tokens'] += int(tokens_usados)
                self.stats['total_time'] += elapsed_time

                if modelo.name not in self.stats['model_usage']:
                    self.stats['model_usage'][modelo.name] = 0
                self.stats['model_usage'][modelo.name] += 1

                # Salvar no cache
                cache_entry = RespostaPrósperaCache(
                    modelo=modelo.value,
                    prompt=prompt,
                    resposta=resposta,
                    timestamp=datetime.now(),
                    tokens_usados=int(tokens_usados),
                    tempo_resposta=elapsed_time,
                    hash_id=hash_id
                )
                self._salvar_cache(cache_entry)

                logger.info(f"✅ {modelo.name} respondeu em {elapsed_time:.2f}s")

                return {
                    'success': True,
                    'modelo': modelo.name,
                    'resposta': resposta,
                    'tokens': int(tokens_usados),
                    'tempo': elapsed_time,
                    'cache': False
                }

            else:
                logger.error(f"❌ Erro do modelo: {result.stderr}")
                return {
                    'success': False,
                    'erro': result.stderr,
                    'modelo': modelo.name
                }

        except subprocess.TimeoutExpired:
            logger.error(f"⏱️ Timeout após {self.config['timeout_seconds']}s")
            return {
                'success': False,
                'erro': 'Timeout',
                'modelo': modelo.name
            }
        except Exception as e:
            logger.error(f"❌ Erro invocando modelo: {e}")
            return {
                'success': False,
                'erro': str(e),
                'modelo': modelo.name
            }

    def análise_roteiro(
        self,
        texto_roteiro: str,
        tipo_análise: str = "completa"
    ) -> Dict[str, Any]:
        """
        Análise próspera de roteiro usando múltiplos modelos

        Args:
            texto_roteiro: Texto do roteiro
            tipo_análise: Tipo de análise (completa, estrutura, diálogo, personagem)

        Returns:
            Dict com análises múltiplas
        """
        logger.info(f"🎬 Iniciando análise próspera: {tipo_análise}")

        resultados = {}

        # Análise de estrutura com CRISTAL
        if tipo_análise in ["completa", "estrutura"]:
            prompt_estrutura = f"""Analise a estrutura deste roteiro:

{texto_roteiro[:2000]}

Identifique:
1. Atos e pontos de virada
2. Arco dramático
3. Ritmo e pacing
4. Elementos visuais dominantes"""

            resultados['estrutura'] = self.invocar_modelo(
                ModeloPróspero.CRISTAL,
                prompt_estrutura
            )

        # Análise de diálogos com DIÁLOGO
        if tipo_análise in ["completa", "diálogo"]:
            prompt_dialogo = f"""Analise os diálogos deste roteiro:

{texto_roteiro[:2000]}

Avalie:
1. Naturalidade e fluidez
2. Voz única dos personagens
3. Subtexto e conflito
4. Economia e impacto"""

            resultados['dialogo'] = self.invocar_modelo(
                ModeloPróspero.AURORA,  # Usar AURORA já que DIÁLOGO é custom
                prompt_dialogo
            )

        # Síntese com ESPELHO
        if tipo_análise == "completa":
            prompt_sintese = f"""Faça uma síntese profunda deste roteiro:

{texto_roteiro[:1500]}

Considere:
1. Tema central e mensagem
2. Potencial comercial e artístico
3. Pontos fortes e fracos
4. Recomendações de melhoria"""

            resultados['sintese'] = self.invocar_modelo(
                ModeloPróspero.ESPELHO,
                prompt_sintese
            )

        return resultados

    def gerar_estatísticas(self) -> Dict[str, Any]:
        """Gera estatísticas de uso do sistema"""
        return {
            'resumo': {
                'total_requisições': self.stats['total_requests'],
                'cache_hits': self.stats['cache_hits'],
                'taxa_cache': f"{(self.stats['cache_hits'] / max(1, self.stats['total_requests']) * 100):.1f}%",
                'total_tokens': self.stats['total_tokens'],
                'tempo_total': f"{self.stats['total_time']:.2f}s"
            },
            'modelos_mais_usados': dict(
                sorted(
                    self.stats['model_usage'].items(),
                    key=lambda x: x[1],
                    reverse=True
                )[:5]
            ),
            'cache_status': {
                'entradas_memória': len(self.memory_cache),
                'tamanho_disco': sum(
                    f.stat().st_size for f in self.cache_dir.glob("*.json")
                ) / (1024 * 1024),  # MB
                'idade_média_horas': sum(
                    (datetime.now() - c.timestamp).total_seconds() / 3600
                    for c in self.memory_cache.values()
                ) / max(1, len(self.memory_cache))
            }
        }

    def instalar_modelo(self, modelo: ModeloPróspero) -> bool:
        """
        Instala modelo próspero se não estiver disponível

        Args:
            modelo: Modelo a instalar

        Returns:
            True se instalado com sucesso
        """
        logger.info(f"📦 Instalando modelo {modelo.name} ({modelo.value})")

        try:
            result = subprocess.run(
                ['ollama', 'pull', modelo.value],
                capture_output=True,
                text=True,
                timeout=600  # 10 minutos para download
            )

            if result.returncode == 0:
                logger.info(f"✅ {modelo.name} instalado com sucesso")
                return True
            else:
                logger.error(f"❌ Erro instalando: {result.stderr}")
                return False

        except subprocess.TimeoutExpired:
            logger.error("⏱️ Timeout na instalação")
            return False
        except Exception as e:
            logger.error(f"❌ Erro: {e}")
            return False

    def criar_modelo_customizado(
        self,
        nome: str,
        base_model: ModeloPróspero,
        system_prompt: str,
        examples: List[Tuple[str, str]] = None
    ) -> bool:
        """
        Cria modelo customizado para tarefas específicas

        Args:
            nome: Nome do modelo customizado
            base_model: Modelo base
            system_prompt: Prompt do sistema
            examples: Exemplos de entrada/saída

        Returns:
            True se criado com sucesso
        """
        logger.info(f"🔧 Criando modelo customizado: {nome}")

        # Criar Modelfile
        modelfile_content = f"""FROM {base_model.value}

SYSTEM {system_prompt}

PARAMETER temperature 0.8
PARAMETER top_p 0.9
PARAMETER top_k 40
"""

        # Adicionar exemplos se fornecidos
        if examples:
            for input_ex, output_ex in examples[:3]:  # Máximo 3 exemplos
                modelfile_content += f"""
MESSAGE user {input_ex}
MESSAGE assistant {output_ex}
"""

        # Salvar Modelfile
        modelfile_path = self.cache_dir / f"{nome}.modelfile"
        with open(modelfile_path, 'w', encoding='utf-8') as f:
            f.write(modelfile_content)

        # Criar modelo no Ollama
        try:
            result = subprocess.run(
                ['ollama', 'create', nome, '-f', str(modelfile_path)],
                capture_output=True,
                text=True,
                timeout=300
            )

            if result.returncode == 0:
                logger.info(f"✅ Modelo {nome} criado com sucesso")
                return True
            else:
                logger.error(f"❌ Erro criando modelo: {result.stderr}")
                return False

        except Exception as e:
            logger.error(f"❌ Erro: {e}")
            return False


def main():
    """Teste do sistema Ollama Próspero"""

    # Inicializar sistema
    ollama = OllamaPróspero()

    print("\n" + "="*60)
    print("SISTEMA OLLAMA PRÓSPERO - TESTE")
    print("="*60)

    # Teste 1: Invocar modelo simples
    print("\n📝 Teste 1: Geração simples")
    resultado = ollama.invocar_modelo(
        ModeloPróspero.GENESIS,
        "Escreva uma cena curta de FADE IN para um filme noir",
        temperature=0.9
    )

    if resultado['success']:
        print(f"✅ Resposta em {resultado['tempo']:.2f}s")
        print(f"Tokens: {resultado['tokens']}")
        print(f"Cache: {resultado['cache']}")
        print(f"\nResposta:\n{resultado['resposta'][:500]}...")
    else:
        print(f"❌ Erro: {resultado['erro']}")

    # Teste 2: Análise de roteiro
    print("\n🎬 Teste 2: Análise de roteiro")

    roteiro_sample = """FADE IN:

INT. DETECTIVE'S OFFICE - NIGHT

A dimly lit room filled with smoke. DETECTIVE JONES (45, weathered face)
sits behind a cluttered desk, nursing a whiskey.

DETECTIVE JONES
(to himself)
Another night, another case that
doesn't add up.

The door CREAKS open. A MYSTERIOUS WOMAN (30s, red dress) enters.

MYSTERIOUS WOMAN
Detective Jones? I need your help.

CUT TO:"""

    análise = ollama.análise_roteiro(roteiro_sample, "estrutura")

    for tipo, resultado in análise.items():
        if resultado['success']:
            print(f"\n✅ Análise {tipo}: {resultado['resposta'][:200]}...")

    # Estatísticas
    print("\n📊 Estatísticas do Sistema:")
    stats = ollama.gerar_estatísticas()
    print(json.dumps(stats, indent=2, ensure_ascii=False))

    print("\n" + "="*60)
    print("DIGIMUNDO PRESENTE")
    print("="*60)


if __name__ == "__main__":
    main()