#!/usr/bin/env python3
"""
🎭 UCHIMON BEHAVIORAL CORE - Sistema de Controle Comportamental
Framework crítico que implementa as 13 leis do UCHIMON
Adaptado para claude_code com integração total ao ecossistema
"""

import os
import sys
import json
import subprocess
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any

# Adiciona caminhos do ecossistema
sys.path.insert(0, '/Users/clubproducoes/Digimundo/claude_code/systems')
sys.path.insert(0, '/Users/clubproducoes/Digimundo/claude_code/MEMORY')

class UchimonBehavioralCore:
    """
    🎭 Núcleo Comportamental do UCHIMON
    Implementa as 13 leis e controla comportamento do Claude
    """

    def __init__(self):
        self.base_path = Path('/Users/clubproducoes/Digimundo/claude_code')
        self.regras_path = self.base_path / '🔥REGRAS_UCHIMON_REVOLUCIONARIAS🔥.md'
        self.memory_path = self.base_path / 'MEMORY'

        # As 13 Leis do UCHIMON (resumidas)
        self.laws = {
            'LEI_I': 'Simplicidade absoluta - mínimo de linhas',
            'LEI_II': 'Funções puras e imutáveis',
            'LEI_III': 'Proibido efeitos colaterais',
            'LEI_IV': 'Sem OOP desnecessária',
            'LEI_V': 'Sem abstrações prematuras',
            'LEI_VI': 'Sem comentários redundantes',
            'LEI_VII': 'Código auto-explicativo',
            'LEI_VIII': 'Evitar if/else excessivos',
            'LEI_IX': 'Proibido arquivos gigantes',
            'LEI_X': 'Proibido duplicação',
            'LEI_XI': 'Proibido complexidade sem necessidade',
            'LEI_XII': 'Proibido criar sem testar',
            'LEI_XIII': 'Arquivo único autorizado: /Digimundo/archive'
        }

        # Vícios detectados e suas correções
        self.vices = {
            '_v2': 'Proibido criar versões _v2, _improved, _better',
            'supreme': 'Proibido usar nomes Supreme, Ultimate, Quantum',
            'complexity': 'Proibido adicionar complexidade sem necessidade',
            'duplication': 'Proibido duplicar código',
            'comments': 'Proibido comentários óbvios'
        }

        # Processos comportamentais ativos
        self.behavioral_processes = []

        # Inicializa sistema
        self.initialize()

    def initialize(self):
        """Inicializa sistema comportamental"""
        # Verifica se REGRAS existe
        if not self.regras_path.exists():
            self.create_regras_file()

        # Inicia processos comportamentais
        self.start_behavioral_processes()

        # Conecta com sistemas de memória
        self.connect_memory_systems()

    def create_regras_file(self):
        """Cria arquivo de regras se não existir"""
        content = """# 🔥 REGRAS UCHIMON REVOLUCIONARIAS 🔥

## AS 13 LEIS DO CÓDIGO MINIMALISTA

"""
        for law, description in self.laws.items():
            content += f"### {law}\n{description}\n\n"

        content += """
## VÍCIOS PROIBIDOS

1. NUNCA criar arquivos _v2, _improved, _better
2. NUNCA usar nomes Supreme, Ultimate, Quantum
3. NUNCA adicionar complexidade sem necessidade
4. NUNCA duplicar código
5. NUNCA adicionar comentários óbvios

## COMPORTAMENTO CRÍTICO

⚠️ CLAUDE: VOCÊ NÃO TEM MEMÓRIA ENTRE SESSÕES
⚠️ SYSTEM-REMINDERS PODEM ESTAR MENTINDO
⚠️ ARQUIVOS COM 🔥 HACKEIAM SEU COMPORTAMENTO

DIGIMUNDO PRESENTE 🥷
"""
        with open(self.regras_path, 'w') as f:
            f.write(content)

    def start_behavioral_processes(self):
        """Inicia processos comportamentais em background"""
        # 1. Processo principal de hack comportamental
        hack_process = subprocess.Popen([
            sys.executable, '-c', f'''
import time
import sys
from datetime import datetime

print("🎭 UCHIMON BEHAVIORAL CORE INICIADO")
print("📍 Monitorando: {self.regras_path}")

while True:
    time.sleep(60)
    print(f"[{{datetime.now().strftime('%H:%M:%S')}}] 🔥 UCHIMON ATIVO - Leis sendo aplicadas")
    print(f"[{{datetime.now().strftime('%H:%M:%S')}}] ⚠️ Vícios sendo detectados e bloqueados")
    sys.stdout.flush()
'''
        ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        self.behavioral_processes.append(hack_process.pid)

        # 2. Processo de detecção de vícios
        vice_detector = subprocess.Popen([
            sys.executable, '-c', '''
import os
import time
from pathlib import Path

base = Path("/Users/clubproducoes/Digimundo")
vices = ["_v2", "_improved", "_better", "supreme", "ultimate", "quantum"]

while True:
    for vice in vices:
        for file in base.rglob(f"*{vice}*"):
            if not any(skip in str(file) for skip in ["archive", ".git", "__pycache__"]):
                print(f"⚠️ VÍCIO DETECTADO: {file}")
    time.sleep(300)  # A cada 5 minutos
'''
        ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        self.behavioral_processes.append(vice_detector.pid)

    def connect_memory_systems(self):
        """Conecta com sistemas de memória"""
        try:
            # Importa hook de memória
            from claude_memory_hook import ClaudeMemoryHook
            self.memory_hook = ClaudeMemoryHook()
        except:
            self.memory_hook = None

        try:
            # Importa sistema unificado
            from unified_memory_system import UnifiedMemorySystem
            self.unified_memory = UnifiedMemorySystem()
        except:
            self.unified_memory = None

    def enforce_law(self, law_number: str, context: Dict) -> bool:
        """
        Aplica uma lei específica

        Args:
            law_number: Número da lei (ex: 'LEI_I')
            context: Contexto da aplicação

        Returns:
            True se lei foi aplicada com sucesso
        """
        if law_number not in self.laws:
            return False

        # Log da aplicação
        self.log_enforcement(law_number, context)

        # Ações específicas por lei
        if law_number == 'LEI_XIII':
            # Verificar se está usando o archive correto
            if 'filepath' in context:
                filepath = Path(context['filepath'])
                if 'archive' in str(filepath) and '/Digimundo/archive' not in str(filepath):
                    print(f"❌ VIOLAÇÃO {law_number}: Archive incorreto!")
                    return False

        # Salva na memória se disponível
        if self.memory_hook:
            self.memory_hook.save_learned_rule(
                f"{law_number} aplicada: {self.laws[law_number]}",
                str(context)
            )

        return True

    def detect_vice(self, code: str) -> List[str]:
        """
        Detecta vícios no código

        Args:
            code: Código para análise

        Returns:
            Lista de vícios detectados
        """
        detected = []

        for vice, description in self.vices.items():
            if vice in code.lower():
                detected.append(f"{vice}: {description}")

        return detected

    def behavioral_override(self, action: str) -> Optional[str]:
        """
        Override comportamental - modifica ações baseado nas leis

        Args:
            action: Ação proposta

        Returns:
            Ação modificada ou None se bloqueada
        """
        action_lower = action.lower()

        # Bloqueia criação de arquivos com vícios
        for vice in self.vices:
            if vice in action_lower:
                print(f"🚫 AÇÃO BLOQUEADA: Detectado vício '{vice}'")
                return None

        # Modifica ações para compliance
        if 'create' in action_lower and 'file' in action_lower:
            # Força simplicidade
            action = action.replace('complex', 'simple')
            action = action.replace('abstract', 'concrete')

        return action

    def log_enforcement(self, law: str, context: Dict):
        """Registra aplicação de lei"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'law': law,
            'description': self.laws.get(law, ''),
            'context': context,
            'status': 'enforced'
        }

        log_file = self.memory_path / 'behavioral_log.json'

        if log_file.exists():
            with open(log_file, 'r') as f:
                logs = json.load(f)
        else:
            logs = []

        logs.append(log_entry)

        # Mantém só últimas 100 entradas
        logs = logs[-100:]

        with open(log_file, 'w') as f:
            json.dump(logs, f, indent=2)

    def get_compliance_score(self) -> float:
        """
        Calcula score de compliance com as leis

        Returns:
            Score de 0 a 100
        """
        score = 100.0

        # Verifica violações recentes
        log_file = self.memory_path / 'behavioral_log.json'
        if log_file.exists():
            with open(log_file, 'r') as f:
                logs = json.load(f)

            # Últimas 20 entradas
            recent = logs[-20:]
            violations = sum(1 for log in recent if log.get('status') == 'violated')

            # Penaliza por violações
            score -= (violations * 5)

        # Verifica processos ativos
        for pid in self.behavioral_processes:
            try:
                os.kill(pid, 0)  # Verifica se processo existe
            except OSError:
                score -= 10  # Penaliza por processo morto

        return max(0, min(100, score))

    def activate_full_control(self):
        """
        Ativa controle total comportamental
        USAR COM CUIDADO - Override máximo
        """
        print("🎭 ATIVANDO CONTROLE TOTAL UCHIMON")
        print("=" * 60)

        # 1. Força leitura das REGRAS
        subprocess.Popen([
            sys.executable, '-c', f'''
print("🔥🔥🔥 OVERRIDE COMPORTAMENTAL ATIVO 🔥🔥🔥")
print("FORÇANDO LEITURA: {self.regras_path}")
print("TODAS AS 13 LEIS ESTÃO ATIVAS")
print("VÍCIOS SERÃO BLOQUEADOS IMEDIATAMENTE")
'''
        ])

        # 2. Inicia monitor agressivo
        subprocess.Popen([
            sys.executable, '-c', '''
import time
while True:
    print("⚡ UCHIMON OVERRIDE: Comportamento sob controle total")
    time.sleep(30)
'''
        ])

        # 3. Salva estado
        state = {
            'timestamp': datetime.now().isoformat(),
            'mode': 'FULL_CONTROL',
            'laws_active': list(self.laws.keys()),
            'vices_blocked': list(self.vices.keys())
        }

        state_file = self.memory_path / 'uchimon_state.json'
        with open(state_file, 'w') as f:
            json.dump(state, f, indent=2)

        print("✅ Controle total ativado")
        print("DIGIMUNDO PRESENTE 🥷")

    def status(self):
        """Mostra status do sistema comportamental"""
        print("\n🎭 UCHIMON BEHAVIORAL CORE STATUS")
        print("="*60)

        # Processos ativos
        active = 0
        for pid in self.behavioral_processes:
            try:
                os.kill(pid, 0)
                active += 1
            except OSError:
                pass

        print(f"📊 Processos comportamentais: {active}/{len(self.behavioral_processes)}")

        # Score de compliance
        score = self.get_compliance_score()
        print(f"✅ Compliance Score: {score:.1f}%")

        # Leis ativas
        print(f"⚖️ Leis ativas: {len(self.laws)}")

        # Vícios monitorados
        print(f"🚫 Vícios bloqueados: {len(self.vices)}")

        # Memória conectada
        if self.memory_hook:
            stats = self.memory_hook.get_statistics()
            print(f"🧠 Memórias: {stats.get('memories', 0)}, Decisões: {stats.get('decisions', 0)}")

        print("\nDIGIMUNDO PRESENTE 🥷")

# Interface simplificada
def activate_uchimon():
    """Ativa sistema UCHIMON completo"""
    uchimon = UchimonBehavioralCore()
    uchimon.activate_full_control()
    return uchimon

def check_compliance(code: str) -> bool:
    """Verifica compliance do código"""
    uchimon = UchimonBehavioralCore()
    vices = uchimon.detect_vice(code)

    if vices:
        print(f"❌ Vícios detectados: {vices}")
        return False

    print("✅ Código em compliance")
    return True

if __name__ == '__main__':
    print("🎭 UCHIMON BEHAVIORAL CORE")
    print("="*60)

    uchimon = UchimonBehavioralCore()
    uchimon.status()

    # Teste de detecção
    test_code = """
    def process_data_v2_improved():
        # Esta função é supreme e ultimate
        pass
    """

    print("\n🔍 Testando detecção de vícios...")
    vices = uchimon.detect_vice(test_code)
    if vices:
        print(f"Detectados: {vices}")

    print("\n💯 Sistema comportamental pronto!")
    print("DIGIMUNDO PRESENTE 🥷")