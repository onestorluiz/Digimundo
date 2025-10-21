#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Gera HTML formatado do tutorial (PDF opcional se tiver wkhtmltopdf)"""

import os
from pathlib import Path

def main():
    # Ler guia rápido
    guia = Path("GUIA_RAPIDO.md").read_text(encoding="utf-8")
    
    # Converter MD básico para HTML
    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Scripturemon - Guia Técnico</title>
    <style>
        body {{
            font-family: 'SF Mono', Monaco, 'Courier New', monospace;
            max-width: 900px;
            margin: 40px auto;
            padding: 20px;
            background: #1e1e1e;
            color: #d4d4d4;
        }}
        h1 {{ color: #4ec9b0; border-bottom: 2px solid #4ec9b0; padding-bottom: 10px; }}
        h2 {{ color: #569cd6; margin-top: 30px; }}
        h3 {{ color: #c586c0; }}
        pre {{
            background: #2d2d2d;
            border: 1px solid #3e3e3e;
            border-radius: 5px;
            padding: 15px;
            overflow-x: auto;
        }}
        code {{
            background: #2d2d2d;
            padding: 2px 5px;
            border-radius: 3px;
            color: #ce9178;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        th, td {{
            border: 1px solid #3e3e3e;
            padding: 10px;
            text-align: left;
        }}
        th {{
            background: #2d2d2d;
            color: #569cd6;
        }}
        a {{ color: #4ec9b0; }}
        hr {{ border: 1px solid #3e3e3e; }}
        .highlight {{ background: #364200; }}
        .success {{ color: #4ec9b0; }}
        .warning {{ color: #dcdcaa; }}
        .error {{ color: #f48771; }}
    </style>
</head>
<body>
    <div class="content">
        {guia.replace('```bash', '<pre><code class="bash">').replace('```', '</code></pre>')
             .replace('# 🚀', '<h1>🚀')
             .replace('## ', '<h2>')
             .replace('### ', '<h3>')
             .replace('---', '<hr>')
             .replace('✅', '<span class="success">✅</span>')
             .replace('⚡', '<span class="warning">⚡</span>')
             .replace('🔧', '🔧')
             .replace('|------|---------|', '</th></tr></thead><tbody>')
             .replace('| Erro | Solução |', '<table><thead><tr><th>Erro</th><th>Solução')
             .replace('| "', '<tr><td>"')
             .replace('" | `', '"</td><td><code>')
             .replace('` |', '</code></td></tr>')
             .replace('**', '<strong>').replace('**', '</strong>')
        }
    </div>
    
    <footer style="text-align: center; margin-top: 50px; color: #808080;">
        <p>Scripturemon Ultimate v2.0 - Sistema de IA para Roteiros</p>
        <p>Compressão 84.9% | Análise 4D | Memória L1-L4</p>
    </footer>
</body>
</html>"""
    
    # Salvar HTML
    output_html = Path("GUIA_SCRIPTUREMON.html")
    output_html.write_text(html_content, encoding="utf-8")
    print(f"[OK] HTML gerado: {output_html}")
    
    # Tentar gerar PDF se tiver ferramentas
    try:
        # Método 1: wkhtmltopdf
        if os.system("which wkhtmltopdf >/dev/null 2>&1") == 0:
            os.system(f"wkhtmltopdf {output_html} GUIA_SCRIPTUREMON.pdf 2>/dev/null")
            print("[OK] PDF gerado: GUIA_SCRIPTUREMON.pdf")
        # Método 2: weasyprint (se instalado)
        else:
            try:
                from weasyprint import HTML as WPHTML
                WPHTML(string=html_content).write_pdf("GUIA_SCRIPTUREMON.pdf")
                print("[OK] PDF gerado via weasyprint")
            except:
                print("[INFO] Para gerar PDF, instale: brew install wkhtmltopdf")
    except:
        print("[INFO] HTML pronto. PDF opcional (precisa wkhtmltopdf)")
    
    print(f"\n📖 Abra o arquivo: {output_html.absolute()}")

if __name__ == "__main__":
    main()