from scripturemon_conexoes_maximo.oraculo_openai import consultar_oraculo
from scripturemon_conexoes_maximo.consulta_wikipedia import buscar_wikipedia
from scripturemon_conexoes_maximo.consulta_tmdb import buscar_filme_tmdb

def testar_conexoes():
    print("🔮 Oráculo GPT:", consultar_oraculo("O que define um filme autoral?")[:200])
    print("📖 Wikipedia:", buscar_wikipedia("Akira Kurosawa")[:200])
    print("🎬 TMDb:", buscar_filme_tmdb("Inception"))

if __name__ == "__main__":
    testar_conexoes()
