"""
Theory Indexer - Busca rápida em livros de teoria
Python faz busca (rápido, zero tokens), LLM interpreta (contexto rico)
"""

from pathlib import Path
from typing import List, Dict, Optional
import re


class TheoryIndexer:
    """
    Indexador simples e rápido de livros de teoria.

    Estratégia:
    1. Python carrega e chunka livros (uma vez)
    2. Python busca termos relevantes (regex, zero tokens)
    3. Python retorna trechos + metadados
    4. LLM recebe contexto rico e interpreta
    """

    def __init__(self, theory_dir: Path = None):
        """Inicializa indexador"""
        if theory_dir is None:
            theory_dir = Path(__file__).parent.parent.parent / "knowledge" / "theory_books"

        self.theory_dir = theory_dir
        self.books = {}
        self.chunks = {}

        # Cache de buscas
        self._search_cache = {}

    def index_book(self, book_path: Path, chunk_size: int = 500):
        """
        Indexa um livro dividindo em chunks para busca rápida.

        Args:
            book_path: Caminho do livro .txt
            chunk_size: Tamanho dos chunks em palavras
        """
        print(f"📚 Indexando: {book_path.name}...")

        try:
            content = book_path.read_text(encoding='utf-8', errors='ignore')
        except Exception as e:
            print(f"   ❌ Erro ao ler {book_path.name}: {e}")
            return

        # Dividir em chunks com overlap
        words = content.split()
        chunks = []

        overlap = 50  # 50 palavras de overlap entre chunks
        for i in range(0, len(words), chunk_size - overlap):
            chunk_words = words[i:i + chunk_size]
            chunk_text = ' '.join(chunk_words)

            # Metadados do chunk
            chunk_data = {
                'text': chunk_text,
                'book': book_path.stem,
                'chunk_id': len(chunks),
                'start_word': i,
                'word_count': len(chunk_words)
            }

            chunks.append(chunk_data)

        self.books[book_path.stem] = {
            'path': book_path,
            'total_words': len(words),
            'total_chunks': len(chunks)
        }

        self.chunks[book_path.stem] = chunks

        print(f"   ✅ {len(chunks)} chunks criados ({len(words):,} palavras)")

    def index_all_theory(self):
        """Indexa todos os livros de teoria"""
        if not self.theory_dir.exists():
            print(f"❌ Diretório não encontrado: {self.theory_dir}")
            return

        theory_files = list(self.theory_dir.glob("*.txt"))

        if not theory_files:
            print(f"⚠️ Nenhum arquivo .txt em {self.theory_dir}")
            return

        print(f"\n📚 Indexando {len(theory_files)} livros de teoria...\n")

        for book_file in theory_files:
            self.index_book(book_file)

        print(f"\n✅ Indexação completa!")
        print(f"   Total: {len(self.books)} livros, {sum(len(c) for c in self.chunks.values())} chunks")

    def search(self, query: str, limit: int = 3, book_filter: Optional[str] = None) -> List[Dict]:
        """
        Busca trechos relevantes nos livros.

        Args:
            query: Termo ou conceito a buscar (ex: "subtext", "dialogue authenticity")
            limit: Número máximo de resultados
            book_filter: Filtrar por livro específico (ex: "Dialogue")

        Returns:
            Lista de chunks relevantes com metadados
        """
        # Cache de busca
        cache_key = f"{query}_{limit}_{book_filter}"
        if cache_key in self._search_cache:
            return self._search_cache[cache_key]

        results = []
        query_lower = query.lower()

        # Preparar termos de busca (split multi-word queries)
        query_terms = query_lower.split()

        # Buscar em todos os chunks
        for book_name, book_chunks in self.chunks.items():
            # Filtro por livro
            if book_filter and book_filter.lower() not in book_name.lower():
                continue

            for chunk in book_chunks:
                chunk_text_lower = chunk['text'].lower()

                # Score de relevância
                score = 0

                # Busca exata da query inteira (maior peso)
                if query_lower in chunk_text_lower:
                    score += 10

                # Busca de termos individuais
                for term in query_terms:
                    if term in chunk_text_lower:
                        score += 2

                # Se relevante, adicionar
                if score > 0:
                    result = {
                        'text': chunk['text'][:1000],  # Limitar tamanho
                        'book': chunk['book'],
                        'chunk_id': chunk['chunk_id'],
                        'score': score,
                        'context': f"[{chunk['book']} - Chunk {chunk['chunk_id']}]"
                    }
                    results.append(result)

        # Ordenar por score (mais relevante primeiro)
        results.sort(key=lambda x: x['score'], reverse=True)

        # Limitar resultados
        results = results[:limit]

        # Cache
        self._search_cache[cache_key] = results

        return results

    def search_for_problems(self, problems: List[str], limit_per_problem: int = 2) -> Dict[str, List[Dict]]:
        """
        Busca teoria relevante para lista de problemas detectados.

        MAPEAMENTO PRECISO: Cada regra DrDialogue → termos específicos McKee

        Args:
            problems: Lista de problemas (ex: ["unnatural speech", "lack of subtext"])
            limit_per_problem: Quantos resultados por problema

        Returns:
            Dict mapeando problema → teoria relevante
        """
        results = {}

        for problem in problems:
            problem_lower = problem.lower()

            # MAPEAMENTO PROFUNDO: Problemas → Termos Teoria McKee
            query_terms = []

            # DIAL.R001 - Natural Speech Patterns
            if any(kw in problem_lower for kw in ["natural speech", "contractions", "interruptions", "incomplete thoughts", "written not spoken"]):
                query_terms = [
                    "natural dialogue",
                    "conversational rhythm",
                    "speech patterns",
                    "authentic voice",
                    "how people really talk",
                    "contractions dialogue",
                    "interrupted speech"
                ]

            # DIAL.R002 - Distinct Character Voices
            elif any(kw in problem_lower for kw in ["distinct", "voice", "identical", "same", "character voices", "unique vocabulary"]):
                query_terms = [
                    "character voice",
                    "distinctive dialogue",
                    "unique speech patterns",
                    "character differentiation",
                    "vocal identity",
                    "idiolect",
                    "speech characterization"
                ]

            # DIAL.R003 - Subtext Present
            elif any(kw in problem_lower for kw in ["subtext", "talk around", "hide true feelings", "beneath surface", "indirect"]):
                query_terms = [
                    "subtext",
                    "indirect dialogue",
                    "what characters really mean",
                    "hidden meaning",
                    "unspoken desires",
                    "subconscious wants",
                    "dialogue beneath surface",
                    "implication"
                ]

            # DIAL.R004 - Avoid On-the-Nose
            elif any(kw in problem_lower for kw in ["on-the-nose", "explain everything", "state obvious", "too direct"]):
                query_terms = [
                    "on-the-nose dialogue",
                    "show don't tell",
                    "subtle dialogue",
                    "implied emotion",
                    "indirect expression",
                    "avoid stating obvious"
                ]

            # DIAL.R005 - Dialogue Serves Purpose
            elif any(kw in problem_lower for kw in ["purpose", "empty", "no function", "advance story", "reveal character"]):
                query_terms = [
                    "functional dialogue",
                    "purposeful speech",
                    "dialogue as action",
                    "advancing plot",
                    "revealing character",
                    "every line counts"
                ]

            # DIAL.R006 - Authentic to Character
            elif any(kw in problem_lower for kw in ["authentic", "consistency", "out of character", "background", "education"]):
                query_terms = [
                    "character authenticity",
                    "consistent voice",
                    "true to character",
                    "vocabulary level",
                    "education in dialogue",
                    "background consistency"
                ]

            # DIAL.R007 - Conflict in Conversation
            elif any(kw in problem_lower for kw in ["conflict", "opposing goals", "tension", "disagreement", "want different things"]):
                query_terms = [
                    "conflict in dialogue",
                    "dramatic tension",
                    "opposing desires",
                    "conversational conflict",
                    "dialogue as battle",
                    "competing agendas",
                    "verbal sparring"
                ]

            # DIAL.R008 - Avoid Exposition Dumps
            elif any(kw in problem_lower for kw in ["exposition", "dump", "info dump", "explain", "backstory"]):
                query_terms = [
                    "exposition in dialogue",
                    "invisible exposition",
                    "weave information",
                    "avoid info dumps",
                    "natural revelation",
                    "drip-feed backstory"
                ]

            # DIAL.R009 - White Space Balance
            elif any(kw in problem_lower for kw in ["white space", "monologue", "wall of text", "long speeches", "pacing"]):
                query_terms = [
                    "dialogue rhythm",
                    "speech pacing",
                    "breaking monologues",
                    "conversational flow",
                    "interruption timing",
                    "beat work"
                ]

            # DIAL.R010 - Listen and Respond
            elif any(kw in problem_lower for kw in ["listen", "respond", "talk past", "react", "build on"]):
                query_terms = [
                    "active listening",
                    "response patterns",
                    "conversational exchange",
                    "building dialogue",
                    "reaction to speech",
                    "dialogue interaction"
                ]

            # DIAL.R011 - Emotional Truth
            elif any(kw in problem_lower for kw in ["emotion", "emotional state", "feeling", "affect", "word choice"]):
                query_terms = [
                    "emotional dialogue",
                    "emotion in speech",
                    "feeling through words",
                    "emotional authenticity",
                    "affect word choice",
                    "emotional subtext"
                ]

            # DIAL.R012 - Period and Setting
            elif any(kw in problem_lower for kw in ["period", "setting", "anachronism", "historical", "time"]):
                query_terms = [
                    "period dialogue",
                    "historical accuracy",
                    "setting-appropriate",
                    "time period speech",
                    "era-specific language"
                ]

            # DIAL.R013 - Avoid Clichés
            elif any(kw in problem_lower for kw in ["cliché", "cliched", "overused", "original", "fresh"]):
                query_terms = [
                    "fresh dialogue",
                    "original expression",
                    "avoid clichés",
                    "unique phrasing",
                    "inventive speech"
                ]

            # DIAL.R014 - Power Dynamics
            elif any(kw in problem_lower for kw in ["power", "dynamics", "status", "dominance", "hierarchy"]):
                query_terms = [
                    "power in dialogue",
                    "status games",
                    "dominance speech",
                    "power dynamics",
                    "hierarchical dialogue",
                    "who has control"
                ]

            # DIAL.R015 - Memorable Lines
            elif any(kw in problem_lower for kw in ["memorable", "quotable", "iconic", "impact", "key lines"]):
                query_terms = [
                    "memorable dialogue",
                    "quotable lines",
                    "iconic moments",
                    "crystallize theme",
                    "impact speech"
                ]

            # ===== DR STRUCTURE MAPPINGS =====

            # STRUCT.R001 - Three-Act Structure Present
            elif any(kw in problem_lower for kw in ["three-act", "three act", "paradigm", "acts missing", "no clear acts"]):
                query_terms = [
                    "three act structure",
                    "paradigm",
                    "act structure",
                    "setup confrontation resolution",
                    "structural foundation",
                    "dramatic structure",
                    "beginning middle end",
                    "structural paradigm",
                    "story architecture",
                    "three-act model"
                ]

            # STRUCT.R002 - Inciting Incident Present
            elif any(kw in problem_lower for kw in ["inciting incident", "catalyst", "call to action", "story trigger", "delayed inciting"]):
                query_terms = [
                    "inciting incident",
                    "catalyst",
                    "call to action",
                    "story begins",
                    "precipitating event",
                    "narrative hook",
                    "triggering event",
                    "plot point zero",
                    "story ignition",
                    "act one event"
                ]

            # STRUCT.R003 - Midpoint Present
            elif any(kw in problem_lower for kw in ["midpoint", "middle", "act two center", "false victory", "false defeat"]):
                query_terms = [
                    "midpoint",
                    "structural center",
                    "false victory",
                    "false defeat",
                    "middle turning point",
                    "central reversal",
                    "act two pivot",
                    "story center",
                    "midpoint shift",
                    "central crisis"
                ]

            # STRUCT.R004 - Plot Point 1 Present
            elif any(kw in problem_lower for kw in ["plot point 1", "first plot point", "end of act one", "first turning", "pp1"]):
                query_terms = [
                    "plot point one",
                    "first plot point",
                    "end of act one",
                    "first turning point",
                    "act one climax",
                    "point of no return",
                    "door of no return",
                    "commitment point",
                    "first major event",
                    "act break one"
                ]

            # STRUCT.R005 - Plot Point 2 Present
            elif any(kw in problem_lower for kw in ["plot point 2", "second plot point", "end of act two", "second turning", "pp2"]):
                query_terms = [
                    "plot point two",
                    "second plot point",
                    "end of act two",
                    "second turning point",
                    "act two climax",
                    "darkest moment",
                    "all is lost",
                    "dark night of soul",
                    "final push",
                    "act break two"
                ]

            # STRUCT.R006 - Act Proportions Correct
            elif any(kw in problem_lower for kw in ["act proportion", "25/50/25", "unbalanced acts", "act length", "timing"]):
                query_terms = [
                    "act proportions",
                    "25 50 25",
                    "act balance",
                    "structural timing",
                    "act length",
                    "paradigm timing",
                    "proper act ratio",
                    "structural pacing",
                    "act distribution",
                    "page count balance"
                ]

            # STRUCT.R007 - Rising Action/Tension
            elif any(kw in problem_lower for kw in ["rising action", "escalation", "building tension", "progressive", "stakes"]):
                query_terms = [
                    "rising action",
                    "escalating conflict",
                    "building tension",
                    "progressive complications",
                    "increasing stakes",
                    "story progression",
                    "tension arc",
                    "complication ladder",
                    "ascending action",
                    "dramatic build"
                ]

            # STRUCT.R008 - Climax Placement
            elif any(kw in problem_lower for kw in ["climax", "climactic", "peak", "highest point", "resolution timing"]):
                query_terms = [
                    "climax",
                    "climactic moment",
                    "story climax",
                    "dramatic peak",
                    "highest stakes",
                    "final confrontation",
                    "ultimate crisis",
                    "story peak",
                    "climax placement",
                    "final battle"
                ]

            # STRUCT.R009 - Turning Points
            elif any(kw in problem_lower for kw in ["turning point", "reversal", "twist", "change direction", "pivot"]):
                query_terms = [
                    "turning points",
                    "plot reversals",
                    "story turns",
                    "dramatic reversals",
                    "narrative pivots",
                    "change of direction",
                    "plot twists",
                    "reversal of fortune",
                    "peripeteia",
                    "story pivots"
                ]

            # STRUCT.R010 - Setup and Payoff
            elif any(kw in problem_lower for kw in ["setup", "payoff", "plant", "foreshadow", "callback", "preparation"]):
                query_terms = [
                    "setup and payoff",
                    "plant and pay",
                    "foreshadowing",
                    "dramatic preparation",
                    "setup plant",
                    "narrative payoff",
                    "callback structure",
                    "promise fulfillment",
                    "setup promise",
                    "payoff resolution"
                ]

            # GENERIC FALLBACK
            else:
                # Extrair palavras-chave do problema
                keywords = problem_lower.replace("[critical]", "").replace("[high]", "").replace("[medium]", "").replace("[low]", "").strip()
                query_terms = [keywords]

            # Buscar para cada termo
            problem_results = []
            for term in query_terms:
                term_results = self.search(term, limit=limit_per_problem)
                problem_results.extend(term_results)

            # Deduplicate por chunk_id
            seen = set()
            unique_results = []
            for r in problem_results:
                key = f"{r['book']}_{r['chunk_id']}"
                if key not in seen:
                    seen.add(key)
                    unique_results.append(r)

            # Ordenar por relevância (score) e limitar
            unique_results.sort(key=lambda x: x['score'], reverse=True)
            results[problem] = unique_results[:limit_per_problem * 2]  # Máximo 4 por problema

        return results

    def _get_author(self, book_name: str) -> str:
        """
        Mapeia nome do livro para autor.

        Args:
            book_name: Nome do arquivo do livro

        Returns:
            Nome do autor
        """
        author_map = {
            r'Dialogue.*MacKee|Dialogue.*McKee': 'Robert McKee',
            r'Character.*McKee': 'Robert McKee',
            r'st_o_r_y': 'Robert McKee',
            r'save.*cat': 'Blake Snyder',
            r'hero.*thousand.*faces|campbell|heroi.*mil.*faces': 'Joseph Campbell',
            r'anatomy.*story|truby': 'John Truby',
            r'art.*dramatic|egri': 'Lajos Egri',
            r'screenplay.*field': 'Syd Field',
            r'writers.*journey|vogler': 'Christopher Vogler',
            r'making.*good.*script|seger': 'Linda Seger',
            r'creating.*character.*arcs|weiland': 'K.M. Weiland',
            r'ontology.*tragedy|aristotle': 'Aristotle',
            r'writing.*short.*films|cowgill': 'Linda J. Cowgill',
        }

        for pattern, author in author_map.items():
            if re.search(pattern, book_name, re.IGNORECASE):
                return author
        return 'Unknown Author'

    def format_theory_context(self, theory_results: Dict[str, List[Dict]]) -> str:
        """
        Formata resultados de teoria para prompt LLM, organizados por autor.

        Args:
            theory_results: Dict de problema → chunks relevantes

        Returns:
            String formatada para contexto LLM, separada por autor
        """
        if not theory_results:
            return ""

        # Agrupar citações por autor
        by_author = {}
        for problem, chunks in theory_results.items():
            for chunk in chunks:
                author = self._get_author(chunk['book'])
                if author not in by_author:
                    by_author[author] = []
                by_author[author].append({
                    'problem': problem,
                    'text': chunk['text'],
                    'book': chunk['book'],
                    'context': chunk.get('context', chunk['book'])
                })

        # Formatar output separado por autor
        output = ["RELEVANT THEORY FROM BOOKS (organized by author):\n"]

        for author, citations in sorted(by_author.items()):
            output.append(f"\n{'='*70}")
            output.append(f"📚 DE ACORDO COM {author.upper()}:")
            output.append(f"{'='*70}\n")

            for citation in citations:
                book_short = citation['book'][:50]
                output.append(f"[{book_short}] → Para problema: {citation['problem']}")
                output.append("-" * 70)
                text = citation['text'][:600] + "..." if len(citation['text']) > 600 else citation['text']
                output.append(text)
                output.append("")

        return '\n'.join(output)

    def export_text_chunks(self, book_filter: Optional[str] = None, limit: Optional[int] = None) -> List[Dict]:
        """
        Export theory chunks as structured data for external indexing.

        Enables bidirectional theory access:
        1. search() - Find chunks by query (existing)
        2. export_text_chunks() - Export chunks for external systems (NEW)

        Useful for:
        - Correlation engines (index theory alongside screenplays)
        - ML pipelines (embeddings, clustering)
        - External search systems

        Args:
            book_filter: Optional book name filter (e.g., "Dialogue")
            limit: Max chunks to export (None = all)

        Returns:
            List of dicts with:
                - text: Chunk text
                - book: Source book
                - chunk_id: Position in book
                - word_count: Words in chunk
                - meta: Additional metadata
        """
        exported = []

        for book_name, book_chunks in self.chunks.items():
            # Filter by book if specified
            if book_filter and book_filter.lower() not in book_name.lower():
                continue

            for chunk in book_chunks:
                chunk_data = {
                    "text": chunk['text'],
                    "book": chunk['book'],
                    "chunk_id": chunk['chunk_id'],
                    "word_count": chunk['word_count'],
                    "meta": {
                        "start_word": chunk['start_word'],
                        "source": "TheoryIndexer",
                        "book_path": str(self.books[book_name]['path'])
                    }
                }
                exported.append(chunk_data)

                # Apply limit if specified
                if limit and len(exported) >= limit:
                    return exported

        return exported

    def get_full_book_context(self, query: str, max_books: int = 1, specialist_type: str = None) -> Dict:
        """
        Retorna livro(s) completo(s) mais relevante(s) para a query.

        DEEP DIVE MODE: Para quando temos 128k tokens disponíveis.
        Ao invés de enviar 3-5 chunks (~4.5k palavras), envia o livro inteiro (~77k palavras).

        Args:
            query: Query para identificar livro mais relevante
            max_books: Quantos livros completos retornar (padrão: 1)
            specialist_type: Tipo de especialista para mapeamento direto (opcional)

        Returns:
            {
                'primary_book': {...},  # Livro mais relevante completo
                'total_words': int,
                'estimated_tokens': int
            }
        """
        # MAPEAMENTO SPECIALIST → BOOK (otimização Fase 2)
        SPECIALIST_BOOK_MAP = {
            # Por tipo de especialista
            'dialogue': 'Dialogue-_-The-Art-of-Verbal-Action',
            'character': 'Character-_-The-Art-of-Role',  # CORRIGIDO: era Story-Robert-McKee (errado)
            'psychology': 'Story-Robert-McKee',
            'psychemon': 'Story-Robert-McKee',
            'subtext': 'Dialogue-_-The-Art-of-Verbal-Action',
            'submon': 'Dialogue-_-The-Art-of-Verbal-Action',
            'theme': 'the-art-of-dramatic-writing',  # Egri - premise is king!
            'thememon': 'the-art-of-dramatic-writing',
            'structure': 'making-a-good-script-great',  # Linda Seger - 732 menções, turning points, catalyst
            'pacing': 'Story-Robert-McKee',
            'action': 'Story-Robert-McKee',  # McKee - extensive action design coverage
            'actionmon': 'Story-Robert-McKee',
            'conflict': 'Story-Robert-McKee',  # McKee - extensive conflict design (gap between expectation and result)
            'conflictmon': 'Story-Robert-McKee',
            'tension': 'Story-Robert-McKee',  # McKee - extensive tension/suspense coverage (gap between expectation)
            'tensionmon': 'Story-Robert-McKee',
            'exposition': 'Story-Robert-McKee',  # McKee - extensive exposition coverage (exposition is dullest of all screen tasks)
            'expositionmon': 'Story-Robert-McKee',
            'transitions': 'Story-Robert-McKee',  # McKee/Field/Seger - scene transitions, smooth flow, continuity
            'transitionsmon': 'Story-Robert-McKee',
            'opening': 'save_the_cat',
            'climax': 'Story-Robert-McKee',  # McKee - climax ultimate confrontation, theme expressed, peak tension
            'resolution': 'Story-Robert-McKee',  # McKee - resolution denouement, threads closed, emotional satisfaction
            'worldbuilding': 'Story-Robert-McKee',  # McKee - world-building, setting design, visual storytelling
            'worldbuildingmon': 'Story-Robert-McKee',
            'stakes': 'Story-Robert-McKee',  # McKee - stakes, consequences, what's at risk, audience investment
            'stakesmon': 'Story-Robert-McKee',
            'motivation': 'the-anatomy-of-story',  # Truby - want, need, desire line, ghost, moral weakness
            'motivationmon': 'the-anatomy-of-story',
            'backstory': 'Story-Robert-McKee',  # McKee - backstory revelation, drip-feed technique, weave not dump, strategic timing
            'backstorymon': 'Story-Robert-McKee',
            'foreshadowing': 'Story-Robert-McKee',  # McKee - foreshadowing setup/payoff, plant/reveal, dramatic irony, inevitability
            'foreshadowingmon': 'Story-Robert-McKee',
            'twist': 'Story-Robert-McKee',  # McKee - twist revelation, surprise yet inevitable, earned twist, misdirection
            'twistmon': 'Story-Robert-McKee',
            'symbolism': 'Story-Robert-McKee',  # McKee - symbolism, visual metaphor, motif, thematic resonance, avoid heavy-handed
            'symbolismon': 'Story-Robert-McKee',
            'tone': 'Story-Robert-McKee',  # McKee - tone consistency, atmosphere, mood, voice, avoid inconsistent/tone-deaf moments
            'tonemon': 'Story-Robert-McKee',
            'genre': 'save_the_cat',  # Snyder - genre types, conventions, expectations, tropes, deliver promises
            'genremon': 'save_the_cat',
            'evaluator': 'Story-Robert-McKee',  # McKee - overall quality evaluation, industry standards, professional assessment
            'evaluatormon': 'Story-Robert-McKee',
            'originality': 'Story-Robert-McKee',

            # Por autor específico (para análises multi-autor)
            'mckee': 'st_o_r_y',
            'mckee_story': 'st_o_r_y',
            'mckee_character': 'Character-_-The-Art-of-Role',
            'mckee_dialogue': 'Dialogue-_-The-Art-of-Verbal',
            'truby': 'anatomy_of_story_22_steps',
            'campbell': 'heroi-de-mil-faces',
            'vogler': 'writers_journey_mythic',
            'seger': 'making-a-good-script-great',  # Linda Seger - turning points, catalyst
            'field': 'screenplay_the_foundations',  # Syd Field - paradigma, plot points
            'snyder': 'save_the_cat',  # Blake Snyder - beats, midpoint
            'egri': 'art_of_dramatic_writing',
            'weiland': 'creating_character_arcs',
            'aristotle': 'ontology_and_the_art',
            'cowgill': 'writing_short_films'
        }

        # 1. Se specialist_type fornecido, usar mapeamento direto
        if specialist_type and specialist_type in SPECIALIST_BOOK_MAP:
            preferred_book = SPECIALIST_BOOK_MAP[specialist_type]

            # Buscar livro preferido nos chunks
            for book_name in self.books.keys():
                if preferred_book in book_name:
                    primary_book_name = book_name
                    primary_book = self._load_full_book(primary_book_name)

                    if primary_book:
                        # Busca highlights relevantes para query
                        matches = self.search(query, limit=20, book_filter=primary_book_name)
                        top_chunks = matches[:5] if matches else []
                        primary_book['highlights'] = top_chunks

                        return {
                            'primary_book': primary_book,
                            'total_words': primary_book['word_count'],
                            'estimated_tokens': int(primary_book['word_count'] * 1.3),
                            'query': query,
                            'specialist_type': specialist_type,
                            'relevance_score': 100,  # Mapeamento direto
                            'method': 'specialist_mapping'
                        }

        # 2. Fallback: Busca chunks para identificar livro mais relevante (método original)
        matches = self.search(query, limit=20)

        if not matches:
            return {'primary_book': None, 'total_words': 0, 'estimated_tokens': 0}

        # 3. Agrupa por livro e calcula score total
        book_scores = {}
        for match in matches:
            book = match['book']
            book_scores[book] = book_scores.get(book, 0) + match['score']

        # 4. Ordena livros por relevância
        ranked_books = sorted(book_scores.items(), key=lambda x: x[1], reverse=True)

        # 5. Carrega livro(s) completo(s)
        primary_book_name = ranked_books[0][0]
        primary_book = self._load_full_book(primary_book_name)

        # 5. Identifica top chunks como "highlights"
        top_chunks = [m for m in matches if m['book'] == primary_book_name][:5]
        primary_book['highlights'] = top_chunks

        result = {
            'primary_book': primary_book,
            'total_words': primary_book['word_count'],
            'estimated_tokens': int(primary_book['word_count'] * 1.3),  # ~1.3 tokens/palavra
            'query': query,
            'relevance_score': ranked_books[0][1]
        }

        return result

    def _load_full_book(self, book_name: str) -> Dict:
        """Carrega texto completo de um livro"""
        if book_name not in self.books:
            return None

        book_info = self.books[book_name]
        book_path = book_info['path']

        try:
            full_text = book_path.read_text(encoding='utf-8', errors='ignore')
        except Exception as e:
            print(f"❌ Erro ao ler livro completo {book_name}: {e}")
            return None

        return {
            'name': book_name,
            'path': str(book_path),
            'full_text': full_text,
            'word_count': len(full_text.split()),
            'char_count': len(full_text),
            'total_chunks': book_info['total_chunks']
        }

    def get_stats(self) -> Dict:
        """Retorna estatísticas do índice"""
        return {
            'books_indexed': len(self.books),
            'total_chunks': sum(len(c) for c in self.chunks.values()),
            'total_words': sum(b['total_words'] for b in self.books.values()),
            'cache_size': len(self._search_cache),
            'books': list(self.books.keys())
        }


# Instância global (singleton pattern)
_global_indexer = None


def get_theory_indexer(specialist_type: str = 'dialogue', force_reload: bool = False) -> TheoryIndexer:
    """
    Retorna instância global do indexer (lazy loading).

    Args:
        specialist_type: Tipo de especialista
            - 'dialogue', 'structure', 'character', etc → Indexa livro(s) específico(s)
            - 'all' → Indexa TODOS os 13 livros disponíveis
        force_reload: Se True, força recriação do indexer mesmo que já exista

    Returns:
        TheoryIndexer com livro(s) apropriado(s) indexado(s)
    """
    global _global_indexer

    # Resetar indexer se force_reload=True
    if force_reload:
        _global_indexer = None

    if _global_indexer is None:
        _global_indexer = TheoryIndexer()

        if specialist_type == 'all':
            # MODO ALL: Indexar TODOS os livros disponíveis
            print("📚 Modo ALL: Indexando TODOS os livros de teoria...")
            _global_indexer.index_all_theory()
        else:
            # MODO SELETIVO: Mapear specialist_type para livros específicos
            book_mapping = {
                # Por tipo de especialista (ENRIQUECIDO com múltiplos livros)
                'dialogue': [
                    "Dialogue-_-The-Art-of-Verbal-Action-for-Page_-Stage_-and-Robert-MacKee.txt",  # Score: 100.0
                    "writing_short_films_structure_and_content_for_screenwriters_--_linda_j_cowgill.txt",  # Score: 69.3
                    "the_anatomy_of_story_22_steps_to_becoming_a_master_-_john_truby.txt",  # Score: 59.0
                    "screenplay_the_foundations_of_screenwriting_-_syd_field.txt",  # Score: 35.4
                    "making-a-good-script-great_-revised-_-expanded-seger_-linda-3_-ed_-rev_-_-expanded_-_1_-silman-jame.docx.txt",  # Score: 31.2
                    "st_o_r_y.txt",  # Score: 26.3
                    "the_art_of_dramatic_writing_its_basis_in_the_creative_-_lajos_egri.txt",  # Score: 21.6
                ],
                'structure': [
                    "making-a-good-script-great_-revised-_-expanded-seger_-linda-3_-ed_-rev_-_-expanded_-_1_-silman-jame.docx.txt",  # Seger - 732 menções (turning points, catalyst)
                    "st_o_r_y.txt",  # McKee - 626 menções (inciting incident, climax)
                    "screenplay_the_foundations_of_screenwriting_-_syd_field.txt",  # Field - 419 menções (paradigma, plot points)
                    "save_the_cat.txt",  # Snyder - 391 menções (beats, midpoint, all is lost)
                ],
                'character': ["Character-_-The-Art-of-Role-and-Cast-Design-for-Page_-Stage_-Robert-D-McKee.txt"],
                'pacing': ["st_o_r_y.txt"],
                'theme': ["the_art_of_dramatic_writing_its_basis_in_the_creative_-_lajos_egri.txt"],  # Egri - premise is foundation
                'action': ["st_o_r_y.txt"],  # McKee - action design, visual storytelling, active protagonist
                'conflict': ["st_o_r_y.txt"],  # McKee - conflict design, gap between expectation and result, antagonistic force
                'tension': ["st_o_r_y.txt"],  # McKee - tension/suspense, gap between expectation and result, dramatic question
                'exposition': ["st_o_r_y.txt"],  # McKee - exposition dramatic vs expositional, never stop action to explain, backstory revelation
                'transitions': ["st_o_r_y.txt", "screenplay_the_foundations_of_screenwriting_-_syd_field.txt", "making-a-good-script-great_-revised-_-expanded-seger_-linda-3_-ed_-rev_-_-expanded_-_1_-silman-jame.docx.txt"],  # McKee/Field/Seger - scene transitions, smooth flow, continuity, avoid jarring cuts
                'psychology': ["Character-_-The-Art-of-Role-and-Cast-Design-for-Page_-Stage_-Robert-D-McKee.txt"],
                'subtext': ["Dialogue-_-The-Art-of-Verbal-Action-for-Page_-Stage_-and-Robert-MacKee.txt"],
                'opening': ["st_o_r_y.txt", "save_the_cat.txt"],
                'climax': ["st_o_r_y.txt"],  # McKee - climax ultimate confrontation, theme expressed at climax, peak tension, all forces converge
                'resolution': ["st_o_r_y.txt"],  # McKee - resolution denouement, all threads closed, emotional satisfaction, new equilibrium
                'worldbuilding': ["st_o_r_y.txt", "the-anatomy-of-story.txt"],  # McKee (world-building, setting design) + Truby (world rules, genre worldbuilding)
                'stakes': ["st_o_r_y.txt", "the-anatomy-of-story.txt", "save_the_cat.txt"],  # McKee (stakes, consequences) + Truby (personal stakes, desire) + Snyder (stakes escalation)
                'motivation': ["the_anatomy_of_story_22_steps_to_becoming_a_master_-_john_truby.txt", "st_o_r_y.txt", "Character-_-The-Art-of-Role-and-Cast-Design-for-Page_-Stage_-Robert-D-McKee.txt"],  # Truby (want, need, desire line, ghost) + McKee (desire drives action) + McKee Character (character motivation)
                'backstory': ["st_o_r_y.txt", "the_anatomy_of_story_22_steps_to_becoming_a_master_-_john_truby.txt", "making-a-good-script-great_-revised-_-expanded-seger_-linda-3_-ed_-rev_-_-expanded_-_1_-silman-jame.docx.txt"],  # McKee (backstory revelation, drip-feed, weave not dump) + Truby (ghost, strategic timing) + Seger (show don't tell backstory)
                'foreshadowing': ["st_o_r_y.txt", "screenplay_the_foundations_of_screenwriting_-_syd_field.txt", "the-anatomy-of-story.txt"],  # McKee (setup/payoff, plant/reveal, dramatic irony, inevitability) + Field (plant Act 1 payoff Act 3, structural distance) + Truby (revelation sequence, foreshadowing design)
                'twist': ["st_o_r_y.txt", "the-anatomy-of-story.txt", "poetics-aristotle.txt"],  # McKee (twist revelation, surprise yet inevitable, earned twist, misdirection) + Truby (revelation sequence) + Aristotle (peripeteia/anagnorisis)
                'symbolism': ["st_o_r_y.txt", "the-anatomy-of-story.txt", "poetics-aristotle.txt", "making-a-good-script-great_-revised-_-expanded-seger_-linda-3_-ed_-rev_-_-expanded_-_1_-silman-jame.docx.txt"],  # McKee (symbolism, visual metaphor, motif, thematic resonance) + Truby (symbol web, thematic network) + Aristotle (metaphor, representation) + Seger (visual storytelling, symbolic imagery)
                'tone': ["st_o_r_y.txt", "making-a-good-script-great_-revised-_-expanded-seger_-linda-3_-ed_-rev_-_-expanded_-_1_-silman-jame.docx.txt", "save_the_cat.txt"],  # McKee (tone consistency, atmosphere, mood, voice, avoid inconsistent/tone-deaf) + Seger (tone establishment, opening tone) + Snyder (tone genre expectations)
                'genre': ["save_the_cat.txt", "st_o_r_y.txt", "screenplay_the_foundations_of_screenwriting_-_syd_field.txt"],  # Snyder (genre types, conventions, expectations, tropes, deliver promises) + McKee (genre design conventions) + Field (genre structure conventions)
                'evaluator': ["st_o_r_y.txt", "making-a-good-script-great_-revised-_-expanded-seger_-linda-3_-ed_-rev_-_-expanded_-_1_-silman-jame.docx.txt", "screenplay_the_foundations_of_screenwriting_-_syd_field.txt"],  # McKee (overall quality, industry standards, professional assessment) + Seger (evaluation criteria, strengths/weaknesses identification) + Field (professional standards, industry readiness)
                'relationships': ["Character-_-The-Art-of-Role-and-Cast-Design-for-Page_-Stage_-Robert-D-McKee.txt"],
                'arcs': ["Character-_-The-Art-of-Role-and-Cast-Design-for-Page_-Stage_-Robert-D-McKee.txt", "the_anatomy_of_story_22_steps_to_becoming_a_master_-_john_truby.txt"],

                # Por autor específico
                'mckee': ["st_o_r_y.txt"],
                'mckee_story': ["st_o_r_y.txt"],
                'mckee_character': ["Character-_-The-Art-of-Role-and-Cast-Design-for-Page_-Stage_-Robert-D-McKee.txt"],
                'mckee_dialogue': ["Dialogue-_-The-Art-of-Verbal-Action-for-Page_-Stage_-and-Robert-MacKee.txt"],
                'truby': ["the_anatomy_of_story_22_steps_to_becoming_a_master_-_john_truby.txt"],
                'campbell': ["o-heroi-de-mil-faces-_alta-qualidade_atbc_-jonathan-c_-young_-joseph-campbell-paperback_-1995-cult.docx.txt"],
                'vogler': ["the_writers_journey_mythic_structure_for_writers_2nd.txt"],
                'seger': ["making-a-good-script-great_-revised-_-expanded-seger_-linda-3_-ed_-rev_-_-expanded_-_1_-silman-jame.docx.txt"],  # Seger - turning points
                'field': ["screenplay_the_foundations_of_screenwriting_-_syd_field.txt"],  # Field - paradigma
                'snyder': ["save_the_cat.txt"],  # Snyder - beats, midpoint
                'egri': ["the_art_of_dramatic_writing_its_basis_in_the_creative_-_lajos_egri.txt"],
                'weiland': ["creating_character_arcs_the_masterful_author_s_guide.txt"],
                'aristotle': ["ontology_and_the_art_of_tragedy_an_approach_to_aristotle_s.txt"],
                'cowgill': ["writing_short_films_structure_and_content_for_screenwriters_--_linda_j_cowgill.txt"],
            }

            # Obter lista de livros para este tipo
            book_files = book_mapping.get(specialist_type, ["Dialogue-_-The-Art-of-Verbal-Action-for-Page_-Stage_-and-Robert-MacKee.txt"])

            # Indexar os livros
            for book_name in book_files:
                book_path = _global_indexer.theory_dir / book_name
                if book_path.exists():
                    # Evitar duplicação (cache global)
                    if book_path.stem not in _global_indexer.books:
                        _global_indexer.index_book(book_path, chunk_size=500)
                else:
                    print(f"⚠️ Livro não encontrado: {book_path}")

    return _global_indexer


if __name__ == "__main__":
    # Teste do indexer
    print("🔥 TESTE: Theory Indexer\n")

    indexer = get_theory_indexer()

    print(f"\n📊 Stats: {indexer.get_stats()}\n")

    # Teste de busca
    print("🔍 Buscando: 'subtext'")
    results = indexer.search("subtext", limit=2)

    for r in results:
        print(f"\n{r['context']} (score: {r['score']})")
        print(r['text'][:300] + "...")
