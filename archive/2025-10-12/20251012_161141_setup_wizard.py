#!/usr/bin/env python3
"""
Wizard de Setup do Scripturemon

Assistente interativo para configurar o Scripturemon:
- Verificação de dependências
- Configuração de modelo LLM (Ollama vs GPT)
- Escolha de specialists padrão
- Configuração de workspace
- Teste de configuração

Uso:
    python setup_wizard.py                  # Wizard interativo completo
    python setup_wizard.py --quick          # Setup rápido
    python setup_wizard.py --check-only     # Apenas verificar ambiente
"""

import sys
import subprocess
import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import argparse


class SetupWizard:
    """Assistente de configuração do Scripturemon"""

    def __init__(self):
        self.config_file = Path('workspace/config/scripturemon.json')
        self.config = self._load_config()

    def _load_config(self) -> Dict:
        """Carrega configuração existente"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except:
                pass

        return {
            'version': '1.0',
            'llm': {
                'provider': 'ollama',
                'model': 'scripturemon-optimized',
                'api_key': None
            },
            'specialists': {
                'enabled': ['character', 'structure', 'theme', 'dialogue', 'pacing'],
                'default_authors': ['mckee', 'field', 'truby', 'campbell']
            },
            'workspace': {
                'outputs_dir': 'workspace/outputs',
                'temp_dir': 'workspace/temp',
                'logs_dir': 'workspace/logs'
            },
            'notifications': {
                'enabled': True,
                'sound_enabled': True
            },
            'performance': {
                'parallel_analyses': 1,
                'max_retries': 3,
                'timeout_seconds': 300
            }
        }

    def _save_config(self):
        """Salva configuração"""
        self.config_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)

    def check_dependencies(self) -> Dict[str, bool]:
        """Verifica dependências instaladas"""
        checks = {}

        # Python
        checks['python'] = True  # Se está rodando, Python existe

        # Ollama
        try:
            result = subprocess.run(['ollama', 'list'], capture_output=True, timeout=5)
            checks['ollama'] = result.returncode == 0
        except:
            checks['ollama'] = False

        # PDF reader (pdfplumber ou PyPDF2)
        try:
            import pdfplumber
            checks['pdf_reader'] = True
        except ImportError:
            try:
                import PyPDF2
                checks['pdf_reader'] = True
            except ImportError:
                checks['pdf_reader'] = False

        # Rich (para interface bonita)
        try:
            import rich
            checks['rich'] = True
        except ImportError:
            checks['rich'] = False

        return checks

    def check_ollama_models(self) -> List[str]:
        """Verifica modelos Ollama instalados"""
        try:
            result = subprocess.run(
                ['ollama', 'list'],
                capture_output=True,
                text=True,
                timeout=5
            )

            if result.returncode != 0:
                return []

            # Parse output
            lines = result.stdout.strip().split('\n')[1:]  # Skip header
            models = []

            for line in lines:
                if line.strip():
                    model_name = line.split()[0]
                    models.append(model_name)

            return models

        except Exception as e:
            return []

    def print_welcome(self):
        """Exibe mensagem de boas-vindas"""
        print("\n" + "=" * 80)
        print("🎬 BEM-VINDO AO SCRIPTUREMON - WIZARD DE CONFIGURAÇÃO")
        print("=" * 80)
        print()
        print("Este assistente irá ajudá-lo a configurar o Scripturemon para uso.")
        print("Vamos verificar seu ambiente e configurar as opções necessárias.")
        print()

    def step_check_environment(self) -> bool:
        """Passo 1: Verificar ambiente"""
        print("=" * 80)
        print("📋 PASSO 1: VERIFICANDO AMBIENTE")
        print("=" * 80)
        print()

        checks = self.check_dependencies()

        print("Verificando dependências:")
        print()

        all_ok = True

        for dep, status in checks.items():
            icon = "✅" if status else "❌"
            print(f"  {icon} {dep.upper()}: {'Instalado' if status else 'NÃO INSTALADO'}")

            if not status:
                all_ok = False

        print()

        if not all_ok:
            print("⚠️  ATENÇÃO: Algumas dependências estão faltando.")
            print()

            if not checks['ollama']:
                print("   📦 Ollama não encontrado. Instale em: https://ollama.ai")
                print("      Ou configure para usar GPT-4/Claude API.")
                print()

            if not checks['pdf_reader']:
                print("   📦 Biblioteca PDF não encontrada.")
                print("      Instale com: pip install pdfplumber")
                print()

            if not checks['rich']:
                print("   📦 Rich não encontrado (opcional, mas recomendado).")
                print("      Instale com: pip install rich")
                print()

            response = input("Deseja continuar mesmo assim? (s/N): ").strip().lower()
            if response != 's':
                return False

        else:
            print("✅ Todas as dependências estão instaladas!")
            print()

        return True

    def step_configure_llm(self):
        """Passo 2: Configurar modelo LLM"""
        print("=" * 80)
        print("🤖 PASSO 2: CONFIGURAR MODELO LLM")
        print("=" * 80)
        print()

        print("Escolha o provedor de LLM:")
        print("  1. Ollama (local, gratuito, requer modelo instalado)")
        print("  2. OpenAI GPT-4/GPT-5 (API paga, ~$0.11 por análise)")
        print("  3. Anthropic Claude (API paga)")
        print()

        choice = input("Escolha (1-3) [1]: ").strip() or "1"

        if choice == "1":
            # Ollama
            print()
            print("Verificando modelos Ollama instalados...")
            models = self.check_ollama_models()

            if not models:
                print("⚠️  Nenhum modelo Ollama encontrado.")
                print()
                print("Recomendamos instalar: llama3.1:70b ou qwen2.5:72b")
                print("Comando: ollama pull llama3.1:70b")
                print()

                model = input("Digite o nome do modelo a usar [scripturemon-optimized]: ").strip() or "scripturemon-optimized"
            else:
                print()
                print("Modelos disponíveis:")
                for i, model in enumerate(models, 1):
                    print(f"  {i}. {model}")
                print()

                model_choice = input(f"Escolha o modelo (1-{len(models)}) [1]: ").strip() or "1"
                try:
                    model = models[int(model_choice) - 1]
                except:
                    model = models[0]

            self.config['llm']['provider'] = 'ollama'
            self.config['llm']['model'] = model
            self.config['llm']['api_key'] = None

            print()
            print(f"✅ Configurado para usar Ollama com modelo: {model}")

        elif choice == "2":
            # OpenAI
            print()
            api_key = input("Cole sua OpenAI API Key: ").strip()

            if not api_key:
                print("❌ API Key não fornecida. Mantendo configuração anterior.")
            else:
                model = input("Modelo OpenAI [gpt-4-turbo]: ").strip() or "gpt-4-turbo"

                self.config['llm']['provider'] = 'openai'
                self.config['llm']['model'] = model
                self.config['llm']['api_key'] = api_key

                print()
                print(f"✅ Configurado para usar OpenAI {model}")
                print("💰 Custo estimado: ~$0.11 por análise specialist")

        elif choice == "3":
            # Anthropic
            print()
            api_key = input("Cole sua Anthropic API Key: ").strip()

            if not api_key:
                print("❌ API Key não fornecida. Mantendo configuração anterior.")
            else:
                model = input("Modelo Claude [claude-3-opus]: ").strip() or "claude-3-opus"

                self.config['llm']['provider'] = 'anthropic'
                self.config['llm']['model'] = model
                self.config['llm']['api_key'] = api_key

                print()
                print(f"✅ Configurado para usar Anthropic {model}")

        print()

    def step_configure_specialists(self):
        """Passo 3: Configurar specialists"""
        print("=" * 80)
        print("🔬 PASSO 3: CONFIGURAR SPECIALISTS")
        print("=" * 80)
        print()

        print("Specialists disponíveis:")
        all_specialists = [
            'character', 'structure', 'theme', 'dialogue',
            'pacing', 'genre', 'transitions'
        ]

        for i, spec in enumerate(all_specialists, 1):
            enabled = "✓" if spec in self.config['specialists']['enabled'] else " "
            print(f"  [{enabled}] {i}. Dr{spec.title()}")

        print()
        print("Configuração atual inclui: " + ", ".join(self.config['specialists']['enabled']))
        print()

        response = input("Deseja alterar os specialists ativos? (s/N): ").strip().lower()

        if response == 's':
            print()
            print("Digite os números dos specialists desejados (separados por vírgula):")
            print("Exemplo: 1,2,3,4,5")
            print()

            selection = input("Specialists: ").strip()

            if selection:
                try:
                    indices = [int(x.strip()) - 1 for x in selection.split(',')]
                    selected_specs = [all_specialists[i] for i in indices if 0 <= i < len(all_specialists)]

                    if selected_specs:
                        self.config['specialists']['enabled'] = selected_specs
                        print()
                        print(f"✅ Specialists configurados: {', '.join(selected_specs)}")
                except:
                    print("❌ Seleção inválida. Mantendo configuração anterior.")

        print()

        # Authors
        print("Authors disponíveis:")
        all_authors = [
            'mckee', 'field', 'truby', 'campbell', 'vogler',
            'seger', 'snyder', 'egri', 'weiland', 'aristotle'
        ]

        current = self.config['specialists']['default_authors']
        print(f"Configuração atual: {', '.join(current)}")
        print()

        response = input("Deseja usar todos os authors? (S/n): ").strip().lower()

        if response == 'n':
            print()
            print("Digite os authors desejados (separados por vírgula):")
            print("Exemplo: mckee,field,truby")
            print()

            selection = input("Authors: ").strip()

            if selection:
                selected_authors = [a.strip() for a in selection.split(',') if a.strip() in all_authors]

                if selected_authors:
                    self.config['specialists']['default_authors'] = selected_authors
                    print()
                    print(f"✅ Authors configurados: {', '.join(selected_authors)}")
        else:
            self.config['specialists']['default_authors'] = all_authors
            print("✅ Todos os authors serão usados")

        print()

    def step_configure_workspace(self):
        """Passo 4: Configurar workspace"""
        print("=" * 80)
        print("📁 PASSO 4: CONFIGURAR WORKSPACE")
        print("=" * 80)
        print()

        print("Diretórios de workspace:")
        print(f"  • Outputs: {self.config['workspace']['outputs_dir']}")
        print(f"  • Temp:    {self.config['workspace']['temp_dir']}")
        print(f"  • Logs:    {self.config['workspace']['logs_dir']}")
        print()

        response = input("Deseja alterar os diretórios? (s/N): ").strip().lower()

        if response == 's':
            outputs = input(f"Diretório de outputs [{self.config['workspace']['outputs_dir']}]: ").strip()
            if outputs:
                self.config['workspace']['outputs_dir'] = outputs

            temp = input(f"Diretório temp [{self.config['workspace']['temp_dir']}]: ").strip()
            if temp:
                self.config['workspace']['temp_dir'] = temp

            logs = input(f"Diretório de logs [{self.config['workspace']['logs_dir']}]: ").strip()
            if logs:
                self.config['workspace']['logs_dir'] = logs

            print()
            print("✅ Diretórios configurados")

        # Criar diretórios
        for dir_path in self.config['workspace'].values():
            Path(dir_path).mkdir(parents=True, exist_ok=True)

        print()

    def step_configure_notifications(self):
        """Passo 5: Configurar notificações"""
        print("=" * 80)
        print("🔔 PASSO 5: CONFIGURAR NOTIFICAÇÕES")
        print("=" * 80)
        print()

        print("O Scripturemon pode enviar notificações nativas do macOS.")
        print()

        enabled = input("Ativar notificações? (S/n): ").strip().lower() != 'n'
        self.config['notifications']['enabled'] = enabled

        if enabled:
            sound = input("Ativar som nas notificações? (S/n): ").strip().lower() != 'n'
            self.config['notifications']['sound_enabled'] = sound

            print()
            print(f"✅ Notificações ativadas{' com som' if sound else ' (sem som)'}")
        else:
            print()
            print("✅ Notificações desativadas")

        print()

    def step_save_config(self):
        """Passo final: Salvar configuração"""
        print("=" * 80)
        print("💾 SALVANDO CONFIGURAÇÃO")
        print("=" * 80)
        print()

        self._save_config()

        print(f"✅ Configuração salva em: {self.config_file}")
        print()

    def step_test_config(self):
        """Teste opcional da configuração"""
        print("=" * 80)
        print("🧪 TESTE DE CONFIGURAÇÃO")
        print("=" * 80)
        print()

        response = input("Deseja testar a configuração? (s/N): ").strip().lower()

        if response != 's':
            return

        print()
        print("Testando conexão com LLM...")

        if self.config['llm']['provider'] == 'ollama':
            try:
                result = subprocess.run(
                    ['ollama', 'list'],
                    capture_output=True,
                    timeout=5
                )

                if result.returncode == 0:
                    print("✅ Ollama está funcionando")
                else:
                    print("❌ Erro ao conectar com Ollama")
            except Exception as e:
                print(f"❌ Erro: {e}")

        else:
            print("⚠️  Teste de APIs externas não implementado ainda")
            print("   Teste manualmente rodando uma análise simples")

        print()

    def run_wizard(self, quick: bool = False):
        """Executa o wizard completo"""
        self.print_welcome()

        # Passo 1: Verificar ambiente
        if not self.step_check_environment():
            print()
            print("❌ Setup cancelado. Instale as dependências necessárias.")
            print()
            return

        # Passo 2: Configurar LLM
        if not quick:
            self.step_configure_llm()

        # Passo 3: Configurar specialists
        if not quick:
            self.step_configure_specialists()

        # Passo 4: Configurar workspace
        self.step_configure_workspace()

        # Passo 5: Notificações
        if not quick:
            self.step_configure_notifications()

        # Salvar
        self.step_save_config()

        # Teste opcional
        if not quick:
            self.step_test_config()

        # Finalizar
        print("=" * 80)
        print("🎉 CONFIGURAÇÃO CONCLUÍDA!")
        print("=" * 80)
        print()
        print("Você está pronto para usar o Scripturemon!")
        print()
        print("Próximos passos:")
        print("  1. Execute: python analyze_all_specialists.py <seu_roteiro.pdf>")
        print("  2. Monitore com: python dashboard.py")
        print("  3. Veja histórico: python analysis_history.py")
        print()
        print("=" * 80)
        print()


def main():
    """Main execution"""
    parser = argparse.ArgumentParser(description='Wizard de configuração do Scripturemon')
    parser.add_argument('--quick', action='store_true', help='Setup rápido (usa defaults)')
    parser.add_argument('--check-only', action='store_true', help='Apenas verificar ambiente')

    args = parser.parse_args()

    wizard = SetupWizard()

    if args.check_only:
        wizard.print_welcome()
        wizard.step_check_environment()
    else:
        wizard.run_wizard(quick=args.quick)


if __name__ == '__main__':
    main()
