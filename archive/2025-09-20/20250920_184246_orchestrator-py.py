#!/usr/bin/env python3
"""
🧠 ORCHESTRATOR - Coordenador Principal do DigiMundo Swarm
Gerencia e coordena todos os agentes do sistema
"""

import asyncio
import json
import logging
import psutil
import time
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum
import os
from pathlib import Path

# Importações dos agentes
from memory_agent import MemoryAgent
from learning_agent import LearningAgent
from execution_agent import ExecutionAgent
from model_switcher import ModelSwitcher

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("Orchestrator")


class TaskPriority(Enum):
    """Prioridades de tarefas"""
    CRITICAL = 1
    HIGH = 2
    NORMAL = 3
    LOW = 4


class AgentStatus(Enum):
    """Status dos agentes"""
    IDLE = "idle"
    BUSY = "busy"
    ERROR = "error"
    OFFLINE = "offline"


@dataclass
class Task:
    """Estrutura de uma tarefa"""
    id: str
    type: str
    priority: TaskPriority
    data: Dict[str, Any]
    created_at: datetime
    assigned_to: Optional[str] = None
    status: str = "pending"
    result: Optional[Any] = None
    error: Optional[str] = None


class Orchestrator:
    """Coordenador principal do sistema de agentes"""
    
    def __init__(self, config_path: str = "config.json"):
        self.config = self._load_config(config_path)
        self.agents = {}
        self.task_queue = asyncio.Queue()
        self.results_queue = asyncio.Queue()
        self.agent_status = {}
        self.metrics = {
            'tasks_processed': 0,
            'tasks_failed': 0,
            'start_time': datetime.now(),
            'agent_metrics': {}
        }
        
        # Inicializar componentes
        self.model_switcher = ModelSwitcher()
        self._initialize_agents()
        
        logger.info("🚀 Orchestrator inicializado")
    
    def _load_config(self, config_path: str) -> Dict:
        """Carregar configuração"""
        default_config = {
            'base_path': os.path.expanduser("~/Digimundo"),
            'monitor_paths': ["~/Digimundo"],
            'memory': {
                'db_path': "./chroma_db",
                'collection_name': "digimundo_memory"
            },
            'models': {
                'tiny': "tinyllama:latest",
                'small': "llama3.2:3b",
                'medium': "llama3.2:latest",
                'large': "mixtral:8x7b"
            },
            'thresholds': {
                'ram_critical': 90,
                'ram_high': 70,
                'ram_medium': 50,
                'cpu_high': 80
            }
        }
        
        if Path(config_path).exists():
            with open(config_path, 'r') as f:
                loaded_config = json.load(f)
                default_config.update(loaded_config)
        
        return default_config
    
    def _initialize_agents(self):
        """Inicializar todos os agentes"""
        try:
            # Memory Agent
            self.agents['memory'] = MemoryAgent(
                db_path=self.config['memory']['db_path'],
                collection_name=self.config['memory']['collection_name']
            )
            self.agent_status['memory'] = AgentStatus.IDLE
            
            # Learning Agent
            self.agents['learning'] = LearningAgent(
                paths_to_monitor=self.config['monitor_paths'],
                memory_agent=self.agents['memory']
            )
            self.agent_status['learning'] = AgentStatus.IDLE
            
            # Execution Agent
            self.agents['execution'] = ExecutionAgent(
                allowed_commands=self.config.get('allowed_commands', []),
                sandbox_mode=self.config.get('sandbox_mode', True)
            )
            self.agent_status['execution'] = AgentStatus.IDLE
            
            logger.info("✅ Todos os agentes inicializados")
            
        except Exception as e:
            logger.error(f"❌ Erro ao inicializar agentes: {e}")
            raise
    
    def get_system_metrics(self) -> Dict[str, float]:
        """Obter métricas do sistema"""
        return {
            'cpu_percent': psutil.cpu_percent(interval=1),
            'ram_percent': psutil.virtual_memory().percent,
            'ram_available_gb': psutil.virtual_memory().available / (1024**3),
            'disk_percent': psutil.disk_usage('/').percent
        }
    
    async def decide_model(self) -> str:
        """Decidir qual modelo usar baseado nos recursos"""
        metrics = self.get_system_metrics()
        
        # Decisão baseada em RAM disponível
        ram_gb = metrics['ram_available_gb']
        
        if ram_gb < 1:
            return self.config['models']['tiny']
        elif ram_gb < 2:
            return self.config['models']['small']
        elif ram_gb < 4:
            return self.config['models']['medium']
        else:
            # Verificar CPU também para modelos grandes
            if metrics['cpu_percent'] < self.config['thresholds']['cpu_high']:
                return self.config['models']['large']
            else:
                return self.config['models']['medium']
    
    async def process_task(self, task: Task) -> Task:
        """Processar uma tarefa"""
        logger.info(f"📋 Processando tarefa {task.id} (tipo: {task.type})")
        
        try:
            # Decidir modelo apropriado
            model = await self.decide_model()
            await self.model_switcher.switch_model(model)
            
            # Roteamento de tarefas
            if task.type == "query":
                result = await self._handle_query(task)
            elif task.type == "learn":
                result = await self._handle_learn(task)
            elif task.type == "execute":
                result = await self._handle_execute(task)
            elif task.type == "remember":
                result = await self._handle_remember(task)
            else:
                raise ValueError(f"Tipo de tarefa desconhecido: {task.type}")
            
            task.status = "completed"
            task.result = result
            self.metrics['tasks_processed'] += 1
            
        except Exception as e:
            logger.error(f"❌ Erro ao processar tarefa {task.id}: {e}")
            task.status = "failed"
            task.error = str(e)
            self.metrics['tasks_failed'] += 1
        
        return task
    
    async def _handle_query(self, task: Task) -> Any:
        """Processar consulta usando memória e LLM"""
        query = task.data.get('query', '')
        
        # Buscar memórias relevantes
        memories = await self.agents['memory'].search(query, n_results=5)
        
        # Construir contexto
        context = "\n".join([m['content'] for m in memories])
        
        # Gerar resposta
        response = await self.model_switcher.generate(
            prompt=f"Contexto:\n{context}\n\nPergunta: {query}\n\nResposta:",
            temperature=0.7
        )
        
        # Armazenar interação na memória
        await self.agents['memory'].store({
            'type': 'interaction',
            'query': query,
            'response': response,
            'timestamp': datetime.now().isoformat()
        })
        
        return response
    
    async def _handle_learn(self, task: Task) -> Any:
        """Processar aprendizado de novos arquivos"""
        file_path = task.data.get('file_path')
        
        if not file_path:
            # Aprender de todos os arquivos monitorados
            result = await self.agents['learning'].scan_all()
        else:
            # Aprender de arquivo específico
            result = await self.agents['learning'].learn_from_file(file_path)
        
        return result
    
    async def _handle_execute(self, task: Task) -> Any:
        """Executar comando do sistema"""
        command = task.data.get('command')
        
        # Verificar com LLM se o comando é seguro
        safety_check = await self.model_switcher.generate(
            prompt=f"Este comando é seguro para executar? Responda apenas SIM ou NÃO: {command}",
            temperature=0.1
        )
        
        if "SIM" in safety_check.upper():
            result = await self.agents['execution'].execute(command)
        else:
            result = {
                'success': False,
                'error': f"Comando bloqueado por segurança: {command}"
            }
        
        # Registrar execução
        await self.agents['memory'].store({
            'type': 'execution',
            'command': command,
            'result': result,
            'timestamp': datetime.now().isoformat()
        })
        
        return result
    
    async def _handle_remember(self, task: Task) -> Any:
        """Armazenar informação na memória"""
        content = task.data.get('content')
        metadata = task.data.get('metadata', {})
        
        result = await self.agents['memory'].store(
            content=content,
            metadata=metadata
        )
        
        return result
    
    async def task_dispatcher(self):
        """Dispatcher principal de tarefas"""
        logger.info("🚀 Task dispatcher iniciado")
        
        while True:
            try:
                # Pegar próxima tarefa
                task = await self.task_queue.get()
                
                # Verificar recursos antes de processar
                metrics = self.get_system_metrics()
                
                # Se recursos críticos, pausar
                if metrics['ram_percent'] > self.config['thresholds']['ram_critical']:
                    logger.warning("⚠️ RAM crítica, pausando processamento...")
                    await asyncio.sleep(10)
                    await self.task_queue.put(task)  # Recolocar na fila
                    continue
                
                # Processar tarefa
                completed_task = await self.process_task(task)
                
                # Colocar resultado na fila
                await self.results_queue.put(completed_task)
                
            except Exception as e:
                logger.error(f"Erro no dispatcher: {e}")
                await asyncio.sleep(5)
    
    async def monitor_agents(self):
        """Monitorar saúde dos agentes"""
        while True:
            try:
                for agent_name, agent in self.agents.items():
                    # Verificar se agente está respondendo
                    if hasattr(agent, 'health_check'):
                        is_healthy = await agent.health_check()
                        
                        if is_healthy:
                            self.agent_status[agent_name] = AgentStatus.IDLE
                        else:
                            self.agent_status[agent_name] = AgentStatus.ERROR
                            logger.error(f"❌ Agente {agent_name} não está saudável")
                
                # Log de status
                logger.info(f"📊 Status dos agentes: {dict(self.agent_status)}")
                
                await asyncio.sleep(30)  # Verificar a cada 30 segundos
                
            except Exception as e:
                logger.error(f"Erro ao monitorar agentes: {e}")
                await asyncio.sleep(60)
    
    async def auto_learn_cycle(self):
        """Ciclo automático de aprendizado"""
        while True:
            try:
                # Criar tarefa de aprendizado
                learn_task = Task(
                    id=f"auto_learn_{int(time.time())}",
                    type="learn",
                    priority=TaskPriority.LOW,
                    data={},
                    created_at=datetime.now()
                )
                
                await self.task_queue.put(learn_task)
                
                # Aguardar intervalo (1 hora por padrão)
                await asyncio.sleep(3600)
                
            except Exception as e:
                logger.error(f"Erro no ciclo de aprendizado: {e}")
                await asyncio.sleep(300)
    
    def add_task(self, task_type: str, data: Dict[str, Any], 
                 priority: TaskPriority = TaskPriority.NORMAL) -> str:
        """Adicionar nova tarefa à fila"""
        task_id = f"{task_type}_{int(time.time() * 1000)}"
        
        task = Task(
            id=task_id,
            type=task_type,
            priority=priority,
            data=data,
            created_at=datetime.now()
        )
        
        # Adicionar de forma síncrona (será processada async)
        asyncio.create_task(self.task_queue.put(task))
        
        logger.info(f"📝 Tarefa {task_id} adicionada à fila")
        return task_id
    
    def get_metrics(self) -> Dict[str, Any]:
        """Obter métricas do sistema"""
        uptime = (datetime.now() - self.metrics['start_time']).total_seconds()
        
        return {
            'uptime_seconds': uptime,
            'tasks_processed': self.metrics['tasks_processed'],
            'tasks_failed': self.metrics['tasks_failed'],
            'success_rate': (self.metrics['tasks_processed'] / 
                           (self.metrics['tasks_processed'] + self.metrics['tasks_failed']) 
                           if self.metrics['tasks_processed'] > 0 else 0),
            'agent_status': dict(self.agent_status),
            'system_metrics': self.get_system_metrics(),
            'queue_size': self.task_queue.qsize()
        }
    
    async def run(self):
        """Executar o orchestrator"""
        logger.info("🚀 Iniciando DigiMundo Orchestrator...")
        
        # Criar tarefas assíncronas
        tasks = [
            asyncio.create_task(self.task_dispatcher()),
            asyncio.create_task(self.monitor_agents()),
            asyncio.create_task(self.auto_learn_cycle())
        ]
        
        # Aguardar todas as tarefas
        try:
            await asyncio.gather(*tasks)
        except KeyboardInterrupt:
            logger.info("🛑 Encerrando Orchestrator...")
            for task in tasks:
                task.cancel()


def main():
    """Função principal"""
    orchestrator = Orchestrator()
    
    # Adicionar algumas tarefas de exemplo
    orchestrator.add_task("learn", {})
    orchestrator.add_task("query", {"query": "O que é o DigiMundo?"})
    
    # Executar
    asyncio.run(orchestrator.run())


if __name__ == "__main__":
    main()
