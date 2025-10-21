#!/usr/bin/env python3
"""
🧠 DEEP SCREENPLAY LEARNING - Machine Learning Profundo com mixtral-r1:32b
Processa livros inteiros + roteiros com 128K tokens para extrair conhecimento acionável
"""

import sys
import json
import time
import hashlib
import asyncio
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import subprocess

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.unified_memory_system import get_unified_memory, MemoryType
from src.core.screenplay_library import get_screenplay_library

class DeepScreenplayLearning:
    """
    Machine Learning profundo com mixtral-r1:32b
    128K tokens = livro completo + roteiro para comparação
    """

    def __init__(self):
        self.memory = get_unified_memory()
        self.library = get_screenplay_library()
        self.model = "mixtral-dedicated-q5"  # Modelo híbrido CPU+GPU otimizado!

        # Configuração otimizada para 128K tokens
        self.config = {
            'num_ctx': 131072,     # 128K tokens
            'num_thread': 14,      # 14 cores
            'num_gpu': 999,        # Todas camadas GPU
            'num_batch': 2048,     # Batch grande
            'temperature': 0.3,    # Baixa para análise precisa
            'top_p': 0.9,
            'top_k': 40
        }

        self.stats = {
            'books_processed': 0,
            'comparisons_made': 0,
            'insights_extracted': 0,
            'processing_time': 0
        }

    def check_model(self) -> bool:
        """Verifica se o modelo está disponível"""
        try:
            result = subprocess.run(
                ['ollama', 'list'],
                capture_output=True,
                text=True,
                timeout=5
            )
            return self.model in result.stdout
        except:
            return False

    async def analyze_book_with_examples(self, book_path: Path, example_screenplays: List[str]) -> Dict:
        """
        Analisa livro teórico completo com exemplos práticos de roteiros

        Args:
            book_path: Caminho do livro de teoria
            example_screenplays: Lista de roteiros para exemplificar

        Returns:
            Conhecimento estruturado e mapeado
        """

        print(f"\n📚 Processando: {book_path.name}")
        print(f"   Com exemplos: {', '.join(example_screenplays)}")

        # Ler livro completo
        book_content = book_path.read_text(encoding='utf-8', errors='ignore')
        book_tokens = len(book_content) // 4  # Estimativa de tokens

        print(f"   📖 Livro: {book_tokens} tokens estimados")

        # Ajustar conteúdo se necessário
        if book_tokens > 80000:  # Deixar espaço para roteiro
            book_content = book_content[:320000]  # ~80K tokens
            print(f"   ⚠️ Truncado para 80K tokens")

        # Pegar exemplo de roteiro
        screenplay_content = ""
        screenplay_title = ""

        for title in example_screenplays:
            content = self.library.get_screenplay(title)
            if content:
                screenplay_title = title
                screenplay_content = content[:120000]  # ~30K tokens
                break

        if not screenplay_content:
            print("   ❌ Nenhum roteiro exemplo encontrado")
            return {}

        print(f"   🎬 Roteiro: {screenplay_title} ({len(screenplay_content)//4} tokens)")

        # Criar prompt mega-complexo para mixtral-r1:32b
        analysis_prompt = f"""You are a master screenplay analyst with access to both theoretical knowledge and practical examples.

THEORETICAL BOOK (First 80K tokens):
{book_content}

EXAMPLE SCREENPLAY ({screenplay_title}):
{screenplay_content}

DEEP ANALYSIS TASK:
1. Extract the 10 most important concepts from the book
2. For EACH concept, find a SPECIFIC example in the screenplay
3. Include page numbers, dialogue quotes, or scene descriptions
4. Identify where the screenplay follows or breaks the book's rules
5. Generate actionable insights for writers

Output as structured JSON:
{{
    "book": "book name",
    "screenplay": "screenplay name",
    "concepts": [
        {{
            "concept_name": "...",
            "book_explanation": "what the book says",
            "book_page": "page reference if found",
            "screenplay_example": "specific example from screenplay",
            "screenplay_timing": "minute/page where it happens",
            "alignment": "follows|breaks|adapts the rule",
            "actionable_insight": "what writers should learn from this"
        }}
    ],
    "patterns": ["list of patterns found"],
    "contradictions": ["where screenplay succeeds by breaking rules"],
    "synthesis": "overall insight combining theory and practice"
}}

Take your time for deep analysis. Quality over speed."""

        # Chamar mixtral-r1:32b com configuração completa
        start_time = time.time()

        try:
            print(f"\n   🧠 Iniciando análise profunda com {self.model}...")
            print(f"   ⏱️ Estimado: 2-5 minutos...")

            # Preparar payload
            payload = {
                'model': self.model,
                'prompt': analysis_prompt,
                'options': self.config,
                'stream': False
            }

            # Chamar via curl (mais confiável para processos longos)
            cmd = [
                'curl', '-s', '--max-time', '600',  # 10 minutos timeout
                'http://localhost:11434/api/generate',
                '-d', json.dumps(payload)
            ]

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=600
            )

            if result.returncode == 0 and result.stdout:
                response_data = json.loads(result.stdout)
                analysis_text = response_data.get('response', '')

                # Processar resposta
                analysis = self.parse_analysis(analysis_text)

                processing_time = time.time() - start_time
                self.stats['processing_time'] += processing_time

                print(f"   ✅ Análise completa em {processing_time:.1f} segundos")

                # Salvar insights na memória
                if analysis:
                    await self.save_deep_insights(analysis, book_path.name)
                    self.stats['insights_extracted'] += len(analysis.get('concepts', []))

                return analysis

            else:
                print(f"   ❌ Erro na análise: {result.stderr}")
                return {}

        except subprocess.TimeoutExpired:
            print(f"   ⏱️ Timeout após 10 minutos")
            return {}
        except Exception as e:
            print(f"   ❌ Erro: {e}")
            return {}

    def parse_analysis(self, response_text: str) -> Dict:
        """Extrai JSON da resposta"""
        try:
            # Tentar encontrar JSON na resposta
            import re
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except:
            pass

        # Fallback: criar estrutura básica
        return {
            'raw_analysis': response_text,
            'concepts': [],
            'patterns': [],
            'synthesis': response_text[:500] if response_text else ''
        }

    async def save_deep_insights(self, analysis: Dict, book_name: str):
        """Salva insights profundos na memória unificada"""

        # Salvar cada conceito com contexto rico
        for concept in analysis.get('concepts', []):
            concept_key = f"deep_learning:{book_name}:{concept.get('concept_name', 'unknown')}"

            self.memory.store(
                memory_type=MemoryType.KNOWLEDGE,
                key=concept_key[:100],  # Limitar tamanho da chave
                value={
                    'concept': concept.get('concept_name'),
                    'theory': concept.get('book_explanation'),
                    'example': concept.get('screenplay_example'),
                    'timing': concept.get('screenplay_timing'),
                    'alignment': concept.get('alignment'),
                    'insight': concept.get('actionable_insight'),
                    'book': book_name,
                    'screenplay': analysis.get('screenplay', 'unknown')
                },
                metadata={
                    'source': 'deep_learning',
                    'model': self.model,
                    'tokens_used': self.config['num_ctx'],
                    'extraction_date': datetime.now().isoformat()
                },
                confidence=0.95,  # Alta confiança do mixtral-r1:32b
                source='deep_ml_extraction'
            )

        # Salvar síntese geral
        if analysis.get('synthesis'):
            self.memory.store(
                memory_type=MemoryType.KNOWLEDGE,
                key=f"synthesis:{book_name}",
                value={
                    'synthesis': analysis['synthesis'],
                    'patterns': analysis.get('patterns', []),
                    'contradictions': analysis.get('contradictions', [])
                },
                confidence=0.9,
                source='deep_ml_synthesis'
            )

        print(f"   💾 {len(analysis.get('concepts', []))} conceitos salvos na memória")

    async def compare_theory_with_practice(self):
        """
        Processa teoria e compara com prática
        Foco nos livros mais importantes
        """

        print("🧠 DEEP LEARNING COM mixtral-R1:32B")
        print("=" * 60)

        # Verificar modelo
        if not self.check_model():
            print(f"❌ Modelo {self.model} não encontrado!")
            print("Execute: ollama pull mixtral-r1:32b")
            return

        # Livros prioritários para processar
        priority_books = [
            ("Save The Cat.txt", ["Inception", "The Dark Knight", "The Matrix"]),
            ("The Anatomy of Story_ 22 Steps to Becoming a Master  -  John Truby.txt",
             ["Pulp Fiction", "The Godfather", "Casablanca"]),
            ("S•T• O • R • Y.txt", ["Gladiator", "The Shawshank Redemption", "Forrest Gump"]),
            ("The Writers Journey_ Mythic Structure for Writers, 2nd .txt",
             ["Star Wars_ Episode IV  A New Hope", "The Matrix", "The Dark Knight"])
        ]

        teoria_path = Path("digilibrary/BIBLIOTECA_ROTEIROS/teoria")

        for book_name, example_screenplays in priority_books:
            book_path = teoria_path / book_name

            if not book_path.exists():
                print(f"\n⚠️ Livro não encontrado: {book_name}")
                continue

            # Processar livro com exemplos
            analysis = await self.analyze_book_with_examples(book_path, example_screenplays)

            if analysis:
                self.stats['books_processed'] += 1
                self.stats['comparisons_made'] += len(example_screenplays)

            # Pausar entre processamentos pesados
            await asyncio.sleep(5)

        # Relatório final
        print("\n" + "=" * 60)
        print("📊 RESULTADO DO DEEP LEARNING:")
        print(f"  📚 Livros processados: {self.stats['books_processed']}")
        print(f"  🎬 Comparações realizadas: {self.stats['comparisons_made']}")
        print(f"  💡 Insights extraídos: {self.stats['insights_extracted']}")
        print(f"  ⏱️ Tempo total: {self.stats['processing_time']:.1f} segundos")

        # Verificar memória
        mem_stats = self.memory.get_stats()
        print(f"\n💾 MEMÓRIA ENRIQUECIDA:")
        print(f"  Total entradas: {mem_stats['total_entries']}")
        print(f"  Conhecimento: {mem_stats['by_type'].get('knowledge', 0)} conceitos")
        print(f"  Tamanho: {mem_stats['db_size_kb']:.1f} KB")

        return self.stats

    async def quick_concept_extraction(self, concept: str, examples_count: int = 3):
        """
        Extração rápida de um conceito específico
        Para consultas dos Ollamas
        """

        # Buscar na memória
        entries = self.memory.search(
            query=concept,
            memory_types=[MemoryType.KNOWLEDGE],
            limit=examples_count
        )

        insights = []
        for entry in entries:
            if isinstance(entry.value, dict):
                insight = entry.value.get('insight', '')
                example = entry.value.get('example', '')
                if insight or example:
                    insights.append({
                        'concept': entry.value.get('concept', concept),
                        'insight': insight,
                        'example': example,
                        'screenplay': entry.value.get('screenplay', 'unknown')
                    })

        return insights

async def main():
    """Executa deep learning completo"""

    learner = DeepScreenplayLearning()

    print("🎯 OPÇÕES DE DEEP LEARNING:")
    print("1. Análise completa (todos os livros prioritários)")
    print("2. Análise de um livro específico")
    print("3. Buscar conceito na memória")

    choice = input("\nEscolha (1-3): ").strip()

    if choice == '1':
        await learner.compare_theory_with_practice()

    elif choice == '2':
        teoria_path = Path("digilibrary/BIBLIOTECA_ROTEIROS/teoria")
        books = list(teoria_path.glob("*.txt"))

        print("\n📚 Livros disponíveis:")
        for i, book in enumerate(books, 1):
            print(f"{i}. {book.name}")

        book_idx = int(input("\nEscolha o número: ")) - 1
        if 0 <= book_idx < len(books):
            # Sugerir roteiros
            screenplays = ["Inception", "The Matrix", "Pulp Fiction"]
            analysis = await learner.analyze_book_with_examples(books[book_idx], screenplays)
            print(f"\n✅ Análise salva na memória")

    elif choice == '3':
        concept = input("\nConceito para buscar: ")
        insights = await learner.quick_concept_extraction(concept)

        print(f"\n💡 INSIGHTS SOBRE '{concept}':")
        for i, insight in enumerate(insights, 1):
            print(f"\n{i}. {insight['concept']}")
            print(f"   📖 {insight['insight']}")
            print(f"   🎬 {insight['screenplay']}: {insight['example'][:100]}...")

    print("\n✅ Deep Learning completo!")
    print("\n🎬 CONHECIMENTO DISPONÍVEL PARA OLLAMAS:")
    print("  • Conceitos teóricos mapeados em exemplos práticos")
    print("  • Comparações livro ↔ roteiro")
    print("  • Insights acionáveis para escritores")

if __name__ == "__main__":
    asyncio.run(main())