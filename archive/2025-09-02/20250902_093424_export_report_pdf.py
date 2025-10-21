#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Exporta reports/index.html para PDF em reports/report.pdf.
Motores (em ordem): WeasyPrint -> Playwright (Chromium) -> wkhtmltopdf -> Chrome/Chromium headless.
Uso:
  python scripts/export_report_pdf.py --html reports/index.html --out reports/report.pdf --engine auto
"""
from __future__ import annotations
import argparse, shutil, subprocess, sys
from pathlib import Path

def try_weasyprint(html: Path, out: Path) -> bool:
    try:
        from weasyprint import HTML
        HTML(filename=str(html)).write_pdf(str(out))
        print("[OK] PDF via WeasyPrint")
        return True
    except Exception as e:
        print("[SKIP] weasyprint:", str(e)[:120])
        return False

def try_playwright(html: Path, out: Path) -> bool:
    try:
        from playwright.sync_api import sync_playwright
    except Exception as e:
        print("[SKIP] playwright import:", str(e)[:120]); return False
    try:
        with sync_playwright() as p:
            try:
                browser = p.chromium.launch(headless=True)
            except Exception:
                # tenta instalar chromium
                try:
                    subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"],
                                   check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    browser = p.chromium.launch(headless=True)
                except Exception as e2:
                    print("[SKIP] playwright launch:", str(e2)[:120]); return False
            page = browser.new_page()
            page.goto(html.resolve().as_uri(), wait_until="load")
            page.pdf(path=str(out), format="A4", print_background=True)
            browser.close()
        print("[OK] PDF via Playwright/Chromium")
        return True
    except Exception as e:
        print("[SKIP] playwright:", str(e)[:120]); return False

def try_wkhtmltopdf(html: Path, out: Path) -> bool:
    exe = shutil.which("wkhtmltopdf")
    if not exe:
        print("[SKIP] wkhtmltopdf not found")
        return False
    try:
        subprocess.run([exe, str(html), str(out)], check=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("[OK] PDF via wkhtmltopdf")
        return True
    except Exception as e:
        print("[SKIP] wkhtmltopdf:", str(e)[:120]); return False

def try_chrome_headless(html: Path, out: Path) -> bool:
    candidates = [
        "google-chrome", "chromium", "chromium-browser",
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    ]
    for bin_ in candidates:
        if shutil.which(bin_) or Path(bin_).exists():
            cmd = [bin_, "--headless", "--disable-gpu", f"--print-to-pdf={out}", html.resolve().as_uri()]
            try:
                subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                if out.exists():
                    print(f"[OK] PDF via {bin_} --headless")
                    return True
            except Exception as e:
                print(f"[SKIP] {bin_}:", str(e)[:120])
    return False

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--html", default="reports/index.html")
    ap.add_argument("--out", default="reports/report.pdf")
    ap.add_argument("--engine", default="auto", choices=["auto","weasyprint","playwright","wkhtmltopdf","chrome"])
    args = ap.parse_args()

    html = Path(args.html); out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    if not html.exists():
        print("[ERR] HTML não encontrado:", html); sys.exit(1)

    ok = False
    order = {
        "auto": ["weasyprint","playwright","wkhtmltopdf","chrome"],
        "weasyprint": ["weasyprint"],
        "playwright": ["playwright"],
        "wkhtmltopdf": ["wkhtmltopdf"],
        "chrome": ["chrome"]
    }[args.engine]

    for eng in order:
        if eng == "weasyprint": ok = try_weasyprint(html, out)
        elif eng == "playwright": ok = try_playwright(html, out)
        elif eng == "wkhtmltopdf": ok = try_wkhtmltopdf(html, out)
        elif eng == "chrome": ok = try_chrome_headless(html, out)
        if ok: break

    if not ok:
        print("[FAIL] Nenhum motor disponível. Sugestões:")
        print(" - pip install weasyprint   # requer libs do sistema (cairo/pango)")
        print(" - pip install playwright && python -m playwright install chromium")
        print(" - brew install wkhtmltopdf  # macOS")
        print(" - usar Google Chrome headless com --print-to-pdf")
        sys.exit(2)
    else:
        print(f"[DONE] PDF -> {out}")

if __name__ == "__main__":
    main()