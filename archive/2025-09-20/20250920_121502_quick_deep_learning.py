#!/usr/bin/env python3
"""
⚡ QUICK DEEP LEARNING - Versão simplificada e funcional
Machine Learning com deeplearning-cinema (mixtral-r1:32b customizado)
"""

import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent.parent))  # Corrigir path para src

from src.core.unified_memory_system import get_unified_memory, MemoryType
from src.core.screenplay_library import get_screenplay_library

def analyze_save_the_cat():
    """Análise específica de Save the Cat com exemplos"""

    print("🧠 DEEP LEARNING: SAVE THE CAT")
    print("=" * 60)

    # Carregar Save the Cat
    teoria_path = Path("digilibrary/BIBLIOTECA_ROTEIROS/teoria/Save The Cat.txt")
    if not teoria_path.exists():
        print("❌ Save The Cat.txt não encontrado!")
        return

    book_content = teoria_path.read_text(encoding='utf-8', errors='ignore')
    print(f"📚 Livro carregado: {len(book_content)} caracteres")

    # Carregar exemplo de roteiro diretamente
    roteiro_path = Path("digilibrary/BIBLIOTECA_ROTEIROS/roteiros_mestres/Inception - Screenplay.docx.txt")
    if not roteiro_path.exists():
        # Tentar outro
        roteiro_path = Path("digilibrary/BIBLIOTECA_ROTEIROS/roteiros_mestres/The Matrix - Screenplay.docx.txt")

    if roteiro_path.exists():
        screenplay = roteiro_path.read_text(encoding='utf-8', errors='ignore')
        print(f"🎬 Roteiro: {roteiro_path.stem}")
    else:
        print("❌ Nenhum roteiro exemplo disponível")
        return

    print(f"🎬 Roteiro carregado: {len(screenplay)} caracteres")

    # Truncar para caber em 128K tokens
    book_sample = book_content[:200000]  # ~50K tokens
    screenplay_sample = screenplay[:100000]  # ~25K tokens

    # Criar prompt específico
    prompt = f"""Analyze Save the Cat concepts in a real screenplay.

BOOK EXCERPT (Save the Cat):
{book_sample}

SCREENPLAY EXCERPT:
{screenplay_sample}

Find and explain these Save the Cat beats in the screenplay:
1. Opening Image (page 1)
2. Theme Stated (page 5)
3. Set-up (pages 1-10)
4. Catalyst (page 12)
5. Debate (pages 12-25)
6. Break into Two (page 25)
7. B Story (page 30)
8. Fun and Games (pages 30-55)
9. Midpoint (page 55)
10. Bad Guys Close In (pages 55-75)
11. All Is Lost (page 75)
12. Dark Night of the Soul (pages 75-85)
13. Break into Three (page 85)
14. Finale (pages 85-110)
15. Final Image (page 110)

For each beat found, provide:
- The exact text/scene from the screenplay
- Page or time estimate
- How it matches Blake Snyder's description

Be specific with examples."""

    print("\n🤖 Chamando deeplearning-cinema (2-5 minutos)...")

    # Preparar comando
    payload = {
        'model': 'mixtral-dedicated-q5',  # Modelo híbrido otimizado!
        'prompt': prompt,
        'stream': False
    }

    try:
        # Chamar Ollama
        result = subprocess.run(
            ['curl', '-s', '--max-time', '300',
             'http://localhost:11434/api/generate',
             '-d', json.dumps(payload)],
            capture_output=True,
            text=True
        )

        if result.returncode == 0 and result.stdout:
            response = json.loads(result.stdout)
            analysis = response.get('response', '')

            print("\n📊 ANÁLISE COMPLETA!")
            print("-" * 60)
            print(analysis[:2000])  # Primeiros 2000 chars
            print("-" * 60)

            # Salvar na memória
            memory = get_unified_memory()
            memory.store(
                memory_type=MemoryType.KNOWLEDGE,
                key="save_the_cat_analysis",
                value={
                    'analysis': analysis,
                    'book': 'Save The Cat',
                    'screenplay': 'Example',
                    'timestamp': datetime.now().isoformat()
                },
                confidence=0.95,
                source='deep_learning'
            )

            print("\n✅ Análise salva na memória unificada!")

    except Exception as e:
        print(f"❌ Erro: {e}")

def test_quick_concept():
    """Teste rápido de conceito específico"""

    print("\n🔍 TESTE RÁPIDO: Three-Act Structure")
    print("=" * 60)

    prompt = """Explain the three-act structure in 100 words.
Give one specific example from The Matrix.
Be precise with timing."""

    payload = {
        'model': 'mixtral-dedicated-q5',  # Modelo híbrido otimizado!
        'prompt': prompt,
        'stream': False
    }

    print("🤖 Processando...")

    try:
        result = subprocess.run(
            ['curl', '-s', '--max-time', '60',
             'http://localhost:11434/api/generate',
             '-d', json.dumps(payload)],
            capture_output=True,
            text=True
        )

        if result.returncode == 0 and result.stdout:
            response = json.loads(result.stdout)
            print("\n💡 RESPOSTA:")
            print(response.get('response', 'Sem resposta'))

    except Exception as e:
        print(f"❌ Erro: {e}")

def main():
    print("🎯 QUICK DEEP LEARNING")
    print("1. Analisar Save the Cat")
    print("2. Teste rápido de conceito")

    choice = input("\nEscolha (1-2): ").strip()

    if choice == '1':
        analyze_save_the_cat()
    elif choice == '2':
        test_quick_concept()

    # Verificar memória
    memory = get_unified_memory()
    stats = memory.get_stats()
    print(f"\n💾 MEMÓRIA: {stats['total_entries']} entradas, {stats['db_size_kb']:.1f} KB")

if __name__ == "__main__":
    main()