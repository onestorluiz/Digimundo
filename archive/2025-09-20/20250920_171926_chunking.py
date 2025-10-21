from typing import List, Dict
import re

def split_by_scenes(pages: List[str], scene_markers=None) -> List[Dict]:
    scene_markers = scene_markers or ["INT.", "EXT.", "INT/", "EXT/"]
    scenes = []
    current = {"title":"", "content":[], "start_page":1}
    page_num = 1
    pattern = re.compile(rf'^\s*(?:{"|".join([re.escape(m) for m in scene_markers])})', re.IGNORECASE)
    for txt in pages:
        lines = txt.splitlines()
        for i, line in enumerate(lines):
            if pattern.match(line):
                if current["content"]:
                    scenes.append({**current, "end_page": page_num, "text":"\n".join(current["content"])})
                    current = {"title": line.strip(), "content":[], "start_page": page_num}
            current["content"].append(line)
        page_num += 1
    if current["content"]:
        scenes.append({**current, "end_page": page_num-1, "text":"\n".join(current["content"])})
    return scenes

def smart_chunk(texts: List[str], target_tokens: int = 500, overlap_tokens: int = 100) -> List[str]:
    target_words = int(target_tokens * 0.75)
    overlap_words = int(overlap_tokens * 0.75)
    chunks = []
    for t in texts:
        words = t.split()
        if len(words) <= target_words:
            chunks.append(t)
            continue
        start = 0
        while start < len(words):
            end = min(len(words), start + target_words)
            chunk = " ".join(words[start:end])
            chunks.append(chunk)
            start = max(end - overlap_words, start + 1)
    return chunks
