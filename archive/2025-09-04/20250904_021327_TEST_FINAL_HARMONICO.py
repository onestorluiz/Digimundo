#!/usr/bin/env python3
"""
🎯 TESTE FINAL HARMÔNICO - VALIDAÇÃO COMPLETA DO SISTEMA
"""

import sys
import os
import json
import time
from datetime import datetime
from pathlib import Path

sys.path.insert(0, '.')

class TesteFinalHarmonico:
    def __init__(self):
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "tests_passed": 0,
            "tests_failed": 0,
            "modules_restored": 0,
            "systems_online": 0,
            "harmony_score": 0
        }
        
    def run_complete_test(self):
        print("\n" + "="*70)
        print("🎯 TESTE FINAL HARMÔNICO - SISTEMA SCRIPTUREMON")
        print("="*70)
        
        # 1. Verificar módulos restaurados
        print("\n📦 VERIFICANDO MÓDULOS RESTAURADOS...")
        self.check_restored_modules()
        
        # 2. Testar sistemas principais
        print("\n🔧 TESTANDO SISTEMAS PRINCIPAIS...")
        self.test_main_systems()
        
        # 3. Testar integração
        print("\n🔗 TESTANDO INTEGRAÇÃO...")
        self.test_integration()
        
        # 4. Calcular harmonia
        print("\n🎭 CALCULANDO HARMONIA...")
        self.calculate_harmony()
        
        # 5. Relatório final
        self.generate_report()
        
    def check_restored_modules(self):
        """Verifica todos os módulos restaurados"""
        modules_to_check = {
            'Análise Narrativa': [
                'beats_detect.py', 'pacing.py', 'themes.py', 'timeline.py',
                'scene_graph.py', 'character_graph.py', 'character_analytics.py', 'surgery.py'
            ],
            'Sistema de Comparação': [
                'compare_core.py', 'compare_batch.py', 'compare_memory.py',
                'compare_report.py', 'compare_search.py', 'compare_teach.py', 'compare_graft.py'
            ],
            'Visualização': [
                'charts_radar.py', 'charts_svg.py', 'heatmap_svg.py'
            ],
            'Exportação': [
                'export_html.py', 'export_md.py', 'export_md_short.py'
            ],
            'Auxiliares': [
                'mixer.py', 'notes_merge.py', 'doc_resolver.py', 'ref_manager.py',
                'evidence.py', 'citations.py', 'anchors.py', 'align_text.py'
            ]
        }
        
        total_found = 0
        total_expected = 0
        
        for category, modules in modules_to_check.items():
            found = 0
            print(f"\n  {category}:")
            for module in modules:
                path = Path(f"apps/scripturemon/{module}")
                total_expected += 1
                if path.exists():
                    found += 1
                    total_found += 1
                    print(f"    ✅ {module}")
                else:
                    print(f"    ❌ {module}")
            print(f"    [{found}/{len(modules)} encontrados]")
        
        self.results["modules_restored"] = total_found
        success_rate = (total_found / total_expected) * 100
        print(f"\n  📊 Taxa de restauração: {success_rate:.1f}%")
        
        if success_rate > 90:
            self.results["tests_passed"] += 1
        else:
            self.results["tests_failed"] += 1
            
    def test_main_systems(self):
        """Testa sistemas principais"""
        systems_to_test = [
            ("SCRIPTUREMON_ULTIMATE_SYMBIOTIC", "ScripturemonUltimateSymbiotic"),
            ("SYMBIOTIC_FUSION_ULTIMATE", "SymbioticFusion"),
            ("apps.scripturemon.chat", "ScripturemonChat"),
            ("apps.scripturemon.memory_unification", "get_unified_memory"),
            ("apps.scripturemon.telepathy_network", "TelepathicNetwork")
        ]
        
        systems_online = 0
        for module_name, class_name in systems_to_test:
            try:
                module = __import__(module_name, fromlist=[class_name])
                if hasattr(module, class_name):
                    systems_online += 1
                    print(f"  ✅ {module_name}")
                    self.results["tests_passed"] += 1
                else:
                    print(f"  ❌ {module_name}: classe não encontrada")
                    self.results["tests_failed"] += 1
            except Exception as e:
                print(f"  ❌ {module_name}: {str(e)[:50]}")
                self.results["tests_failed"] += 1
        
        self.results["systems_online"] = systems_online
        
    def test_integration(self):
        """Testa integração entre sistemas"""
        print("\n  Testando fluxo de dados...")
        
        try:
            # Teste simples de integração
            from apps.scripturemon.memory_unification import get_unified_memory
            mem = get_unified_memory()
            mem.store_unified_memory("teste_harmonico", source="test", memory_type="general")
            result = mem.retrieve_unified_memory("teste_harmonico", limit=1)
            
            if result:
                print("    ✅ Memória unificada funcionando")
                self.results["tests_passed"] += 1
            else:
                print("    ⚠️ Memória unificada vazia")
                
        except Exception as e:
            print(f"    ❌ Erro na integração: {str(e)[:50]}")
            self.results["tests_failed"] += 1
            
        # Verificar Redis
        try:
            import redis
            r = redis.Redis()
            r.ping()
            print("    ✅ Redis conectado")
            self.results["tests_passed"] += 1
        except:
            print("    ⚠️ Redis offline (modo fallback)")
            
        # Verificar Ollama
        try:
            import subprocess
            result = subprocess.run(['ollama', 'list'], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                models = len(result.stdout.strip().split('\n')) - 1
                print(f"    ✅ Ollama com {models} modelos")
                self.results["tests_passed"] += 1
            else:
                print("    ❌ Ollama não disponível")
                self.results["tests_failed"] += 1
        except:
            print("    ❌ Ollama não instalado")
            self.results["tests_failed"] += 1
            
    def calculate_harmony(self):
        """Calcula score de harmonia do sistema"""
        total_tests = self.results["tests_passed"] + self.results["tests_failed"]
        if total_tests == 0:
            self.results["harmony_score"] = 0
            return
            
        # Cálculo ponderado
        module_weight = 0.4  # 40% do peso para módulos restaurados
        system_weight = 0.4  # 40% do peso para sistemas online
        test_weight = 0.2    # 20% do peso para testes passados
        
        module_score = (self.results["modules_restored"] / 45) * 100 * module_weight
        system_score = (self.results["systems_online"] / 5) * 100 * system_weight
        test_score = (self.results["tests_passed"] / total_tests) * 100 * test_weight
        
        self.results["harmony_score"] = module_score + system_score + test_score
        
        print(f"\n  📊 Scores parciais:")
        print(f"    Módulos: {module_score/module_weight:.1f}%")
        print(f"    Sistemas: {system_score/system_weight:.1f}%")
        print(f"    Testes: {test_score/test_weight:.1f}%")
        
    def generate_report(self):
        """Gera relatório final"""
        print("\n" + "="*70)
        print("📊 RELATÓRIO FINAL")
        print("="*70)
        
        print(f"\n✅ Testes aprovados: {self.results['tests_passed']}")
        print(f"❌ Testes falhados: {self.results['tests_failed']}")
        print(f"📦 Módulos restaurados: {self.results['modules_restored']}/45")
        print(f"🔧 Sistemas online: {self.results['systems_online']}/5")
        print(f"\n🎭 HARMONIA DO SISTEMA: {self.results['harmony_score']:.1f}/100")
        
        # Salvar relatório
        report_file = Path("test_final_harmonico_report.json")
        with open(report_file, 'w') as f:
            json.dump(self.results, f, indent=2)
        print(f"\n💾 Relatório salvo em: {report_file}")
        
        # Veredicto final
        print("\n" + "="*70)
        if self.results["harmony_score"] >= 80:
            print("✅ SISTEMA EM HARMONIA PERFEITA!")
            print("   Todos os componentes principais funcionando")
            print("   Restauração bem-sucedida!")
        elif self.results["harmony_score"] >= 60:
            print("⚠️ SISTEMA FUNCIONAL COM PEQUENOS AJUSTES NECESSÁRIOS")
            print("   A maioria dos componentes funcionando")
        else:
            print("❌ SISTEMA PRECISA DE ATENÇÃO")
            print("   Alguns componentes críticos falhando")
        print("="*70)

if __name__ == "__main__":
    tester = TesteFinalHarmonico()
    tester.run_complete_test()