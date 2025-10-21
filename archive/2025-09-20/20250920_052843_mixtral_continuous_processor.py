#!/usr/bin/env python3
"""
🚀 PROCESSADOR CONTÍNUO MIXTRAL Q5
Sistema automatizado para análise de roteiros e livros
"""

import asyncio
import time
import sys
from pathlib import Path
from typing import List, Dict, Any
import ollama

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.core.screenplay_library import ScreenplayLibrary
from src.core.unified_memory_system import UnifiedMemorySystem


class MixtralContinuousProcessor:
    """Processador contínuo automatizado com Mixtral Q5"""

    def __init__(self):
        self.model = "mixtral-dedicated-q5"
        self.library = ScreenplayLibrary()
        self.memory = UnifiedMemorySystem()
        self.processed_count = 0

        # Frameworks de análise
        self.frameworks = [
            "save_the_cat",
            "heros_journey",
            "three_act_structure",
            "character_arc",
            "thematic_analysis"
        ]

    async def analyze_screenplay(self, title: str, content: str) -> Dict[str, Any]:
        """Análise completa de roteiro com Mixtral"""

        print(f"\n📖 ANALISANDO: {title}")
        print("-" * 60)

        # Prompt estruturado para análise completa
        prompt = f"""Analyze this complete screenplay using professional frameworks:

SCREENPLAY: {title}

{content[:50000]}  # Primeiros 50K chars

Provide comprehensive analysis covering:

1. SAVE THE CAT BEATS (with page numbers):
   - Opening Image
   - Theme Stated
   - Set-up
   - Catalyst
   - Debate
   - Break into Two
   - B Story
   - Fun and Games
   - Midpoint
   - Bad Guys Close In
   - All Is Lost
   - Dark Night of the Soul
   - Break into Three
   - Finale
   - Final Image

2. THREE-ACT STRUCTURE:
   - Act I (pages 1-25): Setup, inciting incident
   - Act II-A (pages 25-60): Rising action, obstacles
   - Act II-B (pages 60-90): Complications, crisis
   - Act III (pages 90-120): Climax, resolution

3. CHARACTER ANALYSIS:
   - Protagonist's want vs need
   - Character arc transformation
   - Supporting character functions
   - Relationships and dynamics

4. THEMATIC ELEMENTS:
   - Central theme identification
   - Symbolic meanings
   - Visual metaphors
   - Subtext analysis

5. COMMERCIAL VIABILITY:
   - Genre conventions
   - Market appeal
   - Audience targeting
   - Comparable films

Provide specific page numbers and quotes where possible."""

        try:
            start_time = time.time()

            # Gerar análise com Mixtral
            response = ollama.generate(
                model=self.model,
                prompt=prompt,
                options={
                    'num_ctx': 131072,  # 128K context
                    'num_thread': 24,
                    'num_gpu': 60,
                    'temperature': 0.2,
                    'num_predict': 2000
                }
            )

            end_time = time.time()
            duration = end_time - start_time

            analysis = response['response']

            print(f"✅ Análise completa em {duration:.1f}s")
            print(f"📊 Tamanho: {len(analysis)} caracteres")

            # Salvar na memória
            self.memory.store_knowledge(
                key=f"mixtral_analysis:{title}",
                content=analysis,
                metadata={
                    "screenplay": title,
                    "framework": "comprehensive",
                    "model": self.model,
                    "duration": duration,
                    "timestamp": time.time()
                }
            )

            return {
                "success": True,
                "title": title,
                "analysis": analysis,
                "duration": duration,
                "model": self.model
            }

        except Exception as e:
            print(f"❌ Erro: {e}")
            return {
                "success": False,
                "title": title,
                "error": str(e)
            }

    async def compare_with_masters(self, screenplay_title: str, analysis: str) -> str:
        """Compara roteiro com obras-primas"""

        print(f"\n🔍 COMPARANDO {screenplay_title} COM OBRAS-PRIMAS...")

        # Buscar roteiros mestres para comparação
        masters = [
            "Casablanca", "The Godfather", "Pulp Fiction",
            "Inception", "The Dark Knight", "Parasite"
        ]

        comparison_prompt = f"""Compare this screenplay analysis with masterpiece films:

SCREENPLAY ANALYSIS:
{analysis[:20000]}

Compare with these masterpieces and identify:

1. STRUCTURAL SIMILARITIES:
   - Which masters use similar beats?
   - Comparable pacing patterns
   - Similar turning points

2. CHARACTER PATTERNS:
   - Archetypal similarities
   - Character arc comparisons
   - Relationship dynamics

3. THEMATIC CONNECTIONS:
   - Shared themes with masters
   - Similar symbolic elements
   - Comparable messages

4. INNOVATION OPPORTUNITIES:
   - What this screenplay does differently
   - Unique elements vs masters
   - Fresh approaches identified

5. IMPROVEMENT SUGGESTIONS:
   - What masters do better
   - Specific techniques to adopt
   - Page-specific recommendations

Provide actionable insights with specific examples."""

        try:
            response = ollama.generate(
                model=self.model,
                prompt=comparison_prompt,
                options={
                    'num_ctx': 131072,
                    'temperature': 0.25,
                    'num_predict': 1500
                }
            )

            comparison = response['response']

            # Salvar comparação
            self.memory.store_knowledge(
                key=f"master_comparison:{screenplay_title}",
                content=comparison,
                metadata={
                    "type": "comparison",
                    "screenplay": screenplay_title,
                    "compared_with": "masterpieces"
                }
            )

            return comparison

        except Exception as e:
            return f"Erro na comparação: {e}"

    async def run_continuous_analysis(self):
        """Loop principal de análise contínua"""

        print("🚀 INICIANDO PROCESSAMENTO CONTÍNUO MIXTRAL Q5")
        print("=" * 60)
        print(f"Modelo: {self.model}")
        print("Context: 128K tokens")
        print("Análise: Save the Cat + Comparações com Mestres")
        print("=" * 60)

        # Obter lista de roteiros
        screenplays = self.library.list_screenplays()
        print(f"\n📚 {len(screenplays)} roteiros encontrados")

        # Processar cada roteiro
        for i, title in enumerate(screenplays[:10], 1):  # Limitar a 10 para teste
            print(f"\n{'='*60}")
            print(f"[{i}/10] PROCESSAMENTO {i}")
            print(f"{'='*60}")

            # Obter conteúdo do roteiro
            content = self.library.get_screenplay(title)
            if not content:
                print(f"⚠️ Não foi possível carregar: {title}")
                continue

            # Análise principal
            result = await self.analyze_screenplay(title, content)

            if result['success']:
                # Comparação com mestres
                comparison = await self.compare_with_masters(
                    title, result['analysis']
                )

                print(f"\n📋 RESUMO {title}:")
                print(f"   • Análise: {len(result['analysis'])} chars")
                print(f"   • Comparação: {len(comparison)} chars")
                print(f"   • Tempo: {result['duration']:.1f}s")

                self.processed_count += 1

            # Pausa entre processamentos
            print(f"\n⏳ Pausa de 30 segundos...")
            await asyncio.sleep(30)

        print(f"\n✅ PROCESSAMENTO CONCLUÍDO!")
        print(f"📊 Total processado: {self.processed_count} roteiros")
        print(f"🧠 Modelo: {self.model} (Mixtral Q5)")
        print("\nDIGIMUNDO PRESENTE 🥷")

    async def quick_demo(self):
        """Demo rápido com 1 roteiro"""

        print("🧪 DEMO RÁPIDO MIXTRAL Q5")
        print("=" * 40)

        screenplays = self.library.list_screenplays()
        if not screenplays:
            print("❌ Nenhum roteiro encontrado")
            return

        # Pegar primeiro roteiro
        title = screenplays[0]
        content = self.library.get_screenplay(title)

        if content:
            result = await self.analyze_screenplay(title, content)
            if result['success']:
                print(f"\n📋 PREVIEW DA ANÁLISE:")
                print("=" * 40)
                preview = result['analysis'][:500]
                print(f"{preview}...")
                print(f"\n✅ Análise completa salva na memória")

        print("\nDIGIMUNDO PRESENTE 🥷")


async def main():
    """Função principal"""

    processor = MixtralContinuousProcessor()

    print("\nEscolha o modo:")
    print("1. Demo rápido (1 roteiro)")
    print("2. Processamento contínuo (10 roteiros)")

    choice = input("\nOpção (1 ou 2): ").strip()

    if choice == "1":
        await processor.quick_demo()
    else:
        await processor.run_continuous_analysis()


if __name__ == "__main__":
    asyncio.run(main())