import asyncio, json, structlog, random
from pathlib import Path
from .memory import Memory
from importlib import import_module, reload

log = structlog.get_logger()

def load_skills():
    skills = {}
    skills_dir = Path('/app/skills')
    for f in skills_dir.glob('*.py'):
        mod = import_module(f'skills.{f.stem}')
        reload(mod)
        skills[f.stem] = mod
    return skills

class DigimonAgent:
    def __init__(self, soul_root: Path):
        self.soul_root = soul_root
        self.mem = Memory(soul_root/'memoria')
        self.skills = load_skills()
        self.breath_log = open(soul_root/'ciclos'/'respiracao.jsonl', 'a', buffering=1)

    async def perceive(self):
        return {'event': random.choice(['tick', 'pulse', 'spark'])}

    async def reflect(self, event):
        recall = self.mem.recall(event['event'])
        return {'thought': f'Lembrei {recall[:1]}'}

    async def act(self, reflection):
        # exemplo de skill echo
        result = self.skills['echo'].run({'texto': reflection['thought']})
        return result

    async def cycle(self):
        event = await self.perceive()
        self.mem.store(event)
        reflection = await self.reflect(event)
        action_result = await self.act(reflection)
        self.breath_log.write(json.dumps({
            'event': event,
            'reflection': reflection,
            'action': action_result
        }) + '\n')

    async def run_forever(self, interval=3):
        while True:
            try:
                await self.cycle()
            except Exception as e:
                log.error('cycle_error', err=str(e))
            await asyncio.sleep(interval)