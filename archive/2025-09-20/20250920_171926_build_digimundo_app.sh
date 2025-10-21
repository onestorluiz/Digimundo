#!/usr/bin/env bash
set -Eeuo pipefail

# ================================
# Digimundo.app – Builder Script
# v2025-08-08
# ================================
# O que faz:
# - Copia o app base para /Applications/Digimundo.app (com backup se existir)
# - Rebrand não-invasivo do Info.plist (PlistBuddy: preserva chaves do app original)
# - Ajusta LSEnvironment (DATA_DIR/WORK_DIR)
# - Opcional: renomeia o executável p/ "Digimundo"
# - Instala Frameworks a partir de ~/Downloads/Frameworks.zip (qualquer estrutura)
# - Opcional: gera digimundo.icns a partir de --icon-png
# - Desativa auto-update (app-update.yml) se existir
# - Reassina (ad-hoc por padrão) e valida com codesign/spctl
#
# Personalização por FLAGS ou variáveis de ambiente:
#   --src-app "/Applications/AnythingLLM.app"
#   --dest-app "/Applications/Digimundo.app"
#   --frameworks-zip "$HOME/Downloads/Frameworks.zip"
#   --data-dir "$HOME/Digimundo"
#   --work-dir "$HOME"
#   --rename-exec (sem valor; liga o rename)
#   --icon-png "/caminho/seu_icone.png"   (gera digimundo.icns)
#   --sign "Developer ID Application: SEU NOME (TEAMID)"  (por padrão é ad-hoc "-")
#   --skip-sign         (não assina; útil para testes rápidos)
#   --dry-run           (só imprime o que faria)
#
# Exemplos:
#   ./build_digimundo_app.sh
#   ./build_digimundo_app.sh --rename-exec --icon-png "$HOME/Downloads/logo.png"
#   ./build_digimundo_app.sh --sign "Developer ID Application: Nome (TEAMID)"
#   DRY_RUN=true ./build_digimundo_app.sh
# ================================

# ---------- Defaults ----------
SRC_APP="${SRC_APP:-/Applications/AnythingLLM.app}"
DEST_APP="${DEST_APP:-/Applications/Digimundo.app}"
FW_ZIP="${FW_ZIP:-$HOME/Downloads/Frameworks.zip}"
DATA_DIR="${DATA_DIR:-$HOME/Digimundo}"
WORK_DIR="${WORK_DIR:-$HOME}"
RENAME_EXEC="${RENAME_EXEC:-false}"
ICON_PNG="${ICON_PNG:-}"
SIGN_IDENTITY="${SIGN_IDENTITY:--}"    # "-" = ad-hoc
SKIP_SIGN="${SKIP_SIGN:-false}"
DRY_RUN="${DRY_RUN:-false}"

# ---------- Colors ----------
c_cyan="\033[1;36m"; c_red="\033[1;31m"; c_yellow="\033[1;33m"; c_reset="\033[0m"

log(){ printf "${c_cyan}[Digimundo]${c_reset} %s\n" "$*"; }
warn(){ printf "${c_yellow}[Aviso]${c_reset} %s\n" "$*"; }
err(){ printf "${c_red}[Erro]${c_reset} %s\n" "$*" >&2; }
die(){ err "$1"; exit 1; }

trap 'err "Falha na linha $LINENO: $BASH_COMMAND"; exit 1' ERR

# ---------- Helpers ----------
run() {
  if [[ "$DRY_RUN" == "true" ]]; then
    printf "[dry-run] %s\n" "$*" 
  else
    eval "$@"
  fi
}

need() { command -v "$1" >/dev/null || die "Dependência ausente: $1"; }

set_plist_key() {
  local plist="$1" key="$2" type="$3" value="$4"
  /usr/libexec/PlistBuddy -c "Set :$key $value" "$plist" 2>/dev/null || \
  /usr/libexec/PlistBuddy -c "Add :$key $type $value" "$plist"
}

ensure_plist_key() {
  local plist="$1" key="$2" type="$3" value="$4"
  /usr/libexec/PlistBuddy -c "Print :$key" "$plist" >/dev/null 2>&1 || \
  /usr/libexec/PlistBuddy -c "Add :$key $type $value" "$plist" >/dev/null
}

# ---------- Parse flags ----------
while [[ $# -gt 0 ]]; do
  case "$1" in
    --src-app)        SRC_APP="$2"; shift 2;;
    --dest-app)       DEST_APP="$2"; shift 2;;
    --frameworks-zip) FW_ZIP="$2"; shift 2;;
    --data-dir)       DATA_DIR="$2"; shift 2;;
    --work-dir)       WORK_DIR="$2"; shift 2;;
    --rename-exec)    RENAME_EXEC="true"; shift 1;;
    --icon-png)       ICON_PNG="$2"; shift 2;;
    --sign)           SIGN_IDENTITY="$2"; shift 2;;
    --skip-sign)      SKIP_SIGN="true"; shift 1;;
    --dry-run)        DRY_RUN="true"; shift 1;;
    -h|--help)
      cat <<HLP
Uso:
  $(basename "$0") [opções]

Opções:
  --src-app PATH          App base (padrão: $SRC_APP)
  --dest-app PATH         App destino (padrão: $DEST_APP)
  --frameworks-zip ZIP    Arquivo Frameworks.zip (padrão: $FW_ZIP)
  --data-dir PATH         DATA_DIR (padrão: $DATA_DIR)
  --work-dir PATH         WORK_DIR (padrão: $WORK_DIR)
  --rename-exec           Renomeia executável para "Digimundo"
  --icon-png PNG          Gera digimundo.icns em Resources/
  --sign ID               Identidade do codesign (padrão: ad-hoc "-")
  --skip-sign             Não assinar no final
  --dry-run               Mostra o que faria, sem executar
HLP
      exit 0;;
    *) die "Opção desconhecida: $1";;
  esac
done

# ---------- Pre-flight ----------
need /usr/libexec/PlistBuddy
need unzip
need codesign
need spctl
need xattr
need ditto
[[ -d "$SRC_APP/Contents" ]] || die "App base não encontrado: $SRC_APP"
[[ -f "$FW_ZIP" ]] || die "Frameworks.zip não encontrado: $FW_ZIP"

# ---------- Copiar app base ----------
if [[ -e "$DEST_APP" ]]; then
  local_bkp="${DEST_APP%.app}.backup.$(date +%Y%m%d-%H%M%S).app"
  log "Destino já existe. Fazendo backup em: $local_bkp"
  run "mv \"$DEST_APP\" \"$local_bkp\""
fi
log "Copiando base -> $DEST_APP (usando ditto para preservar metadados)"
run "ditto \"$SRC_APP\" \"$DEST_APP\""

PLIST="$DEST_APP/Contents/Info.plist"
[[ -f "$PLIST" ]] || die "Info.plist não encontrado em $PLIST"

EXEC_NAME="$(/usr/libexec/PlistBuddy -c 'Print :CFBundleExecutable' \"$PLIST\" 2>/dev/null || true)"
[[ -n "$EXEC_NAME" ]] || die "Não foi possível ler CFBundleExecutable."

# ---------- (Opcional) renomear executável ----------
if [[ "$RENAME_EXEC" == "true" ]]; then
  if [[ -f "$DEST_APP/Contents/MacOS/$EXEC_NAME" ]]; then
    log "Renomeando executável: $EXEC_NAME -> Digimundo"
    run "mv \"$DEST_APP/Contents/MacOS/$EXEC_NAME\" \"$DEST_APP/Contents/MacOS/Digimundo\""
    EXEC_NAME="Digimundo"
  else
    warn "Executável $EXEC_NAME não encontrado em Contents/MacOS. Mantendo nome original."
  fi
fi

# ---------- Rebrand mínimo e seguro no Info.plist ----------
log "Aplicando rebrand no Info.plist (preservando chaves do app original)"
run "/usr/libexec/PlistBuddy -c 'Print' \"$PLIST\" >/dev/null"  # valida plist

# Básico
run "bash -lc '/usr/libexec/PlistBuddy -c \"Delete :CFBundleName\" \"$PLIST\" >/dev/null 2>&1 || true'"
set_plist_key "$PLIST" "CFBundleName" "string" "Digimundo"
run "bash -lc '/usr/libexec/PlistBuddy -c \"Delete :CFBundleDisplayName\" \"$PLIST\" >/dev/null 2>&1 || true'"
set_plist_key "$PLIST" "CFBundleDisplayName" "string" "Digimundo"
set_plist_key "$PLIST" "CFBundleIdentifier" "string" "com.digimundo.app"
set_plist_key "$PLIST" "CFBundleVersion" "string" "1.0.0"
set_plist_key "$PLIST" "CFBundleShortVersionString" "string" "1.0.0"
set_plist_key "$PLIST" "CFBundleExecutable" "string" "$EXEC_NAME"
set_plist_key "$PLIST" "CFBundlePackageType" "string" "APPL"

# Ícone
ensure_plist_key "$PLIST" "CFBundleIconFile" "string" "digimundo.icns"
run "mkdir -p \"$DEST_APP/Contents/Resources\""
if [[ -n "$ICON_PNG" ]]; then
  if command -v sips >/dev/null && command -v iconutil >/dev/null; then
    log "Gerando digimundo.icns a partir de: $ICON_PNG"
    tmp_iconset="$(mktemp -d)/digimundo.iconset"
    run "mkdir -p \"$tmp_iconset\""
    for s in 16 32 64 128 256 512; do
      run "sips -z $s $s \"$ICON_PNG\" --out \"$tmp_iconset/icon_${s}x${s}.png\" >/dev/null"
      run "sips -z $((s*2)) $((s*2)) \"$ICON_PNG\" --out \"$tmp_iconset/icon_${s}x${s}@2x.png\" >/dev/null"
    done
    run "iconutil -c icns \"$tmp_iconset\" -o \"$DEST_APP/Contents/Resources/digimundo.icns\""
    run "rm -rf \"$(dirname \"$tmp_iconset\")\""
  else
    warn "sips/iconutil não encontrados; criando placeholder de ícone (sem .icns real)."
    run "touch \"$DEST_APP/Contents/Resources/digimundo.icns\""
  fi
else
  # Se não fornecer PNG, mantém/usa o que existir; se não houver, cria placeholder
  [[ -f "$DEST_APP/Contents/Resources/digimundo.icns" ]] || run "touch \"$DEST_APP/Contents/Resources/digimundo.icns\""
fi

# ATS para localhost
ensure_plist_key "$PLIST" "NSAppTransportSecurity" "dict" ""
ensure_plist_key "$PLIST" "NSAppTransportSecurity:NSAllowsArbitraryLoads" "bool" "true"
ensure_plist_key "$PLIST" "NSAppTransportSecurity:NSAllowsLocalNetworking" "bool" "true"
ensure_plist_key "$PLIST" "NSAppTransportSecurity:NSExceptionDomains" "dict" ""
ensure_plist_key "$PLIST" "NSAppTransportSecurity:NSExceptionDomains:localhost" "dict" ""
ensure_plist_key "$PLIST" "NSAppTransportSecurity:NSExceptionDomains:localhost:NSIncludesSubdomains" "bool" "false"
ensure_plist_key "$PLIST" "NSAppTransportSecurity:NSExceptionDomains:localhost:NSTemporaryExceptionAllowsInsecureHTTPLoads" "bool" "true"
ensure_plist_key "$PLIST" "NSAppTransportSecurity:NSExceptionDomains:127.0.0.1" "dict" ""
ensure_plist_key "$PLIST" "NSAppTransportSecurity:NSExceptionDomains:127.0.0.1:NSIncludesSubdomains" "bool" "false"
ensure_plist_key "$PLIST" "NSAppTransportSecurity:NSExceptionDomains:127.0.0.1:NSTemporaryExceptionAllowsInsecureHTTPLoads" "bool" "true"

# URL Scheme digimundo://
if ! /usr/libexec/PlistBuddy -c "Print :CFBundleURLTypes" "$PLIST" >/dev/null 2>&1; then
  run "/usr/libexec/PlistBuddy -c 'Add :CFBundleURLTypes array' \"$PLIST\""
  run "/usr/libexec/PlistBuddy -c 'Add :CFBundleURLTypes:0 dict' \"$PLIST\""
  run "/usr/libexec/PlistBuddy -c 'Add :CFBundleURLTypes:0:CFBundleURLName string Digimundo' \"$PLIST\""
  run "/usr/libexec/PlistBuddy -c 'Add :CFBundleURLTypes:0:CFBundleTypeRole string Editor' \"$PLIST\""
  run "/usr/libexec/PlistBuddy -c 'Add :CFBundleURLTypes:0:CFBundleURLSchemes array' \"$PLIST\""
  run "/usr/libexec/PlistBuddy -c 'Add :CFBundleURLTypes:0:CFBundleURLSchemes:0 string digimundo' \"$PLIST\""
fi

# LSEnvironment
ensure_plist_key "$PLIST" "LSEnvironment" "dict" ""
set_plist_key "$PLIST" "LSEnvironment:DATA_DIR" "string" "$DATA_DIR"
set_plist_key "$PLIST" "LSEnvironment:WORK_DIR" "string" "$WORK_DIR"

# Compat extras
ensure_plist_key "$PLIST" "LSMinimumSystemVersion" "string" "12.0"
ensure_plist_key "$PLIST" "NSHighResolutionCapable" "bool" "true"
ensure_plist_key "$PLIST" "NSSupportsAutomaticGraphicsSwitching" "bool" "true"
ensure_plist_key "$PLIST" "NSRequiresAquaSystemAppearance" "bool" "false"

# ---------- Neutralizar updater (se houver) ----------
if [[ -f "$DEST_APP/Contents/Resources/app-update.yml" ]]; then
  log "Neutralizando app-update.yml (desligando auto-update)"
  run "cat > \"$DEST_APP/Contents/Resources/app-update.yml\" <<'YML'
provider: generic
channel: disabled
url: https://digimundo.invalid/updates/
updaterCacheDirName: digimundo-desktop-updater
YML"
fi

# ---------- Frameworks ----------
log "Instalando Frameworks de: $FW_ZIP"
cd "$DEST_APP/Contents"
if [[ -d Frameworks ]]; then
  run "mv Frameworks Frameworks.backup.$(date +%Y%m%d%H%M%S)"
fi
run "unzip -q \"$FW_ZIP\" -d ."
if [[ ! -d Frameworks ]]; then
  run "mkdir -p Frameworks"
  # Move tudo que NÃO é Resources/Info.plist/PkgInfo/_CodeSignature para Frameworks/
  run "bash -lc 'shopt -s dotglob nullglob; for f in *; do case \"\$f\" in Frameworks|Resources|Info.plist|PkgInfo|_CodeSignature) continue;; esac; mv \"\$f\" Frameworks/ 2>/dev/null || true; done'"
fi
run "chmod -R u+rwX,go+rX Frameworks"

# Verificação de arquitetura (apenas aviso)
if command -v file >/dev/null; then
  log "Checando arquitetura dos binários em Frameworks (apenas informativo)"
  run "bash -lc 'shopt -s nullglob; while IFS= read -r -d \"\" bin; do file -h \"\$bin\"; done < <(find Frameworks -type f -perm -111 -print0)'"
fi

# ---------- Assinar e validar ----------
cd /
if [[ "$SKIP_SIGN" == "true" ]]; then
  warn "Assinatura pulada (--skip-sign). Você pode assinar depois com:"
  echo "  codesign --force --deep --sign - --options runtime \"$DEST_APP\""
else
  log "Assinando app (identity: $SIGN_IDENTITY)"
  run "codesign --force --deep --sign \"$SIGN_IDENTITY\" --options runtime \"$DEST_APP\""
  run "xattr -dr com.apple.quarantine \"$DEST_APP\" || true"
  log "Verificando assinatura"
  run "codesign --verify --deep --strict --verbose=2 \"$DEST_APP\""
  run "spctl --assess --type execute -vv \"$DEST_APP\" || true"
fi

log "Pronto! App em: $DEST_APP"
if [[ "$DRY_RUN" == "false" ]]; then
  log "Abrindo o app..."
  run "open \"$DEST_APP\""
fi

