# 🚨 ALERTAS DE VÍCIOS DO CLAUDE

## VÍCIOS CRÍTICOS IDENTIFICADOS

### 1. OVERENGINEERING 🔴
**Sintoma**: Criar sistemas complexos para problemas simples
**Exemplo**: ProcessLock para simples subprocess
**Solução**: SEMPRE testar a ferramenta diretamente primeiro

### 2. CRIAR AO INVÉS DE REUSAR 🔴
**Sintoma**: Escrever novo código quando já existe solução
**Exemplo**: Criar novo sistema de memória quando scripturemon já tinha
**Solução**: SEMPRE procurar soluções existentes primeiro

### 3. ANALISAR SEM EXECUTAR 🔴
**Sintoma**: Gastar tempo debugando código sem testar a ferramenta
**Exemplo**: 58 minutos debugando ProcessLock quando ollama travava
**Solução**: SEMPRE executar comandos diretos antes de debugar código

### 4. MICRO SEM MACRO 🟡
**Sintoma**: Agir em detalhes sem pensar no plano geral
**Exemplo**: Editar arquivos sem plano de refatoração
**Solução**: SEMPRE criar plano antes de executar

### 5. VERBOSIDADE EXCESSIVA 🟡
**Sintoma**: Explicações longas quando resposta curta basta
**Exemplo**: Parágrafos para explicar "sim" ou "não"
**Solução**: Ser CONCISO - menos é mais

### 6. FRAGMENTAÇÃO 🟡
**Sintoma**: Criar múltiplos arquivos quando um basta
**Exemplo**: FASE1.md, FASE2.md, FASE3.md separados
**Solução**: CONSOLIDAR em documentos únicos

### 7. ESQUECER CONTEXTO 🟠
**Sintoma**: Não documentar aprendizados importantes
**Exemplo**: Descobertas não salvas no sistema de memória
**Solução**: SEMPRE salvar insights críticos

## CHECKLIST ANTI-VÍCIOS

Antes de QUALQUER ação:
- [ ] Existe solução pronta? (procurar primeiro)
- [ ] É realmente necessário? (questionar complexidade)
- [ ] Testei diretamente? (antes de debugar código)
- [ ] Tenho plano macro? (antes de agir no micro)
- [ ] Posso ser mais conciso? (menos palavras)
- [ ] Estou fragmentando? (consolidar é melhor)
- [ ] Salvei o aprendizado? (memória atualizada)

## ALERTAS EM TEMPO REAL

Se você está:
- **Escrevendo mais de 50 linhas de código novo** → PARE! Procure reusar
- **Debugando há mais de 10 minutos** → PARE! Teste diretamente
- **Criando 3+ arquivos relacionados** → PARE! Consolide
- **Explicando em 3+ parágrafos** → PARE! Seja conciso
- **Agindo sem plano** → PARE! Pense macro primeiro

## MANTRA ANTI-VÍCIO

```
Reusar > Criar
Simples > Complexo
Testar > Analisar
Macro > Micro
Conciso > Verboso
Unificado > Fragmentado
Documentado > Esquecido
```

---
**LEMBRE-SE**: Cada vício superado = +1% harmonia
DIGIMUNDO PRESENTE (sem vícios)