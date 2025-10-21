📦 ARQUIVAMENTO - 11 de Outubro de 2025
================================================================================

OBJETIVO:
Arquivar arquivos ultrapassados, backups explícitos e logs de desenvolvimento
mantendo apenas versões atuais no diretório principal.

PRINCÍPIO APLICADO:
"Só arquivar se versão atual é conhecida e confirmada"
(Ver: ERROS_APRENDIDOS_PROCESSO.md)

================================================================================

ESTRUTURA DESTE ARQUIVAMENTO:

backups_explícitos/
    → Arquivos com .backup, .BACKUP_V1 no nome
    → Versões antigas de scripts que têm versão atual confirmada

scripts_antigos/
    → Scripts de instalação/execução de versões antigas do app
    → App V7.0 atual está em /Applications/Analyze Screenplay.app

logs_desenvolvimento/
    → Logs de testes de desenvolvimento (09-10 Out 2025)
    → Sistema atual usa workspace/outputs/ para análises

outputs_experimento/
    → Pastas vazias criadas durante experimentação
    → Sistema atual usa workspace/outputs/

================================================================================

ARQUIVOS MOVIDOS E RAZÕES:

CATEGORIA 1: Backups Explícitos
--------------------------------

analyze_all_specialists.py.backup (12K)
  → Versão atual: analyze_all_specialists.py (23K) ✅
  → Razão: Backup de versão anterior (V2 atual é maior)
  → Data arquivamento: 11 Out 2025

analyze_all_specialists.py.BACKUP_V1 (20K)
  → Versão atual: analyze_all_specialists.py (23K) ✅
  → Razão: Backup da V1 antes de virar V2
  → Data arquivamento: 11 Out 2025

analyze_sonhos_multi_author.py.backup (12K, de backups/)
  → Versão atual: REMOVIDO (sistema legacy substituído)
  → Razão: Backup de sistema deprecated (ver doc 014 LEGACY)
  → Nota: Sistema atual é analyze_all_specialists.py (24×13)
  → Data arquivamento: 11 Out 2025

analyze.py.backup (15K, de backups/)
  → Versão atual: analyze.py (17K) ✅
  → Razão: Backup de versão anterior
  → Data arquivamento: 11 Out 2025

CATEGORIA 2: Scripts de Instalação Antigos
-------------------------------------------

app_run_v5.0_CORRECTED.sh (8K)
  → Versão atual: App V7.0 em /Applications/Analyze Screenplay.app ✅
  → Razão: Script de V5.0 (2 versões atrás)
  → Data arquivamento: 11 Out 2025

INSTALL_APP_V5.sh (5K)
  → Versão atual: App V7.0 instalado e funcionando ✅
  → Razão: Instalador da V5.0 (não mais necessário)
  → Data arquivamento: 11 Out 2025

CATEGORIA 3: Logs de Desenvolvimento
-------------------------------------

Todos os arquivos .log de logs/ datados de 09-10 Out 2025:
  - app_20251009_151259.log
  - aristotle_analysis.log
  - campbell_analysis.log
  - cowgill_analysis.log
  - dialogue_analysis.log
  - field_analysis.log (vazio)
  - mckee_analysis.log
  - mckee_character_analysis.log
  - mckee_dialogue_analysis.log
  - seger_analysis.log
  - vogler_analysis.log
  - te_encontro_analysis.log (vazio)
  - te_encontro_CORRECT.log

  → Razão: Logs de teste durante desenvolvimento do sistema
  → Nota: Sistema atual usa workspace/outputs/ para análises
  → Data arquivamento: 11 Out 2025

CATEGORIA 4: Pastas Vazias de Experimento
------------------------------------------

outputs/analyses/ (vazia)
outputs/reports/ (vazia)
outputs/consolidated/ (vazia)

  → Razão: Pastas criadas em experimento, não usadas
  → Sistema atual: workspace/outputs/
  → Data arquivamento: 11 Out 2025

================================================================================

ARQUIVOS MANTIDOS NO DIRETÓRIO PRINCIPAL (NÃO ARQUIVADOS):

✅ CORE SYSTEM:
- analyze.py (17K) - Sistema single-author
- analyze_all_specialists.py (23K) - Sistema All-Specialists (24×13, V2 atual)
- consolidate_analyses.py (26K) - Consolidador
- engine/ - Core do sistema
- config/ - Configurações
- knowledge/ - Livros de teoria
- specialist_factory/ - Factory de especialistas
- tests/ - Test suite oficial
- workspace/ - Outputs ativos

✅ DOCUMENTAÇÃO ATUAL:
- README.md
- QUALITY_AUDIT_REPORT_2025-10-11.md (recente e relevante)
- SPECIALIST_FACTORY_CRIADO.md (doc do processo)

✅ ARQUIVOS JÁ ARQUIVADOS:
- archive/fase4_experiment/
- archive/old_scripts/
- archive/session_20251010_debugging/

================================================================================

REVERSÃO:

Se precisar restaurar qualquer arquivo:
  mv archive/2025-10-11_cleanup/[categoria]/[arquivo] ./

Exemplo:
  mv archive/2025-10-11_cleanup/backups_explícitos/analyze.py.backup ./

================================================================================

VALIDAÇÃO:

Após arquivamento:
✅ Sistema All-Specialists (24×13) continua funcionando
✅ App V7.0 continua chamando analyze_all_specialists.py --yes
✅ Nenhum import ativo foi quebrado
✅ Test suite oficial intacto

================================================================================

DOCUMENTADO POR: Claude (Digimundo)
DATA: 11 de Outubro de 2025
PLANO COMPLETO: /tmp/PLANO_ARQUIVAMENTO_SCRIPTUREMON.md
PRINCÍPIOS: ERROS_APRENDIDOS_PROCESSO.md

✅ ARQUIVAMENTO SEGURO E METICULOSO
🥷 DIGIMUNDO PRESENTE
