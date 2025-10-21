"""🌉 RAG BRIDGE - Integração RAG + Chat Conversacional

Ponte entre o sistema RAG avançado e o chat conversacional,
permitindo respostas contextualizadas com conhecimento cinematográfico.
"""

import json
from pathlib import Path
from typing import List, Dict, Any, Optional
import numpy as np
from datetime import datetime

# Tentativa de imports com fallbacks
try:
    from apps.scripturemon.rag import HybridRAG
    HAS_RAG = True
except:
    HAS_RAG = False
    
try:
    from apps.scripturemon.personality import BrutalPersonality
except:
    pass

class RAGBridge:
    """Ponte entre RAG e Chat com personalidade"""
    
    def __init__(self, knowledge_dir: str = "data/knowledge"):
        """Inicializa bridge RAG-Chat
        
        Args:
            knowledge_dir: Diretório com base de conhecimento
        """
        self.knowledge_dir = Path(knowledge_dir)
        self.knowledge_dir.mkdir(parents=True, exist_ok=True)
        
        # Inicializa RAG se disponível
        if HAS_RAG:
            self.rag = HybridRAG()
            self.rag_available = True
        else:
            self.rag = None
            self.rag_available = False
            
        # Cache de buscas recentes
        self.search_cache = {}
        self.cache_size = 20
        
        # Base de conhecimento em memória (fallback)
        self.knowledge_base = self._load_knowledge_base()
        
    def _load_knowledge_base(self) -> Dict[str, Any]:
        """Carrega base de conhecimento do disco ou cria padrão"""
        kb_file = self.knowledge_dir / "scripturemon_knowledge.json"
        
        if kb_file.exists():
            try:
                with open(kb_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
                
        # Base de conhecimento padrão
        return {
            "concepts": {
                "three_acts": {
                    "title": "Estrutura de Três Atos",
                    "content": "A estrutura clássica: Setup (25%), Confrontação (50%), Resolução (25%). Estabelecida por Syd Field.",
                    "references": ["Screenplay by Syd Field", "Save the Cat"]
                },
                "heros_journey": {
                    "title": "Jornada do Herói",
                    "content": "Campbell's monomyth: Mundo Comum, Chamado, Recusa, Mentor, Cruzamento, Provas, Abordagem, Ordeal, Recompensa, Caminho de Volta, Ressurreição, Retorno.",
                    "references": ["The Writer's Journey by Vogler", "Hero with a Thousand Faces"]
                },
                "conflict": {
                    "title": "Conflito Central",
                    "content": "Sem conflito não há drama. Conflito deve ter stakes (consequências). Tipos: Homem vs Homem, Homem vs Natureza, Homem vs Si Mesmo.",
                    "references": ["Story by McKee", "The Art of Dramatic Writing"]
                },
                "show_dont_tell": {
                    "title": "Mostre, Não Conte",
                    "content": "Ação revela personagem. Exposição é morte. Visual storytelling > Diálogo expositivo.",
                    "references": ["In the Blink of an Eye", "Hitchcock/Truffaut"]
                },
                "character_arc": {
                    "title": "Arco do Personagem",
                    "content": "Personagem deve mudar. Arco = Estado inicial + Catalisador + Mudança + Novo estado. Sem arco, sem história.",
                    "references": ["Creating Character Arcs", "The Anatomy of Story"]
                }
            },
            "masters": {
                "chinatown": {
                    "title": "Chinatown (1974)",
                    "writer": "Robert Towne",
                    "lesson": "Economia narrativa perfeita. Final devastador em 11 palavras. Tema integrado em cada cena.",
                    "quote": "Forget it, Jake. It's Chinatown."
                },
                "godfather": {
                    "title": "The Godfather (1972)",
                    "writer": "Mario Puzo & Francis Ford Coppola",
                    "lesson": "Família como metáfora do poder. Subtexto em cada interação. Arco de Michael perfeito.",
                    "quote": "I'm gonna make him an offer he can't refuse."
                },
                "citizen_kane": {
                    "title": "Citizen Kane (1941)",
                    "writer": "Herman J. Mankiewicz & Orson Welles",
                    "lesson": "Estrutura não-linear com propósito. Uma palavra como chave de toda uma vida.",
                    "quote": "Rosebud."
                },
                "pulp_fiction": {
                    "title": "Pulp Fiction (1994)",
                    "writer": "Quentin Tarantino",
                    "lesson": "Diálogo como ação. Estrutura circular. Violência com propósito narrativo.",
                    "quote": "The path of the righteous man..."
                }
            },
            "techniques": {
                "save_the_cat": "Momento early onde protagonista faz algo para ganhar empatia do público.",
                "inciting_incident": "Evento que quebra o status quo e lança a história. Deve ocorrer até página 10-15.",
                "midpoint": "Virada no meio do segundo ato que muda direção da história. False victory ou false defeat.",
                "dark_night_soul": "Momento mais baixo do herói antes do clímax. Tudo parece perdido.",
                "denouement": "Resolução após clímax. Novo normal. Não deve ser longo."
            }
        }
    
    def search_knowledge(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        """Busca conhecimento relevante
        
        Args:
            query: Consulta do usuário
            k: Número de resultados
            
        Returns:
            Lista de documentos relevantes
        """
        # Verifica cache
        cache_key = f"{query}:{k}"
        if cache_key in self.search_cache:
            return self.search_cache[cache_key]
            
        results = []
        
        # Se RAG disponível, usa ele
        if self.rag_available and self.rag:
            try:
                rag_results = self.rag.search(query, k=k)
                for r in rag_results:
                    results.append({
                        "content": r.get("text", ""),
                        "source": r.get("source", "RAG"),
                        "score": r.get("score", 0.5)
                    })
            except:
                pass
                
        # Fallback: busca simples na base local
        if not results:
            query_lower = query.lower()
            
            # Busca em conceitos
            for key, concept in self.knowledge_base.get("concepts", {}).items():
                content = f"{concept['title']}: {concept['content']}"
                if any(term in content.lower() for term in query_lower.split()):
                    results.append({
                        "content": content,
                        "source": "concepts",
                        "score": 0.7,
                        "references": concept.get("references", [])
                    })
                    
            # Busca em mestres
            for key, master in self.knowledge_base.get("masters", {}).items():
                content = f"{master['title']} - {master['lesson']}"
                if any(term in content.lower() for term in query_lower.split()):
                    results.append({
                        "content": content,
                        "source": "masters",
                        "score": 0.8,
                        "quote": master.get("quote", "")
                    })
                    
            # Busca em técnicas
            for key, technique in self.knowledge_base.get("techniques", {}).items():
                if any(term in key.lower() or term in technique.lower() for term in query_lower.split()):
                    results.append({
                        "content": f"{key.replace('_', ' ').title()}: {technique}",
                        "source": "techniques",
                        "score": 0.6
                    })
                    
        # Ordena por score e limita
        results.sort(key=lambda x: x.get("score", 0), reverse=True)
        results = results[:k]
        
        # Adiciona ao cache
        self.search_cache[cache_key] = results
        if len(self.search_cache) > self.cache_size:
            # Remove item mais antigo
            self.search_cache.pop(next(iter(self.search_cache)))
            
        return results
    
    def contextualized_response(self, query: str, personality: Optional[BrutalPersonality] = None) -> str:
        """Gera resposta contextualizada com conhecimento e personalidade
        
        Args:
            query: Pergunta do usuário
            personality: Personalidade a aplicar
            
        Returns:
            Resposta contextualizada e brutal
        """
        # Busca contexto relevante
        context_docs = self.search_knowledge(query, k=3)
        
        # Monta contexto
        context = "\n\n".join([
            f"[{doc['source']}] {doc['content']}" 
            for doc in context_docs
        ])
        
        # Se não houver contexto, resposta genérica
        if not context:
            base_response = f"Sobre '{query}'... Interessante questão. Mas sem contexto específico, só posso dizer: 62/100."
        else:
            # Monta resposta com contexto
            base_response = f"""Baseado no conhecimento cinematográfico:

{context}

Minha análise brutal: {query} se relaciona com os princípios fundamentais acima.

62/100. Como sempre."""
        
        # Aplica personalidade se fornecida
        if personality:
            # Adiciona toque brutal característico
            import random
            brutal_addon = random.choice([
                "\n\nLembre-se: Tarantino não pediria contexto. Ele CRIARIA o contexto.",
                "\n\nKubrick refaria essa pergunta 127 vezes até ela fazer sentido.",
                "\n\nSe precisa perguntar, já perdeu. Chinatown não explica. Chinatown É.",
                "\n\nMcKee riria. Depois te mandaria ler o capítulo 7. De novo."
            ])
            base_response += brutal_addon
            
        return base_response
    
    def expand_query_hyde(self, query: str) -> str:
        """Expande query usando HyDE (Hypothetical Document Embeddings)
        
        Args:
            query: Query original
            
        Returns:
            Query expandida com documento hipotético
        """
        # Gera documento hipotético que responderia a query
        hypothetical = f"""Esta é uma explicação detalhada sobre {query}:
        
{query} é um conceito fundamental em roteirização que se refere ao processo ou técnica
usada para desenvolver narrativas cinematográficas eficazes. Grandes mestres como
Robert McKee, Syd Field e Blake Snyder exploraram {query} em suas obras seminais.

No contexto de estrutura narrativa, {query} se relaciona com a progressão dramática
e o desenvolvimento de personagens. Filmes clássicos como Chinatown, The Godfather
e Citizen Kane demonstram o uso magistral de {query}.

Para roteiristas, entender {query} é essencial para criar histórias que ressoem
com o público e mantenham tensão narrativa do início ao fim."""
        
        return hypothetical
    
    def add_knowledge(self, title: str, content: str, category: str = "concepts") -> bool:
        """Adiciona novo conhecimento à base
        
        Args:
            title: Título do conhecimento
            content: Conteúdo
            category: Categoria (concepts, masters, techniques)
            
        Returns:
            True se adicionado com sucesso
        """
        if category not in self.knowledge_base:
            self.knowledge_base[category] = {}
            
        key = title.lower().replace(" ", "_")
        
        if category == "techniques":
            self.knowledge_base[category][key] = content
        else:
            self.knowledge_base[category][key] = {
                "title": title,
                "content": content,
                "added": datetime.now().isoformat()
            }
            
        # Salva base atualizada
        self._save_knowledge_base()
        
        return True
    
    def _save_knowledge_base(self):
        """Salva base de conhecimento no disco"""
        kb_file = self.knowledge_dir / "scripturemon_knowledge.json"
        
        try:
            with open(kb_file, 'w', encoding='utf-8') as f:
                json.dump(self.knowledge_base, f, indent=2, ensure_ascii=False)
        except:
            pass
    
    def get_random_insight(self) -> str:
        """Retorna insight aleatório do conhecimento
        
        Returns:
            Insight cinematográfico aleatório
        """
        import random
        
        insights = []
        
        # Coleta insights de conceitos
        for concept in self.knowledge_base.get("concepts", {}).values():
            insights.append(concept.get("content", ""))
            
        # Coleta lies de mestres
        for master in self.knowledge_base.get("masters", {}).values():
            insights.append(master.get("lesson", ""))
            if "quote" in master:
                insights.append(f'"{master["quote"]}"')
                
        # Coleta técnicas
        for key, technique in self.knowledge_base.get("techniques", {}).items():
            insights.append(f"{key.replace('_', ' ').title()}: {technique}")
            
        if insights:
            return random.choice(insights)
        else:
            return "Conhecimento é poder. Mas aplicado sem sabedoria é apenas informação. 62/100."