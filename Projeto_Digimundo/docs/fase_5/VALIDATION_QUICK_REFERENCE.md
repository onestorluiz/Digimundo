# 🚀 Quick Reference: Documentation Validation Systems

> **TL;DR**: Comandos essenciais para validar e manter documentação sincronizada

---

## ⚡ Comandos Mais Usados

### 1. Validar Documentação (Local)

```bash
# Validação simples (somente relatório)
python3 scripts/phase5/validate_documentation.py

# Com auto-correção
python3 scripts/phase5/validate_documentation.py --auto-update

# Modo CI (exit code 1 se falhar)
python3 scripts/phase5/validate_documentation.py --ci-mode
```

### 2. Instalar/Atualizar Pre-Commit Hook

```bash
# Instalar hook (somente validação)
./scripts/phase5/install_validation_hook.sh

# Instalar hook com auto-update
./scripts/phase5/install_validation_hook.sh --auto-update

# Verificar se hook está instalado
ls -la .git/hooks/pre-commit

# Remover hook
rm .git/hooks/pre-commit
```

### 3. Bypass Validation (Emergências)

```bash
# Bypass pre-commit hook (use com cuidado!)
git commit --no-verify -m "emergency: fix production bug"
```

### 4. Ver Último Relatório

```bash
# Listar relatórios
ls -lt docs/fase_5/VALIDATION_REPORT_*.md | head -5

# Ver último relatório
cat $(ls -t docs/fase_5/VALIDATION_REPORT_*.md | head -1)
```

### 5. Ver Changelog de Métricas

```bash
# Ver histórico de updates automáticos
cat docs/fase_5/METRICS_UPDATE_LOG.md
```

---

## 🔧 Troubleshooting

### Problema: Validação Falha com Drift > 5%

**Sintoma**:
```
⚠️  duplications drift: 12.5% (expected 13903, got 15640)
❌ COMMIT BLOCKED
```

**Solução**:
```bash
# Opção 1: Auto-atualizar (recomendado)
python3 scripts/phase5/validate_documentation.py --auto-update
git add docs/fase_5/*.md scripts/phase5/validate_documentation.py
git commit -m "chore: update metrics after codebase changes"

# Opção 2: Investigar manualmente
python3 scripts/phase5/ai_semantic_analyzer.py --duplicates
# Analisar se o drift faz sentido
```

### Problema: Hook Não Executa

**Sintoma**: Commit passa sem validação

**Solução**:
```bash
# Verificar se hook existe
ls -la .git/hooks/pre-commit

# Verificar se é executável
chmod +x .git/hooks/pre-commit

# Re-instalar
./scripts/phase5/install_validation_hook.sh
```

### Problema: CI Failing no GitHub Actions

**Sintoma**: PR bloqueado por validation failure

**Solução**:
```bash
# 1. Rodar localmente
python3 scripts/phase5/validate_documentation.py

# 2. Ver o que falhou
cat $(ls -t docs/fase_5/VALIDATION_REPORT_*.md | head -1)

# 3. Auto-corrigir
python3 scripts/phase5/validate_documentation.py --auto-update

# 4. Commit e push
git add docs/fase_5/*.md
git commit -m "fix: sync documentation metrics"
git push
```

### Problema: AI Scripts Timeout

**Sintoma**: Validation trava ou demora >3min

**Solução**:
```bash
# Aumentar timeout no validate_documentation.py
# Linha 77: timeout=180 → timeout=300

# Ou executar AI scripts separadamente
python3 scripts/phase5/ai_semantic_analyzer.py --patterns
python3 scripts/phase5/ai_impact_analyzer.py --analyze app/models/
```

---

## 📊 Interpretando Resultados

### Status Codes

| Exit Code | Significado | Ação |
|-----------|-------------|------|
| 0 | ✅ Tudo OK | Continue normalmente |
| 1 | ❌ Validation failed | Veja relatório e corrija |

### Métricas e Tolerâncias

| Métrica | Threshold | O que significa |
|---------|-----------|----------------|
| Duplications | ±5% | Diferença aceitável: ±695 duplicações |
| Dead files | ±5% | Diferença aceitável: ±9 arquivos |
| Dead percentage | ±5% | Diferença aceitável: ±5% absoluto |
| ORM percentage | ±5% | Diferença aceitável: ±5% absoluto |

**Exemplo**:
```
✅ duplications: Expected 13903, Got 13891 (±0.1%)  ← OK (< 5%)
⚠️  duplications: Expected 13903, Got 15640 (±12.5%) ← DRIFT (> 5%)
```

---

## 🎯 Workflows Comuns

### Workflow 1: Antes de Abrir PR

```bash
# 1. Certifique-se que validação passa
python3 scripts/phase5/validate_documentation.py

# 2. Se falhar, auto-corrija
python3 scripts/phase5/validate_documentation.py --auto-update

# 3. Commit correções
git add docs/fase_5/*.md
git commit -m "chore: sync documentation"

# 4. Push e abra PR
git push origin feature-branch
```

### Workflow 2: Atualizar Baseline Após Refactoring

```bash
# Cenário: Você refatorou código e reduziu duplicações

# 1. Executar análise fresca
python3 scripts/phase5/ai_semantic_analyzer.py --duplicates --dead-code --patterns > /tmp/fresh_analysis.txt

# 2. Ver novas métricas
grep "more duplicates" /tmp/fresh_analysis.txt
grep "Dead files" /tmp/fresh_analysis.txt

# 3. Auto-atualizar documentação
python3 scripts/phase5/validate_documentation.py --auto-update

# 4. Commit como parte do refactoring
git add docs/fase_5/*.md scripts/phase5/validate_documentation.py
git commit -m "refactor: reduce duplications + update metrics

- Reduced semantic duplications from 13,903 to 11,245
- Metrics automatically updated by validation system"
```

### Workflow 3: Setup em Novo Clone do Repo

```bash
# 1. Clonar repo
git clone <repo-url>
cd <repo-name>

# 2. Instalar hook
./scripts/phase5/install_validation_hook.sh --auto-update

# 3. Validar estado atual
python3 scripts/phase5/validate_documentation.py

# Done! ✅
```

---

## 📖 Mais Informações

- **Sistema completo**: [BEYOND_SILICON_VALLEY_SYSTEMS.md](./BEYOND_SILICON_VALLEY_SYSTEMS.md)
- **Estratégia AI**: [AI_STRATEGY_MASTER.md](./AI_STRATEGY_MASTER.md)
- **Guias práticos**: [03_QUICK_START_GUIDES.md](./03_QUICK_START_GUIDES.md)

---

## 🆘 Suporte

**Se validação continua falhando**:

1. Leia o relatório completo: `docs/fase_5/VALIDATION_REPORT_*.md`
2. Execute AI scripts manualmente para debug
3. Verifique se scripts estão na versão correta
4. Abra issue com relatório anexado

**Bypass temporário** (somente emergências):
```bash
git commit --no-verify
```

---

**Última atualização**: 2025-11-16
**Versão**: 1.0.0

🤖 **Generated with [Claude Code](https://claude.com/claude-code)**
