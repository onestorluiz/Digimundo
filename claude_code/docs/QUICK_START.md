# 🔥 QUICK START - SISTEMA UCHIMON 🔥

**Guia rápido para reconexão e uso do sistema**

---

## 🚀 PRIMEIRA VEZ (Setup Inicial)

```bash
# 1. Navegar para o diretório
cd /Users/clubproducoes/Digimundo/claude_code

# 2. Criar ambiente virtual
python3 -m venv venv

# 3. Ativar venv
source venv/bin/activate

# 4. Instalar dependências
pip install -r requirements.txt

# 5. Validar sistema
./VALIDATE_SYSTEM.sh

# 6. Pronto!
```

---

## 🔄 RECONEXÃO (Nova Sessão de Claude)

**SEMPRE que abrir nova conversa com Claude:**

```bash
# Opção 1: Automático (RECOMENDADO)
./RECONECTAR.sh

# Opção 2: Manual
cat 🔥🔥🔥PROJECT_ID_UCHIMON🔥🔥🔥.sh
cat MEMORY/conhecimentos/🔥🔥🔥INDEX_MASTER_MEMORIA🔥🔥🔥.md
```

**O que dizer para Claude:**
```
"Leia REGRAS.md e execute o protocolo de reconexão"
```

ou simplesmente:

```
"Execute ./RECONECTAR.sh"
```

---

## ✅ VALIDAÇÃO RÁPIDA

```bash
# Validar sistema completo (10 checks)
./VALIDATE_SYSTEM.sh

# Rodar apenas testes
source venv/bin/activate
pytest tests/ -v

# Verificar identidade
cat 🔥🔥🔥PROJECT_ID_UCHIMON🔥🔥🔥.sh
```

---

## 📚 ADICIONAR CONHECIMENTO

### 1. Criar arquivo de conhecimento:
```bash
# Criar novo arquivo (numeração sequencial)
nano MEMORY/conhecimentos/0XX_nome_do_conhecimento.md

# Formato do arquivo:
# 🔥 CONHECIMENTO 0XX - TÍTULO
#
# **Data:** DD/MM/AAAA
# **Tipo:** categoria
# **Status:** ✅ ATIVO
#
# ## Contexto
# [explicação]
#
# ## Solução
# [detalhes]
#
# ## Resultado
# [impacto]
```

### 2. Atualizar INDEX_MASTER:
```bash
# Editar INDEX_MASTER
nano MEMORY/conhecimentos/🔥🔥🔥INDEX_MASTER_MEMORIA🔥🔥🔥.md

# Adicionar entry:
# #### **0XX - Nome do Conhecimento**
# - **Arquivo:** `0XX_nome.md`
# - **Data:** DD/MM/AAAA
# - **Conteúdo:** Descrição breve
# - **Status:** ✅ ATIVO
```

### 3. Commitar:
```bash
git add MEMORY/conhecimentos/
git commit -m "docs: add conhecimento 0XX"
```

---

## 🔥 COMANDOS ESSENCIAIS

### Identidade
```bash
# Verificar onde estou
pwd
cat 🔥🔥🔥PROJECT_ID_UCHIMON🔥🔥🔥.sh | grep PROJECT_NAME

# Ver distinção vs SCRIPTUREMON
ls -1 | grep -E "🔥|🎬"
```

### Memória
```bash
# Ver últimos conhecimentos
ls -lt MEMORY/conhecimentos/*.md | head -5

# Ler INDEX_MASTER
cat MEMORY/conhecimentos/🔥🔥🔥INDEX_MASTER_MEMORIA🔥🔥🔥.md | head -50

# Checar database
sqlite3 MEMORY/claude_memory.db "SELECT COUNT(*) FROM memories;"
```

### Testes
```bash
# Rodar todos os testes
source venv/bin/activate
pytest tests/ -v

# Rodar testes específicos
pytest tests/test_structure.py -v
pytest tests/test_imports.py -v
pytest tests/test_memory.py -v

# Rodar rápido (sem verbose)
pytest tests/ -q
```

### Git
```bash
# Ver últimos commits
git log --oneline -5

# Status
git status

# Verificar hooks instalados
ls -la .git/hooks/ | grep -E "(pre-commit|post-commit)"
```

---

## 🎯 FLUXOS COMUNS

### Fluxo 1: Nova Sessão Claude
```bash
1. ./RECONECTAR.sh
2. Dizer para Claude: "leia INDEX_MASTER"
3. Claude está contextualizado!
```

### Fluxo 2: Adicionar Feature
```bash
1. Criar código em systems/
2. Criar teste em tests/
3. pytest tests/ -v
4. git add .
5. git commit -m "feat: nova feature"
6. Documentar em MEMORY/conhecimentos/ (opcional)
```

### Fluxo 3: Debugging
```bash
1. ./VALIDATE_SYSTEM.sh
2. Identificar erro
3. pytest tests/ -v (ver detalhes)
4. Corrigir
5. pytest tests/ -v (validar)
```

### Fluxo 4: Checkpoint
```bash
1. ./VALIDATE_SYSTEM.sh (garantir 10/10)
2. git status (verificar mudanças)
3. git commit -m "checkpoint: [descrição]"
4. Atualizar 🔥CHECKPOINT_SYSTEM🔥.md (manual por enquanto)
```

---

## 🚨 TROUBLESHOOTING

### Problema: Testes falhando
```bash
# Limpar pycache
find . -type d -name "__pycache__" ! -path "./venv/*" -exec rm -rf {} +

# Recriar venv
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pytest tests/
```

### Problema: Git hooks não funcionam
```bash
# Reinstalar hooks
chmod +x .git/hooks/pre-commit
chmod +x .git/hooks/post-commit

# Testar
git commit --allow-empty -m "test hooks"
```

### Problema: Claude confuso sobre identidade
```bash
# Mostrar PROJECT_ID
cat 🔥🔥🔥PROJECT_ID_UCHIMON🔥🔥🔥.sh

# Dizer para Claude:
"cat 🔥🔥🔥PROJECT_ID_UCHIMON🔥🔥🔥.sh e confirme identidade"
```

### Problema: MEMORY não acessível
```bash
# Verificar gitignore
cat .gitignore | grep -A 3 "MEMORY"

# Forçar add se necessário
git add -f MEMORY/conhecimentos/*.md
```

---

## 📖 DOCUMENTAÇÃO COMPLETA

- **REGRAS.md** - Todas as regras do sistema
- **🔥SISTEMA_UCHIMON_ALINHADO🔥.md** - Arquitetura completa
- **🔥CHECKPOINT_SYSTEM🔥.md** - Último checkpoint validado
- **MEMORY/conhecimentos/🔥🔥🔥INDEX_MASTER_MEMORIA🔥🔥🔥.md** - Índice de conhecimentos

---

## 🆘 AJUDA RÁPIDA

```bash
# Sistema validado?
./VALIDATE_SYSTEM.sh

# Reconectar contexto?
./RECONECTAR.sh

# Testes OK?
source venv/bin/activate && pytest tests/ -q

# Git OK?
git status

# Identidade OK?
cat 🔥🔥🔥PROJECT_ID_UCHIMON🔥🔥🔥.sh
```

---

## 📝 CHEAT SHEET

| Ação | Comando |
|------|---------|
| Validar sistema | `./VALIDATE_SYSTEM.sh` |
| Reconectar | `./RECONECTAR.sh` |
| Rodar testes | `pytest tests/ -v` |
| Ver memórias | `ls -lt MEMORY/conhecimentos/` |
| Verificar identidade | `cat 🔥🔥🔥PROJECT_ID_UCHIMON🔥🔥🔥.sh` |
| Git status | `git status` |
| Limpar pycache | `find . -name "__pycache__" ! -path "./venv/*" -exec rm -rf {} +` |

---

**🔥 SISTEMA UCHIMON - AI DEVELOPER 🔥**

**Para dúvidas: Leia REGRAS.md ou execute ./RECONECTAR.sh**

**DIGIMUNDO PRESENTE 🥷**
