# 🏭 Specialist Factory

**Sistema de criação de especialistas para Scripturemon**
**Versão**: 1.0
**Data**: 10 de Outubro 2025

---

## 🎯 O Que É Isto?

Um sistema **simbiótico** que trabalha **COM** as limitações naturais da IA, não contra elas.

### Problema Que Resolve

Quando uma IA cria código repetitivamente:
- ❌ Perde contexto entre sessões
- ❌ Esquece detalhes críticos
- ❌ Repete erros
- ❌ Assume coisas sem verificar
- ❌ Deixa placeholders e referências quebradas

### Como Resolve

Este sistema **força** a IA a fazer o certo usando seu comportamento automático:
- ✅ Templates com placeholders explícitos
- ✅ Checklists passo-a-passo
- ✅ Validação automática que pega erros
- ✅ Memória persistente entre sessões
- ✅ Blueprints que contextualizam

---

## 📂 Estrutura

```
specialist_factory/
├── README.md                    # Este arquivo
├── BLUEPRINT_SPECIALIST.md      # Guia completo de criação
├── CHECKLIST_CRIACAO.md         # Checklist passo-a-passo
├── MEMORIA_ESPECIALISTAS.md     # Histórico persistente
├── validate_specialist.py       # Script de validação automática
│
└── templates/                   # Templates prontos
    ├── TEMPLATE_specialist.py   # Código do especialista
    ├── TEMPLATE_prompts.py      # Prompts personalizados
    ├── TEMPLATE_README.md       # Documentação
    └── TEMPLATE_test.py         # Testes unitários
```

---

## 🚀 Como Usar

### Para Humanos

Quando quiser criar um novo especialista:

```bash
cd /Users/clubproducoes/Digimundo/scripturemon/specialist_factory

# Diga para a IA:
"Crie um novo especialista chamado [NOME] baseado no autor [AUTOR]
focando em [ÁREA]. Siga o specialist_factory."
```

A IA vai automaticamente:
1. Ler BLUEPRINT_SPECIALIST.md
2. Ler MEMORIA_ESPECIALISTAS.md
3. Seguir CHECKLIST_CRIACAO.md
4. Criar arquivos a partir de templates
5. Rodar validate_specialist.py
6. Atualizar MEMORIA_ESPECIALISTAS.md

### Para IAs (Claude/Outras)

**Quando humano pedir para criar especialista:**

```markdown
1. Read: specialist_factory/BLUEPRINT_SPECIALIST.md
2. Read: specialist_factory/MEMORIA_ESPECIALISTAS.md
3. Read: specialist_factory/CHECKLIST_CRIACAO.md
4. Seguir checklist RIGOROSAMENTE
5. Após criação: bash python3 validate_specialist.py <nome>
6. Se validação falhar: corrigir e re-validar
7. Atualizar MEMORIA_ESPECIALISTAS.md
```

**NÃO pule nenhum passo. NÃO assuma que leu antes. SEMPRE leia novamente.**

---

## 📋 Workflow Visual

```
Humano pede novo especialista
         │
         ▼
    [IA lê BLUEPRINT]
         │
         ▼
    [IA lê MEMORIA]
         │
         ▼
    [IA lê CHECKLIST]
         │
         ▼
    [IA copia templates]
         │
         ▼
  [IA substitui {{placeholders}}]
         │
         ▼
    [IA integra ao sistema]
         │
         ▼
  [IA roda validate_specialist.py]
         │
         ├─── PASSOU ────┐
         │               ▼
         │          [Teste real]
         │               │
         │               ▼
         │       [Atualiza MEMORIA]
         │               │
         │               ▼
         │           ✅ PRONTO
         │
         └─── FALHOU ───┐
                        ▼
                  [Corrige erros]
                        │
                        ▼
                  [Re-valida] ──┐
                                │
                                └──> (loop até passar)
```

---

## 🧪 Validação Automática

O script `validate_specialist.py` verifica:

1. ✅ Todos arquivos criados existem
2. ✅ Nenhum placeholder `{{}}` deixado
3. ✅ Imports funcionam
4. ✅ Paths são relativos (não absolutos)
5. ✅ Deep context queries definidas
6. ✅ Critérios de validação implementados
7. ✅ Classe tem métodos obrigatórios

**Uso:**
```bash
python3 validate_specialist.py dialogue
```

**Output esperado:**
```
🔍 Validating Specialist: dialogue
================================================================================

📁 Checking files exist...
📦 Checking imports...
🗂️  Checking for hardcoded paths...
🔍 Checking deep context queries...
✅ Checking validation criteria...
🏗️  Checking class structure...

================================================================================
📊 VALIDATION RESULTS
================================================================================

✅ PASSED (25 checks):
   ✓ File exists: specialist.py
   ✓ File exists: prompts.py
   ... (etc)

================================================================================
✅ ✅ ✅  VALIDATION PASSED  ✅ ✅ ✅

Specialist is ready for testing!
================================================================================
```

---

## 📚 Arquivos Principais

### 1. BLUEPRINT_SPECIALIST.md
**O que é**: Guia completo e detalhado
**Quando ler**: SEMPRE antes de criar especialista
**Contém**:
- Passo-a-passo completo
- Anti-padrões a evitar
- Troubleshooting
- Checklist final

### 2. CHECKLIST_CRIACAO.md
**O que é**: Checklist interativo passo-a-passo
**Quando usar**: Durante criação do especialista
**Contém**:
- Checkboxes para cada etapa
- Comandos exatos a executar
- Validações intermediárias

### 3. MEMORIA_ESPECIALISTAS.md
**O que é**: Memória persistente entre sessões
**Quando atualizar**: Após CADA criação/modificação
**Contém**:
- Histórico de especialistas
- Quirks descobertos
- Erros comuns e soluções
- Métricas de referência

### 4. validate_specialist.py
**O que é**: Script de validação automática
**Quando rodar**: Após criação, antes de testar
**Valida**:
- Arquivos existem
- Placeholders substituídos
- Imports funcionam
- Código bem estruturado

---

## 🎓 Filosofia do Sistema

### Princípio 1: Assume Zero Memória
IA esquece tudo entre sessões → Documentos persistentes

### Princípio 2: Força Verificação
IA assume coisas → Checklist força grep/read

### Princípio 3: Auto-Validação
IA deixa erros → Script pega automaticamente

### Princípio 4: Aprendizado Acumulativo
Cada erro vira padrão documentado → Nunca repete

### Princípio 5: Simbiótico
Trabalha COM comportamento natural da IA, não contra

---

## ✅ Garantias do Sistema

Se seguir 100% do processo:

- ✅ Nenhum placeholder `{{}}` esquecido
- ✅ Nenhum path absoluto hardcoded
- ✅ Imports sempre funcionam
- ✅ Deep context sempre carrega
- ✅ Validação sempre consistente
- ✅ Documentação sempre atualizada
- ✅ Histórico sempre preservado

---

## 🔧 Manutenção

### Adicionar Novo Tipo de Validação

Edite `validate_specialist.py` e adicione método:
```python
def _check_nova_validacao(self):
    """Descrição da validação."""
    # Implementar
    pass
```

Chame no método `validate()`.

### Melhorar Templates

Edite arquivos em `templates/`:
- `TEMPLATE_specialist.py` - Código base
- `TEMPLATE_prompts.py` - Prompts
- `TEMPLATE_README.md` - Documentação

**Importante**: Mantenha placeholders `{{}}` claros.

### Documentar Novo Padrão

Quando descobrir erro/quirk:
1. Edite `MEMORIA_ESPECIALISTAS.md`
2. Adicione na seção apropriada
3. Descreva problema e solução
4. Marque "aplicar em futuros"

---

## 📊 Métricas de Sucesso

**Sistema funciona se:**
- Tempo de criação: ~30-45 min (consistente)
- Taxa de erro: <5% após validação
- Especialistas passam em teste real: >90%
- Documentação sempre atualizada

**Medir mensalmente:**
- Quantos especialistas criados
- Quantos passaram validação na primeira
- Quantos erros repetidos (deve ser 0)
- Tempo médio de criação

---

## 🚨 Troubleshooting

### "validate_specialist.py não encontra arquivos"
**Causa**: Paths incorretos
**Solução**: Rodar de dentro de `specialist_factory/`

### "Import error ao validar"
**Causa**: Estrutura de diretórios errada
**Solução**: Verificar que `engine/specialists/<nome>/` existe

### "Muitos placeholders esquecidos"
**Causa**: Não seguiu checklist
**Solução**: Ler CHECKLIST_CRIACAO.md e seguir rigorosamente

### "Validação passa mas teste real falha"
**Causa**: Prompts ruins ou deep context não carrega
**Solução**: Revisar prompts comparando com especialista funcionando

---

## 🎯 Próximos Passos

Após criar este sistema:

1. **Criar primeiro especialista** usando o sistema
2. **Documentar quirks** descobertos
3. **Iterar templates** se necessário
4. **Expandir validações** conforme encontra erros

---

## 📞 Suporte

Se sistema não funcionar como esperado:

1. Ler `MEMORIA_ESPECIALISTAS.md` para padrões conhecidos
2. Verificar que seguiu 100% do checklist
3. Rodar validate_specialist.py e ler erros
4. Comparar com especialista funcionando

---

## 🏆 Créditos

**Criado por**: Claude Code + Digimundo
**Data**: 10 de Outubro 2025
**Versão**: 1.0

**Filosofia**: Sistemas que compensam limitações são melhores que lutar contra elas.

---

**DIGIMUNDO PRESENTE 🥷**

**"O sistema não te torna perfeito. Te torna consistente."**
