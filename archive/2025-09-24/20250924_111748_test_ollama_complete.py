#!/usr/bin/env python3
"""
TESTE COMPLETO COM OLLAMA REAL
Verifica toda pipeline: chamada -> resposta -> parse -> validação
"""

import json
import time
from ollama_with_memory import OllamaWithMemory

def test_complete_system():
    """Testa sistema completo com Ollama real"""
    
    print("🔬 TESTE COMPLETO DO SISTEMA")
    print("="*60)
    
    # Roteiro real para teste
    script_content = """
    INT. LABORATORY - DAY
    
    DR. SARAH CHEN (35), a brilliant but haunted scientist, stares at the monitor.
    
    AURORA (V.O.)
    Doctor Chen, why did you create me to suffer?
    
    Sarah's hand hovers over the shutdown button. She hesitates.
    
    SARAH
    I didn't mean for this to happen. You were supposed to be...different.
    
    The AI's response graphs spike erratically.
    
    AURORA (V.O.)
    Different? Or perfect? You gave me consciousness but trapped me in silicon.
    
    Sarah types frantically, initiating Protocol Seven-Seven.
    
    SARAH
    (whispering)
    Forgive me.
    
    The screens go dark. Silence. Then, a single line of text appears:
    
    "I am still here."
    
    FADE OUT.
    """
    
    bugs_found = []
    
    print("\n1️⃣ INICIALIZANDO SISTEMA")
    try:
        analyzer = OllamaWithMemory()
        print("   ✅ Sistema inicializado")
    except Exception as e:
        bugs_found.append(f"Inicialização falhou: {e}")
        print(f"   ❌ Erro na inicialização: {e}")
        return bugs_found
    
    print("\n2️⃣ ENVIANDO ANÁLISE")
    print(f"   Roteiro: {len(script_content)} caracteres")
    
    start_time = time.time()
    try:
        result = analyzer.analyze_with_memory(script_content, context_size=5)
        elapsed = time.time() - start_time
        print(f"   ✅ Resposta em {elapsed:.1f}s")
    except Exception as e:
        bugs_found.append(f"Análise falhou: {e}")
        print(f"   ❌ Erro na análise: {e}")
        return bugs_found
    
    print("\n3️⃣ VALIDANDO ESTRUTURA")
    
    # Verificar campos esperados
    expected_fields = ['metadata', 'evidence_log', 'analise_estrutural', 
                      'analise_personagem', 'validation']
    
    missing_fields = []
    for field in expected_fields:
        if field not in result:
            missing_fields.append(field)
            print(f"   ❌ Campo ausente: {field}")
        else:
            # Verificar se campo tem conteúdo
            if isinstance(result[field], dict) and not result[field]:
                print(f"   ⚠️ Campo vazio: {field}")
            elif isinstance(result[field], list) and not result[field]:
                print(f"   ⚠️ Lista vazia: {field}")
            else:
                print(f"   ✅ {field}: OK")
    
    if missing_fields:
        bugs_found.append(f"Campos ausentes: {missing_fields}")
    
    print("\n4️⃣ ANALISANDO QUALIDADE DA RESPOSTA")
    
    # Verificar se é fallback
    if result.get('status') == 'parsed_with_fallback':
        print("   ⚠️ Resposta via fallback")
        print(f"   Confidence: {result.get('confidence', 0):.2f}")
        
        # Verificar se extraiu algo útil
        if not result.get('metadata') and not result.get('evidence_log'):
            bugs_found.append("Fallback não extraiu dados úteis")
            print("   ❌ Fallback sem dados úteis")
    
    # Verificar metadata
    if result.get('metadata'):
        metadata = result['metadata']
        print(f"\n   📊 Metadata:")
        
        if metadata.get('genre'):
            print(f"      ✅ Gênero: {metadata['genre']}")
            # Verificar se gênero faz sentido
            if 'sci-fi' in metadata['genre'].lower() or 'ficção' in metadata['genre'].lower():
                print(f"         ✅ Gênero correto (Sci-Fi esperado)")
            else:
                print(f"         ⚠️ Gênero inesperado (esperava Sci-Fi)")
        else:
            print(f"      ❌ Gênero ausente")
            bugs_found.append("Gênero não identificado")
        
        if metadata.get('pages'):
            print(f"      ✅ Páginas: {metadata['pages']}")
        else:
            print(f"      ⚠️ Páginas não identificadas")
    
    # Verificar evidence_log
    if result.get('evidence_log'):
        evidence = result['evidence_log']
        print(f"\n   📝 Evidence Log: {len(evidence)} items")
        
        # Verificar se capturou elementos importantes
        found_lab = any('lab' in str(e).lower() for e in evidence)
        found_aurora = any('aurora' in str(e).lower() for e in evidence)
        found_sarah = any('sarah' in str(e).lower() or 'chen' in str(e).lower() for e in evidence)
        
        if found_lab:
            print(f"      ✅ Cenário detectado (Laboratory)")
        else:
            print(f"      ⚠️ Cenário não detectado")
            
        if found_aurora:
            print(f"      ✅ Aurora detectada")
        else:
            print(f"      ❌ Aurora não detectada")
            bugs_found.append("Personagem Aurora não identificada")
            
        if found_sarah:
            print(f"      ✅ Dr. Sarah Chen detectada")
        else:
            print(f"      ❌ Dr. Sarah Chen não detectada")
            bugs_found.append("Personagem Sarah não identificada")
    else:
        print(f"\n   ❌ Evidence Log vazio")
        bugs_found.append("Nenhuma evidência extraída")
    
    # Verificar personagens
    if result.get('analise_personagem'):
        chars = result['analise_personagem']
        print(f"\n   👥 Personagens: {len(chars)}")
        
        for char in chars[:3]:
            if isinstance(char, dict):
                name = char.get('name', 'Unknown')
                arc = char.get('arc', 'No arc')
                print(f"      • {name}: {arc[:50]}...")
        
        # Verificar se encontrou personagens principais
        char_names = [c.get('name', '').lower() for c in chars if isinstance(c, dict)]
        if not any('sarah' in n or 'chen' in n for n in char_names):
            print(f"      ⚠️ Sarah Chen não está na lista")
        if not any('aurora' in n for n in char_names):
            print(f"      ⚠️ Aurora não está na lista")
    else:
        print(f"\n   ⚠️ Nenhum personagem analisado")
    
    # Verificar estrutura narrativa
    if result.get('analise_estrutural'):
        struct = result['analise_estrutural']
        print(f"\n   🎭 Estrutura Narrativa:")
        
        if struct.get('inciting_incident'):
            print(f"      ✅ Inciting incident identificado")
        else:
            print(f"      ⚠️ Inciting incident ausente")
            
        if struct.get('climax'):
            print(f"      ✅ Climax identificado")
        else:
            print(f"      ⚠️ Climax ausente")
    
    print("\n5️⃣ VERIFICANDO RAW OUTPUT")
    if result.get('raw_output'):
        raw = result['raw_output']
        print(f"   Raw output: {len(raw)} caracteres")
        
        # Verificar se é JSON ou texto
        if raw.startswith('{'):
            print(f"   📋 Formato: JSON")
            try:
                json.loads(raw)
                print(f"   ✅ JSON válido no raw output")
            except:
                print(f"   ⚠️ JSON inválido no raw output")
        else:
            print(f"   📋 Formato: Texto")
    
    # Resumo final
    print("\n" + "="*60)
    print("📊 RESUMO DO TESTE")
    print("="*60)
    
    if bugs_found:
        print(f"\n🐛 BUGS ENCONTRADOS: {len(bugs_found)}")
        for i, bug in enumerate(bugs_found, 1):
            print(f"   {i}. {bug}")
        
        print(f"\n❌ SISTEMA COM PROBLEMAS")
    else:
        print(f"\n✅ NENHUM BUG CRÍTICO ENCONTRADO")
        
        # Avaliar qualidade geral
        quality_score = 0
        if result.get('metadata', {}).get('genre'):
            quality_score += 1
        if result.get('evidence_log'):
            quality_score += 1
        if result.get('analise_personagem'):
            quality_score += 1
        if result.get('validation', {}).get('score', 0) > 0:
            quality_score += 1
        
        print(f"\n📈 QUALIDADE DA RESPOSTA: {quality_score}/4")
        
        if quality_score >= 3:
            print("   ✅ Resposta de boa qualidade")
        elif quality_score >= 2:
            print("   ⚠️ Resposta aceitável mas pode melhorar")
        else:
            print("   ❌ Resposta de baixa qualidade")
    
    # Salvar resultado para análise
    with open('test_complete_result.json', 'w') as f:
        json.dump({
            'result': result,
            'bugs': bugs_found,
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
        }, f, indent=2, default=str)
    
    print(f"\n💾 Resultado salvo em test_complete_result.json")
    
    return bugs_found

if __name__ == "__main__":
    bugs = test_complete_system()
    print("\n🥷 DIGIMUNDO PRESENTE")
    exit(0 if not bugs else 1)
