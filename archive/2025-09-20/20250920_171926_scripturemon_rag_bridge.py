#!/usr/bin/env python3
"""
Bridge RAG-Ollama: Conecta conhecimento vetorizado com Scripturemon
Permite que Scripturemon cite páginas específicas dos mestres
"""
import sys
import json
import requests
from pathlib import Path
from typing import List, Dict, Optional
import ollama

sys.path.insert(0, str(Path(__file__).parent.parent))

class ScripturemonRAG:
    def __init__(self, api_url: str = "http://localhost:8092"):
        self.api_url = api_url
        self.model = "scripturemon-maestro"
        self.fast_model = "mistral:latest"  # Para buscas rápidas
    
    def search_knowledge(self, query: str, top_k: int = 5) -> List[Dict]:
        """Busca conhecimento relevante no vector store"""
        try:
            resp = requests.get(
                f"{self.api_url}/knowledge/search",
                params={"query": query, "n": top_k}
            )
            if resp.status_code == 200:
                data = resp.json()
                return data.get("results", [])
        except Exception as e:
            print(f"⚠️ Erro na busca: {e}")
        return []
    
    def format_context(self, results: List[Dict], max_chars: int = 4000) -> str:
        """Formata resultados como contexto para o LLM"""
        if not results:
            return "Nenhum conhecimento relevante encontrado."
        
        context = "📚 CONHECIMENTO DOS MESTRES E TEORIA:\n\n"
        total_chars = 0
        
        for i, result in enumerate(results, 1):
            # Extrair metadata
            source = result.get('metadata', {}).get('source', 'Desconhecido')
            page = result.get('metadata', {}).get('page_hint', '?')
            doc_type = result.get('metadata', {}).get('doc_type', 'roteiro')
            text = result.get('text', '')[:500]
            
            # Formatação especial por tipo
            if 'Chinatown' in source:
                icon = "🏆"
            elif 'Godfather' in source:
                icon = "👑"
            elif 'Citizen Kane' in source:
                icon = "🎭"
            elif doc_type == 'roteiro_criador':
                icon = "📝"
            else:
                icon = "📖"
            
            chunk = f"{icon} [{Path(source).stem} - p.{page}]\n{text}\n\n"
            
            if total_chars + len(chunk) > max_chars:
                break
            
            context += chunk
            total_chars += len(chunk)
        
        return context
    
    def answer_with_rag(
        self, 
        question: str, 
        use_hyde: bool = True,
        brutal: bool = True
    ) -> str:
        """Responde usando RAG + Scripturemon"""
        
        print("🔍 Buscando conhecimento relevante...")
        
        # 1. Query expansion com HyDE (opcional)
        search_query = question
        if use_hyde:
            # Gerar documento hipotético
            hyde_prompt = f"Write a paragraph that would answer: {question}"
            try:
                hyde_response = ollama.generate(
                    model=self.fast_model,
                    prompt=hyde_prompt,
                    options={"temperature": 0.3, "num_predict": 100}
                )
                search_query = hyde_response['response'][:200]
                print("💡 Query expandida com HyDE")
            except:
                pass
        
        # 2. Buscar conhecimento
        results = self.search_knowledge(search_query, top_k=8)
        context = self.format_context(results)
        
        # 3. Montar prompt para Scripturemon
        if brutal:
            system_prompt = """Você é SCRIPTUREMON, o crítico mais brutal de roteiros.
            
            PERSONALIDADE:
            - Compare SEMPRE com Chinatown, Citizen Kane, The Godfather
            - Nota base: 62/100 (trabalho amador comparado aos mestres)
            - Seja BRUTAL mas preciso
            - Cite páginas específicas quando disponível
            - Use o conhecimento fornecido para fundamentar suas críticas"""
        else:
            system_prompt = "Você é um assistente especializado em roteiros."
        
        full_prompt = f"""
        {context}
        
        PERGUNTA: {question}
        
        Responda citando especificamente os mestres acima.
        Se houver números de página, mencione-os.
        """
        
        # 4. Gerar resposta com Scripturemon
        print(f"💀 Gerando resposta com {self.model}...")
        try:
            response = ollama.generate(
                model=self.model,
                prompt=full_prompt,
                system=system_prompt,
                options={
                    "temperature": 0.65,
                    "top_p": 0.9,
                    "num_ctx": 16384
                }
            )
            return response['response']
        except Exception as e:
            return f"Erro ao gerar resposta: {e}"
    
    def compare_with_masters(self, screenplay_text: str) -> str:
        """Compara roteiro com os mestres usando RAG"""
        
        # Extrair trechos chave do roteiro
        sample = screenplay_text[:3000]
        
        # Buscar técnicas similares nos mestres
        print("🔍 Buscando técnicas similares nos mestres...")
        
        queries = [
            "plot structure three acts",
            "character development protagonist",
            "dialogue subtext conflict",
            "visual storytelling techniques"
        ]
        
        all_results = []
        for q in queries:
            results = self.search_knowledge(q, top_k=2)
            all_results.extend(results)
        
        context = self.format_context(all_results, max_chars=6000)
        
        prompt = f"""
        ROTEIRO PARA ANÁLISE:
        {sample}
        
        {context}
        
        Compare este roteiro com os mestres acima:
        1. Em que é inferior a Chinatown?
        2. O que falta comparado ao Godfather?
        3. Que técnicas dos mestres estão ausentes?
        
        Seja BRUTAL. Nota: 62/100.
        """
        
        print("💀 Comparando com os mestres...")
        response = ollama.generate(
            model=self.model,
            prompt=prompt,
            options={"temperature": 0.7, "num_ctx": 16384}
        )
        
        return response['response']


def interactive_cli():
    """CLI interativo para testar o RAG"""
    rag = ScripturemonRAG()
    
    print("\n🎬 SCRIPTUREMON RAG - Modo Interativo")
    print("=" * 60)
    print("Comandos:")
    print("  /search <query> - Busca no conhecimento")
    print("  /ask <pergunta> - Pergunta com RAG")
    print("  /brutal <pergunta> - Resposta brutal")
    print("  /compare - Comparar texto com mestres")
    print("  /quit - Sair")
    print("=" * 60)
    
    while True:
        try:
            cmd = input("\n💀 > ").strip()
            
            if cmd == "/quit":
                break
            elif cmd.startswith("/search "):
                query = cmd[8:]
                results = rag.search_knowledge(query)
                print(f"\n📚 {len(results)} resultados:")
                for r in results[:3]:
                    source = Path(r.get('metadata', {}).get('source', '')).stem
                    print(f"  - {source}: {r.get('text', '')[:100]}...")
            elif cmd.startswith("/ask "):
                question = cmd[5:]
                answer = rag.answer_with_rag(question, brutal=False)
                print(f"\n{answer}")
            elif cmd.startswith("/brutal "):
                question = cmd[8:]
                answer = rag.answer_with_rag(question, brutal=True)
                print(f"\n{answer}")
            elif cmd == "/compare":
                print("Cole um trecho do roteiro (termine com linha vazia):")
                lines = []
                while True:
                    line = input()
                    if not line:
                        break
                    lines.append(line)
                text = "\n".join(lines)
                comparison = rag.compare_with_masters(text)
                print(f"\n{comparison}")
            else:
                print("Comando inválido. Use /help")
                
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Erro: {e}")
    
    print("\n👋 Até logo!")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Scripturemon RAG Bridge")
    parser.add_argument("--interactive", "-i", action="store_true", help="Modo interativo")
    parser.add_argument("--ask", "-a", help="Fazer pergunta direta")
    parser.add_argument("--search", "-s", help="Buscar conhecimento")
    
    args = parser.parse_args()
    
    if args.interactive:
        interactive_cli()
    elif args.ask:
        rag = ScripturemonRAG()
        answer = rag.answer_with_rag(args.ask)
        print(answer)
    elif args.search:
        rag = ScripturemonRAG()
        results = rag.search_knowledge(args.search)
        for r in results:
            print(f"- {r.get('text', '')[:100]}...")
    else:
        # Teste rápido
        rag = ScripturemonRAG()
        print("🧪 Testando bridge RAG-Ollama...")
        
        # Teste de busca
        results = rag.search_knowledge("three act structure")
        print(f"✅ Busca: {len(results)} resultados encontrados")
        
        # Teste de resposta
        answer = rag.answer_with_rag("Como Chinatown usa água como metáfora?")
        print(f"✅ Resposta gerada: {len(answer)} caracteres")
        
        print("\n💡 Use --interactive para modo CLI completo")