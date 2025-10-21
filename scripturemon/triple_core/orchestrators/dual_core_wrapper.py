"""
DualCoreWrapper - Wrapper para combinar análise Python + LLM

Arquitetura Dual-Core:
1. Python Core: Análise estrutural e dados objetivos
2. LLM Core: Insights qualitativos e contexto
3. Synthesis: Combina ambos para análise completa

Este wrapper NÃO modifica os especialistas Python existentes.
Ele adiciona uma camada LLM que enriquece os resultados Python.
"""

import json
import logging
from typing import Dict, Any, Optional, List
from pathlib import Path
import subprocess
import time
import sys

# Add core path for theory_indexer
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

logger = logging.getLogger(__name__)


class DualCoreWrapper:
    """
    Wrapper que transforma qualquer especialista Python em Dual-Core.

    Fluxo:
    1. Chama specialist.analyze() → resultado Python
    2. Formata resultado para LLM
    3. Chama LLM com contexto → insights qualitativos
    4. Sintetiza Python + LLM → resultado final

    Compatível com todos os 24 especialistas existentes.
    """

    def __init__(
        self,
        python_specialist: Any,
        llm_model: str = "scripturemon-optimized",  # Modelo otimizado!
        llm_timeout: int = 600,  # 10 minutos para deep context
        fallback_to_python: bool = True,
        use_theory: bool = True,
        deep_context: bool = False,
        specialist_type: Optional[str] = None
    ):
        """
        Inicializa Dual-Core Wrapper.

        Args:
            python_specialist: Instância do especialista Python (ex: DrDialogue)
            llm_model: Modelo Ollama a usar
            llm_timeout: Timeout em segundos para LLM
            fallback_to_python: Se True, retorna só Python quando LLM falha
            use_theory: Se True, Python busca teoria relevante (zero tokens)
            deep_context: Se True, envia livro completo ao LLM (requer 128k tokens)
            specialist_type: Tipo de especialista (auto-detect se None, ou 'all' para todos os livros)
        """
        self.python_specialist = python_specialist
        self.llm_model = llm_model
        self.llm_timeout = llm_timeout
        self.fallback_to_python = fallback_to_python
        self.use_theory = use_theory
        self.deep_context = deep_context

        # Extrair informações do especialista
        self.specialist_name = getattr(python_specialist, 'name', 'Unknown Specialist')
        self.specialist_specialty = getattr(python_specialist, 'specialty', 'Unknown')
        self.specialist_identity = getattr(python_specialist, 'identity', '')

        # Detectar tipo de especialista para mapeamento de livro (ou usar override)
        self.specialist_type = specialist_type or self._detect_specialist_type()

        # Theory Indexer (lazy loading)
        self.theory_indexer = None
        if self.use_theory:
            try:
                from core.theory_indexer import get_theory_indexer
                self.theory_indexer = get_theory_indexer(specialist_type=self.specialist_type)
                logger.info(f"📚 Theory indexer loaded: {self.theory_indexer.get_stats()['books_indexed']} books")
            except Exception as e:
                logger.warning(f"⚠️ Theory indexer failed to load: {e}")
                self.use_theory = False

        logger.info(f"DualCoreWrapper initialized for: {self.specialist_name}")

    def _detect_specialist_type(self) -> str:
        """Detecta tipo de especialista baseado no nome da classe"""
        class_name = self.python_specialist.__class__.__name__.lower()

        # Mapeamento de nomes de classe para tipos
        if 'dialogue' in class_name:
            return 'dialogue'
        elif 'psychology' in class_name or 'psychemon' in class_name:
            return 'psychemon'
        elif 'subtext' in class_name or 'submon' in class_name:
            return 'submon'
        elif 'theme' in class_name or 'thememon' in class_name:
            return 'thememon'
        elif 'arc' in class_name:
            return 'character'
        elif 'relationship' in class_name:
            return 'character'
        elif 'structure' in class_name:
            return 'structure'
        elif 'pacing' in class_name:
            return 'pacing'
        elif 'tone' in class_name:
            return 'structure'
        elif 'opening' in class_name:
            return 'opening'
        elif 'climax' in class_name:
            return 'climax'
        elif 'resolution' in class_name:
            return 'resolution'
        elif 'action' in class_name:
            return 'structure'
        elif 'symbolism' in class_name:
            return 'symbolism'
        elif 'genre' in class_name:
            return 'genre'
        elif 'originality' in class_name:
            return 'originality'
        else:
            return 'dialogue'  # Default fallback

    def analyze(self, screenplay_text: str, **kwargs) -> Dict[str, Any]:
        """
        Executa análise Dual-Core completa.

        Args:
            screenplay_text: Texto do roteiro a analisar
            **kwargs: Argumentos adicionais para specialist.analyze()

        Returns:
            Dict com resultado completo (python_analysis + llm_insights + synthesis)
        """
        result = {
            'dual_core': True,
            'specialist': self.specialist_name,
            'timestamp': time.time()
        }

        # FASE 1: PYTHON CORE - Análise estrutural
        logger.info(f"[DUAL-CORE] Phase 1: Python Analysis ({self.specialist_name})")
        try:
            python_result = self.python_specialist.analyze(screenplay_text, **kwargs)

            # Convert dataclass to dict if needed
            if hasattr(python_result, '__dataclass_fields__'):
                from dataclasses import asdict
                python_result = asdict(python_result)

            result['python_analysis'] = python_result
            result['python_success'] = True
            logger.info(f"[DUAL-CORE] Python analysis completed: {len(str(python_result))} bytes")
        except Exception as e:
            logger.error(f"[DUAL-CORE] Python analysis failed: {e}")
            result['python_analysis'] = {'error': str(e)}
            result['python_success'] = False

            # Se Python falha, não tem o que enriquecer com LLM
            if not self.fallback_to_python:
                raise
            return result

        # FASE 2: LLM CORE - Insights qualitativos
        logger.info(f"[DUAL-CORE] Phase 2: LLM Enrichment ({self.llm_model})")
        try:
            llm_prompt = self._build_llm_prompt(screenplay_text, python_result)
            llm_response = self._call_llm(llm_prompt)

            result['llm_insights'] = llm_response
            result['llm_success'] = True
            logger.info(f"[DUAL-CORE] LLM analysis completed: {len(llm_response)} bytes")
        except Exception as e:
            logger.error(f"[DUAL-CORE] LLM analysis failed: {e}")
            result['llm_insights'] = {'error': str(e)}
            result['llm_success'] = False

            # Fallback: retorna só análise Python
            if self.fallback_to_python:
                logger.warning("[DUAL-CORE] Fallback to Python-only mode")
                return result
            raise

        # FASE 3: SYNTHESIS - Combinar Python + LLM
        logger.info("[DUAL-CORE] Phase 3: Synthesis")
        result['synthesis'] = self._synthesize(python_result, llm_response)

        return result

    def _build_llm_prompt(self, screenplay_text: str, python_result: Dict) -> str:
        """
        Constrói prompt para LLM com contexto da análise Python + teoria relevante.

        ESTRATÉGIA:
        1. Python fornece dados objetivos (métricas, scores)
        2. Python busca teoria relevante (ZERO TOKENS)
        3. LLM recebe contexto completo e interpreta

        Este prompt é crítico para qualidade Dual-Core.
        LLM recebe:
        1. Identidade do especialista
        2. Dados objetivos Python
        3. TEORIA RELEVANTE (buscada por Python!)
        4. Texto do roteiro
        5. Instrução para insights qualitativos
        """
        # Formatar resultado Python de forma legível
        python_summary = self._format_python_result(python_result)

        # BUSCAR TEORIA RELEVANTE (Python, zero tokens)
        theory_context = ""
        theory_mode = "NONE"

        if self.use_theory and self.theory_indexer:
            # Extrair problemas da análise Python
            problems = python_result.get('recommendations', [])
            if not problems:
                problems = [python_result.get('diagnosis', '')]

            try:
                if self.deep_context:
                    # DEEP DIVE MODE: Enviar livro completo (128k tokens)
                    logger.info("📚 DEEP DIVE MODE: Loading full book...")

                    # Busca query baseada nos problemas
                    query = " ".join(problems[:3]) if problems else self.specialist_type

                    # Passar specialist_type para mapeamento direto (Fase 2 otimização)
                    deep_result = self.theory_indexer.get_full_book_context(
                        query=query,
                        max_books=1,
                        specialist_type=self.specialist_type
                    )

                    if deep_result and deep_result['primary_book']:
                        book = deep_result['primary_book']
                        theory_context = f"""
<documento_fonte id="livro_mckee" tipo="teoria_completa">
<metadados>
  <titulo>{book['name']}</titulo>
  <palavras>{book['word_count']:,}</palavras>
  <tokens_estimados>{deep_result['estimated_tokens']:,}</tokens_estimados>
  <relevancia>{deep_result['relevance_score']}</relevancia>
</metadados>

<secoes_chave>
"""
                        # Adicionar highlights (top chunks encontrados)
                        for i, chunk in enumerate(book.get('highlights', [])[:5], 1):
                            theory_context += f"  <secao id='{i}' contexto='{chunk['context']}' score='{chunk['score']}'>\n"
                            theory_context += f"    {chunk['text'][:200]}...\n"
                            theory_context += f"  </secao>\n"

                        theory_context += f"""
</secoes_chave>

<texto_completo>
{book['full_text']}
</texto_completo>
</documento_fonte>
"""
                        theory_mode = "DEEP (Full Book)"
                        logger.info(f"📚 Deep context loaded: {book['word_count']:,} words, ~{deep_result['estimated_tokens']:,} tokens")
                else:
                    # SHALLOW MODE: Apenas chunks (modo original)
                    theory_results = self.theory_indexer.search_for_problems(problems, limit_per_problem=2)
                    theory_context = self.theory_indexer.format_theory_context(theory_results)
                    theory_mode = "SHALLOW (Chunks)"

                    if theory_context:
                        logger.info(f"📚 Theory context added: {len(theory_context)} chars")
            except Exception as e:
                logger.warning(f"⚠️ Theory search failed: {e}")

        # Limitar tamanho do texto (primeiras 2000 palavras)
        words = screenplay_text.split()
        if len(words) > 2000:
            screenplay_excerpt = ' '.join(words[:2000]) + '\n[... excerpt continues ...]'
        else:
            screenplay_excerpt = screenplay_text

        # Construir task baseado no modo
        if self.deep_context and theory_mode == "DEEP (Full Book)":
            task_instructions = """YOUR MISSION:
Take the knowledge Python gives you and delve as deeply as possible into the theory book provided.

You are a Script Doctor - stick to DATA and FACTS. Don't invent anything.

WHAT YOU HAVE BEEN GIVEN:
1. Python Analysis: Objective metrics, scores, and problems detected in the screenplay
2. Theory Book (FULL TEXT above): The complete reference material for your specialty
3. Screenplay Text: The script being analyzed - memorize it fully

YOUR SPECIALTY: You are HUNGRY for knowledge in your area of expertise.
Don't skimp on tokens - do IN-DEPTH and REVEALING research in the book provided.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CRITICAL INSTRUCTIONS:

1. FOCUS ON THE KNOWLEDGE YOU'VE BEEN GIVEN
   - The Python analysis tells you WHAT problems exist
   - The book above contains the theory to explain WHY and HOW to fix
   - The screenplay is your patient - analyze it thoroughly

2. DO NOT REPRODUCE COPYRIGHTED MATERIAL
   - You may SUMMARIZE concepts from the book
   - You may QUOTE SHORT EXCERPTS (2-3 sentences max)
   - You may REFERENCE specific concepts by name
   - Do NOT reproduce long sections verbatim

3. STICK TO THE DOCUMENTS PROVIDED
   - Use the book text above (not your training memory)
   - When you reference theory, it should come from the material provided
   - Be helpful, but ensure accuracy to the source material

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

YOUR ANALYSIS STRUCTURE:

1. INTERPRETATION (2 detailed paragraphs):
   → First paragraph: What Python metrics reveal + connection to theory
   → Second paragraph: Overall quality assessment based on data + theory

2. PATTERNS (2 detailed paragraphs):
   → First paragraph: Recurring patterns from Python + theory analysis
   → Second paragraph: How these patterns affect screenplay effectiveness

3. PROBLEMS - Identify top 3-4 issues (1 paragraph per problem = 3-4 paragraphs):
   For EACH problem, write one substantial paragraph covering:
   → Describe the specific problem in detail
   → Explain WHY it's a problem (ground in theory from book)
   → Show WHERE it appears in the screenplay
   → Explain IMPACT on the story

4. SOLUTIONS - Fix each problem (1 paragraph per solution = 3-4 paragraphs):
   For EACH problem above, write one substantial paragraph covering:
   → Specific, actionable solution
   → Ground solution in theory from the book
   → Concrete examples of implementation
   → Expected improvement outcome

5. DEPTH & SYNTHESIS (2 detailed paragraphs):
   → First paragraph: Advanced insights about interconnections between problems
   → Second paragraph: Final professional assessment and path forward

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

RESPONSE FORMAT:
Write 12-14 SUBSTANTIAL paragraphs following the structure above (2+2+3-4+3-4+2)
Each paragraph should be detailed and thorough (5-8 sentences)
Expected output: 2500-4000 tokens
Be exhaustive and comprehensive - this is professional script analysis.
"""
        else:
            # SHALLOW MODE: Ajustar instruções baseado em specialist_type
            if self.specialist_type == 'all':
                # MODO ALL: Pedir SEÇÕES DEDICADAS POR AUTOR
                task_instructions = """TASK - COMPREHENSIVE MULTI-AUTHOR ANALYSIS:

You have been given theory context organized by MULTIPLE AUTHORS.
The context above shows "📚 DE ACORDO COM [AUTHOR]:" sections.

YOUR MISSION: Write a DEDICATED ANALYSIS SECTION for EACH AUTHOR whose theory appears above.

═══════════════════════════════════════════════════════════════
STRUCTURE - For EACH AUTHOR (McKee, Truby, Campbell, Snyder, Field, Vogler, Seger, etc):
═══════════════════════════════════════════════════════════════

Write 7 EXTENSIVE PARAGRAPHS analyzing the screenplay through THAT AUTHOR'S lens:

1. TEORIA DESTE AUTOR (1 parágrafo de 10-15 sentenças):
   → Qual é o princípio central deste autor (baseado no contexto fornecido)
   → Como este princípio se aplica ao roteiro em análise
   → Cite o conceito específico do autor
   → Explique em profundidade a teoria
   → Dê exemplos de como grandes roteiristas usam esse princípio
   → Conecte com os dados Python

2. PADRÃO IDENTIFICADO (1 parágrafo de 10-15 sentenças):
   → Que padrão no roteiro este autor ajuda a identificar
   → Por que este padrão é significativo segundo esta teoria
   → Onde este padrão aparece (liste MÚLTIPLAS cenas específicas)
   → Analise a frequência e intensidade do padrão
   → Compare com o que seria ideal segundo este autor
   → Explique as consequências dramáticas

3. PROBLEMA #1 (1 parágrafo de 10-15 sentenças):
   → Descreva problema específico segundo este autor
   → CITE CENA e PÁGINA exata do roteiro
   → CITE DIÁLOGO verbatim entre aspas
   → Explique por que é problema segundo esta teoria
   → Impacto na história
   → Impacto nos personagens
   → Impacto no público

4. SOLUÇÃO #1 (1 parágrafo de 10-15 sentenças):
   → Solução específica baseada na teoria deste autor
   → Exemplo CONCRETO de como reescrever (escreva a nova versão completa)
   → CITE número de cena onde aplicar
   → Explique PASSO A PASSO como implementar
   → Resultado esperado detalhado
   → Como isso melhora outros aspectos

5. PROBLEMA #2 (1 parágrafo de 10-15 sentenças):
   → Segundo problema identificado por este autor
   → CITE múltiplas CENAS e diálogos específicos
   → Conexão com teoria
   → Análise profunda do erro
   → Consequências se não for corrigido

6. SOLUÇÃO #2 (1 parágrafo de 10-15 sentenças):
   → Segunda solução baseada neste autor
   → Implementação específica com exemplo completo
   → Reescreva diálogo/cena inteira como deveria ser
   → Melhoria esperada em detalhes
   → Conexões com outras cenas

7. SÍNTESE (1 parágrafo de 10-15 sentenças):
   → Contribuição única deste autor para a análise
   → Como esta perspectiva complementa as outras
   → Insight final profundo
   → Recomendação estratégica geral
   → Visão de futuro do roteiro se aplicadas as correções

═══════════════════════════════════════════════════════════════

REPEAT THE 7-PARAGRAPH STRUCTURE ABOVE FOR EACH AUTHOR IN THE CONTEXT.

CRITICAL REQUIREMENTS:
- Start each author section with: "═══ ANÁLISE SEGUNDO [AUTHOR NAME] ═══"
- ALWAYS cite specific scene numbers and page numbers
- ALWAYS quote dialogue verbatim when analyzing it
- Each paragraph: 10-15 sentences MINIMUM (not maximum!)
- Total expected output: 49-105 paragraphs (if 7-15 authors × 7 paragraphs each)
- Expected total: 20,000-40,000 characters
- DO NOT STOP until you've covered ALL authors in the context above
- If context shows 5+ authors, write analysis for ALL 5+

EXAMPLE FORMAT:
═══ ANÁLISE SEGUNDO ROBERT MCKEE ═══
[7 extensive paragraphs analyzing through McKee's lens, 10-15 sentences each]

═══ ANÁLISE SEGUNDO JOHN TRUBY ═══
[7 extensive paragraphs analyzing through Truby's lens, 10-15 sentences each]

═══ ANÁLISE SEGUNDO JOSEPH CAMPBELL ═══
[7 extensive paragraphs analyzing through Campbell's lens, 10-15 sentences each]

═══ ANÁLISE SEGUNDO CHRISTOPHER VOGLER ═══
[7 extensive paragraphs analyzing through Vogler's lens, 10-15 sentences each]

═══ ANÁLISE SEGUNDO LINDA SEGER ═══
[7 extensive paragraphs analyzing through Seger's lens, 10-15 sentences each]

[etc for EVERY SINGLE author in context - do not skip any!]

BE EXHAUSTIVE. This is the most comprehensive multi-source analysis possible.
You have 128k context window - USE IT FULLY. Write long, detailed, specific analysis.
"""
            else:
                # MODO SELETIVO: Prompt original mais curto
                task_instructions = """TASK:
Based on the Python analysis data and theory above, provide qualitative insights:

1. INTERPRETATION: What do these metrics tell us about the quality?
2. PATTERNS: What patterns emerge from the data?
3. PROBLEMS: What are the most critical issues to fix?
4. SOLUTIONS: Specific actionable recommendations (citing theory when relevant)
5. CONTEXT: Any nuances the data might miss?

Focus on insights that complement the objective Python data with subjective professional judgment.
Reference McKee's theory when applicable.

RESPONSE FORMAT:
Provide clear, actionable insights in 3-5 paragraphs. Be specific and reference the data.
"""

        # FEW-SHOT EXAMPLES (Critical for quality)
        few_shot_examples = """
═══════════════════════════════════════════════════════════════
📚 EXEMPLOS DE ANÁLISE (Few-Shot Learning)
═══════════════════════════════════════════════════════════════

✅ EXEMPLO DE ANÁLISE CORRETA (SIGA ESTE FORMATO):

Cena: 12, Página: 15
Diálogo: SAMANTHA: "Mas eu estava tendo um sonho lindo..."
Contexto: Alberto acabou de acordá-la bruscamente

Análise: Esta fala revela o padrão de evasão da realidade que define
Samantha desde a cena 3. McKee estabelece no Capítulo 4 ("Character")
que "o verdadeiro caráter é revelado sob pressão" - quando confrontada
com a realidade desagradável do despertar, Samantha escolhe verbalmente
focar no sonho (passado idealizado) ao invés do presente. A estrutura
gramatical "estava tendo" (pretérito imperfeito) reforça sua permanência
no estado onírico. A escolha da palavra "lindo" (não "bom" ou "interessante")
demonstra idealização excessiva, conectando com o subtexto de sua recusa
em processar o trauma estabelecido na terapia (cena 8).

Problema: O diálogo é puramente expositivo - declara o estado emocional
diretamente sem mostrar comportamento. McKee adverte no Cap 7 contra
"on-the-nose dialogue" onde personagens "explicam seus sentimentos ao
invés de agir".

Solução Específica: Reescrever sem o diálogo expositivo. Substituir por
ação: Samantha vira o rosto para a parede, puxa o cobertor sobre a cabeça,
murmura indistinto. Alberto repete a pergunta. Samantha: "Mais cinco minutos."
Esta versão MOSTRA evasão via comportamento físico + fala indireta, ao invés
de DECLARAR o sentimento.

---

❌ EXEMPLO DE ANÁLISE INCORRETA (NÃO FAÇA ASSIM):

"O diálogo de Samantha na cena 12 poderia ser melhorado. O personagem
precisa de mais desenvolvimento emocional e a fala soa artificial. A autora
deveria trabalhar mais no subtexto e tornar as falas mais naturais.
Recomendo revisar toda a cena para criar mais tensão dramática."

[Por quê está errado: Genérico, sem citações, sem números de cena/página
específicos, sem conexão com teoria McKee, sem exemplo concreto de reescrita,
poderia aplicar-se a qualquer roteiro]

═══════════════════════════════════════════════════════════════
"""

        prompt = f"""You are {self.specialist_identity}

ROLE: {self.specialist_name}
SPECIALTY: {self.specialist_specialty}
THEORY MODE: {theory_mode}

<analise_python tipo="metricas_objetivas">
{python_summary}
</analise_python>

{theory_context if theory_context else ""}

<documento_fonte id="roteiro_analise" tipo="screenplay">
{screenplay_excerpt}
</documento_fonte>

{few_shot_examples}

{task_instructions}

<instrucoes_finais prioridade="maxima">
LEMBRE-SE (Reforço Primacy/Recency):
1. Cite EXATAMENTE do <roteiro_analise>: números de cena e diálogos verbatim
2. Conecte ao <livro_mckee>: capítulos e conceitos específicos com citações
3. EVITE análise genérica: seja específico com exemplos concretos do roteiro
4. Estruture em 12-14 parágrafos detalhados conforme formato obrigatório
5. Cada parágrafo DEVE ter: cena/página + citação + teoria + análise causal

Comece sua análise pela PRIMEIRA cena do roteiro fornecido.
</instrucoes_finais>
"""
        return prompt

    def _format_python_result(self, python_result: Dict) -> str:
        """
        Formata resultado Python para prompt LLM.

        Converte Dict Python em texto estruturado e legível.
        """
        # Serializar como JSON pretty-printed
        try:
            formatted = json.dumps(python_result, indent=2, default=str)

            # Limitar tamanho (máximo 3000 caracteres)
            if len(formatted) > 3000:
                formatted = formatted[:3000] + '\n... (truncated)'

            return formatted
        except Exception as e:
            logger.warning(f"Failed to format Python result: {e}")
            return str(python_result)[:3000]

    def _call_llm(self, prompt: str) -> str:
        """
        Chama LLM via Ollama.

        Usa subprocess para chamar ollama run com prompt via stdin.
        """
        try:
            # Chamar Ollama com prompt via stdin
            cmd = ['ollama', 'run', self.llm_model]

            logger.debug(f"Calling LLM: {' '.join(cmd)}")

            result = subprocess.run(
                cmd,
                input=prompt,
                capture_output=True,
                text=True,
                timeout=self.llm_timeout
            )

            if result.returncode != 0:
                raise Exception(f"Ollama failed: {result.stderr}")

            response = result.stdout.strip()

            # Remover linhas de controle/progress do Ollama
            lines = response.split('\n')
            clean_lines = [l for l in lines if not l.startswith('[')]
            response = '\n'.join(clean_lines).strip()

            return response

        except subprocess.TimeoutExpired:
            raise Exception(f"LLM timeout after {self.llm_timeout}s")
        except Exception as e:
            raise Exception(f"LLM call failed: {e}")

    def _synthesize(self, python_result: Dict, llm_response: str) -> Dict[str, Any]:
        """
        Sintetiza resultados Python + LLM em análise final.

        Combina:
        - Métricas objetivas Python
        - Insights qualitativos LLM
        - Recomendações combinadas
        """
        synthesis = {
            'summary': 'Dual-Core analysis combining Python metrics with LLM insights',
            'python_metrics_count': len(str(python_result)),
            'llm_insights_count': len(llm_response),
            'combined_analysis': {
                'objective_data': 'See python_analysis section',
                'qualitative_insights': llm_response[:500] + '...' if len(llm_response) > 500 else llm_response,
                'methodology': 'Python structural analysis enriched with LLM contextual understanding'
            },
            'quality_score': self._calculate_quality_score(python_result, llm_response)
        }

        return synthesis

    def _calculate_quality_score(self, python_result: Dict, llm_response: str) -> float:
        """
        Calcula score de qualidade 0.0-1.0 baseado em Python + LLM.

        Heurística simples por enquanto:
        - Python fornece dados objetivos
        - LLM fornece contexto
        - Score combinado considera ambos
        """
        # Por enquanto, score básico baseado em completude
        score = 0.5  # baseline

        # +0.3 se Python tem dados ricos
        if isinstance(python_result, dict) and len(python_result) > 5:
            score += 0.3

        # +0.2 se LLM deu resposta substancial
        if len(llm_response) > 200:
            score += 0.2

        return min(score, 1.0)

    def export_formatted(self, result: Dict[str, Any], screenplay_title: str = "Untitled",
                        format: str = "txt", auto_open: bool = False) -> Path:
        """
        Exporta resultado em formato bem formatado.

        Args:
            result: Resultado do analyze()
            screenplay_title: Título do roteiro
            format: 'txt' ou 'html'
            auto_open: Se True, abre arquivo automaticamente

        Returns:
            Path do arquivo gerado
        """
        from triple_core.exporters.formatted_exporter import FormattedExporter
        import subprocess

        exporter = FormattedExporter()

        if format.lower() == 'html':
            filepath = exporter.export_html(result, screenplay_title)
        else:
            filepath = exporter.export_txt(result, screenplay_title)

        # Auto-open se solicitado
        if auto_open:
            try:
                subprocess.run(['open', str(filepath)], check=True)
            except Exception as e:
                logger.warning(f"Could not auto-open file: {e}")

        return filepath

    def __repr__(self):
        return f"DualCoreWrapper({self.specialist_name}, {self.llm_model})"
