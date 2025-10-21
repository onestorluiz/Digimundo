#!/usr/bin/env python3
"""
Analisador forense rápido - versão simplificada com skip list completa
"""

import os
import sys
import json
import time
import signal
from pathlib import Path
from datetime import datetime
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Lista completa de arquivos problemáticos para pular
SKIP_FILES = [
    'fix_all_indentation.py',
    'fix_all_memory_systems.py',
    'fix_all_relative_imports.py',
    'telepathic_network.py',
    'telepathic_network_advanced.py',
    'digimon_producermon_ultra_supreme.py',
    'hyper_quantum_unified_orchestrator.py',
    'analyze_all_memory_systems.py',  # Arquivo que travou
    'quantum_entangled_memory.py',
    'quantum_blockchain_memory.py',
    'telepathic_memory_supreme.py',
]

def analyze_file_quick(filepath: Path) -> dict:
    """Análise rápida baseada em padrões"""

    # Verificar se deve pular
    if filepath.name in SKIP_FILES:
        return {
            'file': filepath.name,
            'status': 'SKIPPED',
            'reason': 'Known problematic file',
            'vices_percentage': 100
        }

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = content.splitlines()
    except:
        return {
            'file': filepath.name,
            'status': 'ERROR',
            'reason': 'Could not read file',
            'vices_percentage': 0
        }

    # Análise baseada em padrões
    vices_count = 0
    total_checks = 10

    # Check 1: Nome do arquivo
    name_lower = filepath.name.lower()
    if any(word in name_lower for word in ['quantum', 'telepathic', 'supreme', 'ultra', 'hyper']):
        vices_count += 2  # Peso dobrado para nomes problemáticos

    if 'fix_all' in name_lower or 'add_missing' in name_lower:
        vices_count += 2

    # Check 2: Tamanho do arquivo
    if len(lines) > 500:
        vices_count += 1
    if len(lines) > 1000:
        vices_count += 1

    # Check 3: Imports problemáticos
    problematic_imports = [
        'from quantum', 'import quantum',
        'from telepathic', 'import telepathic',
        'from blockchain', 'import blockchain',
        'import pickle', 'from pickle',
        'import marshal', 'from marshal'
    ]
    for imp in problematic_imports:
        if any(imp in line.lower() for line in lines[:50]):  # Check primeiras 50 linhas
            vices_count += 1
            break

    # Check 4: Threading + Async (mistura de paradigmas)
    has_threading = any('threading' in line or 'Thread' in line for line in lines)
    has_async = any('async def' in line or 'await ' in line for line in lines)
    if has_threading and has_async:
        vices_count += 2

    # Check 5: Memory mapping sem cleanup
    has_mmap = any('mmap' in line for line in lines)
    has_close = any('.close()' in line or 'with ' in line for line in lines)
    if has_mmap and not has_close:
        vices_count += 1

    # Check 6: Hardcoded paths
    if any('/tmp/' in line or '/private/tmp' in line for line in lines):
        vices_count += 1

    # Check 7: Classes gigantes
    class_count = sum(1 for line in lines if line.strip().startswith('class '))
    if class_count > 5:
        vices_count += 1

    # Check 8: Try/except genéricos
    if any('except:' in line or 'except Exception:' in line for line in lines):
        vices_count += 1

    # Calcular porcentagem
    vices_percentage = (vices_count / total_checks) * 100

    # Classificar
    if vices_percentage >= 80:
        status = 'BROKEN'
    elif vices_percentage >= 50:
        status = 'PROBLEMATIC'
    elif vices_percentage >= 30:
        status = 'WARNING'
    else:
        status = 'OK'

    return {
        'file': filepath.name,
        'status': status,
        'vices_percentage': vices_percentage,
        'lines': len(lines),
        'size_kb': filepath.stat().st_size / 1024
    }

def main():
    """Executa análise rápida"""

    # Diretório para analisar
    base_dir = Path('/Users/clubproducoes/Digimundo/scripturemon-champion/apps/scripturemon')

    # Coletar arquivos Python
    python_files = sorted(base_dir.glob('*.py'))
    total_files = len(python_files)

    logger.info(f"🚀 Iniciando análise rápida de {total_files} arquivos")
    logger.info(f"⚠️ Pulando {len(SKIP_FILES)} arquivos problemáticos conhecidos")

    results = []
    start_time = time.time()

    # Analisar cada arquivo
    for i, filepath in enumerate(python_files, 1):
        logger.info(f"[{i}/{total_files}] Analisando: {filepath.name}")

        result = analyze_file_quick(filepath)
        results.append(result)

        # Log do resultado
        emoji = {
            'OK': '✅',
            'WARNING': '⚠️',
            'PROBLEMATIC': '🟠',
            'BROKEN': '🔴',
            'SKIPPED': '⏭️',
            'ERROR': '❌'
        }.get(result['status'], '❓')

        logger.info(f"  {emoji} {result['status']}: {result['vices_percentage']:.0f}% vícios")

    # Estatísticas finais
    elapsed_time = time.time() - start_time

    broken_count = sum(1 for r in results if r['status'] == 'BROKEN')
    problematic_count = sum(1 for r in results if r['status'] == 'PROBLEMATIC')
    warning_count = sum(1 for r in results if r['status'] == 'WARNING')
    ok_count = sum(1 for r in results if r['status'] == 'OK')
    skipped_count = sum(1 for r in results if r['status'] == 'SKIPPED')

    logger.info("\n" + "="*60)
    logger.info("📊 RESULTADOS DA ANÁLISE RÁPIDA")
    logger.info(f"⏱️ Tempo total: {elapsed_time:.1f} segundos")
    logger.info(f"📁 Total de arquivos: {total_files}")
    logger.info(f"🔴 BROKEN: {broken_count} ({broken_count/total_files*100:.1f}%)")
    logger.info(f"🟠 PROBLEMATIC: {problematic_count} ({problematic_count/total_files*100:.1f}%)")
    logger.info(f"⚠️ WARNING: {warning_count} ({warning_count/total_files*100:.1f}%)")
    logger.info(f"✅ OK: {ok_count} ({ok_count/total_files*100:.1f}%)")
    logger.info(f"⏭️ SKIPPED: {skipped_count}")

    # Salvar resultados
    output_file = Path('forensic_results/quick_analysis_results.json')
    output_file.parent.mkdir(exist_ok=True)

    with open(output_file, 'w') as f:
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'total_files': total_files,
            'elapsed_seconds': elapsed_time,
            'statistics': {
                'broken': broken_count,
                'problematic': problematic_count,
                'warning': warning_count,
                'ok': ok_count,
                'skipped': skipped_count
            },
            'results': results
        }, f, indent=2)

    logger.info(f"\n💾 Resultados salvos em: {output_file}")

    # Listar os piores arquivos
    logger.info("\n🔥 TOP 10 PIORES ARQUIVOS (não pulados):")
    worst_files = sorted(
        [r for r in results if r['status'] != 'SKIPPED'],
        key=lambda x: x['vices_percentage'],
        reverse=True
    )[:10]

    for i, file_result in enumerate(worst_files, 1):
        logger.info(f"{i}. {file_result['file']}: {file_result['vices_percentage']:.0f}% vícios ({file_result['status']})")

if __name__ == '__main__':
    main()