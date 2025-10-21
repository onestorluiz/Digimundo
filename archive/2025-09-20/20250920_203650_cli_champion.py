#!/usr/bin/env python3
"""
🎬 CLI CHAMPION - Interface de Linha de Comando Unificada
Comando único para todo o sistema ScriptureMon Champion
"""

import typer
from rich import print
from rich.table import Table
from rich.console import Console
from pathlib import Path
import sys

# Adiciona o diretório raiz ao path para imports
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

app = typer.Typer(rich_markup_mode="rich")
console = Console()

@app.command()
def status():
    """📊 Mostra status do sistema e estatísticas"""
    try:
        from src.core.unified_memory_system import get_unified_memory

        mem = get_unified_memory()

        table = Table(title="🎬 ScriptureMon Champion - Status")
        table.add_column("Componente", style="cyan")
        table.add_column("Status", style="green")
        table.add_column("Detalhes", style="yellow")

        # Memória
        try:
            stats = mem.get_stats() if hasattr(mem, 'get_stats') else {"entries": "N/A"}
            table.add_row("Memória Unificada", "✅ OK", f"Entradas: {stats}")
        except Exception as e:
            table.add_row("Memória Unificada", "❌ ERRO", str(e))

        # Modelos
        try:
            import subprocess
            result = subprocess.run(['ollama', 'list'], capture_output=True, text=True)
            models = len([line for line in result.stdout.split('\n') if 'mixtral' in line.lower()])
            table.add_row("Modelos Mixtral", "✅ OK" if models > 0 else "⚠️ AVISO", f"{models} modelos")
        except:
            table.add_row("Modelos Mixtral", "❓ DESCONHECIDO", "Ollama não verificado")

        # Biblioteca
        library_path = project_root / "digilibrary" / "BIBLIOTECA_ROTEIROS"
        if library_path.exists():
            scripts = len(list(library_path.rglob("*.txt")))
            table.add_row("Biblioteca Roteiros", "✅ OK", f"{scripts} roteiros")
        else:
            table.add_row("Biblioteca Roteiros", "❌ ERRO", "Pasta não encontrada")

        console.print(table)

    except Exception as e:
        console.print(f"❌ Erro ao verificar status: {e}", style="red")

@app.command()
def analyze(file: str = typer.Argument(..., help="Arquivo de roteiro para analisar")):
    """🎭 Analisa um roteiro usando Script Doctor"""
    try:
        from src.core.script_doctor_system import ScriptDoctorSystem

        file_path = Path(file)
        if not file_path.exists():
            console.print(f"❌ Arquivo não encontrado: {file}", style="red")
            return

        console.print(f"🎬 Analisando roteiro: {file}")

        text = file_path.read_text(encoding="utf-8", errors="replace")

        sd = ScriptDoctorSystem()
        result = sd.analyze_script(text)

        console.print("✅ Análise completa!")
        console.print(result)

    except Exception as e:
        console.print(f"❌ Erro na análise: {e}", style="red")

@app.command()
def memory_stats():
    """🧠 Estatísticas detalhadas da memória"""
    try:
        from src.core.unified_memory_system import get_unified_memory

        mem = get_unified_memory()

        console.print("🧠 [bold]Estatísticas da Memória Unificada[/bold]")

        # Informações básicas
        if hasattr(mem, 'retrieve_all'):
            all_entries = mem.retrieve_all()
            console.print(f"📦 Total de entradas: {len(all_entries)}")

            # Contar por tipo
            types_count = {}
            for entry in all_entries:
                entry_type = entry.get('type', 'unknown')
                types_count[entry_type] = types_count.get(entry_type, 0) + 1

            if types_count:
                table = Table(title="Distribuição por Tipo")
                table.add_column("Tipo", style="cyan")
                table.add_column("Quantidade", style="green")

                for t, count in sorted(types_count.items()):
                    table.add_row(t, str(count))

                console.print(table)
        else:
            console.print("⚠️ Método retrieve_all não disponível")

    except Exception as e:
        console.print(f"❌ Erro ao obter estatísticas: {e}", style="red")

@app.command()
def models():
    """🤖 Lista modelos Ollama disponíveis"""
    try:
        import subprocess

        console.print("🤖 [bold]Modelos Ollama Disponíveis[/bold]")

        result = subprocess.run(['ollama', 'list'], capture_output=True, text=True)

        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')
            if len(lines) > 1:  # Pular header
                table = Table()
                table.add_column("Modelo", style="cyan")
                table.add_column("ID", style="yellow")
                table.add_column("Tamanho", style="green")
                table.add_column("Modificado", style="blue")

                for line in lines[1:]:  # Pular header
                    if line.strip():
                        parts = line.split()
                        if len(parts) >= 4:
                            table.add_row(parts[0], parts[1], parts[2], " ".join(parts[3:]))

                console.print(table)
            else:
                console.print("📭 Nenhum modelo encontrado")
        else:
            console.print(f"❌ Erro ao listar modelos: {result.stderr}", style="red")

    except FileNotFoundError:
        console.print("❌ Ollama não está instalado ou não está no PATH", style="red")
    except Exception as e:
        console.print(f"❌ Erro: {e}", style="red")

@app.command()
def library():
    """📚 Mostra roteiros disponíveis na biblioteca"""
    try:
        from src.core.screenplay_library import ScreenplayLibrary

        library = ScreenplayLibrary()

        console.print("📚 [bold]Biblioteca de Roteiros[/bold]")

        if hasattr(library, 'list_screenplays'):
            screenplays = library.list_screenplays()

            if screenplays:
                table = Table()
                table.add_column("Título", style="cyan")
                table.add_column("Categoria", style="yellow")
                table.add_column("Tamanho", style="green")

                for screenplay in screenplays[:20]:  # Limitar a 20 para não sobrecarregar
                    title = screenplay.get('title', 'Sem título')
                    category = screenplay.get('category', 'Desconhecida')
                    size = screenplay.get('size', 'N/A')
                    table.add_row(title, category, str(size))

                console.print(table)

                if len(screenplays) > 20:
                    console.print(f"... e mais {len(screenplays) - 20} roteiros")
            else:
                console.print("📭 Nenhum roteiro encontrado")
        else:
            console.print("⚠️ Método list_screenplays não disponível")

    except Exception as e:
        console.print(f"❌ Erro ao listar biblioteca: {e}", style="red")

def main():
    """Entry point principal"""
    try:
        app()
    except KeyboardInterrupt:
        console.print("\n👋 Saindo...", style="yellow")
    except Exception as e:
        console.print(f"❌ Erro crítico: {e}", style="red")
        sys.exit(1)

if __name__ == "__main__":
    main()