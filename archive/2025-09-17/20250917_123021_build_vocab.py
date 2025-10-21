import json, math, random, os, re
from collections import Counter, defaultdict
from typing import Dict, List, Tuple
from pathlib import Path
import tiktoken
from .apps.scripturemon.digilang.tokenizer_utils import get_single_token_strings, ENC_NAME
from .apps.scripturemon.digilang_advanced.vocab_schema import Vocab, VocabMeta
SEED = 42
random.seed(SEED)
BUDGETS = {'core_symbols': 120, 'relation': 80, 'connectives': 80, 'mwe': 600, 'entity_prefix': 12, 'num_alphabet': 64}
CORE_LABELS = ['ACT_1', 'ACT_2', 'ACT_3', 'ACT_1A', 'ACT_1B', 'ACT_2A', 'ACT_2B', 'ACT_3A', 'ACT_3B', 'BEAT_OPENING', 'BEAT_THEME', 'BEAT_CATALYST', 'BEAT_DEBATE', 'BEAT_B2', 'BEAT_BSTORY', 'BEAT_FUN', 'BEAT_MIDPOINT', 'BEAT_BADGUYS', 'BEAT_LOST', 'BEAT_DARK', 'BEAT_B3', 'BEAT_FINALE', 'BEAT_IMAGE', 'BEAT_TURN', 'INT', 'EXT', 'INT_EXT', 'DAY', 'NIGHT', 'DUSK', 'DAWN', 'MORNING', 'NOON', 'AFTERNOON', 'EVENING', 'MIDNIGHT', 'LATER', 'CONTINUOUS', 'SAME', 'CUT_TO', 'SMASH_CUT', 'DISSOLVE_TO', 'FADE_IN', 'FADE_OUT', 'FADE_BLACK', 'MATCH_CUT', 'JUMP_CUT', 'CROSS_CUT', 'PARALLEL', 'INTERCUT_WITH', 'CLOSE_UP', 'EXTREME_CU', 'WIDE', 'EXTREME_WIDE', 'MEDIUM', 'TIGHT', 'OVER_SHOULDER', 'POV', 'REVERSE', 'PUSH_IN', 'PULL_OUT', 'PAN', 'TILT', 'MONTAGE', 'FLASHBACK', 'FLASHFORWARD', 'VOICE_OVER', 'NARRATION', 'CONFLICT', 'OBSTACLE', 'MOTIF', 'PAYOFF', 'SETUP', 'PLANT', 'REVEAL', 'TWIST', 'GOAL', 'WANT', 'NEED', 'ARC', 'STAKES', 'TENSION', 'RELEASE', 'CLIMAX', 'INCITING', 'CATALYST', 'CRISIS', 'RESOLUTION', 'DENOUEMENT', 'EPILOGUE', 'PROTAGONIST', 'ANTAGONIST', 'ALLY', 'MENTOR', 'THRESHOLD', 'ORDEAL', 'ACTION', 'COMEDY', 'DRAMA', 'HORROR', 'THRILLER', 'ROMANCE', 'SCIFI', 'FANTASY', 'WESTERN', 'MYSTERY', 'CRIME', 'WAR', 'BIOPIC', 'DOCUMENTARY']
ENTITY_PREFIXES = ['PERSONA', 'CHARACTER', 'ACTOR', 'LOCAL', 'LOCATION', 'SET', 'OBJ', 'PROP', 'ITEM', 'MOTIF', 'SYMBOL', 'THEME', 'EVENT', 'ACTION', 'BEAT', 'TIME', 'WHEN', 'TEMPORAL']
SEED_MWES = ['CUT TO:', 'SMASH CUT:', 'DISSOLVE TO:', 'FADE IN:', 'FADE OUT:', 'FADE BLACK:', 'INT.', 'EXT.', 'INT/EXT.', 'VOICE OVER', 'V.O.', 'INTERCUT', 'INTERCUT WITH:', 'CLOSE UP', 'EXTREME CLOSE UP', 'WIDE SHOT', 'EXTREME WIDE SHOT', 'ESTABLISHING SHOT', 'MEDIUM SHOT', 'TIGHT SHOT', 'OVER THE SHOULDER', 'POINT OF VIEW', 'REVERSE ANGLE', 'PUSH IN', 'PULL OUT', 'FLASHBACK', 'FLASHFORWARD', 'MONTAGE', 'TIME CUT', 'MATCH CUT', 'JUMP CUT', 'LATER', 'CONTINUOUS', 'SAME TIME', 'MEANWHILE', 'SIMULTANEOUSLY', 'ENTER', 'EXIT', 'EXEUNT', 'ASIDE', 'SOLILOQUY', 'STAGE DIRECTIONS', 'SCENE', 'ACT', 'PROLOGUE', 'EPILOGUE', 'CHORUS', 'MY LORD', 'MY LADY', 'WHAT SAY YOU', 'I PRAY THEE', 'THOU ART', 'HATH NOT', 'DOTH NOT', 'WILL NOT', 'SHALL NOT', 'CANNOT', 'GOOD MORROW', 'GOOD NIGHT', 'FAREWELL', 'WHAT HO', 'MARRY', 'IN SOOTH', 'FORSOOTH', 'MAYHAP', 'PERCHANCE', 'METHINKS', 'ROOM IN THE CASTLE', 'ENTER THE KING', 'ENTER HAMLET', 'EXIT GHOST', 'FIRST WITCH', 'SECOND WITCH', 'THIRD WITCH', 'ALL WITCHES', 'MEANWHILE', 'HOWEVER', 'THEREFORE', 'NEVERTHELESS', 'FURTHERMORE', 'MOREOVER', 'CONSEQUENTLY', 'SUBSEQUENTLY', 'INITIALLY', 'FINALLY', 'SUDDENLY', 'IMMEDIATELY', 'EVENTUALLY', 'SIMULTANEOUSLY', 'AFTERWARDS']

def load_corpus_texts(corpus_dir: Path) -> List[str]:
    texts = []
    for p in corpus_dir.rglob('*.txt'):
        if p.stat().st_size > 0:
            try:
                texts.append(p.read_text(encoding='utf-8', errors='ignore'))
            except Exception:
                pass
    return texts

def mine_mwes(texts: List[str], topk: int=600) -> List[str]:
    """Mine multi-word expressions with smart filtering and scoring."""
    import tiktoken
    enc = tiktoken.get_encoding('cl100k_base')

    def norm(s: str) -> str:
        s = re.sub('\\s+', ' ', s.strip())
        return s

    def token_savings(phrase: str) -> float:
        """Calculate potential token savings for this phrase."""
        original_tokens = len(enc.encode(phrase))
        return max(0, original_tokens - 1)
    counts = Counter()
    savings_map = {}
    for t in texts:
        words = re.findall("[A-Z][A-Z\\s]*\\.?|[A-Za-z][A-Za-z\\.\\-'/]*|\\d+|[.,:;!?]", t)
        for n in range(2, 8):
            for i in range(len(words) - n + 1):
                phrase = norm(' '.join(words[i:i + n]).upper())
                if len(phrase) < 4 or len(phrase) > 60:
                    continue
                if re.match('^[^\\w\\s]+$', phrase) or re.match('^\\d+$', phrase):
                    continue
                common_words = {'THE', 'AND', 'OF', 'TO', 'A', 'IN', 'IS', 'IT', 'YOU', 'THAT'}
                phrase_words = phrase.split()
                if len(phrase_words) == 2 and all((w in common_words for w in phrase_words)):
                    continue
                counts[phrase] += 1
                if phrase not in savings_map:
                    savings_map[phrase] = token_savings(phrase)
    for m in SEED_MWES:
        key = m.upper()
        counts[key] += 50
        savings_map[key] = token_savings(m)
    scored_phrases = []
    for phrase, freq in counts.items():
        if freq >= 2:
            savings = savings_map.get(phrase, 0)
            score = freq * (savings + 1)
            scored_phrases.append((phrase, score, freq, savings))
    scored_phrases.sort(key=lambda x: x[1], reverse=True)
    seen = set()
    result = []
    for phrase, score, freq, savings in scored_phrases:
        if phrase not in seen and len(result) < topk:
            result.append(phrase)
            seen.add(phrase)
    print(f'[DEBUG] Mined {len(result)} MWEs, avg savings per phrase: {sum((savings_map[p] for p in result)) / len(result):.1f} tokens')
    return result

def pick_symbols(candidate_pool: List[str], k: int, used: set) -> List[str]:
    out = []
    for s in candidate_pool:
        if s in used:
            continue
        if s in {'|', '¦', '‖', 'l', 'I'}:
            continue
        out.append(s)
        used.add(s)
        if len(out) >= k:
            break
    return out

def choose_token_for(label: str, pool: List[str], used: set) -> str:
    sym = pick_symbols(pool, 1, used)[0]
    return sym

def build_num_alphabet(pool: List[str], used: set, k: int) -> List[str]:
    return pick_symbols(pool, k, used)

def build_vocab(corpus_dir: str, out_path: str) -> None:
    enc = tiktoken.get_encoding(ENC_NAME)
    pool = get_single_token_strings(max_candidates=8000)
    used = set()
    symbols: Dict[str, str] = {}
    for lbl in CORE_LABELS:
        symbols[lbl] = choose_token_for(lbl, pool, used)
    for i in range(BUDGETS['relation']):
        symbols[f'REL_{i:02d}'] = choose_token_for(f'REL_{i:02d}', pool, used)
    for i in range(BUDGETS['connectives']):
        symbols[f'CONN_{i:02d}'] = choose_token_for(f'CONN_{i:02d}', pool, used)
    entity_prefix = {}
    for i, lbl in enumerate(ENTITY_PREFIXES):
        entity_prefix[lbl] = choose_token_for(lbl, pool, used)
    num_alphabet = build_num_alphabet(pool, used, BUDGETS['num_alphabet'])
    texts = load_corpus_texts(Path(corpus_dir))
    mwe_list = mine_mwes(texts, topk=BUDGETS['mwe'])
    mwe_map = {}
    for phrase in mwe_list:
        sym = choose_token_for(f'MWE:{phrase}', pool, used)
        mwe_map[phrase] = sym
    vocab = Vocab(meta=VocabMeta(budgets=BUDGETS, notes='Token-aware vocabulary; every value must encode to length==1 in cl100k_base.'), symbols=symbols, entity_prefix=entity_prefix, num_alphabet=num_alphabet, mwe_map=mwe_map)
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    vocab_json = vocab.model_dump_json(indent=2)
    Path(out_path).write_text(vocab_json, encoding='utf-8')
    print(f'[OK] vocab written to {out_path} with {len(symbols)} core+rel+conn, {len(mwe_map)} MWE, num_alphabet={len(num_alphabet)}')
if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('--corpus', type=str, default='data/original')
    ap.add_argument('--out', type=str, default='src/digilang/vocab.json')
    args = ap.parse_args()
    build_vocab(args.corpus, args.out)