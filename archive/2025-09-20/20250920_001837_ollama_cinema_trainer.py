#!/usr/bin/env python3
"""
🎬🧠 OLLAMA CINEMA TRAINER - Sistema de Aprendizado Contínuo
Treina modelos Ollama com conhecimento cinematográfico extraído de TXTs
Evolui modelfiles com conhecimento acumulado
Integrado ao sistema ScriptDoctorSystem
"""

import json
import time
import hashlib
import sqlite3
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime
import asyncio
import re

@dataclass
class CinemaKnowledge:
    """Conhecimento cinematográfico extraído"""
    concept: str
    source: str
    confidence: float
    examples: List[str]
    embeddings: Optional[Dict] = None
    timestamp: datetime = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()

@dataclass
class TrainingSession:
    """Sessão de treinamento com Ollama"""
    session_id: str
    model_name: str
    documents_processed: int
    knowledge_extracted: int
    modelfile_updates: List[str]
    duration_seconds: float
    timestamp: datetime

class OllamaCinemaTrainer:
    """
    Sistema de treinamento contínuo para Ollama
    Aprende com PDFs de teoria cinematográfica e roteiros
    """

    def __init__(self):
        self.data_dir = Path("/Users/clubproducoes/Digimundo/scripturemon-champion/data")
        self.modelfiles_dir = self.data_dir / "models" / "modelfiles"
        self.knowledge_base = []

        # Usar sistema unificado de memória
        try:
            from src.core.unified_memory_system import get_unified_memory
            self.memory = get_unified_memory().get_learning_adapter()
            self.use_unified = True
            print("✅ Using Unified Memory System")
        except:
            # Fallback para DB próprio
            self.learning_db = self.data_dir / "cinema_learning.db"
            self.use_unified = False
            self.init_database()

    def init_database(self):
        """Inicializa banco de conhecimento cinematográfico"""
        conn = sqlite3.connect(self.learning_db)
        cursor = conn.cursor()

        # Tabela de conhecimento
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cinema_knowledge (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                concept TEXT NOT NULL,
                source TEXT NOT NULL,
                confidence REAL,
                examples TEXT,
                embeddings TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Tabela de sessões de treinamento
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS training_sessions (
                session_id TEXT PRIMARY KEY,
                model_name TEXT,
                documents_processed INTEGER,
                knowledge_extracted INTEGER,
                modelfile_updates TEXT,
                duration_seconds REAL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Tabela de evolução de modelos
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS model_evolution (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                model_name TEXT,
                generation INTEGER,
                parent_model TEXT,
                fitness_score REAL,
                knowledge_concepts INTEGER,
                system_prompt TEXT,
                parameters TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)

        conn.commit()
        conn.close()

    async def extract_knowledge_from_text(self, text: str, source: str) -> List[CinemaKnowledge]:
        """
        Extrai conhecimento cinematográfico de texto
        Usa Ollama para identificar conceitos, técnicas e padrões
        """
        knowledge_items = []

        # Prompts especializados para diferentes tipos de conhecimento
        extraction_prompts = {
            "narrative_techniques": """
                Identify narrative techniques in this text.
                Focus on: story structure, plot devices, narrative patterns.
                Format: TECHNIQUE: description | EXAMPLE: specific example
            """,
            "character_patterns": """
                Extract character development patterns.
                Focus on: archetypes, arcs, relationships, psychology.
                Format: PATTERN: description | APPLICATION: how to use
            """,
            "cinematic_elements": """
                Find cinematic techniques and visual storytelling elements.
                Focus on: camera work, editing, visual metaphors, mise-en-scène.
                Format: ELEMENT: description | EFFECT: impact on audience
            """,
            "dialogue_techniques": """
                Analyze dialogue writing techniques.
                Focus on: subtext, voice, rhythm, exposition.
                Format: TECHNIQUE: description | EXAMPLE: dialogue sample
            """,
            "thematic_concepts": """
                Identify thematic concepts and philosophical ideas.
                Focus on: themes, symbols, metaphors, meaning.
                Format: THEME: concept | IMPLEMENTATION: how it appears
            """
        }

        # Processar cada tipo de conhecimento
        for knowledge_type, prompt in extraction_prompts.items():
            try:
                # Usar producer_director para evitar conflitos
                from src.core.producer_director_minimal import ProducerDirectorMinimal
                producer = ProducerDirectorMinimal()

                # Dividir texto em chunks se muito longo
                chunk_size = 4000
                text_chunk = text[:chunk_size] if len(text) > chunk_size else text

                full_prompt = f"{prompt}\n\nText to analyze:\n{text_chunk}"

                # Usar Producer-Director para extrair conhecimento
                response = producer.process(
                    prompt=full_prompt,
                    multi_model=False  # Single model para extração
                )

                # Processar resposta
                if response:
                    lines = response.split('\n')
                    for line in lines:
                        if ':' in line:
                            parts = line.split('|')
                            if len(parts) >= 1:
                                concept_part = parts[0].split(':')
                                if len(concept_part) >= 2:
                                    concept = concept_part[1].strip()
                                    examples = [p.strip() for p in parts[1:] if p.strip()]

                                    knowledge = CinemaKnowledge(
                                        concept=concept,
                                        source=f"{source}:{knowledge_type}",
                                        confidence=0.8,
                                        examples=examples
                                    )
                                    knowledge_items.append(knowledge)

            except Exception as e:
                print(f"⚠️ Error extracting {knowledge_type}: {e}")

        return knowledge_items

# UNUSED - Candidate for removal
#     def update_modelfile_with_knowledge(self, model_name: str, knowledge_items: List[CinemaKnowledge]) -> str:
        """
        Atualiza modelfile com conhecimento acumulado
        Cria system prompt enriquecido com conceitos aprendidos
        """

        # Agrupar conhecimento por tipo
        narrative_concepts = []
        character_concepts = []
        cinematic_concepts = []
        dialogue_concepts = []
        thematic_concepts = []

        for item in knowledge_items:
            if "narrative" in item.source.lower():
                narrative_concepts.append(item.concept)
            elif "character" in item.source.lower():
                character_concepts.append(item.concept)
            elif "cinematic" in item.source.lower():
                cinematic_concepts.append(item.concept)
            elif "dialogue" in item.source.lower():
                dialogue_concepts.append(item.concept)
            elif "thematic" in item.source.lower():
                thematic_concepts.append(item.concept)

        # Criar system prompt enriquecido
        enriched_prompt = f"""You are an expert screenplay analyst with deep knowledge acquired through continuous learning.

Your specialized knowledge includes:

NARRATIVE TECHNIQUES:
{chr(10).join(f'- {c}' for c in narrative_concepts[:10])}

CHARACTER DEVELOPMENT:
{chr(10).join(f'- {c}' for c in character_concepts[:10])}

CINEMATIC ELEMENTS:
{chr(10).join(f'- {c}' for c in cinematic_concepts[:10])}

DIALOGUE MASTERY:
{chr(10).join(f'- {c}' for c in dialogue_concepts[:10])}

THEMATIC UNDERSTANDING:
{chr(10).join(f'- {c}' for c in thematic_concepts[:10])}

Apply this accumulated knowledge to provide deep, insightful analysis.
Reference specific techniques and concepts when relevant.
Your analysis should demonstrate mastery of cinematic storytelling.
"""

        # Criar novo modelfile
        modelfile_content = f"""FROM llama3.2:3b

SYSTEM "{enriched_prompt}"

PARAMETER temperature 0.7
PARAMETER num_ctx 16384
PARAMETER num_thread 8
PARAMETER top_k 40
PARAMETER top_p 0.9
PARAMETER repeat_penalty 1.1

# Knowledge base: {len(knowledge_items)} concepts learned
# Last updated: {datetime.now().isoformat()}
"""

        # Salvar modelfile
        modelfile_path = self.modelfiles_dir / f"{model_name}_evolved.modelfile"
        modelfile_path.write_text(modelfile_content)

        return str(modelfile_path)

    def save_knowledge_to_memory(self, knowledge_items: List[CinemaKnowledge]):
        """Salva conhecimento no sistema de memória"""
        if self.use_unified:
            # Usar sistema unificado
            for item in knowledge_items:
                self.memory.save_knowledge(
                    concept=item.concept,
                    confidence=item.confidence,
                    examples=item.examples
                )
        else:
            # Fallback para DB próprio
            conn = sqlite3.connect(self.learning_db)
            cursor = conn.cursor()

            for item in knowledge_items:
                cursor.execute("""
                    INSERT INTO cinema_knowledge (concept, source, confidence, examples)
                    VALUES (?, ?, ?, ?)
                """, (
                    item.concept,
                    item.source,
                    item.confidence,
                    json.dumps(item.examples)
                ))

            conn.commit()
            conn.close()

    def get_accumulated_knowledge(self, min_confidence: float = 0.7) -> List[CinemaKnowledge]:
        """Recupera conhecimento acumulado"""
        if self.use_unified:
            # Usar sistema unificado
            entries = self.memory.get_knowledge(min_confidence)
            knowledge_items = []
            for entry in entries[:500]:
                if isinstance(entry.value, dict):
                    knowledge = CinemaKnowledge(
                        concept=entry.value.get('concept', entry.key),
                        source=entry.source,
                        confidence=entry.confidence,
                        examples=entry.value.get('examples', [])
                    )
                    knowledge_items.append(knowledge)
            return knowledge_items
        else:
            # Fallback para DB próprio
            conn = sqlite3.connect(self.learning_db)
            cursor = conn.cursor()

            cursor.execute("""
                SELECT concept, source, confidence, examples
                FROM cinema_knowledge
                WHERE confidence >= ?
                ORDER BY confidence DESC, timestamp DESC
                LIMIT 500
            """, (min_confidence,))

            knowledge_items = []
            for row in cursor.fetchall():
                knowledge = CinemaKnowledge(
                    concept=row[0],
                    source=row[1],
                    confidence=row[2],
                    examples=json.loads(row[3]) if row[3] else []
                )
                knowledge_items.append(knowledge)

            conn.close()
            return knowledge_items

    async def train_on_document(self, document_path: Path) -> List[CinemaKnowledge]:
        """Treina com um documento específico (TXT já convertido)"""
        print(f"📚 Training on: {document_path.name}")

        # Carregar texto (assumir TXT já convertido manualmente)
        if document_path.suffix == '.txt':
            text = document_path.read_text(encoding='utf-8')
        elif document_path.suffix == '.pdf':
            # Procurar versão TXT correspondente
            txt_path = document_path.with_suffix('.txt')
            if txt_path.exists():
                text = txt_path.read_text(encoding='utf-8')
            else:
                print(f"ℹ️ TXT version not found for {document_path.name}")
                print(f"   Please convert manually first")
                return []
        else:
            print(f"⚠️ Unsupported format: {document_path.suffix}")
            return []

        # Extrair conhecimento
        knowledge = await self.extract_knowledge_from_text(
            text,
            document_path.stem
        )

        # Salvar no banco
        if knowledge:
            self.save_knowledge_to_memory(knowledge)
            print(f"✅ Extracted {len(knowledge)} knowledge items")

        return knowledge

    async def evolve_model(self, base_model: str = "scripturemon-cpu-themes") -> str:
        """
        Evolui um modelo com conhecimento acumulado
        Cria nova geração de modelfile
        """
        print(f"🧬 Evolving model: {base_model}")

        # Recuperar conhecimento acumulado
        knowledge = self.get_accumulated_knowledge()
        print(f"📊 Using {len(knowledge)} knowledge concepts")

        # Atualizar modelfile
        new_modelfile = self.update_modelfile_with_knowledge(base_model, knowledge)

        # Registrar evolução
        conn = sqlite3.connect(self.learning_db)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO model_evolution (
                model_name, generation, parent_model,
                fitness_score, knowledge_concepts
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            f"{base_model}_evolved",
            1,  # Generation
            base_model,
            0.85,  # Fitness score
            len(knowledge)
        ))

        conn.commit()
        conn.close()

        print(f"✅ Created evolved model: {new_modelfile}")
        return new_modelfile

    async def continuous_learning_session(self, duration_minutes: int = 30):
        """
        Sessão de aprendizado contínuo
        Processa documentos e evolui modelos
        """
        session_id = hashlib.md5(str(time.time()).encode()).hexdigest()[:8]
        start_time = time.time()
        end_time = start_time + (duration_minutes * 60)

        print(f"🎓 Starting learning session: {session_id}")
        print(f"⏱️ Duration: {duration_minutes} minutes")

        documents_processed = 0
        total_knowledge = []

        # Processar documentos de teoria
        theory_dir = self.data_dir / "screenplays"
        if theory_dir.exists():
            txt_files = list(theory_dir.glob("*.txt"))[:5]  # Limitar para teste

            for txt_file in txt_files:
                if time.time() > end_time:
                    break

                knowledge = await self.train_on_document(txt_file)
                total_knowledge.extend(knowledge)
                documents_processed += 1

                # Pequena pausa entre documentos
                await asyncio.sleep(2)

        # Evoluir modelos com conhecimento
        if total_knowledge:
            await self.evolve_model("scripturemon-cpu-themes")
            await self.evolve_model("scripturemon-cpu-structure")

        # Registrar sessão
        session = TrainingSession(
            session_id=session_id,
            model_name="cinema-learner",
            documents_processed=documents_processed,
            knowledge_extracted=len(total_knowledge),
            modelfile_updates=["themes_evolved", "structure_evolved"],
            duration_seconds=time.time() - start_time,
            timestamp=datetime.now()
        )

        # Salvar sessão
        conn = sqlite3.connect(self.learning_db)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO training_sessions VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            session.session_id,
            session.model_name,
            session.documents_processed,
            session.knowledge_extracted,
            json.dumps(session.modelfile_updates),
            session.duration_seconds,
            session.timestamp
        ))

        conn.commit()
        conn.close()

        print(f"\n📊 Session Complete!")
        print(f"  Documents: {documents_processed}")
        print(f"  Knowledge: {len(total_knowledge)} concepts")
        print(f"  Duration: {session.duration_seconds:.1f}s")

        return session

async def main():
    """Demo do sistema de treinamento"""
    trainer = OllamaCinemaTrainer()

    # Sessão de aprendizado de 5 minutos
    session = await trainer.continuous_learning_session(duration_minutes=5)

    print("\n🎬 Cinema Training Complete!")
    print(f"Knowledge base enriched with cinematic concepts")
    print(f"Models evolved with accumulated wisdom")

if __name__ == "__main__":
    asyncio.run(main())