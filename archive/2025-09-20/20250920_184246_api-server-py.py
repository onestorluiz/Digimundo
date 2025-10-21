#!/usr/bin/env python3
"""
🌐 API SERVER - Interface REST para DigiMundo Swarm
Controle e monitoramento via API
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional
import asyncio
import json
import logging
from datetime import datetime
import uvicorn

# Importar componentes
from orchestrator import Orchestrator, TaskPriority

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("APIServer")

# Criar aplicação FastAPI
app = FastAPI(
    title="DigiMundo Swarm API",
    description="API para controle do sistema de agentes autônomos DigiMundo",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Instância global do orchestrator
orchestrator = None


# Modelos Pydantic
class TaskRequest(BaseModel):
    """Requisição para criar tarefa"""
    type: str = Field(..., description="Tipo da tarefa: query, learn, execute, remember")
    data: Dict[str, Any] = Field(..., description="Dados da tarefa")
    priority: str = Field(default="normal", description="Prioridade: critical, high, normal, low")
    
    class Config:
        json_schema_extra = {
            "example": {
                "type": "query",
                "data": {"query": "O que é o DigiMundo?"},
                "priority": "normal"
            }
        }


class CommandRequest(BaseModel):
    """Requisição para executar comando"""
    command: str = Field(..., description="Comando a executar")
    timeout: Optional[int] = Field(default=60, description="Timeout em segundos")
    
    class Config:
        json_schema_extra = {
            "example": {
                "command": "ls -la",
                "timeout": 30
            }
        }


class LearnRequest(BaseModel):
    """Requisição para aprender de arquivo"""
    file_path: Optional[str] = Field(None, description="Caminho do arquivo (None para scan completo)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "file_path": "~/Digimundo/docs/README.md"
            }
        }


class MemoryRequest(BaseModel):
    """Requisição para armazenar memória"""
    content: str = Field(..., description="Conteúdo a armazenar")
    metadata: Optional[Dict[str, Any]] = Field(default={}, description="Metadados")
    
    class Config:
        json_schema_extra = {
            "example": {
                "content": "DigiMundo é um sistema de consciência artificial",
                "metadata": {"type": "definition", "topic": "digimundo"}
            }
        }


class QueryRequest(BaseModel):
    """Requisição de consulta"""
    query: str = Field(..., description="Consulta")
    context_size: int = Field(default=5, description="Número de memórias de contexto")
    
    class Config:
        json_schema_extra = {
            "example": {
                "query": "Como funciona o sistema de memória?",
                "context_size": 5
            }
        }


# Endpoints da API

@app.on_event("startup")
async def startup_event():
    """Inicializar sistema na startup"""
    global orchestrator
    logger.info("🚀 Iniciando DigiMundo API Server...")
    
    try:
        orchestrator = Orchestrator()
        # Iniciar orchestrator em background
        asyncio.create_task(orchestrator.run())
        logger.info("✅ Orchestrator iniciado com sucesso")
    except Exception as e:
        logger.error(f"❌ Erro ao iniciar orchestrator: {e}")
        raise


@app.get("/")
async def root():
    """Endpoint raiz"""
    return {
        "name": "DigiMundo Swarm API",
        "version": "1.0.0",
        "status": "online",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health")
async def health_check():
    """Verificar saúde do sistema"""
    if not orchestrator:
        raise HTTPException(status_code=503, detail="Sistema não inicializado")
    
    metrics = orchestrator.get_metrics()
    
    # Verificar saúde dos agentes
    agents_healthy = all(
        status != "error" 
        for status in metrics['agent_status'].values()
    )
    
    health_status = {
        "status": "healthy" if agents_healthy else "degraded",
        "timestamp": datetime.now().isoformat(),
        "uptime_seconds": metrics['uptime_seconds'],
        "agents": metrics['agent_status'],
        "system": metrics['system_metrics']
    }
    
    return health_status


@app.get("/metrics")
async def get_metrics():
    """Obter métricas do sistema"""
    if not orchestrator:
        raise HTTPException(status_code=503, detail="Sistema não inicializado")
    
    return orchestrator.get_metrics()


@app.get("/agents")
async def list_agents():
    """Listar status dos agentes"""
    if not orchestrator:
        raise HTTPException(status_code=503, detail="Sistema não inicializado")
    
    return {
        "agents": orchestrator.agent_status,
        "count": len(orchestrator.agents)
    }


@app.post("/tasks")
async def create_task(task: TaskRequest):
    """Criar nova tarefa"""
    if not orchestrator:
        raise HTTPException(status_code=503, detail="Sistema não inicializado")
    
    # Mapear prioridade
    priority_map = {
        "critical": TaskPriority.CRITICAL,
        "high": TaskPriority.HIGH,
        "normal": TaskPriority.NORMAL,
        "low": TaskPriority.LOW
    }
    
    priority = priority_map.get(task.priority.lower(), TaskPriority.NORMAL)
    
    # Adicionar tarefa
    task_id = orchestrator.add_task(
        task_type=task.type,
        data=task.data,
        priority=priority
    )
    
    return {
        "task_id": task_id,
        "status": "queued",
        "queue_size": orchestrator.task_queue.qsize()
    }


@app.get("/tasks/{task_id}")
async def get_task_status(task_id: str):
    """Obter status de uma tarefa"""
    # Por enquanto, retornar placeholder
    # Em produção, implementar tracking de tarefas
    return {
        "task_id": task_id,
        "status": "processing",
        "message": "Tracking de tarefas será implementado"
    }


@app.post("/query")
async def query(request: QueryRequest):
    """Fazer consulta ao sistema"""
    if not orchestrator:
        raise HTTPException(status_code=503, detail="Sistema não inicializado")
    
    # Criar tarefa de query
    task_id = orchestrator.add_task(
        task_type="query",
        data={
            "query": request.query,
            "context_size": request.context_size
        },
        priority=TaskPriority.HIGH
    )
    
    # Aguardar resultado (com timeout)
    timeout = 30  # segundos
    start_time = asyncio.get_event_loop().time()
    
    while True:
        if asyncio.get_event_loop().time() - start_time > timeout:
            raise HTTPException(status_code=408, detail="Timeout na consulta")
        
        # Verificar se tem resultado
        if not orchestrator.results_queue.empty():
            result = await orchestrator.results_queue.get()
            if result.id == task_id:
                if result.status == "completed":
                    return {
                        "query": request.query,
                        "response": result.result,
                        "task_id": task_id
                    }
                else:
                    raise HTTPException(
                        status_code=500, 
                        detail=f"Erro na consulta: {result.error}"
                    )
        
        await asyncio.sleep(0.1)


@app.post("/execute")
async def execute_command(request: CommandRequest):
    """Executar comando"""
    if not orchestrator:
        raise HTTPException(status_code=503, detail="Sistema não inicializado")
    
    # Criar tarefa de execução
    task_id = orchestrator.add_task(
        task_type="execute",
        data={
            "command": request.command,
            "timeout": request.timeout
        },
        priority=TaskPriority.NORMAL
    )
    
    return {
        "task_id": task_id,
        "status": "queued",
        "command": request.command
    }


@app.post("/learn")
async def learn(request: LearnRequest, background_tasks: BackgroundTasks):
    """Aprender de arquivo ou fazer scan completo"""
    if not orchestrator:
        raise HTTPException(status_code=503, detail="Sistema não inicializado")
    
    # Criar tarefa de aprendizado
    task_id = orchestrator.add_task(
        task_type="learn",
        data={"file_path": request.file_path},
        priority=TaskPriority.LOW
    )
    
    return {
        "task_id": task_id,
        "status": "queued",
        "type": "file" if request.file_path else "full_scan"
    }


@app.post("/memory")
async def store_memory(request: MemoryRequest):
    """Armazenar informação na memória"""
    if not orchestrator:
        raise HTTPException(status_code=503, detail="Sistema não inicializado")
    
    # Criar tarefa de memória
    task_id = orchestrator.add_task(
        task_type="remember",
        data={
            "content": request.content,
            "metadata": request.metadata
        },
        priority=TaskPriority.NORMAL
    )
    
    return {
        "task_id": task_id,
        "status": "queued"
    }


@app.get("/memory/search")
async def search_memory(query: str, limit: int = 5):
    """Buscar na memória"""
    if not orchestrator:
        raise HTTPException(status_code=503, detail="Sistema não inicializado")
    
    # Buscar diretamente (síncrono para queries rápidas)
    memories = await orchestrator.agents['memory'].search(query, n_results=limit)
    
    return {
        "query": query,
        "results": memories,
        "count": len(memories)
    }


@app.get("/memory/stats")
async def memory_stats():
    """Estatísticas da memória"""
    if not orchestrator:
        raise HTTPException(status_code=503, detail="Sistema não inicializado")
    
    return orchestrator.agents['memory'].get_stats()


@app.get("/model/info")
async def model_info():
    """Informações do modelo atual"""
    if not orchestrator:
        raise HTTPException(status_code=503, detail="Sistema não inicializado")
    
    return orchestrator.model_switcher.get_model_info()


@app.post("/model/switch")
async def switch_model(model_name: Optional[str] = None):
    """Trocar modelo"""
    if not orchestrator:
        raise HTTPException(status_code=503, detail="Sistema não inicializado")
    
    success = await orchestrator.model_switcher.switch_model(model_name)
    
    if success:
        return {
            "status": "success",
            "current_model": orchestrator.model_switcher.get_model_info()
        }
    else:
        raise HTTPException(status_code=400, detail="Falha ao trocar modelo")


@app.get("/files/learned")
async def list_learned_files():
    """Listar arquivos aprendidos"""
    if not orchestrator:
        raise HTTPException(status_code=503, detail="Sistema não inicializado")
    
    stats = orchestrator.agents['learning'].get_stats()
    
    return {
        "learned_files": stats['learned_files'],
        "total_size_mb": stats['total_size_mb'],
        "chunks_created": stats['chunks_created']
    }


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket para atualizações em tempo real"""
    await websocket.accept()
    
    try:
        while True:
            # Enviar métricas a cada 5 segundos
            if orchestrator:
                metrics = orchestrator.get_metrics()
                await websocket.send_json({
                    "type": "metrics",
                    "data": metrics,
                    "timestamp": datetime.now().isoformat()
                })
            
            await asyncio.sleep(5)
            
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
    finally:
        await websocket.close()


@app.get("/logs/stream")
async def stream_logs():
    """Stream de logs em tempo real"""
    async def generate():
        # Simulação - em produção, conectar ao sistema de logs real
        while True:
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "level": "INFO",
                "message": "Sistema operacional",
                "agent": "orchestrator"
            }
            yield f"data: {json.dumps(log_entry)}\n\n"
            await asyncio.sleep(1)
    
    return StreamingResponse(generate(), media_type="text/event-stream")


@app.post("/shutdown")
async def shutdown_system():
    """Desligar sistema (requer autenticação em produção)"""
    if not orchestrator:
        raise HTTPException(status_code=503, detail="Sistema não inicializado")
    
    # TODO: Adicionar autenticação
    logger.warning("⚠️ Shutdown requisitado via API")
    
    return {
        "status": "shutdown_initiated",
        "message": "Sistema será desligado em 5 segundos"
    }


# Função principal para rodar o servidor
def run_api_server(host: str = "0.0.0.0", port: int = 8000):
    """Executar servidor API"""
    logger.info(f"🌐 Iniciando API Server em {host}:{port}")
    logger.info(f"📚 Documentação disponível em http://{host}:{port}/docs")
    
    uvicorn.run(
        app,
        host=host,
        port=port,
        log_level="info",
        access_log=True
    )


if __name__ == "__main__":
    run_api_server()
