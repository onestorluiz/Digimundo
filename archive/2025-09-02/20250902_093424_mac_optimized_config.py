#!/usr/bin/env python3
"""
🍎 MAC OPTIMIZED CONFIG - Configuração Otimizada para Mac
Modelos leves e eficientes para rodar sem travar o sistema
"""

# CONFIGURAÇÃO OTIMIZADA PARA MAC (Max 15GB RAM para modelos)
MAC_OPTIMIZED_MODELS = {
    "principal": {
        "model": "qwen2.5-coder:7b",  # 4.7GB - Excelente para análise de código/roteiros
        "context": 32768,  # 32k tokens - bom para roteiros médios
        "temperature": 0.7
    },
    "criativo": {
        "model": "gemma2:latest",  # 5.4GB - Ótimo para análise criativa
        "context": 8192,
        "temperature": 0.8
    },
    "rápido": {
        "model": "llama3.2:3b",  # 2.0GB - Ultra rápido para respostas simples
        "context": 8192,
        "temperature": 0.6
    },
    "português": {
        "model": "mistral-ptbr:latest",  # 4.4GB - Especializado em PT-BR
        "context": 8192,
        "temperature": 0.7
    },
    "fallback": {
        "model": "mistral:instruct",  # 4.1GB - Confiável como backup
        "context": 8192,
        "temperature": 0.7
    }
}

# CONFIGURAÇÕES DE PERFORMANCE
PERFORMANCE_SETTINGS = {
    "max_parallel_models": 2,  # Máximo 2 modelos em paralelo
    "max_total_ram_gb": 15,    # Máximo 15GB RAM para modelos
    "timeout_seconds": 30,      # Timeout mais curto
    "cache_enabled": True,      # Cache agressivo
    "batch_size": 1            # Processar um por vez
}

# MODELOS PARA REMOVER (muito pesados)
HEAVY_MODELS_TO_REMOVE = [
    "llama3.1:70b",
    "yi:34b", 
    "mixtral:8x7b",
    "evolutionmon-custom:latest",
    "evolutionmon-infinity:latest",
    "linguamon-mixtral:latest",
    "linguamon:latest",
    "sabio-clone-sombras:latest",
    "linguamon-ultra:latest"
]

# PRIORIDADE DE MODELOS PARA MAC
MAC_MODEL_PRIORITY = [
    "qwen2.5-coder:7b",        # Principal - análise profunda
    "scripturemon-gen9:latest", # Especializado em cinema
    "gemma2:latest",            # Criatividade
    "mistral-ptbr:latest",      # Português
    "mistral:instruct",         # Backup confiável
    "llama3.2:3b",             # Ultra rápido
    "phi3:mini"                # Micro modelo de emergência
]

def get_optimal_model(task_type: str = "general") -> dict:
    """Retorna o modelo ideal para cada tipo de tarefa"""
    
    task_mapping = {
        "analyze": MAC_OPTIMIZED_MODELS["principal"],
        "creative": MAC_OPTIMIZED_MODELS["criativo"],
        "quick": MAC_OPTIMIZED_MODELS["rápido"],
        "portuguese": MAC_OPTIMIZED_MODELS["português"],
        "general": MAC_OPTIMIZED_MODELS["principal"]
    }
    
    return task_mapping.get(task_type, MAC_OPTIMIZED_MODELS["fallback"])

def calculate_ram_usage(models_list: list) -> float:
    """Calcula uso estimado de RAM para lista de modelos"""
    
    model_sizes = {
        "qwen2.5-coder:7b": 4.7,
        "gemma2:latest": 5.4,
        "llama3.2:3b": 2.0,
        "mistral-ptbr:latest": 4.4,
        "mistral:instruct": 4.1,
        "scripturemon-gen9:latest": 4.1,
        "phi3:mini": 2.2
    }
    
    total = sum(model_sizes.get(m, 3.0) for m in models_list)
    return total

def can_load_model(model: str, current_loaded: list) -> bool:
    """Verifica se pode carregar mais um modelo sem exceder limite"""
    
    future_models = current_loaded + [model]
    total_ram = calculate_ram_usage(future_models)
    
    return total_ram <= PERFORMANCE_SETTINGS["max_total_ram_gb"]