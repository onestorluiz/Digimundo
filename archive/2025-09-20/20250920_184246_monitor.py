from fastapi import APIRouter
import psutil, time

router = APIRouter()

@router.get('/metrics')
def metrics():
    mem = psutil.virtual_memory()
    cpu = psutil.cpu_percent()
    ts = int(time.time())
    return f"digimon_memory_bytes {mem.used}\ndigimon_cpu_percent {cpu}\ndigimon_timestamp {ts}\n"