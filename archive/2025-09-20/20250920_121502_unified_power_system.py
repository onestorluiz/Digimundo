#!/usr/bin/env python3
"""
⚡ SISTEMA UNIFICADO DE POTÊNCIA E MODELOS
Harmoniza controle de potência com seleção de modelos (32b/mixtral)
Totalmente compatível com M3 Ultra (60 GPU cores, 96GB RAM)
"""

import json
import time
from pathlib import Path
from typing import Dict, Any, Optional
import subprocess
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent))


class UnifiedPowerSystem:
    """Sistema harmonizado de potência e modelos"""

    # Arquivo de configuração unificado
    CONFIG_FILE = Path(__file__).parent.parent.parent / "data" / "unified_power_config.json"

    # Hardware specs do M3 Ultra
    HARDWARE = {
        "cpu_cores": 28,
        "gpu_cores": 60,
        "neural_cores": 32,  # Não usado pelo Ollama
        "ram_gb": 96,
        "bandwidth_gbps": 800
    }

    # Presets harmonizados incluindo modelo
    PRESETS = {
        "ECO_32B": {
            "name": "🌱 Eco 32B",
            "model": "mixtral-dedicated-q5",  # mixtral-r1:32b
            "model_ram_gb": 25,
            "sleep_between_scripts": 2.0,
            "ollama_frequency": 5,
            "ollama_timeout": 30,
            "scene_chunk_size": 500,
            "num_predict": 30,
            "num_ctx": 131072,  # 128K
            "num_thread": 8,
            "num_gpu": 20,  # 33% dos 60 cores
            "description": "Mínimo recurso, roda para sempre (25GB RAM, 0.1% CPU)"
        },

        "BALANCED_32B": {
            "name": "⚖️ Balanced 32B",
            "model": "mixtral-dedicated-q5",
            "model_ram_gb": 25,
            "sleep_between_scripts": 1.0,
            "ollama_frequency": 3,
            "ollama_timeout": 45,
            "scene_chunk_size": 1000,
            "num_predict": 50,
            "num_ctx": 131072,
            "num_thread": 14,
            "num_gpu": 30,  # 50% dos 60 cores
            "description": "Bom equilíbrio para uso diário (25GB RAM, 10% CPU)"
        },

        "TURBO_32B": {
            "name": "🚀 Turbo 32B",
            "model": "mixtral-dedicated-q5",
            "model_ram_gb": 30,
            "sleep_between_scripts": 0.5,
            "ollama_frequency": 2,
            "ollama_timeout": 60,
            "scene_chunk_size": 2000,
            "num_predict": 100,
            "num_ctx": 131072,
            "num_thread": 20,
            "num_gpu": 45,  # 75% dos 60 cores
            "description": "Alta performance com 32B (30GB RAM, 40% CPU)"
        },

        "ECO_MIXTRAL": {
            "name": "🌿 Eco Mixtral Q5",
            "model": "mixtral-eco-q5",
            "model_ram_gb": 30,
            "sleep_between_scripts": 5.0,
            "ollama_frequency": 10,
            "ollama_timeout": 600,
            "scene_chunk_size": 10000,
            "num_predict": 500,
            "num_ctx": 32768,  # 32K para economizar
            "num_thread": 12,
            "num_gpu": 40,  # 67% dos 60 cores
            "description": "Mixtral Q5 sustentável 24/7 (30GB RAM, 20% CPU)"
        },

        "BALANCED_MIXTRAL": {
            "name": "⚡ Balanced Mixtral Q5",
            "model": "mixtral-eco-q5",  # Usa eco mas com mais recursos
            "model_ram_gb": 45,
            "sleep_between_scripts": 3.0,
            "ollama_frequency": 5,
            "ollama_timeout": 900,
            "scene_chunk_size": 20000,
            "num_predict": 1000,
            "num_ctx": 65536,  # 64K
            "num_thread": 18,
            "num_gpu": 50,  # 83% dos 60 cores
            "description": "Mixtral Q5 equilibrado (35 GB RAM, 40% CPU)"
        },

        "DEDICATED_MIXTRAL": {
            "name": "🔥 Dedicated Mixtral Q5",
            "model": "mixtral-dedicated-q5",
            "model_ram_gb": 77,
            "sleep_between_scripts": 0,
            "ollama_frequency": 1,
            "ollama_timeout": 1200,
            "scene_chunk_size": 50000,
            "num_predict": 2000,
            "num_ctx": 131072,  # 128K completo
            "num_thread": 24,
            "num_gpu": 60,  # TODOS os 60 cores
            "description": "Máxima potência Mixtral Q5 (77GB RAM, 80% CPU)"
        },

        "SMART_AUTO": {
            "name": "🧠 Smart Auto",
            "model": "auto",  # Escolhe baseado em métricas
            "model_ram_gb": 0,  # Calculado dinamicamente
            "sleep_between_scripts": 1.0,
            "ollama_frequency": 3,
            "ollama_timeout": 60,
            "scene_chunk_size": 2000,
            "num_predict": 100,
            "num_ctx": 65536,
            "num_thread": 16,
            "num_gpu": 40,
            "description": "Escolhe modelo baseado em recursos disponíveis"
        }
    }

    @classmethod
    def check_system_resources(cls) -> Dict[str, Any]:
        """Verifica recursos disponíveis do sistema"""

        resources = {
            "timestamp": time.time(),
            "hardware": cls.HARDWARE
        }

        # Verificar RAM disponível
        try:
            result = subprocess.run(
                ["vm_stat"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                # Parse vm_stat output
                lines = result.stdout.split('\n')
                for line in lines:
                    if "Pages free" in line:
                        pages_free = int(line.split(':')[1].strip().replace('.', ''))
                        # Cada página = 4KB
                        free_gb = (pages_free * 4096) / (1024**3)
                        resources["ram_free_gb"] = round(free_gb, 1)
                        break
        except:
            resources["ram_free_gb"] = 50  # Estimativa segura

        # Verificar modelos Ollama disponíveis
        try:
            result = subprocess.run(
                ["ollama", "list"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                resources["available_models"] = []
                lines = result.stdout.split('\n')[1:]  # Skip header
                for line in lines:
                    if line.strip():
                        model_name = line.split()[0]
                        if "deeplearning" in model_name or "mixtral" in model_name or "mixtral" in model_name:
                            resources["available_models"].append(model_name)
        except:
            resources["available_models"] = []

        # Verificar processos Ollama rodando
        try:
            result = subprocess.run(
                ["pgrep", "-f", "ollama"],
                capture_output=True,
                text=True,
                timeout=5
            )
            resources["ollama_running"] = result.returncode == 0
        except:
            resources["ollama_running"] = False

        return resources

    @classmethod
    def recommend_preset(cls) -> str:
        """Recomenda preset baseado em recursos"""

        resources = cls.check_system_resources()
        ram_free = resources.get("ram_free_gb", 50)
        models = resources.get("available_models", [])

        # Lógica de recomendação
        has_mixtral = any("mixtral" in m for m in models)
        has_32b = any("32b" in m or "hybrid" in m for m in models)

        if ram_free < 30:
            return "ECO_32B"
        elif ram_free < 50:
            if has_32b:
                return "BALANCED_32B"
            return "ECO_32B"
        elif ram_free < 70:
            if has_mixtral:
                return "ECO_mixtral"
            elif has_32b:
                return "TURBO_32B"
            return "BALANCED_32B"
        else:  # ram_free >= 70
            if has_mixtral:
                return "BALANCED_mixtral"
            return "TURBO_32B"

    @classmethod
    def get_current_config(cls) -> Dict[str, Any]:
        """Lê configuração atual"""
        if cls.CONFIG_FILE.exists():
            with open(cls.CONFIG_FILE, 'r') as f:
                config = json.load(f)
                # Adicionar info de hardware
                config["hardware"] = cls.HARDWARE
                return config

        # Default é ECO_32B
        return cls.PRESETS["ECO_32B"].copy()

    @classmethod
    def set_preset(cls, preset: str) -> Dict[str, Any]:
        """Define preset de potência"""

        preset = preset.upper()

        # Permitir shortcuts
        shortcuts = {
            "ECO": "ECO_32B",
            "BALANCED": "BALANCED_32B",
            "TURBO": "TURBO_32B",
            "mixtral": "BALANCED_mixtral",
            "MAX": "DEDICATED_mixtral",
            "AUTO": "SMART_AUTO"
        }

        if preset in shortcuts:
            preset = shortcuts[preset]

        if preset not in cls.PRESETS:
            raise ValueError(f"Preset inválido. Use: {list(cls.PRESETS.keys())}")

        config = cls.PRESETS[preset].copy()
        config["preset"] = preset
        config["timestamp"] = time.time()
        config["hardware"] = cls.HARDWARE

        # Se for SMART_AUTO, escolher modelo
        if preset == "SMART_AUTO":
            resources = cls.check_system_resources()
            recommended = cls.recommend_preset()
            actual_preset = cls.PRESETS[recommended]
            config["model"] = actual_preset["model"]
            config["model_ram_gb"] = actual_preset["model_ram_gb"]
            config["auto_selected"] = recommended

        # Salvar
        cls.CONFIG_FILE.parent.mkdir(exist_ok=True)
        with open(cls.CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=2)

        return config

    @classmethod
    def show_status(cls) -> None:
        """Mostra status atual com informações harmonizadas"""

        config = cls.get_current_config()
        resources = cls.check_system_resources()
        preset = config.get("preset", "ECO_32B")

        print("⚡ SISTEMA UNIFICADO DE POTÊNCIA - M3 ULTRA")
        print("=" * 60)

        print(f"\n💻 HARDWARE:")
        print(f"  • CPU: {cls.HARDWARE['cpu_cores']} cores")
        print(f"  • GPU: {cls.HARDWARE['gpu_cores']} cores")
        print(f"  • RAM: {cls.HARDWARE['ram_gb']} GB")
        print(f"  • Bandwidth: {cls.HARDWARE['bandwidth_gbps']} GB/s")

        print(f"\n📊 RECURSOS DISPONÍVEIS:")
        print(f"  • RAM livre: {resources.get('ram_free_gb', 'N/A')} GB")
        print(f"  • Ollama: {'✅ Rodando' if resources.get('ollama_running') else '❌ Parado'}")

        if resources.get("available_models"):
            print(f"  • Modelos disponíveis:")
            for model in resources["available_models"][:5]:
                print(f"    - {model}")

        print(f"\n🎯 PRESET ATUAL: {config.get('name', preset)}")

        if preset in cls.PRESETS:
            print(f"📝 {cls.PRESETS[preset]['description']}")

        if config.get("auto_selected"):
            print(f"  🧠 Auto-selecionado: {config['auto_selected']}")

        print(f"\n⚙️ CONFIGURAÇÕES:")
        print(f"  • Modelo: {config.get('model', 'N/A')}")
        print(f"  • RAM do modelo: {config.get('model_ram_gb', 0)} GB")
        print(f"  • Contexto: {config.get('num_ctx', 0):,} tokens")
        print(f"  • GPU cores usados: {config.get('num_gpu', 0)}/{cls.HARDWARE['gpu_cores']}")
        print(f"  • CPU threads: {config.get('num_thread', 0)}/{cls.HARDWARE['cpu_cores']}")
        print(f"  • Pausa entre scripts: {config.get('sleep_between_scripts', 0)}s")
        print(f"  • Frequência Ollama: 1/{config.get('ollama_frequency', 1)}")

        # Estimativas
        if config.get('sleep_between_scripts', 0) > 0:
            scripts_per_min = 60 / (config['sleep_between_scripts'] + 3)  # +3s processing
        else:
            scripts_per_min = 20  # Max estimate

        ollama_per_hour = (scripts_per_min * 60) / config.get('ollama_frequency', 1)

        print(f"\n📈 PERFORMANCE ESTIMADA:")
        print(f"  • Taxa: ~{scripts_per_min:.1f} roteiros/min")
        print(f"  • Ollama: ~{ollama_per_hour:.0f} chamadas/hora")

        # Recomendação
        recommended = cls.recommend_preset()
        if recommended != preset and preset != "SMART_AUTO":
            print(f"\n💡 RECOMENDAÇÃO:")
            print(f"  Com {resources.get('ram_free_gb', 50)} GB RAM livre,")
            print(f"  considere usar: {recommended}")

    @classmethod
    def validate_harmony(cls) -> Dict[str, bool]:
        """Valida harmonia total do sistema"""

        checks = {
            "config_exists": False,
            "models_available": False,
            "ollama_running": False,
            "ram_sufficient": False,
            "gpu_compatible": False,
            "power_profiles_valid": False
        }

        # 1. Verificar arquivo de config
        checks["config_exists"] = cls.CONFIG_FILE.exists()

        # 2. Verificar modelos
        resources = cls.check_system_resources()
        checks["models_available"] = len(resources.get("available_models", [])) > 0

        # 3. Verificar Ollama
        checks["ollama_running"] = resources.get("ollama_running", False)

        # 4. Verificar RAM
        config = cls.get_current_config()
        ram_needed = config.get("model_ram_gb", 25)
        ram_free = resources.get("ram_free_gb", 0)
        checks["ram_sufficient"] = ram_free > ram_needed + 10  # +10GB buffer

        # 5. Verificar GPU
        checks["gpu_compatible"] = cls.HARDWARE["gpu_cores"] >= 60

        # 6. Verificar profiles
        checks["power_profiles_valid"] = all(
            "model" in p and "num_gpu" in p
            for p in cls.PRESETS.values()
        )

        return checks


def main():
    """Interface CLI unificada"""
    import sys

    if len(sys.argv) < 2:
        UnifiedPowerSystem.show_status()
        print("\n💡 USO:")
        print("  python3 unified_power_system.py [preset|status|check|recommend]")
        print("\n📋 PRESETS DISPONÍVEIS:")
        print("  • eco_32b    - Mínimo recurso com 32B")
        print("  • balanced_32b - Equilibrado com 32B")
        print("  • turbo_32b  - Alta performance com 32B")
        print("  • eco_mixtral    - Econômico com mixtral")
        print("  • balanced_mixtral - Equilibrado com mixtral")
        print("  • dedicated_mixtral - Máximo com mixtral")
        print("  • auto       - Escolha inteligente")
        print("\nDIGIMUNDO PRESENTE 🥷")
        return

    command = sys.argv[1].lower()

    if command == "status":
        UnifiedPowerSystem.show_status()

    elif command == "check":
        print("🔍 VERIFICANDO HARMONIA DO SISTEMA...")
        print("=" * 60)
        checks = UnifiedPowerSystem.validate_harmony()

        all_good = True
        for check, result in checks.items():
            icon = "✅" if result else "❌"
            print(f"{icon} {check.replace('_', ' ').title()}: {result}")
            if not result:
                all_good = False

        print("\n" + "=" * 60)
        if all_good:
            print("✅ SISTEMA EM PERFEITA HARMONIA!")
        else:
            print("⚠️ Alguns componentes precisam atenção")

    elif command == "recommend":
        recommended = UnifiedPowerSystem.recommend_preset()
        resources = UnifiedPowerSystem.check_system_resources()

        print("🧠 RECOMENDAÇÃO INTELIGENTE")
        print("=" * 60)
        print(f"\nRAM livre: {resources.get('ram_free_gb', 'N/A')} GB")
        print(f"Modelos disponíveis: {len(resources.get('available_models', []))}")
        print(f"\n🎯 Preset recomendado: {recommended}")
        print(f"   {UnifiedPowerSystem.PRESETS[recommended]['description']}")

    else:
        # Assume que é um preset
        try:
            config = UnifiedPowerSystem.set_preset(command)
            print(f"✅ Potência ajustada para: {config['name']}")
            print(f"   Modelo: {config['model']}")
            print(f"   RAM: {config['model_ram_gb']} GB")
            print(f"   GPU: {config['num_gpu']}/{UnifiedPowerSystem.HARDWARE['gpu_cores']} cores")
        except ValueError as e:
            print(f"❌ Erro: {e}")

    print("\nDIGIMUNDO PRESENTE 🥷")


if __name__ == "__main__":
    main()