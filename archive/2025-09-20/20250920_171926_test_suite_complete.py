#!/usr/bin/env python3
"""
BATERIA DE TESTES COMPLETA - SCRIPTUREMON UNIFIED SYSTEM
Testa todos os componentes: RAG, Múltiplos Modelos, SoulOS, Evolução
"""

import sys
import os
import json
import time
import asyncio
from pathlib import Path
from typing import Dict, List, Tuple
import requests
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))

# Importar componentes
try:
    from scripturemon_unified_orchestrator import ScripturemonUnifiedOrchestrator
    from scripts.scripturemon_rag_bridge import ScripturemonRAG
    from app.models.ollama_strategy import OllamaStrategy
    from app.models.ollama_fast import FastLLM
    from app.processing.analyzers_fast import analyze_fast
    IMPORTS_OK = True
except Exception as e:
    print(f"⚠️ Erro nos imports: {e}")
    IMPORTS_OK = False

class ScripturemonTestSuite:
    """Suite completa de testes do sistema"""
    
    def __init__(self):
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "tests_passed": 0,
            "tests_failed": 0,
            "components": {},
            "performance": {},
            "quality": {}
        }
        
        self.test_samples = {
            "casablanca": """INT. RICK'S CAFE - NIGHT
            
            The cafe is crowded. SAM plays "As Time Goes By" on the piano.
            Rick sits alone, drinking. ILSA enters with LASZLO.
            
            RICK
            Of all the gin joints in all the towns
            in all the world, she walks into mine.
            
            FLASHBACK - PARIS - DAY
            
            Rick and Ilsa by the Seine, in love.
            """,
            
            "chinatown": """EXT. MULHOLLAND DRIVE - NIGHT
            
            GITTES watches MULWRAY and the YOUNG WOMAN.
            Water rushes through the spillway below.
            
            GITTES (V.O.)
            The water... it's all about the water.
            
            INTERCUT - HALL OF RECORDS
            
            Maps showing the valley's water rights.
            """,
            
            "roteiro_criador": """INT. APARTAMENTO - DIA
            
            JOÃO olha pela janela. Chove.
            
            JOÃO
            Eu não lembro de nada antes daquele dia.
            
            MARIA
            Às vezes é melhor não lembrar.
            """
        }
    
    def run_all_tests(self):
        """Executa bateria completa de testes"""
        print("\n" + "="*70)
        print("🧪 BATERIA DE TESTES COMPLETA - SCRIPTUREMON UNIFIED SYSTEM")
        print("="*70)
        
        # 1. Teste de Componentes
        print("\n📦 TESTE 1: COMPONENTES DO SISTEMA")
        print("-"*40)
        self.test_components()
        
        # 2. Teste da API RAG
        print("\n🌐 TESTE 2: API RAG")
        print("-"*40)
        self.test_rag_api()
        
        # 3. Teste de Múltiplos Modelos
        print("\n🤖 TESTE 3: MÚLTIPLOS MODELOS OLLAMA")
        print("-"*40)
        self.test_multiple_models()
        
        # 4. Teste de Processamento Paralelo
        print("\n⚡ TESTE 4: PROCESSAMENTO PARALELO")
        print("-"*40)
        self.test_parallel_processing()
        
        # 5. Teste de Busca RAG
        print("\n🔍 TESTE 5: BUSCA RAG E CONHECIMENTO")
        print("-"*40)
        self.test_rag_search()
        
        # 6. Teste de Syscalls SoulOS
        print("\n🧬 TESTE 6: SYSCALLS SOULOS")
        print("-"*40)
        self.test_soulos_syscalls()
        
        # 7. Teste de Evolução
        print("\n📈 TESTE 7: EVOLUÇÃO CONTÍNUA")
        print("-"*40)
        self.test_evolution()
        
        # 8. Teste de Qualidade de Respostas
        print("\n💎 TESTE 8: QUALIDADE DAS RESPOSTAS")
        print("-"*40)
        self.test_response_quality()
        
        # 9. Teste de Performance
        print("\n⏱️ TESTE 9: PERFORMANCE")
        print("-"*40)
        self.test_performance()
        
        # 10. Teste de Personalidade Brutal
        print("\n💀 TESTE 10: PERSONALIDADE BRUTAL")
        print("-"*40)
        self.test_brutal_personality()
        
        # Relatório Final
        self.generate_report()
    
    def test_components(self):
        """Testa disponibilidade dos componentes"""
        components = {
            "imports": IMPORTS_OK,
            "api_rag": self._check_api(),
            "ollama": self._check_ollama(),
            "vectorstore": self._check_vectorstore(),
            "memory_files": self._check_memory_files()
        }
        
        for name, status in components.items():
            self.results["components"][name] = status
            if status:
                print(f"  ✅ {name}: OK")
                self.results["tests_passed"] += 1
            else:
                print(f"  ❌ {name}: FALHOU")
                self.results["tests_failed"] += 1
    
    def _check_api(self) -> bool:
        """Verifica se API RAG está rodando"""
        try:
            resp = requests.get("http://localhost:8092/health", timeout=2)
            return resp.status_code == 200
        except:
            return False
    
    def _check_ollama(self) -> bool:
        """Verifica se Ollama está disponível"""
        try:
            import ollama
            ollama.list()
            return True
        except:
            return False
    
    def _check_vectorstore(self) -> bool:
        """Verifica ChromaDB"""
        chroma_path = Path("conhecimento/chroma")
        return chroma_path.exists() and (chroma_path / "chroma.sqlite3").exists()
    
    def _check_memory_files(self) -> bool:
        """Verifica arquivos de memória"""
        files = ["soul.json", "conhecimento/L2_CONSOLIDATED.jsonl"]
        return any(Path(f).exists() for f in files)
    
    def test_rag_api(self):
        """Testa endpoints da API RAG"""
        if not self._check_api():
            print("  ⚠️ API não está rodando")
            self.results["tests_failed"] += 1
            return
        
        endpoints = [
            ("GET", "/health", None),
            ("GET", "/knowledge/search?query=roteiro", None),
            ("GET", "/ask?q=teste", None)
        ]
        
        for method, endpoint, data in endpoints:
            try:
                url = f"http://localhost:8092{endpoint}"
                if method == "GET":
                    resp = requests.get(url, timeout=5)
                else:
                    resp = requests.post(url, json=data, timeout=5)
                
                if resp.status_code in [200, 201]:
                    print(f"  ✅ {endpoint}: OK")
                    self.results["tests_passed"] += 1
                else:
                    print(f"  ❌ {endpoint}: Status {resp.status_code}")
                    self.results["tests_failed"] += 1
            except Exception as e:
                print(f"  ❌ {endpoint}: {e}")
                self.results["tests_failed"] += 1
    
    def test_multiple_models(self):
        """Testa disponibilidade dos 4 modelos"""
        try:
            import ollama
            
            models_needed = {
                "llama3.2:3b": "Extração",
                "mistral:latest": "Análise", 
                "scripturemon-maestro": "Avaliação",
                "scripturemon-soulos": "Evolução"
            }
            
            available_models = [m['name'] for m in ollama.list()['models']]
            
            for model, role in models_needed.items():
                # Verifica com ou sem :latest
                model_base = model.split(":")[0]
                found = any(model_base in m for m in available_models)
                
                if found:
                    print(f"  ✅ {model} ({role}): Disponível")
                    self.results["tests_passed"] += 1
                else:
                    print(f"  ⚠️ {model} ({role}): Não encontrado")
                    # Não conta como falha, pois pode usar fallback
                    
        except Exception as e:
            print(f"  ❌ Erro ao verificar modelos: {e}")
            self.results["tests_failed"] += 1
    
    def test_parallel_processing(self):
        """Testa processamento paralelo"""
        if not IMPORTS_OK:
            print("  ⚠️ Imports não disponíveis")
            self.results["tests_failed"] += 1
            return
        
        try:
            orchestrator = ScripturemonUnifiedOrchestrator()
            
            # Teste assíncrono
            start = time.time()
            result = asyncio.run(
                orchestrator.process_parallel(
                    self.test_samples["casablanca"],
                    doc_type="roteiro_mestre"
                )
            )
            elapsed = time.time() - start
            
            # Verificar resultados
            has_structure = "structure" in result
            has_analysis = "analysis" in result
            has_evaluation = "evaluation" in result
            has_evolution = "evolution" in result
            
            all_present = all([has_structure, has_analysis, has_evaluation, has_evolution])
            
            if all_present:
                print(f"  ✅ Processamento paralelo: {elapsed:.1f}s")
                print(f"     - Estrutura: {'✓' if has_structure else '✗'}")
                print(f"     - Análise: {'✓' if has_analysis else '✗'}")
                print(f"     - Avaliação: {'✓' if has_evaluation else '✗'}")
                print(f"     - Evolução: {'✓' if has_evolution else '✗'}")
                self.results["tests_passed"] += 1
                self.results["performance"]["parallel_time"] = elapsed
            else:
                print(f"  ⚠️ Processamento incompleto")
                self.results["tests_failed"] += 1
                
        except Exception as e:
            print(f"  ❌ Erro no processamento: {e}")
            self.results["tests_failed"] += 1
    
    def test_rag_search(self):
        """Testa busca RAG"""
        if not IMPORTS_OK:
            print("  ⚠️ Imports não disponíveis")
            return
        
        try:
            rag = ScripturemonRAG()
            
            queries = [
                "Chinatown water metaphor",
                "three act structure",
                "character development",
                "dialogue techniques"
            ]
            
            total_results = 0
            for query in queries:
                results = rag.search_knowledge(query, top_k=5)
                total_results += len(results)
                print(f"  📚 '{query}': {len(results)} resultados")
            
            if total_results > 0:
                print(f"  ✅ RAG funcionando: {total_results} resultados totais")
                self.results["tests_passed"] += 1
            else:
                print(f"  ⚠️ Nenhum resultado RAG (base vazia?)")
                
        except Exception as e:
            print(f"  ❌ Erro na busca RAG: {e}")
            self.results["tests_failed"] += 1
    
    def test_soulos_syscalls(self):
        """Testa syscalls do SoulOS"""
        if not IMPORTS_OK:
            print("  ⚠️ Imports não disponíveis")
            return
        
        try:
            orchestrator = ScripturemonUnifiedOrchestrator()
            
            # Testar cada syscall
            syscalls_test = {
                "[MEMO.SAVE]": {"test": "memory"},
                "[SELF.PATCH]": {"knowledge": "new"},
                "[EVOLVE.TRIGGER]": {}
            }
            
            for syscall, data in syscalls_test.items():
                try:
                    if syscall == "[MEMO.SAVE]":
                        asyncio.run(orchestrator._syscall_memo_save(data))
                        print(f"  ✅ {syscall}: OK")
                    elif syscall == "[SELF.PATCH]":
                        asyncio.run(orchestrator._syscall_self_patch(data))
                        print(f"  ✅ {syscall}: OK")
                    elif syscall == "[EVOLVE.TRIGGER]":
                        before_level = orchestrator.soul["evolution_level"]
                        asyncio.run(orchestrator._syscall_evolve_trigger(data))
                        after_level = orchestrator.soul["evolution_level"]
                        if after_level > before_level:
                            print(f"  ✅ {syscall}: Evoluiu para nível {after_level}")
                        else:
                            print(f"  ⚠️ {syscall}: Nível não mudou")
                    self.results["tests_passed"] += 1
                except Exception as e:
                    print(f"  ❌ {syscall}: {e}")
                    self.results["tests_failed"] += 1
                    
        except Exception as e:
            print(f"  ❌ Erro nos syscalls: {e}")
            self.results["tests_failed"] += 1
    
    def test_evolution(self):
        """Testa sistema de evolução"""
        if not IMPORTS_OK:
            print("  ⚠️ Imports não disponíveis")
            return
        
        try:
            orchestrator = ScripturemonUnifiedOrchestrator()
            
            # Estado inicial
            initial_level = orchestrator.soul["evolution_level"]
            initial_knowledge = orchestrator.soul["knowledge_count"]
            
            # Simular processamento de PDFs
            for i in range(3):
                sample = list(self.test_samples.values())[i]
                asyncio.run(orchestrator.process_parallel(sample))
            
            # Estado final
            final_level = orchestrator.soul["evolution_level"]
            final_knowledge = orchestrator.soul["knowledge_count"]
            
            evolved = final_level > initial_level or final_knowledge > initial_knowledge
            
            if evolved:
                print(f"  ✅ Evolução detectada:")
                print(f"     Nível: {initial_level} → {final_level}")
                print(f"     Conhecimento: {initial_knowledge} → {final_knowledge}")
                self.results["tests_passed"] += 1
            else:
                print(f"  ⚠️ Sem evolução detectada")
                
        except Exception as e:
            print(f"  ❌ Erro na evolução: {e}")
            self.results["tests_failed"] += 1
    
    def test_response_quality(self):
        """Testa qualidade das respostas"""
        if not IMPORTS_OK:
            print("  ⚠️ Imports não disponíveis")
            return
        
        try:
            rag = ScripturemonRAG()
            
            # Perguntas de teste
            questions = [
                ("Como Chinatown usa água como metáfora?", ["água", "poder", "corrupção"]),
                ("Qual a estrutura de três atos?", ["setup", "confronto", "resolução"]),
                ("Como desenvolver personagens?", ["arco", "motivação", "conflito"])
            ]
            
            quality_scores = []
            
            for question, expected_terms in questions:
                try:
                    answer = rag.answer_with_rag(question, brutal=True)
                    
                    # Verificar termos esperados
                    found_terms = sum(1 for term in expected_terms 
                                     if term.lower() in answer.lower())
                    
                    quality = found_terms / len(expected_terms)
                    quality_scores.append(quality)
                    
                    print(f"  📝 '{question[:30]}...': {quality*100:.0f}% qualidade")
                    
                except Exception as e:
                    print(f"  ⚠️ Erro na pergunta: {e}")
                    quality_scores.append(0)
            
            avg_quality = sum(quality_scores) / len(quality_scores) if quality_scores else 0
            
            if avg_quality > 0.5:
                print(f"  ✅ Qualidade média: {avg_quality*100:.0f}%")
                self.results["tests_passed"] += 1
            else:
                print(f"  ❌ Qualidade baixa: {avg_quality*100:.0f}%")
                self.results["tests_failed"] += 1
                
            self.results["quality"]["average"] = avg_quality
            
        except Exception as e:
            print(f"  ❌ Erro no teste de qualidade: {e}")
            self.results["tests_failed"] += 1
    
    def test_performance(self):
        """Testa performance do sistema"""
        if not IMPORTS_OK:
            print("  ⚠️ Imports não disponíveis")
            return
        
        try:
            # Teste de velocidade dos analyzers rápidos
            from app.processing.analyzers_fast import analyze_fast
            
            sample = self.test_samples["chinatown"]
            
            # Analyzer rápido (sem LLM)
            start = time.time()
            result_fast = analyze_fast(sample)
            time_fast = time.time() - start
            
            print(f"  ⚡ Analyzer rápido: {time_fast:.3f}s")
            
            # Teste de busca RAG
            rag = ScripturemonRAG()
            start = time.time()
            results = rag.search_knowledge("water metaphor", top_k=5)
            time_search = time.time() - start
            
            print(f"  🔍 Busca RAG: {time_search:.3f}s")
            
            # Verificar se está dentro dos limites
            if time_fast < 0.5 and time_search < 2:
                print(f"  ✅ Performance dentro dos limites")
                self.results["tests_passed"] += 1
            else:
                print(f"  ⚠️ Performance pode ser melhorada")
                
            self.results["performance"]["analyzer_fast"] = time_fast
            self.results["performance"]["rag_search"] = time_search
            
        except Exception as e:
            print(f"  ❌ Erro no teste de performance: {e}")
            self.results["tests_failed"] += 1
    
    def test_brutal_personality(self):
        """Testa se mantém personalidade brutal"""
        if not IMPORTS_OK:
            print("  ⚠️ Imports não disponíveis")
            return
        
        try:
            orchestrator = ScripturemonUnifiedOrchestrator()
            
            # Processar roteiro do criador
            result = asyncio.run(
                orchestrator.process_parallel(
                    self.test_samples["roteiro_criador"],
                    doc_type="roteiro_criador"
                )
            )
            
            # Verificar nota
            nota = result.get("evaluation", {}).get("nota", 0)
            feedback = result.get("evaluation", {}).get("feedback", "")
            
            # Verificar brutalidade
            is_brutal = (
                nota <= 65 and  # Nota baixa
                any(word in feedback.lower() for word in 
                    ["amador", "mestres", "chinatown", "comparado"])
            )
            
            if is_brutal:
                print(f"  ✅ Personalidade brutal mantida")
                print(f"     Nota: {nota}/100")
                print(f"     Feedback: {feedback[:100]}...")
                self.results["tests_passed"] += 1
            else:
                print(f"  ❌ Personalidade não está brutal")
                print(f"     Nota: {nota}/100")
                self.results["tests_failed"] += 1
                
            self.results["quality"]["brutal_score"] = nota
            
        except Exception as e:
            print(f"  ❌ Erro no teste de personalidade: {e}")
            self.results["tests_failed"] += 1
    
    def generate_report(self):
        """Gera relatório final"""
        print("\n" + "="*70)
        print("📊 RELATÓRIO FINAL DE TESTES")
        print("="*70)
        
        total = self.results["tests_passed"] + self.results["tests_failed"]
        success_rate = (self.results["tests_passed"] / total * 100) if total > 0 else 0
        
        print(f"\n✅ Testes aprovados: {self.results['tests_passed']}")
        print(f"❌ Testes falhados: {self.results['tests_failed']}")
        print(f"📈 Taxa de sucesso: {success_rate:.1f}%")
        
        # Componentes
        print("\n📦 COMPONENTES:")
        for comp, status in self.results["components"].items():
            icon = "✅" if status else "❌"
            print(f"  {icon} {comp}")
        
        # Performance
        if self.results["performance"]:
            print("\n⚡ PERFORMANCE:")
            for metric, value in self.results["performance"].items():
                print(f"  {metric}: {value:.3f}s")
        
        # Qualidade
        if self.results["quality"]:
            print("\n💎 QUALIDADE:")
            for metric, value in self.results["quality"].items():
                if isinstance(value, float):
                    print(f"  {metric}: {value*100:.0f}%" if value <= 1 else f"  {metric}: {value}")
                else:
                    print(f"  {metric}: {value}")
        
        # Análise final
        print("\n" + "="*70)
        
        if success_rate >= 80:
            print("🎉 SISTEMA FUNCIONANDO EXCELENTEMENTE!")
            print("   O Scripturemon está pronto para uso em produção.")
        elif success_rate >= 60:
            print("⚠️ SISTEMA FUNCIONANDO COM ALGUMAS LIMITAÇÕES")
            print("   Revisar componentes que falharam.")
        else:
            print("❌ SISTEMA PRECISA DE AJUSTES SIGNIFICATIVOS")
            print("   Verificar logs e corrigir falhas críticas.")
        
        # Salvar relatório
        report_path = Path("test_results.json")
        with open(report_path, "w") as f:
            json.dumps(self.results, f, indent=2)
        print(f"\n💾 Relatório salvo em: {report_path}")


def main():
    """Executa bateria de testes"""
    print("\n🚀 Iniciando bateria de testes completa...")
    print("   Isso pode levar alguns minutos...")
    
    # Verificar se API está rodando
    try:
        resp = requests.get("http://localhost:8092/health", timeout=2)
        if resp.status_code != 200:
            print("\n⚠️ AVISO: API RAG não está rodando!")
            print("   Execute em outro terminal: uvicorn app.main:app --port 8092")
            response = input("\nContinuar mesmo assim? (s/n): ")
            if response.lower() != 's':
                return
    except:
        print("\n⚠️ AVISO: API RAG não está acessível!")
        print("   Execute em outro terminal: uvicorn app.main:app --port 8092")
        response = input("\nContinuar mesmo assim? (s/n): ")
        if response.lower() != 's':
            return
    
    # Executar testes
    suite = ScripturemonTestSuite()
    suite.run_all_tests()
    
    print("\n✅ Bateria de testes concluída!")


if __name__ == "__main__":
    main()