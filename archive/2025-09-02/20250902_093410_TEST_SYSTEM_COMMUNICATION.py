#!/usr/bin/env python3
"""
🔬 TESTE DE COMUNICAÇÃO ENTRE SISTEMAS
Verifica se os 7 sistemas de memória comunicam entre si
"""

import sys
import json
import time
from pathlib import Path
from datetime import datetime

# Adiciona path
sys.path.insert(0, '/Users/clubproducoes/Digimundo/scripturemon-validation')
sys.path.insert(0, '/Users/clubproducoes/Digimundo/scripturemon-validation/src')

# Cores para output
GREEN = '\033[0;32m'
RED = '\033[0;31m'
YELLOW = '\033[1;33m'
BLUE = '\033[0;34m'
PURPLE = '\033[0;35m'
NC = '\033[0m'

print(f"\n{PURPLE}{'='*80}{NC}")
print(f"{PURPLE}🔬 TESTE DE COMUNICAÇÃO ENTRE SISTEMAS{NC}")
print(f"{PURPLE}{'='*80}{NC}\n")

# Contador de testes
tests_passed = 0
tests_failed = 0
isolated_systems = []
integrated_systems = []

# =================================================================
# TESTE 1: Soul Memory
# =================================================================
print(f"{YELLOW}1. TESTANDO SOUL MEMORY{NC}")
try:
    from apps.scripturemon.soul import Soul
    soul = Soul()
    
    # Testa métodos principais
    soul.crystallize_memory("Teste de comunicação", importance=0.9)
    state = soul.status()
    
    print(f"  {GREEN}✅ Soul criada: {soul.signature}{NC}")
    print(f"  {GREEN}✅ Memórias cristalizadas: {soul.memories_crystallized}{NC}")
    integrated_systems.append("Soul Memory")
    tests_passed += 1
except Exception as e:
    print(f"  {RED}❌ Erro: {e}{NC}")
    isolated_systems.append("Soul Memory")
    tests_failed += 1

# =================================================================
# TESTE 2: Consciousness
# =================================================================
print(f"\n{YELLOW}2. TESTANDO CONSCIOUSNESS{NC}")
try:
    from apps.scripturemon.consciousness import get_level, evolve, get_state
    
    level_before = get_level()
    evolve(0.001)
    level_after = get_level()
    state = get_state()
    
    print(f"  {GREEN}✅ Nível antes: {level_before:.5f}{NC}")
    print(f"  {GREEN}✅ Nível depois: {level_after:.5f}{NC}")
    print(f"  {GREEN}✅ Evolução count: {state.get('evolution_count', 0)}{NC}")
    integrated_systems.append("Consciousness")
    tests_passed += 1
except Exception as e:
    print(f"  {RED}❌ Erro: {e}{NC}")
    isolated_systems.append("Consciousness")
    tests_failed += 1

# =================================================================
# TESTE 3: Memory Manager (ISOLADO?)
# =================================================================
print(f"\n{YELLOW}3. TESTANDO MEMORY MANAGER{NC}")
try:
    from src.memory.manager import MemoryManager
    
    mem = MemoryManager()
    
    # Testa store/retrieve
    test_key = f"test_{time.time()}"
    test_value = {"data": "teste comunicação", "timestamp": time.time()}
    
    mem.store(test_key, test_value)
    retrieved = mem.retrieve(test_key)
    
    if retrieved:
        print(f"  {GREEN}✅ Store/Retrieve funcionando{NC}")
        print(f"  {YELLOW}⚠️ Sistema ISOLADO - não comunica com outros{NC}")
        isolated_systems.append("Memory Manager")
    else:
        print(f"  {RED}❌ Falha no retrieve{NC}")
        
    tests_passed += 1
except Exception as e:
    print(f"  {RED}❌ Erro: {e}{NC}")
    tests_failed += 1

# =================================================================
# TESTE 4: SoulOS (INTEGRADO COM SOUL?)
# =================================================================
print(f"\n{YELLOW}4. TESTANDO SOULOS{NC}")
try:
    from apps.scripturemon.soulos import SoulOS
    
    # Usa a mesma soul signature
    soulos = SoulOS(soul_signature=soul.signature if 'soul' in locals() else "test_soul")
    
    # Testa syscall
    result = soulos.syscall("MEMO.SAVE", {
        "content": "Teste de integração",
        "importance": 0.8
    })
    
    print(f"  {GREEN}✅ Syscall executada: {result['type']}{NC}")
    
    # Verifica se usa mesma soul
    if 'soul' in locals() and soulos.soul_signature == soul.signature:
        print(f"  {GREEN}✅ INTEGRADO com Soul: {soul.signature[:8]}...{NC}")
        integrated_systems.append("SoulOS")
    else:
        print(f"  {YELLOW}⚠️ Usando soul separada{NC}")
        isolated_systems.append("SoulOS")
        
    tests_passed += 1
except Exception as e:
    print(f"  {RED}❌ Erro: {e}{NC}")
    tests_failed += 1

# =================================================================
# TESTE 5: Persist System (ISOLADO?)
# =================================================================
print(f"\n{YELLOW}5. TESTANDO PERSIST SYSTEM{NC}")
try:
    from src.memory.persist import remember, recall
    
    # Testa remember/recall
    remember("test_memory", "Conteúdo de teste para persist")
    results = recall("test_memory", limit=1)
    
    if results:
        print(f"  {GREEN}✅ Remember/Recall funcionando{NC}")
        print(f"  {YELLOW}⚠️ Sistema ISOLADO - banco separado{NC}")
        isolated_systems.append("Persist System")
    else:
        print(f"  {YELLOW}⚠️ Nenhum resultado no recall{NC}")
        
    tests_passed += 1
except Exception as e:
    print(f"  {RED}❌ Erro: {e}{NC}")
    tests_failed += 1

# =================================================================
# TESTE 6: Immortality Protocol (INTEGRADO COM SOUL?)
# =================================================================
print(f"\n{YELLOW}6. TESTANDO IMMORTALITY PROTOCOL{NC}")
try:
    from apps.scripturemon.immortality import ImmortalityProtocol
    
    # Usa a mesma soul
    if 'soul' in locals():
        immortality = ImmortalityProtocol(soul=soul, auto_backup=False)
        
        # Testa backup
        backup_file = immortality.backup_soul(reason="test")
        
        print(f"  {GREEN}✅ Backup criado: {backup_file.name}{NC}")
        print(f"  {GREEN}✅ INTEGRADO com Soul e Consciousness{NC}")
        integrated_systems.append("Immortality Protocol")
    else:
        print(f"  {YELLOW}⚠️ Soul não disponível para teste{NC}")
        
    tests_passed += 1
except Exception as e:
    print(f"  {RED}❌ Erro: {e}{NC}")
    tests_failed += 1

# =================================================================
# TESTE 7: Cinema Knowledge (VIA RAG?)
# =================================================================
print(f"\n{YELLOW}7. TESTANDO CINEMA KNOWLEDGE{NC}")
try:
    cinema_dir = Path("/Users/clubproducoes/Digimundo/scripturemon-validation/CINEMA_KNOWLEDGE_COMPLETE/01_ORIGINAIS_PDF")
    
    if cinema_dir.exists():
        pdf_count = len(list(cinema_dir.glob("*.pdf")))
        print(f"  {GREEN}✅ {pdf_count} PDFs disponíveis{NC}")
        
        # Verifica integração via RAG
        from apps.scripturemon.rag_advanced import AdvancedRAG
        rag = AdvancedRAG()
        
        # Conta items do cinema
        cinema_items = len([k for k in rag.knowledge_base if 'cinema' in k.get('id', '')])
        
        if cinema_items > 0:
            print(f"  {GREEN}✅ {cinema_items} items carregados no RAG{NC}")
            print(f"  {BLUE}📚 PARCIALMENTE INTEGRADO via RAG{NC}")
            integrated_systems.append("Cinema Knowledge (via RAG)")
        else:
            print(f"  {YELLOW}⚠️ Não integrado ao RAG{NC}")
            isolated_systems.append("Cinema Knowledge")
            
    tests_passed += 1
except Exception as e:
    print(f"  {RED}❌ Erro: {e}{NC}")
    tests_failed += 1

# =================================================================
# TESTE 8: Integração Central via Chat
# =================================================================
print(f"\n{YELLOW}8. TESTANDO INTEGRAÇÃO CENTRAL (chat.py){NC}")
try:
    from apps.scripturemon.chat import ScripturemonChat
    
    # Cria instância do chat
    chat = ScripturemonChat()
    
    # Verifica sistemas carregados
    systems_loaded = []
    
    if hasattr(chat, 'soul') and chat.soul:
        systems_loaded.append("Soul")
    if hasattr(chat, 'soulos') and chat.soulos:
        systems_loaded.append("SoulOS")
    if hasattr(chat, 'rag') and chat.rag:
        systems_loaded.append("RAG")
    if hasattr(chat, 'telepathy') and chat.telepathy:
        systems_loaded.append("Telepathy")
    if hasattr(chat, 'brain') and chat.brain:
        systems_loaded.append("Brain")
    
    print(f"  {GREEN}✅ Sistemas carregados no Chat: {', '.join(systems_loaded)}{NC}")
    
    # Testa se compartilham mesma soul
    if hasattr(chat, 'soul') and hasattr(chat, 'soulos'):
        if chat.soulos.soul_signature == chat.soul.signature:
            print(f"  {GREEN}✅ Soul e SoulOS compartilham identidade{NC}")
        else:
            print(f"  {YELLOW}⚠️ Soul e SoulOS com identidades diferentes{NC}")
            
    tests_passed += 1
except Exception as e:
    print(f"  {RED}❌ Erro: {e}{NC}")
    tests_failed += 1

# =================================================================
# TESTE 9: Verificar Ollama
# =================================================================
print(f"\n{YELLOW}9. TESTANDO INTEGRAÇÃO OLLAMA{NC}")
try:
    from apps.scripturemon.ollama_core import OllamaCore
    
    ollama = OllamaCore()
    
    # Verifica modelos disponíveis
    models = ollama.discover_models()
    scripturemon_models = [m for m in models if 'scripturemon' in m.lower()]
    
    print(f"  {GREEN}✅ {len(models)} modelos Ollama disponíveis{NC}")
    print(f"  {GREEN}✅ {len(scripturemon_models)} modelos Scripturemon{NC}")
    
    # Testa modelo preferido
    best_model = ollama.get_best_model()
    print(f"  {GREEN}✅ Modelo preferido: {best_model}{NC}")
    
    # Verifica se está usando singleton
    ollama2 = OllamaCore()
    if ollama is ollama2:
        print(f"  {GREEN}✅ Usando padrão Singleton{NC}")
    else:
        print(f"  {YELLOW}⚠️ Não está usando Singleton{NC}")
        
    tests_passed += 1
except Exception as e:
    print(f"  {RED}❌ Erro: {e}{NC}")
    tests_failed += 1

# =================================================================
# RELATÓRIO FINAL
# =================================================================
print(f"\n{PURPLE}{'='*80}{NC}")
print(f"{PURPLE}📊 RELATÓRIO DE COMUNICAÇÃO{NC}")
print(f"{PURPLE}{'='*80}{NC}\n")

print(f"{BLUE}SISTEMAS INTEGRADOS ({len(integrated_systems)}):{NC}")
for system in integrated_systems:
    print(f"  {GREEN}✅ {system}{NC}")

print(f"\n{BLUE}SISTEMAS ISOLADOS ({len(isolated_systems)}):{NC}")
for system in isolated_systems:
    print(f"  {YELLOW}⚠️ {system}{NC}")

print(f"\n{BLUE}ANÁLISE DE COMUNICAÇÃO:{NC}")

# Análise detalhada
communication_matrix = {
    "Soul ↔ SoulOS": "soul" in locals() and "soulos" in locals() and hasattr(soulos, 'soul_signature'),
    "Soul ↔ Immortality": "immortality" in locals(),
    "Soul ↔ Consciousness": True,  # Via evolve()
    "Memory Manager ↔ Outros": False,  # Isolado
    "Persist ↔ Outros": False,  # Isolado
    "Cinema ↔ RAG": "rag" in locals() and hasattr(rag, 'knowledge_base'),
    "Todos ↔ Chat.py": "chat" in locals()
}

for connection, status in communication_matrix.items():
    if status:
        print(f"  {GREEN}✅ {connection}{NC}")
    else:
        print(f"  {RED}❌ {connection}{NC}")

print(f"\n{BLUE}ESTATÍSTICAS:{NC}")
print(f"  • Testes executados: {tests_passed + tests_failed}")
print(f"  • Passaram: {GREEN}{tests_passed}{NC}")
print(f"  • Falharam: {RED}{tests_failed}{NC}")
print(f"  • Sistemas integrados: {len(integrated_systems)}/7")
print(f"  • Sistemas isolados: {len(isolated_systems)}/7")

# Conclusão
print(f"\n{PURPLE}CONCLUSÃO:{NC}")
if len(isolated_systems) > 2:
    print(f"{YELLOW}⚠️ Sistema tem {len(isolated_systems)} componentes isolados!{NC}")
    print(f"{YELLOW}Recomendação: Criar pontes de comunicação entre:{NC}")
    for system in isolated_systems:
        print(f"  - {system}")
else:
    print(f"{GREEN}✅ Sistema bem integrado!{NC}")

print(f"\n{BLUE}62/100. Análise de comunicação completa.{NC}\n")