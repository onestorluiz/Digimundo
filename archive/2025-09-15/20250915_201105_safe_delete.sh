#!/bin/bash
# SAFE DELETE - Sempre usar isso ao invés de rm -rf

TARGET="$1"

# Proteções hardcoded
if [[ "$TARGET" == *"validation"* ]] || \
   [[ "$TARGET" == *"main"* ]] || \
   [[ "$TARGET" == *"core"* ]] || \
   [[ "$TARGET" == *"src"* ]] || \
   [[ "$TARGET" == *"apps"* ]] || \
   [[ "$TARGET" == *"LEGACY_SYSTEMS"* ]]; then

   echo "🚨 BLOQUEADO: Path contém palavra protegida"
   echo "Target: $TARGET"
   echo "Razão: Matches protected pattern"
   exit 1
fi

# Verificar tamanho
SIZE=$(du -sh "$TARGET" 2>/dev/null | cut -f1)
echo "📊 Tamanho: $SIZE"

# Se maior que 100MB, exigir confirmação
if [[ $(du -s "$TARGET" 2>/dev/null | cut -f1) -gt 100000 ]]; then
   echo "⚠️ AVISO: Maior que 100MB!"
   echo "Path: $TARGET"
   echo "Digite 'CONFIRMO DELETAR $TARGET' para proceder:"
   read CONFIRM
   if [[ "$CONFIRM" != "CONFIRMO DELETAR $TARGET" ]]; then
      echo "❌ Cancelado"
      exit 1
   fi
fi

# Mover para lixeira ao invés de deletar
echo "♻️ Movendo para ~/.Trash ao invés de deletar permanentemente..."
mv "$TARGET" ~/.Trash/
echo "✅ Movido para lixeira (recuperável)"