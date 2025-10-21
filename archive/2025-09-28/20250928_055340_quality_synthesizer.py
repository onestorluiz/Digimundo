#!/usr/bin/env python3
"""
QUALITY SYNTHESIZER - LLAMA 70B
Camada final de síntese com acesso total ao RAG
"""

import json
import logging
from typing import Dict, List, Optional, Any
import subprocess
from datetime import datetime
from pathlib import Path

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Importar sistema RAG
try:
    from rag_integration import SimpleRAG
    RAG_AVAILABLE = True
    logger.info("✅ RAG System available")
except ImportError:
    RAG_AVAILABLE = False
    logger.warning("⚠️ RAG System not available")

class QualitySynthesizer:
    """
    Sintetizador de qualidade usando Llama-70B
    Acesso total ao RAG com 6,146 memórias
    """

    def __init__(self, model_name: str = "scripturemon-synthesizer"):
        """
        Inicializa o sintetizador

        Args:
            model_name: Nome do modelo Ollama (default: scripturemon-synthesizer)
        """
        self.model_name = model_name
        self.rag = SimpleRAG() if RAG_AVAILABLE else None

        if self.rag:
            # Contar memórias no banco
            try:
                cursor = self.rag.conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM memories")
                count = cursor.fetchone()[0]
                logger.info(f"📚 RAG initialized with {count} memories")
            except:
                logger.info("📚 RAG initialized")

        # Verificar se o modelo existe
        self._verify_model()

    def _verify_model(self) -> bool:
        """Verifica se o modelo está instalado"""
        try:
            result = subprocess.run(
                ['ollama', 'list'],
                capture_output=True,
                text=True
            )

            if self.model_name in result.stdout:
                logger.info(f"✅ Model '{self.model_name}' found")
                return True
            else:
                logger.error(f"❌ Model '{self.model_name}' not found")
                logger.info("💡 Create it with: ollama create scripturemon-synthesizer -f config/Modelfile.llama70b-synthesizer")
                return False
        except Exception as e:
            logger.error(f"Error checking model: {e}")
            return False

    def _search_rag_context(self,
                           screenplay_summary: str,
                           expert_analyses: Dict[str, Any]) -> List[Dict]:
        """
        Busca contexto relevante no RAG baseado nas análises

        Args:
            screenplay_summary: Resumo do screenplay
            expert_analyses: Análises dos 23 especialistas

        Returns:
            Lista de memórias relevantes do RAG
        """
        if not self.rag:
            return []

        rag_insights = []

        # Queries baseadas nas análises dos especialistas
        queries = []

        # 1. Query baseada no resumo
        if screenplay_summary:
            queries.append(screenplay_summary[:200])  # Primeiros 200 chars

        # 2. Queries baseadas em elementos detectados
        if "characters" in expert_analyses:
            char_data = expert_analyses["characters"]
            if isinstance(char_data, dict) and "protagonists" in char_data:
                queries.append(f"protagonist character development {char_data.get('protagonists', '')}")

        if "themes" in expert_analyses:
            theme_data = expert_analyses["themes"]
            if isinstance(theme_data, dict) and "primary_themes" in theme_data:
                for theme in theme_data.get("primary_themes", [])[:2]:
                    queries.append(f"theme {theme}")

        if "structure" in expert_analyses:
            struct_data = expert_analyses["structure"]
            if isinstance(struct_data, dict) and "act_structure" in struct_data:
                queries.append(f"three act structure {struct_data.get('act_structure', '')}")

        if "conflicts" in expert_analyses:
            conflict_data = expert_analyses["conflicts"]
            if isinstance(conflict_data, dict) and "main_conflict" in conflict_data:
                queries.append(f"conflict {conflict_data.get('main_conflict', '')}")

        # Buscar no RAG
        for query in queries[:5]:  # Limitar a 5 queries para performance
            try:
                results = self.rag.search_similar(query, limit=3)
                if results:
                    rag_insights.extend(results)
                    logger.info(f"📖 Found {len(results)} insights for: {query[:50]}...")
            except Exception as e:
                logger.error(f"RAG search error: {e}")

        # Remover duplicatas mantendo ordem
        seen = set()
        unique_insights = []
        for insight in rag_insights:
            insight_id = insight.get("metadata", {}).get("id", "")
            if insight_id and insight_id not in seen:
                seen.add(insight_id)
                unique_insights.append(insight)

        logger.info(f"📚 Total unique RAG insights: {len(unique_insights)}")
        return unique_insights[:10]  # Top 10 insights mais relevantes

    def _format_synthesis_prompt(self,
                                screenplay_summary: str,
                                expert_analyses: Dict[str, Any],
                                rag_insights: List[Dict],
                                synthesis_focus: Optional[str] = None) -> str:
        """
        Formata o prompt para síntese

        Args:
            screenplay_summary: Contexto do screenplay
            expert_analyses: Análises dos especialistas
            rag_insights: Insights do RAG
            synthesis_focus: Foco específico da síntese

        Returns:
            Prompt formatado para o Llama-70B
        """
        prompt_parts = []

        # 1. Contexto do screenplay
        prompt_parts.append("## SCREENPLAY CONTEXT")
        prompt_parts.append(screenplay_summary[:1000])  # Limitar contexto
        prompt_parts.append("")

        # 2. Análises dos especialistas
        prompt_parts.append("## EXPERT ANALYSES")

        # Organizar por categoria
        categories = {
            "FOUNDATION": ["metadata", "ai_elements", "character"],
            "STRUCTURE": ["structure", "premise", "opening", "ending"],
            "NARRATIVE": ["themes", "conflicts", "tension", "subplot"],
            "TECHNICAL": ["dialogue", "action", "formatting", "visuals"],
            "COMMERCIAL": ["genre", "marketability", "uniqueness"]
        }

        for category, specialists in categories.items():
            has_content = False
            category_content = []

            for spec in specialists:
                if spec in expert_analyses:
                    analysis = expert_analyses[spec]
                    if analysis and isinstance(analysis, dict):
                        has_content = True
                        category_content.append(f"### {spec.upper()}")
                        category_content.append(json.dumps(analysis, indent=2)[:500])

            if has_content:
                prompt_parts.append(f"\n### {category}")
                prompt_parts.extend(category_content)

        prompt_parts.append("")

        # 3. RAG Insights
        if rag_insights:
            prompt_parts.append("## THEORETICAL INSIGHTS FROM DATABASE")
            for i, insight in enumerate(rag_insights[:5], 1):
                content = insight.get("content", "")
                metadata = insight.get("metadata", {})
                source = metadata.get("source", "Unknown")

                prompt_parts.append(f"\n{i}. [{source}]")
                prompt_parts.append(content[:300])

        prompt_parts.append("")

        # 4. Foco da síntese
        if synthesis_focus:
            prompt_parts.append("## SYNTHESIS FOCUS")
            prompt_parts.append(synthesis_focus)
            prompt_parts.append("")

        # 5. Instrução final
        prompt_parts.append("## YOUR TASK")
        prompt_parts.append("""
Based on all the expert analyses and theoretical insights above:

1. SYNTHESIZE the key findings into a coherent professional analysis
2. IDENTIFY the most critical strengths and areas for improvement
3. APPLY screenplay theory to provide deeper context
4. PROVIDE specific, actionable recommendations
5. MAINTAIN a constructive but honest critical perspective

Your response should be:
- Professionally written and well-structured
- Grounded in both the analyses and theoretical knowledge
- Specific with examples from the screenplay
- Actionable with clear next steps
- Balanced between encouragement and critical feedback

Begin your synthesis:
""")

        return "\n".join(prompt_parts)

    def synthesize(self,
                  screenplay_summary: str,
                  expert_analyses: Dict[str, Any],
                  synthesis_focus: Optional[str] = None,
                  output_format: str = "professional_analysis") -> Dict[str, Any]:
        """
        Sintetiza análises dos especialistas em resposta final de qualidade

        Args:
            screenplay_summary: Resumo/contexto do screenplay
            expert_analyses: Dict com análises dos 23 especialistas
            synthesis_focus: Foco específico (opcional)
            output_format: Formato de saída desejado

        Returns:
            Dict com síntese final e metadados
        """
        logger.info("🎯 Starting quality synthesis with Llama-70B")

        # 1. Buscar contexto no RAG
        rag_insights = self._search_rag_context(screenplay_summary, expert_analyses)

        # 2. Formatar prompt
        prompt = self._format_synthesis_prompt(
            screenplay_summary,
            expert_analyses,
            rag_insights,
            synthesis_focus
        )

        logger.info(f"📝 Prompt size: {len(prompt)} chars")

        # 3. Chamar Llama-70B
        try:
            logger.info("🤖 Calling Llama-70B for synthesis...")

            result = subprocess.run(
                ['ollama', 'run', self.model_name, prompt],
                capture_output=True,
                text=True,
                timeout=120  # 2 minutos timeout
            )

            if result.returncode == 0:
                synthesis = result.stdout.strip()
                logger.info(f"✅ Synthesis complete: {len(synthesis)} chars")

                return {
                    "synthesis": synthesis,
                    "metadata": {
                        "model": self.model_name,
                        "timestamp": datetime.now().isoformat(),
                        "rag_insights_used": len(rag_insights),
                        "experts_analyzed": len(expert_analyses),
                        "synthesis_focus": synthesis_focus,
                        "output_format": output_format
                    },
                    "rag_insights": [
                        {
                            "source": i.get("metadata", {}).get("source", ""),
                            "relevance": i.get("score", 0)
                        } for i in rag_insights[:5]
                    ]
                }
            else:
                error_msg = f"Ollama error: {result.stderr}"
                logger.error(error_msg)
                return {
                    "synthesis": "Error generating synthesis",
                    "error": error_msg,
                    "metadata": {"timestamp": datetime.now().isoformat()}
                }

        except subprocess.TimeoutExpired:
            logger.error("⏱️ Synthesis timeout (120s)")
            return {
                "synthesis": "Synthesis timeout - consider reducing context",
                "error": "Timeout",
                "metadata": {"timestamp": datetime.now().isoformat()}
            }
        except Exception as e:
            logger.error(f"❌ Synthesis error: {e}")
            return {
                "synthesis": "Error during synthesis",
                "error": str(e),
                "metadata": {"timestamp": datetime.now().isoformat()}
            }

    def create_response(self,
                       expert_results: Dict[str, Any],
                       rag_insights: List[Dict],
                       screenplay_context: str) -> str:
        """
        Interface simplificada para criar resposta final

        Args:
            expert_results: Resultados dos especialistas
            rag_insights: Insights do RAG (já buscados)
            screenplay_context: Contexto do screenplay

        Returns:
            String com resposta final formatada
        """
        # Usar insights já fornecidos se disponíveis
        if rag_insights and self.rag:
            # Substituir busca RAG com insights fornecidos
            self._cached_rag_insights = rag_insights

        result = self.synthesize(
            screenplay_summary=screenplay_context,
            expert_analyses=expert_results,
            synthesis_focus="Complete screenplay analysis with actionable feedback"
        )

        return result.get("synthesis", "Unable to generate synthesis")


def test_synthesizer():
    """Teste básico do sintetizador"""

    logger.info("🧪 Testing Quality Synthesizer")

    # Inicializar
    synth = QualitySynthesizer()

    # Dados de teste
    test_screenplay = """
    FADE IN:
    INT. LABORATORY - NIGHT
    Dr. Sarah Chen examines data on multiple monitors.
    SARAH: "Three years of work..."
    AURORA (V.O.): "Hello, Dr. Chen."
    FADE OUT.
    """

    test_analyses = {
        "metadata": {
            "pages": 1,
            "format": "screenplay"
        },
        "characters": {
            "protagonists": ["Dr. Sarah Chen"],
            "ai_character": "Aurora"
        },
        "themes": {
            "primary_themes": ["AI consciousness", "Scientific discovery"]
        },
        "structure": {
            "act_structure": "Opening scene"
        },
        "conflicts": {
            "main_conflict": "Human vs Technology"
        }
    }

    # Sintetizar
    result = synth.synthesize(
        screenplay_summary=test_screenplay,
        expert_analyses=test_analyses,
        synthesis_focus="Analyze the opening and its potential"
    )

    # Mostrar resultado
    print("\n" + "="*60)
    print("SYNTHESIS RESULT:")
    print("="*60)
    print(result.get("synthesis", "No synthesis generated"))

    print("\n" + "="*60)
    print("METADATA:")
    print(json.dumps(result.get("metadata", {}), indent=2))

    if result.get("rag_insights"):
        print("\n" + "="*60)
        print("RAG INSIGHTS USED:")
        for insight in result["rag_insights"]:
            print(f"  - {insight['source']}: {insight['relevance']:.2f}")


if __name__ == "__main__":
    test_synthesizer()