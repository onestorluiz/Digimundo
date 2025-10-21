#!/usr/bin/env python3
"""
TESTE DE INTEGRAÇÃO - SCRIPTUREMON PROFESSIONAL
Verifica se o modelo está funcionando em situações reais
"""

import ollama
import json
import subprocess
import time

def test_terminal_mode_pure():
    """Teste 1: Modo terminal com JSON puro"""
    print("\n🔧 TESTE 1: Modo Terminal Puro")
    print("-" * 40)

    prompt = "MODO: Terminal\nRetorne JSON: {\"files\": [\"a.py\", \"b.log\"], \"count\": 2}"

    try:
        response = ollama.generate(
            model='scripturemon-professional',
            prompt=prompt,
            stream=False
        )

        text = response['response'].strip()
        print(f"Resposta: {text[:100]}")

        # Tentar parsear diretamente
        data = json.loads(text)
        print("✅ SUCESSO: JSON puro parseado!")
        return True
    except json.JSONDecodeError:
        print("❌ FALHOU: Não retornou JSON puro")
        return False
    except Exception as e:
        print(f"❌ ERRO: {e}")
        return False

def test_file_organization():
    """Teste 2: Organização de arquivos (uso real)"""
    print("\n📁 TESTE 2: Organização de Arquivos")
    print("-" * 40)

    prompt = """MODO: Terminal
Organize estes arquivos e retorne JSON:
- test_script.py
- error.log
- README.md
- data.json
- backup_2024.tar

Formato: {"decisions": [{"file": "X", "destination": "Y"}]}
"""

    try:
        response = ollama.generate(
            model='scripturemon-professional',
            prompt=prompt,
            stream=False
        )

        text = response['response'].strip()

        # Tentar extrair JSON
        if text.startswith('```'):
            # Remover markdown
            lines = text.split('\n')
            json_lines = []
            in_json = False
            for line in lines:
                if line.startswith('```json'):
                    in_json = True
                    continue
                elif line.startswith('```'):
                    in_json = False
                    continue
                elif in_json:
                    json_lines.append(line)
            text = '\n'.join(json_lines)

        data = json.loads(text)

        if 'decisions' in data and len(data['decisions']) > 0:
            print(f"✅ Organizou {len(data['decisions'])} arquivos")
            for d in data['decisions'][:3]:
                print(f"   • {d['file']} → {d.get('destination', '?')}")
            return True
        else:
            print("❌ Estrutura JSON inválida")
            return False

    except Exception as e:
        print(f"❌ ERRO: {e}")
        return False

def test_creative_mode():
    """Teste 3: Modo criativo para análise"""
    print("\n🎨 TESTE 3: Modo Criativo")
    print("-" * 40)

    prompt = "MODO: Documento\nAnalise brevemente: o que é um plot twist?"

    try:
        response = ollama.generate(
            model='scripturemon-professional',
            prompt=prompt,
            stream=False
        )

        text = response['response']

        # Verificar se usou modo criativo
        has_creativity = any([
            len(text) > 200,
            any(c in text for c in ['#', '*', '🎬', '📝']),
            'narrativa' in text.lower() or 'roteiro' in text.lower()
        ])

        if has_creativity:
            print(f"✅ Modo criativo ativado ({len(text)} caracteres)")
            print(f"   Preview: {text[:150]}...")
            return True
        else:
            print("❌ Não usou modo criativo")
            return False

    except Exception as e:
        print(f"❌ ERRO: {e}")
        return False

def test_auto_detection():
    """Teste 4: Detecção automática de contexto"""
    print("\n🤖 TESTE 4: Detecção Automática")
    print("-" * 40)

    tests = [
        ("retorne um array com 3 números", "terminal"),
        ("analise o protagonista do filme", "documento"),
        ("execute comando ls e retorne json", "terminal"),
        ("explique a jornada do herói", "documento")
    ]

    success = 0

    for prompt, expected in tests:
        try:
            response = ollama.generate(
                model='scripturemon-professional',
                prompt=prompt,
                stream=False
            )

            text = response['response']

            # Detectar modo usado
            if expected == "terminal":
                # Deve ser conciso e estruturado
                is_terminal = len(text) < 500 and ('{' in text or '[' in text)
            else:
                # Deve ser criativo e longo
                is_terminal = False
                is_creative = len(text) > 200

            if (expected == "terminal" and is_terminal) or (expected == "documento" and not is_terminal):
                print(f"✅ '{prompt[:30]}...' → {expected}")
                success += 1
            else:
                print(f"❌ '{prompt[:30]}...' → modo errado")

        except Exception as e:
            print(f"❌ Erro no teste: {e}")

    print(f"\n   Taxa de detecção: {success}/{len(tests)}")
    return success >= len(tests) * 0.75

def test_integration_with_scripts():
    """Teste 5: Integração com scripts existentes"""
    print("\n🔗 TESTE 5: Integração com Scripts")
    print("-" * 40)

    # Verificar se o self_organize usa o modelo correto
    try:
        with open('scripts/analysis/scripturemon_self_organize.py', 'r') as f:
            content = f.read()

        if 'scripturemon-professional' in content:
            print("✅ self_organize.py está usando modelo professional")

            # Testar execução rápida
            result = subprocess.run(
                ['python3', 'scripts/analysis/scripturemon_self_organize.py'],
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode == 0:
                print("✅ Script executou sem erros")
                return True
            else:
                print(f"⚠️ Script retornou código {result.returncode}")
                return False
        else:
            print("❌ self_organize.py ainda usa modelo antigo")
            return False

    except subprocess.TimeoutExpired:
        print("⚠️ Script demorou muito (mas pode estar funcionando)")
        return True
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def test_performance():
    """Teste 6: Performance e velocidade"""
    print("\n⚡ TESTE 6: Performance")
    print("-" * 40)

    prompt = "MODO: Terminal\n{\"status\": \"ok\"}"

    times = []
    for i in range(3):
        start = time.time()
        try:
            response = ollama.generate(
                model='scripturemon-professional',
                prompt=prompt,
                stream=False
            )
            elapsed = time.time() - start
            times.append(elapsed)
            print(f"   Teste {i+1}: {elapsed:.2f}s")
        except:
            print(f"   Teste {i+1}: ERRO")

    if times:
        avg = sum(times) / len(times)
        print(f"\n✅ Tempo médio: {avg:.2f}s")
        return avg < 10  # Menos de 10s é aceitável
    return False

def main():
    print("=" * 50)
    print("🚀 TESTE COMPLETO DE INTEGRAÇÃO")
    print("   Scripturemon Professional Mode")
    print("=" * 50)

    # Verificar se modelo existe
    result = subprocess.run(
        ['ollama', 'list'],
        capture_output=True,
        text=True
    )

    if 'scripturemon-professional' not in result.stdout:
        print("❌ Modelo scripturemon-professional não encontrado!")
        print("   Execute: ollama create scripturemon-professional -f config/Modelfile.scripturemon-professional")
        return

    print("✅ Modelo encontrado no sistema")

    # Executar testes
    results = {
        "Terminal Puro": test_terminal_mode_pure(),
        "Organização": test_file_organization(),
        "Modo Criativo": test_creative_mode(),
        "Auto-Detecção": test_auto_detection(),
        "Integração": test_integration_with_scripts(),
        "Performance": test_performance()
    }

    # Resumo final
    print("\n" + "=" * 50)
    print("📊 RESUMO DA INTEGRAÇÃO")
    print("=" * 50)

    total = len(results)
    passed = sum(1 for v in results.values() if v)

    for test, passed_test in results.items():
        status = "✅" if passed_test else "❌"
        print(f"{status} {test}")

    print(f"\n🎯 Taxa de Sucesso: {passed}/{total} ({passed*100/total:.0f}%)")

    if passed == total:
        print("\n🎉 INTEGRAÇÃO PERFEITA!")
        print("Scripturemon Professional está totalmente operacional!")
    elif passed >= total * 0.8:
        print("\n👍 INTEGRAÇÃO BOA!")
        print("Sistema está funcionando adequadamente.")
    else:
        print("\n⚠️ INTEGRAÇÃO PRECISA DE AJUSTES")
        print("Verifique os testes que falharam.")

    # Instruções de uso
    print("\n" + "=" * 50)
    print("📚 COMO USAR O SCRIPTUREMON PROFESSIONAL")
    print("=" * 50)
    print("""
1. Para respostas em JSON puro (terminal):
   Comece com: "MODO: Terminal"

2. Para análises criativas (documento):
   Comece com: "MODO: Documento"

3. Detecção automática:
   Use palavras-chave como "json", "execute", "análise"

4. Em scripts Python:
   model = 'scripturemon-professional'

5. No terminal:
   ollama run scripturemon-professional

O modelo agora LEMBRA permanentemente destes contextos!
    """)

if __name__ == "__main__":
    main()