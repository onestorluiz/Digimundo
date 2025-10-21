from __future__ import annotations
from dataclasses import dataclass
from typing import List, Optional
from pathlib import Path
import json

from ..analysis.script_doctor import ScriptDoctor
from ..analysis.theory import TheoryComparator
from ..learning.learning_lite import LearningLite
from .ollama import OllamaReal

try:
    _HAS_OLLAMA = True
except Exception:
    _HAS_OLLAMA = False

@dataclass
class CoachPlan:
    structure: List[str]
    character: List[str]
    rhythm: List[str]
    dialogue: List[str]
    visuals: List[str]
    custom: List[str]

class DoctorCoach:
    """
    ULTIMATE COACH com robustez do hotfix ChatGPT.
    Garantir plano acionável mesmo sem Ollama nem teoria.
    Regras:
      - Sempre preencher cada seção com 2-4 itens no mínimo (heurísticos);
      - Usar métricas de análise (pacing/dialogue/avg_scene_len/beats) para priorização;
      - Se Ollama responder JSON válido, ele refina (mas nunca zera a base).
    """
    def __init__(self, genre: str = "generic", theory_dir: str = "theory",
                 ollama_model: str = "mixtral-dedicated-q5", endpoint: str = "http://127.0.0.1:11434/api/generate"):
        self.doctor = ScriptDoctor(use_learning=True, genre=genre)
        self.learning = LearningLite()
        self.theory = TheoryComparator(Path(theory_dir))
        try:
            self.theory.build()
        except Exception:
            pass

        try:
            self._ollama = OllamaReal()
            self._ollama.default_model = ollama_model
        except Exception:
            self._ollama = None

    def _fallback_items(self, sa, stc, tags) -> CoachPlan:
        """Gera plano base robusto usando heurísticas das métricas reais"""

        # --- STRUCTURE ---
        structure: List[str] = []
        if hasattr(stc, 'missing_beats') and stc.missing_beats:
            structure.append("Completar beats ausentes: " + ", ".join(stc.missing_beats[:6]))

        # Reforços por confiança baixa (se houver beats)
        if hasattr(stc, 'beats') and stc.beats:
            weak = sorted(stc.beats, key=lambda b: getattr(b, 'confidence', 0.5))[:3]
            if weak:
                structure.append("Reforçar beats com menor confiança: " + ", ".join(getattr(b, 'name', str(b)) for b in weak))

        # Sempre um cheque cruzado
        structure.append("Cruzar Save the Cat, 3 Atos e Story Circle e alinhar transições.")

        # --- CHARACTER ---
        character: List[str] = []
        if hasattr(sa, "top_characters") and sa.top_characters:
            character.append(f"Explicitar WANT/NEED do(a) protagonista {sa.top_characters[0]} em cena ativa.")
        character.append("Garantir viradas de poder claras nas cenas-chave (quem quer o quê, agora).")

        # --- RHYTHM ---
        rhythm: List[str] = []
        pacing = getattr(sa, "pacing_score", 0.0)
        if pacing < 0.3:
            rhythm.append("Variar ritmo: intercalar 1-2 cenas curtas a cada 3 longas.")

        avg_scene = getattr(sa, "avg_scene_len", 0.0)
        if avg_scene > 400:
            rhythm.append("Dividir cenas > 400 palavras em duas unidades dramáticas.")
        rhythm.append("Criar checkpoints de progressão a cada ~10% (micro-metas visíveis).")

        # --- DIALOGUE ---
        dialogue: List[str] = []
        dlg_ratio = getattr(sa, "dialogue_ratio", 0.0)
        if dlg_ratio > 0.65:
            dialogue.append("Converter exposição em ação visual ou subtexto (mostrar > dizer).")
        if dlg_ratio < 0.25:
            dialogue.append("Inserir diálogos objetivos com conflito e subtexto nas viradas.")
        dialogue.append("Aplicar 'poda de redundâncias': cortar 10-15% das falas mais literais.")

        # --- VISUALS ---
        visuals: List[str] = []
        # Extrair motivos das tags se disponível
        motifs = []
        if tags:
            for tag in tags:
                if hasattr(tag, 'key') and tag.key and tag.key.startswith('motif:'):
                    motifs.append(tag.key.split(':', 1)[1])

        if motifs:
            visuals.append("Recorrência consciente de motivos: " + ", ".join(motifs[:6]))
        visuals.append("Amarrar 'imagem final' como espelho transformado da abertura.")

        # --- CUSTOM ---
        custom: List[str] = []
        try:
            stats = self.learning.beat_stats()
            if stats and stats.get("midpoint"):
                mean_pct = stats['midpoint'].get('mean_pct', 50)
                custom.append(f"Checar midpoint ~{mean_pct:.0f}% do seu acervo: tensionar reversão/falso triunfo.")
        except Exception:
            pass

        custom.append("Criar uma cena 'prova de conceito do gênero' (promessa do filme) se ainda não existir.")

        # Garantir mínimos obrigatórios
        def ensure_min(xs: List[str], fill: List[str]):
            while len(xs) < 2 and fill:
                xs.append(fill.pop(0))

        ensure_min(structure, ["Reforçar ligação tema↔protagonista nas escolhas do Ato 2."])
        ensure_min(character, ["Apertar arco interno (lie→truth) em 2 cenas do Ato 3."])
        ensure_min(rhythm, ["Inserir escalada de stakes a cada 15-20 páginas."])
        ensure_min(dialogue, ["Marcar falas > 80 palavras para fragmentação por ação/silêncio."])
        ensure_min(visuals, ["Materializar metáforas visuais do tema (prop/locação/cor) em 3 pontos."])
        ensure_min(custom, ["Definir micro‑objetivos de reescrita para a próxima sessão (3 itens)."])

        return CoachPlan(structure, character, rhythm, dialogue, visuals, custom)

    def plan(self, text: str, screenplay_name: str = "Unknown") -> CoachPlan:
        """Gera plano de coaching robusto com fallback garantido"""
        sa = self.doctor.analyze_script(text, screenplay_name=screenplay_name)
        stc = self.doctor.analyze_save_the_cat(text)

        # Tags simulation - seria necessário implementar AutoTagger
        tags = []  # Por enquanto vazio, pode ser implementado depois

        base = self._fallback_items(sa, stc, tags)

        # Tentar refino com LLM (nunca substituir por vazio)
        if self._ollama:
            prompt = f"""Você é um Script Doctor Coach. Refine o plano abaixo, mantendo no mínimo 2 itens por seção.
Responda em JSON com chaves: structure, character, rhythm, dialogue, visuals, custom.

[PLANO-BASE]
{json.dumps(base.__dict__, ensure_ascii=False)}

[ANÁLISE]
scenes={getattr(sa,'scenes',0)}, avg_scene_len={getattr(sa,'avg_scene_len',0.0):.1f}, dialogue_ratio={getattr(sa,'dialogue_ratio',0.0):.2f}, pacing_score={getattr(sa,'pacing_score',0.0):.2f}, missing_beats={getattr(stc,'missing_beats',[])}
"""
            try:
                result = self._ollama.generate(prompt, temperature=0.4, max_tokens=600)
                if result.success and result.completion.strip().startswith("{"):
                    data = json.loads(result.completion)

                    def pick(name):
                        xs = data.get(name) or []
                        return xs if isinstance(xs, list) and xs else getattr(base, name)

                    return CoachPlan(
                        structure=pick("structure"),
                        character=pick("character"),
                        rhythm=pick("rhythm"),
                        dialogue=pick("dialogue"),
                        visuals=pick("visuals"),
                        custom=pick("custom")
                    )
            except Exception:
                pass

        return base

    def apply_light_rewrites(self, text: str) -> str:
        """Aplica reescritas leves para melhorar o texto"""
        import re

        # Limpar espaços extra
        t = re.sub(r"[ \t]+", " ", text)

        # Marcar diálogos longos para fragmentação
        def mark_long_dialogue(m):
            block = m.group(0)
            body = m.group(1)
            word_count = len(body.split())

            if word_count > 80:
                return block + "\n[COACH] Sugerir cortar/fragmentar este diálogo."
            return block

        t = re.sub(r"^[A-Z][A-Z0-9\- ]+\n(.+?)(?=\n[A-Z]|\n\n|\Z)",
                   mark_long_dialogue, t, flags=re.M|re.S)

        return t

    def coach(self, text: str, screenplay_name: str = "Unknown", out_path: Optional[str] = None):
        """Executa coaching completo: análise + plano + reescrita leve"""
        plan = self.plan(text, screenplay_name)
        rewritten = self.apply_light_rewrites(text)

        if out_path:
            Path(out_path).parent.mkdir(parents=True, exist_ok=True)
            Path(out_path).write_text(rewritten, encoding="utf-8")

        return plan, (rewritten if out_path else None)