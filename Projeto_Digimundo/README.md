# 🎬 CineProd - Projeto Digimundo

Sistema completo de gestão de produção audiovisual desenvolvido em Flask.

## 📁 Estrutura do Projeto

```
Projeto_Digimundo/
│
├── 📂 cineprod-flask/          # 🎯 APLICAÇÃO PRINCIPAL (857 MB)
│   ├── app/                    # Código da aplicação
│   ├── config/                 # Configurações
│   ├── migrations/             # Migrações do banco de dados
│   ├── tests/                  # Testes automatizados
│   ├── venv/                   # Ambiente virtual Python
│   └── ...                     # Outros arquivos da aplicação
│
├── 📂 docs/                    # 📚 DOCUMENTAÇÃO (344 KB)
│   ├── architecture/           # Arquitetura e mapas do sistema
│   │   ├── ARQUITETURA_CINEPROD_SCRIPTUREMON.md
│   │   ├── CINEPROD_SYSTEM_ANALYSIS_COMPLETE.md
│   │   └── MAPA_SISTEMA_COMPLETO.md
│   │
│   ├── development/            # Planejamento e desenvolvimento
│   │   ├── CINEPROD_UPGRADE_MASTER_PLAN.md
│   │   ├── PLANO_DESENVOLVIMENTO_ATUALIZADO.md
│   │   └── PROMPTS_MULTI_TASK_CINEPROD.md
│   │
│   ├── debugging/              # Análises e correções
│   │   ├── CINEPROD_DEBUGGING_MAP.md
│   │   └── RELATORIO_ANALISE_COMPLETA_FINAL.md
│   │
│   └── reports/                # Relatórios e progresso
│       ├── ANALISE_VERSOES_ANTERIORES.md
│       ├── PROGRESS.md
│       ├── RESUMO_ACOES_APLICADAS.md
│       └── VPS_STATUS_REPORT_2025-10-28.md
│
├── 📂 assets/                  # 🎨 RECURSOS VISUAIS (2.5 MB)
│   └── logos/                  # Logos do sistema
│       ├── logo_club_sistema.png
│       ├── logo_club_sistema_fundo_azul.png
│       ├── logo_club_sistema_fundo_azul_2.png
│       └── logo_club_sistema_transparent.png
│
├── 📂 archive/                 # 📦 VERSÕES ANTIGAS (1.9 MB)
│   ├── prototypes/             # Protótipos HTML antigos
│   │   ├── CineProd-CRUD-Complete.html
│   │   ├── CineProd-DigimonStyle.html
│   │   └── cineprod-deploy.tar.gz
│   │
│   └── old-versions/           # Versões antigas TSX/HTML
│       └── (19 arquivos de versões anteriores)
│
├── 📂 backups/                 # 💾 BACKUPS (54 MB)
│   └── cineprod-backup-20251023-022646.tar.gz
│
├── .gitignore                  # Regras do Git
└── README.md                   # Este arquivo
```

## 🚀 Como Usar

### Desenvolvimento Local
```bash
cd cineprod-flask
source venv/bin/activate
python wsgi.py
```

### Produção (VPS)
```bash
ssh root@82.25.74.142
cd /opt/cineprod
sudo systemctl restart cineprod
```

## 📊 Estatísticas

- **Total do Projeto**: ~916 MB
- **Aplicação Principal**: 857 MB (93.6%)
- **Backups**: 54 MB (5.9%)
- **Assets**: 2.5 MB (0.3%)
- **Archive**: 1.9 MB (0.2%)
- **Documentação**: 344 KB (0.04%)

## 🔧 Manutenção

### Backups
Os backups automáticos são armazenados em `/backups/` e devem ser feitos regularmente.

### Documentação
Mantenha a documentação atualizada em `/docs/` seguindo a estrutura por categoria.

### Archive
Versões antigas e protótipos devem ser movidos para `/archive/` para manter a raiz limpa.

## 📝 Histórico de Organização

**2025-10-30**: Reorganização completa da estrutura do projeto
- ✅ Criada estrutura de pastas organizada
- ✅ Documentação categorizada em `/docs/`
- ✅ Assets separados em `/assets/`
- ✅ Versões antigas arquivadas em `/archive/`
- ✅ Removidas pastas duplicadas e temporárias (-792 KB)
- ✅ Limpeza de arquivos `.DS_Store`
- ✅ Atualizado `.gitignore` com novas regras

## 🌐 Links Úteis

- **Produção**: https://cineprod.digimundo.pt
- **Documentação Técnica**: `/docs/architecture/`
- **Planejamento**: `/docs/development/`
- **Relatórios**: `/docs/reports/`

---

**Desenvolvido por**: Club Produções / Digimundo
**Sistema**: CineProd V2 - Gestão de Produção Audiovisual
