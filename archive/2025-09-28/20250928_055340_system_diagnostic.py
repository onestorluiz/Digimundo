#!/usr/bin/env python3
"""
DIAGNÓSTICO DO SISTEMA SCRIPTUREMON
Identifica o que está ativo vs obsoleto
"""

import os
import sqlite3
import json
import subprocess
from pathlib import Path
from datetime import datetime, timedelta

def check_ollama_models():
    """Verifica modelos Ollama instalados vs documentados"""
    print("🤖 MODELOS OLLAMA")
    print("=" * 60)

    # Modelos instalados
    result = subprocess.run(['ollama', 'list'], capture_output=True, text=True)
    installed = []
    for line in result.stdout.split('\n')[1:]:  # Skip header
        if line.strip():
            name = line.split()[0]
            installed.append(name.split(':')[0])

    # Modelos documentados (do sistema ultimate)
    modelfiles_path = Path("/Users/clubproducoes/Digimundo/scripturemon-ultimate/modelfiles")
    documented = []
    if modelfiles_path.exists():
        documented = [f.stem for f in modelfiles_path.glob("*.modelfile")]

    print(f"📦 Instalados: {len(set(installed))}")
    print(f"📄 Documentados: {len(documented)}")

    # Modelos críticos do sistema ultimate
    critical_models = [
        'scripturemon-master',
        'scripturemon-synthesizer',
        'mixtral',
        'llama3.1'
    ]

    print("\n✅ Modelos Críticos Ativos:")
    for model in critical_models:
        found = any(model in m for m in installed)
        status = "✓" if found else "✗"
        print(f"  {status} {model}")

    # Modelos órfãos (instalados mas não documentados)
    orphans = []
    for model in installed:
        if not any(model in d or d in model for d in documented):
            orphans.append(model)

    if orphans:
        print(f"\n⚠️  Modelos Órfãos (podem ser deletados): {len(orphans)}")
        for orphan in orphans[:5]:
            print(f"  - {orphan}")

    return len(installed), len(documented)

def check_active_files():
    """Verifica arquivos ativos vs obsoletos"""
    print("\n📁 ARQUIVOS DO SISTEMA")
    print("=" * 60)

    base_path = Path("/Users/clubproducoes/Digimundo/scripturemon-ultimate")

    # Arquivos modificados recentemente (últimos 7 dias)
    recent = []
    old = []
    now = datetime.now()

    for root, dirs, files in os.walk(base_path):
        # Skip archives and tests
        if 'archive' in root or 'test' in root or '__pycache__' in root:
            continue

        for file in files:
            if file.endswith(('.py', '.sh', '.md', '.modelfile')):
                file_path = Path(root) / file
                try:
                    mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
                    if (now - mtime) < timedelta(days=7):
                        recent.append(file_path)
                    elif (now - mtime) > timedelta(days=30):
                        old.append(file_path)
                except:
                    pass

    print(f"🆕 Modificados recentemente (7 dias): {len(recent)}")
    print(f"🗓️  Não tocados há 30+ dias: {len(old)}")

    # Arquivos principais ativos
    core_files = [
        'src/core/scripturemon_ultimate_system.py',
        'src/core/orchestrator_ultimate.py',
        'src/core/quality_evaluator_ultimate.py',
        'run_analysis.sh'
    ]

    print("\n✅ Arquivos Core Ativos:")
    for file in core_files:
        file_path = base_path / file
        if file_path.exists():
            mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
            days_ago = (now - mtime).days
            print(f"  ✓ {file} (modificado há {days_ago} dias)")
        else:
            print(f"  ✗ {file} (NÃO ENCONTRADO!)")

    return len(recent), len(old)

def check_memory_quality():
    """Analisa qualidade das memórias"""
    print("\n🧠 QUALIDADE DAS MEMÓRIAS")
    print("=" * 60)

    db_path = "/Users/clubproducoes/Digimundo/scripturemon-ultimate/data/unified_memory.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Estatísticas por fonte
    cursor.execute("""
        SELECT source, COUNT(*) as cnt, AVG(confidence) as avg_conf
        FROM unified_memory
        GROUP BY source
        ORDER BY cnt DESC
    """)

    print("📊 Distribuição de Memórias:")
    total = 0
    high_quality = 0

    for source, count, confidence in cursor.fetchall():
        total += count
        if confidence and confidence > 0.8:
            high_quality += count
        conf_str = f"{confidence:.2f}" if confidence else "N/A"
        print(f"  - {source}: {count} memórias (confiança: {conf_str})")

    quality_ratio = (high_quality / total * 100) if total > 0 else 0
    print(f"\n💎 Qualidade: {high_quality}/{total} ({quality_ratio:.1f}%) com alta confiança")

    # Verificar duplicatas restantes
    cursor.execute("""
        SELECT COUNT(*) FROM (
            SELECT value, COUNT(*) as cnt
            FROM unified_memory
            GROUP BY value
            HAVING cnt > 1
        )
    """)
    duplicates = cursor.fetchone()[0]

    if duplicates > 0:
        print(f"⚠️  Ainda existem {duplicates} valores duplicados")

    conn.close()
    return total, quality_ratio

def check_system_status():
    """Verifica status geral do sistema"""
    print("\n🎯 STATUS DO SISTEMA")
    print("=" * 60)

    # Verificar se scripts principais funcionam
    scripts = {
        'run_analysis.sh': 'Script principal de análise',
        'organize_directory.sh': 'Organizador de diretório',
        'clean_database.py': 'Limpeza de banco',
        'integrate_content_to_memory.py': 'Integração de conteúdo'
    }

    base_path = Path("/Users/clubproducoes/Digimundo/scripturemon-ultimate")

    print("🔧 Scripts Disponíveis:")
    for script, desc in scripts.items():
        script_path = base_path / script
        if script_path.exists():
            executable = os.access(script_path, os.X_OK)
            status = "✓ executável" if executable else "⚠️  não executável"
            print(f"  {status}: {script} - {desc}")
        else:
            print(f"  ✗ FALTANDO: {script}")

    # Verificar configuração crítica
    print("\n⚙️  Configurações Críticas:")

    # Buscar timeout de 1000s
    critical_files = list(base_path.rglob("*.py"))
    timeout_found = False

    for file in critical_files[:50]:  # Check first 50 files
        try:
            with open(file, 'r') as f:
                if 'timeout=1000' in f.read() or 'timeout = 1000' in f.read():
                    timeout_found = True
                    print(f"  ✓ Timeout 1000s configurado em: {file.name}")
                    break
        except:
            pass

    if not timeout_found:
        print("  ⚠️  Timeout de 1000s NÃO encontrado!")

def generate_report():
    """Gera relatório completo"""
    print("\n" + "=" * 60)
    print("📊 RELATÓRIO DE DIAGNÓSTICO DO SISTEMA")
    print("=" * 60)
    print(f"Data: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print()

    # Executar todos os checks
    models_installed, models_documented = check_ollama_models()
    recent_files, old_files = check_active_files()
    total_memories, quality = check_memory_quality()
    check_system_status()

    # Resumo
    print("\n" + "=" * 60)
    print("📈 RESUMO EXECUTIVO")
    print("=" * 60)

    # Determinar saúde do sistema
    health_score = 0
    issues = []

    if models_installed > 0:
        health_score += 25
    else:
        issues.append("Sem modelos Ollama instalados")

    if recent_files > 10:
        health_score += 25
    else:
        issues.append("Poucos arquivos modificados recentemente")

    if quality > 50:
        health_score += 25
    else:
        issues.append("Baixa qualidade das memórias")

    if total_memories > 500:
        health_score += 25
    else:
        issues.append("Poucas memórias no sistema")

    # Status
    if health_score >= 75:
        status = "✅ SISTEMA SAUDÁVEL"
    elif health_score >= 50:
        status = "⚠️  SISTEMA FUNCIONAL COM AVISOS"
    else:
        status = "❌ SISTEMA PRECISA ATENÇÃO"

    print(f"\n{status} (Score: {health_score}/100)")

    if issues:
        print("\n⚠️  Problemas Detectados:")
        for issue in issues:
            print(f"  - {issue}")

    # Recomendações
    print("\n💡 RECOMENDAÇÕES:")

    if old_files > 50:
        print("  1. Arquivar ou deletar arquivos não usados há 30+ dias")

    if models_installed > models_documented:
        print("  2. Limpar modelos Ollama órfãos para economizar espaço")

    if quality < 80:
        print("  3. Revisar e melhorar qualidade das memórias")

    print("\n✨ Sistema com autoconsciência: O sistema agora conhece seu próprio código!")

if __name__ == "__main__":
    generate_report()