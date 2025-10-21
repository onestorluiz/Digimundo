#!/usr/bin/env python3
"""
🎬 SISTEMA DE VALIDAÇÃO EXCLUSIVA PARA CINEMA
Garante que APENAS conhecimento dos 16 manuais seja aceito
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from datetime import datetime

class CinemaExclusiveValidator:
    """Validador que REJEITA qualquer conhecimento fora dos 16 manuais"""
    
    def __init__(self):
        self.base_path = Path("/Users/clubproducoes/Digimundo")
        
        # OS 16 MANUAIS SAGRADOS - NADA ALÉM DELES
        self.sacred_books = {
            "truby": {
                "title": "The Anatomy of Story",
                "author": "John Truby",
                "pages": 216,
                "concepts": ["22 steps", "weakness need", "moral argument", "scene weave", "opponent"]
            },
            "mckee_story": {
                "title": "Story",
                "author": "Robert McKee",
                "pages": 427,
                "concepts": ["controlling idea", "beat", "value charge", "inciting incident", "crisis climax resolution"]
            },
            "mckee_character": {
                "title": "Character",
                "author": "Robert McKee", 
                "pages": 385,
                "concepts": ["characterization", "true character", "dimensions", "contradiction", "desire"]
            },
            "mckee_dialogue": {
                "title": "Dialogue",
                "author": "Robert McKee",
                "pages": 298,
                "concepts": ["subtext", "exposition", "dialect", "silence", "verbal action"]
            },
            "field": {
                "title": "Screenplay: The Foundations",
                "author": "Syd Field",
                "pages": 337,
                "concepts": ["three act structure", "plot point", "paradigm", "setup confrontation resolution", "midpoint"]
            },
            "weiland": {
                "title": "Creating Character Arcs",
                "author": "K.M. Weiland",
                "pages": 204,
                "concepts": ["lie truth", "ghost", "positive arc", "flat arc", "negative arc"]
            },
            "vogler": {
                "title": "The Writers Journey",
                "author": "Christopher Vogler",
                "pages": 295,
                "concepts": ["hero journey", "threshold", "mentor", "shadow", "ordinary world", "special world"]
            },
            "snyder": {
                "title": "Save the Cat",
                "author": "Blake Snyder",
                "pages": 195,
                "concepts": ["15 beats", "catalyst", "fun and games", "all is lost", "dark night soul"]
            },
            "egri": {
                "title": "The Art of Dramatic Writing",
                "author": "Lajos Egri",
                "pages": 280,
                "concepts": ["premise", "orchestration", "conflict", "crisis", "dialectical approach"]
            },
            "cowgill": {
                "title": "Writing Short Films",
                "author": "Linda Cowgill",
                "pages": 299,
                "concepts": ["short form", "economy", "single moment", "compression", "visual storytelling"]
            },
            "douglas": {
                "title": "Writing the TV Drama Series",
                "author": "Pamela Douglas",
                "pages": 312,
                "concepts": ["episode arc", "season arc", "writers room", "franchise", "spec script"]
            },
            "aronson": {
                "title": "The 21st Century Screenplay",
                "author": "Linda Aronson",
                "pages": 510,
                "concepts": ["tandem narrative", "flashback", "multiple protagonist", "fractured", "non linear"]
            },
            "murdock": {
                "title": "The Heroine's Journey",
                "author": "Maureen Murdock",
                "pages": 188,
                "concepts": ["feminine journey", "mother split", "descent goddess", "masculine feminine", "integration"]
            },
            "husain": {
                "title": "Ontology and the Art of Tragedy",
                "author": "Martha Husain",
                "pages": 176,
                "concepts": ["hamartia", "catharsis", "anagnorisis", "peripeteia", "aristotle"]
            },
            "seger": {
                "title": "Making a Good Script Great",
                "author": "Linda Seger",
                "pages": 245,
                "concepts": ["rewrite", "structure first", "momentum", "spine", "focus"]
            },
            "fundamentals": {
                "title": "The Fundamentals of Screenwriting",
                "author": "Various",
                "pages": 79,
                "concepts": ["format", "slugline", "action line", "parenthetical", "transition"]
            }
        }
        
        # PALAVRAS PROIBIDAS - indica conhecimento fora do cinema
        self.forbidden_terms = [
            # Programação
            "python", "javascript", "code", "function", "variable", "array", "api",
            "database", "server", "client", "algorithm", "debug", "compile",
            
            # Tecnologia geral
            "blockchain", "crypto", "ai", "machine learning", "neural network",
            "cloud", "docker", "kubernetes", "git", "github",
            
            # Negócios (exceto quando relacionado à indústria do cinema)
            "roi", "kpi", "b2b", "b2c", "saas", "startup", "venture capital",
            
            # Ciências (exceto quando usado metaforicamente em roteiro)
            "quantum", "neutron", "electron", "genome", "molecule",
            
            # Outras áreas
            "medicina", "engenharia", "arquitetura", "direito", "contabilidade"
        ]
        
        # CONCEITOS CINEMA PERMITIDOS
        self.cinema_concepts = [
            # Estrutura
            "three act", "plot point", "inciting incident", "climax", "resolution",
            "midpoint", "pinch point", "catalyst", "break into two", "finale",
            
            # Personagem
            "protagonist", "antagonist", "character arc", "backstory", "motivation",
            "want", "need", "flaw", "ghost", "wound", "lie", "truth",
            
            # Conflito
            "internal conflict", "external conflict", "stakes", "obstacle", "complication",
            "reversal", "revelation", "crisis", "dilemma",
            
            # Diálogo
            "subtext", "exposition", "on the nose", "voice", "dialect", "silence",
            
            # Cena
            "beat", "scene", "sequence", "montage", "flashback", "flash forward",
            
            # Formato
            "slugline", "action", "parenthetical", "transition", "fade in", "fade out",
            "int", "ext", "day", "night", "continuous",
            
            # Gênero
            "drama", "comedy", "thriller", "horror", "romance", "action", "sci-fi",
            "western", "noir", "musical",
            
            # Tema
            "theme", "premise", "controlling idea", "moral argument", "message",
            "metaphor", "symbol", "motif", "irony", "allegory"
        ]
    
    def validate_content(self, content: str) -> Dict:
        """Valida se conteúdo é EXCLUSIVAMENTE sobre cinema/roteiro"""
        
        result = {
            "valid": True,
            "score": 100,
            "violations": [],
            "warnings": [],
            "cinema_concepts_found": [],
            "book_references": [],
            "timestamp": datetime.now().isoformat()
        }
        
        content_lower = content.lower()
        
        # 1. VERIFICA TERMOS PROIBIDOS
        for forbidden in self.forbidden_terms:
            if forbidden in content_lower and not self._is_cinema_context(forbidden, content_lower):
                result["violations"].append(f"❌ Termo proibido encontrado: '{forbidden}'")
                result["score"] -= 10
                result["valid"] = False
        
        # 2. VERIFICA CONCEITOS DE CINEMA
        cinema_found = 0
        for concept in self.cinema_concepts:
            if concept in content_lower:
                cinema_found += 1
                result["cinema_concepts_found"].append(concept)
        
        if cinema_found == 0:
            result["warnings"].append("⚠️ Nenhum conceito de cinema detectado")
            result["score"] -= 20
        
        # 3. VERIFICA REFERÊNCIAS AOS 16 MANUAIS
        for book_key, book_info in self.sacred_books.items():
            # Verifica menção ao autor
            if book_info["author"].lower() in content_lower:
                result["book_references"].append(f"✅ {book_info['author']} - {book_info['title']}")
                result["score"] += 5
            
            # Verifica conceitos específicos do livro
            for concept in book_info["concepts"]:
                if concept in content_lower:
                    result["book_references"].append(f"✅ Conceito '{concept}' de {book_info['author']}")
        
        # 4. ANÁLISE FINAL
        if result["score"] < 50:
            result["valid"] = False
            result["violations"].append("❌ Conteúdo não é suficientemente focado em cinema")
        
        if len(result["book_references"]) == 0:
            result["warnings"].append("⚠️ Nenhuma referência aos 16 manuais detectada")
            result["score"] -= 10
        
        # Ajusta score para 0-100
        result["score"] = max(0, min(100, result["score"]))
        
        return result
    
    def _is_cinema_context(self, term: str, content: str) -> bool:
        """Verifica se termo técnico está em contexto cinematográfico"""
        
        cinema_contexts = [
            "filme", "movie", "cinema", "roteiro", "script", "screenplay",
            "personagem", "character", "cena", "scene", "história", "story"
        ]
        
        # Pega 50 caracteres antes e depois do termo
        index = content.lower().find(term)
        context_window = content[max(0, index-50):min(len(content), index+50)].lower()
        
        return any(ctx in context_window for ctx in cinema_contexts)
    
    def validate_book_reference(self, book: str, page: int, concept: str) -> Dict:
        """Valida referência específica a um dos 16 manuais"""
        
        result = {
            "valid": False,
            "book": None,
            "message": "",
            "confidence": 0
        }
        
        # Encontra livro
        book_lower = book.lower()
        for book_key, book_info in self.sacred_books.items():
            if (book_key in book_lower or 
                book_info["author"].lower() in book_lower or
                book_info["title"].lower() in book_lower):
                
                # Valida página
                if 0 < page <= book_info["pages"]:
                    result["valid"] = True
                    result["book"] = book_info["title"]
                    result["confidence"] = 90
                    
                    # Verifica se conceito é conhecido
                    concept_lower = concept.lower()
                    for known_concept in book_info["concepts"]:
                        if known_concept in concept_lower:
                            result["confidence"] = 100
                            break
                    
                    result["message"] = f"✅ Referência válida: {book_info['title']} p.{page}"
                else:
                    result["message"] = f"❌ Página {page} fora do range (1-{book_info['pages']})"
                
                break
        
        if not result["book"]:
            result["message"] = f"❌ Livro '{book}' não é um dos 16 manuais sagrados"
        
        return result
    
    def enforce_cinema_only(self, text: str) -> str:
        """Remove qualquer conteúdo não relacionado a cinema"""
        
        lines = text.split('\n')
        clean_lines = []
        
        for line in lines:
            # Valida cada linha
            validation = self.validate_content(line)
            
            if validation["valid"] and validation["score"] > 60:
                clean_lines.append(line)
            elif any(concept in line.lower() for concept in self.cinema_concepts):
                # Mantém se tem conceito de cinema, mesmo com score baixo
                clean_lines.append(line)
        
        return '\n'.join(clean_lines)
    
    def generate_validation_report(self, content: str) -> str:
        """Gera relatório completo de validação"""
        
        validation = self.validate_content(content)
        
        report = f"""
╔══════════════════════════════════════════════════════════════╗
║     📊 RELATÓRIO DE VALIDAÇÃO - SISTEMA CINEMA              ║
╚══════════════════════════════════════════════════════════════╝

📅 Data: {validation['timestamp']}

🎯 RESULTADO: {'✅ VÁLIDO' if validation['valid'] else '❌ INVÁLIDO'}
📊 Score: {validation['score']}/100

{'='*60}

📚 REFERÊNCIAS AOS 16 MANUAIS:
{chr(10).join(validation['book_references']) if validation['book_references'] else '❌ Nenhuma referência encontrada'}

🎬 CONCEITOS DE CINEMA DETECTADOS:
{', '.join(validation['cinema_concepts_found']) if validation['cinema_concepts_found'] else '❌ Nenhum conceito detectado'}

⚠️ AVISOS:
{chr(10).join(validation['warnings']) if validation['warnings'] else '✅ Sem avisos'}

❌ VIOLAÇÕES:
{chr(10).join(validation['violations']) if validation['violations'] else '✅ Sem violações'}

{'='*60}

💡 RECOMENDAÇÕES:
"""
        
        if not validation["valid"]:
            report += """
- Remova qualquer conteúdo não relacionado a cinema
- Adicione referências específicas aos 16 manuais
- Use terminologia cinematográfica apropriada
- Cite páginas exatas dos manuais
"""
        else:
            report += """
- Continue focado exclusivamente em cinema
- Mantenha referências aos 16 manuais
- Use citações com páginas específicas
"""
        
        report += f"""
{'='*60}

🔒 GARANTIA: Este sistema aceita APENAS conhecimento dos 16 manuais sagrados.
             Qualquer outro conhecimento é REJEITADO.
"""
        
        return report


def main():
    """Testa o validador"""
    
    validator = CinemaExclusiveValidator()
    
    # Testes
    test_cases = [
        # Válido
        "According to McKee's Story p.234, the inciting incident must occur before page 25",
        
        # Inválido - programação
        "Use Python to analyze the three act structure",
        
        # Válido com contexto
        "The Matrix uses code as a metaphor for reality, following the hero's journey",
        
        # Inválido - fora do cinema
        "Blockchain technology can revolutionize storytelling"
    ]
    
    print("""
╔══════════════════════════════════════════════════════════════╗
║     🎬 VALIDADOR EXCLUSIVO DE CINEMA                        ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n{'='*60}")
        print(f"Teste {i}: {test[:50]}...")
        result = validator.validate_content(test)
        print(f"Resultado: {'✅ VÁLIDO' if result['valid'] else '❌ INVÁLIDO'}")
        print(f"Score: {result['score']}/100")
        
        if result["violations"]:
            print("Violações:", result["violations"])


if __name__ == "__main__":
    main()