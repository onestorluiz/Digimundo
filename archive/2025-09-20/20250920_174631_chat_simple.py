#!/usr/bin/env python3
"""
Chat Simplificado - ScriptureMon Champion
Inspirado no chat original mas adaptado para o sistema Champion
Fase 5.B - Reparação Inteligente
Fase 7 - Integração com OllamaCore
"""

import sys
import os
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any, List
import logging

# Importa módulos locais
from .doctor import analyze, deep_analyze, validate_script
from .ai_sentiment import analyze_text_sentiment
from .backup_manager import create_backup
from .memory_simple import get_cache_stats, get_memory_cache

# NOVO: Importa OllamaCore para LLM real
try:
    from .ollama_core import OllamaCore
    ollama_available = True
except ImportError:
    ollama_available = False
    print("⚠️ OllamaCore não disponível - modo fallback ativo")

logger = logging.getLogger(__name__)

class ConversationHistory:
    """Gerencia histórico simplificado de conversas"""
    
    def __init__(self, max_size: int = 10):
        self.max_size = max_size
        self.history = []
        
    def add(self, user_input: str, bot_response: str):
        """Adiciona interação ao histórico"""
        self.history.append({
            "user": user_input,
            "bot": bot_response,
            "timestamp": datetime.now().isoformat()
        })
        
        # Mantém apenas últimas N mensagens
        if len(self.history) > self.max_size:
            self.history.pop(0)
            
    def get_context(self) -> str:
        """Retorna contexto formatado"""
        if not self.history:
            return "Nenhuma conversa anterior."
        
        context = []
        for h in self.history[-3:]:  # Últimas 3 interações
            context.append(f"User: {h['user'][:100]}")
            context.append(f"Bot: {h['bot'][:100]}")
        
        return "\n".join(context)

class SimpleChat:
    """
    Sistema de chat simplificado para ScriptureMon Champion
    Baseado no chat original mas sem dependências complexas
    Fase 7: Integrado com OllamaCore
    """

    def __init__(self):
        """Inicializa chat simplificado"""
        self.history = ConversationHistory()
        self.running = True
        self.style = "professional"  # professional, casual, technical

        # Inicializa OllamaCore se disponível
        self.ollama = None
        if ollama_available:
            try:
                self.ollama = OllamaCore()
                logger.info(f"✅ OllamaCore inicializado com {len(self.ollama.models)} modelos")
            except Exception as e:
                logger.warning(f"⚠️ OllamaCore não pôde ser inicializado: {e}")

        self.stats = {
            "messages": 0,
            "commands": 0,
            "analyses": 0,
            "start_time": datetime.now()
        }
        
        # Comandos disponíveis
        self.commands = {
            "/help": self.cmd_help,
            "/status": self.cmd_status,
            "/analyze": self.cmd_analyze,
            "/deep": self.cmd_deep_analyze,
            "/validate": self.cmd_validate,
            "/sentiment": self.cmd_sentiment,
            "/cache": self.cmd_cache,
            "/style": self.cmd_style,
            "/history": self.cmd_history,
            "/clear": self.cmd_clear,
            "/backup": self.cmd_backup,
            "/exit": self.cmd_exit,
            "/quit": self.cmd_exit
        }
        
        logger.info("✅ SimpleChat inicializado")
    
    def cmd_help(self, args: str = "") -> str:
        """Mostra comandos disponíveis"""
        return """
🎬 **COMANDOS DO SCRIPTUREMON CHAMPION**

**Análise:**
• `/analyze [arquivo]` - Analisa um roteiro
• `/deep [arquivo]` - Análise profunda com AI
• `/validate [arquivo]` - Valida formato de roteiro
• `/sentiment [texto]` - Análise de sentimento

**Chat:**
• `/style [professional|casual|technical]` - Muda estilo
• `/history` - Mostra histórico recente
• `/clear` - Limpa histórico

**Sistema:**
• `/status` - Status do sistema
• `/cache` - Estatísticas do cache
• `/backup` - Criar backup
• `/help` - Esta ajuda
• `/exit` ou `/quit` - Sair

Digite normalmente para conversar!
"""
    
    def cmd_status(self, args: str = "") -> str:
        """Mostra status do sistema"""
        uptime = datetime.now() - self.stats['start_time']
        hours = int(uptime.total_seconds() // 3600)
        minutes = int((uptime.total_seconds() % 3600) // 60)
        
        return f"""
📊 **STATUS DO SISTEMA**

**Uptime:** {hours}h {minutes}m
**Mensagens:** {self.stats['messages']}
**Comandos:** {self.stats['commands']}
**Análises:** {self.stats['analyses']}
**Estilo:** {self.style}
**Ollama:** {'✅ Ativo' if self.ollama else '❌ Offline'}
**Histórico:** {len(self.history.history)} mensagens

✅ Sistema operacional
"""
    
    def cmd_analyze(self, args: str) -> str:
        """Analisa um roteiro"""
        if not args:
            return "❌ Use: /analyze caminho/do/arquivo.txt"
        
        file_path = Path(args.strip())
        if not file_path.exists():
            return f"❌ Arquivo não encontrado: {file_path}"
        
        try:
            result = analyze(file_path)
            self.stats['analyses'] += 1
            
            if result['status'] == 'success':
                return f"""
✅ **ANÁLISE COMPLETA**

**Arquivo:** {file_path.name}
**Score:** {result['score']}/100 ({result['grade']})

**Pontos Fortes:**
{chr(10).join(['• ' + s for s in result.get('strengths', [])[:3]])}

**Pontos a Melhorar:**
{chr(10).join(['• ' + w for w in result.get('weaknesses', [])[:3]])}

**Recomendações:**
{chr(10).join(['• ' + r for r in result.get('recommendations', [])[:3]])}
"""
            else:
                return f"❌ Erro na análise: {result.get('message', 'Desconhecido')}"
                
        except Exception as e:
            logger.error(f"Erro analisando: {e}")
            return f"❌ Erro: {str(e)}"
    
    def cmd_deep_analyze(self, args: str) -> str:
        """Análise profunda com AI de um roteiro"""
        if not args:
            return "❌ Use: /deep caminho/do/arquivo.txt"
        
        file_path = Path(args.strip())
        if not file_path.exists():
            return f"❌ Arquivo não encontrado: {file_path}"
        
        try:
            result = deep_analyze(file_path)
            self.stats['analyses'] += 1
            
            if result['status'] == 'success':
                output = f"""
🤖 **ANÁLISE PROFUNDA COM AI**

**Arquivo:** {file_path.name}
**Score:** {result['score']}/100 ({result['grade']})

**📈 Métricas AI:**
• Sentimento: {result['deep_metrics']['sentiment']:.2f}
• Complexidade: {result['deep_metrics']['complexity']:.2f}
• Originalidade: {result['deep_metrics']['originality']:.2f}
• Potencial Mercado: {result['deep_metrics']['market_potential']:.2f}

**🎯 Recomendações AI:**"""
                
                if result.get('ai_recommendations'):
                    for i, rec in enumerate(result['ai_recommendations'][:3], 1):
                        output += f"\n{i}. [{rec['priority'].upper()}] {rec['title']}"
                        output += f"\n   {rec['description'][:100]}..."
                else:
                    output += "\nNenhuma recomendação gerada."
                
                return output
            else:
                return f"❌ Erro na análise: {result.get('message', 'Desconhecido')}"
                
        except Exception as e:
            logger.error(f"Erro em deep_analyze: {e}")
            return f"❌ Erro: {str(e)}"
    
    def cmd_validate(self, args: str) -> str:
        """Valida formato de roteiro"""
        if not args:
            return "❌ Use: /validate caminho/do/arquivo.txt"
        
        file_path = Path(args.strip())
        if not file_path.exists():
            return f"❌ Arquivo não encontrado: {file_path}"
        
        try:
            result = validate_script(file_path)
            
            if result['valid']:
                return f"""
✅ **ROTEIRO VÁLIDO**

**Páginas estimadas:** {result.get('estimated_pages', 'N/A')}
**Formatação detectada:** {'Sim' if result.get('has_formatting') else 'Não'}

**Avisos:**
{chr(10).join(['• ' + w for w in result.get('warnings', [])])}
"""
            else:
                return f"""
❌ **ROTEIRO INVÁLIDO**

**Erros:**
{chr(10).join(['• ' + e for e in result.get('errors', [])])}

**Avisos:**
{chr(10).join(['• ' + w for w in result.get('warnings', [])])}
"""
                
        except Exception as e:
            logger.error(f"Erro validando: {e}")
            return f"❌ Erro: {str(e)}"
    
    def cmd_sentiment(self, args: str) -> str:
        """Análise de sentimento de texto"""
        if not args:
            return "❌ Use: /sentiment seu texto aqui"
        
        try:
            result = analyze_text_sentiment(args)
            
            # Determinar sentimento dominante
            if result.compound > 0.1:
                dominant = "POSITIVO 😊"
            elif result.compound < -0.1:
                dominant = "NEGATIVO 😔"
            else:
                dominant = "NEUTRO 😐"
            
            return f"""
🎭 **ANÁLISE DE SENTIMENTO**

**Texto:** "{args[:100]}{'...' if len(args) > 100 else ''}"

**Sentimento:** {dominant}
**Score Composto:** {result.compound:.2f}

**Detalhes:**
• Positivo: {result.positive*100:.1f}%
• Negativo: {result.negative*100:.1f}%
• Neutro: {result.neutral*100:.1f}%
• Confiança: {result.confidence*100:.1f}%
"""
            
        except Exception as e:
            logger.error(f"Erro em sentimento: {e}")
            return f"❌ Erro: {str(e)}"
    
    def cmd_style(self, args: str) -> str:
        """Muda estilo de resposta"""
        styles = ["professional", "casual", "technical"]
        
        if not args or args not in styles:
            return f"❌ Use: /style {{'|'.join(styles)}}"
        
        self.style = args
        return f"✅ Estilo mudado para: {self.style}"
    
    def cmd_history(self, args: str = "") -> str:
        """Mostra histórico recente"""
        if not self.history.history:
            return "📜 Histórico vazio"
        
        output = ["📜 **HISTÓRICO RECENTE**\n"]
        for h in self.history.history[-5:]:
            time = datetime.fromisoformat(h['timestamp']).strftime("%H:%M")
            output.append(f"[{time}] User: {h['user'][:50]}...")
            output.append(f"[{time}] Bot: {h['bot'][:50]}...\n")
        
        return "\n".join(output)
    
    def cmd_clear(self, args: str = "") -> str:
        """Limpa histórico"""
        self.history.history = []
        return "✅ Histórico limpo"
    
    def cmd_cache(self, args: str = "") -> str:
        """Mostra estatísticas do cache"""
        try:
            stats = get_cache_stats()
            cache = get_memory_cache()
            recent = cache.list_recent(5)
            
            output = f"""
💾 **CACHE E MEMÓRIA**

**📊 Estatísticas:**
• Diretório: {stats['cache_directory']}
• Arquivos: {stats['total_files']}
• Tamanho: {stats['total_size_mb']} MB
• Taxa de Acerto: {stats['hit_rate']}

**📈 Conteúdo:**
• Análises em cache: {stats['analyses_cached']}
• Conversas salvas: {stats['conversations_saved']}
• Recomendações: {stats['recommendations_cached']}

**🕐 Análises Recentes:**"""
            
            if recent['analyses']:
                for analysis in recent['analyses'][:3]:
                    output += f"\n• {analysis['file']} - Score: {analysis['score']}"
            else:
                output += "\nNenhuma análise recente"
            
            return output
            
        except Exception as e:
            logger.error(f"Erro obtendo cache: {e}")
            return f"❌ Erro: {str(e)}"
    
    def cmd_backup(self, args: str = "") -> str:
        """Cria backup do sistema"""
        try:
            result = create_backup()
            return f"✅ Backup criado: {result['filename']} ({result['size_mb']:.2f} MB)"
        except Exception as e:
            return f"❌ Erro criando backup: {str(e)}"
    
    def cmd_exit(self, args: str = "") -> str:
        """Sai do chat"""
        self.running = False
        return "👋 Até logo! Obrigado por usar o ScriptureMon."
    
    def process_command(self, user_input: str) -> str:
        """Processa comandos"""
        parts = user_input.split(maxsplit=1)
        command = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ""
        
        if command in self.commands:
            self.stats['commands'] += 1
            return self.commands[command](args)
        
        return f"❌ Comando desconhecido: {command}\nDigite /help para ajuda."
    
    def generate_response(self, user_input: str) -> str:
        """Gera resposta para entrada normal"""

        # NOVO: Usa OllamaCore se disponível
        if self.ollama:
            try:
                # Prepara contexto com histórico
                context = self.history.get_context()

                # Prompt baseado no estilo
                style_prompts = {
                    "professional": "Você é um analista de roteiros profissional. Responda de forma técnica e precisa.",
                    "casual": "Você é um amigo que entende de cinema. Responda de forma descontraída.",
                    "technical": "Você é um especialista técnico em narrativa cinematográfica. Use termos técnicos."
                }

                system_prompt = style_prompts.get(self.style, style_prompts["professional"])

                # Gera resposta com Ollama
                # Adiciona contexto ao prompt se disponível
                full_prompt = user_input
                if context and context != "Nenhuma conversa anterior.":
                    full_prompt = f"Contexto anterior:\n{context}\n\nPergunta: {user_input}"

                response = self.ollama.generate(
                    prompt=full_prompt,
                    system=system_prompt,
                    max_tokens=500
                )

                # OllamaCore.generate() retorna string diretamente, não dict
                if response:
                    if isinstance(response, str):
                        return response
                    elif isinstance(response, dict) and response.get('text'):
                        return response['text']

            except Exception as e:
                logger.warning(f"Ollama falhou, usando fallback: {e}")

        # Fallback: Respostas baseadas no estilo
        responses = {
            "professional": {
                "greeting": "Olá! Como posso ajudar com sua análise de roteiro hoje?",
                "unknown": "Desculpe, não entendi completamente. Pode reformular?",
                "roteiro": "Para análise de roteiros, use /analyze com o caminho do arquivo.",
                "help": "Digite /help para ver todos os comandos disponíveis."
            },
            "casual": {
                "greeting": "E aí! Vamos analisar uns roteiros hoje?",
                "unknown": "Ops, não peguei essa. Tenta de novo?",
                "roteiro": "Quer analisar um roteiro? Manda /analyze e o arquivo!",
                "help": "Perdido? Digita /help que eu te mostro o caminho!"
            },
            "technical": {
                "greeting": "Sistema iniciado. Aguardando comandos.",
                "unknown": "Entrada não reconhecida. Reformule a query.",
                "roteiro": "Execute /analyze <path> para processar script.",
                "help": "Execute /help para documentação de comandos."
            }
        }
        
        style_responses = responses.get(self.style, responses["professional"])
        
        # Detecta intenção básica
        lower_input = user_input.lower()
        
        if any(word in lower_input for word in ["olá", "oi", "hey", "hello"]):
            return style_responses["greeting"]
        elif "roteiro" in lower_input or "script" in lower_input:
            return style_responses["roteiro"]
        elif "ajuda" in lower_input or "help" in lower_input:
            return style_responses["help"]
        else:
            # Resposta genérica baseada no contexto
            return style_responses["unknown"]
    
    def chat_loop(self):
        """Loop principal do chat"""
        print("\n🎬 ScriptureMon Chat - Modo Interativo")
        print("Digite /help para ajuda ou /exit para sair")
        print("-" * 50)
        
        while self.running:
            try:
                # Prompt
                user_input = input("\n🎬 > ").strip()
                
                if not user_input:
                    continue
                
                # Processa entrada
                if user_input.startswith("/"):
                    response = self.process_command(user_input)
                else:
                    self.stats['messages'] += 1
                    response = self.generate_response(user_input)
                
                # Adiciona ao histórico
                self.history.add(user_input, response)
                
                # Mostra resposta
                print(response)
                
            except KeyboardInterrupt:
                print("\n\n⚠️  Interrompido. Use /exit para sair corretamente.")
            except EOFError:
                # Quando recebe EOF (como em pipe)
                print("\n❌ Entrada fechada. Saindo...")
                break
            except Exception as e:
                logger.error(f"Erro no chat: {e}")
                print(f"❌ Erro: {str(e)}")
    
    def process_single(self, user_input: str) -> str:
        """Processa uma única entrada (para modo não-interativo)"""
        if user_input.startswith("/"):
            return self.process_command(user_input)
        else:
            return self.generate_response(user_input)

def main():
    """Função principal do chat"""
    try:
        chat = SimpleChat()
        
        # Verifica se tem input via pipe
        if not sys.stdin.isatty():
            # Modo não-interativo (pipe)
            input_text = sys.stdin.read().strip()
            if input_text:
                response = chat.process_single(input_text)
                print(response)
        else:
            # Modo interativo
            chat.chat_loop()
            
    except Exception as e:
        logger.error(f"Erro fatal no chat: {e}")
        print(f"❌ Erro fatal: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()