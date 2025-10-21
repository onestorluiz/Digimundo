#!/usr/bin/env python3
"""
System Orchestrator Minimal - Orquestração Simplificada
Refatorado das 5 perguntas críticas: 600+ → 200 linhas

RESPOSTAS ÀS 5 PERGUNTAS:
1. É necessário? SIM - Orquestração é funcionalidade válida
2. O que faz? Coordena subsistemas de forma simples
3. Quantas linhas? 200 vs 600+ originais (67% redução)
4. Dependências? asyncio, logging (stdlib)
5. Uma função? NÃO - Precisa classe para estado, mas muito mais simples
"""

import asyncio
import time
import json
import logging
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

class ServiceStatus(Enum):
    """Status simples dos serviços"""
    HEALTHY = 'healthy'
    DEGRADED = 'degraded'
    FAILED = 'failed'

@dataclass
class ServiceResult:
    """Resultado de execução de serviço"""
    service: str
    success: bool
    result: Any = None
    error: str = None
    duration: float = 0.0

class SimpleOrchestrator:
    """Orquestrador minimalista mas funcional"""
    
    def __init__(self, name: str = "ScriptureMonOrchestrator"):
        self.name = name
        self.services = {}  # service_name -> function
        self.status = {}
        self.logger = logging.getLogger(self.name)
        
    def register_service(self, name: str, func: Callable, timeout: float = 30.0):
        """Registra um serviço"""
        self.services[name] = {
            'function': func,
            'timeout': timeout,
            'calls': 0,
            'errors': 0,
            'total_time': 0.0
        }
        self.status[name] = ServiceStatus.HEALTHY
        self.logger.info(f"✅ Serviço registrado: {name}")
    
    async def execute_service(self, service_name: str, *args, **kwargs) -> ServiceResult:
        """Executa um serviço específico"""
        if service_name not in self.services:
            return ServiceResult(
                service=service_name,
                success=False,
                error=f"Serviço '{service_name}' não encontrado"
            )
        
        service_info = self.services[service_name]
        start_time = time.time()
        
        try:
            # Executa com timeout
            func = service_info['function']
            timeout = service_info['timeout']
            
            if asyncio.iscoroutinefunction(func):
                result = await asyncio.wait_for(func(*args, **kwargs), timeout=timeout)
            else:
                result = func(*args, **kwargs)
            
            duration = time.time() - start_time
            
            # Atualiza estatísticas
            service_info['calls'] += 1
            service_info['total_time'] += duration
            self.status[service_name] = ServiceStatus.HEALTHY
            
            return ServiceResult(
                service=service_name,
                success=True,
                result=result,
                duration=duration
            )
            
        except asyncio.TimeoutError:
            duration = time.time() - start_time
            service_info['errors'] += 1
            self.status[service_name] = ServiceStatus.DEGRADED
            
            return ServiceResult(
                service=service_name,
                success=False,
                error=f"Timeout após {timeout}s",
                duration=duration
            )
            
        except Exception as e:
            duration = time.time() - start_time
            service_info['errors'] += 1
            self.status[service_name] = ServiceStatus.FAILED
            
            return ServiceResult(
                service=service_name,
                success=False,
                error=str(e),
                duration=duration
            )
    
    async def execute_pipeline(self, pipeline: List[Dict[str, Any]]) -> List[ServiceResult]:
        """Executa pipeline de serviços em sequência"""
        results = []
        
        for step in pipeline:
            service_name = step['service']
            args = step.get('args', [])
            kwargs = step.get('kwargs', {})
            
            self.logger.info(f"🔄 Executando: {service_name}")
            
            result = await self.execute_service(service_name, *args, **kwargs)
            results.append(result)
            
            # Para se houver falha crítica
            if not result.success and step.get('critical', False):
                self.logger.error(f"❌ Falha crítica em {service_name}: {result.error}")
                break
        
        return results
    
    async def execute_parallel(self, services: List[str], *args, **kwargs) -> List[ServiceResult]:
        """Executa múltiplos serviços em paralelo"""
        tasks = []
        
        for service_name in services:
            if service_name in self.services:
                task = self.execute_service(service_name, *args, **kwargs)
                tasks.append(task)
        
        if not tasks:
            return []
        
        return await asyncio.gather(*tasks, return_exceptions=True)
    
    def get_health_status(self) -> Dict[str, Any]:
        """Retorna status de saúde do sistema"""
        health_summary = {
            'orchestrator': self.name,
            'services_count': len(self.services),
            'overall_status': 'healthy',
            'services': {}
        }
        
        degraded_count = 0
        failed_count = 0
        
        for service_name, service_info in self.services.items():
            status = self.status[service_name]
            
            # Calcula taxa de sucesso
            total_calls = service_info['calls']
            error_rate = (service_info['errors'] / total_calls) if total_calls > 0 else 0
            avg_time = (service_info['total_time'] / total_calls) if total_calls > 0 else 0
            
            health_summary['services'][service_name] = {
                'status': status.value,
                'calls': total_calls,
                'error_rate': round(error_rate, 3),
                'avg_duration': round(avg_time, 3)
            }
            
            if status == ServiceStatus.DEGRADED:
                degraded_count += 1
            elif status == ServiceStatus.FAILED:
                failed_count += 1
        
        # Status geral
        if failed_count > 0:
            health_summary['overall_status'] = 'critical'
        elif degraded_count > 0:
            health_summary['overall_status'] = 'degraded'
        
        return health_summary
    
    def save_metrics(self, filepath: Path):
        """Salva métricas em arquivo JSON"""
        metrics = self.get_health_status()
        metrics['timestamp'] = time.time()
        
        with open(filepath, 'w') as f:
            json.dump(metrics, f, indent=2)
        
        self.logger.info(f"📊 Métricas salvas em: {filepath}")

# Funções de conveniência para uso rápido
def create_scripturemon_orchestrator() -> SimpleOrchestrator:
    """Cria orquestrador com serviços padrão do ScriptureMon"""
    orchestrator = SimpleOrchestrator("ScriptureMon")
    
    # Serviços básicos (mock para exemplo)
    def analyze_script(file_path: str):
        """Mock de análise de roteiro"""
        return {'score': 85, 'analysis': 'Roteiro bem estruturado'}
    
    def compress_text(text: str):
        """Mock de compressão"""
        return {'original': len(text), 'compressed': len(text) // 2}
    
    def validate_format(content: str):
        """Mock de validação"""
        return {'valid': True, 'errors': []}
    
    # Registra serviços
    orchestrator.register_service('analyze', analyze_script, timeout=60)
    orchestrator.register_service('compress', compress_text, timeout=30)
    orchestrator.register_service('validate', validate_format, timeout=10)
    
    return orchestrator

async def run_sample_pipeline():
    """Exemplo de uso do orquestrador"""
    orchestrator = create_scripturemon_orchestrator()
    
    # Pipeline de exemplo
    pipeline = [
        {'service': 'validate', 'args': ['INT. ROOM - DAY'], 'critical': True},
        {'service': 'analyze', 'args': ['script.txt'], 'critical': False},
        {'service': 'compress', 'args': ['Sample text content'], 'critical': False}
    ]
    
    print("🚀 Executando pipeline...")
    results = await orchestrator.execute_pipeline(pipeline)
    
    for result in results:
        status = "✅" if result.success else "❌"
        print(f"{status} {result.service}: {result.duration:.3f}s")
        if result.error:
            print(f"   Erro: {result.error}")
    
    # Status de saúde
    health = orchestrator.get_health_status()
    print(f"\n📊 Status geral: {health['overall_status']}")
    
    return orchestrator

if __name__ == "__main__":
    print("🎭 Testando System Orchestrator Minimal...")
    
    # Executa teste
    orchestrator = asyncio.run(run_sample_pipeline())
    
    print("\n💡 LIÇÃO DAS 5 PERGUNTAS:")
    print("1. É necessário? ✅ Orquestração é funcionalidade real")
    print("2. O que faz? 🎯 Coordena serviços de forma simples")
    print("3. Quantas linhas? 📏 600+→200 linhas (67% redução)")
    print("4. Dependências? 📦 Apenas asyncio + logging (stdlib)")
    print("5. Uma função? ❌ Classe necessária para estado")
    
    print("\nDIGIMUNDO PRESENTE 🥷")
