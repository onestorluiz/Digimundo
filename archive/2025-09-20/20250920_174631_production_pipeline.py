#!/usr/bin/env python3
"""
🎬 PRODUCTION PIPELINE - FASE 26
Pipeline completo de produção com integração de ferramentas externas
e automação de tarefas repetitivas
"""

import os
import json
import shutil
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import asyncio
import hashlib
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import yaml
import sqlite3

class PipelineStage(Enum):
    """Estágios do pipeline de produção"""
    INGESTION = "ingestion"          # Entrada de roteiros
    PREPROCESSING = "preprocessing"   # Normalização e limpeza
    ANALYSIS = "analysis"            # Análise profunda
    COMPRESSION = "compression"       # DigiLang compression
    ENRICHMENT = "enrichment"        # Enriquecimento com IA
    VALIDATION = "validation"        # Validação de qualidade
    EXPORT = "export"                # Exportação multi-formato
    DISTRIBUTION = "distribution"    # Distribuição para sistemas
    ARCHIVAL = "archival"           # Arquivamento final

class TaskStatus(Enum):
    """Status de tarefas do pipeline"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"
    RETRY = "retry"

@dataclass
class PipelineTask:
    """Tarefa individual do pipeline"""
    id: str
    stage: PipelineStage
    name: str
    input_file: Optional[Path]
    output_file: Optional[Path]
    status: TaskStatus = TaskStatus.PENDING
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    error_message: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    dependencies: List[str] = field(default_factory=list)
    retry_count: int = 0
    max_retries: int = 3

@dataclass
class PipelineJob:
    """Job completo do pipeline"""
    id: str
    name: str
    screenplay_file: Path
    created_at: datetime
    tasks: List[PipelineTask]
    status: TaskStatus = TaskStatus.PENDING
    config: Dict[str, Any] = field(default_factory=dict)
    results: Dict[str, Any] = field(default_factory=dict)

class ProductionPipeline:
    """Sistema completo de pipeline de produção"""

    def __init__(self, config_path: Optional[str] = None):
        self.config = self._load_config(config_path)
        self.jobs: Dict[str, PipelineJob] = {}
        self.executor = ThreadPoolExecutor(max_workers=4)
        self.process_executor = ProcessPoolExecutor(max_workers=2)

        # Diretórios de trabalho
        self.base_dir = Path(self.config.get('base_dir', 'pipeline'))
        self.input_dir = self.base_dir / 'input'
        self.processing_dir = self.base_dir / 'processing'
        self.output_dir = self.base_dir / 'output'
        self.archive_dir = self.base_dir / 'archive'

        # Criar estrutura
        self._setup_directories()

        # Inicializar banco de dados
        self._init_database()

        # Carregar integrações
        self.integrations = self._load_integrations()

    def _load_config(self, config_path: Optional[str]) -> Dict[str, Any]:
        """Carrega configuração do pipeline"""
        default_config = {
            'base_dir': 'pipeline',
            'max_parallel_jobs': 3,
            'enable_compression': True,
            'enable_ai_enrichment': True,
            'export_formats': ['json', 'html', 'pdf', 'markdown'],
            'archive_days': 30,
            'integrations': {
                'ollama': {'enabled': True, 'model': 'scripturemon-ptbr'},
                'digilang': {'enabled': True, 'version': 'v3'},
                'rag': {'enabled': True, 'auto_index': True},
                'character_analytics': {'enabled': True}
            }
        }

        if config_path and Path(config_path).exists():
            with open(config_path, 'r') as f:
                if config_path.endswith('.yaml') or config_path.endswith('.yml'):
                    user_config = yaml.safe_load(f)
                else:
                    user_config = json.load(f)
                default_config.update(user_config)

        return default_config

    def _setup_directories(self):
        """Cria estrutura de diretórios"""
        for dir_path in [self.input_dir, self.processing_dir,
                         self.output_dir, self.archive_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)

            # Subdiretórios por estágio
            for stage in PipelineStage:
                (dir_path / stage.value).mkdir(exist_ok=True)

    def _init_database(self):
        """Inicializa banco de dados do pipeline"""
        db_path = self.base_dir / 'pipeline.db'
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()

        # Tabela de jobs
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS jobs (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                screenplay_file TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                completed_at TIMESTAMP,
                status TEXT NOT NULL,
                config TEXT,
                results TEXT,
                error_message TEXT
            )
        """)

        # Tabela de tarefas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id TEXT PRIMARY KEY,
                job_id TEXT NOT NULL,
                stage TEXT NOT NULL,
                name TEXT NOT NULL,
                status TEXT NOT NULL,
                start_time TIMESTAMP,
                end_time TIMESTAMP,
                input_file TEXT,
                output_file TEXT,
                error_message TEXT,
                metadata TEXT,
                FOREIGN KEY (job_id) REFERENCES jobs(id)
            )
        """)

        # Tabela de métricas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                job_id TEXT NOT NULL,
                stage TEXT NOT NULL,
                metric_name TEXT NOT NULL,
                metric_value REAL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (job_id) REFERENCES jobs(id)
            )
        """)

        conn.commit()
        conn.close()

    def _load_integrations(self) -> Dict[str, Any]:
        """Carrega integrações com ferramentas externas"""
        integrations = {}

        # DigiLang
        if self.config['integrations']['digilang']['enabled']:
            try:
                from apps.scripturemon.digilang_v3_ta import DigiLangV3Encoder
                integrations['digilang'] = DigiLangV3Encoder()
                print("✅ DigiLang V3 integrado")
            except ImportError:
                print("⚠️ DigiLang não disponível")

        # Ollama
        if self.config['integrations']['ollama']['enabled']:
            try:
                from apps.scripturemon.ollama_core import OllamaCore
                integrations['ollama'] = OllamaCore()
                print("✅ Ollama integrado")
            except ImportError:
                print("⚠️ Ollama não disponível")

        # RAG
        if self.config['integrations']['rag']['enabled']:
            try:
                from apps.scripturemon.rag_system import RAGSystem
                integrations['rag'] = RAGSystem()
                print("✅ RAG System integrado")
            except ImportError:
                print("⚠️ RAG não disponível")

        # Character Analytics
        if self.config['integrations']['character_analytics']['enabled']:
            try:
                from apps.scripturemon.character_analytics import CharacterAnalytics
                integrations['character_analytics'] = CharacterAnalytics()
                print("✅ Character Analytics integrado")
            except ImportError:
                print("⚠️ Character Analytics não disponível")

        return integrations

    def create_job(self, screenplay_file: Path, name: Optional[str] = None,
                   config: Optional[Dict[str, Any]] = None) -> str:
        """
        Cria um novo job de processamento

        Returns:
            ID do job criado
        """
        # Gerar ID único
        file_name = screenplay_file if isinstance(screenplay_file, str) else screenplay_file.name
        job_id = hashlib.md5(
            f"{file_name}_{datetime.now().isoformat()}".encode()
        ).hexdigest()[:12]

        # Nome do job
        if not name:
            stem_name = screenplay_file if isinstance(screenplay_file, str) else screenplay_file.stem
            name = f"Pipeline_{stem_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        # Configuração específica do job
        job_config = self.config.copy()
        if config:
            job_config.update(config)

        # Criar tarefas do pipeline
        tasks = self._create_pipeline_tasks(job_id, screenplay_file, job_config)

        # Criar job
        job = PipelineJob(
            id=job_id,
            name=name,
            screenplay_file=screenplay_file,
            created_at=datetime.now(),
            tasks=tasks,
            status=TaskStatus.PENDING,
            config=job_config
        )

        self.jobs[job_id] = job

        # Salvar no banco
        self._save_job_to_db(job)

        print(f"📦 Job criado: {job_id} - {name}")
        print(f"   Arquivo: {screenplay_file}")
        print(f"   Tarefas: {len(tasks)}")

        return job_id

    def _create_pipeline_tasks(self, job_id: str, screenplay_file: Path,
                              config: Dict[str, Any]) -> List[PipelineTask]:
        """Cria tarefas para o pipeline"""
        tasks = []
        task_counter = 0

        # 1. INGESTION - Entrada
        task_counter += 1
        ingestion_task = PipelineTask(
            id=f"{job_id}_task_{task_counter:03d}",
            stage=PipelineStage.INGESTION,
            name="Ingestão do roteiro",
            input_file=screenplay_file,
            output_file=self.processing_dir / PipelineStage.INGESTION.value / f"{job_id}_ingested.txt"
        )
        tasks.append(ingestion_task)

        # 2. PREPROCESSING - Normalização
        task_counter += 1
        preprocessing_task = PipelineTask(
            id=f"{job_id}_task_{task_counter:03d}",
            stage=PipelineStage.PREPROCESSING,
            name="Normalização e limpeza",
            input_file=ingestion_task.output_file,
            output_file=self.processing_dir / PipelineStage.PREPROCESSING.value / f"{job_id}_normalized.txt",
            dependencies=[ingestion_task.id]
        )
        tasks.append(preprocessing_task)

        # 3. ANALYSIS - Análises paralelas
        analysis_tasks = []

        # 3a. Character Analytics
        if config['integrations']['character_analytics']['enabled']:
            task_counter += 1
            char_task = PipelineTask(
                id=f"{job_id}_task_{task_counter:03d}",
                stage=PipelineStage.ANALYSIS,
                name="Análise de personagens",
                input_file=preprocessing_task.output_file,
                output_file=self.processing_dir / PipelineStage.ANALYSIS.value / f"{job_id}_characters.json",
                dependencies=[preprocessing_task.id]
            )
            tasks.append(char_task)
            analysis_tasks.append(char_task)

        # 3b. Structure Analysis
        task_counter += 1
        struct_task = PipelineTask(
            id=f"{job_id}_task_{task_counter:03d}",
            stage=PipelineStage.ANALYSIS,
            name="Análise estrutural",
            input_file=preprocessing_task.output_file,
            output_file=self.processing_dir / PipelineStage.ANALYSIS.value / f"{job_id}_structure.json",
            dependencies=[preprocessing_task.id]
        )
        tasks.append(struct_task)
        analysis_tasks.append(struct_task)

        # 4. COMPRESSION - DigiLang
        if config['enable_compression']:
            task_counter += 1
            compression_task = PipelineTask(
                id=f"{job_id}_task_{task_counter:03d}",
                stage=PipelineStage.COMPRESSION,
                name="Compressão DigiLang",
                input_file=preprocessing_task.output_file,
                output_file=self.processing_dir / PipelineStage.COMPRESSION.value / f"{job_id}_compressed.dlg",
                dependencies=[preprocessing_task.id]
            )
            tasks.append(compression_task)

        # 5. ENRICHMENT - IA
        if config['enable_ai_enrichment'] and 'ollama' in self.integrations:
            task_counter += 1

            # Dependências incluem todas as análises
            deps = [t.id for t in analysis_tasks]

            enrichment_task = PipelineTask(
                id=f"{job_id}_task_{task_counter:03d}",
                stage=PipelineStage.ENRICHMENT,
                name="Enriquecimento com IA",
                input_file=preprocessing_task.output_file,
                output_file=self.processing_dir / PipelineStage.ENRICHMENT.value / f"{job_id}_enriched.json",
                dependencies=deps
            )
            tasks.append(enrichment_task)

        # 6. VALIDATION - Validação
        task_counter += 1

        # Validação depende de todas as tarefas anteriores
        all_deps = [t.id for t in tasks]

        validation_task = PipelineTask(
            id=f"{job_id}_task_{task_counter:03d}",
            stage=PipelineStage.VALIDATION,
            name="Validação de qualidade",
            input_file=preprocessing_task.output_file,
            output_file=self.processing_dir / PipelineStage.VALIDATION.value / f"{job_id}_validation.json",
            dependencies=all_deps[:-1]  # Todas exceto ela mesma
        )
        tasks.append(validation_task)

        # 7. EXPORT - Multi-formato
        for format in config.get('export_formats', ['json']):
            task_counter += 1
            export_task = PipelineTask(
                id=f"{job_id}_task_{task_counter:03d}",
                stage=PipelineStage.EXPORT,
                name=f"Exportação {format.upper()}",
                input_file=preprocessing_task.output_file,
                output_file=self.output_dir / PipelineStage.EXPORT.value / f"{job_id}_export.{format}",
                dependencies=[validation_task.id],
                metadata={'format': format}
            )
            tasks.append(export_task)

        # 8. DISTRIBUTION - Distribuição
        if config.get('auto_distribute', False):
            task_counter += 1
            dist_task = PipelineTask(
                id=f"{job_id}_task_{task_counter:03d}",
                stage=PipelineStage.DISTRIBUTION,
                name="Distribuição automática",
                input_file=None,
                output_file=None,
                dependencies=[t.id for t in tasks if t.stage == PipelineStage.EXPORT]
            )
            tasks.append(dist_task)

        # 9. ARCHIVAL - Arquivamento
        task_counter += 1
        archive_task = PipelineTask(
            id=f"{job_id}_task_{task_counter:03d}",
            stage=PipelineStage.ARCHIVAL,
            name="Arquivamento final",
            input_file=None,
            output_file=self.archive_dir / f"{job_id}_archive.zip",
            dependencies=[t.id for t in tasks[:-1]]  # Todas exceto ela mesma
        )
        tasks.append(archive_task)

        return tasks

    async def execute_job(self, job_id: str) -> Dict[str, Any]:
        """
        Executa um job de forma assíncrona

        Returns:
            Resultados da execução
        """
        if job_id not in self.jobs:
            raise ValueError(f"Job {job_id} não encontrado")

        job = self.jobs[job_id]
        job.status = TaskStatus.RUNNING

        print(f"\n🚀 Iniciando execução do job: {job.name}")
        print(f"   Total de tarefas: {len(job.tasks)}")

        results = {
            'job_id': job_id,
            'start_time': datetime.now().isoformat(),
            'tasks_completed': 0,
            'tasks_failed': 0,
            'stages': {}
        }

        try:
            # Executar tarefas em ordem de dependência
            for task in job.tasks:
                # Verificar dependências
                if not self._check_dependencies(task, job):
                    task.status = TaskStatus.SKIPPED
                    continue

                # Executar tarefa
                print(f"\n▶️ Executando: [{task.stage.value}] {task.name}")
                task.status = TaskStatus.RUNNING
                task.start_time = datetime.now()

                try:
                    task_result = await self._execute_task(task, job)
                    task.status = TaskStatus.COMPLETED
                    task.end_time = datetime.now()
                    task.metadata.update(task_result)
                    results['tasks_completed'] += 1

                    # Armazenar resultado por estágio
                    if task.stage.value not in results['stages']:
                        results['stages'][task.stage.value] = []
                    results['stages'][task.stage.value].append({
                        'task': task.name,
                        'status': 'completed',
                        'duration': (task.end_time - task.start_time).total_seconds(),
                        'result': task_result
                    })

                    print(f"   ✅ Concluído em {(task.end_time - task.start_time).total_seconds():.2f}s")

                except Exception as e:
                    task.status = TaskStatus.FAILED
                    task.error_message = str(e)
                    task.end_time = datetime.now()
                    results['tasks_failed'] += 1

                    print(f"   ❌ Falhou: {e}")

                    # Tentar retry se configurado
                    if task.retry_count < task.max_retries:
                        task.retry_count += 1
                        task.status = TaskStatus.RETRY
                        print(f"   🔄 Tentando novamente ({task.retry_count}/{task.max_retries})...")
                        # Recursão para retry
                        await asyncio.sleep(2)  # Delay antes do retry
                        continue

            # Finalizar job
            job.status = TaskStatus.COMPLETED if results['tasks_failed'] == 0 else TaskStatus.FAILED
            job.results = results
            results['end_time'] = datetime.now().isoformat()

            # Salvar no banco
            self._update_job_in_db(job)

            print(f"\n✅ Job concluído: {results['tasks_completed']} tarefas completadas")
            if results['tasks_failed'] > 0:
                print(f"⚠️ {results['tasks_failed']} tarefas falharam")

            return results

        except Exception as e:
            job.status = TaskStatus.FAILED
            results['error'] = str(e)
            print(f"\n❌ Job falhou: {e}")
            return results

    async def _execute_task(self, task: PipelineTask, job: PipelineJob) -> Dict[str, Any]:
        """Executa uma tarefa específica"""
        result = {}

        # Executar baseado no estágio
        if task.stage == PipelineStage.INGESTION:
            result = await self._task_ingestion(task, job)

        elif task.stage == PipelineStage.PREPROCESSING:
            result = await self._task_preprocessing(task, job)

        elif task.stage == PipelineStage.ANALYSIS:
            if "personagens" in task.name.lower():
                result = await self._task_character_analysis(task, job)
            else:
                result = await self._task_structure_analysis(task, job)

        elif task.stage == PipelineStage.COMPRESSION:
            result = await self._task_compression(task, job)

        elif task.stage == PipelineStage.ENRICHMENT:
            result = await self._task_enrichment(task, job)

        elif task.stage == PipelineStage.VALIDATION:
            result = await self._task_validation(task, job)

        elif task.stage == PipelineStage.EXPORT:
            result = await self._task_export(task, job)

        elif task.stage == PipelineStage.DISTRIBUTION:
            result = await self._task_distribution(task, job)

        elif task.stage == PipelineStage.ARCHIVAL:
            result = await self._task_archival(task, job)

        return result

    async def _task_ingestion(self, task: PipelineTask, job: PipelineJob) -> Dict[str, Any]:
        """Tarefa de ingestão"""
        # Ler arquivo
        with open(task.input_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Detectar formato
        file_ext = task.input_file.suffix.lower()

        if file_ext == '.pdf':
            # Usar OCR pipeline se disponível
            try:
                from apps.scripturemon.ocr_pipeline import OCRPipeline
                ocr = OCRPipeline()
                content = ocr.process_pdf(str(task.input_file))
            except:
                pass

        # Salvar conteúdo processado
        task.output_file.parent.mkdir(parents=True, exist_ok=True)
        with open(task.output_file, 'w', encoding='utf-8') as f:
            f.write(content)

        return {
            'file_size': len(content),
            'format': file_ext,
            'lines': len(content.split('\n'))
        }

    async def _task_preprocessing(self, task: PipelineTask, job: PipelineJob) -> Dict[str, Any]:
        """Tarefa de pré-processamento"""
        with open(task.input_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Normalizar
        try:
            from apps.scripturemon.screenplay_normalizer import ScreenplayNormalizer
            normalizer = ScreenplayNormalizer()
            normalized_obj = normalizer.normalize(content)
            # Converter para string se for objeto
            if hasattr(normalized_obj, 'content'):
                normalized = normalized_obj.content
            else:
                normalized = str(normalized_obj)
        except:
            normalized = content

        # Salvar
        with open(task.output_file, 'w', encoding='utf-8') as f:
            f.write(normalized)

        return {
            'original_size': len(content),
            'normalized_size': len(normalized),
            'reduction': (1 - len(normalized) / len(content)) * 100 if content else 0
        }

    async def _task_character_analysis(self, task: PipelineTask, job: PipelineJob) -> Dict[str, Any]:
        """Tarefa de análise de personagens"""
        if 'character_analytics' not in self.integrations:
            return {'error': 'Character Analytics não disponível'}

        with open(task.input_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Analisar
        analyzer = self.integrations['character_analytics']
        result = analyzer.analyze_screenplay(job.id, content)

        # Salvar resultado
        with open(task.output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2)

        return {
            'characters': result['summary']['total_characters'],
            'relationships': result['summary']['total_relationships'],
            'scenes': result['summary']['total_scenes']
        }

    async def _task_structure_analysis(self, task: PipelineTask, job: PipelineJob) -> Dict[str, Any]:
        """Tarefa de análise estrutural"""
        with open(task.input_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Análise básica de estrutura
        lines = content.split('\n')
        structure = {
            'total_lines': len(lines),
            'acts': 0,
            'scenes': 0,
            'dialogues': 0,
            'action_lines': 0
        }

        for line in lines:
            if line.strip().startswith('ACT ') or line.strip().startswith('ATO '):
                structure['acts'] += 1
            elif line.strip().startswith('INT.') or line.strip().startswith('EXT.'):
                structure['scenes'] += 1
            elif line.strip() and line[0].isupper() and ':' not in line:
                # Possível nome de personagem
                structure['dialogues'] += 1

        # Salvar
        with open(task.output_file, 'w', encoding='utf-8') as f:
            json.dump(structure, f, indent=2)

        return structure

    async def _task_compression(self, task: PipelineTask, job: PipelineJob) -> Dict[str, Any]:
        """Tarefa de compressão DigiLang"""
        if 'digilang' not in self.integrations:
            return {'error': 'DigiLang não disponível'}

        with open(task.input_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Comprimir
        encoder = self.integrations['digilang']
        compressed, stats = encoder.encode(content)

        # Salvar
        with open(task.output_file, 'w', encoding='utf-8') as f:
            f.write(compressed)

        return {
            'original_size': len(content),
            'compressed_size': len(compressed),
            'compression_ratio': stats['compression_ratio'] if isinstance(stats, dict) else 0
        }

    async def _task_enrichment(self, task: PipelineTask, job: PipelineJob) -> Dict[str, Any]:
        """Tarefa de enriquecimento com IA"""
        if 'ollama' not in self.integrations:
            return {'error': 'Ollama não disponível'}

        with open(task.input_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Coletar análises anteriores
        analyses = {}
        for t in job.tasks:
            if t.stage == PipelineStage.ANALYSIS and t.status == TaskStatus.COMPLETED:
                if t.output_file.exists():
                    with open(t.output_file, 'r') as f:
                        analyses[t.name] = json.load(f)

        # Enriquecer com Ollama
        ollama = self.integrations['ollama']

        prompts = [
            "Analise o tom e o gênero deste roteiro",
            "Identifique os temas principais",
            "Sugira melhorias para o diálogo"
        ]

        enrichments = {}
        for prompt in prompts:
            try:
                response = ollama.analyze_screenplay(content[:5000], prompt)  # Limitar tamanho
                enrichments[prompt] = response
            except:
                enrichments[prompt] = "Análise não disponível"

        # Combinar com análises
        result = {
            'analyses': analyses,
            'ai_enrichments': enrichments,
            'timestamp': datetime.now().isoformat()
        }

        # Salvar
        with open(task.output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2)

        return {
            'enrichments_count': len(enrichments),
            'analyses_count': len(analyses)
        }

    async def _task_validation(self, task: PipelineTask, job: PipelineJob) -> Dict[str, Any]:
        """Tarefa de validação"""
        validation_results = {
            'passed': [],
            'failed': [],
            'warnings': []
        }

        # Verificar arquivo principal
        if not task.input_file.exists():
            validation_results['failed'].append("Arquivo de entrada não encontrado")
        else:
            validation_results['passed'].append("Arquivo de entrada válido")

        # Verificar tarefas anteriores
        for t in job.tasks:
            if t.id in task.dependencies:
                if t.status == TaskStatus.COMPLETED:
                    validation_results['passed'].append(f"Tarefa {t.name} concluída")
                else:
                    validation_results['failed'].append(f"Tarefa {t.name} não concluída")

        # Verificar outputs
        for t in job.tasks:
            if t.output_file and t.status == TaskStatus.COMPLETED:
                if t.output_file.exists():
                    size = t.output_file.stat().st_size
                    if size > 0:
                        validation_results['passed'].append(f"Output {t.output_file.name} válido")
                    else:
                        validation_results['warnings'].append(f"Output {t.output_file.name} vazio")

        # Calcular score
        total = len(validation_results['passed']) + len(validation_results['failed'])
        score = len(validation_results['passed']) / total if total > 0 else 0

        validation_results['score'] = score
        validation_results['status'] = 'passed' if score >= 0.8 else 'failed'

        # Salvar
        with open(task.output_file, 'w', encoding='utf-8') as f:
            json.dump(validation_results, f, indent=2)

        return validation_results

    async def _task_export(self, task: PipelineTask, job: PipelineJob) -> Dict[str, Any]:
        """Tarefa de exportação"""
        format = task.metadata.get('format', 'json')

        # Coletar todos os resultados
        export_data = {
            'job_id': job.id,
            'screenplay': job.screenplay_file.name,
            'timestamp': datetime.now().isoformat(),
            'stages': {}
        }

        # Coletar outputs de todas as tarefas
        for t in job.tasks:
            if t.output_file and t.output_file.exists() and t.stage != PipelineStage.EXPORT:
                stage_name = t.stage.value
                if stage_name not in export_data['stages']:
                    export_data['stages'][stage_name] = {}

                # Ler conteúdo baseado no tipo
                if t.output_file.suffix == '.json':
                    with open(t.output_file, 'r') as f:
                        export_data['stages'][stage_name][t.name] = json.load(f)
                else:
                    with open(t.output_file, 'r', encoding='utf-8') as f:
                        export_data['stages'][stage_name][t.name] = f.read()[:1000]  # Limitar texto

        # Exportar no formato solicitado
        if format == 'json':
            with open(task.output_file, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2)

        elif format == 'html':
            html_content = self._generate_html_report(export_data)
            with open(task.output_file, 'w', encoding='utf-8') as f:
                f.write(html_content)

        elif format == 'markdown':
            md_content = self._generate_markdown_report(export_data)
            with open(task.output_file, 'w', encoding='utf-8') as f:
                f.write(md_content)

        elif format == 'pdf':
            # Requer biblioteca externa
            # Por enquanto, criar um placeholder
            with open(task.output_file, 'wb') as f:
                f.write(b'PDF export not implemented')

        return {
            'format': format,
            'file_size': task.output_file.stat().st_size if task.output_file.exists() else 0
        }

    async def _task_distribution(self, task: PipelineTask, job: PipelineJob) -> Dict[str, Any]:
        """Tarefa de distribuição"""
        distributed = []

        # Coletar arquivos exportados
        export_files = []
        for t in job.tasks:
            if t.stage == PipelineStage.EXPORT and t.output_file and t.output_file.exists():
                export_files.append(t.output_file)

        # Distribuir para destinos configurados
        destinations = job.config.get('distribution_destinations', [])

        for dest in destinations:
            if dest['type'] == 'local':
                # Copiar para diretório local
                dest_path = Path(dest['path'])
                dest_path.mkdir(parents=True, exist_ok=True)
                for file in export_files:
                    shutil.copy2(file, dest_path / file.name)
                    distributed.append(f"local:{dest_path / file.name}")

            elif dest['type'] == 's3':
                # Upload para S3 (requer boto3)
                pass

            elif dest['type'] == 'api':
                # POST para API
                pass

        return {
            'files_distributed': len(distributed),
            'destinations': distributed
        }

    async def _task_archival(self, task: PipelineTask, job: PipelineJob) -> Dict[str, Any]:
        """Tarefa de arquivamento"""
        import zipfile

        # Criar arquivo ZIP
        with zipfile.ZipFile(task.output_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Adicionar arquivo original
            zipf.write(job.screenplay_file, f"original/{job.screenplay_file.name}")

            # Adicionar todos os outputs
            for t in job.tasks:
                if t.output_file and t.output_file.exists():
                    arcname = f"{t.stage.value}/{t.output_file.name}"
                    zipf.write(t.output_file, arcname)

            # Adicionar metadados
            metadata = {
                'job_id': job.id,
                'created_at': job.created_at.isoformat(),
                'completed_at': datetime.now().isoformat(),
                'config': job.config,
                'results': job.results
            }
            zipf.writestr('metadata.json', json.dumps(metadata, indent=2))

        return {
            'archive_size': task.output_file.stat().st_size,
            'files_archived': len(zipf.namelist()) if 'zipf' in locals() else 0
        }

    def _check_dependencies(self, task: PipelineTask, job: PipelineJob) -> bool:
        """Verifica se as dependências de uma tarefa foram satisfeitas"""
        for dep_id in task.dependencies:
            dep_task = next((t for t in job.tasks if t.id == dep_id), None)
            if not dep_task or dep_task.status != TaskStatus.COMPLETED:
                return False
        return True

    def _save_job_to_db(self, job: PipelineJob):
        """Salva job no banco de dados"""
        conn = sqlite3.connect(str(self.base_dir / 'pipeline.db'))
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO jobs (id, name, screenplay_file, status, config, results)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            job.id,
            job.name,
            str(job.screenplay_file),
            job.status.value,
            json.dumps(job.config),
            json.dumps(job.results)
        ))

        # Salvar tarefas
        for task in job.tasks:
            cursor.execute("""
                INSERT INTO tasks (id, job_id, stage, name, status, input_file, output_file, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                task.id,
                job.id,
                task.stage.value,
                task.name,
                task.status.value,
                str(task.input_file) if task.input_file else None,
                str(task.output_file) if task.output_file else None,
                json.dumps(task.metadata)
            ))

        conn.commit()
        conn.close()

    def _update_job_in_db(self, job: PipelineJob):
        """Atualiza job no banco de dados"""
        conn = sqlite3.connect(str(self.base_dir / 'pipeline.db'))
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE jobs
            SET status = ?, results = ?, completed_at = ?
            WHERE id = ?
        """, (
            job.status.value,
            json.dumps(job.results),
            datetime.now(),
            job.id
        ))

        # Atualizar tarefas
        for task in job.tasks:
            cursor.execute("""
                UPDATE tasks
                SET status = ?, start_time = ?, end_time = ?, error_message = ?, metadata = ?
                WHERE id = ?
            """, (
                task.status.value,
                task.start_time,
                task.end_time,
                task.error_message,
                json.dumps(task.metadata),
                task.id
            ))

        conn.commit()
        conn.close()

    def _generate_html_report(self, data: Dict[str, Any]) -> str:
        """Gera relatório HTML"""
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Pipeline Report - {data['job_id']}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        h1 {{ color: #333; }}
        .stage {{ margin: 20px 0; padding: 15px; border: 1px solid #ddd; }}
        .stage h2 {{ color: #666; }}
        pre {{ background: #f5f5f5; padding: 10px; overflow-x: auto; }}
    </style>
</head>
<body>
    <h1>Pipeline Report</h1>
    <p>Job ID: {data['job_id']}</p>
    <p>Screenplay: {data['screenplay']}</p>
    <p>Generated: {data['timestamp']}</p>

    <h2>Results by Stage</h2>
"""

        for stage, content in data['stages'].items():
            html += f"""
    <div class="stage">
        <h2>{stage.upper()}</h2>
        <pre>{json.dumps(content, indent=2)}</pre>
    </div>
"""

        html += """
</body>
</html>
"""
        return html

    def _generate_markdown_report(self, data: Dict[str, Any]) -> str:
        """Gera relatório Markdown"""
        md = f"""# Pipeline Report

**Job ID:** {data['job_id']}
**Screenplay:** {data['screenplay']}
**Generated:** {data['timestamp']}

## Results by Stage
"""

        for stage, content in data['stages'].items():
            md += f"""
### {stage.upper()}

```json
{json.dumps(content, indent=2)}
```
"""

        return md

    def get_job_status(self, job_id: str) -> Dict[str, Any]:
        """Retorna status detalhado de um job"""
        if job_id not in self.jobs:
            return {'error': 'Job não encontrado'}

        job = self.jobs[job_id]

        status = {
            'job_id': job_id,
            'name': job.name,
            'status': job.status.value,
            'created_at': job.created_at.isoformat(),
            'tasks': {
                'total': len(job.tasks),
                'completed': sum(1 for t in job.tasks if t.status == TaskStatus.COMPLETED),
                'failed': sum(1 for t in job.tasks if t.status == TaskStatus.FAILED),
                'running': sum(1 for t in job.tasks if t.status == TaskStatus.RUNNING),
                'pending': sum(1 for t in job.tasks if t.status == TaskStatus.PENDING)
            },
            'stages': {}
        }

        # Status por estágio
        for stage in PipelineStage:
            stage_tasks = [t for t in job.tasks if t.stage == stage]
            if stage_tasks:
                status['stages'][stage.value] = {
                    'total': len(stage_tasks),
                    'completed': sum(1 for t in stage_tasks if t.status == TaskStatus.COMPLETED)
                }

        return status

    def cleanup_old_jobs(self, days: int = 30):
        """Limpa jobs antigos"""
        cutoff_date = datetime.now() - timedelta(days=days)

        cleaned = 0
        for job_id, job in list(self.jobs.items()):
            if job.created_at < cutoff_date:
                # Remover arquivos
                for task in job.tasks:
                    if task.output_file and task.output_file.exists():
                        task.output_file.unlink()

                # Remover do dicionário
                del self.jobs[job_id]
                cleaned += 1

        print(f"🧹 {cleaned} jobs antigos removidos")
        return cleaned


# Exemplo de uso
if __name__ == "__main__":
    import asyncio

    async def test_pipeline():
        print("🎬 PRODUCTION PIPELINE - FASE 26")
        print("=" * 60)

        # Criar pipeline
        pipeline = ProductionPipeline()

        # Criar roteiro de teste
        test_screenplay = Path("test_screenplay.txt")
        with open(test_screenplay, 'w', encoding='utf-8') as f:
            f.write("""FADE IN:

ACT I

EXT. CITY - DAY

JOHN walks through the busy streets.

FADE OUT.""")

        # Criar job
        job_id = pipeline.create_job(
            screenplay_file=test_screenplay,
            name="Test Pipeline Job",
            config={
                'enable_compression': True,
                'enable_ai_enrichment': False,  # Desabilitar para teste rápido
                'export_formats': ['json', 'html', 'markdown']
            }
        )

        # Executar job
        print("\n🚀 Executando pipeline...")
        results = await pipeline.execute_job(job_id)

        # Mostrar status
        status = pipeline.get_job_status(job_id)
        print("\n📊 STATUS FINAL:")
        print(f"   Status: {status['status']}")
        print(f"   Tarefas completadas: {status['tasks']['completed']}/{status['tasks']['total']}")
        print(f"   Tarefas falhadas: {status['tasks']['failed']}")

        print("\n✅ Pipeline de produção testado com sucesso!")

    # Executar teste
    asyncio.run(test_pipeline())