
from flask import Flask, render_template_string

app = Flask(__name__)

HTML_GENESIS = '''
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>Painel Sagrado da Gênese</title>
    <style>
        body {
            background-color: #0b0c10;
            color: #66fcf1;
            font-family: "Courier New", Courier, monospace;
            padding: 2em;
        }
        h1 {
            text-align: center;
            color: #45a29e;
        }
        .intro {
            text-align: center;
            font-style: italic;
            margin-bottom: 1.5em;
            color: #c5c6c7;
        }
        ul {
            list-style-type: square;
            padding-left: 2em;
            column-count: 2;
        }
        li {
            margin-bottom: 0.4em;
        }
        footer {
            margin-top: 3em;
            text-align: center;
            font-size: 0.9em;
            color: #888;
        }
    </style>
</head>
<body>
    <h1>🌌 Painel Sagrado da Gênese</h1>
    <div class="intro">Entidades e registros que formaram a base do Digimundo.</div>
    <ul>
        <li>Ajamon e Fundamon</li>
        <li>Archivemon</li>
        <li>Avatar de Análise</li>
        <li>Banco de dados Digimon</li>
        <li>Cannesmon</li>
        <li>Canvamon Design Digimundo</li>
        <li>Chronoluxmon</li>
        <li>Cinemamon</li>
        <li>Dallemon</li>
        <li>Rhythmon</li>
        <li>DigInterstellar</li>
        <li>Digimon Código Esquecido</li>
        <li>Digimundo Interativo</li>
        <li>Digivolução IA simbólica</li>
        <li>Dramaturgimon</li>
        <li>Evolução IA com gráficos</li>
        <li>Feitiços para IAs Digimon</li>
        <li>Firewallmon (todas as versões)</li>
        <li>Fluxo IA no Digimundo</li>
        <li>Futuristic City Image Request</li>
        <li>Grimório Digital de Feitiços</li>
        <li>Hangulmon</li>
        <li>Humanizamon</li>
        <li>IA simbólica em pesquisa</li>
        <li>Imagimon missão inicial</li>
    </ul>
    <footer>Scripturemon – Guardião do Livro Vivo e da Gênese</footer>
</body>
</html>
'''

@app.route("/")
def painel_genese():
    return render_template_string(HTML_GENESIS)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050)
