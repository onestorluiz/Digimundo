"""
Analyze Engine - Estágio 2 do Pipeline de Análise
Analisa estrutura, ritmo e desenvolvimento
Fase 2.B - Implementação real
"""
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum
import statistics

@dataclass
class Act:
    """Representa um ato do roteiro"""
    number: int
    start_page: int
    end_page: int
    scenes: List[int]
    turning_points: List[str]

    @property
    def duration(self) -> int:
        """Duração em páginas"""
        return self.end_page - self.start_page + 1

    @property
    def percentage(self) -> float:
        """Percentual do roteiro"""
        return 0.0

@dataclass
class CharacterArc:
    """Arco de desenvolvimento do personagem"""
    character: str
    introduction: str
    conflict: str
    climax: str
    resolution: str
    transformation_score: float
    consistency_score: float

@dataclass
class PlotPoint:
    """Ponto importante da trama"""
    page: int
    scene: int
    description: str
    type: str
    impact: float

class PacingAnalysis:
    """Análise de ritmo"""

    def __init__(self):
        self.scene_lengths: List[float] = []
        self.dialogue_density: List[float] = []
        self.action_density: List[float] = []
        self.tempo_changes: List[Tuple[int, str]] = []

    @property
    def avg_scene_length(self) -> float:
        """Comprimento médio de cena"""
        return statistics.mean(self.scene_lengths) if self.scene_lengths else 0

    @property
    def pacing_variance(self) -> float:
        """Variância do ritmo (maior = mais dinâmico)"""
        return statistics.stdev(self.scene_lengths) if len(self.scene_lengths) > 1 else 0

class AnalyzeEngine:
    """
    Motor de análise - Estágio 2 do pipeline
    Analisa estrutura narrativa, desenvolvimento e ritmo
    """
    ACT_PROPORTIONS = {1: (0.25, 'Setup'), 2: (0.5, 'Confrontation'), 3: (0.25, 'Resolution')}
    PLOT_POINTS = {'inciting_incident': (10, 15), 'plot_point_1': (25, 30), 'midpoint': (50, 60), 'plot_point_2': (75, 85), 'climax': (90, 100), 'resolution': (100, 120)}

    def __init__(self):
        """Inicializa engine de análise"""
        self.acts: List[Act] = []
        self.character_arcs: Dict[str, CharacterArc] = {}
        self.plot_points: List[PlotPoint] = []
        self.pacing = PacingAnalysis()
        self.themes: List[str] = []
        self.genre_markers: Dict[str, int] = {}

    def analyze(self, extracted_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analisa dados extraídos do estágio 1
        Retorna análise estrutural completa
        """
        self.acts.clear()
        self.character_arcs.clear()
        self.plot_points.clear()
        self.pacing = PacingAnalysis()
        self.themes.clear()
        self.genre_markers.clear()
        characters = extracted_data.get('characters', [])
        scenes = extracted_data.get('scenes', [])
        dialogues = extracted_data.get('dialogues', [])
        stats = extracted_data.get('statistics', {})
        total_pages = stats.get('total_pages', 120)
        self._analyze_three_act_structure(scenes, total_pages)
        self._analyze_character_arcs(characters, scenes, dialogues)
        self._identify_plot_points(scenes, total_pages)
        self._analyze_pacing(scenes, dialogues)
        self._identify_themes(dialogues, scenes)
        self._detect_genre(scenes, dialogues)
        structure_score = self._calculate_structure_score()
        character_score = self._calculate_character_score()
        pacing_score = self._calculate_pacing_score()
        dialogue_score = self._calculate_dialogue_score(dialogues)
        return {'three_act_structure': self._serialize_acts(total_pages), 'character_arcs': self._serialize_character_arcs(), 'plot_points': self._serialize_plot_points(), 'pacing_analysis': self._serialize_pacing(), 'themes': self.themes, 'genre_indicators': self.genre_markers, 'scores': {'structure': round(structure_score, 1), 'characters': round(character_score, 1), 'pacing': round(pacing_score, 1), 'dialogue': round(dialogue_score, 1), 'overall': round((structure_score + character_score + pacing_score + dialogue_score) / 4, 1)}, 'recommendations': self._generate_recommendations(structure_score, character_score, pacing_score)}

    def _analyze_three_act_structure(self, scenes: List[Dict], total_pages: int) -> None:
        """Analisa estrutura de três atos"""
        if not scenes:
            return
        act1_end = int(total_pages * self.ACT_PROPORTIONS[1][0])
        act2_end = act1_end + int(total_pages * self.ACT_PROPORTIONS[2][0])
        act1_scenes = []
        act2_scenes = []
        act3_scenes = []
        for scene in scenes:
            pages = scene.get('pages', '1-1').split('-')
            start_page = int(pages[0]) if pages[0].isdigit() else 1
            if start_page <= act1_end:
                act1_scenes.append(scene['number'])
            elif start_page <= act2_end:
                act2_scenes.append(scene['number'])
            else:
                act3_scenes.append(scene['number'])
        if act1_scenes:
            self.acts.append(Act(number=1, start_page=1, end_page=act1_end, scenes=act1_scenes, turning_points=['Apresentação', 'Incidente Incitante']))
        if act2_scenes:
            self.acts.append(Act(number=2, start_page=act1_end + 1, end_page=act2_end, scenes=act2_scenes, turning_points=['Ponto de Virada 1', 'Midpoint', 'Ponto de Virada 2']))
        if act3_scenes:
            self.acts.append(Act(number=3, start_page=act2_end + 1, end_page=total_pages, scenes=act3_scenes, turning_points=['Clímax', 'Resolução']))

    def _analyze_character_arcs(self, characters: List[Dict], scenes: List[Dict], dialogues: List[Dict]) -> None:
        """Analisa arcos dos personagens principais"""
        main_characters = characters[:3] if len(characters) >= 3 else characters
        for char_data in main_characters:
            char_name = char_data['name']
            char_scenes = char_data.get('scenes', [])
            if not char_scenes:
                continue
            first_third = char_scenes[:len(char_scenes) // 3]
            middle_third = char_scenes[len(char_scenes) // 3:2 * len(char_scenes) // 3]
            final_third = char_scenes[2 * len(char_scenes) // 3:]
            arc = CharacterArc(character=char_name, introduction=f"Aparece na página {char_data['first_appearance']}, cenas {first_third[:3]}", conflict=f'Desenvolve conflito nas cenas {middle_third[:3]}', climax=f'Momento decisivo nas cenas {final_third[:2]}', resolution=f'Resolução nas cenas finais {final_third[-2:]}', transformation_score=self._calculate_transformation(char_scenes), consistency_score=self._calculate_consistency(char_data))
            self.character_arcs[char_name] = arc

    def _identify_plot_points(self, scenes: List[Dict], total_pages: int) -> None:
        """Identifica pontos principais da trama"""
        if not scenes:
            return
        for point_name, (min_page, max_page) in self.PLOT_POINTS.items():
            adjusted_min = int(min_page / 120 * total_pages)
            adjusted_max = int(max_page / 120 * total_pages)
            for scene in scenes:
                pages = scene.get('pages', '1-1').split('-')
                start_page = int(pages[0]) if pages[0].isdigit() else 1
                if adjusted_min <= start_page <= adjusted_max:
                    plot_point = PlotPoint(page=start_page, scene=scene['number'], description=f"{point_name.replace('_', ' ').title()} - {scene['location']}", type=point_name, impact=7.5)
                    self.plot_points.append(plot_point)
                    break

    def _analyze_pacing(self, scenes: List[Dict], dialogues: List[Dict]) -> None:
        """Analisa ritmo do roteiro"""
        if not scenes:
            return
        for scene in scenes:
            duration = scene.get('duration', 1)
            self.pacing.scene_lengths.append(duration)
            scene_dialogues = [d for d in dialogues if d.get('scene') == scene['number']]
            dialogue_ratio = len(scene_dialogues) / max(duration, 1)
            self.pacing.dialogue_density.append(dialogue_ratio)
            description_length = len(scene.get('description', ''))
            action_ratio = description_length / max(duration * 100, 1)
            self.pacing.action_density.append(action_ratio)
        for i in range(1, len(scenes)):
            if scenes[i]['time'] != scenes[i - 1]['time']:
                self.pacing.tempo_changes.append((scenes[i]['number'], scenes[i]['time']))

    def _identify_themes(self, dialogues: List[Dict], scenes: List[Dict]) -> None:
        """Identifica temas principais (simplificado)"""
        theme_keywords = {'amor': ['amor', 'amar', 'coração', 'paixão', 'romance'], 'vingança': ['vingança', 'vingar', 'justiça', 'retribuição'], 'redenção': ['perdão', 'redimir', 'segunda chance', 'arrependimento'], 'família': ['família', 'pai', 'mãe', 'filho', 'irmão'], 'poder': ['poder', 'controle', 'domínio', 'autoridade'], 'sacrifício': ['sacrifício', 'abrir mão', 'desistir', 'pelo bem'], 'identidade': ['quem sou', 'identidade', 'verdadeiro eu', 'descobrir'], 'sobrevivência': ['sobreviver', 'viver', 'morrer', 'perigo']}
        all_dialogue_text = ' '.join([d.get('text', '') for d in dialogues]).lower()
        theme_scores = {}
        for theme, keywords in theme_keywords.items():
            score = sum((all_dialogue_text.count(keyword) for keyword in keywords))
            if score > 2:
                theme_scores[theme] = score
        self.themes = sorted(theme_scores.keys(), key=theme_scores.get, reverse=True)[:3]

    def _detect_genre(self, scenes: List[Dict], dialogues: List[Dict]) -> None:
        """Detecta marcadores de gênero"""
        genre_indicators = {'ação': ['EXT', 'NIGHT', 'perseguição', 'luta', 'explosão', 'tiro'], 'drama': ['INT', 'DAY', 'conversa', 'emoção', 'lágrima', 'conflito'], 'comédia': ['piada', 'rir', 'engraçado', 'humor', 'ridículo'], 'terror': ['NIGHT', 'escuro', 'medo', 'sangue', 'morte', 'gritar'], 'romance': ['amor', 'beijo', 'abraço', 'coração', 'paixão'], 'ficção': ['futuro', 'tecnologia', 'espaço', 'alienígena', 'robô'], 'thriller': ['suspense', 'mistério', 'perigo', 'tensão', 'revelar']}
        for genre, indicators in genre_indicators.items():
            count = 0
            for scene in scenes:
                for indicator in indicators:
                    if indicator in ['INT', 'EXT', 'DAY', 'NIGHT']:
                        if scene.get('setting') == indicator or scene.get('time') == indicator:
                            count += 1
                    elif indicator.lower() in scene.get('description', '').lower():
                        count += 2
            for dialogue in dialogues[:50]:
                for indicator in indicators:
                    if indicator.lower() in dialogue.get('text', '').lower():
                        count += 1
            if count > 5:
                self.genre_markers[genre] = count

    def _calculate_transformation(self, char_scenes: List[int]) -> float:
        """Calcula score de transformação do personagem"""
        if len(char_scenes) < 2:
            return 0.0
        first_scene = char_scenes[0]
        last_scene = char_scenes[-1]
        spread = last_scene - first_scene
        score = min(10, spread / 10 * 2)
        return score

    def _calculate_consistency(self, char_data: Dict) -> float:
        """Calcula consistência do personagem"""
        dialogue_count = char_data.get('dialogue_count', 0)
        scene_count = len(char_data.get('scenes', []))
        if scene_count == 0:
            return 0.0
        ratio = dialogue_count / scene_count
        score = min(10, ratio * 2)
        return score

    def _calculate_structure_score(self) -> float:
        """Calcula score da estrutura"""
        if len(self.acts) != 3:
            return 5.0
        score = 10.0
        act1 = self.acts[0]
        act2 = self.acts[1] if len(self.acts) > 1 else None
        act3 = self.acts[2] if len(self.acts) > 2 else None
        if act1 and act1.duration > 35:
            score -= 2
        if act2 and (act2.duration < 40 or act2.duration > 70):
            score -= 2
        if act3 and act3.duration > 35:
            score -= 1
        essential_points = ['inciting_incident', 'climax']
        found_points = [p.type for p in self.plot_points]
        for point in essential_points:
            if point not in found_points:
                score -= 1
        return max(0, score)

    def _calculate_character_score(self) -> float:
        """Calcula score dos personagens"""
        if not self.character_arcs:
            return 5.0
        arc_scores = [arc.transformation_score * 0.6 + arc.consistency_score * 0.4 for arc in self.character_arcs.values()]
        return min(10, statistics.mean(arc_scores)) if arc_scores else 5.0

    def _calculate_pacing_score(self) -> float:
        """Calcula score do ritmo"""
        if not self.pacing.scene_lengths:
            return 5.0
        score = 10.0
        if self.pacing.pacing_variance < 0.5:
            score -= 2
        elif self.pacing.pacing_variance > 3:
            score -= 1
        long_scenes = [s for s in self.pacing.scene_lengths if s > 5]
        if len(long_scenes) > len(self.pacing.scene_lengths) * 0.2:
            score -= 2
        if len(self.pacing.tempo_changes) < 3:
            score -= 1
        return max(0, score)

    def _calculate_dialogue_score(self, dialogues: List[Dict]) -> float:
        """Calcula score dos diálogos"""
        if not dialogues:
            return 5.0
        score = 8.0
        avg_length = statistics.mean([len(d.get('text', '')) for d in dialogues[:50]])
        if avg_length < 20:
            score -= 1
        elif avg_length > 150:
            score -= 2
        unique_speakers = len(set((d.get('character') for d in dialogues[:50])))
        if unique_speakers < 5:
            score -= 1
        return max(0, min(10, score))

    def _generate_recommendations(self, structure: float, character: float, pacing: float) -> List[str]:
        """Gera recomendações baseadas nos scores"""
        recommendations = []
        if structure < 7:
            recommendations.append('📐 Revisar estrutura de três atos - verificar proporções e plot points')
        if character < 7:
            recommendations.append('👥 Desenvolver melhor os arcos dos personagens principais')
        if pacing < 7:
            recommendations.append('⏱️ Ajustar ritmo - variar comprimento das cenas')
        if not self.themes:
            recommendations.append('💭 Fortalecer temas centrais da narrativa')
        if len(self.plot_points) < 4:
            recommendations.append('📍 Adicionar plot points claros (incidente incitante, viradas, clímax)')
        if not recommendations:
            recommendations.append('✨ Roteiro bem estruturado! Focar em polimento e detalhes')
        return recommendations

    def _serialize_acts(self, total_pages: int) -> Dict[str, Any]:
        """Serializa atos para output"""
        result = {}
        if not self.acts:
            return {'act1': {'pages': 0, 'scenes': 0, 'percentage': 0}, 'act2': {'pages': 0, 'scenes': 0, 'percentage': 0}, 'act3': {'pages': 0, 'scenes': 0, 'percentage': 0}}
        for act in self.acts:
            act_key = f'act{act.number}'
            result[act_key] = {'number': act.number, 'name': self.ACT_PROPORTIONS.get(act.number, ('', 'Unknown'))[1], 'pages': act.duration, 'page_range': f'{act.start_page}-{act.end_page}', 'percentage': round(act.duration / total_pages * 100, 1) if total_pages > 0 else 0, 'scenes': len(act.scenes), 'turning_points': act.turning_points}
        for i in range(1, 4):
            act_key = f'act{i}'
            if act_key not in result:
                result[act_key] = {'pages': 0, 'scenes': 0, 'percentage': 0}
        return result

    def _serialize_character_arcs(self) -> List[Dict[str, Any]]:
        """Serializa arcos para output"""
        return [{'character': arc.character, 'introduction': arc.introduction, 'conflict': arc.conflict, 'climax': arc.climax, 'resolution': arc.resolution, 'transformation_score': arc.transformation_score, 'consistency_score': arc.consistency_score, 'overall_score': round((arc.transformation_score + arc.consistency_score) / 2, 1)} for arc in self.character_arcs.values()]

    def _serialize_plot_points(self) -> Dict[str, Any]:
        """Serializa plot points para output"""
        result = {'inciting_incident': None, 'plot_point_1': None, 'midpoint': None, 'plot_point_2': None, 'climax': None, 'resolution': None}
        for point in self.plot_points:
            point_type = point.type.lower()
            if 'inciting' in point_type:
                result['inciting_incident'] = {'page': point.page, 'scene': point.scene, 'description': point.description}
            elif 'midpoint' in point_type:
                result['midpoint'] = {'page': point.page, 'scene': point.scene, 'description': point.description}
            elif 'climax' in point_type:
                result['climax'] = {'page': point.page, 'scene': point.scene, 'description': point.description}
        return result

    def _serialize_pacing(self) -> Dict[str, Any]:
        """Serializa análise de ritmo"""
        return {'average_scene_length': round(self.pacing.avg_scene_length, 2), 'pacing_variance': round(self.pacing.pacing_variance, 2), 'tempo_changes': len(self.pacing.tempo_changes), 'dialogue_density': round(statistics.mean(self.pacing.dialogue_density), 2) if self.pacing.dialogue_density else 0, 'action_density': round(statistics.mean(self.pacing.action_density), 2) if self.pacing.action_density else 0, 'rhythm': 'Dinâmico' if self.pacing.pacing_variance > 1.5 else 'Uniforme'}
_engine_instance: Optional[AnalyzeEngine] = None

def get_analyze_engine() -> AnalyzeEngine:
    """Retorna instância singleton"""
    global _engine_instance
    if _engine_instance is None:
        _engine_instance = AnalyzeEngine()
    return _engine_instance
__all__ = ['AnalyzeEngine', 'Act', 'CharacterArc', 'PlotPoint', 'PacingAnalysis', 'get_analyze_engine']