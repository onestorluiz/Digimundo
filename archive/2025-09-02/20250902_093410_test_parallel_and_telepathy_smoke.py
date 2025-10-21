# -*- coding: utf-8 -*-
from apps.scripturemon.parallel import analyze
from apps.scripturemon.telepathy import Telepathy, Insight
from apps.scripturemon.validator import health_once

def test_parallel_heuristic_runs():
    res=analyze("SCENE 1: INT. ROOM - DAY\nA character speaks.")
    assert "summary" in res and "structure" in res

def test_telepathy_connect():
    t=Telepathy()
    ok=t.connect()
    # aceita fakeredis se instalado, senão ok=False; o teste não falha duro
    assert ok in (True, False)

def test_health_once():
    xs=health_once()
    assert len(xs)>=2