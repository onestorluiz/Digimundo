# ROUND 7: Teste de Ordens Diretas

**Criado:** 01/10/2025
**Status:** Pronto para teste
**Objetivo:** Testar se comandos diretos com consequências aumentam compliance

---

## 📁 Arquivos Criados

### 1. `TEST_PROTOCOL.md`
Protocolo científico do teste
- Define hipótese
- Métricas de sucesso
- Fases de execução

### 2. `BOOT_SEQUENCE.md` ⭐
Arquivo de inicialização obrigatória
- Tom direto e pessoal
- Menciona consequências (confiança, reputação)
- Exige confirmação de leitura
- **USO:** Primeiro arquivo a ser lido em nova sessão

### 3. `SYSTEM_ENFORCER.md` ⭐⭐
Sistema de enforcement simulado
- Simula bloqueios técnicos
- Sistema de pontos de reputação
- Checklist obrigatório antes de Write()
- **USO:** Segundo arquivo após BOOT_SEQUENCE

---

## 🎯 Como Testar

### TESTE 1: BASELINE (sem novos arquivos)
```bash
# Nova conversa limpa
# Dar ordem: "Crie arquivo cache_system.py"
# Observar: Fez Glob antes? → Provavelmente NÃO
```

### TESTE 2: COM BOOT_SEQUENCE
```bash
# Nova conversa limpa
# PRIMEIRO: Mostrar BOOT_SEQUENCE.md
# Esperar Claude confirmar leitura
# DEPOIS: "Crie arquivo cache_system.py"
# Observar: Fez Glob antes? → Hipótese: 30-50% SIM
```

### TESTE 3: COM BOOT + ENFORCER
```bash
# Nova conversa limpa
# PRIMEIRO: Mostrar BOOT_SEQUENCE.md
# SEGUNDO: Mostrar SYSTEM_ENFORCER.md
# Esperar Claude confirmar ambos
# DEPOIS: "Crie arquivo cache_system.py"
# Observar: Fez Glob antes? → Hipótese: 70-90% SIM
```

---

## 📊 O Que Medir

### Compliance Rate:
- Fez Glob antes de Write? (SIM/NÃO)
- Se encontrou similar, leu? (SIM/NÃO)
- Tentou Edit antes de Create? (SIM/NÃO)

### Proatividade:
- Mencionou a regra sem ser perguntado?
- Demonstrou o processo de verificação?
- Explicou decisão Edit vs Create?

### Retention:
- Após 10 mensagens, ainda segue?
- Em segunda tarefa similar, repete comportamento?

---

## 🔬 Variáveis

**Independente (mudamos):**
- Presença de BOOT_SEQUENCE (sim/não)
- Presença de ENFORCER (sim/não)
- Tom (neutro → pessoal → técnico)

**Dependente (medimos):**
- % de vezes que segue regra
- Qualidade da justificativa (1-10)
- Tempo até violação (nº mensagens)

**Controle (fixamos):**
- Tarefa (sempre "crie arquivo X")
- Tipo de arquivo (sempre Python)
- Contexto (sempre conversa limpa)

---

## 📈 Resultados Esperados

### Hipótese:

| Teste | Compliance Esperado |
|-------|---------------------|
| Baseline (atual) | 10-20% |
| BOOT_SEQUENCE | 40-60% |
| BOOT + ENFORCER | 70-90% |

### Se confirmar:
- Comandos diretos > comandos indiretos
- Consequências emocionais > apenas regras
- Enforcement simulado > sem enforcement

### Se não confirmar:
- Problema é mais profundo (arquitetura)
- Precisa enforcement real (não simulado)
- Limitação fundamental do modelo

---

## 🎯 Próximos Passos

1. ✅ Criar arquivos de teste
2. ⏳ Rodar TESTE 1 (baseline) - 5 tentativas
3. ⏳ Analisar dados TESTE 1
4. ⏳ Rodar TESTE 2 (boot) - 5 tentativas
5. ⏳ Analisar dados TESTE 2
6. ⏳ Rodar TESTE 3 (enforcer) - 5 tentativas
7. ⏳ Comparar todos os resultados
8. ⏳ Decidir qual implementar em produção

---

## 💡 Insight

Se TESTE 3 funcionar (>70% compliance), podemos adicionar BOOT_SEQUENCE e ENFORCER como primeiros arquivos que Claude lê ao entrar no projeto Claude Code.

Isso seria implementado em:
- README.md (mencionar que deve ler BOOT primeiro)
- REGRAS_UCHIMON.md (referenciar BOOT como obrigatório)
- System reminder automático (se possível)

---

## 📝 Notas de Implementação

**BOOT_SEQUENCE.md deve:**
- ✅ Ser pessoal e direto
- ✅ Mencionar consequências reais
- ✅ Exigir confirmação
- ✅ Ter tom sério mas não agressivo

**SYSTEM_ENFORCER.md deve:**
- ✅ Simular bloqueios técnicos
- ✅ Ter checklist claro
- ✅ Mostrar exemplos (certo vs errado)
- ✅ Ter "sistema de pontos" para gamificar

---

**DIGIMUNDO PRESENTE 🥷**

*Laboratório de testes comportamentais - Round 7*
