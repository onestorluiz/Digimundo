#!/usr/bin/env python3
"""
Wrapper para analyze.py com monitoramento detalhado de qualidade.
Executa análise completa e gera relatório de qualidade por etapa.
"""

import sys
import subprocess
import time
from pathlib import Path
from datetime import datetime
import json

# Configuração
SCREENPLAY = "inputs/examples/Te Encontro em Mim .pdf"
AUTHORS = [
    "aristotle", "campbell", "cowgill", "dialogue", "egri", "field",
    "mckee", "mckee_character", "mckee_dialogue", "seger", "snyder",
    "truby", "vogler"
]

OUTPUT_DIR = Path("workspace/outputs")
LOG_FILE = OUTPUT_DIR / f"quality_monitor_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

def log(message: str, level: str = "INFO"):
    """Log com timestamp."""
    timestamp = datetime.now().strftime("%H:%M:%S")
    log_msg = f"[{timestamp}] [{level}] {message}"
    print(log_msg)
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(log_msg + "\n")

def check_file_quality(file_path: Path) -> dict:
    """Analisa qualidade de um arquivo HTML gerado."""
    if not file_path.exists():
        return {
            "exists": False,
            "size": 0,
            "score_estimate": 0.0,
            "quality": "MISSING"
        }

    content = file_path.read_text(encoding='utf-8')
    size = len(content)

    # Heurísticas de qualidade
    score = 0.0
    issues = []

    # 1. Tamanho (15-22KB esperado)
    if size < 10000:
        issues.append(f"Too small: {size} bytes")
        score = 3.0
    elif size < 15000:
        issues.append(f"Below target: {size} bytes")
        score = 5.0
    elif size < 22000:
        score = 8.0  # Ideal range
    else:
        score = 7.0  # Larger is ok but not optimal

    # 2. Conteúdo (scene references)
    scene_keywords = ["cena", "página", "scene", "page"]
    scene_count = sum(content.lower().count(kw) for kw in scene_keywords)
    if scene_count < 3:
        issues.append(f"Few scene refs: {scene_count}")
        score = min(score, 4.0)

    # 3. Quotes (dialogue examples)
    quote_markers = ['"', '«', '»', '"', '"']
    quote_count = sum(content.count(marker) for marker in quote_markers)
    if quote_count < 10:
        issues.append(f"Few quotes: {quote_count}")
        score = min(score, 5.0)

    # 4. Rewrites (ANTES/DEPOIS)
    rewrite_keywords = ["ANTES:", "DEPOIS:", "ORIGINAL:", "SUGERIDO:"]
    rewrite_count = sum(content.count(kw) for kw in rewrite_keywords)
    if rewrite_count < 4:  # At least 2 rewrites (2 keywords each)
        issues.append(f"Few rewrites: {rewrite_count}")
        score = min(score, 6.0)

    # Qualidade final
    if score >= 7.0:
        quality = "EXCELLENT"
    elif score >= 5.0:
        quality = "GOOD"
    elif score >= 3.0:
        quality = "ACCEPTABLE"
    else:
        quality = "POOR"

    return {
        "exists": True,
        "size": size,
        "score_estimate": score,
        "quality": quality,
        "scene_count": scene_count,
        "quote_count": quote_count,
        "rewrite_count": rewrite_count,
        "issues": issues
    }

def main():
    """Executa análise com monitoramento."""
    log("="*80)
    log("🎬 ANÁLISE MONITORADA - TE ENCONTRO EM MIM")
    log("="*80)
    log("")

    # Criar diretório de output
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Info
    log(f"📄 Roteiro: {SCREENPLAY}")
    log(f"👥 Autores: {len(AUTHORS)} (13 total)")
    log(f"📊 Qualidade esperada: 15.5-18.0/10 (auditoria manual)")
    log(f"⏱️  Tempo estimado: 90-120 minutos")
    log("")

    # Confirmar arquivo existe
    screenplay_path = Path(SCREENPLAY)
    if not screenplay_path.exists():
        log(f"❌ Arquivo não encontrado: {SCREENPLAY}", "ERROR")
        return 1

    log(f"✅ Arquivo encontrado: {screenplay_path.stat().st_size:,} bytes")
    log("")

    # Construir comando
    authors_str = " ".join(AUTHORS)
    cmd = [
        "python3", "-u", "analyze.py",
        str(screenplay_path),
        "--authors", *AUTHORS,
        "--deep",
        "--use-personalized-prompts"
    ]

    log("🚀 INICIANDO ANÁLISE COMPLETA")
    log(f"   Comando: {' '.join(cmd)}")
    log("")

    # Executar
    start_time = time.time()

    try:
        # Run com output em tempo real
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True
        )

        current_author = None
        author_start_time = {}
        author_results = {}

        # Monitor output
        for line in process.stdout:
            line = line.rstrip()
            if not line:
                continue

            # Log everything
            print(line)
            with open(LOG_FILE, 'a', encoding='utf-8') as f:
                f.write(line + "\n")

            # Detect author changes
            for author in AUTHORS:
                if f"Analyzing with {author}" in line or f"Author: {author.upper()}" in line:
                    if current_author and current_author in author_start_time:
                        # Previous author finished
                        elapsed = time.time() - author_start_time[current_author]
                        log(f"   ⏱️  {current_author} finished in {elapsed:.1f}s", "INFO")

                    current_author = author
                    author_start_time[author] = time.time()
                    log(f"▶️  Starting {author.upper()}", "PROGRESS")
                    break

            # Detect completion
            if "Analysis completed" in line or "✅" in line:
                if current_author and current_author in author_start_time:
                    elapsed = time.time() - author_start_time[current_author]
                    log(f"   ✅ {current_author} completed in {elapsed:.1f}s", "SUCCESS")

        # Wait for completion
        process.wait()
        total_time = time.time() - start_time

        log("")
        log("="*80)
        log(f"🎉 ANÁLISE COMPLETA - {total_time:.1f}s ({total_time/60:.1f} min)")
        log("="*80)
        log("")

        # Analyze quality of outputs
        log("📊 ANÁLISE DE QUALIDADE DOS OUTPUTS")
        log("")

        results = []
        total_score = 0.0

        for author in AUTHORS:
            # Find output file
            output_files = list(OUTPUT_DIR.glob(f"*{author}*.html"))

            if not output_files:
                log(f"⚠️  {author.upper()}: No output file found", "WARNING")
                results.append({
                    "author": author,
                    "quality": "MISSING",
                    "score": 0.0
                })
                continue

            # Get most recent
            output_file = max(output_files, key=lambda p: p.stat().st_mtime)

            # Analyze quality
            quality_data = check_file_quality(output_file)
            results.append({
                "author": author,
                "file": output_file.name,
                **quality_data
            })

            score = quality_data["score_estimate"]
            total_score += score

            # Log
            status = "✅" if quality_data["quality"] in ["EXCELLENT", "GOOD"] else "⚠️"
            log(f"{status} {author.upper():20s} | {score:.1f}/10 | {quality_data['size']:,} bytes | {quality_data['quality']}")

            if quality_data.get("issues"):
                for issue in quality_data["issues"]:
                    log(f"      └─ {issue}", "DETAIL")

        # Summary
        avg_score = total_score / len(AUTHORS) if AUTHORS else 0.0

        log("")
        log("="*80)
        log("📈 RESUMO FINAL")
        log("="*80)
        log(f"   Total de autores: {len(AUTHORS)}")
        log(f"   Tempo total: {total_time/60:.1f} minutos")
        log(f"   Tempo médio/autor: {total_time/len(AUTHORS):.1f}s")
        log(f"   Score médio estimado: {avg_score:.1f}/10 (validador técnico)")
        log(f"   Qualidade esperada (audit manual): 15.5-18.0/10")
        log("")

        # Check for consolidated output
        consolidated_files = list(OUTPUT_DIR.glob("*consolidated*.html"))
        if consolidated_files:
            consolidated = max(consolidated_files, key=lambda p: p.stat().st_mtime)
            log(f"📄 Consolidado gerado: {consolidated.name}")
            log(f"   Tamanho: {consolidated.stat().st_size:,} bytes")
        else:
            log("⚠️  Nenhum arquivo consolidado encontrado", "WARNING")

        log("")
        log(f"📊 Log completo salvo em: {LOG_FILE}")

        # Save JSON report
        report_file = OUTPUT_DIR / f"quality_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        report = {
            "timestamp": datetime.now().isoformat(),
            "screenplay": str(screenplay_path),
            "total_time": total_time,
            "authors_count": len(AUTHORS),
            "average_score": avg_score,
            "results": results
        }

        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

        log(f"📄 Relatório JSON: {report_file}")
        log("")
        log("✅ ANÁLISE MONITORADA CONCLUÍDA COM SUCESSO!")

        return 0

    except Exception as e:
        log(f"❌ ERRO: {e}", "ERROR")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
