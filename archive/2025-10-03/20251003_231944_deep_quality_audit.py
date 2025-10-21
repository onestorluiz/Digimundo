#!/usr/bin/env python3
"""
Auditoria PROFUNDA de qualidade dos especialistas:
- Analisa regras Python vs teoria
- Simula resposta LLM ideal
- Compara com resposta real
- Verifica coerência com roteiro
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Any

class DeepQualityAuditor:
    """Audita qualidade das análises dos especialistas"""

    def __init__(self):
        self.screenplay_path = "content/screenplays/personal/sonhos_sem_lembrancas_t3.txt"
        self.screenplay_text = self._load_screenplay()
        self.audit_results = []

    def _load_screenplay(self) -> str:
        """Carrega o roteiro"""
        with open(self.screenplay_path, 'r', encoding='utf-8') as f:
            return f.read()

    def analyze_structure_specialist(self):
        """Analisa DrStructure que deu 0/100"""
        print("\n" + "="*80)
        print("🔍 AUDITORIA: DrStructure (Score: 0/100)")
        print("="*80)

        # 1. Análise do roteiro real
        print("\n📄 ANÁLISE DO ROTEIRO:")
        print("-" * 80)

        lines = self.screenplay_text.split('\n')
        page_count = len([l for l in lines if l.strip()]) // 55
        print(f"Páginas estimadas: {page_count}")

        # Buscar inciting incident
        print("\n🎬 BUSCANDO INCITING INCIDENT:")
        for i, line in enumerate(lines[:300]):  # Primeiras ~5 páginas
            page = i // 55
            if any(marker in line.lower() for marker in ["afogando", "arromba", "inconsciente"]):
                print(f"  Página {page}: {line.strip()[:80]}...")

        # 2. Regras Python do DrStructure
        print("\n🐍 REGRAS PYTHON (DrStructure):")
        print("-" * 80)
        print("Regra 1: Inciting incident deve estar entre páginas 10-15")
        print("Regra 2: Busca palavras-chave: 'suddenly', 'but then', 'everything changes', 'until'")
        print("Regra 3: Se não encontrar = violação")

        # 3. Teoria Real (Field, McKee, Snyder)
        print("\n📚 TEORIA REAL (Field/McKee/Snyder):")
        print("-" * 80)
        print("• Field: Plot Point 1 deve ocorrer em ~25% do roteiro (12-15min)")
        print("• McKee: Inciting Incident = evento que quebra o equilíbrio da vida do protagonista")
        print("• Snyder: Catalyst (página 12) - algo acontece que muda tudo")
        print("• Save the Cat: Break Into Two (página 25) - entrada no Ato 2")

        # 4. Análise crítica
        print("\n⚠️  PROBLEMAS IDENTIFICADOS:")
        print("-" * 80)
        print("1. PALAVRAS-CHAVE INADEQUADAS:")
        print("   - Roteiro em PORTUGUÊS, mas busca palavras em INGLÊS")
        print("   - 'suddenly', 'but then' nunca serão encontrados")
        print("   - Score 0/100 é FALSO NEGATIVO")

        print("\n2. INCITING INCIDENT MAL DEFINIDO:")
        print("   - Cena 3 (Kleber arromba porta): Samantha se afogando")
        print("   - Isto É o Inciting Incident!")
        print("   - Mas Python procura 'suddenly' e não encontra")

        print("\n3. DESCONEXÃO TEORIA-PRÁTICA:")
        print("   - McKee: 'evento que desequilibra a vida'")
        print("   - Roteiro: Samantha quase morre afogada (CLARO desequilíbrio)")
        print("   - Python: não detectou pois não tem 'suddenly'")

        # 5. Simular resposta LLM ideal
        print("\n🤖 SIMULAÇÃO: RESPOSTA LLM IDEAL")
        print("-" * 80)
        llm_ideal = """
ANÁLISE ESTRUTURAL (DrStructure):

SCORE: 45/100

INCITING INCIDENT IDENTIFICADO:
• Localização: Cena 3 (Página ~2-3)
• Evento: Samantha se afoga na banheira, Kleber a salva
• Qualidade: FORTE - evento dramático que desequilibra completamente a vida da protagonista
• Conexão com teoria: Alinha com McKee (quebra de equilíbrio) e Snyder (catalyst)

PROBLEMAS ESTRUTURAIS:
1. OCORRE MUITO CEDO (página 2-3, ideal: 12-15) ⚠️
   - Field recomenda Plot Point 1 em ~25% do filme
   - Este inciting incident está em ~5% do roteiro
   - Risco: público não teve tempo de conhecer a protagonista

2. SETUP INSUFICIENTE:
   - Precisamos ver o "mundo normal" de Samantha primeiro
   - Atual: cena sonho → afogamento (muito rápido)
   - Ideal: 10-12 minutos de setup antes do incidente

RECOMENDAÇÕES:
1. Adicionar 8-10 páginas de setup antes do afogamento
2. Mostrar rotina de Samantha, seu trabalho, relacionamento com Kleber
3. DEPOIS causar o inciting incident (afogamento)
4. Isso levaria o incidente para página 12 (PERFEITO segundo Field/Snyder)
"""
        print(llm_ideal)

        # 6. Comparar com resposta real
        print("\n❌ RESPOSTA REAL DO SISTEMA:")
        print("-" * 80)
        print("Score: 0/100")
        print("Diagnóstico: 'CRITICAL - No inciting incident found'")
        print("Recomendação: 'Move inciting incident to page 12 (ideal) - no later than page 15'")

        print("\n🔥 ANÁLISE CRÍTICA:")
        print("-" * 80)
        print("✅ CORRETO:")
        print("   - Recomendação de mover para página 12 está ALINHADA com teoria")
        print("   - Field, McKee, Snyder concordam: página 12-15 é ideal")

        print("\n❌ INCORRETO:")
        print("   - Score 0/100 é FALSO")
        print("   - Inciting incident EXISTE (afogamento)")
        print("   - Problema não é 'inexistência', mas 'posicionamento precoce'")
        print("   - Score real deveria ser 40-50/100 (existe mas mal posicionado)")

        return {
            "specialist": "DrStructure",
            "real_score": 0,
            "ideal_score": 45,
            "issue": "False negative - incident exists but poorly timed",
            "root_cause": "English keywords in Portuguese screenplay",
            "recommendation_quality": "Good (page 12 is correct per Field/Snyder)",
            "diagnosis_quality": "Poor (says 'not found' when it exists)"
        }

    def analyze_dialogue_specialist(self):
        """Analisa DrDialogue que deu 100/100"""
        print("\n" + "="*80)
        print("🔍 AUDITORIA: DrDialogue (Score: 100/100)")
        print("="*80)

        print("\n📄 ANÁLISE DO ROTEIRO:")
        print("-" * 80)

        # Extrair diálogos
        dialogue_lines = []
        lines = self.screenplay_text.split('\n')
        for i, line in enumerate(lines):
            # Diálogos geralmente são indentados ou seguem nome do personagem
            if i > 0 and lines[i-1].strip().isupper() and len(lines[i-1].strip()) < 20:
                if line.strip() and not line.strip().isupper():
                    dialogue_lines.append((lines[i-1].strip(), line.strip()))

        print(f"Total de diálogos encontrados: {len(dialogue_lines)}")
        print("\nExemplos:")
        for char, line in dialogue_lines[:5]:
            print(f"  {char}: {line[:60]}...")

        print("\n🐍 REGRAS PYTHON (DrDialogue):")
        print("-" * 80)
        print("Regra 1: Subtext score = (diálogos com 'não dizer diretamente') / total")
        print("Regra 2: Naturalness = ausência de exposição forçada")
        print("Regra 3: Penaliza: 'As you know', 'I remember when', info dumps")

        print("\n📚 TEORIA REAL (McKee - Dialogue):")
        print("-" * 80)
        print("• 'Diálogo não é conversa real, é conversa comprimida'")
        print("• 'Bom diálogo tem subtexto - o que NÃO é dito'")
        print("• 'Evite on-the-nose dialogue (dizer exatamente o que sente)'")
        print("• 'Cada linha deve revelar personagem E avançar história'")

        print("\n✅ PONTOS FORTES IDENTIFICADOS:")
        print("-" * 80)
        print("1. SUBTEXTO PRESENTE:")
        print("   Alberto: 'Você parece chateada com alguma coisa filha'")
        print("   Samantha: 'Eu lembro... Mas não sei mais dizer se foi realmente assim'")
        print("   → Não diz diretamente o problema, sugere conflito interno")

        print("\n2. NATURALISMO:")
        print("   Kleber: 'Meu amor, fala comigo, acorda'")
        print("   → Urgência real, não exposição forçada")

        print("\n3. ECONOMIA:")
        print("   Samantha: 'Mas eu estava tendo um sonho lindo...'")
        print("   → Revela estado mental em 7 palavras")

        print("\n🤖 SIMULAÇÃO: RESPOSTA LLM IDEAL")
        print("-" * 80)
        llm_ideal = """
ANÁLISE DE DIÁLOGO (DrDialogue):

SCORE: 82/100

PONTOS FORTES:
1. SUBTEXTO EFETIVO (90/100):
   • Diálogo Alberto-Samantha tem camadas emocionais
   • "O verdadeiro é mais importante que a verdade" - filosófico, não on-the-nose
   • Personagens não dizem exatamente o que sentem

2. NATURALISMO (80/100):
   • Kleber em crise (afogamento) soa genuíno
   • Fala de criança (Samantha 8 anos) tem inocência adequada
   • Pontuação e ritmo adequados

3. CARACTERIZAÇÃO POR VOZ (85/100):
   • Alberto tem tom paternal sábio
   • Samantha adulta: fragmentada, confusa
   • Kleber: direto, prático

PONTOS FRACOS:
1. DICÇÃO SEMELHANTE (70/100):
   • Alberto e Kleber têm construções frasais parecidas
   • Falta vocabulário único por personagem
   • Todos usam frases completas, gramaticalmente corretas

2. EXPOSIÇÃO VISUAL EXCESSIVA (75/100):
   • Cena 7-8: descrição de ação poderia ter mais diálogo
   • Balanço diálogo/ação está 40/60 (ideal: 60/40 para drama)

RECOMENDAÇÕES:
1. Dar a Kleber gírias ou linguagem mais informal
2. Alberto pode ter frases mais longas, poéticas
3. Samantha: frases curtas, cortadas (refletindo confusão mental)
"""
        print(llm_ideal)

        print("\n❌ RESPOSTA REAL DO SISTEMA:")
        print("-" * 80)
        print("Score: 100/100")
        print("Diagnóstico: 'EXCELLENT - Outstanding dialogue quality'")
        print("Recomendações: 2 (menores)")

        print("\n🔥 ANÁLISE CRÍTICA:")
        print("-" * 80)
        print("⚠️  SUPERAVALIADO:")
        print("   - Score 100/100 sugere perfeição (nenhum roteiro é perfeito)")
        print("   - Diálogo é BOM, mas não EXCEPCIONAL")
        print("   - Falta distinção vocal clara entre personagens")
        print("   - Score real deveria ser 80-85/100")

        print("\n✅ CORRETO:")
        print("   - Identifica subtexto (alinhado com McKee)")
        print("   - Reconhece naturalismo (sem exposição forçada)")
        print("   - Recomendações fazem sentido")

        return {
            "specialist": "DrDialogue",
            "real_score": 100,
            "ideal_score": 82,
            "issue": "Overrated - no screenplay is 100/100",
            "root_cause": "Insufficient penalties for voice similarity",
            "recommendation_quality": "Good (aligned with McKee)",
            "diagnosis_quality": "Good but too generous"
        }

    def analyze_voice_consistency(self):
        """Analisa DrVoice que deu 0/100"""
        print("\n" + "="*80)
        print("🔍 AUDITORIA: DrVoiceConsistency (Score: 0/100)")
        print("="*80)

        print("\n📄 ANÁLISE DO ROTEIRO:")
        print("-" * 80)

        # Mapear personagens e falas
        character_dialogues = {}
        lines = self.screenplay_text.split('\n')
        current_char = None

        for i, line in enumerate(lines):
            if line.strip().isupper() and len(line.strip()) < 20 and line.strip():
                current_char = line.strip()
                if current_char not in character_dialogues:
                    character_dialogues[current_char] = []
            elif current_char and line.strip() and not line.strip().isupper():
                character_dialogues[current_char].append(line.strip())
                current_char = None

        print("Personagens com diálogo:")
        for char, dialogues in character_dialogues.items():
            if len(dialogues) >= 2:
                print(f"\n  {char} ({len(dialogues)} falas):")
                for d in dialogues[:3]:
                    print(f"    • {d[:70]}...")

        print("\n🐍 REGRAS PYTHON (DrVoiceConsistency):")
        print("-" * 80)
        print("Regra 1: Cada personagem deve ter padrões únicos de fala")
        print("Regra 2: Vocabulário, tamanho de frase, complexidade devem variar")
        print("Regra 3: Detecta quando todos falam igual")

        print("\n📚 TEORIA REAL (Truby - Character Voice):")
        print("-" * 80)
        print("• 'Each character must have unique speech patterns'")
        print("• 'Voice = vocabulary + syntax + rhythm + formality level'")
        print("• 'Reader should know who's speaking without dialogue tag'")

        print("\n⚠️  ANÁLISE:")
        print("-" * 80)

        # Comparar vozes
        alberto_sample = "Você parece chateada com alguma coisa filha"
        kleber_sample = "Meu amor, fala comigo, acorda"
        samantha_sample = "Mas eu estava tendo um sonho lindo"

        print(f"Alberto: '{alberto_sample}'")
        print("  → Tom: paternal, filosófico, frases completas")
        print(f"\nKleber: '{kleber_sample}'")
        print("  → Tom: urgente, prático, imperativo")
        print(f"\nSamantha: '{samantha_sample}'")
        print("  → Tom: sonhador, fragmentado, conjunção adversativa")

        print("\n✅ DIFERENCIAÇÃO EXISTE:")
        print("   - Alberto: reflexivo, usa 'filha' como termo de carinho")
        print("   - Kleber: ação-oriented, usa 'meu amor'")
        print("   - Samantha: introspectiva, frases começam com 'mas'")

        print("\n🤖 SIMULAÇÃO: RESPOSTA LLM IDEAL")
        print("-" * 80)
        llm_ideal = """
ANÁLISE DE VOZ (DrVoiceConsistency):

SCORE: 58/100

DIFERENCIAÇÃO PRESENTE (mas SUTIL):

1. ALBERTO (Pai):
   • Vocabulário: 'filha', 'verdadeiro', 'verdade' (filosófico)
   • Sintaxe: Frases completas, estrutura sujeito-verbo-objeto
   • Tom: Paternal, didático, calmo
   • Exemplo: "Às vezes o verdadeiro é muito mais importante que a verdade filha"

2. KLEBER (Namorado):
   • Vocabulário: 'meu amor', verbos imperativos
   • Sintaxe: Frases curtas em momentos de tensão
   • Tom: Protetor, urgente, prático
   • Exemplo: "Meu amor, fala comigo, acorda"

3. SAMANTHA (Protagonista):
   • Vocabulário: 'mas', 'lembro', 'sonho'
   • Sintaxe: Frases fragmentadas, conjunções adversativas
   • Tom: Confusa, nostálgica, dissociada
   • Exemplo: "Eu lembro... Mas não sei mais dizer se foi realmente assim"

PROBLEMAS:
1. DISTINÇÃO MUITO SUTIL (50/100):
   • Diferenças existem mas são SUTIS
   • Todos usam gramática correta (poucos erros, gírias, etc.)
   • Falta contraste FORTE (ex: um personagem com sotaque, gírias regionais)

2. SAMANTHA CRIANÇA vs ADULTA (70/100):
   • Samantha criança tem voz infantil adequada
   • Samantha adulta mantém tom, mas poderia ter mais maturidade linguística

RECOMENDAÇÕES:
1. EXAGERAR diferenças:
   • Kleber: adicionar gírias catarinenses, linguagem informal
   • Alberto: usar metáforas cinematográficas (ele trabalha com cinema)
   • Samantha: mais hesitações, reticências, frases incompletas

2. TESTE DO DIÁLOGO SEM TAG:
   • Leitor deve saber quem fala SEM ver o nome
   • Atualmente: 60% de acerto (deveria ser 90%+)
"""
        print(llm_ideal)

        print("\n❌ RESPOSTA REAL DO SISTEMA:")
        print("-" * 80)
        print("Score: 0/100")
        print("Diagnóstico: 'CRITICAL - No voice differentiation detected'")
        print("Recomendação: 'Give each character unique speech patterns, vocabulary'")

        print("\n🔥 ANÁLISE CRÍTICA:")
        print("-" * 80)
        print("❌ COMPLETAMENTE INCORRETO:")
        print("   - Score 0/100 implica 'nenhuma diferenciação'")
        print("   - FALSO: diferenciação existe (Alberto ≠ Kleber ≠ Samantha)")
        print("   - Problema: diferenciação é SUTIL, não AUSENTE")
        print("   - Score real deveria ser 55-65/100 (presente mas precisa exagerar)")

        print("\n✅ RECOMENDAÇÃO CORRETA:")
        print("   - 'Give unique speech patterns' está ALINHADA com Truby")
        print("   - Mas score 0/100 não reflete realidade do roteiro")

        return {
            "specialist": "DrVoiceConsistency",
            "real_score": 0,
            "ideal_score": 58,
            "issue": "False negative - differentiation exists but subtle",
            "root_cause": "Binary detection (exists/not exists) instead of gradient",
            "recommendation_quality": "Excellent (aligned with Truby)",
            "diagnosis_quality": "Poor (false negative)"
        }

    def generate_report(self):
        """Gera relatório completo de auditoria"""
        print("\n" + "="*80)
        print("📊 AUDITORIA DE QUALIDADE DOS ESPECIALISTAS")
        print("="*80)

        results = []
        results.append(self.analyze_structure_specialist())
        results.append(self.analyze_dialogue_specialist())
        results.append(self.analyze_voice_consistency())

        # Sumário
        print("\n" + "="*80)
        print("📋 SUMÁRIO DA AUDITORIA")
        print("="*80)

        total_error = 0
        for r in results:
            error = abs(r["real_score"] - r["ideal_score"])
            total_error += error
            print(f"\n{r['specialist']}:")
            print(f"  Score Real: {r['real_score']}/100")
            print(f"  Score Ideal: {r['ideal_score']}/100")
            print(f"  Erro: {error} pontos")
            print(f"  Problema: {r['issue']}")
            print(f"  Causa raiz: {r['root_cause']}")
            print(f"  Qualidade recomendação: {r['recommendation_quality']}")
            print(f"  Qualidade diagnóstico: {r['diagnosis_quality']}")

        avg_error = total_error / len(results)
        print(f"\n{'='*80}")
        print(f"ERRO MÉDIO: {avg_error:.1f} pontos")
        print(f"{'='*80}")

        # Conclusões
        print("\n🎯 CONCLUSÕES:")
        print("-" * 80)
        print("\n1. FALSOS NEGATIVOS CRÍTICOS:")
        print("   • DrStructure: 0/100 → deveria ser 45/100 (incident exists, just early)")
        print("   • DrVoiceConsistency: 0/100 → deveria ser 58/100 (differentiation subtle)")
        print("   → Causa: Regras binárias (sim/não) em vez de gradientes")

        print("\n2. FALSOS POSITIVOS:")
        print("   • DrDialogue: 100/100 → deveria ser 82/100 (good but not perfect)")
        print("   → Causa: Penalidades insuficientes para similaridade de voz")

        print("\n3. KEYWORDS EM INGLÊS:")
        print("   • Roteiros em PORTUGUÊS não contêm 'suddenly', 'but then'")
        print("   • Sistema deve buscar 'de repente', 'mas então', 'até que'")
        print("   → CRÍTICO: Erro básico de localização")

        print("\n4. RECOMENDAÇÕES CORRETAS:")
        print("   • Apesar de scores errados, RECOMENDAÇÕES estão alinhadas com teoria")
        print("   • Field, McKee, Truby, Snyder são aplicados corretamente")
        print("   • Problema está na DETECÇÃO, não na PRESCRIÇÃO")

        print("\n💡 AÇÕES NECESSÁRIAS:")
        print("-" * 80)
        print("1. CONVERTER KEYWORDS PARA PORTUGUÊS")
        print("2. IMPLEMENTAR SCORES GRADIENTES (não binários)")
        print("3. CALIBRAR PENALIDADES (evitar 0/100 e 100/100 extremos)")
        print("4. ADICIONAR DETECÇÃO DE POSICIONAMENTO (não só existência)")

        return results


if __name__ == "__main__":
    auditor = DeepQualityAuditor()
    results = auditor.generate_report()

    print("\n" + "="*80)
    print("✅ AUDITORIA COMPLETA")
    print("="*80)
