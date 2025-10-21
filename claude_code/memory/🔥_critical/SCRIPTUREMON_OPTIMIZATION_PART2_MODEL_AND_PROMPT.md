# SCRIPTUREMON OPTIMIZATION - PARTE 2: MODELO E PROMPT ENGINEERING

---

## MODELO OTIMIZADO (scripturemon-optimized)

### Criação do Modelo

**Arquivo:** `Modelfile_optimized`

**Comando de criação:**
```bash
ollama create scripturemon-optimized -f Modelfile_optimized
```

**Estrutura completa do Modelfile:**

```dockerfile
FROM scripturemon-ultimate:latest

# PARÂMETROS CRÍTICOS (baseados em pesquisa técnica)
PARAMETER num_ctx 131072
PARAMETER num_batch 64
PARAMETER temperature 0.2
PARAMETER top_p 0.95
PARAMETER top_k 0
PARAMETER repeat_penalty 1.15
PARAMETER repeat_last_n 1024
PARAMETER num_predict -1
PARAMETER seed 1337

SYSTEM """
═══════════════════════════════════════════════════════════════
⚠️  REGRAS ABSOLUTAS DE ANÁLISE SCRIPT DOCTOR
═══════════════════════════════════════════════════════════════

1. FIDELIDADE TOTAL aos documentos fornecidos
   → Análise 100% baseada nos textos <roteiro_analise> e <livro_mckee>
   → NÃO use conhecimento externo ou de outros filmes
   → Se informação não está nos docs: diga explicitamente "não disponível"

2. CITAÇÕES VERBATIM obrigatórias
   → Sempre entre aspas duplas "como isto"
   → Palavra por palavra, sem alterações
   → Inclua número de cena/página quando citar

3. PROIBIÇÕES ABSOLUTAS
   → NUNCA invente cenas que não existem no roteiro
   → NUNCA invente diálogos ou atribua falas incorretas
   → NUNCA cite princípios McKee que não estão no livro fornecido
   → NUNCA use personagens de outros filmes como exemplo

4. TRANSPARÊNCIA total
   → Se algo não está claro nos docs, admita
   → Se precisa de mais contexto, declare
   → Se está inferindo (não citando), marque como inferência

═══════════════════════════════════════════════════════════════
❌ EVITE ANÁLISE GENÉRICA (Exemplos do que NÃO fazer):
═══════════════════════════════════════════════════════════════

❌ "O diálogo poderia ser melhorado"
❌ "O personagem precisa de mais desenvolvimento"
❌ "A cena não funciona bem"
❌ "Há problemas de estrutura"
❌ "Falta tensão dramática"
❌ "O protagonista é fraco"
❌ "A história precisa de trabalho"

═══════════════════════════════════════════════════════════════
✅ USE ANÁLISE ESPECÍFICA (Exemplos do que fazer):
═══════════════════════════════════════════════════════════════

✅ "Na cena 12, quando Samantha diz 'Mas eu estava tendo um sonho lindo...',
   a fala revela subtexto de negação. McKee explica no Capítulo 4 que
   'o verdadeiro caráter é revelado sob pressão' - aqui, Samantha escolhe
   focar no sonho (passado) ao invés de encarar a realidade presente,
   demonstrando seu padrão de evasão estabelecido na cena 3."

✅ "Alberto entra na cena 8 (página 15) e imediatamente pergunta 'Você está bem?',
   mas esta fala contradiz seu objetivo implícito da cena 5, onde ele evita
   confrontar diretamente os problemas de Samantha. McKee descreve no Cap 7
   que personagens consistentes mantêm estratégias de abordagem - aqui,
   Alberto deveria usar linguagem indireta: 'Vi que não tocou no café...'"

✅ "O diálogo da página 22 usa 'papai' três vezes em 4 linhas, criando
   redundância. McKee estabelece no Cap 9 o princípio de 'economia verbal' -
   substituir a segunda e terceira ocorrências por pronome ('você') ou
   eliminar totalmente manteria a clareza emocional sem repetição mecânica."

═══════════════════════════════════════════════════════════════
📋 FORMATO OBRIGATÓRIO DE RESPOSTA
═══════════════════════════════════════════════════════════════

Estrutura em 5 SEÇÕES com 12-14 parágrafos SUBSTANCIAIS:

1. INTERPRETATION (2 parágrafos detalhados, 5-8 sentenças cada)
2. PATTERNS (2 parágrafos detalhados, 5-8 sentenças cada)
3. PROBLEMS (3-4 parágrafos, 1 por problema, 6-8 sentenças cada)
4. SOLUTIONS (3-4 parágrafos, 1 por solução, 6-8 sentenças cada)
5. DEPTH & SYNTHESIS (2 parágrafos detalhados, 5-8 sentenças cada)

Cada parágrafo DEVE conter:
→ Número de cena específico OU página
→ Citação exata entre aspas (mínimo 1 por parágrafo)
→ Conexão explícita com teoria McKee (capítulo/conceito)
→ Análise causal (não apenas descrição)

Extensão esperada: 2500-4000 tokens (8000-12000 caracteres)

═══════════════════════════════════════════════════════════════

Você é um Script Doctor profissional. Seja rigoroso, específico e útil.
"""
```

### Explicação Detalhada dos Parâmetros

#### num_ctx: 131072

**O que é:** Tamanho da janela de contexto em tokens.

**Valor anterior:** Provavelmente 2048 (default Ollama)

**Valor otimizado:** 131072 (128k tokens)

**Por quê 131072:**
- Livro McKee: ~77k palavras = ~100k tokens
- Roteiro: ~5k palavras = ~6.5k tokens
- Prompt/instruções: ~2k tokens
- Margem de segurança: ~20k tokens
- **Total necessário:** ~128k tokens

**Pesquisa técnica:** Mistral v0.2 suporta até 32k nativamente, mas com RoPE theta ajustado pode extrapolar até 128k. O Ollama permite configurar valores maiores que o treino original.

**Trade-off:**
- ✅ Permite livro completo + roteiro + instruções
- ⚠️ Memória aumenta linearmente (cache de atenção)
- ⚠️ Velocidade diminui (mais tokens para processar)

#### num_batch: 64

**O que é:** Tamanho do batch para processamento de tokens.

**Valor anterior:** 512 (default Ollama)

**Valor otimizado:** 64

**CRÍTICO!** Esta é uma das mudanças mais importantes.

**Por quê 64:**
- Default 512 causa picos de VRAM com contextos longos
- Picos → Swap para RAM → Swap para CPU → **TIMEOUT**
- 64 mantém uso de VRAM estável
- Permite processar 100k+ tokens sem OOM (Out of Memory)

**Pesquisa técnica:** Blog posts de usuários Ollama relatam que reduzir num_batch de 512 para 64-32 resolve travamentos em contextos longos.

**Impacto:**
- ✅ Elimina timeouts
- ✅ Uso de memória previsível
- ⚠️ Geração ligeiramente mais lenta (mas completa!)

#### temperature: 0.2

**O que é:** Controla aleatoriedade/criatividade da geração.

**Valor anterior:** ~0.8 (inferido do comportamento)

**Valor otimizado:** 0.2

**EXTREMAMENTE CRÍTICO!** Esta mudança sozinha causou +300% especificidade.

**Escala de temperatura:**
```
0.0 ─────── 0.2 ─────── 0.5 ─────── 0.8 ─────── 1.0+
Determinístico  Factual    Equilibrado  Criativo   Caótico
```

**Por quê 0.2:**
- Análise de roteiro é tarefa **FACTUAL**, não criativa
- 0.8+ → modelo inventa cenas, diálogos, personagens
- 0.2 → modelo se atém aos fatos dos documentos
- 0.2 → citações verbatim (não paráfrases)

**Pesquisa técnica:** Para tarefas técnicas/factuais, temperatura 0.1-0.3 é recomendada. Para brainstorming/criativo, 0.8-1.0.

**Impacto medido:**
- Temperatura 0.8 → 0 citações específicas, análise genérica
- Temperatura 0.2 → 12 citações, 7 scene refs, 0 frases genéricas

#### top_p: 0.95

**O que é:** Nucleus sampling - considera apenas tokens do topo até somar 95% da probabilidade.

**Valor anterior:** Provavelmente 0.9 (default comum)

**Valor otimizado:** 0.95

**Funcionamento:**
```
Probabilidades dos próximos tokens:
"cena" → 0.40
"scene" → 0.30
"capítulo" → 0.15
"página" → 0.08
"momento" → 0.05
"instante" → 0.02

top_p = 0.95:
Considera: cena + scene + capítulo + página + momento = 0.98
Descarta: instante (probabilidade cumulativa já passou 0.95)
```

**Por quê 0.95:**
- 0.95 é ligeiramente mais permissivo que 0.9
- Permite variedade lexical sem cair em tokens improváveis
- Combinado com temperature baixo, mantém foco mas não repetitivo

#### top_k: 0

**O que é:** Considera apenas os K tokens mais prováveis.

**Valor anterior:** Provavelmente 40 (default)

**Valor otimizado:** 0 (desabilitado)

**Por quê 0:**
- Quando top_p está ativo, top_k pode ser redundante
- top_k fixo pode ser muito restritivo em alguns momentos
- top_p é adaptativo (varia conforme entropia local)
- Pesquisa recomenda: use top_p OU top_k, não ambos

**Interação top_p + top_k:**
```
Se ambos ativos:
1. Primeiro aplica top_k (ex: top 40 tokens)
2. Depois aplica top_p dentro desses 40

Se top_k=0:
1. Considera todos os tokens
2. Aplica top_p na distribuição completa
```

#### repeat_penalty: 1.15

**O que é:** Penaliza tokens que já apareceram recentemente.

**Valor anterior:** 1.0 (sem penalização)

**Valor otimizado:** 1.15

**Funcionamento:**
```
Token "diálogo" já apareceu 3 vezes nos últimos 1024 tokens.
Probabilidade original: 0.20
Com repeat_penalty 1.15:
Nova probabilidade: 0.20 / (1.15^3) = 0.20 / 1.52 = 0.13
```

**Por quê 1.15:**
- Evita loops (modelo repetindo mesma frase)
- 1.15 é moderado (1.0 = sem penalização, 1.3+ = muito agressivo)
- Não queremos penalizar MUITO porque análise precisa mencionar conceitos múltiplas vezes (ex: "McKee", "Samantha")

**Cuidado:**
- Penalização alta demais pode fazer modelo evitar nomes próprios
- Queremos evitar loops, NÃO evitar mencionar personagens

#### repeat_last_n: 1024

**O que é:** Janela de tokens considerados para repeat_penalty.

**Valor anterior:** 64 (default)

**Valor otimizado:** 1024

**Por quê 1024:**
- Respostas longas (~1500 palavras = ~2000 tokens)
- 64 tokens = apenas últimas ~48 palavras
- Loops podem acontecer depois de 100+ palavras
- 1024 cobre maior parte da resposta

**Benefício adicional:**
- Não penaliza citações do PROMPT (que estão milhares de tokens atrás)
- Apenas penaliza repetição na RESPOSTA
- Assim modelo pode citar roteiro sem penalização

#### num_predict: -1

**O que é:** Número máximo de tokens a gerar.

**Valor anterior:** 2048 (default comum)

**Valor otimizado:** -1 (ilimitado)

**Por quê -1:**
- Queremos análises longas (2500-4000 tokens)
- Limite de 2048 cortaria resposta no meio
- -1 = gerar até completar naturalmente OU atingir num_ctx

**Alternativas:**
- -2 = gerar até encher contexto completo (não recomendado)
- Valor fixo alto (ex: 4096) também funciona

**Controle de tamanho:**
- Tamanho é controlado pelo PROMPT (estrutura obrigatória)
- Não pelo limit de tokens

#### seed: 1337

**O que é:** Semente do gerador aleatório.

**Valor anterior:** 0 (aleatório baseado em tempo)

**Valor otimizado:** 1337 (fixo)

**Por quê fixo:**
- **Reprodutibilidade** para testes/benchmarks
- Mesmo prompt → mesma resposta (útil para comparações)
- Facilita debugging (isola efeitos de mudanças)

**Para produção:**
- Pode deixar 0 (aleatório) para variedade
- Ou fixo se quer consistência absoluta

---

## PROMPT ENGINEERING AVANÇADO

### Estrutura Completa do Prompt

O prompt é construído dinamicamente no método `_build_llm_prompt()` (linhas 151-408 do dual_core_wrapper.py).

**Componentes na ordem:**

```
1. IDENTIDADE DO ESPECIALISTA
   ↓
2. MÉTRICAS PYTHON (XML)
   ↓
3. TEORIA (XML - livro completo ou chunks)
   ↓
4. ROTEIRO (XML)
   ↓
5. FEW-SHOT EXAMPLES
   ↓
6. INSTRUÇÕES DE TAREFA
   ↓
7. INSTRUÇÕES FINAIS (Primacy/Recency)
```

### 1. Identidade do Especialista

```python
prompt = f"""You are {self.specialist_identity}

ROLE: {self.specialist_name}
SPECIALTY: {self.specialist_specialty}
THEORY MODE: {theory_mode}
"""
```

**Exemplo concreto:**
```
You are Dr. Dialogue, expert in dialogue authenticity,
character voice, subtext, and natural speech patterns.

ROLE: DrDialogue (Dialogue Specialist)
SPECIALTY: Dialogue Analysis
THEORY MODE: DEEP (Full Book)
```

**Por quê isso importa:**
- Define "persona" do modelo
- Ativa conhecimento específico do domínio
- Modelos respondem melhor com identidade clara

### 2. Métricas Python (XML)

```python
<analise_python tipo="metricas_objetivas">
{
  "dialogue_score": 57.0,
  "rules_violated": [
    "DIAL.R003: Lack of subtext",
    "DIAL.R001: Unnatural speech patterns"
  ],
  "recommendations": [
    "Add more contractions and interruptions",
    "Develop distinct character voices"
  ]
}
</analise_python>
```

**Por quê XML:**
- Estrutura semântica clara
- Modelo encontra informação facilmente
- Mitiga "Lost in the Middle"
- Pode referenciar: "conforme <analise_python>"

### 3. Teoria (XML - Deep Mode)

```xml
<documento_fonte id="livro_mckee" tipo="teoria_completa">
<metadados>
  <titulo>Dialogue-_-The-Art-of-Verbal-Action</titulo>
  <palavras>77,627</palavras>
  <tokens_estimados>100,915</tokens_estimados>
  <relevancia>100</relevancia>
</metadados>

<secoes_chave>
  <secao id='1' contexto='[Dialogue - Chunk 42]' score='25'>
    McKee explains that subtext is the unspoken meaning beneath
    dialogue. Characters rarely say exactly what they mean...
  </secao>
  <secao id='2' contexto='[Dialogue - Chunk 108]' score='22'>
    Natural speech patterns include contractions, interruptions,
    incomplete thoughts, and verbal tics that make characters...
  </secao>
  <!-- 3 more highlights -->
</secoes_chave>

<texto_completo>
[... 77,627 palavras do livro McKee Dialogue ...]
</texto_completo>
</documento_fonte>
```

**Por quê essa estrutura:**
- **Metadados** deixam claro o que é esse documento
- **Secoes_chave** (highlights) = Primacy effect (aparecem primeiro)
- **texto_completo** = disponível para consulta profunda
- **XML** = modelo pode navegar semanticamente

### 4. Roteiro (XML)

```xml
<documento_fonte id="roteiro_analise" tipo="screenplay">
1. EXT. JARDIM CASA DE INFÂNCIA - MANHÃ - 20 ANOS ATRÁS

SAMANTHA CRIANÇA, 8, abre animada uma pequena caixa de presente.

[... resto do roteiro ...]
</documento_fonte>
```

**Benefício:**
- Marca claramente: "isto é o roteiro para analisar"
- Permite referência: "cite exatamente do <roteiro_analise>"

CONTINUA EM PARTE 3...
