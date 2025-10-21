#!/usr/bin/env python3
"""
Scripturemon - Análise Multi-Autor de Roteiros

Analisa roteiros usando 13 perspectivas teóricas diferentes.
Gera HTMLs individuais por autor + consolidação final.

Uso:
    python analyze.py <roteiro>                    # Todos os 13 autores
    python analyze.py <roteiro> --author mckee     # Apenas McKee
    python analyze.py <roteiro> --authors mckee field truby  # Vários autores
    python analyze.py                              # Usa exemplo padrão
"""

import sys
from pathlib import Path
import time
from datetime import datetime
import re
import argparse

sys.path.insert(0, str(Path.cwd()))

from engine.analyzers.dr_dialogue import DrDialogue
from engine.orchestration.dual_core_wrapper import DualCoreWrapper


def sanitize_filename(name: str) -> str:
    """Remove caracteres inválidos do nome do arquivo."""
    # Remove caracteres especiais, mantém apenas letras, números, underscores e hífens
    name = re.sub(r'[^\w\s-]', '', name)
    # Substitui espaços por underscores
    name = re.sub(r'\s+', '_', name)
    return name.upper()


def get_next_analysis_number(base_dir: Path, screenplay_name: str, specialist: str) -> int:
    """
    Encontra o próximo número disponível para análise.

    Args:
        base_dir: Diretório base de outputs
        screenplay_name: Nome do roteiro
        specialist: Tipo de especialista (dialogue, structure, etc)

    Returns:
        Próximo número disponível (1, 2, 3, etc)
    """
    # Procurar por pastas existentes com o padrão
    pattern = f"{screenplay_name}_{specialist}_*"
    existing = list(base_dir.glob(pattern))

    if not existing:
        return 1

    # Extrair números existentes
    numbers = []
    for folder in existing:
        match = re.search(r'_(\d{4})$', folder.name)
        if match:
            numbers.append(int(match.group(1)))

    if not numbers:
        return 1

    return max(numbers) + 1


def create_analysis_structure(screenplay_path: str, specialist_type: str = 'dialogue'):
    """
    Cria estrutura organizada de pastas para análise.

    Args:
        screenplay_path: Caminho do roteiro
        specialist_type: Tipo de especialista

    Returns:
        Dict com paths de todas as pastas criadas
    """
    # Extrair nome do roteiro do path
    screenplay_file = Path(screenplay_path)
    screenplay_name = screenplay_file.stem  # Nome sem extensão
    screenplay_name = sanitize_filename(screenplay_name)

    # Diretório base
    base_dir = Path('workspace/outputs')
    base_dir.mkdir(parents=True, exist_ok=True)

    # Obter próximo número
    number = get_next_analysis_number(base_dir, screenplay_name, specialist_type)

    # Nome da pasta principal
    analysis_folder_name = f"{screenplay_name}_{specialist_type}_{number:04d}"
    analysis_dir = base_dir / analysis_folder_name

    # Criar estrutura de subpastas
    structure = {
        'root': analysis_dir,
        'individuais': analysis_dir / '1_individuais',
        'logs': analysis_dir / '2_logs',
        'consolidados': analysis_dir / '3_consolidados'
    }

    # Criar todas as pastas
    for folder in structure.values():
        folder.mkdir(parents=True, exist_ok=True)

    return structure


def parse_arguments():
    """Parse argumentos de linha de comando."""
    # Lista de autores disponíveis
    available_authors = [
        'aristotle', 'campbell', 'cowgill', 'dialogue', 'egri',
        'field', 'mckee', 'mckee_character', 'mckee_dialogue',
        'seger', 'snyder', 'truby', 'vogler'
    ]

    parser = argparse.ArgumentParser(
        description='Análise multi-autor de roteiros',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  python analyze.py meu_roteiro.pdf                      # Todos os 13 autores
  python analyze.py meu_roteiro.pdf --author mckee       # Apenas McKee
  python analyze.py meu_roteiro.pdf --authors mckee field truby  # Vários
  python analyze.py                                      # Exemplo padrão

Autores disponíveis:
  aristotle, campbell, cowgill, dialogue, egri, field,
  mckee, mckee_character, mckee_dialogue, seger, snyder, truby, vogler
        """
    )

    parser.add_argument(
        'screenplay',
        help='Caminho do roteiro (.txt ou .pdf) - OBRIGATÓRIO'
    )

    parser.add_argument(
        '--author',
        choices=available_authors,
        help='Analisar com um autor específico'
    )

    parser.add_argument(
        '--authors',
        nargs='+',
        choices=available_authors,
        help='Analisar com múltiplos autores'
    )

    parser.add_argument(
        '--specialist',
        default='dialogue',
        help='Tipo de especialista (padrão: dialogue)'
    )

    parser.add_argument(
        '--deep',
        action='store_true',
        default=True,
        help='Deep context mode - livro completo (~128k tokens)'
    )

    parser.add_argument(
        '--word-limit',
        type=int,
        default=None,
        help='Limite de palavras do roteiro para análise (padrão: roteiro completo)'
    )

    parser.add_argument(
        '--use-personalized-prompts',
        action='store_true',
        default=True,  # ⚠️ FASE 2 ATIVADA: Validado com EGRI, SNYDER, TRUBY (todos 8.0/10)
        help='Usar prompts personalizados FASE 2 (melhora qualidade para 8/10) [ATIVADO POR PADRÃO]'
    )

    parser.add_argument(
        '--no-personalized-prompts',
        action='store_false',
        dest='use_personalized_prompts',
        help='Desativar prompts personalizados (usar sistema antigo V11/V12)'
    )

    args = parser.parse_args()

    # Determinar lista de autores
    if args.author:
        authors = [args.author]
    elif args.authors:
        authors = args.authors
    else:
        # Padrão: todos os 13 autores
        authors = available_authors

    return args, authors


# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    # Parse argumentos
    args, AUTHORS = parse_arguments()

    # Validar roteiro existe
    screenplay_path = Path(args.screenplay)
    if not screenplay_path.exists():
        print(f'❌ ERRO: Roteiro não encontrado: {screenplay_path}')
        print()
        print('💡 Dica: Coloque seus roteiros em inputs/to_analyze/')
        print('   ou use inputs/examples/SONHOS SEM LEMBRANÇAS T.3.pdf')
        sys.exit(1)

    print('='*80)
    print('🎯 SCRIPTUREMON - ANÁLISE MULTI-AUTOR')
    print('='*80)
    print()
    print(f'📄 Roteiro: {screenplay_path.name}')
    print(f'👥 Autores: {len(AUTHORS)}')
    if len(AUTHORS) <= 3:
        print(f'   {", ".join(a.upper() for a in AUTHORS)}')
    else:
        print(f'   Todos os 13 autores teóricos')
    print()

    # Criar estrutura organizada de pastas
    print('📁 Criando estrutura de pastas...')
    folders = create_analysis_structure(
        screenplay_path=str(screenplay_path),
        specialist_type=args.specialist
    )

    print(f'   ✅ Pasta principal: {folders["root"].name}')
    print(f'   📂 Individuais: {folders["individuais"].name}')
    print(f'   📂 Logs: {folders["logs"].name}')
    print(f'   📂 Consolidados: {folders["consolidados"].name}')
    print()

    # Ler PDF ou TXT
    print('📖 Lendo roteiro...')
    try:
        if screenplay_path.suffix.lower() == '.pdf':
            import PyPDF2
            with open(screenplay_path, 'rb') as f:
                pdf_reader = PyPDF2.PdfReader(f)
                screenplay = ""
                for page in pdf_reader.pages:
                    screenplay += page.extract_text() + "\n"
            word_count = len(screenplay.split())
            print(f'   ✅ {len(pdf_reader.pages)} páginas, {word_count:,} palavras')
        else:
            # TXT file
            screenplay = screenplay_path.read_text(encoding='utf-8', errors='ignore')
            word_count = len(screenplay.split())
            print(f'   ✅ {word_count:,} palavras')
    except Exception as e:
        print(f'   ❌ Erro ao ler roteiro: {e}')
        sys.exit(1)

    print()

    # Usar roteiro completo ou limite especificado
    if args.word_limit:
        screenplay_excerpt = ' '.join(screenplay.split()[:args.word_limit])
        print(f'📚 Autores para analisar: {len(AUTHORS)}')
        print(f'📝 Analisando: {len(screenplay_excerpt.split())} palavras (primeiras {args.word_limit})')
    else:
        screenplay_excerpt = screenplay
        print(f'📚 Autores para analisar: {len(AUTHORS)}')
        print(f'📝 Analisando: ROTEIRO COMPLETO ({word_count:,} palavras)')

    if args.deep:
        print('🔥 Deep context mode: Livro completo (~128k tokens)')
    print()
    print('⚠️  AVISO: Deep context - cada análise pode levar ~2-3 minutos')
    print(f'⏱️  Tempo estimado total: ~{len(AUTHORS) * 2.5:.1f} minutos')
    print()

    print('🚀 Iniciando análises...')
    print()

    total_chars = 0
    total_time = 0
    successful_analyses = []

    for i, author in enumerate(AUTHORS, 1):
        print(f'\n{"="*80}')
        print(f'📖 [{i}/{len(AUTHORS)}] Analisando com {author.upper()}...')
        print(f'{"="*80}\n')

        try:
            # Criar wrapper específico para este autor
            specialist = DrDialogue()
            wrapper = DualCoreWrapper(
                python_specialist=specialist,
                llm_model='scripturemon-optimized',
                # llm_timeout removed - None by default (no timeout for deep analysis)
                use_theory=True,
                deep_context=args.deep,
                specialist_type=author,  # UM autor por vez
                two_pass_llm=True,  # ⚠️ TWO-PASS LLM v12.0: Identificar problemas + Expandir soluções
                use_personalized_prompts=args.use_personalized_prompts  # ⚠️ FASE 2: Prompts personalizados
            )

            print(f'⏳ Executando análise com {author.upper()}...')
            if args.deep:
                print(f'   📚 Carregando livro completo (~128k tokens)')
            if args.use_personalized_prompts:
                print(f'   🎯 FASE 2: Prompts personalizados ATIVADOS (nivel 10 quality)')
            print(f'   🤖 Gerando análise...')

            start = time.time()
            result = wrapper.analyze(screenplay_excerpt)
            elapsed = time.time() - start
            total_time += elapsed

            llm_text = result.get('llm_insights', '')
            total_chars += len(llm_text)

            print(f'✅ Completo em {elapsed:.1f}s')
            print(f'📏 Output: {len(llm_text):,} chars')

            # Show nivel 10 validation if personalized prompts were used
            if args.use_personalized_prompts and 'nivel_10_validation' in result:
                validation = result['nivel_10_validation']
                status = '✅ PASSOU' if validation['passed'] else '❌ FALHOU'
                print(f'📊 Nivel 10 Validation: {status} (Score: {validation["score"]:.1f}/10)')

            # Export HTML individual para pasta organizada
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            html_filename = f"ANALISE_{author.upper()}_{timestamp}.html"
            html_path = folders['individuais'] / html_filename

            # Temporariamente exportar para pasta padrão
            temp_html = wrapper.export_formatted(
                result,
                screenplay_title=f"{screenplay_path.stem}_ANALISE_{author.upper()}",
                format="html"
            )

            # Mover para pasta organizada
            import shutil
            shutil.move(str(temp_html), str(html_path))

            print(f'💾 HTML salvo: {html_path.name}')
            successful_analyses.append({
                'author': author,
                'html_path': html_path,
                'chars': len(llm_text)
            })

        except Exception as e:
            print(f'❌ ERRO ao processar {author}: {e}')
            import traceback
            traceback.print_exc()

        print()

    print(f'\n{"="*80}')
    print('✅ ANÁLISES INDIVIDUAIS COMPLETAS!')
    print(f'{"="*80}\n')

    print(f'📊 Estatísticas:')
    print(f'   Autores processados: {len(successful_analyses)}/{len(AUTHORS)}')
    print(f'   Tempo total: {total_time:.1f}s ({total_time/60:.1f} min)')
    print(f'   Output total: {total_chars:,} chars')
    if successful_analyses:
        total_analysis_chars = sum(a['chars'] for a in successful_analyses)
        print(f'   Média por autor: {total_analysis_chars/len(successful_analyses):,.0f} chars')
    print()

    # Salvar log de execução
    log_path = folders['logs'] / f'execution_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt'
    with open(log_path, 'w', encoding='utf-8') as f:
        f.write(f'ANÁLISE MULTI-AUTOR\n')
        f.write(f'{"="*80}\n\n')
        f.write(f'Roteiro: {screenplay_path.name}\n')
        f.write(f'Especialidade: {args.specialist}\n')
        f.write(f'Data: {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}\n\n')
        f.write(f'Autores processados: {len(successful_analyses)}/{len(AUTHORS)}\n')
        f.write(f'Tempo total: {total_time:.1f}s ({total_time/60:.1f} min)\n')
        f.write(f'Output total: {total_chars:,} chars\n\n')
        f.write('AUTORES:\n')
        for analysis in successful_analyses:
            f.write(f'  - {analysis["author"].upper()}: {analysis["chars"]:,} chars\n')

    print(f'📝 Log salvo: {log_path.name}')
    print()

    # CONSOLIDAÇÃO
    if successful_analyses:
        print(f'{"="*80}')
        print('🔨 CONSOLIDANDO ANÁLISES...')
        print(f'{"="*80}\n')

        from consolidate_analyses import consolidate_html_analyses

        # Copiar HTMLs individuais para pasta temporária para consolidação
        import shutil
        temp_dir = Path('workspace/outputs/formatted')

        # ✅ FIX: Limpar pasta temporária antes de consolidar
        # Isso garante que só use arquivos da rodada atual (não mistura com análises antigas)
        if temp_dir.exists():
            shutil.rmtree(temp_dir)
        temp_dir.mkdir(parents=True, exist_ok=True)

        for analysis in successful_analyses:
            src = analysis['html_path']
            dst = temp_dir / src.name
            shutil.copy(str(src), str(dst))

        print('   🌐 Traduzindo análises em inglês para português...')
        consolidated_html = consolidate_html_analyses(
            pattern='ANALISE_*.html',
            output_name='ANALISE_COMPLETA',
            translate=True  # TRADUÇÃO AUTOMÁTICA!
        )

        # Mover HTML consolidado para pasta organizada
        if consolidated_html:
            final_path = folders['consolidados'] / consolidated_html.name
            shutil.move(str(consolidated_html), str(final_path))
            consolidated_html = final_path

        if consolidated_html:
            print()
            print(f'{"="*80}')
            print('🎉 PROCESSO COMPLETO!')
            print(f'{"="*80}\n')

            print(f'📊 Resultados:')
            print(f'   ✅ {len(successful_analyses)} análises individuais')
            print(f'   ✅ 1 análise consolidada')
            print(f'   📁 Pasta: {folders["root"]}')
            print()

            print(f'📂 Estrutura final:')
            print(f'   {folders["root"].name}/')
            print(f'   ├── 1_individuais/ ({len(successful_analyses)} HTMLs)')
            print(f'   ├── 2_logs/ (1 arquivo)')
            print(f'   └── 3_consolidados/ (1 HTML consolidado)')
            print()

            print(f'Para visualizar:')
            print(f'   open "{consolidated_html}"')
            print()

            # Abrir automaticamente
            import subprocess
            subprocess.run(['open', str(consolidated_html)])
            print('🌐 HTML consolidado aberto no browser!')

            # Salvar caminho completo no log final
            summary_path = folders['root'] / 'README.txt'
            with open(summary_path, 'w', encoding='utf-8') as f:
                f.write(f'ANÁLISE MULTI-AUTOR - {screenplay_path.stem}\n')
                f.write(f'{"="*80}\n\n')
                f.write(f'📁 Estrutura:\n\n')
                f.write(f'1_individuais/\n')
                f.write(f'  - {len(successful_analyses)} análises individuais por autor\n')
                f.write(f'  - Formato: ANALISE_[AUTOR]_[TIMESTAMP].html\n\n')
                f.write(f'2_logs/\n')
                f.write(f'  - Logs de execução e estatísticas\n\n')
                f.write(f'3_consolidados/\n')
                f.write(f'  - Análise final consolidada e traduzida\n')
                f.write(f'  - Arquivo: {consolidated_html.name}\n\n')
                f.write(f'{"="*80}\n')
                f.write(f'Gerado em: {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}\n')

            print(f'📝 README criado: {summary_path.name}')

    else:
        print('❌ Nenhuma análise foi concluída com sucesso.')
