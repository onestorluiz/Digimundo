#!/usr/bin/env python3
"""
Comparação de Eficiência - Batman Screenplay Compression
V19 Personalizado vs Batman Ultimate

Assinado: Nestor Luiz, CEO - Digimundo/ScriptureMon Champion
Data: 14/09/2025
"""

import sys
from pathlib import Path
import json
import time
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Adicionar path do projeto
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from apps.scripturemon.digilang_v19_personalized import DigiLangV19Personalized
from apps.scripturemon.digilang_batman_ultimate import DigiLangBatmanUltimate

def compare_compression_methods():
    """Comparar métodos de compressão no Dark Knight"""

    print("=" * 70)
    print("🦇 COMPARAÇÃO DE COMPRESSÃO - THE DARK KNIGHT")
    print("=" * 70)

    # Path do PDF
    pdf_path = "./digilibrary/BIBLIOTECA_ROTEIROS/roteiros_mestres/The Dark Knight - Release.pdf"

    results = {}

    # 1. Testar V19 Personalizado
    print("\n📊 Testando V19 Personalizado...")
    print("-" * 50)

    v19 = DigiLangV19Personalized()
    start_time = time.time()
    v19_result = v19.process_pdf(pdf_path)
    v19_time = time.time() - start_time

    if v19_result and v19_result.get('success'):
        v19_stats = v19_result['stats']
        results['V19 Personalizado'] = {
            'token_compression': v19_stats['token_compression'],
            'tokens_saved': v19_stats['original_tokens'] - v19_stats['compressed_tokens'],
            'original_tokens': v19_stats['original_tokens'],
            'compressed_tokens': v19_stats['compressed_tokens'],
            'dictionary_size': len(v19_result['dictionary']),
            'execution_time': v19_time
        }

        print(f"✅ V19 Personalizado:")
        print(f"   Compressão: {v19_stats['token_compression']:.2f}%")
        print(f"   Tokens salvos: {results['V19 Personalizado']['tokens_saved']:,}")
        print(f"   Dicionário: {results['V19 Personalizado']['dictionary_size']} padrões")
        print(f"   Tempo: {v19_time:.2f}s")
    else:
        print("❌ V19 Personalizado falhou")

    # 2. Testar Batman Ultimate
    print("\n🦇 Testando Batman Ultimate...")
    print("-" * 50)

    batman = DigiLangBatmanUltimate()
    start_time = time.time()
    batman_result = batman.process_batman_screenplay(pdf_path)
    batman_time = time.time() - start_time

    if batman_result and batman_result.get('success'):
        batman_stats = batman_result['stats']
        results['Batman Ultimate'] = {
            'token_compression': batman_stats['token_compression'],
            'tokens_saved': batman_stats['tokens_saved'],
            'original_tokens': batman_stats['original_tokens'],
            'compressed_tokens': batman_stats['compressed_tokens'],
            'dictionary_size': sum(
                len(d) for d in [
                    batman_result['dictionary'].get('characters', {}),
                    batman_result['dictionary'].get('locations', {}),
                    batman_result['dictionary'].get('times', {}),
                    batman_result['dictionary'].get('moods', {}),
                    batman_result['dictionary'].get('actions', {}),
                    batman_result['dictionary'].get('phrases', {}),
                    batman_result['dictionary'].get('technical', {})
                ]
            ),
            'execution_time': batman_time
        }

        print(f"✅ Batman Ultimate:")
        print(f"   Compressão: {batman_stats['token_compression']:.2f}%")
        print(f"   Tokens salvos: {batman_stats['tokens_saved']:,}")
        print(f"   Dicionário: {results['Batman Ultimate']['dictionary_size']} padrões")
        print(f"   Tempo: {batman_time:.2f}s")
    else:
        print("❌ Batman Ultimate falhou")

    # 3. Análise Comparativa
    print("\n" + "=" * 70)
    print("📊 ANÁLISE COMPARATIVA")
    print("=" * 70)

    if len(results) == 2:
        v19_data = results['V19 Personalizado']
        batman_data = results['Batman Ultimate']

        # Comparar compressão
        compression_diff = v19_data['token_compression'] - batman_data['token_compression']
        tokens_diff = v19_data['tokens_saved'] - batman_data['tokens_saved']
        time_diff = v19_data['execution_time'] - batman_data['execution_time']

        print(f"\n📈 Taxa de Compressão:")
        print(f"   V19 Personalizado: {v19_data['token_compression']:.2f}%")
        print(f"   Batman Ultimate: {batman_data['token_compression']:.2f}%")
        print(f"   {'🏆 V19 é melhor' if compression_diff > 0 else '🦇 Batman é melhor'} por {abs(compression_diff):.2f}%")

        print(f"\n💾 Tokens Salvos:")
        print(f"   V19 Personalizado: {v19_data['tokens_saved']:,} tokens")
        print(f"   Batman Ultimate: {batman_data['tokens_saved']:,} tokens")
        print(f"   {'🏆 V19 salva mais' if tokens_diff > 0 else '🦇 Batman salva mais'} {abs(tokens_diff):,} tokens")

        print(f"\n📚 Tamanho do Dicionário:")
        print(f"   V19 Personalizado: {v19_data['dictionary_size']} padrões")
        print(f"   Batman Ultimate: {batman_data['dictionary_size']} padrões")
        dict_efficiency_v19 = v19_data['tokens_saved'] / v19_data['dictionary_size'] if v19_data['dictionary_size'] > 0 else 0
        dict_efficiency_batman = batman_data['tokens_saved'] / batman_data['dictionary_size'] if batman_data['dictionary_size'] > 0 else 0
        print(f"   Eficiência V19: {dict_efficiency_v19:.1f} tokens/padrão")
        print(f"   Eficiência Batman: {dict_efficiency_batman:.1f} tokens/padrão")

        print(f"\n⏱️ Tempo de Execução:")
        print(f"   V19 Personalizado: {v19_data['execution_time']:.2f}s")
        print(f"   Batman Ultimate: {batman_data['execution_time']:.2f}s")
        print(f"   {'🏆 V19 é mais rápido' if time_diff < 0 else '🦇 Batman é mais rápido'} por {abs(time_diff):.2f}s")

        # Análise detalhada
        print("\n" + "=" * 70)
        print("🔍 ANÁLISE DETALHADA")
        print("=" * 70)

        print("\n🎯 Pontos Fortes de cada método:")

        print("\n✅ V19 Personalizado:")
        print("   • Mineração automática de padrões")
        print("   • Dicionário maior e mais abrangente")
        print("   • Melhor taxa de compressão geral")
        print("   • Adaptação automática a qualquer documento")

        print("\n✅ Batman Ultimate:")
        print("   • Símbolos validados garantidamente de 1 token")
        print("   • Categorização hierárquica clara")
        print("   • Mineração específica para roteiros Batman")
        print("   • Menor tempo de execução")

        # Recomendação
        print("\n" + "=" * 70)
        print("💡 RECOMENDAÇÃO")
        print("=" * 70)

        if compression_diff > 2:
            print("\n🏆 V19 Personalizado é significativamente melhor!")
            print(f"   Oferece {compression_diff:.2f}% mais compressão")
            print(f"   Salva {tokens_diff:,} tokens adicionais")
        elif compression_diff > 0:
            print("\n🏆 V19 Personalizado é ligeiramente melhor")
            print(f"   Oferece {compression_diff:.2f}% mais compressão")
        elif compression_diff > -2:
            print("\n🤝 Métodos são equivalentes")
            print("   Diferença de compressão negligível")
        else:
            print("\n🦇 Batman Ultimate é melhor!")
            print(f"   Oferece {abs(compression_diff):.2f}% mais compressão")

        # Insights para melhorias
        print("\n" + "=" * 70)
        print("🚀 INSIGHTS PARA MELHORIAS")
        print("=" * 70)

        print("\n1. Combinar as melhores práticas:")
        print("   • Usar validação de 1 token do Batman Ultimate")
        print("   • Manter mineração automática do V19")
        print("   • Adicionar categorização hierárquica")

        print("\n2. Otimizações possíveis:")
        print("   • Pré-validar pool de símbolos expandido")
        print("   • Implementar cache de padrões por tipo de documento")
        print("   • Usar frases comuns pré-mapeadas para roteiros")

        print("\n3. Próximos passos:")
        print("   • Testar com outros roteiros Batman")
        print("   • Expandir para Marvel/DC universe")
        print("   • Criar dicionários especializados por gênero")

    # Salvar relatório
    report_path = Path("./output/batman_compression_comparison.json")
    report_path.parent.mkdir(exist_ok=True)

    report = {
        'test_date': time.strftime('%Y-%m-%d %H:%M:%S'),
        'pdf_file': pdf_path,
        'results': results,
        'signature': 'Nestor Luiz, CEO - Digimundo/ScriptureMon Champion'
    }

    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print(f"\n📄 Relatório salvo em: {report_path}")

    return results

def main():
    """Função principal"""
    results = compare_compression_methods()

    print("\n" + "=" * 70)
    print("✅ COMPARAÇÃO CONCLUÍDA!")
    print("=" * 70)

    return 0

if __name__ == "__main__":
    sys.exit(main())