# 🚀 QUICK START GUIDE - Phase 5 Scripts

**Versão**: 2.0
**Status**: ✅ Pronto para uso

---

## ⚡ TL;DR (Uso Rápido)

```bash
# Verificar se arquivo já existe antes de criar
python3 scripts/phase5/check_file_exists.py app/services/new_service.py

# Validar todos os imports
python3 scripts/phase5/validate_imports.py

# Ver progresso da implementação
python3 scripts/phase5/show_progress.py

# Sincronizar manifest com filesystem
python3 scripts/phase5/sync_manifest.py --dry-run

# ✅ Funciona de QUALQUER diretório!
```

---

## 📋 Scripts Disponíveis

### 1. check_file_exists.py

**Propósito**: Prevenir criação de arquivos duplicados

**Uso**:
```bash
python3 scripts/phase5/check_file_exists.py <caminho-do-arquivo>
```

**Exemplos**:
```bash
# Verificar se EventStoreService já existe
python3 scripts/phase5/check_file_exists.py app/services/event_store_service.py

# Output: ✅ File does NOT exist (safe to create)
# Exit code: 0 (pode criar)

# Verificar arquivo que JÁ existe
python3 scripts/phase5/check_file_exists.py app/services/scene_service.py

# Output: ❌ File EXISTS
# Exit code: 1 (NÃO criar - duplicaria!)
```

**Quando usar**:
- ✅ Antes de criar qualquer arquivo novo
- ✅ Quando não tiver certeza se arquivo já existe
- ✅ Em scripts de automação para prevenção

---

### 2. validate_imports.py

**Propósito**: Validar todos os imports após refatoração

**Uso**:
```bash
# Validar tudo
python3 scripts/phase5/validate_imports.py

# Validar arquivo específico
python3 scripts/phase5/validate_imports.py --file app/services/scene_service.py
```

**Output**:
```
🔍 Validating imports...

======================================================================
IMPORT VALIDATION RESULTS
======================================================================

Total imports checked: 1880
✅ Valid:  1880
❌ Broken: 0

✅ All imports are valid!
```

**Quando usar**:
- ✅ Após renomear/mover arquivos
- ✅ Após refatoração grande
- ✅ Antes de fazer commit
- ✅ Em CI/CD pipeline

---

### 3. show_progress.py

**Propósito**: Dashboard visual do progresso da Fase 5

**Uso**:
```bash
# Progresso geral
python3 scripts/phase5/show_progress.py

# Progresso de uma fase específica
python3 scripts/phase5/show_progress.py --phase 5.1

# Listar arquivos por estado
python3 scripts/phase5/show_progress.py --state planned

# Detalhado (arquivo por arquivo)
python3 scripts/phase5/show_progress.py --detailed
```

**Output**:
```
┌────────────────────────────────────────────────────┐
│ FASE 5 - PLATFORM EVOLUTION                        │
│ Overall Implementation Progress                    │
├────────────────────────────────────────────────────┤
│ Progress: ░░░░░░░░░░░░░░░░░░░░░░░░ 0%             │
│                                                    │
│ ✅ Finalized:      0 files                         │
│ 🟡 In Progress:    0 files                         │
│ ⏳ Planned:       21 files                         │
│                                                    │
│ Total Files:      26                               │
└────────────────────────────────────────────────────┘
```

**Quando usar**:
- ✅ Daily standup (ver progresso)
- ✅ Sprint planning (estimar trabalho)
- ✅ Code review (verificar completude)
- ✅ Reporting para stakeholders

---

### 4. sync_manifest.py

**Propósito**: Sincronizar FILE_MANIFEST.yaml com realidade do filesystem

**Uso**:
```bash
# Preview changes (dry run)
python3 scripts/phase5/sync_manifest.py --dry-run

# Apply changes
python3 scripts/phase5/sync_manifest.py
```

**Output**:
```
🔄 Syncing FILE_MANIFEST.yaml with filesystem...

📊 Checking file states...
✓ Found 1 state changes:
  ⚠  tests/unit/test_old.py: deprecated but still exists

📂 Scanning for untracked files...
⚠️  Found 198 untracked files:
  - app/models/activity.py
  - app/models/budget.py
  ... and 196 more

Summary:
  State changes: 1
  Untracked files: 198
```

**Quando usar**:
- ✅ Após criar arquivos novos
- ✅ Após deletar arquivos antigos
- ✅ Semanalmente (manter manifest atualizado)
- ✅ Antes de code review importante

---

## 🔄 Workflows Comuns

### Workflow 1: Criar Novo Arquivo

```bash
# 1. Verificar se já existe
python3 scripts/phase5/check_file_exists.py app/services/conflict_detection_service.py
# → ✅ File does NOT exist

# 2. Criar o arquivo (no seu IDE favorito)
# ...

# 3. Sincronizar manifest
python3 scripts/phase5/sync_manifest.py

# 4. Ver progresso atualizado
python3 scripts/phase5/show_progress.py --phase 5.2
```

### Workflow 2: Refatoração Grande

```bash
# 1. ANTES de refatorar - validar imports estão ok
python3 scripts/phase5/validate_imports.py
# → ✅ All imports valid (baseline)

# 2. Fazer refatoração (renomear, mover arquivos, etc.)
# ...

# 3. Validar imports novamente
python3 scripts/phase5/validate_imports.py
# → ❌ Se houver quebrados, vai mostrar quais

# 4. Corrigir imports quebrados
# ...

# 5. Validar novamente até 100%
python3 scripts/phase5/validate_imports.py
# → ✅ All imports valid

# 6. Rodar testes
pytest tests/ -v

# 7. Sincronizar manifest
python3 scripts/phase5/sync_manifest.py

# 8. Commit
git add .
git commit -m "Refactor: rename service X to Y"
```

### Workflow 3: Daily Standup

```bash
# Morning routine (2 minutos)

# 1. Sincronizar manifest
python3 scripts/phase5/sync_manifest.py

# 2. Ver progresso
python3 scripts/phase5/show_progress.py

# 3. Ver próximos arquivos a implementar
python3 scripts/phase5/show_progress.py --state planned --phase 5.1 --detailed

# 4. Compartilhar progresso no standup
# "Ontem: implementei 3 arquivos da fase 5.1"
# "Hoje: vou implementar EventStoreService"
# "Bloqueadores: nenhum"
```

### Workflow 4: Code Review

```bash
# Checklist para aprovação de PR

# 1. Validar imports
python3 scripts/phase5/validate_imports.py
# → ✅ Must pass

# 2. Verificar manifest sync
python3 scripts/phase5/sync_manifest.py --dry-run
# → ⚠️ Se houver untracked files, pedir para adicionar ao manifest

# 3. Verificar progresso
python3 scripts/phase5/show_progress.py
# → Ver se progresso aumentou conforme esperado

# 4. Se tudo ok, aprovar PR
# ✅ Imports: valid
# ✅ Manifest: synced
# ✅ Progress: +X files
```

---

## 💡 Dicas Pro

### Dica 1: Alias no Shell

Adicione ao seu `.bashrc` ou `.zshrc`:

```bash
# Phase 5 Scripts Aliases
alias p5check='python3 scripts/phase5/check_file_exists.py'
alias p5validate='python3 scripts/phase5/validate_imports.py'
alias p5progress='python3 scripts/phase5/show_progress.py'
alias p5sync='python3 scripts/phase5/sync_manifest.py'

# Uso:
# p5check app/services/new_file.py
# p5validate
# p5progress --phase 5.1
# p5sync --dry-run
```

### Dica 2: VSCode Tasks

Adicione ao `.vscode/tasks.json`:

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Phase 5: Check file exists",
      "type": "shell",
      "command": "python3",
      "args": [
        "${workspaceFolder}/scripts/phase5/check_file_exists.py",
        "${relativeFile}"
      ],
      "group": "test"
    },
    {
      "label": "Phase 5: Validate imports",
      "type": "shell",
      "command": "python3",
      "args": [
        "${workspaceFolder}/scripts/phase5/validate_imports.py"
      ],
      "group": "test"
    },
    {
      "label": "Phase 5: Show progress",
      "type": "shell",
      "command": "python3",
      "args": [
        "${workspaceFolder}/scripts/phase5/show_progress.py"
      ],
      "group": "test"
    }
  ]
}
```

### Dica 3: Pre-commit Hook

Crie `.git/hooks/pre-commit`:

```bash
#!/bin/bash

echo "🔍 Validating imports before commit..."
python3 scripts/phase5/validate_imports.py

if [ $? -ne 0 ]; then
    echo "❌ Commit blocked: broken imports detected"
    echo "Fix imports and try again"
    exit 1
fi

echo "✅ All imports valid"
exit 0
```

```bash
chmod +x .git/hooks/pre-commit
```

### Dica 4: GitHub Actions

Crie `.github/workflows/phase5-validation.yml`:

```yaml
name: Phase 5 Validation

on:
  pull_request:
    branches: [main, develop]
  push:
    branches: [main, develop]

jobs:
  validate:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: pip install pyyaml

      - name: Validate imports
        run: python3 scripts/phase5/validate_imports.py

      - name: Check manifest sync
        run: python3 scripts/phase5/sync_manifest.py --dry-run

      - name: Show progress
        run: python3 scripts/phase5/show_progress.py
```

---

## ❓ Troubleshooting

### Problema: "FileNotFoundError: FILE_MANIFEST.yaml not found"

**Causa**: Script não conseguiu encontrar FILE_MANIFEST.yaml

**Solução**:
```bash
# Verificar se arquivo existe
ls docs/fase_5/FILE_MANIFEST.yaml

# Se não existir, está no lugar errado
# FILE_MANIFEST deve estar em Projeto_Digimundo/docs/fase_5/
```

### Problema: "ModuleNotFoundError: No module named 'yaml'"

**Causa**: PyYAML não instalado

**Solução**:
```bash
pip install pyyaml

# Verificar instalação
python3 -c "import yaml; print(yaml.__version__)"
```

### Problema: Scripts não encontram arquivos Python

**Causa**: Executando do diretório errado ou estrutura de projeto diferente

**Solução**:
```bash
# Verificar estrutura esperada
ls cineprod-flask/app/
ls cineprod-flask/tests/

# Se estrutura estiver correta, scripts devem auto-detectar
# Se não estiver, verificar implementação de detect_project_root()
```

---

## 📚 Documentação Adicional

Para mais informações, consulte:

- **ARCHITECTURE_CHANGE_MANAGEMENT_SYSTEM.md** - Sistema completo
- **FILE_MANIFEST.yaml** - Source of truth para todos os arquivos
- **MIGRATION_PLAN.md** - Plano de migração fase por fase
- **SYSTEM_TESTING_REPORT.md** - Relatório de testes completo
- **AUTO_DETECTION_IMPLEMENTATION_SUMMARY.md** - Detalhes técnicos da implementação

---

## ✅ Checklist de Uso Diário

### Morning (2 min)
- [ ] `python3 scripts/phase5/sync_manifest.py`
- [ ] `python3 scripts/phase5/show_progress.py`

### Antes de Criar Arquivo (10 seg)
- [ ] `python3 scripts/phase5/check_file_exists.py <path>`

### Após Refatoração (1 min)
- [ ] `python3 scripts/phase5/validate_imports.py`
- [ ] `python3 scripts/phase5/sync_manifest.py`

### Antes de Commit (30 seg)
- [ ] `python3 scripts/phase5/validate_imports.py`

### End of Day (1 min)
- [ ] `python3 scripts/phase5/sync_manifest.py`
- [ ] `python3 scripts/phase5/show_progress.py`

---

**Criado por**: Claude Code (Sonnet 4.5)
**Versão**: 2.0
**Data**: 2025-11-16

🎯 **DIGIMUNDO PRESENTE** 🥷
