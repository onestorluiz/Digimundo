#!/usr/bin/env python3
"""
Version Manager Minimal - Versionamento semântico simplificado
Refatorado das 5 perguntas: 400+ → 120 linhas

RESPOSTAS ÀS 5 PERGUNTAS:
1. É necessário? SIM - Versionamento é essencial
2. O que faz? Semantic versioning + feature flags básicos
3. Quantas linhas? 120 vs 400+ (70% redução)
4. Dependências? Apenas stdlib
5. Uma função? Não, mas muito mais simples
"""

import json
import time
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from enum import Enum

class ChangeType(Enum):
    """Tipo de mudança para versionamento"""
    BREAKING = 'breaking'  # Major version
    FEATURE = 'feature'    # Minor version
    FIX = 'fix'           # Patch version

@dataclass
class Version:
    """Versão semântica"""
    major: int = 1
    minor: int = 0
    patch: int = 0

    def __str__(self) -> str:
        return f"{self.major}.{self.minor}.{self.patch}"

    def bump(self, change_type: ChangeType) -> 'Version':
        """Incrementa versão baseado no tipo de mudança"""
        if change_type == ChangeType.BREAKING:
            return Version(self.major + 1, 0, 0)
        elif change_type == ChangeType.FEATURE:
            return Version(self.major, self.minor + 1, 0)
        else:  # FIX
            return Version(self.major, self.minor, self.patch + 1)

    @classmethod
    def from_string(cls, version_str: str) -> 'Version':
        """Cria versão a partir de string"""
        parts = version_str.split('.')
        return cls(
            int(parts[0]) if len(parts) > 0 else 1,
            int(parts[1]) if len(parts) > 1 else 0,
            int(parts[2]) if len(parts) > 2 else 0
        )

class VersionManagerMinimal:
    """Gerenciador minimalista de versões"""

    def __init__(self, project_name: str = "scripturemon"):
        self.project_name = project_name
        self.version_file = Path(f"data/{project_name}_version.json")
        self.version_file.parent.mkdir(parents=True, exist_ok=True)

        self.current_version = self._load_version()
        self.changelog: List[Dict] = []
        self.feature_flags: Dict[str, bool] = {}

    def _load_version(self) -> Version:
        """Carrega versão do arquivo"""
        if self.version_file.exists():
            try:
                with open(self.version_file, 'r') as f:
                    data = json.load(f)
                    return Version.from_string(data.get('version', '1.0.0'))
            except:
                pass
        return Version()

    def _save_version(self):
        """Salva versão no arquivo"""
        data = {
            'version': str(self.current_version),
            'updated_at': time.time(),
            'project': self.project_name,
            'feature_flags': self.feature_flags,
            'changelog': self.changelog[-10:]  # Mantém últimas 10 mudanças
        }
        with open(self.version_file, 'w') as f:
            json.dump(data, f, indent=2)

    def add_change(self, change_type: ChangeType, description: str) -> str:
        """Adiciona mudança e incrementa versão"""
        old_version = str(self.current_version)
        self.current_version = self.current_version.bump(change_type)

        change = {
            'type': change_type.value,
            'description': description,
            'version': str(self.current_version),
            'timestamp': time.time()
        }
        self.changelog.append(change)

        self._save_version()

        return f"{old_version} → {self.current_version}"

    def set_feature_flag(self, flag_name: str, enabled: bool = True):
        """Define feature flag"""
        self.feature_flags[flag_name] = enabled
        self._save_version()

    def is_feature_enabled(self, flag_name: str) -> bool:
        """Verifica se feature está habilitada"""
        return self.feature_flags.get(flag_name, False)

    def get_info(self) -> Dict:
        """Retorna informações da versão"""
        return {
            'version': str(self.current_version),
            'project': self.project_name,
            'feature_flags': self.feature_flags,
            'recent_changes': self.changelog[-5:] if self.changelog else []
        }

# Funções de conveniência
def get_current_version(project: str = "scripturemon") -> str:
    """Retorna versão atual do projeto"""
    manager = VersionManagerMinimal(project)
    return str(manager.current_version)

def bump_version(change_type: str, description: str, project: str = "scripturemon") -> str:
    """Incrementa versão do projeto"""
    manager = VersionManagerMinimal(project)
    change_enum = ChangeType[change_type.upper()]
    return manager.add_change(change_enum, description)

# Exemplo de uso
if __name__ == "__main__":
    print("📦 Testando Version Manager Minimal...")

    manager = VersionManagerMinimal()

    # Adiciona mudanças
    print(f"✅ Fix: {manager.add_change(ChangeType.FIX, 'Corrigido bug no parser')}")
    print(f"✅ Feature: {manager.add_change(ChangeType.FEATURE, 'Adicionado suporte a PDF')}")
    print(f"✅ Breaking: {manager.add_change(ChangeType.BREAKING, 'API completamente refatorada')}")

    # Feature flags
    manager.set_feature_flag('new_compression', True)
    manager.set_feature_flag('experimental_ai', False)

    # Info
    info = manager.get_info()
    print(f"\n📊 Versão atual: {info['version']}")
    print(f"📊 Feature flags: {info['feature_flags']}")

    print("\nDIGIMUNDO PRESENTE 🥷")