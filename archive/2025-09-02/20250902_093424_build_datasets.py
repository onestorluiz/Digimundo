#!/usr/bin/env python
import os
import urllib.request
import json
from pathlib import Path
import re

def download_shakespeare():
    """Download Shakespeare plays from Project Gutenberg"""
    base_path = Path("data/original")
    base_path.mkdir(parents=True, exist_ok=True)
    
    plays = {
        "hamlet": "https://www.gutenberg.org/files/1524/1524-0.txt",
        "macbeth": "https://www.gutenberg.org/files/1533/1533-0.txt",
        "romeo_juliet": "https://www.gutenberg.org/files/1513/1513-0.txt"
    }
    
    print("📚 Downloading Shakespeare plays...")
    for name, url in plays.items():
        output_path = base_path / f"{name}.txt"
        if not output_path.exists():
            print(f"  Downloading {name}...")
            urllib.request.urlretrieve(url, output_path)
    
    # Process into acts and scenes
    for play_file in base_path.glob("*.txt"):
        process_play(play_file)
    
    print("✅ Datasets ready")

def process_play(filepath: Path):
    """Extract acts and scenes from play"""
    text = filepath.read_text(encoding='utf-8', errors='ignore')
    
    # Find acts and scenes
    acts = re.split(r'ACT [IVX]+', text)
    
    output_dir = filepath.parent.parent / "structured" / filepath.stem
    output_dir.mkdir(parents=True, exist_ok=True)
    
    for i, act in enumerate(acts[1:], 1):  # Skip pre-act content
        scenes = re.split(r'SCENE [IVX]+', act)
        for j, scene in enumerate(scenes[1:], 1):  # Skip pre-scene content
            scene_file = output_dir / f"act{i}_scene{j}.txt"
            scene_file.write_text(scene[:5000])  # Limit size

def generate_qa_pairs():
    """Generate QA pairs from structured plays"""
    qa_pairs = []
    
    structured_dir = Path("data/structured")
    for play_dir in structured_dir.glob("*"):
        for scene_file in play_dir.glob("*.txt"):
            text = scene_file.read_text()
            
            # Extract character names (simple heuristic)
            characters = re.findall(r'^([A-Z][A-Z]+)\.|^([A-Z][a-z]+)\.', text, re.MULTILINE)
            characters = list(set([c[0] or c[1] for c in characters if c[0] or c[1]]))
            
            if characters:
                # Generate simple QA
                qa_pairs.append({
                    "question": f"Who appears in {play_dir.name} {scene_file.stem}?",
                    "answer": ", ".join(characters[:3]),
                    "context": text[:500]
                })
    
    # Save QA pairs
    qa_file = Path("data/qa_pairs.json")
    qa_file.write_text(json.dumps(qa_pairs, indent=2))
    print(f"✅ Generated {len(qa_pairs)} QA pairs")

if __name__ == "__main__":
    download_shakespeare()
    generate_qa_pairs()
