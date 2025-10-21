# 📁 DIRECTORY STRUCTURE - Scripturemon

**Última Atualização**: 10 de Outubro 2025, 18:45
**Status**: ✅ Organizado e Limpo

---

## 🎯 Estrutura Atual

```
scripturemon/
├── 📄 README.md                      # Documentação principal
├── 📄 SPECIALIST_FACTORY_CRIADO.md   # Status da Specialist Factory
├── 🐍 analyze.py                     # Script principal de análise
├── 🐍 consolidate_analyses.py        # Consolidação de análises
│
├── 📂 engine/                        # Core do sistema
│   ├── analyzers/                    # Especialistas
│   │   ├── dr_dialogue.py ✅         # DrDialogue (referência para os 23 restantes)
│   │   └── ...
│   ├── prompts/                      # Prompts personalizados
│   ├── indexer/                      # Sistema de indexação
│   ├── exporters/                    # Exportadores (HTML, MD, etc.)
│   ├── orchestration/                # Orquestração
│   └── utils/                        # Utilitários
│
├── 📂 specialist_factory/            # Sistema de criação de especialistas
│   ├── BLUEPRINT_SPECIALIST.md       # Guia completo (440 linhas)
│   ├── CHECKLIST_CRIACAO.md          # Checklist passo-a-passo
│   ├── MEMORIA_ESPECIALISTAS.md      # Memória persistente
│   ├── ARQUITETURA_SISTEMA.md        # Arquitetura documentada
│   ├── LISTA_ESPECIALISTAS_ALVO.md   # Lista dos 24 especialistas
│   ├── validate_specialist.py        # Validação automática
│   └── templates/                    # Templates prontos
│       ├── TEMPLATE_specialist.py
│       ├── TEMPLATE_prompts.py
│       └── TEMPLATE_README.md
│
├── 📂 knowledge/                     # Base de conhecimento
│   ├── theory_books/                 # 13 livros de teoria
│   └── master_screenplays/           # Roteiros referência
│
├── 📂 inputs/                        # Entradas
│   ├── examples/                     # Roteiros de exemplo
│   └── to_analyze/                   # Para análise
│
├── 📂 outputs/                       # Saídas do sistema
│   ├── analyses/                     # Análises geradas
│   ├── reports/                      # Relatórios
│   └── consolidated/                 # Consolidados
│
├── 📂 workspace/                     # Workspace de trabalho
│   ├── outputs/                      # Outputs temporários
│   │   └── formatted/                # HTMLs formatados
│   └── sessions/                     # Sessões de análise
│
├── 📂 logs/                          # Logs do sistema
│   ├── aristotle_analysis.log
│   ├── campbell_analysis.log
│   ├── dialogue_analysis.log
│   ├── field_analysis.log
│   └── ... (todos os logs organizados aqui)
│
├── 📂 backups/                       # Backups de código
│   ├── analyze.py.backup
│   └── analyze_sonhos_multi_author.py.backup
│
├── 📂 docs/                          # Documentação
│   ├── DIRECTORY_STRUCTURE.md        # Este arquivo
│   ├── archive/                      # Docs arquivados
│   │   ├── ANALISE_*.md
│   │   ├── AUDITORIA_*.md
│   │   ├── FASE*.md
│   │   ├── TWO_PASS_*.md
│   │   └── ... (30+ docs de sessões anteriores)
│   └── sessions/                     # Docs de sessões
│
├── 📂 archive/                       # Arquivos arquivados
│   ├── old_modelfiles/               # Modelfiles antigos
│   │   ├── Modelfile.scripturemon
│   │   ├── Modelfile.scripturemon-v2
│   │   ├── Modelfile.scripturemon-v3
│   │   └── Modelfile.scripturemon-final
│   ├── old_scripts/                  # Scripts antigos
│   │   ├── analyze_sonhos_multi_author.py
│   │   └── analyze_with_checkpoints.py
│   ├── fase4_experiment/             # Experimentos Fase 4
│   └── session_20251010_debugging/   # Sessões de debug
│
├── 📂 config/                        # Configurações
│   └── rules/                        # Regras YAML
│
└── 📂 tests/                         # Testes do sistema
```

---

## 🔍 Detalhes por Diretório

### 📂 engine/analyzers/
**Propósito**: Especialistas de análise

**Crítico**:
- `dr_dialogue.py` - **DrDialogue** é o especialista de referência ✅
- Modelo para criar os 23 especialistas restantes
- NÃO modificar sem verificar impacto

### 📂 specialist_factory/
**Propósito**: Sistema de criação de especialistas

**Componentes**:
- **BLUEPRINT**: Guia passo-a-passo completo
- **CHECKLIST**: Checklist interativo
- **MEMORIA**: Histórico e aprendizados
- **ARQUITETURA**: Documentação do sistema de 24 especialistas
- **validate_specialist.py**: Validação automática

**Uso**: Ver `SPECIALIST_FACTORY_CRIADO.md`

### 📂 knowledge/
**Propósito**: Base de conhecimento (13 livros + roteiros referência)

**Conteúdo**:
- 13 livros de teoria (Aristotle, McKee, Truby, Field, etc.)
- Master screenplays para referência

**Importante**: Deep context queries consultam esses livros

### 📂 logs/
**Propósito**: Todos os logs do sistema

**Organização**:
- Logs de análises (`*_analysis.log`)
- Logs de testes
- Logs da aplicação

**Manutenção**: Limpar periodicamente logs antigos

### 📂 docs/
**Propósito**: Documentação organizada

**Estrutura**:
- `archive/`: Docs de sessões anteriores (30+ arquivos)
- `sessions/`: Documentação de sessões específicas

**Arquivados**:
- Análises de qualidade
- Auditorias
- Planos de fase
- Migrações
- Resumos de sessão

### 📂 backups/
**Propósito**: Backups de código

**Conteúdo**:
- Versões anteriores de scripts principais
- Backups antes de refatorações

### 📂 archive/
**Propósito**: Arquivos não mais em uso ativo

**Subdiretórios**:
- `old_modelfiles/`: 4 Modelfiles de versões antigas
- `old_scripts/`: Scripts experimentais descontinuados
- `fase4_experiment/`: Experimentos da Fase 4
- `session_*/`: Sessões de debug/desenvolvimento

---

## 📊 Estatísticas

### Arquivos Movidos na Organização (10 Out 2025)

| Categoria | Quantidade | Destino |
|-----------|-----------|---------|
| **Logs** | 12 | `logs/` |
| **Backups** | 2 | `backups/` |
| **Docs** | 30+ | `docs/archive/` |
| **Modelfiles** | 4 | `archive/old_modelfiles/` |
| **Scripts** | 2 | `archive/old_scripts/` |

### Estado Atual

| Item | Count | Observação |
|------|-------|-----------|
| **Especialistas Criados** | 1 | DrDialogue ✅ |
| **Especialistas Planejados** | 23 | Ver MEMORIA_ESPECIALISTAS.md |
| **Livros de Teoria** | 13 | knowledge/theory_books/ |
| **Templates Prontos** | 3 | specialist_factory/templates/ |

---

## 🔒 Arquivos Críticos (NÃO MOVER/DELETAR)

1. **engine/analyzers/dr_dialogue.py** - Especialista de referência
2. **specialist_factory/** (todo) - Sistema de criação
3. **knowledge/theory_books/** - Base de conhecimento
4. **analyze.py** - Script principal
5. **README.md** - Documentação principal

---

## 🚀 Próximos Passos

### Limpeza Futura
- Arquivar workspace/sessions/ antigas (manter últimas 10)
- Limpar logs/ periodicamente
- Revisar docs/archive/ e consolidar duplicatas

### Expansão
- Criar 23 especialistas restantes usando specialist_factory/
- Documentar cada especialista em MEMORIA_ESPECIALISTAS.md
- Manter estrutura organizada

---

## 📝 Histórico de Organizações

### 2025-10-10 (Esta Organização)
**Objetivo**: Limpar diretório raiz, organizar logs/docs/backups
**Resultado**:
- ✅ Diretório raiz limpo (só essenciais)
- ✅ Logs organizados em logs/
- ✅ Docs arquivados em docs/archive/
- ✅ Backups em backups/
- ✅ Modelfiles antigos arquivados
- ✅ DrDialogue 100% funcional

**Arquivos Mantidos no Root**:
- README.md
- SPECIALIST_FACTORY_CRIADO.md
- analyze.py
- consolidate_analyses.py
- (+ diretórios organizados)

---

**Criado**: 10 de Outubro 2025, 18:45
**Por**: Claude Code + Digimundo
**Status**: ✅ ORGANIZADO E DOCUMENTADO

**DIGIMUNDO PRESENTE 🥷**
