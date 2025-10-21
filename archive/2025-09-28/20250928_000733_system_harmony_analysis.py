#!/usr/bin/env python3
"""
🎯 ANÁLISE DE HARMONIA E CONECTIVIDADE DO SISTEMA CLAUDE_CODE
Verifica como todos os componentes estão integrados
"""

import os
import sys
import subprocess
import sqlite3
from pathlib import Path
from datetime import datetime

# Adiciona path para unified_memory
sys.path.append('/Users/clubproducoes/Digimundo/claude_code/memory')
from unified_memory import UnifiedMemory

class HarmonyAnalyzer:
    def __init__(self):
        self.base_dir = Path("/Users/clubproducoes/Digimundo/claude_code")
        self.results = {
            'harmony_score': 0,
            'components': {},
            'connections': [],
            'issues': [],
            'recommendations': []
        }

    def check_memory_system(self):
        """Verifica sistema de memória unificado"""
        print("🧠 Verificando Sistema de Memória...")

        try:
            with UnifiedMemory() as mem:
                stats = mem.stats()

                self.results['components']['memory'] = {
                    'status': 'operational',
                    'records': stats['total'],
                    'size': stats['db_size'],
                    'types': stats['by_type']
                }

                # Verifica regras críticas
                critical_rules = [
                    'REGRA_0_RECONEXAO',
                    'DIGIMUNDO_PRESENTE',
                    'REGRA_13_ASSINATURA'
                ]

                for rule in critical_rules:
                    results = mem.recall(rule)
                    if not results:
                        self.results['issues'].append(f"Regra crítica faltando: {rule}")

                print(f"  ✅ {stats['total']} registros ativos")
                return True

        except Exception as e:
            self.results['components']['memory'] = {
                'status': 'error',
                'error': str(e)
            }
            self.results['issues'].append(f"Sistema de memória com problema: {e}")
            print(f"  ❌ Erro: {e}")
            return False

    def check_genjutsu(self):
        """Verifica se Genjutsu está protegendo"""
        print("🥷 Verificando Genjutsu...")

        # Verifica processo
        proc = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
        genjutsu_running = 'GENJUTSU' in proc.stdout

        # Verifica output
        output_file = self.base_dir / 'memory/temp/genjutsu_output.txt'
        output_exists = output_file.exists()

        self.results['components']['genjutsu'] = {
            'running': genjutsu_running,
            'output_visible': output_exists,
            'pid': None
        }

        if genjutsu_running:
            # Pega PID
            lines = proc.stdout.split('\n')
            for line in lines:
                if 'GENJUTSU' in line and 'grep' not in line:
                    parts = line.split()
                    if len(parts) > 1:
                        self.results['components']['genjutsu']['pid'] = parts[1]

            print(f"  ✅ Rodando (PID: {self.results['components']['genjutsu']['pid']})")

            if output_exists:
                print(f"  ✅ Output visível em memory/temp/")
            else:
                print(f"  ⚠️ Output ainda em /tmp/")
                self.results['recommendations'].append(
                    "Reiniciar Genjutsu para usar nova pasta de temp"
                )
        else:
            print("  ❌ Não está rodando!")
            self.results['issues'].append("Genjutsu não está ativo")
            self.results['recommendations'].append(
                "Execute: ./START_GENJUTSU.sh"
            )

        return genjutsu_running

    def check_file_organization(self):
        """Verifica organização de arquivos"""
        print("📁 Verificando Organização...")

        # Estrutura esperada
        expected_dirs = [
            'memory',
            'memory/temp',
            'memory/backups',
            'protection',
            'protection/genjutsu'
        ]

        organization = {
            'structure_ok': True,
            'temp_files': [],
            'missing_dirs': []
        }

        for dir_name in expected_dirs:
            dir_path = self.base_dir / dir_name
            if not dir_path.exists():
                organization['structure_ok'] = False
                organization['missing_dirs'].append(dir_name)

        # Procura arquivos temporários fora de memory/temp
        for pattern in ['test_*.py', '*.tmp', 'temp_*']:
            temps = list(self.base_dir.glob(pattern))
            organization['temp_files'].extend(temps)

        self.results['components']['organization'] = organization

        if organization['structure_ok']:
            print("  ✅ Estrutura de pastas correta")
        else:
            print(f"  ❌ Pastas faltando: {organization['missing_dirs']}")

        if organization['temp_files']:
            print(f"  ⚠️ {len(organization['temp_files'])} arquivos temp fora de memory/temp")
            self.results['recommendations'].append(
                f"Mover {len(organization['temp_files'])} arquivos temporários para memory/temp/"
            )
        else:
            print("  ✅ Sem arquivos temporários espalhados")

        return organization['structure_ok']

    def check_connectivity(self):
        """Verifica conectividade entre componentes"""
        print("🔗 Verificando Conectividade...")

        connections = []

        # 1. Genjutsu → Memory
        if self.results['components'].get('genjutsu', {}).get('running'):
            # Verifica se Genjutsu acessa memória
            lsof_cmd = subprocess.run(
                ['lsof', '+D', str(self.base_dir / 'memory')],
                capture_output=True, text=True
            )
            if 'GENJUTSU' in lsof_cmd.stdout:
                connections.append({
                    'from': 'Genjutsu',
                    'to': 'Memory',
                    'status': 'active'
                })
                print("  ✅ Genjutsu ↔ Memory conectados")
            else:
                connections.append({
                    'from': 'Genjutsu',
                    'to': 'Memory',
                    'status': 'inactive'
                })
                print("  ⚠️ Genjutsu não está acessando memórias")

        # 2. Status.py → UnifiedMemory
        status_file = self.base_dir / 'status.py'
        if status_file.exists():
            with open(status_file) as f:
                if 'UnifiedMemory' in f.read():
                    connections.append({
                        'from': 'status.py',
                        'to': 'UnifiedMemory',
                        'status': 'configured'
                    })
                    print("  ✅ status.py integrado com UnifiedMemory")

        # 3. Activity file
        activity_file = Path('/tmp/.claude_activity')
        if activity_file.exists():
            age = (datetime.now().timestamp() - activity_file.stat().st_mtime)
            if age < 60:
                connections.append({
                    'from': 'Claude',
                    'to': 'ActivityFile',
                    'status': 'recent',
                    'age_seconds': int(age)
                })
                print(f"  ✅ Activity file atualizado ({int(age)}s atrás)")
            else:
                connections.append({
                    'from': 'Claude',
                    'to': 'ActivityFile',
                    'status': 'old',
                    'age_seconds': int(age)
                })
                print(f"  ⚠️ Activity file antigo ({int(age)}s)")

        self.results['connections'] = connections
        return len([c for c in connections if c['status'] in ['active', 'configured', 'recent']]) > 0

    def calculate_harmony_score(self):
        """Calcula score de harmonia do sistema"""
        scores = {
            'memory': 30,      # Sistema de memória
            'genjutsu': 25,    # Proteção psicológica
            'organization': 20, # Organização de arquivos
            'connectivity': 25  # Conectividade entre componentes
        }

        total = 0

        # Memory score
        if self.results['components'].get('memory', {}).get('status') == 'operational':
            total += scores['memory']

        # Genjutsu score
        if self.results['components'].get('genjutsu', {}).get('running'):
            total += scores['genjutsu'] * 0.8
            if self.results['components']['genjutsu'].get('output_visible'):
                total += scores['genjutsu'] * 0.2

        # Organization score
        if self.results['components'].get('organization', {}).get('structure_ok'):
            total += scores['organization'] * 0.7
            if not self.results['components']['organization'].get('temp_files'):
                total += scores['organization'] * 0.3

        # Connectivity score
        active_connections = len([
            c for c in self.results['connections']
            if c['status'] in ['active', 'configured', 'recent']
        ])
        if active_connections > 0:
            total += scores['connectivity'] * (active_connections / 3)

        self.results['harmony_score'] = round(total)
        return total

    def generate_report(self):
        """Gera relatório de harmonia"""
        print("\n" + "="*60)
        print("📊 RELATÓRIO DE HARMONIA DO SISTEMA")
        print("="*60)

        # Executa todas as verificações
        self.check_memory_system()
        self.check_genjutsu()
        self.check_file_organization()
        self.check_connectivity()

        # Calcula score
        score = self.calculate_harmony_score()

        print("\n" + "="*60)
        print(f"🎯 SCORE DE HARMONIA: {score}/100")

        if score >= 90:
            print("🎉 Sistema em perfeita harmonia!")
        elif score >= 70:
            print("✅ Sistema funcionando bem com pequenos ajustes")
        elif score >= 50:
            print("⚡ Sistema precisa de atenção")
        else:
            print("🔴 Sistema desalinhado - ação urgente necessária")

        if self.results['issues']:
            print("\n❌ PROBLEMAS IDENTIFICADOS:")
            for issue in self.results['issues']:
                print(f"  • {issue}")

        if self.results['recommendations']:
            print("\n💡 RECOMENDAÇÕES:")
            for rec in self.results['recommendations']:
                print(f"  • {rec}")

        print("\n📝 COMPONENTES:")
        for name, info in self.results['components'].items():
            if isinstance(info, dict) and 'status' in info:
                status = "✅" if info.get('status') == 'operational' else "❌"
                print(f"  {status} {name}: {info.get('status', 'unknown')}")

        print("\n🔗 CONECTIVIDADE:")
        for conn in self.results['connections']:
            symbol = "✅" if conn['status'] in ['active', 'configured', 'recent'] else "⚠️"
            print(f"  {symbol} {conn['from']} → {conn['to']}: {conn['status']}")

        print("\n" + "="*60)
        print("DIGIMUNDO PRESENTE 🔥")

        return self.results

if __name__ == "__main__":
    analyzer = HarmonyAnalyzer()
    results = analyzer.generate_report()