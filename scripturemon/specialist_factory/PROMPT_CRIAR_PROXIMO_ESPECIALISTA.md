# 🏭 PROMPT: Criar Próximo Especialista

**Use este prompt em uma nova sessão Claude (sem contexto)**

---

## 📋 COPIE E COLE ESTE PROMPT:

```
Olá! Preciso criar o próximo especialista do sistema Scripturemon usando o specialist_factory.

## CONTEXTO DO SISTEMA

### Arquitetura: 24 Especialistas
- Sistema NÃO é "13 especialistas por autor"
- Sistema É "24 especialistas por ASPECTO"
- Cada especialista:
  - Foca em **1 ASPECTO** (dialogue, character, structure, pacing, etc.)
  - Consulta **TODOS os 13 livros** de teoria internamente
  - Usa **deep context queries** específicas para seu aspecto
  - Extrai conceitos relevantes de TODOS os autores

### Especialista de Referência
- **DrDialogue** ✅ já criado e funcionando
- Localização: `/Users/clubproducoes/Digimundo/scripturemon/engine/analyzers/dr_dialogue.py`
- Serve como MODELO EXATO para os 23 restantes

### Próximo a Criar
**DrCharacter** - Especialista em análise de personagens

## SISTEMA SPECIALIST_FACTORY

### Localização
`/Users/clubproducoes/Digimundo/scripturemon/specialist_factory/`

### Arquivos Importantes
1. **BLUEPRINT_SPECIALIST.md** - Guia completo passo-a-passo (440 linhas)
2. **CHECKLIST_CRIACAO.md** - Checklist interativo (280 linhas)
3. **MEMORIA_ESPECIALISTAS.md** - Lista dos 24 + histórico
4. **ARQUITETURA_SISTEMA.md** - Documentação da arquitetura
5. **LISTA_ESPECIALISTAS_ALVO.md** - Detalhes de cada especialista
6. **validate_specialist.py** - Validação automática
7. **templates/** - Templates prontos (3 arquivos)

## INSTRUÇÕES

### Passo 1: Leitura Obrigatória (10 min)
1. Leia `specialist_factory/BLUEPRINT_SPECIALIST.md` COMPLETO
2. Leia `specialist_factory/MEMORIA_ESPECIALISTAS.md`
3. Leia `specialist_factory/ARQUITETURA_SISTEMA.md`
4. Leia `specialist_factory/LISTA_ESPECIALISTAS_ALVO.md` (seção DrCharacter)

### Passo 2: Seguir Checklist (30-45 min)
1. Abra `specialist_factory/CHECKLIST_CRIACAO.md`
2. **SIGA RIGOROSAMENTE** cada fase
3. **NÃO pule validações**
4. **NÃO assuma** - sempre verifique com grep/read

### Passo 3: Criar DrCharacter
**Aspecto**: Character Analysis
**Base**: DrDialogue (clonar estrutura)
**Foco**: Análise de personagens usando sabedoria dos 13 autores

**Deep Context Queries** (exemplos):
- McKee/Story Ch.6 → "True Character", "Character Arc", "Dimension"
- Truby/Anatomy Ch.3 → "Weakness/Need", "Ghost", "Desire Line"
- Field/Screenplay Ch.4 → "Three Dimensions", "Character Biography"
- Snyder/Save the Cat → "Transformation Machine", "Save the Cat moment"
- Vogler/Writer's Journey → "Archetypes", "Hero pattern"
- Campbell/Hero 1000 → "Hero transformation", "Supernatural aid"
- Aristotle/Poetics Ch.13 → "Hamartia", "Tragic hero"
- (... + outros 6 autores)

### Passo 4: Validação
```bash
cd /Users/clubproducoes/Digimundo/scripturemon
python3 specialist_factory/validate_specialist.py character
```

### Passo 5: Teste Real
```bash
python3 analyze.py "inputs/examples/Te Encontro em Mim .pdf" --specialist character --deep
```

### Passo 6: Documentar
1. Atualizar `specialist_factory/MEMORIA_ESPECIALISTAS.md`
2. Adicionar entrada para DrCharacter
3. Documentar quirks descobertos
4. Registrar tempo de criação

### Passo 7: Commit Git
```bash
git add .
git commit -m "✨ Criar DrCharacter - Especialista #2/24

## Novo Especialista

**Nome**: DrCharacter
**Aspecto**: Character Analysis
**Status**: ✅ Criado e Validado

## Arquitetura
- Consulta os 13 livros com queries específicas de CHARACTER
- Deep context extraindo conceitos de todos os autores
- Baseado no modelo DrDialogue

## Validação
- ✅ validate_specialist.py passou
- ✅ Teste real executado
- ✅ Score: X.X/10

**Próximo**: DrStructure (#3/24)

🥷 DIGIMUNDO PRESENTE"
```

## PADRÕES IMPORTANTES

### ❌ NÃO FAÇA
- ❌ Deixar placeholders `{{}}` no código
- ❌ Usar paths absolutos (usar `Path(__file__)`)
- ❌ Copiar DrDialogue sem adaptar para CHARACTER
- ❌ Pular validação automática
- ❌ Esquecer de atualizar MEMORIA

### ✅ FAÇA
- ✅ Usar templates de `specialist_factory/templates/`
- ✅ Substituir TODOS os placeholders
- ✅ Queries específicas para CHARACTER (não dialogue!)
- ✅ Rodar validate_specialist.py
- ✅ Testar com roteiro real
- ✅ Documentar em MEMORIA_ESPECIALISTAS.md

## EXEMPLO: DrDialogue (Referência)

DrDialogue foca em DIALOGUE e consulta:
- McKee → "Subtext", "Dialogue as Action"
- Truby → "Moral Dialogue"
- Field → "Functional dialogue"
- Snyder → "Realistic dialogue"
- (... todos os 13 autores)

**DrCharacter deve fazer o MESMO, mas focado em CHARACTER.**

## TEMPO ESTIMADO
- Leitura: 10 min
- Criação: 20-30 min
- Validação: 5 min
- Teste: 10-15 min
- Documentação: 5 min
**Total**: 50-65 minutos

## RESULTADO ESPERADO

Ao final, você terá:
1. ✅ DrCharacter criado em `engine/analyzers/dr_character.py`
2. ✅ Prompts em `engine/analyzers/character/prompts.py`
3. ✅ README em `engine/analyzers/character/README.md`
4. ✅ Validação 100% passou
5. ✅ Teste real executado com sucesso
6. ✅ MEMORIA_ESPECIALISTAS.md atualizada
7. ✅ Commit no git

## COMEÇAR AGORA

**Primeira ação**:
```bash
cd /Users/clubproducoes/Digimundo/scripturemon
cat specialist_factory/BLUEPRINT_SPECIALIST.md
```

Leia o blueprint completo, depois siga o CHECKLIST_CRIACAO.md passo-a-passo.

**IMPORTANTE**: Não pule etapas. O sistema compensa limitações de IA forçando verificações. Confie no processo.

Boa sorte! 🥷
```

---

## 📝 Notas para Uso

1. **Copie TODO o conteúdo** entre as ``` acima
2. **Cole em nova sessão Claude** (sem contexto)
3. **Claude vai começar automaticamente** seguindo as instruções
4. **Tempo total**: ~1 hora para criar DrCharacter

---

**Criado**: 10 de Outubro 2025, 19:00
**Para**: Próxima sessão Claude criar DrCharacter
**Status**: ✅ Pronto para uso

**DIGIMUNDO PRESENTE 🥷**
