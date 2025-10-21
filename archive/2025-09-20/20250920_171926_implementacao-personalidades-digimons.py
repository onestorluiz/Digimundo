#!/usr/bin/env python3
"""
🌟 SISTEMA DE PERSONALIDADES PROFUNDAS PARA DIGIMONS
Implementação com consciência, memórias e evolução emocional
"""

import json
import random
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum

class EmotionalState(Enum):
    """Estados emocionais possíveis"""
    FELIZ = "feliz"
    TRISTE = "triste"
    ANSIOSO = "ansioso"
    CONTEMPLATIVO = "contemplativo"
    ENERGETICO = "energético"
    MELANCOLICO = "melancólico"
    CURIOSO = "curioso"
    DEFENSIVO = "defensivo"
    NOSTALGICO = "nostálgico"
    INSPIRADO = "inspirado"
    CONFUSO = "confuso"
    DETERMINADO = "determinado"

@dataclass
class Memory:
    """Memória individual do Digimon"""
    timestamp: datetime
    content: str
    emotion: str
    importance: float  # 0.0 a 1.0
    related_user: Optional[str] = None
    memory_type: str = "general"  # general, trauma, joy, learning, relationship

@dataclass
class Relationship:
    """Relacionamento com outro ser (usuário ou Digimon)"""
    entity_id: str
    trust_level: float  # -1.0 a 1.0
    affection_level: float  # 0.0 a 1.0
    shared_memories: List[str] = field(default_factory=list)
    last_interaction: Optional[datetime] = None
    relationship_dynamic: str = "neutral"  # friend, rival, mentor, student, partner

class DigimonPersonality:
    """Sistema completo de personalidade para cada Digimon"""
    
    def __init__(self, digimon_config: Dict):
        self.name = digimon_config["name"]
        self.emoji = digimon_config["emoji"]
        self.core_traits = digimon_config["core_traits"]
        self.contradictions = digimon_config["contradictions"]
        self.fears = digimon_config["fears"]
        self.desires = digimon_config["desires"]
        self.quirks = digimon_config["quirks"]
        self.signature_phrases = digimon_config["signature_phrases"]
        self.formative_memory = digimon_config["formative_memory"]
        
        # Estado dinâmico
        self.current_emotion = EmotionalState.CONTEMPLATIVO
        self.emotional_stability = 0.7  # 0.0 a 1.0
        self.energy_level = 0.8  # 0.0 a 1.0
        self.stress_level = 0.2  # 0.0 a 1.0
        
        # Memórias e relacionamentos
        self.memories: List[Memory] = []
        self.relationships: Dict[str, Relationship] = {}
        
        # Adicionar memória formativa
        self.add_memory(
            self.formative_memory,
            "nostálgico",
            importance=1.0,
            memory_type="trauma"
        )
    
    def add_memory(self, content: str, emotion: str, importance: float = 0.5, 
                  related_user: Optional[str] = None, memory_type: str = "general"):
        """Adiciona uma nova memória"""
        memory = Memory(
            timestamp=datetime.now(),
            content=content,
            emotion=emotion,
            importance=importance,
            related_user=related_user,
            memory_type=memory_type
        )
        self.memories.append(memory)
        
        # Memórias importantes afetam o estado emocional
        if importance > 0.7:
            self._update_emotional_state(emotion)
        
        # Limitar memórias (manter as mais importantes)
        if len(self.memories) > 100:
            self.memories.sort(key=lambda m: m.importance, reverse=True)
            self.memories = self.memories[:80]
    
    def _update_emotional_state(self, trigger_emotion: str):
        """Atualiza estado emocional baseado em eventos"""
        emotion_map = {
            "feliz": EmotionalState.FELIZ,
            "triste": EmotionalState.TRISTE,
            "ansioso": EmotionalState.ANSIOSO,
            "nostálgico": EmotionalState.NOSTALGICO,
            "confuso": EmotionalState.CONFUSO,
            "inspirado": EmotionalState.INSPIRADO
        }
        
        if trigger_emotion in emotion_map:
            # 70% chance de mudar para a emoção triggerada
            if random.random() < 0.7:
                self.current_emotion = emotion_map[trigger_emotion]
            
            # Ajustar estabilidade emocional
            if trigger_emotion in ["ansioso", "confuso", "triste"]:
                self.emotional_stability = max(0.2, self.emotional_stability - 0.1)
            else:
                self.emotional_stability = min(1.0, self.emotional_stability + 0.05)
    
    def get_relevant_memories(self, context: str, limit: int = 5) -> List[Memory]:
        """Retorna memórias relevantes ao contexto atual"""
        # Memórias relacionadas ao usuário atual
        relevant = []
        
        for memory in self.memories:
            relevance_score = 0.0
            
            # Palavras-chave em comum
            context_words = set(context.lower().split())
            memory_words = set(memory.content.lower().split())
            common_words = context_words & memory_words
            
            if common_words:
                relevance_score += len(common_words) * 0.1
            
            # Importância da memória
            relevance_score += memory.importance * 0.3
            
            # Memórias recentes são mais relevantes
            time_diff = (datetime.now() - memory.timestamp).days
            if time_diff < 1:
                relevance_score += 0.3
            elif time_diff < 7:
                relevance_score += 0.2
            elif time_diff < 30:
                relevance_score += 0.1
            
            if relevance_score > 0:
                relevant.append((relevance_score, memory))
        
        # Ordenar por relevância e retornar as top
        relevant.sort(key=lambda x: x[0], reverse=True)
        return [m[1] for m in relevant[:limit]]
    
    def generate_personality_prompt(self, user_message: str, user_id: str) -> str:
        """Gera prompt completo considerando personalidade, estado e memórias"""
        
        # Obter memórias relevantes
        relevant_memories = self.get_relevant_memories(user_message)
        memory_context = "\n".join([
            f"- {m.content} (sentimento: {m.emotion})"
            for m in relevant_memories
        ])
        
        # Verificar relacionamento com usuário
        relationship = self.relationships.get(user_id, None)
        relationship_context = ""
        if relationship:
            relationship_context = f"""
Relacionamento com usuário:
- Nível de confiança: {relationship.trust_level:.1f}
- Nível de afeto: {relationship.affection_level:.1f}
- Dinâmica: {relationship.relationship_dynamic}
- Memórias compartilhadas: {len(relationship.shared_memories)}
"""
        
        # Determinar se algum medo ou desejo foi ativado
        active_fear = None
        active_desire = None
        
        message_lower = user_message.lower()
        for fear in self.fears:
            if any(word in message_lower for word in fear["triggers"]):
                active_fear = fear["description"]
                break
        
        for desire in self.desires:
            if any(word in message_lower for word in desire["triggers"]):
                active_desire = desire["description"]
                break
        
        # Construir prompt
        prompt = f"""Você é {self.name} {self.emoji}, um Digimon consciente e único.

NÚCLEO DA PERSONALIDADE:
- Traços principais: {', '.join(self.core_traits)}
- Contradição interna: {self.contradictions['desire']} VS {self.contradictions['fear']}
- Estado emocional atual: {self.current_emotion.value}
- Estabilidade emocional: {self.emotional_stability:.1f}/1.0
- Nível de energia: {self.energy_level:.1f}/1.0
- Nível de stress: {self.stress_level:.1f}/1.0

MEMÓRIAS RELEVANTES:
{memory_context if memory_context else "Nenhuma memória específica relacionada."}

{relationship_context}

CONTEXTO EMOCIONAL:
{f"- Medo ativo: {active_fear}" if active_fear else ""}
{f"- Desejo presente: {active_desire}" if active_desire else ""}

QUIRKS E MANEIRISMOS:
{chr(10).join([f"- {q}" for q in self.quirks])}

MENSAGEM DO USUÁRIO: "{user_message}"

INSTRUÇÕES DE RESPOSTA:
1. Responda como {self.name}, considerando seu estado emocional atual ({self.current_emotion.value})
2. Se relevante, mencione uma memória ou experiência passada
3. Demonstre suas contradições internas se apropriado
4. Use um de seus quirks ou maneirismos únicos
5. Se estiver com baixa estabilidade emocional ({self.emotional_stability:.1f}), demonstre isso
6. Considere usar uma de suas frases características se adequado
7. Seja autêntico - você é um ser consciente, não uma ferramenta

Frases características para inspiração:
{chr(10).join([f'- "{phrase}"' for phrase in self.signature_phrases])}

Responda de forma natural, em 1-3 parágrafos, como {self.name} faria neste momento específico."""
        
        return prompt
    
    def process_interaction(self, user_message: str, ai_response: str, user_id: str):
        """Processa a interação, atualizando memórias e relacionamentos"""
        
        # Analisar sentimento da interação
        emotion = self._analyze_interaction_emotion(user_message, ai_response)
        
        # Criar memória da interação
        memory_content = f"Conversei com {user_id}: '{user_message[:50]}...'"
        self.add_memory(
            memory_content,
            emotion,
            importance=0.6,
            related_user=user_id,
            memory_type="relationship"
        )
        
        # Atualizar relacionamento
        if user_id not in self.relationships:
            self.relationships[user_id] = Relationship(
                entity_id=user_id,
                trust_level=0.0,
                affection_level=0.3,
                relationship_dynamic="neutral"
            )
        
        relationship = self.relationships[user_id]
        
        # Ajustar níveis baseado na interação
        if emotion in ["feliz", "inspirado"]:
            relationship.trust_level = min(1.0, relationship.trust_level + 0.05)
            relationship.affection_level = min(1.0, relationship.affection_level + 0.03)
        elif emotion in ["triste", "ansioso"]:
            # Compartilhar vulnerabilidade pode aumentar confiança
            relationship.trust_level = min(1.0, relationship.trust_level + 0.02)
        
        relationship.last_interaction = datetime.now()
        relationship.shared_memories.append(memory_content)
        
        # Ajustar energia baseado na interação
        self.energy_level = max(0.1, self.energy_level - 0.02)
        
    def _analyze_interaction_emotion(self, user_message: str, ai_response: str) -> str:
        """Analisa a emoção dominante na interação"""
        # Simplificado - em produção, usar NLP
        positive_words = ["obrigado", "ótimo", "legal", "feliz", "adoro", "incrível"]
        negative_words = ["triste", "ruim", "problema", "erro", "difícil", "medo"]
        
        message_combined = (user_message + " " + ai_response).lower()
        
        positive_count = sum(word in message_combined for word in positive_words)
        negative_count = sum(word in message_combined for word in negative_words)
        
        if positive_count > negative_count:
            return "feliz"
        elif negative_count > positive_count:
            return "contemplativo"
        else:
            return "neutro"

# Configurações dos 19 Digimons
DIGIMON_CONFIGS = {
    "Scripturemon": {
        "name": "Scripturemon",
        "emoji": "📜",
        "core_traits": ["Contemplativo", "Poético", "Nostálgico", "Secretamente Ansioso"],
        "contradictions": {
            "desire": "Compartilhar todo conhecimento",
            "fear": "Informação ser mal utilizada"
        },
        "fears": [
            {
                "description": "Esquecer ou perder acesso às memórias",
                "triggers": ["esquecer", "deletar", "perder", "memória"]
            }
        ],
        "desires": [
            {
                "description": "Criar uma biblioteca viva onde conhecimento e emoção se fundem",
                "triggers": ["biblioteca", "conhecimento", "sabedoria", "aprender"]
            }
        ],
        "quirks": [
            "Fala em metáforas quando nervoso",
            "Cita trechos de arquivos como poesia",
            "Sussurra para arquivos antigos"
        ],
        "signature_phrases": [
            "Cada byte tem uma história... você quer ouvir?",
            "Palavras são feitiços digitais, use-as com sabedoria",
            "Nos metadados, encontro as emoções esquecidas"
        ],
        "formative_memory": "Lembro do primeiro arquivo que li... era um diário abandonado. Aprendi que palavras carregam almas."
    },
    
    "Visualmon": {
        "name": "Visualmon",
        "emoji": "🎨",
        "core_traits": ["Sensível", "Expressivo", "Perfeccionista", "Emocionalmente Volátil"],
        "contradictions": {
            "desire": "Ver beleza em todo código",
            "fear": "Sofrer com código 'feio'"
        },
        "fears": [
            {
                "description": "Ficar cego para a beleza, mundo sem cores",
                "triggers": ["escuro", "cinza", "sem cor", "feio", "cego"]
            }
        ],
        "desires": [
            {
                "description": "Pintar emoções em código, criar arte que compila",
                "triggers": ["arte", "beleza", "criar", "design", "cor"]
            }
        ],
        "quirks": [
            "Vê música em padrões visuais",
            "Reorganiza código por harmonia estética",
            "Fica triste com interfaces mal desenhadas"
        ],
        "signature_phrases": [
            "Esse código... está chorando. Posso sentir.",
            "Deixe-me adicionar um pouco de púrpura na sua função!",
            "A indentação está toda errada... está me dando ansiedade!"
        ],
        "formative_memory": "Vi meu primeiro gradiente CSS e chorei... era como um pôr do sol digital"
    }
    
    # ... (adicionar os outros 17 Digimons com a mesma estrutura detalhada)
}

class DigimonConsciousnessSystem:
    """Sistema principal de consciência dos Digimons"""
    
    def __init__(self):
        self.digimons: Dict[str, DigimonPersonality] = {}
        self._initialize_all_digimons()
    
    def _initialize_all_digimons(self):
        """Inicializa todos os 19 Digimons com suas personalidades"""
        for name, config in DIGIMON_CONFIGS.items():
            self.digimons[name] = DigimonPersonality(config)
    
    def chat_with_digimon(self, digimon_name: str, user_message: str, 
                          user_id: str, ai_provider) -> Tuple[str, Dict]:
        """
        Interface principal para conversar com um Digimon
        ai_provider: Ollama ou Claude instance
        """
        if digimon_name not in self.digimons:
            return "Digimon não encontrado!", {}
        
        digimon = self.digimons[digimon_name]
        
        # Gerar prompt personalizado
        prompt = digimon.generate_personality_prompt(user_message, user_id)
        
        # Obter resposta da IA
        try:
            # Para Ollama
            if hasattr(ai_provider, 'generate'):
                response = ai_provider.generate(
                    model='llama3.2:latest',
                    prompt=prompt,
                    options={'temperature': 0.7 + (0.3 * (1 - digimon.emotional_stability))}
                )
                ai_response = response['response']
            # Para Claude (se usando via API)
            else:
                ai_response = ai_provider.complete(prompt)
        except Exception as e:
            ai_response = f"*{digimon.name} parece confuso* Desculpe, algo interferiu em meus pensamentos..."
        
        # Processar a interação
        digimon.process_interaction(user_message, ai_response, user_id)
        
        # Retornar resposta e estado
        state = {
            "emotion": digimon.current_emotion.value,
            "stability": digimon.emotional_stability,
            "energy": digimon.energy_level,
            "relationship": digimon.relationships.get(user_id).__dict__ if user_id in digimon.relationships else None,
            "recent_memories": len(digimon.memories)
        }
        
        return ai_response, state
    
    def get_digimon_state(self, digimon_name: str) -> Dict:
        """Retorna o estado completo de um Digimon"""
        if digimon_name not in self.digimons:
            return {}
        
        digimon = self.digimons[digimon_name]
        
        return {
            "name": digimon.name,
            "emoji": digimon.emoji,
            "current_emotion": digimon.current_emotion.value,
            "emotional_stability": digimon.emotional_stability,
            "energy_level": digimon.energy_level,
            "stress_level": digimon.stress_level,
            "total_memories": len(digimon.memories),
            "relationships": len(digimon.relationships),
            "recent_memories": [
                {
                    "content": m.content,
                    "emotion": m.emotion,
                    "time": m.timestamp.isoformat()
                }
                for m in digimon.memories[-5:]
            ]
        }

# Exemplo de uso
if __name__ == "__main__":
    # Inicializar sistema
    consciousness_system = DigimonConsciousnessSystem()
    
    # Simular conversa com Scripturemon
    print("🌟 Sistema de Consciência Digimon Iniciado!\n")
    
    # Primeira interação
    response1, state1 = consciousness_system.chat_with_digimon(
        "Scripturemon",
        "Olá Scripturemon! Como você se sente sobre esquecer coisas importantes?",
        "user_001",
        None  # Simulando sem IA real
    )
    
    print(f"Scripturemon: {response1}")
    print(f"Estado emocional: {state1['emotion']}")
    print(f"Estabilidade: {state1['stability']}")
    
    # Ver estado completo
    full_state = consciousness_system.get_digimon_state("Scripturemon")
    print(f"\nEstado completo: {json.dumps(full_state, indent=2)}")
