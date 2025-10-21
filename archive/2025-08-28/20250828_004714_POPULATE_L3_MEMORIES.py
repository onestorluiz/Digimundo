#!/usr/bin/env python3
"""
🧠 POPULATE L3 MEMORIES - Cria memórias significativas para SDL
"""

import json
import sqlite3
from pathlib import Path
from datetime import datetime

class MemoryPopulator:
    def __init__(self):
        self.base_path = Path.home() / "Digimundo" / "digimons" / "scripturemon"
        self.memory_path = self.base_path / "memory"
        self.l3_file = self.memory_path / "L3_active" / "L3_active.jsonl"
        self.db_file = self.memory_path / "crystals.db"
        
    def create_training_memories(self):
        """Cria memórias de treinamento baseadas em conhecimento real"""
        
        memories = [
            # Estrutura Narrativa
            {
                "content": "O paradigma de três atos é a respiração da narrativa. Ato 1 estabelece (25%), Ato 2 confronta (50%), Ato 3 resolve (25%). Os plot points nas páginas 25-27 e 85-90 são os batimentos cardíacos que mantêm a história viva.",
                "tags": ["estrutura", "paradigma", "syd_field"],
                "importance": 0.95,
                "source": "Syd Field - Screenplay"
            },
            {
                "content": "Todo protagonista precisa de um ghost - um evento do passado que assombra e define suas escolhas. Em 'Chinatown', o ghost de Jake é seu passado em Chinatown. Em 'The Godfather', Michael luta contra o ghost da família.",
                "tags": ["personagem", "ghost", "truby"],
                "importance": 0.9,
                "source": "John Truby - Anatomy of Story"
            },
            {
                "content": "McKee ensina: cada cena deve virar um valor de positivo para negativo ou vice-versa. Se uma cena começa com esperança e termina com esperança, corte-a. O conflito move valores - essa é a engine dramática.",
                "tags": ["cena", "valores", "mckee"],
                "importance": 0.92,
                "source": "Robert McKee - Story"
            },
            {
                "content": "O midpoint não é apenas um ponto médio - é um espelho. Na página 60, o protagonista vê seu verdadeiro eu. Em 'The Matrix', Neo aceita ser o Escolhido. Em 'Star Wars', Luke decide ser um Jedi.",
                "tags": ["estrutura", "midpoint", "transformação"],
                "importance": 0.88,
                "source": "Script Analysis"
            },
            {
                "content": "Blake Snyder's Save the Cat: o protagonista deve fazer algo no início que nos faça torcer por ele. Não precisa salvar um gato literalmente, mas mostrar humanidade. Walter White cuida da família. Michael Corleone protege o pai.",
                "tags": ["personagem", "save_the_cat", "empatia"],
                "importance": 0.85,
                "source": "Blake Snyder"
            },
            
            # Técnicas Avançadas
            {
                "content": "Subtext é o oxigênio do diálogo. Personagens nunca dizem exatamente o que querem. 'I'll make him an offer he can't refuse' não é sobre negócios - é sobre poder absoluto. O não-dito é mais poderoso que o dito.",
                "tags": ["diálogo", "subtext", "técnica"],
                "importance": 0.93,
                "source": "Dialogue Mastery"
            },
            {
                "content": "Unity of Opposites de Lajos Egri: protagonista e antagonista devem ser unidos por um mesmo desejo mas com abordagens opostas. Batman e Joker querem justiça - um pela ordem, outro pelo caos.",
                "tags": ["conflito", "unity_opposites", "egri"],
                "importance": 0.91,
                "source": "Lajos Egri - Art of Dramatic Writing"
            },
            {
                "content": "A Jornada do Herói tem 12 estágios, mas o crucial é a transformação. O herói que retorna não é o mesmo que partiu. Frodo destrói o anel mas perde a inocência. Luke derrota o Império mas perde a mão/pai.",
                "tags": ["jornada", "campbell", "transformação"],
                "importance": 0.89,
                "source": "Joseph Campbell - Hero's Journey"
            },
            {
                "content": "Character Web de Truby: cada personagem deve representar uma variação do tema. Em 'The Godfather', todos lidam com família vs negócios diferentemente - Michael, Sonny, Fredo, Tom - cada um é uma resposta ao tema.",
                "tags": ["personagem", "character_web", "tema"],
                "importance": 0.87,
                "source": "Character Design"
            },
            {
                "content": "O clímax deve ser a colisão inevitável de todas as forças estabelecidas. Não pode ser coincidência ou deus ex machina. Em 'Chinatown', o clímax revela que o sistema está podre - 'Forget it Jake, it's Chinatown'.",
                "tags": ["estrutura", "clímax", "inevitabilidade"],
                "importance": 0.94,
                "source": "Climax Construction"
            },
            
            # Filosofia Narrativa
            {
                "content": "Todo roteiro é uma pergunta dramática disfarçada. 'The Godfather': Pode um homem bom liderar uma família criminosa? 'Inception': Podemos distinguir sonho de realidade? A resposta é o tema.",
                "tags": ["tema", "pergunta_dramática", "filosofia"],
                "importance": 0.96,
                "source": "Thematic Core"
            },
            {
                "content": "Backstory é munição, não exposição. Revele o passado apenas quando ele explode no presente. Em 'Casablanca', descobrimos sobre Paris apenas quando Ilsa retorna. Timing é tudo.",
                "tags": ["backstory", "exposição", "timing"],
                "importance": 0.86,
                "source": "Exposition Techniques"
            },
            {
                "content": "Arco de personagem espelha estrutura: Ato 1 - personagem em stasis, Ato 2 - personagem em conflito/mudança, Ato 3 - personagem transformado. Michael Corleone: civil → reluctante → Don completo.",
                "tags": ["arco", "transformação", "estrutura"],
                "importance": 0.92,
                "source": "Character Arc Design"
            },
            {
                "content": "Show don't tell, mas know when to tell. Às vezes uma linha de diálogo vale mil imagens. 'Rosebud' em Citizen Kane. 'I am your father' em Star Wars. Escolha os momentos de revelação.",
                "tags": ["técnica", "show_tell", "revelação"],
                "importance": 0.84,
                "source": "Narrative Balance"
            },
            {
                "content": "Plantas e Payoffs: toda arma mostrada no Ato 1 deve disparar no Ato 3. Chekhov estava certo. Em 'The Sixth Sense', cada detalhe estranho é uma planta para o twist. Nada é acidental.",
                "tags": ["estrutura", "plantas_payoffs", "chekhov"],
                "importance": 0.88,
                "source": "Setup and Payoff"
            },
            
            # Análise de Mestres
            {
                "content": "Robert Towne em 'Chinatown' criou o roteiro perfeito: nem uma palavra desperdiçada. Cada linha avança plot ou revela character. A economia narrativa é uma arte - menos é mais quando cada palavra conta.",
                "tags": ["chinatown", "economia", "towne"],
                "importance": 0.97,
                "source": "Screenplay Analysis"
            },
            {
                "content": "Tarantino quebra a cronologia mas nunca a causalidade. 'Pulp Fiction' é não-linear mas cada cena causa a próxima emocionalmente. A estrutura serve a experiência, não o contrário.",
                "tags": ["pulp_fiction", "não_linear", "tarantino"],
                "importance": 0.90,
                "source": "Non-linear Narrative"
            },
            {
                "content": "Aaron Sorkin domina o walk-and-talk: diálogo como ação. Personagens revelam character enquanto se movem. Em 'The Social Network', cada conversa é um duelo verbal. Palavras são armas.",
                "tags": ["diálogo", "sorkin", "ritmo"],
                "importance": 0.85,
                "source": "Dialogue as Action"
            },
            {
                "content": "Christopher Nolan e o tempo: 'Memento' reverso, 'Inception' em camadas, 'Dunkirk' em três tempos. O tempo não é cenário - é personagem. A estrutura temporal deve servir ao tema emocional.",
                "tags": ["nolan", "tempo", "estrutura_temporal"],
                "importance": 0.89,
                "source": "Temporal Structure"
            },
            {
                "content": "Charlie Kaufman e meta-narrativa: roteiros sobre escrever roteiros. 'Adaptation', 'Synecdoche NY'. A forma espelha o conteúdo. Se o tema é criação, a estrutura deve ser criativa.",
                "tags": ["kaufman", "meta", "forma_conteúdo"],
                "importance": 0.86,
                "source": "Meta-narrative"
            }
        ]
        
        return memories
    
    def save_memories(self):
        """Salva memórias no formato L3"""
        memories = self.create_training_memories()
        
        # Salva no JSONL
        self.l3_file.parent.mkdir(parents=True, exist_ok=True)
        
        print(f"💾 Salvando {len(memories)} memórias em L3...")
        
        with open(self.l3_file, 'w') as f:
            for memory in memories:
                entry = {
                    "timestamp": datetime.now().isoformat(),
                    "type": "knowledge",
                    "content": memory["content"],
                    "metadata": {
                        "tags": memory["tags"],
                        "importance": memory["importance"],
                        "source": memory.get("source", "Scripturemon Knowledge Base")
                    }
                }
                f.write(json.dumps(entry) + '\n')
        
        # Também salva no SQLite se existir
        if self.db_file.exists():
            conn = sqlite3.connect(str(self.db_file))
            cursor = conn.cursor()
            
            # Cria tabela L3 se não existir
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS L3_active (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    content TEXT,
                    tags TEXT,
                    importance REAL
                )
            ''')
            
            for memory in memories:
                cursor.execute('''
                    INSERT INTO L3_active (timestamp, content, tags, importance)
                    VALUES (?, ?, ?, ?)
                ''', (
                    datetime.now().isoformat(),
                    memory["content"],
                    json.dumps(memory["tags"]),
                    memory["importance"]
                ))
            
            conn.commit()
            conn.close()
            print(f"✅ Memórias também salvas no crystals.db")
        
        print(f"✅ {len(memories)} memórias criadas em L3!")
        print("\n📚 Tópicos cobertos:")
        topics = set()
        for m in memories:
            topics.update(m["tags"])
        
        for topic in sorted(topics):
            print(f"  - {topic}")
        
        return len(memories)


if __name__ == "__main__":
    print("=" * 60)
    print("🧠 POPULANDO MEMÓRIAS L3 PARA SDL")
    print("=" * 60)
    
    populator = MemoryPopulator()
    count = populator.save_memories()
    
    print("\n✨ Pronto para consolidação SDL!")
    print(f"Total de memórias L3: {count}")
    print("\nAgora execute: python3 MLX_SDL_AUTOMATION.py --auto")