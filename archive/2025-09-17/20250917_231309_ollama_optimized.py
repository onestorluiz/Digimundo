#!/usr/bin/env python3
"""
🚀 OLLAMA OTIMIZADO - SEMPRE USA CONFIGURAÇÃO HÍBRIDA
Substitui todas as chamadas ollama.generate() por versão otimizada
Mac Studio M3 Ultra - 96GB RAM - 28 cores
"""

import ollama
from typing import Dict, Any, Optional
import psutil

# CONFIGURAÇÃO HÍBRIDA OBRIGATÓRIA
# Descoberta crítica: Ollama usa defaults péssimos por padrão!
HYBRID_CONFIG_BASE = {
    'num_thread': 14,     # 14 dos 28 cores CPU
    'num_gpu': 999,       # Todas camadas na GPU
    'num_batch': 2048,    # Batch grande para eficiência
    'num_keep': 1024,     # Mantém contexto
    'mmap': True,         # Memory mapping ESSENCIAL
    'use_mlock': True,    # Trava na RAM (sem swap)
    'numa': False,        # Mac não usa NUMA
    'f16_kv': True,       # FP16 para KV cache
}

# Configurações de contexto por tamanho de modelo
CONTEXT_BY_SIZE = {
    '70b': 131072,   # 128K tokens
    '32b': 65536,    # 64K tokens
    '14b': 32768,    # 32K tokens
    '7b': 32768,     # 32K tokens
    '8b': 32768,     # 32K tokens
    '3b': 65536,     # 64K tokens (pequeno aguenta muito!)
    '2b': 49152,     # 48K tokens
    'default': 16384  # 16K default seguro
}

def detect_model_size(model_name: str) -> str:
    """Detecta tamanho do modelo pelo nome"""

    model_lower = model_name.lower()

    # Busca padrões comuns
    if '70b' in model_lower:
        return '70b'
    elif '32b' in model_lower:
        return '32b'
    elif '14b' in model_lower:
        return '14b'
    elif '8b' in model_lower:
        return '8b'
    elif '7b' in model_lower:
        return '7b'
    elif '3b' in model_lower:
        return '3b'
    elif '2b' in model_lower:
        return '2b'

    return 'default'

def get_optimal_context(model_name: str, requested_context: Optional[int] = None) -> int:
    """Retorna contexto ótimo para o modelo"""

    if requested_context:
        return requested_context

    size = detect_model_size(model_name)
    return CONTEXT_BY_SIZE.get(size, CONTEXT_BY_SIZE['default'])

def check_ram_for_context(context_size: int) -> bool:
    """Verifica se tem RAM suficiente para o contexto"""

    ram = psutil.virtual_memory()
    available_gb = ram.available / (1024**3)

    # Estima ~4 bytes por token
    required_gb = (context_size * 4) / (1024**3)

    return available_gb > required_gb * 2  # Margem de segurança 2x

def generate(model: str, prompt: str, **kwargs) -> Dict[str, Any]:
    """
    🚀 SUBSTITUTO OTIMIZADO para ollama.generate()

    SEMPRE usa configuração híbrida CPU+GPU+RAM
    NUNCA usa defaults péssimos do Ollama

    Uso:
    ```python
    from ollama_optimized import generate

    # Substitui ollama.generate() por esta versão!
    response = generate("deepseek-r1:70b", prompt)
    # Automaticamente usa 128K contexto, 14 cores, etc!
    ```
    """

    # Configuração base híbrida
    options = HYBRID_CONFIG_BASE.copy()

    # Detecta e configura contexto ótimo
    requested_ctx = kwargs.get('options', {}).get('num_ctx')
    optimal_ctx = get_optimal_context(model, requested_ctx)

    # Verifica RAM
    if not check_ram_for_context(optimal_ctx):
        print(f"⚠️ RAM insuficiente para {optimal_ctx} tokens, reduzindo...")
        optimal_ctx = optimal_ctx // 2

    options['num_ctx'] = optimal_ctx

    # Merge com options do usuário (se houver)
    if 'options' in kwargs:
        user_options = kwargs['options']
        options.update(user_options)  # User options têm prioridade

    # Substitui options
    kwargs['options'] = options

    # Log da configuração (debug)
    if kwargs.get('verbose'):
        print(f"🚀 Ollama Otimizado: {model}")
        print(f"   • Contexto: {options['num_ctx']:,} tokens")
        print(f"   • CPU: {options['num_thread']} cores")
        print(f"   • GPU: {'Todas camadas' if options['num_gpu'] == 999 else options['num_gpu']}")
        print(f"   • Batch: {options['num_batch']}")

    # Chama Ollama com configuração otimizada
    return ollama.generate(model, prompt, **kwargs)

def chat(model: str, messages: list, **kwargs) -> Dict[str, Any]:
    """
    🚀 SUBSTITUTO OTIMIZADO para ollama.chat()

    SEMPRE usa configuração híbrida
    """

    # Mesma lógica de otimização
    options = HYBRID_CONFIG_BASE.copy()

    optimal_ctx = get_optimal_context(model)
    options['num_ctx'] = optimal_ctx

    if 'options' in kwargs:
        options.update(kwargs['options'])

    kwargs['options'] = options

    return ollama.chat(model, messages, **kwargs)

def embeddings(model: str, prompt: str, **kwargs) -> Dict[str, Any]:
    """
    🚀 SUBSTITUTO OTIMIZADO para ollama.embeddings()
    """

    options = HYBRID_CONFIG_BASE.copy()

    if 'options' in kwargs:
        options.update(kwargs['options'])

    kwargs['options'] = options

    return ollama.embeddings(model, prompt, **kwargs)

# Funções helper convenientes

def generate_fast(model: str, prompt: str, **kwargs):
    """Geração rápida com contexto menor"""

    kwargs['options'] = kwargs.get('options', {})
    kwargs['options']['num_ctx'] = 8192  # Contexto menor = mais rápido
    kwargs['options']['temperature'] = 0.7

    return generate(model, prompt, **kwargs)

def generate_deep(model: str, prompt: str, **kwargs):
    """Geração profunda com contexto máximo"""

    kwargs['options'] = kwargs.get('options', {})
    kwargs['options']['num_ctx'] = 131072  # Contexto MÁXIMO
    kwargs['options']['temperature'] = 0.5  # Mais focado
    kwargs['options']['num_thread'] = 20   # Mais CPU

    return generate(model, prompt, **kwargs)

def generate_balanced(model: str, prompt: str, **kwargs):
    """Geração balanceada (padrão recomendado)"""

    return generate(model, prompt, **kwargs)  # Usa configs automáticas

# Exemplo de uso e teste

def test_configuration():
    """Testa e mostra configuração otimizada"""

    print("🚀 CONFIGURAÇÃO OLLAMA OTIMIZADA")
    print("="*60)

    models_to_test = [
        "deepseek-r1:70b",
        "deepseek-r1:32b",
        "llama3.2:3b",
        "mistral:7b"
    ]

    for model in models_to_test:
        ctx = get_optimal_context(model)
        print(f"\n{model}")
        print(f"  • Contexto: {ctx:,} tokens")
        print(f"  • CPU: 14 cores")
        print(f"  • GPU: Todas camadas")
        print(f"  • RAM estimada: {(ctx * 4) / (1024**3):.1f}GB")

    print("\n" + "="*60)
    print("✅ SEMPRE use 'from ollama_optimized import generate'")
    print("❌ NUNCA use 'import ollama' direto!")
    print("\nDIGIMUNDO PRESENTE")

if __name__ == "__main__":
    test_configuration()