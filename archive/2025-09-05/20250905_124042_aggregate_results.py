#!/usr/bin/env python3
"""Agrega resultados de todas as execuções de verificação"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

def load_run_results(profile: str) -> Dict:
    """Carrega resultados de um profile"""
    json_path = Path(f'reports/verify/runs/{profile}.json')
    if json_path.exists():
        with open(json_path, 'r') as f:
            return json.load(f)
    return None

def aggregate_results() -> Dict:
    """Agrega resultados de todos os profiles"""
    profiles = ['FULL', 'REDIS_OFF', 'RAG_OFF']
    
    aggregate = {
        'timestamp': datetime.now().isoformat(),
        'profiles': {},
        'summary': {
            'total_checks': 0,
            'total_passes': 0,
            'total_failures': 0,
            'total_blocked': 0,
            'by_check': {}
        }
    }
    
    # Coletar resultados por profile
    for profile in profiles:
        results = load_run_results(profile)
        if results:
            aggregate['profiles'][profile] = results
            
            # Atualizar estatísticas
            for check_name, check_result in results['checks'].items():
                if check_name not in aggregate['summary']['by_check']:
                    aggregate['summary']['by_check'][check_name] = {
                        'passes': 0,
                        'failures': 0,
                        'blocked': 0,
                        'profiles': {}
                    }
                
                status = 'pass' if check_result.get('pass') else check_result.get('status', 'fail')
                aggregate['summary']['by_check'][check_name]['profiles'][profile] = status
                
                if check_result.get('pass'):
                    aggregate['summary']['by_check'][check_name]['passes'] += 1
                    aggregate['summary']['total_passes'] += 1
                elif check_result.get('status') == 'blocked':
                    aggregate['summary']['by_check'][check_name]['blocked'] += 1
                    aggregate['summary']['total_blocked'] += 1
                else:
                    aggregate['summary']['by_check'][check_name]['failures'] += 1
                    aggregate['summary']['total_failures'] += 1
                
                aggregate['summary']['total_checks'] += 1
    
    # Calcular taxa de sucesso geral
    if aggregate['summary']['total_checks'] > 0:
        aggregate['summary']['overall_pass_rate'] = (
            aggregate['summary']['total_passes'] / aggregate['summary']['total_checks']
        ) * 100
    else:
        aggregate['summary']['overall_pass_rate'] = 0
    
    return aggregate

def generate_summary_markdown(aggregate: Dict) -> str:
    """Gera relatório Markdown consolidado"""
    lines = []
    lines.append("# Relatório de Verificação - Sumário Agregado\n")
    lines.append(f"**Data:** {aggregate['timestamp']}\n")
    lines.append(f"**Profiles testados:** {', '.join(aggregate['profiles'].keys())}\n")
    
    # Estatísticas gerais
    lines.append("\n## Estatísticas Gerais\n")
    summary = aggregate['summary']
    lines.append(f"- **Total de verificações:** {summary['total_checks']}")
    lines.append(f"- **Passou:** {summary['total_passes']} ✅")
    lines.append(f"- **Falhou:** {summary['total_failures']} ❌")
    lines.append(f"- **Bloqueado:** {summary['total_blocked']} 🚫")
    lines.append(f"- **Taxa de sucesso:** {summary['overall_pass_rate']:.1f}%\n")
    
    # Tabela de resultados por check
    lines.append("\n## Resultados por Check\n")
    lines.append("| Check | FULL | REDIS_OFF | RAG_OFF | Status |")
    lines.append("|-------|------|-----------|---------|---------|")
    
    for check_name, check_data in summary['by_check'].items():
        row = [check_name]
        
        for profile in ['FULL', 'REDIS_OFF', 'RAG_OFF']:
            status = check_data['profiles'].get(profile, 'N/A')
            if status == 'pass':
                row.append('✅')
            elif status == 'blocked':
                row.append('🚫')
            else:
                row.append('❌')
        
        # Status geral do check
        if check_data['passes'] == 3:
            row.append('✅ PASS')
        elif check_data['passes'] > 0:
            row.append('⚠️ PARCIAL')
        elif check_data['blocked'] > 0:
            row.append('🚫 BLOQUEADO')
        else:
            row.append('❌ FAIL')
        
        lines.append(f"| {' | '.join(row)} |")
    
    # Análise por profile
    lines.append("\n## Análise por Profile\n")
    
    for profile, data in aggregate['profiles'].items():
        lines.append(f"\n### {profile}\n")
        
        passed = sum(1 for r in data['checks'].values() if r.get('pass'))
        total = len(data['checks'])
        rate = (passed/total)*100 if total > 0 else 0
        
        lines.append(f"- **Taxa de sucesso:** {rate:.1f}%")
        lines.append(f"- **Passou:** {passed}/{total}")
        
        # Listar falhas específicas
        failures = [k for k, v in data['checks'].items() if not v.get('pass') and v.get('status') != 'blocked']
        if failures:
            lines.append(f"- **Falhas:** {', '.join(failures)}")
    
    # Conclusões
    lines.append("\n## Conclusões\n")
    
    critical_issues = []
    warnings = []
    
    # Analisar issues críticas
    for check_name, check_data in summary['by_check'].items():
        if check_data['failures'] == 3:
            critical_issues.append(f"- **{check_name}**: Falhou em todos os profiles")
        elif check_data['failures'] > 0:
            warnings.append(f"- **{check_name}**: Falhou em {check_data['failures']} profile(s)")
    
    if critical_issues:
        lines.append("### ⚠️ Issues Críticas\n")
        lines.extend(critical_issues)
        lines.append("")
    
    if warnings:
        lines.append("### ⚡ Avisos\n")
        lines.extend(warnings)
        lines.append("")
    
    # Recomendações
    lines.append("### 💡 Recomendações\n")
    
    if summary['overall_pass_rate'] < 50:
        lines.append("1. **Revisar implementação**: Taxa de sucesso muito baixa, verificar módulos básicos")
    elif summary['overall_pass_rate'] < 80:
        lines.append("1. **Ajustes necessários**: Alguns componentes precisam de correção")
    else:
        lines.append("1. **Sistema estável**: Alta taxa de sucesso, apenas ajustes menores necessários")
    
    if 'memory' in [c for c, d in summary['by_check'].items() if d['failures'] > 0]:
        lines.append("2. **Sistema de memória**: Verificar implementação do UnifiedMemoryManager")
    
    if 'telepathy' in [c for c, d in summary['by_check'].items() if d['failures'] > 0]:
        lines.append("3. **Comunicação Redis**: Revisar fallback chain e configurações")
    
    lines.append("\n---\n")
    lines.append(f"**Gerado em:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    return '\n'.join(lines)

def main():
    """Função principal"""
    print("📊 Agregando resultados de verificação...")
    
    # Agregar resultados
    aggregate = aggregate_results()
    
    # Salvar JSON agregado
    output_dir = Path('reports/verify')
    json_path = output_dir / 'aggregate_summary.json'
    with open(json_path, 'w') as f:
        json.dump(aggregate, f, indent=2)
    print(f"✅ JSON agregado salvo: {json_path}")
    
    # Gerar e salvar Markdown
    markdown = generate_summary_markdown(aggregate)
    md_path = output_dir / 'aggregate_summary.md'
    with open(md_path, 'w') as f:
        f.write(markdown)
    print(f"✅ Relatório Markdown salvo: {md_path}")
    
    # Estatísticas finais
    print(f"\n📈 Estatísticas Finais:")
    print(f"  - Total de verificações: {aggregate['summary']['total_checks']}")
    print(f"  - Taxa de sucesso geral: {aggregate['summary']['overall_pass_rate']:.1f}%")
    print(f"  - Passes: {aggregate['summary']['total_passes']}")
    print(f"  - Failures: {aggregate['summary']['total_failures']}")
    print(f"  - Blocked: {aggregate['summary']['total_blocked']}")

if __name__ == "__main__":
    main()