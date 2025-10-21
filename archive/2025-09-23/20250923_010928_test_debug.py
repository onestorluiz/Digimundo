
print('START', flush=True)
#!/usr/bin/env python3
"""
Sistema de Aprendizado Contínuo e Evolutivo para Ollama v2.0
Com retry logic, detecção de problemas e melhorias de estabilidade
"""

import sys
import json
import time
from datetime import datetime
import sqlite3
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple
from collections import defaultdict
import requests
import hashlib
import subprocess
import os
import re

sys.path.insert(0, 'src')

# Importa ProcessLock para evitar múltiplas instâncias
from process_lock import ProcessLock

# Importa templates de prompts específicos
try:
    from prompt_templates import (
        get_prompt_for_analysis,
        score_analysis_quality,
        needs_reanalysis
    )
    PROMPT_TEMPLATES_AVAILABLE = True
except ImportError:
    PROMPT_TEMPLATES_AVAILABLE = False

# Importa SafeJSONParser se disponível
try:
    from safe_json_parser_20250921_214934 import safe_json_parse, calculate_confidence
    SAFE_PARSER_AVAILABLE = True
except ImportError:
    SAFE_PARSER_AVAILABLE = False

from scripturemon_champion.analysis.script_doctor import ScriptDoctor

class OllamaContinuousLearning:
    """
    Sistema de aprendizado contínuo que evolui a cada ciclo
    Versão 2.0 com retry logic e melhor estabilidade
    """

    def __init__(self, model: str = "mixtral-cpu-force:latest", timeout: int = 300):
        # Lock removido - causava travamento
        # self.lock = ProcessLock("ollama_learning")
        # if not self.lock.acquire(timeout=5):
        #     print("⚠️ Outra instância já está rodando. Saindo...")
        #     sys.exit(1)

        self.doctor = ScriptDoctor()
        self.model = model
        self.ollama_endpoint = "http://127.0.0.1:11434/api/generate"
        self.timeout = timeout  # Timeout configurável (default 5 minutos)

        # Limpa processos órfãos antes de iniciar
        self.cleanup_orphan_processes()

        # Verifica conexão com Ollama
        if not self.check_ollama_with_retry():
            print("\n⚠️ Sistema iniciando em modo degradado sem Ollama")
            print("   Análises com LLM não estarão disponíveis")

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

    def check_ollama_with_retry(self, max_retries: int = 3, wait_time: int = 5) -> bool:
        """Verifica se Ollama está rodando com retry logic"""
        print("🔍 Verificando conexão com Ollama...")

        for attempt in range(max_retries):
            try:
                response = requests.get("http://127.0.0.1:11434/api/tags", timeout=10)
                if response.status_code == 200:
                    print("✅ Ollama conectado com sucesso!")

                    # Verifica se modelo existe
                    models = response.json().get("models", [])
                    model_exists = any(self.model in m.get("name", "") for m in models)

                    if not model_exists:
                        print(f"⚠️ Modelo {self.model} não encontrado")
                        print(f"💡 Instale com: ollama pull {self.model}")
                    else:
                        print(f"✅ Modelo {self.model} disponível")

                    return True
                else:
                    print(f"  Tentativa {attempt + 1}/{max_retries}: Status {response.status_code}")
            except requests.exceptions.ConnectionError:
                print(f"  Tentativa {attempt + 1}/{max_retries}: Conexão recusada")
            except requests.exceptions.Timeout:
                print(f"  Tentativa {attempt + 1}/{max_retries}: Timeout")
            except Exception as e:
                print(f"  Tentativa {attempt + 1}/{max_retries}: Erro {type(e).__name__}")

            if attempt < max_retries - 1:
                print(f"  ⏳ Aguardando {wait_time}s antes de tentar novamente...")
                time.sleep(wait_time)

        print("\n❌ FALHA: Ollama não está respondendo após múltiplas tentativas")
        print("\n📝 SOLUÇÕES:")
        print("1. Verifique se Ollama está instalado: ollama --version")
        print("2. Inicie o servidor: ollama serve")
        print("3. Em outro terminal, teste: ollama list")
        print("4. Verifique se a porta 11434 está livre: lsof -i :11434")
        return False

    def read_file(self, file_path):
        """Método simples para ler arquivo"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            return None

    def cleanup_orphan_processes(self):
        """Limpa processos órfãos do Ollama"""
        print("🧹 Verificando processos órfãos...")

        try:
            result = subprocess.run(["ps", "aux"], capture_output=True, text=True)
            ollama_processes = []

            for line in result.stdout.split('\n'):
                if 'ollama' in line.lower() and 'grep' not in line:
                    parts = line.split()
                    if len(parts) > 1:
                        pid = parts[1]
                        cmd = ' '.join(parts[10:])[:50]  # Comando truncado
                        ollama_processes.append((pid, cmd))

            if ollama_processes:
                print(f"  Encontrados {len(ollama_processes)} processos Ollama")
                active = []
                for pid, cmd in ollama_processes:
                    try:
                        os.kill(int(pid), 0)
                        active.append((pid, cmd))
                        print(f"    PID {pid}: {cmd}")
                    except:
                        pass

                if len(active) > 1:
                    print(f"  ⚠️ Múltiplas instâncias detectadas!")
                    print("  💡 Para limpar: pkill ollama && sleep 2 && ollama serve")
                elif len(active) == 1:
                    print(f"  ✅ Uma instância ativa (PID: {active[0][0]})")
                else:
                    print("  ℹ️ Nenhum processo ativo")
            else:
                print("  ✅ Nenhum processo órfão encontrado")
        except Exception as e:
            print(f"  ⚠️ Erro ao verificar processos: {e}")

    def ollama_request(self, prompt: str, temperature: float = 0.5, max_retries: int = 2) -> Optional[str]:
        """Faz requisição ao Ollama com retry logic melhorado"""
        timeout = self.timeout  # Usa timeout configurável

        for attempt in range(max_retries):
            try:
                if attempt == 0:
                    print(f"  📡 Enviando request...")
                else:
                    print(f"  🔄 Retry {attempt}/{max_retries - 1}...")

                response = requests.post(
                    self.ollama_endpoint,
                    json={
                        "model": self.model,
                        "prompt": prompt,
                        "stream": False,
                        "temperature": temperature,
                        "top_p": 0.9,
                        "options": {
                            "num_ctx": 200000,
                            "num_thread": 14,
                            "num_gpu": 50,
                            "num_batch": 2048
                        }
                    },
                    timeout=timeout
                )

                if response.status_code == 200:
                    result = response.json().get("response", "")
                    if result:
                        print("  ✅ Resposta recebida com sucesso")
                    return result
                elif response.status_code == 404:
                    print(f"  ❌ Modelo {self.model} não encontrado")
                    print(f"  💡 Instale com: ollama pull {self.model}")
                    return None
                else:
                    print(f"  ⚠️ Status HTTP {response.status_code}")
                    if attempt < max_retries - 1:
                        print(f"  ⏳ Aguardando 5s antes de retry...")
                        time.sleep(5)

            except requests.exceptions.Timeout:
                print(f"  ⏱️ Timeout após {timeout}s")
                if attempt < max_retries - 1:
                    print(f"  🔄 Tentando com timeout menor...")
                    timeout = max(300, timeout // 2)  # Mínimo 5 minutos
                else:
                    print("  ❌ Análise muito demorada, considere simplificar o prompt")

            except requests.exceptions.ConnectionError:
                print(f"  ❌ Erro de conexão com Ollama")
                if attempt == 0:
                    print("  🔍 Tentando reconectar...")
                    if self.check_ollama_with_retry(max_retries=1):
                        continue
                print("  💡 Verifique se Ollama está rodando: ollama serve")
                return None

            except Exception as e:
                print(f"  ❌ Erro inesperado: {type(e).__name__}: {str(e)[:100]}")
                if attempt < max_retries - 1:
                    print(f"  ⏳ Aguardando 3s antes de retry...")
                    time.sleep(3)

        print("  ❌ Todas as tentativas falharam")
        return None

    def init_knowledge_db(self):
        """Inicializa banco de dados de conhecimento evolutivo"""

        conn = sqlite3.connect(self.knowledge_db)

        # WAL mode - mais robusto contra corrupção
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
                theory TEXT,
                similarity_score REAL,
                shared_patterns TEXT,
                differences TEXT,
                timestamp TEXT
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
        """Recupera conhecimento acumulado de ciclos anteriores"""
        conn = sqlite3.connect(self.knowledge_db)
        cursor = conn.cursor()

        # Pegar últimos insights mais relevantes
        cursor.execute("""
            SELECT content
            FROM insights
            WHERE confidence > 0.7
            ORDER BY insight_id DESC
            LIMIT 10
        """)
        insights = cursor.fetchall()

        # Pegar padrões mais frequentes
        cursor.execute("""
            SELECT description, occurrences
            FROM patterns
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

    def save_checkpoint(self, screenplay: str, theory: str, completed: list):
        """Salva checkpoint para retomar análise"""
        checkpoint = {
            'last_screenplay': screenplay,
            'last_theory': theory,
            'completed_analyses': completed,
            'completed_count': len(completed),
            'timestamp': datetime.now().isoformat(),
            'cycle': self.cycle_count
        }

        with open('checkpoint_analysis.json', 'w') as f:
            json.dump(checkpoint, f, indent=2)

        print(f"💾 Checkpoint salvo: {len(completed)} análises completadas")

    def load_checkpoint(self) -> dict:
        """Carrega checkpoint se existir"""
        checkpoint_file = Path('checkpoint_analysis.json')

        if checkpoint_file.exists():
            with open(checkpoint_file, 'r') as f:
                checkpoint = json.load(f)
                print(f"📂 Checkpoint carregado: {checkpoint['completed_count']} análises prévias")
                return checkpoint

        return {'completed_analyses': [], 'last_screenplay': None, 'last_theory': None}

    def extract_theory_techniques(self, theory_text: str, theory_name: str) -> dict:
        """Extrai técnicas principais de uma teoria usando Ollama"""

        print(f"  📚 Extraindo técnicas de {theory_name[:30]}...")

        # Limita texto para ser mais eficiente
        theory_excerpt = theory_text[:15000]  # 15K chars é suficiente

        # Prompt otimizado e focado
        prompt = f"""Analise esta teoria de roteiro e extraia AS TÉCNICAS PRINCIPAIS.

TEORIA: {theory_name}

TRECHO DO CONTEÚDO:
{theory_excerpt}

Extraia APENAS o essencial em JSON:
{{
  "theory_name": "{theory_name}",
  "main_techniques": [lista de 5-10 técnicas principais],
  "structural_elements": [elementos estruturais chave],
  "key_concepts": [conceitos fundamentais],
  "specific_beats": [beats narrativos se mencionados]
}}

Seja CONCISO e ESPECÍFICO."""

        try:
            response = self.ollama_request(prompt, temperature=0.3)

            if response and "{" in response:
                start = response.find("{")
                end = response.rfind("}") + 1
                if end > start:
                    if SAFE_PARSER_AVAILABLE:
                        result, confidence = safe_json_parse(response[start:end])
                        if confidence > 0.5:
                            print(f"    ✅ Técnicas extraídas (confiança: {confidence:.0%})")
                            return result
                    else:
                        result = json.loads(response[start:end])
                        print(f"    ✅ Técnicas extraídas com sucesso!")
                        return result
        except json.JSONDecodeError as e:
            if SAFE_PARSER_AVAILABLE:
                result, confidence = safe_json_parse(response)
                if confidence > 0.25:
                    print(f"    ⚠️ JSON recuperado com SafeParser (confiança: {confidence:.0%})")
                    return result
            print(f"    ⚠️ Erro ao decodificar JSON: {e}")
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
2. Dê 2-3 exemplos concretos com páginas/diálogos
3. Avalie aderência geral (0-1)

Responda em JSON simples:
{{
  "adherence": 0.0-1.0,
  "techniques_found": ["técnica1", "técnica2"],
  "key_examples": ["exemplo1 com página", "exemplo2 com diálogo"],
  "insight": "descoberta principal",
  "pattern": "padrão identificado"
}}"""

        return prompt

    def phase1_theory_analysis(self, max_theories: int = 10):
        """Fase 1: Análise de teorias de roteiro com checkpoint e validação"""

        print("\n🎬 FASE 1: ANÁLISE DE TEORIAS DE ROTEIRO")
        print("="*60)

        # Carrega checkpoint
        checkpoint = self.load_checkpoint()
        completed_analyses = checkpoint.get('completed_analyses', [])

        # Busca teorias disponíveis
        theory_files = list(self.theory_dir.glob("*.docx")) + \
                      list(self.theory_dir.glob("*.txt")) + \
                      list(self.theory_dir.glob("*.pdf"))

        # Busca roteiros profissionais para análise
        master_screenplays = list(self.masters_dir.glob("*"))

        if not theory_files:
            print("❌ Nenhuma teoria encontrada em 'theory/'")
            return

        if not master_screenplays:
            print("❌ Nenhum roteiro profissional encontrado em 'screenplays/masters/'")
            return

        print(f"📚 {len(theory_files)} teorias disponíveis")
        print(f"🎬 {len(master_screenplays)} roteiros profissionais para análise")

        # Limita número de teorias para teste
        theory_files = theory_files[:max_theories]

        analysis_count = 0

        for theory_file in theory_files:
            print(f"\n📖 Processando teoria: {theory_file.name}")

            # Lê conteúdo da teoria
            theory_content = self.read_file(str(theory_file))

            if not theory_content:
                print(f"  ⚠️ Não foi possível ler {theory_file.name}")
                continue

            # Extrai técnicas da teoria
            theory_data = self.extract_theory_techniques(
                theory_content,
                theory_file.stem
            )

            # Analisa cada roteiro com esta teoria
            for screenplay_file in master_screenplays[:3]:  # Top 3 roteiros por teoria

                # Cria chave única para esta análise
                analysis_key = f"{screenplay_file.name}||{theory_file.name}"

                # Pula se já foi analisada
                if analysis_key in completed_analyses:
                    print(f"  ⏭️ Pulando {screenplay_file.name} (já analisado)")
                    continue

                print(f"\n  🎬 Analisando: {screenplay_file.name}")

                # Lê roteiro
                screenplay_content = self.read_file(str(screenplay_file))
                if not screenplay_content:
                    print(f"    ⚠️ Não foi possível ler {screenplay_file.name}")
                    continue

                # Cria prompt especializado
                analysis_prompt = self.create_theory_based_prompt(
                    screenplay_content,
                    screenplay_file.stem,
                    theory_data
                )

                # Envia para Ollama com retry
                result = self.ollama_request(analysis_prompt, temperature=0.5)

                if result:
                    try:
                        # Parse resultado
                        if "{" in result:
                            start = result.find("{")
                            end = result.rfind("}") + 1
                            if SAFE_PARSER_AVAILABLE:
                                analysis, confidence = safe_json_parse(result[start:end])
                                if confidence < 0.5:
                                    print(f"    ⚠️ Análise com baixa confiança: {confidence:.0%}")
                            else:
                                analysis = json.loads(result[start:end])

                            # Salva no banco
                            self.save_analysis_result(
                                screenplay_file.name,
                                theory_file.name,
                                analysis
                            )

                            # Marca como completada
                            completed_analyses.append(analysis_key)
                            analysis_count += 1

                            # Salva checkpoint a cada análise
                            self.save_checkpoint(
                                screenplay_file.name,
                                theory_file.name,
                                completed_analyses
                            )

                            # Mostra resultado
                            print(f"    ✅ Aderência: {analysis.get('adherence', 0):.1%}")
                            print(f"    📝 Insight: {analysis.get('insight', 'N/A')[:100]}")

                    except Exception as e:
                        print(f"    ⚠️ Erro ao processar resultado: {e}")
                else:
                    print(f"    ❌ Falha na análise")

                # Pequena pausa entre análises
                time.sleep(2)

        print(f"\n✅ Fase 1 completa: {analysis_count} novas análises realizadas")
        print(f"📊 Total acumulado: {len(completed_analyses)} análises")

    def save_analysis_result(self, screenplay: str, theory: str, analysis: dict):
        """Salva resultado da análise no banco"""

        conn = sqlite3.connect(self.knowledge_db)
        cursor = conn.cursor()

        # Salva insight principal
        if 'insight' in analysis:
            cursor.execute("""
                INSERT INTO insights (cycle_id, type, content, confidence, timestamp)
                VALUES (?, ?, ?, ?, ?)
            """, (
                self.cycle_count,
                'theory_analysis',
                analysis['insight'],
                analysis.get('adherence', 0.5),
                datetime.now().isoformat()
            ))

        # Salva padrão descoberto
        if 'pattern' in analysis and analysis['pattern']:
            cursor.execute("""
                INSERT OR REPLACE INTO patterns
                (pattern_type, description, occurrences, examples, first_seen_cycle, last_seen_cycle)
                VALUES (?, ?,
                    COALESCE((SELECT occurrences FROM patterns WHERE description = ?), 0) + 1,
                    ?, ?, ?)
            """, (
                'structural',
                analysis['pattern'],
                analysis['pattern'],
                json.dumps(analysis.get('key_examples', [])),
                self.cycle_count,
                self.cycle_count
            ))

        conn.commit()
        conn.close()

    def run_continuous_learning(self, cycles: int = 1):
        """Executa ciclos de aprendizado contínuo"""

        print("\n" + "="*60)
        print("🚀 INICIANDO APRENDIZADO CONTÍNUO EVOLUTIVO")
        print(f"📊 Ciclo atual: #{self.cycle_count + 1}")
        print("="*60)

        for cycle in range(cycles):
            print(f"\n🔄 CICLO {self.cycle_count + cycle + 1}")
            print("-"*60)

            # Fase 1: Análise de teorias
            self.phase1_theory_analysis(max_theories=5)

            # Salva progresso do ciclo
            conn = sqlite3.connect(self.knowledge_db)
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO learning_cycles (timestamp, phase, insights_count, patterns_found)
                VALUES (?, ?,
                    (SELECT COUNT(*) FROM insights WHERE cycle_id = ?),
                    (SELECT COUNT(*) FROM patterns WHERE last_seen_cycle = ?))
            """, (
                datetime.now().isoformat(),
                'theory_analysis',
                self.cycle_count + cycle + 1,
                self.cycle_count + cycle + 1
            ))

            conn.commit()
            conn.close()

            print(f"\n✅ Ciclo {self.cycle_count + cycle + 1} completo!")

        print("\n" + "="*60)
        print("🎯 APRENDIZADO CONTÍNUO FINALIZADO")
        print(f"📊 Total de ciclos executados: {cycles}")
        print("="*60)

def main():
    """Função principal"""
    import argparse
    from process_lock import ProcessLock

    parser = argparse.ArgumentParser(description='Sistema de Aprendizado Contínuo Ollama v2.0')
    parser.add_argument('--cycles', type=int, default=1, help='Número de ciclos de aprendizado')
    parser.add_argument('--model', type=str, default='mixtral-cpu-force:latest',
                       help='Modelo Ollama a usar')

    args = parser.parse_args()

    # Executar sem lock problemático
    print("🚀 Executando análise...")
    learner = OllamaContinuousLearning(model=args.model)
    learner.run_continuous_learning(cycles=args.cycles)

if __name__ == "__main__":
    main()