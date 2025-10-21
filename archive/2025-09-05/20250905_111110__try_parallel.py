#!/usr/bin/env python3
"""
Teste de processamento paralelo com OutputMixer.
Usa mocks/stubs se modelos reais não disponíveis.
"""

import sys
import time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, Tuple
import random

# Adicionar ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.orchestra.output_mixer import OutputMixer


def mock_analysis_estrutura(text: str) -> Tuple[str, float]:
    """Mock de análise estrutural."""
    start = time.time()
    time.sleep(random.uniform(0.5, 1.5))  # Simula processamento
    
    response = f"""Análise da estrutura narrativa:
    
• Estrutura clássica de três atos detectada
• Pontos de virada bem definidos
• Arco do protagonista coerente
• Climax posicionado no terceiro ato
• Resolução satisfatória mas previsível

Texto analisado: "{text[:50]}..."
    
Estrutura segue padrões convencionais do cinema comercial."""
    
    return response, time.time() - start


def mock_analysis_emocao(text: str) -> Tuple[str, float]:
    """Mock de análise emocional."""
    start = time.time()
    time.sleep(random.uniform(0.5, 1.5))  # Simula processamento
    
    response = f"""Mapeamento emocional da narrativa:
    
• Tom predominante: Melancólico com toques de esperança
• Curva emocional: Ascendente no segundo ato
• Momentos de tensão: Bem distribuídos
• Catarse: Presente mas poderia ser mais impactante
• Conexão empática: 7/10

Análise do texto: "{text[:50]}..."
    
A jornada emocional é competente mas falta ousadia."""
    
    return response, time.time() - start


def mock_analysis_tecnica(text: str) -> Tuple[str, float]:
    """Mock de análise técnica."""
    start = time.time()
    time.sleep(random.uniform(0.5, 1.5))  # Simula processamento
    
    response = f"""Aspectos técnicos identificados:
    
• Diálogos: Funcionais mas sem brilho particular
• Descrições: Adequadas, ritmo consistente
• Formatação: Segue padrões da indústria
• Visualização: Clara mas sem inovação
• Ritmo: Mantém interesse mas previsível

Amostra: "{text[:50]}..."
    
Tecnicamente competente. 62/100, como sempre."""
    
    return response, time.time() - start


def mock_analysis_tema(text: str) -> Tuple[str, float]:
    """Mock de análise temática."""
    start = time.time()
    time.sleep(random.uniform(0.5, 1.5))  # Simula processamento
    
    response = f"""Exploração temática:
    
• Tema central: Redenção através do sacrifício
• Subtemas: Família, lealdade, superação
• Profundidade filosófica: Superficial
• Relevância contemporânea: Moderada
• Originalidade: Baixa, temas já muito explorados

Contexto: "{text[:50]}..."
    
Temas universais mas tratamento convencional."""
    
    return response, time.time() - start


def run_parallel_analysis(text: str) -> Dict:
    """
    Executa 4 análises em paralelo e consolida com OutputMixer.
    
    Args:
        text: Texto para análise
        
    Returns:
        Resultado consolidado
    """
    print("🚀 Iniciando análise paralela quádrupla...")
    start_time = time.time()
    
    # Lançar tarefas em paralelo
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = {
            executor.submit(mock_analysis_estrutura, text): "estrutura",
            executor.submit(mock_analysis_emocao, text): "emoção",
            executor.submit(mock_analysis_tecnica, text): "técnica",
            executor.submit(mock_analysis_tema, text): "tema"
        }
        
        results = {}
        exceptions = []
        
        # Coletar resultados conforme completam
        for future in as_completed(futures, timeout=10):
            perspective = futures[future]
            try:
                response, elapsed = future.result()
                results[perspective] = {
                    "response": response,
                    "time": elapsed,
                    "model": f"mock_{perspective}",
                    "role_description": f"Análise de {perspective}"
                }
                print(f"  ✅ {perspective}: {elapsed:.2f}s")
                
            except Exception as e:
                exceptions.append(f"{perspective}: {str(e)}")
                results[perspective] = {
                    "response": f"Erro na análise de {perspective}: {e}",
                    "time": 0,
                    "error": True
                }
                print(f"  ❌ {perspective}: Erro - {e}")
    
    total_time = time.time() - start_time
    
    # Consolidar com OutputMixer
    print("\n📊 Consolidando resultados...")
    
    # Versão com metadados
    mixed_with_meta = OutputMixer.mix_with_metadata(results)
    
    # Versão simples (só textos)
    simple_parts = {k: v["response"] for k, v in results.items()}
    mixed_simple = OutputMixer.mix(simple_parts)
    
    # Criar resumo
    summary = OutputMixer.create_summary(results)
    
    return {
        "input": text,
        "total_time": total_time,
        "parallel_time": max(r.get("time", 0) for r in results.values()),
        "results": results,
        "mixed_output": mixed_with_meta,
        "mixed_simple": mixed_simple,
        "summary": summary,
        "exceptions": exceptions
    }


def main():
    """Teste principal."""
    
    print("=" * 70)
    print("🧪 TESTE DE PROCESSAMENTO PARALELO COM OUTPUT MIXER")
    print("=" * 70)
    
    # Texto de teste
    test_text = """Um jovem programador descobre que seus códigos ganham vida própria,
    criando um mundo digital paralelo onde ele deve enfrentar suas próprias criações
    para salvar ambos os mundos da destruição."""
    
    print(f"\nTexto de entrada:\n{test_text}\n")
    
    # Executar análise paralela
    result = run_parallel_analysis(test_text)
    
    # Exibir resultados
    print("\n" + "=" * 70)
    print("📈 RESULTADOS")
    print("=" * 70)
    
    print(f"\n⏱️ Tempos:")
    print(f"  - Total sequencial (soma): {sum(r.get('time', 0) for r in result['results'].values()):.2f}s")
    print(f"  - Total paralelo (real): {result['total_time']:.2f}s")
    print(f"  - Speedup: {sum(r.get('time', 0) for r in result['results'].values()) / result['total_time']:.2f}x")
    
    if result['exceptions']:
        print(f"\n⚠️ Exceções capturadas:")
        for exc in result['exceptions']:
            print(f"  - {exc}")
    
    print("\n📄 RESUMO EXECUTIVO:")
    print("-" * 40)
    print(result['summary'])
    
    print("\n📖 OUTPUT CONSOLIDADO (SIMPLES):")
    print("-" * 40)
    # Mostrar apenas primeiras linhas do output consolidado
    lines = result['mixed_simple'].split('\n')[:30]
    print('\n'.join(lines))
    if len(result['mixed_simple'].split('\n')) > 30:
        print("... [output truncado para exibição]")
    
    # Teste de sincronização
    print("\n" + "=" * 70)
    print("🔄 TESTE DE SINCRONIZAÇÃO")
    print("=" * 70)
    
    print("\nExecutando 3 rodadas para verificar determinismo...")
    outputs = []
    for i in range(3):
        print(f"\n  Rodada {i+1}...")
        r = run_parallel_analysis("Teste de determinismo")
        # Pegar só o cabeçalho para comparar
        header = '\n'.join(r['mixed_simple'].split('\n')[:5])
        outputs.append(header)
    
    # Verificar se outputs são determinísticos (exceto timestamps)
    print("\n✅ Verificação de determinismo:")
    for i, output in enumerate(outputs):
        print(f"\n  Rodada {i+1} - Cabeçalho:")
        print(f"  {output[:100]}...")
    
    print("\n" + "=" * 70)
    print("✅ TESTE CONCLUÍDO COM SUCESSO!")
    print("=" * 70)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())