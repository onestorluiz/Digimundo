#!/usr/bin/env python3
"""
Sistema de Aprendizado Contínuo e Evolutivo para Ollama
Analisa teorias → compara roteiros → evolui conhecimento → repete com insights acumulados
"""

import sys
import json
import time
from datetime import datetime
import sqlite3
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple
from datetime import datetime
from collections import defaultdict
import requests
import hashlib

sys.path.insert(0, 'src')

from scripturemon_champion.analysis.script_doctor import ScriptDoctor

class OllamaContinuousLearning:
    """
    Sistema de aprendizado contínuo que evolui a cada ciclo
    """

    def __init__(self, model: str = "mixtral-token-turbo:latest"):
        self.doctor = ScriptDoctor()
        self.model = model
        self.ollama_endpoint = "http://127.0.0.1:11434/api/generate"

        # Diretórios
        self.theory_dir = Path("theory")
        self.masters_dir = Path("screenplays/masters")  # 34 roteiros profissionais
        self.screenplays_dir = Path("screenplays")
        self.my_screenplays_dir = Path("my_screenplays")
        self.knowledge_db = Path("data/learning/ollama_knowledge.db")

        # Inicializar banco de conhecimento
        self.knowledge_db.parent.mkdir(parents=True, exist_ok=True)
        self.init_knowledge_db()

        # Estado do aprendizado
        self.cycle_count = self.get_cycle_count()
        self.accumulated_insights = []
        self.pattern_memory = defaultdict(list)

    def init_knowledge_db(self):
        """Inicializa banco de dados de conhecimento evolutivo"""

        conn = sqlite3.connect(self.knowledge_db)

        # WAL mode - mais robusto contra corrupção (do ChatGPT)
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute("PRAGMA synchronous=NORMAL;")

        cursor = conn.cursor()

        # Tabela de ciclos de aprendizado
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS learning_cycles (
                cycle_id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                phase TEXT,
                insights_count INTEGER,
                patterns_found INTEGER
            )
        """)

        # Tabela de insights acumulados
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS insights (
                insight_id INTEGER PRIMARY KEY AUTOINCREMENT,
                cycle_id INTEGER,
                type TEXT,
                content TEXT,
                confidence REAL,
                timestamp TEXT
            )
        """)

        # Tabela de padrões descobertos
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS patterns (
                pattern_id INTEGER PRIMARY KEY AUTOINCREMENT,
                pattern_type TEXT,
                description TEXT,
                occurrences INTEGER,
                examples TEXT,
                first_seen_cycle INTEGER,
                last_seen_cycle INTEGER
            )
        """)

        # Tabela de comparações entre roteiros
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS screenplay_comparisons (
                comparison_id INTEGER PRIMARY KEY AUTOINCREMENT,
                screenplay1 TEXT,
                screenplay2 TEXT,
                similarity_score REAL,
                common_elements TEXT,
                differences TEXT,
                cycle_id INTEGER
            )
        """)

        conn.commit()
        conn.close()

    def get_cycle_count(self) -> int:
        """Obtém número de ciclos já realizados"""

        conn = sqlite3.connect(self.knowledge_db)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM learning_cycles")
        count = cursor.fetchone()[0]
        conn.close()
        return count

    def get_accumulated_knowledge(self) -> str:
        """Recupera conhecimento acumulado dos ciclos anteriores"""

        conn = sqlite3.connect(self.knowledge_db)
        cursor = conn.cursor()

        # Últimos 20 insights de alta confiança
        cursor.execute("""
            SELECT content FROM insights
            WHERE confidence > 0.7
            ORDER BY insight_id DESC
            LIMIT 20
        """)
        insights = cursor.fetchall()

        # Padrões mais frequentes
        cursor.execute("""
            SELECT description, occurrences FROM patterns
            WHERE occurrences > 2
            ORDER BY occurrences DESC
            LIMIT 10
        """)
        patterns = cursor.fetchall()

        conn.close()

        knowledge = "CONHECIMENTO ACUMULADO:\n\n"

        if insights:
            knowledge += "Insights Anteriores:\n"
            for insight in insights:
                knowledge += f"• {insight[0]}\n"

        if patterns:
            knowledge += "\nPadrões Descobertos:\n"
            for pattern, count in patterns:
                knowledge += f"• {pattern} (visto {count}x)\n"

        return knowledge

    def ollama_request(self, prompt: str, temperature: float = 0.5) -> Optional[str]:
        """Faz requisição ao Ollama com tratamento de erro"""

        try:
            response = requests.post(
                self.ollama_endpoint,
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "temperature": temperature,
                    "top_p": 0.9
                },
                timeout=900  # 15 minutos para análise ULTRA PROFUNDA com 200K tokens
            )

            if response.status_code == 200:
                return response.json().get("response", "")

        except requests.exceptions.Timeout:
            print(f"⚠️ TIMEOUT: Análise levou mais de 15 minutos. Considere aumentar o timeout.")
        except requests.exceptions.ConnectionError as e:
            print(f"⚠️ Erro de conexão: {e}")
            print("❌ Ollama não está rodando. Inicie com: ollama serve")
        except Exception as e:
            print(f"⚠️ Erro inesperado: {type(e).__name__}: {e}")

        return None

    def extract_theory_techniques(self, theory_path: Path) -> dict:
        """Extrai técnicas específicas de cada teoria usando o próprio modelo"""

        print(f"    🔍 Extraindo técnicas de: {theory_path.stem[:50]}...")

        # Ler teoria
        theory_text = theory_path.read_text(encoding='utf-8', errors='ignore')[:20000]  # Reduzido para 20K
        theory_name = theory_path.stem

        # Prompt otimizado e focado
        prompt = f"""Analise esta teoria de roteiro e extraia AS TÉCNICAS PRINCIPAIS.

TEORIA: {theory_name}

TRECHO DO CONTEÚDO:
{theory_text}

Extraia APENAS o essencial em JSON:
{{
  "theory_name": "{theory_name}",
  "main_techniques": [lista de 5-10 técnicas principais],
  "structural_elements": [elementos estruturais chave],
  "key_concepts": [conceitos fundamentais],
  "specific_beats": [beats narrativos se mencionados]
}}

Seja CONCISO e ESPECÍFICO."""

        print(f"    📡 Enviando request para Ollama...")

        try:
            response = self.ollama_request(prompt, temperature=0.3)

            if response and "{" in response:
                start = response.find("{")
                end = response.rfind("}") + 1
                result = json.loads(response[start:end])
                print(f"    ✅ Técnicas extraídas com sucesso!")
                return result
        except Exception as e:
            print(f"    ⚠️ Erro na extração: {e}")

        # Fallback com técnicas genéricas
        print(f"    ⚠️ Usando técnicas genéricas como fallback")
        return {
            "theory_name": theory_name,
            "main_techniques": ["estrutura em 3 atos", "arco do herói", "conflito"],
            "structural_elements": ["setup", "confrontation", "resolution"],
            "key_concepts": ["tema", "personagem", "diálogo"],
            "specific_beats": []
        }


    def create_theory_based_prompt(self, screenplay_text: str, screenplay_name: str, theory_data: dict) -> str:
        """Cria um prompt especializado baseado nas técnicas extraídas da teoria"""

        techniques = theory_data.get('main_techniques', [])
        elements = theory_data.get('structural_elements', [])
        concepts = theory_data.get('key_concepts', [])
        beats = theory_data.get('specific_beats', [])

        # Limitar texto para eficiência
        screenplay_excerpt = screenplay_text[:30000]  # 30K é suficiente para análise profunda

        prompt = f"""Analise este roteiro aplicando a teoria {theory_data.get('theory_name', '')[:50]}.

ROTEIRO: {screenplay_name}

PRIMEIRO ATO (amostra para análise):
{screenplay_excerpt}

TÉCNICAS A VERIFICAR:
"""

        # Limitar para eficiência mas manter qualidade
        if techniques:
            prompt += f"\nTÉCNICAS PRINCIPAIS (top {min(len(techniques), 5)}):\n"
            for i, tech in enumerate(techniques[:5], 1):  # Top 5 técnicas
                prompt += f"  {i}. {tech}\n"

        if elements:
            prompt += f"\nELEMENTOS ESTRUTURAIS (top {min(len(elements), 5)}):\n"
            for elem in elements[:5]:  # Top 5 elementos
                prompt += f"  • {elem}\n"

        if concepts:
            prompt += f"\nCONCEITOS-CHAVE (top {min(len(concepts), 3)}):\n"
            for concept in concepts[:3]:  # Top 3 conceitos
                prompt += f"  • {concept}\n"

        if beats and len(beats) > 0:
            prompt += f"\nBEATS NARRATIVOS:\n"
            for beat in beats[:3]:  # Top 3 beats
                prompt += f"  • {beat}\n"

        prompt += """\n
ANÁLISE FOCADA:
1. Quais técnicas da teoria estão presentes no roteiro?
2. Dê 2-3 exemplos concretos
3. Avalie aderência geral (0-1)

Responda em JSON simples:
{{
  "adherence": 0.0-1.0,
  "techniques_found": ["técnica1", "técnica2"],
  "key_examples": ["exemplo1", "exemplo2"],
  "insight": "descoberta principal",
  "pattern": "padrão identificado"
}}"""

        return prompt

    def phase1_theory_analysis(self, screenplays: List[Path], theories: List[Path]):
        """Fase 1: Análise de roteiros contra teorias"""

        print(f"\n{'='*80}")
        print(f"📚 FASE 1: ANÁLISE TEÓRICA (Ciclo {self.cycle_count + 1})")
        print(f"{'='*80}")

        # Conhecimento acumulado
        prior_knowledge = self.get_accumulated_knowledge()

        insights = []

        # Carregar checkpoint se existir
        checkpoint = self.load_checkpoint()
        completed_analyses = checkpoint.get('completed_analyses', [])

        # Cache de técnicas extraídas para cada teoria
        theory_techniques_cache = {}

        # Com savepoints, podemos fazer TODAS as análises!
        # Se interromper, continua de onde parou
        for i, screenplay in enumerate(screenplays):  # TODOS os roteiros
            text = screenplay.read_text(encoding='utf-8', errors='ignore')
            analysis = self.doctor.analyze_script(text, screenplay.stem)

            for j, theory_file in enumerate(theories):  # TODAS as teorias

                # Verificar se já foi analisado
                analysis_key = f"{screenplay.stem}||{theory_file.stem}"
                if analysis_key in completed_analyses:
                    print(f"  ✔️ Pulando (já analisado): {screenplay.stem[:30]} x {theory_file.stem[:30]}")
                    continue
                if not theory_file.exists():
                    continue

                # Extrair técnicas da teoria (com cache)
                if theory_file.stem not in theory_techniques_cache:
                    print(f"\n  📚 Iniciando extração de técnicas de: {theory_file.stem[:50]}...")
                    print(f"  ⏰ AVISO: Isto pode levar até 15 minutos por teoria!")
                    try:
                        theory_techniques = self.extract_theory_techniques(theory_file)
                        theory_techniques_cache[theory_file.stem] = theory_techniques
                        print(f"  ✅ Técnicas extraídas com sucesso!")
                    except Exception as e:
                        print(f"  ❌ ERRO ao extrair técnicas: {e}")
                        continue
                else:
                    theory_techniques = theory_techniques_cache[theory_file.stem]
                    print(f"  📦 Usando técnicas do cache para {theory_file.stem[:30]}")

                # Criar prompt especializado baseado na teoria
                print(f"  🎬 [{i+1}/{len(screenplays)}] x [{j+1}/{len(theories)}] Analisando {screenplay.stem[:30]} com teoria {theory_file.stem[:30]}...")
                print(f"     ⏰ Tempo estimado: 15 minutos para análise ULTRA profunda com 200K tokens")
                start_time = time.time()

                prompt = self.create_theory_based_prompt(text, screenplay.stem, theory_techniques)
                # O prompt agora é criado pela função especializada

                response = self.ollama_request(prompt)

                if response and "{" in response:
                    try:
                        start = response.find("{")
                        end = response.rfind("}") + 1
                        data = json.loads(response[start:end])

                        insight = {
                            "screenplay": screenplay.stem,
                            "theory": theory_file.stem,
                            "adherence": data.get("adherence", 0.5),
                            "three_act_structure": data.get("three_act_structure", ""),
                            "key_scenes": data.get("key_scenes", []),
                            "character_arc": data.get("character_arc", ""),
                            "dialogue_quality": data.get("dialogue_quality", ""),
                            "unique_techniques": data.get("unique_techniques", ""),
                            "thematic_depth": data.get("thematic_depth", ""),
                            "insight": data.get("insight", ""),
                            "pattern": data.get("pattern", "")
                        }

                        insights.append(insight)

                        # Salvar checkpoint após CADA análise
                        completed_analyses.append(analysis_key)
                        self.save_checkpoint(screenplay.stem, theory_file.stem, completed_analyses)

                        elapsed = time.time() - start_time
                        print(f"  ✓ Completo em {elapsed:.1f}s - {screenplay.stem[:30]} vs {theory_file.stem[:30]}: {insight.get('theory_adherence', insight.get('adherence', 0.5)):.1%}")

                        # Salvar insight no banco imediatamente
                        self.save_insights([insight], [], {})
                        print(f"  💾 Checkpoint salvo! Total analisado: {len(completed_analyses)}")

                    except:
                        pass

                time.sleep(2)

        # Salvar insights
        self.save_insights(insights, "theory_analysis")
        return insights

    def phase2_screenplay_comparison(self, screenplays: List[Path]):
        """Fase 2: Comparação entre roteiros"""

        print(f"\n{'='*80}")
        print(f"🎭 FASE 2: COMPARAÇÃO ENTRE ROTEIROS (Ciclo {self.cycle_count + 1})")
        print(f"{'='*80}")

        prior_knowledge = self.get_accumulated_knowledge()
        comparisons = []

        # Comparar TODOS os pares de roteiros (análise completa)
        for i in range(len(screenplays) - 1):
            for j in range(i + 1, len(screenplays)):
                screenplay1 = screenplays[i]
                screenplay2 = screenplays[j]

                text1 = screenplay1.read_text(encoding='utf-8', errors='ignore')
                text2 = screenplay2.read_text(encoding='utf-8', errors='ignore')

                analysis1 = self.doctor.analyze_script(text1, screenplay1.stem)
                analysis2 = self.doctor.analyze_script(text2, screenplay2.stem)

                prompt = f"""{prior_knowledge}

=== ROTEIRO 1: {screenplay1.stem} ===
ESTRUTURA COMPLETA:
Cenas: {analysis1.scenes}, Personagens: {len(analysis1.top_characters)}, Diálogo: {analysis1.dialogue_ratio:.1%}

PRIMEIRO ATO (30K chars para contexto massivo):
{text1[:30000]}

=== ROTEIRO 2: {screenplay2.stem} ===
ESTRUTURA COMPLETA:
Cenas: {analysis2.scenes}, Personagens: {len(analysis2.top_characters)}, Diálogo: {analysis2.dialogue_ratio:.1%}

PRIMEIRO ATO (30K chars para contexto massivo):
{text2[:30000]}

ANÁLISE PROFUNDA E COMPARATIVA (use TODO o contexto de 200K tokens):

1. ESTRUTURA NARRATIVA:
   - Compare os 3 atos de cada roteiro
   - Identifique pontos de virada (plot points)
   - Analise ritmo e progressão dramática

2. DESENVOLVIMENTO DE PERSONAGENS:
   - Compare arcos dos protagonistas
   - Analise antagonistas e forças opostas
   - Examine personagens secundários

3. DIÁLOGOS E ESTILO:
   - Compare qualidade e naturalidade dos diálogos
   - Identifique voice única de cada roteiro
   - Analise subtexto e camadas de significado

4. TEMAS E SIMBOLISMO:
   - Temas centrais de cada obra
   - Uso de metáforas visuais
   - Profundidade filosófica

5. TÉCNICAS CINEMATOGRÁFICAS:
   - Descrições de cena e atmosfera
   - Uso de ação vs diálogo
   - Recursos visuais e sonoros

Responda em JSON com ANÁLISE PROFUNDA E DETALHADA:
{{
  "similarity_score": 0.0-1.0,
  "narrative_structure": {{
    "screenplay1_acts": "análise dos 3 atos",
    "screenplay2_acts": "análise dos 3 atos",
    "structural_similarity": 0.0-1.0
  }},
  "character_development": {{
    "protagonist1_arc": "evolução detalhada",
    "protagonist2_arc": "evolução detalhada",
    "character_complexity": "comparação de profundidade"
  }},
  "dialogue_analysis": {{
    "style1": "estilo de diálogo roteiro 1",
    "style2": "estilo de diálogo roteiro 2",
    "effectiveness": "qual é mais efetivo e por quê"
  }},
  "thematic_analysis": {{
    "themes1": ["tema1", "tema2", "tema3"],
    "themes2": ["tema1", "tema2", "tema3"],
    "philosophical_depth": "comparação de profundidade"
  }},
  "cinematic_techniques": {{
    "visual_storytelling1": "técnicas visuais",
    "visual_storytelling2": "técnicas visuais",
    "innovation_level": "qual é mais inovador"
  }},
  "common_elements": ["elemento profundo 1", "elemento profundo 2", "elemento profundo 3"],
  "key_differences": ["diferença fundamental 1", "diferença fundamental 2", "diferença fundamental 3"],
  "unique_insight": "descoberta profunda e única sobre a comparação",
  "recommendation": "qual roteiro é mais forte e por quê"
}}"""

                response = self.ollama_request(prompt, temperature=0.6)

                if response and "{" in response:
                    try:
                        start = response.find("{")
                        end = response.rfind("}") + 1
                        data = json.loads(response[start:end])

                        comparison = {
                            "screenplay1": screenplay1.stem,
                            "screenplay2": screenplay2.stem,
                            "similarity": data.get("similarity", 0.5),
                            "common": data.get("common_elements", []),
                            "differences": data.get("key_differences", []),
                            "insight": data.get("unique_insight", "")
                        }

                        comparisons.append(comparison)
                        print(f"  ✓ {screenplay1.stem} ↔ {screenplay2.stem}: {comparison['similarity']:.1%} similar")

                    except:
                        pass

                time.sleep(2)

        # Salvar comparações
        self.save_comparisons(comparisons)
        return comparisons

    def phase3_pattern_extraction(self, insights: List, comparisons: List):
        """Fase 3: Extração de padrões e evolução do conhecimento"""

        print(f"\n{'='*80}")
        print(f"🔍 FASE 3: EXTRAÇÃO DE PADRÕES (Ciclo {self.cycle_count + 1})")
        print(f"{'='*80}")

        prior_knowledge = self.get_accumulated_knowledge()

        # Compilar dados para análise
        insights_summary = "\n".join([f"• {i.get('insight', '')}" for i in insights if i.get('insight')])
        patterns_seen = "\n".join([f"• {i.get('pattern', '')}" for i in insights if i.get('pattern')])

        comparison_insights = "\n".join([f"• {c.get('insight', '')}" for c in comparisons if c.get('insight')])

        prompt = f"""{prior_knowledge}

INSIGHTS DA ANÁLISE TEÓRICA:
{insights_summary}

PADRÕES OBSERVADOS:
{patterns_seen}

INSIGHTS DAS COMPARAÇÕES:
{comparison_insights}

Baseado em tudo isso, identifique:
1. Padrões recorrentes que confirmam ou contradizem conhecimento anterior
2. Novas descobertas que expandem o conhecimento
3. Regras gerais que podem ser aplicadas

Responda em JSON:
{{
  "confirmed_patterns": ["padrão1", "padrão2"],
  "new_discoveries": ["descoberta1", "descoberta2"],
  "general_rules": ["regra1", "regra2"],
  "evolution_insight": "como o conhecimento evoluiu neste ciclo"
}}"""

        response = self.ollama_request(prompt, temperature=0.7)

        if response and "{" in response:
            try:
                start = response.find("{")
                end = response.rfind("}") + 1
                data = json.loads(response[start:end])

                # Salvar padrões descobertos
                self.save_patterns(data)

                print("\n📊 PADRÕES EXTRAÍDOS:")

                if data.get("confirmed_patterns"):
                    print("\n✅ Padrões Confirmados:")
                    for pattern in data["confirmed_patterns"][:3]:
                        print(f"  • {pattern}")

                if data.get("new_discoveries"):
                    print("\n🆕 Novas Descobertas:")
                    for discovery in data["new_discoveries"][:3]:
                        print(f"  • {discovery}")

                if data.get("general_rules"):
                    print("\n📐 Regras Gerais:")
                    for rule in data["general_rules"][:3]:
                        print(f"  • {rule}")

                if data.get("evolution_insight"):
                    print(f"\n💡 Evolução: {data['evolution_insight']}")

                return data

            except:
                pass

        return {}

    def save_insights(self, insights: List, phase: str):
        """Salva insights no banco de conhecimento"""

        conn = sqlite3.connect(self.knowledge_db)
        cursor = conn.cursor()

        for insight in insights:
            cursor.execute("""
                INSERT INTO insights (cycle_id, type, content, confidence, timestamp)
                VALUES (?, ?, ?, ?, ?)
            """, (
                self.cycle_count + 1,
                phase,
                json.dumps(insight, ensure_ascii=False),
                insight.get("adherence", 0.5),
                datetime.now().isoformat()
            ))

        conn.commit()
        conn.close()

    def save_comparisons(self, comparisons: List):
        """Salva comparações entre roteiros"""

        conn = sqlite3.connect(self.knowledge_db)
        cursor = conn.cursor()

        for comp in comparisons:
            cursor.execute("""
                INSERT INTO screenplay_comparisons
                (screenplay1, screenplay2, similarity_score, common_elements, differences, cycle_id)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                comp["screenplay1"],
                comp["screenplay2"],
                comp["similarity"],
                json.dumps(comp["common"], ensure_ascii=False),
                json.dumps(comp["differences"], ensure_ascii=False),
                self.cycle_count + 1
            ))

        conn.commit()
        conn.close()

    def save_patterns(self, patterns: Dict):
        """Salva padrões descobertos"""

        conn = sqlite3.connect(self.knowledge_db)
        cursor = conn.cursor()

        # Atualizar ou inserir padrões
        all_patterns = []

        if patterns.get("confirmed_patterns"):
            all_patterns.extend([(p, "confirmed") for p in patterns["confirmed_patterns"]])

        if patterns.get("new_discoveries"):
            all_patterns.extend([(p, "discovery") for p in patterns["new_discoveries"]])

        if patterns.get("general_rules"):
            all_patterns.extend([(p, "rule") for p in patterns["general_rules"]])

        for pattern_desc, pattern_type in all_patterns:
            # Verificar se padrão já existe
            pattern_hash = hashlib.md5(pattern_desc.encode()).hexdigest()[:8]

            cursor.execute("""
                SELECT pattern_id, occurrences FROM patterns
                WHERE description = ?
            """, (pattern_desc,))

            existing = cursor.fetchone()

            if existing:
                # Atualizar ocorrências
                cursor.execute("""
                    UPDATE patterns
                    SET occurrences = occurrences + 1,
                        last_seen_cycle = ?
                    WHERE pattern_id = ?
                """, (self.cycle_count + 1, existing[0]))
            else:
                # Inserir novo padrão
                cursor.execute("""
                    INSERT INTO patterns
                    (pattern_type, description, occurrences, first_seen_cycle, last_seen_cycle)
                    VALUES (?, ?, 1, ?, ?)
                """, (pattern_type, pattern_desc, self.cycle_count + 1, self.cycle_count + 1))

        conn.commit()
        conn.close()

    def phase4_self_critique(self, cycle_id: int):
        """Fase 4: Auto-crítica - Ollama questiona seus próprios insights"""

        print(f"\n{'='*80}")
        print(f"🤔 FASE 4: AUTO-CRÍTICA (Ciclo {cycle_id})")
        print(f"{'='*80}")

        conn = sqlite3.connect(self.knowledge_db)
        cursor = conn.cursor()

        # Pegar últimos insights do ciclo
        cursor.execute("""
            SELECT insight_id, content, confidence
            FROM insights
            WHERE cycle_id = ?
            ORDER BY insight_id DESC
            LIMIT 10
        """, (cycle_id,))

        insights_to_review = cursor.fetchall()

        for insight_id, content, old_confidence in insights_to_review:
            if not self.ollama_request:
                continue

            # Ollama critica seu próprio insight
            critique_prompt = f"""Analise criticamente este insight que você mesmo gerou:

{content}

Seja BRUTALMENTE HONESTO:
1. Este insight é realmente válido? (0-1)
2. É genérico demais?
3. Tem evidência suficiente?

Responda com um único número de 0.0 a 1.0 representando qualidade."""

            response = self.ollama_request(critique_prompt, temperature=0.2)

            try:
                # Extrair score
                import re
                matches = re.findall(r'[0-1](?:\.\d+)?', response or "0.5")
                critique_score = float(matches[0]) if matches else 0.5

                # Ajustar confiança: média ponderada
                new_confidence = (old_confidence * 0.6) + (critique_score * 0.4)

                # Atualizar no banco
                cursor.execute("""
                    UPDATE insights
                    SET confidence = ?
                    WHERE insight_id = ?
                """, (new_confidence, insight_id))

                if critique_score < 0.3:
                    print(f"  ❌ Insight fraco detectado (score: {critique_score:.2f})")
                elif critique_score > 0.7:
                    print(f"  ✅ Insight validado (score: {critique_score:.2f})")

            except Exception as e:
                print(f"  ⚠️ Erro na crítica: {e}")

        conn.commit()
        conn.close()

        print("  🤔 Auto-crítica completa - insights reavaliados")

    def complete_cycle(self):
        """Completa um ciclo de aprendizado"""

        conn = sqlite3.connect(self.knowledge_db)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO learning_cycles (timestamp, phase, insights_count, patterns_found)
            VALUES (?, 'complete', ?, ?)
        """, (
            datetime.now().isoformat(),
            len(self.accumulated_insights),
            len(self.pattern_memory)
        ))

        conn.commit()
        conn.close()

        self.cycle_count += 1

    def load_checkpoint(self):
        """Carrega checkpoint de onde parou"""
        checkpoint_file = Path("checkpoint_analysis.json")

        if checkpoint_file.exists():
            with open(checkpoint_file, 'r') as f:
                checkpoint = json.load(f)
                print(f"💾 CHECKPOINT ENCONTRADO!")
                print(f"  • Último roteiro: {checkpoint.get('last_screenplay', 'N/A')}")
                print(f"  • Última teoria: {checkpoint.get('last_theory', 'N/A')}")
                print(f"  • Análises completas: {checkpoint.get('completed_count', 0)}")
                return checkpoint
        return {}

    def save_checkpoint(self, screenplay: str, theory: str, completed: list):
        """Salva checkpoint após cada análise"""
        checkpoint = {
            'last_screenplay': screenplay,
            'last_theory': theory,
            'completed_analyses': completed,
            'completed_count': len(completed),
            'timestamp': datetime.now().isoformat(),
            'cycle': self.cycle_count
        }

        with open('checkpoint_analysis.json', 'w') as f:
            json.dump(checkpoint, f, indent=2, ensure_ascii=False)

    def run_continuous_loop(self, max_cycles: int = None):
        """Executa loop contínuo de aprendizado com SAVEPOINTS"""

        print("🚀 INICIANDO LOOP CONTÍNUO DE APRENDIZADO EVOLUTIVO")
        print(f"📊 Ciclos anteriores completados: {self.cycle_count}")

        # Coletar arquivos - PRIORIZAR MASTERS (34 roteiros profissionais)
        screenplays = []

        # Primeiro: Roteiros mestres profissionais
        if self.masters_dir.exists():
            masters = list(self.masters_dir.glob("*.txt"))
            screenplays.extend(masters)
            print(f"  📌 {len(masters)} roteiros mestres carregados (Alien, Fight Club, Inception...)")

        # Segundo: Roteiros do usuário para comparação
        if self.my_screenplays_dir.exists():
            user_scripts = list(self.my_screenplays_dir.glob("*.txt"))
            screenplays.extend(user_scripts)
            if user_scripts:
                print(f"  📝 {len(user_scripts)} roteiros do usuário incluídos")

        # Terceiro: Outros roteiros se necessário
        if len(screenplays) < 5 and self.screenplays_dir.exists():
            others = list(self.screenplays_dir.glob("*.txt"))
            screenplays.extend([s for s in others if s not in screenplays])

        theories = []
        if self.theory_dir.exists():
            theories = list(self.theory_dir.glob("*.txt"))

        print(f"📚 {len(screenplays)} roteiros, {len(theories)} teorias disponíveis")

        cycles_run = 0

        try:
            while True:
                if max_cycles and cycles_run >= max_cycles:
                    break

                print(f"\n{'='*80}")
                print(f"🔄 CICLO {self.cycle_count + 1} - INICIANDO")
                print(f"{'='*80}")

                # Fase 1: Análise teórica
                insights = self.phase1_theory_analysis(screenplays, theories)

                # Fase 2: Comparação entre roteiros
                comparisons = self.phase2_screenplay_comparison(screenplays)

                # Fase 3: Extração de padrões
                patterns = self.phase3_pattern_extraction(insights, comparisons)

                # Fase 4: Auto-crítica (NOVA!)
                self.phase4_self_critique(self.cycle_count + 1)

                # Completar ciclo
                self.complete_cycle()

                print(f"\n✅ CICLO {self.cycle_count} COMPLETO!")

                # Mostrar estatísticas
                conn = sqlite3.connect(self.knowledge_db)
                cursor = conn.cursor()

                cursor.execute("SELECT COUNT(*) FROM insights")
                total_insights = cursor.fetchone()[0]

                cursor.execute("SELECT COUNT(*) FROM patterns")
                total_patterns = cursor.fetchone()[0]

                cursor.execute("SELECT COUNT(*) FROM screenplay_comparisons")
                total_comparisons = cursor.fetchone()[0]

                conn.close()

                print(f"\n📈 ESTATÍSTICAS ACUMULADAS:")
                print(f"  • Total de insights: {total_insights}")
                print(f"  • Padrões identificados: {total_patterns}")
                print(f"  • Comparações realizadas: {total_comparisons}")

                cycles_run += 1

                # Pausa entre ciclos
                print(f"\n⏸️ Aguardando 30 segundos para próximo ciclo...")
                time.sleep(30)

        except KeyboardInterrupt:
            print("\n\n🛑 Loop interrompido pelo usuário")
            print(f"✅ Completados {cycles_run} ciclos nesta sessão")

    def show_evolution_report(self):
        """Mostra relatório de evolução do conhecimento"""

        conn = sqlite3.connect(self.knowledge_db)
        cursor = conn.cursor()

        print("\n" + "="*80)
        print("📊 RELATÓRIO DE EVOLUÇÃO DO CONHECIMENTO")
        print("="*80)

        # Padrões mais frequentes
        cursor.execute("""
            SELECT description, occurrences, pattern_type
            FROM patterns
            ORDER BY occurrences DESC
            LIMIT 10
        """)

        patterns = cursor.fetchall()

        if patterns:
            print("\n🏆 TOP 10 PADRÕES MAIS RECORRENTES:")
            for i, (desc, count, ptype) in enumerate(patterns, 1):
                print(f"  {i}. [{ptype}] {desc} (visto {count}x)")

        # Evolução por ciclo
        cursor.execute("""
            SELECT cycle_id, insights_count, patterns_found, timestamp
            FROM learning_cycles
            ORDER BY cycle_id DESC
            LIMIT 5
        """)

        cycles = cursor.fetchall()

        if cycles:
            print("\n📈 ÚLTIMOS 5 CICLOS:")
            for cycle_id, insights, patterns, timestamp in cycles:
                print(f"  Ciclo {cycle_id}: {insights} insights, {patterns} padrões - {timestamp[:10]}")

        conn.close()

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Aprendizado Contínuo Evolutivo com Ollama")
    parser.add_argument("--cycles", type=int, help="Número de ciclos (vazio = infinito)")
    parser.add_argument("--report", action="store_true", help="Mostrar relatório de evolução")

    args = parser.parse_args()

    system = OllamaContinuousLearning()

    if args.report:
        system.show_evolution_report()
    else:
        # Verificar Ollama
        try:
            response = requests.get("http://127.0.0.1:11434/api/tags", timeout=30)  # 30s para modelos grandes
            if response.status_code == 200:
                print("✅ Ollama conectado")
                system.run_continuous_loop(max_cycles=args.cycles)
            else:
                print(f"❌ Ollama não está respondendo. Status: {response.status_code}")
        except requests.exceptions.Timeout:
            print("❌ Timeout ao conectar com Ollama (30s). Verifique se o servidor está respondendo.")
        except requests.exceptions.ConnectionError as e:
            print(f"❌ Erro de conexão com Ollama: {e}")
            print("❌ Ollama não está rodando. Inicie com: ollama serve")
        except Exception as e:
            print(f"❌ Erro inesperado: {type(e).__name__}: {e}")