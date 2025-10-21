import requests
print("Testando API Ollama...")
r = requests.post("http://127.0.0.1:11434/api/generate",
                  json={"model":"mixtral-cpu-force:latest","prompt":"Responda apenas: OK","stream":False},
                  timeout=30)
print(f"Status: {r.status_code}")
print(f"Resposta: {r.json()['response'][:100]}")
print("✅ FUNCIONA!")
