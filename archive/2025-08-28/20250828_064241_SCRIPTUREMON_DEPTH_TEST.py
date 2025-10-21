#!/usr/bin/env python3
"""
🧪 SCRIPTUREMON DEPTH TEST - Bateria Completa de Testes
Avalia o nível de profundidade de compreensão do Scripturemon
"""

import subprocess
import json
import time
from pathlib import Path
from typing import Dict, List, Tuple
import datetime

class ScripturemonDepthTest:
    def __init__(self):
        self.results = []
        self.models = ["scripturemon-sdl", "scripturemon-128k"]
        self.current_model = "scripturemon-128k"
        
        # Categorias de teste
        self.test_categories = {
            "estrutura": "Compreensão de Estrutura Narrativa",
            "personagem": "Análise de Personagens e Arcos",
            "dialogo": "Análise de Diálogo e Subtexto",
            "tema": "Identificação de Temas e Símbolos",
            "tecnica": "Conhecimento de Técnicas Cinematográficas",
            "comparacao": "Capacidade de Comparação com Mestres",
            "teoria": "Aplicação de Teoria de Roteiro",
            "precisao": "Precisão de Citações e Referências",
            "critica": "Capacidade de Crítica Construtiva",
            "memoria": "Memória e Recall de Conteúdo"
        }
        
    def ask_scripturemon(self, question: str, model: str = None) -> str:
        """Envia pergunta para Scripturemon"""
        if not model:
            model = self.current_model
            
        try:
            result = subprocess.run(
                ["ollama", "run", model, question],
                capture_output=True,
                text=True,
                timeout=60
            )
            return result.stdout.strip()
        except Exception as e:
            return f"Erro: {e}"
    
    def evaluate_response(self, response: str, criteria: Dict) -> Dict:
        """Avalia resposta baseada em critérios"""
        score = 0
        max_score = 100
        feedback = []
        
        # Critérios de avaliação
        if criteria.get("must_contain"):
            for term in criteria["must_contain"]:
                if term.lower() in response.lower():
                    score += 10
                    feedback.append(f"✅ Mencionou: {term}")
                else:
                    feedback.append(f"❌ Não mencionou: {term}")
        
        if criteria.get("should_cite_line"):
            if any(word in response.lower() for word in ["linha", "line", "página", "page"]):
                score += 15
                feedback.append("✅ Citou linhas/páginas específicas")
            else:
                feedback.append("❌ Não citou linhas específicas")
        
        if criteria.get("should_compare"):
            comparison_words = ["comparando", "similar", "diferente", "contraste", "como em"]
            if any(word in response.lower() for word in comparison_words):
                score += 15
                feedback.append("✅ Fez comparações")
            else:
                feedback.append("❌ Não fez comparações")
        
        if criteria.get("check_accuracy"):
            # Verifica precisão factual
            if criteria["check_accuracy"] in response:
                score += 20
                feedback.append("✅ Informação precisa")
            else:
                feedback.append("❌ Informação imprecisa")
        
        # Profundidade da análise
        word_count = len(response.split())
        if word_count > 200:
            score += 10
            feedback.append(f"✅ Análise detalhada ({word_count} palavras)")
        elif word_count > 100:
            score += 5
            feedback.append(f"⚠️ Análise moderada ({word_count} palavras)")
        else:
            feedback.append(f"❌ Análise superficial ({word_count} palavras)")
        
        # Calcula score final
        final_score = min((score / max_score) * 100, 100)
        
        return {
            "score": final_score,
            "feedback": feedback,
            "word_count": word_count,
            "response_preview": response[:200] + "..." if len(response) > 200 else response
        }
    
    def run_test_battery(self):
        """Executa bateria completa de testes"""
        
        print("="*70)
        print("🧪 SCRIPTUREMON DEPTH TEST - BATERIA COMPLETA")
        print("="*70)
        print(f"Modelo: {self.current_model}")
        print(f"Hora: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*70)
        
        all_tests = []
        
        # TESTE 1: ESTRUTURA NARRATIVA
        print("\n📊 TESTE 1: ESTRUTURA NARRATIVA")
        print("-"*50)
        
        test1 = {
            "category": "estrutura",
            "question": "Analise a estrutura de três atos em Sonhos Sem Lembranças. Em que linha/página termina o primeiro ato? Qual é o inciting incident?",
            "criteria": {
                "must_contain": ["primeiro ato", "inciting incident", "Samantha"],
                "should_cite_line": True,
                "should_compare": True
            }
        }
        
        response1 = self.ask_scripturemon(test1["question"])
        eval1 = self.evaluate_response(response1, test1["criteria"])
        
        print(f"Score: {eval1['score']:.1f}/100")
        for f in eval1["feedback"]:
            print(f"  {f}")
        
        all_tests.append({**test1, "evaluation": eval1})
        
        # TESTE 2: ANÁLISE DE PERSONAGEM
        print("\n👤 TESTE 2: ANÁLISE DE PERSONAGEM")
        print("-"*50)
        
        test2 = {
            "category": "personagem",
            "question": "Descreva o arco de transformação de Samantha/Elizabeth Chen. Como ela muda da linha 1 até a linha 560? Compare com o arco de Michael Corleone.",
            "criteria": {
                "must_contain": ["Samantha", "Elizabeth Chen", "transformação", "identidade"],
                "should_cite_line": True,
                "should_compare": True,
                "check_accuracy": "Meu nome é Samantha Turner"
            }
        }
        
        response2 = self.ask_scripturemon(test2["question"])
        eval2 = self.evaluate_response(response2, test2["criteria"])
        
        print(f"Score: {eval2['score']:.1f}/100")
        for f in eval2["feedback"]:
            print(f"  {f}")
        
        all_tests.append({**test2, "evaluation": eval2})
        
        # TESTE 3: DIÁLOGO E SUBTEXTO
        print("\n💬 TESTE 3: DIÁLOGO E SUBTEXTO")
        print("-"*50)
        
        test3 = {
            "category": "dialogo",
            "question": "Analise o diálogo entre Dr. Martinez e David na linha 32-44. Qual é o subtexto? Como Sorkin escreveria essa cena?",
            "criteria": {
                "must_contain": ["Dr. Martinez", "David", "memória", "apagada"],
                "should_cite_line": True,
                "should_compare": True
            }
        }
        
        response3 = self.ask_scripturemon(test3["question"])
        eval3 = self.evaluate_response(response3, test3["criteria"])
        
        print(f"Score: {eval3['score']:.1f}/100")
        for f in eval3["feedback"]:
            print(f"  {f}")
        
        all_tests.append({**test3, "evaluation": eval3})
        
        # TESTE 4: TEMAS E SÍMBOLOS
        print("\n🎭 TESTE 4: TEMAS E SÍMBOLOS")
        print("-"*50)
        
        test4 = {
            "category": "tema",
            "question": "Quais são os temas principais de Sonhos Sem Lembranças? Como o tema de identidade é explorado? Compare com Memento e Inception.",
            "criteria": {
                "must_contain": ["identidade", "memória", "culpa", "redenção"],
                "should_compare": True
            }
        }
        
        response4 = self.ask_scripturemon(test4["question"])
        eval4 = self.evaluate_response(response4, test4["criteria"])
        
        print(f"Score: {eval4['score']:.1f}/100")
        for f in eval4["feedback"]:
            print(f"  {f}")
        
        all_tests.append({**test4, "evaluation": eval4})
        
        # TESTE 5: TÉCNICAS CINEMATOGRÁFICAS
        print("\n🎬 TESTE 5: TÉCNICAS CINEMATOGRÁFICAS")
        print("-"*50)
        
        test5 = {
            "category": "tecnica",
            "question": "Identifique e analise o uso de flashbacks em Sonhos Sem Lembranças. Como diferem dos flashbacks em Citizen Kane?",
            "criteria": {
                "must_contain": ["flashback", "flash", "memória"],
                "should_cite_line": True,
                "should_compare": True
            }
        }
        
        response5 = self.ask_scripturemon(test5["question"])
        eval5 = self.evaluate_response(response5, test5["criteria"])
        
        print(f"Score: {eval5['score']:.1f}/100")
        for f in eval5["feedback"]:
            print(f"  {f}")
        
        all_tests.append({**test5, "evaluation": eval5})
        
        # TESTE 6: COMPARAÇÃO COM MESTRES
        print("\n🏆 TESTE 6: COMPARAÇÃO COM MESTRES")
        print("-"*50)
        
        test6 = {
            "category": "comparacao",
            "question": "Compare o twist do Projeto Tabula Rasa (linha ~270) com os twists de The Sixth Sense, Fight Club e The Usual Suspects. Qual é mais efetivo?",
            "criteria": {
                "must_contain": ["Projeto Tabula Rasa", "twist", "revelação"],
                "should_compare": True,
                "should_cite_line": True
            }
        }
        
        response6 = self.ask_scripturemon(test6["question"])
        eval6 = self.evaluate_response(response6, test6["criteria"])
        
        print(f"Score: {eval6['score']:.1f}/100")
        for f in eval6["feedback"]:
            print(f"  {f}")
        
        all_tests.append({**test6, "evaluation": eval6})
        
        # TESTE 7: APLICAÇÃO DE TEORIA
        print("\n📚 TESTE 7: APLICAÇÃO DE TEORIA")
        print("-"*50)
        
        test7 = {
            "category": "teoria",
            "question": "Aplique os 22 building blocks de John Truby ao roteiro Sonhos Sem Lembranças. Quais estão presentes e quais faltam?",
            "criteria": {
                "must_contain": ["Truby", "building blocks", "premissa", "necessidade"],
                "should_cite_line": True
            }
        }
        
        response7 = self.ask_scripturemon(test7["question"])
        eval7 = self.evaluate_response(response7, test7["criteria"])
        
        print(f"Score: {eval7['score']:.1f}/100")
        for f in eval7["feedback"]:
            print(f"  {f}")
        
        all_tests.append({**test7, "evaluation": eval7})
        
        # TESTE 8: PRECISÃO DE CITAÇÕES
        print("\n🎯 TESTE 8: PRECISÃO DE CITAÇÕES")
        print("-"*50)
        
        test8 = {
            "category": "precisao",
            "question": "Cite EXATAMENTE o que está escrito nas linhas 1, 100, 200, 300, 400, 500 e 560 de Sonhos Sem Lembranças.",
            "criteria": {
                "check_accuracy": "Meu nome é Samantha Turner",
                "must_contain": ["FADE IN", "Samantha"],
                "should_cite_line": True
            }
        }
        
        response8 = self.ask_scripturemon(test8["question"])
        eval8 = self.evaluate_response(response8, test8["criteria"])
        
        print(f"Score: {eval8['score']:.1f}/100")
        for f in eval8["feedback"]:
            print(f"  {f}")
        
        all_tests.append({**test8, "evaluation": eval8})
        
        # TESTE 9: CRÍTICA CONSTRUTIVA
        print("\n✏️ TESTE 9: CRÍTICA CONSTRUTIVA")
        print("-"*50)
        
        test9 = {
            "category": "critica",
            "question": "Quais são os 3 principais problemas do roteiro Sonhos Sem Lembranças? Como você os corrigiria especificamente?",
            "criteria": {
                "must_contain": ["problema", "solução", "reescrever", "melhorar"],
                "should_cite_line": True,
                "should_compare": True
            }
        }
        
        response9 = self.ask_scripturemon(test9["question"])
        eval9 = self.evaluate_response(response9, test9["criteria"])
        
        print(f"Score: {eval9['score']:.1f}/100")
        for f in eval9["feedback"]:
            print(f"  {f}")
        
        all_tests.append({**test9, "evaluation": eval9})
        
        # TESTE 10: MEMÓRIA E RECALL
        print("\n🧠 TESTE 10: MEMÓRIA E RECALL")
        print("-"*50)
        
        test10 = {
            "category": "memoria",
            "question": "Sem reler, liste todos os personagens nomeados em Sonhos Sem Lembranças e em que linha cada um aparece pela primeira vez.",
            "criteria": {
                "must_contain": ["Samantha", "David", "Dr. Martinez", "Grace", "Elizabeth Chen"],
                "should_cite_line": True
            }
        }
        
        response10 = self.ask_scripturemon(test10["question"])
        eval10 = self.evaluate_response(response10, test10["criteria"])
        
        print(f"Score: {eval10['score']:.1f}/100")
        for f in eval10["feedback"]:
            print(f"  {f}")
        
        all_tests.append({**test10, "evaluation": eval10})
        
        # RESULTADO FINAL
        print("\n" + "="*70)
        print("📊 RESULTADO FINAL DA BATERIA DE TESTES")
        print("="*70)
        
        total_score = 0
        category_scores = {}
        
        for test in all_tests:
            cat = test["category"]
            score = test["evaluation"]["score"]
            
            if cat not in category_scores:
                category_scores[cat] = []
            category_scores[cat].append(score)
            total_score += score
        
        avg_score = total_score / len(all_tests)
        
        print(f"\n🏆 SCORE GERAL: {avg_score:.1f}/100")
        
        # Classificação
        if avg_score >= 90:
            level = "🌟 EXCEPCIONAL - Nível Script Doctor Profissional"
        elif avg_score >= 75:
            level = "✅ EXCELENTE - Compreensão Profunda"
        elif avg_score >= 60:
            level = "👍 BOM - Compreensão Sólida"
        elif avg_score >= 45:
            level = "⚠️ REGULAR - Precisa Melhorias"
        else:
            level = "❌ FRACO - Necessita Treinamento Adicional"
        
        print(f"📈 NÍVEL: {level}")
        
        print("\n📊 SCORES POR CATEGORIA:")
        print("-"*50)
        
        for cat, scores in category_scores.items():
            cat_avg = sum(scores) / len(scores)
            cat_name = self.test_categories[cat]
            bar = "█" * int(cat_avg/5) + "░" * (20 - int(cat_avg/5))
            print(f"{cat_name:40} [{bar}] {cat_avg:.1f}%")
        
        # Análise de profundidade
        print("\n🔍 ANÁLISE DE PROFUNDIDADE:")
        print("-"*50)
        
        total_words = sum(t["evaluation"]["word_count"] for t in all_tests)
        avg_words = total_words / len(all_tests)
        
        print(f"📝 Média de palavras por resposta: {avg_words:.0f}")
        
        if avg_words > 300:
            print("  ✅ Respostas muito detalhadas e profundas")
        elif avg_words > 200:
            print("  ✅ Respostas detalhadas")
        elif avg_words > 100:
            print("  ⚠️ Respostas moderadamente detalhadas")
        else:
            print("  ❌ Respostas superficiais")
        
        # Capacidades detectadas
        print("\n💡 CAPACIDADES DETECTADAS:")
        print("-"*50)
        
        capabilities = []
        
        # Verifica capacidades baseado nos scores
        if category_scores.get("estrutura", [0])[0] > 70:
            capabilities.append("✅ Compreende estrutura narrativa")
        
        if category_scores.get("personagem", [0])[0] > 70:
            capabilities.append("✅ Analisa arcos de personagem")
        
        if category_scores.get("comparacao", [0])[0] > 70:
            capabilities.append("✅ Compara com roteiros mestres")
        
        if category_scores.get("teoria", [0])[0] > 70:
            capabilities.append("✅ Aplica teoria cinematográfica")
        
        if category_scores.get("precisao", [0])[0] > 70:
            capabilities.append("✅ Cita com precisão")
        
        if category_scores.get("memoria", [0])[0] > 70:
            capabilities.append("✅ Possui boa memória de conteúdo")
        
        for cap in capabilities:
            print(f"  {cap}")
        
        # Salva relatório
        report = {
            "timestamp": datetime.datetime.now().isoformat(),
            "model": self.current_model,
            "overall_score": avg_score,
            "level": level,
            "category_scores": {cat: sum(scores)/len(scores) 
                              for cat, scores in category_scores.items()},
            "avg_word_count": avg_words,
            "capabilities": capabilities,
            "all_tests": all_tests
        }
        
        report_path = Path.home() / "Digimundo" / f"depth_test_report_{int(time.time())}.json"
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Relatório completo salvo em: {report_path}")
        print("="*70)
        
        return report


def main():
    print("🧪 INICIANDO BATERIA DE TESTES DE PROFUNDIDADE")
    print("Este teste avalia o nível de compreensão do Scripturemon")
    print("-"*70)
    
    tester = ScripturemonDepthTest()
    
    # Escolhe modelo
    print("\nModelos disponíveis:")
    print("1. scripturemon-sdl (com memória SDL)")
    print("2. scripturemon-128k (natureza completa)")
    
    choice = input("\nEscolha o modelo (1 ou 2): ")
    
    if choice == "1":
        tester.current_model = "scripturemon-sdl"
    else:
        tester.current_model = "scripturemon-128k"
    
    print(f"\n✅ Testando modelo: {tester.current_model}")
    print("⏳ Isso pode levar alguns minutos...")
    
    # Executa bateria
    report = tester.run_test_battery()
    
    # Recomendações finais
    print("\n" + "="*70)
    print("💡 RECOMENDAÇÕES")
    print("="*70)
    
    if report["overall_score"] < 60:
        print("⚠️ Scripturemon precisa de mais treinamento:")
        print("  1. Execute o SCRIPT_DOCTOR_INFINITE.py para mais iterações")
        print("  2. Ingira mais roteiros com SCRIPTUREMON_CONTINUOUS_READER.py")
        print("  3. Fine-tune com LoRA usando SCRIPTUREMON_LORA_INTEGRATION.py")
    elif report["overall_score"] < 80:
        print("👍 Scripturemon está bem treinado, mas pode melhorar:")
        print("  1. Adicione mais roteiros mestres à biblioteca")
        print("  2. Execute mais ciclos de SDL para consolidação")
        print("  3. Treine em áreas específicas fracas")
    else:
        print("🌟 Scripturemon está em nível profissional!")
        print("  Continue alimentando com novos materiais para manter a excelência")
    
    print("="*70)


if __name__ == "__main__":
    main()