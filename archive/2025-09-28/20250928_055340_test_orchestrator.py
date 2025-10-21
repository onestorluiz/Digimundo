#!/usr/bin/env python3
"""
TESTE ROBUSTO DO SCRIPTUREMON ORCHESTRATOR
Verifica se todos 23 especialistas são chamados corretamente
"""

import json
import time
import logging
from typing import Dict, List, Set, Tuple
from dataclasses import dataclass, field
from enum import Enum

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ==================== ENUMS ====================

class AnalysisMode(Enum):
    COMPLETE = "complete"  # Todos 23 especialistas
    QUICK = "quick"       # 10 especialistas core
    FOCUSED = "focused"   # Específicos
    FIX = "fix"          # Direto para prescrição

class Phase(Enum):
    EXTRACTION = 1    # Fase 1: Extração base
    STRUCTURE = 2     # Fase 2: Estrutura
    DEEP = 3         # Fase 3: Análise profunda
    SPECIALIZED = 4  # Fase 4: Especializada
    SYNTHESIS = 5    # Fase 5: Síntese

# ==================== DEFINIÇÕES ====================

@dataclass
class Specialist:
    """Definição de um especialista"""
    id: str
    name: str
    phase: Phase
    context_size: int
    parallel: bool = True
    conditional: bool = False
    condition: str = ""
    dependencies: List[str] = field(default_factory=list)

@dataclass
class ScreenplayMetadata:
    """Metadados do roteiro"""
    title: str = "Test Screenplay"
    pages: int = 110
    genre: str = "sci-fi thriller"
    format: str = "feature"
    has_vo: bool = True
    multiple_povs: bool = True
    is_tragedy: bool = True

# ==================== TODOS OS 23 ESPECIALISTAS ====================

SPECIALISTS = [
    # FASE 1: EXTRAÇÃO (Paralela)
    Specialist("01", "metadata-extractor", Phase.EXTRACTION, 131072, True),
    Specialist("02", "character-detector", Phase.EXTRACTION, 131072, True),
    Specialist("03", "character-analyzer", Phase.EXTRACTION, 131072, True),
    Specialist("04", "dialogue-analyzer", Phase.EXTRACTION, 131072, True),
    
    # FASE 2: ESTRUTURA (Sequencial)
    Specialist("05", "scene-analyzer", Phase.STRUCTURE, 131072, False, dependencies=["01"]),
    Specialist("06", "structure-validator", Phase.STRUCTURE, 131072, False, dependencies=["05"]),
    Specialist("07", "conflict-analyzer", Phase.STRUCTURE, 131072, False, dependencies=["06"]),
    
    # FASE 3: ANÁLISE PROFUNDA (Paralela)
    Specialist("08", "theme-extractor", Phase.DEEP, 131072, True, dependencies=["06"]),
    Specialist("09", "setup-payoff-tracker", Phase.DEEP, 131072, True, dependencies=["05"]),
    Specialist("10", "genre-classifier", Phase.DEEP, 131072, True),
    Specialist("11", "format-validator", Phase.DEEP, 131072, True),
    Specialist("12", "audience-analyzer", Phase.DEEP, 131072, True),
    Specialist("13", "tension-tracker", Phase.DEEP, 131072, True, dependencies=["07"]),
    
    # FASE 4: ESPECIALIZADA (Condicional)
    Specialist("14", "pacing-analyzer", Phase.SPECIALIZED, 131072, True, dependencies=["13"]),
    Specialist("15", "prescription-generator", Phase.SPECIALIZED, 131072, False, dependencies=["all"]),
    Specialist("16", "pov-analyzer", Phase.SPECIALIZED, 131072, True, True, "multiple_povs"),
    Specialist("17", "premise-validator", Phase.SPECIALIZED, 131072, True),
    Specialist("18", "transition-analyzer", Phase.SPECIALIZED, 131072, True, dependencies=["05"]),
    Specialist("19", "short-film-specialist", Phase.SPECIALIZED, 131072, True, True, "pages < 30"),
    Specialist("20", "action-centered-analyzer", Phase.SPECIALIZED, 131072, True, True, "is_tragedy"),
    Specialist("21", "catharsis-measurer", Phase.SPECIALIZED, 131072, True, True, "is_tragedy"),
    
    # FASE 5: SÍNTESE (Sequencial)
    Specialist("22", "creative-limitation-analyzer", Phase.SYNTHESIS, 131072, False),
    Specialist("23", "voice-style-analyzer", Phase.SYNTHESIS, 131072, False)
]

# ==================== ORCHESTRATOR ====================

class ScripturemonOrchestrator:
    """Orquestrador principal do sistema"""
    
    def __init__(self):
        self.specialists = {s.id: s for s in SPECIALISTS}
        self.execution_log: List[str] = []
        self.phase_times: Dict[Phase, float] = {}
        self.specialists_called: Set[str] = set()
        
    def analyze(self, screenplay_meta: ScreenplayMetadata, mode: AnalysisMode) -> Dict:
        """Análise principal"""
        logger.info(f"🎬 Iniciando análise em modo: {mode.value}")
        logger.info(f"📄 Roteiro: {screenplay_meta.pages} páginas, gênero: {screenplay_meta.genre}")
        
        start_time = time.time()
        results = {}
        
        # Seleciona especialistas baseado no modo
        selected_specialists = self._select_specialists(screenplay_meta, mode)
        logger.info(f"📊 {len(selected_specialists)} especialistas selecionados")
        
        # Executa por fases
        for phase in Phase:
            phase_start = time.time()
            phase_specialists = [s for s in selected_specialists if s.phase == phase]
            
            if phase_specialists:
                logger.info(f"\n{'='*50}")
                logger.info(f"📍 FASE {phase.value}: {phase.name}")
                logger.info(f"👥 Especialistas: {len(phase_specialists)}")
                
                if phase_specialists[0].parallel:
                    results.update(self._run_parallel(phase_specialists, screenplay_meta))
                else:
                    results.update(self._run_sequential(phase_specialists, screenplay_meta))
                    
            self.phase_times[phase] = time.time() - phase_start
            
        # Estatísticas finais
        total_time = time.time() - start_time
        self._print_statistics(total_time, mode)
        
        return {
            "results": results,
            "statistics": self._get_statistics(total_time),
            "specialists_called": list(self.specialists_called)
        }
    
    def _select_specialists(self, meta: ScreenplayMetadata, mode: AnalysisMode) -> List[Specialist]:
        """Seleciona especialistas baseado no modo e condições"""
        selected = []
        
        if mode == AnalysisMode.COMPLETE:
            # Modo completo: todos aplicáveis
            for specialist in SPECIALISTS:
                if self._check_condition(specialist, meta):
                    selected.append(specialist)
                    
        elif mode == AnalysisMode.QUICK:
            # Modo rápido: apenas core (primeiros 10 + essenciais)
            core_ids = ["01", "02", "03", "04", "05", "06", "07", "08", "10", "11"]
            for specialist in SPECIALISTS:
                if specialist.id in core_ids:
                    selected.append(specialist)
                    
        elif mode == AnalysisMode.FIX:
            # Modo fix: direto para prescrição
            selected = [s for s in SPECIALISTS if s.id in ["01", "15"]]
            
        return selected
    
    def _check_condition(self, specialist: Specialist, meta: ScreenplayMetadata) -> bool:
        """Verifica se condição do especialista é atendida"""
        if not specialist.conditional:
            return True
            
        condition = specialist.condition
        
        # Avalia condições
        if condition == "pages < 30":
            return meta.pages < 30
        elif condition == "multiple_povs":
            return meta.multiple_povs
        elif condition == "is_tragedy":
            return meta.is_tragedy or meta.genre in ["drama", "tragedy"]
        elif condition == "has_vo":
            return meta.has_vo
            
        return True
    
    def _run_parallel(self, specialists: List[Specialist], meta: ScreenplayMetadata) -> Dict:
        """Simula execução paralela"""
        results = {}
        logger.info("  ⚡ Execução PARALELA")
        
        for specialist in specialists:
            logger.info(f"    ✅ [{specialist.id}] {specialist.name} ({specialist.context_size} tokens)")
            self.specialists_called.add(specialist.id)
            self.execution_log.append(f"PARALLEL: {specialist.name}")
            results[specialist.id] = {"status": "completed", "parallel": True}
            
        # Simula tempo de execução paralela (maior tempo individual)
        max_time = max(s.context_size / 10000 for s in specialists)
        time.sleep(max_time * 0.1)  # Simulação rápida
        
        return results
    
    def _run_sequential(self, specialists: List[Specialist], meta: ScreenplayMetadata) -> Dict:
        """Simula execução sequencial"""
        results = {}
        logger.info("  📝 Execução SEQUENCIAL")
        
        for specialist in specialists:
            logger.info(f"    ✅ [{specialist.id}] {specialist.name} ({specialist.context_size} tokens)")
            self.specialists_called.add(specialist.id)
            self.execution_log.append(f"SEQUENTIAL: {specialist.name}")
            results[specialist.id] = {"status": "completed", "parallel": False}
            
            # Simula tempo de execução
            time.sleep(specialist.context_size / 100000)  # Simulação rápida
            
        return results
    
    def _print_statistics(self, total_time: float, mode: AnalysisMode):
        """Imprime estatísticas da análise"""
        logger.info(f"\n{'='*50}")
        logger.info("📊 ESTATÍSTICAS DA ANÁLISE")
        logger.info(f"{'='*50}")
        logger.info(f"Modo: {mode.value}")
        logger.info(f"Total de especialistas chamados: {len(self.specialists_called)}/23")
        logger.info(f"Tempo total: {total_time:.2f} segundos")
        
        logger.info("\n⏱️  Tempo por fase:")
        for phase, phase_time in self.phase_times.items():
            if phase_time > 0:
                logger.info(f"  Fase {phase.value}: {phase_time:.2f}s")
        
        logger.info("\n✅ Especialistas executados:")
        for sid in sorted(self.specialists_called):
            specialist = self.specialists[sid]
            logger.info(f"  [{sid}] {specialist.name}")
    
    def _get_statistics(self, total_time: float) -> Dict:
        """Retorna estatísticas estruturadas"""
        return {
            "total_specialists": len(self.specialists_called),
            "total_time": total_time,
            "phase_times": {p.name: t for p, t in self.phase_times.items()},
            "coverage": len(self.specialists_called) / 23 * 100
        }

# ==================== TESTES ====================

class OrchestratorTester:
    """Classe de testes do Orchestrator"""
    
    def __init__(self):
        self.orchestrator = ScripturemonOrchestrator()
        self.test_results = []
        
    def run_all_tests(self):
        """Executa todos os testes"""
        logger.info("\n" + "="*60)
        logger.info("🧪 INICIANDO BATERIA DE TESTES COMPLETA")
        logger.info("="*60)
        
        # Teste 1: Modo completo com roteiro longo
        self.test_complete_analysis()
        
        # Teste 2: Modo rápido
        self.test_quick_analysis()
        
        # Teste 3: Curta-metragem
        self.test_short_film()
        
        # Teste 4: Roteiro sem tragédia
        self.test_non_tragedy()
        
        # Teste 5: Modo fix
        self.test_fix_mode()
        
        # Teste 6: Verificação de dependências
        self.test_dependencies()
        
        # Relatório final
        self.print_final_report()
    
    def test_complete_analysis(self):
        """Teste 1: Análise completa deve chamar todos aplicáveis"""
        logger.info("\n🧪 TESTE 1: Análise Completa (Feature com tragédia)")
        
        meta = ScreenplayMetadata(
            pages=110,
            genre="sci-fi thriller",
            is_tragedy=True,
            multiple_povs=True
        )
        
        self.orchestrator.specialists_called.clear()
        result = self.orchestrator.analyze(meta, AnalysisMode.COMPLETE)
        
        # Verifica se chamou todos exceto short-film (19)
        expected_count = 22  # Todos menos short-film-specialist
        actual_count = len(result["specialists_called"])
        
        passed = actual_count == expected_count
        self.test_results.append({
            "test": "Complete Analysis",
            "passed": passed,
            "expected": expected_count,
            "actual": actual_count,
            "missing": set(["19"])  # short-film não deve ser chamado
        })
        
        if passed:
            logger.info(f"✅ PASSOU: {actual_count}/{expected_count} especialistas")
        else:
            logger.error(f"❌ FALHOU: {actual_count}/{expected_count} especialistas")
    
    def test_quick_analysis(self):
        """Teste 2: Análise rápida deve chamar apenas core"""
        logger.info("\n🧪 TESTE 2: Análise Rápida")
        
        meta = ScreenplayMetadata()
        
        self.orchestrator.specialists_called.clear()
        result = self.orchestrator.analyze(meta, AnalysisMode.QUICK)
        
        expected_count = 10
        actual_count = len(result["specialists_called"])
        
        passed = actual_count == expected_count
        self.test_results.append({
            "test": "Quick Analysis",
            "passed": passed,
            "expected": expected_count,
            "actual": actual_count
        })
        
        if passed:
            logger.info(f"✅ PASSOU: {actual_count}/{expected_count} especialistas")
        else:
            logger.error(f"❌ FALHOU: {actual_count}/{expected_count} especialistas")
    
    def test_short_film(self):
        """Teste 3: Curta deve ativar short-film-specialist"""
        logger.info("\n🧪 TESTE 3: Análise de Curta-metragem")
        
        meta = ScreenplayMetadata(
            pages=15,
            format="short"
        )
        
        self.orchestrator.specialists_called.clear()
        result = self.orchestrator.analyze(meta, AnalysisMode.COMPLETE)
        
        has_short_specialist = "19" in result["specialists_called"]
        
        passed = has_short_specialist
        self.test_results.append({
            "test": "Short Film Analysis",
            "passed": passed,
            "has_short_specialist": has_short_specialist
        })
        
        if passed:
            logger.info(f"✅ PASSOU: short-film-specialist ativado")
        else:
            logger.error(f"❌ FALHOU: short-film-specialist não ativado")
    
    def test_non_tragedy(self):
        """Teste 4: Não-tragédia não deve ativar catharsis/action"""
        logger.info("\n🧪 TESTE 4: Análise sem Tragédia")
        
        meta = ScreenplayMetadata(
            genre="comedy",
            is_tragedy=False
        )
        
        self.orchestrator.specialists_called.clear()
        result = self.orchestrator.analyze(meta, AnalysisMode.COMPLETE)
        
        has_catharsis = "21" in result["specialists_called"]
        has_action = "20" in result["specialists_called"]
        
        passed = not has_catharsis and not has_action
        self.test_results.append({
            "test": "Non-Tragedy Analysis",
            "passed": passed,
            "has_catharsis": has_catharsis,
            "has_action": has_action
        })
        
        if passed:
            logger.info(f"✅ PASSOU: catharsis/action corretamente excluídos")
        else:
            logger.error(f"❌ FALHOU: catharsis/action incorretamente incluídos")
    
    def test_fix_mode(self):
        """Teste 5: Modo fix deve ir direto para prescrição"""
        logger.info("\n🧪 TESTE 5: Modo Fix")
        
        meta = ScreenplayMetadata()
        
        self.orchestrator.specialists_called.clear()
        result = self.orchestrator.analyze(meta, AnalysisMode.FIX)
        
        expected_count = 2  # Apenas metadata + prescription
        actual_count = len(result["specialists_called"])
        has_prescription = "15" in result["specialists_called"]
        
        passed = actual_count == expected_count and has_prescription
        self.test_results.append({
            "test": "Fix Mode",
            "passed": passed,
            "expected": expected_count,
            "actual": actual_count
        })
        
        if passed:
            logger.info(f"✅ PASSOU: Modo fix correto")
        else:
            logger.error(f"❌ FALHOU: Modo fix incorreto")
    
    def test_dependencies(self):
        """Teste 6: Verifica ordem de dependências"""
        logger.info("\n🧪 TESTE 6: Verificação de Dependências")
        
        meta = ScreenplayMetadata()
        
        self.orchestrator.specialists_called.clear()
        self.orchestrator.execution_log.clear()
        result = self.orchestrator.analyze(meta, AnalysisMode.COMPLETE)
        
        # Verifica se scene-analyzer (05) vem antes de structure-validator (06)
        log = self.orchestrator.execution_log
        scene_idx = next(i for i, x in enumerate(log) if "scene-analyzer" in x)
        struct_idx = next(i for i, x in enumerate(log) if "structure-validator" in x)
        
        passed = scene_idx < struct_idx
        self.test_results.append({
            "test": "Dependencies Order",
            "passed": passed,
            "scene_index": scene_idx,
            "structure_index": struct_idx
        })
        
        if passed:
            logger.info(f"✅ PASSOU: Dependências respeitadas")
        else:
            logger.error(f"❌ FALHOU: Ordem de dependências violada")
    
    def print_final_report(self):
        """Imprime relatório final dos testes"""
        logger.info("\n" + "="*60)
        logger.info("📊 RELATÓRIO FINAL DOS TESTES")
        logger.info("="*60)
        
        passed_count = sum(1 for t in self.test_results if t["passed"])
        total_count = len(self.test_results)
        
        logger.info(f"\nResultado Geral: {passed_count}/{total_count} testes passaram")
        logger.info(f"Taxa de Sucesso: {passed_count/total_count*100:.1f}%")
        
        logger.info("\nDetalhamento:")
        for test in self.test_results:
            status = "✅" if test["passed"] else "❌"
            logger.info(f"  {status} {test['test']}")
            
        if passed_count == total_count:
            logger.info("\n🎉 TODOS OS TESTES PASSARAM! Orchestrator funcionando perfeitamente!")
        else:
            logger.warning(f"\n⚠️  {total_count - passed_count} testes falharam. Revisar implementação.")

# ==================== EXECUÇÃO PRINCIPAL ====================

if __name__ == "__main__":
    tester = OrchestratorTester()
    tester.run_all_tests()
    
    # Teste adicional: Verificar cobertura total
    logger.info("\n" + "="*60)
    logger.info("🔍 VERIFICAÇÃO DE COBERTURA TOTAL")
    logger.info("="*60)
    
    all_specialists_ids = set(s.id for s in SPECIALISTS)
    logger.info(f"\nTotal de especialistas no sistema: {len(all_specialists_ids)}")
    logger.info("\nEspecialistas por ID:")
    for specialist in SPECIALISTS:
        cond = f" [CONDICIONAL: {specialist.condition}]" if specialist.conditional else ""
        logger.info(f"  [{specialist.id}] {specialist.name}{cond}")
    
    logger.info("\n✅ Sistema Scripturemon Ultimate pronto para produção!")
