from fastapi import FastAPI, WebSocket
import asyncio, os, json, structlog
from pathlib import Path
from .agent import DigimonAgent

log = structlog.get_logger()
app = FastAPI()
soul_path = Path(os.getenv('SOUL_PATH', '/data/digimon_soul'))
agent = DigimonAgent(soul_path)

@app.on_event('startup')
async def start_agent():
    loop = asyncio.get_event_loop()
    loop.create_task(agent.run_forever())

@app.post('/skill/echo')
async def echo_skill(payload: dict):
    text = payload.get('texto', 'ping')
    return {'resposta': f'Espelho cognitivo: {text}'}

@app.websocket('/stream')
async def stream(ws: WebSocket):
    await ws.accept()
    path = soul_path/'ciclos'/'respiracao.jsonl'
    async def tail():
        with open(path, 'r') as f:
            f.seek(0,2)
            while True:
                line = f.readline()
                if line:
                    yield line
                else:
                    await asyncio.sleep(1)
    async for line in tail():
        await ws.send_text(line)

if __name__ == '__main__':
    import uvicorn, sys
    port = int(os.getenv('PORT', '9001'))
    uvicorn.run('digimon_core.main:app', host='0.0.0.0', port=port, reload=False)