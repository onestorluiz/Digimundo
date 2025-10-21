from __future__ import annotations
import os, time, shutil, subprocess, atexit
from pathlib import Path

ROOT = Path(os.environ.get("SCRIPTUREMON_HOME", Path(__file__).resolve().parents[2]))
RUNTIME = ROOT / "runtime"
RUNTIME.mkdir(parents=True, exist_ok=True)
TMPDIR = RUNTIME / "tmp"
TMPDIR.mkdir(parents=True, exist_ok=True)

CONF = TMPDIR / "redis.conf"
PID  = TMPDIR / "redis.pid"
LOG  = TMPDIR / "redis.log"

_SERVER_PATHS = [
    shutil.which("redis-server"),
    "/opt/homebrew/bin/redis-server",
    "/opt/homebrew/opt/redis/bin/redis-server",
    "/usr/local/bin/redis-server",
    "/usr/local/opt/redis/bin/redis-server",
]
_CLI_PATHS = [
    shutil.which("redis-cli"),
    "/opt/homebrew/bin/redis-cli",
    "/opt/homebrew/opt/redis/bin/redis-cli",
    "/usr/local/bin/redis-cli",
    "/usr/local/opt/redis/bin/redis-cli",
]

_started_here = False

def _which_any(cands): 
    for p in cands:
        if p and Path(p).exists():
            return p
    return None

def _write_conf(port:int=6379):
    CONF.write_text(f"""
bind 127.0.0.1
port {port}
daemonize yes
pidfile {PID}
logfile {LOG}
dir {TMPDIR}
save ""
appendonly no
""", encoding="utf-8")

def ensure_redis(port:int=6379, wait_s:float=2.0)->bool:
    """
    Garante que há um redis acessível em 127.0.0.1:port.
    Se não tiver, tenta iniciar efêmero. Se não conseguir, retorna False.
    """
    global _started_here
    try:
        import redis
        r = redis.Redis(host="127.0.0.1", port=port, socket_connect_timeout=0.2)
        r.ping()
        return True
    except Exception:
        pass

    srv = _which_any(_SERVER_PATHS)
    if not srv:
        return False

    # start ephemeral
    try:
        _write_conf(port=port)
        subprocess.run([srv, str(CONF)], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        # esperar ficar pronto
        t0 = time.time()
        while time.time() - t0 < wait_s:
            try:
                import redis
                r = redis.Redis(host="127.0.0.1", port=port, socket_connect_timeout=0.2)
                r.ping()
                _started_here = True
                break
            except Exception:
                time.sleep(0.1)
        # test final
        import redis
        redis.Redis(host="127.0.0.1", port=port, socket_connect_timeout=0.2).ping()
        return True
    except Exception:
        return False

def shutdown_if_started():
    global _started_here
    if not _started_here:
        return
    cli = _which_any(_CLI_PATHS)
    if cli:
        try:
            subprocess.run([cli, "-p", "6379", "shutdown"], timeout=1, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception:
            pass
    else:
        try:
            import redis
            r = redis.Redis(host="127.0.0.1", port=6379, socket_connect_timeout=0.2)
            r.shutdown()
        except Exception:
            pass
    _started_here = False

atexit.register(shutdown_if_started)