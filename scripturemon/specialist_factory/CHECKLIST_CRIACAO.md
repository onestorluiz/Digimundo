# ✅ CHECKLIST: Criar Novo Especialista

**Especialista**: `{{SPECIALIST_NAME}}`
**Autor Base**: `{{AUTHOR_NAME}}`
**Data Início**: `{{DATE}}`

---

## 📖 FASE 0: LEITURA OBRIGATÓRIA

- [ ] Li `BLUEPRINT_SPECIALIST.md` **COMPLETO** (não pulei nenhuma seção)
- [ ] Li `MEMORIA_ESPECIALISTAS.md` para aprender com anteriores
- [ ] Entendi o fluxo: Pré-criação → Criação → Integração → Validação → Teste → Documentação

**Tempo estimado desta fase**: 10 minutos

---

## 🔍 FASE 1: PRÉ-CRIAÇÃO (Validações)

### 1.1. Verificar Duplicatas

```bash
cd /Users/clubproducoes/Digimundo/scripturemon
grep -r "{{SPECIALIST_NAME}}" engine/
```

- [ ] Comando executado
- [ ] Resultado: VAZIO (especialista não existe)
- [ ] Se NÃO vazio: PARAR e escolher outro nome

### 1.2. Entender Estrutura Atual

```bash
tree engine/specialists/ -L 2
```

- [ ] Comando executado
- [ ] Vi estrutura de outros especialistas
- [ ] Entendi organização de arquivos

### 1.3. Verificar Autor Base

```bash
grep "{{AUTHOR_NAME}}" engine/prompts/author_prompts.py
```

- [ ] Comando executado
- [ ] Autor EXISTE em author_prompts.py
- [ ] Se NÃO existe: Preciso criar entrada do autor também

### 1.4. Verificar Livro de Teoria

```bash
ls -lh theory/ | grep -i "{{AUTHOR_NAME}}"
```

- [ ] Comando executado
- [ ] Livro do autor EXISTE em theory/
- [ ] Anotei path completo: `_______________`

**Tempo estimado desta fase**: 5 minutos

---

## 🏗️ FASE 2: CRIAÇÃO DE ARQUIVOS

### 2.1. Criar Diretório do Especialista

```bash
mkdir -p engine/specialists/{{SPECIALIST_NAME}}
```

- [ ] Diretório criado
- [ ] Caminho: `engine/specialists/{{SPECIALIST_NAME}}/`

### 2.2. Criar specialist.py

```bash
cp specialist_factory/templates/TEMPLATE_specialist.py \
   engine/specialists/{{SPECIALIST_NAME}}/specialist.py
```

- [ ] Arquivo copiado
- [ ] Abri arquivo para edição
- [ ] Substituí `{{SPECIALIST_NAME}}` → `_______________`
- [ ] Substituí `{{AUTHOR_NAME}}` → `_______________`
- [ ] Substituí `{{FOCUS_AREA}}` → `_______________`
- [ ] Substituí `{{SPECIALIST_CLASS_NAME}}` → `_______________`
- [ ] Substituí `{{DATE}}` → `_______________`
- [ ] Ajustei path do livro de teoria (linha ~45)
- [ ] Salvei arquivo

**Grep de verificação:**
```bash
grep "{{" engine/specialists/{{SPECIALIST_NAME}}/specialist.py
```

- [ ] Grep retornou VAZIO (nenhum placeholder restante)

### 2.3. Criar prompts.py

```bash
cp specialist_factory/templates/TEMPLATE_prompts.py \
   engine/specialists/{{SPECIALIST_NAME}}/prompts.py
```

- [ ] Arquivo copiado
- [ ] Substituí `{{SPECIALIST_NAME}}` → `_______________`
- [ ] Substituí `{{AUTHOR_NAME}}` → `_______________`
- [ ] Criei 5-7 deep context queries específicas
- [ ] Escrevi prompt principal de análise
- [ ] Defini critérios de validação
- [ ] Salvei arquivo

**Grep de verificação:**
```bash
grep "{{" engine/specialists/{{SPECIALIST_NAME}}/prompts.py
```

- [ ] Grep retornou VAZIO

### 2.4. Criar README.md

```bash
cp specialist_factory/templates/TEMPLATE_README.md \
   engine/specialists/{{SPECIALIST_NAME}}/README.md
```

- [ ] Arquivo copiado
- [ ] Documentei propósito do especialista
- [ ] Listei critérios de validação
- [ ] Adicionei exemplo de uso
- [ ] Salvei arquivo

### 2.5. Criar Teste

```bash
cp specialist_factory/templates/TEMPLATE_test.py \
   tests/test_{{SPECIALIST_NAME}}.py
```

- [ ] Arquivo copiado
- [ ] Adaptei teste para especialista
- [ ] Salvei arquivo

**Tempo estimado desta fase**: 20 minutos

---

## 🔗 FASE 3: INTEGRAÇÃO AO SISTEMA

### 3.1. Atualizar __init__.py

```bash
# Editar: engine/specialists/__init__.py
```

**Adicionar linha:**
```python
from .{{SPECIALIST_NAME}}.specialist import {{SPECIALIST_CLASS_NAME}}
```

- [ ] Linha adicionada
- [ ] Salvei arquivo

### 3.2. Registrar em analyze.py

```bash
# Editar: analyze.py (aproximadamente linha 150-200)
```

**Adicionar no dicionário SPECIALISTS:**
```python
'{{SPECIALIST_NAME}}': {{SPECIALIST_CLASS_NAME}},
```

- [ ] Entrada adicionada
- [ ] Salvei arquivo

### 3.3. Adicionar em author_prompts.py (se necessário)

```bash
# Editar: engine/prompts/author_prompts.py
```

- [ ] Se autor novo: Adicionei entrada completa
- [ ] Se autor existe: Confirmei que está ok
- [ ] Salvei arquivo

**Tempo estimado desta fase**: 5 minutos

---

## ✅ FASE 4: VALIDAÇÃO AUTOMÁTICA

### 4.1. Executar Script de Validação

```bash
cd specialist_factory
python3 validate_specialist.py {{SPECIALIST_NAME}}
```

- [ ] Script executado
- [ ] Resultado: **100% PASS** ✅

**Se FALHOU:**
- [ ] Li todos os erros listados
- [ ] Corrigi cada erro
- [ ] Re-executei validação
- [ ] Loop até 100% PASS

**Tempo estimado desta fase**: 5-10 minutos (se tudo ok)

---

## 🧪 FASE 5: TESTE REAL

### 5.1. Teste com Roteiro de Exemplo

```bash
cd /Users/clubproducoes/Digimundo/scripturemon
python3 analyze.py "inputs/examples/Te Encontro em Mim .pdf" \
    --specialist {{SPECIALIST_NAME}} --deep
```

- [ ] Comando executado
- [ ] Execução SEM ERROS
- [ ] Tempo de execução: `_______` minutos

### 5.2. Verificar Output

```bash
ls -lh workspace/outputs/formatted/ | tail -1
```

- [ ] Arquivo HTML gerado
- [ ] Tamanho > 15KB
- [ ] Nome: `ANALISE_{{SPECIALIST_NAME}}_*.html`

### 5.3. Validar Conteúdo

```bash
open workspace/outputs/formatted/ANALISE_{{SPECIALIST_NAME}}_*.html
```

- [ ] Abri arquivo HTML no navegador
- [ ] Li primeira análise completa
- [ ] Conteúdo faz sentido
- [ ] Teoria do autor foi aplicada
- [ ] Score obtido: `_______/10`

### 5.4. Critérios de Aceitação

- [ ] Score >= 7.0
- [ ] Pelo menos 3 cenas analisadas
- [ ] Pelo menos 3 quotes de diálogos
- [ ] Pelo menos 2 propostas de rewrite
- [ ] Citações de teoria do autor presentes

**Se teste FALHOU:**
- [ ] Li logs de erro completo
- [ ] Identifiquei problema (prompts? deep context? código?)
- [ ] Corrigi problema
- [ ] Re-testei

**Tempo estimado desta fase**: 10-15 minutos

---

## 📝 FASE 6: DOCUMENTAÇÃO

### 6.1. Atualizar MEMORIA_ESPECIALISTAS.md

```bash
# Editar: specialist_factory/MEMORIA_ESPECIALISTAS.md
```

**Adicionar entrada:**
```markdown
## Specialist N: {{SPECIALIST_NAME}}
- **Data**: {{DATE}}
- **Autor Base**: {{AUTHOR_NAME}}
- **Status**: ✅ Produção
- **Foco**: {{FOCUS_AREA}}
- **Deep Context**: theory/{{BOOK_NAME}}
- **Quirks**: [Documentar comportamentos peculiares]
- **Notas**: [Aprendizados durante criação]
- **Score Médio**: {{SCORE}}/10
- **Tempo Médio**: {{TIME}} minutos
```

- [ ] Entrada adicionada
- [ ] Salvei arquivo

### 6.2. Atualizar MAPEAMENTO_ARQUIVOS_SCRIPTUREMON.md

```bash
# Editar: MAPEAMENTO_ARQUIVOS_SCRIPTUREMON.md
```

- [ ] Adicionei referência ao novo especialista
- [ ] Salvei arquivo

### 6.3. Criar Entrada no Changelog (se existir)

- [ ] Documentei criação do especialista
- [ ] Listei features principais

**Tempo estimado desta fase**: 5 minutos

---

## 🎯 CHECKLIST FINAL DE CONCLUSÃO

### Arquivos Criados

- [ ] `engine/specialists/{{SPECIALIST_NAME}}/specialist.py`
- [ ] `engine/specialists/{{SPECIALIST_NAME}}/prompts.py`
- [ ] `engine/specialists/{{SPECIALIST_NAME}}/README.md`
- [ ] `tests/test_{{SPECIALIST_NAME}}.py`

### Arquivos Modificados

- [ ] `engine/specialists/__init__.py`
- [ ] `analyze.py`
- [ ] `engine/prompts/author_prompts.py` (se necessário)
- [ ] `specialist_factory/MEMORIA_ESPECIALISTAS.md`
- [ ] `MAPEAMENTO_ARQUIVOS_SCRIPTUREMON.md`

### Validações

- [ ] Nenhum placeholder `{{}}` restante (grep confirmou)
- [ ] Nenhum path absoluto hardcoded
- [ ] validate_specialist.py passou 100%
- [ ] Teste real executou sem erros
- [ ] Score >= 7.0 obtido
- [ ] Output HTML gerado e validado

### Documentação

- [ ] README do especialista completo
- [ ] MEMORIA_ESPECIALISTAS.md atualizado
- [ ] MAPEAMENTO atualizado

### Git (se usando)

- [ ] `git add` todos arquivos novos
- [ ] `git commit` com mensagem descritiva
- [ ] `git push` (se aplicável)

---

## 🎉 CONCLUSÃO

**Status**:
- [ ] ✅ COMPLETO - Especialista pronto para produção
- [ ] 🧪 EM TESTE - Funciona mas precisa ajustes
- [ ] ❌ FALHOU - Precisa revisão completa

**Score Final**: `_______/10`
**Tempo Total**: `_______` minutos

**Próximos Passos**:
- [ ] Testar com outros roteiros
- [ ] Ajustar prompts se necessário
- [ ] Coletar feedback de uso real
- [ ] Iterar e melhorar

---

**Data Conclusão**: `{{DATE_END}}`
**Criado por**: Claude + Digimundo

**DIGIMUNDO PRESENTE 🥷**
