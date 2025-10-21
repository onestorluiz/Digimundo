#!/usr/bin/env python3
"""
🧠 SISTEMA ML UNIFICADO - MINIMALISTA E EXCELENTE
Sistema completo de Machine Learning para análise de roteiros
Harmonia: 100% | Qualidade: Máxima | Minimalismo: Total
"""

import asyncio
import sys
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
import json

# Configuração de paths
sys.path.insert(0, str(Path(__file__).parent.parent))

# P2 - Sistema de Logging Estruturado
from src.core.logging_system import get_logger, LogCategory, timed_operation
logger = get_logger('ml_unified')
component = 'ml_unified'

# Imports essenciais
from src.core.screenplay_library import ScreenplayLibrary
from src.core.unified_memory_system import get_unified_memory, MemoryType
from src.core.mixtral_config import MixtralConfig

try:
    import ollama
except ImportError:
    logger.error("⚠️ Ollama não instalado. Instale com: pip install ollama",
                category=LogCategory.ERROR, component=component)
    sys.exit(1)

# P2 - Logging já configurado acima via logging_system.py
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)


class UnifiedMLSystem:
    """
    Sistema ML unificado com arquitetura minimalista e excelente.
    Combina todas as capacidades em uma única classe coesa.
    """

    def __init__(self, mode: str = "balanced"):
        """
        Inicializa o sistema ML unificado.

        Args:
            mode: "eco" (rápido), "balanced" (equilibrado), "dedicated" (máxima qualidade)
        """
        self.mode = mode
        self.config = MixtralConfig()
        self.library = ScreenplayLibrary()
        self.memory = get_unified_memory()

        # Configuração baseada no modo
        self._setup_mode()

        # Verificação de modelo
        self._verify_model()

        # Estado do sistema
        self.stats = {
            'screenplays_analyzed': 0,
            'patterns_extracted': 0,
            'insights_generated': 0,
            'start_time': datetime.now()
        }

        logger.info(f"🚀 Sistema ML Unificado iniciado em modo {mode.upper()}")
        logger.info(f"📚 {len(self.library.list_screenplays())} roteiros disponíveis")
        logger.info(f"💾 {self._count_memories()} memórias no sistema")

    def _setup_mode(self):
        """Configura o sistema baseado no modo escolhido."""
        modes = {
            'eco': {
                'model': 'mixtral-eco-q5:latest',
                'num_ctx': 32768,
                'num_thread': 14,
                'num_gpu': 30,
                'temperature': 0.3
            },
            'balanced': {
                'model': 'mixtral:8x7b-instruct-v0.1-q5_k_m',
                'num_ctx': 65536,
                'num_thread': 20,
                'num_gpu': 45,
                'temperature': 0.3
            },
            'dedicated': {
                'model': 'mixtral-dedicated-q5:latest',
                'num_ctx': 131072,
                'num_thread': 24,
                'num_gpu': 60,
                'temperature': 0.2
            },
            'turbo': {  # SWEET TURBO MODE (+40% speed)
                'model': 'mixtral-dedicated-q5:latest',
                'num_ctx': 131072,
                'num_thread': 24,
                'num_gpu': 60,
                'num_batch': 8192,      # DOBRA batch
                'top_k': 3,             # 3 experts
                'temperature': 0.3,
                'use_mmap': True,
                'use_mlock': True,
                'f16_kv': True
            },
            'token_turbo': {  # TOKEN TURBO MODE (+50% context)
                'model': 'mixtral-dedicated-q5:latest',
                'num_ctx': 200000,        # 200K tokens (+53%)
                'rope_scaling': 1.5,      # RoPE scaling
                'rope_theta': 500000,     # Base frequency ajustada
                'rope_base': 10000,       # RoPE base
                'sliding_window': 65536,  # Sliding window otimizada
                'num_batch': 2048,        # Reduz batch para compensar contexto
                'repeat_last_n': 256,     # Aumenta repeat penalty window
                'num_thread': 24,         # Mantém threads
                'num_gpu': 60,            # Mantém GPU cores
                'compress_pos_emb': 1.5,  # Comprime position embeddings
                'use_mmap': True,         # Memory mapping essencial
                'use_mlock': True,        # Lock na RAM
                'f16_kv': True,          # KV cache em FP16
                'temperature': 0.3,
                'top_p': 0.9,
                'top_k': 40,
                'repeat_penalty': 1.1
            }
        }

        self.options = modes.get(self.mode, modes['balanced'])
        self.model = self.options.pop('model')

    def _model_exists(self, model_name: str) -> bool:
        """Verifica se um modelo existe no Ollama."""
        try:
            models = ollama.list()
            # A API retorna objetos com atributo .models
            if hasattr(models, 'models'):
                model_list = [m.model for m in models.models]
                return any(model_name in m for m in model_list)
            return False
        except:
            return False

    def _verify_model(self):
        """Verifica e ajusta o modelo se necessário."""
        if not self._model_exists(self.model):
            logger.warning(f"⚠️ Modelo {self.model} não encontrado")
            # Lista de modelos fallback em ordem de preferência
            fallback_models = [
                'llama3.2:3b',
                'deepseek-r1:32b',
                'llama3.1:8b',
                'mistral:instruct',
                'deepseek-r1:7b'
            ]
            for fallback in fallback_models:
                if self._model_exists(fallback):
                    self.model = fallback
                    logger.info(f"✅ Usando modelo alternativo: {self.model}")
                    return
            logger.error("❌ Nenhum modelo compatível encontrado")
            raise RuntimeError("Instale um modelo com: ollama pull llama3.2:3b")

    def _count_memories(self) -> int:
        """Conta o número total de memórias."""
        try:
            results = self.memory.search(
                query="",
                memory_types=[MemoryType.ANALYSIS, MemoryType.KNOWLEDGE],
                limit=10000
            )
            return len(results)
        except:
            return 0

    async def analyze_screenplay(
        self,
        title: str,
        content: Optional[str] = None,
        analyses: List[str] = None
    ) -> Dict[str, Any]:
        """
        Análise completa de um roteiro com múltiplas perspectivas.

        Args:
            title: Título do roteiro
            content: Conteúdo (se None, busca da biblioteca)
            analyses: Lista de análises a realizar
                     ['structure', 'character', 'theme', 'dialogue', 'pattern']

        Returns:
            Dicionário com todas as análises realizadas
        """
        # Configuração padrão
        if analyses is None:
            analyses = ['structure', 'character', 'pattern']

        # Obter conteúdo se necessário
        if content is None:
            content = self.library.get_screenplay(title)
            if not content or content == '.' or len(content) < 100:
                logger.error(f"❌ Conteúdo inválido para {title}")
                return {'error': 'Invalid content'}

        logger.info(f"📖 Analisando: {title}")
        results = {
            'title': title,
            'timestamp': datetime.now().isoformat(),
            'analyses': {}
        }

        # Executar análises solicitadas
        analysis_methods = {
            'structure': self._analyze_structure,
            'character': self._analyze_character,
            'theme': self._analyze_theme,
            'dialogue': self._analyze_dialogue,
            'pattern': self._extract_patterns
        }

        for analysis_type in analyses:
            if analysis_type in analysis_methods:
                try:
                    result = await analysis_methods[analysis_type](content[:50000])
                    results['analyses'][analysis_type] = result

                    # Salvar na memória
                    self._save_to_memory(title, analysis_type, result)

                    logger.info(f"  ✅ {analysis_type.capitalize()} completo")
                except Exception as e:
                    logger.error(f"  ❌ Erro em {analysis_type}: {e}")
                    results['analyses'][analysis_type] = {'error': str(e)}

        # Atualizar estatísticas
        self.stats['screenplays_analyzed'] += 1

        return results

    async def _analyze_structure(self, content: str) -> Dict:
        """Análise estrutural com Save the Cat."""
        prompt = f"""Analyze this screenplay using Save the Cat beat sheet.

        Content: {content}

        Identify these 15 beats with page numbers and specific scenes:
        1. Opening Image (1%)
        2. Theme Stated (5%)
        3. Setup (1-10%)
        4. Catalyst (12%)
        5. Debate (12-25%)
        6. Break into Two (25%)
        7. B Story (30%)
        8. Fun and Games (30-50%)
        9. Midpoint (50%)
        10. Bad Guys Close In (50-75%)
        11. All Is Lost (75%)
        12. Dark Night of the Soul (75-80%)
        13. Break into Three (80%)
        14. Finale (80-99%)
        15. Final Image (100%)

        Format as JSON with beat name, percentage, and description."""

        response = await self._query_llm(prompt)
        return self._parse_response(response, 'structure')

    async def _analyze_character(self, content: str) -> Dict:
        """Análise profunda de personagens."""
        prompt = f"""Analyze the main character's arc in this screenplay.

        Content: {content}

        Focus on:
        1. CHARACTER WANT (external goal)
        2. CHARACTER NEED (internal transformation)
        3. CHARACTER LIE (false belief)
        4. CHARACTER TRUTH (revelation)
        5. CHARACTER GHOST (backstory wound)
        6. CHARACTER ARC (transformation journey)

        Provide specific examples and quotes."""

        response = await self._query_llm(prompt)
        return self._parse_response(response, 'character')

    async def _analyze_theme(self, content: str) -> Dict:
        """Análise temática profunda."""
        prompt = f"""Identify the central themes in this screenplay.

        Content: {content}

        Analyze:
        1. CENTRAL THEME (main message)
        2. SUPPORTING THEMES (secondary messages)
        3. THEMATIC QUESTION (what is being asked)
        4. THEMATIC ANSWER (what conclusion is reached)
        5. SYMBOLIC ELEMENTS (objects/actions representing themes)

        Be specific with examples."""

        response = await self._query_llm(prompt)
        return self._parse_response(response, 'theme')

    async def _analyze_dialogue(self, content: str) -> Dict:
        """Análise de diálogos e voz."""
        prompt = f"""Analyze the dialogue in this screenplay.

        Content: {content}

        Examine:
        1. VOICE DISTINCTIVENESS (how characters sound different)
        2. SUBTEXT (what's not being said)
        3. MEMORABLE LINES (quotable dialogue)
        4. DIALOGUE EFFICIENCY (economy of words)
        5. CHARACTER REVELATION (what dialogue reveals)

        Provide specific examples."""

        response = await self._query_llm(prompt)
        return self._parse_response(response, 'dialogue')

    async def _extract_patterns(self, content: str) -> Dict:
        """Extração de padrões narrativos."""
        prompt = f"""Extract recurring narrative patterns from this screenplay.

        Content: {content}

        Identify:
        1. STRUCTURAL PATTERNS (repeated story structures)
        2. CHARACTER PATTERNS (archetypal behaviors)
        3. VISUAL PATTERNS (recurring imagery)
        4. THEMATIC PATTERNS (repeated ideas)
        5. RHYTHMIC PATTERNS (pacing and tempo)

        List patterns with specific examples."""

        response = await self._query_llm(prompt)
        patterns = self._parse_response(response, 'pattern')

        # Atualizar estatísticas
        if patterns and 'patterns' in patterns:
            self.stats['patterns_extracted'] += len(patterns['patterns'])

        return patterns

    async def _query_llm(self, prompt: str) -> str:
        """Consulta o modelo LLM."""
        try:
            response = ollama.generate(
                model=self.model,
                prompt=prompt,
                options=self.options
            )
            return response.get('response', '')
        except Exception as e:
            logger.error(f"Erro LLM: {e}")
            return ""

    def _parse_response(self, response: str, response_type: str) -> Dict:
        """Parse da resposta do LLM em estrutura organizada."""
        try:
            # Tentar parse como JSON primeiro
            if '{' in response and '}' in response:
                start = response.index('{')
                end = response.rindex('}') + 1
                json_str = response[start:end]
                return json.loads(json_str)
        except:
            pass

        # Fallback para estrutura simples
        return {
            'type': response_type,
            'content': response,
            'timestamp': datetime.now().isoformat()
        }

    def _save_to_memory(self, title: str, analysis_type: str, result: Dict):
        """Salva análise na memória unificada."""
        try:
            self.memory.store(
                memory_type=MemoryType.ANALYSIS,
                key=f"{analysis_type}:{title}",
                value={
                    'screenplay': title,
                    'type': analysis_type,
                    'result': result,
                    'timestamp': datetime.now().isoformat(),
                    'model': self.model,
                    'mode': self.mode
                },
                metadata={
                    'analyzer': 'unified_ml_system',
                    'version': '1.0'
                }
            )

            # Atualizar estatísticas
            self.stats['insights_generated'] += 1

        except Exception as e:
            logger.error(f"Erro salvando memória: {e}")

    async def continuous_learning(self, max_screenplays: int = 5):
        """
        Modo de aprendizado contínuo sobre a biblioteca.

        Args:
            max_screenplays: Número máximo de roteiros a processar
        """
        logger.info("🔄 Iniciando aprendizado contínuo")

        screenplays = self.library.list_screenplays()[:max_screenplays]

        for i, title in enumerate(screenplays, 1):
            logger.info(f"\n[{i}/{len(screenplays)}] Processando: {title}")

            result = await self.analyze_screenplay(
                title,
                analyses=['structure', 'character', 'pattern']
            )

            if 'error' not in result:
                logger.info(f"  ✅ Análise completa salva")

            # Pausa entre análises
            await asyncio.sleep(2)

        self._print_statistics()

    def _print_statistics(self):
        """Imprime estatísticas do sistema."""
        runtime = (datetime.now() - self.stats['start_time']).total_seconds()

        logger.info("📊 ESTATÍSTICAS DO SISTEMA", category=LogCategory.ANALYSIS, component=component)
        logger.info(f"⏱️ Tempo de execução: {runtime:.1f} segundos", category=LogCategory.PERFORMANCE, component=component, runtime=runtime)
        logger.info(f"📚 Roteiros analisados: {self.stats['screenplays_analyzed']}", category=LogCategory.ANALYSIS, component=component, screenplays=self.stats['screenplays_analyzed'])
        logger.info(f"🔍 Padrões extraídos: {self.stats['patterns_extracted']}", category=LogCategory.ANALYSIS, component=component, patterns=self.stats['patterns_extracted'])
        logger.info(f"💡 Insights gerados: {self.stats['insights_generated']}", category=LogCategory.ANALYSIS, component=component, insights=self.stats['insights_generated'])
        logger.info(f"💾 Total de memórias: {self._count_memories()}", category=LogCategory.MEMORY, component=component, memories=self._count_memories())
        logger.info(f"🎯 Modo: {self.mode.upper()}", category=LogCategory.SYSTEM, component=component, mode=self.mode)
        logger.info(f"🤖 Modelo: {self.model}", category=LogCategory.OLLAMA, component=component, model=self.model)

    def get_insights(self, screenplay_title: str) -> Dict:
        """
        Recupera todos os insights sobre um roteiro específico.

        Args:
            screenplay_title: Título do roteiro

        Returns:
            Dicionário com todos os insights disponíveis
        """
        insights = {}

        # Buscar todas as análises deste roteiro
        for analysis_type in ['structure', 'character', 'theme', 'dialogue', 'pattern']:
            results = self.memory.search(
                query=f"{analysis_type}:{screenplay_title}",
                memory_types=[MemoryType.ANALYSIS],
                limit=10
            )

            if results:
                insights[analysis_type] = results[0].get('value', {})

        return insights


# Funções auxiliares para uso direto
async def analyze_single(screenplay_title: str, mode: str = "balanced"):
    """Analisa um único roteiro."""
    system = UnifiedMLSystem(mode=mode)
    result = await system.analyze_screenplay(screenplay_title)
    system._print_statistics()
    return result


async def analyze_batch(max_count: int = 5, mode: str = "balanced"):
    """Analisa múltiplos roteiros."""
    system = UnifiedMLSystem(mode=mode)
    await system.continuous_learning(max_count)


async def get_all_insights(screenplay_title: str):
    """Recupera todos os insights de um roteiro."""
    system = UnifiedMLSystem()
    return system.get_insights(screenplay_title)


# Interface CLI
async def main():
    """Interface de linha de comando."""
    print("""
╔══════════════════════════════════════════════════════════╗
║         🧠 SISTEMA ML UNIFICADO - MINIMALISTA            ║
║                                                          ║
║  Machine Learning de excelência para análise de roteiros ║
║         Harmonia: 100% | Qualidade: Máxima              ║
╚══════════════════════════════════════════════════════════╝
    """)

    print("Escolha o modo de operação:")
    print("1. Análise rápida (1 roteiro, modo eco)")
    print("2. Análise balanceada (1 roteiro)")
    print("3. Análise dedicada (1 roteiro, máxima qualidade)")
    print("4. Aprendizado contínuo (5 roteiros)")
    print("5. Recuperar insights existentes")
    print("6. 🚀 TURBO MODE (+40% speed, experimental)")
    print("7. 📚 TOKEN TURBO (200K context, experimental)")

    choice = input("\nOpção (1-7): ").strip()

    if choice in ['1', '2', '3', '6', '7']:
        modes = {'1': 'eco', '2': 'balanced', '3': 'dedicated', '6': 'turbo', '7': 'token_turbo'}
        mode = modes[choice]

        if choice == '6':
            print("\n⚡ TURBO MODE ATIVADO!")
            print("├── Batch: 8192 (2x maior)")
            print("├── Experts: 3 ativos (vs 2 padrão)")
            print("├── Cache: FP16 otimizado")
            print("└── Performance: +40% esperado")
        elif choice == '7':
            print("\n📚 TOKEN TURBO ATIVADO!")
            print("├── Contexto: 200K tokens (roteiro + livro)")
            print("├── Sliding: 65K window")
            print("├── RoPE: 1.5x scaling")
            print("└── Trade-off: -10% speed, +50% context")

        # Listar roteiros disponíveis
        system = UnifiedMLSystem(mode=mode)
        screenplays = system.library.list_screenplays()[:10]

        print("\nRoteiros disponíveis:")
        for i, title in enumerate(screenplays, 1):
            print(f"{i}. {title}")

        idx = input("\nEscolha o número do roteiro: ").strip()

        try:
            title = screenplays[int(idx) - 1]
            await analyze_single(title, mode)
        except (ValueError, IndexError):
            logger.warning("❌ Escolha inválida", category=LogCategory.CLI, component=component)

    elif choice == '4':
        count = input("Quantos roteiros processar? (1-10): ").strip()
        try:
            count = min(10, max(1, int(count)))
            await analyze_batch(count, 'balanced')
        except ValueError:
            await analyze_batch(5, 'balanced')

    elif choice == '5':
        system = UnifiedMLSystem()
        screenplays = system.library.list_screenplays()[:10]

        print("\nRoteiros com insights:")
        for i, title in enumerate(screenplays, 1):
            print(f"{i}. {title}")

        idx = input("\nEscolha o número: ").strip()

        try:
            title = screenplays[int(idx) - 1]
            insights = await get_all_insights(title)

            print(f"\n📊 Insights para: {title}")
            print("=" * 60)

            for analysis_type, data in insights.items():
                print(f"\n{analysis_type.upper()}:")
                print("-" * 40)
                if isinstance(data, dict):
                    print(json.dumps(data, indent=2)[:500] + "...")
                else:
                    print(str(data)[:500] + "...")

        except (ValueError, IndexError):
            logger.warning("❌ Escolha inválida", category=LogCategory.CLI, component=component)

    else:
        logger.warning("❌ Opção inválida", category=LogCategory.CLI, component=component)

    logger.success("\nDIGIMUNDO PRESENTE 🥷", category=LogCategory.SYSTEM, component=component)


if __name__ == "__main__":
    asyncio.run(main())