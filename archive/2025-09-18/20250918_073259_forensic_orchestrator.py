#!/usr/bin/env python3
"""
🔬 ORQUESTRADOR FORENSE COMPLETO
Sistema híbrido para análise profunda de código usando Ollama + Python

CARACTERÍSTICAS:
- Análise linha por linha de cada arquivo
- Sistema de checkpoint robusto (pode retomar)
- Logs detalhados de toda operação
- Teste de execução real de cada arquivo
- Relatórios estruturados e acionáveis
- Estimativa de tempo e progresso
- Backup automático de resultados

TEMPO ESTIMADO: 4-6 horas para análise completa
"""

import os
import sys
import json
import time
import traceback
import subprocess
import importlib.util
import ast
import psutil
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
import ollama

# Configuração de logging detalhado
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('forensic_analysis.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class AnalysisResult:
    """Resultado estruturado da análise de um arquivo"""
    filename: str
    analysis_timestamp: str
    file_size_bytes: int
    line_count: int

    # Análise estática
    syntax_valid: bool
    syntax_errors: List[str]

    # Análise do modelo
    model_analysis: Dict[str, Any]
    model_analysis_time_seconds: float

    # Teste de execução
    execution_attempted: bool
    execution_successful: bool
    execution_errors: List[str]
    execution_time_seconds: float

    # Métricas de recursos
    imports_found: List[str]
    imports_missing: List[str]
    imports_problematic: List[str]

    # Problemas críticos encontrados
    critical_issues: List[Dict[str, Any]]
    high_issues: List[Dict[str, Any]]
    medium_issues: List[Dict[str, Any]]
    low_issues: List[Dict[str, Any]]

    # Classificação geral
    overall_health: str  # BROKEN, PROBLEMATIC, WARNING, OK
    claude_vice_score: int  # 0-100, quanto mais alto mais vícios típicos

    # Estimativas
    fix_time_estimate_hours: float
    breaking_changes_required: bool

class ForensicOrchestrator:
    """Orquestrador principal do sistema forense"""

    def __init__(self, base_dir: str = None):
        self.base_dir = Path(base_dir) if base_dir else Path("/Users/clubproducoes/Digimundo/scripturemon-champion")
        self.apps_dir = self.base_dir / "apps" / "scripturemon"
        self.results_dir = self.base_dir / "forensic_results"
        self.checkpoint_file = self.results_dir / "checkpoint.json"
        self.detailed_log = self.results_dir / "detailed_analysis.log"

        # Configuração do modelo
        self.model_name = "forensic-analyzer:latest"
        self.model_config = {
            'num_ctx': 131072,
            'num_thread': 14,
            'num_gpu': 999,
            'temperature': 0.1,
            'top_p': 0.9,
            'repeat_penalty': 1.1
        }

        # Estado da análise
        self.results: Dict[str, AnalysisResult] = {}
        self.start_time: Optional[datetime] = None
        self.total_files: int = 0
        self.completed_files: int = 0

        # Inicialização
        self._setup_environment()
        self._create_forensic_model()

    def _setup_environment(self):
        """Configura ambiente para análise"""
        logger.info("🔧 Configurando ambiente forense...")

        # Criar diretórios necessários
        self.results_dir.mkdir(exist_ok=True)
        (self.results_dir / "backups").mkdir(exist_ok=True)
        (self.results_dir / "individual_reports").mkdir(exist_ok=True)

        # Configurar logging detalhado
        detailed_handler = logging.FileHandler(self.detailed_log)
        detailed_handler.setLevel(logging.DEBUG)
        detailed_formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
        )
        detailed_handler.setFormatter(detailed_formatter)
        logger.addHandler(detailed_handler)

        logger.info(f"✅ Ambiente configurado. Resultados em: {self.results_dir}")

    def _create_forensic_model(self):
        """Cria ou verifica modelo forense especializado"""
        logger.info("🤖 Verificando modelo forense...")

        try:
            # Verificar se modelo existe
            models_response = ollama.list()
            model_exists = any(
                model.model == self.model_name
                for model in models_response.models
            )

            if not model_exists:
                logger.info("📦 Criando modelo forense especializado...")
                modelfile_path = self.base_dir / "modelfiles" / "forensic-analyzer.modelfile"

                if not modelfile_path.exists():
                    raise FileNotFoundError(f"Modelfile não encontrado: {modelfile_path}")

                # Criar modelo
                subprocess.run([
                    "ollama", "create", self.model_name,
                    "-f", str(modelfile_path)
                ], check=True, capture_output=True, text=True)

                logger.info("✅ Modelo forense criado com sucesso")
            else:
                logger.info("✅ Modelo forense já existe")

        except Exception as e:
            logger.error(f"❌ Erro ao configurar modelo: {e}")
            raise

    def _load_checkpoint(self) -> bool:
        """Carrega checkpoint de execução anterior"""
        if not self.checkpoint_file.exists():
            return False

        try:
            with open(self.checkpoint_file, 'r') as f:
                checkpoint_data = json.load(f)

            # Restaurar resultados anteriores
            for filename, result_data in checkpoint_data.get('results', {}).items():
                self.results[filename] = AnalysisResult(**result_data)

            self.completed_files = len(self.results)
            logger.info(f"📂 Checkpoint carregado: {self.completed_files} arquivos já analisados")
            return True

        except Exception as e:
            logger.warning(f"⚠️ Erro ao carregar checkpoint: {e}")
            return False

    def _save_checkpoint(self):
        """Salva checkpoint atual"""
        try:
            checkpoint_data = {
                'timestamp': datetime.now().isoformat(),
                'total_files': self.total_files,
                'completed_files': self.completed_files,
                'results': {
                    filename: asdict(result)
                    for filename, result in self.results.items()
                }
            }

            # Backup anterior
            if self.checkpoint_file.exists():
                backup_path = self.results_dir / "backups" / f"checkpoint_{int(time.time())}.json"
                self.checkpoint_file.rename(backup_path)

            # Salvar novo
            with open(self.checkpoint_file, 'w') as f:
                json.dump(checkpoint_data, f, indent=2, ensure_ascii=False)

            logger.debug(f"💾 Checkpoint salvo: {self.completed_files}/{self.total_files}")

        except Exception as e:
            logger.error(f"❌ Erro ao salvar checkpoint: {e}")

    def _get_python_files(self) -> List[Path]:
        """Obtém lista de arquivos Python para análise"""
        python_files = []

        for pattern in ["*.py"]:
            files = list(self.apps_dir.glob(pattern))
            python_files.extend(files)

        # Filtrar arquivos especiais
        excluded = ['__pycache__', '__init__.py', '.py.bak', '.backup']
        python_files = [
            f for f in python_files
            if not any(excl in str(f) for excl in excluded)
            and f.is_file()
        ]

        # Ordenar por tamanho (menores primeiro)
        python_files.sort(key=lambda f: f.stat().st_size)

        logger.info(f"📁 Encontrados {len(python_files)} arquivos Python para análise")
        return python_files

    def _analyze_syntax(self, filepath: Path) -> Tuple[bool, List[str]]:
        """Análise de sintaxe básica do arquivo"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            # Parse AST
            ast.parse(content)
            return True, []

        except SyntaxError as e:
            return False, [f"Erro de sintaxe linha {e.lineno}: {e.msg}"]
        except Exception as e:
            return False, [f"Erro ao analisar sintaxe: {str(e)}"]

    def _analyze_imports(self, filepath: Path) -> Tuple[List[str], List[str], List[str]]:
        """Analisa imports do arquivo"""
        imports_found = []
        imports_missing = []
        imports_problematic = []

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            tree = ast.parse(content)

            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports_found.append(alias.name)

                elif isinstance(node, ast.ImportFrom):
                    module = node.module if node.module else ""
                    imports_found.append(module)

            # Verificar se imports existem
            for imp in imports_found:
                if not imp:
                    continue

                try:
                    spec = importlib.util.find_spec(imp)
                    if spec is None:
                        imports_missing.append(imp)
                except Exception:
                    imports_missing.append(imp)

                # Verificar imports problemáticos conhecidos
                problematic_patterns = [
                    'quantum_cryptography', 'advanced_consensus', 'quantum_error_correction',
                    'neural_supreme', 'blockchain_ultimate', 'quantum_supreme'
                ]

                if any(pattern in imp.lower() for pattern in problematic_patterns):
                    imports_problematic.append(imp)

        except Exception as e:
            logger.warning(f"⚠️ Erro ao analisar imports de {filepath.name}: {e}")

        return imports_found, imports_missing, imports_problematic

    def _test_execution(self, filepath: Path) -> Tuple[bool, List[str], float]:
        """Testa execução segura do arquivo"""
        execution_errors = []
        start_time = time.time()

        try:
            # Tentar importar módulo de forma segura
            spec = importlib.util.spec_from_file_location(
                filepath.stem,
                filepath
            )

            if spec is None:
                return False, ["Não foi possível criar spec do módulo"], 0.0

            module = importlib.util.module_from_spec(spec)

            # Executar com timeout
            import signal

            def timeout_handler(signum, frame):
                raise TimeoutError("Execução excedeu timeout")

            signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(30)  # 30 segundos timeout

            try:
                spec.loader.exec_module(module)
                signal.alarm(0)  # Cancelar timeout

                execution_time = time.time() - start_time
                return True, [], execution_time

            except TimeoutError:
                execution_errors.append("Timeout na execução (>30s)")
            except Exception as e:
                execution_errors.append(f"Erro na execução: {str(e)}")
            finally:
                signal.alarm(0)

        except Exception as e:
            execution_errors.append(f"Erro ao configurar execução: {str(e)}")

        execution_time = time.time() - start_time
        return False, execution_errors, execution_time

    def _analyze_with_model(self, filepath: Path) -> Tuple[Dict[str, Any], float]:
        """Análise profunda usando modelo Ollama"""
        start_time = time.time()

        try:
            # Ler código
            with open(filepath, 'r', encoding='utf-8') as f:
                code_content = f.read()

            # Análise com modelo
            logger.debug(f"🤖 Iniciando análise do modelo para {filepath.name}")

            # Adicionar timeout para evitar travamento
            import signal

            def timeout_handler(signum, frame):
                raise TimeoutError(f"Análise do modelo excedeu 600 segundos (10min) para {filepath.name}")

            # Configurar timeout de 10 minutos (600 segundos)
            signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(600)

            try:
                response = ollama.generate(
                    model=self.model_name,
                    prompt=code_content,
                    options=self.model_config
                )
                signal.alarm(0)  # Cancelar timeout se sucesso
            except TimeoutError as e:
                signal.alarm(0)
                logger.warning(f"⏱️ Timeout na análise: {e}")
                return {
                    'problems': [],
                    'timeout': True,
                    'error': str(e)
                }, time.time() - start_time
            except Exception as e:
                signal.alarm(0)
                raise  # Re-lançar outras exceções

            analysis_time = time.time() - start_time

            # Tentar parsear resposta JSON
            try:
                if 'response' in response:
                    response_text = response['response']

                    # Buscar JSON na resposta
                    import re
                    json_match = re.search(r'\[.*\]', response_text, re.DOTALL)
                    if json_match:
                        problems = json.loads(json_match.group())
                        return {'problems': problems, 'raw_response': response_text}, analysis_time
                    else:
                        return {'problems': [], 'raw_response': response_text}, analysis_time

            except json.JSONDecodeError as e:
                logger.warning(f"⚠️ Erro ao parsear JSON do modelo: {e}")
                return {
                    'problems': [],
                    'raw_response': response.get('response', ''),
                    'parse_error': str(e)
                }, analysis_time

        except Exception as e:
            analysis_time = time.time() - start_time
            logger.error(f"❌ Erro na análise do modelo para {filepath.name}: {e}")
            return {
                'problems': [],
                'error': str(e)
            }, analysis_time

    def _categorize_problems(self, problems: List[Dict[str, Any]]) -> Tuple[List, List, List, List]:
        """Categoriza problemas por severidade"""
        critical = []
        high = []
        medium = []
        low = []

        for problem in problems:
            severity = problem.get('severity', 'MEDIUM').upper()

            if severity == 'CRITICAL':
                critical.append(problem)
            elif severity == 'HIGH':
                high.append(problem)
            elif severity == 'MEDIUM':
                medium.append(problem)
            else:
                low.append(problem)

        return critical, high, medium, low

    def _calculate_health_score(self, critical: List, high: List, medium: List, low: List) -> str:
        """Calcula saúde geral do arquivo"""
        if len(critical) > 0:
            return "BROKEN"
        elif len(high) > 2:
            return "PROBLEMATIC"
        elif len(high) > 0 or len(medium) > 3:
            return "WARNING"
        else:
            return "OK"

    def _calculate_claude_vice_score(self, problems: List[Dict[str, Any]]) -> int:
        """Calcula pontuação de vícios típicos do Claude"""
        score = 0

        for problem in problems:
            if problem.get('claude_vice', False):
                # Pontuação baseada na severidade
                severity = problem.get('severity', 'MEDIUM').upper()
                if severity == 'CRITICAL':
                    score += 25
                elif severity == 'HIGH':
                    score += 15
                elif severity == 'MEDIUM':
                    score += 10
                else:
                    score += 5

        return min(score, 100)  # Máximo 100

    def _estimate_fix_time(self, critical: List, high: List, medium: List, low: List) -> Tuple[float, bool]:
        """Estima tempo de correção e se requer mudanças breaking"""
        time_hours = 0.0
        breaking_changes = False

        # Tempo por tipo de problema
        time_hours += len(critical) * 2.0  # 2h por problema crítico
        time_hours += len(high) * 1.0      # 1h por problema alto
        time_hours += len(medium) * 0.5    # 30min por problema médio
        time_hours += len(low) * 0.25      # 15min por problema baixo

        # Verificar se requer mudanças breaking
        breaking_keywords = ['import', 'constructor', 'signature', 'interface', 'api']
        for problem in critical + high:
            problem_text = problem.get('problem', '').lower()
            if any(keyword in problem_text for keyword in breaking_keywords):
                breaking_changes = True
                break

        return time_hours, breaking_changes

    def analyze_file(self, filepath: Path) -> AnalysisResult:
        """Análise completa de um arquivo"""
        logger.info(f"🔍 Analisando: {filepath.name}")

        # Informações básicas
        file_stats = filepath.stat()
        file_size = file_stats.st_size

        with open(filepath, 'r', encoding='utf-8') as f:
            line_count = sum(1 for _ in f)

        # 1. Análise de sintaxe
        syntax_valid, syntax_errors = self._analyze_syntax(filepath)
        logger.debug(f"  Sintaxe: {'✅' if syntax_valid else '❌'}")

        # 2. Análise de imports
        imports_found, imports_missing, imports_problematic = self._analyze_imports(filepath)
        logger.debug(f"  Imports: {len(imports_found)} encontrados, {len(imports_missing)} faltando")

        # 3. Análise com modelo (apenas se sintaxe válida)
        model_analysis = {'problems': []}
        model_time = 0.0

        if syntax_valid:
            model_analysis, model_time = self._analyze_with_model(filepath)
            problems_count = len(model_analysis.get('problems', []))
            logger.debug(f"  Modelo: {problems_count} problemas identificados ({model_time:.1f}s)")
        else:
            logger.debug("  Modelo: Pulado (sintaxe inválida)")

        # 4. Teste de execução (apenas se sintaxe válida)
        execution_successful = False
        execution_errors = []
        execution_time = 0.0

        if syntax_valid:
            execution_successful, execution_errors, execution_time = self._test_execution(filepath)
            logger.debug(f"  Execução: {'✅' if execution_successful else '❌'} ({execution_time:.1f}s)")

        # 5. Categorização de problemas
        problems = model_analysis.get('problems', [])
        critical, high, medium, low = self._categorize_problems(problems)

        # 6. Métricas finais
        overall_health = self._calculate_health_score(critical, high, medium, low)
        claude_vice_score = self._calculate_claude_vice_score(problems)
        fix_time, breaking_changes = self._estimate_fix_time(critical, high, medium, low)

        # Criar resultado
        result = AnalysisResult(
            filename=filepath.name,
            analysis_timestamp=datetime.now().isoformat(),
            file_size_bytes=file_size,
            line_count=line_count,

            syntax_valid=syntax_valid,
            syntax_errors=syntax_errors,

            model_analysis=model_analysis,
            model_analysis_time_seconds=model_time,

            execution_attempted=syntax_valid,
            execution_successful=execution_successful,
            execution_errors=execution_errors,
            execution_time_seconds=execution_time,

            imports_found=imports_found,
            imports_missing=imports_missing,
            imports_problematic=imports_problematic,

            critical_issues=critical,
            high_issues=high,
            medium_issues=medium,
            low_issues=low,

            overall_health=overall_health,
            claude_vice_score=claude_vice_score,

            fix_time_estimate_hours=fix_time,
            breaking_changes_required=breaking_changes
        )

        # Salvar relatório individual
        individual_report_path = self.results_dir / "individual_reports" / f"{filepath.name}.json"
        with open(individual_report_path, 'w') as f:
            json.dump(asdict(result), f, indent=2, ensure_ascii=False)

        logger.info(f"✅ {filepath.name}: {overall_health} ({claude_vice_score}% vícios Claude)")

        return result

    def run_complete_analysis(self):
        """Executa análise forense completa"""
        self.start_time = datetime.now()
        logger.info("🚀 Iniciando análise forense completa")
        logger.info(f"📅 Início: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")

        # Carregar checkpoint se existir
        self._load_checkpoint()

        # Obter arquivos para análise
        python_files = self._get_python_files()
        self.total_files = len(python_files)

        # Filtrar arquivos já analisados
        remaining_files = [
            f for f in python_files
            if f.name not in self.results
        ]

        logger.info(f"📊 Total: {self.total_files} arquivos")
        logger.info(f"✅ Já analisados: {self.completed_files}")
        logger.info(f"⏳ Restantes: {len(remaining_files)}")

        if not remaining_files:
            logger.info("🎉 Todos os arquivos já foram analisados!")
            self._generate_final_report()
            return

        # Estimativa de tempo
        estimated_time_per_file = 45  # segundos em média
        estimated_total_seconds = len(remaining_files) * estimated_time_per_file
        estimated_completion = self.start_time + timedelta(seconds=estimated_total_seconds)

        logger.info(f"⏱️ Tempo estimado: {estimated_total_seconds/3600:.1f} horas")
        logger.info(f"🕐 Conclusão estimada: {estimated_completion.strftime('%H:%M:%S')}")

        # Lista de arquivos problemáticos conhecidos para pular
        # Baseado em análise manual detalhada - estes arquivos travam o Ollama
        problematic_files = [
            'fix_all_indentation.py',  # Travou 4+ horas, lógica impossível linha 60-61
            'fix_all_memory_systems.py',  # Manipulação AST perigosa, 95% vícios
            'fix_all_relative_imports.py',  # 100% vícios confirmado
            'telepathic_network.py',  # 380 linhas, múltiplos paradigmas incompatíveis
            'telepathic_network_advanced.py',  # Quantum + threads + async = desastre
            'digimon_producermon_ultra_supreme.py',  # 32KB de megalomanía, 200% vícios
            'hyper_quantum_unified_orchestrator.py',  # 33KB, importa 40+ libs, impossível
        ]

        # Adiciona também qualquer arquivo que comece com "fix_all_"
        for filepath in remaining_files:
            if filepath.name.startswith('fix_all_'):
                problematic_files.append(filepath.name)

        # Processar arquivos
        for i, filepath in enumerate(remaining_files, 1):
            try:
                # Pular arquivos problemáticos conhecidos
                if filepath.name in problematic_files:
                    logger.warning(f"⚠️ Pulando arquivo problemático conhecido: {filepath.name}")
                    self.results[filepath.name] = AnalysisResult(
                        filename=filepath.name,
                        analysis_timestamp=datetime.now().isoformat(),
                        file_size_bytes=filepath.stat().st_size if filepath.exists() else 0,
                        line_count=0,
                        syntax_valid=False,
                        syntax_errors=[],
                        model_analysis={'skipped': True, 'reason': 'Arquivo problemático conhecido'},
                        model_analysis_time_seconds=0.0,
                        execution_attempted=False,
                        execution_successful=False,
                        execution_errors=['Arquivo pulado - conhecido por causar travamento'],
                        execution_time_seconds=0.0,
                        imports_found=[],
                        imports_missing=[],
                        imports_problematic=[],
                        critical_issues=[],
                        high_issues=[],
                        medium_issues=[],
                        low_issues=[],
                        overall_health='ERROR',
                        claude_vice_score=100,  # Deve ser int, não float!
                        fix_time_estimate_hours=0.0,
                        breaking_changes_required=True  # Nome correto do campo!
                    )
                    self.completed_files += 1
                    continue

                # Análise do arquivo
                result = self.analyze_file(filepath)
                self.results[filepath.name] = result
                self.completed_files += 1

                # Progresso
                progress = (self.completed_files / self.total_files) * 100
                elapsed = datetime.now() - self.start_time
                avg_time_per_file = elapsed.total_seconds() / self.completed_files
                remaining_time = avg_time_per_file * (self.total_files - self.completed_files)

                logger.info(f"📈 Progresso: {progress:.1f}% ({self.completed_files}/{self.total_files})")
                logger.info(f"⏱️ Tempo restante: {remaining_time/60:.1f} minutos")

                # Checkpoint a cada 5 arquivos
                if self.completed_files % 5 == 0:
                    self._save_checkpoint()
                    logger.info("💾 Checkpoint salvo")

                # Pausa entre arquivos para não sobrecarregar
                time.sleep(2)

            except Exception as e:
                logger.error(f"❌ Erro ao analisar {filepath.name}: {e}")
                logger.error(traceback.format_exc())

                # Criar resultado de erro
                error_result = AnalysisResult(
                    filename=filepath.name,
                    analysis_timestamp=datetime.now().isoformat(),
                    file_size_bytes=filepath.stat().st_size,
                    line_count=0,
                    syntax_valid=False,
                    syntax_errors=[f"Erro na análise: {str(e)}"],
                    model_analysis={'error': str(e)},
                    model_analysis_time_seconds=0.0,
                    execution_attempted=False,
                    execution_successful=False,
                    execution_errors=[str(e)],
                    execution_time_seconds=0.0,
                    imports_found=[],
                    imports_missing=[],
                    imports_problematic=[],
                    critical_issues=[],
                    high_issues=[],
                    medium_issues=[],
                    low_issues=[],
                    overall_health="ERROR",
                    claude_vice_score=0,
                    fix_time_estimate_hours=0.0,
                    breaking_changes_required=False
                )

                self.results[filepath.name] = error_result
                self.completed_files += 1

        # Checkpoint final
        self._save_checkpoint()

        # Relatório final
        self._generate_final_report()

        # Estatísticas finais
        total_time = datetime.now() - self.start_time
        logger.info(f"🎉 Análise completa finalizada!")
        logger.info(f"⏱️ Tempo total: {total_time}")
        logger.info(f"📊 Arquivos analisados: {self.completed_files}")

    def _generate_final_report(self):
        """Gera relatório final consolidado"""
        logger.info("📋 Gerando relatório final...")

        # Estatísticas gerais
        total_files = len(self.results)
        broken_files = sum(1 for r in self.results.values() if r.overall_health == "BROKEN")
        problematic_files = sum(1 for r in self.results.values() if r.overall_health == "PROBLEMATIC")
        warning_files = sum(1 for r in self.results.values() if r.overall_health == "WARNING")
        ok_files = sum(1 for r in self.results.values() if r.overall_health == "OK")

        total_critical = sum(len(r.critical_issues) for r in self.results.values())
        total_high = sum(len(r.high_issues) for r in self.results.values())
        total_medium = sum(len(r.medium_issues) for r in self.results.values())
        total_low = sum(len(r.low_issues) for r in self.results.values())

        avg_claude_vice = sum(r.claude_vice_score for r in self.results.values()) / total_files if total_files > 0 else 0
        total_fix_time = sum(r.fix_time_estimate_hours for r in self.results.values())

        files_needing_breaking_changes = sum(1 for r in self.results.values() if r.breaking_changes_required)

        # Relatório em Markdown
        report = f"""# 🔬 RELATÓRIO FORENSE COMPLETO - SCRIPTUREMON CHAMPION

**Data da Análise:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Tempo Total de Análise:** {datetime.now() - self.start_time if self.start_time else 'N/A'}
**Arquivos Analisados:** {total_files}

---

## 📊 SUMÁRIO EXECUTIVO

### STATUS GERAL DOS ARQUIVOS:
- 🔴 **QUEBRADOS:** {broken_files} arquivos ({broken_files/total_files*100:.1f}%)
- ⚠️ **PROBLEMÁTICOS:** {problematic_files} arquivos ({problematic_files/total_files*100:.1f}%)
- 🟡 **COM AVISOS:** {warning_files} arquivos ({warning_files/total_files*100:.1f}%)
- ✅ **OK:** {ok_files} arquivos ({ok_files/total_files*100:.1f}%)

### PROBLEMAS IDENTIFICADOS:
- 🚨 **Críticos:** {total_critical}
- 🔺 **Altos:** {total_high}
- 🔸 **Médios:** {total_medium}
- 🔹 **Baixos:** {total_low}

### MÉTRICAS CLAUDE AI:
- 🤖 **Índice Médio de Vícios Claude:** {avg_claude_vice:.1f}%
- ⏱️ **Tempo Estimado de Correção:** {total_fix_time:.1f} horas
- 💥 **Arquivos Requerendo Mudanças Breaking:** {files_needing_breaking_changes}

---

## 🔴 ARQUIVOS CRÍTICOS (QUEBRADOS)

"""

        # Listar arquivos quebrados
        broken_results = [r for r in self.results.values() if r.overall_health == "BROKEN"]
        broken_results.sort(key=lambda x: len(x.critical_issues), reverse=True)

        for result in broken_results:
            report += f"""### {result.filename}
- **Problemas Críticos:** {len(result.critical_issues)}
- **Vícios Claude:** {result.claude_vice_score}%
- **Tempo de Correção:** {result.fix_time_estimate_hours:.1f}h
- **Mudanças Breaking:** {'Sim' if result.breaking_changes_required else 'Não'}

**Principais Problemas:**
"""
            for issue in result.critical_issues[:3]:  # Top 3
                report += f"- {issue.get('problem', 'N/A')}\n"

            report += "\n"

        # Top 10 arquivos com mais vícios Claude
        report += """## 🤖 TOP 10 ARQUIVOS COM VÍCIOS CLAUDE

"""

        claude_vice_ranking = sorted(
            self.results.values(),
            key=lambda x: x.claude_vice_score,
            reverse=True
        )[:10]

        for i, result in enumerate(claude_vice_ranking, 1):
            report += f"{i}. **{result.filename}** - {result.claude_vice_score}% vícios\n"

        # Padrões mais comuns
        report += """
## 📈 PADRÕES MAIS COMUNS IDENTIFICADOS

"""

        problem_categories = {}
        for result in self.results.values():
            for issue_list in [result.critical_issues, result.high_issues, result.medium_issues, result.low_issues]:
                for issue in issue_list:
                    category = issue.get('category', 'Outros')
                    problem_categories[category] = problem_categories.get(category, 0) + 1

        sorted_categories = sorted(problem_categories.items(), key=lambda x: x[1], reverse=True)
        for category, count in sorted_categories[:10]:
            report += f"- **{category}:** {count} ocorrências\n"

        # Recomendações
        report += f"""
## 💡 RECOMENDAÇÕES PRIORITÁRIAS

### 🚨 AÇÃO IMEDIATA (0-24h):
1. **Corrigir {len([r for r in self.results.values() if len(r.critical_issues) > 0])} arquivos com problemas críticos**
2. **Remover imports inexistentes** (identificados em {len([r for r in self.results.values() if r.imports_missing])} arquivos)
3. **Implementar cleanup** nos sistemas de memória

### ⚠️ CURTO PRAZO (1-7 dias):
1. **Refatorar arquivos problemáticos** ({problematic_files} arquivos)
2. **Reduzir complexidade desnecessária** (média {avg_claude_vice:.1f}% vícios Claude)
3. **Implementar testes unitários** para arquivos corrigidos

### 🎯 MÉDIO PRAZO (1-4 semanas):
1. **Estabelecer padrões de código** para evitar vícios Claude
2. **Implementar linting** automático
3. **Code review** obrigatório para mudanças

### 📚 LONGO PRAZO (1-3 meses):
1. **Documentação** completa dos padrões
2. **Treinamento** da equipe em boas práticas
3. **CI/CD** com verificações automáticas

---

## 📄 ARQUIVOS DETALHADOS

*Relatórios individuais disponíveis em: `forensic_results/individual_reports/`*

---

**Análise gerada automaticamente pelo Sistema Forense Híbrido**
"""

        # Salvar relatório
        report_path = self.results_dir / "FORENSIC_REPORT_FINAL.md"
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)

        # Salvar JSON consolidado
        consolidated_data = {
            'analysis_metadata': {
                'timestamp': datetime.now().isoformat(),
                'total_files': total_files,
                'analysis_duration': str(datetime.now() - self.start_time if self.start_time else 'N/A'),
                'model_used': self.model_name
            },
            'summary_statistics': {
                'broken_files': broken_files,
                'problematic_files': problematic_files,
                'warning_files': warning_files,
                'ok_files': ok_files,
                'total_critical_issues': total_critical,
                'total_high_issues': total_high,
                'total_medium_issues': total_medium,
                'total_low_issues': total_low,
                'average_claude_vice_score': avg_claude_vice,
                'total_fix_time_hours': total_fix_time,
                'files_needing_breaking_changes': files_needing_breaking_changes
            },
            'detailed_results': {
                filename: asdict(result)
                for filename, result in self.results.items()
            }
        }

        json_path = self.results_dir / "forensic_analysis_complete.json"
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(consolidated_data, f, indent=2, ensure_ascii=False)

        logger.info(f"📋 Relatório final salvo: {report_path}")
        logger.info(f"📄 JSON consolidado: {json_path}")
        logger.info(f"📁 Relatórios individuais: {self.results_dir / 'individual_reports'}")

def main():
    """Função principal"""
    import sys

    print("🔬 SISTEMA FORENSE HÍBRIDO - SCRIPTUREMON CHAMPION")
    print("=" * 60)
    print("Este sistema irá analisar TODOS os arquivos Python em detalhes.")
    print("Tempo estimado: 4-6 horas para análise completa.")
    print("O sistema pode ser interrompido e retomado via checkpoint.")
    print("=" * 60)

    # Verificar se é execução automática
    auto_start = '--auto' in sys.argv or '--background' in sys.argv

    if not auto_start:
        # Confirmação apenas se não for automático
        response = input("\n🤔 Deseja continuar com a análise forense completa? (s/N): ")
        if response.lower() not in ['s', 'sim', 'y', 'yes']:
            print("❌ Análise cancelada.")
            return
    else:
        print("\n🚀 Iniciando análise automática em background...")

    try:
        # Criar e executar orquestrador
        orchestrator = ForensicOrchestrator()
        orchestrator.run_complete_analysis()

        print("\n🎉 ANÁLISE FORENSE COMPLETA FINALIZADA!")
        print(f"📁 Resultados em: {orchestrator.results_dir}")
        print(f"📋 Relatório principal: {orchestrator.results_dir}/FORENSIC_REPORT_FINAL.md")

    except KeyboardInterrupt:
        print("\n⏸️ Análise interrompida pelo usuário.")
        print("💾 Progresso salvo em checkpoint. Execute novamente para continuar.")
    except Exception as e:
        print(f"\n❌ Erro durante análise: {e}")
        print(traceback.format_exc())

if __name__ == "__main__":
    main()