"""
Formatted Exporter - Gera relatórios bem formatados do Dual-Core

Suporta múltiplos formatos:
1. TXT formatado (melhor legibilidade em qualquer editor)
2. HTML (formatação rica, pode abrir no browser)
3. PDF (via HTML, requer wkhtmltopdf)
"""

from typing import Dict, Any
from pathlib import Path
from datetime import datetime
import json


class FormattedExporter:
    """
    Exporta análise Dual-Core em formatos bem formatados.

    Formatos suportados:
    - TXT: Texto simples formatado com bordas e seções (MANTÉM CÓDIGOS)
    - HTML: Rich formatting com CSS, abre no browser (REMOVE CÓDIGOS)
    - PDF: Requer wkhtmltopdf (opcional)
    """

    def __init__(self, output_dir: Path = None):
        self.output_dir = output_dir or Path("workspace/outputs/formatted")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def _remove_rule_codes(text: str) -> str:
        """
        Remove códigos de regras (ex: DIAL.R003:) do texto para HTML.
        Mantém apenas a descrição legível.

        Exemplos:
        - "DIAL.R003: Lack of subtext" → "Lack of subtext"
        - "CHAR.R001: Flat character" → "Flat character"
        """
        import re
        # Pattern: XXX.RXXX: (qualquer código de especialista + regra)
        pattern = r'\b[A-Z]{3,4}\.R\d{3}:\s*'
        return re.sub(pattern, '', text)

    def export_txt(self, result: Dict[str, Any], screenplay_title: str = "Untitled") -> Path:
        """
        Exporta para TXT formatado com bordas e seções claras.

        Suporta Dual-Core e Triple-Core automaticamente.

        VANTAGEM: Abre em qualquer editor, legível, sem necessidade de HTML/PDF
        """
        # Detectar se é Triple-Core
        is_triple = result.get('triple_core', False) or 'python_core2' in result

        if is_triple:
            return self._export_triple_txt(result, screenplay_title)
        else:
            return self._export_dual_txt(result, screenplay_title)

    def _export_dual_txt(self, result: Dict[str, Any], screenplay_title: str = "Untitled") -> Path:
        """Exporta Dual-Core TXT (original)"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{screenplay_title.replace(' ', '_')}_{timestamp}.txt"
        filepath = self.output_dir / filename

        # Extrair dados
        python_analysis = result.get('python_analysis', {})
        llm_insights = result.get('llm_insights', 'N/A')
        synthesis = result.get('synthesis', {})
        specialist_name = result.get('specialist', 'Unknown')

        # Construir conteúdo formatado
        content = []

        # HEADER
        content.append("=" * 80)
        content.append("SCRIPTUREMON - ANÁLISE DUAL-CORE")
        content.append("=" * 80)
        content.append("")
        content.append(f"Roteiro: {screenplay_title}")
        content.append(f"Especialista: {specialist_name}")
        content.append(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        content.append(f"Modo: {'Deep Dive' if result.get('deep_context') else 'Shallow'}")
        content.append("")

        # PARTE 1: ANÁLISE PYTHON (OBJETIVA)
        content.append("=" * 80)
        content.append("PARTE 1: ANÁLISE PYTHON (DADOS OBJETIVOS)")
        content.append("=" * 80)
        content.append("")

        # Score principal
        if 'overall_score' in python_analysis:
            content.append(f"📊 SCORE GERAL: {python_analysis['overall_score']}/100")
            content.append("")

        # Regras violadas
        if 'rules_violated' in python_analysis:
            content.append("⚠️  REGRAS VIOLADAS:")
            violations = python_analysis['rules_violated']
            if isinstance(violations, list):
                for v in violations:
                    content.append(f"   • {v}")
            else:
                content.append(f"   {violations}")
            content.append("")

        # Recomendações
        if 'recommendations' in python_analysis:
            content.append("💡 RECOMENDAÇÕES PYTHON:")
            recommendations = python_analysis['recommendations']
            if isinstance(recommendations, list):
                for i, rec in enumerate(recommendations, 1):
                    content.append(f"   {i}. {rec}")
            else:
                content.append(f"   {recommendations}")
            content.append("")

        # Diagnóstico completo (se houver)
        if 'diagnosis' in python_analysis:
            content.append("📋 DIAGNÓSTICO DETALHADO:")
            content.append(f"   {python_analysis['diagnosis']}")
            content.append("")

        # Dados adicionais (JSON formatado)
        content.append("📈 DADOS TÉCNICOS (JSON):")
        content.append("-" * 80)
        content.append(json.dumps(python_analysis, indent=2, ensure_ascii=False))
        content.append("-" * 80)
        content.append("")

        # PARTE 2: INSIGHTS LLM (QUALITATIVOS)
        content.append("")
        content.append("=" * 80)
        content.append("PARTE 2: INSIGHTS LLM (ANÁLISE QUALITATIVA)")
        content.append("=" * 80)
        content.append("")

        if isinstance(llm_insights, dict) and 'error' in llm_insights:
            content.append(f"❌ ERRO: {llm_insights['error']}")
        else:
            # Formatar insights LLM com parágrafos
            insights_text = str(llm_insights)

            # Dividir em seções se houver headers numerados
            if any(s in insights_text for s in ['1. ', '2. ', '3. ', '4. ', '5.']):
                # Tem estrutura numerada
                for line in insights_text.split('\n'):
                    if line.strip():
                        # Headers de seção em destaque
                        if line.strip().startswith(('1.', '2.', '3.', '4.', '5.')):
                            content.append("")
                            content.append("─" * 80)
                            content.append(f"📖 {line.strip()}")
                            content.append("─" * 80)
                        else:
                            # Parágrafo normal com indentação
                            content.append(f"   {line.strip()}")
            else:
                # Sem estrutura: simplesmente quebrar em parágrafos
                paragraphs = insights_text.split('\n\n')
                for para in paragraphs:
                    if para.strip():
                        content.append(para.strip())
                        content.append("")

        content.append("")

        # PARTE 3: SYNTHESIS (COMBINAÇÃO)
        content.append("")
        content.append("=" * 80)
        content.append("PARTE 3: SÍNTESE (PYTHON + LLM)")
        content.append("=" * 80)
        content.append("")

        if synthesis:
            content.append("🎯 RESUMO EXECUTIVO:")
            content.append(f"   {synthesis.get('summary', 'N/A')}")
            content.append("")

            if 'quality_score' in synthesis:
                score = synthesis['quality_score']
                content.append(f"⭐ QUALITY SCORE: {score:.2f}/1.0")

                # Classificação visual
                if score >= 0.85:
                    content.append("   Classificação: 🌟 EXCELENTE")
                elif score >= 0.70:
                    content.append("   Classificação: ✅ MUITO BOM")
                elif score >= 0.50:
                    content.append("   Classificação: 👍 BOM")
                else:
                    content.append("   Classificação: ⚠️  PRECISA MELHORAR")
                content.append("")

            if 'combined_analysis' in synthesis:
                content.append("📊 ANÁLISE COMBINADA:")
                combined = synthesis['combined_analysis']
                for key, value in combined.items():
                    content.append(f"   • {key}: {value}")
                content.append("")

        # FOOTER
        content.append("")
        content.append("=" * 80)
        content.append("FIM DO RELATÓRIO")
        content.append("=" * 80)
        content.append("")
        content.append(f"Gerado por Scripturemon Dual-Core em {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")

        # Salvar
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write('\n'.join(content))

        return filepath

    def _export_triple_txt(self, result: Dict[str, Any], screenplay_title: str = "Untitled") -> Path:
        """Exporta Triple-Core TXT (3 cores + exemplos)"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{screenplay_title.replace(' ', '_')}_{timestamp}_TRIPLE.txt"
        filepath = self.output_dir / filename

        content = []

        # HEADER
        content.append("=" * 80)
        content.append("SCRIPTUREMON - ANÁLISE TRIPLE-CORE")
        content.append("=" * 80)
        content.append("")
        content.append(f"Roteiro: {screenplay_title}")
        content.append(f"Especialista: {result.get('specialist', 'Unknown')}")
        content.append(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        content.append(f"Arquitetura: 3 Cores (Python Base + Python Examples + LLM)")
        content.append("")

        # CORE 1: Python Base
        content.append("=" * 80)
        content.append("CORE 1: ANÁLISE PYTHON BASE")
        content.append("=" * 80)
        content.append("")

        core1 = result.get('python_core1', result.get('python_analysis', {}))
        if core1:
            # Formatação humanizada (como Dual-Core)
            if 'overall_score' in core1 or 'score' in core1:
                score = core1.get('overall_score', core1.get('score', 'N/A'))
                content.append(f"📊 SCORE GERAL: {score}/100")
                content.append("")

            if 'rules_violated' in core1:
                content.append("⚠️  REGRAS VIOLADAS:")
                violations = core1['rules_violated']
                if isinstance(violations, list):
                    for v in violations:
                        content.append(f"   • {v}")
                else:
                    content.append(f"   • {violations}")
                content.append("")

            if 'recommendations' in core1:
                content.append("💡 RECOMENDAÇÕES:")
                recs = core1['recommendations']
                if isinstance(recs, list):
                    for i, rec in enumerate(recs, 1):
                        content.append(f"   {i}. {rec}")
                else:
                    content.append(f"   {recs}")
                content.append("")

            if 'diagnosis' in core1:
                content.append("📋 DIAGNÓSTICO:")
                content.append(f"   {core1['diagnosis']}")
                content.append("")

            # JSON técnico separado
            content.append("📈 DADOS TÉCNICOS COMPLETOS:")
            content.append("-" * 80)
            content.append(json.dumps(core1, indent=2, ensure_ascii=False))
            content.append("-" * 80)
        content.append("")

        # CORE 2: Exemplos de Mestres
        content.append("=" * 80)
        content.append("CORE 2: EXEMPLOS DE ROTEIROS MESTRES")
        content.append("=" * 80)
        content.append("")

        core2 = result.get('python_core2', {})
        if core2:
            content.append(f"Exemplos encontrados: {core2.get('total_examples', 0)}")
            content.append(f"Roteiros pesquisados: {len(core2.get('master_screenplays_searched', []))}")
            content.append("")
            for ex in core2.get('examples_found', [])[:10]:
                content.append(f"  • {ex.get('screenplay')}: {ex.get('character')}")
                content.append(f"    Problema: {ex.get('problem_addressed')}")
                content.append(f"    Lição: {ex.get('lesson')}")
                content.append("")
        content.append("")

        # CORE 3: LLM
        content.append("=" * 80)
        content.append("CORE 3: INSIGHTS LLM")
        content.append("=" * 80)
        content.append("")
        content.append(str(result.get('llm_insights', 'N/A')))
        content.append("")

        # SÍNTESE
        content.append("=" * 80)
        content.append("SÍNTESE FINAL")
        content.append("=" * 80)
        content.append("")
        synthesis = result.get('synthesis', {})
        if synthesis:
            content.append(json.dumps(synthesis, indent=2, ensure_ascii=False))
        content.append("")

        # FOOTER
        content.append("=" * 80)
        content.append(f"Gerado por Scripturemon Triple-Core em {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")

        # Salvar
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write('\n'.join(content))

        return filepath

    def export_html(self, result: Dict[str, Any], screenplay_title: str = "Untitled") -> Path:
        """
        Exporta para HTML com CSS rico.

        Suporta Dual-Core e Triple-Core automaticamente.

        VANTAGEM: Formatação visual rica, cores, pode abrir no browser
        """
        # Detectar Triple-Core
        is_triple = result.get('triple_core', False) or 'python_core2' in result

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{screenplay_title.replace(' ', '_')}_{timestamp}.html"
        filepath = self.output_dir / filename

        # Extrair dados (compatível com Dual e Triple)
        if is_triple:
            python_analysis = result.get('python_core1', {})
            python_core2 = result.get('python_core2', {})
        else:
            python_analysis = result.get('python_analysis', {})
            python_core2 = None

        llm_insights = result.get('llm_insights', 'N/A')
        synthesis = result.get('synthesis', {})
        specialist_name = result.get('specialist', 'Unknown')

        # CSS moderno
        css = """
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
                line-height: 1.6;
                color: #333;
                background: #f5f5f5;
                padding: 20px;
            }
            .container {
                max-width: 1200px;
                margin: 0 auto;
                background: white;
                border-radius: 8px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                overflow: hidden;
            }
            .header {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 30px;
                text-align: center;
            }
            .header h1 { font-size: 2.5em; margin-bottom: 10px; }
            .header .meta { opacity: 0.9; font-size: 1.1em; }

            .section {
                padding: 30px;
                border-bottom: 1px solid #eee;
            }
            .section:last-child { border-bottom: none; }

            .section-title {
                font-size: 1.8em;
                color: #667eea;
                margin-bottom: 20px;
                padding-bottom: 10px;
                border-bottom: 3px solid #667eea;
            }

            .part-1 .section-title { color: #3b82f6; border-color: #3b82f6; }
            .part-2 .section-title { color: #10b981; border-color: #10b981; }
            .part-3 .section-title { color: #f59e0b; border-color: #f59e0b; }
            .part-4 .section-title { color: #ef4444; border-color: #ef4444; }

            .score-badge {
                display: inline-block;
                background: #667eea;
                color: white;
                padding: 10px 20px;
                border-radius: 20px;
                font-size: 1.2em;
                font-weight: bold;
                margin: 10px 0;
            }

            .score-excellent { background: #10b981; }
            .score-good { background: #3b82f6; }
            .score-warning { background: #f59e0b; }

            .list-item {
                background: #f9fafb;
                padding: 15px;
                margin: 10px 0;
                border-left: 4px solid #667eea;
                border-radius: 4px;
            }

            .insight-paragraph {
                background: #f0fdf4;
                padding: 20px;
                margin: 15px 0;
                border-radius: 8px;
                border-left: 4px solid #10b981;
            }

            .insight-header {
                font-weight: bold;
                color: #059669;
                margin-bottom: 10px;
                font-size: 1.1em;
            }

            .json-viewer {
                background: #1e293b;
                color: #e2e8f0;
                padding: 20px;
                border-radius: 8px;
                overflow-x: auto;
                font-family: 'Courier New', monospace;
                font-size: 0.9em;
            }

            .synthesis-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 20px;
                margin-top: 20px;
            }

            .synthesis-card {
                background: #f9fafb;
                padding: 20px;
                border-radius: 8px;
                border: 1px solid #e5e7eb;
            }

            .synthesis-card h3 {
                color: #667eea;
                margin-bottom: 10px;
            }

            .footer {
                text-align: center;
                padding: 20px;
                background: #f9fafb;
                color: #6b7280;
            }
        </style>
        """

        # HTML content
        html = f"""
        <!DOCTYPE html>
        <html lang="pt-BR">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Scripturemon - {screenplay_title}</title>
            {css}
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🎬 SCRIPTUREMON</h1>
                    <div class="meta">
                        <strong>{screenplay_title}</strong><br>
                        Especialista: {specialist_name} | {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
                    </div>
                </div>

                <!-- PARTE 1: PYTHON -->
                <div class="section part-1">
                    <h2 class="section-title">📊 PARTE 1: Análise Python (Dados Objetivos)</h2>
        """

        # Score
        if 'overall_score' in python_analysis:
            score = python_analysis['overall_score']
            html += f'<div class="score-badge">Score: {score}/100</div>'

        # Violations (REMOVE CÓDIGOS no HTML)
        if 'rules_violated' in python_analysis:
            html += '<h3 style="margin-top: 20px;">⚠️ Regras Violadas</h3>'
            violations = python_analysis['rules_violated']
            if isinstance(violations, list):
                for v in violations:
                    clean_v = self._remove_rule_codes(v)  # Remove DIAL.R003: etc
                    html += f'<div class="list-item">{clean_v}</div>'
            else:
                clean_v = self._remove_rule_codes(str(violations))
                html += f'<div class="list-item">{clean_v}</div>'

        # Recommendations
        if 'recommendations' in python_analysis:
            html += '<h3 style="margin-top: 20px;">💡 Recomendações</h3>'
            recommendations = python_analysis['recommendations']
            if isinstance(recommendations, list):
                for i, rec in enumerate(recommendations, 1):
                    html += f'<div class="list-item"><strong>{i}.</strong> {rec}</div>'
            else:
                html += f'<div class="list-item">{recommendations}</div>'

        # REMOVER JSON TÉCNICO DO HTML - mantém apenas no TXT
        # (Outras IAs trabalharão em cima do TXT, HTML é para visualização humana)

        html += '</div>'

        # PARTE 2: EXEMPLOS DE MESTRES (só Triple-Core)
        if is_triple and python_core2:
            html += """
                <div class="section part-2">
                    <h2 class="section-title">📚 PARTE 2: Exemplos de Roteiros Mestres</h2>
            """

            total = python_core2.get('total_examples', 0)
            html += f'<p><strong>Exemplos encontrados:</strong> {total}</p>'

            for i, ex in enumerate(python_core2.get('examples_found', [])[:10], 1):
                html += f'''
                <div class="list-item">
                    <strong>#{i}: {ex.get("screenplay")}</strong><br>
                    Personagem: {ex.get("character")}<br>
                    Problema: {ex.get("problem_addressed")}<br>
                    Lição: {ex.get("lesson")}
                </div>
                '''

            html += '</div>'

        # PARTE 2 ou 3: LLM (dependendo se tem Core 2)
        parte_num = 3 if is_triple else 2
        html += f"""
                <div class="section part-{parte_num}">
                    <h2 class="section-title">🤖 PARTE {parte_num}: Insights LLM (Análise Qualitativa)</h2>
        """

        if isinstance(llm_insights, dict) and 'error' in llm_insights:
            html += f'<div class="list-item" style="border-color: #ef4444;">❌ Erro: {llm_insights["error"]}</div>'
        else:
            insights_text = str(llm_insights)

            # Detectar seções numeradas
            if any(s in insights_text for s in ['1. ', '2. ', '3. ', '4. ', '5.']):
                current_section = []
                for line in insights_text.split('\n'):
                    line = line.strip()
                    if line:
                        if line.startswith(('1.', '2.', '3.', '4.', '5.')):
                            # Salvar seção anterior
                            if current_section:
                                html += f'<div class="insight-paragraph">{"<br>".join(current_section)}</div>'
                            # Começar nova seção
                            current_section = [f'<div class="insight-header">{line}</div>']
                        else:
                            current_section.append(line)

                # Salvar última seção
                if current_section:
                    html += f'<div class="insight-paragraph">{"<br>".join(current_section)}</div>'
            else:
                # Sem estrutura: parágrafos simples
                paragraphs = insights_text.split('\n\n')
                for para in paragraphs:
                    if para.strip():
                        html += f'<div class="insight-paragraph">{para.strip().replace(chr(10), "<br>")}</div>'

        html += '</div>'

        # PARTE 3 ou 4: SYNTHESIS (dependendo se tem Core 2)
        synthesis_num = 4 if is_triple else 3
        html += f"""
                <div class="section part-{synthesis_num}">
                    <h2 class="section-title">🎯 PARTE {synthesis_num}: Síntese (Python + LLM)</h2>
        """

        if synthesis:
            # Quality score visual
            if 'quality_score' in synthesis:
                score = synthesis['quality_score']
                score_class = 'score-excellent' if score >= 0.85 else 'score-good' if score >= 0.70 else 'score-warning'
                classification = '🌟 EXCELENTE' if score >= 0.85 else '✅ MUITO BOM' if score >= 0.70 else '👍 BOM' if score >= 0.50 else '⚠️ PRECISA MELHORAR'

                html += f'<div class="score-badge {score_class}">Quality Score: {score:.2f}/1.0 - {classification}</div>'

            # Grid de cards
            html += '<div class="synthesis-grid">'

            # Summary card
            if 'summary' in synthesis:
                html += f"""
                <div class="synthesis-card">
                    <h3>📝 Resumo</h3>
                    <p>{synthesis['summary']}</p>
                </div>
                """

            # Combined analysis cards
            if 'combined_analysis' in synthesis:
                combined = synthesis['combined_analysis']
                for key, value in combined.items():
                    html += f"""
                    <div class="synthesis-card">
                        <h3>📊 {key.replace('_', ' ').title()}</h3>
                        <p>{value}</p>
                    </div>
                    """

            html += '</div>'

        html += '</div>'

        # FOOTER
        html += f"""
                <div class="footer">
                    Gerado por Scripturemon Dual-Core em {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
                </div>
            </div>
        </body>
        </html>
        """

        # Salvar
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)

        return filepath


# Função helper para uso rápido
def export_analysis(result: Dict[str, Any], screenplay_title: str = "Untitled", format: str = "txt") -> Path:
    """
    Export helper function.

    Args:
        result: Resultado do DualCoreWrapper.analyze()
        screenplay_title: Título do roteiro
        format: 'txt' ou 'html'

    Returns:
        Path do arquivo gerado
    """
    exporter = FormattedExporter()

    if format.lower() == 'html':
        return exporter.export_html(result, screenplay_title)
    else:
        return exporter.export_txt(result, screenplay_title)
