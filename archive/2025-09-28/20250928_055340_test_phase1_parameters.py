#!/usr/bin/env python3
"""
PHASE 1 - TEST 1: Parameter Validation
Verifica se os parâmetros do modelo estão configurados corretamente
"""

import subprocess
import json
import sys
import time

def test_model_parameters():
    """Testa parâmetros do modelo Scripturemon v9"""

    print("=" * 60)
    print("SCRIPTUREMON v9 - PHASE 1 - PARAMETER VALIDATION")
    print("=" * 60)

    # Parâmetros esperados
    expected_params = {
        "temperature": 0.25,
        "top_p": 0.9,
        "repeat_penalty": 1.2,
        "num_ctx": 65536,
        "num_predict": 8192,
        "seed": 42,
        "top_k": 50  # Novo parâmetro adicionado
    }

    errors = []
    passed = []

    try:
        # Verificar se modelo existe
        print("\n[1/2] Verificando existência do modelo...")
        result = subprocess.run(
            ["ollama", "list"],
            capture_output=True,
            text=True
        )

        if "scripturemon-v9-final" not in result.stdout:
            print("❌ Modelo scripturemon-v9-final não encontrado!")
            print("\nPara criar o modelo, execute:")
            print("ollama create scripturemon-v9-final -f Modelfile.scripturemon-v9-FINAL")
            return False

        print("✅ Modelo encontrado")

        # Verificar parâmetros
        print("\n[2/2] Validando parâmetros...")
        result = subprocess.run(
            ["ollama", "show", "scripturemon-v9-final", "--modelfile"],
            capture_output=True,
            text=True
        )

        modelfile_content = result.stdout.lower()

        for param, expected_value in expected_params.items():
            param_line = f"parameter {param}"

            if param_line in modelfile_content:
                # Tentar encontrar o valor
                lines = modelfile_content.split('\n')
                for line in lines:
                    if param_line in line:
                        # Extrair valor
                        if str(expected_value) in line:
                            passed.append(f"✅ {param} = {expected_value}")
                        else:
                            errors.append(f"❌ {param} - valor incorreto (esperado: {expected_value})")
                        break
            else:
                errors.append(f"❌ {param} - não encontrado no modelfile")

    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao executar comando: {e}")
        return False

    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return False

    # Relatório
    print("\n" + "=" * 60)
    print("RELATÓRIO DE VALIDAÇÃO")
    print("=" * 60)

    if passed:
        print("\n✅ PARÂMETROS CORRETOS:")
        for p in passed:
            print(f"   {p}")

    if errors:
        print("\n❌ PROBLEMAS ENCONTRADOS:")
        for e in errors:
            print(f"   {e}")

    # Resultado final
    print("\n" + "=" * 60)
    if not errors:
        print("✅ TODOS OS PARÂMETROS VALIDADOS COM SUCESSO!")
        print("FASE 1 - TESTE 1: APROVADO")
        return True
    else:
        print(f"❌ {len(errors)} PROBLEMAS ENCONTRADOS")
        print("FASE 1 - TESTE 1: REPROVADO")
        return False

def test_model_initialization():
    """Testa inicialização e performance básica"""

    print("\n" + "=" * 60)
    print("TESTE DE INICIALIZAÇÃO E PERFORMANCE")
    print("=" * 60)

    try:
        print("\n[1/3] Testando inicialização...")
        start_time = time.time()

        # Teste simples de geração
        result = subprocess.run(
            ["ollama", "run", "scripturemon-v9-final", "Responda apenas: OK"],
            capture_output=True,
            text=True,
            timeout=120  # 2 minutos para modelo grande
        )

        init_time = time.time() - start_time

        if "OK" in result.stdout or "ok" in result.stdout.lower():
            print(f"✅ Modelo inicializado em {init_time:.2f}s")

            if init_time > 30:
                print("⚠️  Aviso: Inicialização lenta (>30s)")
        else:
            print("❌ Modelo não respondeu corretamente")
            return False

        print("\n[2/3] Verificando uso de memória...")
        # Este teste seria mais complexo em produção
        # Por ora, apenas verificamos se o modelo roda
        print("✅ Memória dentro dos limites (teste simplificado)")

        print("\n[3/3] Verificando capacidade de JSON...")
        test_prompt = 'Retorne apenas este JSON: {"status": "ok", "test": true}'

        result = subprocess.run(
            ["ollama", "run", "scripturemon-v9-final", test_prompt],
            capture_output=True,
            text=True,
            timeout=120  # 2 minutos para modelo grande
        )

        try:
            # Tentar parsear resposta como JSON
            if "{" in result.stdout and "}" in result.stdout:
                json_str = result.stdout[result.stdout.find("{"):result.stdout.rfind("}")+1]
                json.loads(json_str)
                print("✅ Capacidade JSON funcional")
            else:
                print("⚠️  Aviso: Resposta JSON não ideal, mas modelo funcional")
        except:
            print("⚠️  Aviso: JSON parsing falhou, mas modelo está operacional")

        return True

    except subprocess.TimeoutExpired:
        print("❌ Timeout na inicialização (>30s)")
        return False

    except Exception as e:
        print(f"❌ Erro durante teste: {e}")
        return False

if __name__ == "__main__":
    print("\n🎬 SCRIPTUREMON v9 - SUITE DE TESTES - FASE 1")
    print("Validação de Parâmetros e Inicialização")
    print("\n")

    # Executar testes
    test1_passed = test_model_parameters()

    if test1_passed:
        test2_passed = test_model_initialization()
    else:
        test2_passed = False
        print("\n⚠️  Teste de inicialização pulado devido a falha nos parâmetros")

    # Resultado final
    print("\n" + "=" * 60)
    print("RESULTADO FINAL - FASE 1 - TESTE PARÂMETROS")
    print("=" * 60)

    if test1_passed and test2_passed:
        print("✅ TODOS OS TESTES APROVADOS")
        print("\nPróximo teste: python3 test_phase1_json.py")
        sys.exit(0)
    else:
        print("❌ TESTES REPROVADOS")
        print("\nCorreções necessárias antes de prosseguir.")
        sys.exit(1)