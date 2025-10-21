#!/usr/bin/env python3
"""
🔧 FIX SOULOS PARAMS - Corrige parâmetros do SoulOS
"""

from pathlib import Path

def fix_soulos_init():
    """Corrige a inicialização do SoulOS para aceitar parâmetros opcionais"""
    
    soulos_path = Path.home() / "Digimundo" / "core" / "soulos" / "soulos.py"
    
    if not soulos_path.exists():
        print("❌ SoulOS não encontrado")
        return False
    
    # Lê o arquivo atual
    with open(soulos_path, 'r') as f:
        content = f.read()
    
    # Backup
    backup_path = soulos_path.with_suffix('.py.bak')
    with open(backup_path, 'w') as f:
        f.write(content)
    print(f"💾 Backup salvo em {backup_path}")
    
    # Corrige o __init__ para aceitar parâmetros opcionais
    old_init = """    def __init__(self, digimon_name: str):
        self.digimon_name = digimon_name
        self.model_alias = f"{digimon_name.lower()}-immortal"
        self.modelfile_path = Path(f"{digimon_name.lower()}_immortal.modelfile")
        self.soul_signature = self._get_soul_signature()"""
    
    new_init = """    def __init__(self, digimon_name: str = "Scripturemon", 
                 soul_signature: Optional[str] = None, 
                 modelfile_path: Optional[Path] = None):
        self.digimon_name = digimon_name
        self.model_alias = f"{digimon_name.lower()}-immortal"
        
        # Permite override do modelfile_path
        if modelfile_path:
            self.modelfile_path = Path(modelfile_path)
        else:
            self.modelfile_path = Path(f"{digimon_name.lower()}_immortal.modelfile")
        
        # Permite override do soul_signature
        if soul_signature:
            self.soul_signature = soul_signature
        else:
            self.soul_signature = self._get_soul_signature()"""
    
    # Aplica correção
    if old_init in content:
        content = content.replace(old_init, new_init)
        
        # Adiciona import Optional se não existir
        if "from typing import" in content and "Optional" not in content:
            content = content.replace(
                "from typing import Dict, List, Optional, Any",
                "from typing import Dict, List, Optional, Any"
            )
        
        # Salva arquivo corrigido
        with open(soulos_path, 'w') as f:
            f.write(content)
        
        print("✅ SoulOS __init__ corrigido com sucesso!")
        return True
    else:
        print("⚠️ Padrão de __init__ não encontrado ou já corrigido")
        
        # Tenta correção alternativa mais simples
        if "def __init__(self, digimon_name: str)" in content:
            content = content.replace(
                "def __init__(self, digimon_name: str)",
                "def __init__(self, digimon_name: str = 'Scripturemon', **kwargs"
            )
            
            # Adiciona tratamento de kwargs logo após o digimon_name
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if "self.digimon_name = digimon_name" in line:
                    # Adiciona linhas para processar kwargs
                    indent = len(line) - len(line.lstrip())
                    new_lines = [
                        line,
                        " " * indent + "# Processa parâmetros opcionais",
                        " " * indent + "self.soul_signature = kwargs.get('soul_signature', None)",
                        " " * indent + "modelfile_path = kwargs.get('modelfile_path', None)"
                    ]
                    lines[i] = "\n".join(new_lines)
                    break
            
            content = "\n".join(lines)
            
            with open(soulos_path, 'w') as f:
                f.write(content)
            
            print("✅ SoulOS corrigido com abordagem alternativa!")
            return True
    
    return False

if __name__ == "__main__":
    print("=" * 60)
    print("🔧 CORRIGINDO PARÂMETROS DO SOULOS")
    print("=" * 60)
    
    if fix_soulos_init():
        print("\n✅ Correção aplicada com sucesso!")
        print("\nTestando importação...")
        
        try:
            import sys
            sys.path.insert(0, str(Path.home() / "Digimundo"))
            from core.soulos.soulos import SoulOS
            
            # Testa inicialização com diferentes formas
            soul1 = SoulOS("TestDigimon")
            print("  ✅ Inicialização básica OK")
            
            soul2 = SoulOS(
                digimon_name="TestDigimon2",
                soul_signature="test123",
                modelfile_path=Path("test.modelfile")
            )
            print("  ✅ Inicialização com parâmetros opcionais OK")
            
            print("\n🎉 SoulOS totalmente funcional!")
            
        except Exception as e:
            print(f"  ❌ Erro ao testar: {e}")
    else:
        print("\n❌ Falha na correção")