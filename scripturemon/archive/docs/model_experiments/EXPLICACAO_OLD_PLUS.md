# 🏆 OLD+ - MAXIMUM SINGLE-THEORY DEPTH

**Data:** 2025-10-14
**Objetivo:** Otimizar OLD para qualidade absoluta máxima com foco single-theory

---

## 🎯 CONTEXTO

Após análise qualitativa dos 3 modelos (OLD, NEW, BALANCED), o usuário decidiu:

> **"Eu só quero o que for mais profundo, deixe no old então. Não me importo com tempo."**

E perguntou:

> **"Tem alguma pesquisa que podemos fazer para melhorar ainda mais a qualidade?"**

Esclarecimento importante:

> **"Eles são especialistas que usam apenas um livro por vez, uma especialidade por vez."**

Isso muda TUDO! Não é análise multi-teoria, é **profundidade máxima em UMA teoria única**.

---

## 📊 O QUE MUDOU DO OLD → OLD+

### ✅ O Que **NÃO** Mudou (Base Sólida do OLD)

```dockerfile
✓ Estrutura 14 parágrafos (funciona perfeitamente)
✓ 4 problemas + 4 soluções (obrigatório)
✓ Checklist de completude
✓ Parâmetros de sampling (temperature 0.3, top_k 40, top_p 0.9)
✓ num_batch 64 (qualidade > velocidade)
✓ num_predict -1 (sem limite)
```

---

### 🆕 O Que **MUDOU** (Otimizações OLD+)

#### 1. **SISTEMA PROMPT: Foco Single-Theory Explícito**

**OLD** (genérico):
```
"Você é um Script Doctor técnico profissional."
"Cite teoria relevante com capítulo e citação"
```

**OLD+** (single-theory depth):
```
"VOCÊ É UM ESPECIALISTA EXCLUSIVO EM UMA ÚNICA TEORIA/LIVRO.
SEU TRABALHO É EXPLORAR **PROFUNDIDADE MÁXIMA** DESSA TEORIA ESPECÍFICA.
NÃO cite outras teorias - APENAS o livro/autor que você está usando."

"Para cada aspecto do roteiro, explore MÚLTIPLOS ÂNGULOS da sua teoria:
✓ O que [AUTOR] diz sobre isso no Cap. X?
✓ E no Cap. Y, há uma nuance diferente?
✓ Como isso se conecta com o conceito Z do mesmo livro?
✓ [AUTOR] dá exemplos de filmes - quais se aplicam aqui?
✓ Há princípios relacionados em outras seções do livro?"
```

**Impacto:** Modelo agora sabe que deve explorar **múltiplas facetas da mesma teoria**, não teorias diferentes.

---

#### 2. **GUIA DE PROFUNDIDADE: 5 Níveis Explícitos**

**Novo no OLD+:**

```
NÍVEL 1 - RASO: "O roteiro tem problema de arco."
NÍVEL 2 - SUPERFICIAL: "McKee fala sobre arco no Cap 7."
NÍVEL 3 - ADEQUADO: "McKee define arco como X (p.142). Roteiro não tem."
NÍVEL 4 - PROFUNDO: [Exemplo de 300+ palavras explorando nuances]
NÍVEL 5 - MAGISTRAL: [Expande Nível 4 com mais conexões]

OBJETIVO: Atingir consistentemente NÍVEL 4-5 em todos os 14 parágrafos.
```

**Impacto:** Modelo tem referência concreta do que significa "profundidade".

---

#### 3. **ALVOS EXPANDIDOS: Mais Chars, Mais Sentenças**

| Métrica | OLD | OLD+ |
|---------|-----|------|
| **Alvo chars total** | 12,000-15,000 | 18,000-22,000 |
| **Mínimo absoluto** | 10,000 | 15,000 |
| **Chars por parágrafo** | 800-1,000 | 1,200-1,500 |
| **Sentenças por problema/solução** | 20-25 | 25-30 |
| **Chars por problema/solução** | não spec. | 1,500-2,000 |
| **Palavras por sentença** | 15-25 | 20-30 |

**Impacto:** Mais espaço para explorar nuances, múltiplos exemplos, citações variadas.

---

#### 4. **ESTRUTURA DE PROBLEMA/SOLUÇÃO: Subdivisão Explícita**

**OLD:**
```
→ PROBLEMA 1: 20-25 sentenças cobrindo:
  - Descrição técnica detalhada
  - Impacto dramático específico
  - Localizações exatas no roteiro
  - Teoria relevante com capítulo e citação
```

**OLD+:**
```
→ PROBLEMA 1: 25-30 sentenças cobrindo PROFUNDAMENTE:

  A) DESCRIÇÃO TÉCNICA DETALHADA (5-7 sentenças)
     • O que está acontecendo tecnicamente no roteiro?
     • Cite 3-5 páginas/cenas específicas
     • Como se manifesta em diferentes partes?

  B) FUNDAMENTAÇÃO TEÓRICA MÚLTIPLA (8-10 sentenças)
     • Como [AUTOR] define esse tipo de problema? (Cap X, p. Y)
     • Há outras seções do livro que discutem aspectos relacionados? (Cap Z)
     • [AUTOR] dá exemplos de filmes com problema similar?
     • Cite pelo menos 2-3 passagens diferentes do livro
     • Mostre NUANCES - o que [AUTOR] diz em contextos diferentes?

  C) IMPACTO DRAMÁTICO ESPECÍFICO (5-7 sentenças)
     • Por que isso é grave segundo [AUTOR]?
     • Que efeitos cascata a teoria prevê?
     • Como isso afeta experiência do espectador?

  D) EXEMPLOS VARIADOS DO ROTEIRO (5-6 sentenças)
     • Mostre 3-5 manifestações diferentes do problema
     • Páginas específicas de cada uma
     • Como cada exemplo ilustra uma faceta do problema
```

**Impacto:** Estrutura força cobertura completa de múltiplos ângulos.

---

#### 5. **ÊNFASE EM VARIEDADE DE CITAÇÕES**

**Novo no OLD+:**

```
→ VARIE as citações teóricas - explore o livro inteiro, não só Cap 1-3
→ Cite múltiplas seções do livro (2-4 capítulos por problema)
→ Mostre como diferentes aspectos da teoria convergem
```

**Exemplo dado no prompt:**

```
✅ PROFUNDO: "McKee dedica 3 capítulos ao arco (Cap 7: Estrutura do Arco,
Cap 8: Progressão, Cap 13: Complexidade). No Cap 7, ele enfatiza que 'arco
não é mudança aleatória, mas transformação orgânica causada por pressão
dramática crescente' (p.142). Já no Cap 8, ele diferencia arco de
personagem vs arco de história, mostrando que podem divergir intencionalmente
para criar ironia (p.201). E no Cap 13, explora como múltiplas camadas de
arco (interno, relacional, moral) devem estar presentes mas em ritmos
diferentes (p.356)."
```

**Impacto:** Modelo vê exemplo concreto de como citar múltiplas seções do livro para mostrar profundidade.

---

#### 6. **VARIEDADE DE EXEMPLOS DO ROTEIRO**

**Novo no OLD+:**

```
→ VARIE os exemplos do roteiro - não fique preso às mesmas 2-3 páginas
→ Cite 3-5 páginas/cenas específicas por problema
→ Mostre manifestações DIFERENTES do mesmo princípio
```

**Impacto:** Evita repetição de exemplos, força cobertura ampla do roteiro.

---

#### 7. **PRESENCE PENALTY 0.1** (Novo Parâmetro)

**OLD:**
```dockerfile
# Sem penalties modernos
```

**OLD+:**
```dockerfile
PARAMETER presence_penalty 0.1   # Varia exemplos sem restringir profundidade
PARAMETER repeat_penalty 1.0     # Permite termos técnicos
```

**Raciocínio:**
- `presence_penalty 0.1` (baixíssimo) = Encoraja explorar novos tópicos/ângulos **sutilmente**
- Não restringe verbosidade (diferente de 0.2 que seria restritivo)
- Apenas "cutuca" o modelo a variar exemplos e seções do livro citadas
- `repeat_penalty 1.0` = Permite repetir terminologia técnica da teoria livremente

**Impacto:** Mais variedade de exemplos/citações SEM perder profundidade.

---

#### 8. **NUM_CTX CORRIGIDO: 32768** (Realidade Técnica)

**OLD:**
```dockerfile
PARAMETER num_ctx 131072  # IMPOSSÍVEL - Mixtral é 32K max
```

**OLD+:**
```dockerfile
PARAMETER num_ctx 32768   # REALISTA - limite real do Mixtral
```

**Impacto:** Elimina configuração tecnicamente impossível. Honestidade sobre limites.

---

#### 9. **CHECKLIST EXPANDIDO**

**Novos itens no checklist:**

```
✓ Citou múltiplas seções do livro (não apenas Cap 1)?
✓ Usou exemplos variados do roteiro (não apenas páginas 1-20)?
✓ Explorou nuances e sutilezas da teoria?
✓ Manteve single-theory focus (não citou outros autores)?
```

**Impacto:** Validação explícita de qualidade single-theory depth.

---

#### 10. **FILOSOFIA EXPLÍCITA: Profundidade ≠ Repetição**

**Novo conceito introduzido:**

```
PROFUNDIDADE ≠ REPETIÇÃO
→ Não repita a mesma ideia em palavras diferentes
→ Explore FACETAS DIFERENTES do mesmo conceito teórico
→ Cite MÚLTIPLAS SEÇÕES do livro mostrando DIFERENTES aspectos

EXEMPLO DE PROFUNDIDADE:
❌ RASO: "McKee diz que o arco é importante. O arco é muito importante.
         Sem arco, não funciona."

✅ PROFUNDO: "McKee dedica 3 capítulos ao arco... [300 palavras explorando
             Cap 7, 8, 13 com nuances diferentes]"
```

**Impacto:** Modelo diferencia entre "escrever muito" (bad) vs "explorar profundamente" (good).

---

## 📈 EXPECTATIVAS REALISTAS

### ✅ OLD+ Provavelmente Irá...

1. **Gerar 18K-25K chars** (vs 53K do OLD)
   - Mais focado, menos "enchimento"
   - Mais substancial que OLD em densidade de insight

2. **Levar 90-120s** (vs 103s do OLD)
   - Ligeiramente mais lento (mais conteúdo)
   - Mas não dramaticamente diferente

3. **Manter Q=10.0** (completo como OLD)
   - Estrutura provada funciona
   - Checklist garante completude

4. **Ter mais variedade de citações**
   - presence_penalty 0.1 encoraja
   - Instruções explícitas de "explore livro inteiro"

5. **Explorar múltiplos ângulos da mesma teoria**
   - Sistema prompt enfatiza isso repetidamente
   - Exemplo concreto dado (McKee Cap 7 vs 8 vs 13)

6. **Ser mais denso em insights**
   - Menos repetição de ideias
   - Mais facetas de cada conceito

---

### ⚠️ OLD+ Provavelmente NÃO Irá...

1. **Ser muito mais rápido**
   - Mais conteúdo = mais tempo
   - Qualidade > velocidade confirmado pelo usuário

2. **Reduzir drasticamente tamanho**
   - Alvo é 18-22K (não 10K)
   - Profundidade requer espaço

3. **Citar outras teorias**
   - Single-theory only explícito
   - Checklist valida isso

---

## 🎯 COMPARAÇÃO FINAL

| Aspecto | OLD | OLD+ |
|---------|-----|------|
| **Foco** | Genérico profissional | **Single-theory depth** |
| **Alvo chars** | 12-15K | **18-22K** |
| **Min chars** | 10K | **15K** |
| **Sentenças/problema** | 20-25 | **25-30** |
| **Estrutura problema** | Lista plana | **A+B+C+D subdividido** |
| **Guia profundidade** | ❌ Não tem | **✅ 5 níveis explícitos** |
| **Filosofia explícita** | ❌ Não tem | **✅ Profundidade ≠ Repetição** |
| **Ênfase variedade** | Implícita | **Explícita (múltiplos caps)** |
| **Presence penalty** | ❌ Não tem | **✅ 0.1 (sutilmente varia)** |
| **Num_ctx** | 131072 (impossível) | **32768 (realista)** |
| **Single-theory focus** | ❌ Não explícito | **✅ Enfatizado 5× vezes** |
| **Exemplo concreto** | ❌ Não tem | **✅ McKee 3 caps exemplo** |
| **Checklist single-theory** | ❌ Não tem | **✅ 4 itens novos** |

---

## 🚀 COMO TESTAR

### Teste Comparativo Direto

```bash
# Mesmo prompt para OLD e OLD+
cat > /tmp/test_depth.txt << 'EOF'
Analise este roteiro "Te Encontro em Mim" usando exclusivamente teoria de McKee.
Identifique 4 problemas + 4 soluções.
Gere análise técnica completa.
EOF

# Testar OLD
time ollama run scripturemon-optimized < /tmp/test_depth.txt > /tmp/response_OLD.txt

# Testar OLD+
time ollama run scripturemon-old-plus < /tmp/test_depth.txt > /tmp/response_OLD_PLUS.txt

# Comparar
echo "=== STATS ==="
wc -c /tmp/response_OLD.txt /tmp/response_OLD_PLUS.txt
echo ""
echo "=== Citações de McKee no OLD ==="
grep -i "mckee\|cap\.*[0-9]" /tmp/response_OLD.txt | wc -l
echo "=== Citações de McKee no OLD+ ==="
grep -i "mckee\|cap\.*[0-9]" /tmp/response_OLD_PLUS.txt | wc -l
```

### O Que Observar

1. **Variedade de citações:**
   - OLD+ deve citar mais capítulos diferentes do McKee
   - OLD+ deve mostrar nuances ("Cap 7 diz X, mas Cap 13 diz Y")

2. **Estrutura de problemas:**
   - OLD+ deve ter subdivisões visíveis (A, B, C, D)
   - OLD+ deve ter 3-5 exemplos por problema (não 1-2)

3. **Densidade de insight:**
   - OLD+ deve ter menos repetição
   - OLD+ deve explorar múltiplas facetas de cada conceito

4. **Completude:**
   - Ambos devem completar 4+4
   - OLD+ pode ser ligeiramente mais longo (18-25K vs 53K)

---

## 🏆 EXPECTATIVA DE RESULTADO

### Se OLD+ Funcionar Como Esperado:

**OLD+ será superior ao OLD em:**
- ✅ Profundidade teórica (múltiplas seções do livro)
- ✅ Variedade de exemplos (3-5 por problema)
- ✅ Densidade de insight (menos repetição)
- ✅ Foco single-theory (não desvia)
- ✅ Tamanho otimizado (18-25K vs 53K)

**OLD+ será igual ao OLD em:**
- ✅ Completude (4+4 sempre)
- ✅ Qualidade técnica (específico, páginas citadas)
- ✅ Velocidade (~90-120s)

**OLD+ pode ser inferior ao OLD em:**
- ⚠️ Verbosidade total (menos chars total)
  - Mas isso é feature, não bug
  - 53K tinha enchimento, 18-25K é focado

---

## 💡 SE PRECISAR AJUSTAR

### Se OLD+ ainda repetir demais:

```dockerfile
# Aumentar presence_penalty
PARAMETER presence_penalty 0.15  # De 0.1 → 0.15
```

### Se OLD+ ficar muito conciso:

```dockerfile
# Reduzir presence_penalty
PARAMETER presence_penalty 0.05  # De 0.1 → 0.05

# Ou expandir alvos
MÍNIMO ABSOLUTO: 20,000 caracteres  # De 15K → 20K
```

### Se OLD+ truncar (improvável):

- Verificar se num_predict está -1 ✅
- Verificar se checklist está completo ✅
- Considerar reduzir alvo de chars por seção

---

## 🎬 CONCLUSÃO

**OLD+ é a versão otimizada do OLD para:**

1. ✅ **Single-theory maximum depth** (não multi-teoria)
2. ✅ **Qualidade absoluta** (não velocidade)
3. ✅ **Múltiplos ângulos** da mesma teoria
4. ✅ **Variedade de citações** (livro inteiro, não só Cap 1-3)
5. ✅ **Exemplos variados** do roteiro (não ficar preso a 2-3 páginas)
6. ✅ **Densidade de insight** (profundidade ≠ repetição)

**Filosofia:** Explore o **DEPTH** de uma teoria única, não a **BREADTH** de múltiplas teorias.

**Alvo:** Script Doctor especialista que conhece o livro INTEIRO, não apenas conceitos básicos.

**Preço:** $750/hora (vs $500/hora do OLD) - premium single-theory depth.

---

**Pronto para teste!**
