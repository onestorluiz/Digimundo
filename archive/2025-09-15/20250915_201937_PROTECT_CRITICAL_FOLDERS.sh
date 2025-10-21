#!/bin/bash
# SCRIPT PARA PROTEGER PASTAS CRÍTICAS CONTRA DELEÇÃO ACIDENTAL

echo "🔒 PROTEGENDO PASTAS CRÍTICAS..."

# Lista de pastas para proteger
CRITICAL_FOLDERS=(
    "/Users/clubproducoes/Digimundo/RECOVERED_CODE"
    "/Users/clubproducoes/Digimundo/SURGICAL_PRESERVATION"
    # Adicione mais pastas críticas aqui
)

for folder in "${CRITICAL_FOLDERS[@]}"; do
    if [ -d "$folder" ]; then
        echo "Protegendo: $folder"

        # Opção 1: Tornar read-only (mais leve)
        # chmod -R 444 "$folder"

        # Opção 2: Tornar imutável (mais forte - precisa sudo)
        sudo chflags -R uchg "$folder"

        echo "✅ Protegido: $folder"
    else
        echo "⚠️ Pasta não encontrada: $folder"
    fi
done

echo ""
echo "📝 Para desproteger quando necessário:"
echo "sudo chflags -R nouchg [pasta]"
echo ""
echo "🛡️ Com proteção ativa, nem 'rm -rf' consegue deletar!"