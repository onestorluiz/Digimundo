
import threading
from queue import Queue, Empty
class RateLimiter:
    def __init__(self, tps: float):
        self.tps=tps; self.last=0.0; self.lock=threading.Lock()
    def acquire(self):
        with self.lock:
            import time as _t
            now=_t.time()
            wait=max(0, (1.0/self.tps)-(now-self.last))
            if wait>0: _t.sleep(wait)
            self.last=_t.time()
def run_parallel(tasks: list[callable], max_workers=4, limiter: RateLimiter|None=None):
    q=Queue(); [q.put(t) for t in tasks]; results=[]; lock=threading.Lock()
    def worker():
        while True:
            try: t=q.get_nowait()
            except Empty: break
            if limiter: limiter.acquire()
            res=t()
            with lock: results.append(res)
            q.task_done()
    th=[threading.Thread(target=worker) for _ in range(max_workers)]
    [x.start() for x in th]; [x.join() for x in th]
    return results
