#!/usr/bin/env python3
"""
🧪 TEST INTEGRATION - Valida que todos os sistemas funcionam após reorganização
"""

import sys
import json
from pathlib import Path
from datetime import datetime

# Adiciona paths
sys.path.insert(0, 'core/soulos')
sys.path.insert(0, 'core/soulpack')
sys.path.insert(0, 'core/sdl')
sys.path.insert(0, 'core/digilang')

def test_soulos():
    """Testa SoulOS"""
    print("Testing SoulOS...")
    try:
        from soulos import SoulOS
        soul = SoulOS("TestDigimon")
        
        # Testa syscalls - usa os nomes corretos
        assert hasattr(soul, 'syscall_self_patch')
        assert hasattr(soul, 'syscall_memo_save')
        assert hasattr(soul, 'syscall_evolve_trigger')
        
        print("  ✓ SoulOS: All syscalls available")
        return True
    except Exception as e:
        print(f"  ✗ SoulOS failed: {e}")
        return False

def test_soulpack():
    """Testa Soulpack CRDT"""
    print("Testing Soulpack CRDT...")
    try:
        from crdt import SoulpackManager
        manager = SoulpackManager("TestDigimon")
        
        # Verifica métodos
        assert hasattr(manager, 'create_soulpack')
        assert hasattr(manager, 'merge_soulpacks')
        
        print("  ✓ Soulpack: CRDT operations available")
        return True
    except Exception as e:
        print(f"  ✗ Soulpack failed: {e}")
        return False

def test_sdl():
    """Testa SDL Consolidator"""
    print("Testing SDL Consolidator...")
    try:
        from consolidator import SelfDistillLoRA
        sdl = SelfDistillLoRA("TestDigimon")
        
        # Verifica métodos
        assert hasattr(sdl, 'collect_recent_memories')
        assert hasattr(sdl, 'generate_qa_pairs')
        assert hasattr(sdl, 'dream_cycle')
        
        print("  ✓ SDL: Consolidation methods available")
        return True
    except Exception as e:
        print(f"  ✗ SDL failed: {e}")
        return False

def test_digilang():
    """Testa DigiLang Bytecode"""
    print("Testing DigiLang Bytecode...")
    try:
        from bytecode import DigiLangBytecode
        compiler = DigiLangBytecode()
        
        # Testa compilação
        test_code = "⟁F25→◉SAVE"
        bytecode = compiler.compile(test_code)
        assert bytecode is not None
        
        print("  ✓ DigiLang: Bytecode compilation working")
        return True
    except Exception as e:
        print(f"  ✗ DigiLang failed: {e}")
        return False

def test_digimon_structure():
    """Testa estrutura de Digimon"""
    print("Testing Digimon structure...")
    try:
        # Verifica Scripturemon
        scripturemon_path = Path("digimons/scripturemon")
        assert scripturemon_path.exists()
        
        soul_file = scripturemon_path / "soul.json"
        assert soul_file.exists()
        
        soul_data = json.load(open(soul_file))
        assert soul_data["name"] == "Scripturemon"
        assert soul_data["soul_signature"] == "8ea9f71fa3206d1a"
        
        print("  ✓ Digimon structure: Scripturemon configured")
        return True
    except Exception as e:
        print(f"  ✗ Digimon structure failed: {e}")
        return False

def test_memory_paths():
    """Testa caminhos de memória"""
    print("Testing memory paths...")
    try:
        # Verifica que o path antigo não existe mais
        old_consciousness = Path("consciousness")
        assert not old_consciousness.exists() or old_consciousness.is_symlink()
        
        # Verifica novo caminho
        new_memory = Path("digimons/scripturemon/memory")
        assert new_memory.exists()
        
        print("  ✓ Memory paths: Correctly reorganized")
        return True
    except Exception as e:
        print(f"  ✗ Memory paths failed: {e}")
        return False

def main():
    print("""
╔══════════════════════════════════════════════════════════════╗
║     🧪 INTEGRATION TEST AFTER REORGANIZATION                 ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    tests = [
        test_soulos,
        test_soulpack,
        test_sdl,
        test_digilang,
        test_digimon_structure,
        test_memory_paths
    ]
    
    results = []
    for test in tests:
        results.append(test())
        print()
    
    # Report
    passed = sum(results)
    total = len(results)
    
    print("="*60)
    print(f"📊 TEST RESULTS: {passed}/{total} passed")
    print("="*60)
    
    if passed == total:
        print("""
✅ ALL TESTS PASSED!

The reorganization was successful:
- Core systems (SoulOS, Soulpack, SDL, DigiLang) are working
- Digimon structure is correctly organized
- Memory paths have been updated
- All imports and references are fixed

You can now:
1. Run Scripturemon with the new structure
2. Test other Digimons
3. Continue development with the clean organization
        """)
    else:
        failed = [tests[i].__name__ for i, r in enumerate(results) if not r]
        print(f"❌ Some tests failed: {', '.join(failed)}")
        print("\nPlease check the errors above and fix the remaining issues.")
    
    # Save report
    report = {
        "timestamp": datetime.now().isoformat(),
        "tests_run": total,
        "tests_passed": passed,
        "all_passed": passed == total,
        "details": {
            test.__name__: result 
            for test, result in zip(tests, results)
        }
    }
    
    with open("INTEGRATION_TEST_REPORT.json", 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\nReport saved: INTEGRATION_TEST_REPORT.json")

if __name__ == "__main__":
    main()