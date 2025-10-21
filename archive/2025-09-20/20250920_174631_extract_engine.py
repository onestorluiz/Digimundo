#!/usr/bin/env python3
"""
Extract Engine - Estágio 1 do Pipeline de Análise
Extrai elementos fundamentais de roteiros
Fase 2.B - Implementação real
"""

import re
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum
import json

@dataclass
class Character:
    """Representa um personagem extraído"""
    name: str
    first_appearance: int  # Página
    dialogue_count: int = 0
    action_count: int = 0
    scenes: List[int] = field(default_factory=list)
    description: Optional[str] = None
    
    @property
    def importance_score(self) -> float:
        """Calcula importância baseada em presença"""
        return (self.dialogue_count * 2 + self.action_count + len(self.scenes)) / 10

@dataclass
class Scene:
    """Representa uma cena extraída"""
    number: int
    location: str
    time: str  # DAY/NIGHT/DAWN/DUSK
    setting: str  # INT/EXT
    page_start: int
    page_end: int
    characters: List[str] = field(default_factory=list)
    description: str = ""
    
    @property
    def duration_pages(self) -> float:
        """Duração estimada em páginas"""
        return self.page_end - self.page_start + 1

@dataclass
class Dialogue:
    """Representa um diálogo extraído"""
    character: str
    text: str
    scene: int
    page: int
    emotional_tone: Optional[str] = None

class ScriptFormat(Enum):
    """Formatos de roteiro suportados"""
    FOUNTAIN = "fountain"
    FINAL_DRAFT = "fdx"
    PDF = "pdf"
    PLAIN_TEXT = "txt"

class ExtractEngine:
    """
    Motor de extração - Estágio 1 do pipeline
    Extrai personagens, cenas, diálogos e ações
    """
    
    # Padrões regex para identificação
    PATTERNS = {
        # Slug line: INT./EXT. LOCATION - TIME
        "slug_line": r'^(INT\.|EXT\.|INT/EXT\.|I/E\.)\s+(.+?)\s*[-–]\s*(DAY|NIGHT|DAWN|DUSK|CONTINUOUS|LATER|MOMENTS LATER)',
        
        # Nome de personagem (CAPS, pode ter parênteses)
        "character": r'^([A-Z][A-Z\s]+)(\s*\([^\)]+\))?$',
        
        # Diálogo (indentado, não caps)
        "dialogue": r'^\s{10,}(.+)$',
        
        # Parênteses de ação (parenthetical)
        "parenthetical": r'^\s*\(([^\)]+)\)\s*$',
        
        # Transição (FADE IN:, CUT TO:, etc)
        "transition": r'^(FADE\s+(IN|OUT|TO BLACK)|CUT\s+TO|DISSOLVE\s+TO|MATCH\s+CUT|SMASH\s+CUT|IRIS\s+(IN|OUT)|WIPE\s+TO):?\s*$',
        
        # Número de página
        "page_number": r'^\s*(\d+)\s*\.?\s*$'
    }
    
    def __init__(self):
        """Inicializa engine de extração"""
        self.characters: Dict[str, Character] = {}
        self.scenes: List[Scene] = []
        self.dialogues: List[Dialogue] = []
        self.current_page = 1
        self.current_scene = 0
        self.format = ScriptFormat.PLAIN_TEXT
    
    def extract(self, script_content: str, format: ScriptFormat = ScriptFormat.PLAIN_TEXT) -> Dict[str, Any]:
        """
        Extrai todos os elementos do roteiro
        Retorna dicionário com elementos extraídos
        """
        self.format = format
        
        # Reset estado
        self.characters.clear()
        self.scenes.clear()
        self.dialogues.clear()
        self.current_page = 1
        self.current_scene = 0
        
        # Processa conteúdo baseado no formato
        if format == ScriptFormat.FOUNTAIN:
            self._process_fountain(script_content)
        elif format == ScriptFormat.FINAL_DRAFT:
            self._process_fdx(script_content)
        elif format == ScriptFormat.PDF:
            self._process_pdf(script_content)
        else:
            self._process_plain_text(script_content)
        
        # Calcula estatísticas
        stats = self._calculate_statistics()
        
        return {
            "characters": self._serialize_characters(),
            "scenes": self._serialize_scenes(),
            "dialogues": self._serialize_dialogues(),
            "statistics": stats,
            "format": format.value
        }
    
    def _process_plain_text(self, content: str) -> None:
        """Processa roteiro em texto simples"""
        lines = content.split('\n')
        
        current_character = None
        in_dialogue = False
        scene_description = []
        
        for i, line in enumerate(lines):
            # Detecta número de página
            if re.match(self.PATTERNS["page_number"], line):
                page_match = re.match(self.PATTERNS["page_number"], line)
                if page_match:
                    self.current_page = int(page_match.group(1))
                continue
            
            # Detecta slug line (nova cena)
            slug_match = re.match(self.PATTERNS["slug_line"], line, re.IGNORECASE)
            if slug_match:
                # Salva cena anterior se houver
                if self.current_scene > 0 and self.scenes:
                    self.scenes[-1].page_end = self.current_page
                    self.scenes[-1].description = '\n'.join(scene_description)
                
                # Cria nova cena
                self.current_scene += 1
                setting = slug_match.group(1).replace('.', '').strip()
                location = slug_match.group(2).strip()
                time = slug_match.group(3).strip()
                
                scene = Scene(
                    number=self.current_scene,
                    location=location,
                    time=time,
                    setting=setting,
                    page_start=self.current_page,
                    page_end=self.current_page
                )
                self.scenes.append(scene)
                scene_description = []
                in_dialogue = False
                current_character = None
                continue
            
            # Detecta nome de personagem
            char_match = re.match(self.PATTERNS["character"], line.strip())
            if char_match and not in_dialogue and len(line.strip()) > 2:
                char_name = char_match.group(1).strip()
                
                # Ignora transições que parecem nomes
                if not re.match(self.PATTERNS["transition"], char_name):
                    current_character = self._normalize_character_name(char_name)
                    in_dialogue = True
                    
                    # Adiciona personagem se não existe
                    if current_character not in self.characters:
                        self.characters[current_character] = Character(
                            name=current_character,
                            first_appearance=self.current_page
                        )
                    
                    # Adiciona à cena atual
                    if self.scenes and current_character not in self.scenes[-1].characters:
                        self.scenes[-1].characters.append(current_character)
                    
                    # Adiciona cena ao personagem
                    if self.scenes and self.current_scene not in self.characters[current_character].scenes:
                        self.characters[current_character].scenes.append(self.current_scene)
                    
                    continue
            
            # Detecta diálogo
            if in_dialogue and current_character:
                dialogue_match = re.match(self.PATTERNS["dialogue"], line)
                parenthetical_match = re.match(self.PATTERNS["parenthetical"], line.strip())
                
                if dialogue_match or parenthetical_match:
                    if dialogue_match:
                        dialogue_text = dialogue_match.group(1).strip()
                        
                        # Adiciona diálogo
                        dialogue = Dialogue(
                            character=current_character,
                            text=dialogue_text,
                            scene=self.current_scene,
                            page=self.current_page
                        )
                        self.dialogues.append(dialogue)
                        self.characters[current_character].dialogue_count += 1
                    
                    # Parenthetical é parte do diálogo
                    if parenthetical_match and self.dialogues:
                        self.dialogues[-1].emotional_tone = parenthetical_match.group(1)
                    
                    continue
                elif line.strip() == "":
                    # Linha vazia termina diálogo
                    in_dialogue = False
                    current_character = None
                else:
                    # Linha não-diálogo termina modo diálogo
                    in_dialogue = False
                    current_character = None
            
            # Coleta descrição de cena
            if self.scenes and not in_dialogue and line.strip():
                scene_description.append(line.strip())
                
                # Conta ações de personagens mencionados
                for char_name in self.characters:
                    if char_name in line.upper():
                        self.characters[char_name].action_count += 1
        
        # Finaliza última cena
        if self.scenes:
            self.scenes[-1].page_end = self.current_page
            self.scenes[-1].description = '\n'.join(scene_description)
    
    def _process_fountain(self, content: str) -> None:
        """Processa formato Fountain (simplificado)"""
        # Fountain usa marcação similar a Markdown
        # Por enquanto, converte para plain text
        self._process_plain_text(content)
    
    def _process_fdx(self, content: str) -> None:
        """Processa formato Final Draft XML (stub)"""
        # Requer parsing XML
        # Por enquanto, tenta extrair texto
        import xml.etree.ElementTree as ET
        try:
            root = ET.fromstring(content)
            # Extrai texto de todos os elementos
            text_content = []
            for elem in root.iter():
                if elem.text:
                    text_content.append(elem.text)
            self._process_plain_text('\n'.join(text_content))
        except:
            # Fallback para texto simples
            self._process_plain_text(content)
    
    def _process_pdf(self, content: str) -> None:
        """Processa PDF (assumindo texto já extraído)"""
        # PDF requer biblioteca externa para extração
        # Assume que conteúdo já foi extraído como texto
        self._process_plain_text(content)
    
    def _normalize_character_name(self, name: str) -> str:
        """Normaliza nome de personagem"""
        # Remove (V.O.), (O.S.), (CONT'D) etc
        name = re.sub(r'\([^\)]+\)', '', name).strip()
        # Remove números (JOHN 2 -> JOHN)
        name = re.sub(r'\s+\d+$', '', name).strip()
        return name
    
    def _calculate_statistics(self) -> Dict[str, Any]:
        """Calcula estatísticas da extração"""
        total_dialogue = sum(char.dialogue_count for char in self.characters.values())
        total_action = sum(char.action_count for char in self.characters.values())
        
        # Identifica protagonista (mais diálogos)
        protagonist = None
        if self.characters:
            protagonist = max(self.characters.values(), key=lambda c: c.dialogue_count).name
        
        # Calcula distribuição de cenas
        scene_distribution = {
            "INT": sum(1 for s in self.scenes if s.setting == "INT"),
            "EXT": sum(1 for s in self.scenes if s.setting == "EXT"),
            "DAY": sum(1 for s in self.scenes if s.time == "DAY"),
            "NIGHT": sum(1 for s in self.scenes if s.time == "NIGHT")
        }
        
        return {
            "total_characters": len(self.characters),
            "total_scenes": len(self.scenes),
            "total_dialogues": len(self.dialogues),
            "total_pages": self.current_page,
            "dialogue_lines": total_dialogue,
            "action_mentions": total_action,
            "protagonist": protagonist,
            "scene_distribution": scene_distribution,
            "avg_scene_length": sum(s.duration_pages for s in self.scenes) / len(self.scenes) if self.scenes else 0
        }
    
    def _serialize_characters(self) -> List[Dict[str, Any]]:
        """Serializa personagens para output"""
        return [
            {
                "name": char.name,
                "first_appearance": char.first_appearance,
                "dialogue_count": char.dialogue_count,
                "action_count": char.action_count,
                "scenes": char.scenes,
                "importance_score": round(char.importance_score, 2),
                "description": char.description
            }
            for char in sorted(self.characters.values(), key=lambda c: c.importance_score, reverse=True)
        ]
    
    def _serialize_scenes(self) -> List[Dict[str, Any]]:
        """Serializa cenas para output"""
        return [
            {
                "number": scene.number,
                "location": scene.location,
                "time": scene.time,
                "setting": scene.setting,
                "pages": f"{scene.page_start}-{scene.page_end}",
                "duration": scene.duration_pages,
                "characters": scene.characters,
                "description": scene.description[:200] + "..." if len(scene.description) > 200 else scene.description
            }
            for scene in self.scenes
        ]
    
    def _serialize_dialogues(self) -> List[Dict[str, Any]]:
        """Serializa diálogos (primeiros 20 para amostra)"""
        return [
            {
                "character": dialogue.character,
                "text": dialogue.text,
                "scene": dialogue.scene,
                "page": dialogue.page,
                "tone": dialogue.emotional_tone
            }
            for dialogue in self.dialogues[:20]  # Amostra
        ]
    
    def extract_from_file(self, filepath: str) -> Dict[str, Any]:
        """Extrai de arquivo"""
        # Detecta formato pela extensão
        if filepath.endswith('.fountain'):
            format = ScriptFormat.FOUNTAIN
        elif filepath.endswith('.fdx'):
            format = ScriptFormat.FINAL_DRAFT
        elif filepath.endswith('.pdf'):
            format = ScriptFormat.PDF
        else:
            format = ScriptFormat.PLAIN_TEXT
        
        # Lê arquivo
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            return self.extract(content, format)
        except Exception as e:
            return {
                "error": f"Erro lendo arquivo: {str(e)}",
                "characters": [],
                "scenes": [],
                "dialogues": [],
                "statistics": {}
            }

# Singleton global
_engine_instance: Optional[ExtractEngine] = None

def get_extract_engine() -> ExtractEngine:
    """Retorna instância singleton"""
    global _engine_instance
    if _engine_instance is None:
        _engine_instance = ExtractEngine()
    return _engine_instance

__all__ = ["ExtractEngine", "Character", "Scene", "Dialogue", "ScriptFormat", "get_extract_engine"]