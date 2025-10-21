#!/usr/bin/env python3
"""
Script para mover arquivos problemáticos identificados pela análise forense
para pasta de limpeza organizada por categoria.
"""

import json
import shutil
from pathlib import Path
import os

# Diretórios
SOURCE_BASE = Path("/Users/clubproducoes/Digimundo/scripturemon-champion/deployments/green_v2.0.0/code/apps/scripturemon")
DEST_BASE = Path("/Users/clubproducoes/Digimundo/Pre_Limpeza_Minimalista/scripturemon_problematicos")
FORENSIC_REPORT = Path("/Users/clubproducoes/Digimundo/scripturemon-champion/forensic_results/FORENSIC_REPORT_FINAL.md")

# Criar estrutura de destino
categories = {
    "memory": DEST_BASE / "memory_systems",
    "digilang": DEST_BASE / "digilang_versions",
    "monitoring": DEST_BASE / "monitoring_systems",
    "test": DEST_BASE / "test_files",
    "harmony": DEST_BASE / "harmony_systems",
    "ollama": DEST_BASE / "ollama_configs",
    "telepathy": DEST_BASE / "telepathy_systems",
    "soul": DEST_BASE / "soul_systems",
    "script_doctor": DEST_BASE / "script_doctor",
    "misc": DEST_BASE / "miscellaneous"
}

# Criar pastas
for folder in categories.values():
    folder.mkdir(parents=True, exist_ok=True)

# Lista dos piores arquivos da análise forense (163 quebrados)
problematic_files = [
    # Sistemas de memória (31 problemas críticos)
    "synesthetic_crossmodal_memory.py",
    "persistent_memory_system.py",
    "entropic_reverse_memory.py",
    "memory_interconnect_matrix.py",
    "memory_fixes.py",
    "telepathic_memory_supreme.py",
    "quantum_entangled_memory.py",
    "holographic_fractal_memory.py",
    "crystalline_lattice_memory.py",
    "neural_swarm_memory.py",
    "dreamscape_oniric_memory.py",
    "temporal_loop_memory.py",
    "akashic_universal_memory.py",
    "blockchain_immutable_memory.py",
    "plasma_field_memory.py",
    "gravitational_wave_memory.py",
    "biophotonic_coherent_memory.py",
    "morphogenetic_field_memory.py",
    "tachyon_superluminal_memory.py",
    "zero_point_vacuum_memory.py",
    "toroidal_vortex_memory.py",
    "hyperdimensional_tesseract_memory.py",
    "chronological_timeline_memory.py",
    "probability_wave_memory.py",
    "consciousness_field_memory.py",
    "etheric_template_memory.py",
    "astral_projection_memory.py",
    "causal_plane_memory.py",

    # Sistemas de monitoring (28 problemas críticos)
    "monitoring_observability_supreme.py",
    "telemetry_monitoring_api.py",
    "monitoring.py",
    "monitoring_dashboard.py",
    "monitoring_prometheus.py",
    "monitoring_grafana.py",

    # Harmony systems (26 problemas críticos)
    "harmony_perfection_resolver.py",
    "harmony_booster.py",
    "harmony_calculator.py",
    "synergy_repair_system.py",
    "component_resolver.py",

    # DigiLang versions (26 problemas críticos cada)
    "digilang_v27_mega_ultimate.py",
    "digilang_v26_mega_multilayer.py",
    "digilang_v25_hybrid_ultimate.py",
    "digilang_v24_ultimate_pt.py",
    "digilang_v22_mega.py",
    "digilang_v10_supreme.py",
    "digilang_bytecode.py",
    "digilang_tpd.py",
    "digilang_interpreter.py",
    "digilang_compiler.py",
    "digilang_optimizer.py",
    "digilang_adaptive_selector.py",

    # Soul/consciousness systems
    "soul_os.py",
    "soul_signature.py",
    "consciousness.py",
    "immortality.py",

    # Telepathy systems
    "telepathy.py",
    "telepathic_network.py",
    "telepathic_broadcast.py",

    # Script doctor systems
    "distributed_script_doctor_trainer.py",
    "script_doctor_ultimate.py",
    "script_doctor_analyzer.py",

    # Test files (24 problemas críticos)
    "test_clean_ecosystem.py",
    "test_45gb_memory.py",
    "test_supreme_integration.py",
    "memory_debug_test.py",

    # Análises problemáticas
    "analyze_redundancies.py",
    "analyze_all_memory_systems.py",
    "analyze_all_file_locations.py",

    # Ollama configs (24 problemas críticos)
    "ollama_45gb_orchestrator.py",
    "ollama_quadruple.py",
    "ollama_max_config.py",
    "ollama_config_maximum.py",
    "ollama_optimized.py",
    "ollama_fallback.py",
    "ollama_manager.py",
    "ollama_service.py",

    # Outros problemáticos
    "bootstrap.py",
    "cache_manager.py",
    "redis_cache.py",
    "sqlite_dao.py",
    "gpu_accelerator.py",
    "load_balancer.py",
    "rate_limiter_supreme.py",
    "performance_optimizer.py",
    "backup_manager.py",
    "compression_service.py",
    "validator.py",
    "parallel.py",
    "extract_engine.py",
    "persona.py",
    "cli_chat.py",
    "ultimate_screenplay_chat.py",
    "unified_cli.py",
    "unified_manager.py",
    "system_manager.py",
    "membridge.py",
    "doctor.py",
    "config_silicon_valley.py",
    "hybrid_processing_config.py",

    # Fixes e patches problemáticos
    "fix_all_memory_systems.py",
    "fix_all_relative_imports.py",
    "fix_indentation_errors.py",
    "fix_remaining_imports.py",
    "apply_fallback_imports.py",
    "add_missing_methods.py",
    "add_retrieve_memory.py",
    "final_fix_syntax.py",

    # Fallbacks imaginários
    "librosa_fallback.py",
    "matplotlib_fallback.py",
    "mpl_toolkits_fallback.py",
    "deap_fallback.py",

    # Integrações problemáticas
    "claude_integration.py",
    "rag_integration.py",
    "rag_smart_manager.py",
    "digilibrary_integration.py",

    # OCR problemático
    "ocr_reader.py",
    "ocr_ai_corrector.py",
    "pdf_detector.py",

    # Normalizadores
    "screenplay_normalizer.py",
    "producer_director_system.py",

    # Forensic próprio
    "forensic_monitor.py",
    "forensic_notifier.py",
    "forensic_quick_analyzer.py",

    # Visualização problemática
    "memory_visualization_dashboard.py",

    # DigiLang simples mas problemáticos
    "digilang_simple.py",
    "digilang_enhanced.py",
    "digilang_dictionary.py",
    "tpd_multilayer_pt.py",

    # Bibliotecas quick
    "quick_biblioteca_check.py",
    "quick_quantum_test.py"
]

def categorize_file(filename):
    """Categoriza arquivo baseado no nome."""
    name_lower = filename.lower()

    if "memory" in name_lower:
        return "memory"
    elif "digilang" in name_lower:
        return "digilang"
    elif "monitor" in name_lower or "telemetry" in name_lower:
        return "monitoring"
    elif "test" in name_lower:
        return "test"
    elif "harmony" in name_lower or "synergy" in name_lower:
        return "harmony"
    elif "ollama" in name_lower:
        return "ollama"
    elif "telepathy" in name_lower or "telepathic" in name_lower:
        return "telepathy"
    elif "soul" in name_lower or "consciousness" in name_lower or "immortal" in name_lower:
        return "soul"
    elif "script_doctor" in name_lower or "doctor" in name_lower:
        return "script_doctor"
    else:
        return "misc"

# Estatísticas
moved_count = 0
not_found_count = 0
already_moved = 0

print("🚀 Iniciando transferência de arquivos problemáticos...")
print(f"📁 Total de arquivos para mover: {len(problematic_files)}")
print("-" * 60)

# Mover arquivos
for filename in problematic_files:
    source = SOURCE_BASE / filename
    category = categorize_file(filename)
    dest_folder = categories[category]
    dest = dest_folder / filename

    if source.exists():
        if not dest.exists():
            try:
                shutil.move(str(source), str(dest))
                moved_count += 1
                print(f"✅ Movido: {filename} → {category}/")
            except Exception as e:
                print(f"❌ Erro ao mover {filename}: {e}")
        else:
            already_moved += 1
            print(f"⚠️ Já existe: {filename} em {category}/")
    else:
        # Tentar encontrar em apps/scripturemon (caso esteja lá)
        alt_source = Path(f"/Users/clubproducoes/Digimundo/scripturemon-champion/apps/scripturemon/{filename}")
        if alt_source.exists():
            try:
                shutil.move(str(alt_source), str(dest))
                moved_count += 1
                print(f"✅ Movido (alt): {filename} → {category}/")
            except Exception as e:
                print(f"❌ Erro ao mover {filename}: {e}")
        else:
            not_found_count += 1
            print(f"❓ Não encontrado: {filename}")

print("-" * 60)
print("\n📊 RESUMO DA OPERAÇÃO:")
print(f"✅ Arquivos movidos: {moved_count}")
print(f"⚠️ Já movidos anteriormente: {already_moved}")
print(f"❓ Não encontrados: {not_found_count}")
print(f"📁 Total processado: {len(problematic_files)}")

# Criar relatório
report_path = DEST_BASE / "TRANSFER_REPORT.md"
with open(report_path, "w") as f:
    f.write("# 📋 RELATÓRIO DE TRANSFERÊNCIA - ARQUIVOS PROBLEMÁTICOS\n\n")
    f.write(f"**Data:** {os.popen('date').read().strip()}\n")
    f.write(f"**Total de arquivos:** {len(problematic_files)}\n\n")
    f.write("## 📊 Estatísticas\n\n")
    f.write(f"- ✅ Movidos com sucesso: {moved_count}\n")
    f.write(f"- ⚠️ Já existiam no destino: {already_moved}\n")
    f.write(f"- ❓ Não encontrados: {not_found_count}\n\n")
    f.write("## 📁 Estrutura Criada\n\n")
    for cat, path in categories.items():
        count = len(list(path.glob("*.py")))
        f.write(f"- **{cat}/** - {count} arquivos\n")
    f.write("\n## 🎯 Decisão\n\n")
    f.write("Todos estes arquivos foram identificados como **QUEBRADOS** ")
    f.write("pela análise forense com os seguintes vícios:\n\n")
    f.write("- Imports imaginários\n")
    f.write("- Complexidade desnecessária (quantum/blockchain)\n")
    f.write("- God classes (500+ linhas)\n")
    f.write("- Memory leaks\n")
    f.write("- Duplicação compulsiva\n\n")
    f.write("## ✨ Próximos Passos\n\n")
    f.write("1. Manter apenas OmniMemory V4 como sistema de memória\n")
    f.write("2. Usar DigiLang v26 como versão principal\n")
    f.write("3. Deletar ou refatorar os arquivos movidos\n")

print(f"\n📄 Relatório salvo em: {report_path}")
print("\n✨ TRANSFERÊNCIA COMPLETA!")
print("🎯 Recomendação: Todos esses arquivos podem ser DELETADOS")
print("    pois suas funcionalidades já estão no OmniMemory V4")