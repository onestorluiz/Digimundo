#!/usr/bin/env python3
"""
Teste do SDL Collector - Verifica coleta passiva sem modificar comportamento.
"""

import sys
import json
import tempfile
from pathlib import Path

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.sdl.collector import SDLCollector, SAFE_SDL_CONFIG


def test_passive_collection_only():
    """Testa que coleta só acontece em modo passivo."""
    print("\n1. TESTANDO COLETA PASSIVA")
    print("-" * 40)
    
    # Teste 1: SDL enabled = coleta desativada
    config1 = {
        'sdl': {
            'enabled': True,  # SDL ativo = modifica comportamento
            'passive_collect_only': True
        }
    }
    collector1 = SDLCollector(config1)
    
    assert not collector1.is_active(), "Não deve coletar quando SDL está enabled"
    
    # Teste 2: passive_collect_only=False = coleta desativada
    config2 = {
        'sdl': {
            'enabled': False,
            'passive_collect_only': False  # Coleta passiva desativada
        }
    }
    collector2 = SDLCollector(config2)
    
    assert not collector2.is_active(), "Não deve coletar quando passive_collect_only=False"
    
    # Teste 3: Configuração correta para coleta passiva
    config3 = {
        'sdl': {
            'enabled': False,  # SDL desabilitado = não modifica comportamento
            'passive_collect_only': True  # Coleta passiva ativada
        }
    }
    collector3 = SDLCollector(config3)
    
    assert collector3.is_active(), "Deve coletar quando enabled=False e passive_collect_only=True"
    
    print("✅ Lógica de coleta passiva correta")
    print(f"  - enabled=True, passive=True: coleta={collector1.is_active()} (esperado: False)")
    print(f"  - enabled=False, passive=False: coleta={collector2.is_active()} (esperado: False)")
    print(f"  - enabled=False, passive=True: coleta={collector3.is_active()} (esperado: True)")
    
    return True


def test_no_op_behavior():
    """Testa que collect é no-op quando inativo."""
    print("\n2. TESTANDO COMPORTAMENTO NO-OP")
    print("-" * 40)
    
    # Collector inativo
    config = {
        'sdl': {
            'enabled': True,  # SDL ativo = sem coleta
            'passive_collect_only': True
        }
    }
    collector = SDLCollector(config)
    
    # Tentar coletar
    result = collector.collect(
        input_text="teste entrada",
        output_text="teste saída"
    )
    
    assert result == False, "collect deve retornar False quando inativo"
    assert collector.samples_count == 0, "Não deve ter amostras quando inativo"
    
    print("✅ No-op quando inativo")
    print(f"  - Resultado da coleta: {result} (esperado: False)")
    print(f"  - Amostras coletadas: {collector.samples_count} (esperado: 0)")
    
    return True


def test_data_collection():
    """Testa coleta real de dados."""
    print("\n3. TESTANDO COLETA DE DADOS")
    print("-" * 40)
    
    # Usar diretório temporário
    with tempfile.TemporaryDirectory() as tmpdir:
        # Configurar collector ativo
        config = SAFE_SDL_CONFIG.copy()
        config['sdl']['max_samples_per_file'] = 2  # Arquivo pequeno para teste
        
        collector = SDLCollector(config)
        collector.data_dir = Path(tmpdir)  # Usar dir temporário
        collector._init_collection_file()
        
        # Coletar algumas amostras
        samples = [
            ("Como criar um personagem?", "Para criar um personagem..."),
            ("Qual a estrutura de três atos?", "A estrutura de três atos..."),
            ("Como escrever diálogos?", "Diálogos efetivos...")
        ]
        
        for input_text, output_text in samples:
            result = collector.collect(
                input_text=input_text,
                output_text=output_text,
                context={"test": True},
                metadata={"model": "test"}
            )
            assert result == True, f"Coleta deve retornar True"
        
        # Forçar salvamento
        collector.flush()
        
        # Verificar arquivos criados
        files = list(Path(tmpdir).glob("sdl_samples_*.jsonl"))
        assert len(files) > 0, "Deve ter criado arquivo(s) de amostras"
        
        # Verificar conteúdo
        total_samples = 0
        for file in files:
            with open(file, 'r') as f:
                lines = f.readlines()
                total_samples += len(lines)
                
                # Verificar primeira linha
                if lines:
                    sample = json.loads(lines[0])
                    assert 'id' in sample
                    assert 'input' in sample
                    assert 'output' in sample
                    assert 'context' in sample
                    assert 'metadata' in sample
        
        assert total_samples == len(samples), f"Deve ter {len(samples)} amostras salvas"
        
        print(f"✅ Dados coletados corretamente")
        print(f"  - Amostras coletadas: {total_samples}")
        print(f"  - Arquivos criados: {len(files)}")
        
    return True


def test_compression():
    """Testa compressão de dados."""
    print("\n4. TESTANDO COMPRESSÃO")
    print("-" * 40)
    
    collector = SDLCollector(SAFE_SDL_CONFIG)
    
    # Sample grande
    long_text = "A" * 2000
    sample = {
        'id': 'test123',
        'timestamp': '2025-09-05T12:00:00',
        'input': long_text,
        'output': long_text,
        'context': {'key1': 'value1' * 100},
        'metadata': {}
    }
    
    # Comprimir
    compressed = collector._compress_sample(sample)
    
    assert len(compressed['input']) < len(long_text), "Input deve ser truncado"
    assert len(compressed['output']) < len(long_text), "Output deve ser truncado"
    assert compressed['metadata'].get('input_truncated') == True
    assert compressed['metadata'].get('output_truncated') == True
    
    print("✅ Compressão funcionando")
    print(f"  - Input original: {len(long_text)} chars")
    print(f"  - Input comprimido: {len(compressed['input'])} chars")
    print(f"  - Truncado: {compressed['metadata'].get('input_truncated')}")
    
    return True


def test_stats():
    """Testa estatísticas do collector."""
    print("\n5. TESTANDO ESTATÍSTICAS")
    print("-" * 40)
    
    collector = SDLCollector(SAFE_SDL_CONFIG)
    
    stats = collector.get_stats()
    
    assert 'active' in stats
    assert 'enabled' in stats
    assert 'passive_collect_only' in stats
    assert 'total_collected_session' in stats
    assert 'data_dir' in stats
    
    print("✅ Estatísticas disponíveis:")
    for key, value in stats.items():
        print(f"  - {key}: {value}")
    
    return True


def main():
    """Executa todos os testes."""
    print("=" * 60)
    print("TESTE DO SDL COLLECTOR")
    print("=" * 60)
    
    tests = [
        test_passive_collection_only,
        test_no_op_behavior,
        test_data_collection,
        test_compression,
        test_stats
    ]
    
    results = []
    for test in tests:
        try:
            passed = test()
            results.append((test.__name__, passed))
        except Exception as e:
            print(f"❌ Erro no teste {test.__name__}: {e}")
            results.append((test.__name__, False))
    
    # Resumo
    print("\n" + "=" * 60)
    print("RESUMO")
    print("=" * 60)
    
    passed = sum(1 for _, p in results if p)
    total = len(results)
    
    for name, passed in results:
        status = "✅" if passed else "❌"
        print(f"{status} {name}")
    
    print(f"\nTotal: {passed}/{total} testes passaram")
    
    if passed == total:
        print("\n🎉 SDL COLLECTOR FUNCIONANDO CORRETAMENTE!")
    else:
        print("\n⚠️ Alguns testes falharam")
    
    return 0 if passed == total else 1


if __name__ == "__main__":
    exit(main())