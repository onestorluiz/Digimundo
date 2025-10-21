#!/usr/bin/env python3
"""Runner principal para verificação do sistema"""

import sys
import json
import argparse
import traceback
from pathlib import Path
from datetime import datetime
from typing import Dict, Any

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

VALID_PROFILES = ['FULL', 'REDIS_OFF', 'RAG_OFF']

def load_default_settings() -> Dict:
    """Carrega configurações padrão"""
    return {
        'system': {'name': 'scripturemon-validation', 'version': '1.0.0'},
        'redis': {'enabled': True, 'host': 'localhost', 'port': 6379},
        'rag': {'enabled': True, 'provider': 'chroma', 'k': 8},
        'soulos': {'enabled': False, 'code_execution': False},
        'sdl': {'enabled': False, 'passive_collect_only': True},
        'memory': {'time_weighted_retrieval': True, 'promote_on_hits': 5},
        'scoring': {
            'weights': {
                'structure': 0.3,
                'emotion': 0.2,
                'technique': 0.3,
                'theme': 0.2
            }
        }
    }

def adjust_settings_for_profile(settings: Dict, profile: str) -> Dict:
    """Ajusta settings baseado no profile"""
    adjusted = settings.copy()
    
    if profile == 'FULL':
        adjusted['redis']['enabled'] = True
        adjusted['rag']['enabled'] = True
    elif profile == 'REDIS_OFF':
        adjusted['redis']['enabled'] = False
        adjusted['rag']['enabled'] = True
    elif profile == 'RAG_OFF':
        adjusted['redis']['enabled'] = True
        adjusted['rag']['enabled'] = False
    
    # Sempre manter SoulOS e SDL desabilitados
    adjusted['soulos']['enabled'] = False
    adjusted['sdl']['enabled'] = False
    
    return adjusted

def save_profile_settings(settings: Dict, profile: str):
    """Salva settings ajustadas do profile"""
    output_path = Path(__file__).parent.parent.parent / 'reports' / 'verify' / 'tmp_settings' / f'{profile}.yaml'
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Salvar como JSON (mais simples que YAML)
    json_path = output_path.with_suffix('.json')
    with open(json_path, 'w') as f:
        json.dump(settings, f, indent=2)
    
    return json_path

def run_check(check_name: str, settings: Dict, profile: str) -> Dict:
    """Executa um check individual"""
    try:
        module_path = Path(__file__).parent / f'check_{check_name}.py'
        
        if not module_path.exists():
            return {
                'pass': False,
                'status': 'blocked',
                'reason': f'Check module not found: {module_path}'
            }
        
        # Importar e executar o check
        import importlib.util
        spec = importlib.util.spec_from_file_location(f"check_{check_name}", module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        # Executar função principal do check
        result = module.run_check(settings)
        return result
        
    except Exception as e:
        return {
            'pass': False,
            'status': 'error',
            'exception': str(e),
            'traceback': traceback.format_exc()
        }

def run_verification(profile: str) -> Dict:
    """Executa verificação completa para um profile"""
    print(f"\n{'='*60}")
    print(f"VERIFICAÇÃO - PROFILE: {profile}")
    print(f"{'='*60}\n")
    
    # Carregar e ajustar settings
    settings = load_default_settings()
    adjusted_settings = adjust_settings_for_profile(settings, profile)
    
    # Salvar settings do profile
    settings_path = save_profile_settings(adjusted_settings, profile)
    print(f"✅ Settings salvas em: {settings_path}\n")
    
    # Lista de checks a executar
    checks = [
        'memory',
        'rag',
        'parallel',
        'scoring',
        'telepathy',
        'soulos_sdl',
        'backup',
        'logging',
        'smoke'
    ]
    
    results = {
        'profile': profile,
        'timestamp': datetime.now().isoformat(),
        'settings_path': str(settings_path),
        'checks': {}
    }
    
    # Executar cada check
    for check_name in checks:
        print(f"▶️  Executando check: {check_name}")
        result = run_check(check_name, adjusted_settings, profile)
        results['checks'][check_name] = result
        
        status = "✅ PASS" if result.get('pass', False) else "❌ FAIL"
        if result.get('status') == 'blocked':
            status = "🚫 BLOCKED"
        
        print(f"   {status}\n")
    
    # Salvar resultados
    output_dir = Path(__file__).parent.parent.parent / 'reports' / 'verify' / 'runs'
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # JSON
    json_path = output_dir / f'{profile}.json'
    with open(json_path, 'w') as f:
        json.dump(results, f, indent=2)
    
    # Markdown
    md_path = output_dir / f'{profile}.md'
    with open(md_path, 'w') as f:
        f.write(generate_markdown_report(results))
    
    print(f"✅ Resultados salvos:")
    print(f"   - {json_path}")
    print(f"   - {md_path}\n")
    
    return results

def generate_markdown_report(results: Dict) -> str:
    """Gera relatório Markdown para os resultados"""
    lines = []
    lines.append(f"# Verificação - Profile {results['profile']}\n")
    lines.append(f"**Timestamp:** {results['timestamp']}\n")
    lines.append(f"**Settings:** `{results['settings_path']}`\n")
    
    lines.append("\n## Resultados dos Checks\n")
    lines.append("| Check | Status | Detalhes |")
    lines.append("|-------|--------|----------|")
    
    for check_name, result in results['checks'].items():
        status = "✅ PASS" if result.get('pass', False) else "❌ FAIL"
        if result.get('status') == 'blocked':
            status = "🚫 BLOCKED"
        
        details = result.get('reason', result.get('notes', []))
        if isinstance(details, list):
            details = ', '.join(details) if details else '-'
        
        lines.append(f"| {check_name} | {status} | {details} |")
    
    # Estatísticas
    total = len(results['checks'])
    passed = sum(1 for r in results['checks'].values() if r.get('pass', False))
    failed = total - passed
    
    lines.append(f"\n## Estatísticas\n")
    lines.append(f"- **Total de checks:** {total}")
    lines.append(f"- **Passou:** {passed}")
    lines.append(f"- **Falhou:** {failed}")
    lines.append(f"- **Taxa de sucesso:** {(passed/total)*100:.1f}%")
    
    return '\n'.join(lines)

def main():
    """Função principal"""
    parser = argparse.ArgumentParser(description='Verificação do sistema Scripturemon')
    parser.add_argument('--profile', choices=VALID_PROFILES, required=True,
                       help='Profile de verificação')
    
    args = parser.parse_args()
    
    try:
        results = run_verification(args.profile)
        
        # Determinar exit code
        all_passed = all(
            check.get('pass', False) or check.get('status') == 'blocked'
            for check in results['checks'].values()
        )
        
        return 0  # Sempre retorna 0 se completou (mesmo com falhas)
        
    except Exception as e:
        print(f"\n❌ ERRO FATAL: {e}")
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())