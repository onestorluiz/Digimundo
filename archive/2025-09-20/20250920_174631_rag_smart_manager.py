#!/usr/bin/env python3
"""
🧠 RAG SMART MANAGER - Sistema Inteligente de Ativação do RAG
Ativa automaticamente quando detecta trabalho com roteiros
"""

import re
import time
import threading
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
from pathlib import Path
import json

class RAGSmartManager:
    """Gerenciador inteligente do sistema RAG"""

    def __init__(self):
        self.rag_instance = None
        self.is_active = False
        self.last_activity = None
        self.activation_history = []
        self.current_context = "general"

        # Timeout de inatividade (10 minutos)
        self.inactivity_timeout = 600

        # Thread de monitoramento
        self.monitor_thread = None
        self.monitoring = False

        # Cache de configuração
        self.config_file = Path("data/rag_smart_config.json")
        self.load_config()

    def load_config(self):
        """Carrega configuração persistente"""
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                config = json.load(f)
                self.inactivity_timeout = config.get('timeout', 600)

    def analyze_context(self, text: str) -> str:
        """
        Analisa o contexto da conversa para determinar se deve ativar RAG

        Returns:
            'screenplay' - Trabalho com roteiros (ATIVA RAG)
            'technical' - Comandos técnicos (DESATIVA RAG)
            'general' - Conversa geral (MANTÉM ESTADO ATUAL)
        """
        text_lower = text.lower()

        # TRIGGERS PARA ATIVAR RAG - Qualquer menção a roteiro
        screenplay_triggers = [
            # Palavras diretas
            'roteiro', 'screenplay', 'script', 'filme', 'movie', 'film',
            'cena', 'scene', 'ato', 'act', 'sequência', 'sequence',

            # Elementos narrativos
            'personagem', 'character', 'protagonista', 'protagonist',
            'antagonista', 'antagonist', 'vilão', 'villain', 'herói', 'hero',
            'diálogo', 'dialogue', 'dialog', 'fala', 'speech',
            'narrativa', 'narrative', 'história', 'story', 'plot', 'enredo',

            # Estrutura
            'fade in', 'fade out', 'cut to', 'int.', 'ext.',
            'flashback', 'montage', 'voice over', 'v.o.', 'o.s.',

            # Desenvolvimento
            'arco', 'arc', 'desenvolvimento', 'development',
            'motivação', 'motivation', 'conflito', 'conflict',
            'clímax', 'climax', 'resolução', 'resolution',

            # Perguntas sobre conteúdo
            'quem é', 'who is', 'o que acontece', 'what happens',
            'por que', 'why', 'quando', 'when', 'onde', 'where',
            'qual cena', 'which scene', 'em que momento', 'at what point',

            # Análise
            'analisar', 'analyze', 'análise', 'analysis',
            'estrutura', 'structure', 'tema', 'theme',
            'gênero', 'genre', 'tom', 'tone'
        ]

        # TRIGGERS PARA DESATIVAR RAG - Comandos técnicos
        technical_triggers = [
            'compress', 'comprimir', 'compact',
            'convert', 'converter', 'export',
            'status', 'system', 'sistema',
            'config', 'configuração', 'settings',
            'install', 'instalar', 'update', 'atualizar',
            'backup', 'restore', 'delete', 'deletar',
            'mkdir', 'cd', 'ls', 'pwd', 'chmod',
            'git', 'commit', 'push', 'pull',
            'debug', 'log', 'error', 'erro',
            'memory', 'memória', 'cpu', 'ram',
            'start', 'stop', 'restart', 'iniciar', 'parar'
        ]

        # Verificar contexto de roteiro primeiro (prioridade)
        for trigger in screenplay_triggers:
            if trigger in text_lower:
                return 'screenplay'

        # Verificar contexto técnico
        for trigger in technical_triggers:
            if trigger in text_lower:
                return 'technical'

        # Padrões especiais com regex
        screenplay_patterns = [
            r'\b(fade\s+(in|out))\b',
            r'\b(int\.|ext\.)\s+\w+',
            r'\b\w+\s*\([^)]*\)\s*\n',  # Nome (descrição) - formato de personagem
            r'cena\s+\d+',
            r'página\s+\d+',
            r'ato\s+(i|ii|iii|1|2|3)'
        ]

        for pattern in screenplay_patterns:
            if re.search(pattern, text_lower):
                return 'screenplay'

        return 'general'

    def should_activate(self, text: str) -> bool:
        """Determina se deve ativar o RAG baseado no contexto"""
        context = self.analyze_context(text)

        if context == 'screenplay':
            self.current_context = 'screenplay'
            return True
        elif context == 'technical':
            self.current_context = 'technical'
            return False
        else:
            # Mantém estado atual se contexto é geral
            return self.current_context == 'screenplay'

    def activate_rag(self) -> bool:
        """Ativa o sistema RAG"""
        if self.is_active:
            self.last_activity = datetime.now()
            return True

        try:
            print("🔮 [RAG] Detectado contexto de roteiro - ativando sistema...")

            # Importar e inicializar RAG
            from apps.scripturemon.rag_system import RAGSystem
            self.rag_instance = RAGSystem()

            # Pré-carregar roteiros existentes (async)
            self._preload_screenplays()

            self.is_active = True
            self.last_activity = datetime.now()

            # Registrar ativação
            self.activation_history.append({
                'activated_at': datetime.now().isoformat(),
                'context': self.current_context
            })

            # Iniciar monitoramento de inatividade
            if not self.monitoring:
                self._start_monitoring()

            print("✅ [RAG] Sistema ativado e pronto para consultas sobre roteiros")
            return True

        except Exception as e:
            print(f"❌ [RAG] Erro ao ativar: {e}")
            return False

    def deactivate_rag(self, reason: str = "manual"):
        """Desativa o sistema RAG"""
        if not self.is_active:
            return

        print(f"🔌 [RAG] Desativando sistema ({reason})...")

        self.rag_instance = None
        self.is_active = False
        self.current_context = "general"

        # Registrar desativação
        if self.activation_history:
            self.activation_history[-1]['deactivated_at'] = datetime.now().isoformat()
            self.activation_history[-1]['deactivation_reason'] = reason

        print("💤 [RAG] Sistema desativado - recursos liberados")

    def _preload_screenplays(self):
        """Pré-carrega roteiros em background"""
        def load_worker():
            try:
                screenplay_dir = Path("library/processed")
                if not screenplay_dir.exists():
                    return

                loaded = 0
                for script_file in screenplay_dir.glob("*.txt")[:10]:  # Primeiros 10
                    try:
                        with open(script_file, 'r', encoding='utf-8') as f:
                            content = f.read()
                        self.rag_instance.index_screenplay(script_file.stem, content)
                        loaded += 1
                    except:
                        pass

                if loaded > 0:
                    print(f"📚 [RAG] {loaded} roteiros pré-indexados")

            except Exception as e:
                print(f"⚠️ [RAG] Erro no pré-carregamento: {e}")

        # Executar em thread separada
        thread = threading.Thread(target=load_worker, daemon=True)
        thread.start()

    def _start_monitoring(self):
        """Inicia monitoramento de inatividade"""
        def monitor_worker():
            self.monitoring = True
            while self.is_active:
                time.sleep(60)  # Verificar a cada minuto

                if self.last_activity:
                    inactive_time = (datetime.now() - self.last_activity).total_seconds()

                    if inactive_time > self.inactivity_timeout:
                        self.deactivate_rag("inactivity")
                        break

            self.monitoring = False

        self.monitor_thread = threading.Thread(target=monitor_worker, daemon=True)
        self.monitor_thread.start()

    def process_input(self, text: str) -> Dict[str, Any]:
        """
        Processa input e gerencia RAG automaticamente

        Returns:
            Dict com status e informações do RAG
        """
        # Analisar se deve ativar/desativar
        should_be_active = self.should_activate(text)

        result = {
            'text': text,
            'context': self.current_context,
            'rag_was_active': self.is_active,
            'rag_is_active': False,
            'rag_activated': False,
            'rag_deactivated': False
        }

        # Gerenciar estado do RAG
        if should_be_active and not self.is_active:
            # Ativar RAG
            if self.activate_rag():
                result['rag_activated'] = True
                result['rag_is_active'] = True

        elif not should_be_active and self.is_active and self.current_context == 'technical':
            # Desativar RAG apenas se contexto mudou para técnico
            self.deactivate_rag("context_change")
            result['rag_deactivated'] = True

        elif self.is_active:
            # RAG já ativo, atualizar última atividade
            self.last_activity = datetime.now()
            result['rag_is_active'] = True

        # Adicionar instância RAG se ativa
        if self.is_active and self.rag_instance:
            result['rag'] = self.rag_instance

        return result

    def get_status(self) -> Dict[str, Any]:
        """Retorna status atual do sistema"""
        return {
            'active': self.is_active,
            'context': self.current_context,
            'last_activity': self.last_activity.isoformat() if self.last_activity else None,
            'timeout_seconds': self.inactivity_timeout,
            'activation_count': len(self.activation_history),
            'monitoring': self.monitoring
        }


# Singleton global
_smart_manager = None

def get_smart_manager() -> RAGSmartManager:
    """Retorna instância única do Smart Manager"""
    global _smart_manager
    if _smart_manager is None:
        _smart_manager = RAGSmartManager()
    return _smart_manager


# Funções de conveniência
def process_with_smart_rag(text: str) -> Dict[str, Any]:
    """Processa texto com RAG inteligente"""
    manager = get_smart_manager()
    return manager.process_input(text)


def rag_status() -> Dict[str, Any]:
    """Retorna status do RAG"""
    manager = get_smart_manager()
    return manager.get_status()


if __name__ == "__main__":
    print("🧠 TESTE DO RAG SMART MANAGER")
    print("=" * 60)

    manager = RAGSmartManager()

    # Testes de contexto
    test_inputs = [
        "Como comprimir um arquivo?",  # Técnico - RAG desliga
        "Quem é o protagonista do filme?",  # Roteiro - RAG liga
        "Analisar a estrutura do roteiro",  # Roteiro - RAG mantém
        "Qual o tema principal da história?",  # Roteiro - RAG mantém
        "Fazer backup do sistema",  # Técnico - RAG desliga
        "Em qual cena aparece o vilão?",  # Roteiro - RAG liga
        "Verificar status",  # Técnico - RAG desliga
        "O diálogo está bom?",  # Roteiro - RAG liga
    ]

    print("\n📝 Testando detecção de contexto:\n")
    for text in test_inputs:
        result = manager.process_input(text)

        status = "🟢 RAG ATIVO" if result['rag_is_active'] else "🔴 RAG INATIVO"
        action = ""
        if result['rag_activated']:
            action = " (ATIVADO AGORA)"
        elif result['rag_deactivated']:
            action = " (DESATIVADO AGORA)"

        print(f"'{text[:40]}...'")
        print(f"  Contexto: {result['context']} | {status}{action}")
        print()

    # Status final
    print("\n📊 Status Final:")
    status = manager.get_status()
    for key, value in status.items():
        print(f"  {key}: {value}")

    print("\n✅ Smart Manager funcionando!")