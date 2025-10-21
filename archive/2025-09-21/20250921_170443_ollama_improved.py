#!/usr/bin/env python3
"""
Melhorias para o sistema Ollama - Detecção e Retry Logic
"""

import requests
import time
from typing import Optional

def check_ollama_with_retry(max_retries: int = 3, wait_time: int = 5) -> bool:
    """
    Verifica se Ollama está rodando com retry logic
    """
    print("🔍 Verificando conexão com Ollama...")

    for attempt in range(max_retries):
        try:
            # Primeiro tenta endpoint de status
            response = requests.get("http://127.0.0.1:11434/api/tags", timeout=10)

            if response.status_code == 200:
                print("✅ Ollama conectado com sucesso!")
                return True
            else:
                print(f"  Tentativa {attempt + 1}/{max_retries}: Status {response.status_code}")

        except requests.exceptions.ConnectionError:
            print(f"  Tentativa {attempt + 1}/{max_retries}: Conexão recusada")
        except requests.exceptions.Timeout:
            print(f"  Tentativa {attempt + 1}/{max_retries}: Timeout")
        except Exception as e:
            print(f"  Tentativa {attempt + 1}/{max_retries}: Erro {type(e).__name__}")

        if attempt < max_retries - 1:
            print(f"  ⏳ Aguardando {wait_time}s antes de tentar novamente...")
            time.sleep(wait_time)

    # Se todas as tentativas falharam
    print("\n❌ FALHA: Ollama não está respondendo após múltiplas tentativas")
    print("\n📝 SOLUÇÕES:")
    print("1. Verifique se Ollama está instalado: ollama --version")
    print("2. Inicie o servidor: ollama serve")
    print("3. Em outro terminal, teste: ollama list")
    print("4. Verifique se a porta 11434 está livre: lsof -i :11434")

    return False


def ollama_request_with_retry(
    endpoint: str,
    model: str,
    prompt: str,
    temperature: float = 0.5,
    max_retries: int = 2,
    timeout: int = 900
) -> Optional[str]:
    """
    Faz requisição ao Ollama com retry logic
    """

    for attempt in range(max_retries):
        try:
            print(f"  📡 Enviando request (tentativa {attempt + 1}/{max_retries})...")

            response = requests.post(
                endpoint,
                json={
                    "model": model,
                    "prompt": prompt,
                    "stream": False,
                    "temperature": temperature,
                    "top_p": 0.9
                },
                timeout=timeout
            )

            if response.status_code == 200:
                return response.json().get("response", "")
            elif response.status_code == 404:
                print(f"  ❌ Modelo {model} não encontrado")
                print(f"  💡 Certifique-se que o modelo está instalado: ollama pull {model}")
                return None
            else:
                print(f"  ⚠️ Status {response.status_code}")

        except requests.exceptions.Timeout:
            print(f"  ⏱️ Timeout após {timeout}s")
            if attempt < max_retries - 1:
                print(f"  🔄 Tentando novamente com timeout menor...")
                timeout = timeout // 2  # Reduz timeout pela metade
        except requests.exceptions.ConnectionError:
            print(f"  ❌ Erro de conexão")
            if attempt == 0 and check_ollama_with_retry(max_retries=1):
                # Tenta reconectar uma vez
                continue
            return None
        except Exception as e:
            print(f"  ❌ Erro inesperado: {type(e).__name__}: {e}")

        if attempt < max_retries - 1:
            print(f"  ⏳ Aguardando 3s antes de retry...")
            time.sleep(3)

    return None


def cleanup_orphan_processes():
    """
    Limpa processos órfãos do Ollama
    """
    import subprocess
    import os

    print("🧹 Limpando processos órfãos...")

    try:
        # Lista processos ollama
        result = subprocess.run(
            ["ps", "aux"],
            capture_output=True,
            text=True
        )

        ollama_processes = []
        for line in result.stdout.split('\n'):
            if 'ollama' in line and 'grep' not in line:
                parts = line.split()
                if len(parts) > 1:
                    pid = parts[1]
                    ollama_processes.append(pid)

        if ollama_processes:
            print(f"  Encontrados {len(ollama_processes)} processos Ollama")

            # Verifica quais estão ativos
            active = []
            for pid in ollama_processes:
                try:
                    os.kill(int(pid), 0)  # Signal 0 apenas verifica se processo existe
                    active.append(pid)
                except:
                    pass

            if len(active) > 1:
                print(f"  ⚠️ Múltiplas instâncias detectadas: {active}")
                print("  💡 Considere reiniciar Ollama: pkill ollama && ollama serve")
            else:
                print(f"  ✅ Apenas uma instância ativa")

        else:
            print("  ✅ Nenhum processo órfão encontrado")

    except Exception as e:
        print(f"  ⚠️ Erro ao verificar processos: {e}")


def test_model_availability(model_name: str) -> bool:
    """
    Testa se um modelo específico está disponível
    """
    print(f"🔍 Verificando modelo {model_name}...")

    try:
        response = requests.get("http://127.0.0.1:11434/api/tags", timeout=10)

        if response.status_code == 200:
            models = response.json().get("models", [])

            for model in models:
                if model_name in model.get("name", ""):
                    size_gb = model.get("size", 0) / (1024**3)
                    print(f"  ✅ Modelo encontrado: {model.get('name')} ({size_gb:.1f}GB)")
                    return True

            print(f"  ❌ Modelo {model_name} não encontrado")
            print(f"  💡 Instale com: ollama pull {model_name}")
            return False

    except Exception as e:
        print(f"  ❌ Erro ao verificar modelos: {e}")
        return False


if __name__ == "__main__":
    print("="*60)
    print("🔧 TESTE DE MELHORIAS DO SISTEMA OLLAMA")
    print("="*60)

    # 1. Limpa processos órfãos
    cleanup_orphan_processes()
    print()

    # 2. Verifica conexão com retry
    if check_ollama_with_retry():
        print()

        # 3. Verifica modelo Token Turbo
        if test_model_availability("mixtral-token-turbo:latest"):
            print()

            # 4. Testa request com retry
            print("📝 Testando request com retry...")
            response = ollama_request_with_retry(
                endpoint="http://127.0.0.1:11434/api/generate",
                model="mixtral-token-turbo:latest",
                prompt="Say 'System working!' in 5 words",
                timeout=30
            )

            if response:
                print(f"  ✅ Resposta: {response[:100]}...")
            else:
                print("  ❌ Falha no request")

    print("\n" + "="*60)
    print("✅ Teste completo!")