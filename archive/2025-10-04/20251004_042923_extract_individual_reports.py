#!/usr/bin/env python3
"""
Extrai relatórios individuais HTML dos 22 especialistas
a partir do relatório consolidado existente.
"""

from pathlib import Path
from bs4 import BeautifulSoup
import json
import re

def generate_specialist_html(name, data):
    """Gera HTML individual a partir dos dados do especialista."""
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
    if 'diagnosis' in data:
        html += f"""
        <h2>🔍 Diagnóstico</h2>
        <div class="diagnosis">
            {data['diagnosis']}
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

    return html


print("="*80)
print("📝 EXTRAÇÃO DE RELATÓRIOS INDIVIDUAIS HTML")
print("="*80)
print()

# Carregar HTML consolidado
html_file = Path("workspace/outputs/analysis_corrected/Sonhos_Sem_Lembranças_T.3_20251004_034833.html")
print(f"📄 Lendo: {html_file.name}")
print()

with open(html_file, 'r', encoding='utf-8') as f:
    html_content = f.read()

soup = BeautifulSoup(html_content, 'html.parser')

# Criar diretório de destino
output_dir = Path("workspace/outputs/individual_html")
output_dir.mkdir(parents=True, exist_ok=True)

# Buscar dados JSON inline
print("🔍 Buscando dados JSON inline...")
scripts = soup.find_all('script')
specialist_results = None

for script in scripts:
    if script.string and 'specialist_results' in script.string:
        # Tentar extrair JSON
        json_match = re.search(r'const\s+data\s*=\s*({.*?});', script.string, re.DOTALL)
        if json_match:
            try:
                data = json.loads(json_match.group(1))
                specialist_results = data.get('specialist_results', {})
                break
            except:
                continue

if specialist_results:
    print(f"✅ Encontrados {len(specialist_results)} especialistas no JSON")
    print()

    for i, (name, data) in enumerate(specialist_results.items(), 1):
        print(f"[{i}/22] {name}...")

        # Criar HTML individual
        html_content = generate_specialist_html(name, data)

        # Salvar
        filename = name.lower().replace(' ', '_').replace('-', '_') + '.html'
        filepath = output_dir / filename
        filepath.write_text(html_content, encoding='utf-8')
        print(f"   ✅ {filepath.name}")

    print()
    print("="*80)
    print(f"✅ {len(specialist_results)} RELATÓRIOS GERADOS!")
    print("="*80)
    print()
    print(f"📂 Localização: {output_dir}")
else:
    print("❌ Não foi possível encontrar dados JSON no HTML")
