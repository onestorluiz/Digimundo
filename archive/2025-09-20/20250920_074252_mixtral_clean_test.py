#!/usr/bin/env python3
"""
🧪 TESTE LIMPO MIXTRAL - SEM COMPLEXIDADES
Teste direto e simples para verificar funcionalidade básica
"""

import ollama
import time
from pathlib import Path


def test_mixtral_basic():
    """Teste básico do Mixtral sem dependências complexas"""

    print("🧪 TESTE BÁSICO MIXTRAL Q5")
    print("=" * 40)

    model = "mixtral-dedicated-q5"

    # Teste simples com prompt pequeno
    prompt = """Analyze this screenplay scene:

FADE IN:

INT. OFFICE - DAY

JOHN (30s) sits at his desk, staring at a computer screen.

JOHN
(to himself)
This doesn't make sense.

He picks up a phone and dials.

JOHN (CONT'D)
(into phone)
We need to talk.

FADE OUT.

Provide a brief Save the Cat analysis of this scene."""

    try:
        print(f"🧠 Modelo: {model}")
        print(f"📝 Prompt: {len(prompt)} caracteres")
        print("⏳ Processando...")

        start_time = time.time()

        response = ollama.generate(
            model=model,
            prompt=prompt,
            options={
                'num_ctx': 32768,    # Contexto menor para teste
                'num_thread': 14,
                'num_gpu': 50,
                'temperature': 0.3,
                'num_predict': 500
            }
        )

        end_time = time.time()
        duration = end_time - start_time

        analysis = response['response']

        print(f"\\n✅ SUCESSO!")
        print(f"⏱️ Tempo: {duration:.1f}s")
        print(f"📊 Resposta: {len(analysis)} caracteres")
        print(f"\\n📋 ANÁLISE GERADA:")
        print("-" * 40)
        print(analysis[:400] + "..." if len(analysis) > 400 else analysis)

        return True

    except Exception as e:
        print(f"\\n❌ ERRO: {e}")
        return False


def test_library_access():
    """Teste de acesso à biblioteca de roteiros"""

    print("\\n\\n📚 TESTE BIBLIOTECA DE ROTEIROS")
    print("=" * 40)

    library_path = Path("digilibrary/BIBLIOTECA_ROTEIROS/roteiros_mestres")

    if not library_path.exists():
        print(f"❌ Caminho não existe: {library_path}")
        return False

    txt_files = list(library_path.glob("*.txt"))
    print(f"📁 Pasta: {library_path}")
    print(f"📄 Arquivos .txt encontrados: {len(txt_files)}")

    if txt_files:
        # Testar primeiro arquivo
        first_file = txt_files[0]
        print(f"\\n🎬 Teste com: {first_file.name}")

        try:
            content = first_file.read_text(encoding='utf-8', errors='ignore')
            print(f"📊 Tamanho: {len(content):,} caracteres")
            print(f"📝 Preview: {content[:200]}...")
            return True
        except Exception as e:
            print(f"❌ Erro ao ler arquivo: {e}")
            return False
    else:
        print("❌ Nenhum arquivo .txt encontrado")
        return False


def main():
    """Função principal de teste"""

    print("🚀 TESTE COMPLETO MIXTRAL SYSTEM")
    print("=" * 50)

    # 1. Teste básico do modelo
    model_ok = test_mixtral_basic()

    # 2. Teste da biblioteca
    library_ok = test_library_access()

    print(f"\\n\\n📊 RESULTADOS:")
    print(f"🧠 Modelo Mixtral: {'✅' if model_ok else '❌'}")
    print(f"📚 Biblioteca: {'✅' if library_ok else '❌'}")

    if model_ok and library_ok:
        print("\\n🎉 SISTEMA FUNCIONANDO!")
        print("Pronto para processamento completo.")
    else:
        print("\\n⚠️ PROBLEMAS DETECTADOS")
        print("Verificar configurações antes de usar.")

    print("\\nDIGIMUNDO PRESENTE 🥷")


if __name__ == "__main__":
    main()