"""
GPT-5 Self-Evaluator - AI-Powered System Analysis

This module enables GPT-5 to evaluate its own performance after completing
a full screenplay analysis with all 24 specialists.

The self-evaluator generates a comprehensive report covering:
- Performance ratings per specialist
- Cost/benefit analysis
- System architecture feedback
- Upgrade recommendations
- Comparison with Ollama baseline
"""

import os
import json
from typing import Dict, Any, List
from datetime import datetime

def run_self_evaluation(
    analysis_results: List[Dict[str, Any]],
    cost_summary: Dict[str, Any],
    execution_time: float,
    screenplay_title: str = "Unknown"
) -> str:
    """
    Run GPT-5 self-evaluation after completing all specialist analyses.

    Args:
        analysis_results: List of analysis results from all specialists
        cost_summary: Cost summary from dual_core_wrapper.get_openai_cost_summary()
        execution_time: Total execution time in seconds
        screenplay_title: Title of analyzed screenplay

    Returns:
        Markdown-formatted evaluation report
    """

    try:
        from openai import OpenAI
    except ImportError:
        return "# ERROR: OpenAI library not installed\n\nRun: pip install openai"

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return "# ERROR: OPENAI_API_KEY not set\n\nPlease set OPENAI_API_KEY environment variable."

    client = OpenAI(api_key=api_key)

    # Build comprehensive context for GPT-5
    context = _build_evaluation_context(
        analysis_results=analysis_results,
        cost_summary=cost_summary,
        execution_time=execution_time,
        screenplay_title=screenplay_title
    )

    # Build evaluation prompt
    prompt = _build_evaluation_prompt(context)

    print("\n🤖 GPT-5 analyzing system performance...")
    print(f"   Context size: {len(prompt):,} characters")
    print(f"   Specialists analyzed: {len(analysis_results)}")
    print(f"   Total cost so far: ${cost_summary.get('total_cost', 0):.4f}")
    print(f"   Execution time: {execution_time:.1f}s ({execution_time/60:.1f} min)")

    # Call GPT-5 for self-evaluation
    response = client.chat.completions.create(
        model="gpt-5",
        messages=[
            {
                "role": "system",
                "content": """You are an expert AI systems analyst evaluating the Scripturemon screenplay analysis system.

Your role is to provide objective, data-driven evaluation of:
- Analysis quality across all specialists
- Cost-effectiveness and budget optimization
- System architecture strengths and weaknesses
- Concrete, actionable improvement recommendations
- Comparison with alternative approaches (Ollama, etc.)

Be critical but constructive. Focus on measurable improvements."""
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        max_completion_tokens=8000  # Allow for comprehensive report
    )

    report = response.choices[0].message.content.strip()

    # Add metadata header
    metadata_header = _build_metadata_header(
        cost_summary=cost_summary,
        execution_time=execution_time,
        screenplay_title=screenplay_title,
        evaluation_tokens_in=response.usage.prompt_tokens,
        evaluation_tokens_out=response.usage.completion_tokens
    )

    full_report = metadata_header + "\n\n" + report

    print(f"✅ Self-evaluation complete")
    print(f"   Evaluation cost: ${(response.usage.prompt_tokens/1_000_000*1.00 + response.usage.completion_tokens/1_000_000*4.00):.4f}")
    print(f"   Report length: {len(report):,} characters")

    return full_report


def _build_evaluation_context(
    analysis_results: List[Dict[str, Any]],
    cost_summary: Dict[str, Any],
    execution_time: float,
    screenplay_title: str
) -> Dict[str, Any]:
    """Build comprehensive context for evaluation."""

    # Extract specialist names and key metrics
    specialists_summary = []
    for result in analysis_results:
        specialist_name = result.get('specialist_name', 'Unknown')

        # Try to extract quality scores or key metrics
        analysis = result.get('analysis', {})
        synthesis = analysis.get('synthesis', {})
        quality_score = synthesis.get('quality_score', 0.0)

        specialists_summary.append({
            'name': specialist_name,
            'quality_score': quality_score,
            'has_python_metrics': 'python_analysis' in analysis,
            'has_llm_insights': 'llm_analysis' in analysis,
            'response_length': len(str(analysis))
        })

    context = {
        'screenplay_title': screenplay_title,
        'total_specialists': len(analysis_results),
        'execution_time_seconds': execution_time,
        'execution_time_minutes': execution_time / 60,
        'specialists_summary': specialists_summary,
        'cost_summary': cost_summary,
        'timestamp': datetime.now().isoformat()
    }

    return context


def _build_evaluation_prompt(context: Dict[str, Any]) -> str:
    """Build comprehensive evaluation prompt for GPT-5."""

    prompt = f"""# SCRIPTUREMON SELF-EVALUATION REQUEST

You just completed a full screenplay analysis using 24 specialists for: **{context['screenplay_title']}**

## SYSTEM CONTEXT

**Scripturemon** is an advanced screenplay analysis system combining:
- **Python Core:** Structural metrics (acts, scenes, dialogue, pacing, etc.)
- **LLM Core (YOU):** Deep contextual insights using theory from 13 master books
- **24 Specialists:** character, structure, dialogue, theme, opening, climax, resolution, motivation, conflict, backstory, worldbuilding, symbolism, action, tension, subtext, exposition, foreshadowing, stakes, pacing, tone, transitions, twist, genre, evaluator

**Theory Foundation (13 books):**
1. McKee STORY - Gap theory, beats, sequences
2. McKee DIALOGUE - Subtext, character voice
3. McKee CHARACTER - Dimensionality, revelation under pressure
4. Campbell Hero 1000 Faces - Monomyth, hero's journey
5. Truby Anatomy 22 Steps - Organic plot, moral argument
6. Field Screenplay - Three-act paradigm, plot points
7. Vogler Writer's Journey - 12 stages, 8 archetypes
8. Egri Dramatic Writing - Premise-driven drama
9. Seger Good Script Great - Script development
10. Cowgill Short Films - Compression, economy
11. Aristotle Poetics - Mimesis, catharsis, unity
12. Snyder Save the Cat - 15-beat structure
13. Weiland Character Arcs - Positive/flat/negative arcs

**Query System:**
- ~3,120 ultra-specific queries across all specialists
- BM25 indexing for theory retrieval
- Deep context queries using exact author terminology

## PERFORMANCE DATA

**Execution Metrics:**
- Total specialists: {context['total_specialists']}
- Execution time: {context['execution_time_minutes']:.1f} minutes
- API calls: {context['cost_summary'].get('total_calls', 0)}
- Input tokens: {context['cost_summary'].get('total_input_tokens', 0):,}
- Output tokens: {context['cost_summary'].get('total_output_tokens', 0):,}
- **Total cost: ${context['cost_summary'].get('total_cost', 0):.4f}**

**Specialists Analyzed:**
"""

    # Add specialist-by-specialist summary
    for spec in context['specialists_summary']:
        prompt += f"- **{spec['name']}**: Quality={spec['quality_score']:.2f}, "
        prompt += f"Python={'✓' if spec['has_python_metrics'] else '✗'}, "
        prompt += f"LLM={'✓' if spec['has_llm_insights'] else '✗'}, "
        prompt += f"Length={spec['response_length']:,} chars\n"

    prompt += f"""
## YOUR EVALUATION TASK

Provide a comprehensive, data-driven evaluation covering:

### 1. PERFORMANCE ANALYSIS (Rate 1-10)
For each aspect, provide:
- Numerical rating (1-10)
- Key strengths observed
- Specific weaknesses identified
- Evidence from the data above

**Evaluate:**
- Overall analysis depth and quality
- Theory integration effectiveness
- Cost efficiency (value per dollar)
- Speed vs Ollama baseline (estimated 8-16 hours)
- Insight quality vs generic AI analysis
- Coverage across all 24 specialists

### 2. COST-BENEFIT ANALYSIS
- Is ${context['cost_summary'].get('total_cost', 0):.4f} justified by quality?
- Compare to Ollama (free but 10-20x slower)
- Break down cost per specialist
- Recommend optimal use cases for GPT-5 vs Ollama
- Suggest cost reduction strategies

### 3. SYSTEM ARCHITECTURE REVIEW
Evaluate the current architecture:
- Dual-Core design (Python + LLM)
- 24-specialist distribution
- Theory indexer effectiveness
- Query system quality
- Identify architectural bottlenecks
- Suggest structural improvements

### 4. THEORY INTEGRATION ASSESSMENT
- How well are the 13 theory books utilized?
- Are queries retrieving relevant passages?
- Gaps in theoretical coverage?
- Suggestions for additional theory books?
- Query optimization opportunities?

### 5. SPECIALIST-SPECIFIC RECOMMENDATIONS
For specialists with low quality scores or issues:
- Identify problematic specialists
- Diagnose root causes
- Suggest specific fixes (prompts, queries, logic)

### 6. UPGRADE ROADMAP
Prioritized list of improvements:
1. **Critical** (implement immediately)
2. **High Priority** (next sprint)
3. **Medium Priority** (future enhancement)
4. **Low Priority** (nice to have)

For each:
- Specific improvement description
- Expected impact (quality/cost/speed)
- Implementation complexity (low/med/high)
- Estimated time to implement

### 7. COMPARISON: GPT-5 vs OLLAMA
Based on this analysis:
- Quality difference (your honest assessment)
- Speed difference (measured: {context['execution_time_minutes']:.1f} min vs ~480-960 min)
- When to use GPT-5 vs Ollama?
- Hybrid strategies?

## OUTPUT FORMAT

Generate a **professional Markdown report** with:
- Clear section headers (##, ###)
- Numerical ratings with justification
- Specific, actionable recommendations
- Data-driven conclusions
- Honest self-assessment (be critical where needed)

**Be specific, be honest, be actionable.**

Your evaluation will drive the next phase of system development.
"""

    return prompt


def _build_metadata_header(
    cost_summary: Dict[str, Any],
    execution_time: float,
    screenplay_title: str,
    evaluation_tokens_in: int,
    evaluation_tokens_out: int
) -> str:
    """Build metadata header for evaluation report."""

    eval_cost = (evaluation_tokens_in / 1_000_000) * 1.00 + (evaluation_tokens_out / 1_000_000) * 4.00
    total_with_eval = cost_summary.get('total_cost', 0) + eval_cost

    header = f"""# SCRIPTUREMON GPT-5 SELF-EVALUATION REPORT
## Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## ANALYSIS METADATA

**Screenplay:** {screenplay_title}
**Execution Time:** {execution_time:.1f}s ({execution_time/60:.1f} minutes)
**Specialists:** {cost_summary.get('total_calls', 0)}

**Cost Breakdown:**
- Analysis Cost: ${cost_summary.get('total_cost', 0):.4f}
- Evaluation Cost: ${eval_cost:.4f}
- **Total Cost: ${total_with_eval:.4f}**

**Token Usage:**
- Analysis Tokens: {cost_summary.get('total_input_tokens', 0):,} in + {cost_summary.get('total_output_tokens', 0):,} out
- Evaluation Tokens: {evaluation_tokens_in:,} in + {evaluation_tokens_out:,} out
- **Total Tokens: {cost_summary.get('total_input_tokens', 0) + evaluation_tokens_in:,} in + {cost_summary.get('total_output_tokens', 0) + evaluation_tokens_out:,} out**

---
"""

    return header


if __name__ == "__main__":
    # Simple test
    print("GPT-5 Self-Evaluator Module")
    print("Import this module and call run_self_evaluation() after analysis")
