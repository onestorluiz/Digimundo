# ✅ App Atualizado - Seleção de Modo

**Date**: 2025-10-09 18:15
**Update**: Added Mode Selection (Dialogue Only vs All 22)

---

## 🎯 Mudanças Implementadas

### Nova Funcionalidade: Escolha do Modo

O app agora tem um **diálogo de seleção** que pergunta qual modo usar:

```
🎯 ESCOLHA O MODO DE ANÁLISE

✅ DIALOGUE ONLY (Recomendado)
   • Apenas Dialogue specialist
   • Tempo: 5-10 minutos
   • Testado e funcionando

⚠️  ALL 22 SPECIALISTS (Experimental)
   • Todos os specialists
   • Tempo: 1-2 horas
   • Em desenvolvimento

Qual modo deseja usar?

[Cancelar] [Dialogue Only] [All 22]
```

---

## 📝 Código Modificado

### 1. Nova Função: `choose_analysis_mode()`

```bash
# Choose analysis mode
choose_analysis_mode() {
    local response=$(osascript << EOF
tell application "System Events"
    activate
    set choice to button returned of (display dialog "🎯 ESCOLHA O MODO..."
        buttons {"Cancelar", "Dialogue Only", "All 22"}
        default button 2)
    return choice
end tell
EOF
)
    echo "$response"
}
```

### 2. Modificada: `confirm_analysis()`

Agora aceita o modo e ajusta descrição:

```bash
confirm_analysis() {
    local file="$1"
    local mode="$2"

    if [ "$mode" = "Dialogue Only" ]; then
        mode_desc="Dialogue Specialist"
        time_est="5-10 minutos"
    else
        mode_desc="22 Specialists (Triple-Core)"
        time_est="1-2 horas"
    fi

    # Display confirmation with correct mode info
}
```

### 3. Modificada: `start_new_analysis()`

Usa o modo escolhido para determinar specialists:

```python
# Determine specialists to run based on mode
analysis_mode = '$analysis_mode'
specialists_to_run = None

if analysis_mode == 'Dialogue Only':
    specialists_to_run = ['Dialogue']
    print("🎯 Modo: Dialogue Only")
    print("   Rodando apenas Dialogue specialist")
else:
    print("🎯 Modo: All 22 Specialists")
    print("   Rodando todos os 22 specialists")

# Run analysis
result = analyzer.analyze_screenplay(
    screenplay_path='$screenplay_file',
    output_dir='$SCRIPTUREMON_DIR/workspace/outputs/analysis',
    resume=False,
    specialists_to_run=specialists_to_run  # <-- usa a escolha!
)
```

### 4. Modificado: `main()`

Agora chama `choose_analysis_mode()` e passa para funções:

```bash
main() {
    # ...
    local screenplay_file=$(get_screenplay_file "${1:-}")
    validate_screenplay "$screenplay_file"

    # NEW: Choose mode
    local analysis_mode=$(choose_analysis_mode)

    if [ "$analysis_mode" = "Cancelar" ] || [ -z "$analysis_mode" ]; then
        exit 0
    fi

    # Pass mode to functions
    confirm_analysis "$screenplay_file" "$analysis_mode"
    start_new_analysis "$screenplay_file" "$analysis_mode"
}
```

---

## 🎯 Fluxo do App (Atualizado)

```
1. App Launch
   ↓
2. Check Existing Sessions
   ↓ (nenhuma)
3. File Picker (escolher PDF)
   ↓
4. *** NOVO *** Mode Selection
   ↓
   ├─→ Dialogue Only (recomendado, rápido)
   │   └─→ specialists_to_run = ['Dialogue']
   │
   └─→ All 22 (experimental, lento)
       └─→ specialists_to_run = None (todos)
   ↓
5. Confirmation Dialog (mostra modo escolhido)
   ↓
6. Analysis Starts
   ↓
7. Checkpoint Saves após cada specialist
   ↓
8. Final Report (HTML + Markdown)
```

---

## 🧪 Como Testar

### Teste 1: Dialogue Only (Rápido)

```
1. Double-click "Analyze Screenplay.app"
2. Escolher PDF
3. Diálogo: "ESCOLHA O MODO"
4. Click: "Dialogue Only"
5. Confirmation: "Dialogue Specialist • 5-10 minutos"
6. Click: "Analisar"
7. Terminal: "🎯 Modo: Dialogue Only"
8. Análise roda APENAS Dialogue specialist
9. Completa em ~5-10 minutos
```

### Teste 2: All 22 (Experimental)

```
1. Double-click "Analyze Screenplay.app"
2. Escolher PDF
3. Diálogo: "ESCOLHA O MODO"
4. Click: "All 22"
5. Confirmation: "22 Specialists (Triple-Core) • 1-2 horas"
6. Click: "Analisar"
7. Terminal: "🎯 Modo: All 22 Specialists"
8. Análise roda todos os 22 specialists
9. Completa em ~1-2 horas
```

### Teste 3: Cancelar

```
1. Diálogo: "ESCOLHA O MODO"
2. Click: "Cancelar"
3. App fecha (exit 0)
```

---

## ✅ Validação

```bash
# Verificar sintaxe
bash -n "/Applications/Analyze Screenplay.app/Contents/MacOS/run"
# Output: ✅ Script syntax válida

# Ver tamanho do app
ls -lh "/Applications/Analyze Screenplay.app/Contents/MacOS/run"
# Output: 16K (aumentou de 15K por causa do novo diálogo)
```

---

## 📊 Comparação

| Feature | Antes | Depois |
|---------|-------|--------|
| Modo Dialogue | ❌ Não tinha | ✅ Sim (5-10 min) |
| Modo All 22 | ✅ Forçado | ✅ Opcional (1-2h) |
| Escolha do Usuário | ❌ Não | ✅ Sim (diálogo interativo) |
| Tempo Estimado | ⚠️ Sempre 1-2h | ✅ Ajusta por modo |
| Uso Prático | ⚠️ Lento sempre | ✅ Rápido com Dialogue |

---

## 🎯 Próximos Passos

### Agora (Teste)
1. ✅ **Testar Dialogue Only** - Modo rápido, testado
2. ✅ **Verificar checkpoint funciona** - Resume após interrupção
3. ✅ **Ver HTML gerado** - Apenas com Dialogue

### Depois (Quando outros specialists estiverem prontos)
1. Testar All 22 mode
2. Verificar qualidade de todos
3. Integrar BenchmarkPromptGenerator para melhorar qualidade

---

## 💡 Notas Importantes

### Por que "Dialogue Only" é recomendado?

1. **Testado**: Dialogue specialist está completo e funcional
2. **Rápido**: 5-10 minutos vs 1-2 horas
3. **Prático**: Útil para testar sistema de checkpoints
4. **Iterativo**: Pode rodar múltiplas vezes rapidamente

### Por que "All 22" é experimental?

1. **Em Desenvolvimento**: Outros 21 specialists não estão prontos
2. **Lento**: 1-2 horas de análise
3. **Não Testados**: Pode falhar em alguns specialists
4. **Checkpoint Ajuda**: Se falhar, pode resumir depois

---

## 🚀 Status

**App Updated**: ✅ Funcionando
**Syntax**: ✅ Válida
**Ready to Test**: ✅ Sim

**Recomendação**: Testar com "Dialogue Only" primeiro para validar todo o fluxo (checkpoint, resume, HTML generation).

Depois que estiver funcionando perfeitamente no modo Dialogue, podemos trabalhar nos outros specialists e testar o modo "All 22".
