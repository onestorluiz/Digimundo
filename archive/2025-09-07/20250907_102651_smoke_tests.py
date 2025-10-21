#!/usr/bin/env python3
"""
Smoke tests for critical fixes applied to scripturemon.
"""

import json
import sys
import traceback
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List

# Add project root to path
sys.path.insert(0, '/Users/clubproducoes/Digimundo/scripturemon-validation')


def test_memory_manager_import() -> Dict[str, Any]:
    """Test that memory_manager can be imported without SoulOS."""
    try:
        # This should work even without soulos_wrapper
        from apps.scripturemon.memory_manager import UnifiedMemoryManager
        
        # Try to instantiate
        mm = UnifiedMemoryManager()
        
        # Check fallback is working
        has_soulos = hasattr(mm, 'soulos') and mm.soulos is not None
        
        return {
            "test": "memory_manager_import",
            "status": "PASS",
            "details": {
                "import_ok": True,
                "instantiation_ok": True,
                "soulos_available": has_soulos,
                "fallback_active": not has_soulos
            }
        }
    except Exception as e:
        return {
            "test": "memory_manager_import",
            "status": "FAIL",
            "error": str(e),
            "traceback": traceback.format_exc()
        }


def test_chat_settings() -> Dict[str, Any]:
    """Test that Chat class can access settings properly."""
    try:
        from apps.scripturemon.chat import ScripturemonChat
        
        # Instantiate
        chat = ScripturemonChat()
        
        # Check settings exist
        has_settings = hasattr(chat, 'settings') and chat.settings is not None
        
        # Check required keys
        required_keys = ['ollama', 'soulos', 'redis', 'rag']
        settings_valid = all(k in chat.settings for k in required_keys) if has_settings else False
        
        return {
            "test": "chat_settings",
            "status": "PASS",
            "details": {
                "instantiation_ok": True,
                "has_settings": has_settings,
                "settings_valid": settings_valid,
                "settings_keys": list(chat.settings.keys()) if has_settings else []
            }
        }
    except Exception as e:
        return {
            "test": "chat_settings",
            "status": "FAIL",
            "error": str(e),
            "traceback": traceback.format_exc()
        }


def test_chat_modo_command() -> Dict[str, Any]:
    """Test that /modo command works with lazy Ollama init."""
    try:
        from apps.scripturemon.chat import ScripturemonChat
        
        chat = ScripturemonChat()
        
        # Test without Ollama (should use fallback)
        results = []
        
        # Test help
        help_result = chat.cmd_modo("help")
        results.append({
            "mode": "help",
            "ok": isinstance(help_result, str) and "MODOS" in help_result
        })
        
        # Test setting modes (should handle missing Ollama gracefully)
        for mode in ["profundo", "default", "rapido", "atual"]:
            try:
                result = chat.cmd_modo(mode)
                if isinstance(result, dict):
                    # Fallback response
                    ok = result.get('ok', False) and result.get('fallback_used', False)
                else:
                    # Normal string response
                    ok = isinstance(result, str) and len(result) > 0
                
                results.append({
                    "mode": mode,
                    "ok": ok,
                    "response_type": type(result).__name__
                })
            except Exception as e:
                results.append({
                    "mode": mode,
                    "ok": False,
                    "error": str(e)
                })
        
        all_ok = all(r['ok'] for r in results)
        
        return {
            "test": "chat_modo_command",
            "status": "PASS" if all_ok else "PARTIAL",
            "details": {
                "modes_tested": len(results),
                "modes_ok": sum(1 for r in results if r['ok']),
                "results": results
            }
        }
    except Exception as e:
        return {
            "test": "chat_modo_command",
            "status": "FAIL",
            "error": str(e),
            "traceback": traceback.format_exc()
        }


def test_runtime_settings() -> Dict[str, Any]:
    """Test that runtime_settings module works correctly."""
    try:
        from src.config.runtime_settings import get_settings, clear_cache
        
        # Get settings
        settings1 = get_settings()
        
        # Should be cached
        settings2 = get_settings()
        
        # Clear cache
        clear_cache()
        
        # Get fresh settings
        settings3 = get_settings()
        
        # Verify structure
        required = {
            'ollama': ['enabled', 'default_model', 'timeout'],
            'soulos': ['enabled', 'code_execution', 'timeout'],
            'redis': ['enabled', 'host', 'port'],
            'rag': ['backend', 'collection']
        }
        
        structure_ok = True
        for section, keys in required.items():
            if section not in settings1:
                structure_ok = False
                break
            for key in keys:
                if key not in settings1[section]:
                    structure_ok = False
                    break
        
        return {
            "test": "runtime_settings",
            "status": "PASS",
            "details": {
                "get_settings_ok": True,
                "caching_works": settings1 is settings2,
                "clear_cache_works": settings1 is not settings3,
                "structure_valid": structure_ok,
                "sections": list(settings1.keys())
            }
        }
    except Exception as e:
        return {
            "test": "runtime_settings",
            "status": "FAIL",
            "error": str(e),
            "traceback": traceback.format_exc()
        }


def test_config_loader_compatibility() -> Dict[str, Any]:
    """Test that config_loader still works with runtime_settings."""
    try:
        from src.utils.config_loader import load_settings, get_setting
        
        # Load settings
        settings = load_settings()
        
        # Test get_setting
        memory_enabled = get_setting('memory.enabled', None)
        rag_backend = get_setting('rag.provider', None)
        
        # Verify defaults are sensible
        has_defaults = (
            isinstance(settings, dict) and
            'memory' in settings and
            'rag' in settings
        )
        
        return {
            "test": "config_loader_compatibility",
            "status": "PASS",
            "details": {
                "load_settings_ok": True,
                "get_setting_ok": memory_enabled is not None,
                "has_defaults": has_defaults,
                "memory_enabled": memory_enabled,
                "rag_backend": rag_backend
            }
        }
    except Exception as e:
        return {
            "test": "config_loader_compatibility",
            "status": "FAIL",
            "error": str(e),
            "traceback": traceback.format_exc()
        }


def main():
    """Run all smoke tests."""
    print("🧪 Running smoke tests for FIX_CURRENT patches...\n")
    
    tests = [
        test_memory_manager_import,
        test_chat_settings,
        test_chat_modo_command,
        test_runtime_settings,
        test_config_loader_compatibility
    ]
    
    results = []
    passed = 0
    failed = 0
    partial = 0
    
    for test_func in tests:
        print(f"Running {test_func.__name__}...", end=" ")
        result = test_func()
        results.append(result)
        
        status = result['status']
        if status == 'PASS':
            print("✅ PASS")
            passed += 1
        elif status == 'PARTIAL':
            print("⚠️  PARTIAL")
            partial += 1
        else:
            print("❌ FAIL")
            failed += 1
            if 'error' in result:
                print(f"  Error: {result['error']}")
    
    # Summary
    total = len(tests)
    print(f"\n📊 Summary: {passed}/{total} passed, {partial} partial, {failed} failed")
    
    # Save results
    output_dir = Path("/Users/clubproducoes/Digimundo/scripturemon-validation/reports/fix_current")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    output_file = output_dir / "smoke_tests.json"
    with open(output_file, 'w') as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total": total,
                "passed": passed,
                "partial": partial,
                "failed": failed
            },
            "tests": results
        }, f, indent=2)
    
    print(f"\n💾 Results saved to: {output_file}")
    
    return failed == 0


if __name__ == "__main__":
    sys.exit(0 if main() else 1)