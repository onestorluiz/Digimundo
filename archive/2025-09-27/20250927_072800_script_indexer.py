
from dataclasses import dataclass
from typing import List, Tuple
import re
SCENE_RE = r'^(INT\.|EXT\.)[^\n]*$'
@dataclass
class Scene:
    title: str
    start_line: int
    end_line: int
    text: str
def _split_lines(text: str) -> List[str]: return text.splitlines()
def _is_scene_header(line: str) -> bool: return bool(re.match(SCENE_RE, line.strip()))
def parse_scenes(script_text: str) -> List[Scene]:
    lines = _split_lines(script_text); scenes: List[Scene] = []
    cur_title = "START"; cur_start = 1
    for i, line in enumerate(lines, start=1):
        if _is_scene_header(line):
            if i > cur_start:
                seg = "\n".join(lines[cur_start-1:i-1]).rstrip("\n")
                scenes.append(Scene(title=cur_title, start_line=cur_start, end_line=i-1, text=seg))
            cur_title = line.strip(); cur_start = i
    if cur_start <= len(lines):
        seg = "\n".join(lines[cur_start-1:]).rstrip("\n")
        scenes.append(Scene(title=cur_title, start_line=cur_start, end_line=len(lines), text=seg))
    return scenes
def line_to_page_line(line_no: int, page_lines: int = 55) -> Tuple[int, int]:
    page = (line_no - 1) // page_lines + 1
    line_in_page = (line_no - 1) % page_lines + 1
    return page, line_in_page
def format_offset(start_line: int, end_line: int, page_lines: int = 55) -> str:
    ps, ls = line_to_page_line(start_line, page_lines); pe, le = line_to_page_line(end_line, page_lines)
    return f"p{ps}:l{ls}-{le}" if ps == pe else f"p{ps}:l{ls}-p{pe}:l{le}"
