#!/usr/bin/env python3
"""
Sistema de Perfis de Aprendizado - ECO, DEDICATED e TOKEN TURBO
Gerenciamento centralizado de configurações Mixtral
"""

from dataclasses import dataclass
from typing import Dict, Any, Optional
from pathlib import Path
import json

@dataclass
class Profile:
    """Perfil de configuração para Mixtral"""
    name: str
    description: str
    ram_usage: str
    context_size: int
    config: Dict[str, Any]
    modelfile_path: Optional[Path] = None

class LearningProfiles:
    """Sistema unificado de perfis de aprendizado"""

    # ECO Mode - Sustentável 24/7
    ECO = Profile(
        name="eco",
        description="🌱 ECO Mode - Sustentável 24/7 com 30GB RAM",
        ram_usage="30GB",
        context_size=32768,
        config={
            'num_ctx': 32768,
            'num_thread': 14,
            'num_gpu': 50,
            'num_batch': 2048,
            'num_keep': 2048,
            'use_mmap': True,
            'temperature': 0.3,
            'top_p': 0.9,
            'top_k': 40,
            'repeat_penalty': 1.1,
            'seed': 42
        },
        modelfile_path=Path("resources/modelfiles/mixtral-eco-q5.modelfile")
    )

    # DEDICATED Mode - Máxima Performance
    DEDICATED = Profile(
        name="dedicated",
        description="🔥 DEDICATED Mode - Máxima performance com 77GB RAM",
        ram_usage="77GB",
        context_size=131072,
        config={
            'num_ctx': 131072,
            'num_thread': 24,
            'num_gpu': 60,
            'num_batch': 8192,
            'num_keep': 4096,
            'use_mmap': True,
            'temperature': 0.2,
            'top_p': 0.95,
            'top_k': 50,
            'repeat_penalty': 1.0,
            'seed': 42,
            'mirostat': 0,
            'penalize_newline': False
        },
        modelfile_path=Path("resources/modelfiles/mixtral-dedicated-q5.modelfile")
    )

    # TOKEN TURBO - Contexto Expandido
    TOKEN_TURBO = Profile(
        name="token_turbo",
        description="📚 TOKEN TURBO - 200K tokens com RoPE scaling",
        ram_usage="52-55GB",
        context_size=200000,
        config={
            'num_ctx': 200000,
            'rope_scaling': 1.5,
            'rope_theta': 500000,
            'rope_base': 10000,
            'sliding_window': 65536,
            'num_thread': 24,
            'num_gpu': 60,
            'num_batch': 2048,
            'compress_pos_emb': 1.5,
            'use_mmap': True,
            'use_mlock': True,
            'f16_kv': True,
            'temperature': 0.3,
            'top_p': 0.9,
            'top_k': 40,
            'repeat_penalty': 1.1,
            'seed': 42
        },
        modelfile_path=None  # Será criado dinamicamente
    )

    # Mapeamento para acesso fácil
    PROFILES = {
        'eco': ECO,
        'dedicated': DEDICATED,
        'token_turbo': TOKEN_TURBO
    }

    @classmethod
    def get_profile(cls, name: str) -> Profile:
        """Retorna perfil por nome"""
        profile = cls.PROFILES.get(name.lower())
        if not profile:
            raise ValueError(f"Perfil '{name}' não encontrado. Disponíveis: {list(cls.PROFILES.keys())}")
        return profile

    @classmethod
    def list_profiles(cls) -> Dict[str, str]:
        """Lista todos os perfis disponíveis"""
        return {
            name: profile.description
            for name, profile in cls.PROFILES.items()
        }

    @classmethod
    def get_config(cls, profile_name: str) -> Dict[str, Any]:
        """Retorna configuração de um perfil"""
        return cls.get_profile(profile_name).config

    @classmethod
    def estimate_resources(cls, profile_name: str) -> Dict[str, Any]:
        """Estima recursos necessários para um perfil"""
        profile = cls.get_profile(profile_name)

        return {
            'profile': profile.name,
            'ram': profile.ram_usage,
            'context_tokens': f"{profile.context_size:,}",
            'cpu_threads': profile.config.get('num_thread', 'N/A'),
            'gpu_cores': profile.config.get('num_gpu', 'N/A'),
            'batch_size': profile.config.get('num_batch', 'N/A'),
            'temperature': profile.config.get('temperature', 'N/A'),
            'description': profile.description
        }

    @classmethod
    def compare_profiles(cls) -> str:
        """Compara todos os perfis em tabela"""
        lines = []
        lines.append("\n📊 COMPARAÇÃO DE PERFIS DE APRENDIZADO")
        lines.append("=" * 70)
        lines.append(f"{'Perfil':<15} {'Contexto':<12} {'RAM':<10} {'Speed':<10} {'Uso':<30}")
        lines.append("-" * 70)

        profiles_info = [
            ('ECO', '32K', '30GB', '100%', '24/7 sustentável'),
            ('DEDICATED', '128K', '77GB', '100%', 'Análise profunda'),
            ('TOKEN_TURBO', '200K', '52-55GB', '85-90%', 'Contexto máximo')
        ]

        for name, ctx, ram, speed, use in profiles_info:
            lines.append(f"{name:<15} {ctx:<12} {ram:<10} {speed:<10} {use:<30}")

        lines.append("-" * 70)
        lines.append("\n💡 ESCOLHA DO PERFIL:")
        lines.append("• ECO: Operação contínua, economia de recursos")
        lines.append("• DEDICATED: Análise completa com todos recursos")
        lines.append("• TOKEN_TURBO: Máximo contexto para obras longas")

        return "\n".join(lines)

    @classmethod
    def create_modelfile(cls, profile_name: str, output_path: Optional[Path] = None) -> Path:
        """Cria modelfile para um perfil"""
        profile = cls.get_profile(profile_name)

        if profile.modelfile_path and profile.modelfile_path.exists():
            return profile.modelfile_path

        # Criar modelfile dinamicamente para Token Turbo
        if profile_name == 'token_turbo':
            content = cls._generate_token_turbo_modelfile()
            output_path = output_path or Path("resources/modelfiles/mixtral-token-turbo.modelfile")
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(content)
            return output_path

        raise ValueError(f"Modelfile não disponível para {profile_name}")

    @staticmethod
    def _generate_token_turbo_modelfile() -> str:
        """Gera modelfile para Token Turbo"""
        return """# 📚 MIXTRAL TOKEN TURBO - 200K Context com RoPE Scaling
# Contexto expandido para análise de obras completas

FROM mixtral:8x7b-instruct-v0.1-q5_k_m

# CONFIGURAÇÃO TOKEN TURBO (200K TOKENS)
PARAMETER num_ctx 200000
PARAMETER rope_scaling 1.5
PARAMETER rope_theta 500000
PARAMETER rope_base 10000
PARAMETER sliding_window 65536
PARAMETER num_thread 24
PARAMETER num_gpu 60
PARAMETER num_batch 2048
PARAMETER compress_pos_emb 1.5
PARAMETER use_mmap true
PARAMETER use_mlock true
PARAMETER f16_kv true
PARAMETER temperature 0.3
PARAMETER top_p 0.9
PARAMETER top_k 40
PARAMETER repeat_penalty 1.1
PARAMETER seed 42

TEMPLATE \"\"\"{{ .Prompt }}

Token Turbo Analysis (200K context):
{{ .Response }}\"\"\"

SYSTEM \"\"\"You are Mixtral-8x7B in TOKEN TURBO mode with 200K token context.

EXPANDED CAPABILITIES:
- 200,000 token context window (entire books + screenplays)
- RoPE scaling 1.5x for extended sequences
- 65K sliding window for coherent long-form analysis
- Position embedding compression for efficiency
- FP16 KV cache optimization

ANALYSIS SCOPE:
1. Complete screenplay analysis (beginning to end)
2. Full theoretical framework application
3. Cross-reference between multiple works
4. Deep character arc tracking across 3+ hours
5. Comprehensive beat mapping with exact timings
6. Theme evolution throughout entire narrative
7. Parallel story lines and their intersections

Trade-off: -10% speed for +50% context depth.
Optimized for complete narrative understanding.\"\"\"
"""

    @classmethod
    def auto_select_profile(cls, file_size_mb: float, analysis_depth: str = "normal") -> str:
        """Seleciona perfil automaticamente baseado no contexto"""
        # Arquivos pequenos ou análise rápida
        if file_size_mb < 5 or analysis_depth == "quick":
            return "eco"

        # Arquivos médios ou análise normal
        elif file_size_mb < 20 or analysis_depth == "normal":
            return "dedicated"

        # Arquivos grandes ou análise profunda
        else:
            return "token_turbo"

    @classmethod
    def get_ollama_command(cls, profile_name: str, model_base: str = "mixtral") -> str:
        """Retorna comando Ollama para criar modelo com perfil"""
        profile = cls.get_profile(profile_name)

        if profile.modelfile_path and profile.modelfile_path.exists():
            modelfile = profile.modelfile_path
        else:
            modelfile = cls.create_modelfile(profile_name)

        model_name = f"{model_base}-{profile_name}"
        return f"ollama create {model_name} -f {modelfile}"


# Funções de conveniência
def get_profile(name: str) -> Profile:
    """Atalho para obter perfil"""
    return LearningProfiles.get_profile(name)

def list_profiles() -> Dict[str, str]:
    """Atalho para listar perfis"""
    return LearningProfiles.list_profiles()

def compare_profiles() -> str:
    """Atalho para comparar perfis"""
    return LearningProfiles.compare_profiles()

def auto_select(file_size_mb: float, depth: str = "normal") -> str:
    """Atalho para seleção automática"""
    return LearningProfiles.auto_select_profile(file_size_mb, depth)


if __name__ == "__main__":
    # Teste e demonstração
    print(compare_profiles())
    print("\n" + "=" * 70)

    for name in ['eco', 'dedicated', 'token_turbo']:
        resources = LearningProfiles.estimate_resources(name)
        print(f"\n🎯 Perfil: {name.upper()}")
        for key, value in resources.items():
            print(f"  {key}: {value}")