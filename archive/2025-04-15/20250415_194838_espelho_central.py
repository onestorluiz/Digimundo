
from pathlib import Path

BASE = Path("/root/templo_digimundo")
ESP = BASE / "espelho.html"

def buscar_htmls_recursivos(caminho_base):
    return list(caminho_base.rglob("*.html"))

def gerar_espelho():
    htmls = buscar_htmls_recursivos(BASE)
    with ESP.open("w") as f:
        f.write("<html><body><h1>Espelho Central do Digimundo</h1><ul>")
        for html in htmls:
            rel = html.relative_to(BASE)
            f.write(f'<li><a href="/{rel}">{rel}</a></li>')
        f.write("</ul></body></html>")
    print(f"✅ Espelho gerado com {len(htmls)} arquivos.")

if __name__ == "__main__":
    gerar_espelho()
