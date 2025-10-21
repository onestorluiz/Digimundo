#!/usr/bin/env python3
"""
Ollama Real - Interface verdadeira com Ollama
Adaptado do sistema original para o novo minimalista
Compatível com a filosofia ChatGPT de código mínimo
"""

import subprocess
import json
import time
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class OllamaResponse:
    """Resposta estruturada do Ollama"""
    model: str
    prompt_tokens: int
    completion: str
    latency_ms: int
    success: bool = True
    error: Optional[str] = None

class OllamaReal:
    """Interface real com Ollama - minimalista mas funcional"""

    # Configuração otimizada para Mac Studio M3 Ultra
    DEFAULT_OPTIONS = {
        'num_ctx': 131072,    # 128K tokens
        'num_thread': 14,     # Metade dos 28 cores
        'temperature': 0.7,
        'top_p': 0.9
    }

    def __init__(self):
        self.models = []
        self.default_model = None
        self._discover_models()

    def _discover_models(self):
        """Descobre modelos disponíveis"""
        try:
            result = subprocess.run(
                ['ollama', 'list'],
                capture_output=True,
                text=True,
                timeout=5,
                check=False
            )

            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')[1:]  # Skip header
                for line in lines:
                    if line:
                        model_name = line.split()[0]
                        if ':latest' in model_name:
                            model_name = model_name.replace(':latest', '')
                        self.models.append(model_name)

                # Seleciona modelo padrão - MIXTRAL primeiro!
                for preferred in ['mixtral-dedicated-q5', 'mixtral-eco-q5', 'mixtral', 'deepseek-r1:32b', 'llama2', 'codellama']:
                    if preferred in self.models:
                        self.default_model = preferred
                        break

                if not self.default_model and self.models:
                    self.default_model = self.models[0]

            logger.info(f"Ollama: {len(self.models)} modelos encontrados")

        except Exception as e:
            logger.warning(f"Ollama não disponível: {e}")
            self.models = []

    def generate(self,
                prompt: str,
                model: Optional[str] = None,
                temperature: float = 0.7,
                max_tokens: int = 2048,
                timeout: int = 60,
                options: Optional[Dict] = None) -> OllamaResponse:
        """
        Gera resposta usando Ollama

        Args:
            prompt: Texto do prompt
            model: Modelo a usar (ou default)
            temperature: Criatividade (0-1)
            max_tokens: Máximo de tokens
            timeout: Timeout em segundos
            options: Opções adicionais do Ollama

        Returns:
            OllamaResponse com resultado
        """
        model = model or self.default_model

        if not model:
            return OllamaResponse(
                model="none",
                prompt_tokens=len(prompt.split()),
                completion="Nenhum modelo Ollama disponível",
                latency_ms=0,
                success=False,
                error="No models available"
            )

        # Prepara comando
        cmd = {
            'model': model,
            'prompt': prompt,
            'stream': False,
            'options': options or self.DEFAULT_OPTIONS
        }

        # Ajusta opções
        if temperature is not None:
            cmd['options']['temperature'] = temperature
        if max_tokens:
            cmd['options']['num_predict'] = max_tokens

        try:
            start = time.time()

            # Executa Ollama
            result = subprocess.run(
                ['ollama', 'run', model],
                input=prompt,
                capture_output=True,
                text=True,
                timeout=timeout,
                check=False
            )

            latency = int((time.time() - start) * 1000)

            if result.returncode == 0:
                completion = result.stdout.strip()
                return OllamaResponse(
                    model=model,
                    prompt_tokens=len(prompt.split()),
                    completion=completion,
                    latency_ms=latency,
                    success=True
                )
            else:
                return OllamaResponse(
                    model=model,
                    prompt_tokens=len(prompt.split()),
                    completion="",
                    latency_ms=latency,
                    success=False,
                    error=result.stderr
                )

        except subprocess.TimeoutExpired:
            return OllamaResponse(
                model=model,
                prompt_tokens=len(prompt.split()),
                completion="",
                latency_ms=timeout * 1000,
                success=False,
                error=f"Timeout após {timeout}s"
            )

        except Exception as e:
            return OllamaResponse(
                model=model,
                prompt_tokens=len(prompt.split()),
                completion="",
                latency_ms=0,
                success=False,
                error=str(e)
            )

    def list_models(self) -> List[str]:
        """Lista modelos disponíveis"""
        return self.models.copy()

    def has_model(self, model_name: str) -> bool:
        """Verifica se modelo está disponível"""
        return model_name in self.models

    def pull_model(self, model_name: str, timeout: int = 600) -> bool:
        """
        Baixa um modelo do Ollama

        Args:
            model_name: Nome do modelo
            timeout: Timeout em segundos

        Returns:
            True se sucesso
        """
        try:
            result = subprocess.run(
                ['ollama', 'pull', model_name],
                capture_output=True,
                text=True,
                timeout=timeout,
                check=False
            )

            if result.returncode == 0:
                self._discover_models()  # Atualiza lista
                logger.info(f"Modelo {model_name} baixado com sucesso")
                return True
            else:
                logger.error(f"Erro ao baixar {model_name}: {result.stderr}")
                return False

        except Exception as e:
            logger.error(f"Erro ao baixar modelo: {e}")
            return False

# Compatibilidade com interface antiga
def discover_models() -> List[str]:
    """Descobre modelos (compatibilidade)"""
    ollama = OllamaReal()
    return ollama.list_models()

def generate(prompt: str,
            model: str = 'mock-model',
            temperature: float = 0.2,
            max_tokens: int = 256,
            timeout: int = 30) -> OllamaResponse:
    """Gera resposta (compatibilidade)"""
    ollama = OllamaReal()
    return ollama.generate(prompt, model, temperature, max_tokens, timeout)

# Teste se executado diretamente
if __name__ == "__main__":
    print("Testando Ollama Real...")

    ollama = OllamaReal()
    print(f"Modelos disponíveis: {ollama.list_models()}")
    print(f"Modelo padrão: {ollama.default_model}")

    if ollama.default_model:
        response = ollama.generate(
            "Escreva uma frase sobre cinema em português",
            temperature=0.7,
            max_tokens=50
        )

        if response.success:
            print(f"\nResposta ({response.latency_ms}ms):")
            print(response.completion)
        else:
            print(f"Erro: {response.error}")
    else:
        print("Nenhum modelo Ollama disponível")