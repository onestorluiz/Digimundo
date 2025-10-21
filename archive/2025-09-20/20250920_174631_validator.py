#!/usr/bin/env python3
"""
Validator Module - Sistema de Validação de Saúde (Stub para Fase 1.C)
Validação complexa e profunda do sistema
"""

import time
import sys
import os
import json
from typing import Dict, Any, List, Tuple, Optional
from pathlib import Path
import hashlib

# Estado global de validação
_validation_state = {
    "last_check": None,
    "check_count": 0,
    "issues_found": [],
    "health_history": [],
    "thresholds": {
        "critical": 0.3,
        "warning": 0.6,
        "healthy": 0.8
    }
}

def health_once() -> Dict[str, Any]:
    """
    Executa verificação de saúde única e completa
    Sistema complexo de diagnóstico
    """
    start_time = time.time()
    _validation_state["check_count"] += 1
    
    results = {
        "timestamp": time.time(),
        "check_id": f"health_{_validation_state['check_count']}",
        "components": {},
        "issues": [],
        "metrics": {},
        "recommendations": []
    }
    
    # Verificar componentes principais
    components_status = {
        "python": _check_python(),
        "imports": _check_imports(),
        "filesystem": _check_filesystem(),
        "memory": _check_memory(),
        "models": _check_models(),
        "configuration": _check_configuration(),
        "dependencies": _check_dependencies()
    }
    
    results["components"] = components_status
    
    # Calcular saúde geral
    total_score = sum(c["score"] for c in components_status.values())
    component_count = len(components_status)
    overall_score = total_score / component_count
    
    # Determinar status
    if overall_score >= _validation_state["thresholds"]["healthy"]:
        status = "healthy"
        level = "info"
    elif overall_score >= _validation_state["thresholds"]["warning"]:
        status = "warning"
        level = "warning"
    else:
        status = "critical"
        level = "error"
    
    results["overall"] = {
        "score": overall_score,
        "status": status,
        "level": level
    }
    
    # Coletar métricas do sistema
    results["metrics"] = _collect_metrics()
    
    # Gerar recomendações baseadas nos problemas
    for component, data in components_status.items():
        if data["score"] < 0.8:
            results["recommendations"].append({
                "component": component,
                "action": data.get("recommendation", f"Verificar {component}"),
                "priority": "high" if data["score"] < 0.5 else "medium"
            })
    
    # Adicionar ao histórico
    _validation_state["last_check"] = time.time()
    _validation_state["health_history"].append({
        "timestamp": results["timestamp"],
        "score": overall_score,
        "status": status
    })
    
    # Manter apenas últimas 100 verificações
    if len(_validation_state["health_history"]) > 100:
        _validation_state["health_history"] = _validation_state["health_history"][-100:]
    
    results["duration"] = time.time() - start_time
    
    return results

def _check_python() -> Dict[str, Any]:
    """Verifica ambiente Python"""
    try:
        version = sys.version
        version_info = sys.version_info
        
        # Python 3.8+ recomendado
        if version_info.major == 3 and version_info.minor >= 8:
            score = 1.0
        elif version_info.major == 3:
            score = 0.7
        else:
            score = 0.3
        
        return {
            "score": score,
            "version": version,
            "path": sys.executable,
            "status": "ok" if score > 0.7 else "outdated",
            "recommendation": "Atualizar para Python 3.8+" if score < 0.8 else None
        }
    except Exception as e:
        return {
            "score": 0.0,
            "error": str(e),
            "status": "error"
        }

def _check_imports() -> Dict[str, Any]:
    """Verifica imports críticos"""
    critical_modules = [
        "typer",
        "pathlib",
        "json",
        "concurrent.futures",
        "multiprocessing"
    ]
    
    successful = 0
    failed = []
    
    for module in critical_modules:
        try:
            __import__(module)
            successful += 1
        except ImportError:
            failed.append(module)
    
    score = successful / len(critical_modules)
    
    return {
        "score": score,
        "total": len(critical_modules),
        "successful": successful,
        "failed": failed,
        "status": "ok" if score == 1.0 else "incomplete",
        "recommendation": f"Instalar módulos: {', '.join(failed)}" if failed else None
    }

def _check_filesystem() -> Dict[str, Any]:
    """Verifica sistema de arquivos"""
    required_dirs = ["apps", "bin", "data", "runtime", "backups", "logs"]
    base_path = Path(__file__).parent.parent.parent
    
    existing = 0
    missing = []
    
    for dir_name in required_dirs:
        dir_path = base_path / dir_name
        if dir_path.exists():
            existing += 1
        else:
            missing.append(dir_name)
    
    score = existing / len(required_dirs)
    
    # Verificar permissões de escrita
    writable = True
    try:
        test_file = base_path / "test_write.tmp"
        test_file.touch()
        test_file.unlink()
    except:
        writable = False
        score *= 0.5
    
    return {
        "score": score,
        "required_dirs": len(required_dirs),
        "existing": existing,
        "missing": missing,
        "writable": writable,
        "base_path": str(base_path),
        "status": "ok" if score > 0.8 else "issues",
        "recommendation": f"Criar diretórios: {', '.join(missing)}" if missing else None
    }

def _check_memory() -> Dict[str, Any]:
    """Verifica uso de memória"""
    try:
        import psutil
        
        memory = psutil.virtual_memory()
        score = 1.0 - (memory.percent / 100)
        
        return {
            "score": score,
            "total_gb": memory.total / (1024**3),
            "available_gb": memory.available / (1024**3),
            "percent_used": memory.percent,
            "status": "ok" if score > 0.3 else "low",
            "recommendation": "Liberar memória" if score < 0.3 else None
        }
    except:
        # Fallback se psutil não disponível
        return {
            "score": 0.7,
            "status": "unknown",
            "note": "psutil não disponível"
        }

def _check_models() -> Dict[str, Any]:
    """Verifica modelos Ollama"""
    try:
        # Simular verificação de modelos
        import subprocess
        result = subprocess.run(
            ["ollama", "list"],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            # Contar modelos
            lines = result.stdout.strip().split('\n')
            model_count = max(0, len(lines) - 1)  # Menos header
            
            score = min(1.0, model_count / 3)  # Pelo menos 3 modelos
            
            return {
                "score": score,
                "count": model_count,
                "status": "ok" if model_count > 0 else "no_models",
                "recommendation": "Instalar modelos com 'ollama pull'" if model_count < 3 else None
            }
    except:
        pass
    
    return {
        "score": 0.5,
        "status": "ollama_not_found",
        "recommendation": "Instalar Ollama"
    }

def _check_configuration() -> Dict[str, Any]:
    """Verifica arquivos de configuração"""
    config_files = ["REGRAS.md", "DECISOES.md", "ARQUIVOS_CHECKUP.md"]
    base_path = Path(__file__).parent.parent.parent
    
    found = 0
    missing = []
    
    for config in config_files:
        if (base_path / config).exists():
            found += 1
        else:
            missing.append(config)
    
    score = found / len(config_files)
    
    return {
        "score": score,
        "expected": len(config_files),
        "found": found,
        "missing": missing,
        "status": "configured" if score == 1.0 else "incomplete",
        "recommendation": f"Criar arquivos: {', '.join(missing)}" if missing else None
    }

def _check_dependencies() -> Dict[str, Any]:
    """Verifica dependências do sistema"""
    try:
        # Verificar se CLI funciona
        from apps.scripturemon.cli_champion import app
        cli_ok = True
    except:
        cli_ok = False
    
    try:
        # Verificar bootstrap
        from apps.scripturemon.bootstrap import ensure_bootstrap_once
        bootstrap_ok = True
    except:
        bootstrap_ok = False
    
    score = (1.0 if cli_ok else 0.0) * 0.5 + (1.0 if bootstrap_ok else 0.0) * 0.5
    
    return {
        "score": score,
        "cli": "ok" if cli_ok else "error",
        "bootstrap": "ok" if bootstrap_ok else "error",
        "status": "ready" if score == 1.0 else "incomplete",
        "recommendation": "Verificar imports dos módulos" if score < 1.0 else None
    }

def _collect_metrics() -> Dict[str, Any]:
    """Coleta métricas gerais do sistema"""
    base_path = Path(__file__).parent.parent.parent
    
    # Contar arquivos
    py_files = list(base_path.glob("**/*.py"))
    md_files = list(base_path.glob("**/*.md"))
    
    return {
        "python_files": len(py_files),
        "markdown_files": len(md_files),
        "total_files": len(py_files) + len(md_files),
        "check_count": _validation_state["check_count"],
        "last_check": _validation_state["last_check"],
        "health_history_size": len(_validation_state["health_history"])
    }

def get_health_history(limit: int = 10) -> List[Dict[str, Any]]:
    """Retorna histórico de saúde"""
    return _validation_state["health_history"][-limit:]

def get_validation_report() -> Dict[str, Any]:
    """Gera relatório completo de validação"""
    current = health_once()
    history = get_health_history(20)
    
    # Calcular tendência
    if len(history) >= 2:
        recent_scores = [h["score"] for h in history[-5:]]
        older_scores = [h["score"] for h in history[-10:-5]] if len(history) >= 10 else [history[0]["score"]]
        
        recent_avg = sum(recent_scores) / len(recent_scores)
        older_avg = sum(older_scores) / len(older_scores)
        
        if recent_avg > older_avg + 0.1:
            trend = "improving"
        elif recent_avg < older_avg - 0.1:
            trend = "degrading"
        else:
            trend = "stable"
    else:
        trend = "insufficient_data"
    
    return {
        "current": current,
        "history": history,
        "trend": trend,
        "total_checks": _validation_state["check_count"],
        "system_age": time.time() - (_validation_state["health_history"][0]["timestamp"] if _validation_state["health_history"] else time.time())
    }

__all__ = ["health_once", "get_health_history", "get_validation_report"]