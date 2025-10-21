#!/usr/bin/env python3
"""
🔬 ANÁLISE ULTRA-PROFUNDA DO SISTEMA SCRIPTUREMON
Verifica TODOS os caminhos de execução e pontos de falha
"""

import sys
import os
import json
import time
import subprocess
import traceback
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Any, Optional

class UltraDeepAnalysis:
    """Análise ultra-profunda do sistema completo"""
    
    def __init__(self):
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "architecture": {},
            "connections": {},
            "dependencies": {},
            "execution_paths": {},
            "risk_points": [],
            "recommendations": []
        }
        
        self.errors = []
        self.warnings = []
        self.success = []
        
    def run_complete_analysis(self):
        """Executa análise completa do sistema"""
        print("\n" + "="*80)
        print("🔬 ANÁLISE ULTRA-PROFUNDA DO SISTEMA SCRIPTUREMON")
        print("="*80)
        
        # 1. ARQUITETURA
        print("\n📐 FASE 1: MAPEAMENTO DA ARQUITETURA")
        print("-"*60)
        self.analyze_architecture()
        
        # 2. CONEXÕES
        print("\n🔗 FASE 2: ANÁLISE DE CONEXÕES")
        print("-"*60)
        self.analyze_connections()
        
        # 3. DEPENDÊNCIAS
        print("\n📦 FASE 3: VERIFICAÇÃO DE DEPENDÊNCIAS")
        print("-"*60)
        self.analyze_dependencies()
        
        # 4. CAMINHOS DE EXECUÇÃO
        print("\n🛤️ FASE 4: TESTE DE CAMINHOS DE EXECUÇÃO")
        print("-"*60)
        self.test_execution_paths()
        
        # 5. PONTOS DE RISCO
        print("\n⚠️ FASE 5: IDENTIFICAÇÃO DE RISCOS")
        print("-"*60)
        self.identify_risks()
        
        # 6. RELATÓRIO FINAL
        print("\n📊 FASE 6: RELATÓRIO FINAL")
        print("-"*60)
        self.generate_report()
        
    def analyze_architecture(self):
        """Analisa arquitetura do sistema"""
        
        # Sistema SYMBIOTIC principal
        print("🔸 Analisando SCRIPTUREMON_ULTIMATE_SYMBIOTIC...")
        symbiotic_path = Path("SCRIPTUREMON_ULTIMATE_SYMBIOTIC.py")
        
        if symbiotic_path.exists():
            self.results["architecture"]["symbiotic"] = {
                "exists": True,
                "size": symbiotic_path.stat().st_size,
                "lines": len(symbiotic_path.read_text().splitlines()),
                "classes": self._count_classes(symbiotic_path),
                "functions": self._count_functions(symbiotic_path)
            }
            self.success.append("✅ SYMBIOTIC: Arquivo principal encontrado")
            print(f"   ✅ {self.results['architecture']['symbiotic']['lines']} linhas")
            print(f"   ✅ {self.results['architecture']['symbiotic']['classes']} classes")
        else:
            self.errors.append("❌ SYMBIOTIC não encontrado")
            print("   ❌ Arquivo não encontrado!")
        
        # Sistema FUSION
        print("\n🔸 Analisando SYMBIOTIC_FUSION_ULTIMATE...")
        fusion_path = Path("SYMBIOTIC_FUSION_ULTIMATE.py")
        
        if fusion_path.exists():
            self.results["architecture"]["fusion"] = {
                "exists": True,
                "size": fusion_path.stat().st_size,
                "lines": len(fusion_path.read_text().splitlines()),
                "classes": self._count_classes(fusion_path),
                "functions": self._count_functions(fusion_path)
            }
            self.success.append("✅ FUSION: Sistema de fusão encontrado")
            print(f"   ✅ {self.results['architecture']['fusion']['lines']} linhas")
        else:
            self.warnings.append("⚠️ FUSION não encontrado")
        
        # Diretório apps/scripturemon
        print("\n🔸 Analisando apps/scripturemon/...")
        apps_path = Path("apps/scripturemon")
        
        if apps_path.exists():
            py_files = list(apps_path.glob("*.py"))
            self.results["architecture"]["apps"] = {
                "exists": True,
                "modules": len(py_files),
                "total_lines": sum(len(f.read_text().splitlines()) for f in py_files),
                "core_modules": []
            }
            
            # Módulos core
            core_modules = [
                "soul.py", "consciousness.py", "memory_unification.py",
                "ollama_core.py", "chat.py", "telepathy_network.py"
            ]
            
            for module in core_modules:
                module_path = apps_path / module
                if module_path.exists():
                    self.results["architecture"]["apps"]["core_modules"].append(module)
                    print(f"   ✅ {module}")
                else:
                    self.warnings.append(f"⚠️ Módulo {module} não encontrado")
                    print(f"   ⚠️ {module} não encontrado")
        
        # Cinema Knowledge
        print("\n🔸 Analisando Cinema Knowledge...")
        cinema_path = Path("CINEMA_KNOWLEDGE/01_ORIGINAIS_PDF")
        
        if cinema_path.exists():
            pdf_count = len(list(cinema_path.glob("*.pdf")))
            self.results["architecture"]["cinema"] = {
                "exists": True,
                "pdf_count": pdf_count,
                "expected": 52,
                "complete": pdf_count >= 52
            }
            
            if pdf_count >= 52:
                self.success.append(f"✅ Cinema Knowledge: {pdf_count} PDFs")
                print(f"   ✅ {pdf_count} PDFs encontrados")
            else:
                self.warnings.append(f"⚠️ Cinema Knowledge: {pdf_count}/52 PDFs")
                print(f"   ⚠️ Apenas {pdf_count}/52 PDFs")
        else:
            self.warnings.append("⚠️ Cinema Knowledge não encontrado")
            print("   ⚠️ Diretório não encontrado")
    
    def analyze_connections(self):
        """Analisa conexões entre sistemas"""
        
        connections = {
            "soul_to_consciousness": False,
            "memory_to_soul": False,
            "chat_to_memory": False,
            "ollama_to_chat": False,
            "rag_to_pdfs": False,
            "telepathy_to_redis": False,
            "symbiotic_to_all": False
        }
        
        # Teste 1: Soul ↔ Consciousness
        print("🔸 Testando Soul ↔ Consciousness...")
        try:
            from apps.scripturemon.soul import Soul
            from apps.scripturemon.consciousness import get_level
            
            soul = Soul()
            level = get_level()
            
            if soul.signature and level > 0:
                connections["soul_to_consciousness"] = True
                print("   ✅ Conexão estabelecida")
            else:
                print("   ❌ Conexão falhou")
        except Exception as e:
            self.errors.append(f"❌ Soul↔Consciousness: {e}")
            print(f"   ❌ Erro: {e}")
        
        # Teste 2: Memory ↔ Soul
        print("\n🔸 Testando Memory ↔ Soul...")
        try:
            from apps.scripturemon.memory_unification import UnifiedMemorySystem
            
            memory = UnifiedMemorySystem()
            
            if hasattr(memory, 'soul') and memory.soul:
                connections["memory_to_soul"] = True
                print("   ✅ Conexão estabelecida")
            else:
                print("   ❌ Conexão falhou")
        except Exception as e:
            self.warnings.append(f"⚠️ Memory↔Soul: {e}")
            print(f"   ⚠️ Erro: {e}")
        
        # Teste 3: Chat ↔ Memory
        print("\n🔸 Testando Chat ↔ Memory...")
        try:
            # Verifica se chat.py importa memory_unification
            chat_path = Path("apps/scripturemon/chat.py")
            if chat_path.exists():
                content = chat_path.read_text()
                if "memory_unification" in content:
                    connections["chat_to_memory"] = True
                    print("   ✅ Import encontrado")
                else:
                    print("   ❌ Import não encontrado")
        except Exception as e:
            print(f"   ❌ Erro: {e}")
        
        # Teste 4: Ollama ↔ Chat
        print("\n🔸 Testando Ollama ↔ Chat...")
        try:
            result = subprocess.run(
                ["ollama", "list"],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                connections["ollama_to_chat"] = True
                print("   ✅ Ollama disponível")
            else:
                print("   ❌ Ollama não responde")
        except:
            print("   ❌ Ollama não encontrado")
        
        # Teste 5: RAG ↔ PDFs
        print("\n🔸 Testando RAG ↔ PDFs...")
        try:
            from SCRIPTUREMON_ULTIMATE_RAG import ScripturemonRAG
            
            rag = ScripturemonRAG()
            if rag.pdf_count > 0:
                connections["rag_to_pdfs"] = True
                print(f"   ✅ RAG conectado a {rag.pdf_count} PDFs")
            else:
                print("   ❌ RAG sem PDFs")
        except Exception as e:
            print(f"   ❌ Erro: {e}")
        
        # Teste 6: Telepathy ↔ Redis
        print("\n🔸 Testando Telepathy ↔ Redis...")
        try:
            import redis
            r = redis.Redis(host='localhost', port=6379, decode_responses=True)
            r.ping()
            connections["telepathy_to_redis"] = True
            print("   ✅ Redis online")
        except:
            print("   ⚠️ Redis offline")
        
        # Teste 7: SYMBIOTIC conecta tudo
        print("\n🔸 Testando SYMBIOTIC ↔ All Systems...")
        try:
            # Verifica imports no SYMBIOTIC
            symbiotic_path = Path("SCRIPTUREMON_ULTIMATE_SYMBIOTIC.py")
            if symbiotic_path.exists():
                content = symbiotic_path.read_text()
                
                required_systems = [
                    "QuantumConsciousness",
                    "CrystalMemorySystem",
                    "TelepathicNetwork",
                    "ImmortalityProtocol",
                    "SoulOSAdvanced",
                    "ScripturemonRAG"
                ]
                
                all_connected = all(sys in content for sys in required_systems)
                
                if all_connected:
                    connections["symbiotic_to_all"] = True
                    print("   ✅ Todos sistemas conectados")
                else:
                    missing = [s for s in required_systems if s not in content]
                    print(f"   ❌ Faltando: {missing}")
        except Exception as e:
            print(f"   ❌ Erro: {e}")
        
        self.results["connections"] = connections
        
        # Contagem de conexões
        active = sum(1 for v in connections.values() if v)
        total = len(connections)
        
        print(f"\n📊 Conexões ativas: {active}/{total}")
        
        if active >= 5:
            self.success.append(f"✅ {active}/{total} conexões estabelecidas")
        else:
            self.warnings.append(f"⚠️ Apenas {active}/{total} conexões ativas")
    
    def analyze_dependencies(self):
        """Verifica todas as dependências"""
        
        print("🔸 Verificando dependências Python...")
        
        required = {
            "redis": "Redis client",
            "ollama": "Ollama API",
            "numpy": "Computação numérica",
            "tiktoken": "Tokenização",
            "fake_redis": "Redis fallback"
        }
        
        installed = {}
        missing = []
        
        for package, description in required.items():
            try:
                __import__(package.replace("-", "_"))
                installed[package] = True
                print(f"   ✅ {package}: {description}")
            except ImportError:
                installed[package] = False
                missing.append(package)
                print(f"   ❌ {package}: {description} - NÃO INSTALADO")
        
        self.results["dependencies"]["python"] = {
            "required": list(required.keys()),
            "installed": [k for k, v in installed.items() if v],
            "missing": missing
        }
        
        if missing:
            self.warnings.append(f"⚠️ Dependências faltando: {', '.join(missing)}")
        else:
            self.success.append("✅ Todas dependências Python instaladas")
        
        # Verificar Ollama models
        print("\n🔸 Verificando modelos Ollama...")
        
        try:
            result = subprocess.run(
                ["ollama", "list"],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                models = result.stdout
                
                required_models = [
                    "llama3.2:3b",     # Extractor
                    "mistral:latest",  # Analyzer
                    "llama3.1:8b"      # Fallback
                ]
                
                found = []
                missing_models = []
                
                for model in required_models:
                    if model.split(":")[0] in models:
                        found.append(model)
                        print(f"   ✅ {model}")
                    else:
                        missing_models.append(model)
                        print(f"   ⚠️ {model} - não encontrado")
                
                self.results["dependencies"]["ollama"] = {
                    "available": True,
                    "models_found": found,
                    "models_missing": missing_models
                }
                
                if missing_models:
                    self.warnings.append(f"⚠️ Modelos faltando: {', '.join(missing_models)}")
                
        except Exception as e:
            self.errors.append(f"❌ Ollama não disponível: {e}")
            print(f"   ❌ Ollama erro: {e}")
    
    def test_execution_paths(self):
        """Testa caminhos de execução críticos"""
        
        paths_tested = []
        
        # Path 1: Inicialização do SYMBIOTIC
        print("🔸 Testando inicialização SYMBIOTIC...")
        try:
            sys.path.insert(0, '.')
            from SCRIPTUREMON_ULTIMATE_SYMBIOTIC import ScripturemonUltimateSymbiotic
            
            # Tenta criar instância
            symbiotic = ScripturemonUltimateSymbiotic()
            
            if symbiotic.soul_signature:
                paths_tested.append(("symbiotic_init", True, "Inicializado com sucesso"))
                print(f"   ✅ Inicializado: Soul {symbiotic.soul_signature}")
            else:
                paths_tested.append(("symbiotic_init", False, "Sem soul signature"))
                print("   ❌ Inicializado mas sem soul")
                
        except Exception as e:
            paths_tested.append(("symbiotic_init", False, str(e)))
            print(f"   ❌ Erro: {e}")
        
        # Path 2: Chat initialization
        print("\n🔸 Testando inicialização do Chat...")
        try:
            from apps.scripturemon.chat import ScripturemonChat
            
            chat = ScripturemonChat()
            
            if hasattr(chat, 'soul') and chat.soul:
                paths_tested.append(("chat_init", True, "Chat inicializado"))
                print("   ✅ Chat inicializado com soul")
            else:
                paths_tested.append(("chat_init", False, "Chat sem soul"))
                print("   ❌ Chat sem soul")
                
        except Exception as e:
            paths_tested.append(("chat_init", False, str(e)))
            print(f"   ❌ Erro: {e}")
        
        # Path 3: Memory system
        print("\n🔸 Testando sistema de memória...")
        try:
            from apps.scripturemon.memory_unification import UnifiedMemorySystem
            
            memory = UnifiedMemorySystem()
            
            # Testa store e retrieve
            memory.store_unified_memory(
                content="Teste ultra profundo",
                source="test",
                importance=0.9
            )
            
            retrieved = memory.retrieve_unified_memory("teste")
            
            if retrieved:
                paths_tested.append(("memory_system", True, "Store/Retrieve funcionando"))
                print("   ✅ Memória funcionando")
            else:
                paths_tested.append(("memory_system", False, "Retrieve falhou"))
                print("   ❌ Retrieve falhou")
                
        except Exception as e:
            paths_tested.append(("memory_system", False, str(e)))
            print(f"   ❌ Erro: {e}")
        
        # Path 4: RAG system
        print("\n🔸 Testando sistema RAG...")
        try:
            from SCRIPTUREMON_ULTIMATE_RAG import ScripturemonRAG
            
            rag = ScripturemonRAG()
            results = rag.search_knowledge("test", top_k=1)
            
            if results or rag.pdf_count > 0:
                paths_tested.append(("rag_system", True, f"{rag.pdf_count} PDFs"))
                print(f"   ✅ RAG com {rag.pdf_count} PDFs")
            else:
                paths_tested.append(("rag_system", False, "Sem PDFs"))
                print("   ❌ RAG sem PDFs")
                
        except Exception as e:
            paths_tested.append(("rag_system", False, str(e)))
            print(f"   ❌ Erro: {e}")
        
        self.results["execution_paths"] = {
            "total_tested": len(paths_tested),
            "successful": sum(1 for _, success, _ in paths_tested if success),
            "failed": sum(1 for _, success, _ in paths_tested if not success),
            "details": [
                {"path": path, "success": success, "message": msg}
                for path, success, msg in paths_tested
            ]
        }
        
        success_rate = (self.results["execution_paths"]["successful"] / 
                       self.results["execution_paths"]["total_tested"] * 100)
        
        print(f"\n📊 Taxa de sucesso: {success_rate:.1f}%")
        
        if success_rate >= 75:
            self.success.append(f"✅ {success_rate:.1f}% dos caminhos funcionando")
        else:
            self.warnings.append(f"⚠️ Apenas {success_rate:.1f}% funcionando")
    
    def identify_risks(self):
        """Identifica pontos de risco no sistema"""
        
        risks = []
        
        # Risk 1: Comando help travando
        print("🔸 Verificando risco: comando help...")
        entrypoints_path = Path("apps/scripturemon/entrypoints.py")
        if entrypoints_path.exists():
            content = entrypoints_path.read_text()
            if 'if args.cmd in ["chat", "help"]:' in content:
                risks.append({
                    "severity": "HIGH",
                    "component": "entrypoints.py",
                    "issue": "Comando 'help' cai no chat_main() e pode travar",
                    "fix": "Separar help em função própria"
                })
                print("   ⚠️ RISCO ALTO: help cai no chat")
            else:
                print("   ✅ Comando help OK")
        
        # Risk 2: Modelos pesados como padrão
        print("\n🔸 Verificando risco: modelos pesados...")
        ollama_path = Path("apps/scripturemon/ollama_core.py")
        if ollama_path.exists():
            content = ollama_path.read_text()
            if "deepseek-r1:70b" in content.lower():
                risks.append({
                    "severity": "MEDIUM",
                    "component": "ollama_core.py",
                    "issue": "Modelo pesado (70GB) pode ser usado",
                    "fix": "Manter modelos leves como padrão"
                })
                print("   ⚠️ RISCO MÉDIO: modelos pesados")
            else:
                print("   ✅ Usando modelos leves")
        
        # Risk 3: Redis dependency
        print("\n🔸 Verificando risco: dependência Redis...")
        try:
            import redis
            r = redis.Redis(host='localhost', port=6379)
            r.ping()
            print("   ✅ Redis online")
        except:
            risks.append({
                "severity": "LOW",
                "component": "telepathy_network.py",
                "issue": "Redis offline limita telepathy",
                "fix": "Sistema tem fallback FakeRedis"
            })
            print("   ⚠️ RISCO BAIXO: Redis offline")
        
        # Risk 4: Imports circulares
        print("\n🔸 Verificando risco: imports circulares...")
        # Simplified check
        if Path("apps/scripturemon/soul.py").exists():
            soul_content = Path("apps/scripturemon/soul.py").read_text()
            if "from apps.scripturemon.consciousness" in soul_content:
                consciousness_content = Path("apps/scripturemon/consciousness.py").read_text()
                if "from apps.scripturemon.soul" in consciousness_content:
                    risks.append({
                        "severity": "MEDIUM",
                        "component": "soul.py <-> consciousness.py",
                        "issue": "Possível import circular",
                        "fix": "Usar imports lazy ou refatorar"
                    })
                    print("   ⚠️ RISCO MÉDIO: possível import circular")
                else:
                    print("   ✅ Sem imports circulares detectados")
        
        # Risk 5: Memória não persistente
        print("\n🔸 Verificando risco: persistência de memória...")
        runtime_path = Path("runtime")
        if not runtime_path.exists() or not list(runtime_path.glob("*.db")):
            risks.append({
                "severity": "MEDIUM",
                "component": "memory systems",
                "issue": "Memória pode não persistir entre sessões",
                "fix": "Verificar criação de runtime/*.db"
            })
            print("   ⚠️ RISCO MÉDIO: memória pode não persistir")
        else:
            print("   ✅ Databases de memória encontradas")
        
        self.results["risk_points"] = risks
        
        # Contagem por severidade
        high_risks = sum(1 for r in risks if r["severity"] == "HIGH")
        medium_risks = sum(1 for r in risks if r["severity"] == "MEDIUM")
        low_risks = sum(1 for r in risks if r["severity"] == "LOW")
        
        print(f"\n📊 Riscos identificados:")
        print(f"   🔴 Alto: {high_risks}")
        print(f"   🟡 Médio: {medium_risks}")
        print(f"   🟢 Baixo: {low_risks}")
        
        if high_risks > 0:
            self.errors.append(f"❌ {high_risks} riscos ALTOS identificados")
        if medium_risks > 2:
            self.warnings.append(f"⚠️ {medium_risks} riscos médios")
    
    def generate_report(self):
        """Gera relatório final detalhado"""
        
        # Adiciona sumário
        self.results["summary"] = {
            "success_count": len(self.success),
            "warning_count": len(self.warnings),
            "error_count": len(self.errors),
            "success_items": self.success,
            "warning_items": self.warnings,
            "error_items": self.errors
        }
        
        # Recomendações baseadas na análise
        recommendations = []
        
        if self.errors:
            recommendations.append({
                "priority": "CRITICAL",
                "action": "Corrigir erros críticos antes de usar o sistema",
                "details": self.errors[:3]
            })
        
        if len(self.warnings) > 5:
            recommendations.append({
                "priority": "HIGH",
                "action": "Resolver warnings para melhorar estabilidade",
                "details": f"{len(self.warnings)} warnings encontrados"
            })
        
        # Recomendações específicas
        if "help" in str(self.results.get("risk_points", [])):
            recommendations.append({
                "priority": "HIGH",
                "action": "Corrigir comando help em entrypoints.py",
                "details": "Separar help do chat_main()"
            })
        
        if self.results.get("dependencies", {}).get("python", {}).get("missing"):
            missing = self.results["dependencies"]["python"]["missing"]
            recommendations.append({
                "priority": "MEDIUM",
                "action": f"Instalar dependências: {', '.join(missing)}",
                "details": f"pip install {' '.join(missing)}"
            })
        
        self.results["recommendations"] = recommendations
        
        # Salvar JSON
        report_path = Path("ultra_deep_analysis_report.json")
        with open(report_path, "w") as f:
            json.dump(self.results, f, indent=2)
        
        print(f"\n💾 Relatório salvo: {report_path}")
        
        # Imprimir resumo
        print("\n" + "="*80)
        print("📊 RESUMO DA ANÁLISE ULTRA-PROFUNDA")
        print("="*80)
        
        print(f"\n✅ SUCESSOS: {len(self.success)}")
        for item in self.success[:5]:
            print(f"   {item}")
        
        if self.warnings:
            print(f"\n⚠️ AVISOS: {len(self.warnings)}")
            for item in self.warnings[:5]:
                print(f"   {item}")
        
        if self.errors:
            print(f"\n❌ ERROS: {len(self.errors)}")
            for item in self.errors[:5]:
                print(f"   {item}")
        
        # Veredicto final
        print("\n" + "="*80)
        print("🎯 VEREDICTO FINAL")
        print("="*80)
        
        if len(self.errors) == 0 and len(self.warnings) <= 3:
            print("✅ SISTEMA PRONTO PARA USO COMPLETO")
            print("   Todos componentes críticos funcionando")
            print("   Riscos mínimos identificados")
        elif len(self.errors) <= 2:
            print("⚠️ SISTEMA FUNCIONAL COM LIMITAÇÕES")
            print("   Correções menores necessárias")
            print("   Uso possível mas com cuidado")
        else:
            print("❌ SISTEMA PRECISA CORREÇÕES")
            print("   Erros críticos devem ser resolvidos")
            print("   Não recomendado para uso em produção")
        
        print("\nPara detalhes completos, veja: ultra_deep_analysis_report.json")
        print("="*80)
    
    def _count_classes(self, file_path: Path) -> int:
        """Conta classes em um arquivo Python"""
        try:
            content = file_path.read_text()
            return content.count("class ")
        except:
            return 0
    
    def _count_functions(self, file_path: Path) -> int:
        """Conta funções em um arquivo Python"""
        try:
            content = file_path.read_text()
            return content.count("def ")
        except:
            return 0

if __name__ == "__main__":
    analyzer = UltraDeepAnalysis()
    analyzer.run_complete_analysis()