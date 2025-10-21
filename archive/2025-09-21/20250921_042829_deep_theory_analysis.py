#!/usr/bin/env python3
"""
Sistema de Análise Profunda com 13 Teorias
Utiliza Mixtral para insights teóricos profundos
"""

import sys
import json
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import requests
from dataclasses import dataclass

sys.path.insert(0, 'src')

from scripturemon_champion.analysis.script_doctor import ScriptDoctor

@dataclass
class TheoryInsight:
    """Insight profundo sobre aplicação de teoria"""
    theory_name: str
    adherence_score: float  # 0-1
    strengths: List[str]
    weaknesses: List[str]
    specific_examples: List[str]
    recommendations: List[str]

class DeepTheoryAnalyzer:
    """
    Análise profunda comparando roteiros com 13 teorias clássicas
    """

    def __init__(self):
        self.doctor = ScriptDoctor()
        self.ollama_endpoint = "http://127.0.0.1:11434/api/generate"
        self.model = "mixtral-eco-q5:latest"

        # As 13 teorias fundamentais
        self.theories = [
            "Save the Cat (Blake Snyder)",
            "Story (Robert McKee)",
            "The Hero's Journey (Joseph Campbell)",
            "Three Act Structure (Syd Field)",
            "The Anatomy of Story (John Truby)",
            "Into the Woods (John Yorke)",
            "The Writer's Journey (Christopher Vogler)",
            "Creating Character Arcs (K.M. Weiland)",
            "Story Circle (Dan Harmon)",
            "Sequence Method (Paul Gulino)",
            "Mini-Movie Method (Chris Soth)",
            "Nutshell Technique (Jill Chamberlain)",
            "Story Grid (Shawn Coyne)"
        ]

        # Diretórios
        self.theory_dir = Path("theory")
        self.screenplays_dir = Path("screenplays")
        self.my_screenplays_dir = Path("my_screenplays")

        # Cache de teorias carregadas
        self.theory_cache = {}

    def load_theory(self, theory_name: str) -> Optional[str]:
        """Carrega o conteúdo de uma teoria do diretório theory/"""

        if theory_name in self.theory_cache:
            return self.theory_cache[theory_name]

        # Procurar arquivo correspondente
        theory_files = {
            "Save the Cat": ["save_the_cat.txt", "blake_snyder.txt"],
            "Story": ["story.txt", "mckee.txt"],
            "Hero's Journey": ["hero_journey.txt", "campbell.txt", "monomyth.txt"],
            "Three Act": ["three_act.txt", "syd_field.txt"],
            "Anatomy": ["anatomy.txt", "truby.txt"],
            "Into the Woods": ["into_woods.txt", "yorke.txt"],
            "Writer's Journey": ["writer_journey.txt", "vogler.txt"],
            "Character Arcs": ["character_arcs.txt", "weiland.txt"],
            "Story Circle": ["story_circle.txt", "harmon.txt"],
            "Sequence": ["sequence.txt", "gulino.txt"],
            "Mini-Movie": ["mini_movie.txt", "soth.txt"],
            "Nutshell": ["nutshell.txt", "chamberlain.txt"],
            "Story Grid": ["story_grid.txt", "coyne.txt"]
        }

        for key, possible_files in theory_files.items():
            if key.lower() in theory_name.lower():
                for filename in possible_files:
                    filepath = self.theory_dir / filename
                    if filepath.exists():
                        content = filepath.read_text(encoding='utf-8', errors='ignore')
                        self.theory_cache[theory_name] = content
                        return content

        # Se não encontrou arquivo específico, criar resumo básico
        return self.get_theory_summary(theory_name)

    def get_theory_summary(self, theory_name: str) -> str:
        """Retorna resumo básico da teoria se não houver arquivo"""

        summaries = {
            "Save the Cat": """
15 beats essenciais:
1. Opening Image (0-1%)
2. Theme Stated (5%)
3. Set-Up (1-10%)
4. Catalyst (10%)
5. Debate (10-20%)
6. Break into Two (20%)
7. B Story (22%)
8. Fun and Games (20-50%)
9. Midpoint (50%)
10. Bad Guys Close In (50-75%)
11. All Is Lost (75%)
12. Dark Night of the Soul (75-80%)
13. Break into Three (80%)
14. Finale (80-99%)
15. Final Image (99-100%)
""",
            "Story": """
Princípios de Robert McKee:
- Inciting Incident: desequilíbrio inicial
- Progressive Complications: conflitos crescentes
- Crisis: decisão crucial
- Climax: momento de mudança irreversível
- Resolution: novo equilíbrio
- Valores em conflito
- Gap entre expectativa e resultado
""",
            "Hero's Journey": """
Jornada do Herói (Campbell/Vogler):
1. Mundo Comum
2. Chamado à Aventura
3. Recusa do Chamado
4. Encontro com Mentor
5. Travessia do Primeiro Limiar
6. Testes, Aliados, Inimigos
7. Aproximação da Caverna
8. Provação
9. Recompensa
10. Caminho de Volta
11. Ressurreição
12. Retorno com Elixir
""",
            "Three Act": """
Estrutura de 3 Atos (Syd Field):
- Ato I (25%): Setup
  - Apresentação
  - Incidente Incitante
  - Plot Point 1
- Ato II (50%): Confrontação
  - Desenvolvimento
  - Midpoint
  - Plot Point 2
- Ato III (25%): Resolução
  - Climax
  - Desfecho
""",
            "Character Arcs": """
Arcos de Personagem (K.M. Weiland):
- The Lie: crença falsa inicial
- The Want: objetivo externo
- The Need: necessidade interna real
- The Ghost: trauma do passado
- Positive Arc: Lie → Truth
- Negative Arc: resistência à verdade
- Flat Arc: já conhece a verdade
"""
        }

        for key, summary in summaries.items():
            if key in theory_name:
                return summary

        return f"Teoria: {theory_name}\n[Resumo não disponível]"

    def analyze_screenplay_with_theory(
        self,
        screenplay_text: str,
        screenplay_name: str,
        theory_name: str,
        theory_content: str
    ) -> TheoryInsight:
        """Analisa um roteiro específico contra uma teoria específica"""

        # Análise estrutural básica
        analysis = self.doctor.analyze_script(screenplay_text, screenplay_name)
        stc = self.doctor.analyze_save_the_cat(screenplay_text)

        # Preparar contexto
        context = f"""
ROTEIRO: {screenplay_name}
- Cenas: {analysis.scenes}
- Beats detectados: {len(stc.beats)}/15
- Personagens: {', '.join(analysis.top_characters[:5]) if analysis.top_characters else 'N/A'}
- Diálogo: {analysis.dialogue_ratio:.1%}
- Ritmo: {analysis.pacing_score:.2f}

BEATS PRESENTES:
{', '.join([b.name for b in stc.beats])}

INÍCIO DO ROTEIRO (primeiras 1500 palavras):
{' '.join(screenplay_text.split()[:1500])}
"""

        # Prompt para análise profunda
        prompt = f"""Você é um especialista em teoria de roteiro. Analise este roteiro contra a teoria específica.

{context}

TEORIA: {theory_name}
{theory_content[:2000]}  # Primeiros 2000 chars da teoria

ANÁLISE PROFUNDA REQUERIDA:

1. ADERÊNCIA (0-100%): Quanto o roteiro segue esta teoria específica?

2. PONTOS FORTES (3 específicos):
   - Onde o roteiro aplica bem esta teoria?
   - Cite cenas ou momentos específicos

3. PONTOS FRACOS (3 específicos):
   - Onde o roteiro falha em aplicar a teoria?
   - O que está faltando?

4. EXEMPLOS CONCRETOS (2-3):
   - Cite momentos específicos do roteiro
   - Relacione com conceitos da teoria

5. RECOMENDAÇÕES (3 acionáveis):
   - Como melhorar baseado nesta teoria?
   - Sugestões práticas e específicas

Responda em JSON:
{{
  "adherence_score": [0.0 a 1.0],
  "strengths": ["força 1", "força 2", "força 3"],
  "weaknesses": ["fraqueza 1", "fraqueza 2", "fraqueza 3"],
  "specific_examples": ["exemplo 1", "exemplo 2"],
  "recommendations": ["recomendação 1", "recomendação 2", "recomendação 3"]
}}

Seja ESPECÍFICO e CRÍTICO. Não seja genérico."""

        try:
            response = requests.post(
                self.ollama_endpoint,
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "temperature": 0.4,
                    "top_p": 0.9
                },
                timeout=45
            )

            if response.status_code == 200:
                result = response.json()
                completion = result.get("response", "")

                # Extrair JSON
                if "{" in completion and "}" in completion:
                    start = completion.find("{")
                    end = completion.rfind("}") + 1
                    json_str = completion[start:end]

                    data = json.loads(json_str)

                    return TheoryInsight(
                        theory_name=theory_name,
                        adherence_score=float(data.get("adherence_score", 0.5)),
                        strengths=data.get("strengths", []),
                        weaknesses=data.get("weaknesses", []),
                        specific_examples=data.get("specific_examples", []),
                        recommendations=data.get("recommendations", [])
                    )

        except Exception as e:
            print(f"⚠️ Erro analisando com {theory_name}: {e}")

        # Fallback se Ollama falhar
        return TheoryInsight(
            theory_name=theory_name,
            adherence_score=0.5,
            strengths=["Análise não disponível"],
            weaknesses=["Análise não disponível"],
            specific_examples=["Análise não disponível"],
            recommendations=["Análise não disponível"]
        )

    def deep_analysis(self, screenplay_path: Path, theories_to_analyze: List[str] = None):
        """Análise profunda de um roteiro contra múltiplas teorias"""

        print("=" * 80)
        print(f"🔬 ANÁLISE PROFUNDA: {screenplay_path.name}")
        print("=" * 80)

        # Carregar roteiro
        screenplay_text = screenplay_path.read_text(encoding='utf-8', errors='ignore')
        screenplay_name = screenplay_path.stem

        # Teorias a analisar
        if theories_to_analyze is None:
            theories_to_analyze = self.theories[:5]  # Top 5 por padrão

        insights = []

        for theory_name in theories_to_analyze:
            print(f"\n📚 Analisando contra: {theory_name}")

            # Carregar conteúdo da teoria
            theory_content = self.load_theory(theory_name)

            # Analisar
            insight = self.analyze_screenplay_with_theory(
                screenplay_text,
                screenplay_name,
                theory_name,
                theory_content
            )

            insights.append(insight)

            # Mostrar resultado
            print(f"  📊 Aderência: {insight.adherence_score:.1%}")

            if insight.strengths[0] != "Análise não disponível":
                print(f"  ✅ Força principal: {insight.strengths[0]}")
                print(f"  ❌ Fraqueza principal: {insight.weaknesses[0]}")
                print(f"  💡 Recomendação: {insight.recommendations[0]}")

            time.sleep(2)  # Pausa entre análises

        # Relatório consolidado
        self.generate_deep_report(screenplay_name, insights)

        return insights

    def generate_deep_report(self, screenplay_name: str, insights: List[TheoryInsight]):
        """Gera relatório consolidado com insights profundos"""

        print("\n" + "=" * 80)
        print("📊 RELATÓRIO CONSOLIDADO DE ANÁLISE TEÓRICA")
        print("=" * 80)

        print(f"\n📝 Roteiro: {screenplay_name}")
        print(f"📚 Teorias analisadas: {len(insights)}")

        # Média de aderência
        avg_adherence = sum(i.adherence_score for i in insights) / len(insights)
        print(f"\n📈 ADERÊNCIA MÉDIA: {avg_adherence:.1%}")

        # Ranking de teorias
        sorted_insights = sorted(insights, key=lambda x: x.adherence_score, reverse=True)

        print("\n🏆 RANKING DE ADERÊNCIA:")
        for i, insight in enumerate(sorted_insights, 1):
            print(f"  {i}. {insight.theory_name}: {insight.adherence_score:.1%}")

        # Padrões encontrados
        print("\n🔍 PADRÕES IDENTIFICADOS:")

        # Coletar todas as forças e fraquezas
        all_strengths = []
        all_weaknesses = []

        for insight in insights:
            if insight.strengths[0] != "Análise não disponível":
                all_strengths.extend(insight.strengths)
                all_weaknesses.extend(insight.weaknesses)

        # Encontrar padrões comuns
        from collections import Counter

        if all_strengths:
            strength_patterns = Counter(all_strengths).most_common(3)
            print("\n✅ Forças Recorrentes:")
            for strength, count in strength_patterns:
                if count > 1:
                    print(f"  • {strength} (mencionado {count}x)")

        if all_weaknesses:
            weakness_patterns = Counter(all_weaknesses).most_common(3)
            print("\n❌ Fraquezas Recorrentes:")
            for weakness, count in weakness_patterns:
                if count > 1:
                    print(f"  • {weakness} (mencionado {count}x)")

        # Recomendações prioritárias
        print("\n💡 RECOMENDAÇÕES PRIORITÁRIAS:")

        # Coletar todas as recomendações
        all_recommendations = []
        for insight in insights:
            if insight.recommendations[0] != "Análise não disponível":
                all_recommendations.extend(insight.recommendations)

        # Top 5 recomendações únicas
        unique_recommendations = list(set(all_recommendations))[:5]
        for i, rec in enumerate(unique_recommendations, 1):
            print(f"  {i}. {rec}")

        # Categoria final
        print("\n🎯 DIAGNÓSTICO FINAL:")

        if avg_adherence >= 0.8:
            category = "ROTEIRO MADURO"
            diagnosis = "Alto domínio das teorias clássicas. Pronto para polimento final."
        elif avg_adherence >= 0.6:
            category = "ROTEIRO PROMISSOR"
            diagnosis = "Boa base teórica, mas precisa fortalecer elementos específicos."
        elif avg_adherence >= 0.4:
            category = "ROTEIRO EM DESENVOLVIMENTO"
            diagnosis = "Necessita trabalho estrutural significativo."
        else:
            category = "ROTEIRO EXPERIMENTAL"
            diagnosis = "Abordagem não-convencional ou necessita reestruturação profunda."

        print(f"  Categoria: {category}")
        print(f"  {diagnosis}")

        # Salvar relatório
        output_file = Path(f"deep_analysis_{screenplay_name}_{datetime.now().strftime('%Y%m%d_%H%M')}.json")

        report_data = {
            "screenplay": screenplay_name,
            "timestamp": datetime.now().isoformat(),
            "average_adherence": avg_adherence,
            "category": category,
            "diagnosis": diagnosis,
            "insights": [
                {
                    "theory": i.theory_name,
                    "adherence": i.adherence_score,
                    "strengths": i.strengths,
                    "weaknesses": i.weaknesses,
                    "examples": i.specific_examples,
                    "recommendations": i.recommendations
                }
                for i in insights
            ]
        }

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, ensure_ascii=False, indent=2)

        print(f"\n💾 Relatório salvo: {output_file}")
        print("=" * 80)

    def batch_deep_analysis(self):
        """Analisa todos os roteiros disponíveis contra todas as teorias"""

        print("🚀 INICIANDO ANÁLISE PROFUNDA EM LOTE")
        print(f"📚 {len(self.theories)} teorias para análise")

        # Coletar roteiros
        all_screenplays = []

        if self.my_screenplays_dir.exists():
            all_screenplays.extend(list(self.my_screenplays_dir.glob("*.txt"))[:3])

        if self.screenplays_dir.exists():
            all_screenplays.extend(list(self.screenplays_dir.glob("*.txt"))[:2])

        print(f"📝 {len(all_screenplays)} roteiros para analisar")

        # Analisar cada roteiro
        for screenplay in all_screenplays:
            insights = self.deep_analysis(screenplay, self.theories[:5])  # Top 5 teorias
            time.sleep(5)  # Pausa entre roteiros

        print("\n✅ ANÁLISE PROFUNDA COMPLETA!")

if __name__ == "__main__":
    analyzer = DeepTheoryAnalyzer()

    # Verificar Ollama
    try:
        response = requests.get("http://127.0.0.1:11434/api/tags", timeout=2)
        if response.status_code == 200:
            print("✅ Ollama conectado")
    except:
        print("❌ Ollama não disponível")
        sys.exit(1)

    # Analisar Sonhos Sem Lembranças primeiro
    sonhos = Path("my_screenplays/sonhos_sem_lembrancas_t3.txt")

    if sonhos.exists():
        # Análise profunda com top 5 teorias
        analyzer.deep_analysis(sonhos, analyzer.theories[:5])
    else:
        # Analisar em lote
        analyzer.batch_deep_analysis()