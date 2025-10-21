#!/usr/bin/env python3
"""
Smoke test mínimo para CI manual.
Testa componentes essenciais sem frameworks pesados.
Exit code 0 = sucesso, 1 = falha.
"""

import sys
import os
import json
import tempfile
from pathlib import Path
from typing import Dict, Any, List

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Imports dos módulos a testar
from src.utils.config_manager import load_config
from src.memory.unified_manager import UnifiedMemoryManager
from src.orchestra.output_mixer import OutputMixer
from src.validator.scoring import ScriptScorer
from src.utils.logging_setup import setup_logging

# Configurar logging para o teste
logger = setup_logging("smoke_test", level="INFO", file_logging=False)


class MockScript:
    """Mock de script para teste de scoring."""
    
    def __init__(self, content: str = "INT. CAFE - DAY\n\nJOHN enters."):
        self.content = content
        self.title = "SMOKE TEST SCRIPT"
        self.author = "Test Author"
    
    def get_content(self) -> str:
        return self.content


def test_config_manager() -> bool:
    """Testa carregamento de configuração."""
    print("\n1. TESTANDO CONFIG MANAGER")
    print("-" * 40)
    
    try:
        # Criar config temporária
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            config_data = {
                'system': {
                    'name': 'smoke_test',
                    'version': '1.0.0'
                },
                'memory': {
                    'time_weighted_retrieval': True,
                    'promote_on_hits': 5
                },
                'rag': {
                    'enabled': False,  # Desabilitar para teste rápido
                    'provider': 'chroma',
                    'k': 8
                },
                'scoring': {
                    'weights': {
                        'structure': 0.3,
                        'emotion': 0.2,
                        'technique': 0.3,
                        'theme': 0.2
                    }
                }
            }
            json.dump(config_data, f)
            config_path = f.name
        
        # Carregar config
        config = load_config(config_path)
        
        # Verificar valores
        assert config['system']['name'] == 'smoke_test', "Config name incorreto"
        assert config['memory']['promote_on_hits'] == 5, "Config memory incorreto"
        
        print(f"✅ Config carregada: {config['system']['name']} v{config['system']['version']}")
        
        # Limpar arquivo temporário
        os.unlink(config_path)
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no config manager: {e}")
        return False


def test_unified_memory(config: Dict) -> bool:
    """Testa UnifiedMemoryManager."""
    print("\n2. TESTANDO UNIFIED MEMORY MANAGER")
    print("-" * 40)
    
    try:
        # Inicializar manager
        manager = UnifiedMemoryManager(config)
        print("✅ Manager inicializado")
        
        # Salvar memória de teste
        mem_id = manager.save_memory(
            "Smoke test memory content",
            tags=['smoke', 'test'],
            importance=0.7
        )
        
        if not mem_id:
            raise Exception("Falha ao salvar memória")
        
        print(f"✅ Memória salva com ID: {mem_id}")
        
        # Buscar contexto
        context = manager.get_context("smoke", max_chunks=3)
        print(f"✅ Contexto recuperado: {len(context)} chunks")
        
        # Verificar se tem resultados
        if len(context) > 0:
            print(f"  - Primeiro chunk: {context[0].get('kind', 'unknown')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no memory manager: {e}")
        return False


def test_output_mixer() -> bool:
    """Testa OutputMixer."""
    print("\n3. TESTANDO OUTPUT MIXER")
    print("-" * 40)
    
    try:
        mixer = OutputMixer()
        
        # Simular outputs de múltiplos modelos
        outputs = {
            'extractor': "Key concepts: conflict, resolution",
            'analyzer': "Three-act structure detected",
            'evaluator': "Needs stronger character arc",
            'synthesizer': "Overall: promising but needs work"
        }
        
        # Processar outputs
        mixed = mixer.mix_outputs(outputs)
        
        # Verificar resultado
        assert 'EXTRATOR' in mixed, "Extrator não encontrado no mix"
        assert 'ANALISADOR' in mixed, "Analisador não encontrado no mix"
        
        print(f"✅ Output mixer processou {len(outputs)} outputs")
        print(f"  - Tamanho do mix: {len(mixed)} chars")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no output mixer: {e}")
        return False


def test_script_scorer(config: Dict) -> bool:
    """Testa ScriptScorer."""
    print("\n4. TESTANDO SCRIPT SCORER")
    print("-" * 40)
    
    try:
        scorer = ScriptScorer(config)
        
        # Criar script mock
        script = MockScript("""
FADE IN:

INT. COFFEE SHOP - DAY

A busy coffee shop. SARAH (30s, tired) sits alone at a corner table.

JOHN (40s, confident) enters and spots her.

JOHN
(approaching)
Mind if I sit?

SARAH
(looking up)
Actually, I do.

John hesitates, then sits anyway.

JOHN
We need to talk about what happened.

SARAH
There's nothing to talk about.

FADE OUT.
        """)
        
        # Calcular score
        result = scorer.score(script)
        
        # Verificar resultado
        assert 'total' in result, "Score total não encontrado"
        assert 'breakdown' in result, "Breakdown não encontrado"
        assert result['total'] > 0, "Score deve ser > 0"
        assert result['total'] <= 100, "Score deve ser <= 100"
        
        print(f"✅ Script scorer calculou score: {result['total']:.1f}/100")
        print(f"  - Estrutura: {result['breakdown']['structure']:.1f}")
        print(f"  - Emoção: {result['breakdown']['emotion']:.1f}")
        print(f"  - Técnica: {result['breakdown']['technique']:.1f}")
        print(f"  - Tema: {result['breakdown']['theme']:.1f}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no script scorer: {e}")
        return False


def test_integration(config: Dict) -> bool:
    """Testa integração entre componentes."""
    print("\n5. TESTANDO INTEGRAÇÃO")
    print("-" * 40)
    
    try:
        # Inicializar componentes
        manager = UnifiedMemoryManager(config)
        mixer = OutputMixer()
        scorer = ScriptScorer(config)
        
        print("✅ Componentes inicializados")
        
        # Pipeline simulado
        # 1. Buscar contexto
        context = manager.get_context("test integration", max_chunks=2)
        print(f"✅ Contexto: {len(context)} chunks")
        
        # 2. Simular outputs de modelos
        outputs = {
            'extractor': f"Context has {len(context)} items",
            'analyzer': "Integration test running",
            'evaluator': "All systems operational",
            'synthesizer': "Test successful"
        }
        
        # 3. Mixar outputs
        mixed = mixer.mix_outputs(outputs)
        print(f"✅ Output mixado: {len(mixed)} chars")
        
        # 4. Score de um script
        script = MockScript(mixed[:500])  # Usar output como script
        result = scorer.score(script)
        print(f"✅ Score calculado: {result['total']:.1f}")
        
        # Verificar pipeline completo
        assert len(context) >= 0, "Contexto deve ter >= 0 items"
        assert len(mixed) > 0, "Output mixado deve ter conteúdo"
        assert result['total'] > 0, "Score deve ser > 0"
        
        return True
        
    except Exception as e:
        print(f"❌ Erro na integração: {e}")
        return False


def main() -> int:
    """
    Executa smoke tests.
    
    Returns:
        0 se sucesso, 1 se falha
    """
    print("=" * 60)
    print("SMOKE TEST - SCRIPTUREMON VALIDATION")
    print("=" * 60)
    
    all_passed = True
    results = {}
    
    # Configuração base
    config = {
        'system': {'name': 'smoke_test', 'version': '1.0.0'},
        'memory': {'time_weighted_retrieval': True, 'promote_on_hits': 5},
        'rag': {'enabled': False, 'provider': 'chroma', 'k': 8},
        'scoring': {
            'weights': {
                'structure': 0.3,
                'emotion': 0.2,
                'technique': 0.3,
                'theme': 0.2
            }
        }
    }
    
    # Executar testes
    tests = [
        ("Config Manager", lambda: test_config_manager()),
        ("Unified Memory", lambda: test_unified_memory(config)),
        ("Output Mixer", lambda: test_output_mixer()),
        ("Script Scorer", lambda: test_script_scorer(config)),
        ("Integration", lambda: test_integration(config))
    ]
    
    for test_name, test_func in tests:
        try:
            passed = test_func()
            results[test_name] = passed
            if not passed:
                all_passed = False
        except Exception as e:
            print(f"\n❌ ERRO FATAL em {test_name}: {e}")
            results[test_name] = False
            all_passed = False
    
    # Resumo
    print("\n" + "=" * 60)
    print("RESUMO DOS TESTES")
    print("=" * 60)
    
    for test_name, passed in results.items():
        status = "✅ PASSOU" if passed else "❌ FALHOU"
        print(f"{test_name:20} {status}")
    
    print("-" * 60)
    total = len(results)
    passed_count = sum(1 for p in results.values() if p)
    print(f"Total: {passed_count}/{total} testes passaram")
    
    if all_passed:
        print("\n🎉 TODOS OS TESTES PASSARAM!")
        print("=" * 60)
        return 0
    else:
        print("\n⚠️  ALGUNS TESTES FALHARAM")
        print("=" * 60)
        return 1


if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n⚠️  Teste interrompido pelo usuário")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ ERRO FATAL NÃO TRATADO: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)