#!/usr/bin/env python3
"""
🚀 RUN VALIDATION COMPLETA
==========================
Executa validação completa no sistema
"""
import asyncio
import sys
from pathlib import Path

# Add local apps to path
sys.path.insert(0, str(Path(__file__).parent / 'apps' / 'scripturemon'))
from src.core.integrated_validation_system import IntegratedValidationSystem, ValidationLevel

async def run_validation():
    """Executa validação completa com todas as correções"""
    print('\n' + '=' * 80)
    print('🚀 RUNNING COMPLETE VALIDATION ON SCRIPTUREMON-CHAMPION')
    print('=' * 80)

    # Use projeto atual ao invés de hardcoded path
    project_root = Path(__file__).parent
    system = IntegratedValidationSystem(project_root)

    try:
        report = await system.run_integrated_validation(
            level=ValidationLevel.COMPLETE,
            auto_fix=True,
            generate_report=True
        )
    except Exception as e:
        print(f'❌ Erro durante validação: {e}')
        return None
    print('\n' + '=' * 80)
    print('🎯 FINAL RESULTS:')
    print('=' * 80)
    print(f'  • Initial Harmony: 6.1%')
    print(f'  • Final Harmony: {report.harmony_score:.1f}%')
    print(f'  • Improvement: {report.harmony_score - 6.1:.1f}%')
    print(f'  • Total Issues Fixed: {report.total_issues_fixed}')
    print('=' * 80)
    if report.harmony_score > 80:
        print('\n✅ EXCELLENT! System harmony is now production-ready!')
    elif report.harmony_score > 60:
        print('\n🟢 GOOD! System harmony significantly improved!')
    elif report.harmony_score > 30:
        print('\n🟡 MODERATE improvement. Manual review recommended.')
    else:
        print('\n🔴 Limited improvement. Deep manual intervention needed.')
    return report
if __name__ == '__main__':
    report = asyncio.run(run_validation())

    if report:
        print('\n🎯 Validação concluída com sucesso!')
        print(f'Relatório disponível em: {report.output_path if hasattr(report, "output_path") else "logs/"}')
    else:
        print('\n❌ Validação falhou!')
        sys.exit(1)