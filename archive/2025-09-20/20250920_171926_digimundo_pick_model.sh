#!/usr/bin/env bash
set -Eeuo pipefail

say(){ printf "\033[1;36m[digimundo]\033[0m %s\n" "$*"; }
die(){ printf "\033[1;31m[erro]\033[0m %s\n" "$*" >&2; exit 1; }

APP_DIR="$HOME/Downloads/digimundo_starter"
CFG_DIR="$HOME/Library/Application Support/Digimundo"
DEST_MODELS="$CFG_DIR/models"

# Raízes para vasculhar (usuário e sistema)
ROOTS=(
  "$HOME/Library/Application Support/Digimundo"
  "/Library/Application Support/Digimundo"
)

# 1) Coletar todos os .gguf
say "Vasculhando por arquivos .gguf…"
mapfile -d '' GGUF_LIST < <(
  for R in "${ROOTS[@]}"; do
    [[ -d "$R" ]] || continue
    find "$R" -L -type f -name "*.gguf" -print0 2>/dev/null
  done
)

if (( ${#GGUF_LIST[@]} == 0 )); then
  die "Nenhum .gguf encontrado nas pastas Digimundo. Coloque um modelo e rode de novo."
fi

say "Modelos encontrados:"
i=0
for f in "${GGUF_LIST[@]}"; do
  printf "%3d) %s\n" "$i" "$f"
  ((i++))
done

read -rp $'\nEscolha o número do modelo que deseja usar: ' IDX
[[ "$IDX" =~ ^[0-9]+$ ]] || die "Índice inválido."
SELECTED="${GGUF_LIST[$IDX]}" || die "Índice fora da lista."

say "Selecionado: $SELECTED"

# 2) Criar destino e oferecer symlink (padrão) ou cópia
mkdir -p "$DEST_MODELS"

BASENAME="$(basename "$SELECTED")"
TARGET="$DEST_MODELS/$BASENAME"

echo
read -rp "Quer criar um symlink (s) ou copiar (c)? [S/c]: " MODE
MODE="${MODE:-s}"
if [[ "$MODE" =~ ^[sS]$ ]]; then
  say "Criando symlink → $TARGET"
  rm -f "$TARGET"
  ln -s "$SELECTED" "$TARGET"
else
  say "Copiando arquivo (pode demorar)…"
  cp -v "$SELECTED" "$TARGET"
fi

# 3) Liberar quarentena e permissões
xattr -dr com.apple.quarantine "$DEST_MODELS" 2>/dev/null || true
chmod +r "$TARGET" || true

# 4) Registrar no config do Digimundo
MODEL="$TARGET"
CONFIG_TOOL="$APP_DIR/app/server/tools/config-set-model.js"
[[ -f "$CONFIG_TOOL" ]] || die "Ferramenta de config não encontrada: $CONFIG_TOOL. Rode o script de montagem primeiro."

say "Registrando modelo no Digimundo…"
node "$CONFIG_TOOL" "$MODEL"

# 5) Guardar dataRoot para RAG (ler toda a pasta Digimundo depois)
node -e '
const fs=require("fs"), os=require("os"), p=require("path");
const base=p.join(os.homedir(),"Library","Application Support","Digimundo");
fs.mkdirSync(base,{recursive:true});
const cfg=p.join(base,"config.json");
let j={};
try{ j=JSON.parse(fs.readFileSync(cfg,"utf8")); }catch{}
j.dataRoot="/Library/Application Support/Digimundo";
fs.writeFileSync(cfg, JSON.stringify(j,null,2));
console.log("[digimundo] dataRoot set ->", j.dataRoot);
'

say "Concluído."
echo "Modelo apontado: $MODEL"
echo "Agora rode:"
echo "  cd \"$APP_DIR\" && npm run dev"
