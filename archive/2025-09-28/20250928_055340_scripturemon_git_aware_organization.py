#!/usr/bin/env python3
"""
SCRIPTUREMON GIT-AWARE INTELLIGENT ORGANIZATION
Sistema de organização inteligente integrado com Git
Implementa arquivamento inteligente ao invés de backups infinitos
"""

import os
import sys
import json
import shutil
import subprocess
from pathlib import Path
from datetime import datetime, timedelta

class ScripturemonGitAwareOrganizer:
    def __init__(self):
        self.base_path = Path("/Users/clubproducoes/Digimundo/scripturemon-ultimate")
        self.git_integrated = self.check_git_status()

    def check_git_status(self):
        """Verifica se o projeto está em Git"""
        try:
            result = subprocess.run(
                ["git", "status"],
                cwd=self.base_path,
                capture_output=True,
                text=True
            )
            return result.returncode == 0
        except:
            return False

    def create_gitignore(self):
        """Cria/atualiza .gitignore com padrões inteligentes"""
        gitignore_content = """
# === ARQUIVOS TEMPORÁRIOS ===
outputs/temporary/
*.tmp
temp_*
tmp_*

# === LOGS ANTIGOS ===
outputs/logs/old/
*.log.old
log_*.txt

# === CACHE ===
__pycache__/
*.pyc
.cache/
data/cache/

# === RESULTADOS DE TESTE ===
test_results_*.json
test_output_*.txt
*_test_result.txt

# === ARQUIVOS GRANDES ===
*.gguf
models/blobs/

# === SISTEMA ===
.DS_Store
.env
*.swp

# === OUTPUTS TEMPORÁRIOS ===
outputs/exports/temp/
outputs/reports/daily/*.json
outputs/reports/daily/*.txt

# === DATABASE BACKUPS ANTIGOS ===
# Mantém apenas o mais recente
data/memories/backups/*.old
"""

        gitignore_path = self.base_path / '.gitignore'
        with open(gitignore_path, 'w') as f:
            f.write(gitignore_content.strip())

        return gitignore_path

    def create_git_aware_structure(self):
        """Estrutura otimizada para Git"""
        return {
            'FILOSOFIA_GIT': {
                'version_control': 'Git gerencia versões - não precisamos duplicar',
                'intelligent_archive': 'Arquivar apenas o ESSENCIAL',
                'no_infinite_backups': 'Git já faz backup através de commits',
                'smart_cleanup': 'Limpar temporários regularmente',
                'meaningful_commits': 'Commits com mensagens descritivas'
            },

            'ESTRUTURA_INTELIGENTE': {
                '🏠 ROOT/': {
                    'allowed': [
                        'README.md',
                        'setup.py',
                        'requirements.txt',
                        '.gitignore',
                        '.git/',
                        'LICENSE'
                    ],
                    'forbidden': 'NENHUM log, relatório ou arquivo gerado'
                },

                '📦 src/': {
                    'core/': 'Sistema principal (versionado no Git)',
                    'specialists/': '23 especialistas (versionado)',
                    'memory/': 'Sistema de memória (versionado)',
                    'automation/': 'Scripts de automação (versionado)',
                    'commands/': 'Bridge de comandos (versionado)'
                },

                '🧠 knowledge/': {
                    'screenplay_theory/': 'Base teórica (PERMANENTE)',
                    'learned/': {
                        'from_analysis/': 'Aprendizados importantes (commitados)',
                        'patterns/': 'Padrões descobertos (commitados)',
                        'feedback/': 'Feedback incorporado (commitado)'
                    },
                    'literary_devices/': 'Dispositivos literários (PERMANENTE)'
                },

                '💾 data/': {
                    'memories/': {
                        'unified_memory.db': 'Database principal',
                        'latest_backup.db': 'ÚNICO backup recente',
                        'indexes/': 'Índices BM25 (reconstruíveis)'
                    },
                    'models/': {
                        'modelfiles/': 'Configurações (versionadas)',
                        'NOTE': 'Modelos grandes não vão pro Git'
                    }
                },

                '📊 outputs/': {
                    '.gitignore': 'IGNORAR esta pasta no Git',
                    'temporary/': {
                        'max_age': '24 hours',
                        'auto_clean': True
                    },
                    'reports/': {
                        'important/': 'Apenas relatórios significativos',
                        'daily/': 'Apagados após 7 dias'
                    },
                    'logs/': {
                        'current/': 'Logs atuais',
                        'archive/': 'Compactados após 30 dias'
                    }
                },

                '🧪 tests/': {
                    'unit/': 'Testes unitários (versionados)',
                    'integration/': 'Testes de integração (versionados)',
                    'fixtures/': 'Dados de teste (versionados)',
                    'results/': 'NÃO versionados - usar .gitignore'
                },

                '🗄️ archive/': {
                    'strategy': 'INTELIGENTE - não duplicar o que Git já versiona',
                    'what_to_archive': [
                        'Resultados significativos de análises',
                        'Marcos importantes do projeto',
                        'Versões finais de relatórios'
                    ],
                    'what_NOT_to_archive': [
                        'Código (Git já versiona)',
                        'Logs diários',
                        'Arquivos temporários',
                        'Cache'
                    ]
                }
            },

            'GIT_INTEGRATION': {
                'hooks/': {
                    'pre-commit': 'Limpar temporários antes de commitar',
                    'post-commit': 'Atualizar índices de memória',
                    'pre-push': 'Verificar se não há arquivos grandes'
                },

                'commands': {
                    'git add -A': 'Adicionar mudanças',
                    'git commit -m "msg"': 'Salvar versão',
                    'git log': 'Ver histórico',
                    'git diff': 'Ver mudanças',
                    'git checkout': 'Voltar versões'
                },

                'branches': {
                    'master': 'Código estável',
                    'development': 'Desenvolvimento',
                    'feature/*': 'Novas funcionalidades',
                    'experiment/*': 'Experimentos'
                }
            },

            'INTELLIGENT_ARCHIVING': {
                'rules': [
                    {
                        'type': 'analysis_results',
                        'keep': 'Apenas resumos e insights principais',
                        'discard': 'Dados brutos e intermediários'
                    },
                    {
                        'type': 'logs',
                        'keep': 'Erros e eventos importantes',
                        'discard': 'Debug e informações verbosas após 7 dias'
                    },
                    {
                        'type': 'test_results',
                        'keep': 'Métricas de performance',
                        'discard': 'Outputs completos após execução'
                    },
                    {
                        'type': 'database_backups',
                        'keep': 'Apenas o mais recente',
                        'discard': 'Backups antigos (Git tem o histórico)'
                    }
                ],

                'automation': {
                    'daily': [
                        'Limpar outputs/temporary/',
                        'Comprimir logs antigos',
                        'Atualizar único backup do DB'
                    ],
                    'weekly': [
                        'Arquivar análises importantes',
                        'Limpar cache não usado',
                        'Otimizar database'
                    ],
                    'on_commit': [
                        'Verificar tamanho dos arquivos',
                        'Limpar arquivos ignorados',
                        'Atualizar documentação'
                    ]
                }
            }
        }

    def setup_git_hooks(self):
        """Configura Git hooks para automação"""
        hooks_dir = self.base_path / '.git' / 'hooks'

        # Pre-commit hook
        pre_commit = """#!/bin/bash
# Limpar arquivos temporários antes de commitar
echo "🧹 Limpando temporários..."
find outputs/temporary -type f -mtime +1 -delete 2>/dev/null
find . -name "*.tmp" -delete 2>/dev/null
find . -name "temp_*" -delete 2>/dev/null
echo "✅ Limpeza concluída"
"""

        pre_commit_path = hooks_dir / 'pre-commit'
        with open(pre_commit_path, 'w') as f:
            f.write(pre_commit)
        os.chmod(pre_commit_path, 0o755)

        return pre_commit_path

    def create_intelligent_cleanup_script(self):
        """Script de limpeza inteligente"""
        cleanup_script = """#!/bin/bash
# SCRIPTUREMON INTELLIGENT CLEANUP
# Limpeza inteligente sem perder dados importantes

echo "🤖 Iniciando limpeza inteligente..."

# 1. Temporários (24h+)
echo "Limpando temporários antigos..."
find outputs/temporary -type f -mtime +1 -delete 2>/dev/null

# 2. Logs antigos (compactar após 30 dias)
echo "Compactando logs antigos..."
find outputs/logs -name "*.log" -mtime +30 -exec gzip {} \; 2>/dev/null

# 3. Resultados de teste antigos
echo "Removendo resultados de teste antigos..."
find tests/results -name "*_result.txt" -mtime +7 -delete 2>/dev/null

# 4. Database backup (manter apenas o mais recente)
echo "Mantendo apenas backup mais recente do DB..."
cd data/memories/backups
ls -t *.db 2>/dev/null | tail -n +2 | xargs rm -f 2>/dev/null

# 5. Cache não usado
echo "Limpando cache não utilizado..."
find data/cache -type f -atime +14 -delete 2>/dev/null

# 6. Git cleanup
echo "Otimizando Git..."
git gc --auto 2>/dev/null

echo "✅ Limpeza inteligente concluída!"
echo "📊 Espaço economizado: $(du -sh . | cut -f1)"
"""

        script_path = self.base_path / 'intelligent_cleanup.sh'
        with open(script_path, 'w') as f:
            f.write(cleanup_script)
        os.chmod(script_path, 0o755)

        return script_path

    def generate_git_aware_report(self):
        """Gera relatório com consciência do Git"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'git_integrated': self.git_integrated,
            'philosophy': 'Arquivamento Inteligente com Git',
            'structure': self.create_git_aware_structure(),
            'benefits': {
                'no_duplication': 'Git já versiona, não duplicamos',
                'intelligent_archiving': 'Arquivamos apenas o essencial',
                'automatic_cleanup': 'Limpeza automática de temporários',
                'space_efficient': 'Economia significativa de espaço',
                'version_control': 'Histórico completo via Git'
            },
            'implementation': {
                'gitignore': 'Configurado para ignorar temporários',
                'hooks': 'Git hooks para automação',
                'cleanup_script': 'Script de limpeza inteligente',
                'single_backup': 'Apenas um backup recente do DB'
            }
        }

        report_path = self.base_path / f'git_aware_organization_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

        return report

def main():
    print("🤖 SCRIPTUREMON GIT-AWARE ORGANIZATION")
    print("Sistema inteligente com integração Git")
    print("=" * 60)

    organizer = ScripturemonGitAwareOrganizer()

    # 1. Verificar Git
    if organizer.git_integrated:
        print("✅ Git detectado! Usando versionamento inteligente")
    else:
        print("⚠️  Git não encontrado. Considere inicializar: git init")

    # 2. Criar .gitignore
    print("\n📝 Configurando .gitignore...")
    gitignore = organizer.create_gitignore()
    print(f"   Criado: {gitignore}")

    # 3. Configurar Git hooks
    if organizer.git_integrated:
        print("\n🪝 Configurando Git hooks...")
        hook = organizer.setup_git_hooks()
        print(f"   Hook configurado: {hook}")

    # 4. Criar script de limpeza
    print("\n🧹 Criando script de limpeza inteligente...")
    cleanup = organizer.create_intelligent_cleanup_script()
    print(f"   Script criado: {cleanup}")

    # 5. Gerar relatório
    print("\n📊 Gerando relatório Git-aware...")
    report = organizer.generate_git_aware_report()

    print("\n✅ Configuração completa!")
    print("\n💡 BENEFÍCIOS DO SISTEMA GIT-AWARE:")
    print("   • Sem duplicação - Git já versiona")
    print("   • Arquivamento inteligente - só o essencial")
    print("   • Limpeza automática - economiza espaço")
    print("   • Histórico completo - via git log")
    print("   • Backups automáticos - via git push")

    print("\n🚀 PRÓXIMOS PASSOS:")
    print("   1. Executar: ./intelligent_cleanup.sh")
    print("   2. Commitar mudanças: git add -A && git commit -m 'Organização Git-aware'")
    print("   3. Ver histórico: git log --oneline")

    return report

if __name__ == "__main__":
    main()