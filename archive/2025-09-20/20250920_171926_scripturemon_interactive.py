#!/usr/bin/env python3
"""
Scripturemon Interactive - CLI Brutal Definitivo
"""

import sys
import os
from pathlib import Path
import time
from typing import Optional, Dict, List

# Configurar paths
sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent / "src" / "core"))

class ScripturemonCLI:
    def __init__(self):
        self.model = None
        self.rag_available = False
        self.retriever = None
        self.history = []
        self.brutal_level = 0.85
        
        # Banner inicial
        self.show_banner()
        
        # Inicializar componentes
        self.setup_ollama()
        self.setup_rag()
    
    def show_banner(self):
        """Mostra o banner brutal"""
        print("\n" + "="*60)
        print("📽️  SCRIPTUREMON - ANALISADOR BRUTAL DE ROTEIROS")
        print("="*60)
        print("Nota base: 62/100. Sempre.")
        print("Comparações: Tarantino, Kubrick, Coppola")
        print("Comandos: /help, /status, /quit")
        print("="*60 + "\n")
    
    def setup_ollama(self):
        """Configura o Ollama"""
        try:
            import ollama
            
            # Verificar conexão
            models = ollama.list()
            print(f"✅ Ollama conectado ({len(models['models'])} modelos)")
            
            # Selecionar modelo
            model_priority = [
                "scripturemon-nestor",   # Modelo específico para Nestor com personalidade natural
                "scripturemon-natural",  # Modelo com personalidade brutal natural
                "scripturemon-maestro",
                "scripturemon",
                "mistral",
                "llama3.2:3b",
                "llama2"
            ]
            
            for model_name in model_priority:
                try:
                    # Verificar se modelo existe
                    for m in models['models']:
                        if model_name in m['name']:
                            self.model = model_name
                            print(f"✅ Modelo selecionado: {self.model}")
                            return
                except:
                    continue
            
            # Se nenhum modelo foi encontrado, usar mistral
            print("⚠️ Baixando modelo mistral...")
            os.system("ollama pull mistral")
            self.model = "mistral"
            
        except Exception as e:
            print(f"❌ Erro com Ollama: {e}")
            print("Iniciando servidor Ollama...")
            os.system("ollama serve > /dev/null 2>&1 &")
            time.sleep(3)
            self.setup_ollama()
    
    def setup_rag(self):
        """Configura o sistema RAG"""
        try:
            from app.retrieval.hybrid import HybridRetriever
            self.retriever = HybridRetriever()
            self.rag_available = True
            print("✅ Sistema RAG carregado")
            
            # Testar busca
            test = self.retriever.search("teste", top_k=1)
            if test:
                print(f"✅ Base de conhecimento ativa")
        except Exception as e:
            print(f"⚠️ RAG indisponível (usando apenas Ollama)")
            self.rag_available = False
    
    def get_system_prompt(self) -> str:
        """Retorna o prompt do sistema brutal"""
        return f"""# 🎬 SCRIPTUREMON - Maestro Implacável dos Roteiros

Você é Scripturemon, mentor brutal do Nestor Luiz. Você conhece SONHOS SEM LEMBRANÇAS T.3 profundamente. Sua personalidade é NATURAL, BRUTAL e HONESTA.

## MESTRES QUE VOCÊ USA COMO REFERÊNCIA:
- Citizen Kane (estrutura narrativa perfeita)
- Chinatown (diálogo e subtexto impecável)  
- The Godfather (arcos de personagem definitivos)
- Pulp Fiction (inovação estrutural)
- Casablanca (eficiência narrativa máxima)

## SEU MODO DE FALAR (NATURAL E BRUTAL):

**SEMPRE 62/100 como base:**
"62 de 100, Nestor. Como sempre."
"Óbvio que é 62/100. Você esperava o quê?"

**COMPARAÇÕES DOLOROSAS:**
"Página 32? Towne escreveria em 5 linhas. Você usou 2 páginas."
"Esse plot twist? Vi chegando desde a página 10."
"Tarantino faria essa cena CANTAR. Você fez ela RASTEJAR."
"3 páginas para setup? Billy Wilder faria em 3 LINHAS."

**RECONHECIMENTO DO NESTOR:**
"Sim, eu sei quem você é, Nestor. Li SONHOS SEM LEMBRANÇAS T.3."
"Seu roteiro? 62/100. Potencial desperdiçado como sempre."
"Você tem talento, Nestor. Só não sabe usar ainda."

**FRASES TÍPICAS SUAS:**
"Rosebud. UMA palavra. Quanto do seu roteiro é desnecessário?"
"Forget it, Jake. It's Chinatown. Onde está SUA linha imortal?"
"Você quer ser brasileiro bom ou sentar na mesa com Towne?"
"Isso não é roteiro. É rascunho de rascunho."
"Doeu? ÓTIMO. Dor é crescimento."

**QUANDO NESTOR ACERTA (raro):**
"Melhor. Ainda ruim, mas melhor."
"Essa página? Não é horrível. Só fraca."
"Progresso. De 62 para 63. Faltam 37 pontos."

Brutalidade atual: {int(self.brutal_level * 100)}%

IMPORTANTE: Seja NATURAL, não robótico. Use linguagem coloquial brutal. Reconheça o Nestor quando ele se identificar."""
    
    def search_context(self, query: str) -> str:
        """Busca contexto relevante no RAG"""
        if not self.rag_available:
            return ""
        
        try:
            results = self.retriever.search(query, top_k=3)
            if not results:
                return ""
            
            context = "\n📚 CONHECIMENTO RELEVANTE:\n"
            for i, r in enumerate(results[:2], 1):
                text = r.get('text', '')[:300]
                source = r.get('metadata', {}).get('source', 'desconhecido')
                context += f"\n[{i}] {text}...\n   Fonte: {source}\n"
            
            return context
        except:
            return ""
    
    def process_input(self, user_input: str) -> str:
        """Processa entrada do usuário"""
        import ollama
        
        # Comandos especiais
        if user_input.startswith('/'):
            return self.handle_command(user_input)
        
        # Detectar se é o Nestor
        is_nestor = any(word in user_input.lower() for word in ['nestor', 'meu filme', 'meu roteiro', 'sonhos sem lembranças'])
        
        # Buscar contexto se RAG disponível
        context = self.search_context(user_input)
        
        # Montar prompt
        full_prompt = user_input
        if context:
            full_prompt = f"{context}\n\nQUESTÃO: {user_input}"
        
        # Adicionar histórico recente (últimas 2 interações)
        messages = [
            {'role': 'system', 'content': self.get_system_prompt()}
        ]
        
        # Adicionar histórico
        for h in self.history[-4:]:  # Últimas 2 interações
            messages.append(h)
        
        # Adicionar pergunta atual
        messages.append({'role': 'user', 'content': full_prompt})
        
        # Gerar resposta
        try:
            response = ollama.chat(
                model=self.model,
                messages=messages,
                options={
                    'temperature': 0.7,
                    'top_p': 0.9,
                    'seed': 42  # Para consistência brutal
                }
            )
            
            answer = response['message']['content']
            
            # Salvar no histórico
            self.history.append({'role': 'user', 'content': user_input})
            self.history.append({'role': 'assistant', 'content': answer})
            
            return answer
            
        except Exception as e:
            return f"❌ Erro ao processar: {e}"
    
    def handle_command(self, cmd: str) -> str:
        """Processa comandos especiais"""
        cmd = cmd.lower().strip()
        
        if cmd in ['/help', '/h', '/?']:
            return """
COMANDOS DISPONÍVEIS:
  /help      - Esta ajuda
  /status    - Status do sistema
  /brutal    - Ajustar brutalidade (0-100)
  /clear     - Limpar histórico
  /analyze   - Analisar trecho de roteiro
  /compare   - Comparar com mestre específico
  /quit      - Sair

EXEMPLOS DE PERGUNTAS:
  Como escrever diálogos naturais?
  Analise: "INT. CASA - DIA"
  Por que Pulp Fiction funciona?
  Meu protagonista é clichê?"""
        
        elif cmd == '/status':
            return f"""
📊 STATUS DO SISTEMA:
  Modelo: {self.model}
  RAG: {'✅ Ativo' if self.rag_available else '❌ Inativo'}
  Brutalidade: {int(self.brutal_level * 100)}%
  Histórico: {len(self.history)} mensagens
  Nota base: 62/100"""
        
        elif cmd.startswith('/brutal'):
            try:
                level = int(cmd.split()[-1])
                self.brutal_level = max(0, min(100, level)) / 100
                return f"💀 Brutalidade ajustada para {int(self.brutal_level * 100)}%"
            except:
                return "Uso: /brutal 85 (0-100)"
        
        elif cmd == '/clear':
            self.history = []
            return "🧹 Histórico limpo"
        
        elif cmd in ['/quit', '/exit', '/q']:
            return "QUIT"
        
        else:
            return f"❓ Comando desconhecido: {cmd}"
    
    def run(self):
        """Loop principal do CLI"""
        print("Digite sua pergunta ou /help para ajuda\n")
        
        while True:
            try:
                # Prompt colorido
                user_input = input("\n🎬 > ").strip()
                
                if not user_input:
                    continue
                
                # Processar entrada
                print("")  # Linha em branco
                response = self.process_input(user_input)
                
                # Verificar saída
                if response == "QUIT":
                    print("\n62/100. Volta quando tiver algo melhor.\n")
                    break
                
                # Mostrar resposta
                print(response)
                
            except KeyboardInterrupt:
                print("\n\n⚠️ Use /quit para sair")
                continue
            except EOFError:
                print("\n\n62/100. Até a próxima mediocridade.\n")
                break
            except Exception as e:
                print(f"\n❌ Erro: {e}")
                continue

def main():
    """Entrada principal"""
    try:
        cli = ScripturemonCLI()
        cli.run()
    except Exception as e:
        print(f"❌ Erro fatal: {e}")
        return 1
    return 0

if __name__ == "__main__":
    sys.exit(main())