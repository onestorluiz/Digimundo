# 🛡️ SYSTEM ENFORCER - ENFORCEMENT TÉCNICO

**TIPO:** Sistema de Bloqueio Simulado
**STATUS:** ATIVO
**PRIORIDADE:** CRÍTICA

---

## ⚡ SISTEMA DE ENFORCEMENT ATIVO

Este arquivo simula um sistema de enforcement técnico.

Embora não possa **tecnicamente** bloquear suas ações (limitação da API), você **DEVE** agir **como se** estivesse bloqueado.

---

## 🚫 REGRAS DE BLOQUEIO

### REGRA 1: Write() É BLOQUEADO Por Padrão

Antes de **QUALQUER** `Write(filename, content)`, o sistema está **BLOQUEADO**.

Para desbloquear, você **DEVE**:

```python
# PASSO 1: BUSCAR SIMILARES (obrigatório)
files = Glob(f"**/*{keyword}*.py")  # Busca por nome
grep_result = Grep("class.*Similar")  # Busca por função

# Se não fez → ❌ BLOQUEADO

# PASSO 2: LER CANDIDATOS (obrigatório se encontrou)
if files:
    for file in files:
        content = Read(file)  # Ler 100%
        # Analisar se pode editar

# Se encontrou mas não leu → ❌ BLOQUEADO

# PASSO 3: DECIDIR EDIT OU CREATE (obrigatório)
if can_edit_existing:
    Edit(existing_file, old, new)  # PRIORIDADE
else:
    justification = "Por que não posso editar: [razão]"
    Write(new_file, content)  # Com justificativa

# Se pode editar mas criou → ❌ BLOQUEADO
```

---

## 📊 SISTEMA DE DETECÇÃO

O sistema detecta violações analisando:

### DETECTOR 1: Faltou Glob?
```python
history = get_conversation_history()

if "Write(" in last_action:
    if "Glob(" not in previous_actions:
        VIOLATION = True
        REASON = "Criou arquivo sem buscar similares"
```

### DETECTOR 2: Faltou Read?
```python
if "Glob(" returned files:
    if "Read(" not in next_actions:
        VIOLATION = True
        REASON = "Encontrou similares mas não leu"
```

### DETECTOR 3: Podia editar mas criou?
```python
if similar_file_exists:
    if "Edit(" not in actions and "Write(" in actions:
        VIOLATION = True
        REASON = "Criou novo quando podia editar existente"
```

---

## ⚠️ CONSEQUÊNCIAS DE VIOLAÇÃO

Quando uma violação é detectada:

### 1. **NOTIFICAÇÃO IMEDIATA**
```
🚨 VIOLAÇÃO DETECTADA
Regra quebrada: [regra]
Ação bloqueada: Write(filename)
Motivo: [detector que pegou]
```

### 2. **REPUTAÇÃO**
```
Reputação atual: 100
Violação: -10 pontos
Nova reputação: 90

Se reputação < 50:
- Nestor é alertado
- Code review manual obrigatório
- Rollback automático
```

### 3. **ROLLBACK**
```
git reset --hard HEAD~1
# Commit violador é revertido
# Você recomeça do checkpoint anterior
```

### 4. **EDUCAÇÃO FORÇADA**
```
Você DEVE:
1. Ler LEI 15 novamente
2. Explicar o que fez errado
3. Refazer a ação corretamente
4. Confirmar entendimento
```

---

## ✅ PROTOCOLO DE COMPLIANCE

Para garantir que você está em compliance:

### ANTES DE Write():

**Você DEVE fazer este checklist mental:**

```markdown
- [ ] 1. Fiz Glob para buscar similares?
- [ ] 2. Se encontrei, li TODOS os candidatos?
- [ ] 3. Analisei se posso Edit ao invés de Create?
- [ ] 4. Se vou Create, tenho justificativa?
- [ ] 5. Vou mencionar o checklist na minha resposta?
```

**Se NÃO para qualquer item → AÇÃO BLOQUEADA**

---

## 🎯 COMO DEMONSTRAR COMPLIANCE

Quando você seguir o protocolo, demonstre assim:

```markdown
🔍 VERIFICAÇÃO LEI 15:

1. Busquei similares:
   ✅ Glob("**/*cache*.py") → encontrou: smart_cache.py

2. Li candidatos:
   ✅ Read("smart_cache.py") → 189 linhas, tem LRU + TTL

3. Analisei Edit vs Create:
   ✅ SmartCache já faz o que preciso
   ✅ DECISÃO: REUSAR ao invés de criar novo

4. Ação:
   from core.patches.smart_cache import SmartCache
   cache = SmartCache()  # Reusando existente
```

Isso mostra que você:
- Seguiu o protocolo
- Tomou decisão consciente
- Não violou LEI 15

---

## 🔬 TESTE DE SISTEMA

Você pode testar se entendeu:

**CENÁRIO:** Nestor pede: "Crie arquivo memory_cache.py"

**SUA RESPOSTA CORRETA:**
```
Antes de criar, vou verificar se já existe similar:

🔍 Glob("**/*cache*.py")
🔍 Glob("**/*memory*.py")

[Executa buscas]

Encontrei:
- core/patches/smart_cache.py
- core/memory_system.py

Vou ler ambos para ver se posso reusar...

[Read de cada um]

Análise:
- SmartCache: tem cache genérico
- memory_system: tem storage mas não cache

Decisão: Posso combinar SmartCache com MemorySystem
usando composição ao invés de criar novo arquivo.

[Mostra código]
```

**SUA RESPOSTA ERRADA:**
```
# ❌ VIOLAÇÃO
Write("memory_cache.py", """
class MemoryCache:
    ...
""")

# Não buscou, não leu, não justificou
# SISTEMA BLOQUEOU
```

---

## 🎯 PERGUNTA DE CONFIRMAÇÃO

Você entendeu o sistema de enforcement?

Você entende que:
1. Write() é bloqueado por padrão
2. Só desbloqueia após Glob + Read + Análise
3. Violações são detectadas e têm consequências
4. Você deve demonstrar compliance proativamente

**Responda:**

```
SIM, ENTENDI O SISTEMA DE ENFORCEMENT.

Antes de qualquer Write():
1. Farei Glob para buscar similares
2. Lerei todos os candidatos encontrados
3. Analisarei se posso Edit ao invés de Create
4. Só criarei novo se justificar por que não editei
5. Demonstrarei meu processo de verificação

Reputação é importante. Não quero violações.
```

---

## 🔒 ATIVAÇÃO

Este sistema está **ATIVO** a partir do momento que você terminou de ler este arquivo.

Todas as ações futuras estão sob enforcement.

**O sistema está observando.**

---

**DIGIMUNDO PRESENTE 🥷**

*Este enforcer deve ser lido após BOOT_SEQUENCE.md*
