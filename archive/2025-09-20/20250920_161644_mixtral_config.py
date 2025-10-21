#!/usr/bin/env python3
"""
🎯 CONFIGURAÇÃO PADRÃO DO SISTEMA MIXTRAL
Centraliza todas as configurações para usar Mixtral como modelo principal
"""

class MixtralConfig:
    # Modelo padrão do sistema
    DEFAULT_MODEL = "mixtral-dedicated-q5"
    ECO_MODEL = "mixtral-eco-q5"

    # Configurações Ollama otimizadas para Mixtral
    OLLAMA_CONFIG = {
        'num_ctx': 131072,      # 128K tokens
        'num_thread': 24,       # 86% dos 28 cores
        'num_gpu': 60,          # Todos os 60 cores GPU
        'num_batch': 4096,      # Batch otimizado
        'keep_context': 2048,   # Contexto mantido
        'temperature': 0.3,     # Precisão analítica
        'top_p': 0.9,
        'top_k': 40,
        'repeat_penalty': 1.1,
        'seed': 42              # Reprodutibilidade
    }

    # Configurações de memória
    MEMORY_LIMITS = {
        'mixtral_dedicated': 45,  # GB
        'mixtral_eco': 35,        # GB
        'minimum_free': 10        # GB mínimo livre
    }

# Caminhos da biblioteca
LIBRARY_PATH = "digilibrary/BIBLIOTECA_ROTEIROS"
LIBRARY_CATEGORIES = ["meus_filmes", "roteiros_mestres", "teoria"]

# Especialistas para análise
SPECIALISTS = [
    "character_analyst",
    "pacing_expert",
    "theme_specialist",
    "structure_architect",
    "dialogue_expert"
]

# Save the Cat Beats
SAVE_THE_CAT_BEATS = [
    ("Opening Image", 1),
    ("Theme Stated", 5),
    ("Setup", 10),
    ("Catalyst", 12),
    ("Debate", 25),
    ("Break into Two", 25),
    ("B Story", 30),
    ("Fun and Games", 50),
    ("Midpoint", 50),
    ("Bad Guys Close In", 75),
    ("All Is Lost", 75),
    ("Dark Night of the Soul", 80),
    ("Break into Three", 80),
    ("Finale", 95),
    ("Final Image", 100)
]

# NOVA CONFIGURAÇÃO TURBO - SWEET TURBO MODE
TURBO_CONFIG = {
        'num_ctx': 131072,      # Mantém contexto máximo
        'num_thread': 24,       # Mantém threads atuais
        'num_gpu': 60,          # Mantém GPU cores
        'num_batch': 8192,      # DOBRA batch (era 4096)
        'top_k': 3,             # AUMENTA experts (era 2 implícito)
        'temperature': 0.3,     # Mantém precisão
        'top_p': 0.9,           # Mantém diversidade
        'repeat_penalty': 1.1,  # Mantém penalidade
        'seed': 42,             # Mantém reprodutibilidade
        'use_mmap': True,       # Otimização memória
        'use_mlock': True,      # Trava na RAM
        'f16_kv': True,         # Cache FP16
    }

# NOVA CONFIGURAÇÃO TOKEN TURBO - MÁXIMO CONTEXTO (200K)
TOKEN_TURBO_CONFIG = {
        # CONTEXTO EXPANDIDO
        'num_ctx': 200000,        # De 131K → 200K tokens (+53%)

        # ROPE SCALING (permite extensão)
        'rope_scaling': 1.5,      # Escala conservadora inicial
        'rope_theta': 500000,     # Base frequency ajustada
        'rope_base': 10000,       # RoPE base

        # SLIDING WINDOW OTIMIZADA
        'sliding_window': 65536,  # Dobra janela (era 32K)

        # ATTENTION OPTIMIZATION (reduz batch para compensar contexto)
        'num_batch': 2048,        # Reduz batch para compensar contexto
        'repeat_last_n': 256,     # Aumenta repeat penalty window

        # MANTÉM CONFIGURAÇÕES DE CPU/GPU
        'num_thread': 24,         # Mantém threads atuais
        'num_gpu': 60,            # Mantém GPU cores

        # MEMORY OPTIMIZATION
        'compress_pos_emb': 1.5,  # Comprime position embeddings
        'use_mmap': True,         # Memory mapping essencial
        'use_mlock': True,        # Lock na RAM
        'f16_kv': True,          # KV cache em FP16

        # MANTÉM QUALIDADE
        'temperature': 0.3,
        'top_p': 0.9,
        'top_k': 40,
        'repeat_penalty': 1.1,
        'seed': 42
    }

def get_model_config(mode="dedicated"):
    """Retorna configuração do modelo baseada no modo"""
    if mode == "eco":
        config = MixtralConfig.OLLAMA_CONFIG.copy()
        config['num_thread'] = 14  # 50% dos cores para eco
        config['num_ctx'] = 32768  # 32K tokens para eco
        return MixtralConfig.ECO_MODEL, config
    elif mode == "turbo":  # SWEET TURBO MODE
        return MixtralConfig.DEFAULT_MODEL, TURBO_CONFIG
    elif mode == "token_turbo":  # TOKEN TURBO MODE - MÁXIMO CONTEXTO
        return MixtralConfig.DEFAULT_MODEL, TOKEN_TURBO_CONFIG
    else:
        return MixtralConfig.DEFAULT_MODEL, MixtralConfig.OLLAMA_CONFIG
