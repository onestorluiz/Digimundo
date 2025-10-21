#!/usr/bin/env python3
"""
🎭 CHARACTER ANALYTICS SYSTEM - FASE 25
Análise profunda de personagens, tracking por atos e cenas,
relações e arcos narrativos
"""

import re
from typing import Dict, List, Tuple, Optional, Set, Any
from collections import defaultdict, Counter
from dataclasses import dataclass, field
from pathlib import Path
import json
import sqlite3
from datetime import datetime
from enum import Enum

class CharacterRole(Enum):
    """Tipos de papéis de personagens"""
    PROTAGONIST = "protagonist"
    ANTAGONIST = "antagonist"
    SUPPORTING = "supporting"
    MINOR = "minor"
    BACKGROUND = "background"
    UNKNOWN = "unknown"

class RelationType(Enum):
    """Tipos de relações entre personagens"""
    ROMANTIC = "romantic"
    FAMILY = "family"
    FRIENDSHIP = "friendship"
    RIVALRY = "rivalry"
    PROFESSIONAL = "professional"
    CONFLICT = "conflict"
    ALLIANCE = "alliance"
    MENTORSHIP = "mentorship"
    UNKNOWN = "unknown"

@dataclass
class CharacterAppearance:
    """Aparição de personagem em uma cena"""
    scene_number: int
    act_number: int
    page_number: int
    scene_heading: str
    has_dialogue: bool
    dialogue_count: int
    action_mentions: int
    emotional_tone: Optional[str] = None

@dataclass
class CharacterRelation:
    """Relação entre dois personagens"""
    character_a: str
    character_b: str
    relation_type: RelationType
    strength: float  # 0.0 to 1.0
    scenes_together: List[int]
    interactions: int
    conflict_level: float  # 0.0 to 1.0
    evolution: List[Dict[str, Any]] = field(default_factory=list)

@dataclass
class CharacterArc:
    """Arco narrativo de um personagem"""
    character: str
    start_state: Dict[str, Any]
    end_state: Dict[str, Any]
    turning_points: List[Dict[str, Any]]
    emotional_journey: List[str]
    growth_type: str  # positive, negative, static, circular
    complexity_score: float

@dataclass
class Character:
    """Personagem completo com todas análises"""
    name: str
    role: CharacterRole
    first_appearance: CharacterAppearance
    last_appearance: CharacterAppearance
    appearances: List[CharacterAppearance]
    total_scenes: int
    total_dialogue_lines: int
    total_action_mentions: int
    speaking_style: Dict[str, Any]
    relationships: List[CharacterRelation]
    arc: Optional[CharacterArc]
    importance_score: float
    metadata: Dict[str, Any] = field(default_factory=dict)

class CharacterAnalytics:
    """Sistema de análise profunda de personagens"""

    def __init__(self, db_path: str = "data/character_analytics.db"):
        self.db_path = db_path
        self.characters: Dict[str, Character] = {}
        self.relationships: List[CharacterRelation] = []
        self.scene_map: Dict[int, List[str]] = defaultdict(list)
        self.act_structure: Dict[int, List[int]] = defaultdict(list)

        # Padrões de extração
        self.patterns = {
            'character_name': re.compile(r'^([A-Z][A-Z\s\.\-\']+)(?:\s*\([^\)]*\))?\s*$', re.MULTILINE),
            'scene_heading': re.compile(r'^(INT\.|EXT\.|INT/EXT\.|I/E\.)\s+(.+)$', re.MULTILINE),
            'act_marker': re.compile(r'(ACT|ATO)\s+([IVX]+|\d+)', re.IGNORECASE),
            'dialogue': re.compile(r'^([A-Z][A-Z\s\.\-\']+)(?:\s*\([^\)]*\))?\n(.+?)(?=\n[A-Z]|\n\n|\Z)', re.MULTILINE | re.DOTALL),
            'action_line': re.compile(r'^[^A-Z\n].+$', re.MULTILINE),
            'parenthetical': re.compile(r'\([^\)]+\)'),
            'transition': re.compile(r'^(FADE IN:|FADE OUT:|CUT TO:|DISSOLVE TO:|MATCH CUT:)', re.MULTILINE)
        }

        # Inicializar banco de dados
        self._init_database()

    def _init_database(self):
        """Inicializa banco de dados para análises"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Tabela de personagens
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS characters (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                screenplay_id TEXT NOT NULL,
                name TEXT NOT NULL,
                role TEXT,
                first_scene INTEGER,
                last_scene INTEGER,
                total_scenes INTEGER,
                total_dialogues INTEGER,
                importance_score REAL,
                speaking_style TEXT,
                arc_data TEXT,
                metadata TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(screenplay_id, name)
            )
        """)

        # Tabela de relações
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS relationships (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                screenplay_id TEXT NOT NULL,
                character_a TEXT NOT NULL,
                character_b TEXT NOT NULL,
                relation_type TEXT,
                strength REAL,
                conflict_level REAL,
                scenes_together TEXT,
                interactions INTEGER,
                evolution TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Tabela de aparições
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS appearances (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                screenplay_id TEXT NOT NULL,
                character_name TEXT NOT NULL,
                scene_number INTEGER,
                act_number INTEGER,
                page_number INTEGER,
                has_dialogue BOOLEAN,
                dialogue_count INTEGER,
                action_mentions INTEGER,
                emotional_tone TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Tabela de arcos narrativos
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS character_arcs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                screenplay_id TEXT NOT NULL,
                character_name TEXT NOT NULL,
                start_state TEXT,
                end_state TEXT,
                turning_points TEXT,
                emotional_journey TEXT,
                growth_type TEXT,
                complexity_score REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        conn.commit()
        conn.close()

    def analyze_screenplay(self, screenplay_id: str, content: str) -> Dict[str, Any]:
        """
        Análise completa de personagens em um roteiro

        Returns:
            Dict com todas as análises de personagens
        """
        print(f"🎭 Analisando personagens do roteiro {screenplay_id}...")

        # 1. Extrair estrutura básica
        self._extract_structure(content)

        # 2. Identificar personagens
        characters = self._identify_characters(content)

        # 3. Mapear aparições
        for char_name in characters:
            appearances = self._track_appearances(char_name, content)

            # 4. Determinar papel
            role = self._determine_role(char_name, appearances)

            # 5. Analisar estilo de fala
            speaking_style = self._analyze_speaking_style(char_name, content)

            # 6. Calcular importância
            importance = self._calculate_importance(appearances, len(self.scene_map))

            # Criar objeto Character
            character = Character(
                name=char_name,
                role=role,
                first_appearance=appearances[0] if appearances else None,
                last_appearance=appearances[-1] if appearances else None,
                appearances=appearances,
                total_scenes=len(appearances),
                total_dialogue_lines=sum(a.dialogue_count for a in appearances),
                total_action_mentions=sum(a.action_mentions for a in appearances),
                speaking_style=speaking_style,
                relationships=[],
                arc=None,
                importance_score=importance
            )

            self.characters[char_name] = character

        # 7. Identificar relações
        self._identify_relationships(content)

        # 8. Analisar arcos narrativos
        for char_name in self.characters:
            arc = self._analyze_character_arc(char_name, content)
            self.characters[char_name].arc = arc

        # 9. Salvar no banco
        self._save_to_database(screenplay_id)

        # 10. Gerar relatório
        report = self._generate_report()

        print(f"✅ Análise completa: {len(self.characters)} personagens identificados")
        return report

    def _extract_structure(self, content: str):
        """Extrai estrutura de atos e cenas"""
        lines = content.split('\n')
        current_act = 1
        scene_number = 0

        for i, line in enumerate(lines):
            # Detectar mudança de ato
            act_match = self.patterns['act_marker'].search(line)
            if act_match:
                act_text = act_match.group(2)
                if act_text in ['I', '1']:
                    current_act = 1
                elif act_text in ['II', '2']:
                    current_act = 2
                elif act_text in ['III', '3']:
                    current_act = 3
                else:
                    current_act += 1

            # Detectar heading de cena
            scene_match = self.patterns['scene_heading'].match(line)
            if scene_match:
                scene_number += 1
                self.act_structure[current_act].append(scene_number)

    def _identify_characters(self, content: str) -> Set[str]:
        """Identifica todos os personagens únicos"""
        characters = set()

        # Buscar por nomes em diálogos
        dialogue_matches = self.patterns['dialogue'].findall(content)
        for char_name, _ in dialogue_matches:
            # Limpar nome
            clean_name = char_name.strip()
            # Remover parentéticos do nome
            clean_name = re.sub(r'\s*\([^\)]*\)', '', clean_name)
            if clean_name and len(clean_name) > 1:
                characters.add(clean_name)

        # Filtrar nomes muito comuns ou genéricos
        filtered = {c for c in characters if not self._is_generic_name(c)}

        return filtered

    def _is_generic_name(self, name: str) -> bool:
        """Verifica se é um nome genérico"""
        generic = [
            'FADE IN', 'FADE OUT', 'CUT TO', 'THE END',
            'CONTINUED', 'CONT', 'MORE', 'VOICE', 'NARRATOR',
            'ACT I', 'ACT II', 'ACT III', 'ACT', 'ATO',
            'EXT.', 'INT.', 'EXT', 'INT', 'WAREHOUSE', 'COURTROOM',
            'POLICE STATION', 'APARTMENT', 'OFFICE', 'CITY',
            'NEW YORK CITY', 'LATER', 'DAY', 'NIGHT', 'CONTINUOUS'
        ]

        # Verificar se é nome genérico
        if name.upper() in generic:
            return True

        # Verificar se parece com heading de cena
        if any(word in name.upper() for word in ['EXT.', 'INT.', 'ACT', 'FADE', 'CUT']):
            return True

        # Verificar se é muito curto
        if len(name) < 2:
            return True

        # Verificar se contém apenas números ou pontuação
        if not any(c.isalpha() for c in name):
            return True

        return False

    def _track_appearances(self, character: str, content: str) -> List[CharacterAppearance]:
        """Rastreia todas as aparições de um personagem"""
        appearances = []
        lines = content.split('\n')

        current_scene = 0
        current_act = 1
        current_page = 1
        current_heading = ""
        line_count = 0

        for i, line in enumerate(lines):
            # Atualizar página (aproximadamente 55 linhas por página)
            line_count += 1
            if line_count >= 55:
                current_page += 1
                line_count = 0

            # Detectar cena
            scene_match = self.patterns['scene_heading'].match(line)
            if scene_match:
                current_scene += 1
                current_heading = line

                # Determinar ato pela cena
                for act, scenes in self.act_structure.items():
                    if current_scene in scenes:
                        current_act = act
                        break

            # Detectar diálogo do personagem
            if line.strip().startswith(character):
                # Contar linhas de diálogo
                dialogue_lines = 0
                j = i + 1
                while j < len(lines) and lines[j] and not self.patterns['character_name'].match(lines[j]):
                    if not self.patterns['parenthetical'].match(lines[j].strip()):
                        dialogue_lines += 1
                    j += 1

                # Verificar se já registramos esta cena
                existing = next((a for a in appearances if a.scene_number == current_scene), None)
                if existing:
                    existing.dialogue_count += dialogue_lines
                else:
                    appearances.append(CharacterAppearance(
                        scene_number=current_scene,
                        act_number=current_act,
                        page_number=current_page,
                        scene_heading=current_heading,
                        has_dialogue=True,
                        dialogue_count=dialogue_lines,
                        action_mentions=0
                    ))

            # Detectar menções em ação
            elif not scene_match and not line.strip().startswith(character.upper()):
                if re.search(r'\b' + re.escape(character) + r'\b', line, re.IGNORECASE):
                    existing = next((a for a in appearances if a.scene_number == current_scene), None)
                    if existing:
                        existing.action_mentions += 1
                    else:
                        appearances.append(CharacterAppearance(
                            scene_number=current_scene,
                            act_number=current_act,
                            page_number=current_page,
                            scene_heading=current_heading,
                            has_dialogue=False,
                            dialogue_count=0,
                            action_mentions=1
                        ))

        return sorted(appearances, key=lambda x: x.scene_number)

    def _determine_role(self, character: str, appearances: List[CharacterAppearance]) -> CharacterRole:
        """Determina o papel do personagem baseado em aparições"""
        if not appearances:
            return CharacterRole.UNKNOWN

        total_scenes = max(len(self.scene_map), max((a.scene_number for a in appearances), default=1))
        appearance_rate = len(appearances) / max(total_scenes, 1)
        dialogue_total = sum(a.dialogue_count for a in appearances)

        # Verificar presença em diferentes atos
        acts_present = len(set(a.act_number for a in appearances))

        # Verificar se aparece no início e fim (protagonistas típicos)
        first_scene = min(a.scene_number for a in appearances)
        last_scene = max(a.scene_number for a in appearances)

        # Critérios mais flexíveis para determinar papel
        if (appearance_rate >= 0.4 and dialogue_total >= 3) or (acts_present >= 2 and dialogue_total >= 5):
            # Protagonista: alta presença E múltiplos atos OU muitos diálogos
            return CharacterRole.PROTAGONIST
        elif (appearance_rate >= 0.2 and dialogue_total >= 2) or (acts_present >= 2 and dialogue_total >= 3):
            # Supporting: presença moderada com diálogos significativos
            return CharacterRole.SUPPORTING
        elif dialogue_total >= 1 or appearance_rate >= 0.1:
            # Minor: pelo menos algum diálogo ou várias aparições
            return CharacterRole.MINOR
        else:
            # Background: aparições sem diálogos
            return CharacterRole.BACKGROUND

    def _analyze_speaking_style(self, character: str, content: str) -> Dict[str, Any]:
        """Analisa estilo de fala do personagem"""
        style = {
            'avg_line_length': 0,
            'vocabulary_richness': 0,
            'exclamations': 0,
            'questions': 0,
            'formal_level': 0,
            'emotional_words': [],
            'catchphrases': []
        }

        # Coletar todos os diálogos
        dialogues = []
        dialogue_matches = self.patterns['dialogue'].findall(content)

        for char_name, dialogue_text in dialogue_matches:
            if char_name.strip().startswith(character):
                # Limpar parentéticos
                clean_dialogue = self.patterns['parenthetical'].sub('', dialogue_text)
                dialogues.append(clean_dialogue.strip())

        if not dialogues:
            return style

        # Analisar estilo
        all_text = ' '.join(dialogues)
        words = all_text.split()

        # Comprimento médio de linha
        style['avg_line_length'] = len(words) / max(len(dialogues), 1)

        # Riqueza de vocabulário
        unique_words = set(word.lower() for word in words)
        style['vocabulary_richness'] = len(unique_words) / max(len(words), 1)

        # Exclamações e perguntas
        style['exclamations'] = all_text.count('!')
        style['questions'] = all_text.count('?')

        # Nível de formalidade (simplificado)
        informal_markers = ['gonna', 'wanna', 'yeah', 'nah', 'ain\'t', 'kinda']
        informal_count = sum(1 for word in words if word.lower() in informal_markers)
        style['formal_level'] = 1.0 - (informal_count / max(len(words), 1))

        # Palavras emocionais (simplificado)
        emotional_words = ['love', 'hate', 'fear', 'happy', 'sad', 'angry', 'afraid']
        style['emotional_words'] = [w for w in words if w.lower() in emotional_words]

        # Identificar catchphrases (frases repetidas)
        phrase_counter = Counter()
        for dialogue in dialogues:
            if len(dialogue.split()) <= 5:  # Frases curtas
                phrase_counter[dialogue] += 1

        style['catchphrases'] = [phrase for phrase, count in phrase_counter.items() if count > 2]

        return style

    def _calculate_importance(self, appearances: List[CharacterAppearance], total_scenes: int) -> float:
        """Calcula score de importância do personagem"""
        if not appearances or total_scenes == 0:
            return 0.0

        # Fatores de importância
        appearance_rate = len(appearances) / total_scenes
        dialogue_weight = sum(a.dialogue_count for a in appearances) / max(total_scenes * 10, 1)

        # Distribuição por atos (personagens importantes aparecem em todos os atos)
        acts_present = len(set(a.act_number for a in appearances))
        act_distribution = acts_present / 3.0  # Assumindo 3 atos

        # Presença no início e fim (personagens importantes)
        first_third = len([a for a in appearances if a.scene_number <= total_scenes // 3])
        last_third = len([a for a in appearances if a.scene_number > 2 * total_scenes // 3])
        presence_weight = (first_third + last_third) / max(len(appearances), 1)

        # Calcular score final
        importance = (
            appearance_rate * 0.3 +
            dialogue_weight * 0.3 +
            act_distribution * 0.2 +
            presence_weight * 0.2
        )

        return min(importance, 1.0)

    def _identify_relationships(self, content: str):
        """Identifica relações entre personagens"""
        # Mapear cenas onde personagens aparecem juntos
        scene_characters = defaultdict(list)

        for char_name, character in self.characters.items():
            for appearance in character.appearances:
                scene_characters[appearance.scene_number].append(char_name)

        # Identificar pares de personagens
        character_pairs = defaultdict(lambda: {'scenes': [], 'interactions': 0})

        for scene_num, chars_in_scene in scene_characters.items():
            if len(chars_in_scene) < 2:
                continue

            # Criar pares
            for i in range(len(chars_in_scene)):
                for j in range(i + 1, len(chars_in_scene)):
                    pair = tuple(sorted([chars_in_scene[i], chars_in_scene[j]]))
                    character_pairs[pair]['scenes'].append(scene_num)
                    character_pairs[pair]['interactions'] += 1

        # Criar relações
        for (char_a, char_b), data in character_pairs.items():
            if data['interactions'] < 2:  # Mínimo de 2 cenas juntos
                continue

            # Determinar tipo de relação (simplificado)
            relation_type = self._determine_relation_type(char_a, char_b, content)

            # Calcular força da relação
            strength = min(data['interactions'] / 20.0, 1.0)

            # Criar relação
            relation = CharacterRelation(
                character_a=char_a,
                character_b=char_b,
                relation_type=relation_type,
                strength=strength,
                scenes_together=data['scenes'],
                interactions=data['interactions'],
                conflict_level=0.0  # Simplificado
            )

            self.relationships.append(relation)

            # Adicionar aos personagens
            if char_a in self.characters:
                self.characters[char_a].relationships.append(relation)
            if char_b in self.characters:
                self.characters[char_b].relationships.append(relation)

    def _determine_relation_type(self, char_a: str, char_b: str, content: str) -> RelationType:
        """Determina tipo de relação entre personagens (simplificado)"""
        # Buscar diálogos entre os personagens
        dialogue_context = []
        lines = content.split('\n')

        for i, line in enumerate(lines):
            if line.strip().startswith(char_a) or line.strip().startswith(char_b):
                # Pegar contexto ao redor
                start = max(0, i - 5)
                end = min(len(lines), i + 10)
                context = ' '.join(lines[start:end])
                dialogue_context.append(context.lower())

        combined_context = ' '.join(dialogue_context)

        # Detectar tipos de relação por palavras-chave
        if any(word in combined_context for word in ['love', 'kiss', 'marry', 'romance']):
            return RelationType.ROMANTIC
        elif any(word in combined_context for word in ['father', 'mother', 'son', 'daughter', 'brother', 'sister']):
            return RelationType.FAMILY
        elif any(word in combined_context for word in ['friend', 'buddy', 'pal', 'mate']):
            return RelationType.FRIENDSHIP
        elif any(word in combined_context for word in ['fight', 'kill', 'enemy', 'hate']):
            return RelationType.CONFLICT
        elif any(word in combined_context for word in ['boss', 'employee', 'work', 'job']):
            return RelationType.PROFESSIONAL
        else:
            return RelationType.UNKNOWN

    def _analyze_character_arc(self, character: str, content: str) -> Optional[CharacterArc]:
        """Analisa o arco narrativo do personagem"""
        if character not in self.characters:
            return None

        char_data = self.characters[character]
        if not char_data.appearances:
            return None

        # Dividir aparições em início, meio e fim
        total_appearances = len(char_data.appearances)
        first_third = char_data.appearances[:total_appearances // 3]
        middle_third = char_data.appearances[total_appearances // 3:2 * total_appearances // 3]
        last_third = char_data.appearances[2 * total_appearances // 3:]

        # Analisar estado inicial
        start_state = {
            'act': first_third[0].act_number if first_third else 1,
            'dialogue_density': sum(a.dialogue_count for a in first_third) / max(len(first_third), 1),
            'scene_presence': len(first_third)
        }

        # Analisar estado final
        end_state = {
            'act': last_third[-1].act_number if last_third else 3,
            'dialogue_density': sum(a.dialogue_count for a in last_third) / max(len(last_third), 1),
            'scene_presence': len(last_third)
        }

        # Identificar pontos de virada (mudanças significativas)
        turning_points = []

        # Buscar cenas com picos de diálogo
        for appearance in char_data.appearances:
            if appearance.dialogue_count > char_data.total_dialogue_lines / len(char_data.appearances) * 2:
                turning_points.append({
                    'scene': appearance.scene_number,
                    'act': appearance.act_number,
                    'type': 'dialogue_peak'
                })

        # Determinar tipo de crescimento
        growth_type = "static"
        if end_state['dialogue_density'] > start_state['dialogue_density'] * 1.5:
            growth_type = "positive"
        elif end_state['dialogue_density'] < start_state['dialogue_density'] * 0.5:
            growth_type = "negative"
        elif len(turning_points) > 3:
            growth_type = "complex"

        # Calcular complexidade
        complexity_score = min(
            (len(turning_points) / 10.0) +
            (len(char_data.relationships) / 10.0) +
            (char_data.importance_score * 0.5),
            1.0
        )

        return CharacterArc(
            character=character,
            start_state=start_state,
            end_state=end_state,
            turning_points=turning_points[:5],  # Top 5 turning points
            emotional_journey=[],  # Simplificado
            growth_type=growth_type,
            complexity_score=complexity_score
        )

    def _save_to_database(self, screenplay_id: str):
        """Salva análises no banco de dados"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            # Salvar personagens
            for char_name, character in self.characters.items():
                cursor.execute("""
                    INSERT OR REPLACE INTO characters
                    (screenplay_id, name, role, first_scene, last_scene,
                     total_scenes, total_dialogues, importance_score,
                     speaking_style, arc_data, metadata)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    screenplay_id,
                    char_name,
                    character.role.value,
                    character.first_appearance.scene_number if character.first_appearance else 0,
                    character.last_appearance.scene_number if character.last_appearance else 0,
                    character.total_scenes,
                    character.total_dialogue_lines,
                    character.importance_score,
                    json.dumps(character.speaking_style),
                    json.dumps(self._arc_to_dict(character.arc)) if character.arc else None,
                    json.dumps(character.metadata)
                ))

                # Salvar aparições
                for appearance in character.appearances:
                    cursor.execute("""
                        INSERT INTO appearances
                        (screenplay_id, character_name, scene_number, act_number,
                         page_number, has_dialogue, dialogue_count, action_mentions,
                         emotional_tone)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        screenplay_id,
                        char_name,
                        appearance.scene_number,
                        appearance.act_number,
                        appearance.page_number,
                        appearance.has_dialogue,
                        appearance.dialogue_count,
                        appearance.action_mentions,
                        appearance.emotional_tone
                    ))

            # Salvar relações
            for relation in self.relationships:
                cursor.execute("""
                    INSERT INTO relationships
                    (screenplay_id, character_a, character_b, relation_type,
                     strength, conflict_level, scenes_together, interactions,
                     evolution)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    screenplay_id,
                    relation.character_a,
                    relation.character_b,
                    relation.relation_type.value,
                    relation.strength,
                    relation.conflict_level,
                    json.dumps(relation.scenes_together),
                    relation.interactions,
                    json.dumps(relation.evolution)
                ))

            conn.commit()

        except Exception as e:
            print(f"❌ Erro ao salvar no banco: {e}")
            conn.rollback()
        finally:
            conn.close()

    def _arc_to_dict(self, arc: CharacterArc) -> Dict[str, Any]:
        """Converte arco para dicionário"""
        if not arc:
            return {}

        return {
            'character': arc.character,
            'start_state': arc.start_state,
            'end_state': arc.end_state,
            'turning_points': arc.turning_points,
            'emotional_journey': arc.emotional_journey,
            'growth_type': arc.growth_type,
            'complexity_score': arc.complexity_score
        }

    def _generate_report(self) -> Dict[str, Any]:
        """Gera relatório completo de análise"""
        report = {
            'summary': {
                'total_characters': len(self.characters),
                'protagonists': len([c for c in self.characters.values() if c.role == CharacterRole.PROTAGONIST]),
                'supporting': len([c for c in self.characters.values() if c.role == CharacterRole.SUPPORTING]),
                'total_relationships': len(self.relationships),
                'total_scenes': len(self.scene_map),
                'acts': len(self.act_structure)
            },
            'characters': {},
            'relationships': [],
            'character_network': {},
            'act_distribution': {}
        }

        # Detalhes dos personagens
        for char_name, character in self.characters.items():
            report['characters'][char_name] = {
                'role': character.role.value,
                'importance': character.importance_score,
                'scenes': character.total_scenes,
                'dialogues': character.total_dialogue_lines,
                'first_appearance': character.first_appearance.scene_number if character.first_appearance else None,
                'last_appearance': character.last_appearance.scene_number if character.last_appearance else None,
                'speaking_style': character.speaking_style,
                'arc': character.arc.growth_type if character.arc else 'none',
                'relationships': len(character.relationships)
            }

        # Relações
        for relation in self.relationships:
            report['relationships'].append({
                'pair': f"{relation.character_a} - {relation.character_b}",
                'type': relation.relation_type.value,
                'strength': relation.strength,
                'scenes_together': len(relation.scenes_together),
                'interactions': relation.interactions
            })

        # Rede de personagens
        for char_name, character in self.characters.items():
            connections = []
            for rel in character.relationships:
                other = rel.character_b if rel.character_a == char_name else rel.character_a
                connections.append({
                    'character': other,
                    'strength': rel.strength,
                    'type': rel.relation_type.value
                })
            report['character_network'][char_name] = connections

        # Distribuição por atos
        for act, scenes in self.act_structure.items():
            characters_in_act = set()
            for char_name, character in self.characters.items():
                if any(a.act_number == act for a in character.appearances):
                    characters_in_act.add(char_name)

            report['act_distribution'][f"Act {act}"] = {
                'scenes': len(scenes),
                'characters': list(characters_in_act),
                'character_count': len(characters_in_act)
            }

        return report

    def get_character_profile(self, character_name: str) -> Optional[Dict[str, Any]]:
        """Retorna perfil detalhado de um personagem"""
        if character_name not in self.characters:
            return None

        character = self.characters[character_name]

        profile = {
            'name': character.name,
            'role': character.role.value,
            'importance': character.importance_score,
            'appearances': {
                'total_scenes': character.total_scenes,
                'first_scene': character.first_appearance.scene_number if character.first_appearance else None,
                'last_scene': character.last_appearance.scene_number if character.last_appearance else None,
                'acts_present': list(set(a.act_number for a in character.appearances))
            },
            'dialogue': {
                'total_lines': character.total_dialogue_lines,
                'avg_per_scene': character.total_dialogue_lines / max(character.total_scenes, 1),
                'style': character.speaking_style
            },
            'relationships': [
                {
                    'with': rel.character_b if rel.character_a == character_name else rel.character_a,
                    'type': rel.relation_type.value,
                    'strength': rel.strength,
                    'scenes_together': len(rel.scenes_together)
                }
                for rel in character.relationships
            ],
            'arc': {
                'type': character.arc.growth_type if character.arc else 'none',
                'complexity': character.arc.complexity_score if character.arc else 0,
                'turning_points': character.arc.turning_points if character.arc else []
            } if character.arc else None,
            'timeline': [
                {
                    'scene': a.scene_number,
                    'act': a.act_number,
                    'page': a.page_number,
                    'has_dialogue': a.has_dialogue,
                    'dialogue_lines': a.dialogue_count
                }
                for a in character.appearances[:20]  # Primeiras 20 aparições
            ]
        }

        return profile

    def get_relationship_analysis(self, char_a: str, char_b: str) -> Optional[Dict[str, Any]]:
        """Analisa relação entre dois personagens"""
        # Encontrar relação
        relation = None
        for rel in self.relationships:
            if (rel.character_a == char_a and rel.character_b == char_b) or \
               (rel.character_a == char_b and rel.character_b == char_a):
                relation = rel
                break

        if not relation:
            return None

        return {
            'characters': [relation.character_a, relation.character_b],
            'type': relation.relation_type.value,
            'strength': relation.strength,
            'scenes_together': relation.scenes_together,
            'total_interactions': relation.interactions,
            'conflict_level': relation.conflict_level,
            'evolution': relation.evolution,
            'scene_timeline': [
                {
                    'scene': scene,
                    'act': next((a for a, scenes in self.act_structure.items() if scene in scenes), 1)
                }
                for scene in relation.scenes_together[:10]  # Primeiras 10 cenas
            ]
        }

    def export_to_json(self, output_path: str):
        """Exporta análise completa para JSON"""
        report = self._generate_report()

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

        print(f"📁 Relatório exportado para: {output_path}")
        return output_path

    def export_character_graph(self, output_path: str):
        """Exporta grafo de personagens em formato para visualização"""
        graph_data = {
            'nodes': [],
            'edges': []
        }

        # Adicionar nós (personagens)
        for char_name, character in self.characters.items():
            graph_data['nodes'].append({
                'id': char_name,
                'label': char_name,
                'size': character.importance_score * 100,
                'color': self._get_role_color(character.role),
                'role': character.role.value,
                'scenes': character.total_scenes,
                'dialogues': character.total_dialogue_lines
            })

        # Adicionar arestas (relações)
        for relation in self.relationships:
            graph_data['edges'].append({
                'source': relation.character_a,
                'target': relation.character_b,
                'weight': relation.strength,
                'type': relation.relation_type.value,
                'scenes': len(relation.scenes_together),
                'color': self._get_relation_color(relation.relation_type)
            })

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(graph_data, f, indent=2)

        print(f"📊 Grafo exportado para: {output_path}")
        return output_path

    def _get_role_color(self, role: CharacterRole) -> str:
        """Retorna cor para o papel do personagem"""
        colors = {
            CharacterRole.PROTAGONIST: '#FF6B6B',
            CharacterRole.ANTAGONIST: '#4ECDC4',
            CharacterRole.SUPPORTING: '#45B7D1',
            CharacterRole.MINOR: '#96CEB4',
            CharacterRole.BACKGROUND: '#DDA0DD',
            CharacterRole.UNKNOWN: '#808080'
        }
        return colors.get(role, '#808080')

    def _get_relation_color(self, relation_type: RelationType) -> str:
        """Retorna cor para tipo de relação"""
        colors = {
            RelationType.ROMANTIC: '#FF69B4',
            RelationType.FAMILY: '#98D8C8',
            RelationType.FRIENDSHIP: '#87CEEB',
            RelationType.RIVALRY: '#FFA07A',
            RelationType.PROFESSIONAL: '#D3D3D3',
            RelationType.CONFLICT: '#DC143C',
            RelationType.ALLIANCE: '#90EE90',
            RelationType.MENTORSHIP: '#DDA0DD',
            RelationType.UNKNOWN: '#808080'
        }
        return colors.get(relation_type, '#808080')

# Exemplo de uso
if __name__ == "__main__":
    print("🎭 CHARACTER ANALYTICS SYSTEM - FASE 25")
    print("=" * 60)

    # Criar analisador
    analyzer = CharacterAnalytics()

    # Exemplo de roteiro
    sample_screenplay = """
FADE IN:

ACT I

EXT. CITY STREET - DAY

JOHN (30s, determined) walks quickly through the crowd.

SARAH (20s, confident) catches up to him.

SARAH
John, wait! We need to talk.

JOHN
There's nothing to discuss. The decision is made.

SARAH
You can't just leave like this. What about the team?

INT. OFFICE - LATER

John packs his belongings. MARK (40s, boss) enters.

MARK
I heard you're leaving us.

JOHN
It's time for a change, Mark.

MARK
Sarah told me about your plan. It's risky.

JOHN
Sometimes you have to take risks.

ACT II

INT. SARAH'S APARTMENT - NIGHT

Sarah and John discuss their future.

SARAH
I want to come with you.

JOHN
This is my fight, not yours.

SARAH
We're partners, remember?

ACT III

EXT. AIRPORT - DAY

John and Sarah say goodbye to Mark.

MARK
Take care of each other.

FADE OUT.
    """

    # Analisar
    result = analyzer.analyze_screenplay("sample_001", sample_screenplay)

    # Mostrar resultados
    print("\n📊 RESULTADOS DA ANÁLISE:")
    print(f"  Total de personagens: {result['summary']['total_characters']}")
    print(f"  Protagonistas: {result['summary']['protagonists']}")
    print(f"  Relações: {result['summary']['total_relationships']}")

    print("\n👥 PERSONAGENS PRINCIPAIS:")
    for char_name, data in result['characters'].items():
        print(f"\n  {char_name}:")
        print(f"    - Papel: {data['role']}")
        print(f"    - Importância: {data['importance']:.2%}")
        print(f"    - Cenas: {data['scenes']}")
        print(f"    - Diálogos: {data['dialogues']}")

    print("\n💑 RELAÇÕES:")
    for rel in result['relationships']:
        print(f"  {rel['pair']}: {rel['type']} (força: {rel['strength']:.2f})")

    # Exportar
    analyzer.export_to_json("output/character_analysis.json")
    analyzer.export_character_graph("output/character_graph.json")

    print("\n✅ Sistema de Character Analytics implementado com sucesso!")