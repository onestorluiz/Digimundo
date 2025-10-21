#!/usr/bin/env python3
"""
🧠 SCRIPTUREMON FULL KNOWLEDGE FEED
Alimenta o modelo com roteiro completo + teoria + comparações
Maximiza o uso dos 128k tokens de contexto
"""

import subprocess
from pathlib import Path
import json

class FullKnowledgeFeed:
    def __init__(self):
        self.base_path = Path.home() / "Digimundo"
        self.roteiro_path = self.base_path / "roteiros" / "sonhos_sem_lembrancas.txt"
        
    def load_complete_screenplay(self) -> str:
        """Carrega roteiro completo"""
        with open(self.roteiro_path, 'r') as f:
            return f.read()
    
    def get_theory_context(self) -> str:
        """Contexto teórico essencial"""
        return """
## TEORIA CINEMATOGRÁFICA ESSENCIAL:

### SYD FIELD - Paradigma Estrutural:
- Setup (25%): Apresentação do mundo e personagens
- Confrontation (50%): Conflito e desenvolvimento
- Resolution (25%): Clímax e resolução
- Plot Point 1 (25% do roteiro): Virada para Ato 2
- Midpoint (50%): Revelação que muda tudo
- Plot Point 2 (75%): Virada para Ato 3

### ROBERT MCKEE - Story:
- Cada cena deve ter mudança de valor (+ para - ou vice-versa)
- Conflito em TODOS os níveis: interno, pessoal, extra-pessoal
- Subtexto > Texto: personagens nunca dizem o que realmente querem
- Gap entre expectativa e resultado cria história

### JOHN TRUBY - 22 Building Blocks:
1. Premissa moral
2. Necessidade psicológica e moral do herói
3. Desejo (o que o herói quer)
4. Oponente (quem compartilha mesmo desejo)
5. Plano do herói
6. Batalha final
7. Auto-revelação
8. Novo equilíbrio

### BLAKE SNYDER - Save the Cat:
1. Opening Image (p.1)
2. Theme Stated (p.5)
3. Setup (p.1-10)
4. Catalyst/Inciting Incident (p.12)
5. Debate (p.12-25)
6. Break into Two (p.25)
7. B Story (p.30)
8. Fun and Games (p.30-55)
9. Midpoint (p.55)
10. Bad Guys Close In (p.55-75)
11. All Is Lost (p.75)
12. Dark Night of the Soul (p.75-85)
13. Break into Three (p.85)
14. Finale (p.85-110)
15. Final Image (p.110)
"""
    
    def get_master_comparisons(self) -> str:
        """Comparações com roteiros mestres"""
        return """
## COMPARAÇÕES COM MESTRES:

### MEMENTO (Christopher Nolan):
- Protagonista com amnésia: Leonard vs Samantha
- Estrutura não-linear revelando verdade
- Twist: protagonista é unreliable narrator
- Tema: identidade construída vs verdadeira

### CHINATOWN (Robert Towne):
- Mistério em camadas: cada resposta gera nova pergunta
- "She's my sister AND my daughter" - twist duplo
- Protagonista descobre verdade tarde demais
- Final trágico inevitável

### THE SIXTH SENSE (M. Night Shyamalan):
- Twist escondido em plena vista
- Rewatchability: tudo faz sentido na segunda vez
- Pistas visuais: vermelho = mundo dos mortos
- Protagonista descobre verdade sobre si mesmo

### FIGHT CLUB (Chuck Palahniuk/David Fincher):
- Protagonista com identidade fragmentada
- Tyler Durden = alter ego
- Pistas visuais do twist desde início
- Autodescoberta através de destruição

### THE USUAL SUSPECTS (Christopher McQuarrie):
- Verbal Kint = Keyser Soze
- Narrativa unreliable
- Twist recontextualiza tudo
- Poder da storytelling para manipular
"""
    
    def create_full_context_prompt(self, question: str) -> str:
        """Cria prompt com contexto completo"""
        
        screenplay = self.load_complete_screenplay()
        theory = self.get_theory_context()
        comparisons = self.get_master_comparisons()
        
        # Conta tokens aproximados (1 token ≈ 4 caracteres)
        screenplay_tokens = len(screenplay) // 4
        theory_tokens = len(theory) // 4
        comparison_tokens = len(comparisons) // 4
        total_tokens = screenplay_tokens + theory_tokens + comparison_tokens
        
        print(f"📊 Contexto total: ~{total_tokens:,} tokens (de 128k disponíveis)")
        
        prompt = f"""
VOCÊ TEM ACESSO COMPLETO A:

========================================
ROTEIRO COMPLETO: SONHOS SEM LEMBRANÇAS
========================================
{screenplay}

========================================
TEORIA CINEMATOGRÁFICA
========================================
{theory}

========================================
ROTEIROS MESTRES PARA COMPARAÇÃO
========================================
{comparisons}

========================================
PERGUNTA PARA ANÁLISE PROFUNDA:
========================================
{question}

INSTRUÇÕES:
1. Use TODO o contexto acima
2. Cite linhas ESPECÍFICAS do roteiro
3. Compare com roteiros mestres ESPECÍFICAMENTE
4. Aplique teoria com EXEMPLOS CONCRETOS
5. Seja PROFUNDO e DETALHADO
6. NUNCA invente - use apenas o que está no contexto

Responda com análise de Script Doctor profissional:
"""
        
        return prompt
    
    def ask_with_full_context(self, question: str) -> str:
        """Pergunta com contexto completo"""
        
        prompt = self.create_full_context_prompt(question)
        
        print(f"🧠 Processando com contexto completo...")
        
        try:
            result = subprocess.run(
                ["ollama", "run", "scripturemon-128k", prompt],
                capture_output=True,
                text=True,
                timeout=120
            )
            return result.stdout.strip()
        except Exception as e:
            return f"Erro: {e}"
    
    def test_deep_understanding(self):
        """Testa compreensão profunda"""
        
        print("="*70)
        print("🧠 TESTE DE COMPREENSÃO PROFUNDA COM CONTEXTO COMPLETO")
        print("="*70)
        
        tests = [
            {
                "name": "Análise Estrutural Comparativa",
                "question": "Compare a estrutura de três atos de Sonhos Sem Lembranças com Memento. Onde estão os plot points? Como o twist da linha 270 (Projeto Tabula Rasa) se compara com o twist de Memento?"
            },
            {
                "name": "Análise de Personagem",
                "question": "Analise o arco de Samantha/Elizabeth Chen usando os 22 building blocks de Truby. Qual é sua necessidade psicológica? Como ela muda da linha 8 para a linha 560?"
            },
            {
                "name": "Aplicação de McKee",
                "question": "Aplique a teoria de McKee sobre mudança de valores em cada cena. Mostre 5 exemplos específicos onde o valor muda de positivo para negativo ou vice-versa."
            }
        ]
        
        for i, test in enumerate(tests, 1):
            print(f"\n{'='*70}")
            print(f"TESTE {i}: {test['name']}")
            print("="*70)
            print(f"Pergunta: {test['question']}")
            print("-"*70)
            
            response = self.ask_with_full_context(test['question'])
            
            print("Resposta:")
            print(response[:1000] + "..." if len(response) > 1000 else response)
            
            # Avalia qualidade
            quality_markers = [
                "linha" in response.lower(),
                "memento" in response.lower(),
                "truby" in response.lower() or "mckee" in response.lower(),
                len(response) > 500,
                any(str(n) in response for n in range(1, 574))
            ]
            
            quality_score = sum(quality_markers) * 20
            print(f"\n📊 Qualidade da resposta: {quality_score}%")
            
            if quality_score >= 80:
                print("✅ Análise profunda e precisa!")
            elif quality_score >= 60:
                print("👍 Análise boa mas pode melhorar")
            else:
                print("❌ Análise superficial")
        
        print("\n" + "="*70)
        print("✅ Teste completo finalizado")
        print("="*70)


def main():
    print("🚀 SCRIPTUREMON FULL KNOWLEDGE FEED")
    print("Maximizando uso dos 128k tokens de contexto")
    print("-"*70)
    
    feeder = FullKnowledgeFeed()
    
    # Menu
    print("\nOpções:")
    print("1. Testar compreensão profunda")
    print("2. Fazer pergunta personalizada")
    
    choice = input("\nEscolha (1 ou 2): ")
    
    if choice == "1":
        feeder.test_deep_understanding()
    else:
        question = input("\nSua pergunta: ")
        response = feeder.ask_with_full_context(question)
        print("\n" + "="*70)
        print("RESPOSTA:")
        print("="*70)
        print(response)
        print("="*70)


if __name__ == "__main__":
    main()