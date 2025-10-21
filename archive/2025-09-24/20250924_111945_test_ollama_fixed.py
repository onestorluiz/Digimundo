#!/usr/bin/env python3
"""
TESTE COMPLETO COM OLLAMA REAL - CORRIGIDO
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
        print(f"   Modelo: {analyzer.model}")
    except Exception as e:
        bugs_found.append(f"Inicialização falhou: {e}")
        print(f"   ❌ Erro na inicialização: {e}")
        return bugs_found
    
    print("\n2️⃣ ENVIANDO ANÁLISE")
    print(f"   Roteiro: {len(script_content)} caracteres")
    
    start_time = time.time()
    try:
        # Usar método correto: analyze_with_context
        result = analyzer.analyze_with_context(script_content, save_result=False)
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
        else:
            print("   ✅ Fallback extraiu dados")
    elif result.get('status') == 'empty_fallback':
        print("   ❌ Resposta vazia (empty fallback)")
        bugs_found.append("Resposta completamente vazia do Ollama")
    else:
        print("   ✅ Parse normal bem-sucedido")
    
    # Verificar metadata
    if result.get('metadata'):
        metadata = result['metadata']
        print(f"\n   📊 Metadata:")
        
        if metadata.get('genre'):
            print(f"      ✅ Gênero: {metadata['genre']}")
            # Verificar se gênero faz sentido
            expected_genres = ['sci-fi', 'ficção', 'drama', 'thriller']
            if any(g in metadata['genre'].lower() for g in expected_genres):
                print(f"         ✅ Gênero apropriado")
            else:
                print(f"         ⚠️ Gênero inesperado")
        else:
            print(f"      ❌ Gênero ausente")
            bugs_found.append("Gênero não identificado")
        
        if metadata.get('pages'):
            print(f"      ✅ Páginas: {metadata['pages']}")
        else:
            print(f"      ⚠️ Páginas não identificadas")
            
        if metadata.get('title'):
            print(f"      ✅ Título: {metadata['title']}")
    else:
        print(f"\n   ❌ Metadata completamente ausente")
        bugs_found.append("Metadata não extraída")
    
    # Verificar evidence_log
    if result.get('evidence_log'):
        evidence = result['evidence_log']
        print(f"\n   📝 Evidence Log: {len(evidence)} items")
        
        # Mostrar primeiras evidências
        for i, e in enumerate(evidence[:3], 1):
            if isinstance(e, dict):
                page = e.get('page', '?')
                evid = e.get('evidence', '')[:50]
                print(f"      {i}. Pág {page}: {evid}...")
        
        # Verificar se capturou elementos importantes
        all_evidence = ' '.join(str(e) for e in evidence).lower()
        
        found_lab = 'lab' in all_evidence
        found_aurora = 'aurora' in all_evidence
        found_sarah = 'sarah' in all_evidence or 'chen' in all_evidence
        
        print(f"\n   🔍 Elementos detectados:")
        if found_lab:
            print(f"      ✅ Cenário (Laboratory)")
        else:
            print(f"      ⚠️ Cenário não detectado")
            
        if found_aurora:
            print(f"      ✅ Aurora (IA)")
        else:
            print(f"      ❌ Aurora não detectada")
            bugs_found.append("Personagem Aurora não identificada nas evidências")
            
        if found_sarah:
            print(f"      ✅ Dr. Sarah Chen")
        else:
            print(f"      ❌ Dr. Sarah Chen não detectada")
            bugs_found.append("Personagem Sarah não identificada nas evidências")
    else:
        print(f"\n   ❌ Evidence Log vazio")
        bugs_found.append("Nenhuma evidência extraída")
    
    # Verificar personagens
    if result.get('analise_personagem'):
        chars = result['analise_personagem']
        print(f"\n   👥 Personagens analisados: {len(chars)}")
        
        for char in chars[:3]:
            if isinstance(char, dict):
                name = char.get('name', 'Unknown')
                arc = char.get('arc', 'No arc')
                motivation = char.get('motivation', '')[:30]
                print(f"      • {name}")
                if arc != "No arc":
                    print(f"        Arc: {arc[:50]}...")
                if motivation:
                    print(f"        Motivation: {motivation}...")
        
        # Verificar se encontrou personagens principais
        char_names = ' '.join(str(c.get('name', '')) for c in chars if isinstance(c, dict)).lower()
        
        if 'sarah' not in char_names and 'chen' not in char_names:
            print(f"\n      ⚠️ Sarah Chen não analisada")
        if 'aurora' not in char_names:
            print(f"      ⚠️ Aurora não analisada")
    else:
        print(f"\n   ⚠️ Nenhum personagem analisado")
    
    # Verificar estrutura narrativa
    if result.get('analise_estrutural'):
        struct = result['analise_estrutural']
        print(f"\n   🎭 Estrutura Narrativa:")
        
        elements = ['inciting_incident', 'climax', 'resolution', 'turning_points']
        found_elements = 0
        
        for element in elements:
            if element in struct:
                val = struct[element]
                if val and (not isinstance(val, dict) or val.get('description') or val.get('page')):
                    print(f"      ✅ {element.replace('_', ' ').title()}")
                    found_elements += 1
                else:
                    print(f"      ⚠️ {element.replace('_', ' ').title()} vazio")
            else:
                print(f"      ⚠️ {element.replace('_', ' ').title()} ausente")
        
        if found_elements == 0:
            bugs_found.append("Nenhum elemento estrutural identificado")
    else:
        print(f"\n   ❌ Análise estrutural ausente")
        bugs_found.append("Análise estrutural não realizada")
    
    # Verificar validation
    if result.get('validation'):
        val = result['validation']
        print(f"\n   ✔️ Validação:")
        
        if 'score' in val:
            score = val['score']
            print(f"      Score: {score}")
            if score > 0:
                print(f"      ✅ Score válido")
            else:
                print(f"      ⚠️ Score zero")
        
        if 'valid' in val:
            print(f"      Valid: {val['valid']}")
        
        if 'method' in val:
            print(f"      Method: {val['method']}")
    
    print("\n5️⃣ VERIFICANDO RAW OUTPUT")
    if result.get('raw_output'):
        raw = result['raw_output']
        print(f"   Raw output: {len(raw)} caracteres")
        
        # Verificar formato
        if raw.strip().startswith('{'):
            print(f"   📋 Formato: JSON-like")
            
            # Tentar ver se é JSON válido
            try:
                json.loads(raw)
                print(f"   ✅ JSON válido no raw output")
            except:
                print(f"   ⚠️ JSON malformado no raw output")
                
                # Verificar tipo de erro
                if "'" in raw and '"' in raw:
                    print(f"      • Problema: Aspas mistas detectadas")
                if raw.count('{') != raw.count('}'):
                    print(f"      • Problema: Brackets desbalanceados")
        else:
            print(f"   📋 Formato: Texto puro")
    
    # Análise de performance
    print("\n6️⃣ ANÁLISE DE PERFORMANCE")
    if '_metadata' in result:
        meta = result['_metadata']
        if 'analysis_time' in meta:
            print(f"   ⏱️ Tempo de análise: {meta['analysis_time']:.1f}s")
            if meta['analysis_time'] > 30:
                print(f"      ⚠️ Análise demorada (> 30s)")
                bugs_found.append(f"Performance lenta: {meta['analysis_time']:.1f}s")
            else:
                print(f"      ✅ Tempo aceitável")
        
        if 'context_used' in meta:
            print(f"   📚 Contexto usado: {meta['context_used']} memórias")
    
    # Resumo final
    print("\n" + "="*60)
    print("📊 RESUMO DO TESTE")
    print("="*60)
    
    if bugs_found:
        print(f"\n🐛 BUGS ENCONTRADOS: {len(bugs_found)}")
        for i, bug in enumerate(bugs_found, 1):
            print(f"   {i}. {bug}")
    else:
        print(f"\n✅ NENHUM BUG CRÍTICO ENCONTRADO")
    
    # Avaliar qualidade geral
    quality_score = 0
    quality_items = []
    
    if result.get('metadata', {}).get('genre'):
        quality_score += 1
        quality_items.append("Gênero identificado")
    
    if result.get('evidence_log'):
        quality_score += 1
        quality_items.append(f"{len(result['evidence_log'])} evidências")
    
    if result.get('analise_personagem'):
        quality_score += 1
        quality_items.append(f"{len(result['analise_personagem'])} personagens")
    
    if result.get('validation', {}).get('score', 0) > 0:
        quality_score += 1
        quality_items.append(f"Score: {result['validation']['score']}")
    
    if result.get('analise_estrutural'):
        # Contar elementos estruturais não vazios
        struct_count = sum(1 for v in result['analise_estrutural'].values() if v)
        if struct_count > 0:
            quality_score += 1
            quality_items.append(f"{struct_count} elementos estruturais")
    
    print(f"\n📈 QUALIDADE DA RESPOSTA: {quality_score}/5")
    for item in quality_items:
        print(f"   ✓ {item}")
    
    if quality_score >= 4:
        print("\n   ✅ RESPOSTA DE ALTA QUALIDADE")
    elif quality_score >= 3:
        print("\n   ✅ RESPOSTA DE BOA QUALIDADE")
    elif quality_score >= 2:
        print("\n   ⚠️ RESPOSTA ACEITÁVEL")
    else:
        print("\n   ❌ RESPOSTA DE BAIXA QUALIDADE")
    
    # Status final
    critical_bugs = [b for b in bugs_found if 'não identificad' in b or 'não extraída' in b or 'vazia' in b]
    
    if not bugs_found:
        print("\n🎉 SISTEMA FUNCIONANDO PERFEITAMENTE!")
    elif not critical_bugs:
        print("\n✅ SISTEMA FUNCIONANDO COM PEQUENOS AVISOS")
    else:
        print("\n⚠️ SISTEMA COM PROBLEMAS QUE PRECISAM ATENÇÃO")
    
    # Salvar resultado para análise
    with open('test_complete_result.json', 'w', encoding='utf-8') as f:
        json.dump({
            'result': result,
            'bugs': bugs_found,
            'quality_score': quality_score,
            'quality_items': quality_items,
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
        }, f, indent=2, ensure_ascii=False, default=str)
    
    print(f"\n💾 Resultado salvo em test_complete_result.json")
    
    return bugs_found

if __name__ == "__main__":
    bugs = test_complete_system()
    print("\n🥷 DIGIMUNDO PRESENTE")
    exit(0 if not bugs else 1)
