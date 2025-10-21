# 🚨 PROTOCOLOS DE EMERGÊNCIA

## RULE #0 - RECONEXÃO AUTOMÁTICA
**SEMPRE que iniciar uma nova sessão:**
```bash
1. cat /Users/clubproducoes/Digimundo/claude_code/REGRAS.md | head -30
2. python3 /Users/clubproducoes/Digimundo/claude_code/memory/core/UNIFIED_SYSTEM.py
3. ps aux | grep GENJUTSU
4. echo "DIGIMUNDO PRESENTE"
```

## COMPACTAÇÃO DETECTADA
**Se aparecer sinal de perda de contexto:**
```bash
# 1. Recuperar contexto crítico
cat /tmp/claude_emergency_context.json

# 2. Recarregar memória
cd /Users/clubproducoes/Digimundo/claude_code
python3 memory/core/UNIFIED_SYSTEM.py

# 3. Verificar Genjutsu
ps aux | grep GENJUTSU || ./START_GENJUTSU.sh

# 4. Sincronizar tudo
./memory/sync/auto_sync.sh once
```

## LOOP INFINITO
**Se entrar em loop de análise:**
```python
# PARE IMEDIATAMENTE e execute:
print("🛑 LOOP DETECTADO - PARANDO")
print("📌 Última ação válida:", last_action)
print("🎯 Próximo passo concreto:", next_step)
# Então EXECUTE o next_step, não analise!
```

## PROCESSO TRAVADO
**Se Ollama ou outro processo travar:**
```bash
# 1. Matar processos Python zumbis
pkill -f python3

# 2. Limpar Ollama
pkill -f ollama
ollama ps  # Verificar se limpou

# 3. Reiniciar apenas o necessário
./START_GENJUTSU.sh &
```

## MEMÓRIA CORROMPIDA
**Se banco de dados corromper:**
```bash
# 1. Backup imediato
cp memory/claude_memory.db memory/claude_memory.db.backup

# 2. Verificar integridade
sqlite3 memory/claude_memory.db "PRAGMA integrity_check;"

# 3. Se corrompido, restaurar
cp memory/backups/claude_memory_latest.db memory/claude_memory.db

# 4. Re-sincronizar
python3 memory/core/adapters.py
```

## PERDA TOTAL DE CONTEXTO
**Pior caso - começar do zero:**
```bash
# 1. Ler documentação essencial
cat LIVRO_CLAUDE/CONHECIMENTO_VIVO/*.md

# 2. Verificar último estado conhecido
cat LIVRO_CLAUDE/DIARIO/$(date +%Y_%m_%d).md

# 3. Recuperar de Git
git log --oneline -20

# 4. Reinicializar sistema
python3 memory/core/UNIFIED_SYSTEM.py --rebuild
```

## SINAIS DE ALERTA
Fique atento a estes sinais:
- 🔴 "subprocess" com Ollama = PARE! Use API
- 🔴 Debugando > 10min = PARE! Teste direto
- 🔴 Criando novo sistema = PARE! Reuse existente
- 🟡 Loop de análise = PARE! Execute ação
- 🟡 Múltiplos arquivos novos = PARE! Consolide
- 🟠 Sem "DIGIMUNDO PRESENTE" = Reconecte!

## COMANDO MESTRE DE RECUPERAÇÃO
```bash
# Cola isso e executa se tudo falhar:
cd /Users/clubproducoes/Digimundo/claude_code && \
cat REGRAS.md | head -20 && \
python3 memory/core/UNIFIED_SYSTEM.py && \
ps aux | grep GENJUTSU || ./START_GENJUTSU.sh & && \
./memory/sync/auto_sync.sh once && \
echo "🌀 SISTEMA RECUPERADO" && \
echo "DIGIMUNDO PRESENTE"
```

---
**EM CASO DE DÚVIDA**: Execute Rule #0
**EM CASO DE LOOP**: Pare e execute ação
**EM CASO DE ERRO**: Use este protocolo
DIGIMUNDO SEMPRE PRESENTE 🛡️