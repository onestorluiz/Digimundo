#!/usr/bin/env python3
"""
🎯 BENCHMARK PROMPT GENERATOR - FASE 2
Gera prompts melhorados que produzem análises 10/10.

Baseado em padrões extraídos + análise crítica dos gaps.
"""

import json
from pathlib import Path
from typing import Dict, Any


class BenchmarkPromptGenerator:
    """
    Gera prompts que superam os benchmarks atuais (8/10 e 7/10),
    visando qualidade 10/10.

    Baseado em:
    - benchmark_patterns.json (padrões quantitativos)
    - ANALISE_CRITICA_BENCHMARKS.md (gaps identificados)
    """

    def __init__(self, patterns_path: Path):
        """
        Args:
            patterns_path: Caminho para benchmark_patterns.json
        """
        with open(patterns_path, 'r', encoding='utf-8') as f:
            self.patterns = json.load(f)

        self.aggregated = self.patterns['aggregated_patterns']

    def generate_10_10_prompt(
        self,
        author_type: str,
        base_prompt: str,
        screenplay_excerpt: str
    ) -> str:
        """
        Gera prompt melhorado visando qualidade 10/10.

        Args:
            author_type: Tipo de autor (mckee_dialogue, campbell, etc)
            base_prompt: Prompt original/base
            screenplay_excerpt: Trecho do roteiro a analisar

        Returns:
            Prompt melhorado com requisitos 10/10
        """

        # Carregar requisitos específicos por autor
        author_specific = self._get_author_specific_requirements(author_type)

        # Montar prompt completo
        enhanced_prompt = f"""
{self._get_quality_standards_section()}

{self._get_structure_requirements_section()}

{author_specific}

{self._get_citation_requirements_section()}

{self._get_before_after_requirements_section()}

{self._get_theoretical_connection_section(author_type)}

{self._get_final_checklist_section()}

---

YOUR TASK:

{base_prompt}

---

SCREENPLAY EXCERPT TO ANALYZE:

{screenplay_excerpt}

---

REMEMBER: Your analysis will be scored against the 10/10 checklist above.
Aim for 5,000-6,000 characters with concrete examples, specific citations,
and complete scene rewrites in your before/after examples.
"""

        return enhanced_prompt

    def _get_quality_standards_section(self) -> str:
        """Seção de padrões de qualidade baseados em benchmarks."""
        return f"""
# 🏆 QUALITY STANDARDS - TARGET: 10/10

Based on benchmark analysis, your output MUST meet these MINIMUM requirements:

## Quantitative Targets:
- **LENGTH**: 5,000-6,000 characters (~750-900 words)
  - Current benchmarks: {self.aggregated['avg_char_count']:.0f} chars (8/10)
  - You must EXCEED this by 50%+

- **PARAGRAPHS**: 8-10 well-developed paragraphs
  - Current benchmarks: {self.aggregated['avg_paragraph_count']:.1f} paragraphs
  - You must have 2-3 MORE paragraphs

- **DIRECT QUOTES**: 10-12 verbatim quotes from screenplay
  - Current benchmarks: {self.aggregated['avg_quote_count']:.1f} quotes
  - You must DOUBLE this number

- **SCENE CITATIONS**: 3-4 specific scenes cited with numbers
  - Current benchmarks: {self.aggregated['avg_scene_citations']:.1f} scenes
  - You must cite 2-3 MORE scenes

- **PAGE CITATIONS**: ALL quotes must have page numbers
  - Current benchmarks: {self.aggregated['avg_page_citations']:.1f} pages
  - You must cite pages for EVERY example

- **BEFORE/AFTER EXAMPLES**: 4-5 complete scene rewrites
  - Current benchmarks: {self.aggregated['avg_before_after_examples']:.1f} examples
  - You must have 3-4 MORE examples

- **DEPTH INDICATORS**: 15+ indicators of deep analysis
  - Current benchmarks: {self.aggregated['avg_depth_indicators']:.0f} indicators
  - You must have 50% MORE depth words
"""

    def _get_structure_requirements_section(self) -> str:
        """Seção de requisitos estruturais."""
        return """
## Structural Requirements:

Your analysis MUST have these 5 sections in this exact order:

1. **🎬 Interpretação** (2 paragraphs)
   - Analyze quantitative data + first 4-5 scenes
   - Include specific scene numbers, pages, and character names

2. **Padrões** (2 paragraphs)
   - Identify patterns across MULTIPLE scenes (not just one)
   - Quote dialogue verbatim to demonstrate patterns

3. **Problemas** (3-4 paragraphs)
   - Identify 4-5 DISTINCT problems
   - Each problem must have 2-3 examples from DIFFERENT scenes
   - Each example must cite: scene number, page number, and quote

4. **Soluções** (3-4 paragraphs)
   - For each problem, provide COMPLETE before/after scene rewrites
   - Show 5-15 lines of original scene
   - Show 8-20 lines of rewritten scene
   - Explain technical changes made

5. **Contexto** (1 paragraph)
   - Acknowledge limitations
   - Suggest next steps
"""

    def _get_citation_requirements_section(self) -> str:
        """Seção de requisitos de citação."""
        return """
## Citation Requirements:

CRITICAL: Every example you provide must include:

✅ **Scene number**: "na cena 3" or "scene 3"
✅ **Page number**: "página 5" or "p.5"
✅ **Location on page**: "terço superior", "meio da página", "final"
✅ **Line numbers when possible**: "linhas 112-118"
✅ **Verbatim quote**: Use "aspas" for exact dialogue

### Example of CORRECT citation:
"Na cena 1 (p.2, terço superior, linhas 43-45), Sofia diz:
'Julio, eu tenho medo de tentar e falhar.'"

### Example of INCORRECT citation (TOO VAGUE):
"Sofia expressa medo de falhar"

You must provide 10-12 citations following the CORRECT format.
"""

    def _get_before_after_requirements_section(self) -> str:
        """Seção de requisitos before/after."""
        return """
## Before/After Requirements:

CRITICAL: Your solutions section must include 4-5 COMPLETE scene rewrites.

Each rewrite must show:

### BEFORE (Original Scene):
```
CENA X (PÁGINA Y, LINHAS Z1-Z2):

[5-10 lines of original screenplay text, verbatim]
```

### DEPOIS (Rewritten Scene):
```
CENA X REESCRITA (NOVA VERSÃO):

[8-15 lines of improved screenplay text]
```

### MUDANÇAS TÉCNICAS:
✅ List specific improvements:
- Subtexto: [explain what changed]
- Ação: [explain what action was added]
- Conflito: [explain how conflict was intensified]
- Ritmo: [explain rhythm changes]
- Voz: [explain character voice differentiation]

### Example of COMPLETE before/after:

**ANTES - Cena 1 (p.2, linhas 43-48):**
```
INT. BAR - NOITE

Sofia e Julio bebem.

SOFIA
Julio, eu tenho medo de tentar e falhar.

JULIO
Entendo.
```

**DEPOIS - Cena 1 Reescrita:**
```
INT. BAR - NOITE

Sofia segura o drink. Não bebe. Olha pela janela.

JULIO
Saudade?

SOFIA
(evita olhar)
Não sei se...
(pausa)
Já falhei antes.

Sofia finalmente bebe. Grimace.

JULIO
E se não falhar?

SOFIA
(sarcástica)
Experiência diz o contrário.
```

**MUDANÇAS TÉCNICAS:**
✅ Subtexto: "Já falhei" ao invés de "tenho medo de falhar"
✅ Ação: Segurar drink, grimace = nervosismo sem verbalizar
✅ Conflito: Julio questiona, Sofia resiste com sarcasmo
✅ Ritmo: Pausas, interrupções = naturalidade
✅ Voz: Sofia usa frases curtas, sarcásticas = defensiva

---

You must provide 4-5 examples like this, NOT just abstract suggestions.
"""

    def _get_theoretical_connection_section(self, author_type: str) -> str:
        """Seção de conexão teórica específica por autor."""

        author_lower = author_type.lower()

        if 'mckee' in author_lower and 'dialogue' in author_lower:
            return """
## Theoretical Connection - McKee's Dialogue Theory:

CRITICAL: You must cite Robert McKee's book "Dialogue" explicitly.

Reference specific concepts:
- **Subtexto** (p.87): "characters speak in code, hiding thoughts beneath surface"
- **Conflito em Diálogo** (p.134): "characters with opposing desires"
- **Autenticidade** (p.45): "dialogue that sounds natural but isn't realistic"
- **Voz Individual** (p.102): "each character must have unique speech patterns"

For each problem you identify, cite McKee's relevant principle and show
how the screenplay violates or upholds it.

Example:
"Segundo McKee em 'Dialogue' (p.87), subtexto ocorre quando personagens
escondem sentimentos reais. No roteiro, Sofia declarando 'eu tenho medo'
na cena 1 (p.2) viola este princípio ao expor emoção diretamente."
"""

        elif 'campbell' in author_lower:
            return """
## Theoretical Connection - Campbell's Hero's Journey:

CRITICAL: You must analyze dialogue through the lens of Hero's Journey.

Map the screenplay to Campbell's stages:
1. **Ordinary World** - Where does protagonist start?
2. **Call to Adventure** - What challenge is presented?
3. **Refusal of the Call** - How does protagonist resist?
4. **Meeting with the Mentor** - Who guides them?
5. **Crossing the Threshold** - What's the point of no return?

Analyze how DIALOGUE reflects these stages:
- Does refusal sound authentic? Is resistance dramatic enough?
- Does mentor offer wisdom or just exposition?
- Do threshold guardians challenge protagonist through dialogue?

Example:
"Na cena 1 (p.2), Sofia expressa 'medo de recomeçar' - claramente na
etapa REFUSAL OF THE CALL de Campbell. Porém, a resistência é muito
branda. Campbell defende que o refusal deve ser dramático, criando
tensão real. Sugiro reescrever com conflito mais intenso."
"""

        elif 'field' in author_lower:
            return """
## Theoretical Connection - Field's Paradigm:

CRITICAL: Analyze dialogue within Field's three-act structure.

Identify:
- **Setup (Act 1)**: Does dialogue establish character voices early?
- **Confrontation (Act 2)**: Does dialogue intensity increase?
- **Resolution (Act 3)**: Does dialogue show character transformation?
- **Plot Points**: Do dialogues at plot points create turning moments?

Cite Field's "Screenplay: The Foundations of Screenwriting" when
discussing structure and pacing.
"""

        else:
            # Generic theoretical connection
            return f"""
## Theoretical Connection - {author_type.title()} Theory:

CRITICAL: You must connect your analysis to {author_type}'s specific theory.

Cite the author's book(s) and apply their principles to the screenplay.
Every problem you identify should reference a relevant concept from their work.
"""

    def _get_author_specific_requirements(self, author_type: str) -> str:
        """Requisitos específicos por tipo de autor."""

        author_lower = author_type.lower()

        if 'mckee' in author_lower:
            return """
## McKee-Specific Requirements:

Focus on:
- Dialogue authenticity vs realism
- Subtext and hidden meanings
- Character voice differentiation
- Conflict embedded in dialogue
- Exposition vs revelation through action
"""

        elif 'campbell' in author_lower:
            return """
## Campbell-Specific Requirements:

Focus on:
- Hero's Journey stages reflected in dialogue
- Character transformation arc through speech
- Mentor wisdom vs protagonist resistance
- Threshold guardians challenging protagonist
- Call to adventure and refusal dialogue patterns
"""

        elif 'field' in author_lower:
            return """
## Field-Specific Requirements:

Focus on:
- Dialogue within three-act structure
- Setup of character voices in Act 1
- Escalation of conflict in Act 2
- Resolution and transformation in Act 3
- Plot points created through dialogue
"""

        else:
            return f"## {author_type.title()}-Specific Requirements:\n\nApply {author_type}'s theory to dialogue analysis.\n"

    def _get_final_checklist_section(self) -> str:
        """Checklist final 10/10."""
        return """
---

# ✅ FINAL CHECKLIST - VERIFY BEFORE SUBMITTING:

Before you finish, verify your analysis includes:

- [ ] 5,000-6,000 characters total length
- [ ] 8-10 paragraphs
- [ ] 5 sections: Interpretação, Padrões, Problemas, Soluções, Contexto
- [ ] 10-12 verbatim dialogue quotes with "aspas"
- [ ] 3-4 scene citations with scene numbers
- [ ] ALL quotes have page numbers
- [ ] 50%+ of quotes have line numbers or position
- [ ] 4-5 complete before/after scene rewrites (not just suggestions)
- [ ] Each before/after shows 5-15 lines original + 8-20 lines rewrite
- [ ] Technical explanation for each rewrite
- [ ] 4-5 distinct problems identified
- [ ] Each problem has 2-3 examples from DIFFERENT scenes
- [ ] Cited author's book (title + page + concept)
- [ ] Applied author's specific theory to screenplay
- [ ] Analyzed character arc through dialogue
- [ ] 15+ depth indicators (porque, exemplo, especificamente, etc)

If ANY item above is unchecked, your analysis is INCOMPLETE and will score below 10/10.
"""


def main():
    """Demonstração do gerador."""

    patterns_path = Path('/Users/clubproducoes/Digimundo/claude_code/benchmark_patterns.json')

    generator = BenchmarkPromptGenerator(patterns_path)

    # Exemplo: gerar prompt para McKee Dialogue
    base_prompt = """
Analyze this screenplay excerpt focusing on dialogue quality.
Identify problems and provide solutions.
"""

    screenplay_excerpt = "[Screenplay text would go here]"

    enhanced_prompt = generator.generate_10_10_prompt(
        author_type='mckee_dialogue',
        base_prompt=base_prompt,
        screenplay_excerpt=screenplay_excerpt
    )

    print('='*80)
    print('ENHANCED PROMPT FOR 10/10 QUALITY')
    print('='*80)
    print()
    print(enhanced_prompt)
    print()
    print('='*80)
    print(f'Prompt length: {len(enhanced_prompt):,} characters')
    print('='*80)


if __name__ == '__main__':
    main()
