from __future__ import annotations
def qscore(evi:float, mem:float, coh:float, cites_count:int, len_out:int, act_spread:float|None=None)->float:
    base = 40.0*evi + 25.0*mem + 25.0*coh + 10.0*min(cites_count/4.0, 1.0)
    if act_spread is not None:
        base += 5.0*max(0.0, min(1.0, act_spread))  # diversidade por ato (0..1)
    adj = -5.0 if len_out < 300 else (0.0 if len_out < 1600 else -3.0)
    s = max(0.0, min(100.0, base + adj))
    return round(s, 1)