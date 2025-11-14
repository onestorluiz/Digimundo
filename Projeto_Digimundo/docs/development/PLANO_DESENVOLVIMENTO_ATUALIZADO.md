# 🎯 PLANO DE DESENVOLVIMENTO ATUALIZADO - CINEPROD

**Data:** 2025-10-21
**Versão:** 2.0 (Atualizado após análise das versões anteriores)
**Design Base:** Digimon World 3 (Retro Gaming PS2)
**Inspiração Funcional:** StudioBinder (Software profissional de produção cinematográfica)

---

## 🎨 FONTE DE INSPIRAÇÃO

### **Design Visual:**
- **Digimon World 3** (PlayStation 2)
  - Estética retro gaming
  - Fonte: Press Start 2P
  - Grid animado com scanlines
  - Paleta: Dark Blue (#0a1428), Neon Blue (#4a9fff), Yellow (#ffdd00), Cyan (#00ddff)
  - Window components com bordas neon
  - Efeitos de glow suaves

### **Funcionalidades:**
- **StudioBinder** (https://app.studiobinder.com)
  - Sistema profissional de gestão de produção
  - Call Sheets digitais
  - Mood Boards
  - Storyboards
  - Shot Lists
  - Task Management (Kanban)
  - Calendar/Schedule
  - Documentos e uploads

### **Código Base:**
- Versões anteriores em `/Outras_V/`
  - Especialmente `CineProd-Ultimate-System_4.html` (4.052 linhas)
  - Funcionalidades completas já implementadas em JavaScript vanilla
  - LocalStorage para persistência
  - Bibliotecas: Chart.js, XLSX, jsPDF

---

## 📊 SITUAÇÃO ATUAL

### ✅ **JÁ IMPLEMENTADO (Design Digimon World 3):**
1. ✅ Login page retro
2. ✅ Dashboard com stats
3. ✅ Sidebar menu com Press Start 2P
4. ✅ Projects (CRUD completo)
5. ✅ Crew (CRUD completo)
6. ✅ Equipment (CRUD completo)
7. ✅ Locations (CRUD completo)
8. ✅ Sistema de Modal
9. ✅ LocalStorage persistence
10. ✅ Search/Filter em tabelas
11. ✅ Grid background animado + Scanlines
12. ✅ Window components com neon borders
13. ✅ Glow effects otimizados (legibilidade)

**Arquivo:** `/Projeto_Digimundo/CineProd-DigimonStyle.html`

---

## 🚀 PLANO DE DESENVOLVIMENTO

### **FASE 1: FUNDAÇÃO E MÓDULOS BÁSICOS** ⚡ (AGORA)
**Duração estimada:** 1-2 dias
**Objetivo:** Adicionar funcionalidades essenciais com código pronto das versões anteriores

#### **1.1 Funções Utilitárias**
- [x] Analisar versões anteriores
- [ ] `generateId(prefix)` - Geração de IDs únicos
- [ ] `formatCurrency(value)` - Formatação R$ com Intl.NumberFormat
- [ ] `formatDate(date)` - Formatação pt-BR
- [ ] `formatFileSize(bytes)` - KB, MB, GB
- [ ] `getFileIcon(type)` - Ícones por tipo de arquivo

**Localização:** Adicionar ao `<script>` do CineProd-DigimonStyle.html

#### **1.2 Sistema de Notificações Retro**
- [ ] `showNotification(message, type)` adaptado ao design Digimon
- [ ] Toast messages com tema retro (neon borders, Press Start 2P)
- [ ] Tipos: success (✅), error (❌), warning (⚠️), info (ℹ️)
- [ ] Animações de entrada/saída
- [ ] Auto-dismiss 3 segundos
- [ ] Posição: bottom-right com window styling

**Componentes:**
```css
.notification {
    background: var(--window-bg);
    border: 3px solid var(--neon-blue);
    font-family: 'Press Start 2P', cursive;
    font-size: 7px;
    padding: 15px 20px;
    border-radius: 4px;
    box-shadow: 0 0 10px rgba(74, 159, 255, 0.3);
}
```

#### **1.3 Módulo: Scripts/Roteiros**
- [ ] Tabela de roteiros com design retro
- [ ] CRUD completo:
  - Título, Autor, Versão, Data
  - Formato: Feature, Short, Series, Commercial
  - Status: Development, Draft, Revision, Final, Production
  - Páginas, Sinopse
- [ ] Badge de status com cores retro
- [ ] Botão "Ver" para visualização
- [ ] Integração com notificações

**Fonte:** `CineProd-Ultimate-System_4.html` (linhas 1631-1774)

#### **1.4 Módulo: Budget/Orçamento**
- [ ] Tabela de orçamento com design retro
- [ ] CRUD completo:
  - Categoria: Pre-Production, Production, Post-Production, Equipment, Crew, Locations, Misc
  - Item, Descrição
  - Quantidade, Valor Unitário
  - Valor Total (calculado automaticamente)
  - Projeto vinculado
- [ ] Formatação de moeda (R$)
- [ ] Total geral calculado
- [ ] Stats card no dashboard

**Fonte:** `CineProd-Ultimate-System_4.html` (linhas 1775-1928)

---

### **FASE 2: FUNCIONALIDADES AVANÇADAS** 🔥
**Duração estimada:** 2-3 dias
**Objetivo:** Adicionar módulos complexos com integrações

#### **2.1 Bibliotecas Externas**
- [ ] Chart.js - Gráficos retro
- [ ] XLSX - Exportação Excel
- [ ] jsPDF + autotable - Exportação PDF
- [ ] Adaptar visual dos charts ao tema Digimon

#### **2.2 Módulo: Call Sheets**
- [ ] Tabela de call sheets com design retro
- [ ] CRUD completo:
  - Projeto (dropdown)
  - Data, Call Time, Wrap Time
  - Clima
  - Locação
  - Cenas (múltiplas, separadas por vírgula)
  - Notas importantes
  - **Equipe (checkboxes)** - multi-select
- [ ] Ações especiais:
  - 👁️ Ver (visualização completa)
  - 🖨️ Imprimir
  - 📧 Enviar por email (placeholder)
  - 📄 Exportar PDF individual
- [ ] Layout de impressão otimizado

**Fonte:** `CineProd-Ultimate-System_4.html` (linhas 2366-2633)

#### **2.3 Módulo: Documents/Documentos**
- [ ] Área de upload com design retro
- [ ] **Drag & Drop** upload
- [ ] Upload múltiplo de arquivos
- [ ] Detecção de tipo de arquivo
- [ ] Ícones personalizados:
  - 📄 PDF
  - 🖼️ Imagens
  - 🎥 Vídeos
  - 🎵 Áudio
  - 📝 Texto
  - 📊 Excel
  - 📽️ PowerPoint
  - 📃 Word
  - 📎 Outros
- [ ] Lista de documentos com:
  - Nome, Tipo, Tamanho, Data upload
  - ⬇️ Download
  - 🗑️ Excluir
- [ ] Formatação de tamanho (KB, MB, GB)

**Fonte:** `CineProd-Ultimate-System_4.html` (linhas 2635-2757)

---

### **FASE 3: VISUALIZAÇÃO E CALENDÁRIO** 📅
**Duração estimada:** 2-3 dias
**Objetivo:** Cronograma visual e relatórios

#### **3.1 Módulo: Schedule/Cronograma**
- [ ] Calendário mensal com tema retro
- [ ] Navegação entre meses (← →)
- [ ] Dias do mês em grid
- [ ] Destacar dia atual
- [ ] Eventos por dia (dots coloridos)
- [ ] Modal para adicionar eventos:
  - Título
  - Data/hora
  - Tipo (Filmagem, Reunião, Deadline, etc.)
  - Projeto vinculado
  - Descrição
- [ ] Visualização de eventos do dia
- [ ] Lista lateral de próximos eventos

**Fonte:** `CineProd-Ultimate-System_4.html` (linhas 2762-2937)
**Observação:** Requer redesign completo para tema retro

#### **3.2 Módulo: Reports/Relatórios**
- [ ] Dashboard de relatórios
- [ ] Tabs retro:
  - 📊 Overview (Visão Geral)
  - 💰 Financeiro
  - 🎬 Produção
  - 👥 Equipe
- [ ] **Relatório Overview:**
  - Total de projetos (status breakdown)
  - Total de equipe (por departamento)
  - Total de equipamentos (por categoria)
  - Total de locações
- [ ] **Relatório Financeiro:**
  - Orçamento total
  - Gasto total
  - Saldo
  - Budget por projeto (gráfico)
  - Budget por categoria (gráfico)
- [ ] **Relatório de Produção:**
  - Projetos por status (gráfico pizza retro)
  - Timeline de projetos
  - Equipment em uso vs disponível
- [ ] **Relatório de Equipe:**
  - Crew por departamento (gráfico)
  - Status da equipe (ativo/inativo)
  - Diárias totais
- [ ] Gráficos Chart.js com:
  - Cores do tema retro
  - Fonte Press Start 2P
  - Bordas neon
  - Grid background

**Fonte:** `CineProd-Ultimate-System_4.html` (linhas 2938-3190)
**Observação:** Adaptar visual dos gráficos

---

### **FASE 4: EXPORTAÇÃO E POLIMENTO** 📤
**Duração estimada:** 1-2 dias
**Objetivo:** Exportação de dados e refinamento

#### **4.1 Exportação Excel**
- [ ] `exportAllToExcel()` - Exporta tudo
  - Sheet: Projects
  - Sheet: Crew
  - Sheet: Equipment
  - Sheet: Locations
  - Sheet: Scripts
  - Sheet: Budget
  - Sheet: Call Sheets
- [ ] Botão no header/dashboard
- [ ] Nome do arquivo: `CineProd_Export_YYYYMMDD.xlsx`
- [ ] Formatação de colunas
- [ ] Notificação de sucesso

**Fonte:** `CineProd-Ultimate-System_4.html` (linhas 3198-3252)

#### **4.2 Exportação PDF**
- [ ] `exportCompletePDF()` - Relatório completo
  - Capa com logo retro
  - Índice
  - Seções: Projects, Crew, Equipment, Locations, Budget
  - Formatação retro (cores do tema)
- [ ] `exportCallSheetPDF(id)` - Call sheet individual
  - Layout de impressão profissional
  - Logo e header
  - Todas as informações da call sheet
  - Lista de equipe
  - Notas e observações
- [ ] Botões de export
- [ ] Preview antes de baixar (opcional)

**Fonte:** `CineProd-Ultimate-System_4.html` (linhas 3254-3400+)

#### **4.3 Polimento Final**
- [ ] Revisar todos os módulos
- [ ] Testar CRUD completo
- [ ] Validação de formulários
- [ ] Mensagens de erro consistentes
- [ ] Loading states (opcional)
- [ ] Confirmações de exclusão
- [ ] Breadcrumbs (opcional)
- [ ] Atalhos de teclado (opcional)
- [ ] Responsividade mobile
- [ ] Performance optimization
- [ ] Limpeza de código
- [ ] Comentários e documentação

---

## 📦 MÓDULOS CRIADOS (StudioBinder-inspired)

### **Módulos Criados no Plano Original mas Não Prioritários:**
Estes serão implementados depois da FASE 4, se necessário:

1. **Mood Board** - Quadro de inspiração visual
   - Upload de imagens
   - Drag & drop para organizar
   - Tags e categorias
   - Compartilhamento

2. **Storyboard** - Quadros de storyboard
   - Upload de desenhos/frames
   - Numeração de cenas
   - Descrição por quadro
   - Setas de movimento

3. **Shot List** - Lista de planos
   - Número do plano
   - Tipo de plano (Close, Medium, Wide, etc.)
   - Movimento (Static, Pan, Tilt, etc.)
   - Lente, FPS
   - Descrição

4. **Tasks (Kanban)** - Gestão de tarefas
   - Colunas: To Do, In Progress, Review, Done
   - Drag & drop
   - Atribuição de responsável
   - Prioridade e deadline

**Observação:** Estas funcionalidades são mais complexas e requerem mais tempo de desenvolvimento. Por enquanto, focar no core functionality.

---

## 🎯 ESTRATÉGIA DE DESENVOLVIMENTO

### **Abordagem:**
1. **Copiar código das versões anteriores** (Outras_V/)
2. **Adaptar design** ao tema Digimon World 3
3. **Manter funcionalidade** 100% intacta
4. **Testar cada módulo** antes de avançar
5. **Commit incremental** no GitHub

### **Priorização:**
- ✅ **Funcionalidades essenciais primeiro** (FASE 1 e 2)
- ⚡ **Visualizações depois** (FASE 3)
- 📤 **Exportação e extras por último** (FASE 4)

### **Tecnologias:**
- **Frontend:** HTML5, CSS3, JavaScript (Vanilla)
- **Storage:** LocalStorage (browser)
- **Fontes:** Google Fonts (Press Start 2P)
- **Bibliotecas:**
  - Chart.js (gráficos)
  - XLSX (exportar Excel)
  - jsPDF + autotable (PDFs)

### **Design System:**
- **Paleta:** Dark Blue, Neon Blue, Yellow, Cyan
- **Tipografia:** Press Start 2P (8px base)
- **Componentes:** Windows, Buttons, Inputs, Badges, Notifications
- **Animações:** Grid scroll, Scanlines, Glow effects (suaves)
- **Layout:** Sidebar + Header + Content Area

---

## 📝 ARQUIVO PRINCIPAL

**Arquivo Base:** `/Users/clubproducoes/Digimundo/Projeto_Digimundo/CineProd-DigimonStyle.html`

**Tamanho atual:** ~1.400 linhas
**Tamanho estimado final:** ~3.500-4.000 linhas

---

## 🔄 MIGRAÇÃO FUTURA (Flask/Python)

Após completar todas as fases em HTML/JS, o sistema será migrado para:

- **Backend:** Flask + PostgreSQL
- **Frontend:** Templates Jinja2 + mesmo design retro
- **LLM:** Integração com Ollama (local) + OpenAI (backup)
- **Upload:** Sistema de arquivos real
- **Auth:** Sistema de usuários completo
- **Deploy:** VPS com Docker

**Referência:** Ver `MAPA_SISTEMA_COMPLETO.md` para estrutura Flask

---

## ✅ CHECKLIST DE PROGRESSO

### FASE 1: ⏳ EM ANDAMENTO
- [x] Análise de versões anteriores
- [x] Documento de planejamento
- [ ] Funções utilitárias
- [ ] Sistema de notificações
- [ ] Módulo Scripts
- [ ] Módulo Budget

### FASE 2: ⏸️ AGUARDANDO
- [ ] Bibliotecas externas
- [ ] Módulo Call Sheets
- [ ] Módulo Documents

### FASE 3: ⏸️ AGUARDANDO
- [ ] Módulo Schedule
- [ ] Módulo Reports

### FASE 4: ⏸️ AGUARDANDO
- [ ] Exportação Excel
- [ ] Exportação PDF
- [ ] Polimento final

---

## 🎉 META FINAL

**Sistema CineProd completo** com:
- ✅ Design retro único (Digimon World 3)
- ✅ Funcionalidades profissionais (StudioBinder-inspired)
- ✅ CRUD completo de 10+ módulos
- ✅ Exportação Excel e PDF
- ✅ Relatórios e gráficos
- ✅ Sistema de upload
- ✅ Calendário e cronograma
- ✅ 100% funcional em navegador (sem backend)

**Pronto para:**
- Uso imediato pela equipe de produção
- Migração futura para Flask/Python
- Integração com Scripturemon (análise de roteiros)
- Deploy em VPS

---

**Desenvolvedor:** Claude Code
**Cliente:** Clube Produções / Digimundo
**Início:** 2025-10-21
**Conclusão estimada FASE 1-4:** 6-10 dias
