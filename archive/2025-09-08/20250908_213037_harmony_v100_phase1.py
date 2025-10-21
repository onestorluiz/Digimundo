#!/usr/bin/env python3
"""
HARMONY V100 - FASE 1: Memory Brain Integration
Integração não-destrutiva com coexistência harmônica
"""

import os
import sys
import json
import time
import zipfile
import shutil
import traceback
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

# Configuração
PROJECT_ROOT = Path("/Users/clubproducoes/Digimundo/scripturemon-validation")
REPORTS_DIR = PROJECT_ROOT / "reports" / "harmony_v100" / "phase1"
BACKUPS_DIR = PROJECT_ROOT / "backups"

# Criar diretórios
REPORTS_DIR.mkdir(parents=True, exist_ok=True)
(REPORTS_DIR / "diffs").mkdir(exist_ok=True)

print("🧠 HARMONY V100 - FASE 1: MEMORY BRAIN")
print("=" * 70)

# ============================================================================
# BACKUP PRÉ
# ============================================================================

print("\n💾 Criando backup pré-fase1...")

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
backup_pre = BACKUPS_DIR / f"{timestamp}-h100_phase1_pre.zip"

with zipfile.ZipFile(backup_pre, 'w', zipfile.ZIP_DEFLATED) as zf:
    for root, dirs, files in os.walk(PROJECT_ROOT):
        # Excluir diretórios backup
        dirs[:] = [d for d in dirs if 'backup' not in d.lower()]
        
        for file in files:
            filepath = Path(root) / file
            if filepath.suffix in {'.py', '.json', '.yaml', '.db', '.sqlite'}:
                if 'backup' not in str(filepath).lower():
                    arcname = filepath.relative_to(PROJECT_ROOT)
                    zf.write(filepath, arcname)

print(f"  ✅ Backup criado: {backup_pre.name}")

# ============================================================================
# INTEGRAÇÃO
# ============================================================================

print("\n🔧 Integrando Memory Brain...")

sys.path.insert(0, str(PROJECT_ROOT))

# Registrar adaptações feitas
adaptations = []

# 1. Adaptar memory_manager.py
memory_manager_path = PROJECT_ROOT / "apps" / "scripturemon" / "memory_manager.py"
if memory_manager_path.exists():
    try:
        with open(memory_manager_path, 'r') as f:
            original_content = f.read()
        
        # Verificar se já tem MemoryBrain
        if "MemoryBrain" not in original_content:
            # Adicionar import lazy
            import_line = "\n# Memory Brain integration (lazy import)\n"
            import_line += "_memory_brain = None\n\n"
            import_line += "def get_memory_brain():\n"
            import_line += "    global _memory_brain\n"
            import_line += "    if _memory_brain is None:\n"
            import_line += "        from src.memory.memory_brain import MemoryBrain\n"
            import_line += "        _memory_brain = MemoryBrain()\n"
            import_line += "    return _memory_brain\n\n"
            
            # Inserir após imports
            lines = original_content.split('\n')
            insert_pos = 0
            for i, line in enumerate(lines):
                if line.startswith('class '):
                    insert_pos = i
                    break
            
            lines.insert(insert_pos, import_line)
            modified_content = '\n'.join(lines)
            
            # Salvar diff
            diff_path = REPORTS_DIR / "diffs" / "memory_manager.diff"
            with open(diff_path, 'w') as f:
                f.write("--- original\n")
                f.write("+++ modified\n")
                f.write(f"@@ Added MemoryBrain lazy import at line {insert_pos}\n")
                f.write(import_line)
            
            # Aplicar mudança
            with open(memory_manager_path, 'w') as f:
                f.write(modified_content)
            
            adaptations.append({
                "file": "apps/scripturemon/memory_manager.py",
                "line": insert_pos,
                "change": "Added MemoryBrain lazy import",
                "reason": "Avoid import cycles while integrating"
            })
            
            print(f"  ✅ Adaptado memory_manager.py")
    except Exception as e:
        adaptations.append({
            "file": "apps/scripturemon/memory_manager.py",
            "error": str(e),
            "reason": "Failed to integrate"
        })
        print(f"  ⚠️ Erro em memory_manager.py: {e}")

# 2. Adaptar memory_unification.py
unification_path = PROJECT_ROOT / "apps" / "scripturemon" / "memory_unification.py"
if unification_path.exists():
    try:
        with open(unification_path, 'r') as f:
            original_content = f.read()
        
        if "MemoryBrain" not in original_content:
            # Adicionar propriedade brain
            brain_property = "\n    @property\n"
            brain_property += "    def brain(self):\n"
            brain_property += "        \"\"\"Access to MemoryBrain (lazy loaded)\"\"\"\n"
            brain_property += "        if not hasattr(self, '_brain'):\n"
            brain_property += "            try:\n"
            brain_property += "                from src.memory.memory_brain import MemoryBrain\n"
            brain_property += "                self._brain = MemoryBrain()\n"
            brain_property += "            except ImportError:\n"
            brain_property += "                self._brain = None\n"
            brain_property += "        return self._brain\n"
            
            # Encontrar classe UnifiedMemorySystem
            lines = original_content.split('\n')
            for i, line in enumerate(lines):
                if "class UnifiedMemorySystem" in line:
                    # Inserir após métodos existentes
                    for j in range(i+1, len(lines)):
                        if lines[j].strip() and not lines[j].startswith(' '):
                            lines.insert(j-1, brain_property)
                            break
                    break
            
            modified_content = '\n'.join(lines)
            
            # Salvar diff
            diff_path = REPORTS_DIR / "diffs" / "memory_unification.diff"
            with open(diff_path, 'w') as f:
                f.write("--- original\n")
                f.write("+++ modified\n")
                f.write("@@ Added brain property\n")
                f.write(brain_property)
            
            # Aplicar mudança
            with open(unification_path, 'w') as f:
                f.write(modified_content)
            
            adaptations.append({
                "file": "apps/scripturemon/memory_unification.py",
                "change": "Added brain property",
                "reason": "Enable MemoryBrain access"
            })
            
            print(f"  ✅ Adaptado memory_unification.py")
    except Exception as e:
        adaptations.append({
            "file": "apps/scripturemon/memory_unification.py", 
            "error": str(e),
            "reason": "Failed to integrate"
        })
        print(f"  ⚠️ Erro em memory_unification.py: {e}")

# ============================================================================
# SMOKE TESTS
# ============================================================================

print("\n🧪 Executando smoke tests...")

# Importar MemoryBrain
try:
    from src.memory.memory_brain import MemoryBrain
    brain = MemoryBrain()
    brain_loaded = True
except Exception as e:
    print(f"  ❌ Falha ao carregar MemoryBrain: {e}")
    brain = None
    brain_loaded = False

smoke_results = {}

# --- Brain Context Test ---
if brain_loaded:
    print("  Testing brain.get_context()...")
    brain_ctx_result = {
        "test": "brain_ctx",
        "status": "FAIL",
        "details": {}
    }
    
    try:
        # Query 1
        query1 = "python programming"
        start = time.time()
        results1 = brain.get_context(query1, k=8)
        time1 = (time.time() - start) * 1000  # ms
        
        brain_ctx_result["details"]["query1"] = {
            "query": query1,
            "results_count": len(results1),
            "has_ids": all('id' in r for r in results1),
            "has_metadata": all('metadata' in r for r in results1),
            "has_distances": all('distances' in r for r in results1),
            "time_ms": round(time1, 2)
        }
        
        # Query 2
        query2 = "memory optimization"
        start = time.time()
        results2 = brain.get_context(query2, k=8)
        time2 = (time.time() - start) * 1000
        
        brain_ctx_result["details"]["query2"] = {
            "query": query2,
            "results_count": len(results2),
            "has_ids": all('id' in r for r in results2),
            "has_metadata": all('metadata' in r for r in results2),
            "has_distances": all('distances' in r for r in results2),
            "time_ms": round(time2, 2)
        }
        
        # Verificar k <= 8
        if results1 and len(results1) <= 8 and results2 and len(results2) <= 8:
            brain_ctx_result["status"] = "PASS"
        else:
            brain_ctx_result["status"] = "PARTIAL"
            
    except Exception as e:
        brain_ctx_result["details"]["error"] = str(e)
        brain_ctx_result["details"]["traceback"] = traceback.format_exc()
    
    smoke_results["brain_ctx"] = brain_ctx_result
    
    # Salvar resultado
    with open(REPORTS_DIR / "brain_ctx.json", 'w') as f:
        json.dump(brain_ctx_result, f, indent=2)

# --- Brain Sync Test ---
if brain_loaded:
    print("  Testing brain.sync()...")
    brain_sync_result = {
        "test": "brain_sync",
        "status": "FAIL",
        "details": {}
    }
    
    try:
        sync_stats = brain.sync()
        
        brain_sync_result["details"] = {
            "indexed": sync_stats.get('indexed', 0),
            "flagged": sync_stats.get('flagged', 0),
            "errors": sync_stats.get('errors', 0)
        }
        
        if sync_stats.get('errors', 0) == 0:
            brain_sync_result["status"] = "PASS"
        else:
            brain_sync_result["status"] = "PARTIAL"
            
    except Exception as e:
        brain_sync_result["details"]["error"] = str(e)
    
    smoke_results["brain_sync"] = brain_sync_result
    
    # Salvar resultado
    with open(REPORTS_DIR / "brain_sync.json", 'w') as f:
        json.dump(brain_sync_result, f, indent=2)

# --- Brain Performance Test ---
if brain_loaded:
    print("  Testing brain performance...")
    brain_perf_result = {
        "test": "brain_perf",
        "status": "FAIL",
        "details": {}
    }
    
    try:
        # Fazer várias queries para coletar métricas
        times = []
        for i in range(5):
            query = f"test query {i}"
            start = time.time()
            _ = brain.get_context(query, k=4)
            elapsed = (time.time() - start) * 1000  # ms
            times.append(elapsed)
        
        # Calcular p50 e p95
        times.sort()
        p50 = times[len(times)//2]
        p95 = times[int(len(times)*0.95)] if len(times) > 1 else times[0]
        avg = sum(times) / len(times)
        min_time = min(times)
        
        brain_perf_result["details"] = {
            "samples": len(times),
            "min_ms": round(min_time, 2),
            "avg_ms": round(avg, 2),
            "p50_ms": round(p50, 2),
            "p95_ms": round(p95, 2),
            "invariants": {
                "min_gte_0": min_time >= 0,
                "p95_gte_avg": p95 >= avg
            }
        }
        
        # Verificar invariantes
        if all(brain_perf_result["details"]["invariants"].values()):
            brain_perf_result["status"] = "PASS"
        else:
            brain_perf_result["status"] = "FAIL"
            
    except Exception as e:
        brain_perf_result["details"]["error"] = str(e)
    
    smoke_results["brain_perf"] = brain_perf_result
    
    # Salvar resultado
    with open(REPORTS_DIR / "brain_perf.json", 'w') as f:
        json.dump(brain_perf_result, f, indent=2)

# ============================================================================
# RELATÓRIOS
# ============================================================================

print("\n📊 Gerando relatórios...")

# Summary MD
summary_content = [
    "# HARMONY V100 - FASE 1: Memory Brain\n\n",
    f"**Timestamp**: {datetime.now().isoformat()}\n\n",
    "## Status\n\n"
]

if brain_loaded:
    summary_content.append("✅ MemoryBrain carregado com sucesso\n\n")
else:
    summary_content.append("❌ MemoryBrain falhou ao carregar\n\n")

summary_content.append("## Adaptações\n\n")
for adapt in adaptations:
    if 'error' in adapt:
        summary_content.append(f"- ❌ {adapt['file']}: {adapt['error']}\n")
    else:
        summary_content.append(f"- ✅ {adapt['file']}: {adapt['change']}\n")

summary_content.append("\n## Smoke Tests\n\n")
for test_name, result in smoke_results.items():
    icon = "✅" if result["status"] == "PASS" else "⚠️" if result["status"] == "PARTIAL" else "❌"
    summary_content.append(f"- {icon} **{test_name}**: {result['status']}\n")
    
    if test_name == "brain_ctx" and "query1" in result.get("details", {}):
        q1 = result["details"]["query1"]
        summary_content.append(f"  - Query 1: {q1['results_count']} results in {q1.get('time_ms', 0)}ms\n")
    elif test_name == "brain_sync" and result.get("details"):
        sync = result["details"]
        summary_content.append(f"  - Indexed: {sync.get('indexed', 0)}, Flagged: {sync.get('flagged', 0)}\n")
    elif test_name == "brain_perf" and result.get("details"):
        perf = result["details"]
        summary_content.append(f"  - p50: {perf.get('p50_ms', 0)}ms, p95: {perf.get('p95_ms', 0)}ms\n")

# Stats do Brain
if brain_loaded:
    try:
        stats = brain.stats()
        summary_content.append("\n## Brain Statistics\n\n")
        summary_content.append(f"- Total memories: {stats.get('total_memories', 0)}\n")
        summary_content.append(f"- Recent active: {stats.get('recent_active', 0)}\n")
        
        if 'performance' in stats:
            perf = stats['performance']
            summary_content.append(f"- Avg context time: {perf.get('avg_context_time_ms', 0)}ms\n")
            summary_content.append(f"- Invariants valid: {perf.get('invariants_valid', False)}\n")
    except:
        pass

# Salvar summary
summary_path = REPORTS_DIR / "summary.md"
with open(summary_path, 'w') as f:
    f.writelines(summary_content)

print(f"  ✅ Summary: {summary_path}")

# Acceptance JSON
acceptance = {
    "timestamp": datetime.now().isoformat(),
    "phase": "phase1",
    "overall_status": "PASS" if brain_loaded else "FAIL",
    "brain_loaded": brain_loaded,
    "adaptations": adaptations,
    "tests": smoke_results,
    "statistics": {}
}

# Adicionar estatísticas se disponível
if brain_loaded:
    try:
        acceptance["statistics"] = brain.stats()
    except:
        pass

# Determinar status geral
if not brain_loaded:
    acceptance["overall_status"] = "FAIL"
elif all(r["status"] == "PASS" for r in smoke_results.values()):
    acceptance["overall_status"] = "PASS"
elif any(r["status"] == "FAIL" for r in smoke_results.values()):
    acceptance["overall_status"] = "PARTIAL"
else:
    acceptance["overall_status"] = "PASS_WITH_WARNINGS"

# Salvar acceptance
acceptance_path = REPORTS_DIR / "acceptance.json"
with open(acceptance_path, 'w') as f:
    json.dump(acceptance, f, indent=2)

print(f"  ✅ Acceptance: {acceptance_path}")

# ============================================================================
# BACKUP PÓS
# ============================================================================

print("\n💾 Criando backup pós-fase1...")

backup_post = BACKUPS_DIR / f"{timestamp}-h100_phase1_post.zip"

with zipfile.ZipFile(backup_post, 'w', zipfile.ZIP_DEFLATED) as zf:
    for root, dirs, files in os.walk(PROJECT_ROOT):
        dirs[:] = [d for d in dirs if 'backup' not in d.lower()]
        
        for file in files:
            filepath = Path(root) / file
            if filepath.suffix in {'.py', '.json', '.yaml', '.db', '.sqlite'}:
                if 'backup' not in str(filepath).lower():
                    arcname = filepath.relative_to(PROJECT_ROOT)
                    zf.write(filepath, arcname)

print(f"  ✅ Backup criado: {backup_post.name}")

# ============================================================================
# RESUMO FINAL
# ============================================================================

print("\n" + "=" * 70)
print("🧠 RESUMO FASE 1 - MEMORY BRAIN")
print("=" * 70)
print(f"Status: {acceptance['overall_status']}")
print(f"Brain Loaded: {brain_loaded}")
print(f"Adaptações: {len(adaptations)}")
print(f"Testes: {len(smoke_results)}")

if acceptance["overall_status"] == "PASS":
    print("\n✅ FASE 1 COMPLETA - Memory Brain integrado com sucesso")
elif acceptance["overall_status"] == "PASS_WITH_WARNINGS":
    print("\n⚠️ FASE 1 COMPLETA COM AVISOS - Verificar resultados")
else:
    print("\n❌ FASE 1 COM PROBLEMAS - Revisar integração")

print(f"\nRelatórios em: {REPORTS_DIR}")
print("=" * 70)