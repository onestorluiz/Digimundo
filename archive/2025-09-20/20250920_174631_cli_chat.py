#!/usr/bin/env python3
"""
💬 CLI Chat Interativo com RAG Smart
"""

import sys
from pathlib import Path
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.markdown import Markdown
import typer

from apps.scripturemon.rag_smart_manager import RAGSmartManager
from apps.scripturemon.rag_system import RAGQuery, RetrievalStrategy

app = typer.Typer()
console = Console()

class InteractiveChat:
    """Chat interativo com RAG inteligente"""

    def __init__(self):
        self.smart_manager = RAGSmartManager()
        self.chat_history = []

    def process_message(self, message: str) -> str:
        """Processa mensagem com RAG Smart"""
        # Processar com Smart Manager
        result = self.smart_manager.process_input(message)

        # Feedback visual sobre RAG
        if result['rag_activated']:
            console.print("[dim cyan]🔮 RAG ativado - contexto de roteiro detectado[/dim cyan]")
        elif result['rag_deactivated']:
            console.print("[dim yellow]💤 RAG desativado - mudança de contexto[/dim yellow]")
        elif result['rag_is_active']:
            console.print("[dim green]✓ RAG ativo[/dim green]", end="")

        # Se RAG está ativo e temos uma pergunta sobre roteiro
        if result['rag_is_active'] and result.get('rag'):
            # Criar query RAG
            rag_query = RAGQuery(
                query=message,
                strategy=RetrievalStrategy.HYBRID,
                max_results=5
            )

            try:
                # Executar query
                rag_result = result['rag'].query(rag_query)

                # Adicionar metadados
                response = rag_result.generated_text
                if rag_result.confidence > 0:
                    response += f"\n\n[dim]Confiança: {rag_result.confidence:.1%} | "
                    response += f"Fontes: {len(rag_result.retrieved_chunks)}[/dim]"

                return response

            except Exception as e:
                return f"Erro ao consultar RAG: {e}"

        # Resposta padrão sem RAG
        return self._default_response(message, result['context'])

    def _default_response(self, message: str, context: str) -> str:
        """Resposta padrão quando RAG não está ativo"""
        if context == 'technical':
            return "Para comandos técnicos, use os comandos específicos do CLI (status, compress, etc.)"
        else:
            return "Para perguntas sobre roteiros, mencione elementos como personagens, cenas ou diálogos."

    def chat_loop(self):
        """Loop principal do chat"""
        console.print(Panel.fit(
            "[bold cyan]💬 SCRIPTUREMON CHAT INTERATIVO[/bold cyan]\n"
            "[dim]RAG Smart ativado - detecta automaticamente contexto de roteiros[/dim]\n"
            "[yellow]Digite 'sair' para encerrar[/yellow]",
            border_style="cyan"
        ))

        console.print("\n[dim]Dica: Mencione roteiros, personagens ou cenas para ativar o RAG[/dim]\n")

        while True:
            try:
                # Prompt
                message = Prompt.ask("\n[bold blue]Você[/bold blue]")

                # Comandos especiais
                if message.lower() in ['sair', 'exit', 'quit']:
                    console.print("[yellow]👋 Até logo![/yellow]")
                    break
                elif message.lower() == 'status':
                    status = self.smart_manager.get_status()
                    console.print(f"\n[cyan]Status RAG:[/cyan]")
                    for key, value in status.items():
                        console.print(f"  {key}: {value}")
                    continue
                elif message.lower() == 'clear':
                    console.clear()
                    continue

                # Processar mensagem
                console.print("\n[bold green]Scripturemon[/bold green]: ", end="")
                response = self.process_message(message)

                # Formatar resposta
                if "```" in response:
                    # Tem código
                    console.print(Markdown(response))
                else:
                    console.print(response)

                # Adicionar ao histórico
                self.chat_history.append({
                    'user': message,
                    'assistant': response,
                    'rag_active': self.smart_manager.is_active
                })

            except KeyboardInterrupt:
                console.print("\n[yellow]Use 'sair' para encerrar[/yellow]")
            except Exception as e:
                console.print(f"[red]Erro: {e}[/red]")


@app.command()
def chat():
    """Inicia chat interativo com RAG Smart"""
    chat_session = InteractiveChat()
    chat_session.chat_loop()


@app.command()
def ask(
    question: str = typer.Argument(..., help="Pergunta para o Scripturemon"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Mostrar detalhes do RAG")
):
    """Faz uma pergunta única com RAG Smart"""
    manager = RAGSmartManager()

    # Processar pergunta
    result = manager.process_input(question)

    if verbose:
        console.print(f"[dim]Contexto: {result['context']}[/dim]")
        console.print(f"[dim]RAG: {'Ativo' if result['rag_is_active'] else 'Inativo'}[/dim]")

    # Se RAG está ativo
    if result['rag_is_active'] and result.get('rag'):
        rag_query = RAGQuery(
            query=question,
            strategy=RetrievalStrategy.HYBRID,
            max_results=5
        )

        try:
            rag_result = result['rag'].query(rag_query)
            console.print(rag_result.generated_text)

            if verbose:
                console.print(f"\n[dim]Confiança: {rag_result.confidence:.1%}[/dim]")
                console.print(f"[dim]Chunks: {len(rag_result.retrieved_chunks)}[/dim]")

        except Exception as e:
            console.print(f"[red]Erro: {e}[/red]")
    else:
        # Resposta sem RAG
        if result['context'] == 'technical':
            console.print("Para comandos técnicos, use os comandos específicos do CLI.")
        else:
            console.print("RAG não ativado. Mencione elementos de roteiro para ativar.")


if __name__ == "__main__":
    # Teste direto
    if len(sys.argv) > 1:
        app()
    else:
        # Iniciar chat interativo
        chat_session = InteractiveChat()
        chat_session.chat_loop()