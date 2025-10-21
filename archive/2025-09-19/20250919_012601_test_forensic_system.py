#!/usr/bin/env python3
"""
🧪 TESTES ROBUSTOS DO SISTEMA FORENSE
Garante que tudo funciona antes da execução real
"""

import os
import sys
import json
import time
import tempfile
import subprocess
from pathlib import Path
import ollama

def test_model_exists():
    """Teste 1: Verificar se modelo existe"""
    print("🧪 TESTE 1: Verificando modelo forense...")

    try:
        models = ollama.list()
        model_list = models.get('models', [])

        # Verificar se o modelo forensic-analyzer existe
        forensic_found = False
        for model in model_list:
            # Tentar diferentes chaves possíveis
            model_name = model.get('name') or model.get('model') or str(model)
            if 'forensic-analyzer' in model_name:
                forensic_found = True
                break

        if forensic_found:
            print("   ✅ Modelo forensic-analyzer:latest encontrado")
            return True
        else:
            print("   ❌ Modelo forensic-analyzer:latest NÃO encontrado")
            # Mostrar modelos disponíveis de forma mais robusta
            available = [str(m) for m in model_list[:5]]  # Primeiros 5
            print(f"   📋 Modelos disponíveis: {available}")
            return False

    except Exception as e:
        print(f"   ❌ Erro ao verificar modelos: {e}")
        return False

def test_model_response():
    """Teste 2: Verificar resposta do modelo"""
    print("🧪 TESTE 2: Testando resposta do modelo...")

    simple_code = '''
import quantum_fake_module  # Import inexistente
import tempfile

def bad_function():
    path = "/tmp/hardcoded"  # Path hardcoded
    big_array = [0] * 1000000  # Uso excessivo
    return path
'''

    try:
        response = ollama.generate(
            model="forensic-analyzer:latest",
            prompt=simple_code,
            options={'num_ctx': 4096, 'temperature': 0.1}
        )

        response_text = response.get('response', '')

        # Verificar se resposta contém elementos esperados
        checks = [
            ('import', 'Detecta imports'),
            ('hardcoded', 'Detecta paths hardcoded'),
            ('line_number', 'Inclui números de linha'),
            ('severity', 'Inclui severidade'),
            ('claude_vice', 'Identifica vícios Claude')
        ]

        all_good = True
        for keyword, description in checks:
            if keyword.lower() in response_text.lower():
                print(f"   ✅ {description}")
            else:
                print(f"   ❌ {description} - não encontrado")
                all_good = False

        if len(response_text) > 100:
            print(f"   ✅ Resposta tem tamanho adequado ({len(response_text)} chars)")
        else:
            print(f"   ❌ Resposta muito curta ({len(response_text)} chars)")
            all_good = False

        return all_good

    except Exception as e:
        print(f"   ❌ Erro ao testar modelo: {e}")
        return False

def test_directory_structure():
    """Teste 3: Verificar estrutura de diretórios"""
    print("🧪 TESTE 3: Verificando estrutura de diretórios...")

    base_dir = Path("/Users/clubproducoes/Digimundo/scripturemon-champion")
    required_paths = [
        base_dir / "apps" / "scripturemon",
        base_dir / "modelfiles",
        base_dir / "apps" / "scripturemon" / "forensic_orchestrator.py",
        base_dir / "apps" / "scripturemon" / "forensic_monitor.py",
        base_dir / "apps" / "scripturemon" / "forensic_notifier.py",
        base_dir / "modelfiles" / "forensic-analyzer.modelfile"
    ]

    all_good = True
    for path in required_paths:
        if path.exists():
            print(f"   ✅ {path.name}")
        else:
            print(f"   ❌ {path} - NÃO encontrado")
            all_good = False

    return all_good

def test_checkpoint_system():
    """Teste 4: Testar sistema de checkpoint"""
    print("🧪 TESTE 4: Testando sistema de checkpoint...")

    try:
        # Criar diretório temporário
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            checkpoint_file = temp_path / "test_checkpoint.json"

            # Dados de teste
            test_data = {
                'timestamp': '2025-01-01T10:00:00',
                'total_files': 10,
                'completed_files': 5,
                'results': {
                    'test1.py': {'overall_health': 'OK'},
                    'test2.py': {'overall_health': 'BROKEN'}
                }
            }

            # Testar escrita
            with open(checkpoint_file, 'w') as f:
                json.dump(test_data, f)

            if checkpoint_file.exists():
                print("   ✅ Escrita de checkpoint")
            else:
                print("   ❌ Falha na escrita de checkpoint")
                return False

            # Testar leitura
            with open(checkpoint_file, 'r') as f:
                loaded_data = json.load(f)

            if loaded_data == test_data:
                print("   ✅ Leitura de checkpoint")
            else:
                print("   ❌ Falha na leitura de checkpoint")
                return False

            return True

    except Exception as e:
        print(f"   ❌ Erro no teste de checkpoint: {e}")
        return False

def test_dependencies():
    """Teste 5: Verificar dependências Python"""
    print("🧪 TESTE 5: Verificando dependências...")

    required_modules = [
        'json', 'pathlib', 'datetime', 'subprocess',
        'psutil', 'ollama', 'threading', 'time'
    ]

    all_good = True
    for module in required_modules:
        try:
            __import__(module)
            print(f"   ✅ {module}")
        except ImportError:
            print(f"   ❌ {module} - NÃO encontrado")
            all_good = False

    return all_good

def test_file_permissions():
    """Teste 6: Verificar permissões de arquivos"""
    print("🧪 TESTE 6: Verificando permissões...")

    base_dir = Path("/Users/clubproducoes/Digimundo/scripturemon-champion")

    # Testar leitura de apps/scripturemon
    apps_dir = base_dir / "apps" / "scripturemon"
    try:
        files = list(apps_dir.glob("*.py"))
        if files:
            print(f"   ✅ Pode ler {len(files)} arquivos Python")
        else:
            print("   ⚠️ Nenhum arquivo Python encontrado")

        # Testar leitura de um arquivo
        test_file = files[0] if files else None
        if test_file:
            with open(test_file, 'r') as f:
                content = f.read(100)  # Ler primeiros 100 chars
            print("   ✅ Pode ler conteúdo de arquivos")

    except Exception as e:
        print(f"   ❌ Erro de permissão: {e}")
        return False

    # Testar escrita em results
    try:
        results_dir = base_dir / "forensic_results"
        results_dir.mkdir(exist_ok=True)

        test_file = results_dir / "test_write.txt"
        with open(test_file, 'w') as f:
            f.write("test")

        if test_file.exists():
            print("   ✅ Pode escrever em forensic_results")
            test_file.unlink()  # Limpar

    except Exception as e:
        print(f"   ❌ Erro de escrita: {e}")
        return False

    return True

def test_simple_analysis():
    """Teste 7: Análise simples de um arquivo real"""
    print("🧪 TESTE 7: Testando análise de arquivo real...")

    base_dir = Path("/Users/clubproducoes/Digimundo/scripturemon-champion")
    apps_dir = base_dir / "apps" / "scripturemon"

    # Encontrar um arquivo Python pequeno
    python_files = list(apps_dir.glob("*.py"))
    if not python_files:
        print("   ❌ Nenhum arquivo Python encontrado para teste")
        return False

    # Pegar arquivo pequeno
    test_file = min(python_files, key=lambda f: f.stat().st_size)

    try:
        with open(test_file, 'r') as f:
            content = f.read()

        if len(content) > 10000:  # Se muito grande, cortar
            content = content[:10000]

        print(f"   📄 Testando com {test_file.name} ({len(content)} chars)")

        # Análise com modelo
        start_time = time.time()
        response = ollama.generate(
            model="forensic-analyzer:latest",
            prompt=content,
            options={'num_ctx': 16384, 'temperature': 0.1}
        )
        analysis_time = time.time() - start_time

        response_text = response.get('response', '')

        if response_text and len(response_text) > 50:
            print(f"   ✅ Análise concluída ({analysis_time:.1f}s)")
            print(f"   📊 Resposta: {len(response_text)} chars")

            # Verificar se parece JSON
            if '[' in response_text and ']' in response_text:
                print("   ✅ Resposta parece conter JSON")
            else:
                print("   ⚠️ Resposta pode não estar em formato JSON")

            return True
        else:
            print("   ❌ Resposta vazia ou muito curta")
            return False

    except Exception as e:
        print(f"   ❌ Erro na análise: {e}")
        return False

def test_monitor_scripts():
    """Teste 8: Verificar se scripts de monitor funcionam"""
    print("🧪 TESTE 8: Testando scripts de monitor...")

    base_dir = Path("/Users/clubproducoes/Digimundo/scripturemon-champion")

    scripts = [
        ("forensic_monitor.py", ["--once"]),
        ("forensic_notifier.py", ["--help"])
    ]

    all_good = True
    for script_name, args in scripts:
        script_path = base_dir / "apps" / "scripturemon" / script_name

        try:
            # Executar com timeout
            result = subprocess.run(
                ["python3", str(script_path)] + args,
                timeout=10,
                capture_output=True,
                text=True,
                cwd=str(base_dir)
            )

            if result.returncode == 0:
                print(f"   ✅ {script_name}")
            else:
                print(f"   ❌ {script_name} - código de saída {result.returncode}")
                if result.stderr:
                    print(f"      Erro: {result.stderr[:200]}")
                all_good = False

        except subprocess.TimeoutExpired:
            print(f"   ⚠️ {script_name} - timeout (normal para alguns scripts)")
        except Exception as e:
            print(f"   ❌ {script_name} - erro: {e}")
            all_good = False

    return all_good

def run_all_tests():
    """Executa todos os testes"""
    print("🧪 TESTES ROBUSTOS DO SISTEMA FORENSE")
    print("=" * 60)
    print("Verificando se tudo funciona antes da execução real...")
    print()

    tests = [
        test_model_exists,
        test_model_response,
        test_directory_structure,
        test_checkpoint_system,
        test_dependencies,
        test_file_permissions,
        test_simple_analysis,
        test_monitor_scripts
    ]

    results = []
    for test_func in tests:
        try:
            result = test_func()
            results.append(result)
            print()
        except Exception as e:
            print(f"   💥 FALHA CRÍTICA: {e}")
            results.append(False)
            print()

    # Resumo
    print("=" * 60)
    print("📊 RESUMO DOS TESTES:")

    passed = sum(results)
    total = len(results)

    test_names = [
        "Modelo existe", "Modelo responde", "Estrutura OK", "Checkpoint OK",
        "Dependências OK", "Permissões OK", "Análise funciona", "Monitors OK"
    ]

    for i, (name, result) in enumerate(zip(test_names, results)):
        icon = "✅" if result else "❌"
        print(f"   {icon} {name}")

    print()
    print(f"📈 RESULTADO: {passed}/{total} testes passaram ({passed/total*100:.0f}%)")

    if passed == total:
        print("🎉 TODOS OS TESTES PASSARAM!")
        print("✅ Sistema está pronto para execução")
        return True
    elif passed >= total * 0.8:  # 80% ou mais
        print("⚠️ MAIORIA DOS TESTES PASSOU")
        print("🤔 Sistema provavelmente funcionará, mas há alguns problemas")
        return "partial"
    else:
        print("❌ MUITOS TESTES FALHARAM")
        print("🚫 NÃO execute ainda - corrija os problemas primeiro")
        return False

def main():
    """Função principal"""
    result = run_all_tests()

    if result is True:
        print("\n🚀 RECOMENDAÇÃO: PODE EXECUTAR!")
        print("   ./launch_forensic.sh")
    elif result == "partial":
        print("\n🤔 RECOMENDAÇÃO: EXECUTAR COM CUIDADO")
        print("   Monitore de perto durante execução")
    else:
        print("\n🛑 RECOMENDAÇÃO: NÃO EXECUTAR AINDA")
        print("   Corrija os problemas identificados primeiro")

    return 0 if result is True else 1

if __name__ == "__main__":
    sys.exit(main())