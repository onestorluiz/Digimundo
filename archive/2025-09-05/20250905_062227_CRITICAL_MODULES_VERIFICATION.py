#!/usr/bin/env python3
"""
VERIFICAÇÃO LINHA POR LINHA DOS MÓDULOS CRÍTICOS
"""

from pathlib import Path

def verify_critical_modules():
    """Verifica integridade dos módulos críticos"""
    
    print("\n" + "📚"*35)
    print(" VERIFICAÇÃO DE MÓDULOS CRÍTICOS")
    print("📚"*35)
    
    critical_modules = {
        "memory_manager.py": {
            "expected_classes": ["UnifiedMemoryManager"],
            "expected_functions": ["initialize", "store", "retrieve"],
            "min_lines": 400
        },
        "memorion_supreme.py": {
            "expected_classes": ["MemorionSupreme"],
            "expected_functions": ["evolve", "remember"],
            "min_lines": 700
        },
        "consciousness.py": {
            "expected_functions": ["evolve", "get_level", "get_state"],
            "min_lines": 50
        },
        "quantum_consciousness.py": {
            "expected_classes": ["QuantumConsciousness"],
            "min_lines": 150
        },
        "telepathy_network.py": {
            "expected_classes": ["TelepathyNetwork", "TelepathicNetwork"],
            "min_lines": 70
        },
        "redis_on_demand.py": {
            "expected_functions": ["ensure_redis", "shutdown_if_started"],
            "min_lines": 90
        },
        "cinema_knowledge.py": {
            "expected_classes": ["CinemaKnowledgeBase"],
            "min_lines": 500
        },
        "soulos_crystal.py": {
            "expected_classes": ["SoulOSCrystal"],
            "min_lines": 350
        },
        "memory_unification.py": {
            "expected_classes": ["MemoryUnification"],
            "min_lines": 500
        }
    }
    
    modules_dir = Path("apps/scripturemon")
    all_ok = True
    
    for module_name, expectations in critical_modules.items():
        module_path = modules_dir / module_name
        
        print(f"\n📄 {module_name}")
        print("-" * 50)
        
        if not module_path.exists():
            print(f"  ❌ ARQUIVO NÃO EXISTE!")
            all_ok = False
            continue
            
        content = module_path.read_text()
        lines = content.splitlines()
        
        # Verificar tamanho
        if len(lines) < expectations["min_lines"]:
            print(f"  ⚠️ Arquivo muito pequeno: {len(lines)} linhas (esperado {expectations['min_lines']}+)")
            all_ok = False
        else:
            print(f"  ✅ Tamanho: {len(lines)} linhas")
        
        # Verificar classes esperadas
        if "expected_classes" in expectations:
            for class_name in expectations["expected_classes"]:
                if f"class {class_name}" in content:
                    print(f"  ✅ Classe {class_name} presente")
                else:
                    print(f"  ❌ Classe {class_name} AUSENTE!")
                    all_ok = False
        
        # Verificar funções esperadas
        if "expected_functions" in expectations:
            for func_name in expectations["expected_functions"]:
                if f"def {func_name}" in content:
                    print(f"  ✅ Função {func_name} presente")
                else:
                    print(f"  ⚠️ Função {func_name} não encontrada")
        
        # Verificar imports suspeitos
        suspicious_imports = ["from tentativas", "from test", "from TEST"]
        for suspicious in suspicious_imports:
            if suspicious in content:
                print(f"  ⚠️ Import suspeito: {suspicious}")
                
    print("\n" + "="*50)
    if all_ok:
        print("✅ TODOS OS MÓDULOS CRÍTICOS ESTÃO ÍNTEGROS")
    else:
        print("⚠️ PROBLEMAS DETECTADOS EM MÓDULOS CRÍTICOS")
    
    return all_ok

if __name__ == "__main__":
    import sys
    sys.exit(0 if verify_critical_modules() else 1)
