#!/usr/bin/env python3
"""
Consolida múltiplos HTMLs de análise em um único arquivo master
COM TRADUÇÃO AUTOMÁTICA PARA PORTUGUÊS
"""

import sys
from pathlib import Path
from datetime import datetime
import re
import subprocess
import json

sys.path.insert(0, str(Path.cwd()))

def detect_english(text: str) -> bool:
    """
    Detecta se o texto está predominantemente em inglês.

    Args:
        text: Texto para analisar

    Returns:
        True se o texto está em inglês
    """
    # Remove HTML tags para análise
    clean_text = re.sub(r'<[^>]+>', '', text).lower()

    # Palavras extremamente comuns em inglês que NÃO existem em português
    english_indicators = [
        ' the ', ' is ', ' are ', ' was ', ' were ', ' have ', ' has ', ' had ',
        ' this ', ' that ', ' these ', ' those ', ' will ', ' would ', ' should ',
        ' character ', ' dialogue ', ' screenplay ', ' scene ', ' story ',
        'reveals', 'demonstrates', 'indicates', 'suggests', 'emphasizes',
        ' and ', ' or ', ' but ', ' of ', ' to ', ' in ', ' on ', ' at ',
        ' with ', ' from ', ' by ', ' for ', ' through ', ' between '
    ]

    # Palavras extremamente comuns em português que NÃO existem em inglês
    portuguese_indicators = [
        ' o ', ' a ', ' os ', ' as ', ' um ', ' uma ', ' de ', ' da ', ' do ',
        ' que ', ' para ', ' com ', ' em ', ' por ', ' isso ', ' este ', ' esta ',
        ' roteiro', ' personagem', ' cena', ' história', ' diálogo',
        ' são ', ' está ', ' estava ', ' foram ', ' seja ', ' ser ',
        ' mais ', ' menos ', ' muito ', ' pouco ', ' sobre ', ' entre '
    ]

    english_count = sum(1 for word in english_indicators if word in clean_text)
    portuguese_count = sum(1 for word in portuguese_indicators if word in clean_text)

    # Debug: mostrar contagens
    # print(f'EN: {english_count}, PT: {portuguese_count}')

    # Se tem mais de 2 indicadores ingleses E mais inglês que português, é inglês
    return english_count >= 2 and english_count > portuguese_count


def translate_with_llm(text: str) -> str:
    """
    Traduz texto completo usando LLM (Ollama).

    Args:
        text: Texto em inglês

    Returns:
        Texto traduzido para português
    """
    print(f'      🔤 Traduzindo via LLM ({len(text)} chars)...')

    # Prompt otimizado para tradução
    prompt = f"""Traduza o seguinte texto de análise de roteiro do INGLÊS para o PORTUGUÊS BRASILEIRO.

REGRAS IMPORTANTES:
1. Mantenha TODA a formatação HTML exatamente como está
2. Mantenha nomes próprios em inglês (McKee, Field, Campbell, etc)
3. Traduza termos técnicos adequadamente (screenplay→roteiro, character→personagem, etc)
4. Seja natural e fluente em português brasileiro
5. NÃO adicione explicações ou comentários, APENAS traduza o texto

TEXTO ORIGINAL:
{text}

TRADUÇÃO EM PORTUGUÊS:"""

    try:
        result = subprocess.run(
            ['ollama', 'run', 'scripturemon-optimized', prompt],
            capture_output=True,
            text=True,
            timeout=180  # 3 minutos por bloco
        )

        if result.returncode == 0:
            translation = result.stdout.strip()

            # Limpar possíveis artefatos do LLM
            if translation.startswith('TRADUÇÃO'):
                translation = translation.split('\n', 1)[-1].strip()
            if translation.startswith('Aqui está'):
                lines = translation.split('\n')
                translation = '\n'.join(lines[1:]).strip()

            print(f'      ✅ Traduzido via LLM')
            return translation
        else:
            print(f'      ⚠️  Falha no LLM, usando substituição simples')
            return translate_to_portuguese_simple(text)

    except subprocess.TimeoutExpired:
        print(f'      ⏱️  Timeout no LLM, usando substituição simples')
        return translate_to_portuguese_simple(text)
    except Exception as e:
        print(f'      ❌ Erro no LLM: {e}, usando substituição simples')
        return translate_to_portuguese_simple(text)


def translate_to_portuguese_simple(text: str) -> str:
    """
    Traduz termos-chave de inglês para português (substituição rápida - fallback).

    Args:
        text: Texto em inglês para traduzir

    Returns:
        Texto com termos traduzidos
    """
    # Dicionário de traduções
    translations = {
        # Headers das seções
        '<div class="insight-header">1. Interpretation</div>': '<div class="insight-header">1. INTERPRETAÇÃO</div>',
        '<div class="insight-header">2. Patterns</div>': '<div class="insight-header">2. PADRÕES</div>',
        '<div class="insight-header">3. Problems</div>': '<div class="insight-header">3. PROBLEMAS</div>',
        '<div class="insight-header">4. Solutions</div>': '<div class="insight-header">4. SOLUÇÕES</div>',
        '<div class="insight-header">5. Depth & Synthesis</div>': '<div class="insight-header">5. PROFUNDIDADE & SÍNTESE</div>',

        'Interpretation': 'INTERPRETAÇÃO',
        'Patterns': 'PADRÕES',
        'Problems': 'PROBLEMAS',
        'Solutions': 'SOLUÇÕES',
        'Depth & Synthesis': 'PROFUNDIDADE & SÍNTESE',

        # Termos comuns
        'First Paragraph:': 'Primeiro Parágrafo:',
        'Second Paragraph:': 'Segundo Parágrafo:',
        'Third Paragraph:': 'Terceiro Parágrafo:',
        'Fourth Paragraph:': 'Quarto Parágrafo:',
        'Fifth Paragraph:': 'Quinto Parágrafo:',

        'Problem 1:': 'Problema 1:',
        'Problem 2:': 'Problema 2:',
        'Problem 3:': 'Problema 3:',
        'Problem 4:': 'Problema 4:',

        'Solution 1:': 'Solução 1:',
        'Solution 2:': 'Solução 2:',
        'Solution 3:': 'Solução 3:',
        'Solution 4:': 'Solução 4:',

        'Description:': 'Descrição:',
        'Example:': 'Exemplo:',
        'Impact:': 'Impacto:',
        'Theory Connection:': 'Conexão Teórica:',
        'WHY:': 'PORQUÊ:',
        'WHERE:': 'ONDE:',
        'IMPACT:': 'IMPACTO:',

        'Grounded Theory:': 'Fundamentação Teórica:',
        'Grounded in Theory:': 'Fundamentação Teórica:',
        'Implementation Example:': 'Exemplo de Implementação:',
        'Expected Outcome:': 'Resultado Esperado:',
        'Action:': 'Ação:',

        'The Python metrics reveal': 'As métricas Python revelam',
        'Based on the Python analysis': 'Baseado na análise Python',
        'According to McKee': 'Segundo McKee',
        'As McKee explains': 'Como McKee explica',
        "McKee's theory": 'A teoria de McKee',
        "McKee emphasizes": 'McKee enfatiza',
        "McKee argues": 'McKee argumenta',
        "McKee notes": 'McKee observa',
        "McKee suggests": 'McKee sugere',

        # Palavras-chave (só minúsculas para não conflitar com headers)
        ' screenplay': ' roteiro',
        ' character': ' personagem',
        ' dialogue': ' diálogo',
        ' scene': ' cena',
        ' story': ' história',
        ' script': ' roteiro',
        ' conflict': ' conflito',
        ' theme': ' tema',
        ' plot': ' trama',
        ' narrative': ' narrativa',
        ' tension': ' tensão',
        ' arc': ' arco',
        ' development': ' desenvolvimento',
        ' motivation': ' motivação',
        ' emotion': ' emoção',
        ' dramatic': ' dramático',
        ' authentic': ' autêntico',
        ' expository': ' expositivo',
        ' subtext': ' subtexto',
        ' pacing': ' ritmo',
        ' structure': ' estrutura',
        ' exposition': ' exposição',
        ' protagonist': ' protagonista',
        ' antagonist': ' antagonista',
        ' backstory': ' passado',
        ' flashback': ' flashback',
        ' relationship': ' relação',
        ' audience': ' público',
        ' writer': ' roteirista',

        # Frases inteiras em inglês que aparecem frequentemente
        'The Python metrics reveal': 'As métricas Python revelam',
        'The Python analysis reveals': 'A análise Python revela',
        'Python analysis highlights': 'A análise Python destaca',
        'Based on the Python analysis': 'Baseado na análise Python',
        'According to McKee': 'Segundo McKee',
        'As McKee explains': 'Como McKee explica',
        "McKee's theory": 'A teoria de McKee',
        'McKee emphasizes': 'McKee enfatiza',
        'McKee argues': 'McKee argumenta',
        'McKee notes': 'McKee observa',
        'McKee suggests': 'McKee sugere',
        'McKee stresses': 'McKee enfatiza',
        'McKee defende': 'McKee defende',
        'McKee advises': 'McKee aconselha',
        'According to Field': 'Segundo Field',
        'According to Campbell': 'Segundo Campbell',
        'According to Egri': 'Segundo Egri',
        'According to Truby': 'Segundo Truby',
        'According to Seger': 'Segundo Seger',

        # Frases específicas do texto
        'reveals that there are several areas in need of improvement': 'revela que há várias áreas que precisam de melhoria',
        'in need of improvement in': 'precisam de melhoria em',
        'is revealed under pressure': 'é revelado sob pressão',
        'the true character is revealed': 'o verdadeiro caráter é revelado',
        'must demonstrate their inner nature': 'devem demonstrar sua natureza interior',
        'through actions rather than': 'através de ações em vez de',
        'simply declaring their': 'simplesmente declarar seus',
        'is crucial for creating': 'é crucial para criar',
        'believable and engaging': 'convincentes e envolventes',
        'the overall quality of': 'a qualidade geral de',
        'seems uneven': 'parece irregular',
        'show promise': 'mostram promessa',
        'lack depth and complexity': 'faltam profundidade e complexidade',
        'it is essential to focus on': 'é essencial focar em',
        'well-rounded': 'bem desenvolvidos',
        'who make choices consistent with': 'que fazem escolhas consistentes com',
        'their desires and values': 'seus desejos e valores',
        'should be rewritten to avoid': 'deve ser reescrito para evitar',
        'and instead convey meaning through': 'e em vez disso transmitir significado através de',
        'recurring pattern identified by': 'padrão recorrente identificado por',
        'overuse of': 'uso excessivo de',
        'where characters explain': 'onde os personagens explicam',
        'their feelings or motivations directly': 'seus sentimentos ou motivações diretamente',
        'undermines both the artistry and': 'prejudica tanto a arte quanto',
        'persuasiveness of your work': 'persuasão do seu trabalho',
        'should express themselves indirectly': 'devem se expressar indiretamente',
        'allowing the audience to infer': 'permitindo que o público infira',
        'their intentions and emotions': 'suas intenções e emoções',
        'evident in': 'evidente em',
        'inconsistent application of': 'aplicação inconsistente de',
        'should be woven throughout': 'deve ser entrelaçado ao longo de',
        'providing coherence and unity': 'fornecendo coerência e unidade',
        'in the current version': 'na versão atual',
        'appears sporadically': 'aparece esporadicamente',
        'making it difficult for': 'tornando difícil para',
        'to grasp its significance': 'compreender seu significado',
        'strengthening thematic connections': 'fortalecendo conexões temáticas',
        'will become more cohesive': 'se tornará mais coeso',
        'and impactful': 'e impactante',

        # Conectores e expressões
        'However': 'No entanto',
        'Therefore': 'Portanto',
        'Additionally': 'Além disso',
        'Furthermore': 'Ademais',
        'In conclusion': 'Em conclusão',
        'For example': 'Por exemplo',
        'In other words': 'Em outras palavras',
        'As a result': 'Como resultado',
        'On the other hand': 'Por outro lado',
        'while': 'enquanto',
        'instead': 'em vez disso',
        'instead of': 'em vez de',
        'rather than': 'em vez de',
        'such as': 'como',
        'as well as': 'assim como',
        'In addition': 'Além disso',
        'Moreover': 'Além disso',
        'Consequently': 'Consequentemente',
        'Nevertheless': 'No entanto',
        'Thus': 'Assim',
        'Hence': 'Portanto',

        # Frases completas comuns
        'reveals that there are': 'revela que há',
        'particularly when it comes to': 'particularmente quando se trata de',
        'is crucial': 'é crucial',
        'is essential': 'é essencial',
        'it is necessary': 'é necessário',
        'should be': 'deve ser',
        'must be': 'deve ser',
        'can be': 'pode ser',
        'may be': 'pode ser',
        'will be': 'será',
        'would be': 'seria',
        'could be': 'poderia ser',
        'is needed': 'é necessário',
        'are needed': 'são necessários',
        'in need of improvement': 'precisam de melhoria',
        'lacks': 'carece de',
        'lack': 'falta de',
        'without': 'sem',
        'through': 'através de',
        'throughout': 'ao longo de',
        'within': 'dentro de',
        'between': 'entre',
        'among': 'entre',
        'should': 'deveria',
        'must': 'deve',
        'need to': 'precisa',
        'needs to': 'precisa',
        'have to': 'tem que',
        'has to': 'tem que',
        'ought to': 'deveria',
        'required to': 'necessário',
        'necessary to': 'necessário',

        # Expressões de análise
        'the Python analysis': 'a análise Python',
        'Python analysis': 'análise Python',
        'the roteiro': 'o roteiro',
        'the screenplay': 'o roteiro',
        'the script': 'o roteiro',
        'the story': 'a história',
        'the narrative': 'a narrativa',
        'the character': 'o personagem',
        'the characters': 'os personagens',
        'the dialogue': 'o diálogo',
        'the scene': 'a cena',
        'the scenes': 'as cenas',

        # Palavras soltas (final, só para não conflitar)
        'that': 'que',
        'this': 'isto',
        'these': 'estes',
        'those': 'aqueles',
        'which': 'que',
        'who': 'quem',
        'what': 'o que',
        'when': 'quando',
        'where': 'onde',
        'why': 'por que',
        'how': 'como',
        'each': 'cada',
        'every': 'cada',
        'some': 'alguns',
        'many': 'muitos',
        'several': 'vários',
        'both': 'ambos',
        'all': 'todos',
        'most': 'maioria',
        'few': 'poucos',
        'more': 'mais',
        'less': 'menos',
        'other': 'outro',
        'another': 'outro',
        'much': 'muito',
        'little': 'pouco',
        'good': 'bom',
        'bad': 'ruim',
        'new': 'novo',
        'old': 'velho',
        'first': 'primeiro',
        'last': 'último',
        'long': 'longo',
        'short': 'curto',
        'early': 'cedo',
        'late': 'tarde',
        'next': 'próximo',
        'previous': 'anterior',
        'important': 'importante',
        'significant': 'significativo',
        'main': 'principal',
        'major': 'principal',
        'minor': 'menor',
        'key': 'chave',
        'crucial': 'crucial',
        'essential': 'essencial',
        'necessary': 'necessário',
        'possible': 'possível',
        'difficult': 'difícil',
        'easy': 'fácil',
        'simple': 'simples',
        'complex': 'complexo',
        'clear': 'claro',
        'unclear': 'pouco claro',
        'strong': 'forte',
        'weak': 'fraco',
        'effective': 'eficaz',
        'ineffective': 'ineficaz',
        'successful': 'bem-sucedido',
        'unsuccessful': 'malsucedido',
    }

    result = text
    for en, pt in translations.items():
        result = result.replace(en, pt)

    return result


def consolidate_html_analyses(pattern: str = "SONHOS_ANALISE_*.html",
                              output_name: str = "SONHOS_ANALISE_COMPLETA",
                              translate: bool = True):
    """
    Consolida todos os HTMLs que correspondem ao pattern em um único arquivo.
    TRADUZ automaticamente conteúdo em inglês para português.

    Args:
        pattern: Glob pattern para encontrar HTMLs (ex: "SONHOS_ANALISE_*.html")
        output_name: Nome base do arquivo consolidado
        translate: Se True, traduz conteúdo em inglês para português
    """
    output_dir = Path("workspace/outputs/formatted")

    # Encontrar todos os HTMLs que correspondem ao pattern
    html_files = sorted(output_dir.glob(pattern))

    if not html_files:
        print(f"❌ Nenhum arquivo encontrado com pattern: {pattern}")
        return None

    print('='*80)
    print(f'📚 CONSOLIDANDO {len(html_files)} ANÁLISES')
    print('='*80)
    print()

    # Extrair conteúdo de cada HTML
    consolidated_content = []
    total_chars = 0

    for i, html_file in enumerate(html_files, 1):
        print(f'[{i}/{len(html_files)}] Lendo {html_file.name}...')

        try:
            # Ler HTML
            html_content = html_file.read_text(encoding='utf-8')

            # Extrair seção de insights LLM usando regex (sem BeautifulSoup)
            # Procurar por <div class="section part-2"> ou <div class="section part-3">
            llm_match = re.search(
                r'<div class="section part-[23]">(.*?)</div>\s*<div class="section part-[34]">',
                html_content,
                re.DOTALL
            )

            if llm_match:
                content = llm_match.group(1)

                # Remover o título "PARTE 2: Insights LLM"
                content = re.sub(
                    r'<h2 class="section-title">🤖 PARTE 2: Insights LLM \(Análise Qualitativa\)</h2>',
                    '',
                    content
                )

                # Contar chars removendo tags HTML para estimativa
                text_only = re.sub(r'<[^>]+>', '', content)
                text_only = text_only.strip()

                # TRADUZIR se necessário
                if translate:
                    # Detectar se está em inglês
                    is_english = detect_english(content)

                    if is_english:
                        print(f'   🌍 Detectado conteúdo em inglês')
                        # Tentar tradução via LLM primeiro
                        content = translate_with_llm(content)
                        # Recalcular text_only após tradução
                        text_only = re.sub(r'<[^>]+>', '', content)
                        text_only = text_only.strip()

                total_chars += len(text_only)

                # Identificar autor pelo nome do arquivo
                author_match = re.search(r'ANALISE_([A-Z_]+)_', html_file.name)
                author_name = author_match.group(1) if author_match else f"Autor_{i}"

                # Adicionar header de separação NUMERADO
                consolidated_content.append(f'''
                    <div class="author-separator" style="margin: 40px 0; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 10px; text-align: center;">
                        <h2 style="margin: 0; font-size: 2em;">📚 ANÁLISE {i}: {author_name}</h2>
                    </div>
                ''')

                consolidated_content.append(content)

                print(f'   ✅ {len(text_only):,} chars extraídos')
            else:
                print(f'   ⚠️  Seção de insights não encontrada')

        except Exception as e:
            print(f'   ❌ Erro ao processar: {e}')

    print()
    print(f'📊 Total consolidado: {total_chars:,} chars')
    print()

    # Criar HTML consolidado
    print('🔨 Gerando HTML consolidado...')

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = output_dir / f"{output_name}_{timestamp}.html"

    # CSS do HTML consolidado
    css = """
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            line-height: 1.6;
            color: #333;
            background: #f5f5f5;
            padding: 20px;
        }
        .container {
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }
        .header h1 { font-size: 3em; margin-bottom: 15px; }
        .header .meta { opacity: 0.9; font-size: 1.2em; }

        .section {
            padding: 30px;
            border-bottom: 1px solid #eee;
        }
        .section:last-child { border-bottom: none; }

        .section-title {
            font-size: 1.8em;
            color: #667eea;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 3px solid #667eea;
        }

        .part-2, .part-3 { background: #f9fafb; }

        .insight-paragraph {
            background: #f0fdf4;
            padding: 20px;
            margin: 15px 0;
            border-radius: 8px;
            border-left: 4px solid #10b981;
        }

        .insight-header {
            font-weight: bold;
            color: #059669;
            margin-bottom: 10px;
            font-size: 1.1em;
        }

        .author-separator {
            animation: fadeIn 0.5s ease-in;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(-20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .footer {
            text-align: center;
            padding: 30px;
            background: #f9fafb;
            color: #6b7280;
        }

        .toc {
            background: #eff6ff;
            padding: 30px;
            margin: 20px 0;
            border-radius: 8px;
            border-left: 4px solid #3b82f6;
        }

        .toc h2 {
            color: #1e40af;
            margin-bottom: 15px;
        }

        .toc ul {
            list-style: none;
            padding: 0;
        }

        .toc li {
            padding: 8px 0;
            border-bottom: 1px solid #dbeafe;
        }

        .toc a {
            color: #3b82f6;
            text-decoration: none;
            font-weight: 500;
        }

        .toc a:hover {
            color: #1e40af;
            text-decoration: underline;
        }
    </style>
    """

    # Gerar TOC (Table of Contents)
    toc_items = []
    for i, html_file in enumerate(html_files, 1):
        author_match = re.search(r'ANALISE_([A-Z]+)_', html_file.name)
        author_name = author_match.group(1) if author_match else f"Autor_{i}"
        toc_items.append(f'<li>📚 Análise {i}: {author_name}</li>')

    toc_html = f'''
    <div class="toc">
        <h2>📋 Índice de Análises</h2>
        <ul>
            {''.join(toc_items)}
        </ul>
        <p style="margin-top: 20px; color: #6b7280;">
            <strong>Total:</strong> {len(html_files)} análises completas | {total_chars:,} caracteres
        </p>
    </div>
    '''

    # HTML completo
    html = f"""
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Scripturemon - Análise Completa Multi-Autor</title>
        {css}
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🎬 SCRIPTUREMON</h1>
                <div class="meta">
                    <strong>Análise Completa Multi-Autor</strong><br>
                    {len(html_files)} Perspectivas Teóricas Consolidadas<br>
                    {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
                </div>
            </div>

            {toc_html}

            <div class="section">
                {''.join(consolidated_content)}
            </div>

            <div class="footer">
                <strong>Análise Consolidada</strong><br>
                {len(html_files)} autores × ~{total_chars//len(html_files):,} chars cada = {total_chars:,} chars total<br>
                Gerado por Scripturemon Multi-Author Analysis System<br>
                {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
            </div>
        </div>
    </body>
    </html>
    """

    # Salvar
    output_file.write_text(html, encoding='utf-8')

    print(f'✅ HTML consolidado gerado!')
    print(f'📄 Arquivo: {output_file}')
    print(f'💾 Tamanho: {output_file.stat().st_size:,} bytes')
    print()

    print('📊 Resumo:')
    print(f'   Arquivos processados: {len(html_files)}')
    print(f'   Total de caracteres: {total_chars:,}')
    print(f'   Média por autor: {total_chars//len(html_files):,} chars')
    print()

    return output_file


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Consolida múltiplos HTMLs de análise')
    parser.add_argument('--pattern', default='SONHOS_ANALISE_*.html',
                       help='Pattern glob para encontrar HTMLs')
    parser.add_argument('--output', default='SONHOS_ANALISE_COMPLETA',
                       help='Nome base do arquivo consolidado')
    parser.add_argument('--open', action='store_true',
                       help='Abrir HTML no browser após gerar')
    parser.add_argument('--no-translate', action='store_true',
                       help='Não traduzir conteúdo em inglês')

    args = parser.parse_args()

    result = consolidate_html_analyses(
        args.pattern,
        args.output,
        translate=not args.no_translate
    )

    if result and args.open:
        import subprocess
        subprocess.run(['open', str(result)])
        print('🌐 HTML aberto no browser!')
