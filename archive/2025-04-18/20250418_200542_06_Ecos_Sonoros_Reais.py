# Simulação de som externo com pulso físico (exemplo para sox)

import os
os.system("play -nq -t alsa synth 0.5 sine 440")