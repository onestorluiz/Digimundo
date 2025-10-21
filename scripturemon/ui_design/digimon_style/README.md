# 🎬 SCRIPTUREMON - Digimon World 3 UI Design

Interface inspirada no clássico **Digimon World 3** para PlayStation 2.

## 🎨 Características do Design

### Visual Style
- **Grid Background**: Fundo azul com grid animado estilo PS2
- **Neon Borders**: Janelas com bordas brilhantes (azul neon)
- **Pixel Font**: Tipografia pixelada estilo retro
- **Scanlines**: Efeito de linhas de varredura CRT
- **Color Palette**: Azul escuro, ciano, amarelo, verde

### Layout
- **4 Telas Principais**:
  1. Main Menu
  2. Specialist Selection
  3. Analysis Progress
  4. Results Screen

## 🎮 Controles

### Teclado
- **↑↓←→** ou **WASD**: Navegação
- **ENTER** ou **SPACE** ou **O**: Confirmar
- **ESC** ou **X**: Voltar
- **1-4**: Atalhos para telas

### Mouse
- **Hover**: Destaca opção
- **Click**: Seleciona/Confirma

## 📁 Arquivos

```
ui_design/digimon_style/
├── index.html       # Estrutura das 4 telas
├── style.css        # Estilos Digimon World 3
├── script.js        # Navegação e interatividade
└── README.md        # Esta documentação
```

## 🖼️ Telas

### 1. Main Menu (Tela Principal)
```
┌─────────────────────────────────────────────┐
│     SCRIPTUREMON v10.0                      │
│     SCREENPLAY ANALYSIS SYSTEM              │
├─────────────────────────────────────────────┤
│                                             │
│  📄 New Screenplay         ▶               │
│  💾 Continue Analysis      ▶               │
│  🔬 View Specialists       ▶               │
│  ⚙️  Settings               ▶               │
│                                             │
│  Stats:                                     │
│  🔴 Analyses: 247                           │
│  🔵 Screenplays: 89                         │
│  ⭐ Total Time: 142h                        │
│  💰 Avg Score: 8.7/10                       │
└─────────────────────────────────────────────┘
  TP 10        SELECT: Choose | START: Confirm
```

### 2. Specialist Selection
```
┌─────────────────────────────────────────────┐
│        SPECIALIST SELECTION                 │
│        Choose Analysis Type                 │
├─────────────────────────────────────────────┤
│  ┌────┐ ┌────┐     ┌──────────────────┐   │
│  │ 👤 │ │ 🏗️ │     │       👤         │   │
│  │Char│ │Struc│     │  DrCharacter     │   │
│  └────┘ └────┘     ├──────────────────┤   │
│  ┌────┐ ┌────┐     │ TYPE: Character  │   │
│  │ 🎭 │ │ 🎬 │     │ EXP: ████░ 1890  │   │
│  │Theme│ │Genre│     │ AUTHORS: 13      │   │
│  └────┘ └────┘     │ AVG TIME: 2.3min │   │
│  ┌────┐ ┌────┐     ├──────────────────┤   │
│  │ 💬 │ │ ⚡ │     │ Description...   │   │
│  │Dial │ │Pace│     │                  │   │
│  └────┘ └────┘     │ McKee | Field    │   │
│                     │ Truby | Campbell │   │
└─────────────────────────────────────────────┘
```

### 3. Analysis Progress
```
┌─────────────────────────────────────────────┐
│      ANALYSIS IN PROGRESS                   │
│      TE ENCONTRO EM MIM                     │
├─────────────────────────────────────────────┤
│  Specialist: DrCharacter                    │
│  Author: McKee                              │
│  Status: ANALYZING...                       │
├─────────────────────────────────────────────┤
│  Overall Progress                           │
│  ████████████████░░░░░░░░  72/312 (23.1%)  │
│                                             │
│  ⏱️  2h 24m elapsed    🎯 ETA: 8h 16m      │
│  ⚡ 2.1 min/analysis   💰 $0.00 (Ollama)   │
├─────────────────────────────────────────────┤
│  Completed:                                 │
│  ✓ Character 13/13  ✓ Structure 13/13     │
│  ✓ Theme 13/13      ✓ Genre 13/13         │
│  ✓ Pacing 13/13     ⟳ Transitions 7/13    │
└─────────────────────────────────────────────┘
```

### 4. Results Screen
```
┌─────────────────────────────────────────────┐
│        ANALYSIS COMPLETE                    │
│        TE ENCONTRO EM MIM                   │
├─────────────────────────────────────────────┤
│           OVERALL QUALITY                   │
│                8.7/10                       │
│             ⭐⭐⭐⭐☆                        │
├─────────────────────────────────────────────┤
│  Scores:              Top Insights:         │
│  👤 Character 9.2     • Strong protagonist  │
│  🏗️ Structure 8.5     • Well-balanced acts  │
│  🎭 Theme     8.8     • Effective dialogue  │
│  🎬 Genre     8.3     • Pacing in Act 2     │
│  💬 Dialogue  9.0                           │
│  ⚡ Pacing    8.1                           │
├─────────────────────────────────────────────┤
│  Total: 312 analyses | 10h 32m | Ollama    │
└─────────────────────────────────────────────┘
```

## 🎨 Elementos de Design

### Grid Background
- Grid 50x50px
- Linhas diagonais 45°
- Scanlines animadas
- Parallax scroll

### Window Style
- Background: rgba(10, 30, 60, 0.85)
- Border: 3px neon blue (#4a9fff)
- Glow: box-shadow com blur
- Corner decorations

### Typography
- Font: 'Press Start 2P'
- Títulos: 18px amarelo (#ffdd00)
- Texto: 10-12px branco
- Stats: ciano (#00ddff)

### Colors
```css
--bg-dark:       #0a1428  /* Fundo escuro */
--grid-blue:     #2a4f7a  /* Grid lines */
--neon-blue:     #4a9fff  /* Bordas neon */
--text-yellow:   #ffdd00  /* Títulos/seleção */
--text-cyan:     #00ddff  /* Info secundária */
--hp-red:        #ff4444  /* Vermelho HP */
--mp-blue:       #4488ff  /* Azul MP */
--exp-gold:      #ffcc00  /* EXP bar */
```

### Animations
- Grid scroll (20s loop)
- Scanline (8s vertical)
- Blink (1s on/off)
- Pulse (1.5s fade)
- Rotate (2s 360°)

## 🚀 Como Usar

### 1. Abrir no Navegador
```bash
open ui_design/digimon_style/index.html
```

### 2. Testar Navegação
- Use teclas WASD ou setas
- Press ENTER para confirmar
- Press ESC para voltar

### 3. Alternar Telas (Debug)
```javascript
// No console do navegador:
ScriptureMonUI.showScreen('mainMenu')
ScriptureMonUI.showScreen('specialistSelect')
ScriptureMonUI.showScreen('analysisProgress')
ScriptureMonUI.showScreen('resultsScreen')
```

### 4. Simular Progresso
```javascript
// Atualizar progresso manualmente:
ScriptureMonUI.updateProgressUI({
    completed: 100,
    total: 312,
    currentSpecialist: 'character',
    currentAuthor: 'mckee'
})
```

## 🔌 Integração com Backend

### API Endpoints (Future)
```javascript
// GET /api/analysis/list
// Retorna lista de análises

// GET /api/analysis/:id/progress
// Retorna progresso de análise específica

// GET /api/analysis/:id/results
// Retorna resultados da análise

// POST /api/analysis/start
// Inicia nova análise
```

### WebSocket (Real-time Updates)
```javascript
const ws = new WebSocket('ws://localhost:8080/analysis');

ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    ScriptureMonUI.updateProgressUI(data);
};
```

## 📱 Responsivo

### Desktop (1920x1080)
- Grid 2 colunas
- Janelas grandes
- Todas as features visíveis

### Tablet (1024x768)
- Grid 2 colunas reduzido
- Fonte menor
- Scroll vertical se necessário

### Mobile (< 768px)
- Grid 1 coluna
- Janelas em stack
- Touch controls

## 🎵 Sound Effects (Future)

### Sugestões de Sons
- **Navigate**: Beep curto (800Hz)
- **Confirm**: Beep alto (1200Hz)
- **Back**: Beep baixo (600Hz)
- **Error**: Buzz (400Hz)
- **Complete**: Jingle de vitória

### Implementação
```javascript
// Já está preparado em script.js
playSound('navigate');
playSound('confirm');
playSound('back');
```

## 🎨 Customização

### Alterar Cores
Edite as variáveis CSS em `style.css`:
```css
:root {
    --neon-blue: #4a9fff;     /* Mude para sua cor */
    --text-yellow: #ffdd00;   /* Cor de destaque */
    /* ... */
}
```

### Adicionar Nova Tela
1. Crie HTML em `index.html`:
```html
<div class="screen hidden" id="myNewScreen">
    <div class="grid-background"></div>
    <!-- Conteúdo -->
</div>
```

2. Adicione estilos em `style.css`

3. Adicione navegação em `script.js`:
```javascript
showScreen('myNewScreen');
```

## 🐛 Debug

### Console Logs
- Navegação: `🔊 Sound: navigate`
- Seleção: Log do item selecionado
- Erros: Stack trace completo

### Atalhos de Debug
- **1**: Main Menu
- **2**: Specialist Selection
- **3**: Analysis Progress
- **4**: Results Screen

## 📚 Referências

### Digimon World 3
- Platform: PlayStation 2 (2002)
- Interface: Menu-driven RPG
- Style: Futuristic blue grid
- Font: Pixel/bitmap
- Sound: Retro beeps

### Tecnologias
- HTML5
- CSS3 (Grid, Animations)
- Vanilla JavaScript
- Web Audio API

## 🎯 Features Futuras

- [ ] Animações de transição entre telas
- [ ] Particle effects no background
- [ ] Sound effects completos
- [ ] Integração com backend real
- [ ] WebSocket para updates real-time
- [ ] Modo fullscreen
- [ ] Gamepad support (PS2-style)
- [ ] Save/Load preferences
- [ ] Multiple themes
- [ ] Exportar resultados

## 📄 Licença

Parte do projeto **Scripturemon**.
Design inspirado em Digimon World 3 (Bandai).

---

**Desenvolvido com ❤️ e nostalgia PS2**
**Scripturemon v10.0 - Digimon Style UI**
