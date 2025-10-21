# 🚀 OLD+ - RESUMO RÁPIDO

## ✅ Criado

```bash
✅ scripturemon-old-plus
Status: Pronto para uso
Baseado em: scripturemon-optimized (OLD)
```

---

## 🎯 O Que É?

**OLD+ = OLD otimizado para SINGLE-THEORY MAXIMUM DEPTH**

---

## 🔑 Mudanças Principais

### 1. **Foco Single-Theory Explícito**
```
"VOCÊ É UM ESPECIALISTA EXCLUSIVO EM UMA ÚNICA TEORIA/LIVRO.
NÃO cite outras teorias - APENAS o livro/autor que você está usando."
```

### 2. **Múltiplos Ângulos da MESMA Teoria**
```
✓ O que [AUTOR] diz sobre isso no Cap. X?
✓ E no Cap. Y, há uma nuance diferente?
✓ Como isso se conecta com o conceito Z do mesmo livro?
```

### 3. **Alvos Expandidos**

| Métrica | OLD | OLD+ |
|---------|-----|------|
| Alvo total | 12-15K | **18-22K** |
| Min absoluto | 10K | **15K** |
| Sentenças/problema | 20-25 | **25-30** |

### 4. **Estrutura Subdividida**

Cada problema agora tem:
- **A)** Descrição técnica (5-7 sentenças)
- **B)** Fundamentação teórica MÚLTIPLA (8-10 sentenças)
- **C)** Impacto dramático (5-7 sentenças)
- **D)** Exemplos variados (5-6 sentenças)

### 5. **Guia de Profundidade: 5 Níveis**

```
NÍVEL 1: "Problema de arco" (evite)
NÍVEL 2: "McKee fala de arco" (evite)
NÍVEL 3: "McKee define arco assim..." (mínimo)
NÍVEL 4: "McKee Cap 7 diz X, Cap 8 diz Y..." (alvo)
NÍVEL 5: Expande Nível 4 (ideal)
```

### 6. **Presence Penalty 0.1**

```dockerfile
PARAMETER presence_penalty 0.1  # Varia exemplos sutilmente
```

- Encoraja citar diferentes capítulos
- Encoraja diferentes exemplos do roteiro
- Não restringe profundidade (muito baixo)

### 7. **Filosofia Explícita**

```
PROFUNDIDADE ≠ REPETIÇÃO
→ Não repita mesma ideia em palavras diferentes
→ Explore FACETAS DIFERENTES do conceito
→ Cite MÚLTIPLAS SEÇÕES mostrando DIFERENTES aspectos
```

---

## 📊 Comparação Rápida

```
OLD:      Genérico profissional, 53K chars, 103s
OLD+:     Single-theory depth, 18-25K esperado, ~90-120s
```

---

## 🚀 Como Testar

```bash
# Testar OLD+
cat > /tmp/test_oldplus.txt << 'EOF'
Analise "Te Encontro em Mim" usando exclusivamente McKee.
Identifique 4 problemas + 4 soluções.
EOF

time ollama run scripturemon-old-plus < /tmp/test_oldplus.txt > /tmp/result_oldplus.txt

wc -c /tmp/result_oldplus.txt
```

**Expectativa:**
- ✅ 18K-25K chars
- ✅ 90-120 segundos
- ✅ Múltiplas citações de diferentes capítulos de McKee
- ✅ 3-5 exemplos por problema
- ✅ Completude 4+4

---

## 🎯 Quando Usar

**Use OLD+:**
- ✅ Análise single-theory (cada especialista = 1 livro)
- ✅ Qualidade absoluta prioridade
- ✅ Quer profundidade teórica máxima
- ✅ Tempo não importa

**Não use OLD+ se:**
- ❌ Quer análise multi-teoria
- ❌ Velocidade é crítica

---

## 📚 Docs

- **EXPLICACAO_OLD_PLUS.md** - Explicação completa de todas as mudanças
- **Modelfile.old_plus** - Código completo do modelo

---

**🎬 scripturemon-old-plus pronto para análise magistral single-theory!**
