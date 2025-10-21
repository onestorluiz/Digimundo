"""
🎯📚🚀 SCRIPT DOCTOR ADVANCED TECHNIQUES - STATE OF THE ART 2024/2025
Implementação das técnicas mais avançadas descobertas em pesquisas acadêmicas e da indústria
"""
import os
import sys
import json
import numpy as np
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum, auto
import asyncio
import aiohttp
from collections import defaultdict
import re

class NarrativeBeat(Enum):
    """Save the Cat Beat Sheet - 15 beats com posições exatas"""
    OPENING_IMAGE = (0.01, "Snapshot of protagonist's life before the adventure")
    THEME_STATED = (0.05, 'Hint at lesson protagonist will learn')
    SETUP = (0.1, "Introduce protagonist's world and what's missing")
    CATALYST = (0.12, 'Life-changing event that launches the story')
    DEBATE = (0.12, 0.25, 'Should protagonist go on this journey?')
    BREAK_INTO_TWO = (0.25, 'Protagonist enters new world')
    B_STORY = (0.3, 'Introduction of love interest/mentor')
    FUN_AND_GAMES = (0.3, 0.5, 'Promise of the premise delivered')
    MIDPOINT = (0.5, 'Stakes are raised, time clock appears')
    BAD_GUYS_CLOSE_IN = (0.5, 0.75, 'Things get worse for protagonist')
    ALL_IS_LOST = (0.75, 'Lowest point, whiff of death')
    DARK_NIGHT_OF_SOUL = (0.75, 0.85, 'Protagonist hits rock bottom')
    BREAK_INTO_THREE = (0.85, 'Solution discovered')
    FINALE = (0.85, 0.99, 'Final battle using lessons learned')
    FINAL_IMAGE = (0.99, 'Opposite of opening image')

@dataclass
class BeatAnalysis:
    """Resultado da análise de um beat narrativo"""
    beat: NarrativeBeat
    position: float
    confidence: float
    scene_text: str
    analysis: str
    suggestions: List[str]

class HierarchicalPromptArchitecture:
    """
    Implementação da arquitetura hierárquica de prompts do DeepMind/Dramatron
    Técnica mais poderosa: prompt chaining hierárquico
    """

    def __init__(self, ollama_client):
        self.client = ollama_client
        self.context_chain = []

    async def analyze_hierarchical(self, script_text: str) -> Dict[str, Any]:
        """
        Análise hierárquica em 5 níveis progressivos
        Cada nível usa o output do anterior como contexto
        """
        logline_prompt = f'\n        Extract the core story from this screenplay in ONE sentence:\n        {script_text[:3000]}\n\n        Format: [PROTAGONIST] must [OBJECTIVE] but [OBSTACLE] or else [STAKES].\n        Be specific. Include genre markers.\n        '
        logline = await self.client.generate(logline_prompt, temperature=0.3)
        self.context_chain.append(('logline', logline))
        beats_prompt = f'\n        Given this logline: {logline}\n\n        And this screenplay excerpt: {script_text[:5000]}\n\n        Identify these specific story beats with page numbers:\n        1. CATALYST (around 12% - what kicks off the story?)\n        2. BREAK INTO TWO (25% - entering new world)\n        3. MIDPOINT (50% - false victory or defeat)\n        4. ALL IS LOST (75% - lowest point)\n        5. CLIMAX (90% - final confrontation)\n\n        Output as JSON with page numbers and brief description.\n        '
        beats = await self.client.generate(beats_prompt, temperature=0.2)
        self.context_chain.append(('beats', beats))
        character_prompt = f"\n        Logline: {logline}\n        Structure: {beats}\n\n        Analyze the protagonist's transformation:\n        1. WANT (external goal): What do they pursue?\n        2. NEED (internal growth): What must they learn?\n        3. LIE (false belief): What misconception drives them?\n        4. TRUTH (theme): What truth must they accept?\n        5. GHOST (backstory wound): What past trauma shapes them?\n\n        Track how each beat challenges their lie and reveals their truth.\n        "
        character_arc = await self.client.generate(character_prompt, temperature=0.4)
        self.context_chain.append(('character', character_arc))
        theme_prompt = f'\n        Based on:\n        - Logline: {logline}\n        - Structure: {beats}\n        - Character Arc: {character_arc}\n\n        Identify:\n        1. CENTRAL THEME: The universal truth being explored\n        2. THEMATIC QUESTION: What philosophical question drives the story?\n        3. THEMATIC ARGUMENT: What position does the story take?\n        4. COUNTER-ARGUMENT: How is the opposite view presented?\n        5. SYNTHESIS: How are both views reconciled (or not)?\n\n        Cite specific scenes that explore each element.\n        '
        thematic_analysis = await self.client.generate(theme_prompt, temperature=0.5)
        self.context_chain.append(('theme', thematic_analysis))
        synthesis_prompt = f'\n        Complete Analysis Chain:\n        1. Logline: {logline}\n        2. Structure: {beats}\n        3. Character: {character_arc}\n        4. Theme: {thematic_analysis}\n\n        Provide 5 SPECIFIC, ACTIONABLE improvements:\n        - Include exact page numbers\n        - Quote problematic lines\n        - Provide rewrite suggestions\n        - Explain how each change reinforces theme/character\n\n        Priority order by impact on overall story.\n        '
        final_recommendations = await self.client.generate(synthesis_prompt, temperature=0.3)
        return {'logline': logline, 'beats': beats, 'character_arc': character_arc, 'theme': thematic_analysis, 'recommendations': final_recommendations, 'context_chain': self.context_chain}

class SaveTheCatBeatDetector:
    """
    Detector automático de beats usando as posições exatas do Save the Cat
    Beats aparecem em posições previsíveis no roteiro
    """

    def __init__(self, ollama_client):
        self.client = ollama_client
        self.beat_positions = {'opening_image': (0.0, 0.02), 'theme_stated': (0.04, 0.06), 'setup': (0.01, 0.1), 'catalyst': (0.1, 0.12), 'debate': (0.12, 0.25), 'break_into_two': (0.24, 0.26), 'b_story': (0.28, 0.32), 'fun_and_games': (0.3, 0.5), 'midpoint': (0.48, 0.52), 'bad_guys_close_in': (0.5, 0.75), 'all_is_lost': (0.73, 0.77), 'dark_night': (0.75, 0.85), 'break_into_three': (0.83, 0.87), 'finale': (0.85, 0.98), 'final_image': (0.98, 1.0)}

    def calculate_position(self, page_num: int, total_pages: int) -> float:
        """Calcula posição relativa no roteiro"""
        return page_num / total_pages

    async def detect_beat(self, scene_text: str, page_num: int, total_pages: int) -> BeatAnalysis:
        """
        Detecta qual beat narrativo uma cena representa
        Usa posição + análise de conteúdo
        """
        position = self.calculate_position(page_num, total_pages)
        expected_beat = None
        for beat_name, (start, end) in self.beat_positions.items():
            if start <= position <= end:
                expected_beat = beat_name
                break
        prompt = f"\n        Page {page_num} of {total_pages} (position: {position:.1%})\n        Expected beat: {expected_beat}\n\n        Scene text:\n        {scene_text[:1000]}\n\n        Analyze if this scene matches the expected '{expected_beat}' beat:\n\n        1. Does it fulfill the function of {expected_beat}?\n        2. What story elements confirm or contradict this?\n        3. Confidence level (0-100%)\n        4. If it's a different beat, which one?\n\n        Be specific. Reference actual dialogue/action.\n        "
        analysis = await self.client.generate(prompt, temperature=0.2)
        confidence = self._extract_confidence(analysis)
        return BeatAnalysis(beat=expected_beat, position=position, confidence=confidence, scene_text=scene_text[:500], analysis=analysis, suggestions=self._extract_suggestions(analysis))

    def _extract_confidence(self, analysis: str) -> float:
        """Extrai nível de confiança da análise"""
        import re
        match = re.search('(\\d+)%', analysis)
        if match:
            return float(match.group(1)) / 100
        return 0.5

    def _extract_suggestions(self, analysis: str) -> List[str]:
        """Extrai sugestões da análise"""
        suggestions = []
        lines = analysis.split('\n')
        for line in lines:
            if any((keyword in line.lower() for keyword in ['should', 'could', 'suggest', 'recommend'])):
                suggestions.append(line.strip())
        return suggestions[:3]

class ChainOfThoughtAnalyzer:
    """
    Implementação de Chain-of-Thought para análise narrativa
    Força o modelo a explicar seu raciocínio passo a passo
    """

    def __init__(self, ollama_client):
        self.client = ollama_client

    async def analyze_scene_cot(self, scene_text: str) -> Dict[str, Any]:
        """
        Análise Chain-of-Thought em 7 passos
        """
        cot_prompt = f"\n        Analyze this scene using step-by-step reasoning:\n\n        SCENE:\n        {scene_text}\n\n        STEP 1 - Scene Function:\n        First, identify what narrative purpose this scene serves.\n        Is it: Setup? Catalyst? Complication? Climax? Resolution?\n        Explain your reasoning.\n\n        STEP 2 - Character Objectives:\n        For each character present, identify:\n        - WANT: What they're trying to achieve in this scene\n        - OBSTACLE: What's preventing them\n        - TACTIC: How they're trying to overcome it\n        Show your work.\n\n        STEP 3 - Conflict Analysis:\n        Identify the central conflict:\n        - TYPE: Man vs Man/Self/Nature/Society?\n        - STAKES: What happens if protagonist fails?\n        - ESCALATION: How does tension build?\n        Trace the conflict beat by beat.\n\n        STEP 4 - Dialogue Effectiveness:\n        Examine each exchange:\n        - SUBTEXT: What's unsaid but implied?\n        - VOICE: Is each character distinct?\n        - ECONOMY: Could it be said with fewer words?\n        Quote specific lines as examples.\n\n        STEP 5 - Visual Storytelling:\n        What story is told without dialogue?\n        - ACTIONS: What do characters DO?\n        - ENVIRONMENT: How does setting reflect emotion?\n        - OBJECTS: Any symbolic props/imagery?\n        Describe the visual narrative.\n\n        STEP 6 - Pacing Assessment:\n        Evaluate rhythm and tempo:\n        - ENTRY: Do we enter the scene at the right moment?\n        - EXIT: Do we leave at the peak?\n        - TEMPO: Fast/slow/varied?\n        Rate pacing 1-10 and justify.\n\n        STEP 7 - Synthesis and Improvements:\n        Based on ALL above analysis:\n        1. What's working well?\n        2. What's the biggest problem?\n        3. Provide ONE specific rewrite suggestion\n\n        Show how you arrived at each conclusion.\n        "
        analysis = await self.client.generate(cot_prompt, temperature=0.4)
        steps = self._parse_cot_steps(analysis)
        return {'full_analysis': analysis, 'steps': steps, 'scene_function': steps.get('step_1'), 'character_objectives': steps.get('step_2'), 'conflict': steps.get('step_3'), 'dialogue': steps.get('step_4'), 'visual': steps.get('step_5'), 'pacing': steps.get('step_6'), 'improvements': steps.get('step_7')}

    def _parse_cot_steps(self, analysis: str) -> Dict[str, str]:
        """Parse individual steps from CoT analysis"""
        steps = {}
        current_step = None
        current_content = []
        for line in analysis.split('\n'):
            if 'STEP' in line:
                if current_step:
                    steps[current_step] = '\n'.join(current_content)
                current_step = f"step_{line.split()[1].rstrip(':')}"
                current_content = []
            else:
                current_content.append(line)
        if current_step:
            steps[current_step] = '\n'.join(current_content)
        return steps

class MetaPromptingSystem:
    """
    Sistema de Meta-Prompting onde o LLM cria seus próprios prompts otimizados
    Técnica avançada de auto-otimização
    """

    def __init__(self, ollama_client):
        self.client = ollama_client
        self.optimized_prompts = {}

    async def create_optimized_prompt(self, task_type: str, context: Dict[str, Any]) -> str:
        """
        Pede ao LLM para criar o prompt perfeito para si mesmo
        """
        meta_prompt = f"\n        You are a prompt engineering expert. Create the PERFECT prompt for analyzing:\n\n        Task Type: {task_type}\n        Genre: {context.get('genre', 'unknown')}\n        Script Length: {context.get('pages', 'unknown')} pages\n        Specific Goals: {context.get('goals', 'comprehensive analysis')}\n\n        The prompt should:\n        1. Be highly specific and detailed\n        2. Include exact output format requirements\n        3. Specify evaluation criteria\n        4. Include examples where helpful\n        5. Be self-contained (no external references needed)\n        6. Produce consistent, high-quality results\n\n        Consider:\n        - What context does the model need?\n        - What reasoning steps should be explicit?\n        - What output structure works best?\n        - What temperature/parameters are optimal?\n\n        Create a prompt that YOU would find ideal for this task.\n        Include [PLACEHOLDERS] for variable content.\n        "
        optimized = await self.client.generate(meta_prompt, temperature=0.6)
        self.optimized_prompts[task_type] = optimized
        return optimized

    async def use_optimized_prompt(self, task_type: str, content: str) -> str:
        """
        Usa o prompt otimizado criado pelo próprio LLM
        """
        if task_type not in self.optimized_prompts:
            await self.create_optimized_prompt(task_type, {'goals': 'detailed analysis'})
        prompt = self.optimized_prompts[task_type]
        prompt = prompt.replace('[CONTENT]', content)
        prompt = prompt.replace('[SCRIPT]', content)
        return await self.client.generate(prompt, temperature=0.3)

class MultiAgentValidator:
    """
    Sistema de validação usando múltiplos agentes especializados
    Cada agente é expert em um aspecto específico do roteiro
    """

    def __init__(self, ollama_client):
        self.client = ollama_client
        self.agents = self._initialize_agents()

    def _initialize_agents(self) -> Dict[str, str]:
        """Define agentes especializados"""
        return {'structure_expert': "\n                You are a three-act structure expert with 20 years analyzing Hollywood scripts.\n                You understand Save the Cat, Hero's Journey, and Sequence Method.\n                Focus ONLY on structural elements: setups, payoffs, plot points, pacing.\n                Ignore dialogue and character unless it affects structure.\n            ", 'character_psychologist': '\n                You are a character psychologist specializing in protagonist psychology.\n                You understand wants vs needs, lies vs truths, ghosts and wounds.\n                Focus ONLY on character consistency, arc progression, and motivation.\n                Track internal and external conflicts precisely.\n            ', 'dialogue_doctor': "\n                You are Aaron Sorkin's dialogue coach.\n                You understand subtext, voice differentiation, and verbal dynamics.\n                Focus ONLY on dialogue: rhythm, authenticity, economy, subtext.\n                Each character must have a distinct voice.\n            ", 'theme_philosopher': '\n                You are a thematic analyst with a PhD in comparative literature.\n                You identify central themes, track thematic arguments, and symbolic patterns.\n                Focus ONLY on meaning, symbolism, and philosophical questions.\n                Connect every element to the central thematic statement.\n            ', 'market_analyst': '\n                You are a studio executive evaluating commercial viability.\n                You understand target audiences, genre expectations, and market trends.\n                Focus ONLY on marketability, budget implications, and audience appeal.\n                Be brutally honest about commercial prospects.\n            '}

    async def analyze_with_all_agents(self, script: str) -> Dict[str, Any]:
        """
        Analisa script com todos os agentes em paralelo
        """
        analyses = {}
        tasks = []
        for agent_type, system_prompt in self.agents.items():
            task = self._agent_analysis(agent_type, system_prompt, script)
            tasks.append(task)
        results = await asyncio.gather(*tasks)
        for agent_type, result in zip(self.agents.keys(), results):
            analyses[agent_type] = result
        synthesis = await self._synthesize_analyses(analyses)
        return {'individual_analyses': analyses, 'synthesis': synthesis, 'consensus_score': self._calculate_consensus(analyses)}

    async def _agent_analysis(self, agent_type: str, system_prompt: str, script: str) -> Dict[str, Any]:
        """Análise individual de um agente"""
        prompt = f'\n        {system_prompt}\n\n        Analyze this script excerpt:\n        {script[:3000]}\n\n        Provide:\n        1. Top 3 strengths\n        2. Top 3 weaknesses\n        3. Overall score (1-10)\n        4. Most urgent fix with specific suggestion\n        '
        response = await self.client.generate(prompt, temperature=0.3)
        return {'agent': agent_type, 'analysis': response, 'timestamp': asyncio.get_event_loop().time()}

    async def _synthesize_analyses(self, analyses: Dict[str, Any]) -> str:
        """Sintetiza análises de todos os agentes"""
        synthesis_prompt = f"\n        You are the head script doctor synthesizing feedback from specialist consultants.\n\n        Structure Expert: {analyses['structure_expert']['analysis'][:500]}\n        Character Psychologist: {analyses['character_psychologist']['analysis'][:500]}\n        Dialogue Doctor: {analyses['dialogue_doctor']['analysis'][:500]}\n        Theme Philosopher: {analyses['theme_philosopher']['analysis'][:500]}\n        Market Analyst: {analyses['market_analyst']['analysis'][:500]}\n\n        Create unified feedback that:\n        1. Identifies consensus issues (mentioned by multiple experts)\n        2. Resolves conflicting opinions with reasoning\n        3. Prioritizes fixes by impact on overall script\n        4. Provides 5 specific, actionable notes with page numbers\n\n        Be decisive. The writer needs clear direction.\n        "
        return await self.client.generate(synthesis_prompt, temperature=0.4)

    def _calculate_consensus(self, analyses: Dict[str, Any]) -> float:
        """Calcula nível de consenso entre agentes"""
        scores = []
        for analysis in analyses.values():
            import re
            match = re.search('(\\d+)/10', analysis['analysis'])
            if match:
                scores.append(int(match.group(1)))
        if scores:
            mean = np.mean(scores)
            std = np.std(scores)
            consensus = 1 - std / 10
            return consensus
        return 0.5

class EmotionalArcTracker:
    """
    Rastreia arco emocional de personagens usando análise de sentimento
    Identifica pontos de virada emocionais
    """

    def __init__(self):
        self.emotional_beats = []

    def analyze_character_emotions(self, screenplay_data: Dict[str, Any]) -> Dict[str, List]:
        """
        Analisa trajetória emocional de cada personagem
        """
        character_arcs = defaultdict(list)
        for scene in screenplay_data.get('scenes', []):
            for dialogue in scene.get('dialogues', []):
                character = dialogue.get('character')
                text = dialogue.get('text')
                emotion = self._analyze_emotion(text)
                character_arcs[character].append({'scene': scene.get('number'), 'page': scene.get('page'), 'emotion': emotion, 'intensity': self._calculate_intensity(text), 'text_sample': text[:100]})
        for character, arc in character_arcs.items():
            turning_points = self._detect_turning_points(arc)
            character_arcs[character] = {'arc': arc, 'turning_points': turning_points, 'emotional_range': self._calculate_range(arc)}
        return dict(character_arcs)

    def _analyze_emotion(self, text: str) -> str:
        """Análise básica de emoção"""
        emotions = {'joy': ['happy', 'joy', 'laugh', 'smile', 'love'], 'anger': ['angry', 'rage', 'hate', 'furious'], 'fear': ['afraid', 'scared', 'terror', 'panic'], 'sadness': ['sad', 'cry', 'tears', 'depressed'], 'neutral': []}
        text_lower = text.lower()
        for emotion, keywords in emotions.items():
            if any((keyword in text_lower for keyword in keywords)):
                return emotion
        return 'neutral'

    def _calculate_intensity(self, text: str) -> float:
        """Calcula intensidade emocional"""
        intensity_markers = ['!', '...', 'CAPS', 'very', 'extremely', 'absolutely']
        intensity = 0.5
        for marker in intensity_markers:
            if marker == 'CAPS':
                if text.isupper():
                    intensity += 0.3
            elif marker in text:
                intensity += 0.1
        return min(intensity, 1.0)

    def _detect_turning_points(self, arc: List[Dict]) -> List[Dict]:
        """Detecta mudanças significativas no arco emocional"""
        turning_points = []
        for i in range(1, len(arc) - 1):
            prev_emotion = arc[i - 1]['emotion']
            curr_emotion = arc[i]['emotion']
            next_emotion = arc[i + 1]['emotion']
            if prev_emotion != curr_emotion or curr_emotion != next_emotion:
                turning_points.append({'scene': arc[i]['scene'], 'from_emotion': prev_emotion, 'to_emotion': curr_emotion, 'significance': self._calculate_significance(arc[i])})
        return turning_points

    def _calculate_range(self, arc: List[Dict]) -> float:
        """Calcula amplitude emocional do personagem"""
        emotions = set((beat['emotion'] for beat in arc))
        return len(emotions) / 5.0

    def _calculate_significance(self, beat: Dict) -> float:
        """Calcula significância de um momento emocional"""
        return beat['intensity'] * 0.7 + 0.3
OPTIMIZED_MODELFILE = '\nFROM llama2:13b\n\nPARAMETER temperature 0.3\nPARAMETER top_k 10\nPARAMETER top_p 0.9\nPARAMETER repeat_penalty 1.1\nPARAMETER num_predict 2048\nPARAMETER num_ctx 4096\n\nSYSTEM You are an elite script doctor with expertise in:\n- Three-act structure and Save the Cat methodology\n- Character psychology and authentic dialogue\n- Theme development and symbolic imagery\n- Market analysis and commercial viability\n\nYou provide specific, actionable feedback with:\n- Exact page numbers and scene references\n- Line-by-line dialogue improvements\n- Clear cause-effect reasoning\n- Priority ranking by impact\n\nNever give vague feedback. Always explain WHY a change improves the script.\nUse industry-standard terminology. Reference successful films as comparisons.\n\nTEMPLATE ### Analysis Request:\n{{ .Prompt }}\n\n### Expert Analysis:\n{{ .Response }}\n'

def main():
    """Demonstração das técnicas avançadas"""
    print('\n' + '🎯' * 50)
    print('SCRIPT DOCTOR ADVANCED TECHNIQUES')
    print('State of the Art 2024/2025')
    print('🎯' * 50)

    class MockOllama:

        def generate(self, prompt, temperature=0.5):
            return f'Mock analysis for: {prompt[:100]}...'
    client = MockOllama()
    print('\n📊 Hierarchical Prompt Architecture:')
    hierarchical = HierarchicalPromptArchitecture(client)
    print('\n🎬 Save the Cat Beat Detection:')
    beat_detector = SaveTheCatBeatDetector(client)
    print('\n🧠 Chain of Thought Analysis:')
    cot_analyzer = ChainOfThoughtAnalyzer(client)
    print('\n👥 Multi-Agent Validation:')
    multi_agent = MultiAgentValidator(client)
    print('\n✅ Advanced techniques ready for implementation!')
    print('🚀 These represent cutting-edge script analysis methods')
if __name__ == '__main__':
    asyncio.run(main())