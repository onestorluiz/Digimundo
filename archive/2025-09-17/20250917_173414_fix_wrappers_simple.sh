#!/bin/bash
# Correção simples dos wrappers

WRAPPER_DIR="/Users/clubproducoes/Digimundo/claude_code/protection/wrappers"

# Corrige rm
cat > "$WRAPPER_DIR/rm" << 'EOF'
#!/bin/bash
source /Users/clubproducoes/Digimundo/claude_code/protection/wrapper_template.sh
if [[ "$@" == *"/Users/clubproducoes/Digimundo/scripturemon-champion"* ]]; then
    if ! check_auth; then
        show_claude_instructions
        exit 1
    fi
fi
/bin/rm "$@"
EOF
chmod +x "$WRAPPER_DIR/rm"

# Corrige cat
cat > "$WRAPPER_DIR/cat" << 'EOF'
#!/bin/bash
source /Users/clubproducoes/Digimundo/claude_code/protection/wrapper_template.sh
if [[ "$@" == *"/Users/clubproducoes/Digimundo/scripturemon-champion"* ]]; then
    if ! check_auth; then
        show_claude_instructions
        exit 1
    fi
fi
/bin/cat "$@"
EOF
chmod +x "$WRAPPER_DIR/cat"

echo "✅ Wrappers rm e cat corrigidos!"