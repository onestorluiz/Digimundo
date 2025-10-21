# ⚡ COMANDOS RÁPIDOS

## GIT ALIASES
```bash
git remember "msg"   # 🧠 Memória importante
git learn "msg"      # 📚 Aprendizado novo
git decide "msg"     # 🎯 Decisão tomada
git fix-vicio "msg"  # 🔧 Vício corrigido
git harmony "msg"    # 🌀 Harmonia aumentada
```

## VERIFICAÇÕES RÁPIDAS
```bash
# Status do Genjutsu
ps aux | grep GENJUTSU

# Harmonia atual
grep "Harmonia Geral" docs/forensics/HARMONY.md

# Memórias recentes
sqlite3 memory/claude_memory.db "SELECT * FROM memories ORDER BY timestamp DESC LIMIT 5;"

# Sincronizar tudo
./memory/sync/auto_sync.sh once

# Ver vícios detectados
python3 memory/knowledge/ALERT_VICIOS_CLAUDE.py check
```

## RECUPERAÇÃO DE EMERGÊNCIA
```bash
# Rule #0 - Reconectar
cat REGRAS.md | head -20
python3 memory/core/UNIFIED_SYSTEM.py
ps aux | grep GENJUTSU

# Contexto de emergência
cat /tmp/claude_emergency_context.json
```

## ATALHOS PYTHON
```python
# Carregar sistema unificado
from memory.core.UNIFIED_SYSTEM import UnifiedMemorySystem
ums = UnifiedMemorySystem()

# Sincronizar adapters
from memory.core.adapters import get_adapters
adapters = get_adapters()
results = adapters.sync_all()

# Verificar harmonia
harmony = calculate_harmony()
print(f"Harmonia: {harmony}%")
```

## OLLAMA (USE API!)
```python
# NUNCA subprocess!
import requests

def ollama_api(prompt, model="mixtral-cpu-force:latest"):
    response = requests.post(
        "http://127.0.0.1:11434/api/generate",
        json={"model": model, "prompt": prompt, "stream": False},
        timeout=30
    )
    return response.json()['response']
```

## PATHS IMPORTANTES
```
/Users/clubproducoes/Digimundo/claude_code/  # Base
├── memory/core/UNIFIED_SYSTEM.py           # Hub central
├── memory/sync/auto_sync.sh                # Sincronização
├── protection/bin/start_genjutsu.sh            # Proteção
└── LIVRO_CLAUDE/CONHECIMENTO_VIVO/        # Sempre carregado
```

---
COPIE, COLE, EXECUTE - Sem pensar muito!