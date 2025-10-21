#!/usr/bin/env python3
"""
Gera relatórios HTML individuais para cada um dos 22 especialistas.
Usa os resultados da análise mais recente.
"""

import json
from pathlib import Path
from datetime import datetime

# Carregar resultados da última análise
latest_analysis = Path("workspace/outputs/analysis_corrected")
html_file = list(latest_analysis.glob("*.html"))[0]

print("="*80)
print("📝 GERANDO RELATÓRIOS INDIVIDUAIS HTML")
print("="*80)
print()
print(f"Usando análise: {html_file.name}")
print()

# Re-executar análise para obter dados completos
from triple_core.orchestrators.screenplay_analyzer import ScreenplayAnalyzer

analyzer = ScreenplayAnalyzer(
    llm_model='scripturemon-optimized',
    deep_context=False
)

print("🔄 Re-executando análise para extrair dados completos...")
print("   (Vai usar cache dos specialist results)")
print()

# Analisar novamente (vai ser rápido porque resultados já existem)
result = analyzer.analyze_screenplay(
    screenplay_path='content/screenplays/personal/SONHOS SEM LEMBRANÇAS T.3.pdf',
    output_dir='workspace/outputs/individual_html'
)

# Criar diretório para relatórios individuais
individual_dir = Path("workspace/outputs/individual_html/specialists")
individual_dir.mkdir(parents=True, exist_ok=True)

print()
print("="*80)
print("📄 GERANDO RELATÓRIOS INDIVIDUAIS")
print("="*80)
print()

# Para cada especialista, gerar HTML individual
specialists = result.get('specialist_results', {})

if not specialists:
    print("❌ Sem specialist_results no result!")
    print(f"Keys disponíveis: {list(result.keys())}")
else:
    for i, (specialist_name, specialist_data) in enumerate(specialists.items(), 1):
        print(f"[{i}/22] {specialist_name}...")

        # Criar HTML individual
        html_content = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{specialist_name} - Relatório Individual</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            max-width: 900px;
            margin: 40px auto;
            padding: 20px;
            background: #f5f5f5;
        }}
        .container {{
            background: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        h1 {{ color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }}
        h2 {{ color: #34495e; margin-top: 30px; }}
        .score {{
            font-size: 48px;
            font-weight: bold;
            color: #3498db;
            text-align: center;
            margin: 20px 0;
        }}
        .metric {{
            background: #ecf0f1;
            padding: 15px;
            margin: 10px 0;
            border-radius: 4px;
        }}
        .metric strong {{ color: #2c3e50; }}
        .recommendation {{
            background: #fff3cd;
            border-left: 4px solid #ffc107;
            padding: 10px 15px;
            margin: 10px 0;
        }}
        .violation {{
            background: #f8d7da;
            border-left: 4px solid #dc3545;
            padding: 10px 15px;
            margin: 10px 0;
        }}
        .diagnosis {{
            background: #d1ecf1;
            border-left: 4px solid #17a2b8;
            padding: 15px;
            margin: 20px 0;
            font-style: italic;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🎬 {specialist_name}</h1>

        <div class="score">
            {specialist_data.get('score', 'N/A')}/100
        </div>

        <h2>📊 Métricas</h2>
        <div class="metrics">
"""

        # Adicionar métricas
        for key, value in specialist_data.items():
            if key not in ['specialist', 'score', 'recommendations', 'rule_violations', 'diagnosis', 'signature']:
                if isinstance(value, (int, float)):
                    html_content += f"""
            <div class="metric">
                <strong>{key.replace('_', ' ').title()}:</strong> {value}
            </div>
"""

        # Diagnosis
        if 'diagnosis' in specialist_data:
            html_content += f"""
        </div>

        <h2>🔍 Diagnóstico</h2>
        <div class="diagnosis">
            {specialist_data['diagnosis']}
        </div>
"""

        # Recommendations
        if 'recommendations' in specialist_data and specialist_data['recommendations']:
            html_content += """
        <h2>💡 Recomendações</h2>
"""
            for rec in specialist_data['recommendations']:
                html_content += f"""
        <div class="recommendation">
            {rec}
        </div>
"""

        # Rule Violations
        if 'rule_violations' in specialist_data and specialist_data['rule_violations']:
            html_content += """
        <h2>⚠️ Violações de Regras</h2>
"""
            for viol in specialist_data['rule_violations']:
                html_content += f"""
        <div class="violation">
            <strong>[{viol.get('severity', 'UNKNOWN').upper()}]</strong> {viol.get('title', 'N/A')}<br>
            {viol.get('message', '')}
        </div>
"""

        html_content += """
    </div>
</body>
</html>
"""

        # Salvar arquivo
        filename = specialist_name.lower().replace(' ', '_').replace('-', '_') + '.html'
        filepath = individual_dir / filename
        filepath.write_text(html_content, encoding='utf-8')

        print(f"   ✅ {filepath}")

print()
print("="*80)
print(f"✅ {len(specialists)} RELATÓRIOS GERADOS!")
print("="*80)
print()
print(f"📂 Localização: {individual_dir}")
