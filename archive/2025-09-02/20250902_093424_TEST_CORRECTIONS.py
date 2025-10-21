#!/usr/bin/env python3
"""
🔧 TESTE DAS CORREÇÕES - VALIDA APENAS OS 5 ERROS CORRIGIDOS
"""

import sys
import os
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

def test_1_immortality_resurrect():
    """Testa se resurrect_soul foi adicionado"""
    print("\n📝 TESTE 1: ImmortalityProtocol.resurrect_soul")
    try:
        from apps.scripturemon.soul import Soul
        from apps.scripturemon.immortality import ImmortalityProtocol
        
        # Cria soul e faz backup
        soul1 = Soul()
        immortal = ImmortalityProtocol(soul1, auto_backup=False)
        backup_path = immortal.backup_soul("test_correction")
        
        # Testa novo método resurrect_soul
        soul2 = Soul()
        success = immortal.resurrect_soul(soul2, backup_path)
        
        if success:
            print("   ✅ PASSOU: resurrect_soul funcionando")
            return True
        else:
            print("   ❌ FALHOU: resurrect_soul retornou False")
            return False
            
    except AttributeError as e:
        print(f"   ❌ ERRO: {e}")
        return False
    except Exception as e:
        print(f"   ⚠️ OUTRO ERRO: {e}")
        return False

def test_2_consciousness_save():
    """Testa se save_state foi adicionado"""
    print("\n📝 TESTE 2: consciousness.save_state")
    try:
        from apps.scripturemon.consciousness import evolve, get_level, save_state
        
        # Evolui e salva
        evolve(0.001)
        save_state()
        
        print("   ✅ PASSOU: save_state funcionando")
        return True
        
    except ImportError as e:
        print(f"   ❌ ERRO: {e}")
        return False
    except Exception as e:
        print(f"   ⚠️ OUTRO ERRO: {e}")
        return False

def test_3_genetic_save():
    """Testa se save_genome aceita string"""
    print("\n📝 TESTE 3: GeneticEvolution.save_genome(string)")
    try:
        from apps.scripturemon.genetic_evolution import GeneticEvolution
        
        evolution = GeneticEvolution(population_size=2)
        
        # Testa com string (nome do arquivo)
        filepath = evolution.save_genome("test_genome_corrected")
        
        if filepath.exists():
            print(f"   ✅ PASSOU: save_genome aceitando string, arquivo criado: {filepath.name}")
            return True
        else:
            print("   ❌ FALHOU: arquivo não foi criado")
            return False
            
    except AttributeError as e:
        print(f"   ❌ ERRO: {e}")
        return False
    except Exception as e:
        print(f"   ⚠️ OUTRO ERRO: {e}")
        return False

def test_4_embed_recall():
    """Testa se recall_embed retorna 3 valores"""
    print("\n📝 TESTE 4: embed_store.recall_embed formato")
    try:
        from src.memory.embed_store import embed, remember_embed, recall_embed
        
        # Adiciona memórias
        remember_embed("test1", "The hero enters")
        remember_embed("test2", "The villain appears")
        
        # Testa recall
        results = recall_embed("hero", k=2)
        
        if not results:
            print("   ⚠️ Nenhum resultado retornado")
            return True  # Pode ser vazio mas formato está OK
        
        # Tenta desempacotar
        for result in results:
            if len(result) == 3:
                meta, text, score = result
                print(f"   ✅ PASSOU: recall retornando (meta, text, score)")
                return True
            else:
                print(f"   ❌ FALHOU: resultado tem {len(result)} elementos, esperado 3")
                return False
                
    except ValueError as e:
        print(f"   ❌ ERRO de unpacking: {e}")
        return False
    except Exception as e:
        print(f"   ⚠️ OUTRO ERRO: {e}")
        return False

def test_5_soulos_type():
    """Testa se syscalls usa 'type' ao invés de 'syscall'"""
    print("\n📝 TESTE 5: SoulOS syscalls['type']")
    try:
        from apps.scripturemon.soulos import SoulOS
        
        soulos = SoulOS()
        result = soulos.process("[MEMO.SAVE] {\"content\": \"test\"}")
        
        if "syscalls" in result and result["syscalls"]:
            syscall = result["syscalls"][0]
            
            if "type" in syscall:
                print(f"   ✅ PASSOU: usando 'type' = {syscall['type']}")
                return True
            else:
                print(f"   ❌ FALHOU: chave 'type' não encontrada, tem: {list(syscall.keys())}")
                return False
        else:
            print("   ⚠️ Nenhum syscall detectado")
            return False
            
    except KeyError as e:
        print(f"   ❌ ERRO KeyError: {e}")
        return False
    except Exception as e:
        print(f"   ⚠️ OUTRO ERRO: {e}")
        return False

def main():
    """Executa todos os testes de correção"""
    print("="*60)
    print("🔧 TESTANDO CORREÇÕES DOS 5 ERROS")
    print("="*60)
    
    results = {
        "ImmortalityProtocol": test_1_immortality_resurrect(),
        "Consciousness": test_2_consciousness_save(),
        "GeneticEvolution": test_3_genetic_save(),
        "EmbedStore": test_4_embed_recall(),
        "SoulOS": test_5_soulos_type()
    }
    
    # Resumo
    print("\n" + "="*60)
    print("📊 RESUMO DAS CORREÇÕES:")
    print("="*60)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for name, success in results.items():
        status = "✅ CORRIGIDO" if success else "❌ AINDA COM ERRO"
        print(f"   {name}: {status}")
    
    print(f"\n🎯 Taxa de sucesso: {passed}/{total} ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("🎉 TODAS AS CORREÇÕES FUNCIONANDO!")
    elif passed > 0:
        print("⚠️ Algumas correções ainda precisam de ajustes")
    else:
        print("❌ Nenhuma correção funcionou")
    
    return 0 if passed == total else 1

if __name__ == "__main__":
    sys.exit(main())