"""
Gerenciador de configurações simples.
Carrega configurações de YAML ou JSON.
"""

import json
import yaml
import os
from pathlib import Path
from typing import Dict, Any, Optional


def load_config(config_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Carrega configuração de arquivo YAML ou JSON.
    
    Args:
        config_path: Caminho para arquivo de config (opcional)
        
    Returns:
        Dicionário de configuração
    """
    # Se não fornecido, usar config padrão
    if not config_path:
        return get_default_config()
    
    # Verificar se arquivo existe
    if not os.path.exists(config_path):
        print(f"Arquivo de config não encontrado: {config_path}")
        return get_default_config()
    
    # Detectar formato pelo extensão
    path = Path(config_path)
    
    try:
        with open(config_path, 'r') as f:
            if path.suffix in ['.yaml', '.yml']:
                return yaml.safe_load(f)
            elif path.suffix == '.json':
                return json.load(f)
            else:
                # Tentar JSON primeiro
                f.seek(0)
                try:
                    return json.load(f)
                except:
                    # Tentar YAML
                    f.seek(0)
                    return yaml.safe_load(f)
    except Exception as e:
        print(f"Erro ao carregar config: {e}")
        return get_default_config()


def get_default_config() -> Dict[str, Any]:
    """
    Retorna configuração padrão.
    
    Returns:
        Dicionário de configuração padrão
    """
    return {
        'system': {
            'name': 'scripturemon-validation',
            'version': '1.0.0',
            'debug': False
        },
        'memory': {
            'time_weighted_retrieval': True,
            'promote_on_hits': 5,
            'max_l1_size': 100,
            'max_l2_size': 500,
            'max_l3_size': 2000,
            'max_l4_size': 10000
        },
        'rag': {
            'enabled': True,
            'provider': 'chroma',
            'k': 8,
            'embedding_model': 'all-MiniLM-L6-v2'
        },
        'scoring': {
            'weights': {
                'structure': 0.3,
                'emotion': 0.2,
                'technique': 0.3,
                'theme': 0.2
            },
            'thresholds': {
                'excellent': 80,
                'good': 60,
                'fair': 40
            }
        },
        'models': {
            'extractor': 'llama3.2:3b',
            'analyzer': 'mistral:instruct',
            'evaluator': 'scripturemon-maestro',
            'synthesizer': 'scripturemon-soulos'
        },
        'telepathy': {
            'enabled': True,
            'redis_host': 'localhost',
            'redis_port': 6379,
            'timeout': 1.0,
            'use_fakeredis': True
        },
        'logging': {
            'level': 'INFO',
            'file_enabled': True,
            'console_enabled': True,
            'format': 'standard'
        }
    }


def save_config(config: Dict[str, Any], config_path: str, format: str = 'yaml') -> bool:
    """
    Salva configuração em arquivo.
    
    Args:
        config: Dicionário de configuração
        config_path: Caminho para salvar
        format: Formato ('yaml' ou 'json')
        
    Returns:
        True se sucesso, False se erro
    """
    try:
        with open(config_path, 'w') as f:
            if format == 'yaml':
                yaml.safe_dump(config, f, default_flow_style=False, indent=2)
            else:
                json.dump(config, f, indent=2)
        return True
    except Exception as e:
        print(f"Erro ao salvar config: {e}")
        return False


def merge_configs(base: Dict[str, Any], overlay: Dict[str, Any]) -> Dict[str, Any]:
    """
    Mescla duas configurações, com overlay sobrescrevendo base.
    
    Args:
        base: Configuração base
        overlay: Configuração a sobrescrever
        
    Returns:
        Configuração mesclada
    """
    result = base.copy()
    
    for key, value in overlay.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            # Recursivo para dicionários aninhados
            result[key] = merge_configs(result[key], value)
        else:
            result[key] = value
    
    return result


def validate_config(config: Dict[str, Any]) -> bool:
    """
    Valida se configuração tem campos obrigatórios.
    
    Args:
        config: Configuração a validar
        
    Returns:
        True se válida, False se inválida
    """
    required_fields = [
        'system.name',
        'system.version',
        'memory.promote_on_hits',
        'scoring.weights.structure',
        'scoring.weights.emotion',
        'scoring.weights.technique',
        'scoring.weights.theme'
    ]
    
    for field_path in required_fields:
        parts = field_path.split('.')
        value = config
        
        try:
            for part in parts:
                value = value[part]
        except (KeyError, TypeError):
            print(f"Campo obrigatório ausente: {field_path}")
            return False
    
    # Validar que pesos somam 1.0
    weights = config['scoring']['weights']
    total = sum(weights.values())
    if abs(total - 1.0) > 0.01:
        print(f"Pesos de scoring devem somar 1.0, mas somam {total}")
        return False
    
    return True