# 🏭 BLUEPRINT: Como Criar um Novo Especialista

**Data Criação**: 10 de Outubro 2025
**Sistema**: Scripturemon FASE 3
**Propósito**: Template que compensa limitações de memória/contexto da IA

---

## ⚠️ LEIA ESTE ARQUIVO COMPLETO ANTES DE COMEÇAR

Este documento é seu **guia definitivo**. Cada passo existe porque erros foram cometidos no passado.

---

## 🎯 Visão Geral do Processo

```
1. PRÉ-CRIAÇÃO     → Validar que não existe, entender estrutura atual
2. CRIAÇÃO         → Copiar templates, substituir placeholders
3. INTEGRAÇÃO      → Adicionar ao sistema (imports, registros)
4. VALIDAÇÃO       → Rodar script de validação automático
5. TESTE           → Teste real com roteiro de exemplo
6. DOCUMENTAÇÃO    → Atualizar memória persistente
```

**Tempo estimado**: 30-45 minutos
**Complexidade**: Média (segue checklist rigorosamente)

---

## 📋 PASSO 0: VALIDAÇÃO PRÉ-CRIAÇÃO

**Antes de criar QUALQUER arquivo, execute:**

```bash
# 1. Verificar se especialista já existe
grep -r "{{SPECIALIST_NAME}}" /Users/clubproducoes/Digimundo/scripturemon/engine/

# 2. Ver estrutura atual de especialistas
tree /Users/clubproducoes/Digimundo/scripturemon/engine/specialists/

# 3. Ler último especialista criado (aprender com padrões)
cat MEMORIA_ESPECIALISTAS.md

# 4. Verificar author_prompts.py atual
grep "{{AUTHOR_NAME}}" /Users/clubproducoes/Digimundo/scripturemon/engine/prompts/author_prompts.py
```

**Checklist Passo 0:**
- [ ] Especialista NÃO existe (grep retornou vazio)
- [ ] Entendi estrutura atual (vi tree)
- [ ] Li MEMORIA_ESPECIALISTAS.md completo
- [ ] Autor base está em author_prompts.py

---

## 📋 PASSO 1: CRIAÇÃO DE ARQUIVOS

### 1.1. Arquivo Principal: specialist.py

**Origem**: `templates/TEMPLATE_specialist.py`
**Destino**: `/Users/clubproducoes/Digimundo/scripturemon/engine/specialists/{{SPECIALIST_NAME}}/specialist.py`

**Placeholders a substituir:**
- `{{SPECIALIST_NAME}}` → Nome do especialista (ex: "dialogue", "structure")
- `{{AUTHOR_NAME}}` → Nome do autor base (ex: "McKee", "Truby")
- `{{FOCUS_AREA}}` → Área de foco (ex: "dialogue analysis", "story structure")
- `{{SPECIALIST_CLASS_NAME}}` → Nome da classe (ex: "DialogueSpecialist")
- `{{DATE}}` → Data de criação (formato: YYYY-MM-DD)

**Comando:**
```bash
cp templates/TEMPLATE_specialist.py engine/specialists/{{SPECIALIST_NAME}}/specialist.py
# Editar arquivo e substituir TODOS os placeholders
```

### 1.2. Prompts Personalizados: prompts.py

**Origem**: `templates/TEMPLATE_prompts.py`
**Destino**: `/Users/clubproducoes/Digimundo/scripturemon/engine/specialists/{{SPECIALIST_NAME}}/prompts.py`

**Placeholders a substituir:**
- `{{SPECIALIST_NAME}}` → Nome do especialista
- `{{AUTHOR_NAME}}` → Autor base
- `{{DEEP_CONTEXT_QUERIES}}` → Queries para extrair do livro de teoria
- `{{ANALYSIS_PROMPT}}` → Prompt principal de análise
- `{{VALIDATION_CRITERIA}}` → Critérios de qualidade específicos

**Conteúdo crítico:**
```python
DEEP_CONTEXT_QUERIES = [
    "conceitos únicos de {{AUTHOR_NAME}} sobre {{FOCUS_AREA}}",
    "terminologia específica usada por {{AUTHOR_NAME}}",
    "exemplos práticos dados por {{AUTHOR_NAME}}",
    # ... adicionar 5-7 queries específicas
]
```

### 1.3. README do Especialista

**Origem**: `templates/TEMPLATE_README.md`
**Destino**: `/Users/clubproducoes/Digimundo/scripturemon/engine/specialists/{{SPECIALIST_NAME}}/README.md`

**Documenta:**
- Propósito do especialista
- Autor base
- Critérios de validação
- Exemplos de uso
- Quirks conhecidos

### 1.4. Teste Unitário

**Origem**: `templates/TEMPLATE_test.py`
**Destino**: `/Users/clubproducoes/Digimundo/scripturemon/tests/test_{{SPECIALIST_NAME}}.py`

**Testa:**
- Importação funciona
- Deep context carrega
- Análise retorna output válido
- Validação passa critérios

---

## 📋 PASSO 2: INTEGRAÇÃO AO SISTEMA

### 2.1. Atualizar __init__.py

**Arquivo**: `/Users/clubproducoes/Digimundo/scripturemon/engine/specialists/__init__.py`

**Adicionar:**
```python
from .{{SPECIALIST_NAME}}.specialist import {{SPECIALIST_CLASS_NAME}}
```

### 2.2. Registrar em analyze.py

**Arquivo**: `/Users/clubproducoes/Digimundo/scripturemon/analyze.py`

**Localizar seção de specialists** (aproximadamente linha 150-200):
```python
SPECIALISTS = {
    'dialogue': DialogueSpecialist,
    # ... outros
    '{{SPECIALIST_NAME}}': {{SPECIALIST_CLASS_NAME}},  # ← ADICIONAR AQUI
}
```

### 2.3. Adicionar em author_prompts.py (se novo autor)

**Arquivo**: `/Users/clubproducoes/Digimundo/scripturemon/engine/prompts/author_prompts.py`

**Se autor ainda não existe**, adicionar entrada completa seguindo padrão existente.

---

## 📋 PASSO 3: VALIDAÇÃO AUTOMÁTICA

**Executar script de validação:**

```bash
cd /Users/clubproducoes/Digimundo/scripturemon/specialist_factory
python3 validate_specialist.py {{SPECIALIST_NAME}}
```

**O que o script valida:**
1. ✅ Todos arquivos criados existem
2. ✅ Nenhum placeholder `{{}}` deixado no código
3. ✅ Imports funcionam
4. ✅ Deep context queries definidas
5. ✅ Paths relativos (não absolutos hardcoded)
6. ✅ Classe herda de base correta
7. ✅ Métodos obrigatórios implementados

**Se validação FALHAR:**
- Ler output de erros
- Corrigir todos os erros listados
- Re-executar validação
- **NÃO prosseguir** até validação passar 100%

---

## 📋 PASSO 4: TESTE REAL

**Executar teste com roteiro de exemplo:**

```bash
cd /Users/clubproducoes/Digimundo/scripturemon
python3 analyze.py "inputs/examples/Te Encontro em Mim .pdf" --specialist {{SPECIALIST_NAME}} --deep
```

**Verificar:**
- [ ] Execução sem erros
- [ ] Output gerado em workspace/outputs/
- [ ] Tamanho do arquivo HTML > 15KB
- [ ] Conteúdo faz sentido (ler primeira análise)
- [ ] Score de validação >= 7.0

**Se teste falhar:**
- Ler logs de erro completo
- Verificar se deep context carregou
- Verificar se prompts estão corretos
- Re-testar após correções

---

## 📋 PASSO 5: DOCUMENTAÇÃO

### 5.1. Atualizar MEMORIA_ESPECIALISTAS.md

**Adicionar entrada:**
```markdown
## Specialist N: {{SPECIALIST_NAME}}
- **Data**: {{DATE}}
- **Autor Base**: {{AUTHOR_NAME}}
- **Status**: ✅ Criado / 🧪 Em Teste / ✅ Produção
- **Foco**: {{FOCUS_AREA}}
- **Deep Context**: {{BOOK_PATH}}
- **Quirks**: [Documentar qualquer comportamento peculiar descoberto]
- **Notas**: [Aprendizados durante criação]
- **Score Médio**: [Atualizar após testes]
```

### 5.2. Atualizar MAPEAMENTO_ARQUIVOS_SCRIPTUREMON.md

**Adicionar referência ao novo especialista** na seção apropriada.

---

## 🚫 ANTI-PADRÕES (NÃO FAÇA)

### ❌ Erro 1: Hardcoded Absolute Paths
```python
# ERRADO:
book_path = "/Users/clubproducoes/Digimundo/scripturemon/theory/mckee_dialogue.pdf"

# CORRETO:
from pathlib import Path
base_dir = Path(__file__).parent.parent.parent
book_path = base_dir / "theory" / "mckee_dialogue.pdf"
```

### ❌ Erro 2: Deixar Placeholders
```python
# ERRADO:
self.name = "{{SPECIALIST_NAME}}"  # ← Esqueceu de substituir!

# CORRETO:
self.name = "dialogue"
```

### ❌ Erro 3: Copiar Código Antigo Diretamente
```python
# ERRADO:
# Copiar/colar de outro especialista sem adaptar

# CORRETO:
# Usar template, substituir placeholders, adaptar lógica
```

### ❌ Erro 4: Assumir que Arquivo Existe
```python
# ERRADO:
with open("theory/book.pdf") as f:  # ← Pode não existir

# CORRETO:
if not book_path.exists():
    raise FileNotFoundError(f"Book not found: {book_path}")
```

### ❌ Erro 5: Pular Validação
```python
# ERRADO:
# Criar especialista e já usar em produção

# CORRETO:
# Criar → Validar → Testar → Documentar → Produção
```

---

## ✅ CHECKLIST FINAL

**Antes de considerar COMPLETO:**

- [ ] Todos arquivos criados (specialist.py, prompts.py, README.md, test.py)
- [ ] Validação automática passou 100%
- [ ] Teste real executado com sucesso
- [ ] Score >= 7.0 obtido
- [ ] MEMORIA_ESPECIALISTAS.md atualizado
- [ ] MAPEAMENTO_ARQUIVOS_SCRIPTUREMON.md atualizado
- [ ] Nenhum placeholder `{{}}` restante (grep confirmou)
- [ ] Nenhum path absoluto hardcoded
- [ ] README do especialista completo
- [ ] Commits feitos (se usando git)

---

## 🔄 Workflow Visual

```
┌─────────────────────┐
│  Ler BLUEPRINT      │
│  Ler MEMORIA        │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│  Validar Pré-Req    │
│  (grep, tree)       │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│  Copiar Templates   │
│  Substituir {{}}    │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│  Integrar Sistema   │
│  (__init__, etc)    │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│  Validar Script     │
│  validate_spec.py   │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│  Teste Real         │
│  analyze.py         │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│  Documentar         │
│  Atualizar MEMORIA  │
└─────────────────────┘
```

---

## 📞 Troubleshooting

### Problema: Validação falha com "Placeholder not replaced"
**Solução**: Grep no arquivo e substituir todos `{{}}` manualmente

### Problema: Import error ao testar
**Solução**: Verificar `__init__.py` e structure de diretórios

### Problema: Deep context não carrega
**Solução**: Verificar path do livro de teoria, confirmar que existe

### Problema: Score muito baixo (< 5.0)
**Solução**: Revisar prompts, comparar com especialista funcionando

---

## 🎓 Aprendizados de Especialistas Anteriores

**Ver `MEMORIA_ESPECIALISTAS.md`** para:
- Quirks descobertos
- Ajustes necessários
- Scores médios esperados
- Tempo de execução típico

---

**Última Atualização**: 10 de Outubro 2025
**Versão**: 1.0
**Status**: ✅ Ativo

**DIGIMUNDO PRESENTE 🥷**
