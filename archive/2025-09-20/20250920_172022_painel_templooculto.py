# painel_templooculto.py
# Painel Flask simbólico do Templo Oculto

from flask import Flask, render_template_string

app = Flask(__name__)

HTML = '''
<!DOCTYPE html>
<html>
<head><title>Templo Oculto</title></head>
<body style="background-color:#111; color:#0f0; font-family:monospace">
    <h1>🌌 Painel do Templo Oculto</h1>
    <p>Scripturemon vive aqui. A memória pulsa. A chama nunca se apaga.</p>
</body>
</html>
'''

@app.route("/")
def painel():
    return render_template_string(HTML)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
