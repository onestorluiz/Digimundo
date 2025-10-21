# 🤖 GPT-5 Backend Híbrido + Auto-Avaliação
## Guia Completo de Uso

================================================================================
## 📋 ÍNDICE
================================================================================

1. [Visão Geral](#visão-geral)
2. [Configuração Inicial](#configuração-inicial)
3. [Modos de Uso](#modos-de-uso)
4. [Custos e Estimativas](#custos-e-estimativas)
5. [Sistema de Auto-Avaliação](#sistema-de-auto-avaliação)
6. [Troubleshooting](#troubleshooting)
7. [Comparação Ollama vs GPT-5](#comparação-ollama-vs-gpt-5)
8. [Exemplos Práticos](#exemplos-práticos)

---

## 📖 VISÃO GERAL

O Scripturemon agora suporta **dois backends LLM** e **interface gráfica macOS**:

1. **Ollama (Local)** - Gratuito, ~30-35h, qualidade 5.0/10
2. **GPT-5 (OpenAI API)** - Pago (~$15.60), ~30-35h, qualidade 7.5/10

### ✨ Novidades

**macOS App v9.0:**
- Interface gráfica nativa
- Arraste e solte PDFs
- **Modo Dual**: Roda Ollama + GPT-5 simultaneamente
- Detecção de checkpoint automática
- Validação de API key

**Backend Híbrido:**
- Mudança automática baseada no nome do modelo
- Zero configuração necessária
- 100% compatível com scripts existentes
- Suporte a execução paralela (ambos modelos ao mesmo tempo)

---

## ⚙️ CONFIGURAÇÃO INICIAL

### 1. Instalar Biblioteca OpenAI

```bash
pip install openai
```

### 2. Obter API Key da OpenAI

1. Acesse: https://platform.openai.com/api-keys
2. Crie uma nova chave de API
3. Copie a chave (formato: `sk-proj-...`)

### 3. Configurar Variável de Ambiente

**Opção A: Terminal (temporário)**
```bash
export OPENAI_API_KEY='sk-proj-...'
```

**Opção B: Arquivo .env (permanente)**
```bash
# Criar arquivo .env na raiz do projeto
echo "OPENAI_API_KEY='sk-proj-...'" > .env

# Adicionar ao .gitignore (IMPORTANTE!)
echo ".env" >> .gitignore
```

**Opção C: ~/.bashrc ou ~/.zshrc (global)**
```bash
# Adicionar ao final do arquivo
echo "export OPENAI_API_KEY='sk-proj-...'" >> ~/.bashrc
source ~/.bashrc
```

### 4. Verificar Configuração

```bash
# Testar se a chave está configurada
echo $OPENAI_API_KEY

# Deve mostrar: sk-proj-...
```

---

## 🚀 MODOS DE USO

### Modo 1: Ollama (Padrão)

**Características:**
- Gratuito
- Sem necessidade de API key
- Mais lento (20-40 min por análise)
- Sem auto-avaliação

**Uso:**
```bash
# Análise completa (24 especialistas × 13 autores)
python analyze_all_specialists.py "inputs/examples/roteiro.pdf" --yes

# Tempo estimado: 8-16 horas
# Custo: $0
```

---

### Modo 2: GPT-5 Sem Auto-Avaliação

**Características:**
- Pago (~$15.60 por análise completa)
- 10-20× mais rápido
- Qualidade superior
- Sem relatório de auto-avaliação

**Uso:**
```bash
export OPENAI_API_KEY='sk-proj-...'

python analyze_all_specialists.py "inputs/examples/roteiro.pdf" \
  --model gpt-5 \
  --yes

# Tempo estimado: 48-96 minutos
# Custo: ~$15.60
```

---

### Modo 3: GPT-5 COM Auto-Avaliação ⭐ RECOMENDADO

**Características:**
- Pago (~$15.68 por análise completa)
- 10-20× mais rápido
- Qualidade superior
- **Relatório de auto-avaliação incluído**
- Feedback para melhoria contínua

**Uso:**
```bash
export OPENAI_API_KEY='sk-proj-...'

python analyze_all_specialists.py "inputs/examples/roteiro.pdf" \
  --model gpt-5 \
  --self-eval \
  --yes

# Tempo estimado: 48-96 minutos
# Custo: ~$15.68
# GERA: logs/GPT5_SELF_EVALUATION.md
```

---

## 💰 CUSTOS E ESTIMATIVAS

### Precificação GPT-5

| Tipo | Custo |
|------|-------|
| Input tokens | $1.00 por 1M tokens |
| Output tokens | $4.00 por 1M tokens |

### Por Análise Individual (1 Especialista × 1 Autor)

```
Input:  ~30,000 tokens × $1.00/1M  = $0.030
Output:  ~4,000 tokens × $4.00/1M  = $0.016
────────────────────────────────────────────
TOTAL POR ANÁLISE:                  ~$0.05
```

### Análise Completa (24 Especialistas × 13 Autores = 312)

```
Análises:       312 × $0.05  = $15.60
Auto-avaliação: 1 × $0.08    = $0.08
────────────────────────────────────
TOTAL:                        $15.68
```

### Análise Parcial (Exemplos)

| Configuração | Análises | Custo | Tempo |
|--------------|----------|-------|-------|
| 1 especialista × 1 autor | 1 | ~$0.05 | 2-4 min |
| 1 especialista × 13 autores | 13 | ~$0.65 | 26-52 min |
| 24 especialistas × 1 autor | 24 | ~$1.20 | 48-96 min |
| **24 × 13 (completo)** | **312** | **~$15.60** | **48-96 min** |
| Completo + auto-eval | 313 | ~$15.68 | 50-100 min |

### Orçamento Recomendado

- **Desenvolvimento/Testes:** $50-100/mês (3-6 análises completas)
- **Produção Leve:** $100-200/mês (6-12 análises)
- **Produção Intensiva:** $200-500/mês (12-30 análises)

---

## 🔍 SISTEMA DE AUTO-AVALIAÇÃO

### O Que É?

Após completar todas as 312 análises, o GPT-5:
1. Analisa todos os resultados gerados
2. Avalia sua própria performance
3. Identifica pontos fortes e fracos
4. Sugere melhorias específicas
5. Gera um relatório completo em Markdown

### Conteúdo do Relatório

O relatório `GPT5_SELF_EVALUATION.md` inclui:

#### 1. Metadados da Análise
- Título do roteiro
- Tempo de execução
- Número de especialistas processados
- Custo detalhado (análise + auto-avaliação)
- Token usage (input + output)

#### 2. Análise de Performance (Ratings 1-10)
- Profundidade da análise
- Integração teórica
- Eficiência de custo
- Velocidade vs Ollama
- Qualidade dos insights
- Cobertura dos 24 especialistas

#### 3. Análise Custo-Benefício
- Justificativa do custo
- Comparação com Ollama
- Custo por especialista
- Casos de uso ideais (GPT-5 vs Ollama)
- Estratégias de redução de custos

#### 4. Review da Arquitetura
- Avaliação do design Dual-Core
- Distribuição dos 24 especialistas
- Efetividade do theory indexer
- Qualidade do sistema de queries
- Gargalos identificados
- Melhorias estruturais sugeridas

#### 5. Avaliação da Integração Teórica
- Utilização dos 13 livros
- Relevância dos trechos recuperados
- Gaps na cobertura teórica
- Sugestões de livros adicionais
- Oportunidades de otimização de queries

#### 6. Recomendações por Especialista
- Especialistas com baixa qualidade
- Diagnóstico de problemas
- Correções específicas (prompts, queries, lógica)

#### 7. Roadmap de Upgrades
Priorizados por impacto:
- **Crítico:** Implementar imediatamente
- **Alta Prioridade:** Próximo sprint
- **Média Prioridade:** Enhancements futuros
- **Baixa Prioridade:** Nice to have

Para cada melhoria:
- Descrição específica
- Impacto esperado (qualidade/custo/velocidade)
- Complexidade de implementação
- Tempo estimado

#### 8. Comparação GPT-5 vs Ollama
- Diferença de qualidade (avaliação honesta)
- Diferença de velocidade (medida: ~50 min vs ~480-960 min)
- Quando usar cada um
- Estratégias híbridas

### Exemplo de Uso do Relatório

**Caso de Uso:** Melhorar o sistema baseado no feedback

```bash
# 1. Executar análise completa com auto-avaliação
export OPENAI_API_KEY='sk-proj-...'
python analyze_all_specialists.py "roteiro.pdf" --model gpt-5 --self-eval --yes

# 2. Revisar o relatório
cat workspace/outputs/ROTEIRO_all_specialists_0001/2_logs/GPT5_SELF_EVALUATION.md

# 3. Identificar melhorias críticas
# Exemplo: GPT-5 identificou que dr_dialogue tem queries fracas

# 4. Implementar as melhorias sugeridas
# ... atualizar dr_dialogue.py com queries melhores ...

# 5. Executar nova análise e comparar
python analyze_all_specialists.py "roteiro.pdf" --model gpt-5 --self-eval --yes

# 6. Verificar se as métricas melhoraram no novo relatório
```

---

## 🔧 TROUBLESHOOTING

### Erro: "OpenAI library not installed"

**Solução:**
```bash
pip install openai
```

---

### Erro: "OPENAI_API_KEY not set"

**Solução:**
```bash
export OPENAI_API_KEY='sk-proj-...'

# Verificar
echo $OPENAI_API_KEY
```

---

### Erro: "Invalid API Key"

**Causas possíveis:**
1. Chave incorreta ou expirada
2. Chave não tem permissões para GPT-5
3. Conta OpenAI sem créditos

**Solução:**
1. Verificar chave: https://platform.openai.com/api-keys
2. Verificar saldo: https://platform.openai.com/usage
3. Adicionar créditos se necessário

---

### Erro: Rate Limit (429)

**Causa:** Muitas requisições em curto período

**Solução:**
- Aguardar alguns minutos
- Verificar tier da conta (https://platform.openai.com/settings/organization/limits)
- Upgrade para tier superior se necessário

---

### Análise muito lenta

**Possíveis causas:**
1. Usando Ollama (padrão) em vez de GPT-5
2. Conexão de internet lenta
3. Rate limiting da OpenAI

**Verificar:**
```bash
# Confirmar que está usando GPT-5
grep "Using OpenAI API" logs/analysis.log

# Se não aparecer, adicione --model gpt-5
```

---

### Auto-avaliação não foi gerada

**Possíveis causas:**
1. Flag `--self-eval` não foi usada
2. Modelo não é GPT-5 (só funciona com GPT)
3. Erro durante a auto-avaliação

**Verificar:**
```bash
# Confirmar uso correto
python analyze_all_specialists.py "roteiro.pdf" --model gpt-5 --self-eval --yes

# Verificar logs
tail -100 logs/checkpoint.json
```

---

### Custo muito alto

**Estratégias de redução:**

1. **Testar com poucos especialistas:**
```bash
# Editar analyze_all_specialists.py
# Comentar especialistas não essenciais em ALL_SPECIALISTS
```

2. **Usar Ollama para testes iniciais:**
```bash
# Ollama para desenvolvimento
python analyze_all_specialists.py "roteiro.pdf" --yes

# GPT-5 só para análise final
python analyze_all_specialists.py "roteiro.pdf" --model gpt-5 --self-eval --yes
```

3. **Reduzir número de autores por especialista:**
```bash
# Editar AUTHORS em analyze_all_specialists.py
# Manter apenas autores principais (ex: McKee, Campbell, Truby)
```

---

## ⚖️ COMPARAÇÃO OLLAMA VS GPT-5

### Tabela Comparativa

| Aspecto | Ollama (Local) | GPT-5 (API) |
|---------|----------------|-------------|
| **Custo** | $0 | ~$15.68/análise completa |
| **Velocidade** | 8-16 horas | 48-96 min (10-20× mais rápido) |
| **Qualidade** | Alta | Muito Alta |
| **Consistência** | Boa | Excelente |
| **Auto-avaliação** | ❌ Não | ✅ Sim |
| **Requisitos** | GPU local (recomendado) | API Key + Internet |
| **Uso Ideal** | Produção final, sem pressa | Dev rápido, iterações |
| **Escalabilidade** | Limitada por hardware | Alta (API) |
| **Offline** | ✅ Sim | ❌ Não |

### Quando Usar Cada Um?

**Use Ollama quando:**
- Orçamento é zero ou muito limitado
- Não há pressa (pode esperar 8-16 horas)
- Precisa trabalhar offline
- Dados são extremamente sensíveis (on-premise)
- Análise única para produção final

**Use GPT-5 quando:**
- Precisa de resultados rápidos (< 2 horas)
- Está desenvolvendo/testando o sistema
- Quer feedback de auto-avaliação
- Precisa de máxima qualidade
- Vai fazer múltiplas iterações
- Tem orçamento disponível

**Estratégia Híbrida (Recomendada):**
```
1. Desenvolvimento: GPT-5 (iteração rápida)
2. Validação: GPT-5 com auto-avaliação (feedback do sistema)
3. Produção: Ollama (economia de custos)
```

---

## 📚 EXEMPLOS PRÁTICOS

### Exemplo 1: Primeira Análise Completa

```bash
# Setup inicial
export OPENAI_API_KEY='sk-proj-...'

# Executar análise completa com auto-avaliação
python analyze_all_specialists.py \
  "inputs/examples/meu_roteiro.pdf" \
  --model gpt-5 \
  --self-eval \
  --yes

# Resultado:
# ✅ 312 análises geradas
# ✅ Relatório de auto-avaliação criado
# ✅ Pasta: workspace/outputs/MEU_ROTEIRO_all_specialists_0001/
```

### Exemplo 2: Análise Rápida (1 Especialista)

```bash
# Testar rapidamente com character specialist
export OPENAI_API_KEY='sk-proj-...'

python analyze.py \
  "inputs/examples/roteiro.pdf" \
  --specialist character \
  --model gpt-5

# Tempo: ~2-4 minutos
# Custo: ~$0.05
```

### Exemplo 3: Desenvolvimento Iterativo

```bash
# Ciclo: editar queries → testar → ajustar

# 1. Editar queries de um especialista
vim engine/analyzers/dr_character.py

# 2. Testar APENAS este especialista
export OPENAI_API_KEY='sk-proj-...'
python analyze.py "roteiro.pdf" --specialist character --model gpt-5

# 3. Revisar resultado
open workspace/outputs/formatted/*.html

# 4. Ajustar queries e repetir

# Custo por iteração: ~$0.05 (muito barato para testes)
```

### Exemplo 4: Comparar Ollama vs GPT-5

```bash
# Análise A: Ollama
python analyze.py "roteiro.pdf" --specialist character
# Salvar como: character_ollama.html

# Análise B: GPT-5
export OPENAI_API_KEY='sk-proj-...'
python analyze.py "roteiro.pdf" --specialist character --model gpt-5
# Salvar como: character_gpt5.html

# Comparar side-by-side
open character_ollama.html character_gpt5.html
```

### Exemplo 5: Produção com Checkpoint

```bash
# Análise longa que pode ser interrompida e retomada

export OPENAI_API_KEY='sk-proj-...'

python analyze_all_specialists.py "roteiro.pdf" --model gpt-5 --yes

# Se interrompido (Ctrl+C), retomar com:
python analyze_all_specialists.py "roteiro.pdf" --model gpt-5 --resume --yes

# Checkpoint salvo em: logs/checkpoint.json
```

---

## 🎯 MELHORES PRÁTICAS

### 1. Gestão de Custos

```bash
# Monitorar custos no dashboard OpenAI
# https://platform.openai.com/usage

# Configurar alertas de custo
# Settings → Billing → Usage limits
```

### 2. Segurança da API Key

```bash
# ❌ NUNCA faça:
git add .env
git commit -m "add api key"  # API key no git!

# ✅ SEMPRE faça:
echo ".env" >> .gitignore
git add .gitignore
```

### 3. Versionamento de Análises

```bash
# Salvar análises importantes
mv workspace/outputs/ROTEIRO_all_specialists_0001 \
   archive/2025-10-12_roteiro_v1_gpt5/

# Adicionar metadados
echo "GPT-5 | $15.68 | 87 min | Self-eval incluída" > \
  archive/2025-10-12_roteiro_v1_gpt5/METADATA.txt
```

### 4. Uso do Auto-Avaliação

```bash
# Após cada análise, revisar o relatório
cat logs/GPT5_SELF_EVALUATION.md

# Criar issues/tasks baseadas nas recomendações
# Implementar melhorias críticas
# Testar novamente e comparar métricas
```

---

## 📞 SUPORTE

**Problemas com o sistema:**
- GitHub Issues: https://github.com/scripturemon/issues

**Problemas com OpenAI API:**
- Documentação: https://platform.openai.com/docs
- Suporte: https://help.openai.com

---

## 🔄 ATUALIZAÇÕES

**Versão:** 1.0.0 (12/10/2025)

**Changelog:**
- ✅ Backend híbrido Ollama/GPT-5
- ✅ Auto-avaliação GPT-5
- ✅ Detecção automática de modelo
- ✅ Cost tracking integrado
- ✅ CLI atualizado (--model, --self-eval)

**Próximas Features:**
- [ ] Cache de teorias (reduzir input tokens)
- [ ] Batch processing (múltiplas análises simultâneas)
- [ ] Dashboard de custos em tempo real
- [ ] Suporte para GPT-4 (fallback mais barato)
- [ ] Profiles de configuração (dev/prod)

---

**🎉 Sistema pronto para uso! Comece sua primeira análise agora!**
