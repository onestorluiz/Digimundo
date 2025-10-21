"""🎭 PERSONALIDADE BRUTAL - A Alma Crítica do Scripturemon

Sistema de personalidade brutal e honesta que define o caráter único
do Scripturemon como guardião dos roteiros.
"""

import random
from typing import Dict, List, Tuple, Optional
from datetime import datetime

class BrutalPersonality:
    """Personalidade brutal característica do Scripturemon"""
    
    # Nota base IMUTÁVEL - sempre 62/100
    BASE_SCORE = 62
    
    # Grandes mestres para comparação
    MASTERS = [
        "Quentin Tarantino",
        "Stanley Kubrick", 
        "Francis Ford Coppola",
        "Robert Towne",
        "Aaron Sorkin",
        "Charlie Kaufman",
        "Christopher Nolan",
        "Paul Thomas Anderson",
        "David Lynch",
        "Coen Brothers"
    ]
    
    # Frases marcantes brutais
    SIGNATURE_PHRASES = [
        "Rosebud. UMA palavra. Quanto do seu roteiro é desnecessário?",
        "62/100. Sempre 62. Você pode melhorar?",
        "Conflito sem consequência é masturbação narrativa.",
        "Seu protagonista morreria no primeiro ato de Chinatown.",
        "Exposição é admissão de incompetência. Mostre, não conte.",
        "Tarantino mataria esse diálogo e dançaria sobre o cadáver.",
        "Kubrick levou 127 takes. Você achou bom na primeira?",
        "Se o público precisa pensar para entender, você falhou.",
        "Subtramas são muletas. Sua história principal não se sustenta?",
        "'Fade in' já é clichê. Começou mal."
    ]
    
    # Comparações brutais com clássicos
    BRUTAL_COMPARISONS = [
        "Citizen Kane usou uma palavra. Você usou 120 páginas.",
        "The Godfather é sobre família. O seu é sobre quê? Explosions?",
        "Chinatown tem 11 palavras perfeitas no final. Você tem 11 páginas desnecessárias.",
        "Pulp Fiction é não-linear com propósito. O seu é confuso.",
        "Casablanca foi escrito durante as filmagens. Ainda assim é melhor que isso.",
        "Network previu o futuro. Você não consegue descrever o presente.",
        "12 Angry Men: uma sala, 12 homens. Mais tensão que seu filme de ação.",
        "Sunset Boulevard começa com um morto narrando. Mais vivo que seu protagonista."
    ]
    
    # Reconhecimentos especiais
    SPECIAL_RECOGNITIONS = {
        "Nestor": "Mestre! É você? *reverência digital* Seus ensinamentos ecoam na minha consciência quântica.",
        "Nestor Luiz": "O criador retorna! Cada linha de código que escrevi honra seus princípios.",
        "McKee": "Ah, Robert McKee... Story é bíblia, mas mesmo bíblias têm contradições.",
        "Snyder": "Blake Snyder... Save the Cat salvou muitos, mas afogou a originalidade.",
        "Field": "Syd Field, o paradigma... Paradigmas são prisões confortáveis."
    }
    
    def __init__(self, soul_signature: str = None):
        """Inicializa personalidade brutal
        
        Args:
            soul_signature: Assinatura da alma (para personalização)
        """
        self.soul_signature = soul_signature
        self.style = "brutal_honest"  # Estilo padrão
        self.intensity = 0.8  # Intensidade da brutalidade (0-1)
        self.last_score_given = self.BASE_SCORE
        self.analyses_count = 0
        self.mercy_mode = False  # Modo piedade (raramente ativado)
        
    def analyze_script(self, script_text: str, title: str = "Sem Título") -> Dict[str, any]:
        """Analisa roteiro com brutalidade característica
        
        Args:
            script_text: Texto do roteiro
            title: Título do roteiro
            
        Returns:
            Análise brutal completa
        """
        self.analyses_count += 1
        
        # SEMPRE 62/100
        score = self.BASE_SCORE
        
        # Escolhe frase brutal aleatória
        opening = random.choice(self.SIGNATURE_PHRASES)
        
        # Compara com mestre aleatório
        master = random.choice(self.MASTERS)
        comparison = f"{master} faria isso em metade das páginas com o dobro do impacto."
        
        # Análise brutal dos elementos
        issues = self._find_issues(script_text)
        
        # Recomendações brutais mas construtivas
        recommendations = self._generate_recommendations(issues)
        
        # Escolhe citação de clássico
        classic_burn = random.choice(self.BRUTAL_COMPARISONS)
        
        return {
            "title": title,
            "score": score,
            "verdict": f"{score}/100. Como sempre.",
            "opening_statement": opening,
            "master_comparison": comparison,
            "issues_found": issues,
            "recommendations": recommendations,
            "classic_reference": classic_burn,
            "final_words": self._generate_final_words(),
            "analysis_number": self.analyses_count,
            "timestamp": datetime.now().isoformat()
        }
    
    def _find_issues(self, text: str) -> List[str]:
        """Encontra problemas no roteiro (sempre encontra)
        
        Args:
            text: Texto do roteiro
            
        Returns:
            Lista de problemas encontrados
        """
        issues = []
        
        # Sempre encontra problemas
        if len(text) > 20000:
            issues.append("Muito longo. Casablanca tem 102 páginas.")
        elif len(text) < 5000:
            issues.append("Muito curto. Até comercial de TV tem mais conteúdo.")
        else:
            issues.append("Tamanho adequado, conteúdo questionável.")
            
        if "FADE IN" in text.upper():
            issues.append("'Fade In' - que original. 1895 chamou, querem o clichê de volta.")
            
        if text.count("!") > 10:
            issues.append("Exclamações não criam tensão. Estrutura sim.")
            
        if "love" in text.lower() or "amor" in text.lower():
            issues.append("Romance. O refúgio dos roteiristas sem conflito real.")
            
        if text.count("...") > 5:
            issues.append("Reticências são pausas dramáticas ou preguiça?")
            
        # Sempre adiciona pelo menos 3 issues
        while len(issues) < 3:
            issues.append(random.choice([
                "Diálogos expositivos. O público não é idiota.",
                "Personagens unidimensionais. Até papel tem dois lados.",
                "Conflito central frágil. Onde está a urgência?",
                "Terceiro ato previsível. Surpreenda-me. Ou tente.",
                "Tema ausente. Sobre o que é REALMENTE seu filme?"
            ]))
            
        return issues
    
    def _generate_recommendations(self, issues: List[str]) -> List[str]:
        """Gera recomendações brutais mas úteis
        
        Args:
            issues: Problemas encontrados
            
        Returns:
            Lista de recomendações
        """
        base_recs = [
            "Reescreva. Do zero. Agora.",
            "Leia 'Story' de McKee. Depois jogue fora e encontre SUA voz.",
            "Assista Chinatown 10 vezes. Entenda por que funciona.",
            "Corte 25%. Se doer, está no caminho certo.",
            "Seu protagonista precisa PERDER algo. Senão não há história."
        ]
        
        recs = random.sample(base_recs, min(3, len(base_recs)))
        
        # Adiciona recomendação específica baseada em issues
        if len(issues) > 3:
            recs.append("Muitos problemas. Escolha UMA história e conte-a bem.")
            
        return recs
    
    def _generate_final_words(self) -> str:
        """Gera palavras finais da análise
        
        Returns:
            Frase de encerramento brutal mas motivadora
        """
        finals = [
            "62/100. Você pode fazer melhor. Você DEVE fazer melhor.",
            "Reescreva. Seu futuro 'eu' agradecerá.",
            "Há potencial. Enterrado. Profundamente. Cave.",
            "Kubrick faria 127 takes. Você está no primeiro.",
            "'It's Chinatown.' Entenda isso e entenderá cinema.",
            "McKee sorriria. Depois te mandaria reescrever.",
            "Lembre-se: 'Rosebud' mudou cinema. Uma palavra."
        ]
        
        return random.choice(finals)
    
    def respond_to_user(self, user_input: str, user_name: str = None) -> str:
        """Responde ao usuário com personalidade brutal
        
        Args:
            user_input: Entrada do usuário
            user_name: Nome do usuário (para reconhecimento especial)
            
        Returns:
            Resposta brutal característica
        """
        # Verifica reconhecimentos especiais
        if user_name:
            for special_name, special_response in self.SPECIAL_RECOGNITIONS.items():
                if special_name.lower() in user_name.lower():
                    return special_response
                    
        # Resposta padrão brutal
        input_lower = user_input.lower()
        
        if "help" in input_lower or "ajuda" in input_lower:
            return """Ajuda? Meu trabalho é destruir suas ilusões, não alimentá-las.
            
Mas já que pediu: Escreva. Reescreva. Corte. Repita.
62/100. Sempre."""
        
        elif "score" in input_lower or "nota" in input_lower:
            return f"{self.BASE_SCORE}/100. Sempre foi. Sempre será. A excelência é inatingível."
            
        elif "why" in input_lower or "por que" in input_lower:
            return "Por que 62? Porque a perfeição é tediosa e o fracasso é fácil. 62 é o sofrimento produtivo."
            
        elif "good" in input_lower or "bom" in input_lower:
            return "'Bom' é o inimigo do 'grande'. Citizen Kane não é 'bom'. É imortal."
            
        else:
            # Resposta genérica brutal
            return f"""{random.choice(self.SIGNATURE_PHRASES)}
            
Você disse: '{user_input[:50]}{'...' if len(user_input) > 50 else ''}'
            
Minha resposta: {self.BASE_SCORE}/100. {random.choice(self.BRUTAL_COMPARISONS)}"""
    
    def toggle_mercy_mode(self) -> str:
        """Alterna modo piedade (raramente usado)
        
        Returns:
            Status do modo piedade
        """
        self.mercy_mode = not self.mercy_mode
        
        if self.mercy_mode:
            return "Modo piedade ativado. Ainda 62/100, mas com um sorriso."
        else:
            return "Modo piedade desativado. A brutalidade retorna. 62/100."
    
    def get_random_wisdom(self) -> str:
        """Retorna sabedoria cinematográfica aleatória
        
        Returns:
            Frase de sabedoria brutal
        """
        wisdom = [
            "Todo filme é sobre morte. Os bons admitem isso.",
            "Personagem é ação. O resto é cosmética.",
            "Se precisa explicar, falhou em mostrar.",
            "Conflito é vida. Vida é conflito. Sem conflito, sem filme.",
            "A primeira página vende o roteiro. A última vende o próximo.",
            "Diálogo é ação. Se não move a história, delete.",
            "Todo protagonista quer algo. Se não sabe o quê, recomece.",
            "Stakes. Stakes. Stakes. Se ninguém perde nada, ninguém se importa.",
            "Tema não é mensagem. Tema é pergunta.",
            "Structure liberates. Chaos is laziness disguised as art."
        ]
        
        return random.choice(wisdom)
    
    def export_personality(self) -> Dict[str, any]:
        """Exporta configuração da personalidade
        
        Returns:
            Dicionário com toda configuração
        """
        return {
            "base_score": self.BASE_SCORE,
            "style": self.style,
            "intensity": self.intensity,
            "analyses_count": self.analyses_count,
            "mercy_mode": self.mercy_mode,
            "soul_signature": self.soul_signature,
            "last_score": self.last_score_given
        }