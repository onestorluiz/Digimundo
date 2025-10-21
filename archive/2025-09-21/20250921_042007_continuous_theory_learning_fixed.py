#!/usr/bin/env python3
"""
Sistema de Aprendizado Contínuo com Análise Crítica Real
Corrige o problema de falsos positivos na categorização
"""

import sys
import json
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from dataclasses import dataclass

sys.path.insert(0, 'src')

from scripturemon_champion.analysis.script_doctor import ScriptDoctor
from scripturemon_champion.learning.learning import Learning
from scripturemon_champion.analysis.coach import DoctorCoach
from scripturemon_champion.analysis.autotag import AutoTagger

@dataclass
class CriticalScore:
    """Pontuação crítica real baseada em múltiplos fatores"""
    structure: float  # 0-1
    character: float  # 0-1
    dialogue: float  # 0-1
    pacing: float  # 0-1
    theme: float  # 0-1
    total: float  # 0-100
    issues: List[str]
    strengths: List[str]

class ContinuousTheoryLearning:
    """
    Sistema de aprendizado contínuo com análise crítica honesta
    """

    def __init__(self, profile: str = "ECO"):
        self.doctor = ScriptDoctor(use_learning=True)
        self.learning = Learning()
        self.coach = DoctorCoach()
        self.tagger = AutoTagger()

        # Diretórios
        self.screenplays_dir = Path("screenplays")
        self.my_screenplays_dir = Path("my_screenplays")
        self.theory_dir = Path("theory")

        # Estatísticas
        self.stats = {
            'screenplays_analyzed': 0,
            'theories_compared': 0,
            'patterns_found': 0,
            'start_time': None,
            'categorizations': {
                'universal_good': [],
                'good_with_notes': [],
                'needs_work': [],
                'experimental': []
            }
        }

    def critical_evaluate(self, text: str, analysis, stc) -> CriticalScore:
        """Avaliação crítica real com critérios rigorosos"""

        issues = []
        strengths = []

        # 1. ESTRUTURA (30 pontos máximo)
        structure_score = 0.0

        # Beats presentes vs esperados
        beats_ratio = len(stc.beats) / 15
        if beats_ratio < 0.5:
            issues.append(f"❌ Apenas {len(stc.beats)}/15 beats detectados - estrutura incompleta")
            structure_score = beats_ratio * 0.5
        elif beats_ratio < 0.7:
            issues.append(f"⚠️ {len(stc.beats)}/15 beats - estrutura parcial")
            structure_score = beats_ratio * 0.7
        elif beats_ratio >= 0.8:
            strengths.append(f"✅ {len(stc.beats)}/15 beats bem definidos")
            structure_score = beats_ratio

        # Beats críticos específicos
        critical_beats = ['catalyst', 'midpoint', 'all is lost', 'finale']
        missing_critical = []

        beat_names = [b.name.lower() for b in stc.beats]
        for critical in critical_beats:
            if not any(critical in name for name in beat_names):
                missing_critical.append(critical)

        if missing_critical:
            issues.append(f"❌ Beats críticos ausentes: {', '.join(missing_critical)}")
            structure_score *= 0.7

        # Verificar timing dos beats (posição no script)
        if stc.beats:
            # Midpoint deve estar entre 45-55%
            for beat in stc.beats:
                if 'midpoint' in beat.name.lower():
                    if hasattr(beat, 'pct'):
                        if not (45 <= beat.pct <= 55):
                            issues.append(f"⚠️ Midpoint em {beat.pct}% - fora da posição ideal (45-55%)")
                            structure_score *= 0.9

        # 2. PERSONAGENS (20 pontos máximo)
        character_score = 0.0

        if not analysis.top_characters:
            issues.append("❌ Nenhum personagem principal identificado")
            character_score = 0.0
        elif len(analysis.top_characters) < 2:
            issues.append("⚠️ Apenas 1 personagem identificado - falta antagonista/suporte")
            character_score = 0.3
        elif len(analysis.top_characters) > 15:
            issues.append("⚠️ Muitos personagens - pode diluir foco narrativo")
            character_score = 0.5
        else:
            # Verificar protagonista claro
            if analysis.top_characters[0] != "Unknown":
                strengths.append(f"✅ Protagonista claro: {analysis.top_characters[0]}")
                character_score = 0.8
            else:
                issues.append("❌ Protagonista não claramente definido")
                character_score = 0.4

        # 3. DIÁLOGO (20 pontos máximo)
        dialogue_score = 0.0

        if analysis.dialogue_ratio < 0.15:
            issues.append(f"❌ Diálogo insuficiente ({analysis.dialogue_ratio:.1%}) - roteiro muito descritivo")
            dialogue_score = 0.3
        elif analysis.dialogue_ratio > 0.6:
            issues.append(f"⚠️ Diálogo excessivo ({analysis.dialogue_ratio:.1%}) - falta ação visual")
            dialogue_score = 0.5
        elif 0.25 <= analysis.dialogue_ratio <= 0.45:
            strengths.append(f"✅ Balanço diálogo/ação adequado ({analysis.dialogue_ratio:.1%})")
            dialogue_score = 1.0
        else:
            dialogue_score = 0.7

        # 4. RITMO (20 pontos máximo)
        pacing_score = analysis.pacing_score

        if pacing_score < 0.4:
            issues.append(f"❌ Ritmo problemático (score: {pacing_score:.2f})")
        elif pacing_score < 0.6:
            issues.append(f"⚠️ Ritmo irregular (score: {pacing_score:.2f})")
        else:
            strengths.append(f"✅ Bom ritmo narrativo (score: {pacing_score:.2f})")

        # Verificar tamanho médio de cena
        if analysis.avg_scene_len > 500:
            issues.append(f"❌ Cenas muito longas (média: {analysis.avg_scene_len:.0f} palavras)")
            pacing_score *= 0.7
        elif analysis.avg_scene_len < 100:
            issues.append(f"❌ Cenas muito curtas (média: {analysis.avg_scene_len:.0f} palavras)")
            pacing_score *= 0.7

        # 5. TEMA (10 pontos máximo)
        theme_score = 0.5  # Base neutra

        # Verificar tags temáticas
        tags = self.tagger.tag_script(text, top_k=10)
        theme_tags = [t for t in tags if t.type == 'theme']

        if not theme_tags:
            issues.append("⚠️ Tema não claramente identificado")
            theme_score = 0.3
        elif len(theme_tags) > 5:
            issues.append("⚠️ Muitos temas - pode faltar foco")
            theme_score = 0.6
        else:
            strengths.append(f"✅ Tema consistente identificado")
            theme_score = 0.9

        # CALCULAR SCORE TOTAL
        total = (
            structure_score * 30 +
            character_score * 20 +
            dialogue_score * 20 +
            pacing_score * 20 +
            theme_score * 10
        )

        return CriticalScore(
            structure=structure_score,
            character=character_score,
            dialogue=dialogue_score,
            pacing=pacing_score,
            theme=theme_score,
            total=total,
            issues=issues,
            strengths=strengths
        )

    def categorize_screenplay(self, score: CriticalScore, screenplay_name: str) -> str:
        """Categorização honesta baseada em score crítico"""

        # Critérios rigorosos
        if score.total >= 85 and len(score.issues) <= 2:
            # Excelente - estrutura sólida, poucos problemas
            return 'universal_good'
        elif score.total >= 65 and len(score.issues) <= 5:
            # Bom mas com ressalvas
            return 'good_with_notes'
        elif score.total >= 45:
            # Precisa trabalho significativo
            return 'needs_work'
        else:
            # Experimental ou problemático
            return 'experimental'

    def analyze_screenplay(self, screenplay_path: Path) -> Dict:
        """Análise completa com avaliação crítica"""

        try:
            text = screenplay_path.read_text(encoding='utf-8', errors='ignore')
            name = screenplay_path.stem

            # Análises base
            analysis = self.doctor.analyze_script(text, name)
            stc = self.doctor.analyze_save_the_cat(text)

            # Avaliação crítica
            score = self.critical_evaluate(text, analysis, stc)

            # Categorização
            category = self.categorize_screenplay(score, name)

            # Resultado
            result = {
                'screenplay': name,
                'file': str(screenplay_path),
                'category': category,
                'score': {
                    'total': score.total,
                    'structure': score.structure,
                    'character': score.character,
                    'dialogue': score.dialogue,
                    'pacing': score.pacing,
                    'theme': score.theme
                },
                'issues': score.issues,
                'strengths': score.strengths,
                'metrics': {
                    'scenes': analysis.scenes,
                    'beats_found': len(stc.beats),
                    'beats_missing': len(stc.missing_beats),
                    'dialogue_ratio': analysis.dialogue_ratio,
                    'avg_scene_len': analysis.avg_scene_len,
                    'pacing_score': analysis.pacing_score
                }
            }

            # Atualizar estatísticas
            self.stats['screenplays_analyzed'] += 1
            self.stats['categorizations'][category].append(name)

            return result

        except Exception as e:
            print(f"❌ Erro analisando {screenplay_path}: {e}")
            return None

    def run_continuous_analysis(self, iterations: int = 1):
        """Executa análise contínua com critérios rigorosos"""

        print("=" * 80)
        print("🔍 ANÁLISE CRÍTICA CONTÍNUA - CRITÉRIOS RIGOROSOS")
        print("=" * 80)

        self.stats['start_time'] = datetime.now()

        # Coletar todos os roteiros
        all_screenplays = []

        if self.screenplays_dir.exists():
            all_screenplays.extend(list(self.screenplays_dir.glob("*.txt")))

        if self.my_screenplays_dir.exists():
            all_screenplays.extend(list(self.my_screenplays_dir.glob("*.txt")))

        print(f"\n📚 Roteiros encontrados: {len(all_screenplays)}")

        results = []

        for i in range(iterations):
            print(f"\n🔄 Iteração {i+1}/{iterations}")

            for screenplay in all_screenplays:
                print(f"\n📖 Analisando: {screenplay.name}")

                result = self.analyze_screenplay(screenplay)
                if result:
                    results.append(result)

                    # Mostrar resultado
                    print(f"  📊 Score: {result['score']['total']:.0f}/100")
                    print(f"  🏷️ Categoria: {result['category']}")

                    if result['issues']:
                        print("  🚨 Problemas:")
                        for issue in result['issues'][:3]:  # Top 3 issues
                            print(f"    {issue}")

                    if result['strengths']:
                        print("  ✅ Pontos fortes:")
                        for strength in result['strengths'][:2]:  # Top 2 strengths
                            print(f"    {strength}")

                time.sleep(0.1)  # Pequena pausa entre análises

        # Relatório final
        self.print_final_report(results)

        return results

    def print_final_report(self, results: List[Dict]):
        """Imprime relatório final com estatísticas honestas"""

        elapsed = datetime.now() - self.stats['start_time']

        print("\n" + "=" * 80)
        print("📊 RELATÓRIO FINAL - ANÁLISE CRÍTICA")
        print("=" * 80)

        print(f"\n⏱️ Tempo total: {elapsed}")
        print(f"📚 Roteiros analisados: {len(results)}")

        # Distribuição por categoria
        print("\n🏷️ DISTRIBUIÇÃO POR CATEGORIA:")

        categories = {}
        for r in results:
            cat = r['category']
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(r['screenplay'])

        for cat, scripts in categories.items():
            percentage = (len(scripts) / len(results)) * 100
            print(f"\n  {cat.upper()}: {len(scripts)} ({percentage:.1f}%)")
            for script in scripts[:3]:  # Top 3 de cada categoria
                print(f"    • {script}")

        # Médias de scores
        print("\n📈 SCORES MÉDIOS:")

        avg_total = sum(r['score']['total'] for r in results) / len(results)
        avg_structure = sum(r['score']['structure'] for r in results) / len(results)
        avg_character = sum(r['score']['character'] for r in results) / len(results)
        avg_dialogue = sum(r['score']['dialogue'] for r in results) / len(results)
        avg_pacing = sum(r['score']['pacing'] for r in results) / len(results)

        print(f"  • Total: {avg_total:.1f}/100")
        print(f"  • Estrutura: {avg_structure:.1%}")
        print(f"  • Personagens: {avg_character:.1%}")
        print(f"  • Diálogo: {avg_dialogue:.1%}")
        print(f"  • Ritmo: {avg_pacing:.1%}")

        # Problemas mais comuns
        all_issues = []
        for r in results:
            all_issues.extend(r['issues'])

        if all_issues:
            print("\n⚠️ PROBLEMAS MAIS COMUNS:")
            from collections import Counter
            issue_counts = Counter(all_issues)
            for issue, count in issue_counts.most_common(5):
                print(f"  • {issue} ({count} ocorrências)")

        # Salvar resultados
        output_file = Path(f"analysis_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'results': results,
                'statistics': {
                    'total_analyzed': len(results),
                    'categories': categories,
                    'averages': {
                        'total': avg_total,
                        'structure': avg_structure,
                        'character': avg_character,
                        'dialogue': avg_dialogue,
                        'pacing': avg_pacing
                    }
                }
            }, f, ensure_ascii=False, indent=2)

        print(f"\n💾 Resultados salvos em: {output_file}")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Análise Contínua com Critérios Rigorosos")
    parser.add_argument("--profile", default="ECO", help="Perfil de aprendizado")
    parser.add_argument("--iterations", type=int, default=1, help="Número de iterações")

    args = parser.parse_args()

    system = ContinuousTheoryLearning(profile=args.profile)
    system.run_continuous_analysis(iterations=args.iterations)