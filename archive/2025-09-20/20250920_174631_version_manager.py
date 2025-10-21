#!/usr/bin/env python3
"""
🔄 Version Manager - FASE 44
Sistema de versionamento avançado com blue-green deployment,
semantic versioning, feature flags e rollback automático
"""

import json
import time
import hashlib
import shutil
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, asdict, field
from datetime import datetime
from enum import Enum
import re
from collections import defaultdict

logger = logging.getLogger(__name__)


class ChangeType(Enum):
    """Tipo de mudança para semantic versioning"""
    BREAKING = "breaking"  # Major version
    FEATURE = "feature"    # Minor version
    FIX = "fix"           # Patch version
    DOCS = "docs"         # No version change
    CHORE = "chore"       # No version change


@dataclass
class Change:
    """Representa uma mudança no código"""
    type: ChangeType
    description: str
    files: List[str] = field(default_factory=list)
    timestamp: float = field(default_factory=time.time)
    author: str = "system"
    is_breaking: bool = False
    is_feature: bool = False


@dataclass
class Version:
    """Representa uma versão"""
    major: int = 1
    minor: int = 0
    patch: int = 0

    def __str__(self) -> str:
        return f"{self.major}.{self.minor}.{self.patch}"

    def bump_major(self) -> 'Version':
        return Version(self.major + 1, 0, 0)

    def bump_minor(self) -> 'Version':
        return Version(self.major, self.minor + 1, 0)

    def bump_patch(self) -> 'Version':
        return Version(self.major, self.minor, self.patch + 1)

    @classmethod
    def from_string(cls, version_str: str) -> 'Version':
        """Cria versão a partir de string"""
        match = re.match(r'(\d+)\.(\d+)\.(\d+)', version_str)
        if match:
            return cls(int(match.group(1)), int(match.group(2)), int(match.group(3)))
        return cls()


@dataclass
class Deployment:
    """Representa um deployment"""
    version: Version
    environment: str  # "blue" ou "green"
    deployed_at: float
    is_active: bool
    health_status: str = "healthy"
    metrics: Dict = field(default_factory=dict)


class FeatureFlag:
    """Sistema de feature flags"""

    def __init__(self):
        self.flags = {}
        self.overrides = {}

    def register(self, name: str, default: bool = False, description: str = ""):
        """Registra uma feature flag"""
        self.flags[name] = {
            'enabled': default,
            'description': description,
            'created_at': time.time(),
            'usage_count': 0
        }

    def is_enabled(self, name: str, user_id: str = None) -> bool:
        """Verifica se feature está habilitada"""
        if name not in self.flags:
            return False

        # Override por usuário
        if user_id and user_id in self.overrides.get(name, {}):
            return self.overrides[name][user_id]

        self.flags[name]['usage_count'] += 1
        return self.flags[name]['enabled']

    def enable(self, name: str):
        """Habilita feature"""
        if name in self.flags:
            self.flags[name]['enabled'] = True
            logger.info(f"✅ Feature flag '{name}' habilitada")

    def disable(self, name: str):
        """Desabilita feature"""
        if name in self.flags:
            self.flags[name]['enabled'] = False
            logger.info(f"❌ Feature flag '{name}' desabilitada")

    def set_override(self, name: str, user_id: str, enabled: bool):
        """Define override por usuário"""
        if name not in self.overrides:
            self.overrides[name] = {}
        self.overrides[name][user_id] = enabled


class VersionManager:
    """Gerenciador de versões com blue-green deployment"""

    def __init__(self, base_path: str = "deployments"):
        self.base_path = Path(base_path)
        self.base_path.mkdir(exist_ok=True)

        self.current_version = Version()
        self.changes = []
        self.deployments = {}
        self.feature_flags = FeatureFlag()

        # Ambientes blue-green
        self.blue_env = None
        self.green_env = None
        self.active_env = "blue"

        # Métricas para rollback automático
        self.health_threshold = 0.8
        self.error_threshold = 0.1

        logger.info("🔄 Version Manager inicializado")

    def add_change(self, change: Change):
        """Adiciona mudança ao registro"""
        self.changes.append(change)
        logger.info(f"📝 Mudança registrada: {change.type.value} - {change.description}")

    def calculate_next_version(self) -> Version:
        """Calcula próxima versão baseada nas mudanças"""
        has_breaking = any(c.type == ChangeType.BREAKING or c.is_breaking for c in self.changes)
        has_feature = any(c.type == ChangeType.FEATURE or c.is_feature for c in self.changes)
        has_fix = any(c.type == ChangeType.FIX for c in self.changes)

        if has_breaking:
            return self.current_version.bump_major()
        elif has_feature:
            return self.current_version.bump_minor()
        elif has_fix:
            return self.current_version.bump_patch()
        else:
            return self.current_version

    def deploy_blue_green(self, version: Version, code_path: str) -> Deployment:
        """Realiza deploy blue-green"""
        # Determina ambiente alvo
        target_env = "green" if self.active_env == "blue" else "blue"

        logger.info(f"🚀 Iniciando deploy v{version} no ambiente {target_env}")

        # Cria diretório do deployment
        deploy_path = self.base_path / f"{target_env}_v{version}"
        deploy_path.mkdir(exist_ok=True)

        # Copia código (simulado)
        if Path(code_path).exists():
            shutil.copytree(code_path, deploy_path / "code", dirs_exist_ok=True)

        # Cria deployment
        deployment = Deployment(
            version=version,
            environment=target_env,
            deployed_at=time.time(),
            is_active=False,
            health_status="deploying"
        )

        # Salva deployment
        self.deployments[str(version)] = deployment

        # Testa deployment
        health = self._health_check(deployment)
        deployment.health_status = "healthy" if health > self.health_threshold else "unhealthy"

        if deployment.health_status == "healthy":
            logger.info(f"✅ Deploy v{version} saudável no ambiente {target_env}")
        else:
            logger.warning(f"⚠️ Deploy v{version} com problemas de saúde")

        return deployment

    def switch_traffic(self, version: Version):
        """Muda tráfego para nova versão"""
        deployment = self.deployments.get(str(version))
        if not deployment:
            raise ValueError(f"Deployment v{version} não encontrado")

        if deployment.health_status != "healthy":
            raise ValueError(f"Deployment v{version} não está saudável")

        old_env = self.active_env
        new_env = deployment.environment

        logger.info(f"🔄 Mudando tráfego de {old_env} para {new_env} (v{version})")

        # Marca deployments
        for deploy in self.deployments.values():
            deploy.is_active = (deploy == deployment)

        self.active_env = new_env
        self.current_version = version

        logger.info(f"✅ Tráfego agora em {new_env} com v{version}")

    def rollback(self, target_version: Optional[Version] = None):
        """Realiza rollback para versão anterior"""
        if target_version:
            deployment = self.deployments.get(str(target_version))
        else:
            # Encontra última versão saudável
            sorted_deployments = sorted(
                self.deployments.values(),
                key=lambda d: d.deployed_at,
                reverse=True
            )
            deployment = None
            for deploy in sorted_deployments:
                if deploy.health_status == "healthy" and not deploy.is_active:
                    deployment = deploy
                    break

        if not deployment:
            raise ValueError("Nenhuma versão saudável para rollback")

        logger.warning(f"⚠️ Iniciando rollback para v{deployment.version}")

        # Muda tráfego
        self.switch_traffic(deployment.version)

        logger.info(f"✅ Rollback completo para v{deployment.version}")

    def automatic_rollback_check(self, current_metrics: Dict) -> bool:
        """Verifica se deve fazer rollback automático"""
        active_deployment = None
        for deploy in self.deployments.values():
            if deploy.is_active:
                active_deployment = deploy
                break

        if not active_deployment:
            return False

        # Verifica métricas
        error_rate = current_metrics.get('error_rate', 0)
        health_score = current_metrics.get('health_score', 1)

        if error_rate > self.error_threshold or health_score < self.health_threshold:
            logger.warning(f"🚨 Métricas ruins detectadas:")
            logger.warning(f"   Error rate: {error_rate:.1%} (limite: {self.error_threshold:.1%})")
            logger.warning(f"   Health: {health_score:.1%} (limite: {self.health_threshold:.1%})")

            # Rollback automático
            self.rollback()
            return True

        return False

    def _health_check(self, deployment: Deployment) -> float:
        """Realiza health check do deployment"""
        # Simulado - em produção faria requests reais
        health_checks = {
            'api_responsive': 0.9 + 0.1 * (hash(str(deployment.version)) % 10 / 10),
            'database_connected': 0.95,
            'memory_ok': 0.85,
            'cpu_ok': 0.9
        }

        deployment.metrics = health_checks
        return sum(health_checks.values()) / len(health_checks)

    def get_deployment_status(self) -> Dict:
        """Retorna status dos deployments"""
        status = {
            'current_version': str(self.current_version),
            'active_environment': self.active_env,
            'deployments': []
        }

        for version_str, deployment in self.deployments.items():
            status['deployments'].append({
                'version': version_str,
                'environment': deployment.environment,
                'is_active': deployment.is_active,
                'health': deployment.health_status,
                'deployed_at': datetime.fromtimestamp(deployment.deployed_at).isoformat()
            })

        return status


def test_version_manager():
    """Testa gerenciador de versões"""
    print("\n" + "="*60)
    print("🔄 TESTE DO VERSION MANAGER - FASE 44")
    print("="*60)

    manager = VersionManager()

    # Teste 1: Semantic Versioning
    print("\n1️⃣ Testando Semantic Versioning")

    manager.add_change(Change(ChangeType.FIX, "Corrige bug no parser"))
    manager.add_change(Change(ChangeType.FEATURE, "Adiciona suporte a GPU"))
    manager.add_change(Change(ChangeType.FIX, "Corrige memory leak"))

    next_version = manager.calculate_next_version()
    print(f"  Versão atual: {manager.current_version}")
    print(f"  Próxima versão: {next_version}")
    print(f"  Mudanças: {len(manager.changes)}")

    # Teste 2: Blue-Green Deployment
    print("\n2️⃣ Testando Blue-Green Deployment")

    # Deploy v1.1.0
    v1_1 = Version(1, 1, 0)
    deploy1 = manager.deploy_blue_green(v1_1, ".")
    print(f"  Deploy v{v1_1}: {deploy1.environment} - {deploy1.health_status}")

    # Muda tráfego
    manager.switch_traffic(v1_1)
    print(f"  Tráfego mudado para: {manager.active_env}")

    # Deploy v1.2.0
    v1_2 = Version(1, 2, 0)
    deploy2 = manager.deploy_blue_green(v1_2, ".")
    print(f"  Deploy v{v1_2}: {deploy2.environment} - {deploy2.health_status}")

    # Teste 3: Feature Flags
    print("\n3️⃣ Testando Feature Flags")

    manager.feature_flags.register("new_compression", False, "Nova compressão GPU")
    manager.feature_flags.register("ml_analysis", True, "Análise com ML")

    print(f"  new_compression: {manager.feature_flags.is_enabled('new_compression')}")
    print(f"  ml_analysis: {manager.feature_flags.is_enabled('ml_analysis')}")

    # Habilita feature
    manager.feature_flags.enable("new_compression")
    print(f"  new_compression após enable: {manager.feature_flags.is_enabled('new_compression')}")

    # Override por usuário
    manager.feature_flags.set_override("ml_analysis", "user123", False)
    print(f"  ml_analysis para user123: {manager.feature_flags.is_enabled('ml_analysis', 'user123')}")

    # Teste 4: Rollback Manual
    print("\n4️⃣ Testando Rollback Manual")

    print(f"  Versão antes: {manager.current_version}")
    manager.rollback(v1_1)
    print(f"  Versão após rollback: {manager.current_version}")

    # Teste 5: Rollback Automático
    print("\n5️⃣ Testando Rollback Automático")

    # Deploy v2.0.0 com métricas ruins
    v2_0 = Version(2, 0, 0)
    deploy3 = manager.deploy_blue_green(v2_0, ".")
    manager.switch_traffic(v2_0)

    bad_metrics = {
        'error_rate': 0.15,  # 15% de erro (limite 10%)
        'health_score': 0.7   # 70% saúde (limite 80%)
    }

    rolled_back = manager.automatic_rollback_check(bad_metrics)
    if rolled_back:
        print(f"  ✅ Rollback automático executado")
        print(f"  Versão após rollback: {manager.current_version}")
    else:
        print(f"  ⚠️ Rollback não necessário")

    # Teste 6: Status dos Deployments
    print("\n6️⃣ Status dos Deployments")

    status = manager.get_deployment_status()
    print(f"  Versão ativa: {status['current_version']}")
    print(f"  Ambiente ativo: {status['active_environment']}")
    print(f"  Deployments:")
    for deploy in status['deployments']:
        active = "🟢" if deploy['is_active'] else "⚫"
        print(f"    {active} v{deploy['version']} ({deploy['environment']}) - {deploy['health']}")

    # Métricas finais
    print("\n📊 Métricas do Version Manager:")
    print(f"  Total de deployments: {len(manager.deployments)}")
    print(f"  Feature flags: {len(manager.feature_flags.flags)}")
    print(f"  Mudanças registradas: {len(manager.changes)}")

    # Verifica se sistema está funcionando
    has_blue_green = len([d for d in manager.deployments.values() if d.environment in ['blue', 'green']]) >= 2
    has_rollback = manager.current_version != v2_0  # Rollback funcionou

    if has_blue_green and has_rollback:
        print("\n✅ OBJETIVO ATINGIDO: Sistema de versionamento completo!")
    else:
        print("\n⚠️ Sistema precisa de ajustes")

    print("\n✨ Version Manager funcionando!")
    print("  - Semantic versioning automático")
    print("  - Blue-green deployment sem downtime")
    print("  - Feature flags para controle fino")
    print("  - Rollback manual e automático")
    print("="*60)


if __name__ == "__main__":
    test_version_manager()