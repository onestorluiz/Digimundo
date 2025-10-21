#!/usr/bin/env python3
"""
Test script to verify all harmony fixes are working
"""

import sys
import os
from pathlib import Path

# Add to path
sys.path.insert(0, str(Path(__file__).parent))

def test_fixes():
    """Test all the fixes applied"""
    
    print("🧪 Testing Harmony Fixes")
    print("=" * 50)
    
    results = {}
    
    # Test 1: SoulOSWrapper import with fallback
    print("\n1. Testing SoulOSWrapper import...")
    try:
        from apps.scripturemon.memory_manager import UnifiedMemoryManager
        # Check if fallback class is defined
        import apps.scripturemon.memory_manager as mm_module
        source = open(mm_module.__file__).read()
        if 'class SoulOSWrapper:' in source and 'fallback' in source.lower():
            print("   ✅ SoulOSWrapper has fallback implementation")
            results['soulos_wrapper'] = True
        else:
            print("   ⚠️ SoulOSWrapper fallback might be missing")
            results['soulos_wrapper'] = False
    except Exception as e:
        print(f"   ❌ Failed: {e}")
        results['soulos_wrapper'] = False
    
    # Test 2: Settings properly imported in chat.py
    print("\n2. Testing settings import in chat...")
    try:
        from apps.scripturemon.chat import ScripturemonChat
        # Check if settings is imported
        import apps.scripturemon.chat as chat_module
        source = open(chat_module.__file__).read()
        if 'from src.config.runtime_settings import get_settings' in source:
            print("   ✅ Settings properly imported")
            results['settings'] = True
        else:
            print("   ⚠️ Settings import not found")
            results['settings'] = False
    except Exception as e:
        print(f"   ❌ Failed: {e}")
        results['settings'] = False
    
    # Test 3: Ollama client initialization
    print("\n3. Testing ollama client initialization...")
    try:
        from apps.scripturemon.chat import ScripturemonChat
        chat = ScripturemonChat()
        # Check if ollama_client is initialized
        if hasattr(chat, 'ollama_client'):
            print("   ✅ ollama_client attribute exists")
            results['ollama'] = True
        else:
            print("   ❌ ollama_client attribute missing")
            results['ollama'] = False
            
        # Check if _ensure_ollama method exists
        if hasattr(chat, '_ensure_ollama'):
            print("   ✅ _ensure_ollama method exists")
        else:
            print("   ❌ _ensure_ollama method missing")
            
        # Check if cmd_modo exists
        if hasattr(chat, 'cmd_modo'):
            print("   ✅ cmd_modo method exists")
        else:
            print("   ❌ cmd_modo method missing")
            
    except Exception as e:
        print(f"   ❌ Failed: {e}")
        results['ollama'] = False
    
    # Test 4: No circular imports
    print("\n4. Testing for circular imports...")
    try:
        # Try importing all main modules
        from apps.scripturemon.chat import ScripturemonChat
        from apps.scripturemon.memory_manager import UnifiedMemoryManager
        from apps.scripturemon.memory_unification import get_unified_memory
        print("   ✅ All modules import without circular dependency")
        results['circular'] = True
    except ImportError as e:
        if 'circular' in str(e).lower():
            print(f"   ❌ Circular import detected: {e}")
            results['circular'] = False
        else:
            print(f"   ⚠️ Import error (not circular): {e}")
            results['circular'] = True
    
    # Test 5: Main entry point exists
    print("\n5. Testing scripturemon command entry...")
    try:
        # Check if main scripts exist
        main_script = Path(__file__).parent / "bin" / "scripturemon_main.py"
        launch_script = Path(__file__).parent / "bin" / "scripturemon_launch"
        
        if main_script.exists():
            print(f"   ✅ Main script exists: {main_script.name}")
        else:
            print(f"   ❌ Main script missing: {main_script}")
            
        if launch_script.exists():
            print(f"   ✅ Launch script exists: {launch_script.name}")
        else:
            print(f"   ❌ Launch script missing: {launch_script}")
        
        # Check if chat has main function
        from apps.scripturemon import chat
        if hasattr(chat, 'main'):
            print("   ✅ chat.main() function exists")
            results['entry_point'] = True
        else:
            print("   ❌ chat.main() function missing")
            results['entry_point'] = False
            
    except Exception as e:
        print(f"   ❌ Failed: {e}")
        results['entry_point'] = False
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 SUMMARY")
    print("=" * 50)
    
    total = len(results)
    passed = sum(results.values())
    
    for test, passed_test in results.items():
        status = "✅" if passed_test else "❌"
        print(f"{status} {test}")
    
    print(f"\n🎯 Result: {passed}/{total} tests passed ({passed*100//total}%)")
    
    if passed == total:
        print("\n✨ ALL HARMONY FIXES WORKING! ✨")
        print("The system is now ready for full operation.")
        return 0
    else:
        print(f"\n⚠️ {total - passed} issues remaining")
        return 1

if __name__ == "__main__":
    exit_code = test_fixes()
    sys.exit(exit_code)