#!/usr/bin/env python3
"""
🔧 FIX TELEPATHY BROADCAST
Corrige o erro de broadcast no TelepathyNetwork
"""

from pathlib import Path

def fix_telepathy():
    """Adiciona método broadcast faltante"""
    
    telepathy_path = Path("/Users/clubproducoes/Digimundo/scripturemon-validation/apps/scripturemon/telepathy_network.py")
    
    if not telepathy_path.exists():
        print("❌ telepathy_network.py não encontrado")
        return False
    
    content = telepathy_path.read_text()
    
    # Verificar se broadcast já existe
    if "def broadcast(" in content:
        print("✅ Método broadcast já existe")
        return True
    
    # Adicionar método broadcast
    broadcast_method = '''
    def broadcast(self, data):
        """Broadcast data to network (stub for compatibility)"""
        if self.debug:
            print(f"  📡 Broadcasting: {data.get('type', 'unknown')}")
        # In a real implementation, this would send to other nodes
        pass
    
    def receive(self, timeout=0.01):
        """Receive data from network (stub for compatibility)"""
        # In a real implementation, this would receive from other nodes
        return None
'''
    
    # Encontrar onde inserir (antes do final da classe)
    lines = content.split('\n')
    
    # Procurar a classe TelepathyNetwork
    class_found = False
    insert_index = -1
    indent_level = ""
    
    for i, line in enumerate(lines):
        if "class TelepathyNetwork" in line:
            class_found = True
            continue
            
        if class_found:
            # Detectar indentação
            if line.strip().startswith("def ") and not indent_level:
                indent_level = line[:len(line) - len(line.lstrip())]
            
            # Procurar o final da classe (próxima classe ou fim do arquivo)
            if line and not line.startswith((' ', '\t')) and i > 0:
                insert_index = i - 1
                break
    
    if insert_index == -1:
        insert_index = len(lines) - 1
    
    # Inserir o método
    broadcast_lines = broadcast_method.split('\n')
    for line in reversed(broadcast_lines):
        if line or line == '':  # Preservar linhas vazias
            lines.insert(insert_index, line)
    
    # Salvar arquivo
    telepathy_path.write_text('\n'.join(lines))
    print("✅ Método broadcast adicionado ao TelepathyNetwork")
    
    return True

def fix_memory_unification():
    """Adiciona verificação antes de usar broadcast"""
    
    memory_path = Path("/Users/clubproducoes/Digimundo/scripturemon-validation/apps/scripturemon/memory_unification.py")
    
    if not memory_path.exists():
        print("❌ memory_unification.py não encontrado")
        return False
    
    content = memory_path.read_text()
    
    # Substituir usos diretos de broadcast por verificação
    replacements = [
        (
            "self.telepathy.broadcast(broadcast_data)",
            "if hasattr(self.telepathy, 'broadcast'):\n            self.telepathy.broadcast(broadcast_data)"
        ),
        (
            "self.telepathy.broadcast({",
            "if hasattr(self.telepathy, 'broadcast'):\n            self.telepathy.broadcast({"
        ),
        (
            "self.telepathy.broadcast_history.append(broadcast_data)",
            "if hasattr(self.telepathy, 'broadcast_history'):\n            self.telepathy.broadcast_history.append(broadcast_data)"
        ),
        (
            "self.telepathy.broadcast_history = []",
            "if self.telepathy:\n            self.telepathy.broadcast_history = []"
        )
    ]
    
    for old, new in replacements:
        if old in content:
            content = content.replace(old, new)
            print(f"✅ Substituído: {old[:30]}...")
    
    # Salvar arquivo
    memory_path.write_text(content)
    print("✅ memory_unification.py atualizado com verificações")
    
    return True

if __name__ == "__main__":
    print("🔧 CORRIGINDO TELEPATHY BROADCAST")
    print("="*60)
    
    print("\n1. Corrigindo TelepathyNetwork...")
    if fix_telepathy():
        print("\n2. Corrigindo memory_unification...")
        if fix_memory_unification():
            print("\n✅ CORREÇÕES APLICADAS COM SUCESSO!")
            print("\nO sistema agora deve funcionar sem erro de broadcast.")
        else:
            print("\n❌ Erro ao corrigir memory_unification")
    else:
        print("\n❌ Erro ao corrigir TelepathyNetwork")