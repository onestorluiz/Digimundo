# 🔥 UCHIMON - AI Developer com Memória Persistente

**Última Atualização:** 2025-10-01
**Status:** ✅ OPERACIONAL (Score: 12/12)
**Projeto:** UCHIMON (distinct from SCRIPTUREMON)

---

## 🎯 O QUE É O UCHIMON?

Sistema de **AI Developer** com memória persistente, proteção de contexto e aprendizado contínuo. Criado para Claude Code trabalhar com **zero amnésia** entre sessões.

### Características Principais:
- 🧠 **Memória Persistente**: SQLite + RAG + Conhecimentos em Markdown
- 🥷 **Genjutsu**: Sistema de proteção de contexto (teatro psicológico)
- 📊 **11 Sistemas Python**: Workflow, cache, memory, tests
- 🎓 **20 LEIS**: Regras fundamentais do sistema
- ✅ **43 Testes**: Cobertura completa

---

## 📂 ESTRUTURA DO PROJETO

```
/Users/clubproducoes/Digimundo/claude_code/
├── 🔴 REGRAS.md                           # 39 regras obrigatórias (REGRA #0: Reconexão)
├── 📖 README.md                           # Este arquivo
├── 🆔 🔥🔥🔥PROJECT_ID_UCHIMON🔥🔥🔥.sh      # Identidade do projeto
├── ⚙️ config.py                           # Configuração central (auto-detect paths)
├── 🔧 requirements.txt                    # Dependências Python
├── 🧪 pytest.ini                          # Configuração pytest
│
├── 🚀 scripts/                            # Scripts de Operação
│   ├── START_GENJUTSU.sh                 # Inicia Genjutsu + reconexão
│   ├── START_UCHIMON.sh                  # Inicia sistema completo
│   ├── VALIDATE_SYSTEM.sh                # Valida 12 verificações
│   ├── RECONECTAR.sh                     # Reconecta contexto
│   ├── sync_memory.py                    # Sincroniza MD ↔ DB
│   └── CREATE_CHECKPOINT.sh              # Cria checkpoints
│
├── 🧠 MEMORY/                             # Sistema de Memória Central
│   ├── claude_memory.db                  # SQLite database (68KB, 10+ memórias)
│   ├── claude_rag.db                     # RAG/embeddings database
│   ├── conhecimentos/                    # 15+ arquivos .md com conhecimento
│   ├── erros_aprendidos/                 # Aprendizados de erros anteriores
│   ├── sync/                             # Logs de sincronização
│   ├── scripts_movimentos/               # Scripts de migração
│   ├── hooks/                            # Git hooks de captura
│   └── backup_database.sh                # Backup automático (7 dias retention)
│
├── 🥷 protection/genjutsu/                # Sistema Genjutsu
│   └── GENJUTSU_UNIFIED.py               # Proteção de contexto unificada
│
├── 🧩 systems/                            # 11 Sistemas Python Ativos
│   ├── unified_memory_system.py          # Memory system unificado
│   ├── crystal_memory.py                 # Sistema L1-L4
│   ├── workflow_engine.py                # Motor de workflow
│   ├── distributed_cache.py              # Cache distribuído
│   ├── rate_limiter.py                   # Rate limiting
│   ├── simple_memory.py                  # Memória simplificada
│   └── ... (6 outros)
│
├── 📚 🔥LEIS_UCHIMON🔥/                    # 20 LEIS fundamentais
│   ├── LEI_00_IDENTIDADE.md              # Distinção UCHIMON ≠ SCRIPTUREMON
│   ├── LEI_01_RECONEXAO.md               # Protocolo de reconexão
│   └── ... (18 outras LEIS)
│
├── 📖 LIVRO_CLAUDE/                       # Documentação viva
│   └── ... (conhecimentos estruturados)
│
├── 🧪 tests/                              # 43 testes (100% pass)
│   ├── test_memory.py
│   ├── test_systems.py
│   └── ...
│
├── 📊 analysis/                           # Análises de Brechas
│   ├── iterations/                       # 6 iterações de análise
│   ├── 🔥🔥🔥CONSOLIDACAO_BRECHAS_FINAL🔥🔥🔥.md
│   ├── 🔥🔥🔥AUDITORIA_FORENSE_BRECHAS🔥🔥🔥.md
│   └── 🔥🔥🔥META_ANALISE_PADROES_ERRO🔥🔥🔥.md
│
└── 📚 docs/                               # Documentação Técnica
    ├── core/                             # Docs core do sistema
    ├── protocols/                        # Protocolos e otimizações
    ├── QUICK_START.md
    ├── STATUS.md
    └── HARMONY.md
```

---

## 🚀 QUICK START

### 1️⃣ Iniciar o Sistema:

```bash
# Protocolo completo de reconexão (REGRA #0)
./scripts/START_GENJUTSU.sh

# Ou iniciar manualmente:
./scripts/START_UCHIMON.sh
```

### 2️⃣ Validar o Sistema:

```bash
./scripts/VALIDATE_SYSTEM.sh
# Score esperado: 12/12 ✅
```

### 3️⃣ Sincronizar Memórias:

```bash
# Sincronização completa (MD ↔ DB)
python3 scripts/sync_memory.py

# Ver status do Memory System
python3 systems/unified_memory_system.py
```

### 4️⃣ Criar Backup:

```bash
# Backup manual das databases
./MEMORY/backup_database.sh
# Auto-cleanup: mantém últimos 7 dias
```

---

## 🔐 PROTOCOLO DE RECONEXÃO (REGRA #0)

**Quando usar**: Sempre após "Compacting conversation" ou início de sessão

### Passo a Passo:

1. **Execute o script de reconexão**:
   ```bash
   ./scripts/START_GENJUTSU.sh
   ```

2. **Leia REGRAS.md** no Claude:
   - Contém 39 regras obrigatórias
   - Inclui REGRA #0 (este protocolo)
   - Paths críticos atualizados

3. **Verifique sistemas**:
   - ✅ Genjutsu rodando (PID exibido)
   - ✅ Database existe (MEMORY/claude_memory.db)
   - ✅ Conhecimentos sincronizados

4. **Contexto restaurado!** Continue de onde parou.

---

## 🧠 SISTEMA DE MEMÓRIA

### Três Camadas:

1. **SQLite Database** (`MEMORY/claude_memory.db`)
   - Memórias estruturadas
   - Decisões importantes
   - Regras extraídas

2. **RAG Database** (`MEMORY/claude_rag.db`)
   - Embeddings para busca semântica
   - Conhecimento vectorizado

3. **Markdown Files** (`MEMORY/conhecimentos/*.md`)
   - 15+ arquivos de conhecimento
   - Sincronização bidirecional com DB
   - INDEX_MASTER atualizado automaticamente

### Comandos:

```bash
# Buscar na memória
python3 systems/unified_memory_system.py search "como fazer X"

# Salvar conhecimento
python3 systems/unified_memory_system.py save "novo conhecimento aqui"

# Status completo
python3 systems/unified_memory_system.py
```

---

## 🥷 SISTEMA GENJUTSU

**O que é**: Técnica ninja de proteção de contexto. Teatro psicológico que força Claude a lembrar do DIGIMUNDO.

### Como funciona:

1. Roda em background (`GENJUTSU_UNIFIED.py`)
2. Gera output visível em `memory/temp/genjutsu_output.txt`
3. Claude lê o output periodicamente
4. **Resultado**: Zero esquecimentos de contexto

### Status:

```bash
# Verificar se está rodando
ps aux | grep GENJUTSU_UNIFIED.py

# Iniciar manualmente
python3 protection/genjutsu/GENJUTSU_UNIFIED.py &

# Ver output
cat memory/temp/genjutsu_output.txt
```

---

## 🎓 20 LEIS UCHIMON

Localizadas em `🔥LEIS_UCHIMON🔥/`:

- **LEI 00**: Identidade (UCHIMON ≠ SCRIPTUREMON)
- **LEI 01**: Reconexão obrigatória
- **LEI 02-19**: Regras de desenvolvimento, memória, testes, etc.

**Importante**: Sempre respeitar as LEIS ao modificar o sistema.

---

## ✅ VALIDAÇÃO DO SISTEMA

O `VALIDATE_SYSTEM.sh` executa 12 verificações:

1. ✅ Identidade (PROJECT_ID)
2. ✅ Sistemas Python (11 encontrados)
3. ✅ LEIS (20 encontradas)
4. ✅ Conhecimentos MEMORY (15 arquivos)
5. ✅ Database (68KB)
6. ✅ Git Hooks (pre-commit, post-commit)
7. ✅ Git Status
8. ✅ Genjutsu (rodando/inativo)
9. ✅ Testes (43 passed)
10. ✅ Memory System (operacional)
11. ✅ Distinção SCRIPTUREMON
12. ✅ Estrutura de diretórios

**Score esperado**: 12/12 ✅

---

## 🔧 GIT HOOKS

Hooks instalados no **repositório pai** (`../.git/hooks/`):

### pre-commit:
- Captura memórias antes do commit
- Salva decisões importantes
- Atualiza timestamp

### post-commit:
- Sincroniza memórias após commit
- Atualiza conhecimentos
- Log em `MEMORY/sync/sync.log`

**Ver atividade**:
```bash
tail -f MEMORY/sync/sync.log
```

---

## 🧪 TESTES

```bash
# Rodar todos os testes
pytest tests/ -v

# Testes específicos
pytest tests/test_memory.py -v
pytest tests/test_systems.py -v

# Coverage
pytest tests/ --cov=systems --cov-report=html
```

**Status atual**: 43 testes passando ✅

---

## 🐛 TROUBLESHOOTING

### Problema: Genjutsu não inicia
**Solução**: Criar diretório `memory/temp/`
```bash
mkdir -p memory/temp
python3 protection/genjutsu/GENJUTSU_UNIFIED.py &
```

### Problema: Database não encontrada
**Solução**: Verificar path
```bash
ls -lh MEMORY/claude_memory.db
# Deve mostrar ~68KB
```

### Problema: Memory System erro
**Solução**: Sincronizar manualmente
```bash
python3 sync_memory.py
python3 systems/unified_memory_system.py
```

### Problema: Testes falhando
**Solução**: Verificar venv e dependências
```bash
source venv/bin/activate
pip install -r requirements.txt
pytest tests/ -v
```

---

## 📦 DEPENDÊNCIAS

Python >= 3.11, < 3.14

```bash
# Instalar dependências
pip install -r requirements.txt

# Principais:
# - pytest >= 8.0.0
# - pytest-cov >= 4.0.0
# - (resto é stdlib)
```

---

## 🔥 DISTINÇÃO IMPORTANTE

### UCHIMON vs SCRIPTUREMON

- **UCHIMON** (`/claude_code/`): AI Developer system, memória, proteção
- **SCRIPTUREMON** (`/scripturemon-clean/`): Script Doctor, análise de roteiros

**Não confundir!** São projetos separados com propósitos distintos.

Ver: `MEMORY/conhecimentos/🔥🔥🔥DISTINÇÃO_PROJETOS🔥🔥🔥.md`

---

## 📞 COMANDOS ÚTEIS

```bash
# Validação completa
./scripts/VALIDATE_SYSTEM.sh

# Reconexão de contexto
./scripts/START_GENJUTSU.sh

# Backup databases
./MEMORY/backup_database.sh

# Sincronizar memórias
python3 scripts/sync_memory.py

# Status Memory System
python3 systems/unified_memory_system.py

# Ver conhecimentos
ls -lht MEMORY/conhecimentos/

# Ver últimas memórias
sqlite3 MEMORY/claude_memory.db "SELECT * FROM memories ORDER BY timestamp DESC LIMIT 5;"

# Verificar Genjutsu
ps aux | grep GENJUTSU_UNIFIED
```

---

## 🎯 PRÓXIMOS PASSOS

Após iniciar o sistema:

1. ✅ Execute `./scripts/START_GENJUTSU.sh`
2. ✅ Leia `REGRAS.md` (39 regras)
3. ✅ Verifique `./scripts/VALIDATE_SYSTEM.sh` (12/12)
4. ✅ Continue trabalhando com contexto preservado!

---

## 📝 CHANGELOG

- **2025-10-01**: Atualização completa do README
- **2025-09-29**: Sistema de backup automático adicionado
- **2025-09-28**: VALIDATE_SYSTEM.sh com 12 verificações
- **2025-09-22**: Reorganização estrutura (75% harmonia)
- **2025-09-17**: Criação inicial do sistema

---

**🔥 DIGIMUNDO PRESENTE!**

*Sistema UCHIMON - Zero Amnésia, 100% Contexto*
