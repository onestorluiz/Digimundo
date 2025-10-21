# 🔍 PADRÕES DE BUSCA NO ARCHIVE

## COMANDOS RÁPIDOS PARA ENCONTRAR ARQUIVOS

### 1. BUSCAR POR PALAVRA-CHAVE
```bash
# Em todo archive
grep -r "ProcessLock" /Users/clubproducoes/Digimundo/archive/

# Só em arquivos .md
find /Users/clubproducoes/Digimundo/archive -name "*.md" -exec grep -l "Ollama" {} \;

# Com contexto (3 linhas antes/depois)
grep -r -A 3 -B 3 "subprocess" /Users/clubproducoes/Digimundo/archive/2025-09-*/
```

### 2. BUSCAR POR DATA NO NOME
```bash
# Arquivos do dia 14 de agosto
find /Users/clubproducoes/Digimundo/archive -name "20250814_*"

# Arquivos de setembro
find /Users/clubproducoes/Digimundo/archive -name "202509*"

# Arquivos das 15h do dia 19
find /Users/clubproducoes/Digimundo/archive -name "20250919_15*"
```

### 3. BUSCAR POR TIPO
```bash
# Todos os Python
find /Users/clubproducoes/Digimundo/archive -name "*.py"

# Todos os scripts
find /Users/clubproducoes/Digimundo/archive \( -name "*.sh" -o -name "*.py" \)

# Documentação
find /Users/clubproducoes/Digimundo/archive -name "*.md" | grep -i "doc"
```

### 4. BUSCAR ARQUIVOS IMPORTANTES
```bash
# Bugs documentados
find /Users/clubproducoes/Digimundo/archive -name "*BUG*" -o -name "*ERROR*"

# Planos e análises
find /Users/clubproducoes/Digimundo/archive -name "*PLAN*" -o -name "*ANALYSIS*"

# Sistemas críticos
find /Users/clubproducoes/Digimundo/archive -name "*UNIFIED*" -o -name "*GENJUTSU*"
```

## 📁 LOCALIZAÇÕES CONHECIDAS

### PROBLEMAS E SOLUÇÕES
```bash
# O bug do ProcessLock
/archive/2025-09-22/code/ProcessLock.py
/archive/*/ProcessLock*

# Descoberta Ollama API vs subprocess
/archive/2025-09-17/docs/CRITICAL_OLLAMA_DISCOVERY.md

# Análise de vícios
/archive/2025-09-22/code/ALERT_VICIOS_CLAUDE.py
```

### SISTEMAS IMPORTANTES
```bash
# Sistema unificado de memória
/archive/*/UNIFIED_MEMORY_SYSTEM.py
/archive/*/unified_memory*

# Genjutsu
/archive/*/bin/start_genjutsu.sh
/archive/*/GENJUTSU*

# Crystal Memory
/archive/crystal/
/archive/*/crystal_memory*
```

### DOCUMENTAÇÃO HISTÓRICA
```bash
# Evolução do Scripturemon
/archive/scripturemon-history/

# História do Digimundo
/archive/digimundo-history/docs/

# Planos originais
/archive/MASTER_PLAN_DEBUG/
```

## 🎯 DICAS DE BUSCA EFICIENTE

### 1. USE WILDCARDS
```bash
# Encontrar variações
find /archive -name "*process*lock*" -i

# -i = case insensitive
```

### 2. COMBINE COMANDOS
```bash
# Encontrar e contar
find /archive -name "*.py" | wc -l

# Encontrar e listar com data
find /archive -name "*.md" -exec ls -la {} \; | head -20
```

### 3. USE GREP COM FIND
```bash
# Buscar conteúdo em arquivos específicos
find /archive -name "*.py" -exec grep -l "subprocess" {} \;
```

### 4. ORDENE POR DATA
```bash
# Arquivos mais recentes
find /archive -type f -mtime -7  # Últimos 7 dias

# Arquivos mais antigos
find /archive -type f -mtime +30  # Mais de 30 dias
```

## 📊 ESTATÍSTICAS ÚTEIS

```bash
# Total de arquivos no archive
find /Users/clubproducoes/Digimundo/archive -type f | wc -l

# Tamanho total
du -sh /Users/clubproducoes/Digimundo/archive

# Arquivos por extensão
find /archive -type f | sed 's/.*\.//' | sort | uniq -c | sort -rn

# Pastas mais pesadas
du -sh /archive/* | sort -rh | head -10
```

## 💡 BUSCA INTELIGENTE POR CONTEXTO

### Para encontrar solução de bug:
```bash
grep -r "SOLU[ÇC][AÃ]O\|FIXED\|RESOLVIDO" /archive/
```

### Para encontrar aprendizados:
```bash
grep -r "APRENDIZADO\|LEARNING\|DESCOBERTA" /archive/
```

### Para encontrar decisões:
```bash
grep -r "DECIS[AÃ]O\|DECIDED\|ESCOLHA" /archive/
```

---
**LEMBRE-SE**: O archive é nossa memória histórica.
Cada arquivo conta uma parte da história.

DIGIMUNDO PRESENTE (sabendo onde procurar)