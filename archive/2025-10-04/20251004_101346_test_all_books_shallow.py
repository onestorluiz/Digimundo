#!/usr/bin/env python3
"""
Teste: DrDialogue com specialist_type='all' em SHALLOW mode
(Para ver citações organizadas por autor no output final)
"""

import sys
from pathlib import Path
import time

sys.path.insert(0, str(Path.cwd()))

from triple_core.core_1_specialists.dialogue.dr_dialogue import DrDialogue
from triple_core.orchestrators.dual_core_wrapper import DualCoreWrapper

print('='*80)
print('📚 TESTE: DrDialogue com TODOS OS 13 LIVROS (SHALLOW MODE)')
print('='*80)
print()

# Carregar roteiro (primeiras 1000 palavras)
screenplay_path = Path('content/screenplays/personal/sonhos_sem_lembrancas_t3.txt')
screenplay = screenplay_path.read_text(encoding='utf-8', errors='ignore')
screenplay_excerpt = ' '.join(screenplay.split()[:1000])

print(f'📄 Roteiro: {len(screenplay_excerpt.split())} palavras')
print()

# Criar wrapper com specialist_type='all' + SHALLOW mode
print('🔧 Configurando DualCoreWrapper...')
specialist = DrDialogue()
wrapper = DualCoreWrapper(
    python_specialist=specialist,
    llm_model='scripturemon-optimized',
    llm_timeout=600,
    use_theory=True,
    deep_context=False,  # ⚡ SHALLOW para ver citações por autor
    specialist_type='all'  # ⚡ TODOS OS LIVROS!
)

print(f'   ✅ Specialist: {wrapper.specialist_name}')
print(f'   ✅ Theory Mode: specialist_type="all"')
print(f'   ✅ Deep Context: False (Shallow = chunks organizados por autor)')
print()

# Executar análise
print('⏳ Executando análise Shallow com TODOS os livros...')
print('   (Estimativa: ~2-3 minutos)')
print()

start = time.time()
result = wrapper.analyze(screenplay_excerpt)
elapsed = time.time() - start

print()
print('='*80)
print('✅ ANÁLISE COMPLETA!')
print('='*80)
print()
print(f'⏱️  Tempo: {elapsed:.1f}s ({elapsed/60:.1f} minutos)')

# Verificar output
llm_text = result.get('llm_insights', '')
print(f'📏 Output LLM: {len(llm_text):,} chars ({len(llm_text.split())} palavras)')
print()

# Verificar citações por autor
print('📚 Verificando citações por autor no OUTPUT FINAL:')
authors_found = []
for author in ['MCKEE', 'TRUBY', 'CAMPBELL', 'SNYDER', 'FIELD', 'EGRI', 'VOGLER', 'SEGER', 'WEILAND']:
    if author in llm_text.upper():
        count = llm_text.upper().count(author)
        authors_found.append(f"   ✅ {author}: {count} menções")

if authors_found:
    print('\n'.join(authors_found))
    print()
    print('   ✅ SUCESSO: LLM está citando múltiplos autores!')
else:
    print('   ℹ️  LLM não mencionou autores explicitamente (mas recebeu contexto organizado)')
print()

# Salvar output LLM completo
output_file = Path('workspace/outputs/test_all_books_shallow_result.txt')
output_file.parent.mkdir(parents=True, exist_ok=True)
output_file.write_text(llm_text, encoding='utf-8')
print(f'💾 Output LLM completo salvo em: {output_file}')
print()

# Exportar para HTML
print('📤 Exportando para HTML...')
html_path = wrapper.export_formatted(
    result,
    screenplay_title="SONHOS_ALL_BOOKS_SHALLOW",
    format="html",
    auto_open=True  # ⚡ Abre automaticamente
)

print(f'✅ HTML gerado: {html_path}')
print(f'💾 Tamanho: {html_path.stat().st_size:,} bytes')
print()

# Preview do output
print('📄 Preview (primeiros 3000 chars):')
print('-' * 80)
print(llm_text[:3000])
print('-' * 80)
print()

print('✅ HTML aberto automaticamente no browser!')
print()
