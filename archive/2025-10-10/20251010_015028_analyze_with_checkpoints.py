#!/usr/bin/env python3
"""
Scripturemon with Checkpoints - Never Lose Your Work!

Integrates CheckpointManager with the existing DualCoreWrapper system.
Resume analysis after interruptions, retry failed authors, improve low-quality results.

Usage:
    python analyze_with_checkpoints.py <screenplay>  # New analysis (dialogue only)
    python analyze_with_checkpoints.py <screenplay> --all  # All 13 authors
    python analyze_with_checkpoints.py --resume <session_dir>  # Resume interrupted
    python analyze_with_checkpoints.py --improve <session_dir>  # Retry low quality
"""

import sys
import argparse
from pathlib import Path
import time
from datetime import datetime

sys.path.insert(0, str(Path.cwd()))

from engine.analyzers.dr_dialogue import DrDialogue
from engine.orchestration.dual_core_wrapper import DualCoreWrapper
from engine.utils.checkpoint_manager import CheckpointManager


# Available authors (13 theory perspectives)
AVAILABLE_AUTHORS = [
    'dialogue', 'mckee', 'truby', 'field', 'vogler',
    'campbell', 'snyder', 'seger', 'egri', 'cowgill',
    'mckee_character', 'mckee_dialogue', 'aristotle'
]


def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description='Scripturemon with Checkpoint System',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument('screenplay', nargs='?', help='Path to screenplay file')
    parser.add_argument('--all', action='store_true', help='Run all 13 authors (default: dialogue only)')
    parser.add_argument('--authors', nargs='+', choices=AVAILABLE_AUTHORS, help='Select specific authors')
    parser.add_argument('--resume', metavar='SESSION', help='Resume from session directory')
    parser.add_argument('--improve', metavar='SESSION', help='Improve low-quality analyses in session')
    parser.add_argument('--deep', action='store_true', default=True, help='Deep context mode (default: True)')

    return parser.parse_args()


def run_analysis_with_checkpoints(screenplay_path: str, authors: list, session_dir: Path,
                                  checkpoint_mgr: CheckpointManager, resume: bool = False):
    """
    Run multi-author analysis with checkpoint support.

    Args:
        screenplay_path: Path to screenplay PDF/TXT
        authors: List of author names to run
        session_dir: Session directory for outputs
        checkpoint_mgr: CheckpointManager instance
        resume: If True, skip completed authors
    """
    print('=' * 80)
    print('🎬 SCRIPTUREMON WITH CHECKPOINTS')
    print('=' * 80)
    print()
    print(f'📄 Screenplay: {Path(screenplay_path).name}')
    print(f'👥 Authors: {len(authors)} ({", ".join(authors[:3])}{"..." if len(authors) > 3 else ""})')
    print(f'💾 Session: {session_dir.name}')
    print(f'🔄 Resume mode: {"Yes" if resume else "No"}')
    print()

    # Read screenplay
    print('📖 Reading screenplay...')
    screenplay_path = Path(screenplay_path)

    if screenplay_path.suffix.lower() == '.pdf':
        import PyPDF2
        with open(screenplay_path, 'rb') as f:
            pdf_reader = PyPDF2.PdfReader(f)
            screenplay_text = ""
            for page in pdf_reader.pages:
                screenplay_text += page.extract_text() + "\n"
        word_count = len(screenplay_text.split())
        print(f'   ✅ {len(pdf_reader.pages)} pages, {word_count:,} words')
    else:
        screenplay_text = screenplay_path.read_text(encoding='utf-8', errors='ignore')
        word_count = len(screenplay_text.split())
        print(f'   ✅ {word_count:,} words')

    print()
    print('🚀 Starting analysis with checkpoints...')
    print()

    # Create output directories
    output_dir = session_dir / 'outputs'
    output_dir.mkdir(parents=True, exist_ok=True)

    total_time = 0
    successful = 0
    failed = 0

    for i, author in enumerate(authors, 1):
        # Check if already completed (for resume)
        if resume and checkpoint_mgr.is_specialist_completed(author):
            print(f'⏭️  [{i}/{len(authors)}] {author.upper()}: Already completed (skipping)')
            successful += 1
            continue

        print(f'\n{"=" * 80}')
        print(f'📖 [{i}/{len(authors)}] Analyzing with {author.upper()}...')
        print(f'{"=" * 80}\n')

        # Mark started
        checkpoint_mgr.mark_specialist_started(author)

        try:
            # Create wrapper for this author
            specialist = DrDialogue()
            wrapper = DualCoreWrapper(
                python_specialist=specialist,
                llm_model='scripturemon-optimized',
                use_theory=True,
                deep_context=True,  # DEEP: Full book context with improved prompt
                specialist_type=author,  # One author at a time
                two_pass_llm=True  # ⚠️ TWO-PASS LLM: Identificar problemas + Expandir soluções
            )

            print(f'⏳ Running analysis with {author.upper()}...')
            print(f'   📚 Loading full book context (~128k tokens)')
            print(f'   🤖 Generating forensic analysis...')

            start = time.time()
            result = wrapper.analyze(screenplay_text)
            elapsed = time.time() - start
            total_time += elapsed

            llm_text = result.get('llm_insights', '')
            quality_score = result.get('quality_score', 0.0)

            print(f'✅ Complete in {elapsed:.1f}s')
            print(f'📏 Output: {len(llm_text):,} chars')
            print(f'⭐ Quality: {quality_score:.1f}/10')

            # Export HTML
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            html_filename = f"ANALYSIS_{author.upper()}_{timestamp}.html"

            temp_html = wrapper.export_formatted(
                result,
                screenplay_title=f"{screenplay_path.stem}_{author.upper()}",
                format="html"
            )

            # Move to session output directory
            import shutil
            final_html = output_dir / html_filename
            shutil.move(str(temp_html), str(final_html))

            print(f'💾 Saved: {final_html.name}')

            # Mark completed with quality score
            checkpoint_mgr.mark_specialist_completed(
                author,
                quality_score=quality_score,
                output_path=str(final_html)
            )

            successful += 1

        except Exception as e:
            print(f'❌ FAILED: {author} - {e}')
            checkpoint_mgr.mark_specialist_failed(author, str(e))
            failed += 1
            import traceback
            traceback.print_exc()

        print()

    # Final summary
    print(f'\n{"=" * 80}')
    print('✅ ANALYSIS COMPLETE!')
    print(f'{"=" * 80}\n')

    print(f'📊 Results:')
    print(f'   ✅ Successful: {successful}/{len(authors)}')
    print(f'   ❌ Failed: {failed}/{len(authors)}')
    print(f'   ⏱️  Total time: {total_time:.1f}s ({total_time/60:.1f} min)')
    print(f'   📁 Session: {session_dir}')
    print()

    # Show low quality authors
    low_quality = checkpoint_mgr.get_low_quality_specialists(threshold=7.0)
    if low_quality:
        print(f'⚠️  Low quality analyses (< 7.0/10): {len(low_quality)}')
        for name in low_quality:
            spec = checkpoint_mgr.checkpoint['specialists'][name]
            print(f'   - {name}: {spec.get("quality_score", 0):.1f}/10')
        print()
        print(f'💡 To improve: python analyze_with_checkpoints.py --improve {session_dir}')
        print()

    return {
        'successful': successful,
        'failed': failed,
        'total_time': total_time,
        'session_dir': session_dir
    }


def main():
    args = parse_arguments()

    # RESUME MODE
    if args.resume:
        session_dir = Path(args.resume)
        if not session_dir.exists():
            print(f'❌ Session not found: {session_dir}')
            sys.exit(1)

        checkpoint_mgr = CheckpointManager(session_dir)

        # Get failed/pending specialists
        failed = checkpoint_mgr.get_failed_specialists()
        pending = checkpoint_mgr.get_pending_specialists()
        to_resume = failed + pending

        if not to_resume:
            print('✅ All specialists completed! Nothing to resume.')
            sys.exit(0)

        print(f'🔄 Resuming session: {session_dir.name}')
        print(f'📋 To complete: {len(to_resume)} specialists')
        print()

        # Get screenplay path from checkpoint
        screenplay_path = checkpoint_mgr.checkpoint.get('screenplay_path')
        if not screenplay_path:
            print('❌ Screenplay path not found in checkpoint!')
            sys.exit(1)

        run_analysis_with_checkpoints(
            screenplay_path=screenplay_path,
            authors=to_resume,
            session_dir=session_dir,
            checkpoint_mgr=checkpoint_mgr,
            resume=True
        )
        return

    # IMPROVE MODE
    if args.improve:
        session_dir = Path(args.improve)
        if not session_dir.exists():
            print(f'❌ Session not found: {session_dir}')
            sys.exit(1)

        checkpoint_mgr = CheckpointManager(session_dir)

        # Get low quality specialists
        low_quality = checkpoint_mgr.get_low_quality_specialists(threshold=7.0)

        if not low_quality:
            print('✅ All analyses meet quality threshold! Nothing to improve.')
            sys.exit(0)

        print(f'🔧 Improving low-quality analyses in: {session_dir.name}')
        print(f'📋 To improve: {len(low_quality)} specialists')
        for name in low_quality:
            spec = checkpoint_mgr.checkpoint['specialists'][name]
            print(f'   - {name}: {spec.get("quality_score", 0):.1f}/10')
        print()

        # Get screenplay path from checkpoint
        screenplay_path = checkpoint_mgr.checkpoint.get('screenplay_path')
        if not screenplay_path:
            print('❌ Screenplay path not found in checkpoint!')
            sys.exit(1)

        # Mark for retry
        for name in low_quality:
            checkpoint_mgr.checkpoint['specialists'][name]['status'] = 'pending'
        checkpoint_mgr.save_checkpoint()

        run_analysis_with_checkpoints(
            screenplay_path=screenplay_path,
            authors=low_quality,
            session_dir=session_dir,
            checkpoint_mgr=checkpoint_mgr,
            resume=False  # Re-run even if completed
        )
        return

    # NEW ANALYSIS MODE
    if not args.screenplay:
        print('❌ Error: Screenplay path required for new analysis')
        print()
        print('Usage:')
        print('  python analyze_with_checkpoints.py <screenplay>')
        print('  python analyze_with_checkpoints.py --resume <session_dir>')
        print('  python analyze_with_checkpoints.py --improve <session_dir>')
        sys.exit(1)

    screenplay_path = Path(args.screenplay)
    if not screenplay_path.exists():
        print(f'❌ Screenplay not found: {screenplay_path}')
        sys.exit(1)

    # Determine authors to run
    if args.authors:
        authors = args.authors
    elif args.all:
        authors = AVAILABLE_AUTHORS
    else:
        authors = ['dialogue']  # Default: dialogue only (fast)

    # Create session directory
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    screenplay_name = screenplay_path.stem.replace(' ', '_')
    session_name = f"{screenplay_name}_{timestamp}"
    session_dir = Path('workspace/sessions') / session_name
    session_dir.mkdir(parents=True, exist_ok=True)

    # Initialize checkpoint
    checkpoint_mgr = CheckpointManager(session_dir)
    checkpoint_mgr.initialize_session(
        screenplay_path=str(screenplay_path),
        llm_model='scripturemon-optimized',
        deep_context=True,
        specialist_names=authors
    )

    # Run analysis
    run_analysis_with_checkpoints(
        screenplay_path=str(screenplay_path),
        authors=authors,
        session_dir=session_dir,
        checkpoint_mgr=checkpoint_mgr,
        resume=False
    )


if __name__ == '__main__':
    main()
