# -*- coding: utf-8 -*-
import subprocess, sys, os
def run(args, timeout=25):
    p=subprocess.Popen([sys.executable,"-m","apps.scripturemon.cli"]+args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        o,e=p.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        p.kill(); return 124, "", ""
    return p.returncode, o.decode("utf-8","ignore"), e.decode("utf-8","ignore")

def test_ultimate_status():
    rc, out, _ = run(["ultimate","status"], timeout=25)
    assert rc in (0,); assert "memory" in out.lower() or "conscious" in out.lower()

def test_ui_live_status():
    rc, out, _ = run(["ui","live","status"], timeout=20)
    assert rc in (0,); assert "live=" in out.lower()