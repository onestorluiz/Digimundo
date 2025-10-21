#!/usr/bin/env python3
"""
Análise Crítica com Ollama Mistral como Segunda Opinião
Combina análise estrutural com opinião do LLM
"""

import sys
import json
import time
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
from dataclasses import dataclass
import requests

sys.path.insert(0, 'src')

from scripturemon_champion.analysis.script_doctor import ScriptDoctor
from scripturemon_champion.learning.learning_pro import Learning
from scripturemon_champion.analysis.autotag import AutoTagger

@dataclass
class OllamaOpinion:
    """Opinião do Ollama sobre o roteiro"""
    score: int  # 0-100
    category: str  # universal_good, good_with_notes, needs_work, experimental
    main_issues: List[str]
    main_strengths: List[str]
    recommendation: str

class CriticalAnalysisWithOllama:
    """Análise crítica combinando métricas estruturais e opinião do Mistral"""

    def __init__(self):
        self.doctor = ScriptDoctor(use_learning=True)
        self.learning = Learning()
        self.tagger = AutoTagger()
        self.ollama_endpoint = "http://127.0.0.1:11434/api/generate"
        self.model = "mistral:latest"  # Mistral como padrão

    def get_ollama_opinion(self, text: str, analysis, stc, screenplay_name: str) -> Optional[OllamaOpinion]:
        """Obtém opinião crítica do Ollama Mistral"""

        # Preparar contexto resumido
        context = f"""
Roteiro: {screenplay_name}
Cenas: {analysis.scenes}
Beats detectados: {len(stc.beats)}/15
Beats faltando: {', '.join(stc.missing_beats[:5]) if stc.missing_beats else 'Nenhum'}
Personagens principais: {', '.join(analysis.top_characters[:3]) if analysis.top_characters else 'Não identificados'}
Proporção diálogo: {analysis.dialogue_ratio:.1%}
Ritmo (pacing): {analysis.pacing_score:.2f}
Tamanho médio de cena: {analysis.avg_scene_len:.0f} palavras
"""

        # Incluir trecho do início para contexto
        excerpt = text[:2000] if len(text) > 2000 else text

        prompt = f"""Você é um crítico de roteiros RIGOROSO e HONESTO. Analise este roteiro com critérios profissionais severos.

{context}

INÍCIO DO ROTEIRO:
{excerpt}

Responda em JSON com EXATAMENTE este formato:
{{
  "score": [0-100, seja rigoroso, a maioria dos roteiros deve ficar entre 30-70],
  "category": ["universal_good" apenas se score > 85, "good_with_notes" se 60-85, "needs_work" se 30-60, "experimental" se < 30],
  "main_issues": [liste 3-5 problemas REAIS e ESPECÍFICOS, não genéricos],
  "main_strengths": [liste 1-3 pontos positivos REAIS se houver],
  "recommendation": "[uma recomendação principal clara e específica]"
}}

IMPORTANTE:
- Seja EXTREMAMENTE crítico e honesto
- NÃO seja gentil ou positivo sem motivo
- A maioria dos roteiros tem problemas sérios
- "universal_good" é MUITO raro (menos de 10% dos casos)
- Identifique problemas ESPECÍFICOS, não genéricos
- Se o roteiro tem problemas estruturais graves, o score deve ser baixo
- Beats faltando é problema GRAVE
- Personagens mal definidos é problema GRAVE
- Ritmo ruim é problema GRAVE

Responda APENAS com o JSON, sem texto adicional."""

        try:
            # Chamar Ollama
            response = requests.post(
                self.ollama_endpoint,
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "temperature": 0.3,  # Baixa temperatura para consistência
                    "top_p": 0.9
                },
                timeout=30
            )

            if response.status_code == 200:
                result = response.json()
                completion = result.get("response", "")

                # Tentar extrair JSON
                if "{" in completion and "}" in completion:
                    start = completion.find("{")
                    end = completion.rfind("}") + 1
                    json_str = completion[start:end]

                    data = json.loads(json_str)

                    return OllamaOpinion(
                        score=min(100, max(0, data.get("score", 50))),
                        category=data.get("category", "needs_work"),
                        main_issues=data.get("main_issues", []),
                        main_strengths=data.get("main_strengths", []),
                        recommendation=data.get("recommendation", "Revisar estrutura narrativa")
                    )

        except Exception as e:
            print(f"⚠️ Erro consultando Ollama: {e}")

        return None

    def analyze_screenplay_with_ollama(self, screenplay_path: Path) -> Dict:
        """Análise combinada: métricas estruturais + opinião Ollama"""

        try:
            text = screenplay_path.read_text(encoding='utf-8', errors='ignore')
            name = screenplay_path.stem

            print(f"\n📖 Analisando: {name}")

            # Análise estrutural
            analysis = self.doctor.analyze_script(text, name)
            stc = self.doctor.analyze_save_the_cat(text)

            # Métricas base
            structural_score = (len(stc.beats) / 15) * 40  # 40 pontos máximo
            character_score = 20 if 2 <= len(analysis.top_characters) <= 10 else 10
            dialogue_score = 20 if 0.2 <= analysis.dialogue_ratio <= 0.45 else 10
            pacing_score = analysis.pacing_score * 20

            base_score = structural_score + character_score + dialogue_score + pacing_score

            print(f"  📊 Score base (métricas): {base_score:.0f}/100")

            # Obter opinião do Ollama
            ollama_opinion = self.get_ollama_opinion(text, analysis, stc, name)

            if ollama_opinion:
                print(f"  🤖 Score Mistral: {ollama_opinion.score}/100")

                # Média ponderada: 60% métricas, 40% Ollama
                final_score = (base_score * 0.6) + (ollama_opinion.score * 0.4)

                # Categoria final baseada em ambos
                if final_score >= 85 and ollama_opinion.category == "universal_good":
                    final_category = "universal_good"
                elif final_score >= 65:
                    final_category = "good_with_notes"
                elif final_score >= 45:
                    final_category = "needs_work"
                else:
                    final_category = "experimental"

                # Combinar issues
                all_issues = []

                # Issues estruturais
                if len(stc.beats) < 10:
                    all_issues.append(f"❌ Apenas {len(stc.beats)}/15 beats estruturais")
                if analysis.dialogue_ratio < 0.2:
                    all_issues.append("❌ Diálogo insuficiente")
                elif analysis.dialogue_ratio > 0.5:
                    all_issues.append("⚠️ Diálogo excessivo")
                if analysis.pacing_score < 0.5:
                    all_issues.append("❌ Problemas de ritmo")

                # Issues do Ollama
                all_issues.extend(ollama_opinion.main_issues)

                # Combinar strengths
                all_strengths = []
                if len(stc.beats) >= 12:
                    all_strengths.append("✅ Estrutura bem definida")
                if 0.25 <= analysis.dialogue_ratio <= 0.4:
                    all_strengths.append("✅ Bom balanço diálogo/ação")

                all_strengths.extend(ollama_opinion.main_strengths)

            else:
                # Fallback se Ollama não responder
                print("  ⚠️ Ollama não disponível, usando apenas métricas")
                final_score = base_score
                final_category = self._categorize_by_score(base_score)

                all_issues = []
                if len(stc.beats) < 10:
                    all_issues.append(f"❌ Apenas {len(stc.beats)}/15 beats")
                if analysis.dialogue_ratio < 0.2 or analysis.dialogue_ratio > 0.5:
                    all_issues.append("⚠️ Proporção de diálogo inadequada")

                all_strengths = []
                if len(stc.beats) >= 12:
                    all_strengths.append("✅ Boa estrutura")

            # Resultado final
            result = {
                'screenplay': name,
                'final_score': final_score,
                'base_score': base_score,
                'ollama_score': ollama_opinion.score if ollama_opinion else None,
                'category': final_category,
                'issues': all_issues[:5],  # Top 5 issues
                'strengths': all_strengths[:3],  # Top 3 strengths
                'recommendation': ollama_opinion.recommendation if ollama_opinion else "Revisar estrutura narrativa",
                'metrics': {
                    'scenes': analysis.scenes,
                    'beats': len(stc.beats),
                    'missing_beats': len(stc.missing_beats),
                    'dialogue_ratio': analysis.dialogue_ratio,
                    'pacing': analysis.pacing_score,
                    'characters': len(analysis.top_characters)
                }
            }

            # Mostrar resultado
            print(f"  🎯 Score final: {final_score:.0f}/100")
            print(f"  🏷️ Categoria: {final_category}")

            if all_issues:
                print("  🚨 Principais problemas:")
                for issue in all_issues[:3]:
                    print(f"    {issue}")

            return result

        except Exception as e:
            print(f"❌ Erro analisando {screenplay_path}: {e}")
            return None

    def _categorize_by_score(self, score: float) -> str:
        """Categorização fallback baseada em score"""
        if score >= 85:
            return "universal_good"
        elif score >= 65:
            return "good_with_notes"
        elif score >= 45:
            return "needs_work"
        else:
            return "experimental"

    def analyze_multiple(self, screenplays: List[Path]):
        """Analisa múltiplos roteiros com Ollama"""

        print("=" * 80)
        print("🔍 ANÁLISE CRÍTICA COM OLLAMA MISTRAL")
        print("=" * 80)

        results = []

        for screenplay in screenplays:
            result = self.analyze_screenplay_with_ollama(screenplay)
            if result:
                results.append(result)
            time.sleep(1)  # Pausa entre análises

        # Relatório final
        self.print_report(results)

        return results

    def print_report(self, results: List[Dict]):
        """Imprime relatório consolidado"""

        print("\n" + "=" * 80)
        print("📊 RELATÓRIO CONSOLIDADO")
        print("=" * 80)

        # Distribuição por categoria
        categories = {}
        for r in results:
            cat = r['category']
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(r['screenplay'])

        print("\n🏷️ DISTRIBUIÇÃO:")
        for cat in ['universal_good', 'good_with_notes', 'needs_work', 'experimental']:
            scripts = categories.get(cat, [])
            if scripts:
                print(f"\n{cat.upper()}: {len(scripts)}")
                for script in scripts:
                    # Encontrar o score
                    score = next(r['final_score'] for r in results if r['screenplay'] == script)
                    print(f"  • {script} ({score:.0f}/100)")

        # Top 3 melhores
        sorted_results = sorted(results, key=lambda x: x['final_score'], reverse=True)

        print("\n🏆 TOP 3 MELHORES:")
        for r in sorted_results[:3]:
            print(f"  {r['screenplay']}: {r['final_score']:.0f}/100")

        # Bottom 3
        print("\n⚠️ PRECISAM MAIS TRABALHO:")
        for r in sorted_results[-3:]:
            print(f"  {r['screenplay']}: {r['final_score']:.0f}/100")
            if r['issues']:
                print(f"    Principal problema: {r['issues'][0]}")

        # Salvar JSON
        output = Path(f"ollama_analysis_{datetime.now().strftime('%Y%m%d_%H%M')}.json")
        with open(output, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)

        print(f"\n💾 Resultados salvos: {output}")

if __name__ == "__main__":
    # Testar com Sonhos Sem Lembranças primeiro
    analyzer = CriticalAnalysisWithOllama()

    # Verificar se Ollama está rodando
    print("🔍 Verificando Ollama...")
    try:
        response = requests.get("http://127.0.0.1:11434/api/tags", timeout=2)
        if response.status_code == 200:
            print("✅ Ollama está rodando")
            models = response.json().get("models", [])
            if any("mistral" in m.get("name", "") for m in models):
                print("✅ Mistral disponível")
            else:
                print("⚠️ Mistral não encontrado, tentando com modelo disponível")
                if models:
                    analyzer.model = models[0]["name"]
                    print(f"   Usando: {analyzer.model}")
    except:
        print("❌ Ollama não está respondendo")

    # Analisar
    my_screenplays = Path("my_screenplays")
    if my_screenplays.exists():
        files = list(my_screenplays.glob("*.txt"))[:3]  # Top 3 para teste
        if files:
            analyzer.analyze_multiple(files)
        else:
            print("❌ Nenhum arquivo .txt encontrado em my_screenplays/")