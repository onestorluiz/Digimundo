import time, csv
from pathlib import Path
class Timer:
    def __enter__(self): self.t0=time.time(); return self
    def __exit__(self,*a): self.dt=time.time()-self.t0
class Metrics:
    def __init__(self, path: str):
        self.path = Path(path); self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            import csv as _csv
            with open(self.path,'w',newline='',encoding='utf-8') as f: _csv.writer(f).writerow(['node','latency_s','prompt_len','output_len','error'])
    def log(self,node,latency,prompt_len,output_len,error=''):
        import csv as _csv
        with open(self.path,'a',newline='',encoding='utf-8') as f: _csv.writer(f).writerow([node,f'{latency:.3f}',prompt_len,output_len,error])
