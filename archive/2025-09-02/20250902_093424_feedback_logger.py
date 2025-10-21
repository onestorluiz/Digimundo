#!/usr/bin/env python3
"""
📝 FEEDBACK LOGGER - Sistema de Registro de Análises Criativas
Registra automaticamente todos os feedbacks do Scripturemon em diário de bordo
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional

class FeedbackLogger:
    """Sistema de logging de feedbacks artísticos"""
    
    def __init__(self):
        self.base_dir = Path("/Users/clubproducoes/Digimundo/desenvolvimentos_artisticos")
        self.base_dir.mkdir(parents=True, exist_ok=True)
        
    def log_feedback(self, obra: str, feedback: str, nota: int = 62, 
                     comparacoes: Optional[Dict] = None, 
                     tarefas: Optional[list] = None) -> Path:
        """
        Registra feedback no diário de bordo da obra
        
        Args:
            obra: Nome da obra analisada
            feedback: Texto do feedback
            nota: Nota atribuída (default: 62)
            comparacoes: Comparações com mestres
            tarefas: Lista de tarefas recomendadas
            
        Returns:
            Caminho do arquivo atualizado
        """
        # Sanitiza nome da obra para nome de arquivo
        obra_filename = obra.replace(" ", "_").replace("/", "_")
        log_file = self.base_dir / f"trabalho_criativo_{obra_filename}_Scripturemon.md"
        
        # Timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Prepara entrada do diário
        entry = f"\n---\n\n## 📅 {timestamp}\n\n"
        entry += f"### 🎬 ANÁLISE SCRIPTUREMON\n\n"
        entry += f"#### NOTA: {nota}/100\n\n"
        
        # Adiciona feedback principal
        entry += f"#### 💬 FEEDBACK:\n{feedback}\n\n"
        
        # Adiciona comparações se houver
        if comparacoes:
            entry += "#### 🎭 COMPARAÇÕES COM MESTRES:\n"
            for filme, comparacao in comparacoes.items():
                entry += f"- **{filme}:** {comparacao}\n"
            entry += "\n"
        
        # Adiciona tarefas se houver
        if tarefas:
            entry += "#### 🎯 TAREFAS RECOMENDADAS:\n"
            for tarefa in tarefas:
                entry += f"- [ ] {tarefa}\n"
            entry += "\n"
        
        # Se arquivo não existe, cria com cabeçalho
        if not log_file.exists():
            header = f"# 📚 DIÁRIO DE BORDO CRIATIVO\n"
            header += f"## Obra: {obra}\n"
            header += f"### Sistema de Análise: Scripturemon\n"
            header += f"\n---\n"
            
            with open(log_file, 'w', encoding='utf-8') as f:
                f.write(header)
        
        # Adiciona entrada ao arquivo
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(entry)
        
        print(f"✅ Feedback registrado em: {log_file.name}")
        return log_file
    
    def get_obra_history(self, obra: str) -> str:
        """
        Retorna histórico completo de feedbacks de uma obra
        
        Args:
            obra: Nome da obra
            
        Returns:
            Conteúdo do diário de bordo
        """
        obra_filename = obra.replace(" ", "_").replace("/", "_")
        log_file = self.base_dir / f"trabalho_criativo_{obra_filename}_Scripturemon.md"
        
        if log_file.exists():
            with open(log_file, 'r', encoding='utf-8') as f:
                return f.read()
        else:
            return f"Nenhum feedback registrado para '{obra}' ainda."
    
    def list_obras(self) -> list:
        """
        Lista todas as obras com feedbacks registrados
        
        Returns:
            Lista de nomes de obras
        """
        obras = []
        for file in self.base_dir.glob("trabalho_criativo_*_Scripturemon.md"):
            # Extrai nome da obra do filename
            obra = file.stem.replace("trabalho_criativo_", "").replace("_Scripturemon", "")
            obra = obra.replace("_", " ")
            obras.append(obra)
        
        return obras
    
    def get_stats(self, obra: str) -> Dict:
        """
        Retorna estatísticas dos feedbacks de uma obra
        
        Args:
            obra: Nome da obra
            
        Returns:
            Dicionário com estatísticas
        """
        history = self.get_obra_history(obra)
        
        if "Nenhum feedback" in history:
            return {"total_analises": 0}
        
        # Conta número de análises
        analises = history.count("## 📅")
        
        # Extrai todas as notas
        import re
        notas = re.findall(r"NOTA: (\d+)/100", history)
        notas = [int(n) for n in notas]
        
        stats = {
            "total_analises": analises,
            "notas": notas,
            "media_notas": sum(notas) / len(notas) if notas else 0,
            "evolucao": "estável" if all(n == 62 for n in notas) else "variável"
        }
        
        return stats


# Função helper para integração fácil
def registrar_feedback(obra: str, feedback: str, **kwargs):
    """
    Função simplificada para registrar feedback
    
    Args:
        obra: Nome da obra
        feedback: Texto do feedback
        **kwargs: Argumentos adicionais (nota, comparacoes, tarefas)
    """
    logger = FeedbackLogger()
    return logger.log_feedback(obra, feedback, **kwargs)


if __name__ == "__main__":
    # Teste do sistema
    logger = FeedbackLogger()
    
    print("="*60)
    print("📝 TESTE DO FEEDBACK LOGGER")
    print("="*60)
    
    # Registra um feedback de teste
    logger.log_feedback(
        obra="Teste Script",
        feedback="Este é um feedback de teste do sistema.",
        nota=62,
        comparacoes={
            "Citizen Kane": "Falta profundidade",
            "Chinatown": "Diálogos fracos"
        },
        tarefas=[
            "Reescrever primeiro ato",
            "Adicionar subtexto aos diálogos"
        ]
    )
    
    # Lista obras
    print("\n📚 Obras registradas:")
    for obra in logger.list_obras():
        print(f"  • {obra}")
        stats = logger.get_stats(obra)
        print(f"    Total de análises: {stats['total_analises']}")
    
    print("\n✅ Sistema de logging configurado com sucesso!")