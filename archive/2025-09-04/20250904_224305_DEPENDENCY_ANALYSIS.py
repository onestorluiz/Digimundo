#!/usr/bin/env python3
"""
ANÁLISE PROFUNDA DE DEPENDÊNCIAS - IDENTIFICAR PONTOS DE QUEBRA
"""

import ast
import sys
from pathlib import Path
from collections import defaultdict

def analyze_imports(file_path):
    """Analisa imports de um arquivo Python"""
    try:
        content = Path(file_path).read_text()
        tree = ast.parse(content)
        
        imports = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for name in node.names:
                    imports.add(name.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.add(node.module)
        
        return imports
    except:
        return set()

def check_circular_dependencies():
    """Verifica dependências circulares"""
    print("\n🔄 VERIFICANDO DEPENDÊNCIAS CIRCULARES")
    print("="*60)
    
    app_modules = list(Path("apps/scripturemon").glob("*.py"))
    dependencies = {}
    
    for module in app_modules:
        module_name = module.stem
        imports = analyze_imports(module)
        
        # Filtrar apenas imports locais
        local_imports = {imp for imp in imports if imp.startswith("apps.scripturemon")}
        dependencies[module_name] = local_imports
    
    # Detectar ciclos
    circular_found = False
    for module, deps in dependencies.items():
        for dep in deps:
            dep_name = dep.split('.')[-1]
            if dep_name in dependencies:
                # Verifica se há dependência reversa
                if f"apps.scripturemon.{module}" in dependencies.get(dep_name, set()):
                    print(f"⚠️ Dependência circular: {module} ↔ {dep_name}")
                    circular_found = True
    
    if not circular_found:
        print("✅ Nenhuma dependência circular encontrada")
    
    return not circular_found

def check_missing_modules():
    """Verifica módulos faltantes"""
    print("\n❓ VERIFICANDO MÓDULOS IMPORTADOS MAS AUSENTES")
    print("="*60)
    
    # Analisar bin/scripturemon
    script = Path("bin/scripturemon")
    content = script.read_text()
    
    # Extrair imports tentados
    imports_needed = []
    for line in content.split('\n'):
        if 'from apps.scripturemon' in line or 'import apps.scripturemon' in line:
            imports_needed.append(line.strip())
    
    missing = []
    for imp in imports_needed:
        # Extrair nome do módulo
        if 'from apps.scripturemon.' in imp:
            module = imp.split('from apps.scripturemon.')[1].split(' ')[0]
            module_path = f"apps/scripturemon/{module}.py"
            if not Path(module_path).exists():
                print(f"❌ Módulo ausente: {module_path}")
                print(f"   Importado em: {imp}")
                missing.append(module)
    
    if not missing:
        print("✅ Todos os módulos importados existem")
    
    return len(missing) == 0

def check_redis_integration():
    """Verifica integração com Redis"""
    print("\n🔴 VERIFICANDO INTEGRAÇÃO REDIS")
    print("="*60)
    
    # Verificar se redis_on_demand é usado
    redis_users = []
    for py_file in Path("apps/scripturemon").glob("*.py"):
        content = py_file.read_text()
        if "redis_on_demand" in content or "ensure_redis" in content:
            redis_users.append(py_file.name)
            print(f"✅ {py_file.name} usa redis_on_demand")
    
    if not redis_users:
        print("⚠️ redis_on_demand não está sendo usado por nenhum módulo")
        print("   Isto pode causar falhas se Redis não estiver rodando")
    
    # Verificar se bin/scripturemon inicializa Redis
    script = Path("bin/scripturemon").read_text()
    if "ensure_redis" in script or "redis_on_demand" in script:
        print("✅ bin/scripturemon inicializa Redis on-demand")
        return True
    else:
        print("⚠️ bin/scripturemon NÃO inicializa Redis automaticamente")
        return False

def check_model_configuration():
    """Verifica configuração de modelos"""
    print("\n🤖 VERIFICANDO CONFIGURAÇÃO DE MODELOS")
    print("="*60)
    
    script = Path("bin/scripturemon").read_text()
    
    issues = []
    
    # Verificar modelo principal
    if "deepseek-r1:14b" not in script:
        issues.append("Modelo leve (14b) não configurado como principal")
    
    # Verificar modelos pesados
    if "deepseek-r1:70b" not in script and "deepseek-r1:32b" not in script:
        issues.append("Nenhum modelo pesado configurado")
    
    # Verificar se scripturemon-deepseek ainda existe (duplicação)
    if "scripturemon-deepseek:latest" in script:
        issues.append("Modelo duplicado scripturemon-deepseek ainda configurado (42GB desnecessários)")
    
    if issues:
        for issue in issues:
            print(f"⚠️ {issue}")
        return False
    else:
        print("✅ Modelos configurados corretamente")
        print("  - Principal: deepseek-r1:14b (leve)")
        print("  - Profundo: deepseek-r1:70b ou 32b (pesado)")
        print("  - Sem duplicações desnecessárias")
        return True

def check_timeout_configuration():
    """Verifica configuração de timeouts"""
    print("\n⏰ VERIFICANDO CONFIGURAÇÃO DE TIMEOUTS")
    print("="*60)
    
    script = Path("bin/scripturemon").read_text()
    
    # Procurar por timeout=None para modelos pesados
    if "timeout=None" in script:
        print("✅ Timeout removido para análises profundas (timeout=None encontrado)")
        return True
    elif "timeout" not in script:
        print("⚠️ Configuração de timeout não encontrada")
        return False
    else:
        # Verificar se há lógica condicional para timeout
        if "if.*deep" in script and "timeout" in script:
            print("✅ Timeout condicional implementado para modelos profundos")
            return True
        else:
            print("⚠️ Timeout fixo pode causar problemas com modelos pesados")
            return False

def main():
    print("\n" + "🔬"*30)
    print(" ANÁLISE PROFUNDA DE DEPENDÊNCIAS E PONTOS DE QUEBRA")
    print("🔬"*30)
    
    all_ok = True
    
    # 1. Dependências circulares
    if not check_circular_dependencies():
        all_ok = False
    
    # 2. Módulos faltantes
    if not check_missing_modules():
        all_ok = False
    
    # 3. Integração Redis
    if not check_redis_integration():
        all_ok = False
    
    # 4. Configuração de modelos
    if not check_model_configuration():
        all_ok = False
    
    # 5. Configuração de timeouts
    if not check_timeout_configuration():
        all_ok = False
    
    # Resultado final
    print("\n" + "="*60)
    print("📊 DIAGNÓSTICO FINAL")
    print("="*60)
    
    if all_ok:
        print("✅ SISTEMA ESTÁVEL - Nenhum ponto crítico de quebra detectado")
        print("\n💡 Recomendações para manter estabilidade:")
        print("1. NÃO modifique bin/scripturemon sem backup")
        print("2. NÃO remova módulos em apps/scripturemon/")
        print("3. Mantenha sincronização entre scripturemon e scripturemon.fixed")
        print("4. Teste SEMPRE com inputs simples antes de usar gatilhos")
    else:
        print("⚠️ PONTOS DE ATENÇÃO DETECTADOS")
        print("\n🔧 Correções necessárias listadas acima")
        print("IMPORTANTE: Fazer backup antes de qualquer correção")
    
    return 0 if all_ok else 1

if __name__ == "__main__":
    sys.exit(main())
