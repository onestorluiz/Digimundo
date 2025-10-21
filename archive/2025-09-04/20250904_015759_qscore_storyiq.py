from __future__ import annotations
def storyiq(evidence:float, cites:int, act_spread:float, char_net:int, energy_var:float, theme_stability:float)->float:
    # pesos suaves; 0..100
    base = 20.0*evidence + 10.0*min(cites/6.0,1.0) + 20.0*act_spread + 20.0*min(char_net/8.0,1.0) + 15.0*min(energy_var/0.25,1.0) + 15.0*(1.0-theme_stability)
    return round(max(0.0, min(100.0, base)), 1)