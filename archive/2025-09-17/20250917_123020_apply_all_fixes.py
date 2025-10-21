"""
🔧 APPLY ALL FIXES ITERATIVELY
===============================
Aplica correções em múltiplas rodadas até estabilizar
"""
import sys
from pathlib import Path
import time
sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent / 'apps' / 'scripturemon'))
from ast_based_refactoring import ASTRefactoringSystem
from async_await_validator import AsyncAwaitValidator
from apps.scripturemon.integrated_validation_system import IntegratedValidationSystem, ValidationLevel
import asyncio

def apply_iterative_fixes():
    """Aplica correções iterativamente até estabilizar"""
    print('\n' + '=' * 80)
    print('🔧 APPLYING ALL FIXES ITERATIVELY')
    print('=' * 80)
    project_root = Path('/Users/clubproducoes/Digimundo/scripturemon-champion')
    max_rounds = 5
    round_num = 0
    total_fixes = 0
    harmony_history = []
    while round_num < max_rounds:
        round_num += 1
        print(f'\n📍 ROUND {round_num}/{max_rounds}')
        print('-' * 60)
        fixes_this_round = 0
        print('\n1️⃣ Constructor Fixes:')
        ast_system = ASTRefactoringSystem(project_root)
        constructor_fixes = 0
        for py_file in project_root.rglob('*.py'):
            if '.bak' not in str(py_file) and '__pycache__' not in str(py_file):
                success, fixes = ast_system.process_file(py_file)
                if success and fixes > 0:
                    constructor_fixes += fixes
        fixes_this_round += constructor_fixes
        print(f'   Fixed: {constructor_fixes} constructors')
        print('\n2️⃣ Async/Await Fixes:')
        async_validator = AsyncAwaitValidator(project_root)
        async_validator.validate_project()
        async_fixes = async_validator.auto_fix_issues(dry_run=False)
        fixes_this_round += async_fixes
        print(f'   Fixed: {async_fixes} async issues')
        print('\n3️⃣ Integrated Validation:')
        system = IntegratedValidationSystem(project_root)
        report = system.run_integrated_validation(level=ValidationLevel.STANDARD, auto_fix=True, generate_report=False)
        fixes_this_round += report.total_issues_fixed
        harmony_history.append(report.harmony_score)
        print(f'   Harmony: {report.harmony_score:.1f}%')
        print(f'   Fixed: {report.total_issues_fixed} integrated issues')
        total_fixes += fixes_this_round
        print(f'\n✅ Round {round_num} Complete:')
        print(f'   Fixes this round: {fixes_this_round}')
        print(f'   Total fixes: {total_fixes}')
        if fixes_this_round == 0:
            print('\n🎯 No more fixes needed - system stabilized!')
            break
        time.sleep(1)
    print('\n' + '=' * 80)
    print('🚀 RUNNING FINAL MAXIMUM VALIDATION')
    print('=' * 80)
    final_system = IntegratedValidationSystem(project_root)
    final_report = final_system.run_integrated_validation(level=ValidationLevel.MAXIMUM, auto_fix=False, generate_report=True)
    print('\n' + '=' * 80)
    print('📊 FINAL RESULTS:')
    print('=' * 80)
    print(f'  • Total Rounds: {round_num}')
    print(f'  • Total Fixes Applied: {total_fixes}')
    print(f'  • Initial Harmony: {(harmony_history[0] if harmony_history else 0):.1f}%')
    print(f'  • Final Harmony: {final_report.harmony_score:.1f}%')
    print(f'  • Total Remaining Issues: {final_report.total_issues_found - final_report.total_issues_fixed}')
    if len(harmony_history) > 1:
        print('\n📈 Harmony Progression:')
        for i, score in enumerate(harmony_history, 1):
            bar = '█' * int(score / 2)
            print(f'   Round {i}: {bar} {score:.1f}%')
    if final_report.harmony_score > 80:
        print('\n✅ EXCELLENT! System achieved production-ready harmony!')
    elif final_report.harmony_score > 60:
        print('\n🟢 GOOD! System significantly improved!')
    elif final_report.harmony_score > 40:
        print('\n🟡 MODERATE! System improved but needs more work.')
    else:
        print('\n🔴 System needs significant manual intervention.')
    print('=' * 80)
    return final_report
if __name__ == '__main__':
    report = apply_iterative_fixes()