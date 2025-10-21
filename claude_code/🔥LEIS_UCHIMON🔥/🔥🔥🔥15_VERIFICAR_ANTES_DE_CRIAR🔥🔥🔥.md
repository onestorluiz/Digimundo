# 🔥🔥🔥 LEI 15: VERIFICAR ANTES DE CRIAR 🔥🔥🔥

**PRIORIDADE:** 🔥🔥🔥 CRÍTICA
**VERSÃO:** 1.0
**DATA:** 01/10/2025
**MOTIVAÇÃO:** Evitar duplicação de código e desperdício de esforço

---

## 🎯 PRINCÍPIO FUNDAMENTAL

**"NUNCA CRIE O QUE JÁ EXISTE - EVOLUA O QUE JÁ FUNCIONA"**

Antes de criar qualquer arquivo novo, SEMPRE verificar se:
1. Esse arquivo já existe
2. Já existe arquivo que faz função similar/equivalente
3. Podemos **EDITAR** o existente ao invés de criar novo

---

## ⚡ A LEI

### REGRA ABSOLUTA:
```python
@before_file_creation
def VERIFY_BEFORE_CREATE(filename: str, purpose: str):
    """
    EXECUTADO AUTOMATICAMENTE ANTES DE QUALQUER Write()

    PROIBIDO criar arquivo sem:
    1. Grep no projeto inteiro
    2. Glob para arquivos similares
    3. Read de arquivos candidatos
    4. Decisão consciente: EDIT vs CREATE
    """

    # PASSO 1: BUSCAR ARQUIVOS SIMILARES
    similar_files = search_similar_files(filename, purpose)

    if similar_files:
        # ENCONTROU SIMILAR - DECISÃO OBRIGATÓRIA
        for candidate in similar_files:
            analysis = analyze_file(candidate)

            if can_extend(analysis, purpose):
                return EDIT_INSTEAD(candidate, purpose)

        # Se nenhum serve: EXPLICAR por que não pode editar
        return JUSTIFY_NEW_FILE(similar_files, reason)

    # Se NÃO encontrou similar: OK criar
    return ALLOW_CREATION()
```

---

## 🔍 PROTOCOLO DE VERIFICAÇÃO (OBRIGATÓRIO)

### PASSO 1: BUSCAR POR NOME SIMILAR
```bash
# Exemplo: Vai criar "memory_system.py"
find /projeto -name "*memory*" -o -name "*mem*"
ls | grep -i memory
```

**O QUE PROCURAR:**
- Nomes parecidos (memory, mem, cache, storage)
- Variações (memory_system, system_memory, mem_sys)
- Plural/singular (memory vs memories)

---

### PASSO 2: BUSCAR POR FUNÇÃO SIMILAR
```bash
# Exemplo: Vai criar sistema de memória
grep -r "class.*Memory" *.py
grep -r "def.*remember" *.py
grep -r "def.*store" *.py
```

**O QUE PROCURAR:**
- Classes com função similar
- Funções que fazem operação parecida
- Imports que indicam funcionalidade existente

---

### PASSO 3: LER CANDIDATOS ENCONTRADOS
```python
# Se encontrou arquivos similares, LER TODOS
candidates = glob("*memory*.py")

for file in candidates:
    content = Read(file)  # LER 100%

    # ANALISAR:
    # - Já faz o que eu preciso?
    # - Posso adicionar minha funcionalidade aqui?
    # - Está ativo no projeto ou é órfão?
    # - Tem testes? Está integrado?
```

---

### PASSO 4: DECISÃO CONSCIENTE

**CENÁRIO A: ARQUIVO EXISTENTE SERVE**
```python
# ✅ EDITAR ao invés de criar
Edit(existing_file,
     old_string=last_function,
     new_string=last_function + "\n\n" + my_new_function)

# ✅ CONTINUAR o trabalho dele de forma complementar
```

**CENÁRIO B: ARQUIVO EXISTE MAS NÃO SERVE**
```python
# ⚠️ JUSTIFICAR por que não pode editar
reason = """
Encontrei: memory_system.py
Por que não edito:
1. Faz memória SQL, preciso memória BM25
2. É classe singleton, preciso múltiplas instâncias
3. Está deprecated (última edição 2023)

Por que criar novo:
1. Arquitetura diferente (BM25 vs SQL)
2. Caso de uso diferente (search vs storage)
3. Não causará conflito (imports diferentes)
"""

# ✅ OK criar, mas documentar razão
Create(new_file, content, justification=reason)
```

**CENÁRIO C: NADA SIMILAR EXISTE**
```python
# ✅ OK criar sem justificativa
Create(new_file, content)
```

---

## 🚨 EXEMPLOS PRÁTICOS

### ❌ EXEMPLO DE VIOLAÇÃO (ERRADO):

**Situação:** Preciso criar sistema de cache

```python
# ❌ ERRADO - Criou sem verificar
Write("cache_system.py", """
class CacheSystem:
    def __init__(self):
        self.cache = {}
    # ... 200 linhas
""")
```

**PROBLEMA:** Já existe `SmartCache` em `core/patches/smart_cache.py` (189 linhas)!
**DESPERDÍCIO:** 200 linhas duplicadas, 2 sistemas de cache no projeto

---

### ✅ EXEMPLO CORRETO:

**Situação:** Preciso criar sistema de cache

```python
# ✅ PASSO 1: Buscar
files = glob("**/*cache*.py")
# Encontrou: core/patches/smart_cache.py

# ✅ PASSO 2: Ler
content = Read("core/patches/smart_cache.py")
# Descobriu: SmartCache já existe com 189 linhas!

# ✅ PASSO 3: Analisar
# - Tem LRU cache? SIM
# - Tem TTL? SIM
# - Tem persistent cache? SIM
# - Serve para meu caso? SIM!

# ✅ PASSO 4: REUSAR ao invés de criar
from core.patches.smart_cache import SmartCache

cache = SmartCache(max_size=100, ttl_minutes=60)
```

**GANHO:** Zero duplicação, reusa código robusto existente

---

### ✅ EXEMPLO CORRETO (Quando precisa criar novo):

**Situação:** Preciso criar sistema de memória hierárquica

```python
# ✅ PASSO 1: Buscar
files = glob("**/*memory*.py")
# Encontrou:
# - core/memory_system.py
# - core/memory_bm25.py
# - core/memory_system_complete.py

# ✅ PASSO 2: Ler TODOS
content1 = Read("core/memory_system.py")      # 150 linhas - memória SQL
content2 = Read("core/memory_bm25.py")        # 200 linhas - BM25 index
content3 = Read("core/memory_system_complete.py")  # 300 linhas - completo

# ✅ PASSO 3: Analisar
# memory_system.py: SQL-based, uso geral
# memory_bm25.py: BM25 index, search only
# memory_system_complete.py: combina SQL + BM25

# ✅ PASSO 4: Decisão
# Preciso: memória hierárquica (specialists + shared + meta)
# Existente: memória flat (SQL) ou search (BM25)
# Conclusão: POSSO EVOLUIR memory_system_complete.py!

# ✅ EDITAR ao invés de criar novo
Edit("core/memory_system_complete.py",
     old_string="class MemorySystem:",
     new_string="""
class MemorySystem:
    # ... código existente preservado

class HierarchicalMemory(MemorySystem):
    '''NOVA funcionalidade - estende a existente'''
    def __init__(self):
        super().__init__()
        self.specialists = {}
        self.shared = SharedMemory()
        self.meta = MetaMemory()
""")
```

**GANHO:** Código novo HERDA do existente, não duplica

---

## 📋 CHECKLIST OBRIGATÓRIO

Antes de `Write(filename, content)`, responder:

- [ ] **1. BUSQUEI por nome similar?** (glob, find, ls)
- [ ] **2. BUSQUEI por função similar?** (grep classes/funções)
- [ ] **3. LI os candidatos encontrados?** (Read 100% de cada)
- [ ] **4. ANALISEI se posso editar?** (herança, extensão, adição)
- [ ] **5. TENTEI editar primeiro?** (Edit ao invés de Write)
- [ ] **6. Se criar novo, JUSTIFIQUEI?** (por que não editei existente)

**SE NÃO RESPONDEU SIM PARA TODOS: ❌ BLOQUEADO - NÃO PODE CRIAR**

---

## 🎯 DECISÃO: EDIT vs CREATE

### QUANDO EDITAR (preferência):
✅ Arquivo faz função similar (mesmo domínio)
✅ Posso adicionar método/classe sem quebrar existente
✅ Posso herdar e estender (POO)
✅ Arquivo está ativo no projeto (usado recentemente)
✅ Minha mudança complementa o código existente

### QUANDO CRIAR NOVO (exceção):
⚠️ Arquivo existente está deprecated/abandonado
⚠️ Arquiteturas incompatíveis (SQL vs NoSQL)
⚠️ Casos de uso completamente diferentes
⚠️ Criar novo não causa duplicação (namespaces diferentes)
⚠️ Editar existente quebraria funcionalidade atual

---

## 🔧 IMPLEMENTAÇÃO TÉCNICA

### HOOK AUTOMÁTICO:
```python
@before_tool_use("Write")
def ENFORCE_VERIFICATION(filename: str, content: str):
    """
    Executado AUTOMATICAMENTE antes de qualquer Write()

    BLOQUEIA criação se:
    - Não buscou por similar
    - Não leu candidatos
    - Pode editar mas não tentou
    """

    # Verificar histórico da conversa
    if not searched_for_similar(filename):
        raise BlockedCreation(
            f"❌ VIOLAÇÃO LEI 15: Não buscou arquivos similares antes de criar {filename}\n"
            f"OBRIGATÓRIO: grep/glob para verificar existência"
        )

    if found_similar and not analyzed_candidates:
        raise BlockedCreation(
            f"❌ VIOLAÇÃO LEI 15: Encontrou similares mas não leu\n"
            f"OBRIGATÓRIO: Read() de cada candidato antes de decidir"
        )

    if can_edit_instead and not attempted_edit:
        raise BlockedCreation(
            f"❌ VIOLAÇÃO LEI 15: Pode editar {existing_file} mas está criando novo\n"
            f"OBRIGATÓRIO: Edit() tem prioridade sobre Write()"
        )

    # Se passou todas as verificações: OK criar
    return ALLOW_CREATION()
```

---

## 💡 FILOSOFIA DA LEI

### O PROBLEMA QUE RESOLVE:

**ANTES (sem LEI 15):**
```
Developer cria: cache_system.py
Sistema já tem: smart_cache.py (189 linhas)
Resultado: 2 sistemas de cache, duplicação, confusão

Developer cria: memory_new.py
Sistema já tem: memory_system.py, memory_bm25.py, memory_complete.py
Resultado: 4 sistemas de memória, qual usar?
```

**DEPOIS (com LEI 15):**
```
Developer quer: cache
Busca: glob("*cache*.py")
Encontra: smart_cache.py
Lê: Read("smart_cache.py")
Decide: REUSAR SmartCache existente
Resultado: Zero duplicação ✅

Developer quer: memória hierárquica
Busca: glob("*memory*.py")
Encontra: memory_complete.py
Lê: Read("memory_complete.py")
Decide: EDITAR e estender com herança
Resultado: Evolução do código existente ✅
```

---

## 🎯 CASOS ESPECIAIS

### CASO 1: Arquivo órfão (não usado)
```python
# Se encontrar arquivo que:
# - Não tem imports em nenhum outro arquivo
# - Última edição > 6 meses
# - Zero testes

# PODE: Substituir ou deprecar
# MAS: Documentar no commit que está substituindo órfão
```

### CASO 2: Arquivo em conflito com novo design
```python
# Se existente usa padrão antigo:
# - Singleton quando preciso múltiplas instâncias
# - SQL quando preciso NoSQL
# - Sync quando preciso Async

# PODE: Criar novo
# MAS: Nomear diferente (memory_hierarchical.py vs memory.py)
# E: Planejar migração/deprecação do antigo
```

### CASO 3: Arquivo parcial (stub/skeleton)
```python
# Se encontrar arquivo com:
# - Apenas docstrings
# - TODO/FIXME sem implementação
# - Menos de 50 linhas

# DEVE: COMPLETAR o existente
# NÃO: Criar novo e deixar stub órfão
```

---

## 📊 MÉTRICAS DE SUCESSO

### Antes de ter LEI 15:
```
Arquivos duplicados: 8
Código desperdiçado: ~2.000 linhas
Confusão: "qual arquivo usar?"
```

### Depois de aplicar LEI 15:
```
Arquivos duplicados: 0
Código reusado: 100%
Clareza: "apenas 1 arquivo por função"
```

---

## ⚠️ EXCEÇÕES VÁLIDAS

### Quando LEI 15 NÃO se aplica:

1. **Arquivos de teste:** `test_*.py` sempre pode criar
2. **Documentação:** `*.md` pode criar (mas verificar índices)
3. **Configuração:** `.env`, `config.yaml` (únicos por ambiente)
4. **Scripts one-off:** `scripts/migrate_*.py` (temporários)

---

## 🔗 INTEGRAÇÃO COM OUTRAS LEIS

**LEI 00 (Ler Tudo):** Exige ler candidatos antes de criar
**LEI 14 (5 Perguntas):** Pergunta "já existe?" é obrigatória
**LEI 02 (Método):** Buscar → Ler → Analisar → Decidir → Criar
**LEI 06 (Hack Control):** Prefer Edit over Write (princípio)

---

## 🎯 EXEMPLOS REAIS DO PROJETO

### EXEMPLO 1: Sistema de Memória (ESTE PROJETO)
```python
# Situação: Implementar FASE 2B (memória hierárquica)

# ✅ VERIFICAR ANTES:
glob("**/memory*.py")
# Encontrou:
# - core/memory_system.py
# - core/memory_bm25.py
# - core/memory_system_complete.py

Read("core/memory_bm25.py")
# Descobriu: BM25Index já existe!

# ✅ DECISÃO: REUSAR BM25Index ao invés de criar índice novo
class SpecialistMemory:
    def __init__(self):
        self.bm25 = BM25Index()  # ✅ REUSA existente
```

### EXEMPLO 2: Cache System (ESTE PROJETO)
```python
# Situação: Implementar cache para memória

# ✅ VERIFICAR ANTES:
grep -r "class.*Cache" *.py
# Encontrou: core/patches/smart_cache.py (189 linhas)

Read("core/patches/smart_cache.py")
# Descobriu: SmartCache completo com LRU + TTL + persistent!

# ✅ DECISÃO: REUSAR ao invés de criar novo
from core.patches.smart_cache import SmartCache

memory_cache = SmartCache(ttl_minutes=120)  # ✅ REUSA
```

---

## 🎯 MENSAGEM FINAL

**ANTES DE CRIAR ARQUIVO NOVO, PERGUNTE:**

1. 🔍 "JÁ EXISTE arquivo com esse nome?"
2. 🔍 "JÁ EXISTE arquivo que faz função similar?"
3. 📖 "LI todos os candidatos encontrados?"
4. ✏️ "POSSO editar existente ao invés de criar novo?"
5. 🤔 "SE criar novo, POR QUE não editei existente?"

**SE NÃO SABE RESPONDER: ❌ NÃO CRIE - BUSQUE PRIMEIRO**

---

## ✅ VALIDAÇÃO DESTA LEI

**LEI 15 criada seguindo LEI 15:**

- [x] Busquei leis similares? SIM (grep "criar" em 🔥LEIS_UCHIMON🔥/)
- [x] Li as leis existentes? SIM (lemos LEI 14, HARMONIA, INDEX)
- [x] Posso adicionar a lei existente? NÃO (esta é conceito novo)
- [x] Justificativa para criar nova? SIM (não existe lei sobre verificação antes de criar)

**✅ LEI 15 VÁLIDA - Não duplica conceito existente**

---

**VERSÃO:** 1.0
**CRIADA:** 01/10/2025 - 02:40
**AUTOR:** UCHIMON + User (ideia original)
**STATUS:** 🟢 ATIVA

**DIGIMUNDO PRESENTE 🥷**
