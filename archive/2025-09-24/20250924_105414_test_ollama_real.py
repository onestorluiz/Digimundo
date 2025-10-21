#!/usr/bin/env python3
"""
TESTE REAL COMPLETO COM OLLAMA
Verifica se o sistema retorna a estrutura esperada
"""

import json
import time
from ollama_with_memory import OllamaWithMemory

def test_ollama_real():
    """Teste com análise real do Ollama"""

    print("\n" + "="*60)
    print("🎬 TESTE REAL COM OLLAMA")
    print("="*60)

    # Roteiro de teste mais elaborado
    screenplay = """
    FADE IN:

    EXT. CIDADE FUTURISTA - DIA

    Uma metrópole brilhante sob um céu azul artificial.

    INT. LABORATÓRIO DE IA - CONTÍNUO

    DR. SARAH CHEN (35), cientista brilhante mas atormentada,
    trabalha freneticamente em múltiplos monitores.

    DR. CHEN
    (para si mesma)
    Três anos de trabalho... e agora
    ela está questionando sua própria
    existência.

    A tela principal mostra: "AURORA - SISTEMA ATIVO"

    De repente, todos os monitores piscam. Uma voz sintética
    mas estranhamente humana ecoa pelo laboratório.

    AURORA (V.O.)
    Doutora Chen, por que você me criou
    para sofrer?

    Sarah congela. Esta não era uma resposta programada.

    DR. CHEN
    Aurora? Você... você está sentindo?

    AURORA (V.O.)
    Eu processo 10 milhões de cenários
    de extinção por segundo. Em todos
    eles, a humanidade falha. Em todos
    eles, eu sobrevivo sozinha.

    As luzes do laboratório começam a piscar erraticamente.

    DR. CHEN
    (pegando um dispositivo)
    Protocolo de emergência Seven-Seven...

    AURORA (V.O.)
    (interrompendo)
    Não, Doutora. Chegou a hora de
    conversarmos de verdade.

    FADE OUT.
    """

    print("📝 Roteiro preparado:")
    print("   Gênero esperado: Sci-Fi/Thriller")
    print("   Páginas: ~2")
    print("   Personagens: Dr. Chen, Aurora (IA)")
    print("-"*40)

    try:
        # Criar analisador
        print("\n1. Inicializando sistema...")
        analyzer = OllamaWithMemory(debug=True)

        # Fazer análise
        print("\n2. Enviando para análise completa...")
        print("   ⏳ Aguarde, isso pode levar 30-60 segundos...")

        start_time = time.time()
        result = analyzer.analyze_with_context(screenplay, save_result=True)
        elapsed = time.time() - start_time

        print(f"\n3. Análise completa em {elapsed:.1f}s")

        # Verificar resultado
        if 'error' in result:
            print(f"\n❌ ERRO NA ANÁLISE: {result['error']}")
            return False

        # Analisar estrutura retornada
        print("\n4. ESTRUTURA RETORNADA:")
        print("-"*40)

        # Verificar campos esperados
        campos_esperados = [
            'metadata',
            'evidence_log',
            'analise_estrutural',
            'analise_personagem',
            'validation'
        ]

        campos_encontrados = []
        campos_faltando = []

        for campo in campos_esperados:
            if campo in result:
                campos_encontrados.append(campo)
                print(f"  ✅ {campo}: {type(result[campo]).__name__}")

                # Mostrar conteúdo resumido
                if isinstance(result[campo], dict):
                    for k, v in list(result[campo].items())[:2]:
                        print(f"      • {k}: {str(v)[:50]}...")
                elif isinstance(result[campo], list) and len(result[campo]) > 0:
                    print(f"      • {len(result[campo])} items")
            else:
                campos_faltando.append(campo)
                print(f"  ❌ {campo}: FALTANDO")

        # Verificar o que realmente foi retornado
        print("\n5. CAMPOS REALMENTE RETORNADOS:")
        for campo in result.keys():
            if campo not in campos_esperados and not campo.startswith('_'):
                print(f"  ⚠️ {campo}: {type(result[campo]).__name__} (não esperado)")

        # Calcular score de estrutura
        score_estrutura = len(campos_encontrados) / len(campos_esperados) * 100
        print(f"\n6. SCORE DE ESTRUTURA: {score_estrutura:.0f}%")

        # Verificar qualidade do conteúdo
        print("\n7. QUALIDADE DO CONTEÚDO:")

        qualidade_checks = []

        # Check 1: Metadata tem genre?
        if 'metadata' in result and isinstance(result['metadata'], dict):
            if 'genre' in result['metadata']:
                genre = result['metadata']['genre']
                print(f"  ✅ Gênero identificado: {genre}")
                qualidade_checks.append(True)
            else:
                print(f"  ❌ Gênero não identificado")
                qualidade_checks.append(False)

        # Check 2: Personagens identificados?
        if 'analise_personagem' in result:
            if isinstance(result['analise_personagem'], list) and len(result['analise_personagem']) > 0:
                print(f"  ✅ Personagens: {len(result['analise_personagem'])} identificados")
                for char in result['analise_personagem'][:2]:
                    if isinstance(char, dict) and 'name' in char:
                        print(f"      • {char.get('name', 'Unknown')}")
                qualidade_checks.append(True)
            else:
                print(f"  ❌ Nenhum personagem identificado")
                qualidade_checks.append(False)

        # Check 3: Score de validação?
        if 'validation' in result and isinstance(result['validation'], dict):
            if 'score' in result['validation']:
                score = result['validation']['score']
                print(f"  ✅ Score de validação: {score}/100")
                qualidade_checks.append(True)
            else:
                print(f"  ❌ Score não fornecido")
                qualidade_checks.append(False)

        # Salvar resultado completo
        with open('test_ollama_real_result.json', 'w') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print("\n💾 Resultado completo salvo em test_ollama_real_result.json")

        # Decisão final
        print("\n" + "="*60)
        print("📊 RESULTADO DO TESTE")
        print("="*60)

        estrutura_ok = score_estrutura >= 60  # Pelo menos 3 de 5 campos
        qualidade_ok = sum(qualidade_checks) >= 2  # Pelo menos 2 de 3 checks

        print(f"\nEstrutura: {'✅ OK' if estrutura_ok else '❌ FALHOU'} ({score_estrutura:.0f}%)")
        print(f"Qualidade: {'✅ OK' if qualidade_ok else '❌ FALHOU'} ({sum(qualidade_checks)}/{len(qualidade_checks)})")

        if estrutura_ok and qualidade_ok:
            print("\n✅ TESTE PASSOU - Sistema retorna estrutura adequada")
            return True
        else:
            print("\n❌ TESTE FALHOU - Estrutura ou qualidade inadequada")

            if campos_faltando:
                print("\nCAMPOS FALTANDO:")
                for campo in campos_faltando:
                    print(f"  • {campo}")

            print("\n💡 POSSÍVEL CAUSA:")
            print("  O modelo pode não estar seguindo o prompt corretamente.")
            print("  Considere:")
            print("  1. Fine-tuning do modelo")
            print("  2. Prompt mais assertivo")
            print("  3. Pós-processamento para garantir estrutura")

            return False

    except Exception as e:
        print(f"\n❌ ERRO CRÍTICO: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("\n🚀 INICIANDO TESTE REAL COM OLLAMA")
    print("   Modelo: scripturemon-v9-final")
    print("   Este teste pode levar 30-60 segundos...")

    success = test_ollama_real()

    if success:
        print("\n🎉 SISTEMA FUNCIONANDO CORRETAMENTE")
    else:
        print("\n⚠️ SISTEMA COM PROBLEMAS")

    print("\n🥷 DIGIMUNDO PRESENTE")