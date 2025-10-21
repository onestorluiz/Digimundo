#!/usr/bin/env python3
"""
Verificação estática de sintaxe e imports
"""
import sys
import json
import compileall
import importlib
from pathlib import Path
from datetime import datetime

def check_syntax():
    """Compila todos os módulos Python em src/"""
    project_root = Path(__file__).parent.parent.parent
    src_path = project_root / 'src'
    
    results = {
        'timestamp': datetime.now().isoformat(),
        'syntax_errors': [],
        'import_errors': [],
        'modules_ok': []
    }
    
    # Compile check
    print("Verificando sintaxe...")
    compile_result = compileall.compile_dir(
        src_path, 
        quiet=2,  # Mostra apenas erros
        legacy=False
    )
    
    if not compile_result:
        results['syntax_errors'].append("Erros de compilação detectados em src/")
    
    # Import check dos módulos-alvo
    target_modules = [
        'src.utils.backup_ops',
        'src.orchestra.output_mixer',
        'src.validator.scoring',
        'src.memory.unified_manager',
        'src.memory.sqlite_dao',
        'src.rag.adapter',
        'src.telepathy.channel',
        'src.utils.config_loader',
        'src.utils.logging_setup'
    ]
    
    sys.path.insert(0, str(project_root))
    
    print("Verificando imports...")
    for module_name in target_modules:
        try:
            module = importlib.import_module(module_name)
            results['modules_ok'].append(module_name)
            print(f"✅ {module_name}")
        except ImportError as e:
            results['import_errors'].append({
                'module': module_name,
                'error': str(e)
            })
            print(f"❌ {module_name}: {e}")
        except Exception as e:
            results['import_errors'].append({
                'module': module_name,
                'error': f"Unexpected: {e}"
            })
            print(f"❌ {module_name}: Unexpected error: {e}")
    
    # Salvar resultados
    output_path = project_root / 'reports' / 'fix_v3' / 'compile_check.json'
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nResultados salvos em: {output_path}")
    
    # Status final
    if results['syntax_errors'] or results['import_errors']:
        print("\n⚠️ Erros detectados!")
        return 1
    else:
        print("\n✅ Todos os módulos OK!")
        return 0

if __name__ == '__main__':
    sys.exit(check_syntax())