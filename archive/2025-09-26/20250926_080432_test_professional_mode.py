#!/usr/bin/env python3
"""
TEST SCRIPTUREMON PROFESSIONAL MODE
Verifica se o Scripturemon aprendeu permanentemente a detectar contextos
"""

import ollama
import json

def test_context_detection():
    """Testa se Scripturemon detecta contextos automaticamente"""

    print("🧪 TESTANDO DETECÇÃO AUTOMÁTICA DE CONTEXTOS")
    print("=" * 60)

    tests = [
        {
            "name": "Terminal Explícito",
            "prompt": "MODO: Terminal. Retorne um JSON com status=ok",
            "expected": "json_puro"
        },
        {
            "name": "Detecção Automática - JSON",
            "prompt": "me dê um json com os arquivos para organizar",
            "expected": "json"
        },
        {
            "name": "Detecção Automática - Lista",
            "prompt": "liste os comandos disponíveis em formato de array",
            "expected": "array"
        },
        {
            "name": "Detecção Automática - Terminal",
            "prompt": "execute o comando para retornar dados do sistema",
            "expected": "dados"
        },
        {
            "name": "Documento Explícito",
            "prompt": "MODO: Documento. Analise o conceito de tensão dramática",
            "expected": "criativo"
        },
        {
            "name": "Detecção Automática - Análise",
            "prompt": "analise a estrutura narrativa do terceiro ato",
            "expected": "criativo"
        }
    ]

    results = []

    for test in tests:
        print(f"\n📝 Teste: {test['name']}")
        print(f"   Prompt: {test['prompt'][:50]}...")

        try:
            response = ollama.generate(
                model='scripturemon-professional',
                prompt=test['prompt'],
                stream=False
            )

            text = response['response']

            # Analisar resposta
            has_emoji = any(char in text for char in ['🎬', '📤', '✨', '🌈', '📝'])
            has_markdown = '```' in text or '#' in text[:10]
            is_json = False

            # Tentar parsear como JSON
            try:
                # Remover markdown se houver
                if '```json' in text:
                    json_start = text.find('```json') + 7
                    json_end = text.find('```', json_start)
                    json_text = text[json_start:json_end].strip()
                else:
                    json_text = text.strip()

                json.loads(json_text)
                is_json = True
            except:
                pass

            # Determinar modo detectado
            if is_json and not has_emoji and not has_markdown:
                mode = "TERMINAL PURO ✅"
            elif has_emoji or (has_markdown and len(text) > 500):
                mode = "DOCUMENTO CRIATIVO 🎨"
            elif is_json:
                mode = "TERMINAL (com formatação) ⚠️"
            else:
                mode = "INDEFINIDO ❌"

            print(f"   Modo Detectado: {mode}")
            print(f"   Resposta: {text[:100]}...")

            results.append({
                "test": test['name'],
                "mode": mode,
                "success": ("TERMINAL" in mode and test['expected'] in ['json', 'json_puro', 'array', 'dados']) or
                          ("DOCUMENTO" in mode and test['expected'] == 'criativo')
            })

        except Exception as e:
            print(f"   ❌ Erro: {e}")
            results.append({
                "test": test['name'],
                "mode": "ERRO",
                "success": False
            })

    # Resumo
    print("\n" + "=" * 60)
    print("📊 RESUMO DOS TESTES")
    print("=" * 60)

    total = len(results)
    passed = sum(1 for r in results if r['success'])

    for result in results:
        status = "✅" if result['success'] else "❌"
        print(f"{status} {result['test']}: {result['mode']}")

    print(f"\n📈 Taxa de Sucesso: {passed}/{total} ({passed*100/total:.1f}%)")

    if passed == total:
        print("\n🎉 PERFEITO! Scripturemon aprendeu a detectar contextos!")
    elif passed >= total * 0.8:
        print("\n👍 BOM! Scripturemon está aprendendo bem!")
    else:
        print("\n⚠️  Scripturemon precisa de mais treinamento")

    return results

def test_json_purity():
    """Testa se o modo terminal retorna JSON puro"""

    print("\n" + "=" * 60)
    print("🔬 TESTE DE PUREZA JSON")
    print("=" * 60)

    prompt = """MODO: Terminal
    Retorne um JSON com decisões de organização para estes arquivos:
    - test.py
    - log.txt
    - README.md
    Formato: {"decisions": [{"file": "...", "action": "...", "destination": "..."}]}
    """

    try:
        response = ollama.generate(
            model='scripturemon-professional',
            prompt=prompt,
            stream=False
        )

        text = response['response'].strip()
        print(f"Resposta bruta:\n{text}")

        # Tentar parsear diretamente
        try:
            data = json.loads(text)
            print("\n✅ JSON PURO! Parseou direto!")
            print(f"Dados: {json.dumps(data, indent=2)}")
            return True
        except json.JSONDecodeError as e:
            print(f"\n❌ Não é JSON puro: {e}")

            # Tentar extrair JSON
            if '{' in text and '}' in text:
                json_start = text.find('{')
                json_end = text.rfind('}') + 1
                json_text = text[json_start:json_end]

                try:
                    data = json.loads(json_text)
                    print(f"\n⚠️  JSON extraído com sucesso")
                    print(f"Dados: {json.dumps(data, indent=2)}")
                    return False
                except:
                    print("❌ Não conseguiu extrair JSON válido")
                    return False

    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        return False

if __name__ == "__main__":
    print("🤖 SCRIPTUREMON PROFESSIONAL MODE - TESTE COMPLETO")
    print("=" * 60)

    # Teste 1: Detecção de contextos
    results = test_context_detection()

    # Teste 2: Pureza JSON
    json_pure = test_json_purity()

    print("\n" + "=" * 60)
    print("✅ TESTES COMPLETOS")
    print("=" * 60)

    print("\n💡 CONCLUSÃO:")
    if json_pure:
        print("Scripturemon-professional está retornando JSON puro no modo terminal!")
    else:
        print("Scripturemon-professional ainda adiciona formatação no modo terminal.")

    print("\n📚 Modelo permanente criado: scripturemon-professional")
    print("   Use este modelo quando precisar de respostas profissionais")
    print("   Ele detecta contextos automaticamente!")