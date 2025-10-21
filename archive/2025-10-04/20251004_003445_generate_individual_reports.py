#!/usr/bin/env python3
"""
Gera relatórios individuais detalhados para cada um dos 22 especialistas.
"""

import json
from pathlib import Path
from triple_core.orchestrators.screenplay_analyzer import ScreenplayAnalyzer
from datetime import datetime


def generate_individual_reports(screenplay_path: str, output_dir: str):
    """Generate individual detailed reports for all 22 specialists."""

    print("="*80)
    print("📝 GERANDO RELATÓRIOS INDIVIDUAIS - 22 ESPECIALISTAS")
    print("="*80)
    print()

    # Run full analysis
    print("⏱️  Executando análise completa... (~26 minutos)")
    print()

    analyzer = ScreenplayAnalyzer(
        llm_model='scripturemon-optimized',
        deep_context=False
    )

    result = analyzer.analyze_screenplay(
        screenplay_path=screenplay_path,
        output_dir=output_dir
    )

    # Create individual reports directory
    individual_dir = Path(output_dir) / "individual_reports"
    individual_dir.mkdir(parents=True, exist_ok=True)

    print()
    print("="*80)
    print("📄 GERANDO RELATÓRIOS INDIVIDUAIS")
    print("="*80)
    print()

    screenplay_title = Path(screenplay_path).stem.replace('_', ' ').title()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Generate individual report for each specialist
    for i, specialist_result in enumerate(result['specialist_results'], 1):
        specialist_name = specialist_result['specialist']['name']
        specialist_title = specialist_result['specialist']['title']
        score = specialist_result.get('score', 0)

        # Safe filename
        safe_name = specialist_name.replace(' ', '_').replace('Dr.', 'Dr').replace(',', '')
        filename = f"{i:02d}_{safe_name}_{timestamp}.md"
        filepath = individual_dir / filename

        # Generate detailed markdown report
        report = generate_specialist_markdown(
            specialist_result,
            screenplay_title,
            i
        )

        # Save report
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(report)

        print(f"   ✅ [{i:2d}/22] {specialist_name}: {score:.1f}/100 → {filepath.name}")

    # Also save JSON dump for programmatic access
    json_path = individual_dir / f"all_specialists_{timestamp}.json"
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(result['specialist_results'], f, indent=2, ensure_ascii=False)

    print()
    print(f"   ✅ JSON completo: {json_path.name}")
    print()
    print("="*80)
    print("✅ RELATÓRIOS INDIVIDUAIS GERADOS!")
    print("="*80)
    print()
    print(f"📁 Diretório: {individual_dir}")
    print(f"📊 Total: 22 relatórios Markdown + 1 JSON")
    print()

    return individual_dir


def generate_specialist_markdown(specialist_result: dict, screenplay_title: str, number: int) -> str:
    """Generate detailed markdown report for a single specialist."""

    specialist = specialist_result['specialist']
    name = specialist['name']
    title = specialist['title']
    specialty = specialist.get('specialty', 'Screenplay Analysis')

    score = specialist_result.get('score', 0)
    diagnosis = specialist_result.get('diagnosis', 'No diagnosis available.')
    recommendations = specialist_result.get('recommendations', [])

    # Extract additional details
    details = []
    for key, value in specialist_result.items():
        if key not in ['specialist', 'score', 'diagnosis', 'recommendations', 'signature', 'examples']:
            details.append((key, value))

    # Build report
    report = f"""# {name}
**{title}**

---

## 📋 Informações do Especialista

- **Nome**: {name}
- **Especialidade**: {specialty}
- **Roteiro Analisado**: {screenplay_title}
- **Data da Análise**: {datetime.now().strftime("%Y-%m-%d %H:%M")}

---

## 📊 Score Final

**{score:.1f}/100**

---

## 🔍 Diagnóstico

{diagnosis}

---

## 💡 Recomendações

"""

    if recommendations:
        for i, rec in enumerate(recommendations, 1):
            report += f"{i}. {rec}\n"
    else:
        report += "*Nenhuma recomendação específica.*\n"

    report += "\n---\n\n## 📈 Detalhes da Análise\n\n"

    # Add detailed analysis sections
    if details:
        for key, value in details:
            report += f"### {key.replace('_', ' ').title()}\n\n"

            if isinstance(value, dict):
                report += "```json\n"
                report += json.dumps(value, indent=2, ensure_ascii=False)
                report += "\n```\n\n"
            elif isinstance(value, list):
                if value and isinstance(value[0], dict):
                    report += "```json\n"
                    report += json.dumps(value, indent=2, ensure_ascii=False)
                    report += "\n```\n\n"
                else:
                    for item in value:
                        report += f"- {item}\n"
                    report += "\n"
            else:
                report += f"{value}\n\n"

    # Add examples if available
    if 'examples' in specialist_result and specialist_result['examples']:
        report += "---\n\n## 🎬 Exemplos de Filmes Profissionais\n\n"
        for example in specialist_result['examples']:
            report += f"### {example.get('title', 'Unnamed')}\n"
            report += f"**Contexto**: {example.get('context', 'N/A')}\n\n"
            report += f"{example.get('excerpt', '')}\n\n"
            report += f"*Por que funciona*: {example.get('why_it_works', 'N/A')}\n\n"
            report += "---\n\n"

    # Footer
    report += f"\n---\n\n*Relatório gerado por {name}™*\n"
    report += f"*Sistema Script Doctor™ - Triple-Core Analysis*\n"

    return report


if __name__ == "__main__":
    # Generate individual reports
    output_dir = generate_individual_reports(
        screenplay_path="content/screenplays/personal/sonhos_sem_lembrancas_t3.txt",
        output_dir="workspace/outputs/analysis_improved"
    )

    print(f"✅ Todos os relatórios salvos em: {output_dir}")
