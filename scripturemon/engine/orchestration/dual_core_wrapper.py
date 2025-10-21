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
import re
import os

# Add core path for theory_indexer
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

# Import personalized prompts (FASE 2 - Prompts Personalizados)
from engine.prompts import (
    build_personalized_prompt_pass1,
    build_personalized_prompt_pass2
)

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
        llm_timeout: Optional[int] = None,  # None = sem timeout (necessário para deep analysis)
        fallback_to_python: bool = True,
        use_theory: bool = True,
        deep_context: bool = False,
        specialist_type: Optional[str] = None,
        two_pass_llm: bool = False,  # NOVO: Arquitetura 2 rodadas LLM (default=False para compatibilidade)
        use_personalized_prompts: bool = False  # FASE 2: Prompts específicos por autor (default=False, opt-in)
    ):
        """
        Inicializa Dual-Core Wrapper.

        Args:
            python_specialist: Instância do especialista Python (ex: DrDialogue)
            llm_model: Modelo Ollama a usar
            llm_timeout: Timeout em segundos para LLM (None = sem timeout, recomendado para deep analysis)
            fallback_to_python: Se True, retorna só Python quando LLM falha
            use_theory: Se True, Python busca teoria relevante (zero tokens)
            deep_context: Se True, envia livro completo ao LLM (requer 128k tokens e sem timeout)
            specialist_type: Tipo de especialista (auto-detect se None, ou 'all' para todos os livros)
            two_pass_llm: Se True, usa 2 rodadas LLM (1: identificar problemas, 2: expandir soluções)
                          DEFAULT: False (mantém comportamento original single-pass para compatibilidade)
            use_personalized_prompts: Se True, usa prompts personalizados por autor (FASE 2: Prompts Personalizados)
                                      DEFAULT: False (opt-in, mantém compatibilidade com sistema antigo)
        """
        self.python_specialist = python_specialist
        self.llm_model = llm_model
        self.llm_timeout = llm_timeout
        self.fallback_to_python = fallback_to_python
        self.use_theory = use_theory
        self.deep_context = deep_context
        self.two_pass_llm = two_pass_llm
        self.use_personalized_prompts = use_personalized_prompts

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
                from engine.indexer.theory_indexer import get_theory_indexer
                # Force reload se specialist_type foi especificado manualmente (para análises por autor)
                force_reload = specialist_type is not None
                self.theory_indexer = get_theory_indexer(
                    specialist_type=self.specialist_type,
                    force_reload=force_reload
                )
                logger.info(f"📚 Theory indexer loaded: {self.theory_indexer.get_stats()['books_indexed']} books")
            except Exception as e:
                logger.warning(f"⚠️ Theory indexer failed to load: {e}")
                self.use_theory = False

        # NER Validation (lazy loading)
        self._nlp = None
        self._nlp_available = None
        self.enable_validation = os.getenv('ENABLE_NER_VALIDATION', 'true').lower() == 'true'

        logger.info(f"DualCoreWrapper initialized for: {self.specialist_name}")
        if self.enable_validation:
            logger.info("🔍 NER validation enabled")

    @property
    def nlp(self):
        """Lazy load spaCy model with caching"""
        if self._nlp is None:
            try:
                import spacy
                logger.info("Loading spaCy pt_core_news_lg...")
                self._nlp = spacy.load(
                    "pt_core_news_lg",
                    disable=["parser", "lemmatizer"]  # NER only, save memory
                )
                logger.info("✅ spaCy model loaded successfully")
            except ImportError:
                logger.warning("spaCy not installed. NER validation disabled.")
                self._nlp_available = False
                raise
            except OSError as e:
                logger.error(f"spaCy model not found: {e}")
                logger.info("Install with: python -m spacy download pt_core_news_lg")
                self._nlp_available = False
                raise
        return self._nlp

    def _extract_entities_safe(self, screenplay_text: str, max_chars: int = 150000) -> set:
        """
        Extrai entidades PERSON do roteiro com error handling robusto.

        Args:
            screenplay_text: Texto do roteiro completo
            max_chars: Máximo de caracteres a processar (default: ~50 páginas)

        Returns:
            Set de nomes de personagens em UPPERCASE
        """
        try:
            # Trunca para primeiras N páginas
            sample = screenplay_text[:max_chars]

            entities = set()

            # MÉTODO 1: Regex para nomes em formato de roteiro
            import re

            # Padrão 1A: Linha com NOME_UPPERCASE sozinho (antes de diálogo)
            character_line_pattern = re.compile(r'^\s*([A-ZÁÀÂÃÉÈÊÍÏÓÔÕÖÚÇÑ][A-ZÁÀÂÃÉÈÊÍÏÓÔÕÖÚÇÑ\s]{1,30})$', re.MULTILINE)
            matches = character_line_pattern.findall(sample)
            for match in matches:
                name = match.strip()
                # Filtrar falsos positivos (locações, termos estruturais)
                if name not in ('INT', 'EXT', 'DIA', 'NOITE', 'MANHÃ', 'TARDE', 'FADE', 'CUT', 'DISSOLVE', 'APARTAMENTO', 'CASA', 'RUA'):
                    if len(name) >= 3 and len(name) <= 30:  # Nome razoável
                        entities.add(name)

            # Padrão 1B: Nomes UPPERCASE dentro do texto (ex: "a MARIA está aqui")
            # Palavras em UPPERCASE que parecem nomes (2-3 palavras max)
            names_in_text_pattern = re.compile(r'\b([A-ZÁÀÂÃÉÈÊÍÏÓÔÕÖÚÇÑ]{3,15}(?:\s+[A-ZÁÀÂÃÉÈÊÍÏÓÔÕÖÚÇÑ]{3,15}){0,2})\b')
            matches = names_in_text_pattern.findall(sample)
            for match in matches:
                name = match.strip()
                # Filtrar termos estruturais e palavras comuns
                structural_terms = {
                    'INT', 'EXT', 'DIA', 'NOITE', 'MANHÃ', 'TARDE', 'ANOITECER',
                    'FADE', 'CUT', 'DISSOLVE', 'SMASH', 'JUMP', 'MATCH',
                    'APARTAMENTO', 'CASA', 'RUA', 'COZINHA', 'QUARTO', 'SALA',
                    'ESTÁ', 'SÃO', 'FOI', 'SERÁ', 'TEM', 'HÁ',
                    'ONDE', 'QUANDO', 'COMO', 'PORQUE', 'PORQUÊ'
                }
                if name not in structural_terms and len(name) >= 3 and len(name) <= 30:
                    # Se tem 3+ caracteres e não é termo estrutural, provavelmente é nome
                    entities.add(name)

            # MÉTODO 2: spaCy NER para nomes em formato normal
            for doc in self.nlp.pipe([sample], batch_size=10000):
                for ent in doc.ents:
                    if ent.label_ == "PER" and len(ent.text) > 2:
                        # Normaliza: UPPERCASE, strip
                        name = ent.text.strip().upper()
                        entities.add(name)

            return entities

        except MemoryError:
            logger.error(f"OOM while processing {len(screenplay_text)} chars")
            if max_chars > 50000:
                # Retry com metade
                logger.info(f"Retrying with {max_chars//2} chars")
                return self._extract_entities_safe(screenplay_text, max_chars // 2)
            raise

        except UnicodeDecodeError:
            logger.warning("Encoding error. Cleaning text.")
            # Limpa encoding e retry
            clean_text = screenplay_text.encode('utf-8', errors='ignore').decode('utf-8')
            return self._extract_entities_safe(clean_text, max_chars)

        except Exception as e:
            logger.error(f"Unexpected error in entity extraction: {e}")
            raise

    def _extract_llm_characters(self, llm_insights: str) -> set:
        """
        Extrai personagens mencionados na análise LLM.

        Args:
            llm_insights: Texto da análise gerada pelo LLM

        Returns:
            Set de nomes em UPPERCASE
        """
        try:
            entities = set()

            # MÉTODO 1: spaCy NER (pega nomes em formato normal: "João", "Maria")
            for doc in self.nlp.pipe([llm_insights[:50000]], batch_size=10000):
                for ent in doc.ents:
                    if ent.label_ == "PER" and len(ent.text) > 2:
                        name = ent.text.strip().upper()
                        entities.add(name)

            # MÉTODO 2: Regex para UPPERCASE (caso LLM use formato roteiro)
            import re
            uppercase_names = re.compile(r'\b([A-ZÁÀÂÃÉÈÊÍÏÓÔÕÖÚÇÑ]{3,15}(?:\s+[A-ZÁÀÂÃÉÈÊÍÏÓÔÕÖÚÇÑ]{3,15}){0,2})\b')
            matches = uppercase_names.findall(llm_insights[:50000])

            # Filtrar termos que não são nomes
            structural_terms = {
                'INT', 'EXT', 'DIA', 'NOITE', 'MANHÃ', 'TARDE',
                'FADE', 'CUT', 'DISSOLVE', 'SMASH',
                'APARTAMENTO', 'CASA', 'RUA', 'COZINHA', 'QUARTO',
                'ESTÁ', 'SÃO', 'FOI', 'SERÁ', 'TEM', 'HÁ',
                'ONDE', 'QUANDO', 'COMO', 'PORQUE', 'ACT', 'SCENE',
                'TODO', 'TODOS', 'TODAS', 'TUDO', 'NADA', 'ALGO',
                'MUITO', 'POUCO', 'MAIS', 'MENOS', 'BEM', 'MAL'
            }

            for match in matches:
                name = match.strip()
                if name not in structural_terms and len(name) >= 3:
                    entities.add(name)

            return entities

        except Exception as e:
            logger.error(f"Error extracting LLM characters: {e}")
            return set()

    def _validate_character_names(
        self,
        llm_insights: str,
        screenplay_text: str
    ) -> Dict[str, Any]:
        """
        Valida nomes de personagens do LLM contra NER do roteiro.

        Args:
            llm_insights: Texto da análise LLM
            screenplay_text: Texto completo do roteiro

        Returns:
            Dict com validação: {valid, overlap_ratio, hallucinated, ...}
        """

        # Check se validação habilitada
        if not self.enable_validation:
            return {'valid': True, 'warning': 'Validation disabled'}

        try:
            # Check se spaCy disponível
            if self._nlp_available is False:
                return {'valid': True, 'warning': 'spaCy not available'}

            # Extrai entidades do roteiro (ground truth)
            try:
                screenplay_entities = self._extract_entities_safe(screenplay_text)
            except Exception as e:
                logger.error(f"Entity extraction failed: {e}")
                return {'valid': True, 'warning': f'Extraction failed: {type(e).__name__}'}

            # Se nenhuma entidade encontrada
            if not screenplay_entities:
                logger.warning("No entities found in screenplay")
                return {
                    'valid': True,
                    'warning': 'No entities in screenplay',
                    'screenplay_entities': 0
                }

            # Extrai personagens da resposta LLM
            llm_entities = self._extract_llm_characters(llm_insights)

            if not llm_entities:
                return {
                    'valid': True,
                    'warning': 'No characters in LLM result',
                    'screenplay_entities': len(screenplay_entities)
                }

            # Filtrar referências teóricas (nomes de autores)
            theoretical_names = {
                'MCKEE', 'FIELD', 'TRUBY', 'CAMPBELL', 'VOGLER', 'SEGER',
                'SNYDER', 'EGRI', 'WEILAND', 'ARISTOTLE', 'COWGILL',
                'ARISTOTELES', 'JOHN', 'ROBERT', 'CHRISTOPHER', 'SYD',
                'BLAKE', 'LAJOS', 'JOSEPH', 'CHRIS', 'LINDA'
            }
            llm_entities = llm_entities - theoretical_names

            if not llm_entities:
                return {
                    'valid': True,
                    'warning': 'Only theoretical references found',
                    'screenplay_entities': len(screenplay_entities)
                }

            # Calcula overlap
            intersection = llm_entities.intersection(screenplay_entities)
            overlap_ratio = len(intersection) / len(llm_entities) if llm_entities else 0

            # Identifica possíveis alucinações
            hallucinated = llm_entities - screenplay_entities

            # Threshold: 50% overlap mínimo
            is_valid = overlap_ratio >= 0.5

            return {
                'valid': is_valid,
                'overlap_ratio': overlap_ratio,
                'screenplay_entities': len(screenplay_entities),
                'llm_entities': len(llm_entities),
                'matched': list(intersection),
                'hallucinated': list(hallucinated),
                'risk_level': 'LOW' if is_valid else 'HIGH'
            }

        except Exception as e:
            # Catch-all: nunca deixe validação quebrar análise
            logger.exception(f"Unexpected error in validation: {e}")
            return {
                'valid': True,
                'warning': f'Validation exception: {type(e).__name__}'
            }

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
            if self.two_pass_llm:
                # TWO-PASS ARCHITECTURE: Separate problem identification from solution expansion
                logger.info("[DUAL-CORE] 🔄 TWO-PASS LLM MODE ENABLED")

                # PASS 1: Identify problems (WHAT is wrong)
                logger.info("[DUAL-CORE] 🎯 Pass 1/2: Identifying problems...")
                pass1_prompt = self._build_llm_prompt_pass1(screenplay_text, python_result)
                pass1_response = self._call_llm(pass1_prompt)
                logger.info(f"[DUAL-CORE] ✅ Pass 1 complete: {len(pass1_response)} chars")

                # PASS 2: Expand solutions (HOW to fix with concrete examples)
                logger.info("[DUAL-CORE] 🎯 Pass 2/2: Expanding solutions with examples...")
                pass2_prompt = self._build_llm_prompt_pass2(screenplay_text, python_result, pass1_response)
                pass2_response = self._call_llm(pass2_prompt)
                logger.info(f"[DUAL-CORE] ✅ Pass 2 complete: {len(pass2_response)} chars")

                # Combine both passes
                llm_response = self._combine_two_pass_responses(pass1_response, pass2_response)
                logger.info(f"[DUAL-CORE] 🎉 Combined response: {len(llm_response)} chars")
            else:
                # SINGLE-PASS MODE (original)
                llm_prompt = self._build_llm_prompt(screenplay_text, python_result)
                llm_response = self._call_llm(llm_prompt)

            # VALIDATE QUALITY
            quality_check = self._validate_llm_output(llm_response)
            if not quality_check['valid']:
                logger.warning(f"[DUAL-CORE] ⚠️ LLM output quality warning: {quality_check['reason']}")
                if not self.fallback_to_python:
                    raise Exception(f"LLM output quality too low: {quality_check['reason']}")

            # ADDITIONAL VALIDATION: If using personalized prompts, validate against nivel 10 criteria
            if self.use_personalized_prompts and self.specialist_type:
                passed, nivel_score, issues = self._validate_analysis_quality(llm_response, self.specialist_type)
                logger.info(f"[DUAL-CORE] 📊 NIVEL 10 VALIDATION: {nivel_score:.1f}/10 - {'✅ PASSED' if passed else '❌ FAILED'}")
                for issue in issues:
                    logger.info(f"[DUAL-CORE]   {issue}")

                # Store nivel 10 validation results
                result['nivel_10_validation'] = {
                    'passed': passed,
                    'score': nivel_score,
                    'issues': issues
                }

                # If failed and not in fallback mode, warn
                if not passed and not self.fallback_to_python:
                    logger.warning(f"[DUAL-CORE] ⚠️ Analysis did not meet nivel 10 criteria (score: {nivel_score:.1f}/10)")

            result['llm_insights'] = llm_response
            result['llm_success'] = True
            result['quality_score'] = quality_check['score']
            logger.info(f"[DUAL-CORE] LLM analysis completed: {len(llm_response)} chars, quality: {quality_check['score']:.1f}/10")

            # FASE 2.5: NER VALIDATION - Validar personagens mencionados
            logger.info("[DUAL-CORE] Phase 2.5: NER Validation")
            try:
                validation_result = self._validate_character_names(
                    llm_insights=llm_response,
                    screenplay_text=screenplay_text
                )
                result['validation'] = validation_result

                # Log se validação detectou problemas (non-blocking)
                if not validation_result.get('valid'):
                    logger.warning(
                        f"[DUAL-CORE] ⚠️ NER validation concern: "
                        f"overlap={validation_result.get('overlap_ratio', 0):.1%}, "
                        f"hallucinated={validation_result.get('hallucinated', [])}"
                    )
                else:
                    logger.info(
                        f"[DUAL-CORE] ✅ NER validation passed: "
                        f"overlap={validation_result.get('overlap_ratio', 1):.1%}, "
                        f"matched={len(validation_result.get('matched', []))} characters"
                    )
            except Exception as e:
                logger.error(f"[DUAL-CORE] NER validation failed (non-blocking): {e}")
                result['validation'] = {'valid': True, 'warning': 'Validation error', 'error': str(e)}

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
        book_id = self.specialist_type or "theory_book"  # Para referência dinâmica no prompt

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
<documento_fonte id="livro_{book_id}" tipo="teoria_completa" autor="{self.specialist_type}">
<metadados>
  <titulo>{book['name']}</titulo>
  <autor_specialist_type>{self.specialist_type}</autor_specialist_type>
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

        # Limitar tamanho do texto (REMOVIDO LIMITE NO MODO DEEP_CONTEXT!)
        words = screenplay_text.split()

        # CRÍTICO: No modo deep_context, enviar ROTEIRO COMPLETO (não truncar)
        if self.deep_context:
            screenplay_excerpt = screenplay_text  # FULL TEXT, sem truncamento
            logger.info(f"[DEEP_CONTEXT] Sending FULL screenplay: {len(words)} words")
        elif len(words) > 10000:
            # Modo normal: limite aumentado para 10k palavras (era 2k)
            screenplay_excerpt = ' '.join(words[:10000]) + '\n[... excerpt continues ...]'
            logger.warning(f"[SHALLOW] Screenplay truncated: {len(words)} → 10000 words")
        else:
            screenplay_excerpt = screenplay_text
            logger.info(f"[SHALLOW] Sending screenplay: {len(words)} words")

        # Construir task baseado no modo
        if self.deep_context and theory_mode == "DEEP (Full Book)":
            task_instructions = """🎬 YOU ARE A SCRIPT DOCTOR ANALYZING A REAL SCREENPLAY

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🚨 CRITICAL: THIS IS A REAL SCREENPLAY ANALYSIS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

YOUR PATIENT:
The screenplay provided below in <documento_fonte id="roteiro_analise"> is THE ACTUAL SCREENPLAY you are analyzing.
This is NOT a hypothetical exercise. This is NOT a generic example.
You are a Script Doctor examining THIS SPECIFIC SCREENPLAY.

WHAT YOU HAVE:
1. 📊 Python Analysis: Objective problems found in THIS screenplay
2. 📚 Theory Book: Complete reference material (full text above)
3. 📄 THE SCREENPLAY: The actual script text below - READ IT COMPLETELY

YOUR MISSION:
Analyze THIS SPECIFIC SCREENPLAY using the theory provided.
Quote THE ACTUAL CHARACTERS, THE ACTUAL SCENES, THE ACTUAL DIALOGUE from the screenplay below.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⛔ ABSOLUTE PROHIBITIONS - DO NOT DO THESE THINGS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

❌ DO NOT invent character names (like "JOHN", "MARY", "SARAH", "LUCAS", "ANA")
❌ DO NOT create hypothetical scenes (like "Scene 14, page 28")
❌ DO NOT write "BEFORE/AFTER" examples with made-up dialogue
❌ DO NOT give generic advice that could apply to any screenplay
❌ DO NOT say "I don't have access to the screenplay" - IT IS PROVIDED BELOW!
❌ DO NOT fabricate information not present in the documents
❌ IF information is missing, explicitly state: "Not present in the provided screenplay"

✅ YOU MUST:
✅ Read the COMPLETE screenplay provided in <documento_fonte id="roteiro_analise">
✅ Identify the REAL character names from the screenplay
✅ Quote ACTUAL dialogue lines from the screenplay (with quotation marks)
✅ Cite ACTUAL scene numbers and page references from the screenplay
✅ If the screenplay doesn't have scene numbers, describe SPECIFIC MOMENTS you can identify

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📚 ACADEMIC GROUNDING & CITATIONS (MANDATORY):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

For EVERY theoretical point you make, you MUST:

1. **CITE EXACT PHRASES from the theory book** (in quotation marks):
   ❌ WRONG: "McKee diz que diálogo deve ter subtexto"
   ✅ RIGHT: "McKee afirma: 'True character is revealed in the choices a human being makes under pressure'"

2. **Include FULL BOOK REFERENCE**:
   - Author name
   - Full book title (in quotes or italics)
   - Chapter number and name
   - Page number if available

3. **Mention RESEARCH/STUDIES from the book**:
   - If the author cites research, mention it
   - If the author references other theorists, cite them
   - Academic grounding strengthens your analysis

EXAMPLE OF PROPER CITATION (in Portuguese):
"Segundo Robert McKee, em 'Story: Substance, Structure, Style and the Principles of Screenwriting',
Capítulo 17 (Composição de Cena), o autor afirma: '[EXACT QUOTE from book]'. Esta teoria é
corroborada pelo estudo de [research mentioned in the book, if any]."

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 YOUR ANALYSIS STRUCTURE (MANDATORY):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Write your analysis in PORTUGUESE, following this structure:

1. INTERPRETAÇÃO (2 paragraphs):
   → Paragraph 1: What Python metrics reveal about THIS screenplay + theory connection
   → Paragraph 2: Overall quality assessment of THIS specific story

2. PADRÕES (2 paragraphs):
   → Paragraph 1: Recurring patterns YOU FOUND in THIS screenplay
   → Paragraph 2: Impact of these patterns on THIS story's effectiveness

3. PROBLEMAS (3-4 problems - ONE paragraph PER problem):

   For EACH problem, write ONE SUBSTANTIAL paragraph covering:

   PROBLEMA [N]: [Problem name] (X occorrências no roteiro)
   → Description: What you found in THIS screenplay specifically
   → Impact: How it affects THIS story
   → Locations: WHERE in the screenplay (cite actual moments/pages you can identify)
   → Quote: ACTUAL dialogue or moment from the screenplay (in "quotation marks")
   → Theory: Book + Chapter + EXACT QUOTE from the book (in quotation marks) explaining WHY this is a problem
   → Research: Studies or research mentioned in the book that support this analysis

   EXAMPLE OF CORRECT FORMAT (in Portuguese):
   "PROBLEMA 1: Exposição emocional direta

   No roteiro fornecido, identifiquei múltiplos momentos onde [REAL CHARACTER NAME from the screenplay]
   declara sentimentos explicitamente. Por exemplo, na página [ACTUAL PAGE], [REAL CHARACTER] diz:
   '[ACTUAL QUOTE FROM THE SCREENPLAY]'. Este padrão se repete quando [ANOTHER REAL MOMENT].

   Segundo [AUTHOR from theory book], em '[Full Book Title]', Capítulo [X] ([Chapter Name]), afirma:
   "[EXACT QUOTE FROM THE THEORY BOOK - cite the actual sentence/phrase from the book]".

   O autor também menciona [relevant research/study from the book, if any].

   O impacto é que [specific impact on THIS story with THESE real characters]."

4. SOLUÇÕES (3-4 solutions - ONE paragraph PER solution):

   For EACH problem, write ONE SUBSTANTIAL paragraph:
   → Specific solution for THIS screenplay
   → Theory foundation (book + chapter)
   → Concrete example: Rewrite ACTUAL moment from THIS screenplay
   → Expected result for THIS story

   EXAMPLE OF CORRECT FORMAT (in Portuguese):
   "SOLUÇÃO PARA PROBLEMA 1:

   Para corrigir a exposição direta de [REAL CHARACTER from screenplay], reescrever o momento
   na página [ACTUAL PAGE] onde [he/she] atualmente diz '[ACTUAL QUOTE]'.

   Segundo [AUTHOR], Capítulo [X], [theory principle].

   ANTES (do roteiro atual):
   [ACTUAL line from the screenplay you're analyzing with REAL CHARACTER NAME]

   DEPOIS (sugestão):
   [Your rewrite using THE SAME REAL CHARACTERS from the screenplay]

   Resultado esperado: [Impact on THIS specific story]"

5. PROFUNDIDADE & SÍNTESE (2 paragraphs):
   → Paragraph 1: Advanced insights about problem interconnections in THIS screenplay
   → Paragraph 2: Professional assessment and path forward for THIS specific story

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📏 LENGTH REQUIREMENTS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️  MINIMUM: 10,000 characters (in Portuguese)
🎯 TARGET: 12,000-15,000 characters
📊 This equals: 4000-6000 tokens in Portuguese

Each section:
- INTERPRETAÇÃO: 2 paragraphs × 150-200 words each
- PADRÕES: 2 paragraphs × 150-200 words each
- PROBLEMAS: 3-4 paragraphs × 200-250 words each (WITH ACTUAL QUOTES)
- SOLUÇÕES: 3-4 paragraphs × 200-250 words each (WITH ACTUAL REWRITES using REAL CHARACTERS)
- PROFUNDIDADE & SÍNTESE: 2 paragraphs × 150-200 words each
  - Mention author's book full title in final paragraph
  - Be EXHAUSTIVE and FORENSIC - write as if charging $500/hour for script consulting
  - Never be brief or summary-style - expand every point with deep analysis

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📚 CITATION REQUIREMENTS (CRITICAL):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️  You have the COMPLETE theory book above. You MUST:
1. Quote EXACT SENTENCES from the book (between quotation marks)
2. Cite chapter numbers and names
3. Mention any research/studies the author references
4. Include full book title when citing the author
5. Do NOT paraphrase - use ACTUAL QUOTES from the book!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🌍 LANGUAGE: Write your entire response in PORTUGUESE (PT-BR)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        else:
            # SHALLOW MODE: Ajustar instruções baseado em specialist_type
            if self.specialist_type == 'all':
                # MODO ALL: Pedir SEÇÕES DEDICADAS POR AUTOR
                task_instructions = """COMPREHENSIVE MULTI-AUTHOR ANALYSIS TASK:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🚨 CRITICAL: THIS IS A REAL SCREENPLAY ANALYSIS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⛔ ABSOLUTE PROHIBITIONS:
❌ DO NOT invent character names (like "JOHN", "MARY", "SARAH", "LUCAS")
❌ DO NOT create hypothetical scenes
❌ DO NOT write generic examples that could apply to any screenplay
❌ DO NOT say "I don't have access to the screenplay" - IT IS PROVIDED!
❌ DO NOT fabricate information not present in the documents
❌ IF information is missing, explicitly state: "Not present in the provided screenplay"

✅ MANDATORY REQUIREMENTS:
✅ Read the ACTUAL screenplay provided in <documento_fonte id="roteiro_analise">
✅ Use REAL character names from THIS SPECIFIC SCREENPLAY
✅ Quote ACTUAL dialogue lines from THIS SCREENPLAY (with quotation marks)
✅ Cite ACTUAL scene numbers and page references from THIS SCREENPLAY
✅ Write ANTES/DEPOIS examples using REAL CHARACTER NAMES (not made-up names)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CONTEXT PROVIDED:
You have been given theory context organized by MULTIPLE AUTHORS.
The context above shows "📚 DE ACORDO COM [AUTHOR]:" sections.

YOUR MISSION:
Write a DEDICATED ANALYSIS SECTION for EACH AUTHOR whose theory appears above.
Analyze THIS SPECIFIC SCREENPLAY through each author's lens using REAL CHARACTER NAMES.

═══════════════════════════════════════════════════════════════
STRUCTURE - For EACH AUTHOR (McKee, Truby, Campbell, Snyder, Field, Vogler, Seger, etc):
═══════════════════════════════════════════════════════════════

Write 7 EXTENSIVE PARAGRAPHS analyzing THIS SPECIFIC SCREENPLAY through THAT AUTHOR'S lens:

1. TEORIA DESTE AUTOR (1 parágrafo de 10-15 sentenças):
   → Qual é o princípio central deste autor (baseado no contexto fornecido)
   → Como este princípio se aplica ao roteiro em análise
   → Cite o conceito específico do autor
   → Explique em profundidade a teoria
   → Dê exemplos de como grandes roteiristas usam esse princípio
   → Conecte com os dados Python

2. PADRÃO IDENTIFICADO (1 parágrafo de 10-15 sentenças):
   → Que padrão no ROTEIRO FORNECIDO este autor ajuda a identificar
   → Por que este padrão é significativo segundo esta teoria
   → Onde este padrão aparece (liste MÚLTIPLAS cenas REAIS com números/páginas REAIS)
   → Use NOMES DE PERSONAGENS REAIS do roteiro fornecido
   → Analise a frequência e intensidade do padrão
   → Compare com o que seria ideal segundo este autor
   → Explique as consequências dramáticas para ESTA HISTÓRIA ESPECÍFICA

3. PROBLEMA #1 (1 parágrafo de 10-15 sentenças):
   → Descreva problema específico encontrado NESTE ROTEIRO FORNECIDO segundo este autor
   → CITE CENA e PÁGINA exata do ROTEIRO FORNECIDO
   → CITE DIÁLOGO REAL verbatim entre aspas usando NOMES DE PERSONAGENS REAIS
   → Explique por que é problema segundo esta teoria
   → Impacto na HISTÓRIA DESTE ROTEIRO
   → Impacto nos PERSONAGENS REAIS deste roteiro
   → Impacto no público desta história específica

4. SOLUÇÃO #1 (1 parágrafo de 10-15 sentenças):
   → Solução específica baseada na teoria deste autor para ESTE ROTEIRO
   → Exemplo CONCRETO de como reescrever usando PERSONAGENS REAIS (escreva a nova versão completa)
   → CITE número de cena REAL onde aplicar
   → Explique PASSO A PASSO como implementar NESTA HISTÓRIA
   → Resultado esperado detalhado para ESTA HISTÓRIA
   → Como isso melhora outros aspectos DESTA HISTÓRIA

5. PROBLEMA #2 (1 parágrafo de 10-15 sentenças):
   → Segundo problema identificado por este autor NESTE ROTEIRO FORNECIDO
   → CITE múltiplas CENAS REAIS e diálogos REAIS específicos com PERSONAGENS REAIS
   → Conexão com teoria
   → Análise profunda do erro NESTA HISTÓRIA
   → Consequências se não for corrigido NESTA HISTÓRIA

6. SOLUÇÃO #2 (1 parágrafo de 10-15 sentenças):
   → Segunda solução baseada neste autor para ESTE ROTEIRO
   → Implementação específica com exemplo completo usando PERSONAGENS REAIS
   → Reescreva diálogo/cena inteira como deveria ser usando NOMES REAIS
   → Melhoria esperada em detalhes para ESTA HISTÓRIA
   → Conexões com outras cenas REAIS deste roteiro

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
- ALWAYS cite specific scene numbers and page numbers from THE ACTUAL SCREENPLAY
- ALWAYS quote dialogue verbatim from THE ACTUAL SCREENPLAY when analyzing it
- USE REAL CHARACTER NAMES from the screenplay (not invented names!)
- Each paragraph: 10-15 sentences MINIMUM (not maximum!)
- Total expected output: 49-105 paragraphs (if 7-15 authors × 7 paragraphs each)
- Expected total: 20,000-40,000 characters
- DO NOT STOP until you've covered ALL authors in the context above
- If context shows 5+ authors, write analysis for ALL 5+

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🌍 LANGUAGE: Write your entire response in PORTUGUESE (PT-BR)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

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
                # MODO SELETIVO: Prompt APROFUNDADO com foco em problemas específicos
                task_instructions = """DEEP ANALYSIS OF SPECIFIC PROBLEMS - TASK:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🚨 CRITICAL: THIS IS A REAL SCREENPLAY ANALYSIS - NOT A HYPOTHETICAL EXERCISE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

The Python analysis has identified SPECIFIC problems in THIS SPECIFIC SCREENPLAY.
Your job is to DIVE DEEP into those exact problems using the theory provided.

⛔ ABSOLUTE PROHIBITIONS - DO NOT DO THESE THINGS:
❌ DO NOT invent character names (like "JOHN", "LUCY", "MARK", "SARAH", "ANA", "LUCAS")
❌ DO NOT create hypothetical scenes that don't exist
❌ DO NOT invent scene numbers or page numbers
❌ DO NOT make generic analysis that could apply to any screenplay
❌ DO NOT give McKee-style generic examples with made-up names
❌ DO NOT say "I don't have access to the screenplay" - IT IS PROVIDED BELOW!
❌ DO NOT fabricate information not present in the documents
❌ IF information is missing, explicitly state: "Not present in the provided screenplay"

✅ MANDATORY REQUIREMENTS:
✅ READ the COMPLETE <documento_fonte id="roteiro_analise"> provided below
✅ IDENTIFY the REAL character names from THIS SPECIFIC SCREENPLAY
✅ CITE ACTUAL dialogue lines with "quotation marks" from THIS SCREENPLAY
✅ CITE ACTUAL scene/page numbers from THIS SCREENPLAY
✅ USE the theory context to explain WHY those SPECIFIC moments are problems
✅ Write ANTES/DEPOIS examples using the REAL CHARACTER NAMES from the screenplay

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

YOUR ANALYSIS STRUCTURE (12-14 SUBSTANTIAL PARAGRAPHS - write in PORTUGUESE):

1. INTERPRETAÇÃO (2 paragraphs):
   → What the Python metrics reveal about THIS specific screenplay
   → Connect to theory: WHY these metrics matter (cite author from theory context)

2. PADRÕES (2 paragraphs):
   → Recurring patterns identified by Python in THIS screenplay
   → How these patterns affect THIS story's effectiveness

3. PROBLEMAS (3-4 paragraphs - ONE PER PROBLEM):
   For EACH problem Python detected, write ONE paragraph:

   → NAME the specific problem (from Python analysis)
   → CITE where it appears in THE ACTUAL SCREENPLAY: "Na Cena X, página Y, [REAL CHARACTER] diz: 'actual dialogue'"
   → EXPLAIN why it's a problem using theory from context above
   → ANALYZE impact on THIS story specifically with THESE real characters

4. SOLUÇÕES (3-4 paragraphs - ONE PER PROBLEM):
   For EACH problem, write ONE paragraph with specific solution:

   → Actionable solution grounded in theory
   → REWRITE the actual problematic dialogue/moment using REAL CHARACTER NAMES
   → Explain HOW this fixes the issue
   → Expected improvement for THIS specific story

5. PROFUNDIDADE & SÍNTESE (2 paragraphs):
   → How problems interconnect in THIS screenplay
   → Professional assessment and path forward for THIS specific story

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

RESPONSE FORMAT:
- 12-14 SUBSTANTIAL paragraphs (2+2+3-4+3-4+2)
- Each paragraph: 8-12 sentences (LONGER than before!)
- Expected output: 3500-5000 tokens (MORE than before!)
- MANDATORY: Quote actual dialogue from THE SCREENPLAY, cite actual scenes with REAL CHARACTER NAMES
- MANDATORY: Reference the author from theory context (McKee, Truby, Field, etc)

This is FORENSIC script analysis. Be exhaustive, specific, and deeply analytical.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🌍 LANGUAGE: Write your entire response in PORTUGUESE (PT-BR)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

        # FEW-SHOT EXAMPLES (Critical for quality) - GENÉRICOS para funcionar com qualquer autor
        author_name = self.specialist_type.upper() if self.specialist_type else "THEORY"
        few_shot_examples = f"""
═══════════════════════════════════════════════════════════════
📚 EXEMPLOS DE ANÁLISE (Few-Shot Learning)
═══════════════════════════════════════════════════════════════

✅ EXEMPLO DE ANÁLISE CORRETA (SIGA ESTE FORMATO):

Cena: 12, Página: 15
Diálogo: SAMANTHA: "Mas eu estava tendo um sonho lindo..."
Contexto: Alberto acabou de acordá-la bruscamente

Análise: Esta fala revela o padrão de evasão da realidade que define
Samantha desde a cena 3. A teoria estabelece que "o verdadeiro caráter
é revelado sob pressão" - quando confrontada com a realidade desagradável
do despertar, Samantha escolhe verbalmente focar no sonho (passado idealizado)
ao invés do presente. A estrutura gramatical "estava tendo" (pretérito imperfeito)
reforça sua permanência no estado onírico. A escolha da palavra "lindo" (não
"bom" ou "interessante") demonstra idealização excessiva, conectando com o
subtexto de sua recusa em processar o trauma estabelecido na terapia (cena 8).

Problema: O diálogo é puramente expositivo - declara o estado emocional
diretamente sem mostrar comportamento. A teoria adverte contra
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
específicos, sem conexão com a teoria do livro fornecido, sem exemplo concreto
de reescrita, poderia aplicar-se a qualquer roteiro]

IMPORTANTE: Identifique o AUTOR correto do livro fornecido e cite-o pelo nome!
═══════════════════════════════════════════════════════════════
"""

        # DEBUG: Log python_summary para verificar quantas recomendações estão indo
        logger.info(f"[DEBUG] Python summary being sent to LLM ({len(python_summary)} chars):")
        logger.info(f"[DEBUG] {python_summary[:500]}...")

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
2. Conecte ao <livro_{book_id}>: capítulos e conceitos específicos com citações DO AUTOR fornecido no contexto
3. EVITE análise genérica: seja específico com exemplos concretos do roteiro
4. Estruture em 12-14 parágrafos detalhados conforme formato obrigatório
5. Cada parágrafo DEVE ter: cena/página + citação + teoria + análise causal
6. Cite o AUTOR CORRETO cujo livro foi fornecido acima (verifique os metadados)

Comece sua análise pela PRIMEIRA cena do roteiro fornecido.
</instrucoes_finais>
"""
        return prompt

    def _build_llm_prompt_pass1(self, screenplay_text: str, python_result: Dict) -> str:
        """
        TWO-PASS ARCHITECTURE - PASS 1: Identify problems (WHAT is wrong).

        Focus: Sections 1-3 (INTERPRETAÇÃO, PADRÕES, PROBLEMAS)
        Goal: Identify EXACTLY 4 problems with theory citations
        """
        # FASE 2: Use personalized prompts if enabled
        if self.use_personalized_prompts and self.specialist_type:
            logger.info(f"[DUAL-CORE] 🎯 Using PERSONALIZED PROMPTS for author: {self.specialist_type}")

            # Limit screenplay excerpt for context
            words = screenplay_text.split()
            screenplay_excerpt = ' '.join(words[:5000]) if len(words) > 5000 else screenplay_text

            # Format Python metrics
            python_metrics = self._format_python_result(python_result)

            # Build personalized prompt using FASE 2 system
            try:
                personalized_prompt = build_personalized_prompt_pass1(
                    author=self.specialist_type,
                    screenplay_context=screenplay_excerpt,
                    python_metrics=python_metrics
                )
                logger.info(f"[DUAL-CORE] ✅ Personalized prompt built: {len(personalized_prompt)} chars")
                return personalized_prompt
            except Exception as e:
                logger.warning(f"[DUAL-CORE] ⚠️ Personalized prompt failed: {e}, falling back to default")
                # Fall through to default prompt below

        # DEFAULT: Reuse most of the existing prompt logic but focus on problem identification
        python_summary = self._format_python_result(python_result)

        # Get theory context (same as original)
        theory_context = ""
        theory_mode = "NONE"
        book_id = self.specialist_type or "theory_book"

        if self.use_theory and self.theory_indexer:
            problems = python_result.get('recommendations', [])
            if not problems:
                problems = [python_result.get('diagnosis', '')]

            try:
                if self.deep_context:
                    logger.info("📚 PASS 1: Loading full book context...")
                    query = " ".join(problems[:3]) if problems else self.specialist_type
                    deep_result = self.theory_indexer.get_full_book_context(
                        query=query,
                        max_books=1,
                        specialist_type=self.specialist_type
                    )

                    if deep_result and deep_result['primary_book']:
                        book = deep_result['primary_book']
                        theory_context = f"""
<documento_fonte id="livro_{book_id}" tipo="teoria_completa">
<metadados>
  <titulo>{book['name']}</titulo>
  <palavras>{book['word_count']:,}</palavras>
</metadados>

<texto_completo>
{book['full_text']}
</texto_completo>
</documento_fonte>
"""
                        theory_mode = "DEEP"
            except Exception as e:
                logger.warning(f"⚠️ Theory search failed: {e}")

        # Limit screenplay excerpt (PASS 1: usar mesmo limite que principal)
        words = screenplay_text.split()

        # CRÍTICO: No modo deep_context, enviar ROTEIRO COMPLETO (não truncar)
        if self.deep_context:
            screenplay_excerpt = screenplay_text  # FULL TEXT, sem truncamento
            logger.info(f"[PASS 1 DEEP_CONTEXT] Sending FULL screenplay: {len(words)} words")
        elif len(words) > 10000:
            # Modo normal: limite aumentado para 10k palavras (era 2k)
            screenplay_excerpt = ' '.join(words[:10000]) + '\n[... continues ...]'
            logger.warning(f"[PASS 1 SHALLOW] Screenplay truncated: {len(words)} → 10000 words")
        else:
            screenplay_excerpt = screenplay_text
            logger.info(f"[PASS 1 SHALLOW] Sending screenplay: {len(words)} words")

        # PASS 1 specific instructions
        pass1_task = """
⚠️⚠️⚠️  TWO-PASS ARCHITECTURE - THIS IS PASS 1/2  ⚠️⚠️⚠️

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🚨 CRITICAL: THIS IS A REAL SCREENPLAY ANALYSIS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⛔ ABSOLUTE PROHIBITIONS:
❌ DO NOT invent character names (like "JOHN", "MARY", "SARAH", "LUCAS")
❌ DO NOT create hypothetical scenes
❌ DO NOT write generic examples that could apply to any screenplay
❌ DO NOT say "I don't have access to the screenplay" - IT IS PROVIDED!
❌ DO NOT fabricate information not present in the documents
❌ IF information is missing, explicitly state: "Not present in the provided screenplay"

✅ YOU MUST:
✅ Read the ACTUAL screenplay provided in <roteiro_analise>
✅ Use REAL character names from the screenplay
✅ Quote ACTUAL dialogue lines (with quotation marks)
✅ Cite ACTUAL scene numbers and page references

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

YOUR MISSION IN THIS PASS:
Focus ENTIRELY on IDENTIFYING problems in THIS SPECIFIC SCREENPLAY.
You will have a second pass to expand solutions.

In this pass, generate ONLY sections 1-3:

1. INTERPRETAÇÃO (2 substantial paragraphs):
   → What Python metrics reveal about THIS SPECIFIC SCREENPLAY + connection to theory
   → Overall quality assessment of THIS SPECIFIC STORY

2. PADRÕES (2 substantial paragraphs):
   → Recurring patterns YOU FOUND in THIS SPECIFIC SCREENPLAY
   → Impact of these patterns on THIS STORY's effectiveness

3. PROBLEMAS - EXACTLY 4 PROBLEMS (1 paragraph per problem):

   For EACH problem, write ONE SUBSTANTIAL paragraph:

   PROBLEMA [N]: [Problem name] (X occurrences in Y scenes)
   → Descrição: What YOU FOUND in THIS SCREENPLAY specifically
   → Impacto: How it affects THIS SPECIFIC STORY
   → Localizações: WHERE in THIS SCREENPLAY (cite ACTUAL moments/pages)
   → Citação: ACTUAL dialogue from THIS SCREENPLAY (in "quotation marks")
   → Teoria relevante: [Author] in '[Book Title]', Chapter X ([Chapter Name]), [specific concept]

⚠️  CRITICAL: You MUST identify EXACTLY 4 PROBLEMS in section 3.
⚠️  Each problem MUST cite ACTUAL scenes and ACTUAL dialogue from THIS screenplay
⚠️  Each problem MUST use REAL CHARACTER NAMES from the screenplay
⚠️  DO NOT generate section 4 (SOLUÇÕES) yet - that's for Pass 2
⚠️  DO NOT generate section 5 (PROFUNDIDADE & SÍNTESE) yet - that's for Pass 2

FOCUS: Deep problem identification in THIS SPECIFIC SCREENPLAY with theory backing.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🌍 LANGUAGE: Write your entire response in PORTUGUESE (PT-BR)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

        prompt = f"""
<contexto_dual_core>
<analise_python tipo="estrutural">
{python_summary}
</analise_python>

{theory_context}

<roteiro_analise>
{screenplay_excerpt}
</roteiro_analise>
</contexto_dual_core>

{pass1_task}

Begin your Pass 1 analysis (sections 1-3 only):
"""
        return prompt

    def _build_llm_prompt_pass2(self, screenplay_text: str, python_result: Dict, pass1_response: str) -> str:
        """
        TWO-PASS ARCHITECTURE - PASS 2: Expand solutions (HOW to fix).

        Focus: Section 4 (SOLUÇÕES) + Section 5 (DEPTH & SYNTHESIS)
        Goal: Generate CONCRETE solution examples with line-by-line rewrites
        """
        # FASE 2: Use personalized prompts if enabled
        if self.use_personalized_prompts and self.specialist_type:
            logger.info(f"[DUAL-CORE] 🎯 Using PERSONALIZED PROMPTS PASS 2 for author: {self.specialist_type}")

            # Limit screenplay excerpt for context
            words = screenplay_text.split()
            screenplay_excerpt = ' '.join(words[:5000]) if len(words) > 5000 else screenplay_text

            # Format Python metrics
            python_metrics = self._format_python_result(python_result)

            # Build personalized prompt Pass 2 using FASE 2 system
            try:
                personalized_prompt = build_personalized_prompt_pass2(
                    author=self.specialist_type,
                    screenplay_context=screenplay_excerpt,
                    python_metrics=python_metrics,
                    pass1_result=pass1_response
                )
                logger.info(f"[DUAL-CORE] ✅ Personalized prompt Pass 2 built: {len(personalized_prompt)} chars")
                return personalized_prompt
            except Exception as e:
                logger.warning(f"[DUAL-CORE] ⚠️ Personalized prompt Pass 2 failed: {e}, falling back to default")
                # Fall through to default prompt below

        # DEFAULT: Standard pass 2 prompt
        python_summary = self._format_python_result(python_result)

        # Limit screenplay (PASS 2: usar mesmo limite que principal)
        words = screenplay_text.split()

        # CRÍTICO: No modo deep_context, enviar ROTEIRO COMPLETO (não truncar)
        if self.deep_context:
            screenplay_excerpt = screenplay_text  # FULL TEXT, sem truncamento
            logger.info(f"[PASS 2 DEEP_CONTEXT] Sending FULL screenplay: {len(words)} words")
        elif len(words) > 10000:
            # Modo normal: limite aumentado para 10k palavras (era 2k)
            screenplay_excerpt = ' '.join(words[:10000]) + '\n[... continues ...]'
            logger.warning(f"[PASS 2 SHALLOW] Screenplay truncated: {len(words)} → 10000 words")
        else:
            screenplay_excerpt = screenplay_text
            logger.info(f"[PASS 2 SHALLOW] Sending screenplay: {len(words)} words")

        # PASS 2 specific instructions
        pass2_task = """
⚠️⚠️⚠️  TWO-PASS ARCHITECTURE - THIS IS PASS 2/2  ⚠️⚠️⚠️

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🚨 CRITICAL: THIS IS A REAL SCREENPLAY ANALYSIS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⛔ ABSOLUTE PROHIBITIONS:
❌ DO NOT invent character names in your ANTES/DEPOIS examples
❌ DO NOT create hypothetical scenes that don't exist in the screenplay
❌ DO NOT write generic solutions that could apply to any screenplay
❌ DO NOT fabricate information not present in the documents
❌ IF information is missing, explicitly state: "Not present in the provided screenplay"

✅ YOU MUST:
✅ Rewrite ACTUAL moments from THIS SPECIFIC SCREENPLAY
✅ Use the REAL character names from the screenplay in your rewrites
✅ Reference ACTUAL scenes and pages from the screenplay
✅ Show how to fix THE SPECIFIC PROBLEMS you identified in Pass 1

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

YOUR MISSION IN THIS PASS:
You've already identified the problems in Pass 1 of THIS SPECIFIC SCREENPLAY.
Now EXPAND the solutions with CONCRETE EXAMPLES from THIS SCREENPLAY.

Generate sections 4-5:

4. SOLUÇÕES - One solution per problem (1 paragraph per solution):

   For EACH of the 4 problems identified in Pass 1, write ONE SUBSTANTIAL paragraph:

   SOLUÇÃO PARA PROBLEMA [N]: [Restate problem name]
   → Solução específica: How to fix THIS PROBLEM in THIS SCREENPLAY
   → Fundamentação teórica: [Book/Chapter/Concept from theory]
   → Exemplos concretos: REWRITE ACTUAL MOMENTS from THIS SCREENPLAY
   → Resultado esperado: Expected improvement for THIS SPECIFIC STORY

   EXAMPLE FORMAT (using REAL characters from the screenplay):
   "SOLUÇÃO PARA PROBLEMA 1: Exposição emocional direta

   Para corrigir a exposição direta na cena onde [REAL CHARACTER NAME] revela seus
   sentimentos, reescrever o momento na página [ACTUAL PAGE] onde [he/she] atualmente
   diz '[ACTUAL QUOTE FROM THE SCREENPLAY]'.

   Fundamentação: McKee em 'Dialogue: The Art of Verbal Action', Capítulo 9, explica
   que [theory principle].

   Exemplos concretos do roteiro atual:

   ANTES (página [X], cena [Y] do roteiro):
   [REAL CHARACTER]: '[ACTUAL LINE FROM THE SCREENPLAY YOU'RE ANALYZING]'

   DEPOIS (sugestão usando os MESMOS PERSONAGENS):
   [REAL CHARACTER]: '[Your improved version using THE SAME CHARACTER]'

   Resultado esperado para ESTA história específica: [Impact on THIS story]..."

5. DEPTH & SYNTHESIS (2 detailed paragraphs):
   → Parágrafo 1: Advanced insights about interconnections between problems IN THIS SCREENPLAY
   → Parágrafo 2: Final professional assessment and path forward for THIS SPECIFIC STORY

   In the final paragraph, explicitly recommend:
   "Recomenda-se leitura minuciosa do livro [Author], '[Full Book Title]',
   especialmente os Capítulos [X, Y, Z] para aprofundar nesses aspectos."

⚠️  CRITICAL: Provide CONCRETE LINE-BY-LINE REWRITE EXAMPLES using REAL character names!
⚠️  The examples must be ACTUAL scenes from THIS SPECIFIC SCREENPLAY!
⚠️  Each ANTES must quote the ACTUAL LINE from the screenplay with REAL CHARACTER NAMES
⚠️  Each DEPOIS must use the SAME REAL CHARACTERS (not invented names like JOHN, MARY, ANA!)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🌍 LANGUAGE: Write your entire response in PORTUGUESE (PT-BR)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

        prompt = f"""
<contexto_dual_core>
<analise_python tipo="estrutural">
{python_summary}
</analise_python>

<pass1_analysis tipo="problemas_identificados">
{pass1_response}
</pass1_analysis>

<roteiro_analise>
{screenplay_excerpt}
</roteiro_analise>
</contexto_dual_core>

{pass2_task}

Begin your Pass 2 analysis (sections 4-5 only):
"""
        return prompt

    def _combine_two_pass_responses(self, pass1_response: str, pass2_response: str) -> str:
        """
        Combine Pass 1 (sections 1-3) and Pass 2 (sections 4-5) into final response.
        """
        # Simple concatenation - Pass 1 already has sections 1-3, Pass 2 has sections 4-5
        combined = f"""{pass1_response.strip()}

{pass2_response.strip()}"""

        return combined

    def _validate_llm_output(self, llm_response: str) -> Dict[str, Any]:
        """
        Valida qualidade do output LLM.

        Returns:
            Dict com 'valid' (bool), 'score' (float 0-10), 'reason' (str)
        """
        score = 0.0
        reasons = []

        # 1. Length check - adaptive based on screenplay size
        char_count = len(llm_response)
        word_count = len(llm_response.split())

        # Adaptive expectations:
        # Short films (<30 pages): 5,000-8,000 chars is excellent
        # Medium films (30-90 pages): 8,000-12,000 chars
        # Feature films (90+ pages): 10,000-15,000 chars

        if char_count < 1000:
            reasons.append(f"Too short: {char_count} chars")
            score = 1.0
        elif char_count < 3000:
            reasons.append(f"Below minimum: {char_count} chars")
            score = 3.0
        elif char_count < 5000:
            reasons.append(f"Acceptable: {char_count} chars")
            score = 5.0
        elif char_count < 8000:
            reasons.append(f"Good quality: {char_count} chars")
            score = 7.0
        elif char_count < 12000:
            reasons.append(f"Excellent: {char_count} chars")
            score = 8.5
        else:
            # 12000+ chars = exceptional
            score = 10.0

        # 2. Content checks
        lower_response = llm_response.lower()

        # Check for error patterns
        if 'timeout' in lower_response or 'failed' in lower_response:
            reasons.append("Contains error indicators")
            score = min(score, 2.0)

        # Check for actual analysis content
        has_specific_examples = any(phrase in lower_response for phrase in [
            'cena', 'scene', 'página', 'page', 'diálogo', 'dialogue',
            'personagem', 'character'
        ])

        if not has_specific_examples:
            reasons.append("No specific scene/dialogue references")
            score = min(score, 4.0)

        # Check for depth indicators
        depth_indicators = [
            'porque', 'because', 'portanto', 'therefore',
            'exemplo', 'example', 'especificamente', 'specifically'
        ]
        depth_count = sum(1 for ind in depth_indicators if ind in lower_response)

        if depth_count < 3:
            reasons.append(f"Lacks depth indicators ({depth_count}/3+)")
            score = min(score, 5.0)

        # 3. Final validation
        valid = score >= 5.0  # Minimum acceptable quality

        if not reasons:
            reasons.append(f"Good quality: {char_count} chars, {word_count} words")

        return {
            'valid': valid,
            'score': score,
            'reason': '; '.join(reasons),
            'char_count': char_count,
            'word_count': word_count
        }

    def _validate_analysis_quality(self, analysis: str, author: str) -> tuple[bool, float, list]:
        """
        Valida qualidade de análise baseado nos critérios dos autores nivel 10.

        Critérios baseados em MCKEE_DIALOGUE (8/10) e CAMPBELL (7/10):
        - Mínimo 15,000 caracteres
        - 3+ citações de cenas específicas
        - 3+ citações verbatim de diálogos (20+ palavras)
        - 2+ exemplos ANTES/DEPOIS de reescrita

        Args:
            analysis: Texto da análise LLM
            author: Nome do autor/teoria sendo usada

        Returns:
            Tuple de (passed: bool, score: float 0-10, issues: list[str])
        """
        score = 10.0
        issues = []

        # 1. Length check (15,000 chars minimum)
        char_count = len(analysis)
        if char_count < 15000:
            penalty = 2.0
            score -= penalty
            issues.append(f"Too short: {char_count}/15000 chars (-{penalty})")
        else:
            issues.append(f"✅ Length: {char_count} chars")

        # 2. Scene citations (minimum 3)
        scene_pattern = r'(SCENE\s+\d+|CENA\s+\d+|página\s+\d+|page\s+\d+|p\.\s*\d+)'
        scenes = re.findall(scene_pattern, analysis, re.IGNORECASE)
        scene_count = len(set(scenes))  # Unique scenes
        if scene_count < 3:
            penalty = 2.0
            score -= penalty
            issues.append(f"Too few scene citations: {scene_count}/3 (-{penalty})")
        else:
            issues.append(f"✅ Scenes cited: {scene_count}")

        # 3. Verbatim quotes (minimum 3, each 20+ words)
        # Look for quoted text (using " or ' or «)
        quote_pattern = r'["\'\u00AB]([^"\'\u00BB]{20,})["\'\u00BB]'
        quotes = re.findall(quote_pattern, analysis)
        # Filter for quotes with 20+ characters (rough proxy for 5+ words)
        substantial_quotes = [q for q in quotes if len(q.strip()) >= 20]
        quote_count = len(substantial_quotes)
        if quote_count < 3:
            penalty = 2.0
            score -= penalty
            issues.append(f"Too few quotes: {quote_count}/3 substantial quotes (-{penalty})")
        else:
            issues.append(f"✅ Quotes: {quote_count}")

        # 4. ANTES/DEPOIS rewrites (minimum 2)
        rewrite_pattern = r'(ANTES.*?DEPOIS|BEFORE.*?AFTER|antes:.*?depois:|before:.*?after:)'
        rewrites = re.findall(rewrite_pattern, analysis, re.DOTALL | re.IGNORECASE)
        rewrite_count = len(rewrites)
        if rewrite_count < 2:
            penalty = 2.5
            score -= penalty
            issues.append(f"Too few ANTES/DEPOIS rewrites: {rewrite_count}/2 (-{penalty})")
        else:
            issues.append(f"✅ Rewrites: {rewrite_count}")

        # 5. Theory citations (should mention author name 3+ times)
        # List of possible author names to check
        author_names = [
            'McKee', 'Truby', 'Field', 'Campbell', 'Egri', 'Snyder',
            'Vogler', 'Seger', 'Cowgill', 'Aristotle', 'Yorke'
        ]
        theory_mentions = 0
        for name in author_names:
            theory_mentions += len(re.findall(name, analysis, re.IGNORECASE))

        if theory_mentions < 3:
            penalty = 1.5
            score -= penalty
            issues.append(f"Too few theory citations: {theory_mentions}/3 (-{penalty})")
        else:
            issues.append(f"✅ Theory citations: {theory_mentions}")

        # Final score clamping
        score = max(0.0, min(10.0, score))

        # Pass if score >= 7.0 (nivel profissional)
        passed = score >= 7.0

        return passed, score, issues

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
        Hybrid LLM backend: Ollama (local) or OpenAI (API).

        Auto-detects based on model name:
        - Models starting with 'gpt-' use OpenAI API
        - All other models use Ollama
        """
        try:
            # ═══ DETECT LLM BACKEND ═══
            if self.llm_model.startswith('gpt-'):
                # ═══ OPENAI API PATH ═══
                logger.info(f"[DUAL-CORE] Using OpenAI API: {self.llm_model}")

                try:
                    from openai import OpenAI
                except ImportError:
                    raise Exception("OpenAI library not installed. Run: pip install openai")

                api_key = os.environ.get("OPENAI_API_KEY")
                if not api_key:
                    raise Exception("OPENAI_API_KEY environment variable not set")

                client = OpenAI(api_key=api_key)

                # Call OpenAI API
                response = client.chat.completions.create(
                    model=self.llm_model,
                    messages=[
                        {"role": "system", "content": "You are an expert screenplay analyst with deep knowledge of narrative structure, character development, and cinematic storytelling. Analyze screenplays using precise terminology from McKee, Campbell, Truby, Field, Vogler, and other masters."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.2,  # Analytical mode (NOT creative!) - Medical-grade precision
                    max_completion_tokens=16000
                )

                # Extract response
                response_text = response.choices[0].message.content.strip()

                # Calculate and track cost
                input_tokens = response.usage.prompt_tokens
                output_tokens = response.usage.completion_tokens

                # GPT-5 pricing: $1/1M input, $4/1M output
                cost = (input_tokens / 1_000_000) * 1.00 + (output_tokens / 1_000_000) * 4.00

                # Store cost tracking
                if not hasattr(self, '_openai_costs'):
                    self._openai_costs = []

                self._openai_costs.append({
                    'input_tokens': input_tokens,
                    'output_tokens': output_tokens,
                    'cost': cost,
                    'model': self.llm_model
                })

                logger.info(f"[DUAL-CORE] OpenAI call: {input_tokens:,} in + {output_tokens:,} out = ${cost:.4f}")

                return response_text

            else:
                # ═══ OLLAMA PATH (ORIGINAL - UNCHANGED) ═══
                logger.info(f"[DUAL-CORE] Using Ollama: {self.llm_model}")

                # Chamar Ollama com prompt via stdin
                cmd = ['ollama', 'run', self.llm_model]

                logger.debug(f"Calling LLM: {' '.join(cmd)}")

                # Build subprocess.run() kwargs
                run_kwargs = {
                    'input': prompt,
                    'capture_output': True,
                    'text': True
                }

                # Only add timeout if specified (None = no timeout)
                if self.llm_timeout is not None:
                    run_kwargs['timeout'] = self.llm_timeout
                    logger.info(f"[DUAL-CORE] LLM timeout set to {self.llm_timeout}s")
                else:
                    logger.info("[DUAL-CORE] LLM running without timeout (deep analysis mode)")

                result = subprocess.run(cmd, **run_kwargs)

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

    def get_openai_cost_summary(self) -> Dict[str, Any]:
        """
        Returns summary of OpenAI API costs for this session.

        Returns dict with:
        - total_calls: Number of API calls made
        - total_input_tokens: Total input tokens used
        - total_output_tokens: Total output tokens used
        - total_cost: Total cost in USD
        - calls: List of individual call details
        """
        if not hasattr(self, '_openai_costs') or not self._openai_costs:
            return {
                'total_calls': 0,
                'total_input_tokens': 0,
                'total_output_tokens': 0,
                'total_cost': 0.0,
                'calls': []
            }

        total_input = sum(c['input_tokens'] for c in self._openai_costs)
        total_output = sum(c['output_tokens'] for c in self._openai_costs)
        total_cost = sum(c['cost'] for c in self._openai_costs)

        return {
            'total_calls': len(self._openai_costs),
            'total_input_tokens': total_input,
            'total_output_tokens': total_output,
            'total_cost': total_cost,
            'calls': self._openai_costs.copy()
        }

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
        from engine.exporters.formatted_exporter import FormattedExporter
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
