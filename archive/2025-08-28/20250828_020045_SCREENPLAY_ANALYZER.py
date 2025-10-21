#!/usr/bin/env python3
"""
📖 SCREENPLAY ANALYZER - Sistema de Análise Profunda de Roteiros
Permite ao Scripturemon ler e analisar roteiros completos
"""

import os
import sys
import json
from pathlib import Path
from typing import Dict, List, Optional
import subprocess

class ScreenplayAnalyzer:
    def __init__(self):
        self.base_path = Path.home() / "Digimundo"
        self.screenplays_path = self.base_path / "roteiros"
        self.analysis_cache = self.base_path / "analysis_cache"
        
        # Criar diretórios se não existirem
        self.screenplays_path.mkdir(parents=True, exist_ok=True)
        self.analysis_cache.mkdir(parents=True, exist_ok=True)
        
    def load_screenplay(self, filepath: str) -> Optional[str]:
        """Carrega um roteiro do arquivo"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"Erro ao ler roteiro: {e}")
            return None
    
    def analyze_structure(self, screenplay: str) -> Dict:
        """Analisa estrutura do roteiro"""
        
        lines = screenplay.split('\n')
        total_pages = len(lines) / 55  # Aproximadamente 55 linhas por página
        
        analysis = {
            "total_pages": int(total_pages),
            "acts": {
                "act_1": {"pages": 1, "to": int(total_pages * 0.25)},
                "act_2": {"pages": int(total_pages * 0.25), "to": int(total_pages * 0.75)},
                "act_3": {"pages": int(total_pages * 0.75), "to": int(total_pages)}
            },
            "plot_points": {
                "inciting_incident": int(total_pages * 0.10),
                "plot_point_1": int(total_pages * 0.25),
                "midpoint": int(total_pages * 0.50),
                "plot_point_2": int(total_pages * 0.75),
                "climax": int(total_pages * 0.90)
            }
        }
        
        # Contar elementos
        dialogue_lines = sum(1 for line in lines if line.strip() and not line.isupper() and '(' not in line)
        action_lines = sum(1 for line in lines if line.strip() and line.isupper() and ':' not in line)
        
        analysis["elements"] = {
            "dialogue_percentage": (dialogue_lines / len(lines)) * 100,
            "action_percentage": (action_lines / len(lines)) * 100,
            "scenes": screenplay.count('INT.') + screenplay.count('EXT.')
        }
        
        return analysis
    
    def compare_with_references(self, screenplay: str, issue: str) -> Dict:
        """Compara com roteiros de referência"""
        
        references = {
            "dialogue": {
                "The Social Network": "Diálogo como ping-pong verbal, conflito em cada linha",
                "Pulp Fiction": "Diálogo mundano que revela caráter",
                "His Girl Friday": "Overlapping dialogue, ritmo frenético"
            },
            "structure": {
                "Chinatown": "Cada cena revela e esconde informação simultaneamente",
                "The Godfather": "Paralelos entre família e negócios em cada ato",
                "Star Wars": "Hero's journey clássica com todos os 17 passos"
            },
            "character": {
                "Taxi Driver": "Descida gradual através de detalhes visuais",
                "There Will Be Blood": "Ambição como motor de cada ação",
                "The Dark Knight": "Protagonista e antagonista como espelhos"
            },
            "pacing": {
                "Mad Max Fury Road": "Ação que nunca para mas tem ritmo",
                "Before Sunset": "Tempo real criando urgência",
                "Dunkirk": "Três timelines criando tensão crescente"
            }
        }
        
        # Análise específica baseada no problema
        relevant_refs = references.get(issue, references["structure"])
        
        comparison = {
            "issue": issue,
            "references": relevant_refs,
            "analysis": f"Comparando com os mestres do {issue}..."
        }
        
        return comparison
    
    def generate_deep_analysis(self, screenplay_path: str, question: str) -> str:
        """Gera análise profunda para o Scripturemon"""
        
        # Carrega roteiro
        screenplay = self.load_screenplay(screenplay_path)
        if not screenplay:
            return "Não consegui ler o roteiro. Verifique o arquivo."
        
        # Análise estrutural
        structure = self.analyze_structure(screenplay)
        
        # Determina tipo de análise necessária
        issue_type = self.determine_issue_type(question)
        
        # Compara com referências
        comparison = self.compare_with_references(screenplay, issue_type)
        
        # Gera relatório para Scripturemon
        analysis = f"""
ANÁLISE PROFUNDA DO ROTEIRO:

📊 ESTRUTURA DETECTADA:
- Total: {structure['total_pages']} páginas
- Ato 1: páginas {structure['acts']['act_1']['pages']}-{structure['acts']['act_1']['to']}
- Ato 2: páginas {structure['acts']['act_2']['pages']}-{structure['acts']['act_2']['to']}  
- Ato 3: páginas {structure['acts']['act_3']['pages']}-{structure['acts']['act_3']['to']}

📍 PLOT POINTS ESPERADOS:
- Inciting Incident: página {structure['plot_points']['inciting_incident']}
- Plot Point 1: página {structure['plot_points']['plot_point_1']}
- Midpoint: página {structure['plot_points']['midpoint']}
- Plot Point 2: página {structure['plot_points']['plot_point_2']}

📈 PROPORÇÕES:
- Diálogo: {structure['elements']['dialogue_percentage']:.1f}%
- Ação: {structure['elements']['action_percentage']:.1f}%
- Total de cenas: {structure['elements']['scenes']}

🎬 COMPARAÇÃO COM REFERÊNCIAS ({issue_type}):
{json.dumps(comparison['references'], indent=2, ensure_ascii=False)}

💡 ANÁLISE ESPECÍFICA:
{comparison['analysis']}

TRECHOS RELEVANTES DO ROTEIRO:
{self.extract_relevant_excerpts(screenplay, question)}
"""
        
        return analysis
    
    def determine_issue_type(self, question: str) -> str:
        """Determina tipo de problema baseado na pergunta"""
        
        question_lower = question.lower()
        
        if any(word in question_lower for word in ["diálogo", "fala", "conversa"]):
            return "dialogue"
        elif any(word in question_lower for word in ["estrutura", "ato", "ritmo", "plot"]):
            return "structure"
        elif any(word in question_lower for word in ["personagem", "protagonista", "herói", "vilão"]):
            return "character"
        elif any(word in question_lower for word in ["ritmo", "pacing", "lento", "arrastado"]):
            return "pacing"
        else:
            return "structure"
    
    def extract_relevant_excerpts(self, screenplay: str, question: str) -> str:
        """Extrai trechos relevantes do roteiro"""
        
        lines = screenplay.split('\n')
        
        # Pega amostra do início, meio e fim
        excerpts = []
        
        # Início (primeiras 100 linhas)
        if len(lines) > 100:
            excerpts.append("INÍCIO:\n" + '\n'.join(lines[:100]))
        
        # Meio (em volta da página 60)
        if len(lines) > 3300:  # ~60 páginas
            middle = len(lines) // 2
            excerpts.append("\nMEIO (Midpoint):\n" + '\n'.join(lines[middle-50:middle+50]))
        
        # Fim (últimas 100 linhas)  
        if len(lines) > 200:
            excerpts.append("\nFIM:\n" + '\n'.join(lines[-100:]))
        
        return '\n'.join(excerpts[:500])  # Limita tamanho
    
    def send_to_scripturemon(self, analysis: str, question: str) -> str:
        """Envia análise para Scripturemon processar"""
        
        prompt = f"""
Como Scripturemon, analise profundamente:

PERGUNTA DO NESTOR: {question}

ANÁLISE DO ROTEIRO:
{analysis}

Agora compare com os mestres e dê feedback específico e aplicável.
Não cite teoria - mostre COMO aplicar no roteiro do Nestor.
"""
        
        try:
            result = subprocess.run(
                ["ollama", "run", "scripturemon-sdl", prompt],
                capture_output=True,
                text=True,
                timeout=60
            )
            return result.stdout.strip()
        except Exception as e:
            return f"Erro ao processar com Scripturemon: {e}"


def main():
    """Função principal para testar"""
    
    analyzer = ScreenplayAnalyzer()
    
    print("🎬 SCREENPLAY ANALYZER")
    print("=" * 50)
    
    # Verifica se há roteiro para analisar
    roteiros = list(analyzer.screenplays_path.glob("*.txt")) + \
               list(analyzer.screenplays_path.glob("*.fountain")) + \
               list(analyzer.screenplays_path.glob("*.pdf"))
    
    if not roteiros:
        print("📝 Nenhum roteiro encontrado em ~/Digimundo/roteiros/")
        print("   Coloque seu roteiro lá (.txt, .fountain ou .pdf)")
        
        # Cria roteiro exemplo
        exemplo = analyzer.screenplays_path / "exemplo.txt"
        with open(exemplo, 'w') as f:
            f.write("""FADE IN:

INT. CAFÉ - DIA

JOÃO, 30s, nervoso, olha para o relógio.

MARIA entra apressada.

MARIA
Desculpa o atraso.

JOÃO
Tudo bem. Precisamos conversar.

MARIA
Eu sei.

FADE OUT.""")
        print(f"\n✅ Roteiro exemplo criado em: {exemplo}")
        return
    
    print(f"📚 Roteiros disponíveis:")
    for i, roteiro in enumerate(roteiros, 1):
        print(f"   {i}. {roteiro.name}")
    
    # Análise interativa
    while True:
        print("\n" + "=" * 50)
        choice = input("Escolha o roteiro (número) ou 'sair': ")
        
        if choice.lower() == 'sair':
            break
            
        try:
            idx = int(choice) - 1
            roteiro_path = roteiros[idx]
            
            question = input("Qual sua pergunta sobre o roteiro? ")
            
            print("\n🔍 Analisando profundamente...")
            analysis = analyzer.generate_deep_analysis(str(roteiro_path), question)
            
            print("\n📊 ANÁLISE COMPLETA:")
            print(analysis)
            
            print("\n🎬 Consultando Scripturemon...")
            response = analyzer.send_to_scripturemon(analysis, question)
            
            print("\n💬 SCRIPTUREMON RESPONDE:")
            print(response)
            
        except (ValueError, IndexError):
            print("❌ Escolha inválida")
        except Exception as e:
            print(f"❌ Erro: {e}")


if __name__ == "__main__":
    main()