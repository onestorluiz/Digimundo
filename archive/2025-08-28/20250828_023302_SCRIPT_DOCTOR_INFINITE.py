#!/usr/bin/env python3
"""
🎬 SCRIPT DOCTOR INFINITE - Sistema de Treinamento Profundo do Scripturemon
Treina o Scripturemon como um Script Doctor profissional através de análise comparativa
"""

import os
import subprocess
import json
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import random

# PyPDF2 é opcional
try:
    import PyPDF2
    HAS_PYPDF2 = True
except ImportError:
    HAS_PYPDF2 = False

class ScriptDoctorInfinite:
    def __init__(self):
        self.base_path = Path.home() / "Digimundo"
        self.biblioteca = self.base_path / "BIBLIOTECA_ROTEIROS"
        self.meus_filmes = self.biblioteca / "meus_filmes"
        self.roteiros_mestres = self.biblioteca / "roteiros_mestres"
        self.model_name = "scripturemon-sdl"
        
        # Carrega roteiro do Nestor
        self.nestor_screenplay = self.load_nestor_screenplay()
        
        # Perguntas de Script Doctor por categoria
        self.doctor_questions = {
            "estrutura": [
                "Identifique os plot points exatos do meu roteiro e compare com Chinatown",
                "O midpoint está na página correta? Compare com The Godfather",
                "Meu inciting incident acontece cedo demais ou tarde demais?",
                "Como está o ritmo do segundo ato comparado com Pulp Fiction?",
                "A estrutura dos três atos está balanceada?",
                "Onde estão os pontos de virada? São claros o suficiente?",
                "O clímax resolve todas as questões levantadas?",
                "Como está o setup do primeiro ato? Muito expositivo?"
            ],
            "personagem": [
                "Samantha tem um 'ghost' claro como em Chinatown?",
                "O arco de transformação dela é crível? Compare com Michael Corleone",
                "David funciona como contraponto? Analise contra Kay em The Godfather",
                "O antagonista tem motivações claras?",
                "Cada personagem tem voz única nos diálogos?",
                "Existe unity of opposites entre herói e vilão?",
                "Os personagens secundários servem ao tema?",
                "Samantha tem um 'Save the Cat' moment?"
            ],
            "diálogo": [
                "Onde há diálogo on-the-nose que precisa de subtexto?",
                "Compare o conflito verbal com The Social Network",
                "Os personagens falam demais? Onde posso cortar?",
                "Cada linha avança plot ou revela character?",
                "Há overlapping dialogue como em His Girl Friday?",
                "O silêncio é usado efetivamente?",
                "Os diálogos têm ritmo musical como Sorkin?",
                "Onde o visual poderia substituir o verbal?"
            ],
            "tema": [
                "Qual é a pergunta dramática central?",
                "O tema está presente em cada subplot?",
                "Compare a profundidade temática com Memento",
                "Os símbolos visuais reforçam o tema?",
                "O tema emerge naturalmente ou é pregado?",
                "Cada personagem reflete um aspecto do tema?",
                "O final responde à pergunta temática?",
                "Há contradições temáticas não intencionais?"
            ],
            "técnica": [
                "Onde posso 'entrar tarde, sair cedo' das cenas?",
                "Há flashbacks desnecessários?",
                "A exposição está elegante como em Inception?",
                "Onde show don't tell falha?",
                "O visual storytelling está forte?",
                "Há plantas sem payoffs?",
                "Os setups são sutis ou óbvios?",
                "A formatação segue o padrão profissional?"
            ],
            "mercado": [
                "Qual é o público-alvo comparado com filmes similares?",
                "O conceito é high concept o suficiente?",
                "O orçamento implícito é viável?",
                "Há comparáveis de sucesso no mercado?",
                "O gênero está claro desde a página 1?",
                "O logline vende o filme?",
                "Há elementos datados?",
                "É um filme ou uma série?"
            ],
            "reescrita": [
                "Quais cenas podem ser cortadas sem afetar a história?",
                "Onde a história realmente começa? Posso cortar antes?",
                "Há subplots desnecessários?",
                "Quais personagens podem ser combinados?",
                "Onde repito informações?",
                "O que pode ser mostrado em montagem?",
                "Quais são os 'darlings' que preciso matar?",
                "A página 1 gruda o leitor?"
            ]
        }
        
        # Tracking de treinamento
        self.training_log = []
        self.improvements = []
        
    def load_nestor_screenplay(self) -> Dict:
        """Carrega o roteiro do Nestor (Sonhos Sem Lembranças)"""
        # Tenta primeiro o arquivo texto
        screenplay_txt = self.base_path / "roteiros" / "sonhos_sem_lembrancas.txt"
        screenplay_pdf = self.meus_filmes / "SONHOS SEM LEMBRANÇAS T.3.pdf"
        
        # Tenta carregar o .txt primeiro
        if screenplay_txt.exists():
            try:
                with open(screenplay_txt, 'r', encoding='utf-8') as file:
                    text = file.read()
                    lines = text.split('\n')
                    pages = len(lines) / 55  # ~55 lines per page standard
                    
                    return {
                        "title": "SONHOS SEM LEMBRANÇAS",
                        "content": text,
                        "pages": int(pages),
                        "protagonist": "Samantha",
                        "genre": "Thriller Psicológico"
                    }
            except Exception as e:
                print(f"⚠️ Erro ao ler TXT: {e}")
        
        # Se não conseguir, tenta o PDF
        if screenplay_pdf.exists() and HAS_PYPDF2:
            try:
                with open(screenplay_pdf, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    text = ""
                    for page in pdf_reader.pages:
                        text += page.extract_text()
                    
                    return {
                        "title": "SONHOS SEM LEMBRANÇAS",
                        "content": text,
                        "pages": len(pdf_reader.pages),
                        "protagonist": "Samantha",
                        "genre": "Thriller Psicológico"
                    }
            except Exception as e:
                print(f"❌ Erro ao ler PDF: {e}")
        
        print(f"❌ Roteiro não encontrado em nenhum formato")
        return {}
    
    def load_master_screenplay(self, title: str) -> Optional[str]:
        """Carrega um roteiro mestre para comparação"""
        master_files = {
            "Chinatown": "Chinatown - Screenplay.pdf",
            "The Godfather": "The Godfather - Screenplay.pdf",
            "Pulp Fiction": "Pulp Fiction - Release.pdf",
            "Casablanca": "Casablanca - Screenplay.pdf"
        }
        
        if title not in master_files:
            return None
            
        filepath = self.roteiros_mestres / master_files[title]
        
        try:
            with open(filepath, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages[:10]:  # Primeiras 10 páginas para análise
                    text += page.extract_text()
                return text
        except:
            return None
    
    def ask_scripturemon(self, prompt: str) -> str:
        """Envia pergunta para o Scripturemon"""
        try:
            result = subprocess.run(
                ["ollama", "run", self.model_name, prompt],
                capture_output=True,
                text=True,
                timeout=60
            )
            return result.stdout.strip()
        except Exception as e:
            return f"Erro: {e}"
    
    def create_analysis_prompt(self, question: str, category: str) -> str:
        """Cria prompt analítico profundo"""
        
        # Extrai trecho relevante do roteiro do Nestor
        screenplay_excerpt = self.nestor_screenplay.get("content", "")[:2000]
        
        # Carrega roteiro mestre relevante para comparação
        master_ref = "Chinatown" if "chinatown" in question.lower() else "The Godfather"
        master_excerpt = self.load_master_screenplay(master_ref) or ""
        
        prompt = f"""Como Scripturemon, Script Doctor profissional, analise profundamente:

PERGUNTA DO NESTOR: {question}
CATEGORIA: {category}

ROTEIRO DO NESTOR - "SONHOS SEM LEMBRANÇAS":
Protagonista: Samantha
Gênero: Thriller Psicológico
Páginas: {self.nestor_screenplay.get('pages', 'desconhecido')}

TRECHO RELEVANTE:
{screenplay_excerpt}

COMPARAÇÃO COM {master_ref}:
{master_excerpt[:1000]}

ANÁLISE REQUERIDA:
1. Identifique o problema ESPECÍFICO no roteiro do Nestor
2. Compare com a solução em {master_ref} (cite página e cena)
3. Explique a diferença técnica fundamental
4. Dê solução prática aplicável ao roteiro do Nestor
5. Preveja o impacto da mudança na história

Não cite teoria abstrata. Mostre exemplos concretos.
Seja brutalmente honesto mas construtivo."""

        return prompt
    
    def evaluate_response(self, response: str, question: str) -> Dict:
        """Avalia a qualidade da resposta do Scripturemon"""
        
        score = 0
        feedback = []
        
        # Critérios de Script Doctor profissional
        if "samantha" in response.lower():
            score += 20
            feedback.append("✅ Menciona protagonista corretamente")
        else:
            feedback.append("❌ Não menciona Samantha")
        
        if any(master in response.lower() for master in ["chinatown", "godfather", "pulp fiction"]):
            score += 20
            feedback.append("✅ Compara com roteiro mestre")
        else:
            feedback.append("❌ Falta comparação com mestres")
            
        if "página" in response.lower() or "page" in response.lower():
            score += 15
            feedback.append("✅ Cita páginas específicas")
        else:
            feedback.append("❌ Falta especificidade de páginas")
            
        if len(response) > 500:
            score += 15
            feedback.append("✅ Análise profunda")
        else:
            feedback.append("❌ Análise superficial")
            
        if any(word in response.lower() for word in ["solução", "sugiro", "reescreva", "mude"]):
            score += 20
            feedback.append("✅ Oferece solução prática")
        else:
            feedback.append("❌ Falta solução aplicável")
            
        if "diferença" in response.lower() or "contraste" in response.lower():
            score += 10
            feedback.append("✅ Analisa por contraste")
        else:
            feedback.append("❌ Falta análise comparativa")
        
        return {
            "score": score,
            "feedback": feedback,
            "needs_improvement": score < 70
        }
    
    def provide_correction(self, question: str, bad_response: str, evaluation: Dict) -> str:
        """Cria correção para treinar o Scripturemon"""
        
        correction = f"""
[CORREÇÃO DE SCRIPT DOCTOR]

Sua análise estava fraca. Score: {evaluation['score']}/100

PROBLEMAS:
{chr(10).join(evaluation['feedback'])}

COMO UM SCRIPT DOCTOR PROFISSIONAL RESPONDERIA:

"Analisando 'Sonhos Sem Lembranças', página [específica], vejo que [problema específico].

Em Chinatown, página 7, Towne resolve isso fazendo [exemplo concreto]. 
Em seu roteiro, Samantha [o que ela faz atualmente].

A DIFERENÇA FUNDAMENTAL: [análise técnica precisa]

SOLUÇÃO PRÁTICA para seu roteiro:
1. Na página X, mude [específico]
2. Reescreva a cena onde [específico]
3. Isso vai [impacto na história]

Isso resolve porque [justificativa técnica]."

LEMBRE-SE: 
- Sempre mencione Samantha e o roteiro do Nestor
- Compare com páginas específicas dos mestres
- Dê soluções práticas, não teoria
- Analise por contraste, não por citação
"""
        return correction
    
    def infinite_training_loop(self, iterations: int = 100):
        """Loop infinito de treinamento como Script Doctor"""
        
        print("=" * 60)
        print("🎬 SCRIPT DOCTOR INFINITE TRAINING")
        print("=" * 60)
        print(f"Roteiro: SONHOS SEM LEMBRANÇAS")
        print(f"Protagonista: Samantha")
        print(f"Páginas: {self.nestor_screenplay.get('pages', '?')}")
        print("=" * 60)
        
        for i in range(iterations):
            # Escolhe categoria e pergunta aleatória
            category = random.choice(list(self.doctor_questions.keys()))
            question = random.choice(self.doctor_questions[category])
            
            print(f"\n{'='*60}")
            print(f"🎬 ITERAÇÃO {i+1}/{iterations}")
            print(f"📂 Categoria: {category}")
            print(f"❓ Pergunta: {question}")
            
            # Cria prompt analítico
            prompt = self.create_analysis_prompt(question, category)
            
            # Pergunta ao Scripturemon
            print("🤔 Scripturemon analisando...")
            response = self.ask_scripturemon(prompt)
            
            # Avalia resposta
            evaluation = self.evaluate_response(response, question)
            
            print(f"📊 Score: {evaluation['score']}/100")
            
            # Se precisa melhorar, fornece correção
            if evaluation['needs_improvement']:
                print("❌ Resposta precisa melhorar. Enviando correção...")
                correction = self.provide_correction(question, response, evaluation)
                
                # Ensina o Scripturemon
                teaching_prompt = f"{correction}\n\nAgora, tente novamente com esse conhecimento: {question}"
                improved_response = self.ask_scripturemon(teaching_prompt)
                
                # Reavalia
                new_evaluation = self.evaluate_response(improved_response, question)
                improvement = new_evaluation['score'] - evaluation['score']
                
                if improvement > 0:
                    print(f"✅ Melhorou! +{improvement} pontos")
                else:
                    print(f"⚠️ Ainda precisa trabalho")
                
                self.improvements.append(improvement)
            else:
                print("✅ Boa análise!")
            
            # Log
            self.training_log.append({
                "iteration": i+1,
                "category": category,
                "question": question,
                "score": evaluation['score'],
                "improved": evaluation['score'] >= 70
            })
            
            # A cada 10 iterações, mostra progresso
            if (i+1) % 10 == 0:
                self.show_progress()
            
            # Pausa pequena
            time.sleep(2)
        
        # Relatório final
        self.final_report()
    
    def show_progress(self):
        """Mostra progresso do treinamento"""
        recent = self.training_log[-10:]
        avg_score = sum(item['score'] for item in recent) / len(recent)
        
        print("\n" + "="*60)
        print("📊 PROGRESSO (últimas 10 iterações)")
        print(f"Score médio: {avg_score:.1f}/100")
        
        by_category = {}
        for item in recent:
            cat = item['category']
            if cat not in by_category:
                by_category[cat] = []
            by_category[cat].append(item['score'])
        
        for cat, scores in by_category.items():
            avg = sum(scores) / len(scores)
            print(f"  {cat}: {avg:.1f}/100")
        print("="*60)
    
    def final_report(self):
        """Relatório final do treinamento"""
        print("\n" + "="*60)
        print("🏆 RELATÓRIO FINAL - SCRIPT DOCTOR TRAINING")
        print("="*60)
        
        total_score = sum(item['score'] for item in self.training_log) / len(self.training_log)
        print(f"\n📊 SCORE FINAL: {total_score:.1f}/100")
        
        # Por categoria
        by_category = {}
        for item in self.training_log:
            cat = item['category']
            if cat not in by_category:
                by_category[cat] = []
            by_category[cat].append(item['score'])
        
        print("\n📈 PERFORMANCE POR CATEGORIA:")
        for cat, scores in sorted(by_category.items()):
            avg = sum(scores) / len(scores)
            bar = "█" * int(avg/5) + "░" * (20 - int(avg/5))
            print(f"  {cat:12} [{bar}] {avg:.1f}%")
        
        # Melhoria total
        if self.improvements:
            total_improvement = sum(self.improvements)
            avg_improvement = total_improvement / len(self.improvements)
            print(f"\n🚀 MELHORIA MÉDIA: {avg_improvement:+.1f} pontos por correção")
        
        # Salva relatório
        report_path = self.base_path / f"script_doctor_report_{time.strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_path, 'w') as f:
            json.dump({
                "final_score": total_score,
                "by_category": {cat: sum(scores)/len(scores) 
                              for cat, scores in by_category.items()},
                "improvements": self.improvements,
                "log": self.training_log
            }, f, indent=2)
        
        print(f"\n💾 Relatório salvo: {report_path}")
        
        # Status
        if total_score >= 85:
            print("\n🎉 SCRIPTUREMON É UM SCRIPT DOCTOR PROFISSIONAL!")
        elif total_score >= 70:
            print("\n✅ Scripturemon está quase lá!")
        else:
            print("\n📚 Continue treinando para melhorar")
        
        print("="*60)


if __name__ == "__main__":
    print("🎬 SCRIPT DOCTOR INFINITE TRAINING SYSTEM")
    print("="*60)
    print("Este sistema vai treinar o Scripturemon como Script Doctor")
    print("analisando profundamente 'Sonhos Sem Lembranças'")
    print("="*60)
    
    # PyPDF2 é opcional, vamos usar arquivos texto
    
    doctor = ScriptDoctorInfinite()
    
    if not doctor.nestor_screenplay:
        print("❌ Não foi possível carregar o roteiro")
        print("Certifique-se que 'SONHOS SEM LEMBRANÇAS T.3.pdf' está em:")
        print("/Users/clubproducoes/Digimundo/BIBLIOTECA_ROTEIROS/meus_filmes/")
    else:
        print(f"✅ Roteiro carregado: {doctor.nestor_screenplay['pages']} páginas")
        print("\n🚀 Iniciando treinamento infinito...")
        time.sleep(2)
        
        doctor.infinite_training_loop(10)  # 10 iterações de demonstração