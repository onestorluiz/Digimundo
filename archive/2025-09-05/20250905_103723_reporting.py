import json
import glob
from pathlib import Path
from typing import Dict, Any
from datetime import datetime


def write_phase_report_json(phase: str, payload: dict, path: str) -> None:
    """
    Escreve relatório JSON de uma fase.
    
    Args:
        phase: Nome da fase (ex: FASE_00)
        payload: Dados do relatório
        path: Caminho do arquivo JSON de saída
    """
    # Adicionar metadados padrão se não existirem
    report = {
        'phase': phase,
        'generated_at': datetime.now().isoformat(),
        **payload
    }
    
    # Criar diretório se necessário
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    
    # Escrever JSON
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)


def write_phase_report_md(phase: str, payload: dict, path: str) -> None:
    """
    Escreve relatório Markdown de uma fase.
    
    Args:
        phase: Nome da fase
        payload: Dados do relatório
        path: Caminho do arquivo MD de saída
    """
    # Criar diretório se necessário
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    
    # Construir conteúdo Markdown
    md_content = f"# {phase} - Relatório de Execução\n\n"
    
    # Status
    status = payload.get('status', 'unknown').upper()
    status_icon = "✅" if status == "COMPLETED" else "⚠️" if status == "PARTIAL" else "❌"
    md_content += f"## Status: {status_icon} {status}\n\n"
    
    # Tempos
    if 'start_time' in payload:
        md_content += f"**Início:** {payload['start_time']}  \n"
    if 'end_time' in payload:
        md_content += f"**Término:** {payload['end_time']}  \n"
    md_content += "\n"
    
    # Execução
    md_content += "## Execução\n\n"
    
    exactly_followed = payload.get('exactly_followed', False)
    md_content += f"**Plano seguido exatamente:** {'✅ SIM' if exactly_followed else '❌ NÃO'}  \n"
    
    deviations = payload.get('deviations', [])
    if deviations:
        md_content += f"**Desvios:** {', '.join(deviations)}  \n"
    else:
        md_content += "**Desvios:** Nenhum  \n"
    
    resistance = payload.get('resistance', [])
    if resistance:
        md_content += f"**Resistências:** {', '.join(resistance)}  \n"
    else:
        md_content += "**Resistências:** Nenhuma  \n"
    
    if 'reason' in payload:
        md_content += f"**Razão:** {payload['reason']}  \n"
    
    md_content += "\n"
    
    # Tarefas completadas
    tasks = payload.get('tasks_completed', [])
    if tasks:
        md_content += "## Tarefas Completadas\n\n"
        for i, task in enumerate(tasks, 1):
            md_content += f"{i}. ✅ {task}\n"
        md_content += "\n"
    
    # Detalhes adicionais (genérico para qualquer payload)
    for key, value in payload.items():
        # Pular campos já processados
        if key in ['phase', 'generated_at', 'status', 'start_time', 'end_time', 
                   'exactly_followed', 'deviations', 'resistance', 'reason', 'tasks_completed']:
            continue
        
        # Adicionar seção para outros campos
        if isinstance(value, dict):
            md_content += f"## {key.replace('_', ' ').title()}\n\n"
            for sub_key, sub_value in value.items():
                if isinstance(sub_value, list):
                    md_content += f"**{sub_key.replace('_', ' ').title()}:**\n"
                    for item in sub_value:
                        md_content += f"- {item}\n"
                else:
                    md_content += f"**{sub_key.replace('_', ' ').title()}:** {sub_value}  \n"
            md_content += "\n"
        elif isinstance(value, list):
            md_content += f"## {key.replace('_', ' ').title()}\n\n"
            for item in value:
                md_content += f"- {item}\n"
            md_content += "\n"
        else:
            md_content += f"**{key.replace('_', ' ').title()}:** {value}  \n"
    
    # Conclusão
    md_content += f"\n## Conclusão\n\n{phase} "
    if status == "COMPLETED":
        md_content += "completada com sucesso."
    elif status == "PARTIAL":
        md_content += "parcialmente completada."
    else:
        md_content += "bloqueada ou com falha."
    
    # Escrever arquivo
    with open(path, 'w', encoding='utf-8') as f:
        f.write(md_content)


def merge_phase_reports_json(glob_pattern: str, out_path: str) -> None:
    """
    Agrega todos os relatórios JSON das fases em um único arquivo.
    
    Args:
        glob_pattern: Padrão glob para encontrar arquivos JSON (ex: 'reports/repair/phase_*.json')
        out_path: Caminho do arquivo JSON agregado de saída
    """
    # Encontrar todos os arquivos que correspondem ao padrão
    json_files = sorted(glob.glob(glob_pattern))
    
    # Coletar todos os relatórios
    all_reports = []
    for json_file in json_files:
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                report = json.load(f)
                all_reports.append(report)
        except Exception as e:
            print(f"Erro ao ler {json_file}: {e}")
            continue
    
    # Criar relatório agregado
    aggregated = {
        'type': 'aggregated_phase_reports',
        'generated_at': datetime.now().isoformat(),
        'total_phases': len(all_reports),
        'phases': all_reports,
        'summary': {
            'completed': sum(1 for r in all_reports if r.get('status') == 'completed'),
            'partial': sum(1 for r in all_reports if r.get('status') == 'partial'),
            'blocked': sum(1 for r in all_reports if r.get('status') == 'blocked'),
            'exactly_followed_count': sum(1 for r in all_reports if r.get('exactly_followed', False))
        }
    }
    
    # Criar diretório se necessário
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    
    # Escrever arquivo agregado
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(aggregated, f, indent=2, ensure_ascii=False)