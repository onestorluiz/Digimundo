#!/bin/bash

# 🔧 ATUALIZAR DIGIMUNDO.APP PARA ABRIR CLAUDE CODE CORRETAMENTE

echo "🔧 Atualizando Digimundo.app..."

# Atualizar o script do app
cat > "$HOME/Desktop/Digimundo.app/Contents/MacOS/Digimundo" << 'APP_SCRIPT'
#!/bin/bash

# Digimundo.app launcher script com Claude Code

osascript << 'END_SCRIPT'
tell application "Terminal"
    activate
    
    -- Criar nova janela com PATH correto
    set newWindow to do script "source ~/.zshrc 2>/dev/null || source ~/.bash_profile 2>/dev/null; export PATH=\"$HOME/.local/bin:/opt/homebrew/opt/node@20/bin:/opt/homebrew/bin:/usr/local/bin:$PATH\"; cd /Users/clubproducoes/Digimundo/digimundo_starter && bash CLAUDE_DIGIMUNDO_LAUNCHER.sh"
    
    -- Configurar janela
    tell window 1
        set size to {1200, 800}
        set position to {100, 50}
    end tell
end tell
END_SCRIPT
APP_SCRIPT

# Dar permissão de execução
chmod +x "$HOME/Desktop/Digimundo.app/Contents/MacOS/Digimundo"

echo "✅ Digimundo.app atualizado!"
echo ""
echo "Agora o app irá:"
echo "  1. Iniciar o servidor Digimundo"
echo "  2. Abrir Claude Code com contexto"
echo "  3. Configurar PATH corretamente"
