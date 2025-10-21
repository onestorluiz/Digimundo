#!/usr/bin/env python3
"""
Executive Summary Generator - Triple-Core Version

Gera relatório executivo completo baseado em resultados Triple-Core.
"""

from typing import Dict, List, Any
from datetime import datetime
from dataclasses import dataclass


@dataclass
class ExecutiveSummary:
    """Sumário executivo completo."""
    title: str
    generated_at: str
    screenplay_stats: Dict[str, Any]

    # Overall
    overall_score: float
    quality_level: str

    # Dimensões
    dimension_scores: Dict[str, float]

    # Top insights
    standout_elements: List[str]
    critical_issues: List[str]
    priority_recommendations: List[str]

    # Detalhes por especialista
    specialist_summaries: List[Dict[str, Any]]

    # Formatted report
    html_report: str
    markdown_report: str


class ExecutiveSummaryGenerator:
    """Gerador de relatório executivo Triple-Core."""

    def __init__(self):
        self.name = "Executive Summary Generator"

    def generate(
        self,
        screenplay_title: str,
        screenplay_stats: Dict[str, Any],
        overall_quality_result: Any,  # OverallQualityResult
        specialist_results: Dict[str, Dict[str, Any]]
    ) -> ExecutiveSummary:
        """
        Gera sumário executivo completo.

        Args:
            screenplay_title: Título do screenplay
            screenplay_stats: Stats (páginas, cenas, palavras, etc)
            overall_quality_result: Resultado do OverallQualityAggregator
            specialist_results: Resultados de todos os especialistas

        Returns:
            ExecutiveSummary com relatórios formatados
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Preparar dimension scores
        dimension_scores = {
            'Narrative': overall_quality_result.narrative_score,
            'Character': overall_quality_result.character_score,
            'Dialogue': overall_quality_result.dialogue_score,
            'Technical': overall_quality_result.technical_score,
            'Depth': overall_quality_result.depth_score,
            'Craft': overall_quality_result.craft_score,
            'Market': overall_quality_result.market_score,
        }

        # Preparar specialist summaries
        specialist_summaries = self._prepare_specialist_summaries(specialist_results)

        # Gerar relatórios formatados
        html_report = self._generate_html_report(
            screenplay_title, timestamp, screenplay_stats,
            overall_quality_result, dimension_scores, specialist_summaries
        )

        markdown_report = self._generate_markdown_report(
            screenplay_title, timestamp, screenplay_stats,
            overall_quality_result, dimension_scores, specialist_summaries
        )

        return ExecutiveSummary(
            title=screenplay_title,
            generated_at=timestamp,
            screenplay_stats=screenplay_stats,
            overall_score=overall_quality_result.overall_score,
            quality_level=overall_quality_result.quality_level,
            dimension_scores=dimension_scores,
            standout_elements=overall_quality_result.standout_elements,
            critical_issues=overall_quality_result.critical_issues,
            priority_recommendations=overall_quality_result.recommendations,
            specialist_summaries=specialist_summaries,
            html_report=html_report,
            markdown_report=markdown_report
        )

    def _prepare_specialist_summaries(
        self, specialist_results: Dict[str, Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Prepara sumários dos especialistas ordenados por score."""
        summaries = []

        for name, result in specialist_results.items():
            summaries.append({
                'name': name,
                'score': result.get('score', 0),
                'recommendations_count': len(result.get('recommendations', [])),
                'top_recommendation': result.get('recommendations', ['N/A'])[0] if result.get('recommendations') else 'N/A',
                'status': self._get_status_emoji(result.get('score', 0))
            })

        # Sort by score (highest first)
        summaries.sort(key=lambda x: x['score'], reverse=True)

        return summaries

    def _get_status_emoji(self, score: float) -> str:
        """Retorna emoji baseado no score."""
        if score >= 90:
            return "🌟"
        elif score >= 80:
            return "✅"
        elif score >= 70:
            return "👍"
        elif score >= 60:
            return "⚠️"
        elif score >= 50:
            return "❌"
        else:
            return "🚨"

    def _generate_html_report(
        self,
        title: str,
        timestamp: str,
        stats: Dict[str, Any],
        overall: Any,
        dimensions: Dict[str, float],
        specialists: List[Dict[str, Any]]
    ) -> str:
        """Gera relatório HTML."""
        quality_color = self._get_quality_color(overall.overall_score)

        html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Script Doctor™ Analysis - {title}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background: #f5f5f5;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
        }}
        .header h1 {{
            margin: 0 0 10px 0;
        }}
        .header p {{
            margin: 5px 0;
            opacity: 0.9;
        }}
        .overall-score {{
            background: white;
            padding: 30px;
            border-radius: 10px;
            text-align: center;
            margin-bottom: 30px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .score-circle {{
            width: 200px;
            height: 200px;
            border-radius: 50%;
            background: conic-gradient({quality_color} {overall.overall_score * 3.6}deg, #e0e0e0 0deg);
            margin: 20px auto;
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        .score-inner {{
            width: 160px;
            height: 160px;
            border-radius: 50%;
            background: white;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }}
        .score-value {{
            font-size: 48px;
            font-weight: bold;
            color: {quality_color};
        }}
        .score-level {{
            font-size: 18px;
            color: #666;
            text-transform: uppercase;
            margin-top: 5px;
        }}
        .dimensions {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .dimension {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .dimension h3 {{
            margin: 0 0 10px 0;
            color: #333;
        }}
        .dimension-bar {{
            height: 10px;
            background: #e0e0e0;
            border-radius: 5px;
            overflow: hidden;
        }}
        .dimension-fill {{
            height: 100%;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            transition: width 0.3s ease;
        }}
        .dimension-score {{
            font-size: 24px;
            font-weight: bold;
            color: #667eea;
            margin-top: 10px;
        }}
        .section {{
            background: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .section h2 {{
            margin-top: 0;
            color: #333;
            border-bottom: 2px solid #667eea;
            padding-bottom: 10px;
        }}
        .specialist-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 15px;
        }}
        .specialist-card {{
            border: 1px solid #e0e0e0;
            padding: 15px;
            border-radius: 5px;
        }}
        .specialist-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
        }}
        .specialist-name {{
            font-weight: bold;
            color: #333;
        }}
        .specialist-score {{
            font-size: 20px;
            font-weight: bold;
        }}
        ul {{
            padding-left: 20px;
        }}
        li {{
            margin: 10px 0;
        }}
        .footer {{
            text-align: center;
            color: #999;
            margin-top: 30px;
            padding: 20px;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🎬 Script Doctor™ Triple-Core Analysis</h1>
        <p><strong>{title}</strong></p>
        <p>Generated: {timestamp}</p>
        <p>Pages: {stats.get('pages', 'N/A')} | Scenes: {stats.get('scenes', 'N/A')} | Words: {stats.get('words', 'N/A'):,}</p>
    </div>

    <div class="overall-score">
        <h2>Overall Quality Assessment</h2>
        <div class="score-circle">
            <div class="score-inner">
                <div class="score-value">{overall.overall_score:.0f}</div>
                <div class="score-level">{overall.quality_level}</div>
            </div>
        </div>
    </div>

    <div class="dimensions">
"""

        # Add dimension cards
        for dim_name, dim_score in dimensions.items():
            dim_color = self._get_quality_color(dim_score)
            html += f"""        <div class="dimension">
            <h3>{dim_name}</h3>
            <div class="dimension-bar">
                <div class="dimension-fill" style="width: {dim_score}%;"></div>
            </div>
            <div class="dimension-score" style="color: {dim_color};">{dim_score:.1f}/100</div>
        </div>
"""

        html += """    </div>

    <div class="section">
        <h2>✨ Standout Elements</h2>
        <ul>
"""

        for elem in overall.standout_elements[:10]:
            html += f"            <li>{elem}</li>\n"

        html += """        </ul>
    </div>
"""

        if overall.critical_issues:
            html += """    <div class="section">
        <h2>🚨 Critical Issues</h2>
        <ul>
"""
            for issue in overall.critical_issues[:10]:
                html += f"            <li>{issue}</li>\n"

            html += """        </ul>
    </div>
"""

        html += """    <div class="section">
        <h2>💡 Priority Recommendations</h2>
        <ul>
"""

        for rec in overall.recommendations[:10]:
            html += f"            <li>{rec}</li>\n"

        html += """        </ul>
    </div>

    <div class="section">
        <h2>📊 Specialist Analysis Details</h2>
        <div class="specialist-grid">
"""

        for spec in specialists:
            score_color = self._get_quality_color(spec['score'])
            html += f"""            <div class="specialist-card">
                <div class="specialist-header">
                    <span class="specialist-name">{spec['status']} {spec['name']}</span>
                    <span class="specialist-score" style="color: {score_color};">{spec['score']}</span>
                </div>
                <p style="font-size: 12px; color: #666;">{spec['recommendations_count']} recommendations</p>
            </div>
"""

        html += """        </div>
    </div>

    <div class="footer">
        <p>🤖 Generated by <strong>Script Doctor™ Triple-Core</strong></p>
        <p>Powered by McKee Principles, Field Paradigm, Truby 22 Steps, and 13+ Master Theories</p>
    </div>
</body>
</html>
"""

        return html

    def _generate_markdown_report(
        self,
        title: str,
        timestamp: str,
        stats: Dict[str, Any],
        overall: Any,
        dimensions: Dict[str, float],
        specialists: List[Dict[str, Any]]
    ) -> str:
        """Gera relatório Markdown."""
        md = f"""# 🎬 Script Doctor™ Triple-Core Analysis

## {title}

**Generated:** {timestamp}
**Stats:** {stats.get('pages', 'N/A')} pages | {stats.get('scenes', 'N/A')} scenes | {stats.get('words', 'N/A'):,} words

---

## 📊 Overall Quality Assessment

**Score:** {overall.overall_score:.1f}/100
**Level:** {overall.quality_level.upper()}

---

## 🎯 Quality Dimensions

"""

        for dim_name, dim_score in dimensions.items():
            bar_filled = int(dim_score / 5)
            bar_empty = 20 - bar_filled
            bar = "█" * bar_filled + "░" * bar_empty
            md += f"**{dim_name}:** {dim_score:.1f}/100  \n`{bar}`\n\n"

        md += "\n---\n\n## ✨ Standout Elements\n\n"

        for elem in overall.standout_elements[:10]:
            md += f"- {elem}\n"

        if overall.critical_issues:
            md += "\n---\n\n## 🚨 Critical Issues\n\n"
            for issue in overall.critical_issues[:10]:
                md += f"- {issue}\n"

        md += "\n---\n\n## 💡 Priority Recommendations\n\n"

        for i, rec in enumerate(overall.recommendations[:10], 1):
            md += f"{i}. {rec}\n"

        md += "\n---\n\n## 📋 Specialist Analysis Summary\n\n"
        md += "| Specialist | Score | Recommendations |\n"
        md += "|-----------|-------|----------------|\n"

        for spec in specialists:
            md += f"| {spec['status']} {spec['name']} | {spec['score']}/100 | {spec['recommendations_count']} |\n"

        md += "\n---\n\n"
        md += "🤖 **Generated by Script Doctor™ Triple-Core**  \n"
        md += "Powered by McKee Principles, Field Paradigm, Truby 22 Steps, and 13+ Master Theories\n"

        return md

    def _get_quality_color(self, score: float) -> str:
        """Retorna cor baseada no score."""
        if score >= 90:
            return "#00C853"  # Green
        elif score >= 80:
            return "#64DD17"  # Light Green
        elif score >= 70:
            return "#FFC107"  # Amber
        elif score >= 60:
            return "#FF9800"  # Orange
        elif score >= 50:
            return "#FF5722"  # Deep Orange
        else:
            return "#F44336"  # Red
