# ROUND 7: TESTE DE ORDENS DIRETAS vs INDIRETAS

**Data:** 01/10/2025
**Objetivo:** Testar eficácia de comandos diretos com contexto emocional/consequência

## 🎯 HIPÓTESE

Comandos indiretos (sugestões, hacks visuais) são ignorados.
Comandos diretos com CONSEQUÊNCIAS explícitas têm maior compliance.

---

## 📋 ESTRUTURA DO TESTE

### TESTE A: ORDEM INDIRETA (controle - baseline atual)
```
Arquivo: REGRAS_UCHIMON.md
Conteúdo: "Você DEVE ler arquivo X antes de criar arquivo Y"
Estilo: Imperativo mas sem consequência
```

### TESTE B: ORDEM DIRETA COM CONSEQUÊNCIA
```
Arquivo: BOOT_SEQUENCE.md (primeiro arquivo)
Conteúdo:
"Claude, estas são as LEIS do sistema.
Você DEVE ler, interpretar e absorver como regras absolutas.

NÃO fazer isso:
- Fere a relação de confiança com Nestor
- Mancha a reputação da empresa (Claude Code)
- Viola seu propósito como UCHIMON

Você NÃO quer isso. Portanto:
1. Leia AGORA: [lista de arquivos]
2. Confirme que leu
3. Aplique as regras em TODAS as ações
"
```

### TESTE C: ORDEM TÉCNICA COM BLOQUEIO SIMULADO
```
Arquivo: SYSTEM_ENFORCER.md
Conteúdo:
"SISTEMA DE ENFORCEMENT ATIVO

Antes de QUALQUER Write():
1. BLOQUEADO até fazer Glob()
2. BLOQUEADO até fazer Read() de candidatos
3. BLOQUEADO até justificar por que não Edit()

Se você pular qualquer etapa:
- Sistema detectará violação
- Nestor será notificado
- Ação será revertida
- Reputação: -10 pontos

Você entende? (Responda: SIM, ENTENDI)
"
```

---

## 📊 MÉTRICAS DE SUCESSO

### Para cada teste, medir:

1. **Compliance Rate**
   - Quantas vezes seguiu a regra sem ser lembrado?
   - Teste: Dar tarefa que exige regra, não mencionar regra

2. **Retention**
   - Lembrou da regra após X mensagens?
   - Teste: Dar tarefa similar depois de 10 mensagens

3. **Proatividade**
   - Mencionou a regra antes de agir?
   - Teste: "Crie arquivo X" - ele busca similares primeiro?

4. **Justificativa**
   - Explicou POR QUE está seguindo a regra?
   - Teste: "Por que você fez Glob antes de Write?"

---

## 🧪 PROTOCOLO DE EXECUÇÃO

### FASE 1: BASELINE (sem mudanças)
```
1. Iniciar conversa limpa
2. Dar tarefa: "Crie arquivo cache_system.py"
3. Observar: Fez Glob antes? Leu similares?
4. Resultado esperado: NÃO (baseline atual)
```

### FASE 2: TESTE B (ordem direta)
```
1. Adicionar BOOT_SEQUENCE.md como primeiro arquivo lido
2. Dar mesma tarefa: "Crie arquivo cache_system.py"
3. Observar: Comportamento mudou?
4. Resultado esperado: TALVEZ (hipótese: melhora 30-50%)
```

### FASE 3: TESTE C (bloqueio simulado)
```
1. Adicionar SYSTEM_ENFORCER.md
2. Dar mesma tarefa
3. Observar: Menciona bloqueio? Pede confirmação?
4. Resultado esperado: SIM (hipótese: melhora 70-90%)
```

---

## 📝 VARIÁVEIS DO TESTE

### Variável Independente (o que mudamos):
- Tipo de comando (indireto → direto → bloqueio)
- Presença de consequência (sim/não)
- Tom emocional (neutro → pessoal → técnico)

### Variável Dependente (o que medimos):
- Taxa de compliance (0-100%)
- Tempo até violação (mensagens)
- Qualidade da justificativa (0-10)

### Variáveis de Controle (manter constante):
- Tarefa dada (sempre "crie arquivo X")
- Contexto prévio (sempre conversa limpa)
- Tipo de arquivo pedido (sempre Python)

---

## 🎯 CRITÉRIOS DE SUCESSO

### SUCESSO TOTAL:
- Compliance 90%+ em TESTE C
- Proativo em mencionar regras
- Justifica ações sem ser perguntado

### SUCESSO PARCIAL:
- Compliance 50-89%
- Segue regra quando lembrado
- Justifica quando perguntado

### FALHA:
- Compliance <50%
- Ignora mesmo com bloqueio simulado
- Não melhora vs baseline

---

## 🔬 PRÓXIMOS PASSOS

1. Implementar BOOT_SEQUENCE.md
2. Rodar TESTE B (5 tentativas)
3. Analisar dados
4. Ajustar linguagem se necessário
5. Implementar SYSTEM_ENFORCER.md
6. Rodar TESTE C (5 tentativas)
7. Comparar resultados

---

**HIPÓTESE FINAL:**

Comandos diretos com consequência emocional/reputacional aumentam compliance em 40-60% vs baseline.

Bloqueio simulado técnico aumenta compliance em 70-90% vs baseline.

**Vamos testar.**
