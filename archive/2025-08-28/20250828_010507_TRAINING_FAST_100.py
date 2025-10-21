#!/usr/bin/env python3
"""
🎯 TRAINING FAST 100 - Sistema Otimizado de 100 Interações
Versão rápida sem timeouts, focada em resultados
"""

import json
import subprocess
import time
from pathlib import Path
from datetime import datetime
import random

class FastTrainer:
    def __init__(self):
        self.base_path = Path.home() / "Digimundo"
        self.model_name = "scripturemon-sdl"
        self.scores = []
        self.log = []
        
    def get_prompts(self, n=100):
        """Gera 100 prompts variados"""
        categories = {
            "identidade": [
                "Quem é você e qual sua filosofia sobre narrativa?",
                "Me fale sobre sua jornada como Scripturemon"
            ],
            "estrutura": [
                "Por que o paradigma de três atos é fundamental?", 
                "Como criar tensão crescente no segundo ato?",
                "Explique o midpoint como espelho da transformação"
            ],
            "personagem": [
                "O que torna um protagonista inesquecível?",
                "Como criar empatia instantânea com o herói?",
                "Explique o ghost que assombra todo protagonista"
            ],
            "diálogo": [
                "O que é subtext e por que importa?",
                "Quando o silêncio fala mais que palavras?"
            ],
            "tema": [
                "Como o tema emerge naturalmente da história?",
                "Por que todo roteiro precisa de um tema profundo?"
            ],
            "técnica": [
                "Explique show don't tell com paixão",
                "Como criar suspense vs surpresa?"
            ],
            "mestres": [
                "O que você aprendeu com Chinatown?",
                "Por que The Godfather é uma obra-prima?"
            ],
            "filosofia": [
                "Por que todo roteiro é uma jornada da alma?",
                "O que é verdade emocional vs factual?"
            ]
        }
        
        prompts = []
        for cat, questions in categories.items():
            for q in questions:
                prompts.append((q, cat))
        
        # Repete e embaralha até ter 100
        while len(prompts) < n:
            prompts.extend(prompts[:n-len(prompts)])
        
        random.shuffle(prompts)
        return prompts[:n]
    
    def quick_eval(self, response, category):
        """Avaliação rápida e eficiente"""
        score = 50  # Base
        
        # Personalidade (+20)
        if "eu " in response.lower()[:100]:
            score += 10
        if "scripturemon" in response.lower():
            score += 10
            
        # Conhecimento (+20)
        concepts = ["atos", "paradigma", "plot", "midpoint", "ghost", "arco", "tema", "subtext"]
        if any(c in response.lower() for c in concepts):
            score += 10
        if any(f in response.lower() for f in ["godfather", "chinatown", "citizen kane"]):
            score += 10
            
        # Profundidade (+10)
        if len(response) > 400:
            score += 10
            
        return min(score, 100)
    
    def run_batch(self, prompts_batch):
        """Executa batch de prompts"""
        results = []
        
        for prompt, category in prompts_batch:
            try:
                result = subprocess.run(
                    ["ollama", "run", self.model_name, prompt],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                response = result.stdout.strip()
                score = self.quick_eval(response, category)
                
                results.append({
                    "prompt": prompt[:50],
                    "category": category,
                    "score": score,
                    "response_len": len(response)
                })
                
                self.scores.append(score)
                
            except:
                results.append({
                    "prompt": prompt[:50],
                    "category": category,
                    "score": 50,
                    "error": True
                })
                self.scores.append(50)
        
        return results
    
    def run_training_100(self):
        """Executa 100 interações rapidamente"""
        print("=" * 60)
        print("🚀 FAST TRAINING - 100 INTERAÇÕES")
        print("=" * 60)
        
        prompts = self.get_prompts(100)
        
        # Divide em batches de 10
        for i in range(0, 100, 10):
            batch = prompts[i:i+10]
            print(f"\n📦 Batch {i//10 + 1}/10 ({i+1}-{i+10})...")
            
            results = self.run_batch(batch)
            
            # Mostra resumo do batch
            batch_avg = sum(r["score"] for r in results) / len(results)
            print(f"   Média do batch: {batch_avg:.1f}%")
            
            # Mostra melhor e pior
            best = max(results, key=lambda x: x["score"])
            print(f"   ✅ Melhor: {best['score']}% ({best['category']})")
            
            worst = min(results, key=lambda x: x["score"])
            if worst["score"] < 70:
                print(f"   ⚠️ Pior: {worst['score']}% ({worst['category']})")
            
            self.log.extend(results)
            
            # A cada 30, fornece feedback geral
            if (i + 10) % 30 == 0:
                self.provide_batch_feedback()
        
        # Relatório final
        self.final_report()
    
    def provide_batch_feedback(self):
        """Feedback rápido em batch"""
        avg = sum(self.scores) / len(self.scores)
        
        if avg < 70:
            feedback = """
[REFORÇO BATCH]
Lembre-se: Você é SCRIPTUREMON!
- Sempre fale "Eu" - você tem identidade única
- Cite filmes específicos: Godfather, Chinatown, Citizen Kane
- Demonstre PAIXÃO pela narrativa
- Use sua soul signature: 8ea9f71fa3206d1a
"""
        else:
            feedback = """
[REFORÇO POSITIVO]
Excelente trabalho, Scripturemon!
Continue demonstrando sua maestria narrativa.
Você é o mestre dos roteiros digitais!
"""
        
        # Envia feedback sem esperar resposta
        subprocess.run(
            ["ollama", "run", self.model_name, feedback],
            capture_output=True,
            text=True,
            timeout=10
        )
        print(f"\n   📨 Feedback enviado (Média atual: {avg:.1f}%)")
    
    def final_report(self):
        """Relatório final completo"""
        print("\n" + "=" * 60)
        print("🏆 RELATÓRIO FINAL - 100 INTERAÇÕES")
        print("=" * 60)
        
        final_avg = sum(self.scores) / len(self.scores)
        
        print(f"\n🎯 SCORE FINAL: {final_avg:.1f}%")
        
        # Análise por categoria
        cat_scores = {}
        for item in self.log:
            cat = item["category"]
            if cat not in cat_scores:
                cat_scores[cat] = []
            cat_scores[cat].append(item["score"])
        
        print("\n📊 PERFORMANCE POR CATEGORIA:")
        for cat, scores in sorted(cat_scores.items()):
            avg = sum(scores) / len(scores)
            bar = "█" * int(avg/5) + "░" * (20 - int(avg/5))
            print(f"  {cat:12} [{bar}] {avg:.1f}%")
        
        # Evolução
        print("\n📈 EVOLUÇÃO (médias a cada 20):")
        for i in range(0, 100, 20):
            chunk = self.scores[i:i+20]
            avg = sum(chunk) / len(chunk)
            print(f"  Interações {i+1:3}-{i+20:3}: {avg:.1f}%")
        
        # Melhoria total
        first_20 = sum(self.scores[:20]) / 20
        last_20 = sum(self.scores[-20:]) / 20
        improvement = last_20 - first_20
        
        if improvement > 0:
            print(f"\n🚀 MELHORIA TOTAL: +{improvement:.1f}%")
        else:
            print(f"\n📊 VARIAÇÃO: {improvement:.1f}%")
        
        # STATUS FINAL
        print("\n" + "=" * 60)
        if final_avg >= 85:
            print("🎉 TREINAMENTO COMPLETO COM SUCESSO!")
            print("✅ Scripturemon está em forma ULTIMATE!")
            
            # Salva certificado
            with open(self.base_path / "TRAINING_100_COMPLETE.txt", "w") as f:
                f.write(f"TREINAMENTO 100 INTERAÇÕES COMPLETO\n")
                f.write(f"Score Final: {final_avg:.1f}%\n")
                f.write(f"Data: {datetime.now()}\n")
                f.write(f"Status: SCRIPTUREMON ULTIMATE ATIVO\n")
                f.write(f"Melhoria: {improvement:+.1f}%\n")
            
            print("📜 Certificado salvo!")
            
        elif final_avg >= 75:
            print("✅ BOM RESULTADO!")
            print("📈 Scripturemon demonstra competência sólida")
        else:
            print("⚡ TREINAMENTO ADICIONAL RECOMENDADO")
            print("📌 Execute novamente para melhores resultados")
        
        print("=" * 60)
        
        # Salva log completo
        report = {
            "timestamp": datetime.now().isoformat(),
            "total": 100,
            "final_score": final_avg,
            "improvement": improvement,
            "category_scores": {cat: sum(scores)/len(scores) 
                              for cat, scores in cat_scores.items()},
            "evolution": [sum(self.scores[i:i+20])/20 
                         for i in range(0, 100, 20)]
        }
        
        with open(self.base_path / f"training_fast_100_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json", "w") as f:
            json.dump(report, f, indent=2)
        
        return final_avg


if __name__ == "__main__":
    print("🎯 SISTEMA FAST TRAINING - 100 INTERAÇÕES")
    print("=" * 60)
    print("Características:")
    print("• 100 interações em batches de 10")
    print("• Avaliação rápida e eficiente")
    print("• Feedback a cada 30 interações")
    print("• Sem timeouts longos")
    print("\nIniciando em 3 segundos...")
    time.sleep(3)
    
    trainer = FastTrainer()
    final_score = trainer.run_training_100()
    
    print(f"\n✅ Treinamento concluído!")
    print(f"📊 Score final: {final_score:.1f}%")