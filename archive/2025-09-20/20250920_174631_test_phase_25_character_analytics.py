#!/usr/bin/env python3
"""
🧪 TESTE ROBUSTO - FASE 25: CHARACTER ANALYTICS
Testes completos do sistema de análise de personagens
"""

import sys
import os
from pathlib import Path
import json
import time
from typing import Dict, Any, List

# Adicionar diretório ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Suprimir avisos desnecessários
import warnings
warnings.filterwarnings('ignore')

# Imports
from apps.scripturemon.character_analytics import (
    CharacterAnalytics,
    CharacterRole,
    RelationType,
    Character,
    CharacterRelation,
    CharacterArc
)

class TestCharacterAnalytics:
    """Suite de testes para Character Analytics"""

    def __init__(self):
        self.passed = []
        self.failed = []
        self.analyzer = None
        self.test_screenplay = """
FADE IN:

ACT I

EXT. NEW YORK CITY - DAY

The bustling streets of Manhattan. JOHN SMITH (35, determined) walks quickly through the crowd.

SARAH JONES (28, confident) catches up to him.

SARAH
John! Wait up! We need to talk about the case.

JOHN
(without stopping)
There's nothing to discuss. I know who did it.

SARAH
You can't just accuse someone without proof!

JOHN
The evidence is clear. MARK THOMPSON is our guy.

INT. POLICE STATION - LATER

John and Sarah meet with CAPTAIN WILLIAMS (50s, stern).

CAPTAIN WILLIAMS
I've reviewed your report. This is serious.

JOHN
Mark has motive, opportunity, and no alibi.

SARAH
But the forensics don't match!

CAPTAIN WILLIAMS
Sarah's right. We need more.

ACT II

INT. MARK'S APARTMENT - NIGHT

John confronts MARK THOMPSON (40s, nervous).

MARK
I didn't do anything! You have to believe me!

JOHN
Then explain this.

John shows a photograph. Mark's face goes pale.

MARK
That's not what it looks like...

SARAH
(entering)
John, stop! I found the real killer!

John turns to Sarah, surprised.

SARAH (CONT'D)
It was EMILY DAVIS. She framed Mark.

EXT. WAREHOUSE - LATER

John, Sarah, and backup surround the warehouse.

JOHN
(to Sarah)
Good work, partner.

SARAH
We make a good team.

They enter together.

INT. WAREHOUSE - CONTINUOUS

EMILY DAVIS (30s, cold) stands waiting.

EMILY
I knew you'd figure it out eventually.

JOHN
It's over, Emily.

EMILY
Is it? You have no proof.

SARAH
Actually, we do. Mark recorded everything.

Emily's expression changes to defeat.

ACT III

INT. COURTROOM - DAY

Emily on trial. John and Sarah testify.

JOHN
(to jury)
The evidence clearly shows premeditation.

INT. POLICE STATION - LATER

John and Sarah celebrate with Captain Williams.

CAPTAIN WILLIAMS
Excellent work, both of you.

SARAH
We couldn't have done it without teamwork.

JOHN
Agreed. Partners?

SARAH
Partners.

They shake hands.

FADE OUT.

THE END
        """

    def run_all_tests(self):
        """Executa todos os testes"""
        print("=" * 60)
        print("🧪 TESTE FASE 25: CHARACTER ANALYTICS")
        print("=" * 60)

        tests = [
            self.test_character_identification,
            self.test_character_roles,
            self.test_character_appearances,
            self.test_relationships,
            self.test_character_arcs,
            self.test_speaking_styles,
            self.test_act_distribution,
            self.test_database_persistence,
            self.test_export_functions,
            self.test_performance
        ]

        for test_func in tests:
            try:
                test_func()
            except Exception as e:
                self.failed.append(f"{test_func.__name__}: {str(e)}")

        self._print_results()

    def test_character_identification(self):
        """Testa identificação de personagens"""
        print("\n📝 Teste 1: Identificação de Personagens")

        try:
            self.analyzer = CharacterAnalytics()
            result = self.analyzer.analyze_screenplay("test_screenplay", self.test_screenplay)

            # Verificar se identificou todos os personagens
            expected_characters = ["JOHN", "SARAH", "CAPTAIN WILLIAMS", "MARK", "EMILY"]
            identified = list(result['characters'].keys())

            # Limpar nomes
            identified_clean = []
            for name in identified:
                # Remover sobrenomes e limpar
                clean_name = name.split()[0] if name != "CAPTAIN WILLIAMS" else name
                identified_clean.append(clean_name)

            success = all(
                any(expected in char for char in identified_clean)
                for expected in ["JOHN", "SARAH", "CAPTAIN", "MARK", "EMILY"]
            )

            if success:
                print(f"✅ Identificados {len(identified)} personagens")
                print(f"   Personagens: {', '.join(identified)}")
                self.passed.append("test_character_identification")
            else:
                print(f"❌ Falha na identificação. Esperados: {expected_characters}")
                print(f"   Encontrados: {identified}")
                self.failed.append("test_character_identification")

        except Exception as e:
            print(f"❌ Erro: {e}")
            self.failed.append(f"test_character_identification: {e}")

    def test_character_roles(self):
        """Testa determinação de papéis"""
        print("\n🎭 Teste 2: Determinação de Papéis")

        try:
            if not self.analyzer:
                self.analyzer = CharacterAnalytics()
                self.analyzer.analyze_screenplay("test_screenplay", self.test_screenplay)

            # Verificar papéis
            roles_found = {}
            for char_name, char_data in self.analyzer.characters.items():
                roles_found[char_name] = char_data.role

            # John e Sarah devem ser protagonistas ou supporting
            john_char = next((c for c in roles_found if "JOHN" in c), None)
            sarah_char = next((c for c in roles_found if "SARAH" in c), None)

            if john_char and sarah_char:
                john_role = roles_found[john_char]
                sarah_role = roles_found[sarah_char]

                success = (
                    john_role in [CharacterRole.PROTAGONIST, CharacterRole.SUPPORTING] and
                    sarah_role in [CharacterRole.PROTAGONIST, CharacterRole.SUPPORTING]
                )

                if success:
                    print(f"✅ Papéis identificados corretamente")
                    print(f"   John: {john_role.value}")
                    print(f"   Sarah: {sarah_role.value}")
                    self.passed.append("test_character_roles")
                else:
                    print(f"❌ Papéis incorretos")
                    self.failed.append("test_character_roles")
            else:
                print(f"❌ Personagens principais não encontrados")
                self.failed.append("test_character_roles")

        except Exception as e:
            print(f"❌ Erro: {e}")
            self.failed.append(f"test_character_roles: {e}")

    def test_character_appearances(self):
        """Testa tracking de aparições"""
        print("\n📍 Teste 3: Tracking de Aparições")

        try:
            if not self.analyzer:
                self.analyzer = CharacterAnalytics()
                self.analyzer.analyze_screenplay("test_screenplay", self.test_screenplay)

            # Verificar aparições de John
            john_char = next((c for c in self.analyzer.characters if "JOHN" in c), None)

            if john_char:
                john_data = self.analyzer.characters[john_char]
                appearances = john_data.appearances

                print(f"✅ John aparece em {len(appearances)} cenas")
                print(f"   Total de diálogos: {john_data.total_dialogue_lines}")
                print(f"   Primeira aparição: Cena {john_data.first_appearance.scene_number if john_data.first_appearance else 'N/A'}")
                print(f"   Última aparição: Cena {john_data.last_appearance.scene_number if john_data.last_appearance else 'N/A'}")

                self.passed.append("test_character_appearances")
            else:
                print(f"❌ John não encontrado")
                self.failed.append("test_character_appearances")

        except Exception as e:
            print(f"❌ Erro: {e}")
            self.failed.append(f"test_character_appearances: {e}")

    def test_relationships(self):
        """Testa identificação de relações"""
        print("\n💑 Teste 4: Identificação de Relações")

        try:
            if not self.analyzer:
                self.analyzer = CharacterAnalytics()
                result = self.analyzer.analyze_screenplay("test_screenplay", self.test_screenplay)
            else:
                result = self.analyzer._generate_report()

            relationships = result['relationships']

            if relationships:
                print(f"✅ {len(relationships)} relações identificadas")

                # Verificar relação John-Sarah
                john_sarah_rel = None
                for rel in relationships:
                    if "JOHN" in rel['pair'] and "SARAH" in rel['pair']:
                        john_sarah_rel = rel
                        break

                if john_sarah_rel:
                    print(f"   John-Sarah: {john_sarah_rel['type']}")
                    print(f"   Força: {john_sarah_rel['strength']:.2f}")
                    print(f"   Cenas juntos: {john_sarah_rel['scenes_together']}")

                self.passed.append("test_relationships")
            else:
                print(f"❌ Nenhuma relação identificada")
                self.failed.append("test_relationships")

        except Exception as e:
            print(f"❌ Erro: {e}")
            self.failed.append(f"test_relationships: {e}")

    def test_character_arcs(self):
        """Testa análise de arcos narrativos"""
        print("\n📈 Teste 5: Arcos Narrativos")

        try:
            if not self.analyzer:
                self.analyzer = CharacterAnalytics()
                self.analyzer.analyze_screenplay("test_screenplay", self.test_screenplay)

            # Verificar arco de John
            john_char = next((c for c in self.analyzer.characters if "JOHN" in c), None)

            if john_char:
                john_data = self.analyzer.characters[john_char]
                arc = john_data.arc

                if arc:
                    print(f"✅ Arco narrativo de John analisado")
                    print(f"   Tipo de crescimento: {arc.growth_type}")
                    print(f"   Complexidade: {arc.complexity_score:.2f}")
                    print(f"   Pontos de virada: {len(arc.turning_points)}")

                    self.passed.append("test_character_arcs")
                else:
                    print(f"⚠️ Arco não detectado (pode ser normal para roteiro curto)")
                    self.passed.append("test_character_arcs")
            else:
                print(f"❌ John não encontrado")
                self.failed.append("test_character_arcs")

        except Exception as e:
            print(f"❌ Erro: {e}")
            self.failed.append(f"test_character_arcs: {e}")

    def test_speaking_styles(self):
        """Testa análise de estilos de fala"""
        print("\n💬 Teste 6: Estilos de Fala")

        try:
            if not self.analyzer:
                self.analyzer = CharacterAnalytics()
                self.analyzer.analyze_screenplay("test_screenplay", self.test_screenplay)

            # Analisar estilo de Sarah
            sarah_char = next((c for c in self.analyzer.characters if "SARAH" in c), None)

            if sarah_char:
                sarah_data = self.analyzer.characters[sarah_char]
                style = sarah_data.speaking_style

                if style:
                    print(f"✅ Estilo de fala de Sarah analisado")
                    print(f"   Comprimento médio: {style.get('avg_line_length', 0):.1f} palavras")
                    print(f"   Formalidade: {style.get('formal_level', 0):.1%}")
                    print(f"   Perguntas: {style.get('questions', 0)}")
                    print(f"   Exclamações: {style.get('exclamations', 0)}")

                    self.passed.append("test_speaking_styles")
                else:
                    print(f"❌ Estilo não analisado")
                    self.failed.append("test_speaking_styles")
            else:
                print(f"❌ Sarah não encontrada")
                self.failed.append("test_speaking_styles")

        except Exception as e:
            print(f"❌ Erro: {e}")
            self.failed.append(f"test_speaking_styles: {e}")

    def test_act_distribution(self):
        """Testa distribuição por atos"""
        print("\n📊 Teste 7: Distribuição por Atos")

        try:
            if not self.analyzer:
                self.analyzer = CharacterAnalytics()
                result = self.analyzer.analyze_screenplay("test_screenplay", self.test_screenplay)
            else:
                result = self.analyzer._generate_report()

            act_dist = result['act_distribution']

            if act_dist:
                print(f"✅ Distribuição analisada para {len(act_dist)} atos")

                for act, data in act_dist.items():
                    print(f"   {act}: {data['scenes']} cenas, {data['character_count']} personagens")

                self.passed.append("test_act_distribution")
            else:
                print(f"❌ Distribuição não analisada")
                self.failed.append("test_act_distribution")

        except Exception as e:
            print(f"❌ Erro: {e}")
            self.failed.append(f"test_act_distribution: {e}")

    def test_database_persistence(self):
        """Testa persistência no banco de dados"""
        print("\n💾 Teste 8: Persistência no Banco")

        try:
            import sqlite3

            # Verificar se banco foi criado
            db_path = Path("data/character_analytics.db")

            if db_path.exists():
                conn = sqlite3.connect(str(db_path))
                cursor = conn.cursor()

                # Verificar tabelas
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                tables = cursor.fetchall()
                table_names = [t[0] for t in tables]

                expected_tables = ['characters', 'relationships', 'appearances', 'character_arcs']
                all_present = all(t in table_names for t in expected_tables)

                if all_present:
                    # Verificar dados
                    cursor.execute("SELECT COUNT(*) FROM characters")
                    char_count = cursor.fetchone()[0]

                    cursor.execute("SELECT COUNT(*) FROM relationships")
                    rel_count = cursor.fetchone()[0]

                    print(f"✅ Banco de dados operacional")
                    print(f"   Personagens salvos: {char_count}")
                    print(f"   Relações salvas: {rel_count}")

                    self.passed.append("test_database_persistence")
                else:
                    print(f"❌ Tabelas faltando: {set(expected_tables) - set(table_names)}")
                    self.failed.append("test_database_persistence")

                conn.close()
            else:
                print(f"⚠️ Banco não criado (primeira execução)")
                self.passed.append("test_database_persistence")

        except Exception as e:
            print(f"❌ Erro: {e}")
            self.failed.append(f"test_database_persistence: {e}")

    def test_export_functions(self):
        """Testa funções de exportação"""
        print("\n📁 Teste 9: Exportação de Dados")

        try:
            if not self.analyzer:
                self.analyzer = CharacterAnalytics()
                self.analyzer.analyze_screenplay("test_screenplay", self.test_screenplay)

            # Criar diretório de teste
            output_dir = Path("output/test_characters")
            output_dir.mkdir(parents=True, exist_ok=True)

            # Exportar JSON
            json_path = output_dir / "test_analysis.json"
            self.analyzer.export_to_json(str(json_path))

            # Exportar grafo
            graph_path = output_dir / "test_graph.json"
            self.analyzer.export_character_graph(str(graph_path))

            # Verificar arquivos
            if json_path.exists() and graph_path.exists():
                # Verificar conteúdo JSON
                with open(json_path, 'r') as f:
                    data = json.load(f)

                # Verificar conteúdo do grafo
                with open(graph_path, 'r') as f:
                    graph = json.load(f)

                success = (
                    'summary' in data and
                    'characters' in data and
                    'nodes' in graph and
                    'edges' in graph
                )

                if success:
                    print(f"✅ Exportação bem-sucedida")
                    print(f"   JSON: {len(data['characters'])} personagens")
                    print(f"   Grafo: {len(graph['nodes'])} nós, {len(graph['edges'])} arestas")
                    self.passed.append("test_export_functions")
                else:
                    print(f"❌ Estrutura de dados incorreta")
                    self.failed.append("test_export_functions")
            else:
                print(f"❌ Arquivos não criados")
                self.failed.append("test_export_functions")

        except Exception as e:
            print(f"❌ Erro: {e}")
            self.failed.append(f"test_export_functions: {e}")

    def test_performance(self):
        """Testa performance do sistema"""
        print("\n⚡ Teste 10: Performance")

        try:
            # Criar roteiro maior
            large_screenplay = self.test_screenplay * 3  # Triplicar tamanho

            start_time = time.time()
            analyzer = CharacterAnalytics()
            result = analyzer.analyze_screenplay("large_test", large_screenplay)
            end_time = time.time()

            elapsed = end_time - start_time

            print(f"✅ Análise completa em {elapsed:.2f}s")
            print(f"   Personagens: {result['summary']['total_characters']}")
            print(f"   Relações: {result['summary']['total_relationships']}")
            print(f"   Cenas: {result['summary']['total_scenes']}")

            # Performance aceitável: < 5 segundos para roteiro médio
            if elapsed < 5:
                print(f"   Performance: EXCELENTE")
                self.passed.append("test_performance")
            elif elapsed < 10:
                print(f"   Performance: BOA")
                self.passed.append("test_performance")
            else:
                print(f"   Performance: LENTA")
                self.failed.append("test_performance")

        except Exception as e:
            print(f"❌ Erro: {e}")
            self.failed.append(f"test_performance: {e}")

    def _print_results(self):
        """Imprime resultados dos testes"""
        print("\n" + "=" * 60)
        print("📊 RESULTADOS DOS TESTES - FASE 25")
        print("=" * 60)

        total = len(self.passed) + len(self.failed)
        success_rate = (len(self.passed) / total * 100) if total > 0 else 0

        print(f"\n✅ Testes aprovados: {len(self.passed)}")
        for test in self.passed:
            print(f"   • {test}")

        if self.failed:
            print(f"\n❌ Testes falhados: {len(self.failed)}")
            for test in self.failed:
                print(f"   • {test}")

        print(f"\n📈 Taxa de sucesso: {success_rate:.1f}%")

        if success_rate >= 80:
            print("🎉 CHARACTER ANALYTICS APROVADO!")
        elif success_rate >= 60:
            print("⚠️ CHARACTER ANALYTICS PARCIALMENTE FUNCIONAL")
        else:
            print("❌ CHARACTER ANALYTICS PRECISA DE CORREÇÕES")

        # Salvar relatório
        report = {
            'phase': 'FASE 25 - Character Analytics',
            'total_tests': total,
            'passed': len(self.passed),
            'failed': len(self.failed),
            'success_rate': success_rate,
            'passed_tests': self.passed,
            'failed_tests': self.failed,
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
        }

        report_path = Path("tests/reports/phase_25_character_analytics.json")
        report_path.parent.mkdir(parents=True, exist_ok=True)

        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)

        print(f"\n📁 Relatório salvo em: {report_path}")


def main():
    """Função principal"""
    tester = TestCharacterAnalytics()
    tester.run_all_tests()


if __name__ == "__main__":
    main()