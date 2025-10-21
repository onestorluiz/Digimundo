#!/usr/bin/env python3
"""
🐛 MODO DEBUG - OLLAMA CONTINUOUS LEARNING
Versão com timeouts exagerados e logging verboso para monitoramento manual
"""

import sys
import json
import time
from datetime import datetime
import sqlite3
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple
from collections import defaultdict
import requests
import hashlib
import subprocess
import os
import re
import logging
from colorama import init, Fore, Style

# Inicializa colorama para output colorido
init()

# ============ CONFIGURAÇÃO DE DEBUG ============
DEBUG_MODE = True
SUPER_VERBOSE = True
CHECKPOINT_EVERY = 10  # segundos
TIMEOUT_REQUESTS = 600  # 10 MINUTOS (exagerado propositalmente)
TIMEOUT_OLLAMA = 1200   # 20 MINUTOS para análises grandes
SAVE_EVERY_RESPONSE = True
LOG_LEVEL = logging.DEBUG

# Configuração de logging super verboso
logging.basicConfig(
    level=LOG_LEVEL,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(f'debug_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

sys.path.insert(0, 'src')

# Importa SafeJSONParser com fallback
try:
    from safe_json_parser_20250921_214934 import safe_json_parse, calculate_confidence
    SAFE_PARSER_AVAILABLE = True
    logger.info("✅ SafeJSONParser carregado com sucesso")
except ImportError:
    SAFE_PARSER_AVAILABLE = False
    logger.warning("⚠️ SafeJSONParser não disponível - usando parser básico")

from scripturemon_champion.analysis.script_doctor import ScriptDoctor

class OllamaDebugLearning:
    """
    Sistema de aprendizado com DEBUG EXTREMO
    """

    def __init__(self, model: str = "mixtral-cpu-force:latest"):
        logger.info("=" * 60)
        logger.info("🐛 INICIANDO MODO DEBUG - TIMEOUTS EXAGERADOS")
        logger.info("=" * 60)

        self.doctor = ScriptDoctor()
        self.model = model
        self.ollama_endpoint = "http://127.0.0.1:11434/api/generate"
        self.checkpoint_count = 0
        self.start_time = time.time()

        # Configurações de timeout exageradas
        self.options = {
            "temperature": 0.7,
            "top_k": 100,
            "top_p": 0.9,
            "num_predict": 8192,  # Resposta grande
            "num_ctx": 200000,     # Contexto máximo
            "num_batch": 512,
            "num_thread": 20,      # Usa 20 threads CPU
            "timeout": TIMEOUT_OLLAMA
        }

        logger.info(f"📊 Configurações de DEBUG:")
        logger.info(f"   - Modelo: {self.model}")
        logger.info(f"   - Timeout Requests: {TIMEOUT_REQUESTS}s ({TIMEOUT_REQUESTS/60:.1f} min)")
        logger.info(f"   - Timeout Ollama: {TIMEOUT_OLLAMA}s ({TIMEOUT_OLLAMA/60:.1f} min)")
        logger.info(f"   - Checkpoint a cada: {CHECKPOINT_EVERY}s")

        # Teste de conexão com retry e logging
        self.test_connection_debug()

        # Diretórios
        self.theory_dir = Path("theory")
        self.masters_dir = Path("screenplays/masters")
        self.debug_dir = Path("debug_output")
        self.debug_dir.mkdir(exist_ok=True)

        logger.info(f"📁 Diretórios configurados:")
        logger.info(f"   - Theory: {self.theory_dir}")
        logger.info(f"   - Masters: {self.masters_dir}")
        logger.info(f"   - Debug Output: {self.debug_dir}")

    def test_connection_debug(self):
        """Teste de conexão com debug extremo"""
        logger.info("\n🔍 TESTANDO CONEXÃO COM OLLAMA...")

        for attempt in range(3):
            logger.info(f"   Tentativa {attempt + 1}/3...")

            try:
                start = time.time()
                response = requests.get(
                    "http://127.0.0.1:11434/api/tags",
                    timeout=10
                )
                elapsed = time.time() - start

                logger.info(f"   ✅ Resposta em {elapsed:.2f}s - Status: {response.status_code}")

                if response.status_code == 200:
                    models = response.json().get("models", [])
                    logger.info(f"   📋 Modelos disponíveis: {len(models)}")

                    for model in models:
                        name = model.get("name", "")
                        size = model.get("size", 0) / (1024**3)
                        logger.info(f"      - {name}: {size:.1f}GB")

                        if self.model in name:
                            logger.info(f"   ✅ MODELO {self.model} ENCONTRADO!")
                            return True

            except Exception as e:
                logger.error(f"   ❌ Erro: {e}")

            time.sleep(2)

        logger.error("❌ FALHA NA CONEXÃO COM OLLAMA!")
        return False

    def checkpoint(self, message: str):
        """Cria checkpoint com timestamp e métricas"""
        self.checkpoint_count += 1
        elapsed = time.time() - self.start_time

        # Cor baseada no tempo decorrido
        if elapsed < 60:
            color = Fore.GREEN
        elif elapsed < 300:
            color = Fore.YELLOW
        else:
            color = Fore.RED

        logger.info(f"\n{color}🏁 CHECKPOINT #{self.checkpoint_count}{Style.RESET_ALL}")
        logger.info(f"   📍 {message}")
        logger.info(f"   ⏱️ Tempo decorrido: {elapsed:.2f}s ({elapsed/60:.1f} min)")
        logger.info(f"   💾 Memória: {self.get_memory_usage()}")
        logger.info(f"   🔥 CPU: {self.get_cpu_usage()}")

    def get_memory_usage(self):
        """Obtém uso de memória"""
        try:
            import psutil
            mem = psutil.virtual_memory()
            return f"{mem.percent:.1f}% ({mem.used/(1024**3):.1f}GB / {mem.total/(1024**3):.1f}GB)"
        except:
            return "N/A"

    def get_cpu_usage(self):
        """Obtém uso de CPU do processo Ollama"""
        try:
            result = subprocess.run(
                "ps aux | grep 'ollama.*runner' | grep -v grep | awk '{print $3}' | head -1",
                shell=True,
                capture_output=True,
                text=True
            )
            cpu = result.stdout.strip()
            return f"{cpu}%" if cpu else "0%"
        except:
            return "N/A"

    def analyze_with_ollama_debug(self, prompt: str, context: str = "") -> Optional[str]:
        """
        Análise com Ollama - MODO DEBUG EXTREMO
        """
        self.checkpoint(f"Iniciando análise Ollama - Prompt: {len(prompt)} chars")

        full_prompt = f"{context}\n\n{prompt}" if context else prompt

        logger.info(f"\n📝 PROMPT COMPLETO ({len(full_prompt)} caracteres):")
        logger.info("=" * 40)
        logger.info(full_prompt[:500] + "..." if len(full_prompt) > 500 else full_prompt)
        logger.info("=" * 40)

        payload = {
            "model": self.model,
            "prompt": full_prompt,
            "options": self.options,
            "stream": False
        }

        logger.info(f"\n🚀 ENVIANDO REQUEST PARA OLLAMA...")
        logger.info(f"   Timeout configurado: {TIMEOUT_REQUESTS}s")
        logger.info(f"   Modelo: {self.model}")

        try:
            start = time.time()
            last_checkpoint = start

            # Request com timeout exagerado
            logger.info(f"   ⏳ Aguardando resposta (pode demorar até {TIMEOUT_REQUESTS/60:.1f} minutos)...")

            response = requests.post(
                self.ollama_endpoint,
                json=payload,
                timeout=TIMEOUT_REQUESTS
            )

            elapsed = time.time() - start
            self.checkpoint(f"Resposta recebida após {elapsed:.2f}s")

            if response.status_code == 200:
                result = response.json()
                response_text = result.get('response', '')

                logger.info(f"✅ SUCESSO! Resposta: {len(response_text)} caracteres")

                # Salva resposta em arquivo
                if SAVE_EVERY_RESPONSE:
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    debug_file = self.debug_dir / f"response_{timestamp}.json"
                    with open(debug_file, 'w') as f:
                        json.dump({
                            "prompt": prompt[:200],
                            "response": response_text,
                            "elapsed": elapsed,
                            "model": self.model
                        }, f, indent=2)
                    logger.info(f"   💾 Resposta salva em: {debug_file}")

                return response_text

            else:
                logger.error(f"❌ ERRO HTTP: {response.status_code}")
                logger.error(f"   Response: {response.text}")
                return None

        except requests.exceptions.Timeout:
            logger.error(f"❌ TIMEOUT após {TIMEOUT_REQUESTS}s!")
            return None

        except Exception as e:
            logger.error(f"❌ ERRO INESPERADO: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return None

    def run_debug_cycle(self):
        """
        Executa um ciclo completo de debug
        """
        logger.info("\n" + "=" * 60)
        logger.info("🎬 INICIANDO CICLO DE DEBUG COMPLETO")
        logger.info("=" * 60)

        self.checkpoint("Início do ciclo de debug")

        # 1. Lista arquivos de teoria
        theory_files = list(self.theory_dir.glob("*.txt"))[:2]  # Apenas 2 para debug
        logger.info(f"\n📚 Arquivos de teoria encontrados: {len(theory_files)}")

        for i, file in enumerate(theory_files, 1):
            self.checkpoint(f"Processando teoria {i}/{len(theory_files)}: {file.name}")

            try:
                with open(file, 'r') as f:
                    content = f.read()[:5000]  # Primeiros 5000 chars

                logger.info(f"   📖 Lendo {file.name}: {len(content)} caracteres")

                # Análise debug
                prompt = f"""
                DEBUG MODE - ANALYSIS TEST

                Analyze this screenwriting theory excerpt and provide:
                1. Main concept (1 sentence)
                2. Key insight (1 sentence)
                3. Practical application (1 sentence)

                Keep response under 200 words.

                Text: {content[:1000]}
                """

                response = self.analyze_with_ollama_debug(prompt)

                if response:
                    logger.info(f"   ✅ Análise concluída!")
                    logger.info(f"   Preview: {response[:200]}...")
                else:
                    logger.error(f"   ❌ Falha na análise")

            except Exception as e:
                logger.error(f"   ❌ Erro ao processar {file.name}: {e}")

        # 2. Teste com roteiro
        self.checkpoint("Testando com roteiro de exemplo")

        screenplay_test = """
        DEBUG TEST - MATRIX OPENING

        Analyze the opening of The Matrix:
        - Neo's introduction
        - The white rabbit
        - Trinity's first appearance

        What does this establish about the story world?
        """

        response = self.analyze_with_ollama_debug(screenplay_test)

        # 3. Relatório final
        total_time = time.time() - self.start_time

        logger.info("\n" + "=" * 60)
        logger.info("📊 RELATÓRIO FINAL DE DEBUG")
        logger.info("=" * 60)
        logger.info(f"   ⏱️ Tempo total: {total_time:.2f}s ({total_time/60:.1f} min)")
        logger.info(f"   🏁 Checkpoints: {self.checkpoint_count}")
        logger.info(f"   💾 Memória final: {self.get_memory_usage()}")
        logger.info(f"   🔥 CPU final: {self.get_cpu_usage()}")
        logger.info(f"   📁 Logs salvos em: debug_output/")
        logger.info("=" * 60)

def main():
    """
    Execução principal do modo debug
    """
    print(Fore.CYAN + """
    ╔══════════════════════════════════════════╗
    ║    🐛 MODO DEBUG - SCRIPTUREMON          ║
    ║    Timeouts Exagerados & Logging Total   ║
    ╚══════════════════════════════════════════╝
    """ + Style.RESET_ALL)

    # Cria instância debug
    debug_system = OllamaDebugLearning()

    # Executa ciclo de debug
    debug_system.run_debug_cycle()

    print(Fore.GREEN + "\n✅ DEBUG COMPLETO!" + Style.RESET_ALL)
    print(f"Verifique os logs em: debug_output/")

if __name__ == "__main__":
    main()