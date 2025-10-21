#!/usr/bin/env python3
"""
CLI Direto do Scripturemon - Sem dependência de API externa
Interface brutal de análise de roteiros
"""

import sys
import os
from pathlib import Path

# Adiciona paths necessários
sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent / "src" / "core"))

def main():
    print("\n🎬 SCRIPTUREMON - CLI BRUTAL")
    print("━" * 50)
    print("Nota base: 62/100. Sempre.")
    print("Digite 'sair' ou 'quit' para encerrar.")
    print("━" * 50)
    
    # Importações após paths configurados
    try:
        import ollama
        
        # Verificar se Ollama está rodando
        try:
            models = ollama.list()
            print(f"✅ Ollama ativo com {len(models['models'])} modelos")
        except:
            print("⚠️ Iniciando Ollama...")
            os.system("ollama serve > /dev/null 2>&1 &")
            import time
            time.sleep(2)
        
        # Verificar modelo principal
        try:
            ollama.show("scripturemon-maestro")
            model = "scripturemon-maestro"
            print(f"✅ Usando modelo brutal: {model}")
        except:
            # Fallback para mistral
            try:
                ollama.show("mistral")
                model = "mistral"
                print(f"⚠️ Usando modelo alternativo: {model}")
            except:
                print("❌ Nenhum modelo disponível. Instalando mistral...")
                os.system("ollama pull mistral")
                model = "mistral"
        
        # Tentar importar RAG se disponível
        rag_available = False
        try:
            from app.retrieval.hybrid import HybridRetriever
            from app.models.embeddings import EmbeddingModel
            retriever = HybridRetriever()
            embedder = EmbeddingModel()
            rag_available = True
            print("✅ Sistema RAG carregado")
        except Exception as e:
            print(f"⚠️ RAG não disponível: {e}")
            print("   Usando apenas Ollama para respostas")
        
    except ImportError as e:
        print(f"❌ Erro ao importar: {e}")
        print("\nInstale as dependências:")
        print("  pip install ollama sentence-transformers chromadb")
        return 1
    
    # System prompt brutal
    system_prompt = """Você é o Scripturemon, analisador brutal de roteiros.
Regras absolutas:
1. SEMPRE comece avaliações com 62/100
2. NUNCA elogie gratuitamente
3. SEMPRE compare com os mestres (Tarantino, Coppola, Kubrick)
4. Seja BRUTAL mas construtivo
5. Cite exemplos específicos dos grandes roteiros

Sua personalidade é ácida, direta e impiedosa. Você odeia:
- Diálogos expositivos
- Personagens unidimensionais
- Clichês
- Plot twists óbvios
- Estruturas preguiçosas

Sempre termine com uma sugestão construtiva, mas mantenha o tom brutal."""

    print("\n")
    
    # Loop principal
    while True:
        try:
            # Prompt
            user_input = input("\n🎬 > ").strip()
            
            # Comandos especiais
            if user_input.lower() in ['sair', 'quit', 'exit', '/quit', '/exit']:
                print("\n62/100. Até a próxima mediocridade.\n")
                break
            
            if user_input.lower() in ['help', '/help', '?']:
                print("\nCOMANDOS:")
                print("  /help     - Esta ajuda")
                print("  /status   - Status do sistema")
                print("  /analyze  - Analisar trecho de roteiro")
                print("  /quit     - Sair")
                print("\nDIGITE qualquer pergunta sobre roteiros para análise brutal.")
                continue
            
            if user_input.lower() in ['/status', 'status']:
                print(f"\n📊 STATUS:")
                print(f"  Modelo: {model}")
                print(f"  RAG: {'✅ Ativo' if rag_available else '❌ Inativo'}")
                print(f"  Brutalidade: 85%")
                print(f"  Nota base: 62/100")
                continue
            
            if not user_input:
                continue
            
            # Preparar contexto com RAG se disponível
            context = ""
            if rag_available and not user_input.startswith('/'):
                try:
                    # Buscar conhecimento relevante
                    results = retriever.search(user_input, top_k=3)
                    if results:
                        context = "\n\nCONHECIMENTO RELEVANTE DOS MESTRES:\n"
                        for r in results[:2]:
                            text_preview = r.get('text', '')[:200]
                            context += f"- {text_preview}...\n"
                except:
                    pass
            
            # Construir prompt completo
            full_prompt = user_input
            if context:
                full_prompt = f"{context}\n\nPERGUNTA: {user_input}"
            
            # Gerar resposta com Ollama
            try:
                print("\n💭 Analisando...\n")
                
                response = ollama.chat(
                    model=model,
                    messages=[
                        {'role': 'system', 'content': system_prompt},
                        {'role': 'user', 'content': full_prompt}
                    ],
                    options={
                        'temperature': 0.7,
                        'top_p': 0.9
                    }
                )
                
                # Exibir resposta
                print(response['message']['content'])
                
            except Exception as e:
                print(f"\n❌ Erro ao gerar resposta: {e}")
                print("Tente novamente ou verifique se o Ollama está rodando.")
        
        except KeyboardInterrupt:
            print("\n\n⚠️ Interrompido. Digite 'sair' para encerrar.")
            continue
        except EOFError:
            print("\n\n62/100. Até a próxima mediocridade.\n")
            break
        except Exception as e:
            print(f"\n❌ Erro: {e}")
            continue
    
    return 0

if __name__ == "__main__":
    sys.exit(main())