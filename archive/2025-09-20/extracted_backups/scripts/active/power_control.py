#!/usr/bin/env python3
"""
⚡ SISTEMA DE CONTROLE DE POTÊNCIA - MINIMALISTA E INTELIGENTE
Regula a velocidade de processamento do deep learning autônomo
"""

import json
from pathlib import Path
from typing import Dict, Any

class PowerControl:
    """Controle minimalista de potência do sistema"""

    # Arquivo de configuração
    CONFIG_FILE = Path(__file__).parent.parent.parent / "data" / "power_config.json"

    # Presets de potência
    PRESETS = {
        "ECO": {
            "name": "🌱 Econômico",
            "sleep_between_scripts": 2.0,      # Pausa entre roteiros
            "ollama_frequency": 5,             # Ollama a cada N roteiros
            "ollama_timeout": 20,               # Timeout em segundos
            "scene_chunk_size": 500,           # Caracteres processados
            "num_predict": 30,                 # Palavras de resposta
            "parallel_workers": 1,              # Threads paralelas
            "description": "Roda para sempre com mínimo recurso (0.1% CPU)"
        },
        "BALANCED": {
            "name": "⚖️ Balanceado",
            "sleep_between_scripts": 1.0,
            "ollama_frequency": 3,
            "ollama_timeout": 30,
            "scene_chunk_size": 1000,
            "num_predict": 50,
            "parallel_workers": 2,
            "description": "Equilibrio entre performance e recursos (5-10% CPU)"
        },
        "TURBO": {
            "name": "🚀 Turbo",
            "sleep_between_scripts": 0.5,
            "ollama_frequency": 2,
            "ollama_timeout": 45,
            "scene_chunk_size": 2000,
            "num_predict": 100,
            "parallel_workers": 4,
            "description": "Alta performance (20-40% CPU)"
        },
        "MAXIMUM": {
            "name": "🔥 Máximo",
            "sleep_between_scripts": 0,
            "ollama_frequency": 1,              # Ollama sempre
            "ollama_timeout": 60,
            "scene_chunk_size": 5000,
            "num_predict": 200,
            "parallel_workers": 8,
            "description": "Potência total sem limites (60-80% CPU)"
        },
        "CUSTOM": {
            "name": "⚙️ Customizado",
            "sleep_between_scripts": 1.0,
            "ollama_frequency": 3,
            "ollama_timeout": 30,
            "scene_chunk_size": 1000,
            "num_predict": 50,
            "parallel_workers": 2,
            "description": "Configure manualmente cada parâmetro"
        }
    }

    @classmethod
    def get_current_config(cls) -> Dict[str, Any]:
        """Lê configuração atual"""
        if cls.CONFIG_FILE.exists():
            with open(cls.CONFIG_FILE, 'r') as f:
                return json.load(f)
        # Default é ECO
        return cls.PRESETS["ECO"].copy()

    @classmethod
    def set_preset(cls, preset: str) -> Dict[str, Any]:
        """Define preset de potência"""
        if preset.upper() not in cls.PRESETS:
            raise ValueError(f"Preset inválido. Use: {list(cls.PRESETS.keys())}")

        config = cls.PRESETS[preset.upper()].copy()
        config["preset"] = preset.upper()
        config["timestamp"] = __import__("time").time()

        # Salvar
        cls.CONFIG_FILE.parent.mkdir(exist_ok=True)
        with open(cls.CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=2)

        return config

    @classmethod
    def set_custom(cls, **kwargs) -> Dict[str, Any]:
        """Define configuração customizada"""
        config = cls.get_current_config()

        # Atualizar apenas campos fornecidos
        for key, value in kwargs.items():
            if key in config:
                config[key] = value

        config["preset"] = "CUSTOM"
        config["timestamp"] = __import__("time").time()

        # Salvar
        with open(cls.CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=2)

        return config

    @classmethod
    def show_status(cls) -> None:
        """Mostra status atual"""
        config = cls.get_current_config()
        preset = config.get("preset", "ECO")

        print("⚡ CONTROLE DE POTÊNCIA - STATUS ATUAL")
        print("=" * 50)
        print(f"\n🎯 Preset: {cls.PRESETS[preset]['name']}")
        print(f"📝 {cls.PRESETS[preset]['description']}")
        print("\n⚙️ CONFIGURAÇÕES:")
        print(f"  • Pausa entre scripts: {config['sleep_between_scripts']}s")
        print(f"  • Frequência Ollama: 1/{config['ollama_frequency']}")
        print(f"  • Timeout Ollama: {config['ollama_timeout']}s")
        print(f"  • Tamanho da cena: {config['scene_chunk_size']} chars")
        print(f"  • Resposta Ollama: {config['num_predict']} palavras")
        print(f"  • Workers paralelos: {config['parallel_workers']}")

        # Estimativa de performance
        scripts_per_min = 60 / (config['sleep_between_scripts'] + 2)  # +2s de processamento médio
        ollama_per_hour = (scripts_per_min * 60) / config['ollama_frequency']

        print(f"\n📊 ESTIMATIVAS:")
        print(f"  • Taxa: ~{scripts_per_min:.1f} roteiros/min")
        print(f"  • Ollama: ~{ollama_per_hour:.0f} chamadas/hora")

        # Estimativa de recursos
        if preset == "ECO":
            cpu = "0.1-1%"
            mem = "0.1-0.2%"
        elif preset == "BALANCED":
            cpu = "5-10%"
            mem = "0.2-0.5%"
        elif preset == "TURBO":
            cpu = "20-40%"
            mem = "0.5-1%"
        elif preset == "MAXIMUM":
            cpu = "60-80%"
            mem = "1-2%"
        else:  # CUSTOM
            cpu = "Variável"
            mem = "Variável"

        print(f"  • CPU esperado: {cpu}")
        print(f"  • RAM esperada: {mem}")


def main():
    """Interface CLI para controle de potência"""
    import sys

    if len(sys.argv) < 2:
        PowerControl.show_status()
        print("\n💡 USO:")
        print("  python3 power_control.py [eco|balanced|turbo|maximum]")
        print("  python3 power_control.py custom --sleep=1.0 --ollama=3")
        print("\nDIGIMUNDO PRESENTE 🥷")
        return

    command = sys.argv[1].lower()

    if command in ["eco", "balanced", "turbo", "maximum"]:
        config = PowerControl.set_preset(command)
        print(f"✅ Potência ajustada para: {PowerControl.PRESETS[command.upper()]['name']}")
        PowerControl.show_status()

    elif command == "custom":
        # Parse argumentos custom
        kwargs = {}
        for arg in sys.argv[2:]:
            if arg.startswith("--"):
                key, value = arg[2:].split("=")
                if key == "sleep":
                    kwargs["sleep_between_scripts"] = float(value)
                elif key == "ollama":
                    kwargs["ollama_frequency"] = int(value)
                elif key == "timeout":
                    kwargs["ollama_timeout"] = int(value)
                elif key == "chunk":
                    kwargs["scene_chunk_size"] = int(value)
                elif key == "predict":
                    kwargs["num_predict"] = int(value)
                elif key == "workers":
                    kwargs["parallel_workers"] = int(value)

        if kwargs:
            config = PowerControl.set_custom(**kwargs)
            print("✅ Configuração customizada aplicada")
            PowerControl.show_status()
        else:
            print("❌ Nenhum parâmetro customizado fornecido")

    else:
        PowerControl.show_status()

    print("\nDIGIMUNDO PRESENTE 🥷")


if __name__ == "__main__":
    main()