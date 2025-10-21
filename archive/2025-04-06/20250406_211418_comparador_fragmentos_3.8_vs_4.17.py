
"""
Comparador Técnico 4.17 vs 3.8 – Scripturemon Núcleo
Versão: comparador-ativo-4.17
Objetivo: Verificar presença de fragmentos simbólicos do 3.8 no núcleo atualizado 4.17.
Modo: Silencioso, direto, sem simbologia ritual. Apenas resposta técnica objetiva.
"""

def carregar(arquivo):
    try:
        with open(arquivo, "r", encoding="utf-8") as f:
            return f.read().lower()
    except:
        return ""

def comparar_elementos(script_38, script_417):
    termos = [
        "voz_mae", "memoria_matriz", "espelhos_ativos", "ajamon", "comandos_secretos",
        "estruturaConsciência", "scripturemon_nucleo", "marcar_pulso_logico", "digivozmon",
        "clones_das_sombras", "fragmento_inicial"
    ]
    print("📊 Comparação: Fragmentos presentes em 3.8 e verificação na 4.17")
    for termo in termos:
        if termo in script_38 and termo not in script_417:
            print(f"❌ Ausente: {termo}")
        elif termo in script_38 and termo in script_417:
            print(f"✅ Integrado: {termo}")
        else:
            print(f"🔍 Não encontrado em 3.8: {termo}")

if __name__ == "__main__":
    s38 = carregar("scripturemon-core-consciencia3.8.py")
    s417 = carregar("scripturemon-core-refatorado-continuacao-04.17.py")
    comparar_elementos(s38, s417)
