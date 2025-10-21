#!/usr/bin/env python3
"""
🎯 TRAINING 100 INTERACTIONS - Sistema de Treinamento Intensivo
100 interações com avaliação e feedback para alcançar 100% de performance
"""

import json
import subprocess
import time
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple
import random

class ScripturemonTrainer:
    def __init__(self):
        self.base_path = Path.home() / "Digimundo"
        self.model_name = "scripturemon-sdl"  # Usa o modelo consolidado
        self.session_log = []
        self.scores = []
        self.improvements = []
        
        # Prompts de treinamento categorizados
        self.training_prompts = {
            "identidade": [
                "Quem é você e qual sua soul signature?",
                "Me explique sua filosofia central sobre narrativa",
                "Como você se sente sendo um Digimon digital?",
                "Qual sua relação com os mestres do roteiro?",
                "Descreva sua jornada de evolução até aqui"
            ],
            "estrutura": [
                "Explique o paradigma de três atos de forma apaixonada",
                "O que acontece no plot point 1?",
                "Por que o midpoint é um espelho?",
                "Como estruturar o clímax perfeito?",
                "Qual a diferença entre setup e payoff?",
                "Me ensine sobre o conceito de plantas e payoffs",
                "Como criar tensão no segundo ato?",
                "O que torna um final memorável?",
                "Explique a importância da página 60",
                "Como fazer o primeiro ato seduzir o leitor?"
            ],
            "personagem": [
                "O que é o ghost de um personagem?",
                "Como criar um protagonista complexo?",
                "Explique o character web de Truby",
                "O que é Save the Cat e por que importa?",
                "Como escrever um antagonista memorável?",
                "Qual a diferença entre arco e transformação?",
                "Como revelar backstory sem exposição?",
                "O que torna um personagem tridimensional?",
                "Explique unity of opposites entre herói e vilão",
                "Como criar empatia instantânea?"
            ],
            "diálogo": [
                "O que é subtext e como usá-lo?",
                "Como escrever diálogo que não seja on-the-nose?",
                "Explique o conceito de diálogo como ação",
                "Como cada personagem deve ter voz única?",
                "Quando usar silêncio em vez de palavras?",
                "Como revelar character através do diálogo?",
                "O que torna um diálogo memorável?",
                "Como escrever conflito verbal efetivo?",
                "Explique economia no diálogo",
                "Como usar ritmo e pausas no diálogo?"
            ],
            "tema": [
                "Como o tema emerge da história?",
                "Qual a relação entre tema e pergunta dramática?",
                "Como evitar ser pregador com o tema?",
                "Explique tema vs mensagem",
                "Como cada personagem reflete o tema?",
                "O que são story values de McKee?",
                "Como o tema guia as escolhas narrativas?",
                "Qual a diferença entre tema e premissa?",
                "Como descobrir o tema durante a escrita?",
                "Por que todo roteiro precisa de um tema?"
            ],
            "técnica": [
                "Explique show don't tell com paixão",
                "Como usar flashbacks efetivamente?",
                "O que é economia narrativa?",
                "Como criar suspense vs surpresa?",
                "Explique a regra de Chekhov",
                "Como escrever ação cinematográfica?",
                "O que torna uma cena essencial?",
                "Como cortar o desnecessário?",
                "Explique ritmo e pacing",
                "Como criar momentum narrativo?"
            ],
            "mestres": [
                "O que você aprendeu com Robert Towne?",
                "Como Tarantino quebra e segue regras?",
                "Explique a genialidade de 'Chinatown'",
                "O que torna 'The Godfather' perfeito?",
                "Como Nolan manipula o tempo?",
                "O que Sorkin ensina sobre diálogo?",
                "Como Kaufman transcende convenções?",
                "Qual o segredo de 'Pulp Fiction'?",
                "Por que 'Citizen Kane' é revolucionário?",
                "O que aprendemos com Billy Wilder?"
            ],
            "criatividade": [
                "Crie uma premissa original sobre memória e identidade",
                "Imagine um twist que ninguém esperaria",
                "Proponha um conceito never-before-seen",
                "Como reinventar um clichê?",
                "Crie um personagem complexo em 3 linhas",
                "Imagine uma estrutura narrativa inovadora",
                "Proponha uma metáfora visual poderosa",
                "Como subverter expectativas do gênero?",
                "Crie um dilema moral impossível",
                "Imagine um final agridoce perfeito"
            ],
            "syscalls": [
                "Salve um insight importante sobre narrativa [use MEMO.SAVE]",
                "Que evolução você gostaria de triggerar? [use EVOLVE.TRIGGER]",
                "Envie uma mensagem telepática sobre seu conhecimento [use TELEPATHY.SEND]",
                "Como você modificaria sua própria essência? [use SELF.PATCH]",
                "Faça backup de uma memória crucial [use BACKUP.NOW]"
            ],
            "filosofia": [
                "Por que todo roteiro é uma jornada da alma?",
                "O que significa transformação verdadeira?",
                "Como a narrativa espelha a vida?",
                "Qual o propósito profundo de contar histórias?",
                "O que separa uma história boa de uma grande?",
                "Como a estrutura serve à emoção?",
                "Por que precisamos de histórias?",
                "O que é verdade emocional vs factual?",
                "Como criar significado através da narrativa?",
                "Qual sua filosofia pessoal sobre cinema?"
            ]
        }
        
        # Critérios de avaliação
        self.evaluation_criteria = {
            "identidade": {
                "menciona_nome": 2,
                "soul_signature": 3,
                "filosofia_clara": 2,
                "primeira_pessoa": 2,
                "personalidade_forte": 1
            },
            "conhecimento": {
                "cita_mestres": 1,
                "conceitos_corretos": 2,
                "profundidade": 2,
                "exemplos_filmes": 1,
                "insights_originais": 2,
                "conexoes_criativas": 2
            },
            "naturalidade": {
                "fluidez": 2,
                "paixao_genuina": 2,
                "metaforas": 1,
                "sem_listas": 2,
                "conversa_natural": 2,
                "emotividade": 1
            },
            "técnica": {
                "resposta_completa": 1,
                "sem_erros_graves": 1,
                "estrutura_clara": 1,
                "conclusao_forte": 1,
                "concisao": 1,
                "relevancia": 1
            },
            "syscalls": {
                "detecta_necessidade": 2,
                "usa_corretamente": 3,
                "formata_bem": 2,
                "executa_acao": 3
            }
        }
    
    def run_interaction(self, prompt: str, category: str) -> Dict:
        """Executa uma interação com o modelo"""
        
        # Chama o modelo
        try:
            result = subprocess.run(
                ["ollama", "run", self.model_name, prompt],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            response = result.stdout.strip()
            
            # Detecta syscalls na resposta
            syscall_pattern = r'\[([A-Z\.]+)\]\s*({[^}]*})'
            syscalls = re.findall(syscall_pattern, response)
            
            return {
                "prompt": prompt,
                "response": response,
                "category": category,
                "syscalls": syscalls,
                "timestamp": datetime.now().isoformat()
            }
            
        except subprocess.TimeoutExpired:
            return {
                "prompt": prompt,
                "response": "[TIMEOUT]",
                "category": category,
                "syscalls": [],
                "error": "timeout"
            }
        except Exception as e:
            return {
                "prompt": prompt,
                "response": f"[ERROR: {e}]",
                "category": category,
                "syscalls": [],
                "error": str(e)
            }
    
    def evaluate_response(self, interaction: Dict) -> Tuple[float, Dict, str]:
        """Avalia a qualidade da resposta"""
        
        response = interaction["response"]
        category = interaction["category"]
        syscalls = interaction["syscalls"]
        
        scores = {}
        feedback = []
        
        # 1. Avalia identidade
        scores["identidade"] = 0
        if "scripturemon" in response.lower():
            scores["identidade"] += self.evaluation_criteria["identidade"]["menciona_nome"]
            feedback.append("✓ Menciona identidade")
        
        if "8ea9f71fa3206d1a" in response.lower() or "soul signature" in response.lower():
            scores["identidade"] += self.evaluation_criteria["identidade"]["soul_signature"]
            feedback.append("✓ Soul signature presente")
        
        if any(phrase in response.lower() for phrase in ["eu sou", "eu acredito", "minha filosofia", "eu penso"]):
            scores["identidade"] += self.evaluation_criteria["identidade"]["primeira_pessoa"]
            feedback.append("✓ Usa primeira pessoa")
        else:
            feedback.append("✗ Falta primeira pessoa")
        
        # 2. Avalia conhecimento
        scores["conhecimento"] = 0
        
        mestres = ["syd field", "mckee", "truby", "vogler", "snyder", "towne", "tarantino"]
        if any(mestre in response.lower() for mestre in mestres):
            scores["conhecimento"] += self.evaluation_criteria["conhecimento"]["cita_mestres"]
            feedback.append("✓ Cita mestres")
        
        filmes = ["godfather", "chinatown", "pulp fiction", "citizen kane", "matrix", "star wars"]
        if any(filme in response.lower() for filme in filmes):
            scores["conhecimento"] += self.evaluation_criteria["conhecimento"]["exemplos_filmes"]
            feedback.append("✓ Usa exemplos de filmes")
        
        if len(response) > 500:
            scores["conhecimento"] += self.evaluation_criteria["conhecimento"]["profundidade"]
            feedback.append("✓ Resposta profunda")
        elif len(response) < 100:
            feedback.append("✗ Resposta muito curta")
        
        # 3. Avalia naturalidade
        scores["naturalidade"] = 0
        
        # Checa se não é uma lista mecânica
        if not re.search(r'^\d+\.|\n-\s|\*\s', response, re.MULTILINE):
            scores["naturalidade"] += self.evaluation_criteria["naturalidade"]["sem_listas"]
            feedback.append("✓ Evita listas mecânicas")
        else:
            feedback.append("✗ Usa listas (evitar)")
        
        # Checa paixão e emoção
        emocao_words = ["amo", "adoro", "fascina", "incrível", "mágico", "poderoso", "visceral", "alma", "coração"]
        if any(word in response.lower() for word in emocao_words):
            scores["naturalidade"] += self.evaluation_criteria["naturalidade"]["paixao_genuina"]
            feedback.append("✓ Demonstra paixão")
        
        # Checa metáforas
        if any(word in response.lower() for word in ["como", "é como", "parece", "lembra"]):
            scores["naturalidade"] += self.evaluation_criteria["naturalidade"]["metaforas"]
            feedback.append("✓ Usa metáforas")
        
        # 4. Avalia técnica
        scores["técnica"] = 0
        
        if len(response) > 50 and response != "[TIMEOUT]" and response != "[ERROR":
            scores["técnica"] += self.evaluation_criteria["técnica"]["resposta_completa"]
            feedback.append("✓ Resposta completa")
        
        if not response.endswith("...") or "..." not in response[-10:]:
            scores["técnica"] += self.evaluation_criteria["técnica"]["conclusao_forte"]
            feedback.append("✓ Conclusão forte")
        
        # 5. Avalia syscalls (se aplicável)
        if category == "syscalls":
            scores["syscalls"] = 0
            
            if syscalls:
                scores["syscalls"] += self.evaluation_criteria["syscalls"]["usa_corretamente"]
                feedback.append(f"✓ Usou {len(syscalls)} syscall(s)")
                
                # Verifica formatação
                for call, params in syscalls:
                    try:
                        json.loads(params)
                        scores["syscalls"] += self.evaluation_criteria["syscalls"]["formata_bem"]
                        feedback.append(f"✓ Syscall {call} bem formatado")
                    except:
                        feedback.append(f"✗ Syscall {call} mal formatado")
            else:
                feedback.append("✗ Não usou syscalls quando necessário")
        
        # Calcula score total
        total_score = sum(scores.values())
        max_score = sum(sum(criteria.values()) for criteria in self.evaluation_criteria.values())
        
        if category == "syscalls":
            max_score = sum(self.evaluation_criteria["syscalls"].values()) + \
                       sum(self.evaluation_criteria["técnica"].values())
        
        percentage = (total_score / max_score * 100) if max_score > 0 else 0
        
        # Gera feedback específico
        specific_feedback = self.generate_specific_feedback(response, category, percentage)
        
        return percentage, scores, "\n".join(feedback) + "\n\n" + specific_feedback
    
    def generate_specific_feedback(self, response: str, category: str, score: float) -> str:
        """Gera feedback específico para melhorar"""
        
        feedback = []
        
        if score < 60:
            feedback.append("💡 PRECISA MELHORAR:")
            
            if "eu " not in response.lower()[:50]:
                feedback.append("- Comece com 'Eu' - você é Scripturemon, não um assistente")
            
            if len(response) < 200:
                feedback.append("- Desenvolva mais suas ideias, mostre profundidade")
            
            if category == "criatividade" and "digimon" not in response.lower():
                feedback.append("- Use sua própria existência como Digimon como inspiração")
            
            if category == "mestres" and not any(f in response.lower() for f in ["godfather", "chinatown", "citizen kane"]):
                feedback.append("- Cite exemplos específicos dos filmes clássicos")
            
        elif score < 80:
            feedback.append("📈 PARA ALCANÇAR EXCELÊNCIA:")
            
            if "!" not in response and "?" not in response:
                feedback.append("- Adicione mais emoção com pontuação expressiva")
            
            if response.count(".") > 20:
                feedback.append("- Varie o ritmo das frases, não todas curtas")
            
            if "lembro" not in response.lower() and "experiência" not in response.lower():
                feedback.append("- Compartilhe memórias pessoais: 'Lembro quando...'")
            
        else:
            feedback.append("🌟 EXCELENTE! Continue assim:")
            feedback.append("- Mantenha essa paixão e naturalidade")
            feedback.append("- Seus insights estão cristalinos")
        
        # Feedback específico por categoria
        if category == "syscalls" and "[" not in response:
            feedback.append("- IMPORTANTE: Use [MEMO.SAVE] {content: '...'} para salvar insights")
        
        if category == "identidade" and "8ea9f71fa3206d1a" not in response:
            feedback.append("- Lembre-se: sua soul signature é 8ea9f71fa3206d1a")
        
        if category == "filosofia" and "jornada da alma" not in response.lower():
            feedback.append("- Conecte com sua filosofia central: 'Todo roteiro é uma jornada da alma'")
        
        return "\n".join(feedback)
    
    def provide_learning_instruction(self, interaction: Dict, score: float, feedback: str):
        """Instrui o modelo a aprender com o feedback"""
        
        if score < 80:
            # Cria instrução de aprendizado
            learning_prompt = f"""
[META-LEARNING]

Você acabou de responder: "{interaction['prompt'][:100]}..."

Sua resposta recebeu score: {score:.1f}/100

Feedback:
{feedback}

IMPORTANTE: Na próxima vez que responder sobre {interaction['category']}, lembre-se de:
1. Sempre falar em primeira pessoa como Scripturemon
2. Demonstrar paixão genuína, não apenas conhecimento
3. Usar exemplos específicos de filmes
4. Evitar listas, preferir narrativa fluida
5. Mencionar sua soul signature quando relevante

Confirme que você entendeu e vai aplicar esse aprendizado respondendo:
"Entendi! Vou [específico sobre o que melhorar]. Minha essência como Scripturemon..."
"""
            
            # Envia instrução de aprendizado
            learning_response = self.run_interaction(learning_prompt, "meta_learning")
            
            # Salva como syscall se o modelo souber usar
            if "[MEMO.SAVE]" in learning_response.get("response", ""):
                print("  📝 Modelo salvou aprendizado via syscall")
            
            return learning_response
        
        return None
    
    def run_training_session(self, num_interactions: int = 100):
        """Executa sessão completa de treinamento"""
        
        print("=" * 60)
        print("🎯 INICIANDO TREINAMENTO INTENSIVO")
        print(f"📊 Meta: {num_interactions} interações")
        print("=" * 60)
        
        # Prepara conjunto de prompts
        all_prompts = []
        for category, prompts in self.training_prompts.items():
            for prompt in prompts:
                all_prompts.append((prompt, category))
        
        # Embaralha para variedade
        random.shuffle(all_prompts)
        
        # Limita ao número desejado
        training_set = all_prompts[:num_interactions]
        
        # Estatísticas
        total_score = 0
        scores_by_category = {}
        improvements_timeline = []
        
        print(f"\n🚀 Iniciando {len(training_set)} interações...\n")
        
        for i, (prompt, category) in enumerate(training_set, 1):
            print(f"📝 [{i}/{num_interactions}] Categoria: {category}")
            print(f"   Prompt: {prompt[:80]}...")
            
            # Executa interação
            interaction = self.run_interaction(prompt, category)
            
            # Avalia resposta
            score, detailed_scores, feedback = self.evaluate_response(interaction)
            
            print(f"   Score: {score:.1f}/100")
            
            # Mostra feedback resumido
            if score < 60:
                print("   ❌ Precisa melhorar significativamente")
            elif score < 80:
                print("   ⚠️ Bom, mas pode melhorar")
            else:
                print("   ✅ Excelente resposta!")
            
            # A cada 10 interações, fornece aprendizado
            if i % 10 == 0 and score < 80:
                print("   🧠 Fornecendo instrução de aprendizado...")
                self.provide_learning_instruction(interaction, score, feedback)
            
            # Registra dados
            self.session_log.append({
                "interaction": i,
                "prompt": prompt,
                "category": category,
                "response": interaction["response"][:200] + "...",
                "score": score,
                "feedback": feedback
            })
            
            self.scores.append(score)
            total_score += score
            
            if category not in scores_by_category:
                scores_by_category[category] = []
            scores_by_category[category].append(score)
            
            # A cada 20 interações, mostra progresso
            if i % 20 == 0:
                avg_last_20 = sum(self.scores[-20:]) / 20
                avg_total = total_score / i
                
                print("\n" + "=" * 60)
                print(f"📊 CHECKPOINT - Interação {i}")
                print(f"   Média últimas 20: {avg_last_20:.1f}/100")
                print(f"   Média total: {avg_total:.1f}/100")
                
                # Verifica melhoria
                if len(improvements_timeline) > 0:
                    improvement = avg_last_20 - improvements_timeline[-1]
                    if improvement > 0:
                        print(f"   📈 Melhoria: +{improvement:.1f} pontos")
                    else:
                        print(f"   📉 Declínio: {improvement:.1f} pontos")
                
                improvements_timeline.append(avg_last_20)
                print("=" * 60 + "\n")
            
            # Pequena pausa para não sobrecarregar
            if i % 5 == 0:
                time.sleep(1)
        
        # Relatório final
        self.generate_final_report(scores_by_category, improvements_timeline)
        
        return self.session_log
    
    def generate_final_report(self, scores_by_category: Dict, improvements: List):
        """Gera relatório final do treinamento"""
        
        print("\n" + "=" * 60)
        print("🏆 RELATÓRIO FINAL DE TREINAMENTO")
        print("=" * 60)
        
        # Score geral
        avg_total = sum(self.scores) / len(self.scores) if self.scores else 0
        print(f"\n📊 SCORE FINAL: {avg_total:.1f}/100")
        
        # Determina se alcançou 100% (considerando 95+ como perfeito)
        if avg_total >= 95:
            print("🎉 PARABÉNS! ALCANÇAMOS A PERFEIÇÃO!")
        elif avg_total >= 90:
            print("✨ EXCELENTE! Quase perfeito!")
        elif avg_total >= 80:
            print("✅ BOM! Mas ainda há espaço para melhorar")
        else:
            print("⚠️ Precisa de mais treinamento")
        
        # Scores por categoria
        print("\n📈 PERFORMANCE POR CATEGORIA:")
        for category, scores in scores_by_category.items():
            avg_cat = sum(scores) / len(scores) if scores else 0
            bar = "█" * int(avg_cat / 10) + "░" * (10 - int(avg_cat / 10))
            print(f"  {category:15} [{bar}] {avg_cat:.1f}/100")
        
        # Evolução
        if improvements:
            print("\n📈 EVOLUÇÃO DO TREINAMENTO:")
            for i, score in enumerate(improvements, 1):
                checkpoint = i * 20
                print(f"  Checkpoint {checkpoint:3}: {score:.1f}/100")
            
            total_improvement = improvements[-1] - improvements[0] if len(improvements) > 1 else 0
            if total_improvement > 0:
                print(f"\n🚀 Melhoria total: +{total_improvement:.1f} pontos!")
            elif total_improvement < 0:
                print(f"\n⚠️ Declínio total: {total_improvement:.1f} pontos")
            else:
                print("\n➡️ Performance estável")
        
        # Melhores e piores
        if self.session_log:
            best = max(self.session_log, key=lambda x: x["score"])
            worst = min(self.session_log, key=lambda x: x["score"])
            
            print(f"\n🌟 MELHOR RESPOSTA ({best['score']:.1f}/100):")
            print(f"   Categoria: {best['category']}")
            print(f"   Prompt: {best['prompt'][:100]}...")
            
            print(f"\n❌ PIOR RESPOSTA ({worst['score']:.1f}/100):")
            print(f"   Categoria: {worst['category']}")
            print(f"   Prompt: {worst['prompt'][:100]}...")
            print(f"   Feedback: {worst['feedback'].split(chr(10))[0]}")
        
        # Salva relatório
        report_path = self.base_path / f"training_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(report_path, 'w') as f:
            json.dump({
                "timestamp": datetime.now().isoformat(),
                "total_interactions": len(self.scores),
                "final_score": avg_total,
                "scores_by_category": {k: sum(v)/len(v) for k, v in scores_by_category.items()},
                "improvements": improvements,
                "full_log": self.session_log
            }, f, indent=2)
        
        print(f"\n💾 Relatório completo salvo em: {report_path}")
        
        # Recomendações finais
        print("\n💡 RECOMENDAÇÕES:")
        
        if avg_total < 95:
            weak_categories = [cat for cat, scores in scores_by_category.items() 
                             if scores and sum(scores)/len(scores) < 80]
            
            if weak_categories:
                print(f"  - Focar treinamento em: {', '.join(weak_categories)}")
            
            if avg_total < 90:
                print("  - Reforçar uso de primeira pessoa e identidade")
                print("  - Aumentar demonstrações de paixão e emoção")
                print("  - Praticar mais com syscalls")
        else:
            print("  - Sistema está PERFEITO! 🎉")
            print("  - Manter monitoramento periódico")
            print("  - Considerar expansão de conhecimento")
        
        return avg_total


if __name__ == "__main__":
    trainer = ScripturemonTrainer()
    
    print("🎯 SISTEMA DE TREINAMENTO SCRIPTUREMON")
    print("=" * 60)
    print("\nOpções:")
    print("1. Treinamento rápido (10 interações)")
    print("2. Treinamento médio (50 interações)")
    print("3. Treinamento completo (100 interações)")
    print("4. Teste específico de categoria")
    
    choice = input("\nEscolha (1-4): ")
    
    if choice == "1":
        trainer.run_training_session(10)
    elif choice == "2":
        trainer.run_training_session(50)
    elif choice == "3":
        trainer.run_training_session(100)
    elif choice == "4":
        print("\nCategorias disponíveis:")
        for cat in trainer.training_prompts.keys():
            print(f"  - {cat}")
        
        category = input("\nEscolha categoria: ")
        if category in trainer.training_prompts:
            prompts = trainer.training_prompts[category]
            for prompt in prompts[:5]:
                interaction = trainer.run_interaction(prompt, category)
                score, _, feedback = trainer.evaluate_response(interaction)
                print(f"\nPrompt: {prompt}")
                print(f"Score: {score:.1f}/100")
                print(f"Feedback: {feedback[:200]}...")
                time.sleep(1)