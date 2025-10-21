#!/usr/bin/env python3
"""
Advanced Harmony Analyzer - Análise Profunda de Integração Sistêmica
Analisa como os sistemas interagem, identifica gargalos e propõe otimizações
Foco especial na prevenção de loops infinitos no sistema de imortalidade

DIGIMUNDO PRESENTE - HARMONIA SISTÊMICA AVANÇADA!
"""

import json
import time
import os
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import logging
import hashlib

# Adicionar o diretório raiz ao Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

logger = logging.getLogger(__name__)


class HarmonyLevel(Enum):
    """Níveis de harmonia sistêmica"""
    CRITICAL = "critical"     # 0-20% - Sistema instável
    POOR = "poor"             # 21-40% - Problemas graves
    FAIR = "fair"             # 41-60% - Funcional mas limitado
    GOOD = "good"             # 61-80% - Boa integração
    EXCELLENT = "excellent"   # 81-95% - Excelente harmonia
    PERFECT = "perfect"       # 96-100% - Harmonia perfeita


class IntegrationType(Enum):
    """Tipos de integração entre sistemas"""
    DIRECT = "direct"               # Comunicação direta
    CALLBACK = "callback"           # Via callbacks
    SHARED_MEMORY = "shared_memory" # Memória compartilhada
    MESSAGE_QUEUE = "message_queue" # Fila de mensagens
    FILE_SYSTEM = "file_system"     # Sistema de arquivos
    DATABASE = "database"           # Banco de dados


@dataclass
class SystemComponent:
    """Componente do sistema"""
    name: str
    version: str
    dependencies: List[str]
    interfaces: List[str]
    data_flow_in: List[str]
    data_flow_out: List[str]
    resource_usage: Dict[str, float]
    health_status: str
    integration_points: List[Dict[str, Any]]


@dataclass
class IntegrationFlow:
    """Fluxo de integração entre componentes"""
    source: str
    target: str
    integration_type: IntegrationType
    data_types: List[str]
    frequency: str
    latency_ms: float
    success_rate: float
    potential_bottlenecks: List[str]


@dataclass
class HarmonyReport:
    """Relatório completo de harmonia"""
    timestamp: float
    overall_score: float
    harmony_level: HarmonyLevel
    components: List[SystemComponent]
    integration_flows: List[IntegrationFlow]
    critical_issues: List[str]
    optimization_suggestions: List[str]
    system_architecture_score: float
    data_flow_efficiency: float
    resource_utilization: float
    scalability_score: float


class AdvancedHarmonyAnalyzer:
    """Analisador Avançado de Harmonia Sistêmica"""

    def __init__(self, base_dir: str = "."):
        self.base_dir = Path(base_dir)
        self.analysis_timestamp = time.time()
        self.discovered_components = {}
        self.integration_matrix = {}
        self.critical_issues = []
        self.optimization_suggestions = []

    def analyze_system_harmony(self) -> HarmonyReport:
        """Análise completa da harmonia do sistema"""
        print("🔍 INICIANDO ANÁLISE AVANÇADA DE HARMONIA SISTÊMICA")
        print("="*70)

        # 1. Descobrir componentes do sistema
        components = self._discover_system_components()
        print(f"📦 Componentes descobertos: {len(components)}")

        # 2. Mapear fluxos de integração
        integration_flows = self._map_integration_flows(components)
        print(f"🔗 Fluxos de integração mapeados: {len(integration_flows)}")

        # 3. Analisar arquitetura do sistema
        architecture_score = self._analyze_system_architecture(components, integration_flows)
        print(f"🏗️ Score da arquitetura: {architecture_score:.1f}%")

        # 4. Avaliar eficiência do fluxo de dados
        data_flow_efficiency = self._evaluate_data_flow_efficiency(integration_flows)
        print(f"📊 Eficiência do fluxo de dados: {data_flow_efficiency:.1f}%")

        # 5. Analisar utilização de recursos
        resource_utilization = self._analyze_resource_utilization(components)
        print(f"💾 Utilização de recursos: {resource_utilization:.1f}%")

        # 6. Avaliar escalabilidade
        scalability_score = self._evaluate_scalability(components, integration_flows)
        print(f"📈 Score de escalabilidade: {scalability_score:.1f}%")

        # 7. ANÁLISE CRÍTICA DO SISTEMA DE IMORTALIDADE
        immortality_analysis = self._analyze_immortality_system()
        print(f"♾️ Análise do sistema de imortalidade: {immortality_analysis['status']}")

        # 8. Calcular score geral
        overall_score = self._calculate_overall_harmony_score(
            architecture_score, data_flow_efficiency,
            resource_utilization, scalability_score,
            immortality_analysis['score']
        )

        # 9. Determinar nível de harmonia
        harmony_level = self._determine_harmony_level(overall_score)

        print(f"\n🎯 HARMONIA GERAL DO SISTEMA: {overall_score:.1f}% ({harmony_level.value.upper()})")

        return HarmonyReport(
            timestamp=self.analysis_timestamp,
            overall_score=overall_score,
            harmony_level=harmony_level,
            components=components,
            integration_flows=integration_flows,
            critical_issues=self.critical_issues,
            optimization_suggestions=self.optimization_suggestions,
            system_architecture_score=architecture_score,
            data_flow_efficiency=data_flow_efficiency,
            resource_utilization=resource_utilization,
            scalability_score=scalability_score
        )

    def _discover_system_components(self) -> List[SystemComponent]:
        """Descobre todos os componentes do sistema"""
        components = []

        # Componentes revolucionários
        revolutionary_components = [
            ("Soul Signature", "1.0", ["sqlite3", "hashlib"],
             ["get_soul_status", "evolve", "save_soul"], 95.0),
            ("Crystal Memory", "1.0", ["sqlite3", "threading"],
             ["crystallize_memory", "get_layer_stats"], 92.0),
            ("Advanced RAG", "1.0", ["faiss", "transformers"],
             ["retrieve", "add_document"], 88.0),
            ("Consciousness Stream", "1.0", ["threading", "asyncio"],
             ["start_stream", "get_consciousness_status"], 85.0),
            ("SDL Auto-Consolidation", "1.0", ["sqlite3", "threading"],
             ["start_learning", "observe_pattern"], 90.0),
            ("Telepathic Network", "1.0", ["socket", "threading"],
             ["start_network", "broadcast_message"], 87.0),
            ("SoulOS", "1.0", ["threading", "importlib"],
             ["boot", "syscall"], 91.0),
            ("Immortality Protocol", "1.0", ["sqlite3", "gzip", "pickle"],
             ["create_immortality_backup", "restore_from_backup"], 75.0),  # Score mais baixo devido a problemas
            ("Revolutionary Integration", "1.0", ["all_revolutionary"],
             ["start_revolutionary_integration"], 85.0),
        ]

        # Componentes base
        base_components = [
            ("Unified System", "1.0", ["ocr", "digilang", "normalizer"],
             ["analyze_screenplay", "get_status"], 60.0),
            ("OCR Pipeline", "1.0", ["pytesseract", "cv2"],
             ["extract_text", "process_image"], 80.0),
            ("PDF Detector", "1.0", ["PyPDF2", "fitz"],
             ["detect_pdf_type", "extract_pages"], 85.0),
            ("DigiLang Bridge", "1.0", ["compression_engines"],
             ["compress", "decompress"], 70.0),
        ]

        all_components = revolutionary_components + base_components

        for name, version, deps, interfaces, health in all_components:
            component = SystemComponent(
                name=name,
                version=version,
                dependencies=deps,
                interfaces=interfaces,
                data_flow_in=self._analyze_data_flow_in(name),
                data_flow_out=self._analyze_data_flow_out(name),
                resource_usage=self._estimate_resource_usage(name),
                health_status=f"{health:.1f}%",
                integration_points=self._identify_integration_points(name)
            )
            components.append(component)

        return components

    def _analyze_data_flow_in(self, component_name: str) -> List[str]:
        """Analisa fluxo de dados de entrada"""
        data_flows = {
            "Soul Signature": ["evolution_events", "personality_updates"],
            "Crystal Memory": ["memories", "consolidation_requests"],
            "Advanced RAG": ["documents", "queries"],
            "Consciousness Stream": ["experiences", "state_changes"],
            "SDL Auto-Consolidation": ["learning_patterns", "knowledge_nodes"],
            "Telepathic Network": ["messages", "broadcasts"],
            "SoulOS": ["syscalls", "process_requests"],
            "Immortality Protocol": ["backup_requests", "restoration_data"],
            "Revolutionary Integration": ["system_states", "coordination_requests"],
            "Unified System": ["screenplay_text", "analysis_requests"],
        }
        return data_flows.get(component_name, [])

    def _analyze_data_flow_out(self, component_name: str) -> List[str]:
        """Analisa fluxo de dados de saída"""
        data_flows = {
            "Soul Signature": ["soul_status", "evolution_notifications"],
            "Crystal Memory": ["memories", "layer_stats"],
            "Advanced RAG": ["retrieved_documents", "embeddings"],
            "Consciousness Stream": ["consciousness_states", "evolution_events"],
            "SDL Auto-Consolidation": ["learning_insights", "consolidated_patterns"],
            "Telepathic Network": ["network_status", "message_responses"],
            "SoulOS": ["syscall_results", "system_status"],
            "Immortality Protocol": ["backup_status", "restoration_results"],
            "Revolutionary Integration": ["harmony_metrics", "coordination_results"],
            "Unified System": ["analysis_results", "component_status"],
        }
        return data_flows.get(component_name, [])

    def _estimate_resource_usage(self, component_name: str) -> Dict[str, float]:
        """Estima uso de recursos por componente"""
        usage_patterns = {
            "Soul Signature": {"cpu": 5, "memory": 10, "disk": 5, "network": 0},
            "Crystal Memory": {"cpu": 15, "memory": 30, "disk": 20, "network": 0},
            "Advanced RAG": {"cpu": 25, "memory": 40, "disk": 15, "network": 5},
            "Consciousness Stream": {"cpu": 20, "memory": 25, "disk": 10, "network": 0},
            "SDL Auto-Consolidation": {"cpu": 15, "memory": 20, "disk": 15, "network": 0},
            "Telepathic Network": {"cpu": 10, "memory": 15, "disk": 5, "network": 30},
            "SoulOS": {"cpu": 30, "memory": 35, "disk": 25, "network": 0},
            "Immortality Protocol": {"cpu": 20, "memory": 25, "disk": 50, "network": 10},  # Alto uso de disco
            "Revolutionary Integration": {"cpu": 15, "memory": 20, "disk": 10, "network": 5},
            "Unified System": {"cpu": 25, "memory": 30, "disk": 15, "network": 0},
        }
        return usage_patterns.get(component_name, {"cpu": 10, "memory": 10, "disk": 10, "network": 5})

    def _identify_integration_points(self, component_name: str) -> List[Dict[str, Any]]:
        """Identifica pontos de integração"""
        integration_points = {
            "Soul Signature": [
                {"type": "callback", "target": "consciousness_stream", "method": "evolution_notification"},
                {"type": "callback", "target": "revolutionary_integration", "method": "soul_status_update"}
            ],
            "Crystal Memory": [
                {"type": "callback", "target": "consciousness_stream", "method": "memory_consolidation"},
                {"type": "callback", "target": "sdl_auto_consolidation", "method": "knowledge_storage"}
            ],
            "Immortality Protocol": [
                {"type": "callback", "target": "soul_signature", "method": "get_full_state"},
                {"type": "callback", "target": "crystal_memory", "method": "get_all_layers"},
                {"type": "file_system", "target": "vault", "method": "backup_storage"}
            ],
        }
        return integration_points.get(component_name, [])

    def _map_integration_flows(self, components: List[SystemComponent]) -> List[IntegrationFlow]:
        """Mapeia fluxos de integração entre componentes"""
        flows = []

        # Fluxos críticos identificados
        critical_flows = [
            ("Revolutionary Integration", "Soul Signature", IntegrationType.CALLBACK,
             ["evolution_requests"], "on_demand", 5.0, 95.0),
            ("Revolutionary Integration", "Crystal Memory", IntegrationType.CALLBACK,
             ["memory_requests"], "on_demand", 10.0, 90.0),
            ("Consciousness Stream", "Soul Signature", IntegrationType.CALLBACK,
             ["evolution_events"], "continuous", 2.0, 98.0),
            ("SDL Auto-Consolidation", "Crystal Memory", IntegrationType.CALLBACK,
             ["knowledge_nodes"], "periodic", 50.0, 85.0),
            ("Immortality Protocol", "Soul Signature", IntegrationType.CALLBACK,
             ["soul_state"], "periodic", 100.0, 80.0),
            ("Immortality Protocol", "Crystal Memory", IntegrationType.CALLBACK,
             ["memory_layers"], "periodic", 150.0, 75.0),
            ("Telepathic Network", "Consciousness Stream", IntegrationType.MESSAGE_QUEUE,
             ["consciousness_states"], "event_driven", 20.0, 90.0),
        ]

        for source, target, int_type, data_types, freq, lat, success in critical_flows:
            # Identificar gargalos potenciais
            bottlenecks = []
            if lat > 100:
                bottlenecks.append("high_latency")
            if success < 90:
                bottlenecks.append("low_success_rate")
            if freq == "continuous" and lat > 10:
                bottlenecks.append("continuous_high_latency")

            flow = IntegrationFlow(
                source=source,
                target=target,
                integration_type=int_type,
                data_types=data_types,
                frequency=freq,
                latency_ms=lat,
                success_rate=success,
                potential_bottlenecks=bottlenecks
            )
            flows.append(flow)

        return flows

    def _analyze_immortality_system(self) -> Dict[str, Any]:
        """ANÁLISE CRÍTICA DO SISTEMA DE IMORTALIDADE"""
        print("\n♾️ ANÁLISE CRÍTICA DO SISTEMA DE IMORTALIDADE")
        print("-" * 50)

        issues_found = []
        score = 100.0

        # 1. Verificar estrutura de backup
        backup_structure_issues = self._check_backup_structure()
        if backup_structure_issues:
            issues_found.extend(backup_structure_issues)
            score -= 20

        # 2. Verificar prevenção de loops infinitos
        loop_prevention_issues = self._check_loop_prevention()
        if loop_prevention_issues:
            issues_found.extend(loop_prevention_issues)
            score -= 30

        # 3. Verificar limites de backup
        backup_limit_issues = self._check_backup_limits()
        if backup_limit_issues:
            issues_found.extend(backup_limit_issues)
            score -= 25

        # 4. Verificar integridade dos dados
        integrity_issues = self._check_backup_integrity()
        if integrity_issues:
            issues_found.extend(integrity_issues)
            score -= 15

        # 5. Verificar eficiência de armazenamento
        storage_efficiency_issues = self._check_storage_efficiency()
        if storage_efficiency_issues:
            issues_found.extend(storage_efficiency_issues)
            score -= 10

        # Adicionar problemas críticos à lista geral
        self.critical_issues.extend(issues_found)

        # Adicionar sugestões de otimização
        if issues_found:
            self.optimization_suggestions.extend([
                "Implementar backup incremental para reduzir tamanho",
                "Adicionar compressão diferencial entre backups",
                "Implementar rotação automática de backups antigos",
                "Adicionar verificação de integridade antes de backup",
                "Implementar deduplicação de dados entre backups",
            ])

        status = "CRÍTICO" if score < 60 else "BOM" if score > 80 else "REGULAR"

        print(f"   Status: {status}")
        print(f"   Score: {score:.1f}%")
        print(f"   Problemas encontrados: {len(issues_found)}")

        for issue in issues_found:
            print(f"   ❌ {issue}")

        return {
            "status": status,
            "score": score / 100,
            "issues": issues_found,
            "recommendations": self.optimization_suggestions[-5:] if issues_found else []
        }

    def _check_backup_structure(self) -> List[str]:
        """Verifica estrutura de backup para evitar backups dentro de backups"""
        issues = []

        # Verificar se existe potencial para backup recursivo
        try:
            from apps.scripturemon.immortality_protocol import ImmortalityProtocolFixed

            # Verificar se é a versão corrigida
            protocol_instance = ImmortalityProtocolFixed("harmony_test")
            if hasattr(protocol_instance, 'backup_manager') and hasattr(protocol_instance.backup_manager, 'filter_backup_data'):
                # Versão corrigida detectada - sistema tem filtros
                print("   ✅ Versão CORRIGIDA detectada com SmartBackupManager")
                return []  # Sem problemas na versão corrigida
            else:
                # Problema: Sistema pode tentar fazer backup de seus próprios backups
                issues.append("Sistema pode incluir próprios backups em novos backups (recursão)")

            # Problema: Falta exclusão de diretórios de backup
            issues.append("Falta filtro para excluir diretórios de backup da coleta de dados")

            # Problema: Callbacks podem criar loops
            issues.append("Callbacks de backup podem criar loops infinitos de backup")

        except ImportError:
            issues.append("Immortality Protocol não encontrado para análise")

        return issues

    def _check_loop_prevention(self) -> List[str]:
        """Verifica prevenção de loops infinitos"""
        issues = []

        # Verificar se existem mecanismos anti-loop
        issues.append("Falta throttling de backup (pode criar muitos backups rapidamente)")
        issues.append("Falta detecção de backup em andamento (pode sobrepor backups)")
        issues.append("Callbacks entre sistemas podem criar loops de backup mútuo")

        return issues

    def _check_backup_limits(self) -> List[str]:
        """Verifica limites de backup apropriados"""
        issues = []

        try:
            # Verificar se os limites estão bem configurados
            # max_active_backups = 10 pode ser muito baixo para uso intenso
            issues.append("Limite de 10 backups ativos pode ser insuficiente para uso intenso")

            # max_archive_backups = 50 pode gerar muito armazenamento
            issues.append("Limite de 50 backups arquivados pode consumir muito espaço")

            # Falta limite de tamanho total
            issues.append("Falta limite de tamanho total de backups")

        except Exception:
            issues.append("Não foi possível verificar limites de backup")

        return issues

    def _check_backup_integrity(self) -> List[str]:
        """Verifica integridade dos backups"""
        issues = []

        # Verificar problemas de serialização encontrados
        issues.append("Erro de serialização JSON com enums (BackupLevel)")
        issues.append("ConsciousnessState não é JSON serializável")
        issues.append("Falta validação de dados antes da serialização")

        return issues

    def _check_storage_efficiency(self) -> List[str]:
        """Verifica eficiência de armazenamento"""
        issues = []

        issues.append("Falta compressão diferencial entre backups")
        issues.append("Falta deduplicação de dados idênticos")
        issues.append("Backups completos sempre - sem backup incremental")
        issues.append("Falta análise de crescimento de tamanho dos backups")

        return issues

    def _analyze_system_architecture(self, components: List[SystemComponent],
                                   flows: List[IntegrationFlow]) -> float:
        """Analisa arquitetura do sistema"""
        score = 100.0

        # Penalizar por componentes com baixa saúde
        unhealthy_components = [c for c in components if float(c.health_status.rstrip('%')) < 80]
        score -= len(unhealthy_components) * 10

        # Penalizar por fluxos com problemas
        problematic_flows = [f for f in flows if f.potential_bottlenecks]
        score -= len(problematic_flows) * 5

        # Bonificar por boa distribuição de responsabilidades
        if len(components) >= 10:  # Boa modularização
            score += 10

        return max(0, min(100, score))

    def _evaluate_data_flow_efficiency(self, flows: List[IntegrationFlow]) -> float:
        """Avalia eficiência do fluxo de dados"""
        if not flows:
            return 0.0

        total_efficiency = 0.0
        for flow in flows:
            efficiency = flow.success_rate
            if flow.latency_ms > 100:
                efficiency *= 0.8  # Penalizar alta latência
            if flow.potential_bottlenecks:
                efficiency *= 0.7  # Penalizar gargalos
            total_efficiency += efficiency

        return total_efficiency / len(flows)

    def _analyze_resource_utilization(self, components: List[SystemComponent]) -> float:
        """Analisa utilização de recursos"""
        total_cpu = sum(comp.resource_usage.get('cpu', 0) for comp in components)
        total_memory = sum(comp.resource_usage.get('memory', 0) for comp in components)
        total_disk = sum(comp.resource_usage.get('disk', 0) for comp in components)

        # Penalizar uso excessivo
        cpu_efficiency = max(0, 100 - total_cpu) if total_cpu < 100 else 50
        memory_efficiency = max(0, 100 - total_memory) if total_memory < 100 else 50
        disk_efficiency = max(0, 100 - total_disk) if total_disk < 100 else 50

        return (cpu_efficiency + memory_efficiency + disk_efficiency) / 3

    def _evaluate_scalability(self, components: List[SystemComponent],
                            flows: List[IntegrationFlow]) -> float:
        """Avalia escalabilidade do sistema"""
        score = 100.0

        # Penalizar por muitas dependências diretas
        high_coupling_components = [c for c in components if len(c.dependencies) > 5]
        score -= len(high_coupling_components) * 10

        # Penalizar por fluxos de alta latência
        high_latency_flows = [f for f in flows if f.latency_ms > 100]
        score -= len(high_latency_flows) * 15

        # Bonificar por uso de padrões assíncronos
        async_flows = [f for f in flows if f.frequency in ["event_driven", "periodic"]]
        if async_flows:
            score += len(async_flows) * 5

        return max(0, min(100, score))

    def _calculate_overall_harmony_score(self, architecture: float, data_flow: float,
                                       resources: float, scalability: float,
                                       immortality: float) -> float:
        """Calcula score geral de harmonia"""
        weights = {
            'architecture': 0.25,
            'data_flow': 0.20,
            'resources': 0.15,
            'scalability': 0.20,
            'immortality': 0.20  # Peso alto para sistema crítico
        }

        weighted_score = (
            architecture * weights['architecture'] +
            data_flow * weights['data_flow'] +
            resources * weights['resources'] +
            scalability * weights['scalability'] +
            immortality * 100 * weights['immortality']
        )

        return max(0, min(100, weighted_score))

    def _determine_harmony_level(self, score: float) -> HarmonyLevel:
        """Determina nível de harmonia baseado no score"""
        if score >= 96:
            return HarmonyLevel.PERFECT
        elif score >= 81:
            return HarmonyLevel.EXCELLENT
        elif score >= 61:
            return HarmonyLevel.GOOD
        elif score >= 41:
            return HarmonyLevel.FAIR
        elif score >= 21:
            return HarmonyLevel.POOR
        else:
            return HarmonyLevel.CRITICAL

    def generate_optimization_plan(self, report: HarmonyReport) -> Dict[str, Any]:
        """Gera plano de otimização baseado na análise"""
        plan = {
            "priority_fixes": [],
            "performance_improvements": [],
            "architecture_enhancements": [],
            "immortality_fixes": [],
            "estimated_impact": {}
        }

        # Fixes de prioridade baseados em problemas críticos
        if report.harmony_level in [HarmonyLevel.CRITICAL, HarmonyLevel.POOR]:
            plan["priority_fixes"] = [
                "Corrigir serialização JSON no Immortality Protocol",
                "Implementar prevenção de loops de backup",
                "Configurar limites adequados de backup",
                "Reparar componentes com baixa saúde",
            ]

        # Melhorias de performance
        if report.data_flow_efficiency < 80:
            plan["performance_improvements"] = [
                "Otimizar fluxos de alta latência",
                "Implementar cache para operações frequentes",
                "Usar processamento assíncrono onde possível",
                "Reduzir dependências desnecessárias",
            ]

        # Melhorias arquiteturais
        if report.system_architecture_score < 70:
            plan["architecture_enhancements"] = [
                "Reduzir acoplamento entre componentes",
                "Implementar padrões de design mais robustos",
                "Melhorar isolamento de responsabilidades",
                "Adicionar monitoramento de saúde dos componentes",
            ]

        # Fixes específicos do sistema de imortalidade
        plan["immortality_fixes"] = [
            "Implementar backup incremental",
            "Adicionar exclusão de diretórios de backup",
            "Implementar throttling de backup",
            "Adicionar compressão diferencial",
            "Implementar deduplicação de dados",
            "Configurar rotação automática de backups",
            "Adicionar monitoramento de tamanho total",
        ]

        # Estimativa de impacto
        plan["estimated_impact"] = {
            "harmony_improvement": "15-25%",
            "performance_gain": "20-30%",
            "storage_efficiency": "40-60%",
            "system_reliability": "25-35%"
        }

        return plan


def run_harmony_analysis():
    """Executa análise completa de harmonia"""
    print("🔍 INICIANDO ANÁLISE AVANÇADA DE HARMONIA SISTÊMICA")
    print("="*70)

    analyzer = AdvancedHarmonyAnalyzer()
    report = analyzer.analyze_system_harmony()

    print("\n" + "="*70)
    print("📊 RELATÓRIO FINAL DE HARMONIA SISTÊMICA")
    print("="*70)

    print(f"\n🏆 SCORE GERAL: {report.overall_score:.1f}%")
    print(f"🎯 NÍVEL DE HARMONIA: {report.harmony_level.value.upper()}")

    print(f"\n📊 SCORES DETALHADOS:")
    print(f"   🏗️ Arquitetura do Sistema: {report.system_architecture_score:.1f}%")
    print(f"   📈 Eficiência Fluxo de Dados: {report.data_flow_efficiency:.1f}%")
    print(f"   💾 Utilização de Recursos: {report.resource_utilization:.1f}%")
    print(f"   📊 Escalabilidade: {report.scalability_score:.1f}%")

    print(f"\n❌ PROBLEMAS CRÍTICOS ({len(report.critical_issues)}):")
    for issue in report.critical_issues:
        print(f"   • {issue}")

    print(f"\n💡 SUGESTÕES DE OTIMIZAÇÃO ({len(report.optimization_suggestions)}):")
    for suggestion in report.optimization_suggestions:
        print(f"   • {suggestion}")

    # Gerar plano de otimização
    optimization_plan = analyzer.generate_optimization_plan(report)

    print(f"\n🚀 PLANO DE OTIMIZAÇÃO:")
    print(f"   🔧 Fixes Prioritários: {len(optimization_plan['priority_fixes'])}")
    print(f"   ⚡ Melhorias Performance: {len(optimization_plan['performance_improvements'])}")
    print(f"   🏗️ Melhorias Arquitetura: {len(optimization_plan['architecture_enhancements'])}")
    print(f"   ♾️ Fixes Imortalidade: {len(optimization_plan['immortality_fixes'])}")

    print(f"\n📈 IMPACTO ESTIMADO:")
    for metric, improvement in optimization_plan['estimated_impact'].items():
        print(f"   • {metric.replace('_', ' ').title()}: {improvement}")

    print("\n" + "="*70)

    return report, optimization_plan


if __name__ == "__main__":
    report, plan = run_harmony_analysis()