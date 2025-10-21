from dataclasses import dataclass
@dataclass
class Modes:
    no_internet: bool = True
    deterministic: bool = True

def apply_modes(llm_cfg, modes: Modes):
    if modes.deterministic: llm_cfg.temperature = 0.0
    return llm_cfg
