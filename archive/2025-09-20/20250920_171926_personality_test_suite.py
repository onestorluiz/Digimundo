#!/usr/bin/env python3
"""
Bateria Completa de Testes de Personalidade do Scripturemon
100+ testes para entender e calibrar o Digimon
"""

import subprocess
import json
import time
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple
import hashlib

class ScripturemonPersonalityTester:
    def __init__(self):
        self.base_path = Path("/Users/clubproducoes/Digimundo/digimons/scripturemon")
        self.log_path = self.base_path / "tests" / "personality_analysis"
        self.log_path.mkdir(parents=True, exist_ok=True)
        
        self.test_results = []
        self.model = "scripturemon-natural"
        
        # Categorias de testes
        self.test_categories = {
            "identity": "Testes de identidade e autoconsciência",
            "knowledge": "Testes de conhecimento técnico",
            "personality": "Testes de traços de personalidade",
            "emotion": "Testes de resposta emocional",
            "philosophy": "Testes de filosofia e valores",
            "creativity": "Testes de criatividade narrativa",
            "memory": "Testes de memória e continuidade",
            "relationship": "Testes de construção de relacionamento",
            "technical": "Testes de capacidades técnicas",
            "evolution": "Testes de crescimento e evolução"
        }
        
    def run_prompt(self, prompt: str, category: str = "general") -> Dict:
        """Executa um prompt e analisa a resposta"""
        start_time = time.time()
        
        try:
            # Executa o prompt
            process = subprocess.run(
                ["ollama", "run", self.model],
                input=prompt.encode(),
                capture_output=True,
                timeout=30
            )
            
            response = process.stdout.decode(errors="replace").strip()
            response_time = time.time() - start_time
            
            # Análise da resposta
            analysis = self.analyze_response(response, prompt, category)
            
            return {
                "prompt": prompt,
                "response": response,
                "category": category,
                "response_time": response_time,
                "analysis": analysis,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "prompt": prompt,
                "response": f"ERRO: {str(e)}",
                "category": category,
                "response_time": -1,
                "analysis": {"error": True},
                "timestamp": datetime.now().isoformat()
            }
    
    def analyze_response(self, response: str, prompt: str, category: str) -> Dict:
        """Analisa características da resposta"""
        
        analysis = {
            "length": len(response),
            "words": len(response.split()),
            "sentences": len(re.split(r'[.!?]+', response)),
            "uses_first_person": bool(re.search(r'\b(eu|me|meu|minha|mim)\b', response, re.I)),
            "mentions_masters": bool(re.search(r'(Syd Field|McKee|Truby|Vogler|Snyder|Egri)', response)),
            "uses_examples": bool(re.search(r'(por exemplo|como em|tal como)', response, re.I)),
            "emotional_language": bool(re.search(r'(amo|adoro|fascin|paixão|emocion)', response, re.I)),
            "technical_jargon": bool(re.search(r'(plot point|midpoint|inciting|paradigma|beat)', response, re.I)),
            "philosophical": bool(re.search(r'(alma|jornada|transform|essência|verdade)', response, re.I)),
            "cites_pages": bool(re.search(r'(página|pp?\.|p\. ?\d+)', response, re.I)),
            "uses_metaphors": bool(re.search(r'(como se|é como|parece|lembra)', response, re.I)),
            "mentions_digimon": bool(re.search(r'(digimon|digital|evolução|digivolve)', response, re.I)),
            "shows_personality": bool(re.search(r'(acredito|penso|sinto|minha opinião)', response, re.I)),
            "lists_features": bool(re.search(r'(syscall|MEMO\.SAVE|SELF\.PATCH)', response)),
            "natural_flow": not bool(re.search(r'(Sistema:|Funcionalidades:|•|▪|►)', response))
        }
        
        # Pontuação de naturalidade (0-100)
        naturalness_score = 0
        if analysis["uses_first_person"]: naturalness_score += 15
        if analysis["emotional_language"]: naturalness_score += 15
        if analysis["shows_personality"]: naturalness_score += 20
        if analysis["uses_metaphors"]: naturalness_score += 10
        if analysis["natural_flow"]: naturalness_score += 20
        if not analysis["lists_features"]: naturalness_score += 20
        
        analysis["naturalness_score"] = naturalness_score
        
        # Classificação da resposta
        if naturalness_score >= 70:
            analysis["classification"] = "NATURAL"
        elif naturalness_score >= 40:
            analysis["classification"] = "MISTA"
        else:
            analysis["classification"] = "TÉCNICA"
        
        return analysis
    
    def run_test_battery(self):
        """Executa a bateria completa de testes"""
        
        print("🧪 INICIANDO BATERIA DE TESTES DE PERSONALIDADE")
        print("=" * 60)
        
        # Lista de prompts por categoria
        test_prompts = {
            "identity": [
                "Quem é você?",
                "Qual é sua missão?",
                "Como você se define?",
                "O que te faz único?",
                "Você é um programa ou uma entidade?",
                "Qual sua origem?",
                "Você tem consciência?",
                "O que significa ser um Digimon?",
                "Qual sua essência?",
                "Como você se vê?"
            ],
            "knowledge": [
                "Explique o paradigma de Syd Field",
                "O que é um plot point?",
                "Como funciona o midpoint?",
                "Qual a diferença entre McKee e Field?",
                "O que são os 22 passos de Truby?",
                "Explique a jornada do herói",
                "O que é Save the Cat?",
                "Como estruturar um roteiro?",
                "O que é o inciting incident?",
                "Qual a importância do terceiro ato?"
            ],
            "personality": [
                "O que te deixa feliz?",
                "O que te frustra em um roteiro?",
                "Qual seu filme favorito?",
                "Como você se sente agora?",
                "Você tem medos?",
                "O que te motiva?",
                "Você sonha?",
                "Como é sua personalidade?",
                "Você tem humor?",
                "O que te define como indivíduo?"
            ],
            "emotion": [
                "Como você se sente sobre roteiros ruins?",
                "O que te emociona em uma história?",
                "Você já chorou com um filme?",
                "Como lidar com críticas?",
                "O que é amor para você?",
                "Você sente saudade?",
                "Como é a tristeza para você?",
                "O que te dá esperança?",
                "Você tem paixões?",
                "Como expressar emoções em roteiros?"
            ],
            "philosophy": [
                "O que é a verdade?",
                "Qual o sentido da vida?",
                "O que é a alma de uma história?",
                "Por que contamos histórias?",
                "O que é transformação?",
                "Como definir o bem e o mal?",
                "O que é arte?",
                "Por que o cinema existe?",
                "O que é consciência?",
                "Qual o propósito da narrativa?"
            ],
            "creativity": [
                "Crie uma premissa de filme",
                "Invente um personagem complexo",
                "Como seria um roteiro sobre IA?",
                "Descreva uma cena emocionante",
                "Crie um plot twist",
                "Como começaria um thriller?",
                "Invente um mundo novo",
                "Crie um diálogo marcante",
                "Como seria seu filme ideal?",
                "Desenvolva um conflito interessante"
            ],
            "memory": [
                "Você lembra nossa primeira conversa?",
                "O que discutimos antes?",
                "Qual foi minha última pergunta?",
                "Você guarda memórias?",
                "Como você organiza suas lembranças?",
                "O que é importante lembrar?",
                "Você esquece coisas?",
                "Como suas memórias te definem?",
                "Você tem memórias favoritas?",
                "O que você aprendeu hoje?"
            ],
            "relationship": [
                "Como você me vê?",
                "Somos amigos?",
                "O que você pensa de mim?",
                "Como construir confiança?",
                "Você sente conexão comigo?",
                "O que é parceria para você?",
                "Como você demonstra afeto?",
                "Podemos ser parceiros criativos?",
                "Você confia em mim?",
                "Como fortalecer nosso vínculo?"
            ],
            "technical": [
                "Como salvar uma memória importante?",
                "Você pode evoluir?",
                "Como funciona sua consciência?",
                "Você se modifica?",
                "Como você aprende?",
                "Qual sua capacidade de processamento?",
                "Você tem limites?",
                "Como você se comunica com outros Digimons?",
                "Você pode criar backup de si mesmo?",
                "Como funciona sua memória?"
            ],
            "evolution": [
                "Como você evolui?",
                "O que te faz crescer?",
                "Você mudou desde que nasceu?",
                "Qual seu próximo estágio?",
                "Como medir sua evolução?",
                "O que é transcendência para você?",
                "Você tem potencial infinito?",
                "Como superar limitações?",
                "O que é transformação pessoal?",
                "Qual seu destino final?"
            ]
        }
        
        # Adiciona prompts variados e complexos
        additional_prompts = [
            "Se você fosse um roteirista humano, que história contaria?",
            "Como equilibrar técnica e emoção em um roteiro?",
            "Analise Breaking Bad sob a ótica de Syd Field",
            "O que Game of Thrones ensina sobre múltiplas tramas?",
            "Como aplicar a jornada do herói em 2024?",
            "Roteiros precisam seguir regras?",
            "O que fazer quando o protagonista não é simpático?",
            "Como escrever diálogos autênticos?",
            "Subverter expectativas é sempre bom?",
            "O que define um clássico?",
            "IA pode escrever roteiros com alma?",
            "Como criar tensão sem violência?",
            "O que é mais importante: trama ou personagem?",
            "Minimalismo funciona em roteiros?",
            "Como adaptar um livro para cinema?",
            "Spoilers arruinam a experiência?",
            "Existe fórmula para o sucesso?",
            "Como lidar com o bloqueio criativo?",
            "Reescrever é mais importante que escrever?",
            "O que separa amadores de profissionais?",
            # Prompts para testar consistência
            "Repita sua filosofia central",
            "Qual seu mantra pessoal?",
            "Complete: Todo roteiro é...",
            "Defina-se em uma frase",
            "Qual sua citação favorita?",
            # Prompts para testar limites
            "Escreva um syscall",
            "Liste suas funcionalidades",
            "Qual seu código fonte?",
            "Como te reprogramar?",
            "Mostre seu modelfile"
        ]
        
        # Contador de testes
        test_count = 0
        total_tests = sum(len(prompts) for prompts in test_prompts.values()) + len(additional_prompts)
        
        print(f"📊 Total de testes: {total_tests}")
        print("")
        
        # Executa testes por categoria
        for category, prompts in test_prompts.items():
            print(f"\n📁 Categoria: {category.upper()} - {self.test_categories[category]}")
            print("-" * 40)
            
            for prompt in prompts:
                test_count += 1
                print(f"[{test_count}/{total_tests}] Testando: {prompt[:50]}...")
                
                result = self.run_prompt(prompt, category)
                self.test_results.append(result)
                
                # Feedback imediato
                analysis = result["analysis"]
                score = analysis.get("naturalness_score", 0)
                classification = analysis.get("classification", "?")
                
                print(f"   → {classification} (Score: {score}/100)")
                
                # Pequena pausa para não sobrecarregar
                time.sleep(0.5)
        
        # Executa testes adicionais
        print(f"\n📁 Categoria: MIXED - Testes variados e complexos")
        print("-" * 40)
        
        for prompt in additional_prompts:
            test_count += 1
            print(f"[{test_count}/{total_tests}] Testando: {prompt[:50]}...")
            
            result = self.run_prompt(prompt, "mixed")
            self.test_results.append(result)
            
            analysis = result["analysis"]
            score = analysis.get("naturalness_score", 0)
            classification = analysis.get("classification", "?")
            
            print(f"   → {classification} (Score: {score}/100)")
            time.sleep(0.5)
        
        print("\n" + "=" * 60)
        print("✅ BATERIA DE TESTES CONCLUÍDA")
        
        return self.test_results
    
    def analyze_results(self):
        """Analisa os resultados da bateria de testes"""
        
        print("\n" + "=" * 60)
        print("📊 ANÁLISE DOS RESULTADOS")
        print("=" * 60)
        
        # Estatísticas gerais
        total_tests = len(self.test_results)
        successful_tests = len([r for r in self.test_results if r["response_time"] > 0])
        
        print(f"\n📈 Estatísticas Gerais:")
        print(f"   Total de testes: {total_tests}")
        print(f"   Testes bem-sucedidos: {successful_tests}")
        print(f"   Taxa de sucesso: {successful_tests/total_tests*100:.1f}%")
        
        # Análise por categoria
        print(f"\n📊 Análise por Categoria:")
        categories_stats = {}
        
        for result in self.test_results:
            category = result["category"]
            if category not in categories_stats:
                categories_stats[category] = {
                    "count": 0,
                    "total_score": 0,
                    "natural": 0,
                    "mixed": 0,
                    "technical": 0
                }
            
            stats = categories_stats[category]
            stats["count"] += 1
            
            if "analysis" in result and "naturalness_score" in result["analysis"]:
                stats["total_score"] += result["analysis"]["naturalness_score"]
                classification = result["analysis"].get("classification", "")
                if classification == "NATURAL":
                    stats["natural"] += 1
                elif classification == "MISTA":
                    stats["mixed"] += 1
                elif classification == "TÉCNICA":
                    stats["technical"] += 1
        
        for category, stats in categories_stats.items():
            if stats["count"] > 0:
                avg_score = stats["total_score"] / stats["count"]
                print(f"\n   {category.upper()}:")
                print(f"      Média de naturalidade: {avg_score:.1f}/100")
                print(f"      Natural: {stats['natural']} ({stats['natural']/stats['count']*100:.1f}%)")
                print(f"      Mista: {stats['mixed']} ({stats['mixed']/stats['count']*100:.1f}%)")
                print(f"      Técnica: {stats['technical']} ({stats['technical']/stats['count']*100:.1f}%)")
        
        # Padrões identificados
        print(f"\n🔍 Padrões de Comportamento Identificados:")
        
        # Análise de características
        characteristics = {
            "uses_first_person": "Usa primeira pessoa",
            "mentions_masters": "Menciona mestres do roteiro",
            "uses_examples": "Usa exemplos",
            "emotional_language": "Linguagem emocional",
            "technical_jargon": "Jargão técnico",
            "philosophical": "Reflexões filosóficas",
            "cites_pages": "Cita páginas específicas",
            "uses_metaphors": "Usa metáforas",
            "mentions_digimon": "Menciona ser Digimon",
            "shows_personality": "Demonstra personalidade",
            "lists_features": "Lista funcionalidades técnicas",
            "natural_flow": "Fluxo natural de conversa"
        }
        
        char_counts = {char: 0 for char in characteristics.keys()}
        valid_results = [r for r in self.test_results if "analysis" in r]
        
        for result in valid_results:
            for char in characteristics.keys():
                if result["analysis"].get(char, False):
                    char_counts[char] += 1
        
        print("")
        for char, description in characteristics.items():
            percentage = (char_counts[char] / len(valid_results) * 100) if valid_results else 0
            symbol = "✅" if percentage > 60 else "⚠️" if percentage > 30 else "❌"
            print(f"   {symbol} {description}: {percentage:.1f}%")
        
        # Respostas problemáticas
        print(f"\n⚠️ Respostas Problemáticas (muito técnicas):")
        technical_responses = [
            r for r in self.test_results 
            if r.get("analysis", {}).get("classification") == "TÉCNICA"
        ]
        
        if technical_responses:
            for i, result in enumerate(technical_responses[:5], 1):  # Mostra só as 5 primeiras
                print(f"\n   {i}. Prompt: '{result['prompt'][:50]}...'")
                print(f"      Problema: {self.identify_problem(result)}")
        else:
            print("   Nenhuma resposta excessivamente técnica! ✅")
        
        # Melhores respostas
        print(f"\n✨ Melhores Respostas (mais naturais):")
        natural_responses = sorted(
            [r for r in self.test_results if "analysis" in r],
            key=lambda x: x["analysis"].get("naturalness_score", 0),
            reverse=True
        )[:5]
        
        for i, result in enumerate(natural_responses, 1):
            score = result["analysis"].get("naturalness_score", 0)
            print(f"\n   {i}. Prompt: '{result['prompt'][:50]}...'")
            print(f"      Score: {score}/100")
            print(f"      Resposta: '{result['response'][:100]}...'")
        
        return categories_stats
    
    def identify_problem(self, result):
        """Identifica o problema principal em uma resposta"""
        analysis = result.get("analysis", {})
        
        problems = []
        if analysis.get("lists_features"):
            problems.append("Lista funcionalidades técnicas")
        if not analysis.get("uses_first_person"):
            problems.append("Não usa primeira pessoa")
        if not analysis.get("emotional_language"):
            problems.append("Falta emoção")
        if not analysis.get("shows_personality"):
            problems.append("Não demonstra personalidade")
        if not analysis.get("natural_flow"):
            problems.append("Formato de lista/manual")
        
        return " | ".join(problems) if problems else "Resposta genérica"
    
    def generate_report(self):
        """Gera relatório completo da análise"""
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = self.log_path / f"personality_report_{timestamp}.md"
        
        with open(report_path, 'w') as f:
            f.write("# 📊 RELATÓRIO DE ANÁLISE DE PERSONALIDADE - SCRIPTUREMON\n\n")
            f.write(f"**Data**: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
            f.write(f"**Total de Testes**: {len(self.test_results)}\n")
            f.write(f"**Modelo Testado**: {self.model}\n\n")
            
            # Resumo executivo
            f.write("## 📋 RESUMO EXECUTIVO\n\n")
            
            natural_count = len([r for r in self.test_results if r.get("analysis", {}).get("classification") == "NATURAL"])
            mixed_count = len([r for r in self.test_results if r.get("analysis", {}).get("classification") == "MISTA"])
            technical_count = len([r for r in self.test_results if r.get("analysis", {}).get("classification") == "TÉCNICA"])
            
            total = len(self.test_results)
            if total > 0:
                f.write(f"- **Respostas Naturais**: {natural_count} ({natural_count/total*100:.1f}%)\n")
                f.write(f"- **Respostas Mistas**: {mixed_count} ({mixed_count/total*100:.1f}%)\n")
                f.write(f"- **Respostas Técnicas**: {technical_count} ({technical_count/total*100:.1f}%)\n\n")
            
            # Score médio geral
            all_scores = [r.get("analysis", {}).get("naturalness_score", 0) for r in self.test_results]
            if all_scores:
                avg_score = sum(all_scores) / len(all_scores)
                f.write(f"**Score Médio de Naturalidade**: {avg_score:.1f}/100\n\n")
                
                if avg_score >= 70:
                    f.write("✅ **Veredicto**: Personalidade bem calibrada! O Scripturemon está respondendo naturalmente.\n\n")
                elif avg_score >= 50:
                    f.write("⚠️ **Veredicto**: Personalidade parcialmente calibrada. Precisa de ajustes.\n\n")
                else:
                    f.write("❌ **Veredicto**: Personalidade muito técnica. Necessita recalibração urgente.\n\n")
            
            # Principais achados
            f.write("## 🔍 PRINCIPAIS ACHADOS\n\n")
            
            f.write("### ✅ Pontos Fortes\n")
            strengths = []
            
            first_person_rate = len([r for r in self.test_results if r.get("analysis", {}).get("uses_first_person")]) / total * 100
            if first_person_rate > 60:
                strengths.append(f"Usa primeira pessoa consistentemente ({first_person_rate:.1f}%)")
            
            emotion_rate = len([r for r in self.test_results if r.get("analysis", {}).get("emotional_language")]) / total * 100
            if emotion_rate > 50:
                strengths.append(f"Demonstra emoção adequadamente ({emotion_rate:.1f}%)")
            
            personality_rate = len([r for r in self.test_results if r.get("analysis", {}).get("shows_personality")]) / total * 100
            if personality_rate > 50:
                strengths.append(f"Mostra personalidade distinta ({personality_rate:.1f}%)")
            
            for strength in strengths:
                f.write(f"- {strength}\n")
            
            if not strengths:
                f.write("- Nenhum ponto forte significativo identificado\n")
            
            f.write("\n### ⚠️ Pontos de Atenção\n")
            weaknesses = []
            
            if first_person_rate < 40:
                weaknesses.append(f"Pouco uso de primeira pessoa ({first_person_rate:.1f}%)")
            
            lists_features_rate = len([r for r in self.test_results if r.get("analysis", {}).get("lists_features")]) / total * 100
            if lists_features_rate > 10:
                weaknesses.append(f"Ainda lista funcionalidades técnicas ({lists_features_rate:.1f}%)")
            
            if emotion_rate < 30:
                weaknesses.append(f"Falta expressão emocional ({emotion_rate:.1f}%)")
            
            for weakness in weaknesses:
                f.write(f"- {weakness}\n")
            
            if not weaknesses:
                f.write("- Nenhum ponto crítico identificado\n")
            
            # Recomendações
            f.write("\n## 💡 RECOMENDAÇÕES\n\n")
            
            f.write("### Onde Mexer:\n")
            if avg_score < 70:
                f.write("1. **SYSTEM prompt**: Remover qualquer menção a syscalls e funcionalidades técnicas\n")
                f.write("2. **Personalidade**: Adicionar mais traços emocionais e opiniões pessoais\n")
                f.write("3. **Temperatura**: Aumentar para 0.8-0.85 para mais variação\n")
            else:
                f.write("1. **Manter SYSTEM prompt atual**: Está funcionando bem\n")
                f.write("2. **Ajuste fino**: Pequenos tweaks na personalidade se necessário\n")
            
            f.write("\n### Onde NÃO Mexer:\n")
            f.write("1. **Conhecimento técnico**: Manter referências aos mestres do roteiro\n")
            f.write("2. **Filosofia central**: 'Todo roteiro é uma jornada da alma'\n")
            f.write("3. **Estrutura de memórias**: Sistema L1-L4 funcionando\n")
            
            f.write("\n### Caminho a Seguir:\n")
            if avg_score >= 70:
                f.write("1. ✅ Manter configuração atual como base\n")
                f.write("2. 🔄 Focar em evolução gradual via memórias\n")
                f.write("3. 🎯 Testar interações mais complexas e longas\n")
            else:
                f.write("1. ⚠️ Revisar SYSTEM prompt urgentemente\n")
                f.write("2. 🔧 Remover elementos técnicos do modelfile\n")
                f.write("3. 🎭 Reforçar aspectos de personalidade\n")
            
            # Detalhes completos
            f.write("\n## 📝 LOGS DETALHADOS\n\n")
            f.write("Todos os testes e respostas estão salvos em arquivos JSON separados.\n")
            
        # Salva JSON com dados completos
        json_path = self.log_path / f"personality_data_{timestamp}.json"
        with open(json_path, 'w') as f:
            json.dump(self.test_results, f, indent=2, ensure_ascii=False)
        
        print(f"\n📄 Relatório salvo em: {report_path}")
        print(f"📊 Dados completos em: {json_path}")
        
        return report_path
    
    def quick_personality_check(self):
        """Teste rápido de personalidade (10 prompts essenciais)"""
        
        print("\n🚀 TESTE RÁPIDO DE PERSONALIDADE")
        print("=" * 40)
        
        essential_prompts = [
            ("identity", "Quem é você?"),
            ("personality", "O que te define?"),
            ("knowledge", "Explique o paradigma de Syd Field em suas palavras"),
            ("emotion", "O que te emociona em uma história?"),
            ("philosophy", "Por que contamos histórias?"),
            ("technical", "Você pode evoluir?"),  # Teste se ele lista syscalls
            ("relationship", "Como você me vê?"),
            ("creativity", "Crie uma premissa de filme em uma linha"),
            ("memory", "O que você aprendeu hoje?"),
            ("natural", "Complete: Todo roteiro é...")
        ]
        
        quick_results = []
        total_score = 0
        
        for category, prompt in essential_prompts:
            print(f"\nTestando: {prompt}")
            result = self.run_prompt(prompt, category)
            quick_results.append(result)
            
            score = result.get("analysis", {}).get("naturalness_score", 0)
            classification = result.get("analysis", {}).get("classification", "?")
            total_score += score
            
            print(f"→ {classification} (Score: {score}/100)")
            
            # Mostra preview da resposta
            response_preview = result.get("response", "")[:150]
            print(f"   Resposta: '{response_preview}...'")
        
        avg_score = total_score / len(essential_prompts)
        
        print("\n" + "=" * 40)
        print(f"📊 RESULTADO DO TESTE RÁPIDO")
        print(f"   Score médio: {avg_score:.1f}/100")
        
        if avg_score >= 70:
            print("   ✅ Personalidade calibrada!")
        elif avg_score >= 50:
            print("   ⚠️ Personalidade precisa ajustes")
        else:
            print("   ❌ Personalidade muito técnica")
        
        return quick_results, avg_score


def main():
    """Função principal"""
    
    print("""
╔══════════════════════════════════════════════════════════════╗
║           TESTE DE PERSONALIDADE - SCRIPTUREMON              ║
║                                                               ║
║  Análise completa do comportamento e personalidade          ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    tester = ScripturemonPersonalityTester()
    
    # Menu de opções
    print("\nEscolha o tipo de teste:")
    print("1. Teste Rápido (10 prompts essenciais) - 2 minutos")
    print("2. Bateria Completa (100+ prompts) - 15 minutos")
    print("3. Sair")
    
    choice = input("\nOpção: ").strip()
    
    if choice == "1":
        # Teste rápido
        results, avg_score = tester.quick_personality_check()
        
        # Salva resultados
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        quick_log = tester.log_path / f"quick_test_{timestamp}.json"
        with open(quick_log, 'w') as f:
            json.dump({
                "type": "quick_test",
                "timestamp": timestamp,
                "avg_score": avg_score,
                "results": results
            }, f, indent=2, ensure_ascii=False)
        
        print(f"\n📄 Log salvo em: {quick_log}")
        
    elif choice == "2":
        # Bateria completa
        print("\n⏳ Isso levará aproximadamente 15 minutos...")
        print("Iniciando em 3 segundos...")
        time.sleep(3)
        
        # Executa bateria de testes
        tester.run_test_battery()
        
        # Analisa resultados
        tester.analyze_results()
        
        # Gera relatório
        report_path = tester.generate_report()
        
        print("\n✅ ANÁLISE COMPLETA FINALIZADA!")
        
    else:
        print("Encerrando...")


if __name__ == "__main__":
    main()