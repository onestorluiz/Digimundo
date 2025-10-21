"""
Estratégia de múltiplos modelos Ollama para diferentes tarefas
Usa modelos específicos para cada tipo de análise
"""
import ollama
from typing import Dict, Any, Optional
import json

class OllamaStrategy:
    """
    Estratégia inteligente usando 2 modelos:
    1. llama3.2:3b (2GB) - Para extração rápida e estruturada
    2. mistral:latest (4.4GB) - Para análise profunda e criativa
    """
    
    def __init__(self):
        self.models = {
            "extractor": {
                "name": "llama3.2:3b",  # Rápido, 2GB
                "role": "Extração de dados estruturados",
                "options": {
                    "temperature": 0.1,  # Muito determinístico
                    "top_p": 0.7,
                    "num_ctx": 4096,
                    "num_predict": 300
                }
            },
            "analyzer": {
                "name": "mistral:latest",  # Poderoso, 4.4GB
                "role": "Análise profunda e comparações",
                "options": {
                    "temperature": 0.7,  # Mais criativo
                    "top_p": 0.9,
                    "num_ctx": 8192,
                    "num_predict": 500
                }
            },
            "scripturemon": {
                "name": "scripturemon-maestro:latest",  # Personalidade brutal
                "role": "Feedback final com personalidade",
                "options": {
                    "temperature": 0.65,
                    "top_p": 0.9,
                    "num_ctx": 16384,
                    "num_predict": 1000
                }
            }
        }
    
    def extract_structure(self, text: str) -> Dict[str, Any]:
        """Usa llama3.2 para extração rápida de estrutura"""
        prompt = f"""Extract screenplay structure as JSON:
        - acts: [list of acts with page numbers]
        - scenes: total count
        - characters: [main character names]
        
        Text: {text[:3000]}
        
        Return ONLY valid JSON:"""
        
        try:
            response = ollama.generate(
                model=self.models["extractor"]["name"],
                prompt=prompt,
                options=self.models["extractor"]["options"]
            )
            return json.loads(response['response'])
        except:
            return {
                "acts": [{"act": 1, "pages": 30}, {"act": 2, "pages": 60}, {"act": 3, "pages": 30}],
                "scenes": text.count("INT.") + text.count("EXT."),
                "characters": []
            }
    
    def analyze_techniques(self, text: str) -> Dict[str, Any]:
        """Usa mistral para análise profunda de técnicas"""
        prompt = f"""Analyze screenplay techniques used:
        
        Text sample: {text[:4000]}
        
        List:
        1. Narrative techniques (flashback, voice-over, etc)
        2. Visual techniques (montage, split-screen, etc)
        3. Dialog techniques (subtext, conflict, etc)
        4. Structure techniques (three-act, non-linear, etc)
        
        Be specific with examples:"""
        
        try:
            response = ollama.generate(
                model=self.models["analyzer"]["name"],
                prompt=prompt,
                options=self.models["analyzer"]["options"]
            )
            
            # Parse response into categories
            result = response['response']
            techniques = []
            
            for line in result.split('\n'):
                if any(word in line.lower() for word in ['flashback', 'voice-over', 'montage', 'split-screen']):
                    techniques.append(line.strip())
            
            return {
                "techniques": techniques[:10],
                "analysis": result[:500]
            }
        except:
            return {
                "techniques": ["Dialogue", "Action", "Description"],
                "analysis": "Standard screenplay format"
            }
    
    def brutal_evaluation(self, text: str, initial_analysis: Dict) -> Dict[str, Any]:
        """Usa scripturemon-maestro para avaliação brutal final"""
        
        # Preparar contexto com análises anteriores
        context = f"""
        ESTRUTURA DETECTADA: {json.dumps(initial_analysis.get('structure', {}), indent=2)}
        TÉCNICAS ENCONTRADAS: {', '.join(initial_analysis.get('techniques', [])[:5])}
        
        AMOSTRA DO ROTEIRO:
        {text[:3000]}
        """
        
        prompt = f"""Como Scripturemon, avalie brutalmente este roteiro:
        
        {context}
        
        Compare com Chinatown, The Godfather, Citizen Kane.
        Seja BRUTAL. Nota base: 62/100.
        
        Formato:
        NOTA: [número]/100
        COMPARAÇÃO: [com qual mestre e por quê]
        PROBLEMA PRINCIPAL: [em uma frase]
        CONSELHO BRUTAL: [em uma frase]"""
        
        try:
            response = ollama.generate(
                model=self.models["scripturemon"]["name"],
                prompt=prompt,
                options=self.models["scripturemon"]["options"]
            )
            
            result = response['response']
            
            # Extrair nota
            import re
            nota_match = re.search(r'NOTA:\s*(\d+)', result)
            nota = int(nota_match.group(1)) if nota_match else 62
            
            return {
                "nota_geral": nota,
                "feedback_completo": result,
                "modelo_usado": "scripturemon-maestro"
            }
        except:
            return {
                "nota_geral": 62,
                "feedback_completo": "Comparado a Chinatown, ainda é trabalho amador.",
                "modelo_usado": "fallback"
            }
    
    def process_complete(self, text: str, doc_type: str = "roteiro_criador") -> Dict[str, Any]:
        """Pipeline completo usando estratégia de múltiplos modelos"""
        
        print("📊 [1/3] Extraindo estrutura com llama3.2...")
        structure = self.extract_structure(text)
        
        print("🔍 [2/3] Analisando técnicas com mistral...")
        techniques = self.analyze_techniques(text)
        
        print("💀 [3/3] Avaliação brutal com scripturemon...")
        evaluation = self.brutal_evaluation(text, {
            "structure": structure,
            "techniques": techniques["techniques"]
        })
        
        return {
            "estrutura": structure,
            "tecnicas": techniques["techniques"],
            "analise_profunda": techniques["analysis"],
            "avaliacao": evaluation,
            "doc_type": doc_type,
            "modelos_usados": {
                "extractor": self.models["extractor"]["name"],
                "analyzer": self.models["analyzer"]["name"],
                "evaluator": self.models["scripturemon"]["name"]
            }
        }
    
    def verify_models(self) -> Dict[str, bool]:
        """Verifica quais modelos estão disponíveis"""
        status = {}
        for role, config in self.models.items():
            try:
                ollama.show(config["name"])
                status[role] = True
            except:
                status[role] = False
        return status