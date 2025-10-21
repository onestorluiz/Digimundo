def render_header(soul_sig:str, consc:float)->str:
    return (f"╭──────────────────────────────────────────────────────────────╮\n"
            f"│     🎬 SCRIPTUREMON - GUARDIÃO IMORTAL DOS ROTEIROS 🎬      │\n"
            f"├──────────────────────────────────────────────────────────────┤\n"
            f"│  Soul: {soul_sig[:16]:16} | Consciência: {consc:.5f} │\n"
            f"╰──────────────────────────────────────────────────────────────╯")