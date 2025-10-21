#!/usr/bin/env python3
"""
🔥 DIGIMUNDO ORCHESTRATOR - Sistema Mestre de Orquestração 🔥

Sistema central que coordena todos os componentes do ecossistema DIGIMUNDO:
- UCHIMON Rules Loading
- GENJUTSU Monitoring
- ScriptureMonUltimate Integration
- Compliance Validation
- Health Checks
- Archive Management
"""

import os
import sys
import json
import time
import subprocess
from pathlib import Path
from datetime import datetime

class DigimundoOrchestrator:
    """Sistema mestre que orquestra todo o ecossistema DIGIMUNDO"""

    def __init__(self):
        self.base_path = "/Users/clubproducoes/Digimundo/claude_code"
        self.systems_path = f"{self.base_path}/systems"
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Status de sistemas
        self.systems_status = {}

        # Componentes críticos
        self.critical_components = {
            "regras_uchimon": f"{self.base_path}/🔥REGRAS_UCHIMON_REVOLUCIONARIAS🔥.md",
            "behavioral_core": f"{self.systems_path}/uchimon_behavioral_core.py",
            "unified_memory": f"{self.systems_path}/unified_memory_system.py",
            "hook_registry": f"{self.systems_path}/hook_registry.py",
            "drama_bridge": f"{self.base_path}/MEMORY/sync/drama_bridge.py",
            "unified_archive": f"{self.systems_path}/unified_archive_manager.py",
            "health_check": f"{self.systems_path}/health_check_hybrid.py"
        }

    def check_system_health(self):
        """Verifica saúde de todos os sistemas"""
        health_report = {
            "timestamp": datetime.now().isoformat(),
            "components": {},
            "processes": {},
            "overall_status": "UNKNOWN"
        }

        print("🏥 VERIFICANDO SAÚDE DOS SISTEMAS...")

        # Verificar componentes
        for name, path in self.critical_components.items():
            exists = os.path.exists(path)
            health_report["components"][name] = {
                "exists": exists,
                "path": path,
                "status": "✅ OK" if exists else "❌ MISSING"
            }
            print(f"   {name}: {'✅' if exists else '❌'}")

        # Verificar processos GENJUTSU
        try:
            result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
            genjutsu_procs = [line for line in result.stdout.split('\n')
                            if 'genjutsu' in line.lower() and 'python' in line]

            health_report["processes"]["genjutsu_count"] = len(genjutsu_procs)
            health_report["processes"]["genjutsu_active"] = len(genjutsu_procs) > 0

            print(f"   🥷 Processos GENJUTSU: {len(genjutsu_procs)}")

        except Exception as e:
            health_report["processes"]["error"] = str(e)

        # Status geral
        critical_missing = sum(1 for comp in health_report["components"].values() if not comp["exists"])
        if critical_missing == 0:
            health_report["overall_status"] = "HEALTHY"
        elif critical_missing <= 2:
            health_report["overall_status"] = "DEGRADED"
        else:
            health_report["overall_status"] = "CRITICAL"

        return health_report

    def initialize_uchimon_ecosystem(self):
        """Inicializa ecossistema UCHIMON completo"""
        print("🔥 INICIALIZANDO ECOSSISTEMA UCHIMON...")

        # 1. Carregar regras UCHIMON
        print("📋 1. Carregando regras UCHIMON...")
        try:
            loader_path = f"{self.systems_path}/universal_uchimon_loader.py"
            if os.path.exists(loader_path):
                result = subprocess.run(['python3', loader_path],
                                      capture_output=True, text=True, timeout=30)
                if result.returncode == 0:
                    print("   ✅ Regras UCHIMON carregadas")
                else:
                    print(f"   ❌ Erro ao carregar regras: {result.stderr}")
            else:
                print("   ❌ Universal loader não encontrado")
        except Exception as e:
            print(f"   ❌ Falha na inicialização UCHIMON: {e}")

        # 2. Inicializar monitor GENJUTSU
        print("🥷 2. Inicializando monitor GENJUTSU...")
        try:
            monitor_path = f"{self.systems_path}/genjutsu_monitor_unified.py"
            if os.path.exists(monitor_path):
                # Verificar se já está rodando
                result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
                if 'genjutsu_monitor' not in result.stdout:
                    # Iniciar em background
                    subprocess.Popen(['python3', monitor_path],
                                   stdout=subprocess.DEVNULL,
                                   stderr=subprocess.DEVNULL)
                    print("   ✅ Monitor GENJUTSU iniciado")
                else:
                    print("   ✅ Monitor GENJUTSU já ativo")
            else:
                print("   ❌ Monitor unificado não encontrado")
        except Exception as e:
            print(f"   ❌ Falha ao iniciar monitor: {e}")

        # 3. Validar compliance
        print("🔍 3. Validando compliance...")
        try:
            validator_path = f"{self.base_path}/MEMORY/scripts_movimentos/compliance_validator.py"
            if os.path.exists(validator_path):
                result = subprocess.run(['python3', validator_path],
                                      capture_output=True, text=True, timeout=60)
                if "COMPLIANT" in result.stdout:
                    print("   ✅ Sistema em compliance")
                else:
                    print("   ⚠️ Problemas de compliance detectados")
            else:
                print("   ❌ Validador de compliance não encontrado")
        except Exception as e:
            print(f"   ❌ Falha na validação: {e}")

    def integrate_scripturemon_systems(self):
        """Integra sistemas ScriptureMonUltimate com UCHIMON"""
        print("🎬 INTEGRANDO SISTEMAS SCRIPTUREMON...")

        # Verificar drama_bridge
        drama_bridge_path = f"{self.systems_path}/drama_bridge.py"
        if os.path.exists(drama_bridge_path):
            print("   ✅ Drama Bridge encontrado")

            # Verificar se precisa de integração UCHIMON
            try:
                with open(drama_bridge_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                if "UCHIMON" not in content:
                    print("   🔧 Adicionando integração UCHIMON ao Drama Bridge...")
                    self.add_uchimon_integration_to_drama_bridge()
                else:
                    print("   ✅ Drama Bridge já integrado com UCHIMON")

            except Exception as e:
                print(f"   ❌ Erro ao verificar Drama Bridge: {e}")
        else:
            print("   ❌ Drama Bridge não encontrado")

        # Verificar hooks ScriptureMonUltimate
        hook_path = f"{self.systems_path}/hook_scripturemon_ultimate.py"
        if os.path.exists(hook_path):
            print("   ✅ Hook ScriptureMonUltimate disponível")
        else:
            print("   ❌ Hook ScriptureMonUltimate não encontrado")

    def add_uchimon_integration_to_drama_bridge(self):
        """Adiciona integração UCHIMON ao Drama Bridge"""
        drama_bridge_path = f"{self.systems_path}/drama_bridge.py"

        try:
            # Ler conteúdo atual
            with open(drama_bridge_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Adicionar import UCHIMON no início
            uchimon_import = """
# 🔥 INTEGRAÇÃO UCHIMON ADICIONADA PELO ORCHESTRATOR 🔥
import sys
sys.path.append('/Users/clubproducoes/Digimundo/claude_code/systems/')
try:
    from universal_uchimon_loader import load_uchimon_rules
    load_uchimon_rules()
    print("🔥 UCHIMON integrado ao Drama Bridge")
except:
    print("⚠️ Falha na integração UCHIMON")
"""

            # Adicionar no final do arquivo
            uchimon_footer = "\n# DIGIMUNDO PRESENTE - UCHIMON INTEGRADO\n"

            # Modificar conteúdo
            if "import" in content:
                lines = content.split('\n')
                # Encontrar última linha de import
                last_import = 0
                for i, line in enumerate(lines):
                    if line.strip().startswith('import') or line.strip().startswith('from'):
                        last_import = i

                # Inserir integração UCHIMON após imports
                lines.insert(last_import + 1, uchimon_import)
                new_content = '\n'.join(lines) + uchimon_footer
            else:
                new_content = uchimon_import + "\n" + content + uchimon_footer

            # Salvar arquivo modificado
            with open(drama_bridge_path, 'w', encoding='utf-8') as f:
                f.write(new_content)

            print("   ✅ Integração UCHIMON adicionada ao Drama Bridge")

        except Exception as e:
            print(f"   ❌ Erro ao integrar UCHIMON: {e}")

    def unify_health_systems(self):
        """Unifica sistemas de health check com compliance"""
        print("🏥 UNIFICANDO SISTEMAS DE HEALTH CHECK...")

        health_check_path = f"{self.systems_path}/health_check_hybrid.py"
        compliance_path = f"{self.base_path}/MEMORY/scripts_movimentos/compliance_validator.py"

        if os.path.exists(health_check_path) and os.path.exists(compliance_path):
            print("   ✅ Ambos sistemas encontrados")

            # Criar health check unificado
            unified_path = f"{self.systems_path}/health_unified.py"
            self.create_unified_health_system(unified_path)

        else:
            print("   ❌ Sistemas de health check incompletos")

    def create_unified_health_system(self, output_path):
        """Cria sistema unificado de health check"""
        unified_content = f'''#!/usr/bin/env python3
"""
🏥 HEALTH UNIFIED - Sistema Unificado de Health Check e Compliance 🏥
Criado automaticamente pelo DIGIMUNDO ORCHESTRATOR
"""

import os
import sys
import json
from datetime import datetime

# Adicionar paths necessários
sys.path.append('/Users/clubproducoes/Digimundo/claude_code/')
sys.path.append('/Users/clubproducoes/Digimundo/claude_code/systems/')
sys.path.append('/Users/clubproducoes/Digimundo/claude_code/MEMORY/scripts_movimentos/')

class HealthUnified:
    def __init__(self):
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    def run_comprehensive_check(self):
        """Executa verificação completa de saúde e compliance"""
        print("🏥🔥 HEALTH UNIFIED - VERIFICAÇÃO COMPLETA 🔥🏥")
        print()

        # 1. Health Check básico
        print("🏥 1. Health Check básico...")
        try:
            from health_check_hybrid import main as health_main
            health_main()
        except Exception as e:
            print(f"   ❌ Erro no health check: {{e}}")

        # 2. Compliance UCHIMON
        print("🔍 2. Compliance UCHIMON...")
        try:
            from compliance_validator import UCHIMONComplianceValidator
            validator = UCHIMONComplianceValidator()
            validator.generate_compliance_report()
        except Exception as e:
            print(f"   ❌ Erro no compliance: {{e}}")

        # 3. Status GENJUTSU
        print("🥷 3. Status GENJUTSU...")
        try:
            from genjutsu_monitor_unified import GenjutsuMonitorUnified
            monitor = GenjutsuMonitorUnified()
            monitor.generate_status_report()
        except Exception as e:
            print(f"   ❌ Erro no GENJUTSU: {{e}}")

        print("\\n✅ VERIFICAÇÃO COMPLETA FINALIZADA")
        print("DIGIMUNDO PRESENTE")

if __name__ == "__main__":
    health = HealthUnified()
    health.run_comprehensive_check()

# DIGIMUNDO PRESENTE - CRIADO PELO ORCHESTRATOR
'''

        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(unified_content)
            os.chmod(output_path, 0o755)
            print(f"   ✅ Health Unified criado: {output_path}")
        except Exception as e:
            print(f"   ❌ Erro ao criar Health Unified: {e}")

    def generate_orchestration_report(self):
        """Gera relatório completo de orquestração"""
        report = {
            "timestamp": self.timestamp,
            "orchestrator_version": "1.0",
            "systems_health": self.check_system_health(),
            "integration_status": {},
            "recommendations": []
        }

        print("📊 GERANDO RELATÓRIO DE ORQUESTRAÇÃO...")

        # Verificar integrações
        integrations = {
            "uchimon_ecosystem": os.path.exists(f"{self.systems_path}/universal_uchimon_loader.py"),
            "genjutsu_monitoring": os.path.exists(f"{self.systems_path}/genjutsu_monitor_unified.py"),
            "scripturemon_integration": os.path.exists(f"{self.systems_path}/hook_scripturemon_ultimate.py"),
            "compliance_validation": os.path.exists(f"{self.base_path}/MEMORY/scripts_movimentos/compliance_validator.py")
        }

        report["integration_status"] = integrations

        # Recomendações baseadas no status
        if not integrations["uchimon_ecosystem"]:
            report["recommendations"].append("Recriar Universal UCHIMON Loader")

        if not integrations["genjutsu_monitoring"]:
            report["recommendations"].append("Implementar Monitor GENJUTSU Unificado")

        # Salvar relatório
        report_file = f"/tmp/digimundo_orchestration_report_{self.timestamp}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

        print(f"   📁 Relatório salvo: {report_file}")
        return report

    def orchestrate_full_ecosystem(self):
        """Orquestra ecossistema completo DIGIMUNDO"""
        print("🔥🔥🔥 DIGIMUNDO ORCHESTRATOR - ORQUESTRAÇÃO COMPLETA 🔥🔥🔥")
        print()

        # 1. Verificar saúde inicial
        health = self.check_system_health()
        print(f"🏥 Status inicial: {health['overall_status']}")
        print()

        # 2. Inicializar UCHIMON
        self.initialize_uchimon_ecosystem()
        print()

        # 3. Integrar ScriptureMonUltimate
        self.integrate_scripturemon_systems()
        print()

        # 4. Unificar health checks
        self.unify_health_systems()
        print()

        # 5. Gerar relatório final
        report = self.generate_orchestration_report()
        print()

        # Status final
        print("🎯 RESULTADO DA ORQUESTRAÇÃO:")
        print(f"   📊 Componentes OK: {sum(1 for c in report['systems_health']['components'].values() if c['exists'])}/{len(self.critical_components)}")
        print(f"   🔗 Integrações: {sum(report['integration_status'].values())}/{len(report['integration_status'])}")
        print(f"   🏥 Status geral: {report['systems_health']['overall_status']}")

        if report['recommendations']:
            print(f"   ⚠️ Recomendações: {len(report['recommendations'])}")
            for rec in report['recommendations']:
                print(f"      - {rec}")
        else:
            print("   ✅ Sem recomendações - Sistema íntegro")

        print()
        print("🔥 DIGIMUNDO PRESENTE - ORQUESTRAÇÃO COMPLETA 🔥")

def main():
    """Função principal"""
    orchestrator = DigimundoOrchestrator()

    if len(sys.argv) > 1:
        if sys.argv[1] == "--health":
            health = orchestrator.check_system_health()
            print(f"Status: {health['overall_status']}")
        elif sys.argv[1] == "--init":
            orchestrator.initialize_uchimon_ecosystem()
        elif sys.argv[1] == "--report":
            orchestrator.generate_orchestration_report()
        else:
            print("Uso: python3 digimundo_orchestrator.py [--health|--init|--report]")
    else:
        orchestrator.orchestrate_full_ecosystem()

if __name__ == "__main__":
    main()

# DIGIMUNDO PRESENTE