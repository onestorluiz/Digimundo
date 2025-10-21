#!/usr/bin/env python3
"""
Scripturemon - Análise com TODOS os 24 Especialistas × 13 Autores = 312 Análises
Sistema com CHECKPOINT para continuar de onde parou

FASE 3.5 ENRICHMENT: Todos os especialistas agora têm 78-113 queries profundas.
Cada especialista analisa com TODOS os 13 autores teóricos.

Uso:
    python analyze_all_specialists.py <roteiro.pdf> [--yes] [--resume]

Flags:
    --yes    : Não pedir confirmação (modo automático)
    --resume : Continuar de checkpoint anterior (automático se detectar)

Estrutura de saída:
    ROTEIRO_all_specialists_0001/
    ├── 1_individuais/
    │   ├── CHARACTER/
    │   │   ├── ANALISE_CHARACTER_MCKEE_20251011.html
    │   │   ├── ANALISE_CHARACTER_FIELD_20251011.html
    │   │   └── ... (13 HTMLs)
    │   ├── DIALOGUE/
    │   └── ... (24 especialistas)
    ├── 2_logs/
    │   └── checkpoint.json  ← CHECKPOINT AUTOMÁTICO
    └── 3_consolidados/
        ├── CONSOLIDADO_CHARACTER_20251011.html  (13 autores → 1 HTML)
        └── ... (24 consolidados)

Tempo estimado: ~13 horas (24 × 13 × 2min)
"""

import sys
from pathlib import Path
import time
from datetime import datetime
import json
import re
import shutil
from typing import Dict, List, Any, Optional

# Add path for imports
sys.path.insert(0, str(Path(__file__).parent))

# Import all 24 specialists
from engine.analyzers.dr_character import DrCharacter
from engine.analyzers.dr_structure import DrStructure
from engine.analyzers.dr_pacing import DrPacing
from engine.analyzers.dr_conflict import DrConflict
from engine.analyzers.dr_action import DrAction
from engine.analyzers.dr_theme import DrTheme
from engine.analyzers.dr_tension import DrTension
from engine.analyzers.dr_opening import DrOpening
from engine.analyzers.dr_transitions import DrTransitions
from engine.analyzers.dr_stakes import DrStakes
from engine.analyzers.dr_worldbuilding import DrWorldbuilding
from engine.analyzers.dr_exposition import DrExposition
from engine.analyzers.dr_subtext import DrSubtext
from engine.analyzers.dr_climax import DrClimax
from engine.analyzers.dr_dialogue import DrDialogue
from engine.analyzers.dr_genre import DrGenre
from engine.analyzers.dr_resolution import DrResolution
from engine.analyzers.dr_motivation import DrMotivation
from engine.analyzers.dr_backstory import DrBackstory
from engine.analyzers.dr_foreshadowing import DrForeshadowing
from engine.analyzers.dr_twist import DrTwist
from engine.analyzers.dr_symbolism import DrSymbolism
from engine.analyzers.dr_tone import DrTone
from engine.analyzers.dr_evaluator import DrEvaluator

from triple_core.orchestrators.triple_core_wrapper import TripleCoreWrapper
from consolidate_analyses import consolidate_html_analyses

# Import GPT-5 self-evaluator (optional, only for GPT models)
try:
    from engine.gpt5_self_evaluator import run_self_evaluation
    GPT5_SELF_EVAL_AVAILABLE = True
except ImportError:
    GPT5_SELF_EVAL_AVAILABLE = False


# ============================================================================
# 13 AUTORES TEÓRICOS (from analyze.py)
# ============================================================================

AUTHORS = [
    'mckee',           # Story by Robert McKee
    'field',           # Screenplay by Syd Field
    'truby',           # The Anatomy of Story by John Truby
    'campbell',        # The Hero's Journey by Joseph Campbell
    'vogler',          # The Writer's Journey by Christopher Vogler
    'seger',           # Making a Good Script Great by Linda Seger
    'snyder',          # Save the Cat by Blake Snyder
    'egri',            # The Art of Dramatic Writing by Lajos Egri
    'weiland',         # Creating Character Arcs by K.M. Weiland
    'aristotle',       # Poetics by Aristotle
    'cowgill',         # Writing Short Films by Linda J. Cowgill
    'mckee_character', # Character by Robert McKee
    'mckee_dialogue',  # Dialogue by Robert McKee
]


# ============================================================================
# 24 ESPECIALISTAS (FASE 3 - Complete set)
# ============================================================================

ALL_SPECIALISTS = [
    ('character', DrCharacter, 'character arc, transformation, dimensional depth'),
    ('structure', DrStructure, 'three-act structure, plot points, beats'),
    ('theme', DrTheme, 'controlling idea, premise, thematic consistency'),
    ('genre', DrGenre, 'conventions, expectations, audience contract'),
    ('pacing', DrPacing, 'rhythm, momentum, scene length control'),
    ('transitions', DrTransitions, 'scene connections, act breaks, flow'),
    ('opening', DrOpening, 'hook, world establishment, first impression'),
    ('climax', DrClimax, 'ultimate confrontation, peak tension'),
    ('resolution', DrResolution, 'denouement, threads closed, satisfaction'),
    ('conflict', DrConflict, 'internal/external conflict, escalation'),
    ('tension', DrTension, 'suspense, dramatic irony, anticipation'),
    ('stakes', DrStakes, 'personal/external/moral stakes escalation'),
    ('action', DrAction, 'visual action, set pieces, choreography'),
    ('motivation', DrMotivation, 'want vs need, driving force, goal clarity'),
    ('backstory', DrBackstory, 'reveal timing, weaving, relevance'),
    ('dialogue', DrDialogue, 'subtext, rhythm, character voice'),
    ('subtext', DrSubtext, 'what is unsaid, layered meaning'),
    ('worldbuilding', DrWorldbuilding, 'rules, consistency, immersion'),
    ('exposition', DrExposition, 'information delivery, show vs tell'),
    ('symbolism', DrSymbolism, 'metaphor, motif, thematic reinforcement'),
    ('foreshadowing', DrForeshadowing, 'setup, payoff, dramatic irony'),
    ('twist', DrTwist, 'surprise, inevitability, revelations'),
    ('tone', DrTone, 'atmosphere, mood, consistency'),
    ('evaluator', DrEvaluator, 'overall quality, marketability, readiness'),
]


# ============================================================================
# CHECKPOINT SYSTEM
# ============================================================================

class CheckpointManager:
    """Gerencia salvamento e restauração de progresso"""

    def __init__(self, checkpoint_path: Path):
        self.checkpoint_path = checkpoint_path
        self.data = self._load()

    def _load(self) -> Dict:
        """Carrega checkpoint existente"""
        if self.checkpoint_path.exists():
            try:
                with open(self.checkpoint_path, 'r') as f:
                    return json.load(f)
            except:
                return self._new_checkpoint()
        return self._new_checkpoint()

    def _new_checkpoint(self) -> Dict:
        """Cria novo checkpoint vazio"""
        return {
            'version': '2.0',
            'started_at': datetime.now().isoformat(),
            'last_update': None,
            'total_analyses': 24 * 13,  # 312
            'completed': [],  # Lista de (specialist, author) completos
            'failed': [],     # Lista de falhas
            'current_specialist': None,
            'current_author': None,
        }

    def save(self):
        """Salva checkpoint atual"""
        self.data['last_update'] = datetime.now().isoformat()
        with open(self.checkpoint_path, 'w') as f:
            json.dump(self.data, f, indent=2)

    def is_completed(self, specialist: str, author: str) -> bool:
        """Verifica se análise já foi feita"""
        return [specialist, author] in self.data['completed']

    def mark_completed(self, specialist: str, author: str, result: Dict):
        """Marca análise como completa"""
        if not self.is_completed(specialist, author):
            self.data['completed'].append([specialist, author])
        self.data['current_specialist'] = specialist
        self.data['current_author'] = author
        self.save()

    def mark_failed(self, specialist: str, author: str, error: str):
        """Marca análise como falha"""
        self.data['failed'].append({
            'specialist': specialist,
            'author': author,
            'error': error,
            'timestamp': datetime.now().isoformat()
        })
        self.save()

    def get_progress(self) -> tuple:
        """Retorna (completado, total)"""
        return (len(self.data['completed']), self.data['total_analyses'])

    def get_resume_point(self) -> Optional[tuple]:
        """Retorna (specialist_index, author_index) para resumir"""
        if not self.data['completed']:
            return None

        last_specialist, last_author = self.data['completed'][-1]

        # Encontrar índices
        specialist_idx = next((i for i, (name, _, _) in enumerate(ALL_SPECIALISTS) if name == last_specialist), 0)
        author_idx = next((i for i, name in enumerate(AUTHORS) if name == last_author), 0)

        # Próximo author
        author_idx += 1
        if author_idx >= len(AUTHORS):
            author_idx = 0
            specialist_idx += 1

        if specialist_idx >= len(ALL_SPECIALISTS):
            return None  # Tudo completo!

        return (specialist_idx, author_idx)


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def sanitize_filename(name: str) -> str:
    """Remove caracteres inválidos do nome do arquivo."""
    name = re.sub(r'[^\w\s-]', '', name)
    name = re.sub(r'\s+', '_', name)
    return name.upper()


def get_next_analysis_number(base_dir: Path, screenplay_name: str, specialist: str) -> int:
    """Encontra o próximo número disponível para análise."""
    pattern = f"{screenplay_name}_{specialist}_*"
    existing = list(base_dir.glob(pattern))

    if not existing:
        return 1

    numbers = []
    for folder in existing:
        parts = folder.name.split('_')
        if parts and parts[-1].isdigit():
            numbers.append(int(parts[-1]))

    return max(numbers) + 1 if numbers else 1


def find_latest_analysis_folder(screenplay_path: str, specialist_type: str = 'all_specialists') -> Optional[Path]:
    """
    Encontra a pasta de análise mais recente com checkpoint para continuar.
    Ordena por data de modificação do checkpoint (mais recente primeiro).
    """
    screenplay_name = sanitize_filename(Path(screenplay_path).stem)
    base_dir = Path('workspace/outputs')

    if not base_dir.exists():
        return None

    # Procurar todas as pastas deste roteiro que tenham checkpoint
    pattern = f"{screenplay_name}_{specialist_type}_*"
    candidates = []

    for folder in base_dir.glob(pattern):
        checkpoint_path = folder / "2_logs" / "checkpoint.json"
        if checkpoint_path.exists():
            # Adicionar com timestamp de modificação
            mod_time = checkpoint_path.stat().st_mtime
            candidates.append((mod_time, folder))

    if not candidates:
        return None

    # Ordenar por data de modificação (mais recente primeiro) e retornar
    candidates.sort(reverse=True, key=lambda x: x[0])
    return candidates[0][1]


def create_analysis_structure(screenplay_path: str, specialist_type: str = 'all_specialists', resume_folder: Optional[Path] = None) -> Dict[str, Path]:
    """
    Cria estrutura organizada de pastas para análises múltiplas.
    Se resume_folder é fornecido, reutiliza pasta existente.
    """
    if resume_folder:
        # Reutilizar pasta existente
        root_folder = resume_folder
        individuais = root_folder / "1_individuais"
        logs = root_folder / "2_logs"
        consolidados = root_folder / "3_consolidados"

        # Garantir que subpastas existem
        individuais.mkdir(exist_ok=True)
        logs.mkdir(exist_ok=True)
        consolidados.mkdir(exist_ok=True)
    else:
        # Criar nova pasta
        screenplay_name = sanitize_filename(Path(screenplay_path).stem)
        base_dir = Path('workspace/outputs')
        base_dir.mkdir(parents=True, exist_ok=True)

        # Encontrar próximo número disponível
        number = get_next_analysis_number(base_dir, screenplay_name, specialist_type)

        # Criar pasta principal
        root_folder = base_dir / f"{screenplay_name}_{specialist_type}_{number:04d}"
        root_folder.mkdir(exist_ok=True)

        # Criar subpastas organizadas
        individuais = root_folder / "1_individuais"
        logs = root_folder / "2_logs"
        consolidados = root_folder / "3_consolidados"

        individuais.mkdir(exist_ok=True)
        logs.mkdir(exist_ok=True)
        consolidados.mkdir(exist_ok=True)

    return {
        'root': root_folder,
        'individuais': individuais,
        'logs': logs,
        'consolidados': consolidados
    }


def print_header():
    """Print header with system info"""
    print('='*80)
    print('  🎬 SCRIPTUREMON - ANÁLISE COMPLETA COM 24 ESPECIALISTAS × 13 AUTORES')
    print('='*80)
    print()
    print('📊 Sistema: 24 Script Doctors enriquecidos (78-113 queries cada)')
    print('📚 Contexto: 13 autores teóricos por especialista (deep context)')
    print('⚡ Total: 24 × 13 = 312 análises individuais')
    print('⏱️  Tempo estimado: ~13 horas (pode variar)')
    print('💾 Checkpoint: Salvo após cada análise (pode resumir se parar)')
    print()
    print('='*80)
    print()


# ============================================================================
# ANÁLISE INDIVIDUAL (Specialist × Author)
# ============================================================================

def analyze_specialist_with_author(
    specialist_name: str,
    specialist_class: type,
    specialist_focus: str,
    author: str,
    screenplay_text: str,
    screenplay_path: str,
    folders: Dict[str, Path],
    checkpoint: CheckpointManager,
    llm_model: str = "scripturemon-optimized"
) -> Dict[str, Any]:
    """
    Analisa com 1 especialista usando 1 autor teórico.
    Retorna resultado da análise.
    """

    # Verificar se já foi feito
    if checkpoint.is_completed(specialist_name, author):
        print(f"   ⏭️  {author.upper()}: JÁ COMPLETO (pulando)")
        return {'skipped': True, 'specialist': specialist_name, 'author': author}

    print(f"\n   📖 [{author.upper()}] Iniciando análise...")
    start_time = time.time()

    try:
        # Initialize specialist
        specialist = specialist_class()

        # Wrap with Triple-Core usando este AUTOR específico
        wrapper = TripleCoreWrapper(
            python_specialist=specialist,
            llm_model=llm_model,
            deep_context=True,
            use_theory=True,
            two_pass_llm=True,
            use_personalized_prompts=True,
            specialist_type=author  # ← AUTOR ESPECÍFICO!
        )

        # Analyze with screenplay TEXT (not path!)
        result = wrapper.analyze(screenplay_text)
        elapsed = time.time() - start_time

        # Extract info
        success = result.get('llm_success', False)
        quality = result.get('quality_score', 0)

        # Export HTML individual
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Criar subpasta para este especialista
        specialist_folder = folders['individuais'] / specialist_name.upper()
        specialist_folder.mkdir(exist_ok=True)

        html_filename = f"ANALISE_{specialist_name.upper()}_{author.upper()}_{timestamp}.html"
        html_path = specialist_folder / html_filename

        # Generate HTML
        temp_html = wrapper.export_formatted(
            result,
            screenplay_title=f"{Path(screenplay_path).stem}_{specialist_name.upper()}_{author.upper()}",
            format="html"
        )

        # Move to organized folder
        shutil.move(str(temp_html), str(html_path))

        print(f"   ✅ {author.upper()}: Completo em {elapsed:.1f}s (Q: {quality:.1f}/10)")

        # Salvar checkpoint
        checkpoint.mark_completed(specialist_name, author, {
            'time': elapsed,
            'quality': quality,
            'html_path': str(html_path)
        })

        return {
            'specialist': specialist_name,
            'author': author,
            'success': True,
            'time_seconds': elapsed,
            'quality_score': quality,
            'html_path': html_path,
        }

    except Exception as e:
        elapsed = time.time() - start_time
        print(f"   ❌ {author.upper()}: ERRO - {e}")

        checkpoint.mark_failed(specialist_name, author, str(e))

        return {
            'specialist': specialist_name,
            'author': author,
            'success': False,
            'error': str(e),
            'time_seconds': elapsed
        }


# ============================================================================
# ANÁLISE COMPLETA DE 1 ESPECIALISTA (× 13 autores)
# ============================================================================

def analyze_one_specialist_all_authors(
    specialist_name: str,
    specialist_class: type,
    specialist_focus: str,
    screenplay_text: str,
    screenplay_path: str,
    folders: Dict[str, Path],
    checkpoint: CheckpointManager,
    start_from_author_idx: int = 0,
    llm_model: str = "scripturemon-optimized"
) -> Dict[str, Any]:
    """
    Analisa com 1 especialista usando TODOS os 13 autores.
    Retorna estatísticas agregadas.
    """

    print(f"\n{'='*80}")
    print(f"🔬 Dr{specialist_name.title()} - {specialist_focus}")
    print(f"{'='*80}\n")
    print(f"📚 Analisando com {len(AUTHORS)} autores teóricos...")

    results = []
    total_time = 0

    for i, author in enumerate(AUTHORS):
        if i < start_from_author_idx:
            continue  # Pular autores já completos

        result = analyze_specialist_with_author(
            specialist_name=specialist_name,
            specialist_class=specialist_class,
            specialist_focus=specialist_focus,
            author=author,
            screenplay_text=screenplay_text,
            screenplay_path=screenplay_path,  # Keep for title/filename
            folders=folders,
            checkpoint=checkpoint,
            llm_model=llm_model
        )

        if not result.get('skipped'):
            results.append(result)
            total_time += result.get('time_seconds', 0)

    # Consolidar os 13 HTMLs deste especialista em 1
    print(f"\n   🔄 Consolidando {len(AUTHORS)} análises de Dr{specialist_name.title()}...")
    try:
        specialist_folder = folders['individuais'] / specialist_name.upper()

        # Temporariamente copiar para pasta formatted (onde consolidate_html_analyses procura)
        temp_dir = Path('workspace/outputs/formatted')
        temp_dir.mkdir(parents=True, exist_ok=True)

        for html_file in specialist_folder.glob('*.html'):
            shutil.copy(str(html_file), str(temp_dir / html_file.name))

        # Consolidar
        consolidated_html = consolidate_html_analyses(
            pattern=f'ANALISE_{specialist_name.upper()}_*',
            output_name=f'CONSOLIDADO_{specialist_name.upper()}',
            translate=True
        )

        # Mover para 3_consolidados
        final_path = folders['consolidados'] / consolidated_html.name
        shutil.move(str(consolidated_html), str(final_path))

        # Limpar temp
        for html_file in temp_dir.glob(f'ANALISE_{specialist_name.upper()}_*'):
            html_file.unlink()

        print(f"   ✅ Consolidado salvo: {final_path.name}")

    except Exception as e:
        print(f"   ⚠️  Erro ao consolidar: {e}")

    print(f"\n✅ Dr{specialist_name.title()} COMPLETO!")
    print(f"⏱️  Tempo total: {total_time/60:.1f} min")
    print(f"📊 Análises bem-sucedidas: {sum(1 for r in results if r.get('success'))}/{len(results)}")

    return {
        'specialist': specialist_name,
        'total_time': total_time,
        'results': results,
        'success_rate': sum(1 for r in results if r.get('success')) / len(results) if results else 0
    }


# ============================================================================
# MAIN
# ============================================================================

def main():
    """Main execution"""

    if len(sys.argv) < 2:
        print("Uso: python analyze_all_specialists.py <roteiro.pdf> [--yes] [--resume] [--model MODEL] [--self-eval]")
        print("\nFlags:")
        print("  --yes         : Não pedir confirmação (modo automático)")
        print("  --resume      : Continuar de checkpoint (automático se detectar)")
        print("  --model MODEL : Modelo LLM (padrão: scripturemon-optimized, ex: gpt-5)")
        print("  --self-eval   : Executar auto-avaliação GPT-5 após análise (só GPT-5)")
        print("\nExemplo:")
        print("  python analyze_all_specialists.py inputs/examples/meu_roteiro.pdf --yes")
        print("  python analyze_all_specialists.py inputs/examples/meu_roteiro.pdf --model gpt-5 --self-eval --yes")
        sys.exit(1)

    screenplay_path = sys.argv[1]
    auto_confirm = '--yes' in sys.argv or '-y' in sys.argv
    force_resume = '--resume' in sys.argv
    enable_self_eval = '--self-eval' in sys.argv

    # Parse --model argument
    llm_model = "scripturemon-optimized"  # default - updated 2025-10-14 with Perplexity AI optimizations
    if '--model' in sys.argv:
        model_idx = sys.argv.index('--model')
        if model_idx + 1 < len(sys.argv):
            llm_model = sys.argv[model_idx + 1]

    if not Path(screenplay_path).exists():
        print(f"❌ Erro: Roteiro não encontrado: {screenplay_path}")
        sys.exit(1)

    print_header()

    print(f"📄 Roteiro: {screenplay_path}")
    print(f"🤖 Modelo LLM: {llm_model}")
    print(f"🔬 Especialistas: {len(ALL_SPECIALISTS)}")
    print(f"📚 Autores por especialista: {len(AUTHORS)}")
    print(f"📊 Total de análises: {len(ALL_SPECIALISTS)} × {len(AUTHORS)} = {len(ALL_SPECIALISTS) * len(AUTHORS)}")
    if enable_self_eval and llm_model.startswith('gpt-'):
        print(f"🤖 Auto-avaliação GPT-5: ATIVADA")
    print()

    # Criar estrutura de pastas (ou reusar existente se --resume)
    resume_folder = None
    if force_resume:
        print('🔍 Procurando análise anterior para continuar...')
        resume_folder = find_latest_analysis_folder(screenplay_path, 'all_specialists')
        if resume_folder:
            print(f'   ✅ Encontrada: {resume_folder.name}')
        else:
            print('   ⚠️  Nenhuma análise anterior encontrada. Criando nova...')

    if not resume_folder:
        print('📁 Criando estrutura de pastas...')

    folders = create_analysis_structure(
        screenplay_path=screenplay_path,
        specialist_type='all_specialists',
        resume_folder=resume_folder
    )

    if not resume_folder:
        print(f'   ✅ Pasta principal: {folders["root"].name}')
    print(f'   📂 Individuais: {folders["individuais"].name}/')
    print(f'   📂 Logs: {folders["logs"].name}/')
    print(f'   📂 Consolidados: {folders["consolidados"].name}/')
    print()

    # Ler roteiro do PDF
    print('📖 Lendo roteiro...')
    try:
        screenplay_path_obj = Path(screenplay_path)
        if screenplay_path_obj.suffix.lower() == '.pdf':
            import PyPDF2
            with open(screenplay_path, 'rb') as f:
                pdf_reader = PyPDF2.PdfReader(f)
                screenplay_text = ""
                for page in pdf_reader.pages:
                    screenplay_text += page.extract_text() + "\n"
            word_count = len(screenplay_text.split())
            print(f'   ✅ {len(pdf_reader.pages)} páginas, {word_count:,} palavras')
        else:
            # TXT file
            screenplay_text = screenplay_path_obj.read_text(encoding='utf-8', errors='ignore')
            word_count = len(screenplay_text.split())
            print(f'   ✅ {word_count:,} palavras')
    except Exception as e:
        print(f'   ❌ Erro ao ler roteiro: {e}')
        sys.exit(1)
    print()

    # Inicializar checkpoint
    checkpoint_path = folders['logs'] / 'checkpoint.json'
    checkpoint = CheckpointManager(checkpoint_path)

    # Verificar se há checkpoint anterior
    completed, total = checkpoint.get_progress()
    if completed > 0:
        print(f'💾 Checkpoint detectado: {completed}/{total} análises completas ({completed/total*100:.1f}%)')
        resume_point = checkpoint.get_resume_point()
        if resume_point:
            specialist_idx, author_idx = resume_point
            print(f'   📍 Pode continuar do Dr{ALL_SPECIALISTS[specialist_idx][0].title()} × {AUTHORS[author_idx].upper()}')

            if not force_resume and not auto_confirm:
                response = input('\n❓ Continuar de onde parou? [S/n]: ').strip().lower()
                if response and response != 's':
                    print('❌ Cancelado pelo usuário')
                    sys.exit(0)
        else:
            print('   ✅ Todas as análises já completas!')
            sys.exit(0)
    else:
        resume_point = None
        if not auto_confirm:
            print(f'⚠️  ATENÇÃO: Isso vai gerar {len(ALL_SPECIALISTS) * len(AUTHORS)} análises (~13 horas)')
            response = input('\n❓ Deseja continuar? [s/N]: ').strip().lower()
            if response != 's':
                print('❌ Cancelado pelo usuário')
                sys.exit(0)

    print()
    print('✅ Modo auto-confirm ativado' if auto_confirm else '✅ Confirmado pelo usuário')
    print()
    print('🚀 Iniciando análise...')
    print()

    # Determinar de onde começar
    start_specialist_idx = 0
    start_author_idx = 0

    if resume_point:
        start_specialist_idx, start_author_idx = resume_point
        print(f'🔄 Resumindo do Dr{ALL_SPECIALISTS[start_specialist_idx][0].title()} (especialista {start_specialist_idx + 1}/{len(ALL_SPECIALISTS)})')
        print()

    # Executar análises
    total_start = time.time()
    all_results = []

    for i, (specialist_name, specialist_class, specialist_focus) in enumerate(ALL_SPECIALISTS):
        if i < start_specialist_idx:
            print(f'⏭️  [{i+1}/{len(ALL_SPECIALISTS)}] Dr{specialist_name.title()}: PULADO (já completo)')
            continue

        print(f'\n📈 Progresso geral: {i+1}/{len(ALL_SPECIALISTS)} especialistas')
        completed_now, total_now = checkpoint.get_progress()
        print(f'📊 Análises completas: {completed_now}/{total_now} ({completed_now/total_now*100:.1f}%)')

        author_start_idx = start_author_idx if i == start_specialist_idx else 0

        result = analyze_one_specialist_all_authors(
            specialist_name=specialist_name,
            specialist_class=specialist_class,
            specialist_focus=specialist_focus,
            screenplay_text=screenplay_text,
            screenplay_path=screenplay_path,  # Keep for title/filename
            folders=folders,
            checkpoint=checkpoint,
            start_from_author_idx=author_start_idx,
            llm_model=llm_model
        )

        all_results.append(result)

    total_elapsed = time.time() - total_start

    # ═══ GPT-5 SELF-EVALUATION ═══
    if enable_self_eval and llm_model.startswith('gpt-') and GPT5_SELF_EVAL_AVAILABLE:
        print('\n' + '='*80)
        print('🤖 GPT-5 AUTO-AVALIAÇÃO DO SISTEMA')
        print('='*80)
        print()
        print('🔍 GPT-5 vai analisar sua própria performance e sugerir melhorias...')
        print()

        try:
            # Flatten all analysis results for evaluation
            all_analyses = []
            for specialist_result in all_results:
                if 'results' in specialist_result:
                    all_analyses.extend(specialist_result['results'])

            # Estimate cost (since we don't have centralized tracking yet)
            # For GPT-5: ~$0.11 per specialist-author pair
            estimated_cost = len(all_analyses) * 0.11 if llm_model.startswith('gpt-') else 0.0

            cost_summary = {
                'total_calls': len(all_analyses),
                'total_input_tokens': 0,  # Not tracked in multi-analysis mode
                'total_output_tokens': 0,  # Not tracked in multi-analysis mode
                'total_cost': estimated_cost,
                'calls': []
            }

            # Run self-evaluation
            eval_report = run_self_evaluation(
                analysis_results=all_analyses,
                cost_summary=cost_summary,
                execution_time=total_elapsed,
                screenplay_title=Path(screenplay_path).stem
            )

            # Save evaluation report
            eval_path = folders['logs'] / 'GPT5_SELF_EVALUATION.md'
            with open(eval_path, 'w', encoding='utf-8') as f:
                f.write(eval_report)

            print('✅ Auto-avaliação completa!')
            print(f'📄 Relatório salvo: {eval_path}')
            print()

        except Exception as e:
            print(f'⚠️  Erro na auto-avaliação: {e}')
            print('   (A análise principal foi concluída com sucesso)')
            print()

    # Relatório final
    print('\n' + '='*80)
    print('🎉 ANÁLISE COMPLETA!')
    print('='*80)
    print()
    print(f'⏱️  Tempo total: {total_elapsed/3600:.1f} horas')
    print(f'📊 Especialistas processados: {len(all_results)}')
    print(f'📁 Pasta de saída: {folders["root"]}')
    print()
    print(f'📂 Arquivos gerados:')
    print(f'   • Individuais: {len(list(folders["individuais"].rglob("*.html")))} HTMLs')
    print(f'   • Consolidados: {len(list(folders["consolidados"].glob("*.html")))} HTMLs')
    print(f'   • Checkpoint: {checkpoint_path}')
    print()
    print('✅ Análise completa com sucesso!')
    print()


if __name__ == '__main__':
    main()
