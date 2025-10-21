#!/usr/bin/env python3
"""
Sistema de Checkpoint Melhorado - Scripturemon
Permite listar e continuar análises incompletas
"""

import json
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from datetime import datetime


class CheckpointInfo:
    """Informações de um checkpoint encontrado"""

    def __init__(self, checkpoint_path: Path):
        self.path = checkpoint_path
        self.folder = checkpoint_path.parent.parent
        self.data = self._load()

    def _load(self) -> Dict:
        """Carrega dados do checkpoint"""
        try:
            with open(self.path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            return {}

    @property
    def is_complete(self) -> bool:
        """Verifica se a análise está completa"""
        completed = len(self.data.get('completed', []))
        total = self.data.get('total_analyses', 312)
        return completed >= total

    @property
    def progress(self) -> Tuple[int, int]:
        """Retorna (completos, total)"""
        return (
            len(self.data.get('completed', [])),
            self.data.get('total_analyses', 312)
        )

    @property
    def percentage(self) -> float:
        """Retorna porcentagem completa"""
        completed, total = self.progress
        return (completed / total * 100) if total > 0 else 0

    @property
    def screenplay_name(self) -> str:
        """Nome do roteiro"""
        return self.data.get('screenplay_name', 'Unknown')

    @property
    def model(self) -> str:
        """
        Modelo LLM usado.
        Tenta pegar do checkpoint primeiro, senão extrai do nome da pasta.
        Suporta AMBOS formatos: antigo e novo.
        """
        # Tentar do checkpoint primeiro
        checkpoint_model = self.data.get('model')
        if checkpoint_model:
            return checkpoint_model

        # Fallback: extrair do nome da pasta
        # Novo formato: SCREENPLAY__SCOPE_MODEL_DD-MM-YY_HH-MM_SEQ
        # Antigo formato: SCREENPLAY__SCOPE_SEQ ou SCREENPLAY_SCOPE_SEQ
        folder_name = self.folder.name

        # Verificar formato novo (com timestamps)
        if '__' in folder_name:
            parts = folder_name.split('__')
            if len(parts) == 2:
                # parts[1] = 'SCOPE_MODEL_DD-MM-YY_HH-MM_SEQ' ou 'SCOPE_SEQ'
                rest_parts = parts[1].split('_')
                if len(rest_parts) >= 5:  # Novo formato
                    # rest_parts[1] é o modelo
                    return rest_parts[1]  # 'ollama', 'gpt', 'mixed'

        # Formato antigo ou desconhecido
        return 'ollama'  # Default para análises antigas

    @property
    def last_update(self) -> str:
        """Última atualização"""
        timestamp = self.data.get('last_updated', '')
        try:
            dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            return dt.strftime('%Y-%m-%d %H:%M')
        except:
            return timestamp

    @property
    def current_specialist(self) -> Optional[str]:
        """Especialista atual"""
        if not self.data.get('completed'):
            return "DrCharacter"  # Primeiro especialista

        last = self.data['completed'][-1]
        return last[0] if last else None

    @property
    def current_author(self) -> Optional[str]:
        """Autor atual"""
        if not self.data.get('completed'):
            return "mckee"  # Primeiro autor

        last = self.data['completed'][-1]
        return last[1] if len(last) > 1 else None

    def get_resume_point(self) -> Optional[Tuple[str, str]]:
        """Retorna (specialist, author) para continuar"""
        if self.is_complete:
            return None

        if not self.data.get('completed'):
            return ("character", "mckee")  # Início

        # Pegar último completo
        last_specialist, last_author = self.data['completed'][-1]

        # Importar lista de especialistas e autores
        from analyze_all_specialists import ALL_SPECIALISTS, AUTHORS

        # Encontrar índices
        specialist_idx = next(
            (i for i, (name, _, _) in enumerate(ALL_SPECIALISTS) if name == last_specialist),
            0
        )
        author_idx = next(
            (i for i, name in enumerate(AUTHORS) if name == last_author),
            0
        )

        # Próximo author
        author_idx += 1
        if author_idx >= len(AUTHORS):
            author_idx = 0
            specialist_idx += 1

        if specialist_idx >= len(ALL_SPECIALISTS):
            return None  # Completo!

        next_specialist = ALL_SPECIALISTS[specialist_idx][0]
        next_author = AUTHORS[author_idx]

        return (next_specialist, next_author)

    def __str__(self) -> str:
        """Representação em string"""
        completed, total = self.progress
        return (
            f"{self.folder.name}\n"
            f"  📄 Roteiro: {self.screenplay_name}\n"
            f"  🤖 Modelo: {self.model}\n"
            f"  📊 Progresso: {completed}/{total} ({self.percentage:.1f}%)\n"
            f"  🔬 Último: {self.current_specialist} × {self.current_author}\n"
            f"  🕐 Atualizado: {self.last_update}"
        )


def find_incomplete_checkpoints(workspace_dir: str = "workspace/outputs") -> List[CheckpointInfo]:
    """
    Busca TODAS as análises incompletas no workspace.

    Returns:
        List of CheckpointInfo objects for incomplete analyses
    """
    workspace = Path(workspace_dir)
    if not workspace.exists():
        return []

    incomplete = []

    # Buscar todos os checkpoints
    for checkpoint_path in workspace.glob("*/2_logs/checkpoint.json"):
        checkpoint = CheckpointInfo(checkpoint_path)

        # Adicionar se incompleto
        if not checkpoint.is_complete:
            incomplete.append(checkpoint)

    # Ordenar por última atualização (mais recente primeiro)
    incomplete.sort(
        key=lambda c: c.data.get('last_updated', ''),
        reverse=True
    )

    return incomplete


def prompt_user_with_buttons() -> Optional[CheckpointInfo]:
    """
    Versão com BOTÕES (macOS native dialog).
    Pergunta ao usuário se quer continuar análise anterior.
    Lista checkpoints disponíveis e permite escolha através de botões.

    Returns:
        CheckpointInfo selecionado ou None se começar nova análise
    """
    import subprocess

    # Buscar checkpoints incompletos
    checkpoints = find_incomplete_checkpoints()

    if not checkpoints:
        # Nenhum checkpoint encontrado
        script = '''
        tell application "System Events"
            activate
            display dialog "✅ Nenhuma análise incompleta encontrada.\\n\\nIniciando nova análise..." buttons {"OK"} default button 1 with icon note
        end tell
        '''
        subprocess.run(['osascript', '-e', script], check=False)
        return None

    # Construir mensagem com lista de checkpoints
    msg_lines = ["♻️  ANÁLISES INCOMPLETAS ENCONTRADAS\\n"]
    msg_lines.append(f"Encontradas {len(checkpoints)} análise(s):\\n")

    for i, cp in enumerate(checkpoints, 1):
        completed, total = cp.progress
        percentage = cp.percentage
        resume = cp.get_resume_point()

        msg_lines.append(f"{i}. {cp.screenplay_name}")
        msg_lines.append(f"   🤖 {cp.model}")
        msg_lines.append(f"   📊 {completed}/{total} ({percentage:.1f}%)")
        if resume:
            msg_lines.append(f"   ▶️  Próximo: {resume[0]} × {resume[1]}")
        msg_lines.append("")

    msg_lines.append("\\nQual análise deseja continuar?")
    message = "\\n".join(msg_lines)

    # Construir lista de botões
    # macOS dialog suporta até 3 botões
    # Para todos os casos, vamos usar "choose from list" que suporta qualquer quantidade

    # Criar lista com todas as opções
    items = ["🆕 NOVA ANÁLISE"]  # Primeira opção sempre é nova análise

    for i, cp in enumerate(checkpoints, 1):
        completed, total = cp.progress
        percentage = cp.percentage
        resume = cp.get_resume_point()

        item_text = f"♻️  Checkpoint #{i}: {cp.screenplay_name}"
        item_text += f" ({completed}/{total} - {percentage:.0f}%)"
        if resume:
            item_text += f" → {resume[0]}×{resume[1]}"

        items.append(item_text)

    items_str = '", "'.join(items)

    prompt_text = f"{len(checkpoints)} análise(s) incompleta(s) encontrada(s).\\n\\n"
    prompt_text += "Escolha uma opção:"

    script = f'''
    tell application "System Events"
        activate
        set selectedItem to choose from list {{"{items_str}"}} with prompt "{prompt_text}" default items {{"{items[0]}"}} OK button name "OK" cancel button name "Cancelar"
        return selectedItem
    end tell
    '''
    result = subprocess.run(['osascript', '-e', script], capture_output=True, text=True)

    # Se cancelou (Esc ou botão Cancelar)
    if result.returncode != 0 or result.stdout.strip() == "false":
        print("❌ Cancelado pelo usuário")
        import sys
        sys.exit(0)

    # Parse qual foi selecionado
    selected_text = result.stdout.strip()

    # Se escolheu "Nova Análise"
    if "NOVA ANÁLISE" in selected_text:
        print("✅ Iniciando NOVA análise")
        return None

    # Se escolheu um checkpoint, encontrar qual
    for i, item in enumerate(items[1:], 0):  # Skip first item (Nova Análise)
        if item in selected_text:
            selected = checkpoints[i]
            print(f"\\n✅ Continuando: {selected.folder.name}")
            resume_point = selected.get_resume_point()
            if resume_point:
                spec, auth = resume_point
                print(f"   📍 Retomando em: {spec.capitalize()} × {auth.upper()}\\n")
            return selected

    # Fallback (não deveria chegar aqui)
    print("❌ Seleção inválida")
    return None


def prompt_user_for_checkpoint() -> Optional[CheckpointInfo]:
    """
    Versão com TECLADO (texto no terminal).
    Pergunta ao usuário se quer continuar análise anterior.
    Lista checkpoints disponíveis e permite escolha.

    Returns:
        CheckpointInfo selecionado ou None se começar nova análise
    """
    # Buscar checkpoints incompletos
    checkpoints = find_incomplete_checkpoints()

    if not checkpoints:
        print("✅ Nenhuma análise incompleta encontrada.")
        print("   Iniciando nova análise...\n")
        return None

    # Perguntar se quer continuar
    print("\n♻️  ANÁLISES INCOMPLETAS ENCONTRADAS\n")
    print(f"Encontradas {len(checkpoints)} análise(s) incompleta(s):\n")

    # Listar checkpoints
    for i, checkpoint in enumerate(checkpoints, 1):
        print(f"{i}. {checkpoint}")
        print()

    # Menu
    print("Opções:")
    print("  [1-N] - Continuar análise específica")
    print("  [0]   - Começar NOVA análise")
    print("  [Q]   - Cancelar/Sair")
    print()

    while True:
        choice = input("Escolha [0-{}, Q]: ".format(len(checkpoints))).strip().upper()

        if choice == 'Q':
            print("❌ Cancelado pelo usuário")
            return None

        if choice == '0':
            print("✅ Iniciando NOVA análise")
            return None

        try:
            idx = int(choice) - 1
            if 0 <= idx < len(checkpoints):
                selected = checkpoints[idx]
                print(f"\n✅ Continuando: {selected.folder.name}")
                resume_point = selected.get_resume_point()
                if resume_point:
                    spec, auth = resume_point
                    print(f"   📍 Retomando em: {spec.capitalize()} × {auth.upper()}\n")
                return selected
            else:
                print(f"❌ Número inválido. Escolha entre 1 e {len(checkpoints)}")
        except ValueError:
            print("❌ Entrada inválida. Digite um número ou 'Q'")


def prompt_user_simple() -> bool:
    """
    Versão simplificada: apenas pergunta sim/não para continuar.

    Returns:
        True se deve procurar checkpoint automaticamente
    """
    checkpoints = find_incomplete_checkpoints()

    if not checkpoints:
        return False

    print(f"\n♻️  Encontradas {len(checkpoints)} análise(s) incompleta(s)")

    while True:
        response = input("Deseja continuar uma análise anterior? [S/n]: ").strip().upper()

        if response in ['', 'S', 'SIM', 'Y', 'YES']:
            return True
        elif response in ['N', 'NAO', 'NÃO', 'NO']:
            print("✅ Iniciando nova análise\n")
            return False
        else:
            print("❌ Responda 'S' para sim ou 'N' para não")


# ============================================================================
# TESTE
# ============================================================================

if __name__ == "__main__":
    print("🧪 Testando sistema de checkpoint\n")

    # Buscar checkpoints
    checkpoints = find_incomplete_checkpoints()

    if not checkpoints:
        print("✅ Nenhuma análise incompleta encontrada")
    else:
        print(f"📋 Encontradas {len(checkpoints)} análise(s) incompleta(s):\n")
        for i, cp in enumerate(checkpoints, 1):
            print(f"{i}. {cp}")
            resume = cp.get_resume_point()
            if resume:
                print(f"   → Próximo: {resume[0]} × {resume[1]}")
            print()

    # Test prompt with BUTTONS
    print("\n" + "="*60)
    print("Teste do prompt com BOTÕES (macOS dialog):")
    print("="*60 + "\n")

    selected = prompt_user_with_buttons()
    if selected:
        print(f"\n✅ Checkpoint selecionado: {selected.folder.name}")
        print(f"   Pasta: {selected.folder}")
        print(f"   Progresso: {selected.progress[0]}/{selected.progress[1]}")
    else:
        print("\n✅ Nova análise será iniciada")
