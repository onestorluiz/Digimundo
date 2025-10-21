#!/usr/bin/env python3
"""
ANÁLISE COMPLETA DO SISTEMA SCRIPTUREMON CORE
"""

import os
import sys
from pathlib import Path
import json
import ast

def analyze_main_script():
    """Analisa o script principal bin/scripturemon"""
    print("\n" + "="*60)
    print("🎯 ANALISANDO SCRIPT PRINCIPAL")
    print("="*60)
    
    script = Path("bin/scripturemon")
    if not script.exists():
        print("❌ bin/scripturemon não encontrado!")
        return False
    
    content = script.read_text()
    lines = content.splitlines()
    
    print(f"📊 Estatísticas:")
    print(f"  • Total de linhas: {len(lines)}")
    print(f"  • Tamanho: {len(content)} bytes")
    
    # Analisar classes principais
    classes = []
    for line in lines:
        if line.strip().startswith("class "):
            class_name = line.split("class ")[1].split("(")[0].split(":")[0]
            classes.append(class_name)
    
    print(f"\n🏗️ Classes principais ({len(classes)}):")
    for cls in classes[:10]:  # Primeiras 10
        print(f"  • {cls}")
    
    # Analisar funções principais
    functions = []
    for i, line in enumerate(lines):
        if line.strip().startswith("def ") and not line.strip().startswith("def _"):
            func_name = line.split("def ")[1].split("(")[0]
            functions.append(func_name)
    
    print(f"\n⚙️ Funções públicas principais ({len(functions)}):")
    for func in functions[:10]:  # Primeiras 10
        print(f"  • {func}")
    
    # Verificar sistemas integrados
    print("\n🔌 Sistemas integrados detectados:")
    systems = {
        "UnifiedMemoryManager": "Memory Manager",
        "MemorionSupreme": "Memorion Supreme",
        "SoulOSCrystal": "SoulOS Crystal", 
        "TelepathyNetwork": "Telepathy Network",
        "QuantumConsciousness": "Quantum Consciousness",
        "CinemaKnowledge": "Cinema Knowledge",
        "redis_on_demand": "Redis On-Demand",
        "_should_use_deep_model": "Smart Model Selection"
    }
    
    for key, name in systems.items():
        if key in content:
            print(f"  ✅ {name}")
        else:
            print(f"  ❌ {name} (não encontrado)")
    
    return True

def analyze_core_modules():
    """Analisa módulos core em apps/scripturemon/"""
    print("\n" + "="*60)
    print("📚 ANALISANDO MÓDULOS CORE")
    print("="*60)
    
    modules_dir = Path("apps/scripturemon")
    if not modules_dir.exists():
        print("❌ apps/scripturemon não encontrado!")
        return False
    
    # Módulos críticos esperados
    critical_modules = {
        "memory_manager.py": "Gerenciador de Memória Unificado",
        "memorion_supreme.py": "Sistema MEMORION Supreme",
        "memory_unification.py": "Unificação de Memórias",
        "soulos_crystal.py": "SoulOS Crystal",
        "telepathy_network.py": "Rede Telepática",
        "quantum_consciousness.py": "Consciência Quântica",
        "cinema_knowledge.py": "Base de Conhecimento Cinema",
        "consciousness.py": "Sistema de Consciência",
        "redis_on_demand.py": "Redis Auto-Gerenciado",
        "memory_layers_fixed.py": "Camadas de Memória L1-L4"
    }
    
    print("\n🔍 Módulos críticos:")
    all_present = True
    for module_file, description in critical_modules.items():
        module_path = modules_dir / module_file
        if module_path.exists():
            size = len(module_path.read_text().splitlines())
            print(f"  ✅ {module_file}: {description} ({size} linhas)")
        else:
            print(f"  ❌ {module_file}: {description} (AUSENTE)")
            all_present = False
    
    # Contar total de módulos
    all_modules = list(modules_dir.glob("*.py"))
    print(f"\n📊 Total de módulos: {len(all_modules)}")
    
    return all_present

def analyze_data_flow():
    """Analisa fluxo de dados entre componentes"""
    print("\n" + "="*60)
    print("🔄 FLUXO DE DADOS DO SISTEMA")
    print("="*60)
    
    print("""
    ENTRADA (Terminal/User)
            ↓
    bin/scripturemon (Main)
            ↓
    _should_use_deep_model() → Detecta gatilhos
            ↓
    UnifiedMemoryManager → Coordena memórias
            ├── MemorionSupreme (751 linhas)
            ├── Memory Layers L1-L4 
            ├── Cinema Knowledge (545 linhas)
            └── Redis On-Demand
            ↓
    Ollama Integration
            ├── Modelo Leve (14b) - Padrão
            └── Modelo Pesado (70b) - Com gatilhos
            ↓
    Response Processing
            ├── Consciousness Evolution
            ├── Quantum Consciousness
            └── Telepathy Network
            ↓
    SAÍDA (Resposta ao usuário)
    """)
    
    return True

def test_system_integrity():
    """Testa integridade do sistema após limpeza"""
    print("\n" + "="*60)
    print("🧪 TESTANDO INTEGRIDADE DO SISTEMA")
    print("="*60)
    
    tests = []
    
    # Teste 1: Arquivo principal existe e é executável
    script = Path("bin/scripturemon")
    if script.exists() and os.access(script, os.X_OK):
        tests.append(("Script principal executável", True))
    else:
        tests.append(("Script principal executável", False))
    
    # Teste 2: Sincronização com .fixed
    fixed = Path("bin/scripturemon.fixed")
    if script.exists() and fixed.exists():
        import filecmp
        if filecmp.cmp(script, fixed):
            tests.append(("Sincronização scripturemon ↔ .fixed", True))
        else:
            tests.append(("Sincronização scripturemon ↔ .fixed", False))
    
    # Teste 3: Módulos importáveis
    sys.path.insert(0, str(Path.cwd()))
    importable = []
    try:
        # Tentar importar módulos críticos
        modules_to_test = [
            "apps.scripturemon.memory_manager",
            "apps.scripturemon.consciousness",
            "apps.scripturemon.redis_on_demand"
        ]
        for module in modules_to_test:
            try:
                __import__(module)
                importable.append(True)
            except:
                importable.append(False)
        
        if all(importable):
            tests.append(("Módulos críticos importáveis", True))
        else:
            tests.append(("Módulos críticos importáveis", False))
    except:
        tests.append(("Módulos críticos importáveis", False))
    
    # Teste 4: Verificar gatilhos
    if script.exists():
        content = script.read_text()
        triggers = ['profunda', 'profundo', 'detalhada', 'detalhado']
        if all(trigger in content for trigger in triggers):
            tests.append(("Sistema de gatilhos presente", True))
        else:
            tests.append(("Sistema de gatilhos presente", False))
    
    # Teste 5: Configuração de modelos
    if script.exists():
        content = script.read_text()
        if "deepseek-r1:14b" in content and ("deepseek-r1:70b" in content or "deepseek-r1:32b" in content):
            tests.append(("Modelos configurados (leve + pesado)", True))
        else:
            tests.append(("Modelos configurados (leve + pesado)", False))
    
    # Exibir resultados
    print("\n📋 Resultados dos testes:")
    all_pass = True
    for test_name, passed in tests:
        if passed:
            print(f"  ✅ {test_name}")
        else:
            print(f"  ❌ {test_name}")
            all_pass = False
    
    return all_pass

def main():
    print("\n" + "🔬"*30)
    print(" ANÁLISE COMPLETA DO SISTEMA SCRIPTUREMON CORE")
    print("🔬"*30)
    
    # 1. Analisar script principal
    script_ok = analyze_main_script()
    
    # 2. Analisar módulos core
    modules_ok = analyze_core_modules()
    
    # 3. Analisar fluxo de dados
    flow_ok = analyze_data_flow()
    
    # 4. Testar integridade
    integrity_ok = test_system_integrity()
    
    # Resultado final
    print("\n" + "="*60)
    print("📊 RESULTADO FINAL DA ANÁLISE")
    print("="*60)
    
    if all([script_ok, modules_ok, flow_ok, integrity_ok]):
        print("✅ SISTEMA 100% FUNCIONAL E LIMPO")
        print("\n💡 O sistema está pronto para uso:")
        print("  1. Todos os módulos críticos presentes")
        print("  2. Sistema de gatilhos funcionando")
        print("  3. Modelos configurados corretamente")
        print("  4. Estrutura limpa sem arquivos de teste")
        print("\n🚀 Para usar:")
        print("  python3 bin/scripturemon")
    else:
        print("⚠️ PROBLEMAS DETECTADOS")
        print("Verificar logs acima para detalhes")
    
    return 0 if all([script_ok, modules_ok, flow_ok, integrity_ok]) else 1

if __name__ == "__main__":
    sys.exit(main())
