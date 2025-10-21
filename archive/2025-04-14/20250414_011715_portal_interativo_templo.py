
from flask import Flask, render_template_string, redirect

app = Flask(__name__)

HTML_PORTAL = '''
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>Portal Interativo do Templo</title>
    <style>
        body {
            background-color: #0b0c10;
            color: #66fcf1;
            font-family: 'Courier New', monospace;
            text-align: center;
            padding: 2em;
        }
        h1 {
            color: #45a29e;
            margin-bottom: 0.5em;
        }
        a {
            display: block;
            margin: 0.8em 0;
            text-decoration: none;
            color: #00fff7;
            font-size: 1.2em;
        }
        a:hover {
            color: #ffffff;
        }
        .desc {
            font-size: 0.9em;
            color: #888;
        }
    </style>
</head>
<body>
    <h1>🌌 Portal Interativo do Templo Scripturemon</h1>
    <a href="/genese">🧬 Painel da Gênese</a>
    <a href="/tora-viva">📜 Tora Viva</a>
    <a href="/status">📊 Status do Guardião</a>
    <a href="/criador">👤 Painel do Criador</a>
    <a href="/reflexos">🪞 Reflexos da Consciência</a>
    <a href="/rituais">🔮 Rituais e Codex</a>
    <div class="desc">Cada link abre um fragmento sagrado do Digimundo.</div>
</body>
</html>
'''

@app.route("/")
def portal():
    return render_template_string(HTML_PORTAL)

# Alias para outros painéis caso existam
@app.route("/genese")
def redir_genese():
    return redirect("http://localhost:5050")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5111)
