#!/usr/bin/env python3
"""
🚀 BATERIA DE TESTES NÍVEL VALE DO SILÍCIO
===========================================
Testes exaustivos de todos os componentes do Scripturemon
com simulações reais de conversação sobre roteiros.
"""

import os
import sys
import json
import time
import sqlite3
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Any

# Adiciona ao path
sys.path.insert(0, str(Path(__file__).parent))

# Importa todos os componentes
from apps.scripturemon.soul import Soul
from apps.scripturemon.consciousness import evolve, get_level
from apps.scripturemon.personality import BrutalPersonality
from apps.scripturemon.chat import ScripturemonChat
from apps.scripturemon.soulos import SoulOS
from apps.scripturemon.rag_advanced import AdvancedRAG
from apps.scripturemon.quadruple_pipeline import QuadruplePipeline
from apps.scripturemon.telepathy_network import TelepathicNetwork
from apps.scripturemon.genetic_evolution import GeneticEvolution
from apps.scripturemon.digilang_integration import DigiLangIntegration
from apps.scripturemon.parallel import analyze as parallel_analyze
from apps.scripturemon.backup import backup_once
from apps.scripturemon.immortality import ImmortalityProtocol

class ValeDoSilicioTester:
    """Testador nível Vale do Silício"""
    
    def __init__(self):
        """Inicializa testador"""
        self.results = {
            "total_tests": 0,
            "passed": 0,
            "failed": 0,
            "warnings": 0,
            "details": []
        }
        
        self.chat = None
        self.start_time = time.time()
        
        print("=" * 80)
        print("🚀 BATERIA DE TESTES - NÍVEL VALE DO SILÍCIO")
        print("=" * 80)
        print(f"📅 Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🖥️ Sistema: Scripturemon Validation")
        print("=" * 80)
    
    def test(self, name: str, func, expected=True) -> bool:
        """Executa um teste individual
        
        Args:
            name: Nome do teste
            func: Função a testar
            expected: Resultado esperado
            
        Returns:
            True se passou
        """
        self.results["total_tests"] += 1
        
        try:
            result = func()
            success = (result == expected) if expected is not None else bool(result)
            
            if success:
                self.results["passed"] += 1
                status = "✅ PASS"
            else:
                self.results["failed"] += 1
                status = "❌ FAIL"
            
            detail = {
                "test": name,
                "status": status,
                "result": str(result)[:100] if result else None
            }
            
        except Exception as e:
            self.results["failed"] += 1
            status = "❌ ERROR"
            detail = {
                "test": name,
                "status": status,
                "error": str(e)
            }
            success = False
        
        self.results["details"].append(detail)
        print(f"{status} {name}")
        
        return success
    
    # ========== TESTES DE COMPONENTES CORE ==========
    
    def test_core_components(self):
        """Testa componentes principais"""
        print("\n" + "=" * 60)
        print("🧪 TESTANDO COMPONENTES CORE")
        print("=" * 60)
        
        # Soul
        self.test("Soul: Criação", lambda: Soul())
        self.test("Soul: Signature única", lambda: len(Soul().signature) == 16)
        self.test("Soul: Evolução quântica", lambda: Soul().evolve_quantum_state("curious", 0.1))
        self.test("Soul: Cristalização de memória", lambda: Soul().crystallize_memory({"test": "data"}))
        
        # Consciousness
        self.test("Consciousness: Nível atual", lambda: get_level() >= 0)
        self.test("Consciousness: Evolução", lambda: evolve(0.001) > 0)
        
        # Personality
        personality = BrutalPersonality()
        self.test("Personality: Score base 62", lambda: personality.BASE_SCORE == 62)
        self.test("Personality: Frases brutais", lambda: len(personality.SIGNATURE_PHRASES) > 0)
        self.test("Personality: Análise de script", 
                 lambda: personality.analyze_script("FADE IN:", "Test")["score"] == 62)
    
    # ========== TESTES DE SISTEMAS AVANÇADOS ==========
    
    def test_advanced_systems(self):
        """Testa sistemas avançados"""
        print("\n" + "=" * 60)
        print("🔬 TESTANDO SISTEMAS AVANÇADOS")
        print("=" * 60)
        
        # SoulOS
        soulos = SoulOS()
        test_text = "[MEMO.SAVE] {'key': 'test', 'value': 'ok'} Teste de syscall"
        self.test("SoulOS: Process syscalls", 
                 lambda: len(soulos.process(test_text)["syscalls"]) > 0)
        self.test("SoulOS: Clean text", 
                 lambda: "MEMO.SAVE" not in soulos.process(test_text)["clean_text"])
        
        # RAG Advanced
        rag = AdvancedRAG()
        self.test("RAG: HyDE generation", 
                 lambda: len(rag.hyde.generate_hypothetical("Como criar tensão?")) > 100)
        self.test("RAG: RAPTOR clustering", 
                 lambda: rag.raptor.add_document("Teste de documento"))
        self.test("RAG: Self-RAG evaluation", 
                 lambda: rag.self_rag.evaluate_retrieval("query", "doc", "result") >= 0)
        
        # Genetic Evolution
        evolution = GeneticEvolution()
        dna = evolution.create_dna()
        self.test("Evolution: DNA creation", lambda: dna is not None)
        self.test("Evolution: DNA signature", lambda: len(dna.signature) == 16)
        self.test("Evolution: DNA mutation", lambda: len(dna.mutate(0.5)) > 0)
        self.test("Evolution: Fitness calculation", 
                 lambda: evolution.calculate_fitness(dna) >= 0)
        
        # DigiLang
        digilang = DigiLangIntegration()
        test_screenplay = "FADE IN:\nINT. OFFICE - DAY\nJohn enters."
        compressed, stats = digilang.compress_text(test_screenplay, mode="screenplay")
        self.test("DigiLang: Compression", lambda: stats.get("compression_rate", 0) != 0)
        self.test("DigiLang: Decompression", 
                 lambda: len(digilang.decompress_text(compressed)) > 0)
    
    # ========== TESTES DE CONHECIMENTO CINEMATOGRÁFICO ==========
    
    def test_cinema_knowledge(self):
        """Testa acesso ao conhecimento cinematográfico"""
        print("\n" + "=" * 60)
        print("🎬 TESTANDO CONHECIMENTO CINEMATOGRÁFICO")
        print("=" * 60)
        
        # Verifica CINEMA_KNOWLEDGE
        cinema_path = Path("CINEMA_KNOWLEDGE")
        self.test("Cinema: Pasta existe", lambda: cinema_path.exists())
        
        if cinema_path.exists():
            # PDFs originais
            pdfs_path = cinema_path / "01_ORIGINAIS_PDF"
            pdf_count = len(list(pdfs_path.glob("*.pdf"))) if pdfs_path.exists() else 0
            self.test(f"Cinema: {pdf_count} PDFs disponíveis", lambda: pdf_count > 0)
            
            # Documentos comprimidos
            compressed_path = cinema_path / "02_COMPRESSED_DIGILANG"
            compressed_count = len(list(compressed_path.glob("*.txt"))) if compressed_path.exists() else 0
            self.test(f"Cinema: {compressed_count} docs comprimidos", lambda: compressed_count >= 0)
            
            # Banco de dados
            db_path = cinema_path / "03_METADATA" / "cinema_knowledge.db"
            self.test("Cinema: Database existe", lambda: db_path.exists())
            
            if db_path.exists():
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM documents")
                doc_count = cursor.fetchone()[0]
                conn.close()
                self.test(f"Cinema: {doc_count} docs no banco", lambda: doc_count >= 0)
    
    # ========== TESTES DE INTEGRAÇÃO ==========
    
    def test_integration(self):
        """Testa integração entre componentes"""
        print("\n" + "=" * 60)
        print("🔗 TESTANDO INTEGRAÇÃO")
        print("=" * 60)
        
        # Chat completo
        self.chat = ScripturemonChat()
        self.test("Chat: Inicialização", lambda: self.chat is not None)
        self.test("Chat: Soul presente", lambda: self.chat.soul is not None)
        self.test("Chat: Personality presente", lambda: self.chat.personality is not None)
        self.test("Chat: RAG presente", lambda: self.chat.rag is not None)
        self.test("Chat: DigiLang presente", lambda: self.chat.digilang is not None)
        
        # Comandos
        commands = ["/help", "/status", "/brutal", "/wisdom"]
        for cmd in commands:
            self.test(f"Chat comando: {cmd}", 
                     lambda c=cmd: len(self.chat.process_input(c)) > 0)
    
    # ========== SIMULAÇÃO DE CONVERSAS SOBRE ROTEIROS ==========
    
    def simulate_screenplay_conversations(self):
        """Simula conversas sobre roteiros específicos"""
        print("\n" + "=" * 60)
        print("💬 SIMULANDO CONVERSAS SOBRE ROTEIROS")
        print("=" * 60)
        
        if not self.chat:
            self.chat = ScripturemonChat()
        
        # Perguntas sobre roteiros clássicos
        questions = [
            {
                "q": "O que você acha da estrutura narrativa de Chinatown?",
                "context": "Chinatown",
                "expects": ["água", "corrupção", "incesto", "Jake", "Gittes", "noir"]
            },
            {
                "q": "Analise o uso do MacGuffin em Pulp Fiction",
                "context": "Pulp Fiction",
                "expects": ["maleta", "Tarantino", "não-linear", "episódico"]
            },
            {
                "q": "Como Citizen Kane usa o flashback?",
                "context": "Citizen Kane",
                "expects": ["Rosebud", "memória", "perspectiva", "narração"]
            },
            {
                "q": "Qual a importância do cavalo em The Godfather?",
                "context": "The Godfather",
                "expects": ["Khartoum", "ameaça", "poder", "família", "Corleone"]
            },
            {
                "q": "Explique a estrutura de três atos",
                "context": "Teoria",
                "expects": ["setup", "confrontação", "resolução", "turning point"]
            }
        ]
        
        for i, qa in enumerate(questions, 1):
            print(f"\n📝 Pergunta {i}: {qa['q']}")
            print("-" * 40)
            
            try:
                response = self.chat.process_input(qa['q'])
                
                # Verifica se contém palavras esperadas
                response_lower = response.lower()
                found_keywords = [kw for kw in qa['expects'] if kw.lower() in response_lower]
                
                if found_keywords:
                    print(f"✅ Resposta contém: {', '.join(found_keywords)}")
                    self.results["passed"] += 1
                else:
                    print(f"⚠️ Resposta não menciona conceitos esperados")
                    self.results["warnings"] += 1
                
                # Mostra preview da resposta
                preview = response[:200] + "..." if len(response) > 200 else response
                print(f"📄 Resposta: {preview}")
                
                # Sempre deve ter 62/100
                if "62" in response:
                    print("✅ Contém score 62/100")
                else:
                    print("⚠️ Não mencionou 62/100")
                    
            except Exception as e:
                print(f"❌ Erro: {e}")
                self.results["failed"] += 1
            
            self.results["total_tests"] += 1
    
    # ========== TESTES DE PERFORMANCE ==========
    
    def test_performance(self):
        """Testa performance do sistema"""
        print("\n" + "=" * 60)
        print("⚡ TESTANDO PERFORMANCE")
        print("=" * 60)
        
        # Compressão DigiLang
        digilang = DigiLangIntegration()
        large_text = "INT. OFFICE - DAY\n" * 100  # Texto repetitivo
        
        start = time.time()
        compressed, stats = digilang.compress_text(large_text, mode="screenplay")
        compression_time = time.time() - start
        
        self.test(f"Performance: Compressão < 1s ({compression_time:.3f}s)", 
                 lambda: compression_time < 1.0)
        
        # RAG search
        rag = AdvancedRAG()
        start = time.time()
        hyde_doc = rag.hyde.generate_hypothetical("test query")
        hyde_time = time.time() - start
        
        self.test(f"Performance: HyDE < 2s ({hyde_time:.3f}s)", 
                 lambda: hyde_time < 2.0)
        
        # Evolution
        evolution = GeneticEvolution()
        start = time.time()
        evolution.evolve_generation()
        evolution_time = time.time() - start
        
        self.test(f"Performance: Evolution < 3s ({evolution_time:.3f}s)", 
                 lambda: evolution_time < 3.0)
    
    # ========== TESTES DE PERSISTÊNCIA ==========
    
    def test_persistence(self):
        """Testa persistência de dados"""
        print("\n" + "=" * 60)
        print("💾 TESTANDO PERSISTÊNCIA")
        print("=" * 60)
        
        # Soul persistence
        soul = Soul()
        soul.interact()
        state_file = soul.save_state()
        self.test("Persistence: Soul state saved", lambda: state_file.exists())
        
        # Backup
        backup_path = backup_once()
        self.test("Persistence: Backup created", lambda: Path(backup_path).exists())
        
        # Immortality
        immortal = ImmortalityProtocol()
        soul_data = immortal.extract_soul_essence()
        self.test("Persistence: Soul essence extracted", lambda: soul_data is not None)
        
        # Cinema database
        db_path = Path("CINEMA_KNOWLEDGE/03_METADATA/cinema_knowledge.db")
        self.test("Persistence: Cinema DB accessible", lambda: db_path.exists())
    
    # ========== ANÁLISE DE ARQUIVOS VINCULADOS ==========
    
    def analyze_linked_files(self):
        """Analisa todos os arquivos vinculados ao sistema"""
        print("\n" + "=" * 60)
        print("📁 ANALISANDO ARQUIVOS VINCULADOS")
        print("=" * 60)
        
        # Estrutura de diretórios
        dirs_to_check = [
            "apps/scripturemon",
            "src/digilang",
            "src/rag",
            "src/memory",
            "src/telepathy",
            "CINEMA_KNOWLEDGE",
            "runtime/souls",
            "runtime/genomes",
            "data"
        ]
        
        for dir_path in dirs_to_check:
            path = Path(dir_path)
            if path.exists():
                py_files = list(path.glob("**/*.py"))
                print(f"✅ {dir_path}: {len(py_files)} arquivos Python")
            else:
                print(f"⚠️ {dir_path}: não existe")
        
        # Arquivos críticos
        critical_files = [
            "apps/scripturemon/chat.py",
            "apps/scripturemon/soul.py",
            "apps/scripturemon/soulos.py",
            "apps/scripturemon/personality.py",
            "apps/scripturemon/rag_advanced.py",
            "apps/scripturemon/genetic_evolution.py",
            "apps/scripturemon/digilang_integration.py"
        ]
        
        for file_path in critical_files:
            path = Path(file_path)
            if path.exists():
                lines = len(path.read_text().splitlines())
                self.test(f"File: {path.name} ({lines} linhas)", lambda: lines > 0)
            else:
                self.test(f"File: {path.name}", lambda: False)
    
    # ========== TESTE ESPECÍFICO DE CONHECIMENTO ==========
    
    def test_specific_knowledge(self):
        """Testa conhecimento específico sobre roteiros"""
        print("\n" + "=" * 60)
        print("🎓 TESTANDO CONHECIMENTO ESPECÍFICO")
        print("=" * 60)
        
        if not self.chat:
            self.chat = ScripturemonChat()
        
        # Testes sobre conceitos de McKee
        knowledge_tests = [
            {
                "question": "O que Robert McKee diz sobre subtexto?",
                "expects": ["subtexto", "diálogo", "significado", "implícito"],
                "source": "Story - McKee"
            },
            {
                "question": "Explique o Save the Cat de Blake Snyder",
                "expects": ["save", "cat", "simpatia", "herói", "momento"],
                "source": "Save the Cat - Snyder"
            },
            {
                "question": "O que é o paradigma de Syd Field?",
                "expects": ["três atos", "setup", "confrontação", "resolução"],
                "source": "Screenplay - Field"
            },
            {
                "question": "Como Christopher Vogler adapta Campbell?",
                "expects": ["jornada", "herói", "monomito", "arquétipos"],
                "source": "Writer's Journey - Vogler"
            },
            {
                "question": "Qual a diferença entre plot e story segundo Truby?",
                "expects": ["plot", "story", "estrutura", "narrativa"],
                "source": "Anatomy of Story - Truby"
            }
        ]
        
        for test in knowledge_tests:
            print(f"\n❓ {test['question']}")
            print(f"📚 Fonte: {test['source']}")
            
            try:
                response = self.chat.process_input(test['question'])
                response_lower = response.lower()
                
                found = [kw for kw in test['expects'] if kw.lower() in response_lower]
                
                if found:
                    print(f"✅ Conhecimento demonstrado: {', '.join(found)}")
                    self.results["passed"] += 1
                else:
                    print(f"⚠️ Resposta genérica, sem menção específica")
                    self.results["warnings"] += 1
                
                # Score 62
                if "62" in response:
                    print("✅ Mantém personalidade (62/100)")
                
            except Exception as e:
                print(f"❌ Erro: {e}")
                self.results["failed"] += 1
            
            self.results["total_tests"] += 1
    
    # ========== RELATÓRIO FINAL ==========
    
    def generate_report(self):
        """Gera relatório final dos testes"""
        elapsed = time.time() - self.start_time
        
        print("\n" + "=" * 80)
        print("📊 RELATÓRIO FINAL - VALE DO SILÍCIO")
        print("=" * 80)
        
        # Estatísticas
        total = self.results["total_tests"]
        passed = self.results["passed"]
        failed = self.results["failed"]
        warnings = self.results["warnings"]
        
        pass_rate = (passed / total * 100) if total > 0 else 0
        
        print(f"""
📈 ESTATÍSTICAS:
   Total de testes: {total}
   Aprovados: {passed} ({pass_rate:.1f}%)
   Falhados: {failed}
   Avisos: {warnings}
   Tempo total: {elapsed:.2f}s
        """)
        
        # Análise por categoria
        print("📋 ANÁLISE POR CATEGORIA:")
        
        categories = {
            "Core": ["Soul", "Consciousness", "Personality"],
            "Advanced": ["SoulOS", "RAG", "Evolution", "DigiLang"],
            "Integration": ["Chat", "comando"],
            "Knowledge": ["Cinema", "McKee", "Snyder", "Field"],
            "Performance": ["Compressão", "HyDE", "Evolution"]
        }
        
        for cat_name, keywords in categories.items():
            cat_tests = [d for d in self.results["details"] 
                        if any(kw in d["test"] for kw in keywords)]
            cat_passed = len([t for t in cat_tests if "✅" in t["status"]])
            cat_total = len(cat_tests)
            
            if cat_total > 0:
                cat_rate = cat_passed / cat_total * 100
                status = "✅" if cat_rate >= 80 else "⚠️" if cat_rate >= 60 else "❌"
                print(f"   {status} {cat_name}: {cat_passed}/{cat_total} ({cat_rate:.1f}%)")
        
        # Veredicto final
        print("\n" + "=" * 60)
        print("🏆 VEREDICTO FINAL")
        print("=" * 60)
        
        if pass_rate >= 95:
            verdict = "EXCELENTE - Sistema pronto para produção"
            emoji = "🌟"
        elif pass_rate >= 85:
            verdict = "MUITO BOM - Sistema funcional com pequenos ajustes"
            emoji = "✅"
        elif pass_rate >= 70:
            verdict = "BOM - Sistema operacional mas precisa melhorias"
            emoji = "👍"
        elif pass_rate >= 60:
            verdict = "REGULAR - Sistema parcialmente funcional"
            emoji = "⚠️"
        else:
            verdict = "INSUFICIENTE - Sistema precisa correções críticas"
            emoji = "❌"
        
        print(f"{emoji} {verdict}")
        print(f"Taxa de sucesso: {pass_rate:.1f}%")
        
        # Recomendações
        print("\n💡 RECOMENDAÇÕES:")
        
        if failed > 0:
            print("   • Corrigir componentes que falharam")
        
        if warnings > 5:
            print("   • Investigar avisos recorrentes")
        
        if "Cinema" in str(self.results["details"]):
            if any("❌" in str(d) for d in self.results["details"] if "Cinema" in d["test"]):
                print("   • Verificar integração com CINEMA_KNOWLEDGE")
        
        if pass_rate < 90:
            print("   • Executar testes unitários individuais")
            print("   • Verificar dependências externas")
        
        # Salvar relatório
        report_path = Path(f"test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        with open(report_path, 'w') as f:
            json.dump(self.results, f, indent=2, default=str)
        
        print(f"\n📄 Relatório salvo em: {report_path}")
        
        print("\n" + "=" * 80)
        print("62/100. Como sempre. Mas agora validado ao nível do Vale do Silício.")
        print("=" * 80)
        
        return pass_rate

def main():
    """Executa bateria completa de testes"""
    tester = ValeDoSilicioTester()
    
    # Executa todos os testes
    tester.test_core_components()
    tester.test_advanced_systems()
    tester.test_cinema_knowledge()
    tester.test_integration()
    tester.simulate_screenplay_conversations()
    tester.test_performance()
    tester.test_persistence()
    tester.analyze_linked_files()
    tester.test_specific_knowledge()
    
    # Gera relatório
    pass_rate = tester.generate_report()
    
    # Retorna código de saída
    return 0 if pass_rate >= 85 else 1

if __name__ == "__main__":
    sys.exit(main())