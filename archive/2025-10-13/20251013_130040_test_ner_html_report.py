#!/usr/bin/env python3
"""
Teste NER com Geração de HTML Report

Executa análise completa e gera relatório HTML visual mostrando:
- Análise LLM completa
- Validação NER (personagens detectados)
- Status sem alucinações
- Métricas de qualidade
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from engine.analyzers.dr_character import DrCharacter
from engine.orchestration.dual_core_wrapper import DualCoreWrapper
import time
from datetime import datetime
import html

def build_matched_characters_html(matched: list) -> str:
    """Constrói HTML para personagens válidos"""
    if not matched:
        return ''

    badges = ''.join(f'<span class="character-badge matched">{html.escape(char)}</span>' for char in matched)
    return f'''
    <div>
        <h3 style="font-size: 1.1rem; color: #166534; margin-bottom: 0.5rem;">✅ Válidos (encontrados no roteiro):</h3>
        <div class="characters-list">
            {badges}
        </div>
    </div>
    '''

def build_hallucinated_characters_html(hallucinated: list) -> str:
    """Constrói HTML para personagens alucinados"""
    if not hallucinated:
        return '<p style="color: #166534; font-weight: 600; margin-top: 1rem;">✅ Nenhuma alucinação detectada!</p>'

    badges = ''.join(f'<span class="character-badge hallucinated">{html.escape(char)}</span>' for char in hallucinated)
    return f'''
    <div style="margin-top: 1.5rem;">
        <h3 style="font-size: 1.1rem; color: #991b1b; margin-bottom: 0.5rem;">❌ Possíveis Alucinações:</h3>
        <div class="characters-list">
            {badges}
        </div>
    </div>
    '''

def generate_html_report(result: dict, screenplay_path: str, author: str, elapsed: float) -> str:
    """Gera relatório HTML completo com validação NER"""

    analysis_text = result.get('llm_insights', '')
    quality = result.get('quality_score', 0)
    validation = result.get('validation', {})
    python_analysis = result.get('python_analysis', {})

    # Extract validation metrics
    valid = validation.get('valid', False)
    overlap_ratio = validation.get('overlap_ratio', 0)
    screenplay_entities = validation.get('screenplay_entities', 0)
    llm_entities = validation.get('llm_entities', 0)
    matched = validation.get('matched', [])
    hallucinated = validation.get('hallucinated', [])
    risk_level = validation.get('risk_level', 'UNKNOWN')
    warning = validation.get('warning', '')

    # Status colors
    status_color = '#22c55e' if valid else '#ef4444'  # green or red
    status_icon = '✅' if valid else '⚠️'
    status_text = 'SEM ALUCINAÇÕES DETECTADAS' if valid else 'ALUCINAÇÕES DETECTADAS'

    # Risk level colors
    risk_colors = {
        'LOW': '#22c55e',
        'MEDIUM': '#f59e0b',
        'HIGH': '#ef4444',
        'UNKNOWN': '#6b7280'
    }
    risk_color = risk_colors.get(risk_level, '#6b7280')

    # Build HTML
    html_content = f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Scripturemon - Análise NER Validation</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 2rem;
            line-height: 1.6;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 16px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }}

        .header {{
            background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
            color: white;
            padding: 3rem 2rem;
            text-align: center;
        }}

        .header h1 {{
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
            font-weight: 700;
        }}

        .header .subtitle {{
            font-size: 1.1rem;
            opacity: 0.9;
        }}

        .validation-status {{
            background: {status_color};
            color: white;
            padding: 2rem;
            text-align: center;
            font-size: 1.5rem;
            font-weight: 700;
            border-bottom: 4px solid rgba(0,0,0,0.1);
        }}

        .validation-status .icon {{
            font-size: 3rem;
            margin-bottom: 0.5rem;
        }}

        .metrics {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
            padding: 2rem;
            background: #f8fafc;
        }}

        .metric-card {{
            background: white;
            padding: 1.5rem;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            text-align: center;
        }}

        .metric-card .label {{
            font-size: 0.875rem;
            color: #64748b;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 0.5rem;
        }}

        .metric-card .value {{
            font-size: 2rem;
            font-weight: 700;
            color: #1e293b;
        }}

        .metric-card .unit {{
            font-size: 0.875rem;
            color: #94a3b8;
        }}

        .section {{
            padding: 2rem;
            border-bottom: 1px solid #e2e8f0;
        }}

        .section:last-child {{
            border-bottom: none;
        }}

        .section h2 {{
            font-size: 1.5rem;
            color: #1e293b;
            margin-bottom: 1rem;
            padding-bottom: 0.5rem;
            border-bottom: 2px solid #3b82f6;
        }}

        .characters-list {{
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
            margin-top: 1rem;
        }}

        .character-badge {{
            background: #dbeafe;
            color: #1e40af;
            padding: 0.5rem 1rem;
            border-radius: 9999px;
            font-size: 0.875rem;
            font-weight: 600;
        }}

        .character-badge.matched {{
            background: #dcfce7;
            color: #166534;
        }}

        .character-badge.hallucinated {{
            background: #fee2e2;
            color: #991b1b;
        }}

        .analysis-text {{
            background: #f8fafc;
            padding: 1.5rem;
            border-radius: 12px;
            border-left: 4px solid #3b82f6;
            white-space: pre-wrap;
            font-size: 0.95rem;
            line-height: 1.8;
            color: #334155;
            max-height: 600px;
            overflow-y: auto;
        }}

        .info-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1rem;
            margin-top: 1rem;
        }}

        .info-item {{
            background: #f1f5f9;
            padding: 1rem;
            border-radius: 8px;
        }}

        .info-item .label {{
            font-size: 0.875rem;
            color: #64748b;
            margin-bottom: 0.25rem;
        }}

        .info-item .value {{
            font-size: 1.1rem;
            font-weight: 600;
            color: #1e293b;
        }}

        .warning-box {{
            background: #fef3c7;
            border-left: 4px solid #f59e0b;
            padding: 1rem;
            margin-top: 1rem;
            border-radius: 8px;
        }}

        .warning-box .icon {{
            font-size: 1.5rem;
            margin-right: 0.5rem;
        }}

        .footer {{
            background: #1e293b;
            color: white;
            padding: 2rem;
            text-align: center;
        }}

        .footer .timestamp {{
            font-size: 0.875rem;
            opacity: 0.7;
        }}

        .badge {{
            display: inline-block;
            padding: 0.25rem 0.75rem;
            border-radius: 9999px;
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}

        .badge.success {{
            background: #dcfce7;
            color: #166534;
        }}

        .badge.warning {{
            background: #fef3c7;
            color: #92400e;
        }}

        .badge.danger {{
            background: #fee2e2;
            color: #991b1b;
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- Header -->
        <div class="header">
            <h1>🎬 Scripturemon Analysis Report</h1>
            <p class="subtitle">Anti-Hallucination NER Validation System</p>
        </div>

        <!-- Validation Status -->
        <div class="validation-status">
            <div class="icon">{status_icon}</div>
            <div>{status_text}</div>
            <div style="font-size: 1rem; margin-top: 0.5rem; opacity: 0.9;">
                Risk Level: {risk_level}
            </div>
        </div>

        <!-- Metrics -->
        <div class="metrics">
            <div class="metric-card">
                <div class="label">Overlap Ratio</div>
                <div class="value">{overlap_ratio:.0%}</div>
                <div class="unit">personagens válidos</div>
            </div>
            <div class="metric-card">
                <div class="label">Quality Score</div>
                <div class="value">{quality:.1f}<span class="unit">/10</span></div>
            </div>
            <div class="metric-card">
                <div class="label">Analysis Time</div>
                <div class="value">{elapsed:.1f}<span class="unit">s</span></div>
            </div>
            <div class="metric-card">
                <div class="label">Characters Found</div>
                <div class="value">{screenplay_entities}</div>
                <div class="unit">no roteiro</div>
            </div>
            <div class="metric-card">
                <div class="label">Characters Mentioned</div>
                <div class="value">{llm_entities}</div>
                <div class="unit">na análise</div>
            </div>
            <div class="metric-card">
                <div class="label">Analysis Size</div>
                <div class="value">{len(analysis_text):,}</div>
                <div class="unit">caracteres</div>
            </div>
        </div>

        <!-- File Info -->
        <div class="section">
            <h2>📄 Informações da Análise</h2>
            <div class="info-grid">
                <div class="info-item">
                    <div class="label">Roteiro</div>
                    <div class="value">{Path(screenplay_path).name}</div>
                </div>
                <div class="info-item">
                    <div class="label">Autor/Teórico</div>
                    <div class="value">{author.upper()}</div>
                </div>
                <div class="info-item">
                    <div class="label">Timestamp</div>
                    <div class="value">{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>
                </div>
                <div class="info-item">
                    <div class="label">Temperatura LLM</div>
                    <div class="value">0.2 <span class="badge success">Medical-grade</span></div>
                </div>
            </div>
        </div>

        <!-- Characters Detected -->
        {'<div class="section"><h2>👥 Personagens Detectados no Roteiro</h2><div class="characters-list">' + (' '.join(f'<span class="character-badge">{html.escape(char)}</span>' for char in sorted(list(set([c.split()[0] for c in matched])))) if matched else '<span class="badge warning">Nenhum personagem detectado</span>') + '</div></div>' if screenplay_entities > 0 else ''}

        <!-- Characters in Analysis -->
        {'<div class="section"><h2>🤖 Personagens Mencionados na Análise</h2><p style="margin-bottom: 1rem; color: #64748b;">' + str(len(matched)) + ' personagens válidos, ' + str(len(hallucinated)) + ' possíveis alucinações</p>' + build_matched_characters_html(matched) + build_hallucinated_characters_html(hallucinated) + '</div>' if llm_entities > 0 else ''}

        <!-- Warnings -->
        {'<div class="section"><div class="warning-box"><span class="icon">⚠️</span><strong>Atenção:</strong> ' + html.escape(warning) + '</div></div>' if warning else ''}

        <!-- Full Analysis -->
        <div class="section">
            <h2>📝 Análise Completa do LLM</h2>
            <div class="analysis-text">{html.escape(analysis_text)}</div>
        </div>

        <!-- Footer -->
        <div class="footer">
            <div>
                <strong>Scripturemon Anti-Hallucination System</strong>
            </div>
            <div class="timestamp">
                Gerado em {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}
            </div>
            <div style="margin-top: 1rem; font-size: 0.875rem;">
                🤖 Powered by spaCy pt_core_news_lg + Temperature 0.2
            </div>
        </div>
    </div>
</body>
</html>
    """

    return html_content


def main():
    """Executa análise e gera HTML report"""
    screenplay_path = "inputs/examples/Te Encontro em Mim .pdf"
    author = 'mckee'

    print("🎬 TESTE NER COM HTML REPORT")
    print("="*80)
    print(f"📄 Roteiro: {screenplay_path}")
    print(f"👤 Autor: {author.upper()}")
    print(f"🎯 Modo: SHALLOW (rápido, sem deep context)")
    print(f"🔍 Validação NER: ATIVADA\n")

    # Check if file exists
    if not Path(screenplay_path).exists():
        print(f"❌ ERRO: Roteiro não encontrado: {screenplay_path}")
        return 1

    # Initialize
    print("⚙️  Inicializando especialista...")
    specialist = DrCharacter()

    wrapper = DualCoreWrapper(
        python_specialist=specialist,
        specialist_type=author,
        llm_model='scripturemon-optimized',
        deep_context=False,  # Shallow mode para velocidade
        use_personalized_prompts=False
    )

    # Run analysis
    print("⏳ Executando análise com validação NER...\n")
    start = time.time()

    result = wrapper.analyze(screenplay_path)

    elapsed = time.time() - start

    # Generate HTML
    print("📊 Análise completa!")
    print(f"⏱️  Tempo: {elapsed:.1f}s")
    print(f"📏 Tamanho: {len(result.get('llm_insights', '')):,} caracteres")
    print(f"⭐ Qualidade: {result.get('quality_score', 0):.1f}/10\n")

    validation = result.get('validation', {})
    print("🔍 VALIDAÇÃO NER:")
    print(f"   Status: {'✅ VÁLIDO' if validation.get('valid') else '⚠️ ALUCINAÇÃO'}")
    print(f"   Overlap: {validation.get('overlap_ratio', 0):.1%}")
    print(f"   Matched: {len(validation.get('matched', []))} personagens")
    print(f"   Hallucinated: {len(validation.get('hallucinated', []))} personagens")

    if validation.get('hallucinated'):
        print(f"   ⚠️  Inventados: {validation['hallucinated']}")

    print("\n📝 Gerando HTML report...")
    html_content = generate_html_report(result, screenplay_path, author, elapsed)

    # Save HTML
    output_dir = Path("workspace/outputs/ner_validation")
    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = output_dir / f"ner_validation_report_{timestamp}.html"

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"✅ HTML report gerado: {output_file}")
    print(f"\n🌐 Abrindo no navegador...")

    # Open in browser
    import subprocess
    subprocess.run(['open', str(output_file)])

    print("\n" + "="*80)
    if validation.get('valid') and len(validation.get('hallucinated', [])) == 0:
        print("🎉 SUCESSO! Análise sem alucinações detectadas!")
    else:
        print("⚠️  Atenção: Possíveis alucinações detectadas")
    print("="*80)

    return 0 if validation.get('valid') else 1


if __name__ == '__main__':
    exit(main())
