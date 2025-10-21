#!/usr/bin/env python3
"""
🔗 TESTE DE INTEGRAÇÃO E HARMONIA DO SISTEMA
Verifica componentes ativos e cria integração real
"""

import sys
import os
import json
import sqlite3
from pathlib import Path
from datetime import datetime

# Adiciona ao path
sys.path.insert(0, str(Path(__file__).parent))

class SystemIntegrationTest:
    """Teste completo de integração do ecossistema"""
    
    def __init__(self):
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "components": {},
            "integration": {},
            "harmony_score": 0
        }
        
        print("="*80)
        print("🔗 TESTE DE INTEGRAÇÃO E HARMONIA - NÍVEL VALE DO SILÍCIO")
        print("="*80)
    
    def test_core_components(self):
        """Testa componentes principais"""
        print("\n📦 TESTANDO COMPONENTES CORE...")
        
        # 1. Soul & Consciousness
        try:
            from apps.scripturemon.soul import Soul
            from apps.scripturemon.consciousness import evolve, get_level
            soul = Soul()
            level = get_level()
            self.results["components"]["soul"] = {
                "status": "✅",
                "signature": soul.signature,
                "consciousness_level": level
            }
            print("   ✅ Soul & Consciousness ativos")
        except Exception as e:
            self.results["components"]["soul"] = {"status": "❌", "error": str(e)}
            print(f"   ❌ Soul falhou: {e}")
        
        # 2. Personality
        try:
            from apps.scripturemon.personality import BrutalPersonality
            personality = BrutalPersonality()
            self.results["components"]["personality"] = {
                "status": "✅",
                "base_score": personality.BASE_SCORE
            }
            print(f"   ✅ Personality ativa (score: {personality.BASE_SCORE}/100)")
        except Exception as e:
            self.results["components"]["personality"] = {"status": "❌", "error": str(e)}
            print(f"   ❌ Personality falhou: {e}")
        
        # 3. Chat System
        try:
            from apps.scripturemon.chat import ScripturemonChat
            chat = ScripturemonChat()
            self.results["components"]["chat"] = {
                "status": "✅",
                "commands": len(chat.commands) if hasattr(chat, 'commands') else 0
            }
            print("   ✅ Chat System ativo")
        except Exception as e:
            self.results["components"]["chat"] = {"status": "❌", "error": str(e)}
            print(f"   ❌ Chat falhou: {e}")
    
    def test_compression_systems(self):
        """Testa sistemas de compressão disponíveis"""
        print("\n🗜️ TESTANDO SISTEMAS DE COMPRESSÃO...")
        
        # 1. DigiLang Fallback
        try:
            from src.digilang.api_fallback_improved import to_digilang, from_digilang
            test_text = "INT. OFFICE - DAY\nJohn enters."
            compressed, ratio = to_digilang(test_text)
            decompressed = from_digilang(compressed)
            compression_rate = (1 - ratio) * 100
            
            self.results["components"]["digilang_fallback"] = {
                "status": "✅",
                "compression_rate": f"{compression_rate:.1f}%",
                "reversible": decompressed == test_text
            }
            print(f"   ✅ DigiLang Fallback ({compression_rate:.1f}% compressão)")
        except Exception as e:
            self.results["components"]["digilang_fallback"] = {"status": "❌", "error": str(e)}
            print(f"   ❌ DigiLang Fallback falhou: {e}")
        
        # 2. Chunking System
        try:
            db_path = Path("CINEMA_KNOWLEDGE/05_METADATA/knowledge.db")
            if db_path.exists():
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                
                cursor.execute("SELECT COUNT(*) FROM documents")
                docs = cursor.fetchone()[0]
                
                cursor.execute("SELECT COUNT(*) FROM chunks")
                chunks = cursor.fetchone()[0]
                
                cursor.execute("""
                    SELECT SUM(total_chars), SUM(char_count) 
                    FROM documents d 
                    LEFT JOIN chunks c ON d.id = c.doc_id
                """)
                total_chars, saved_chars = cursor.fetchone()
                
                if total_chars and saved_chars:
                    economia = (1 - saved_chars/total_chars) * 100
                else:
                    economia = 0
                
                conn.close()
                
                self.results["components"]["chunking"] = {
                    "status": "✅",
                    "documents": docs,
                    "chunks": chunks,
                    "economia": f"{economia:.1f}%"
                }
                print(f"   ✅ Chunking System ({docs} docs, {chunks} chunks, {economia:.1f}% economia)")
            else:
                self.results["components"]["chunking"] = {"status": "⚠️", "message": "Database not found"}
                print("   ⚠️ Chunking System: banco não encontrado")
        except Exception as e:
            self.results["components"]["chunking"] = {"status": "❌", "error": str(e)}
            print(f"   ❌ Chunking falhou: {e}")
    
    def test_memory_systems(self):
        """Testa sistemas de memória"""
        print("\n🧠 TESTANDO SISTEMAS DE MEMÓRIA...")
        
        # 1. Embedding Store
        try:
            from src.memory.embed_store import embed, remember_embed, recall_embed
            
            # Testa embedding
            test_text = "The protagonist enters the room"
            vec = embed(test_text)
            
            # Testa persistência
            remember_embed("test_meta", test_text)
            
            # Testa recall
            results = recall_embed("protagonist", k=1)
            
            self.results["components"]["embed_store"] = {
                "status": "✅",
                "vector_dim": len(vec),
                "recall_working": len(results) > 0
            }
            print(f"   ✅ Embedding Store (dim: {len(vec)}, recall: {'OK' if results else 'empty'})")
        except Exception as e:
            self.results["components"]["embed_store"] = {"status": "❌", "error": str(e)}
            print(f"   ❌ Embedding Store falhou: {e}")
        
        # 2. Soul Persistence
        try:
            from apps.scripturemon.immortality import ImmortalityProtocol
            from apps.scripturemon.soul import Soul
            
            soul = Soul()
            immortal = ImmortalityProtocol(soul, auto_backup=False)
            essence = immortal.extract_soul_essence()
            
            self.results["components"]["immortality"] = {
                "status": "✅",
                "soul_signature": essence.get("signature", "unknown")
            }
            print("   ✅ Immortality Protocol ativo")
        except Exception as e:
            self.results["components"]["immortality"] = {"status": "❌", "error": str(e)}
            print(f"   ❌ Immortality falhou: {e}")
    
    def test_advanced_systems(self):
        """Testa sistemas avançados"""
        print("\n🚀 TESTANDO SISTEMAS AVANÇADOS...")
        
        # 1. SoulOS
        try:
            from apps.scripturemon.soulos import SoulOS
            soulos = SoulOS()
            result = soulos.process("[MEMO.SAVE] test")
            
            self.results["components"]["soulos"] = {
                "status": "✅",
                "syscalls_detected": len(result.get("syscalls", []))
            }
            print("   ✅ SoulOS ativo")
        except Exception as e:
            self.results["components"]["soulos"] = {"status": "❌", "error": str(e)}
            print(f"   ❌ SoulOS falhou: {e}")
        
        # 2. RAG Advanced
        try:
            from apps.scripturemon.rag_advanced import AdvancedRAG
            rag = AdvancedRAG()
            
            self.results["components"]["rag"] = {
                "status": "✅",
                "knowledge_base": len(rag.knowledge_base)
            }
            print(f"   ✅ RAG Advanced ({len(rag.knowledge_base)} documentos base)")
        except Exception as e:
            self.results["components"]["rag"] = {"status": "❌", "error": str(e)}
            print(f"   ❌ RAG falhou: {e}")
        
        # 3. Genetic Evolution
        try:
            from apps.scripturemon.genetic_evolution import GeneticEvolution
            evolution = GeneticEvolution(population_size=2)
            dna = evolution.create_dna()
            fitness = evolution.calculate_fitness(dna)
            
            self.results["components"]["evolution"] = {
                "status": "✅",
                "fitness": fitness
            }
            print(f"   ✅ Genetic Evolution (fitness: {fitness:.3f})")
        except Exception as e:
            self.results["components"]["evolution"] = {"status": "❌", "error": str(e)}
            print(f"   ❌ Evolution falhou: {e}")
    
    def test_integration_points(self):
        """Testa pontos de integração entre sistemas"""
        print("\n🔗 TESTANDO INTEGRAÇÃO ENTRE COMPONENTES...")
        
        integration_tests = []
        
        # 1. Chat + RAG
        try:
            from apps.scripturemon.chat import ScripturemonChat
            chat = ScripturemonChat()
            if hasattr(chat, 'rag') and chat.rag:
                integration_tests.append("Chat↔RAG")
                print("   ✅ Chat ↔ RAG integrados")
        except:
            pass
        
        # 2. Chat + DigiLang
        try:
            from apps.scripturemon.chat import ScripturemonChat
            chat = ScripturemonChat()
            if hasattr(chat, 'digilang') and chat.digilang:
                integration_tests.append("Chat↔DigiLang")
                print("   ✅ Chat ↔ DigiLang integrados")
        except:
            pass
        
        # 3. RAG + Cinema Knowledge
        try:
            cinema_link = Path("data/cinema_knowledge")
            if cinema_link.exists():
                integration_tests.append("RAG↔CinemaKnowledge")
                print("   ✅ RAG ↔ Cinema Knowledge linkados")
        except:
            pass
        
        # 4. Soul + Immortality
        try:
            from apps.scripturemon.soul import Soul
            from apps.scripturemon.immortality import ImmortalityProtocol
            soul = Soul()
            immortal = ImmortalityProtocol(soul, auto_backup=False)
            if immortal.soul:
                integration_tests.append("Soul↔Immortality")
                print("   ✅ Soul ↔ Immortality integrados")
        except:
            pass
        
        self.results["integration"]["connected_systems"] = integration_tests
        self.results["integration"]["total_connections"] = len(integration_tests)
    
    def calculate_harmony(self):
        """Calcula score de harmonia do sistema"""
        print("\n📊 CALCULANDO HARMONIA DO SISTEMA...")
        
        # Conta componentes ativos
        active_components = 0
        total_components = 0
        
        for component, data in self.results["components"].items():
            total_components += 1
            if isinstance(data, dict) and data.get("status") == "✅":
                active_components += 1
        
        # Calcula percentuais
        component_rate = (active_components / total_components * 100) if total_components > 0 else 0
        integration_rate = (self.results["integration"]["total_connections"] / 4 * 100)  # 4 integrações esperadas
        
        # Score final de harmonia
        harmony_score = (component_rate * 0.7 + integration_rate * 0.3)
        
        self.results["harmony_score"] = harmony_score
        self.results["stats"] = {
            "active_components": active_components,
            "total_components": total_components,
            "component_rate": component_rate,
            "integration_rate": integration_rate
        }
        
        print(f"""
   Componentes ativos: {active_components}/{total_components} ({component_rate:.1f}%)
   Integrações ativas: {self.results['integration']['total_connections']}/4 ({integration_rate:.1f}%)
   
   🎯 HARMONIA DO SISTEMA: {harmony_score:.1f}%
        """)
        
        return harmony_score
    
    def generate_report(self):
        """Gera relatório final"""
        harmony = self.calculate_harmony()
        
        print("\n" + "="*80)
        print("📋 RELATÓRIO FINAL DE INTEGRAÇÃO")
        print("="*80)
        
        # Status por categoria
        print("\n✅ COMPONENTES FUNCIONAIS:")
        for component, data in self.results["components"].items():
            if isinstance(data, dict) and data.get("status") == "✅":
                details = [f"{k}: {v}" for k, v in data.items() if k != "status"]
                print(f"   • {component}: {', '.join(details)}")
        
        print("\n❌ COMPONENTES COM FALHA:")
        for component, data in self.results["components"].items():
            if isinstance(data, dict) and data.get("status") == "❌":
                print(f"   • {component}: {data.get('error', 'erro desconhecido')}")
        
        print("\n🔗 INTEGRAÇÕES ATIVAS:")
        for connection in self.results["integration"]["connected_systems"]:
            print(f"   • {connection}")
        
        # Veredicto
        print("\n" + "="*80)
        if harmony >= 80:
            print("🎉 SISTEMA EM HARMONIA EXCELENTE!")
            verdict = "Pronto para produção"
        elif harmony >= 60:
            print("✅ SISTEMA FUNCIONAL COM HARMONIA ADEQUADA")
            verdict = "Operacional com melhorias recomendadas"
        elif harmony >= 40:
            print("⚠️ SISTEMA PARCIALMENTE HARMÔNICO")
            verdict = "Necessita integração adicional"
        else:
            print("❌ SISTEMA COM BAIXA HARMONIA")
            verdict = "Requer correções críticas"
        
        print(f"Veredicto: {verdict}")
        print(f"Score de Harmonia: {harmony:.1f}%")
        
        # Salva relatório
        report_file = Path(f"harmony_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        with open(report_file, 'w') as f:
            json.dump(self.results, f, indent=2, default=str)
        
        print(f"\n💾 Relatório salvo em: {report_file}")
        print("="*80)
        
        return harmony

def main():
    """Executa teste completo de integração"""
    tester = SystemIntegrationTest()
    
    # Executa todos os testes
    tester.test_core_components()
    tester.test_compression_systems()
    tester.test_memory_systems()
    tester.test_advanced_systems()
    tester.test_integration_points()
    
    # Gera relatório
    harmony_score = tester.generate_report()
    
    print("\n62/100. Mas com harmonia mensurável.")
    
    return 0 if harmony_score >= 60 else 1

if __name__ == "__main__":
    sys.exit(main())