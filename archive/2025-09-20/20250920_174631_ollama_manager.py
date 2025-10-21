#!/usr/bin/env python3
"""
Ollama Manager - Gerenciador de modelos LLM
Fase 2.A - Chat Engine Real
"""

import json
import subprocess
import time
from typing import Dict, List, Optional, Generator, Any
from dataclasses import dataclass
from enum import Enum
import requests
from apps.scripturemon.bootstrap import get_config

class ModelSize(Enum):
    """Categorias de tamanho de modelo"""
    TINY = "tiny"      # < 2GB
    SMALL = "small"    # 2-5GB  
    MEDIUM = "medium"  # 5-10GB
    LARGE = "large"    # 10-20GB
    XLARGE = "xlarge"  # > 20GB

@dataclass
class OllamaModel:
    """Representa um modelo Ollama"""
    name: str
    id: str
    size_bytes: int
    size_category: ModelSize
    modified: str
    available: bool = True
    loaded: bool = False
    
    @property
    def size_gb(self) -> float:
        """Retorna tamanho em GB"""
        return self.size_bytes / (1024**3)

class OllamaManager:
    """
    Gerenciador central de modelos Ollama
    Coordena descoberta, carregamento e geração
    """
    
    # Mapeamento de modelos preferidos por categoria
    PREFERRED_MODELS = {
        "chat": ["llama3.2:3b", "mistral:instruct", "qwen2.5-coder:7b"],
        "analysis": ["deepseek-r1:7b", "llama3.1:8b"],
        "creative": ["scripturemon-ptbr:latest", "mistral:latest"],
        "heavy": ["scripturemon-ultimate:latest", "deepseek-r1:70b"]
    }
    
    def __init__(self):
        """Inicializa manager"""
        self.config = get_config()
        self.base_url = self.config.get("ollama_url", "http://localhost:11434")
        self.timeout = self.config.get("ollama_timeout", 30)
        self.models_cache: Dict[str, OllamaModel] = {}
        self.current_model: Optional[str] = None
        self._discover_models()
    
    def _discover_models(self) -> None:
        """Descobre modelos disponíveis"""
        try:
            # Tenta via API primeiro
            response = requests.get(f"{self.base_url}/api/tags", timeout=30)
            if response.status_code == 200:
                data = response.json()
                for model in data.get("models", []):
                    name = model["name"]
                    self.models_cache[name] = OllamaModel(
                        name=name,
                        id=model.get("digest", ""),
                        size_bytes=model.get("size", 0),
                        size_category=self._categorize_size(model.get("size", 0)),
                        modified=model.get("modified_at", ""),
                        available=True
                    )
            else:
                # Fallback para comando CLI
                self._discover_via_cli()
        except Exception:
            # Se API falhar, usa CLI
            self._discover_via_cli()
    
    def _discover_via_cli(self) -> None:
        """Descobre modelos via CLI quando API não disponível"""
        try:
            result = subprocess.run(
                ["ollama", "list"],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')[1:]  # Skip header
                for line in lines:
                    if line.strip():
                        parts = line.split()
                        if len(parts) >= 4:
                            name = parts[0]
                            size_str = parts[2]
                            size_bytes = self._parse_size(size_str)
                            
                            self.models_cache[name] = OllamaModel(
                                name=name,
                                id=parts[1] if len(parts) > 1 else "",
                                size_bytes=size_bytes,
                                size_category=self._categorize_size(size_bytes),
                                modified=parts[3] if len(parts) > 3 else "",
                                available=True
                            )
        except Exception as e:
            print(f"⚠️ Erro descobrindo modelos: {e}")
    
    def _parse_size(self, size_str: str) -> int:
        """Converte string de tamanho para bytes"""
        size_str = size_str.upper()
        multipliers = {"KB": 1024, "MB": 1024**2, "GB": 1024**3}
        
        for suffix, mult in multipliers.items():
            if suffix in size_str:
                try:
                    num = float(size_str.replace(suffix, "").strip())
                    return int(num * mult)
                except:
                    pass
        return 0
    
    def _categorize_size(self, size_bytes: int) -> ModelSize:
        """Categoriza tamanho do modelo"""
        gb = size_bytes / (1024**3)
        if gb < 2:
            return ModelSize.TINY
        elif gb < 5:
            return ModelSize.SMALL
        elif gb < 10:
            return ModelSize.MEDIUM
        elif gb < 20:
            return ModelSize.LARGE
        else:
            return ModelSize.XLARGE
    
    def list_models(self, category: Optional[str] = None) -> List[OllamaModel]:
        """Lista modelos disponíveis"""
        models = list(self.models_cache.values())
        
        if category and category in self.PREFERRED_MODELS:
            # Filtra por categoria preferida
            preferred_names = self.PREFERRED_MODELS[category]
            models = [m for m in models if any(pref in m.name for pref in preferred_names)]
        
        return sorted(models, key=lambda m: m.size_bytes)
    
    def get_best_model(self, category: str = "chat", max_size_gb: float = 10) -> Optional[str]:
        """Retorna melhor modelo disponível para categoria"""
        candidates = self.list_models(category)
        
        # Filtra por tamanho máximo
        candidates = [m for m in candidates if m.size_gb <= max_size_gb]
        
        if not candidates:
            # Se não houver candidatos, pega o menor disponível
            all_models = self.list_models()
            if all_models:
                return all_models[0].name
            return None
        
        # Retorna o maior modelo dentro do limite (geralmente melhor)
        return candidates[-1].name
    
    def load_model(self, model_name: Optional[str] = None) -> bool:
        """Carrega modelo na memória"""
        if not model_name:
            model_name = self.get_best_model()
        
        if not model_name:
            print("❌ Nenhum modelo disponível")
            return False
        
        if model_name not in self.models_cache:
            print(f"⚠️ Modelo {model_name} não encontrado")
            return False
        
        try:
            # Testa modelo com geração simples
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": model_name,
                    "prompt": "Hello",
                    "stream": False,
                    "options": {"num_predict": 1}
                },
                timeout=30
            )
            
            if response.status_code == 200:
                self.current_model = model_name
                self.models_cache[model_name].loaded = True
                print(f"✅ Modelo {model_name} carregado")
                return True
            else:
                print(f"❌ Erro carregando {model_name}: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Erro carregando modelo: {e}")
            return False
    
    def unload_model(self, model_name: Optional[str] = None) -> bool:
        """Descarrega modelo da memória"""
        if not model_name:
            model_name = self.current_model
        
        if not model_name:
            return True
        
        try:
            # Ollama descarrega automaticamente após timeout
            # Mas podemos forçar com keep_alive=0
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": model_name,
                    "prompt": "",
                    "keep_alive": 0
                },
                timeout=30
            )
            
            if model_name in self.models_cache:
                self.models_cache[model_name].loaded = False
            
            if self.current_model == model_name:
                self.current_model = None
            
            return True
            
        except:
            # Se falhar, não é crítico
            return True
    
    def generate(self, 
                 prompt: str,
                 model: Optional[str] = None,
                 temperature: float = 0.7,
                 max_tokens: int = 2048,
                 system: Optional[str] = None) -> Optional[str]:
        """Gera resposta síncrona"""
        
        model = model or self.current_model or self.get_best_model()
        if not model:
            return None
        
        # Prepara prompt com system se fornecido
        full_prompt = prompt
        if system:
            full_prompt = f"System: {system}\n\nUser: {prompt}\n\nAssistant:"
        
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": model,
                    "prompt": full_prompt,
                    "stream": False,
                    "options": {
                        "temperature": temperature,
                        "num_predict": max_tokens
                    }
                },
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get("response", "")
            else:
                print(f"❌ Erro na geração: {response.status_code}")
                return None
                
        except requests.Timeout:
            print("⏱️ Timeout na geração")
            return None
        except Exception as e:
            print(f"❌ Erro: {e}")
            return None
    
    def stream_generate(self,
                       prompt: str,
                       model: Optional[str] = None,
                       temperature: float = 0.7,
                       max_tokens: int = 2048,
                       system: Optional[str] = None) -> Generator[str, None, None]:
        """Gera resposta em streaming"""
        
        model = model or self.current_model or self.get_best_model()
        if not model:
            yield "❌ Nenhum modelo disponível"
            return
        
        # Prepara prompt
        full_prompt = prompt
        if system:
            full_prompt = f"System: {system}\n\nUser: {prompt}\n\nAssistant:"
        
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": model,
                    "prompt": full_prompt,
                    "stream": True,
                    "options": {
                        "temperature": temperature,
                        "num_predict": max_tokens
                    }
                },
                stream=True,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                for line in response.iter_lines():
                    if line:
                        try:
                            data = json.loads(line)
                            token = data.get("response", "")
                            if token:
                                yield token
                            
                            if data.get("done", False):
                                break
                        except:
                            continue
            else:
                yield f"❌ Erro: {response.status_code}"
                
        except requests.Timeout:
            yield "⏱️ Timeout na geração"
        except Exception as e:
            yield f"❌ Erro: {e}"
    
    def get_model_info(self, model_name: str) -> Optional[Dict[str, Any]]:
        """Retorna informações detalhadas do modelo"""
        if model_name not in self.models_cache:
            return None
        
        model = self.models_cache[model_name]
        return {
            "name": model.name,
            "id": model.id,
            "size_gb": round(model.size_gb, 2),
            "size_category": model.size_category.value,
            "loaded": model.loaded,
            "available": model.available,
            "modified": model.modified
        }
    
    def health_check(self) -> Dict[str, Any]:
        """Verifica saúde do Ollama"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=30)
            ollama_running = response.status_code == 200
        except:
            ollama_running = False
        
        return {
            "ollama_running": ollama_running,
            "models_available": len(self.models_cache),
            "current_model": self.current_model,
            "base_url": self.base_url,
            "categories": list(self.PREFERRED_MODELS.keys())
        }

# Singleton global
_manager_instance: Optional[OllamaManager] = None

def get_ollama_manager() -> OllamaManager:
    """Retorna instância singleton do manager"""
    global _manager_instance
    if _manager_instance is None:
        _manager_instance = OllamaManager()
    return _manager_instance

__all__ = ["OllamaManager", "OllamaModel", "ModelSize", "get_ollama_manager"]