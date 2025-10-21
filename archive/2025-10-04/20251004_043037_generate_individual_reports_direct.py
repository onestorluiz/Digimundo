#!/usr/bin/env python3
"""
Gera relatórios individuais rodando análise e salvando cada especialista.
Estratégia: Rodar uma vez, salvar todos.
"""

from pathlib import Path
from triple_core.orchestrators.screenplay_analyzer import ScreenplayAnalyzer
import json

print("="*80)
print("📝 GERAÇÃO DE RELATÓRIOS INDIVIDUAIS - ESTRATÉGIA DIRETA")
print("="*80)
print()
print("🎯 Estratégia:")
print("   1. Rodar análise completa (26 min)")
print("   2. Capturar specialist_results")
print("   3. Gerar 22 HTMLs individuais")
print("="*80)
print()

# Criar analyzer
analyzer = ScreenplayAnalyzer(
    llm_model='scripturemon-optimized',
    deep_context=False
)

print("🔄 Executando análise...")
print()

# Analisar PDF
result = analyzer.analyze_screenplay(
    screenplay_path='content/screenplays/personal/SONHOS SEM LEMBRANÇAS T.3.pdf',
    output_dir='workspace/outputs/individual_reports_data'
)

print()
print("✅ Análise completa!")
print(f"📊 Overall Score: {result['overall_score']}/100")
print()

# Extrair specialist_results
specialist_results = result.get('specialist_results', {})

if not specialist_results:
    print("❌ Nenhum specialist_results encontrado!")
    print(f"Keys disponíveis: {list(result.keys())}")
    exit(1)

print(f"✅ {len(specialist_results)} especialistas encontrados")
print()

# Criar diretório
output_dir = Path("workspace/outputs/individual_html")
output_dir.mkdir(parents=True, exist_ok=True)

# Salvar JSON completo para debug
json_path = output_dir / "all_specialists_data.json"
with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(specialist_results, f, ensure_ascii=False, indent=2)
print(f"💾 Dados salvos: {json_path}")
print()

print("="*80)
print("📄 GERANDO HTMLs INDIVIDUAIS")
print("="*80)
print()

for i, (name, data) in enumerate(specialist_results.items(), 1):
    print(f"[{i}/22] {name}...")
    
    score = data.get('score', 'N/A')
    
    html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{name} - Relatório Individual</title>
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
        pre {{
            background: #f8f9fa;
            padding: 15px;
            border-radius: 4px;
            overflow-x: auto;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🎬 {name}</h1>

        <div class="score">
            {score}/100
        </div>

        <h2>📊 Métricas</h2>
        <div class="metrics">
"""
    
    # Adicionar métricas
    for key, value in data.items():
        if key not in ['specialist', 'score', 'recommendations', 'rule_violations', 'diagnosis', 'signature']:
            if isinstance(value, (int, float)):
                html += f"""
            <div class="metric">
                <strong>{key.replace('_', ' ').title()}:</strong> {value}
            </div>
"""
    
    html += """
        </div>
"""
    
    # Diagnosis
    if 'diagnosis' in data and data['diagnosis']:
        diagnosis = str(data['diagnosis']).replace('\n', '<br>')
        html += f"""
        <h2>🔍 Diagnóstico</h2>
        <div class="diagnosis">
            {diagnosis}
        </div>
"""
    
    # Recommendations
    if 'recommendations' in data and data['recommendations']:
        html += """
        <h2>💡 Recomendações</h2>
"""
        for rec in data['recommendations']:
            html += f"""
        <div class="recommendation">
            {rec}
        </div>
"""
    
    # Rule Violations
    if 'rule_violations' in data and data['rule_violations']:
        html += """
        <h2>⚠️ Violações de Regras</h2>
"""
        for viol in data['rule_violations']:
            severity = viol.get('severity', 'UNKNOWN').upper()
            title = viol.get('title', 'N/A')
            message = viol.get('message', '')
            html += f"""
        <div class="violation">
            <strong>[{severity}]</strong> {title}<br>
            {message}
        </div>
"""
    
    html += """
    </div>
</body>
</html>
"""
    
    # Salvar
    filename = name.lower().replace(' ', '_').replace('-', '_') + '.html'
    filepath = output_dir / filename
    filepath.write_text(html, encoding='utf-8')
    
    print(f"   ✅ {filepath.name}")

print()
print("="*80)
print(f"✅ {len(specialist_results)} RELATÓRIOS GERADOS!")
print("="*80)
print()
print(f"📂 Localização: {output_dir}")
print(f"💾 Dados JSON: {json_path}")
