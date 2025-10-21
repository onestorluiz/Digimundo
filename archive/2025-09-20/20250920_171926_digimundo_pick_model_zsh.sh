#!/bin/zsh
set -e

say(){ print -P "%F{cyan}[digimundo]%f $*"; }
die(){ print -P "%F{red}[erro]%f $*" >&2; exit 1; }

APP_DIR="$HOME/Downloads/digimundo_starter"
CFG_DIR="$HOME/Library/Application Support/Digimundo"
DEST_MODELS="$CFG_DIR/models"

# Locais comuns (usuário, sistema, Ollama, LM Studio, seus docs)
typeset -a ROOTS
ROOTS=(
  "$HOME/Library/Application Support/Digimundo"
  "/Library/Application Support/Digimundo"
  "$HOME/.ollama/models"
  "$HOME/Library/Application Support/Ollama/models"
  "$HOME/Library/Application Support/LM Studio/models"
  "$HOME/Documents"
  "$HOME/Downloads"
)

# Coleta candidatos: .gguf diretos e blobs do Ollama (sha256)
typeset -a CAND
say "Vasculhando por modelos (.gguf e blobs GGUF)…"
for R in $ROOTS; do
  [[ -d "$R" ]] || continue
  # .gguf
  while IFS= read -r -d '' f; do CAND+=("$f"); done < <(find "$R" -type f -name "*.gguf" -print0 2>/dev/null)
  # blobs (sem extensão) - testamos se tem mágica GGUF
  while IFS= read -r -d '' f; do
    # lê 4 bytes e confere "GGUF" (47 47 55 46) ou "gguf" (67 67 75 66)
    magic="$(hexdump -n 4 -ve '1/1 "%02x"' "$f" 2>/dev/null || true)"
    if [[ "$magic" == "47475546" || "$magic" == "67677566" ]]; then
      CAND+=("$f")
    fi
  done < <(find "$R" -type f -path "*/blobs/sha256/*" -size +40M -print0 2>/dev/null)
done

(( ${#CAND[@]} > 0 )) || die "Nenhum modelo encontrado. Coloque um .gguf em alguma dessas pastas e rode de novo."

# Lista numerada
say "Modelos encontrados:"
i=1
for f in $CAND; do
  sz=$(stat -f%z "$f" 2>/dev/null || echo 0)
  mb=$(( sz / 1048576 ))
  echo "$i) $f  (${mb} MB)"
  ((i++))
done

print -n "Escolha o número do modelo: "
read sel
[[ "$sel" == <-> ]] || die "Índice inválido."
CHOSEN="${CAND[$sel]}" || die "Índice fora da lista."
say "Selecionado: $CHOSEN"

# Destino
mkdir -p "$DEST_MODELS"
base="${CHOSEN:t}"
# Se não tiver extensão .gguf (caso blob), acrescenta para ficar legível
if [[ "${base:e}" != "gguf" ]]; then
  base="${base}.gguf"
fi
TARGET="$DEST_MODELS/$base"

print -n "Quer criar link simbólico (s) ou copiar (c)? [S/c]: "
read mode
[[ -z "$mode" ]] && mode="s"
if [[ "$mode" == [sS] ]]; then
  say "Criando symlink -> $TARGET"
  rm -f "$TARGET"
  ln -s "$CHOSEN" "$TARGET"
else
  say "Copiando arquivo (pode demorar)…"
  cp -v "$CHOSEN" "$TARGET"
fi

# Libera quarentena e garante leitura
xattr -dr com.apple.quarantine "$TARGET" 2>/dev/null || true
chmod +r "$TARGET" 2>/dev/null || true

# Aponta no config do Digimundo
CONFIG_TOOL="$APP_DIR/app/server/tools/config-set-model.js"
[[ -f "$CONFIG_TOOL" ]] || die "Ferramenta de config não encontrada: $CONFIG_TOOL (rode primeiro o montar_digimundo.sh)."
say "Registrando modelo no Digimundo…"
node "$CONFIG_TOOL" "$TARGET"

# Guarda dataRoots para o RAG (leremos tudo depois)
node - <<'JS'
const fs=require('fs'), os=require('os'), p=require('path');
const base=p.join(os.homedir(),'Library','Application Support','Digimundo');
fs.mkdirSync(base,{recursive:true});
const cfg=p.join(base,'config.json');
let j={}; try{ j=JSON.parse(fs.readFileSync(cfg,'utf8')); }catch{}
j.dataRoots=[p.join(os.homedir(),'Library','Application Support','Digimundo'), '/Library/Application Support/Digimundo'];
fs.writeFileSync(cfg, JSON.stringify(j,null,2));
console.log('[digimundo] dataRoots set no config.json');
JS

say "Concluído."
echo "Modelo apontado: $TARGET"
echo "Para iniciar:  cd \"$APP_DIR\" && npm run dev"
