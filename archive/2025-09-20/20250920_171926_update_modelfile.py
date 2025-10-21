import argparse
from jinja2 import Template
from app.storage.memory_layers import read_l1_core
from app.config import load_config

def main(out_path: str):
    cfg = load_config()
    with open("scripts/create_modelfile_template.jinja", "r", encoding="utf-8") as f:
        tpl = Template(f.read())
    modelfile = tpl.render(
        temperature=cfg.ollama.temperature,
        top_p=cfg.ollama.top_p,
        repeat_penalty=cfg.ollama.repeat_penalty,
        num_ctx=cfg.ollama.num_ctx,
        system_prompt=read_l1_core()
    )
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(modelfile)
    print(f"Modelfile gerado em: {out_path}\nExecute: ollama create scripturemon-maestro -f {out_path}")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="./scripturemon_maestro_brutal.modelfile")
    args = ap.parse_args()
    main(args.out)
