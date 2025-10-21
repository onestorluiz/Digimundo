# 🔬 Research Request: Optimizing Ollama Modelfile for Large-Context Screenplay Analysis System

## 📋 Executive Summary

We're developing **Scripturemon**, a professional screenplay analysis system that uses Mixtral 8x7B via Ollama to generate comprehensive script doctor reports. We're experiencing critical issues with response completeness (97.7% of outputs are truncated at 3-5k characters instead of the required 10-15k) despite having a 128K token context window configured.

**We need expert guidance on Ollama Modelfile parameter optimization to achieve consistent, complete, long-form analytical outputs.**

---

## 🎯 System Overview

### What We're Building

**Scripturemon** is a dual-core screenplay analysis engine that combines:

1. **Python Core**: Structural analysis using 24 specialized analyzers (dialogue, character, pacing, theme, etc.)
2. **LLM Core**: Qualitative analysis synthesizing insights from 13 screenwriting theory books (McKee, Field, Truby, Campbell, Vogler, Seger, Egri, etc.)

### Analysis Pipeline

```
INPUT: Screenplay PDF (60-120 pages)
  ↓
PYTHON ANALYSIS: Objective metrics (structure, dialogue patterns, pacing)
  ↓
LLM ANALYSIS: Deep qualitative insights
  - Context: Screenplay + Full theory book (~100k tokens total)
  - Required Output: 10,000-15,000 characters
  - Actual Output: 3,000-5,000 characters (PROBLEM!)
  ↓
OUTPUT: Comprehensive HTML report with problems + solutions
```

### Scale

- **312 total analyses** per screenplay (24 specialists × 13 authors)
- **Each analysis** processes ~100k tokens input, generates 10-15k chars output
- **Current bottleneck**: 97.7% of analyses incomplete (stop at 3-5k chars)

---

## 🚨 The Problem

### Symptom

**97.7% of LLM outputs are 3,000-5,000 characters when 10,000-15,000 characters are explicitly required.**

### What We've Tried

1. ✅ **Removed `repeat_penalty 1.2`** → Improved output by +42% (4,236 → 6,066 chars) but still insufficient
2. ✅ **Removed `seed`** → Non-deterministic output, went from 2 to 3 problems identified (improvement)
3. ✅ **Temperature optimization** → Tested 0.2-0.4, settled on 0.3 as optimal
4. ✅ **Explicit length requirements** in system prompt (10+ mentions of minimum length)
5. ✅ **Two-pass architecture** → Pass 1 identifies problems, Pass 2 expands solutions (helped but not enough)
6. ❌ **Timeout is NOT the issue** → Q=5.0 (short) and Q=10.0 (complete) have similar processing times (45-120s)

### Current Status

- ✅ Context window: **SHOULD BE 128K** (configured as `num_ctx 131072`)
- ❌ **ACTUAL context window: 32K** (verified via `ollama show`)
- ❌ **Root cause identified**: `FROM <blob-hash>` instead of `FROM <model-name>` ignores all parameters

---

## 📊 Current Modelfile Configuration

### The Broken Modelfile

```dockerfile
# CURRENT (BROKEN - Parameters Ignored!)
FROM /Users/clubproducoes/.ollama/models/blobs/sha256-e6cc1aad...

TEMPLATE "[INST] {{ if .System }}{{ .System }} {{ end }}{{ .Prompt }} [/INST] {{ .Response }}
"

PARAMETER top_k 40
PARAMETER top_p 0.9
PARAMETER min_p 0.05
PARAMETER num_batch 64
PARAMETER num_ctx 131072           # ← IGNORED due to blob hash FROM
PARAMETER num_predict -1
PARAMETER stop [INST]
PARAMETER stop [/INST]
PARAMETER temperature 0.3

MESSAGE assistant "
🎬 **Olá! Sou o Scripturemon Master!**
..."
```

### Historical Modelfile (WORKED with 128K)

```dockerfile
# HISTORICAL (FUNCTIONAL 128K)
FROM mixtral:8x7b-instruct-v0.1-q5_K_M

PARAMETER temperature 0.25
PARAMETER top_p 0.9
PARAMETER top_k 50
PARAMETER repeat_penalty 1.2       # We removed this (+42% improvement)
PARAMETER seed 42                  # We removed this (non-deterministic better)

PARAMETER num_ctx 131072           # 128K tokens - APPLIED CORRECTLY
PARAMETER num_predict 8192
PARAMETER num_thread 10
PARAMETER num_batch 1024           # 16x larger than current!

PARAMETER mirostat 2               # Missing from current!
PARAMETER mirostat_eta 0.1         # Missing from current!
PARAMETER stop "```"
```

---

## 🔬 Specific Research Questions

### 1. **Context Window Application**

**Q1.1:** Does `FROM <blob-hash>` ignore Modelfile parameters in Ollama?
- Our observation: `num_ctx 131072` in Modelfile but `ollama show` reports 32768
- Is this expected behavior?
- How to properly override context window when using blob hash?

**Q1.2:** Is RoPE scaling automatic with `num_ctx 131072` on Mixtral 8x7B?
- Do we need explicit `rope_scaling_type`, `rope_freq_base`, `rope_freq_scale`?
- Does Mixtral 8x7B support 128K natively or needs configuration?
- Are there Ollama-specific parameters for RoPE extension?

**Q1.3:** YaRN vs Linear vs NTK-aware RoPE scaling
- Which method works for Mixtral 8x7B in Ollama?
- How to configure in Modelfile?
- Performance/quality tradeoffs?

---

### 2. **Generation Length Control**

**Q2.1:** Why does LLM stop at 3-5k chars despite explicit 10-15k requirement?
- System prompt mentions "10,000 caracteres" 10+ times
- `num_predict -1` (unlimited) configured
- No timeout applied
- What controls stopping criteria?

**Q2.2:** `num_predict` behavior
- Does `-1` actually mean unlimited in Ollama?
- Should we use explicit large value (e.g., `num_predict 16000`)?
- What's the relationship between `num_predict` (tokens) and output length (chars)?
- Are there internal Ollama limits regardless of parameter?

**Q2.3:** Mirostat for length control
- Historical config had `mirostat 2` and `mirostat_eta 0.1`
- Can Mirostat help prevent premature stopping?
- How does perplexity control affect output length?
- Optimal `mirostat_tau` value for long-form analytical writing?

---

### 3. **Batch Processing Optimization**

**Q3.1:** `num_batch` impact
- Current: 64
- Historical: 1024 (16x larger)
- Does `num_batch` affect output length or just speed?
- Can small batch size cause truncation?
- Memory vs speed tradeoff?

**Q3.2:** Multi-request stability
- Running 312 sequential analyses (24h+ runtime)
- Do parameters drift between requests?
- Should we restart Ollama periodically?
- Are there accumulation effects?

---

### 4. **Sampling Parameters**

**Q4.1:** Current configuration effectiveness
```
temperature: 0.3 (analytical, not creative)
top_k: 40
top_p: 0.9
min_p: 0.05
```
- Is `min_p 0.05` too restrictive for long outputs?
- Should `top_k` be larger for diverse vocabulary in long texts?
- Optimal `top_p` for analytical writing?

**Q4.2:** Removed parameters - should we restore?
- `repeat_penalty 1.2`: We removed it (+42% improvement) - correct decision?
- `seed 42`: We removed it (non-deterministic better) - correct decision?

**Q4.3:** Missing parameters worth testing?
- `tfs_z` (Tail Free Sampling)?
- `typical_p` (Typical Sampling)?
- `presence_penalty` / `frequency_penalty` (if available in Ollama)?

---

### 5. **System Prompt Design**

**Q5.1:** Can system prompt length requirements actually work?
- We explicitly state: "MÍNIMO ABSOLUTO: 10,000 caracteres"
- We include checklists, character count formulas, multiple warnings
- LLM still stops at 3-5k
- Is there a better prompting strategy?

**Q5.2:** Multi-pass vs single-pass generation
- Currently: Pass 1 (identify problems) + Pass 2 (expand solutions)
- Helps but not enough
- Should we use more passes?
- Chunked generation with forced continuation?

---

### 6. **Modelfile Best Practices**

**Q6.1:** `FROM` directive best practices
- Use model name (`FROM mixtral:8x7b`) or blob hash?
- When do parameters get ignored?
- How to ensure parameters are applied?

**Q6.2:** `MESSAGE assistant` impact
- We have greeting message in Modelfile
- Does it condition model behavior?
- Should it be removed for programmatic API calls?
- Does it affect analytical vs conversational tone?

**Q6.3:** `TEMPLATE` customization
- Current: Standard Mistral template `[INST]...[/INST]`
- Should we customize for analytical tasks?
- Does template affect output length?

---

## 🎯 Desired Outcome

### Success Criteria

1. **128K context window** actually applied and verified
2. **≥80% of analyses reach 10,000+ characters** (currently 2.3%)
3. **Complete problem identification + detailed solutions** in every analysis
4. **Stable performance** across 312 sequential analyses
5. **Reasonable speed** (currently 45-120s per analysis, acceptable)

### Metrics

- **Quality Score Distribution**:
  - Current: 97.7% Q=5.0 (incomplete), 2.3% Q=10.0 (complete)
  - Target: 20% Q=5.0, 80% Q=10.0
- **Character Count**:
  - Current Avg: 4,200 chars
  - Target Avg: 12,000 chars
- **Completion Rate**:
  - Current: Analysis stops before 4th problem/solution
  - Target: All 14 paragraphs generated

---

## 💡 Proposed Modelfile (Needs Validation)

Based on our research, we're considering:

```dockerfile
FROM mixtral:8x7b-instruct-v0.1-q5_K_M  # Use model name, not blob hash

# Context
PARAMETER num_ctx 131072                # 128K tokens
PARAMETER num_thread 10
PARAMETER num_batch 1024                # Large batch for stability

# Generation
PARAMETER num_predict 16000             # Explicit large value instead of -1
PARAMETER temperature 0.3               # Tested optimal
PARAMETER top_k 40                      # Tested optimal
PARAMETER top_p 0.9
PARAMETER min_p 0.05

# Mirostat for perplexity control
PARAMETER mirostat 2
PARAMETER mirostat_eta 0.1
PARAMETER mirostat_tau 5.0              # Suggested value?

# Stop sequences
PARAMETER stop [INST]
PARAMETER stop [/INST]

# NO MESSAGE assistant (programmatic use)
# NO repeat_penalty (tested: removal improves output)
# NO seed (tested: non-deterministic better)

TEMPLATE "[INST] {{ if .System }}{{ .System }} {{ end }}{{ .Prompt }} [/INST] {{ .Response }}
"

SYSTEM """
[Detailed analytical instructions: 10,000+ character requirement, 14 paragraphs, etc.]
"""
```

---

## ❓ Specific Questions for the Community

### For Ollama Experts:
1. Is our diagnosis correct that `FROM <blob-hash>` ignores parameters?
2. Best way to configure 128K context on Mixtral 8x7B in Ollama?
3. Does Ollama support RoPE scaling parameters? If so, what are they?

### For Mixtral Users:
4. Has anyone successfully used Mixtral 8x7B with 128K context in Ollama?
5. What's the maximum practical context length you've achieved?
6. Any gotchas with large context windows?

### For Long-Form Generation:
7. Best parameters for consistent 10K+ character analytical outputs?
8. Does Mirostat help with output length? Optimal settings?
9. Should `num_predict` be explicit large value or `-1`?

### For Academic/Research Community:
10. Papers or research on controlling LLM output length?
11. Perplexity-based stopping criteria vs explicit length requirements?
12. Best practices for multi-stage analytical generation?

---

## 🔧 System Specs

- **Hardware**: Mac (Apple Silicon M-series likely)
- **Ollama Version**: [Latest as of Oct 2024]
- **Model**: Mixtral 8x7B Instruct v0.1 (Q5_K_M quantization)
- **Model Size**: 33 GB
- **RAM**: Sufficient for full model loading
- **Use Case**: Programmatic API calls via `subprocess.run(['ollama', 'run', model])`

---

## 📚 References & Prior Art

We've studied:
- McKee's "Story" (analysis methodology)
- Ollama documentation (official docs)
- Reddit r/LocalLLaMA discussions on context extension
- HuggingFace discussions on Mixtral capabilities
- Academic papers on RoPE scaling (YaRN, NTK-aware scaling)

**We're NOT finding clear answers on:**
1. Ollama's specific implementation of RoPE scaling
2. Why `FROM <blob-hash>` might ignore parameters
3. How to reliably generate 10K+ character analytical outputs

---

## 🙏 How You Can Help

1. **Validate our diagnosis** - Is `FROM <blob-hash>` the issue?
2. **Share working Modelfiles** - Anyone achieving 10K+ chars consistently?
3. **Explain Mirostat** - Can it help? Optimal settings for analytical writing?
4. **Suggest parameters** - What are we missing? What should we test?
5. **Point to resources** - Papers, blog posts, GitHub issues we should read?
6. **Share experiences** - Similar use cases? What worked for you?

---

## 📧 Contact & Discussion

We're open to:
- Collaborative debugging sessions
- Sharing our codebase for investigation
- Testing proposed configurations
- Contributing findings back to community
- Academic collaboration (if relevant to research)

**Any insights, suggestions, or pointers to resources would be incredibly valuable!**

Thank you for reading this detailed request. We're committed to solving this systematically and sharing our findings with the community.

---

## 🔄 Updates

[We'll update this section as we test suggestions and learn more]

**Current Status**:
- Analysis running: 130/312 (41.7%)
- Waiting for expert input before recreating model
- Dashboard: http://localhost:8080

---

**Keywords**: Ollama, Mixtral 8x7B, Modelfile optimization, RoPE scaling, long-form generation, context window, Mirostat, perplexity control, LLM parameters, analytical writing, batch processing, screenplay analysis

---

*Posted on behalf of Digimundo/Scripturemon project*
*Looking for technical expertise to solve production system bottleneck*
