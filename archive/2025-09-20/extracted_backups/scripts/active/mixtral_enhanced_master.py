#!/usr/bin/env python3
"""
🚀 MIXTRAL ENHANCED MASTER SYSTEM
Sistema completo com todas as comparações e estratégias do 32B
Incluindo teoria, meus_filmes e roteiros mestres
"""

import asyncio
import time
import sys
import ollama
from pathlib import Path
from typing import List, Dict, Any, Optional
import json

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.core.screenplay_library import ScreenplayLibrary
from src.core.unified_memory_system import UnifiedMemorySystem


class MixtralEnhancedMaster:
    """Sistema Mixtral completo com todas funcionalidades do 32B"""

    def __init__(self):
        self.model = "mixtral-dedicated-q5"
        self.library = ScreenplayLibrary()
        self.memory = UnifiedMemorySystem()

        # Configuração máxima
        self.config = {
            'num_ctx': 131072,     # 128K tokens
            'num_thread': 24,      # 86% CPU
            'num_gpu': 60,         # 100% GPU
            'temperature': 0.2,
            'num_predict': 3000    # Análises completas
        }

        # Obras-primas para comparação (do sistema 32B)
        self.masterpieces = {
            "structure": ["The Godfather", "Pulp Fiction", "Casablanca", "Inception"],
            "character": ["The Shawshank Redemption", "Forrest Gump", "Gladiator"],
            "dialogue": ["Pulp Fiction", "The Social Network", "Casablanca"],
            "theme": ["The Matrix", "The Dark Knight", "Star Wars_ Episode IV  A New Hope"],
            "innovation": ["Inception", "Pulp Fiction", "The Matrix", "Memento"]
        }

        # Livros de teoria prioritários
        self.theory_books = [
            "Save The Cat.txt",
            "The Anatomy of Story_ 22 Steps to Becoming a Master  -  John Truby.txt",
            "S•T• O • R • Y.txt",
            "The Writers Journey_ Mythic Structure for Writers, 2nd .txt"
        ]

    async def analyze_with_masterpiece_comparison(
        self,
        title: str,
        content: str,
        compare_aspects: List[str] = None
    ) -> Dict[str, Any]:
        """
        Análise completa com comparações a obras-primas
        Igual ao sistema 32B mas usando Mixtral
        """

        print(f"\n📖 ANÁLISE APRIMORADA: {title}")
        print(f"🧠 Modelo: {self.model}")
        print(f"📊 Contexto: {self.config['num_ctx']:,} tokens")
        print("-" * 60)

        # Selecionar obras para comparação
        if not compare_aspects:
            compare_aspects = ["structure", "character", "theme"]

        comparison_films = set()
        for aspect in compare_aspects:
            if aspect in self.masterpieces:
                comparison_films.update(self.masterpieces[aspect][:2])

        print(f"🎬 Comparando com: {', '.join(comparison_films)}")

        # Carregar trechos das obras-primas para contexto
        masterpiece_examples = []
        for film in list(comparison_films)[:3]:  # Limitar a 3 para caber no contexto
            film_content = self.library.get_screenplay(film)
            if film_content:
                # Pegar cenas importantes
                excerpt = film_content[:5000]  # Primeira cena
                masterpiece_examples.append(f"\n### {film} (Excerpt)\n{excerpt}")

        # Prompt estruturado com comparações
        prompt = f"""You are a master screenplay analyst comparing new work with cinema masterpieces.

SCREENPLAY TO ANALYZE: {title}

{content[:50000]}  # 50K chars do roteiro principal

MASTERPIECE EXAMPLES FOR COMPARISON:
{"".join(masterpiece_examples[:15000])}  # 15K chars de exemplos

COMPREHENSIVE ANALYSIS REQUIRED:

## 1. SAVE THE CAT STRUCTURE (Compare with masterpieces)
- Opening Image (page/timing)
- Theme Stated (page/dialogue)
- Setup (pages 1-10)
- Catalyst (page 12)
- Debate (pages 12-25)
- Break into Two (page 25)
- B Story (page 30)
- Fun and Games (pages 30-55)
- Midpoint (page 55)
- Bad Guys Close In (pages 55-75)
- All Is Lost (page 75)
- Dark Night of the Soul (pages 75-85)
- Break into Three (page 85)
- Finale (pages 85-110)
- Final Image (page 110)

For each beat, compare with how {list(comparison_films)[0]} handles the same beat.

## 2. CHARACTER ANALYSIS (Compare with iconic characters)
- Protagonist's WANT vs NEED
- Character arc transformation
- Ghost/backstory wound
- Compare protagonist with:
  * Michael Corleone (The Godfather) - transformation arc
  * Andy Dufresne (Shawshank) - hope and persistence
  * Neo (The Matrix) - hero's journey

## 3. THEMATIC DEPTH (Compare themes)
- Central theme statement
- Visual metaphors and symbols
- Subtext layers
- Compare thematic handling with:
  * The Dark Knight - moral complexity
  * The Matrix - reality and choice
  * Inception - layers of meaning

## 4. DIALOGUE EXCELLENCE (Compare dialogue styles)
- Character voice distinctiveness
- Subtext vs text
- Memorable lines
- Compare with:
  * Pulp Fiction - distinctive voices
  * Casablanca - iconic lines
  * The Social Network - rapid-fire wit

## 5. INNOVATION & UNIQUENESS
- What makes this screenplay unique?
- Structural innovations (like Pulp Fiction's non-linear)
- Character innovations (like Memento's memory loss)
- Thematic innovations (like Inception's dream layers)

## 6. SPECIFIC IMPROVEMENTS (Page-level)
Based on masterpiece comparison, provide:
- 5 specific scenes to strengthen (with page numbers)
- 3 character moments to deepen
- 3 dialogue exchanges to sharpen
- 2 structural adjustments

## 7. MARKETABILITY ASSESSMENT
- Target audience (compare with similar successful films)
- Festival potential (Cannes, Sundance, Venice)
- Commercial viability (box office comparisons)
- Awards potential (Oscar categories)

## 8. OVERALL RATING
Rate each aspect 1-10 compared to masterpieces:
- Structure: ?/10 (vs Godfather's perfect structure)
- Character: ?/10 (vs Shawshank's character depth)
- Dialogue: ?/10 (vs Pulp Fiction's dialogue)
- Theme: ?/10 (vs The Dark Knight's thematic weight)
- Innovation: ?/10 (vs Inception's originality)
- Overall: ?/10

Provide specific, actionable insights with page numbers and examples."""

        try:
            start_time = time.time()

            # Análise com Mixtral
            response = ollama.generate(
                model=self.model,
                prompt=prompt,
                options=self.config
            )

            duration = time.time() - start_time
            analysis = response['response']

            print(f"✅ Análise completa em {duration:.1f}s")
            print(f"📊 Resposta: {len(analysis):,} caracteres")

            # Salvar análise aprimorada
            self.memory.store_knowledge(
                key=f"enhanced_analysis:{title}",
                content=analysis,
                metadata={
                    "screenplay": title,
                    "model": self.model,
                    "comparison_films": list(comparison_films),
                    "aspects": compare_aspects,
                    "duration": duration,
                    "timestamp": time.time()
                }
            )

            return {
                "success": True,
                "title": title,
                "analysis": analysis,
                "comparisons": list(comparison_films),
                "duration": duration
            }

        except Exception as e:
            print(f"❌ Erro: {e}")
            return {"success": False, "error": str(e)}

    async def analyze_theory_with_practice(
        self,
        theory_book: str,
        screenplay: str
    ) -> Dict[str, Any]:
        """
        Compara teoria com prática (como o sistema 32B)
        Analisa livro de teoria aplicado a roteiro específico
        """

        print(f"\n📚 TEORIA VS PRÁTICA")
        print(f"📖 Livro: {theory_book}")
        print(f"🎬 Roteiro: {screenplay}")
        print("-" * 60)

        # Carregar livro de teoria
        theory_path = Path("digilibrary/BIBLIOTECA_ROTEIROS/teoria") / theory_book
        if not theory_path.exists():
            print(f"❌ Livro não encontrado: {theory_book}")
            return {"success": False, "error": "Theory book not found"}

        theory_content = theory_path.read_text(encoding='utf-8', errors='ignore')

        # Carregar roteiro
        screenplay_content = self.library.get_screenplay(screenplay)
        if not screenplay_content:
            print(f"❌ Roteiro não encontrado: {screenplay}")
            return {"success": False, "error": "Screenplay not found"}

        # Ajustar tamanhos para caber no contexto
        theory_excerpt = theory_content[:60000]  # 60K chars de teoria
        screenplay_excerpt = screenplay_content[:40000]  # 40K chars de roteiro

        prompt = f"""You are analyzing how theoretical principles are applied in practice.

THEORY BOOK: {theory_book}
{theory_excerpt}

SCREENPLAY: {screenplay}
{screenplay_excerpt}

DEEP ANALYSIS:

1. KEY CONCEPTS FROM BOOK (10 most important)
   For each concept:
   - What the book teaches
   - Page/chapter reference
   - How it should work in theory

2. APPLICATION IN SCREENPLAY
   For each concept above:
   - Where it appears in the screenplay (page/scene)
   - How it's implemented
   - Does it follow or adapt the theory?
   - Specific dialogue or action that demonstrates it

3. THEORY VIOLATIONS THAT WORK
   - Where the screenplay breaks the rules successfully
   - Why it works despite breaking theory
   - What this teaches us

4. MISSING ELEMENTS
   - What the book recommends that's missing
   - Would adding it improve the screenplay?
   - Or does its absence serve a purpose?

5. PRACTICAL INSIGHTS
   - What works in theory vs practice
   - Adaptations needed for modern audiences
   - Genre-specific modifications

6. ACTIONABLE LESSONS
   - 5 specific techniques to apply
   - 3 theory adaptations for contemporary writing
   - 2 rules that can be broken effectively

Provide specific examples with page numbers and quotes."""

        try:
            start_time = time.time()

            response = ollama.generate(
                model=self.model,
                prompt=prompt,
                options=self.config
            )

            duration = time.time() - start_time
            analysis = response['response']

            print(f"✅ Teoria vs Prática analisada em {duration:.1f}s")

            # Salvar insights
            self.memory.store_knowledge(
                key=f"theory_practice:{theory_book}:{screenplay}",
                content=analysis,
                metadata={
                    "theory_book": theory_book,
                    "screenplay": screenplay,
                    "model": self.model,
                    "duration": duration
                }
            )

            return {
                "success": True,
                "theory": theory_book,
                "screenplay": screenplay,
                "analysis": analysis,
                "duration": duration
            }

        except Exception as e:
            print(f"❌ Erro: {e}")
            return {"success": False, "error": str(e)}

    async def run_complete_analysis(self, limit: int = 10):
        """
        Processamento completo: teoria + meus_filmes + roteiros_mestres
        Com todas as comparações e estratégias
        """

        print(f"🚀 MIXTRAL ENHANCED MASTER SYSTEM")
        print("=" * 60)
        print(f"Processando TUDO com comparações aprimoradas")
        print(f"Target: {limit} análises completas")
        print("=" * 60)

        # 1. Processar MEU FILME primeiro (prioridade máxima)
        print("\n📁 MEUS FILMES (Prioridade Máxima)")
        meus_filmes_path = Path("digilibrary/BIBLIOTECA_ROTEIROS/meus_filmes")
        if meus_filmes_path.exists():
            for f in meus_filmes_path.glob("*.txt"):
                content = f.read_text(encoding='utf-8', errors='ignore')
                result = await self.analyze_with_masterpiece_comparison(
                    f.stem,
                    content,
                    ["structure", "character", "dialogue", "theme", "innovation"]
                )

                if result['success']:
                    print(f"\n✅ MEU FILME ANALISADO COM SUCESSO!")
                    print(f"   Comparado com: {', '.join(result['comparisons'])}")

        # 2. Análise Teoria vs Prática
        print("\n📚 TEORIA VS PRÁTICA")
        theory_practice_pairs = [
            ("Save The Cat.txt", "Inception"),
            ("The Anatomy of Story_ 22 Steps to Becoming a Master  -  John Truby.txt", "The Godfather"),
            ("S•T• O • R • Y.txt", "Pulp Fiction")
        ]

        for theory, screenplay in theory_practice_pairs[:2]:  # 2 análises profundas
            await self.analyze_theory_with_practice(theory, screenplay)
            await asyncio.sleep(10)  # Pausa entre análises

        # 3. Processar roteiros mestres com comparações
        print("\n📁 ROTEIROS MESTRES COM COMPARAÇÕES")
        roteiros = self.library.list_screenplays()

        # Filtrar e processar
        processed = 0
        for title in roteiros[:limit]:
            if processed >= limit:
                break

            content = self.library.get_screenplay(title)
            if content and len(content) > 100:
                print(f"\n[{processed+1}/{limit}] Processando: {title}")

                # Análise com comparações
                result = await self.analyze_with_masterpiece_comparison(
                    title,
                    content,
                    ["structure", "character", "theme"]
                )

                if result['success']:
                    processed += 1
                    print(f"   ✅ Comparado com: {', '.join(result['comparisons'])}")

                # Pausa entre processamentos
                if processed < limit:
                    await asyncio.sleep(15)

        print(f"\n✅ PROCESSAMENTO COMPLETO!")
        print(f"📊 Total processado: {processed} análises")
        print(f"🧠 Sistema: Mixtral Enhanced Master")
        print(f"🎯 Incluído: teoria + meus_filmes + comparações")
        print("\nDIGIMUNDO PRESENTE 🥷")


async def main():
    """Função principal"""

    system = MixtralEnhancedMaster()

    print("\n🚀 MIXTRAL ENHANCED MASTER SYSTEM")
    print("================================")
    print("1. Análise completa com comparações")
    print("2. Teoria vs Prática")
    print("3. Processamento completo automatizado")
    print("4. Analisar MEU FILME com todas comparações")

    choice = input("\nEscolha (1-4): ").strip()

    if choice == "1":
        # Análise individual com comparações
        screenplays = system.library.list_screenplays()
        if screenplays:
            title = screenplays[0]
            content = system.library.get_screenplay(title)
            if content:
                await system.analyze_with_masterpiece_comparison(
                    title, content,
                    ["structure", "character", "dialogue", "theme", "innovation"]
                )

    elif choice == "2":
        # Teoria vs Prática
        await system.analyze_theory_with_practice(
            "Save The Cat.txt",
            "Inception"
        )

    elif choice == "3":
        # Processamento completo
        await system.run_complete_analysis(limit=10)

    elif choice == "4":
        # MEU FILME com análise máxima
        meu_filme = "SONHOS SEM LEMBRANÇAS T"  # Será procurado com .3 no nome
        content = system.library.get_screenplay(meu_filme)
        if content:
            await system.analyze_with_masterpiece_comparison(
                meu_filme, content,
                ["structure", "character", "dialogue", "theme", "innovation"]
            )
        else:
            print(f"❌ Não encontrado: {meu_filme}")

    else:
        print("Opção inválida. Executando análise demo...")
        screenplays = system.library.list_screenplays()
        if screenplays:
            title = screenplays[0]
            content = system.library.get_screenplay(title)
            if content:
                await system.analyze_with_masterpiece_comparison(
                    title, content[:10000],
                    ["structure", "character"]
                )


if __name__ == "__main__":
    asyncio.run(main())