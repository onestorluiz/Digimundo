#!/usr/bin/env python3
"""
🔄 MACHINE LEARNING CONTÍNUO ETERNO
Sistema que roda indefinidamente analisando e aprendendo com os roteiros
"""

import asyncio
import sys
from pathlib import Path
import time
import random
from datetime import datetime
import logging

# Adiciona o diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.screenplay_library import ScreenplayLibrary
from src.core.unified_memory_system import get_unified_memory, MemoryType
from src.core.mixtral_config import MixtralConfig, get_model_config
import ollama

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)

class EternalMLSystem:
    """Sistema de ML que roda eternamente"""

    def __init__(self, turbo_mode=False):
        logger.info("🚀 Iniciando Sistema ML Eterno")
        self.library = ScreenplayLibrary()
        self.memory = get_unified_memory()

        # ADICIONAR lógica turbo
        if turbo_mode:
            logger.info("⚡ TURBO MODE ATIVADO!")
            self.model, self.options = get_model_config("turbo")
        else:
            self.model, self.options = get_model_config("dedicated")

        self.processed_count = 0
        self.start_time = time.time()
        self.insights_generated = 0
        self.turbo_mode = turbo_mode

    async def analyze_screenplay(self, title: str, content: str) -> dict:
        """Analisa um roteiro com ML profundo"""
        try:
            logger.info(f"🎬 Analisando: {title}")

            # Análise Save the Cat
            save_cat_prompt = f"""
            Analyze this screenplay using Save the Cat methodology.
            Identify the 15 story beats and their timing.

            Title: {title}
            Content (sample): {content[:20000]}

            Provide detailed analysis of:
            1. Opening Image
            2. Theme Stated
            3. Setup
            4. Catalyst
            5. Debate
            6. Break into Two
            7. B Story
            8. Fun and Games
            9. Midpoint
            10. Bad Guys Close In
            11. All Is Lost
            12. Dark Night of the Soul
            13. Break into Three
            14. Finale
            15. Final Image
            """

            # Análise de personagens
            character_prompt = f"""
            Analyze the character arcs in this screenplay.
            Focus on the protagonist's journey.

            Title: {title}
            Content (sample): {content[:20000]}

            Identify:
            1. WANT - What the character thinks they want
            2. NEED - What they actually need
            3. LIE - The lie they believe
            4. TRUTH - The truth they must learn
            5. GHOST - Their backstory/wound
            6. ARC - Their transformation journey
            """

            # Análise de temas
            theme_prompt = f"""
            Identify the deep themes and symbolic elements.

            Title: {title}
            Content (sample): {content[:20000]}

            Extract:
            1. Central theme
            2. Supporting themes
            3. Symbolic elements
            4. Metaphors used
            5. Universal truths explored
            """

            results = {}

            # Executa análises em paralelo
            tasks = [
                self._analyze_with_ollama(save_cat_prompt, "save_cat"),
                self._analyze_with_ollama(character_prompt, "character"),
                self._analyze_with_ollama(theme_prompt, "theme")
            ]

            analyses = await asyncio.gather(*tasks, return_exceptions=True)

            for i, analysis in enumerate(analyses):
                if not isinstance(analysis, Exception):
                    key = ["save_cat", "character", "theme"][i]
                    results[key] = analysis
                    logger.info(f"  ✅ {key} completo")
                    self.insights_generated += 1

            # Salva na memória
            if results:
                self.memory.store(
                    memory_type=MemoryType.ANALYSIS,
                    key=f"ml:eternal:{title}:{int(time.time())}",
                    value=results,
                    metadata={
                        'title': title,
                        'timestamp': datetime.now().isoformat(),
                        'model': self.model,
                        'system': 'eternal_ml'
                    }
                )
                logger.info(f"  💾 Análise salva na memória")

            self.processed_count += 1
            return results

        except Exception as e:
            logger.error(f"  ❌ Erro ao analisar {title}: {e}")
            return {}

    async def _analyze_with_ollama(self, prompt: str, analysis_type: str) -> str:
        """Executa análise com Ollama"""
        try:
            response = await asyncio.to_thread(
                ollama.generate,
                model=self.model,
                prompt=prompt,
                options=self.options
            )
            return response.get('response', '')
        except Exception as e:
            logger.error(f"Erro Ollama ({analysis_type}): {e}")
            return ""

    async def continuous_learning(self):
        """Aprendizado contínuo eterno"""
        screenplays = self.library.list_screenplays()

        if not screenplays:
            logger.error("Nenhum roteiro disponível")
            return

        logger.info(f"📚 {len(screenplays)} roteiros disponíveis")
        logger.info("🔄 Iniciando aprendizado contínuo eterno...")
        logger.info("=" * 60)

        while True:  # Loop eterno
            try:
                # Embaralha para variedade
                random.shuffle(screenplays)

                for title in screenplays:
                    content = self.library.get_screenplay(title)

                    if not content or content == '.' or len(content) < 1000:
                        logger.warning(f"⚠️ Conteúdo inválido para {title}")
                        continue

                    # Análise
                    await self.analyze_screenplay(title, content)

                    # Estatísticas
                    elapsed = time.time() - self.start_time
                    rate = self.processed_count / (elapsed / 3600) if elapsed > 0 else 0

                    logger.info(f"""
                    📊 ESTATÍSTICAS ETERNAS
                    ├── Roteiros processados: {self.processed_count}
                    ├── Insights gerados: {self.insights_generated}
                    ├── Tempo decorrido: {elapsed/3600:.1f} horas
                    ├── Taxa: {rate:.1f} roteiros/hora
                    └── Memórias no sistema: {len(self.memory.search('', limit=1000))}
                    """)

                    # Pausa entre análises para não sobrecarregar
                    await asyncio.sleep(30)

                logger.info("🔄 Reiniciando ciclo de aprendizado...")
                await asyncio.sleep(60)  # Pausa entre ciclos completos

            except KeyboardInterrupt:
                logger.info("⏹️ Interrompido pelo usuário")
                break
            except Exception as e:
                logger.error(f"Erro no loop: {e}")
                await asyncio.sleep(60)  # Pausa em caso de erro


if __name__ == "__main__":
    import sys
    turbo = "--turbo" in sys.argv  # ADICIONAR

    async def main():
        """Função principal"""
        print("""
        ╔══════════════════════════════════════════════════════════╗
        ║       🔄 MACHINE LEARNING CONTÍNUO ETERNO                ║
        ║                                                          ║
        ║   Sistema que aprende indefinidamente com os roteiros    ║
        ║         Pressione Ctrl+C para interromper               ║
        ╚══════════════════════════════════════════════════════════╝
        """)

        if turbo:  # ADICIONAR
            print("║       🚀 TURBO MODE ATIVADO                              ║")
            print("║       Batch: 8192 | Experts: 3 | FP16 Cache              ║")
            print("╚══════════════════════════════════════════════════════════╝\n")

        system = EternalMLSystem(turbo_mode=turbo)  # MODIFICAR
        await system.continuous_learning()

        print("\n🏁 Sistema ML Eterno finalizado")
        print(f"📊 Total processado: {system.processed_count} roteiros")
        print(f"💡 Insights gerados: {system.insights_generated}")
        print("DIGIMUNDO PRESENTE 🥷")

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n⏹️ Sistema interrompido")