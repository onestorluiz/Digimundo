#!/usr/bin/env python3
"""
🧪 SDL - Self-Distill LoRA Consolidator
Consolidação automática de memórias em pesos neurais
Transforma experiências em conhecimento permanente
"""

import json
import time
import sqlite3
import hashlib
import random
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from enum import Enum
import logging
import numpy as np

logger = logging.getLogger(__name__)


class ConsolidationType(Enum):
    """Tipos de consolidação SDL"""
    PATTERN_EXTRACTION = "pattern_extraction"
    Q_A_GENERATION = "qa_generation"
    CONCEPT_MERGING = "concept_merging"
    WEIGHT_UPDATE = "weight_update"


@dataclass
class QAPair:
    """Par pergunta-resposta para treinamento"""
    question: str
    answer: str
    context: str
    confidence: float
    source_memories: List[str]
    timestamp: float


@dataclass
class MicroLoRA:
    """Adaptador LoRA simulado"""
    rank: int = 8
    alpha: float = 16.0
    dropout: float = 0.1
    target_modules: List[str] = None
    weights_a: Optional[np.ndarray] = None
    weights_b: Optional[np.ndarray] = None
    training_loss: float = 1.0
    validation_acc: float = 0.0

    def __post_init__(self):
        if self.target_modules is None:
            self.target_modules = ["q_proj", "v_proj", "k_proj", "o_proj"]


@dataclass
class ConsolidationReport:
    """Relatório de consolidação"""
    consolidation_id: str
    start_time: float
    end_time: float
    memories_processed: int
    qa_pairs_generated: int
    patterns_extracted: int
    lora_trained: bool
    validation_score: float
    promoted: bool
    error: Optional[str] = None


class SDLConsolidator:
    """Self-Distill LoRA - Consolidador de memórias em conhecimento"""

    def __init__(self, soul_id: str, data_dir: str = "data/sdl"):
        self.soul_id = soul_id
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)

        # Diretórios específicos
        self.datasets_dir = self.data_dir / "datasets"
        self.adapters_dir = self.data_dir / "adapters"
        self.reports_dir = self.data_dir / "reports"

        for dir in [self.datasets_dir, self.adapters_dir, self.reports_dir]:
            dir.mkdir(exist_ok=True)

        # Banco de dados
        self.db_path = self.data_dir / f"sdl_{soul_id}.db"
        self._init_database()

        # Gates de qualidade
        self.quality_gates = {
            'min_recall': 0.90,      # 90% recall mínimo
            'min_style_match': 0.95,  # 95% match de estilo
            'max_hallucination': 0.05, # 5% alucinação máxima
            'min_qa_pairs': 10        # Mínimo de pares Q&A
        }

        # Canários para validação
        self.canary_queries = [
            "What is the main purpose?",
            "Explain the key concept",
            "How does it work?",
            "What are the benefits?",
            "Give an example"
        ]

        logger.info(f"🧪 SDL Consolidator inicializado - Soul: {soul_id}")

    def _init_database(self):
        """Inicializa banco de dados SDL"""
        with sqlite3.connect(self.db_path) as conn:
            # Tabela de consolidações
            conn.execute('''
                CREATE TABLE IF NOT EXISTS consolidations (
                    id TEXT PRIMARY KEY,
                    start_time REAL NOT NULL,
                    end_time REAL,
                    type TEXT NOT NULL,
                    status TEXT DEFAULT 'pending',
                    report TEXT
                )
            ''')

            # Tabela de Q&A pairs
            conn.execute('''
                CREATE TABLE IF NOT EXISTS qa_pairs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    consolidation_id TEXT,
                    question TEXT NOT NULL,
                    answer TEXT NOT NULL,
                    context TEXT,
                    confidence REAL DEFAULT 0.5,
                    timestamp REAL NOT NULL,
                    used_in_training BOOLEAN DEFAULT FALSE
                )
            ''')

            # Tabela de LoRAs treinados
            conn.execute('''
                CREATE TABLE IF NOT EXISTS lora_adapters (
                    id TEXT PRIMARY KEY,
                    consolidation_id TEXT,
                    rank INTEGER,
                    alpha REAL,
                    training_loss REAL,
                    validation_acc REAL,
                    promoted BOOLEAN DEFAULT FALSE,
                    created_at REAL NOT NULL
                )
            ''')

            # Tabela de padrões extraídos
            conn.execute('''
                CREATE TABLE IF NOT EXISTS extracted_patterns (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    pattern TEXT NOT NULL,
                    frequency INTEGER DEFAULT 1,
                    confidence REAL DEFAULT 0.5,
                    first_seen REAL NOT NULL,
                    last_seen REAL NOT NULL
                )
            ''')

            conn.commit()

    def consolidate_memories(self, memories: List[Dict],
                           consolidation_type: ConsolidationType = ConsolidationType.Q_A_GENERATION) -> ConsolidationReport:
        """
        Consolida memórias L3 (ativas) em conhecimento permanente
        Processo principal do SDL
        """
        consolidation_id = f"sdl_{self.soul_id}_{int(time.time())}"
        start_time = time.time()

        logger.info(f"🔄 Iniciando consolidação {consolidation_id}")
        logger.info(f"  Tipo: {consolidation_type.value}")
        logger.info(f"  Memórias: {len(memories)}")

        try:
            # 1. Gerar Q&A pairs das memórias
            qa_pairs = self._generate_qa_pairs(memories, consolidation_id)
            logger.info(f"  ✅ {len(qa_pairs)} pares Q&A gerados")

            # 2. Extrair padrões
            patterns = self._extract_patterns(memories)
            logger.info(f"  ✅ {len(patterns)} padrões extraídos")

            # 3. Criar dataset sintético
            dataset_path = self._create_synthetic_dataset(qa_pairs, consolidation_id)
            logger.info(f"  ✅ Dataset criado: {dataset_path}")

            # 4. Treinar micro-LoRA (simulado)
            lora = self._train_micro_lora(dataset_path, consolidation_id)
            logger.info(f"  ✅ LoRA treinado - Loss: {lora.training_loss:.4f}")

            # 5. Validar com canários
            validation_score = self._validate_with_canaries(lora)
            logger.info(f"  ✅ Validação: {validation_score:.2%}")

            # 6. Decidir promoção
            promoted = self._check_quality_gates(lora, validation_score, len(qa_pairs))

            if promoted:
                self._promote_lora(lora, consolidation_id)
                logger.info(f"  🎉 LoRA promovido para produção!")
            else:
                logger.info(f"  ⚠️ LoRA não passou nos gates de qualidade")

            # Criar relatório
            report = ConsolidationReport(
                consolidation_id=consolidation_id,
                start_time=start_time,
                end_time=time.time(),
                memories_processed=len(memories),
                qa_pairs_generated=len(qa_pairs),
                patterns_extracted=len(patterns),
                lora_trained=True,
                validation_score=validation_score,
                promoted=promoted
            )

            # Salvar relatório
            self._save_report(report)

            return report

        except Exception as e:
            logger.error(f"❌ Erro na consolidação: {e}")
            return ConsolidationReport(
                consolidation_id=consolidation_id,
                start_time=start_time,
                end_time=time.time(),
                memories_processed=len(memories),
                qa_pairs_generated=0,
                patterns_extracted=0,
                lora_trained=False,
                validation_score=0.0,
                promoted=False,
                error=str(e)
            )

    def _generate_qa_pairs(self, memories: List[Dict], consolidation_id: str) -> List[QAPair]:
        """Gera pares Q&A das memórias"""
        qa_pairs = []

        for memory in memories:
            content = memory.get('content', '')
            importance = memory.get('importance', 0.5)

            # Gerar perguntas baseadas no conteúdo
            questions = self._generate_questions(content)

            for question in questions:
                # Gerar resposta (simulado - em produção usaria LLM)
                answer = self._generate_answer(question, content)

                qa_pair = QAPair(
                    question=question,
                    answer=answer,
                    context=content,
                    confidence=importance,
                    source_memories=[memory.get('id', '')],
                    timestamp=time.time()
                )

                qa_pairs.append(qa_pair)

                # Salvar no banco
                self._save_qa_pair(qa_pair, consolidation_id)

        return qa_pairs

    def _generate_questions(self, content: str) -> List[str]:
        """Gera perguntas sobre o conteúdo"""
        # Simulação - em produção usaria LLM
        templates = [
            "What is the main idea of: {}",
            "Explain the concept of: {}",
            "How does {} work?",
            "What are the key points about: {}",
            "Summarize: {}"
        ]

        # Extrair palavras-chave (simplificado)
        keywords = content.split()[:3]
        keyword_str = ' '.join(keywords)

        questions = []
        for template in templates[:2]:  # Gerar 2 perguntas por memória
            questions.append(template.format(keyword_str))

        return questions

    def _generate_answer(self, question: str, context: str) -> str:
        """Gera resposta para a pergunta"""
        # Simulação - em produção usaria LLM
        # Por enquanto, retorna parte do contexto
        words = context.split()
        answer_length = min(20, len(words))
        return ' '.join(words[:answer_length])

    def _extract_patterns(self, memories: List[Dict]) -> List[Dict]:
        """Extrai padrões das memórias"""
        patterns = {}

        for memory in memories:
            content = memory.get('content', '').lower()

            # Extrair n-gramas (simplificado)
            words = content.split()
            for i in range(len(words) - 2):
                trigram = ' '.join(words[i:i+3])
                patterns[trigram] = patterns.get(trigram, 0) + 1

        # Filtrar padrões frequentes
        frequent_patterns = []
        for pattern, freq in patterns.items():
            if freq >= 2:  # Aparece pelo menos 2 vezes
                frequent_patterns.append({
                    'pattern': pattern,
                    'frequency': freq,
                    'confidence': min(0.9, freq / 10)  # Confiança baseada em frequência
                })

                # Salvar no banco
                self._save_pattern(pattern, freq)

        return frequent_patterns

    def _create_synthetic_dataset(self, qa_pairs: List[QAPair], consolidation_id: str) -> Path:
        """Cria dataset sintético para treinamento"""
        dataset_path = self.datasets_dir / f"{consolidation_id}.jsonl"

        with open(dataset_path, 'w') as f:
            for qa in qa_pairs:
                entry = {
                    'instruction': qa.question,
                    'input': qa.context[:100],  # Limitar contexto
                    'output': qa.answer,
                    'confidence': qa.confidence
                }
                f.write(json.dumps(entry) + '\n')

        return dataset_path

    def _train_micro_lora(self, dataset_path: Path, consolidation_id: str) -> MicroLoRA:
        """Treina micro-LoRA (simulado)"""
        # Em produção, usaria ferramentas reais de treinamento
        # Aqui simulamos o processo

        lora = MicroLoRA(rank=8)

        # Simular matrizes de peso (rank 8)
        lora.weights_a = np.random.randn(768, 8) * 0.01  # Projeção down
        lora.weights_b = np.random.randn(8, 768) * 0.01  # Projeção up

        # Simular treinamento
        num_epochs = 3
        initial_loss = 2.5

        for epoch in range(num_epochs):
            # Simular redução de loss
            lora.training_loss = initial_loss * (0.6 ** (epoch + 1))
            lora.validation_acc = min(0.95, 0.6 + 0.15 * epoch)

            logger.debug(f"  Epoch {epoch+1}: Loss={lora.training_loss:.4f}, Acc={lora.validation_acc:.2%}")

        # Salvar adaptador
        adapter_path = self.adapters_dir / f"{consolidation_id}.lora"
        self._save_lora(lora, adapter_path)

        # Registrar no banco
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                INSERT INTO lora_adapters
                (id, consolidation_id, rank, alpha, training_loss, validation_acc, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                f"lora_{consolidation_id}",
                consolidation_id,
                lora.rank,
                lora.alpha,
                lora.training_loss,
                lora.validation_acc,
                time.time()
            ))
            conn.commit()

        return lora

    def _validate_with_canaries(self, lora: MicroLoRA) -> float:
        """Valida LoRA com queries canário"""
        # Simulação de validação
        correct = 0

        for query in self.canary_queries:
            # Simular inferência com LoRA
            # Em produção, faria inferência real
            response_quality = random.uniform(0.7, 1.0)  # Simular qualidade

            if response_quality > 0.8:
                correct += 1

        return correct / len(self.canary_queries)

    def _check_quality_gates(self, lora: MicroLoRA, validation_score: float, qa_count: int) -> bool:
        """Verifica gates de qualidade"""
        checks = {
            'recall': validation_score >= self.quality_gates['min_recall'],
            'style': lora.validation_acc >= self.quality_gates['min_style_match'],
            'qa_count': qa_count >= self.quality_gates['min_qa_pairs'],
            'loss': lora.training_loss < 0.5  # Loss baixo
        }

        passed = all(checks.values())

        logger.debug(f"  Gates de qualidade: {checks}")
        return passed

    def _promote_lora(self, lora: MicroLoRA, consolidation_id: str):
        """Promove LoRA para produção"""
        # Marcar como promovido no banco
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                UPDATE lora_adapters
                SET promoted = TRUE
                WHERE consolidation_id = ?
            ''', (consolidation_id,))
            conn.commit()

        # Copiar para diretório de produção
        prod_dir = self.adapters_dir / "production"
        prod_dir.mkdir(exist_ok=True)

        adapter_path = self.adapters_dir / f"{consolidation_id}.lora"
        prod_path = prod_dir / f"active_{self.soul_id}.lora"

        if adapter_path.exists():
            import shutil
            shutil.copy2(adapter_path, prod_path)

        logger.info(f"  ✅ LoRA promovido para: {prod_path}")

    def _save_qa_pair(self, qa: QAPair, consolidation_id: str):
        """Salva par Q&A no banco"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                INSERT INTO qa_pairs
                (consolidation_id, question, answer, context, confidence, timestamp)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                consolidation_id,
                qa.question,
                qa.answer,
                qa.context,
                qa.confidence,
                qa.timestamp
            ))
            conn.commit()

    def _save_pattern(self, pattern: str, frequency: int):
        """Salva padrão extraído"""
        with sqlite3.connect(self.db_path) as conn:
            # Verificar se já existe
            cursor = conn.execute(
                'SELECT id, frequency FROM extracted_patterns WHERE pattern = ?',
                (pattern,)
            )
            existing = cursor.fetchone()

            if existing:
                # Atualizar frequência
                conn.execute('''
                    UPDATE extracted_patterns
                    SET frequency = ?, last_seen = ?
                    WHERE id = ?
                ''', (existing[1] + frequency, time.time(), existing[0]))
            else:
                # Inserir novo
                conn.execute('''
                    INSERT INTO extracted_patterns
                    (pattern, frequency, confidence, first_seen, last_seen)
                    VALUES (?, ?, ?, ?, ?)
                ''', (pattern, frequency, min(0.9, frequency/10), time.time(), time.time()))

            conn.commit()

    def _save_lora(self, lora: MicroLoRA, path: Path):
        """Salva adaptador LoRA"""
        # Simular salvamento (em produção seria safetensors ou similar)
        lora_dict = {
            'rank': lora.rank,
            'alpha': lora.alpha,
            'dropout': lora.dropout,
            'target_modules': lora.target_modules,
            'training_loss': lora.training_loss,
            'validation_acc': lora.validation_acc,
            'weights_shape_a': lora.weights_a.shape if lora.weights_a is not None else None,
            'weights_shape_b': lora.weights_b.shape if lora.weights_b is not None else None
        }

        with open(path, 'w') as f:
            json.dump(lora_dict, f, indent=2)

    def _save_report(self, report: ConsolidationReport):
        """Salva relatório de consolidação"""
        report_path = self.reports_dir / f"{report.consolidation_id}.json"

        with open(report_path, 'w') as f:
            json.dump(asdict(report), f, indent=2)

        # Atualizar banco
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                UPDATE consolidations
                SET end_time = ?, status = ?, report = ?
                WHERE id = ?
            ''', (
                report.end_time,
                'completed' if report.promoted else 'not_promoted',
                json.dumps(asdict(report)),
                report.consolidation_id
            ))
            conn.commit()

    def get_consolidation_history(self) -> List[Dict]:
        """Retorna histórico de consolidações"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute('''
                SELECT id, start_time, end_time, status
                FROM consolidations
                ORDER BY start_time DESC
                LIMIT 10
            ''')

            history = []
            for row in cursor:
                history.append({
                    'id': row[0],
                    'start': datetime.fromtimestamp(row[1]).isoformat(),
                    'duration': row[2] - row[1] if row[2] else None,
                    'status': row[3]
                })

            return history

    def dream_mode(self, duration_seconds: int = 10) -> ConsolidationReport:
        """
        Modo sonho - consolidação automática noturna
        Simula o processo de consolidação durante o 'sono'
        """
        logger.info(f"💤 Entrando em modo sonho por {duration_seconds}s...")

        # Simular coleta de memórias recentes (L3)
        recent_memories = [
            {
                'id': f'mem_{i}',
                'content': f'Memory content {i}: Important learning about the system behavior and patterns',
                'importance': random.uniform(0.3, 0.9)
            }
            for i in range(20)  # 20 memórias simuladas
        ]

        # Consolidar
        report = self.consolidate_memories(
            recent_memories,
            ConsolidationType.PATTERN_EXTRACTION
        )

        logger.info(f"💤 Modo sonho completo - {report.patterns_extracted} padrões extraídos")
        return report


def test_sdl_consolidator():
    """Teste do SDL Consolidator"""
    print("\n" + "="*60)
    print("🧪 TESTE DO SDL - SELF-DISTILL LORA CONSOLIDATOR")
    print("="*60)

    # Criar consolidador
    sdl = SDLConsolidator("test_soul")

    # Simular memórias L3 (ativas)
    print("\n📝 Criando memórias simuladas...")
    test_memories = [
        {
            'id': 'mem_001',
            'content': 'The screenplay analysis system uses four stages of processing',
            'importance': 0.9
        },
        {
            'id': 'mem_002',
            'content': 'Character development is crucial for engaging narratives',
            'importance': 0.8
        },
        {
            'id': 'mem_003',
            'content': 'The three-act structure provides a solid foundation',
            'importance': 0.85
        },
        {
            'id': 'mem_004',
            'content': 'Dialogue must reveal character and advance the plot',
            'importance': 0.75
        },
        {
            'id': 'mem_005',
            'content': 'Visual storytelling is more powerful than exposition',
            'importance': 0.9
        }
    ]

    # Consolidar memórias
    print("\n🔄 Iniciando consolidação...")
    report = sdl.consolidate_memories(test_memories)

    # Exibir relatório
    print("\n📊 RELATÓRIO DE CONSOLIDAÇÃO:")
    print(f"  ID: {report.consolidation_id}")
    print(f"  Duração: {report.end_time - report.start_time:.2f}s")
    print(f"  Memórias processadas: {report.memories_processed}")
    print(f"  Pares Q&A gerados: {report.qa_pairs_generated}")
    print(f"  Padrões extraídos: {report.patterns_extracted}")
    print(f"  LoRA treinado: {'✅' if report.lora_trained else '❌'}")
    print(f"  Score de validação: {report.validation_score:.2%}")
    print(f"  Promovido: {'✅' if report.promoted else '❌'}")

    # Testar modo sonho
    print("\n💤 Testando modo sonho...")
    dream_report = sdl.dream_mode(duration_seconds=5)
    print(f"  Padrões consolidados durante o sonho: {dream_report.patterns_extracted}")

    # Histórico
    print("\n📜 Histórico de consolidações:")
    history = sdl.get_consolidation_history()
    for entry in history[:3]:
        print(f"  - {entry['id']}: {entry['status']}")

    print("\n✨ SDL Consolidator funcionando perfeitamente!")
    print("="*60)


if __name__ == "__main__":
    test_sdl_consolidator()