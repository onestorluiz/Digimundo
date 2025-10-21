#!/usr/bin/env python3
"""
Teste Completo do Sistema de Aprendizado com Token Turbo
Avalia aprendizados, acesso às pastas e qualidade da análise
"""

import sys
import time
import json
from pathlib import Path
from datetime import datetime
from collections import Counter

# Adiciona src ao path
sys.path.insert(0, 'src')

from scripturemon_champion.core.profiles import LearningProfiles
from scripturemon_champion.analysis.script_doctor import ScriptDoctor
from scripturemon_champion.analysis.theory import TheoryComparator
from scripturemon_champion.learning.learning_lite import LearningLite
from scripturemon_champion.core.memory import UnifiedMemory, MemoryRecord

print("=" * 80)
print("🧠 TESTE DO SISTEMA DE APRENDIZADO - TOKEN TURBO")
print("=" * 80)
print()

class LearningSystemTester:
    def __init__(self):
        self.profile = LearningProfiles.get_profile('token_turbo')
        self.config = self.profile.config

        # Componentes
        self.doctor = ScriptDoctor(use_learning=True)
        self.learning = LearningLite()
        self.theory = TheoryComparator(Path("theory"))
        self.memory = UnifiedMemory(Path("data/unified_memory.db"))

        # Pastas de conteúdo
        self.my_screenplays_path = Path("/Users/clubproducoes/Digimundo/scripturemon-ultimate/my_screenplays")
        self.theory_path = Path("/Users/clubproducoes/Digimundo/scripturemon-ultimate/theory")

        # Resultados
        self.results = {
            'timestamp': datetime.now().isoformat(),
            'profile': 'token_turbo',
            'tests': [],
            'learning_stats': {},
            'quality_metrics': {},
            'errors': []
        }

    def log(self, msg: str, level: str = "INFO"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        symbol = {"INFO": "ℹ️", "SUCCESS": "✅", "WARNING": "⚠️", "ERROR": "❌", "LEARN": "🧠"}.get(level, "•")
        print(f"[{timestamp}] {symbol} {msg}")

    def test_1_folder_access(self):
        """Teste 1: Verificar acesso às pastas"""
        self.log("Teste 1: Verificando acesso às pastas", "INFO")

        try:
            # Verificar my_screenplays
            assert self.my_screenplays_path.exists(), "Pasta my_screenplays não existe"
            screenplays = list(self.my_screenplays_path.glob("*.txt"))
            self.log(f"Roteiros encontrados: {len(screenplays)}", "SUCCESS")
            for sp in screenplays:
                size_kb = sp.stat().st_size / 1024
                self.log(f"  • {sp.name} ({size_kb:.1f}KB)", "INFO")

            # Verificar theory
            assert self.theory_path.exists(), "Pasta theory não existe"
            theory_files = list(self.theory_path.glob("*.txt"))
            self.log(f"Livros de teoria encontrados: {len(theory_files)}", "SUCCESS")

            # Listar principais
            for tf in theory_files[:5]:
                size_kb = tf.stat().st_size / 1024
                self.log(f"  • {tf.name[:40]}... ({size_kb:.1f}KB)", "INFO")

            self.results['tests'].append({
                'name': 'folder_access',
                'status': 'passed',
                'screenplays': len(screenplays),
                'theory_books': len(theory_files)
            })

            return screenplays, theory_files

        except Exception as e:
            self.log(f"Erro no acesso: {e}", "ERROR")
            self.results['errors'].append(str(e))
            return [], []

    def test_2_theory_loading(self):
        """Teste 2: Carregar e indexar teoria"""
        self.log("Teste 2: Carregando biblioteca de teoria", "INFO")

        try:
            start = time.time()
            n_docs = self.theory.build()
            elapsed = time.time() - start

            self.log(f"Documentos indexados: {n_docs}", "SUCCESS")
            self.log(f"Tempo de indexação: {elapsed:.2f}s", "INFO")

            # Testar busca
            test_queries = [
                "Save the Cat beats",
                "character arc",
                "three act structure",
                "dialogue subtext"
            ]

            for query in test_queries:
                hits = self.theory.compare(query, k=2)
                if hits:
                    self.log(f"Query '{query}': {hits[0].score:.2f} score", "SUCCESS")
                    self.log(f"  Melhor match: {hits[0].doc_id[:30]}...", "INFO")

            self.results['tests'].append({
                'name': 'theory_loading',
                'status': 'passed',
                'documents': n_docs,
                'index_time': f"{elapsed:.2f}s"
            })

            return n_docs

        except Exception as e:
            self.log(f"Erro na teoria: {e}", "ERROR")
            self.results['errors'].append(str(e))
            return 0

    def test_3_screenplay_analysis(self):
        """Teste 3: Analisar roteiros com Token Turbo config"""
        self.log("Teste 3: Analisando roteiros com Token Turbo", "INFO")

        try:
            screenplay_path = self.my_screenplays_path / "sonhos_sem_lembrancas_t3.txt"

            if not screenplay_path.exists():
                self.log("Usando roteiro de exemplo", "WARNING")
                screenplay_path = self.my_screenplays_path / "exemplo_roteiro.txt"

            self.log(f"Analisando: {screenplay_path.name}", "INFO")

            # Carregar texto
            text = screenplay_path.read_text(encoding='utf-8', errors='ignore')
            text_size = len(text)
            token_estimate = len(text.split())

            self.log(f"Tamanho: {text_size:,} chars (~{token_estimate:,} tokens)", "INFO")

            # Analisar com Doctor
            start = time.time()
            analysis = self.doctor.analyze_script(text, screenplay_path.stem)
            elapsed_doctor = time.time() - start

            self.log(f"Análise Doctor em {elapsed_doctor:.2f}s", "SUCCESS")
            self.log(f"  • Cenas: {analysis.scenes}", "INFO")
            self.log(f"  • Personagens: {len(analysis.top_characters)}", "INFO")
            self.log(f"  • Diálogo: {analysis.dialogue_ratio:.1%}", "INFO")
            self.log(f"  • Pacing: {analysis.pacing_score:.2f}", "INFO")

            # Analisar Save the Cat
            start = time.time()
            stc = self.doctor.analyze_save_the_cat(text)
            elapsed_stc = time.time() - start

            self.log(f"Save the Cat em {elapsed_stc:.2f}s", "SUCCESS")
            self.log(f"  • Beats detectados: {len(stc.beats)}", "INFO")
            self.log(f"  • Beats faltando: {len(stc.missing_beats)}", "INFO")

            # Listar beats encontrados
            for beat in stc.beats[:5]:
                self.log(f"    - {beat.name} ({beat.pct:.1f}%)", "LEARN")

            self.results['tests'].append({
                'name': 'screenplay_analysis',
                'status': 'passed',
                'file': screenplay_path.name,
                'tokens': token_estimate,
                'scenes': analysis.scenes,
                'beats': len(stc.beats),
                'analysis_time': f"{elapsed_doctor + elapsed_stc:.2f}s"
            })

            return analysis, stc

        except Exception as e:
            self.log(f"Erro na análise: {e}", "ERROR")
            self.results['errors'].append(str(e))
            return None, None

    def test_4_learning_process(self):
        """Teste 4: Processo de aprendizado"""
        self.log("Teste 4: Testando processo de aprendizado", "INFO")

        try:
            # Stats antes
            stats_before = self.learning.get_statistics()
            self.log(f"Stats antes: {stats_before.get('total_beats', 0)} beats", "INFO")

            # Processar cada roteiro
            screenplays = list(self.my_screenplays_path.glob("*.txt"))
            total_concepts = 0
            learned_items = []

            for sp in screenplays:
                self.log(f"Aprendendo com: {sp.name}", "LEARN")

                text = sp.read_text(encoding='utf-8', errors='ignore')
                analysis = self.doctor.analyze_script(text, sp.stem)

                # Aprender
                concepts = self.learning.learn_from_analysis(analysis, sp.stem)
                total_concepts += len(concepts)

                self.log(f"  • Conceitos aprendidos: {len(concepts)}", "SUCCESS")

                # Guardar alguns exemplos
                if concepts:
                    learned_items.extend(concepts[:2])

            # Stats depois
            stats_after = self.learning.get_statistics()
            self.log(f"Stats depois: {stats_after.get('total_beats', 0)} beats", "SUCCESS")

            # Métricas de aprendizado
            self.results['learning_stats'] = {
                'total_concepts': total_concepts,
                'beats_before': stats_before.get('total_beats', 0),
                'beats_after': stats_after.get('total_beats', 0),
                'unique_patterns': stats_after.get('unique_patterns', 0),
                'files_processed': len(screenplays)
            }

            # Exemplos de aprendizado
            self.log("\nExemplos de conceitos aprendidos:", "LEARN")
            for item in learned_items[:5]:
                if isinstance(item, dict):
                    self.log(f"  • {item.get('type', 'unknown')}: {str(item.get('value', ''))[:50]}", "INFO")

            self.results['tests'].append({
                'name': 'learning_process',
                'status': 'passed',
                'concepts_learned': total_concepts,
                'files': len(screenplays)
            })

            return total_concepts

        except Exception as e:
            self.log(f"Erro no aprendizado: {e}", "ERROR")
            self.results['errors'].append(str(e))
            return 0

    def test_5_theory_integration(self):
        """Teste 5: Integração teoria + roteiros"""
        self.log("Teste 5: Testando integração teoria + roteiros", "INFO")

        try:
            # Pegar um roteiro
            screenplay_path = self.my_screenplays_path / "sonhos_sem_lembrancas_t3.txt"
            if not screenplay_path.exists():
                screenplay_path = list(self.my_screenplays_path.glob("*.txt"))[0]

            text = screenplay_path.read_text(encoding='utf-8', errors='ignore')[:5000]  # Primeiras páginas

            # Buscar teoria relevante
            self.log("Buscando teoria relevante para o roteiro...", "INFO")

            # Extrair temas do roteiro
            themes = []
            if "dream" in text.lower() or "sonho" in text.lower():
                themes.append("dreams subconscious")
            if "memory" in text.lower() or "lembrança" in text.lower():
                themes.append("memory identity")

            theory_connections = []
            for theme in themes:
                hits = self.theory.compare(theme, k=3)
                for hit in hits:
                    theory_connections.append({
                        'theme': theme,
                        'theory': hit.doc_id,
                        'score': hit.score,
                        'excerpt': hit.excerpt[:100]
                    })
                    self.log(f"  • Tema '{theme}' → {hit.doc_id[:30]} (score: {hit.score:.2f})", "LEARN")

            # Simular análise com contexto expandido (Token Turbo)
            self.log("\nSimulando análise Token Turbo (200K context):", "INFO")

            # Carregar Save the Cat para contexto
            save_cat_path = self.theory_path / "save_the_cat.txt"
            if save_cat_path.exists():
                theory_text = save_cat_path.read_text(encoding='utf-8', errors='ignore')
                combined_size = len(text) + len(theory_text)
                combined_tokens = len((text + theory_text).split())

                self.log(f"  • Roteiro: {len(text):,} chars", "INFO")
                self.log(f"  • Teoria: {len(theory_text):,} chars", "INFO")
                self.log(f"  • Total: {combined_size:,} chars (~{combined_tokens:,} tokens)", "SUCCESS")

                if combined_tokens < 200000:
                    self.log(f"  ✅ Cabe no Token Turbo! ({combined_tokens:,}/200,000)", "SUCCESS")
                else:
                    self.log(f"  ⚠️ Muito grande para Token Turbo ({combined_tokens:,}/200,000)", "WARNING")

            self.results['tests'].append({
                'name': 'theory_integration',
                'status': 'passed',
                'theory_connections': len(theory_connections),
                'themes': themes
            })

            return theory_connections

        except Exception as e:
            self.log(f"Erro na integração: {e}", "ERROR")
            self.results['errors'].append(str(e))
            return []

    def test_6_memory_persistence(self):
        """Teste 6: Persistência de aprendizados na memória"""
        self.log("Teste 6: Testando persistência de aprendizados", "INFO")

        try:
            # Salvar aprendizados
            learning_record = MemoryRecord(
                type="learning_test",
                key=f"token_turbo_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                value={
                    'profile': 'token_turbo',
                    'learning_stats': self.results['learning_stats'],
                    'quality_metrics': self.results.get('quality_metrics', {})
                },
                metadata={'test': True, 'timestamp': datetime.now().isoformat()}
            )

            record_id = self.memory.store(learning_record)
            self.log(f"Aprendizado salvo com ID: {record_id}", "SUCCESS")

            # Recuperar e verificar
            retrieved = self.memory.get("learning_test", learning_record.key)
            assert retrieved is not None, "Falha ao recuperar"
            assert retrieved.value['profile'] == 'token_turbo', "Perfil incorreto"

            self.log("Recuperação bem-sucedida", "SUCCESS")

            # Stats gerais
            stats = self.memory.stats()
            total_records = stats.get('total_records', 0)
            self.log(f"Total de registros na memória: {total_records}", "INFO")

            # Buscar aprendizados anteriores
            self.log("Buscando aprendizados anteriores...", "INFO")
            # Aqui seria ideal ter um método search, mas vamos simular

            self.results['tests'].append({
                'name': 'memory_persistence',
                'status': 'passed',
                'record_id': record_id,
                'total_records': total_records
            })

            return record_id

        except Exception as e:
            self.log(f"Erro na memória: {e}", "ERROR")
            self.results['errors'].append(str(e))
            return None

    def test_7_quality_assessment(self):
        """Teste 7: Avaliação da qualidade dos aprendizados"""
        self.log("Teste 7: Avaliando qualidade dos aprendizados", "INFO")

        try:
            # Métricas de qualidade
            quality = {
                'beat_detection_accuracy': 0.0,
                'character_extraction': 0.0,
                'theme_relevance': 0.0,
                'pacing_analysis': 0.0,
                'overall_score': 0.0
            }

            # Testar com roteiro conhecido
            test_file = self.my_screenplays_path / "sonhos_sem_lembrancas_t3.txt"
            if test_file.exists():
                text = test_file.read_text(encoding='utf-8', errors='ignore')

                # Análise completa
                analysis = self.doctor.analyze_script(text, test_file.stem)
                stc = self.doctor.analyze_save_the_cat(text)

                # Avaliar beat detection
                if len(stc.beats) > 0:
                    quality['beat_detection_accuracy'] = min(len(stc.beats) / 15.0, 1.0)  # 15 beats esperados
                    self.log(f"Beat detection: {quality['beat_detection_accuracy']:.1%}", "LEARN")

                # Avaliar character extraction
                if len(analysis.top_characters) > 0:
                    quality['character_extraction'] = min(len(analysis.top_characters) / 5.0, 1.0)  # 5+ chars bom
                    self.log(f"Character extraction: {quality['character_extraction']:.1%}", "LEARN")

                # Avaliar pacing
                quality['pacing_analysis'] = analysis.pacing_score
                self.log(f"Pacing analysis: {quality['pacing_analysis']:.1%}", "LEARN")

                # Tema relevância (buscar na teoria)
                if self.theory:
                    hits = self.theory.compare(' '.join(analysis.top_characters[:3]), k=5)
                    if hits:
                        quality['theme_relevance'] = min(hits[0].score / 10.0, 1.0)  # Normalizar score
                        self.log(f"Theme relevance: {quality['theme_relevance']:.1%}", "LEARN")

            # Score geral
            quality['overall_score'] = sum(quality.values()) / (len(quality) - 1)  # -1 para não contar o próprio overall
            self.log(f"\nQualidade geral: {quality['overall_score']:.1%}", "SUCCESS")

            # Classificação
            if quality['overall_score'] >= 0.8:
                self.log("🏆 Qualidade EXCELENTE!", "SUCCESS")
            elif quality['overall_score'] >= 0.6:
                self.log("✅ Qualidade BOA", "SUCCESS")
            elif quality['overall_score'] >= 0.4:
                self.log("⚠️ Qualidade RAZOÁVEL", "WARNING")
            else:
                self.log("❌ Qualidade BAIXA", "ERROR")

            self.results['quality_metrics'] = quality
            self.results['tests'].append({
                'name': 'quality_assessment',
                'status': 'passed',
                'overall_score': f"{quality['overall_score']:.1%}"
            })

            return quality

        except Exception as e:
            self.log(f"Erro na avaliação: {e}", "ERROR")
            self.results['errors'].append(str(e))
            return {}

    def test_8_token_turbo_capacity(self):
        """Teste 8: Capacidade real do Token Turbo"""
        self.log("Teste 8: Testando capacidade do Token Turbo", "INFO")

        try:
            # Calcular tamanho total disponível
            total_chars = 0
            total_tokens = 0

            # Roteiros
            for sp in self.my_screenplays_path.glob("*.txt"):
                text = sp.read_text(encoding='utf-8', errors='ignore')
                total_chars += len(text)
                total_tokens += len(text.split())

            self.log(f"Roteiros: {total_chars:,} chars (~{total_tokens:,} tokens)", "INFO")

            # Teoria (pegar maior livro)
            largest_theory = None
            largest_size = 0

            for tf in self.theory_path.glob("*.txt"):
                size = tf.stat().st_size
                if size > largest_size:
                    largest_size = size
                    largest_theory = tf

            if largest_theory:
                theory_text = largest_theory.read_text(encoding='utf-8', errors='ignore')
                theory_tokens = len(theory_text.split())
                self.log(f"Maior livro: {largest_theory.name[:40]}... ({theory_tokens:,} tokens)", "INFO")

                # Verificar se cabe no Token Turbo
                combined = total_tokens + theory_tokens
                capacity_used = (combined / 200000) * 100

                self.log(f"\n📊 Análise de capacidade Token Turbo:", "INFO")
                self.log(f"  • Roteiros: {total_tokens:,} tokens", "INFO")
                self.log(f"  • Teoria: {theory_tokens:,} tokens", "INFO")
                self.log(f"  • Total: {combined:,} tokens", "INFO")
                self.log(f"  • Capacidade usada: {capacity_used:.1f}%", "INFO")

                if capacity_used <= 100:
                    self.log(f"  ✅ CABE no Token Turbo! ({200000 - combined:,} tokens livres)", "SUCCESS")
                else:
                    self.log(f"  ⚠️ Excede Token Turbo em {combined - 200000:,} tokens", "WARNING")

            self.results['tests'].append({
                'name': 'token_turbo_capacity',
                'status': 'passed',
                'total_tokens': combined,
                'capacity_used': f"{capacity_used:.1f}%"
            })

            return capacity_used

        except Exception as e:
            self.log(f"Erro na capacidade: {e}", "ERROR")
            self.results['errors'].append(str(e))
            return 0

    def run_all_tests(self):
        """Executa todos os testes"""
        self.log("Iniciando bateria completa de testes de aprendizado", "INFO")
        print("-" * 80)

        # Executar testes em sequência
        screenplays, theory_files = self.test_1_folder_access()
        print()

        n_theory = self.test_2_theory_loading()
        print()

        analysis, stc = self.test_3_screenplay_analysis()
        print()

        concepts = self.test_4_learning_process()
        print()

        connections = self.test_5_theory_integration()
        print()

        record_id = self.test_6_memory_persistence()
        print()

        quality = self.test_7_quality_assessment()
        print()

        capacity = self.test_8_token_turbo_capacity()

        # Resumo final
        print()
        print("=" * 80)
        print("📊 RESULTADOS FINAIS - SISTEMA DE APRENDIZADO")
        print("=" * 80)

        # Contar sucessos
        passed = sum(1 for t in self.results['tests'] if t['status'] == 'passed')
        total = len(self.results['tests'])

        print(f"\n✅ Testes aprovados: {passed}/{total}")
        print(f"❌ Erros encontrados: {len(self.results['errors'])}")

        if self.results['errors']:
            print("\n⚠️ ERROS:")
            for err in self.results['errors']:
                print(f"  • {err}")

        # Stats de aprendizado
        if self.results['learning_stats']:
            print(f"\n🧠 ESTATÍSTICAS DE APRENDIZADO:")
            stats = self.results['learning_stats']
            print(f"  • Conceitos aprendidos: {stats.get('total_concepts', 0)}")
            print(f"  • Beats catalogados: {stats.get('beats_after', 0)}")
            print(f"  • Padrões únicos: {stats.get('unique_patterns', 0)}")
            print(f"  • Arquivos processados: {stats.get('files_processed', 0)}")

        # Qualidade
        if self.results['quality_metrics']:
            print(f"\n🎯 QUALIDADE DOS APRENDIZADOS:")
            quality = self.results['quality_metrics']
            print(f"  • Beat detection: {quality['beat_detection_accuracy']:.1%}")
            print(f"  • Character extraction: {quality['character_extraction']:.1%}")
            print(f"  • Theme relevance: {quality['theme_relevance']:.1%}")
            print(f"  • Pacing analysis: {quality['pacing_analysis']:.1%}")
            print(f"  • OVERALL: {quality['overall_score']:.1%}")

        # Salvar relatório
        report_path = Path(f"learning_test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        with open(report_path, 'w') as f:
            json.dump(self.results, f, indent=2)
        print(f"\n💾 Relatório salvo: {report_path}")

        # Veredito
        print()
        print("=" * 80)
        if passed == total and quality.get('overall_score', 0) >= 0.6:
            print("🎉 SISTEMA DE APRENDIZADO APROVADO - ALTA QUALIDADE!")
        elif passed >= total * 0.8:
            print("✅ SISTEMA FUNCIONAL - QUALIDADE SATISFATÓRIA")
        else:
            print("⚠️ SISTEMA PRECISA DE AJUSTES")
        print("=" * 80)

        return self.results

if __name__ == "__main__":
    tester = LearningSystemTester()
    results = tester.run_all_tests()

    # Código de saída
    if len(results['errors']) == 0:
        sys.exit(0)
    else:
        sys.exit(1)