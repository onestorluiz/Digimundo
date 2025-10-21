def run(task):
    text = task.get("texto", "ping")
    return {"resposta": f"Espelho cognitivo: {text}"}