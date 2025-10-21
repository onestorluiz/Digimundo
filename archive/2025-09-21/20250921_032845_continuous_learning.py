#!/usr/bin/env python3
"""
CONTINUOUS LEARNING - Análise em Loop com Aprendizado Profundo
Analisa roteiros e teoria continuamente, evoluindo o conhecimento
"""

import sys
import time
import json
from pathlib import Path
from datetime import datetime
import subprocess

sys.path.insert(0, 'src')

from scripturemon_champion.analysis.script_doctor import ScriptDoctor
from scripturemon_champion.analysis.theory import TheoryComparator
from scripturemon_champion.learning.learning_lite import LearningLite
from scripturemon_champion.core.memory import UnifiedMemory, MemoryRecord

print("=" * 70)
print("🧠 CONTINUOUS LEARNING SYSTEM - SCRIPTUREMON ULTIMATE")
print("=" * 70)
print()

class ContinuousLearner:
    def __init__(self):
        self.doctor = ScriptDoctor(use_learning=True)
        self.learning = LearningLite()
        self.theory = TheoryComparator(Path("theory"))
        self.memory = UnifiedMemory(Path("data/unified_memory.db"))

        # Carregar teoria
        self.n_theory = self.theory.build()
        print(f"✅ {self.n_theory} livros de teoria carregados")

        # Contadores
        self.total_analyzed = 0
        self.total_concepts = 0
        self.start_time = time.time()

        # Verificar modelos disponíveis
        self.check_models()

    def check_models(self):
        """Verifica quais modelos estão disponíveis"""
        try:
            result = subprocess.run(['ollama', 'list'], capture_output=True, text=True)
            models = result.stdout

            self.available_models = {
                'deeplearning': 'deeplearning-main' in models or 'deeplearning-hybrid' in models,
                'mixtral': 'mixtral' in models,
                'deepseek': 'deepseek' in models,
            }

            print(f"\n📡 Modelos disponíveis:")
            for model, available in self.available_models.items():
                status = "✅" if available else "❌"
                print(f"  {status} {model}")
        except:
            self.available_models = {}
            print("⚠️ Ollama não disponível - usando análise local apenas")

    def analyze_screenplay(self, filepath: Path) -> dict:
        """Analisa um roteiro completo"""
        print(f"\n📖 Analisando: {filepath.name}")

        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            text = f.read()

        # Análise básica
        start = time.time()
        analysis = self.doctor.analyze_script(text, filepath.stem)
        stc = self.doctor.analyze_save_the_cat(text)
        elapsed = time.time() - start

        print(f"  ✅ Análise completa em {elapsed:.1f}s")
        print(f"  • Cenas: {analysis.scenes}")
        print(f"  • Beats: {len(stc.beats)}")
        print(f"  • Diálogo: {analysis.dialogue_ratio:.1%}")

        # Aprender
        concepts = self.learning.learn_from_analysis(
            analysis,
            filepath.stem,
            genre=self.detect_genre(text)
        )

        self.total_concepts += len(concepts)
        print(f"  • Conceitos aprendidos: {len(concepts)}")

        # Comparar com teoria
        if self.n_theory > 0:
            query = f"{' '.join(analysis.top_characters[:3])} {filepath.stem}"
            theory_hits = self.theory.compare(query, k=2)
            if theory_hits:
                print(f"  • Match teórico: {theory_hits[0].doc_id[:30]}...")

        # Análise profunda com LLM (se disponível)
        insights = []
        if self.available_models.get('deeplearning') or self.available_models.get('mixtral'):
            insights = self.deep_analysis_llm(text[:5000], filepath.stem)

        return {
            'file': filepath.name,
            'scenes': analysis.scenes,
            'beats': len(stc.beats),
            'dialogue_ratio': analysis.dialogue_ratio,
            'concepts': len(concepts),
            'insights': insights
        }

    def deep_analysis_llm(self, text: str, title: str) -> list:
        """Análise profunda usando LLM"""
        model = 'deeplearning-main' if self.available_models.get('deeplearning') else 'mixtral'

        prompt = f"""Analyze this screenplay excerpt from '{title}':

{text[:2000]}

Extract:
1. Core dramatic pattern
2. Character arc insight
3. Structural strength
4. Unique element

Be extremely concise. Format: JSON list of 4 strings."""

        try:
            result = subprocess.run(
                ['ollama', 'run', model, prompt],
                capture_output=True,
                text=True,
                timeout=30
            )

            # Parse response
            response = result.stdout.strip()
            if response.startswith('['):
                return json.loads(response)
            return []
        except:
            return []

    def detect_genre(self, text: str) -> str:
        """Detecta gênero do roteiro"""
        text_lower = text.lower()

        if 'spaceship' in text_lower or 'robot' in text_lower or 'ai' in text_lower:
            return 'scifi'
        elif 'murder' in text_lower or 'detective' in text_lower:
            return 'thriller'
        elif 'love' in text_lower or 'kiss' in text_lower:
            return 'romance'
        elif 'laugh' in text_lower or 'funny' in text_lower:
            return 'comedy'
        else:
            return 'drama'

    def run_learning_loop(self, max_files: int = None):
        """Executa loop de aprendizado contínuo"""

        # Coletar arquivos
        screenplays = list(Path("screenplays").rglob("*.txt"))
        theory_files = list(Path("theory").rglob("*.txt"))
        my_scripts = list(Path("my_screenplays").rglob("*.txt"))

        all_files = screenplays + my_scripts  # Não analisar theory como roteiro

        if max_files:
            all_files = all_files[:max_files]

        print(f"\n🎬 Iniciando análise de {len(all_files)} arquivos")
        print("-" * 70)

        results = []

        for i, filepath in enumerate(all_files, 1):
            print(f"\n[{i}/{len(all_files)}]", end="")

            try:
                result = self.analyze_screenplay(filepath)
                results.append(result)
                self.total_analyzed += 1

                # Salvar progresso periodicamente
                if i % 5 == 0:
                    self.save_progress(results)

            except Exception as e:
                print(f"  ❌ Erro: {e}")
                continue

            # Estatísticas parciais
            if i % 10 == 0:
                self.print_statistics()

        # Salvar resultados finais
        self.save_final_results(results)
        self.print_final_report()

    def save_progress(self, results: list):
        """Salva progresso na memória"""
        record = MemoryRecord(
            type="continuous_learning_progress",
            key=f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            value={
                'analyzed': self.total_analyzed,
                'concepts': self.total_concepts,
                'results': results[-5:]  # Últimos 5
            },
            metadata={'system': 'continuous_learner'}
        )
        self.memory.store(record)
        print(f"\n💾 Progresso salvo: {self.total_analyzed} arquivos, {self.total_concepts} conceitos")

    def save_final_results(self, results: list):
        """Salva resultados finais"""
        # Exportar conhecimento aprendido
        export_path = Path(f"data/learning/continuous_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        self.learning.export_json(export_path)
        print(f"\n📚 Conhecimento exportado: {export_path}")

        # Salvar análise completa
        analysis_path = Path(f"data/learning/analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        with open(analysis_path, 'w') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'total_files': self.total_analyzed,
                'total_concepts': self.total_concepts,
                'duration': time.time() - self.start_time,
                'results': results
            }, f, indent=2)
        print(f"📊 Análise salva: {analysis_path}")

    def print_statistics(self):
        """Imprime estatísticas parciais"""
        elapsed = time.time() - self.start_time
        rate = self.total_analyzed / (elapsed / 60) if elapsed > 0 else 0

        stats = self.learning.get_statistics()

        print(f"\n📈 ESTATÍSTICAS PARCIAIS:")
        print(f"  • Arquivos analisados: {self.total_analyzed}")
        print(f"  • Conceitos totais: {self.total_concepts}")
        print(f"  • Taxa: {rate:.1f} arquivos/min")
        print(f"  • Beats catalogados: {stats.get('total_beats', 0)}")
        print(f"  • Padrões únicos: {stats.get('unique_patterns', 0)}")

    def print_final_report(self):
        """Relatório final detalhado"""
        elapsed = time.time() - self.start_time

        stats = self.learning.get_statistics()

        print("\n" + "=" * 70)
        print("📊 RELATÓRIO FINAL - CONTINUOUS LEARNING")
        print("=" * 70)

        print(f"\n⏱️ PERFORMANCE:")
        print(f"  • Duração total: {elapsed/60:.1f} minutos")
        print(f"  • Arquivos processados: {self.total_analyzed}")
        print(f"  • Taxa média: {self.total_analyzed/(elapsed/60):.1f} arquivos/min")

        print(f"\n🧠 CONHECIMENTO ADQUIRIDO:")
        print(f"  • Conceitos totais: {self.total_concepts}")
        print(f"  • Beats catalogados: {stats.get('total_beats', 0)}")
        print(f"  • Roteiros únicos: {stats.get('unique_screenplays', 0)}")

        if stats.get('beat_distribution'):
            print(f"\n📊 DISTRIBUIÇÃO DE BEATS:")
            for beat, count in list(stats['beat_distribution'].items())[:5]:
                print(f"  • {beat}: {count} ocorrências")

        print(f"\n💾 MEMÓRIA:")
        mem_stats = self.memory.stats()
        print(f"  • Total de registros: {mem_stats.get('total', 0):,}")
        print(f"  • Tamanho do banco: {mem_stats.get('db_size_mb', 0):.1f}MB")

        print("\n✨ SISTEMA EVOLUIU COM SUCESSO!")
        print("=" * 70)


def main():
    learner = ContinuousLearner()

    print("\n🎯 Opções de execução:")
    print("1. Análise rápida (3 arquivos)")
    print("2. Análise média (10 arquivos)")
    print("3. Análise completa (todos)")

    try:
        choice = input("\nEscolha (1-3): ").strip()
    except (EOFError, KeyboardInterrupt):
        print("\nCancelado")
        return

    if choice == '1':
        learner.run_learning_loop(max_files=3)
    elif choice == '2':
        learner.run_learning_loop(max_files=10)
    elif choice == '3':
        learner.run_learning_loop()
    else:
        print("Opção inválida")


if __name__ == "__main__":
    main()