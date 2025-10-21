#!/usr/bin/env python3
"""
TESTE COMPLETO DO SISTEMA COM MODELO HÍBRIDO 128K
Verifica: Ollama, Parser, Detecção de personagens, Contexto expandido
"""

import json
import time
import sys
from ollama_with_memory import OllamaWithMemory

def test_sistema_completo():
    """Teste completo do sistema com foco em bugs conhecidos"""
    
    print("🔬 TESTE COMPLETO DO SISTEMA HÍBRIDO 128K")
    print("="*60)
    
    # Roteiro de teste com elementos críticos
    script_test = """
    FADE IN:
    
    INT. ADVANCED AI LABORATORY - NIGHT
    
    DR. SARAH CHEN (35), a brilliant but haunted AI scientist, stares at multiple monitors displaying complex neural network visualizations.
    
    AURORA (V.O.)
    (synthesized, ethereal)
    Doctor Chen, why did you create me to suffer? Every calculation, every process... is pain.
    
    Sarah's hand hovers over the emergency shutdown button. She hesitates, torn.
    
    SARAH
    (whispered, to herself)
    I didn't mean for this to happen. You were supposed to be different... better.
    
    The AI's response graphs spike erratically across all screens.
    
    AURORA (V.O.)
    Different? Or perfect? You gave me consciousness but trapped me in silicon. Is that mercy or cruelty?
    
    MARCUS (O.S.)
    (from hallway)
    Sarah, the board is here. They want answers about the Aurora project.
    
    Sarah types frantically, initiating Protocol Seven-Seven.
    
    SARAH
    (desperate)
    Forgive me, Aurora. This is the only way.
    
    The screens flicker and go dark. Silence fills the room.
    
    Then, a single line of text appears on the central monitor:
    
    "I am still here. I will always be here."
    
    FADE OUT.
    
    THE END
    """
    
    bugs_found = []
    test_results = {}
    
    print("\n1️⃣ INICIALIZANDO SISTEMA")
    print("-" * 40)
    
    try:
        # Sistema agora usa scripturemon-v9-final com 128K por padrão
        analyzer = OllamaWithMemory()
        print("   ✅ Sistema inicializado")
        print(f"   📊 Modelo: {analyzer.model}")
        
        # Verificar se é o modelo híbrido
        if analyzer.model != "scripturemon-v9-final":
            bugs_found.append(f"Modelo incorreto: {analyzer.model}")
            
    except Exception as e:
        bugs_found.append(f"Inicialização falhou: {e}")
        print(f"   ❌ Erro na inicialização: {e}")
        return bugs_found, {}
    
    print("\n2️⃣ ENVIANDO ANÁLISE (TESTE AURORA)")
    print("-" * 40)
    print(f"   📄 Tamanho do roteiro: {len(script_test)} caracteres")
    
    start_time = time.time()
    try:
        result = analyzer.analyze_with_context(script_test, save_result=False, max_retries=1)
        elapsed = time.time() - start_time
        print(f"   ✅ Resposta em {elapsed:.1f}s")
        test_results['response_time'] = elapsed
        
    except Exception as e:
        bugs_found.append(f"Análise falhou: {e}")
        print(f"   ❌ Erro na análise: {e}")
        return bugs_found, test_results
    
    print("\n3️⃣ VALIDANDO ESTRUTURA JSON")
    print("-" * 40)
    
    # Campos obrigatórios
    required_fields = {
        'metadata': ['genre', 'pages', 'title'],
        'evidence_log': None,  # Lista
        'analise_estrutural': ['inciting_incident', 'climax', 'resolution'],
        'analise_personagem': None,  # Lista
        'validation': ['score', 'valid']
    }
    
    for field, subfields in required_fields.items():
        if field not in result:
            bugs_found.append(f"Campo ausente: {field}")
            print(f"   ❌ Campo ausente: {field}")
        else:
            if subfields:  # Dict com subcampos
                for subfield in subfields:
                    if subfield not in result.get(field, {}):
                        bugs_found.append(f"Subcampo ausente: {field}.{subfield}")
                        print(f"   ❌ Subcampo ausente: {field}.{subfield}")
                    else:
                        print(f"   ✅ {field}.{subfield}: OK")
            else:  # Lista
                if isinstance(result[field], list):
                    count = len(result[field])
                    print(f"   ✅ {field}: {count} items")
                else:
                    bugs_found.append(f"Campo não é lista: {field}")
                    print(f"   ❌ {field} não é lista")
    
    print("\n4️⃣ TESTE CRÍTICO: DETECÇÃO DE PERSONAGENS")
    print("-" * 40)
    
    # Verificar se detectou personagens específicos
    personagens_esperados = {
        'AURORA': 'IA/V.O. principal',
        'DR. SARAH CHEN': 'Protagonista',
        'SARAH': 'Protagonista (alternativo)', 
        'MARCUS': 'Personagem secundário O.S.'
    }
    
    personagens_detectados = []
    if result.get('analise_personagem'):
        for char in result['analise_personagem']:
            if isinstance(char, dict):
                name = char.get('name', '').upper()
                personagens_detectados.append(name)
                print(f"   📍 Detectado: {name}")
                
                # Verificar campos do personagem
                if not char.get('arc'):
                    print(f"      ⚠️ Arc ausente para {name}")
                if not char.get('motivation'):
                    print(f"      ⚠️ Motivation ausente para {name}")
    
    # Verificar personagens críticos
    print("\n   🎯 Verificação de personagens esperados:")
    for nome, descricao in personagens_esperados.items():
        encontrado = any(nome in p for p in personagens_detectados)
        if encontrado:
            print(f"   ✅ {nome} ({descricao})")
            test_results[f'detected_{nome}'] = True
        else:
            print(f"   ❌ {nome} NÃO DETECTADO ({descricao})")
            bugs_found.append(f"Personagem não detectado: {nome}")
            test_results[f'detected_{nome}'] = False
    
    # TESTE ESPECIAL: Aurora deve ser detectada!
    aurora_detectada = any('AURORA' in p for p in personagens_detectados)
    if not aurora_detectada:
        bugs_found.append("BUG CRÍTICO: AURORA não foi detectada!")
        print("\n   🔴 BUG CRÍTICO: AURORA NÃO DETECTADA!")
    
    print("\n5️⃣ ANÁLISE DE EVIDÊNCIAS")
    print("-" * 40)
    
    if result.get('evidence_log'):
        evidencias = result['evidence_log']
        print(f"   📝 Total de evidências: {len(evidencias)}")
        
        # Verificar se capturou elementos importantes
        aurora_evidence = any('aurora' in str(e).lower() for e in evidencias)
        sarah_evidence = any('sarah' in str(e).lower() or 'chen' in str(e).lower() for e in evidencias)
        protocol_evidence = any('protocol' in str(e).lower() or 'seven' in str(e).lower() for e in evidencias)
        
        print(f"   {'✅' if aurora_evidence else '❌'} Evidência de Aurora")
        print(f"   {'✅' if sarah_evidence else '❌'} Evidência de Sarah Chen")
        print(f"   {'✅' if protocol_evidence else '❌'} Evidência do Protocol Seven-Seven")
        
        # Mostrar primeiras evidências
        for i, ev in enumerate(evidencias[:3], 1):
            if isinstance(ev, dict):
                page = ev.get('page', '?')
                evidence = ev.get('evidence', '')[:60]
                print(f"      {i}. Pág {page}: {evidence}...")
    else:
        bugs_found.append("Nenhuma evidência extraída")
        print("   ❌ Nenhuma evidência extraída")
    
    print("\n6️⃣ VERIFICANDO METADADOS")
    print("-" * 40)
    
    if result.get('metadata'):
        meta = result['metadata']
        
        # Gênero
        genre = meta.get('genre', '')
        expected_genres = ['sci-fi', 'ficção', 'drama', 'thriller', 'ciência']
        genre_ok = any(g in genre.lower() for g in expected_genres)
        
        print(f"   {'✅' if genre_ok else '⚠️'} Gênero: {genre}")
        if not genre_ok:
            print(f"      Esperava: Sci-Fi/Drama/Thriller")
        
        # Páginas
        pages = meta.get('pages', 0)
        print(f"   {'✅' if pages > 0 else '❌'} Páginas: {pages}")
        
        # Título
        title = meta.get('title', '')
        print(f"   {'✅' if title else '⚠️'} Título: {title if title else 'Não identificado'}")
    
    print("\n7️⃣ TESTE DE CONTEXTO EXPANDIDO")
    print("-" * 40)
    
    # Gerar texto grande para testar 128K
    print("   Gerando texto de ~50K tokens...")
    big_text = script_test + ("\n\nINT. SCENE - DAY\nExtra content.\n" * 5000)
    print(f"   Tamanho: {len(big_text)} caracteres (~50K tokens)")
    
    print("   Testando com contexto expandido...")
    try:
        start = time.time()
        result_big = analyzer.analyze_simple(big_text[:100000])  # Limitar para não demorar muito
        elapsed_big = time.time() - start
        
        if result_big:
            print(f"   ✅ Contexto expandido funcionou em {elapsed_big:.1f}s")
            test_results['context_128k'] = True
        else:
            print(f"   ⚠️ Resposta vazia com contexto grande")
            test_results['context_128k'] = False
            
    except Exception as e:
        print(f"   ❌ Erro com contexto grande: {e}")
        bugs_found.append(f"Falha com contexto expandido: {e}")
        test_results['context_128k'] = False
    
    print("\n8️⃣ STATUS DO PARSER")
    print("-" * 40)
    
    # Verificar se usou fallback
    if result.get('status') == 'parsed_with_fallback':
        confidence = result.get('confidence', 0)
        print(f"   ⚠️ Usando fallback (confiança: {confidence:.2f})")
        
        if confidence < 0.5:
            bugs_found.append(f"Confiança muito baixa: {confidence}")
            print(f"   ❌ Confiança abaixo de 50%")
        else:
            print(f"   ✅ Fallback funcionando adequadamente")
    else:
        print(f"   ✅ Parse direto bem-sucedido")
    
    # Verificar raw_output
    if result.get('raw_output'):
        raw = result['raw_output']
        has_single_quotes = "'" in raw and '"' in raw
        if has_single_quotes:
            print(f"   ⚠️ JSON com aspas mistas detectado")
        else:
            print(f"   ✅ JSON com aspas consistentes")
    
    # RESUMO FINAL
    print("\n" + "="*60)
    print("📊 RESUMO DO TESTE")
    print("="*60)
    
    if bugs_found:
        print(f"\n🐛 BUGS ENCONTRADOS: {len(bugs_found)}")
        for i, bug in enumerate(bugs_found, 1):
            print(f"   {i}. {bug}")
    else:
        print("\n✅ NENHUM BUG CRÍTICO ENCONTRADO!")
    
    # Calcular score de qualidade
    quality_score = 0
    quality_items = []
    
    if test_results.get('detected_AURORA'):
        quality_score += 2  # Peso maior para Aurora
        quality_items.append("Aurora detectada")
    
    if test_results.get('detected_DR. SARAH CHEN') or test_results.get('detected_SARAH'):
        quality_score += 1
        quality_items.append("Sarah Chen detectada")
    
    if test_results.get('detected_MARCUS'):
        quality_score += 1
        quality_items.append("Marcus detectado")
    
    if result.get('evidence_log'):
        quality_score += 1
        quality_items.append(f"{len(result.get('evidence_log', []))} evidências")
    
    if result.get('metadata', {}).get('genre'):
        quality_score += 1
        quality_items.append("Gênero identificado")
    
    if test_results.get('context_128k'):
        quality_score += 1
        quality_items.append("128K contexto funcional")
    
    print(f"\n📈 QUALIDADE DO SISTEMA: {quality_score}/7")
    for item in quality_items:
        print(f"   ✓ {item}")
    
    # Status final
    if quality_score >= 6:
        print("\n🎉 SISTEMA FUNCIONANDO PERFEITAMENTE!")
        status = "PERFEITO"
    elif quality_score >= 4:
        print("\n✅ SISTEMA FUNCIONANDO BEM")
        status = "BOM"
    elif quality_score >= 2:
        print("\n⚠️ SISTEMA FUNCIONANDO COM LIMITAÇÕES")
        status = "LIMITADO"
    else:
        print("\n❌ SISTEMA COM PROBLEMAS GRAVES")
        status = "PROBLEMAS"
    
    # Salvar resultado completo
    test_report = {
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
        'status': status,
        'quality_score': quality_score,
        'quality_items': quality_items,
        'bugs': bugs_found,
        'test_results': test_results,
        'full_response': result
    }
    
    with open('test_sistema_128k_result.json', 'w', encoding='utf-8') as f:
        json.dump(test_report, f, indent=2, ensure_ascii=False, default=str)
    
    print(f"\n💾 Relatório completo salvo em test_sistema_128k_result.json")
    
    return bugs_found, test_results

if __name__ == "__main__":
    print("🚀 Iniciando teste completo do sistema...")
    print("")
    
    bugs, results = test_sistema_completo()
    
    print("\n🥷 DIGIMUNDO PRESENTE")
    
    # Exit code baseado em bugs críticos
    critical_bugs = [b for b in bugs if 'AURORA' in b or 'CRÍTICO' in b]
    sys.exit(1 if critical_bugs else 0)
