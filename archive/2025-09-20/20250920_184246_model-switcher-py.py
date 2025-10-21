#!/usr/bin/env python3
"""
🔄 MODEL SWITCHER - Sistema de Troca Dinâmica de Modelos
Alterna entre modelos Ollama baseado em recursos disponíveis
"""

import asyncio
import psutil
import ollama
import logging
import time
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger("ModelSwitcher")


class ModelSize(Enum):
    """Tamanhos de modelo"""
    TINY = "tiny"      # < 1GB RAM
    SMALL = "small"    # < 2GB RAM
    MEDIUM = "medium"  # < 4GB RAM
    LARGE = "large"    # > 4GB RAM


@dataclass
class ModelConfig:
    """Configuração de um modelo"""
    name: str
    size: ModelSize
    ram_required_gb: float
    performance_score: float  # 0-1, maior = melhor
    capabilities: List[str]
    context_length: int


class ModelSwitcher:
    """Gerenciador de modelos com troca dinâmica"""
    
    def __init__(self):
        # Configurações dos modelos
        self.models = {
            ModelSize.TINY: ModelConfig(
                name="tinyllama:latest",
                size=ModelSize.TINY,
                ram_required_gb=0.5,
                performance_score=0.3,
                capabilities=["basic", "fast"],
                context_length=2048
            ),
            ModelSize.SMALL: ModelConfig(
                name="llama3.2:3b",
                size=ModelSize.SMALL,
                ram_required_gb=1.5,
                performance_score=0.6,
                capabilities=["basic", "reasoning", "coding"],
                context_length=4096
            ),
            ModelSize.MEDIUM: ModelConfig(
                name="llama3.2:latest",
                size=ModelSize.MEDIUM,
                ram_required_gb=3.0,
                performance_score=0.8,
                capabilities=["advanced", "reasoning", "coding", "analysis"],
                context_length=8192
            ),
            ModelSize.LARGE: ModelConfig(
                name="mixtral:8x7b",
                size=ModelSize.LARGE,
                ram_required_gb=6.0,
                performance_score=0.95,
                capabilities=["expert", "reasoning", "coding", "analysis", "creative"],
                context_length=32768
            )
        }
        
        # Estado atual
        self.current_model: Optional[ModelConfig] = None
        self.loaded_models: Dict[str, bool] = {}
        
        # Configurações de threshold
        self.thresholds = {
            'ram_critical': 95,    # % - forçar modelo menor
            'ram_high': 85,        # % - considerar modelo menor
            'ram_comfortable': 60, # % - pode usar modelo maior
            'cpu_high': 80,        # % - limitar processamento
            'swap_penalty': 10     # % - penalidade se usando swap
        }
        
        # Cache de performance
        self.performance_cache = {}
        self.model_metrics = {}
        
        # Estatísticas
        self.stats = {
            'switches': 0,
            'forced_downgrades': 0,
            'upgrades': 0,
            'generation_count': 0,
            'total_generation_time': 0
        }
        
        # Inicializar
        self._init_ollama()
        logger.info("✅ Model Switcher inicializado")
    
    def _init_ollama(self):
        """Verificar e inicializar Ollama"""
        try:
            # Verificar modelos disponíveis
            models = ollama.list()
            available = [m['name'] for m in models.get('models', [])]
            
            for model_config in self.models.values():
                self.loaded_models[model_config.name] = model_config.name in available
                
                if self.loaded_models[model_config.name]:
                    logger.info(f"✅ Modelo disponível: {model_config.name}")
                else:
                    logger.warning(f"⚠️ Modelo não encontrado: {model_config.name}")
            
        except Exception as e:
            logger.error(f"❌ Erro ao conectar com Ollama: {e}")
            raise
    
    def get_system_resources(self) -> Dict[str, float]:
        """Obter recursos do sistema"""
        mem = psutil.virtual_memory()
        swap = psutil.swap_memory()
        
        return {
            'ram_total_gb': mem.total / (1024**3),
            'ram_available_gb': mem.available / (1024**3),
            'ram_percent': mem.percent,
            'swap_percent': swap.percent,
            'cpu_percent': psutil.cpu_percent(interval=0.1),
            'cpu_count': psutil.cpu_count()
        }
    
    def calculate_available_ram(self, resources: Dict[str, float]) -> float:
        """Calcular RAM efetivamente disponível para modelo"""
        available = resources['ram_available_gb']
        
        # Penalizar se usando swap
        if resources['swap_percent'] > self.thresholds['swap_penalty']:
            available *= 0.8
        
        # Reservar RAM para o sistema
        system_reserve = 0.5  # GB
        available = max(0, available - system_reserve)
        
        return available
    
    def select_best_model(self, 
                         task_type: Optional[str] = None,
                         required_capabilities: List[str] = None) -> ModelConfig:
        """Selecionar melhor modelo baseado em recursos e tarefa"""
        resources = self.get_system_resources()
        available_ram = self.calculate_available_ram(resources)
        
        logger.info(f"📊 RAM disponível: {available_ram:.1f}GB, CPU: {resources['cpu_percent']:.1f}%")
        
        # Filtrar modelos por capacidade
        suitable_models = []
        
        for model in self.models.values():
            # Verificar se está carregado
            if not self.loaded_models.get(model.name, False):
                continue
            
            # Verificar RAM
            if model.ram_required_gb > available_ram:
                continue
            
            # Verificar capacidades se especificadas
            if required_capabilities:
                if not all(cap in model.capabilities for cap in required_capabilities):
                    continue
            
            suitable_models.append(model)
        
        if not suitable_models:
            # Forçar modelo menor se nenhum adequado
            logger.warning("⚠️ Nenhum modelo adequado, usando TINY")
            return self.models[ModelSize.TINY]
        
        # Selecionar baseado em performance vs recursos
        if resources['ram_percent'] > self.thresholds['ram_critical']:
            # Modo crítico - menor modelo
            selected = min(suitable_models, key=lambda m: m.ram_required_gb)
        elif resources['ram_percent'] > self.thresholds['ram_high']:
            # Modo conservador
            selected = suitable_models[0]
        else:
            # Modo normal - melhor performance
            selected = max(suitable_models, key=lambda m: m.performance_score)
        
        return selected
    
    async def switch_model(self, target_model: str = None) -> bool:
        """Trocar para modelo específico ou melhor disponível"""
        try:
            # Se modelo especificado, validar
            if target_model:
                model_config = None
                for config in self.models.values():
                    if config.name == target_model:
                        model_config = config
                        break
                
                if not model_config:
                    logger.error(f"Modelo não configurado: {target_model}")
                    return False
            else:
                # Selecionar automaticamente
                model_config = self.select_best_model()
            
            # Verificar se já é o modelo atual
            if self.current_model and self.current_model.name == model_config.name:
                return True
            
            # Verificar se modelo está disponível
            if not self.loaded_models.get(model_config.name, False):
                logger.info(f"📥 Baixando modelo {model_config.name}...")
                ollama.pull(model_config.name)
                self.loaded_models[model_config.name] = True
            
            # Registrar troca
            old_model = self.current_model.name if self.current_model else "none"
            self.current_model = model_config
            
            # Atualizar estatísticas
            self.stats['switches'] += 1
            
            if self.current_model and model_config.size.value < self.current_model.size.value:
                self.stats['forced_downgrades'] += 1
            elif self.current_model and model_config.size.value > self.current_model.size.value:
                self.stats['upgrades'] += 1
            
            logger.info(f"🔄 Modelo trocado: {old_model} → {model_config.name}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Erro ao trocar modelo: {e}")
            return False
    
    async def generate(self, prompt: str, 
                      temperature: float = 0.7,
                      max_tokens: Optional[int] = None,
                      system_prompt: Optional[str] = None) -> str:
        """Gerar resposta usando modelo atual"""
        start_time = time.time()
        
        # Garantir que temos um modelo
        if not self.current_model:
            await self.switch_model()
        
        if not self.current_model:
            raise RuntimeError("Nenhum modelo disponível")
        
        try:
            # Preparar prompt completo
            if system_prompt:
                full_prompt = f"{system_prompt}\n\n{prompt}"
            else:
                full_prompt = prompt
            
            # Configurar opções
            options = {
                'temperature': temperature,
                'num_predict': max_tokens or 512,
                'top_p': 0.9,
                'top_k': 40
            }
            
            # Gerar resposta
            logger.info(f"🤖 Gerando com {self.current_model.name}...")
            
            response = ollama.generate(
                model=self.current_model.name,
                prompt=full_prompt,
                options=options
            )
            
            # Extrair texto
            generated_text = response.get('response', '')
            
            # Atualizar métricas
            generation_time = time.time() - start_time
            self.stats['generation_count'] += 1
            self.stats['total_generation_time'] += generation_time
            
            # Atualizar métricas do modelo
            model_name = self.current_model.name
            if model_name not in self.model_metrics:
                self.model_metrics[model_name] = {
                    'uses': 0,
                    'total_time': 0,
                    'errors': 0
                }
            
            self.model_metrics[model_name]['uses'] += 1
            self.model_metrics[model_name]['total_time'] += generation_time
            
            logger.info(f"✅ Geração completa em {generation_time:.2f}s")
            
            return generated_text
            
        except Exception as e:
            logger.error(f"❌ Erro na geração: {e}")
            
            # Registrar erro
            if self.current_model:
                model_name = self.current_model.name
                if model_name in self.model_metrics:
                    self.model_metrics[model_name]['errors'] += 1
            
            # Tentar com modelo menor
            if self.current_model and self.current_model.size != ModelSize.TINY:
                logger.info("🔄 Tentando com modelo menor...")
                smaller_model = self.models[ModelSize.TINY]
                await self.switch_model(smaller_model.name)
                return await self.generate(prompt, temperature, max_tokens, system_prompt)
            
            raise
    
    async def auto_optimize(self):
        """Otimizar modelo baseado em métricas"""
        resources = self.get_system_resources()
        
        # Se recursos críticos, downgrade
        if resources['ram_percent'] > self.thresholds['ram_critical']:
            logger.warning("⚠️ RAM crítica, fazendo downgrade...")
            
            if self.current_model and self.current_model.size != ModelSize.TINY:
                await self.switch_model(self.models[ModelSize.TINY].name)
        
        # Se recursos confortáveis, considerar upgrade
        elif resources['ram_percent'] < self.thresholds['ram_comfortable']:
            if self.current_model:
                # Verificar se pode fazer upgrade
                current_idx = list(self.models.keys()).index(self.current_model.size)
                
                if current_idx < len(self.models) - 1:
                    next_size = list(self.models.keys())[current_idx + 1]
                    next_model = self.models[next_size]
                    
                    if next_model.ram_required_gb <= resources['ram_available_gb']:
                        logger.info("📈 Recursos disponíveis para upgrade")
                        await self.switch_model(next_model.name)
    
    def get_model_info(self) -> Dict[str, Any]:
        """Obter informações do modelo atual"""
        if not self.current_model:
            return {
                'current_model': None,
                'status': 'no_model_loaded'
            }
        
        return {
            'current_model': self.current_model.name,
            'size': self.current_model.size.value,
            'ram_required': self.current_model.ram_required_gb,
            'performance_score': self.current_model.performance_score,
            'capabilities': self.current_model.capabilities,
            'context_length': self.current_model.context_length
        }
    
    def get_stats(self) -> Dict[str, Any]:
        """Obter estatísticas do switcher"""
        avg_generation_time = (self.stats['total_generation_time'] / 
                             self.stats['generation_count'] 
                             if self.stats['generation_count'] > 0 else 0)
        
        return {
            'current_model': self.current_model.name if self.current_model else None,
            'switches': self.stats['switches'],
            'forced_downgrades': self.stats['forced_downgrades'],
            'upgrades': self.stats['upgrades'],
            'generation_count': self.stats['generation_count'],
            'average_generation_time': avg_generation_time,
            'loaded_models': self.loaded_models,
            'model_metrics': self.model_metrics,
            'system_resources': self.get_system_resources()
        }
    
    async def benchmark_models(self) -> Dict[str, Dict[str, float]]:
        """Benchmark todos os modelos disponíveis"""
        logger.info("🏁 Iniciando benchmark de modelos...")
        
        test_prompt = "Explain quantum computing in simple terms."
        results = {}
        
        for model_config in self.models.values():
            if not self.loaded_models.get(model_config.name, False):
                continue
            
            logger.info(f"📊 Testando {model_config.name}...")
            
            # Trocar para modelo
            await self.switch_model(model_config.name)
            
            # Fazer 3 testes
            times = []
            for i in range(3):
                start = time.time()
                
                try:
                    await self.generate(test_prompt, temperature=0.7)
                    elapsed = time.time() - start
                    times.append(elapsed)
                except Exception as e:
                    logger.error(f"Erro no benchmark: {e}")
                    times.append(float('inf'))
            
            # Calcular média
            avg_time = sum(times) / len(times)
            
            results[model_config.name] = {
                'average_time': avg_time,
                'min_time': min(times),
                'max_time': max(times),
                'size': model_config.size.value,
                'ram_required': model_config.ram_required_gb
            }
        
        logger.info("✅ Benchmark completo")
        return results
    
    async def health_check(self) -> bool:
        """Verificar saúde do switcher"""
        try:
            # Verificar conexão Ollama
            models = ollama.list()
            
            # Verificar se tem pelo menos um modelo
            available = [m['name'] for m in models.get('models', [])]
            
            for model_config in self.models.values():
                if model_config.name in available:
                    return True
            
            return False
            
        except:
            return False


# Teste do Model Switcher
async def test_model_switcher():
    """Testar o Model Switcher"""
    print("🧪 Testando Model Switcher...")
    
    switcher = ModelSwitcher()
    
    # Teste 1: Recursos do sistema
    print("\n1️⃣ Recursos do sistema:")
    resources = switcher.get_system_resources()
    for key, value in resources.items():
        if 'gb' in key:
            print(f"   {key}: {value:.2f}")
        else:
            print(f"   {key}: {value:.1f}")
    
    # Teste 2: Selecionar modelo
    print("\n2️⃣ Selecionando melhor modelo...")
    await switcher.switch_model()
    info = switcher.get_model_info()
    print(f"   Modelo: {info['current_model']}")
    print(f"   RAM necessária: {info['ram_required']}GB")
    
    # Teste 3: Gerar texto
    print("\n3️⃣ Gerando texto...")
    text = await switcher.generate("Olá! O que é DigiMundo?", temperature=0.7)
    print(f"   Resposta: {text[:100]}...")
    
    # Teste 4: Estatísticas
    print("\n4️⃣ Estatísticas:")
    stats = switcher.get_stats()
    print(f"   Gerações: {stats['generation_count']}")
    print(f"   Tempo médio: {stats['average_generation_time']:.2f}s")
    
    print("\n✅ Testes concluídos!")


if __name__ == "__main__":
    asyncio.run(test_model_switcher())
