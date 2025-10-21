#!/usr/bin/env python3
"""
Gera HTML detalhado com todos os 22 especialistas expandidos
"""

import json
from pathlib import Path
from triple_core.orchestrators.screenplay_analyzer import ScreenplayAnalyzer

def generate_detailed_html(screenplay_path: str, output_path: str):
    """Gera HTML com detalhes completos dos 22 especialistas"""

    print("🎬 Iniciando análise completa para HTML detalhado...")
    print()

    # Run analysis
    analyzer = ScreenplayAnalyzer(llm_model="scripturemon-optimized", deep_context=False)

    # Get screenplay name
    screenplay_name = Path(screenplay_path).stem

    # Analyze
    html_path, md_path, specialist_results = analyzer.analyze_screenplay(
        screenplay_path,
        output_dir="workspace/outputs/analysis"
    )

    print()
    print("=" * 80)
    print("📊 GERANDO HTML DETALHADO")
    print("=" * 80)
    print()

    # Build detailed HTML
    html_content = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Script Doctor™ - Análise Completa Detalhada - {screenplay_name}</title>
    <style>
        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            line-height: 1.6;
        }}

        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }}

        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}

        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}

        .header .subtitle {{
            font-size: 1.2em;
            opacity: 0.9;
        }}

        .content {{
            padding: 40px;
        }}

        .specialist {{
            margin-bottom: 30px;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            overflow: hidden;
            transition: all 0.3s ease;
        }}

        .specialist:hover {{
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            border-color: #667eea;
        }}

        .specialist-header {{
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            padding: 20px;
            cursor: pointer;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}

        .specialist-header:hover {{
            background: linear-gradient(135deg, #e0e7ff 0%, #c3cfe2 100%);
        }}

        .specialist-title {{
            font-size: 1.3em;
            font-weight: bold;
            color: #333;
        }}

        .specialist-score {{
            font-size: 2em;
            font-weight: bold;
            padding: 10px 20px;
            border-radius: 10px;
            color: white;
        }}

        .score-excellent {{ background: linear-gradient(135deg, #00C853 0%, #64DD17 100%); }}
        .score-good {{ background: linear-gradient(135deg, #FFC107 0%, #FF9800 100%); }}
        .score-needs-work {{ background: linear-gradient(135deg, #FF5722 0%, #F44336 100%); }}
        .score-critical {{ background: linear-gradient(135deg, #D32F2F 0%, #B71C1C 100%); }}

        .specialist-body {{
            padding: 30px;
            display: none;
            background: white;
        }}

        .specialist.expanded .specialist-body {{
            display: block;
        }}

        .specialist.expanded .specialist-header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }}

        .specialist.expanded .specialist-title {{
            color: white;
        }}

        .section {{
            margin-bottom: 25px;
        }}

        .section-title {{
            font-size: 1.1em;
            font-weight: bold;
            color: #667eea;
            margin-bottom: 10px;
            padding-bottom: 5px;
            border-bottom: 2px solid #667eea;
        }}

        .diagnosis {{
            background: #f5f7fa;
            padding: 20px;
            border-left: 4px solid #667eea;
            border-radius: 5px;
            font-style: italic;
        }}

        .recommendations {{
            list-style: none;
        }}

        .recommendations li {{
            padding: 10px;
            margin-bottom: 8px;
            background: #fff3e0;
            border-left: 4px solid #FF9800;
            border-radius: 5px;
        }}

        .recommendations li:before {{
            content: "💡 ";
            margin-right: 5px;
        }}

        .examples {{
            background: #e8f5e9;
            padding: 20px;
            border-radius: 5px;
            border-left: 4px solid #00C853;
        }}

        .example-item {{
            margin-bottom: 15px;
            padding-bottom: 15px;
            border-bottom: 1px solid #c8e6c9;
        }}

        .example-item:last-child {{
            border-bottom: none;
            margin-bottom: 0;
            padding-bottom: 0;
        }}

        .example-title {{
            font-weight: bold;
            color: #2e7d32;
            margin-bottom: 5px;
        }}

        .example-text {{
            font-family: 'Courier New', monospace;
            background: white;
            padding: 10px;
            border-radius: 3px;
            font-size: 0.9em;
        }}

        .toggle-all {{
            text-align: center;
            margin-bottom: 30px;
        }}

        .toggle-all button {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 15px 30px;
            font-size: 1em;
            border-radius: 10px;
            cursor: pointer;
            transition: all 0.3s ease;
        }}

        .toggle-all button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }}

        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}

        .stat-card {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
        }}

        .stat-value {{
            font-size: 2em;
            font-weight: bold;
            margin-bottom: 5px;
        }}

        .stat-label {{
            opacity: 0.9;
            font-size: 0.9em;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎬 Script Doctor™ Triple-Core</h1>
            <div class="subtitle">Análise Completa Detalhada - {screenplay_name}</div>
        </div>

        <div class="content">
            <div class="stats">
                <div class="stat-card">
                    <div class="stat-value">{len(specialist_results)}</div>
                    <div class="stat-label">Especialistas</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">3</div>
                    <div class="stat-label">Cores de Análise</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">13+</div>
                    <div class="stat-label">Teorias Mestres</div>
                </div>
            </div>

            <div class="toggle-all">
                <button onclick="toggleAll()">Expandir/Recolher Todos</button>
            </div>
"""

    # Add each specialist
    for name, result in specialist_results.items():
        score = result.get('score', 0)

        # Determine score class
        if score >= 80:
            score_class = "score-excellent"
        elif score >= 60:
            score_class = "score-good"
        elif score >= 40:
            score_class = "score-needs-work"
        else:
            score_class = "score-critical"

        html_content += f"""
            <div class="specialist">
                <div class="specialist-header" onclick="toggleSpecialist(this)">
                    <div class="specialist-title">📊 {name}</div>
                    <div class="specialist-score {score_class}">{score}/100</div>
                </div>
                <div class="specialist-body">
"""

        # Diagnosis
        diagnosis = result.get('diagnosis', 'N/A')
        html_content += f"""
                    <div class="section">
                        <div class="section-title">🔍 Diagnóstico</div>
                        <div class="diagnosis">{diagnosis}</div>
                    </div>
"""

        # Recommendations
        recommendations = result.get('recommendations', [])
        if recommendations:
            html_content += """
                    <div class="section">
                        <div class="section-title">💡 Recomendações</div>
                        <ul class="recommendations">
"""
            for rec in recommendations[:5]:  # Top 5 recommendations
                html_content += f"                            <li>{rec}</li>\n"

            html_content += """                        </ul>
                    </div>
"""

        # Examples
        examples = result.get('examples', [])
        if examples:
            html_content += """
                    <div class="section">
                        <div class="section-title">📚 Exemplos de Filmes Profissionais</div>
                        <div class="examples">
"""
            for example in examples[:3]:  # Top 3 examples
                movie = example.get('movie', 'N/A')
                excerpt = example.get('excerpt', 'N/A')
                explanation = example.get('explanation', 'N/A')

                html_content += f"""
                            <div class="example-item">
                                <div class="example-title">🎬 {movie}</div>
                                <div class="example-text">{excerpt}</div>
                                <div style="margin-top: 10px; color: #2e7d32;">{explanation}</div>
                            </div>
"""

            html_content += """                        </div>
                    </div>
"""

        # LLM Analysis
        llm_analysis = result.get('llm_analysis', '')
        if llm_analysis and llm_analysis != 'N/A':
            html_content += f"""
                    <div class="section">
                        <div class="section-title">🤖 Análise Profunda (LLM)</div>
                        <div style="background: #f5f7fa; padding: 15px; border-radius: 5px; white-space: pre-wrap;">{llm_analysis}</div>
                    </div>
"""

        html_content += """
                </div>
            </div>
"""

    # Close HTML
    html_content += """
        </div>
    </div>

    <script>
        function toggleSpecialist(header) {
            const specialist = header.parentElement;
            specialist.classList.toggle('expanded');
        }

        function toggleAll() {
            const specialists = document.querySelectorAll('.specialist');
            const anyExpanded = Array.from(specialists).some(s => s.classList.contains('expanded'));

            specialists.forEach(specialist => {
                if (anyExpanded) {
                    specialist.classList.remove('expanded');
                } else {
                    specialist.classList.add('expanded');
                }
            });
        }
    </script>
</body>
</html>
"""

    # Save HTML
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"✅ HTML detalhado gerado: {output_file}")
    print()

    return str(output_file)


if __name__ == "__main__":
    screenplay_path = "content/screenplays/personal/sonhos_sem_lembrancas_t3.txt"
    output_path = "workspace/outputs/analysis/DETAILED_ANALYSIS.html"

    result = generate_detailed_html(screenplay_path, output_path)

    print("=" * 80)
    print("✅ CONCLUÍDO!")
    print("=" * 80)
    print()
    print(f"Abra o arquivo: {result}")
