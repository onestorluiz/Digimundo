#!/usr/bin/env python3
"""
🧠 GRADIENT CONFIG - Configuração Central do Cérebro
"""

# Configuração do modelo Gradient
GRADIENT_CONFIG = {
    "model": "scripturemon-gradient",  # Modelo customizado
    "fallback_model": "llama3-gradient:70b-instruct-1048k-q6_K",
    "num_ctx": 256000,      # 256k tokens
    "temperature": 0.2,     # Factual
    "num_gpu": 60,          # GPU cores do M3 Ultra
    "num_thread": 16,       # Performance cores
    "num_batch": 512,       # Batch otimizado
    "num_predict": 15000,   # Respostas longas
    "timeout": 120,         # 2 minutos timeout
    "f16_kv": True,         # Precisão alta
}

# Capacidades de contexto
CONTEXT_CAPACITY = {
    "pdfs_simultaneos": 15,     # ~200k tokens
    "roteiro_completo": True,    # ~30k tokens
    "historico_completo": True,  # ~100k tokens
    "margem_segura": 26000,      # Tokens de reserva
}

# Mapeamento de PDFs para tokens estimados
PDF_TOKEN_ESTIMATES = {
    "Story_McKee.pdf": 15000,
    "Screenplay_Field.pdf": 10000,
    "Writers_Journey_Vogler.pdf": 12000,
    "Save_the_Cat_Snyder.pdf": 8000,
    "Anatomy_of_Story_Truby.pdf": 13000,
    # ... adicionar outros conforme necessário
}

def get_gradient_command(prompt, context_size=None):
    """Gera comando Ollama otimizado para Gradient"""
    ctx = context_size or GRADIENT_CONFIG["num_ctx"]
    
    return [
        "ollama", "run",
        GRADIENT_CONFIG["model"],
        "--num-ctx", str(ctx),
        "--num-gpu", str(GRADIENT_CONFIG["num_gpu"]),
        "--num-thread", str(GRADIENT_CONFIG["num_thread"]),
        prompt
    ]

def calculate_context_usage(pdfs=0, screenplay_tokens=0, history_tokens=0):
    """Calcula uso de contexto e verifica se cabe"""
    total = pdfs + screenplay_tokens + history_tokens
    available = GRADIENT_CONFIG["num_ctx"]
    
    return {
        "total_used": total,
        "available": available,
        "remaining": available - total,
        "percentage": (total / available) * 100,
        "fits": total < (available - CONTEXT_CAPACITY["margem_segura"])
    }
