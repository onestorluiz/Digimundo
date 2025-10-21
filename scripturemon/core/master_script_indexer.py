"""
MasterScriptIndexer - Indexador de Roteiros Mestres

Indexa todos os roteiros clássicos/famosos em content/screenplays/masters/
para busca rápida de exemplos e soluções.

Usado pelo ExampleFinderCore (Python 2) no Triple-Core.
"""

from pathlib import Path
from typing import List, Dict, Any, Optional
import re
from dataclasses import dataclass


@dataclass
class ScriptExample:
    """Exemplo de diálogo/cena de um roteiro mestre"""
    screenplay: str
    scene_number: Optional[int]
    character: str
    dialogue: str
    context: str  # Contexto da cena (action lines antes/depois)
    line_number: int


class MasterScriptIndexer:
    """
    Indexa roteiros mestres para busca de exemplos.

    Roteiros indexados:
    - The Matrix, Inception, Interstellar (Christopher Nolan)
    - Pulp Fiction, Django Unchained (Tarantino)
    - The Shawshank Redemption, The Dark Knight
    - Apocalypse Now, Casablanca
    - Memento, The Departed, The Shining
    """

    def __init__(self, masters_dir: Path = None):
        self.masters_dir = masters_dir or Path("content/screenplays/masters")
        self.index: List[ScriptExample] = []
        self.screenplay_metadata: Dict[str, Dict[str, Any]] = {}

    def index_all(self) -> int:
        """
        Indexa todos os roteiros mestres.

        Returns:
            Número de exemplos indexados
        """
        if not self.masters_dir.exists():
            raise FileNotFoundError(f"Masters directory not found: {self.masters_dir}")

        screenplay_files = list(self.masters_dir.glob("*.txt"))

        for screenplay_path in screenplay_files:
            self._index_screenplay(screenplay_path)

        return len(self.index)

    def _index_screenplay(self, screenplay_path: Path):
        """Indexa um único roteiro"""
        screenplay_name = self._clean_screenplay_name(screenplay_path.stem)

        with open(screenplay_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        # Metadata
        self.screenplay_metadata[screenplay_name] = {
            'path': screenplay_path,
            'size': len(content),
            'lines': len(content.splitlines())
        }

        # Parse diálogos
        lines = content.splitlines()
        for i, line in enumerate(lines):
            # Detectar personagem (ALL CAPS seguido de diálogo)
            if line.strip() and line.strip().isupper() and len(line.strip()) < 30:
                character = line.strip()

                # FILTROS DE QUALIDADE: Ignorar falsos positivos
                # 1. Ignorar headers de cena/roteiro
                if character in ['FADE IN:', 'FADE OUT:', 'CUT TO:', 'DISSOLVE TO:',
                                'INT.', 'EXT.', 'FADE IN', 'FADE OUT', 'THE END',
                                'CONTINUED:', '(CONTINUED)', 'CONT\'D', 'V.O.', 'O.S.']:
                    continue

                # 2. Ignorar se começa com número (scene heading)
                if character and character[0].isdigit():
                    continue

                # 3. Ignorar se tem pontos/vírgulas (provavelmente stage direction)
                if any(char in character for char in ['.', ',', ':', ';']) and character not in ['DR. CLARISSE', 'MR. SMITH']:
                    continue

                # Pegar diálogo (próximas linhas indentadas)
                dialogue_lines = []
                context_before = []
                context_after = []

                # Contexto antes (action lines)
                for j in range(max(0, i-5), i):
                    if lines[j].strip() and not lines[j].strip().isupper():
                        context_before.append(lines[j].strip())

                # Diálogo (até 15 linhas ou próximo personagem)
                for j in range(i+1, min(i+15, len(lines))):
                    if lines[j].strip():
                        if lines[j].strip().isupper() and len(lines[j].strip()) < 30:
                            break  # Próximo personagem
                        # Ignorar parentheticals
                        if lines[j].strip().startswith('(') and lines[j].strip().endswith(')'):
                            continue
                        dialogue_lines.append(lines[j].strip())
                    else:
                        break  # Linha vazia = fim do diálogo

                # FILTRO DE QUALIDADE: Diálogo precisa ter pelo menos 10 palavras
                full_dialogue = ' '.join(dialogue_lines)
                if len(full_dialogue.split()) < 10:
                    continue  # Diálogo muito curto, ignorar

                # Contexto depois
                for j in range(i+len(dialogue_lines)+1, min(i+len(dialogue_lines)+6, len(lines))):
                    if lines[j].strip() and not lines[j].strip().isupper():
                        context_after.append(lines[j].strip())

                if dialogue_lines:
                    example = ScriptExample(
                        screenplay=screenplay_name,
                        scene_number=self._extract_scene_number(content, i),
                        character=character,
                        dialogue=' '.join(dialogue_lines),
                        context=' '.join(context_before[-2:] + context_after[:2]),
                        line_number=i
                    )
                    self.index.append(example)

    @staticmethod
    def _clean_screenplay_name(filename: str) -> str:
        """Limpa nome do arquivo para nome legível"""
        # Remove sufixos
        name = filename.replace('_-_screenplay', '').replace('_-_release', '').replace('.docx', '')
        name = re.sub(r'[-_]', ' ', name)
        return name.title().strip()

    @staticmethod
    def _extract_scene_number(content: str, line_pos: int) -> Optional[int]:
        """Tenta extrair número da cena (INT./EXT. headers)"""
        lines = content.splitlines()
        # Procurar para trás até achar INT. ou EXT.
        for i in range(line_pos, max(0, line_pos-50), -1):
            line = lines[i].strip().upper()
            if line.startswith(('INT.', 'EXT.')):
                # Tentar extrair número
                match = re.search(r'SCENE\s+(\d+)', line)
                if match:
                    return int(match.group(1))
        return None

    def find_examples_by_problem(self, problem_type: str, max_results: int = 5) -> List[ScriptExample]:
        """
        Busca exemplos de como resolver um tipo de problema.

        Args:
            problem_type: Tipo de problema (ex: "lack of subtext", "flat character")
            max_results: Máximo de exemplos

        Returns:
            Lista de exemplos relevantes
        """
        # TODO: Implementar busca semântica/embeddings
        # Por enquanto: busca simples por keywords

        keywords = problem_type.lower().split()
        results = []

        for example in self.index:
            # Score baseado em keywords no contexto/diálogo
            score = 0
            text = (example.dialogue + ' ' + example.context).lower()

            for keyword in keywords:
                if keyword in text:
                    score += 1

            if score > 0:
                results.append((score, example))

        # Sort por score decrescente
        results.sort(key=lambda x: x[0], reverse=True)

        return [ex for _, ex in results[:max_results]]

    def find_examples_by_character_trait(self, trait: str, max_results: int = 5) -> List[ScriptExample]:
        """
        Busca exemplos de personagens com certa característica.

        Args:
            trait: Característica (ex: "witty", "conflicted", "mysterious")
        """
        # Similar a find_examples_by_problem mas focado em traits
        return self.find_examples_by_problem(trait, max_results)

    def get_screenplay_stats(self, screenplay_name: str) -> Optional[Dict[str, Any]]:
        """Retorna estatísticas de um roteiro específico"""
        return self.screenplay_metadata.get(screenplay_name)

    def list_available_screenplays(self) -> List[str]:
        """Lista todos os roteiros indexados"""
        return list(self.screenplay_metadata.keys())


# Singleton global (carregado sob demanda)
_global_indexer: Optional[MasterScriptIndexer] = None


def get_master_indexer() -> MasterScriptIndexer:
    """Retorna indexer global (singleton)"""
    global _global_indexer
    if _global_indexer is None:
        _global_indexer = MasterScriptIndexer()
        _global_indexer.index_all()
    return _global_indexer
