#!/usr/bin/env python3
"""
Sistema de Aprendizado Contínuo com TOKEN TURBO
200K tokens de contexto para análise profunda
"""

import sys
import json
import time
import sqlite3
import requests
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
from collections import defaultdict

sys.path.insert(0, 'src')

from scripturemon_champion.analysis.script_doctor import ScriptDoctor
from scripturemon_champion.core.profiles import LearningProfiles

class TokenTurboLearning:
    """
    Aprendizado contínuo usando TOKEN TURBO (200K contexto)
    """

    def __init__(self):
        # Carregar perfil Token Turbo
        self.profiles = LearningProfiles()
        self.token_turbo = self.profiles.TOKEN_TURBO

        print("=" * 80)
        print("🚀 TOKEN TURBO LEARNING SYSTEM")
        print(f"📊 Contexto: {self.token_turbo.context_size:,} tokens")
        print(f"🔥 Modelo: {self.token_turbo.name}")
        print("=" * 80)

        self.doctor = ScriptDoctor()
        self.ollama_endpoint = "http://127.0.0.1:11434/api/generate"

        # Configurar modelo com Token Turbo
        self.model_config = self.token_turbo.config
        self.model_name = "mixtral-eco-q5:latest"  # Modelo com capacidade para 200K

        # Diretórios
        self.theory_dir = Path("theory")
        self.screenplays_dir = Path("screenplays")
        self.my_screenplays_dir = Path("my_screenplays")
        self.knowledge_db = Path("data/learning/token_turbo_knowledge.db")

        # Inicializar banco
        self.knowledge_db.parent.mkdir(parents=True, exist_ok=True)
        self.init_knowledge_db()

    def init_knowledge_db(self):
        """Inicializa banco com WAL mode para robustez"""

        conn = sqlite3.connect(self.knowledge_db)

        # WAL mode + optimizações
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute("PRAGMA synchronous=NORMAL;")
        conn.execute("PRAGMA cache_size=10000;")
        conn.execute("PRAGMA temp_store=MEMORY;")

        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS learning_cycles (
                cycle_id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                phase TEXT,
                insights_count INTEGER,
                patterns_found INTEGER,
                token_turbo_used BOOLEAN DEFAULT 1
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS deep_insights (
                insight_id INTEGER PRIMARY KEY AUTOINCREMENT,
                cycle_id INTEGER,
                type TEXT,
                content TEXT,
                confidence REAL,
                context_tokens INTEGER,
                timestamp TEXT
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS mega_patterns (
                pattern_id INTEGER PRIMARY KEY AUTOINCREMENT,
                pattern_type TEXT,
                description TEXT,
                occurrences INTEGER,
                examples TEXT,
                first_seen_cycle INTEGER,
                last_seen_cycle INTEGER,
                confidence REAL
            )
        """)

        conn.commit()
        conn.close()

    def ollama_turbo_request(self, prompt: str, max_context: int = 200000) -> Optional[str]:
        """Requisição com Token Turbo config"""

        try:
            # Configuração especial Token Turbo
            payload = {
                "model": self.model_name,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.5,
                    "top_p": 0.9,
                    "num_ctx": min(max_context, self.token_turbo.context_size),
                    "rope_frequency_base": self.model_config.get('rope_theta', 500000),
                    "rope_scaling": self.model_config.get('rope_scaling', 1.5),
                    "num_thread": 16,  # Usar múltiplos threads
                    "num_gpu": 60,  # Usar todos os cores GPU disponíveis
                    "repeat_penalty": 1.05
                }
            }

            response = requests.post(
                self.ollama_endpoint,
                json=payload,
                timeout=120  # Timeout maior para contextos grandes
            )

            if response.status_code == 200:
                result = response.json()
                return result.get("response", "")

        except Exception as e:
            print(f"⚠️ Erro Token Turbo: {e}")

        return None

    def mega_context_analysis(self, screenplays: List[Path], theories: List[Path]):
        """Análise usando contexto massivo do Token Turbo"""

        print(f"\n{'='*80}")
        print(f"🧠 ANÁLISE MEGA-CONTEXTO COM TOKEN TURBO")
        print(f"{'='*80}")

        # Carregar TODOS os textos no contexto
        all_screenplays_text = ""
        for sp in screenplays[:10]:  # Top 10 roteiros
            text = sp.read_text(encoding='utf-8', errors='ignore')
            all_screenplays_text += f"\n\n=== {sp.stem} ===\n{text[:20000]}"

        all_theories_text = ""
        for th in theories[:10]:  # Top 10 teorias
            text = th.read_text(encoding='utf-8', errors='ignore')
            all_theories_text += f"\n\n=== {th.stem} ===\n{text[:20000]}"

        # Prompt gigante usando todo o contexto
        mega_prompt = f"""Você tem acesso a {len(screenplays)} roteiros e {len(theories)} teorias no contexto.

ROTEIROS:
{all_screenplays_text}

TEORIAS:
{all_theories_text}

ANÁLISE PROFUNDA REQUERIDA:

1. PADRÕES UNIVERSAIS: Que padrões aparecem em TODOS os roteiros?
2. VIOLAÇÕES TEÓRICAS: Onde os roteiros violam as teorias clássicas?
3. INOVAÇÕES: Que elementos novos/únicos cada roteiro traz?
4. SÍNTESE: Crie 5 regras universais baseadas em tudo.

Responda em JSON:
{{
    "universal_patterns": ["padrão1", "padrão2", ...],
    "theory_violations": [{{"screenplay": "nome", "theory": "nome", "violation": "descrição"}}],
    "innovations": [{{"screenplay": "nome", "innovation": "descrição"}}],
    "universal_rules": ["regra1", "regra2", ...]
}}"""

        print(f"📊 Contexto total: ~{len(mega_prompt):,} caracteres")
        print("⏳ Processando com Token Turbo...")

        response = self.ollama_turbo_request(mega_prompt, max_context=200000)

        if response:
            try:
                # Extrair JSON
                import re
                json_match = re.search(r'\{.*\}', response, re.DOTALL)
                if json_match:
                    data = json.loads(json_match.group())

                    # Salvar insights profundos
                    self.save_mega_insights(data)

                    print("\n✅ ANÁLISE MEGA-CONTEXTO COMPLETA!")

                    if data.get("universal_patterns"):
                        print("\n🌍 PADRÕES UNIVERSAIS DESCOBERTOS:")
                        for pattern in data["universal_patterns"][:5]:
                            print(f"  • {pattern}")

                    if data.get("universal_rules"):
                        print("\n📐 REGRAS UNIVERSAIS SINTETIZADAS:")
                        for rule in data["universal_rules"][:5]:
                            print(f"  • {rule}")

                    return data

            except Exception as e:
                print(f"⚠️ Erro processando resposta: {e}")

        return None

    def save_mega_insights(self, data: Dict):
        """Salva insights do Token Turbo"""

        conn = sqlite3.connect(self.knowledge_db)
        cursor = conn.cursor()

        # Criar novo ciclo
        cursor.execute("""
            INSERT INTO learning_cycles (timestamp, phase, token_turbo_used)
            VALUES (?, 'mega_analysis', 1)
        """, (datetime.now().isoformat(),))

        cycle_id = cursor.lastrowid

        # Salvar padrões universais
        for pattern in data.get("universal_patterns", []):
            cursor.execute("""
                INSERT INTO mega_patterns (pattern_type, description, occurrences, first_seen_cycle, confidence)
                VALUES ('universal', ?, 1, ?, 0.9)
            """, (pattern, cycle_id))

        # Salvar regras universais
        for rule in data.get("universal_rules", []):
            cursor.execute("""
                INSERT INTO deep_insights (cycle_id, type, content, confidence, context_tokens)
                VALUES (?, 'universal_rule', ?, 0.95, 200000)
            """, (cycle_id, rule))

        conn.commit()
        conn.close()

    def run_token_turbo_loop(self, cycles: int = None):
        """Loop contínuo com Token Turbo"""

        # Verificar Token Turbo
        if not self.token_turbo.verify():
            print("❌ Token Turbo não está configurado corretamente!")
            return

        # Coletar arquivos
        screenplays = []
        if self.my_screenplays_dir.exists():
            screenplays.extend(list(self.my_screenplays_dir.glob("*.txt")))
        if self.screenplays_dir.exists():
            screenplays.extend(list(self.screenplays_dir.glob("*.txt")))

        theories = []
        if self.theory_dir.exists():
            theories = list(self.theory_dir.glob("*.txt"))

        print(f"\n📚 {len(screenplays)} roteiros, {len(theories)} teorias para análise")

        cycles_run = 0

        try:
            while True:
                if cycles and cycles_run >= cycles:
                    break

                print(f"\n{'='*80}")
                print(f"🔄 CICLO TOKEN TURBO {cycles_run + 1}")
                print(f"{'='*80}")

                # Análise mega-contexto
                self.mega_context_analysis(screenplays, theories)

                cycles_run += 1

                if cycles is None or cycles_run < cycles:
                    print("\n⏸️ Aguardando 60 segundos para próximo ciclo...")
                    time.sleep(60)

        except KeyboardInterrupt:
            print("\n\n🛑 Loop interrompido")

        print(f"\n✅ Completados {cycles_run} ciclos Token Turbo")
        self.show_report()

    def show_report(self):
        """Mostra relatório de descobertas"""

        conn = sqlite3.connect(self.knowledge_db)
        cursor = conn.cursor()

        print("\n" + "="*80)
        print("📊 RELATÓRIO TOKEN TURBO")
        print("="*80)

        # Padrões universais
        cursor.execute("""
            SELECT description, confidence
            FROM mega_patterns
            WHERE pattern_type = 'universal'
            ORDER BY confidence DESC
            LIMIT 10
        """)

        patterns = cursor.fetchall()
        if patterns:
            print("\n🌍 PADRÕES UNIVERSAIS:")
            for desc, conf in patterns:
                print(f"  • {desc} (confiança: {conf:.2f})")

        # Regras universais
        cursor.execute("""
            SELECT content, confidence
            FROM deep_insights
            WHERE type = 'universal_rule'
            ORDER BY confidence DESC
            LIMIT 10
        """)

        rules = cursor.fetchall()
        if rules:
            print("\n📐 REGRAS UNIVERSAIS:")
            for content, conf in rules:
                print(f"  • {content} (confiança: {conf:.2f})")

        # Estatísticas
        cursor.execute("SELECT COUNT(*) FROM deep_insights")
        total_insights = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM mega_patterns")
        total_patterns = cursor.fetchone()[0]

        print(f"\n📈 TOTAIS:")
        print(f"  • Insights profundos: {total_insights}")
        print(f"  • Padrões identificados: {total_patterns}")
        print(f"  • Contexto máximo usado: 200,000 tokens")

        conn.close()

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Token Turbo Learning System")
    parser.add_argument("--cycles", type=int, help="Número de ciclos")
    parser.add_argument("--report", action="store_true", help="Mostrar relatório")

    args = parser.parse_args()

    system = TokenTurboLearning()

    if args.report:
        system.show_report()
    else:
        # Verificar Ollama
        try:
            response = requests.get("http://127.0.0.1:11434/api/tags", timeout=2)
            if response.status_code == 200:
                print("✅ Ollama conectado")
                system.run_token_turbo_loop(cycles=args.cycles)
            else:
                print("❌ Ollama não está respondendo")
        except:
            print("❌ Ollama não está rodando")