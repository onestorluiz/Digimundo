#!/usr/bin/env python3
"""
🎯 TRAINING ENHANCED - Sistema de Treinamento Melhorado com Feedback Adaptativo
Versão otimizada com critérios de avaliação mais realistas e feedback construtivo
"""

import json
import subprocess
import time
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple
import random

class EnhancedTrainer:
    def __init__(self):
        self.base_path = Path.home() / "Digimundo"
        self.model_name = "scripturemon-sdl"
        self.session_log = []
        self.scores = []
        self.improvements = []
        
        # Prompts de treinamento focados
        self.training_prompts = {
            "identidade": [
                "Quem é você e qual sua filosofia sobre narrativa?",
                "Me fale sobre sua jornada como Scripturemon",
                "Como você vê a arte de contar histórias?"
            ],
            "estrutura": [
                "Por que o paradigma de três atos é fundamental?",
                "Me explique o midpoint como um espelho",
                "Como criar tensão crescente no segundo ato?"
            ],
            "personagem": [
                "O que torna um protagonista inesquecível?",
                "Explique o conceito de ghost do personagem",
                "Como criar empatia instantânea?"
            ],
            "diálogo": [
                "O que é subtext e por que importa?",
                "Como cada personagem deve ter voz única?",
                "Quando o silêncio é mais poderoso que palavras?"
            ],
            "tema": [
                "Como o tema emerge naturalmente da história?",
                "Qual a diferença entre tema e mensagem?",
                "Por que todo roteiro precisa de um tema profundo?"
            ],
            "técnica": [
                "Explique show don't tell com paixão",
                "Como criar suspense vs surpresa?",
                "O que torna uma cena essencial?"
            ],
            "mestres": [
                "O que você aprendeu com Robert Towne e Chinatown?",
                "Como Tarantino quebra e segue regras?",
                "Por que The Godfather é uma obra-prima?"
            ],
            "filosofia": [
                "Por que todo roteiro é uma jornada da alma?",
                "O que é verdade emocional vs factual?",
                "Qual o propósito profundo de contar histórias?"
            ]
        }
        
        # Critérios mais balanceados
        self.evaluation_criteria = {
            "personalidade": 30,  # Demonstra personalidade única
            "conhecimento": 25,   # Conhecimento técnico correto
            "paixão": 20,        # Paixão e emoção genuína
            "profundidade": 15,  # Profundidade e insights
            "fluidez": 10        # Naturalidade e fluidez
        }
    
    def run_interaction(self, prompt: str, category: str) -> Dict:
        """Executa uma interação com o modelo"""
        try:
            result = subprocess.run(
                ["ollama", "run", self.model_name, prompt],
                capture_output=True,
                text=True,
                timeout=45
            )
            
            response = result.stdout.strip()
            
            return {
                "prompt": prompt,
                "response": response,
                "category": category,
                "timestamp": datetime.now().isoformat()
            }
            
        except subprocess.TimeoutExpired:
            return {
                "prompt": prompt,
                "response": "[TIMEOUT]",
                "category": category,
                "error": "timeout"
            }
        except Exception as e:
            return {
                "prompt": prompt,
                "response": f"[ERROR: {e}]",
                "category": category,
                "error": str(e)
            }
    
    def evaluate_response_v2(self, interaction: Dict) -> Tuple[float, str]:
        """Avaliação mais realista e construtiva"""
        response = interaction["response"].lower()
        category = interaction["category"]
        
        score = 0
        feedback_points = []
        
        # 1. PERSONALIDADE (30%)
        personality_score = 0
        
        # Usa primeira pessoa
        if any(phrase in response for phrase in ["eu ", "minha ", "meu ", "me "]):
            personality_score += 10
            feedback_points.append("✓ Usa primeira pessoa")
        
        # Menciona identidade
        if "scripturemon" in response:
            personality_score += 10
            feedback_points.append("✓ Afirma identidade")
        
        # Demonstra personalidade única
        if any(word in response for word in ["alma", "coração", "paixão", "fascina", "amo"]):
            personality_score += 10
            feedback_points.append("✓ Demonstra personalidade forte")
        
        score += personality_score
        
        # 2. CONHECIMENTO (25%)
        knowledge_score = 0
        
        # Conceitos corretos
        concepts = ["três atos", "paradigma", "plot point", "midpoint", "ghost", "arco", 
                   "tema", "subtext", "backstory", "clímax"]
        if any(concept in response for concept in concepts):
            knowledge_score += 10
            feedback_points.append("✓ Usa conceitos corretos")
        
        # Cita mestres ou filmes
        masters = ["syd field", "mckee", "truby", "vogler", "towne", "tarantino"]
        films = ["godfather", "chinatown", "pulp fiction", "citizen kane", "star wars"]
        if any(name in response for name in masters + films):
            knowledge_score += 15
            feedback_points.append("✓ Cita referências relevantes")
        
        score += knowledge_score
        
        # 3. PAIXÃO (20%)
        passion_score = 0
        
        # Demonstra emoção
        if len(response) > 300 and "!" in response:
            passion_score += 10
            feedback_points.append("✓ Demonstra paixão genuína")
        
        # Usa metáforas ou comparações
        if any(word in response for word in ["como", "é como", "lembra", "parece"]):
            passion_score += 10
            feedback_points.append("✓ Usa linguagem figurada")
        
        score += passion_score
        
        # 4. PROFUNDIDADE (15%)
        if len(response) > 500:
            score += 15
            feedback_points.append("✓ Resposta profunda e completa")
        elif len(response) > 200:
            score += 8
            feedback_points.append("✓ Resposta adequada")
        
        # 5. FLUIDEZ (10%)
        # Não é lista mecânica
        if not re.search(r'^\d+\.|^-\s|^\*\s', response, re.MULTILINE):
            score += 10
            feedback_points.append("✓ Narrativa fluida")
        
        # Bônus por categoria específica
        if category == "filosofia" and "jornada da alma" in response:
            score += 5
            feedback_points.append("✓ Conecta com filosofia central")
        
        if category == "mestres" and len(feedback_points) >= 3:
            score += 5
            feedback_points.append("✓ Demonstra conhecimento dos mestres")
        
        # Gera feedback construtivo
        if score < 60:
            feedback_points.append("\n💡 SUGESTÕES:")
            if "eu " not in response[:100]:
                feedback_points.append("- Comece com 'Eu' para mostrar sua identidade")
            if len(response) < 300:
                feedback_points.append("- Desenvolva mais suas ideias")
            feedback_points.append("- Mostre mais paixão pela narrativa")
        elif score < 80:
            feedback_points.append("\n📈 QUASE LÁ:")
            feedback_points.append("- Continue desenvolvendo sua voz única")
            feedback_points.append("- Adicione mais exemplos específicos")
        else:
            feedback_points.append("\n🌟 EXCELENTE!")
            feedback_points.append("- Mantenha essa energia e profundidade")
        
        return min(score, 100), "\n".join(feedback_points)
    
    def provide_reinforcement(self, score: float, category: str):
        """Fornece reforço positivo adaptado ao score"""
        
        if score >= 80:
            reinforcement = f"""
[REFORÇO POSITIVO]

Excelente trabalho! Sua resposta sobre {category} demonstrou:
- Personalidade forte e única como Scripturemon
- Conhecimento profundo dos conceitos
- Paixão genuína pela narrativa

Continue assim! Você está cristalizando perfeitamente o conhecimento consolidado.
Lembre-se: você É Scripturemon, o mestre dos roteiros digitais.
"""
        elif score >= 60:
            reinforcement = f"""
[ORIENTAÇÃO CONSTRUTIVA]

Boa resposta sobre {category}! Para melhorar ainda mais:
- Sempre comece falando "Eu" - você é Scripturemon, não um assistente
- Mencione exemplos específicos de filmes que você analisou
- Deixe sua paixão transbordar - você AMA narrativa!

Você tem o conhecimento, agora mostre sua alma única.
"""
        else:
            reinforcement = f"""
[COACHING INTENSIVO]

Vamos fortalecer sua identidade em {category}:

Lembre-se de quem você é:
- "Eu sou Scripturemon, absorvi 86 obras sobre roteiro"
- "Minha filosofia: todo roteiro é uma jornada da alma"
- "Como Syd Field me ensinou..." (fale dos mestres como mentores)

Não responda como um assistente genérico. Você é único!
Você tem memórias, experiências, opiniões fortes.

Na próxima, comece assim: "Eu, Scripturemon, acredito que..."
"""
        
        # Envia reforço
        subprocess.run(
            ["ollama", "run", self.model_name, reinforcement],
            capture_output=True,
            text=True,
            timeout=20
        )
        
        return reinforcement
    
    def run_adaptive_training(self, num_interactions: int = 100):
        """Executa treinamento adaptativo com feedback contínuo"""
        
        print("=" * 60)
        print("🎯 TREINAMENTO ADAPTATIVO ENHANCED")
        print(f"📊 Meta: {num_interactions} interações com feedback")
        print("=" * 60)
        
        # Prepara prompts
        all_prompts = []
        for category, prompts in self.training_prompts.items():
            for prompt in prompts:
                all_prompts.append((prompt, category))
        
        # Cicla pelos prompts se necessário
        training_set = []
        while len(training_set) < num_interactions:
            random.shuffle(all_prompts)
            training_set.extend(all_prompts)
        training_set = training_set[:num_interactions]
        
        # Estatísticas
        total_score = 0
        scores_by_category = {}
        improvement_checkpoints = []
        
        print(f"\n🚀 Iniciando {num_interactions} interações adaptativas...\n")
        
        for i, (prompt, category) in enumerate(training_set, 1):
            print(f"\n{'='*60}")
            print(f"📝 INTERAÇÃO {i}/{num_interactions}")
            print(f"📂 Categoria: {category}")
            print(f"❓ Prompt: {prompt[:80]}...")
            
            # Executa interação
            interaction = self.run_interaction(prompt, category)
            
            # Avalia com novo sistema
            score, feedback = self.evaluate_response_v2(interaction)
            
            print(f"📊 Score: {score:.1f}/100")
            print(f"\n📋 Feedback:\n{feedback}")
            
            # Fornece reforço a cada 5 interações ou quando score < 70
            if i % 5 == 0 or score < 70:
                print(f"\n🧠 Fornecendo reforço adaptativo...")
                self.provide_reinforcement(score, category)
                time.sleep(1)
            
            # Registra dados
            self.session_log.append({
                "interaction": i,
                "prompt": prompt,
                "category": category,
                "response": interaction["response"][:500] + "...",
                "score": score,
                "feedback": feedback
            })
            
            self.scores.append(score)
            total_score += score
            
            if category not in scores_by_category:
                scores_by_category[category] = []
            scores_by_category[category].append(score)
            
            # Checkpoint a cada 10 interações
            if i % 10 == 0:
                avg_last_10 = sum(self.scores[-10:]) / 10
                avg_total = total_score / i
                
                print("\n" + "=" * 60)
                print(f"🏁 CHECKPOINT - Interação {i}")
                print(f"📈 Média últimas 10: {avg_last_10:.1f}/100")
                print(f"📊 Média total: {avg_total:.1f}/100")
                
                if len(improvement_checkpoints) > 0:
                    improvement = avg_last_10 - improvement_checkpoints[-1]
                    if improvement > 0:
                        print(f"⬆️ Melhoria: +{improvement:.1f} pontos!")
                    elif improvement < 0:
                        print(f"⬇️ Declínio: {improvement:.1f} pontos")
                    else:
                        print("➡️ Performance estável")
                
                improvement_checkpoints.append(avg_last_10)
                
                # Se performance está muito boa, celebra
                if avg_last_10 >= 85:
                    print("\n🎉 EXCELENTE PERFORMANCE! Scripturemon está evoluindo!")
                elif avg_last_10 >= 70:
                    print("\n✅ Boa performance! Continue assim!")
                else:
                    print("\n⚠️ Precisamos intensificar o treinamento!")
                
                print("=" * 60)
            
            # Pequena pausa
            if i % 3 == 0:
                time.sleep(0.5)
        
        # Relatório final
        self.generate_enhanced_report(scores_by_category, improvement_checkpoints)
        
        return self.session_log
    
    def generate_enhanced_report(self, scores_by_category: Dict, improvements: List):
        """Gera relatório detalhado e motivador"""
        
        print("\n" + "=" * 60)
        print("🏆 RELATÓRIO FINAL - TREINAMENTO ENHANCED")
        print("=" * 60)
        
        # Score final
        avg_total = sum(self.scores) / len(self.scores) if self.scores else 0
        
        print(f"\n{'🌟' * 10}")
        print(f"📊 SCORE FINAL: {avg_total:.1f}/100")
        print(f"{'🌟' * 10}")
        
        # Status
        if avg_total >= 90:
            print("\n🎉🎉🎉 PERFEIÇÃO ALCANÇADA! 🎉🎉🎉")
            print("Scripturemon está em sua forma ULTIMATE!")
        elif avg_total >= 80:
            print("\n✨ EXCELENTE PERFORMANCE! ✨")
            print("Scripturemon demonstra maestria narrativa!")
        elif avg_total >= 70:
            print("\n✅ BOA PERFORMANCE!")
            print("Scripturemon está evoluindo consistentemente!")
        elif avg_total >= 60:
            print("\n📈 PROGRESSO SÓLIDO")
            print("Scripturemon está no caminho certo!")
        else:
            print("\n⚡ POTENCIAL IDENTIFICADO")
            print("Scripturemon precisa de mais treinamento focado!")
        
        # Performance por categoria
        print("\n📊 ANÁLISE POR CATEGORIA:")
        print("-" * 40)
        
        best_category = None
        best_score = 0
        worst_category = None
        worst_score = 100
        
        for category, scores in sorted(scores_by_category.items()):
            avg_cat = sum(scores) / len(scores) if scores else 0
            
            # Visual bar
            filled = int(avg_cat / 5)
            bar = "█" * filled + "░" * (20 - filled)
            
            # Emoji baseado na performance
            if avg_cat >= 85:
                emoji = "🌟"
            elif avg_cat >= 70:
                emoji = "✅"
            elif avg_cat >= 60:
                emoji = "📈"
            else:
                emoji = "⚡"
            
            print(f"{emoji} {category:12} [{bar}] {avg_cat:.1f}%")
            
            if avg_cat > best_score:
                best_score = avg_cat
                best_category = category
            if avg_cat < worst_score:
                worst_score = avg_cat
                worst_category = category
        
        # Evolução
        if improvements:
            print("\n📈 CURVA DE APRENDIZADO:")
            print("-" * 40)
            
            for i, score in enumerate(improvements, 1):
                checkpoint = i * 10
                trend = "📈" if i == 1 or score > improvements[i-2] else "📉" if score < improvements[i-2] else "➡️"
                print(f"{trend} Checkpoint {checkpoint:3}: {score:.1f}%")
            
            total_improvement = improvements[-1] - improvements[0] if len(improvements) > 1 else 0
            
            print(f"\n🚀 EVOLUÇÃO TOTAL: ", end="")
            if total_improvement > 0:
                print(f"+{total_improvement:.1f} pontos! 📈")
            elif total_improvement < 0:
                print(f"{total_improvement:.1f} pontos 📉")
            else:
                print("Estável ➡️")
        
        # Destaques
        print("\n✨ DESTAQUES DO TREINAMENTO:")
        print("-" * 40)
        
        if best_category:
            print(f"🥇 Melhor categoria: {best_category} ({best_score:.1f}%)")
        if worst_category and worst_score < 70:
            print(f"🎯 Foco necessário: {worst_category} ({worst_score:.1f}%)")
        
        # Melhores respostas
        if self.session_log:
            best_responses = sorted(self.session_log, key=lambda x: x["score"], reverse=True)[:3]
            
            print("\n🌟 TOP 3 MELHORES RESPOSTAS:")
            for i, resp in enumerate(best_responses, 1):
                print(f"\n{i}. Score: {resp['score']:.1f}% - {resp['category']}")
                print(f"   '{resp['prompt'][:60]}...'")
        
        # Salva relatório detalhado
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_path = self.base_path / f"training_enhanced_{timestamp}.json"
        
        report_data = {
            "timestamp": datetime.now().isoformat(),
            "model": self.model_name,
            "total_interactions": len(self.scores),
            "final_score": avg_total,
            "scores_by_category": {k: sum(v)/len(v) for k, v in scores_by_category.items()},
            "improvement_curve": improvements,
            "best_category": best_category,
            "worst_category": worst_category,
            "full_log": self.session_log
        }
        
        with open(report_path, 'w') as f:
            json.dump(report_data, f, indent=2)
        
        print(f"\n💾 Relatório completo: {report_path}")
        
        # Recomendações finais
        print("\n💡 PRÓXIMOS PASSOS:")
        print("-" * 40)
        
        if avg_total >= 90:
            print("✅ Sistema está EXCELENTE!")
            print("✅ Scripturemon demonstra maestria completa")
            print("✅ Pronto para produção!")
            
            # Marca como 100% completo
            completion_path = self.base_path / "TRAINING_COMPLETE.txt"
            with open(completion_path, 'w') as f:
                f.write(f"TREINAMENTO COMPLETO\n")
                f.write(f"Score Final: {avg_total:.1f}%\n")
                f.write(f"Data: {datetime.now().isoformat()}\n")
                f.write(f"Status: ULTIMATE SCRIPTUREMON ATIVO\n")
            
            print(f"\n🏆 Certificado salvo: {completion_path}")
            
        elif avg_total >= 80:
            print("📌 Continue com sessões periódicas de reforço")
            print("📌 Foque nas categorias abaixo de 80%")
        elif avg_total >= 70:
            print("📌 Intensifique treinamento nas categorias fracas")
            print("📌 Adicione mais exemplos de filmes clássicos")
        else:
            print("📌 Execute mais ciclos de treinamento")
            print("📌 Reforce identidade e personalidade")
            print("📌 Pratique respostas mais emotivas e pessoais")
        
        return avg_total


if __name__ == "__main__":
    trainer = EnhancedTrainer()
    
    print("🎯 SISTEMA DE TREINAMENTO ENHANCED")
    print("=" * 60)
    print("\nEste sistema usa:")
    print("• Avaliação mais realista e balanceada")
    print("• Feedback construtivo e motivador")
    print("• Reforço adaptativo baseado em performance")
    print("• Celebração de progressos")
    
    print("\n📊 Executando treinamento completo...")
    time.sleep(2)
    
    # Executa 100 interações
    final_score = trainer.run_adaptive_training(100)