# 🌐 Research Prompts Customized by Platform

Este documento contém versões otimizadas do prompt de pesquisa para diferentes fóruns e comunidades.

---

## 1️⃣ Reddit r/LocalLLaMA (Conciso + Técnico)

**Título**: [Help] Mixtral 8x7B with 128K context in Ollama - parameters ignored?

**Post**:

Hey LocalLLaMA community! Need expert help debugging an Ollama Modelfile issue.

**TL;DR**: Configured `num_ctx 131072` (128K) but `ollama show` reports 32768 (32K). Also, 97.7% of outputs stop at 3-5K chars despite requiring 10-15K. Suspect `FROM <blob-hash>` ignores parameters.

**System**: Scripturemon - screenplay analysis using Mixtral 8x7B
- Input: ~100K tokens (screenplay + theory book)
- Required output: 10-15K characters
- Actual output: 3-5K characters (97.7% of time)

**Current Modelfile**:
```dockerfile
FROM /Users/.ollama/models/blobs/sha256-e6cc...  # ← Suspect this ignores params
PARAMETER num_ctx 131072  # ← Not applied (shows 32768)
PARAMETER num_predict -1
PARAMETER temperature 0.3
```

**Questions**:
1. Does `FROM <blob-hash>` ignore Modelfile parameters?
2. How to properly configure 128K context on Mixtral 8x7B in Ollama?
3. Why does LLM stop at 3-5K chars despite `num_predict -1` and explicit prompts?
4. Should we use `mirostat 2` to prevent early stopping?

**What we've tried**:
- ✅ Removed `repeat_penalty` → +42% improvement but still short
- ✅ Temperature tested (0.3 optimal)
- ❌ Two-pass generation (helped but not enough)
- ❌ Explicit length requirements in prompt (10+ mentions, ignored)

**Full details**: [Link to RESEARCH_PROMPT_MODELFILE_OPTIMIZATION.md]

Anyone successfully running Mixtral 8x7B with 128K context in Ollama? What's your Modelfile?

---

## 2️⃣ Ollama Discord/Forum (Direto ao Ponto)

**Título**: `FROM <blob-hash>` ignores `num_ctx` parameter?

**Mensagem**:

Hi Ollama team! 👋

We're experiencing an issue where Modelfile parameters seem to be ignored when using `FROM <blob-hash>` instead of `FROM <model-name>`.

**Setup**:
```bash
# Modelfile
FROM /Users/.ollama/models/blobs/sha256-e6cc...
PARAMETER num_ctx 131072

# Verification
$ ollama show my-model | grep context
context length      32768  # ← Should be 131072!
```

**Questions**:
1. Is this expected behavior? Should `FROM <blob-hash>` not support parameter overrides?
2. If we change to `FROM mixtral:8x7b-instruct-v0.1-q5_K_M`, will parameters be applied?
3. Does Ollama support RoPE scaling for context extension? Any hidden parameters?

**Context**: Running 312 sequential analyses, need stable 128K context window. Currently getting 32K despite configuration.

Any clarification would be greatly appreciated!

---

## 3️⃣ Stack Overflow (Formal + Code-Heavy)

**Título**: Ollama Modelfile parameters ignored when using blob hash in FROM directive

**Tags**: `ollama`, `llm`, `mixtral`, `modelfile`, `context-length`

**Question**:

I'm configuring an Ollama model with extended context window (128K tokens) but the parameter appears to be ignored.

### Current Configuration

```dockerfile
# Modelfile
FROM /Users/clubproducoes/.ollama/models/blobs/sha256-e6cc1aad1542904098779a9f3af9a1e5ab462b1c40c14c9fcc8ecc24abd81d61

PARAMETER num_ctx 131072
PARAMETER num_predict -1
PARAMETER temperature 0.3
```

### Verification

```bash
$ ollama show scripturemon-optimized:latest | grep "context"
context length      32768  # Expected: 131072
```

### Expected Behavior

Parameters defined in Modelfile should override defaults, resulting in 128K token context window.

### Actual Behavior

Model uses 32K tokens despite `num_ctx 131072` configuration.

### Questions

1. Does `FROM <blob-hash>` prevent parameter overrides in Ollama?
2. Should I use `FROM mixtral:8x7b-instruct-v0.1-q5_K_M` instead for parameters to apply?
3. Are there additional parameters needed for RoPE scaling on Mixtral 8x7B (e.g., `rope_scaling_type`)?

### Environment

- **Ollama Version**: Latest (Oct 2024)
- **Model**: Mixtral 8x7B Instruct v0.1 (Q5_K_M)
- **OS**: macOS
- **Use Case**: Programmatic API calls with large context (~100K tokens)

### What I've Tried

1. Recreating model with `ollama create` - same result
2. Different `num_ctx` values - all ignored
3. Checking with `ollama show` - confirms parameters not applied

Any insights appreciated!

---

## 4️⃣ HuggingFace Forums (Research-Oriented)

**Título**: Optimizing Mixtral 8x7B for Long-Form Analytical Generation

**Post**:

Hello HF community! 🤗

I'm working on a screenplay analysis system using Mixtral 8x7B via Ollama and encountering consistent output truncation issues that might interest the research community.

**Research Problem**:
Despite explicit length requirements (10,000-15,000 characters), the model consistently stops generation at 3,000-5,000 characters in 97.7% of cases.

**Setup**:
- Model: Mixtral 8x7B Instruct v0.1 (Q5_K_M via Ollama)
- Context: ~100K tokens (screenplay + reference material)
- Task: Analytical writing (structured problem identification + solutions)
- Temperature: 0.3 (analytical, not creative)

**Parameters Tested**:
```python
temperature: 0.2 → 0.3 → 0.4 (0.3 optimal)
repeat_penalty: 1.2 → removed (+42% improvement!)
seed: 42 → removed (non-deterministic better)
num_predict: -1 (unlimited)
```

**Hypotheses**:
1. **Context truncation**: Configured 128K but only 32K applied (Ollama issue)
2. **Mirostat missing**: No perplexity control → premature stopping
3. **Prompt engineering insufficient**: Explicit length requirements ignored
4. **Sampling params**: `min_p 0.05` too restrictive for long outputs?

**Questions for Researchers**:
1. Any papers on controlling output length beyond prompt engineering?
2. Perplexity-based stopping criteria - can it extend outputs?
3. Optimal sampling parameters for analytical (non-creative) long-form generation?
4. Multi-stage generation strategies that work?

**Interesting Findings**:
- Removing `repeat_penalty` improved output by +42%
  - Hypothesis: Analytical writing requires term repetition (e.g., "character", "structure")
  - Penalty was suppressing legitimate technical vocabulary
- Non-deterministic generation (no seed) produced more complete outputs
  - Went from identifying 2 problems to 3 problems consistently

**Data Available**:
- 130 completed analyses with metrics
- Quality distribution: 97.7% short (Q=5.0), 2.3% complete (Q=10.0)
- Processing time: 45-120s (not timeout issue)

Would love to collaborate or hear about similar research!

**Full technical details**: [GitHub link if public]

---

## 5️⃣ Academic Mailing Lists (Formal Research)

**Subject**: Request for Collaboration: LLM Output Length Control in Analytical Tasks

**Email**:

Dear Colleagues,

I am reaching out to the research community regarding challenges in controlling Large Language Model output length for structured analytical tasks, which may be of mutual interest.

**Research Context**:

We are developing Scripturemon, a screenplay analysis system that employs a dual-core architecture:
1. Deterministic Python analysis (structural metrics)
2. LLM-based qualitative analysis (Mixtral 8x7B)

The system processes ~100K token inputs (screenplay + reference material) and should generate comprehensive analytical reports (10,000-15,000 characters). However, we observe consistent premature stopping at 3,000-5,000 characters despite explicit length requirements.

**Empirical Observations**:

- Sample size: 130 completed analyses
- Truncation rate: 97.7% stop short of requirements
- Temperature: 0.3 (analytical mode)
- Processing time: 45-120 seconds (eliminating timeout as factor)
- Context window: Configured 128K but only 32K applied (technical limitation)

**Interventions Tested**:

1. Removing repetition penalty → +42% output length improvement
   - Hypothesis: Technical vocabulary requires legitimate repetition
   - Penalty mechanism incompatible with domain-specific terminology

2. Non-deterministic sampling → More complete problem identification
   - Deterministic mode (seed=42): 2 problems identified
   - Non-deterministic mode: 3 problems identified consistently

3. Two-pass generation architecture → Partial improvement
   - Pass 1: Problem identification
   - Pass 2: Solution expansion
   - Still insufficient for target length

**Research Questions**:

1. Beyond prompt engineering, what mechanisms control LLM stopping criteria?
2. Can perplexity-based control (e.g., Mirostat) extend output length?
3. What is the relationship between sampling parameters and output completeness?
4. Are there architectural approaches (multi-stage, chunked generation) that work reliably?

**Potential Collaboration**:

We have:
- Comprehensive dataset with metrics
- Production system requiring solution
- Resources for systematic experimentation

We're seeking:
- Theoretical frameworks for understanding stopping behavior
- Practical parameter optimization guidance
- Potential academic collaboration if research-worthy

**Technical Documentation**:
[Attached: RESEARCH_PROMPT_MODELFILE_OPTIMIZATION.md]

Would appreciate any insights, pointers to relevant literature, or interest in collaboration.

Best regards,
[Your Name]
[Institution/Organization]
[Contact Information]

---

## 6️⃣ Twitter/X Thread (Viral + Accessible)

**Thread**:

🧵 1/ We're building Scripturemon - an AI screenplay analyst using Mixtral 8x7B. Hit a fascinating bug: LLM stops at 3-5K chars despite being explicitly told to generate 10-15K chars. 97.7% truncation rate! 🤔

Let me explain... 👇

2/ The system analyzes screenplays using 24 specialized perspectives (dialogue, pacing, character, etc.) against 13 screenwriting theory books (McKee, Field, Campbell, etc.).

Each analysis processes ~100K tokens but should output 10-15K characters of insights.

3/ **The Problem**:
- Configured: "Generate 10,000+ characters"
- Expected: Detailed analysis with 4 problems + 4 solutions
- Reality: Stops at 3-5K characters (incomplete)
- Frequency: 97.7% of outputs!

Not a timeout issue - same processing time for short & complete outputs.

4/ **What We Tried**:

✅ Removed `repeat_penalty` → +42% improvement!
Why? Technical writing NEEDS repetition. Words like "character", "structure" appear 50+ times legitimately. Penalty was killing it.

But still not enough...

5/ ✅ Removed deterministic seed → Better problem identification!
- Before (seed=42): 2 problems found
- After (random): 3 problems found

Hypothesis: Non-deterministic sampling explores solution space better?

6/ ❌ Explicit length requirements in prompt → IGNORED
We tried:
- "MINIMUM 10,000 characters"
- Character count formulas
- Completion checklists
- Multiple warnings

LLM just... doesn't care? 🤷

7/ **The Mystery Deepens**:

Found old config that HAD 128K context working. Difference?

OLD: `FROM mixtral:8x7b-instruct-v0.1`
NEW: `FROM /Users/.ollama/models/blobs/sha256-...`

Hypothesis: Blob hash ignores Modelfile parameters! 🔍

8/ Also missing from new config:
- `mirostat 2` (perplexity control)
- `num_batch 1024` (was 64 - 16x smaller!)

Could Mirostat prevent premature stopping? 🤔

9/ **Questions for ML Twitter**:

1. Anyone used Mixtral 8x7B with 128K context successfully?
2. Does `FROM <blob-hash>` in Ollama ignore parameters?
3. Can Mirostat help with output length?
4. What REALLY controls when LLMs stop generating?

10/ If you're working on:
- Long-form LLM generation
- Ollama parameter optimization
- RoPE scaling / context extension
- Output length control

Would LOVE to chat! DMs open 📩

Full technical writeup: [link]

#LLM #AI #Mixtral #Ollama #MachineLearning

---

## 7️⃣ GitHub Issue (If Ollama is Open Source)

**Título**: [Bug?] Modelfile parameters ignored when FROM directive uses blob hash

**Labels**: `bug`, `modelfile`, `parameters`, `context-window`

**Description**:

### Bug Description

When a Modelfile uses `FROM <blob-hash>` instead of `FROM <model-name>`, parameters defined in the Modelfile appear to be ignored.

### Steps to Reproduce

1. Create Modelfile with blob hash FROM:
```dockerfile
FROM /Users/user/.ollama/models/blobs/sha256-e6cc1aad...
PARAMETER num_ctx 131072
PARAMETER temperature 0.3
```

2. Create model:
```bash
ollama create my-model -f Modelfile
```

3. Verify parameters:
```bash
ollama show my-model
```

### Expected Behavior

Parameters from Modelfile should be applied:
```
context length      131072
temperature         0.3
```

### Actual Behavior

Default parameters from blob are used instead:
```
context length      32768  # Ignores num_ctx 131072
```

### Environment

- **Ollama Version**: [version]
- **OS**: macOS [version]
- **Model**: Mixtral 8x7B Instruct v0.1 Q5_K_M

### Workaround

Using `FROM mixtral:8x7b-instruct-v0.1-q5_K_M` instead of blob hash appears to apply parameters correctly (not yet tested).

### Questions

1. Is this intended behavior?
2. Should blob hash FROM support parameter overrides?
3. If not, should there be a warning when parameters are ignored?

### Additional Context

This is causing production issues in our screenplay analysis system where we need:
- 128K context window (currently getting 32K)
- Specific sampling parameters for analytical outputs

Happy to provide more details or test fixes!

---

## 📋 Where to Post

### High Priority (Technical Communities):
1. ✅ **Reddit r/LocalLLaMA** - Active community, quick responses
2. ✅ **Ollama Discord/GitHub** - Direct access to developers
3. ✅ **HuggingFace Forums** - Research-oriented discussions

### Medium Priority (Broader Reach):
4. **Stack Overflow** - Long-term reference for others
5. **Twitter/X** - Community awareness, potential connections
6. **Reddit r/MachineLearning** - Academic perspective

### Lower Priority (If Relevant):
7. **Academic mailing lists** - If research collaboration desired
8. **LLM-specific forums** (Together AI, Replicate, etc.)

---

## 🎯 Posting Strategy

### Week 1:
- **Day 1**: Reddit r/LocalLLaMA + Ollama Discord
- **Day 2-3**: Monitor responses, iterate
- **Day 4**: HuggingFace Forums (with updates from Day 1-3)

### Week 2:
- **Day 7**: Stack Overflow (comprehensive Q&A)
- **Day 8**: Twitter thread (if gaining traction)
- **Day 10**: Follow up with findings across all platforms

### Continuous:
- Update all posts with **"🔄 UPDATE"** section as we learn
- Link posts together for cross-referencing
- Thank contributors publicly
- Share final solution everywhere

---

## 📊 Expected Outcomes

### Best Case:
- Ollama dev confirms bug + commits fix
- Community shares working configurations
- We solve 128K context + length issues
- Write blog post about findings

### Realistic Case:
- Multiple helpful suggestions to test
- Deeper understanding of Mirostat/sampling
- Working configuration through iteration
- Contribute back to Ollama docs

### Worst Case:
- Confirm Mixtral 8x7B limitations
- Migrate to different model/approach
- Document findings for others

---

**All prompts ready to copy-paste!**
