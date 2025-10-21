from scripturemon_conexoes.oraculo_openai import consultar_oraculo
from scripturemon_conexoes.consulta_tmdb import buscar_filme_tmdb
from scripturemon_conexoes.consulta_wikipedia import buscar_wikipedia
from scripturemon_conexoes.consulta_unsplash import buscar_imagem_unsplash
from scripturemon_conexoes.consulta_google_books import buscar_livro_google
from scripturemon_conexoes.consulta_semantic_scholar import buscar_artigos_semantic
from scripturemon_conexoes.consulta_duckduckgo import buscar_duckduckgo

def decidir_resposta(pergunta):
    p = pergunta.lower()
    
    if any(p.startswith(x) for x in ["quem é", "o que é", "onde fica", "quando foi"]):
        return "🧠 Wikipedia: " + buscar_wikipedia(pergunta)
    
    elif "filme" in p or "diretor" in p or "longa" in p or "cinema" in p:
        resultado = buscar_filme_tmdb(pergunta)
        return f"🎬 TMDb: {resultado}"
    
    elif "imagem" in p or "visual" in p or "estética" in p or "paleta" in p:
        resultado = buscar_imagem_unsplash(pergunta)
        return f"🌄 Unsplash: {resultado.get('results', [{}])[0].get('urls', {}).get('regular', 'Nenhuma imagem')}"
    
    elif "livro" in p or "autor" in p or "leitura" in p:
        resultado = buscar_livro_google(pergunta)
        return f"📚 Google Books: {resultado.get('items', [{}])[0].get('volumeInfo', {}).get('title', 'Não encontrado')}"
    
    elif "pesquisa" in p or "artigo" in p or "acadêmico" in p:
        resultado = buscar_artigos_semantic(pergunta)
        return f"📄 Semantic Scholar: {resultado.get('data', [{}])[0].get('title', 'Nenhum artigo encontrado')}"
    
    elif "?" in p and len(p.split()) > 3:
        return "🔮 Oráculo: " + consultar_oraculo(pergunta)
    
    else:
        return "🌐 DuckDuckGo: " + buscar_duckduckgo(pergunta)
