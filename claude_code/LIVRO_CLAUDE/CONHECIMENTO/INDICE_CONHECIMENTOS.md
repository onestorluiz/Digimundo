# 📚 ÍNDICE DE CONHECIMENTOS RESGATADOS

## 🗂️ ESTRUTURA DO CONHECIMENTO

### 1. DESCOBERTAS CRÍTICAS
- [Problema do Ollama](#ollama) - Configuração 128K tokens
- [Vulnerabilidades Scripturemon](#vulnerabilidades) - Self-modifying code
- [14 Processos Python](#processos) - Timeout e zumbis

### 2. APRENDIZADOS FUNDAMENTAIS
- [Subprocess vs API](#subprocess-api) - Nunca usar CLI para automação
- [ProcessLock Overengineering](#processlock) - Teste direto > análise
- [Memória Fragmentada](#memoria) - Unificar bancos de dados

### 3. REGRAS DE OURO
- [Regra do Timeout](#timeout) - 60s = problema
- [Regra da API](#api) - CLI para humanos, API para código
- [Regra do Teste Direto](#teste) - Testar ferramenta nua primeiro
- [Regra da Unificação](#unificacao) - Uma verdade, zero ambiguidade

### 4. SISTEMA ANTI-VÍCIOS
- [Vícios Identificados](#vicios) - Overengineering, criar sem verificar
- [Checklist Anti-Vícios](#checklist) - 5 verificações essenciais

### 5. ARQUIVOS ESSENCIAIS
- [Documentação Crítica](#docs) - CRITICAL_OLLAMA_DISCOVERY.md
- [Códigos Importantes](#code) - ALERT_VICIOS_CLAUDE.py
- [Planos e Análises](#plans) - MASTER_PLAN_DEBUG/

## 📍 LOCALIZAÇÕES RÁPIDAS

### Para Buscar Soluções:
```bash
# Problemas conhecidos
grep -r "PROBLEMA\|BUG\|ERROR" /archive/

# Soluções aplicadas
grep -r "SOLUÇÃO\|FIXED\|RESOLVIDO" /archive/

# Decisões tomadas
grep -r "DECISÃO\|DECIDED" /archive/
```

### Arquivos Mais Importantes:
| Conhecimento | Arquivo | Comando |
|--------------|---------|---------|
| Ollama Config | `/archive/2025-09-17/docs/CRITICAL_OLLAMA_DISCOVERY.md` | `cat` |
| Vícios Claude | `/archive/2025-09-22/code/ALERT_VICIOS_CLAUDE.py` | `python3` |
| Plano Debug | `/archive/MASTER_PLAN_DEBUG/` | `ls -la` |

## 🎯 APLICAÇÃO PRÁTICA

### Quando Encontrar Problema Similar:
1. **Buscar** no archive: `grep -r "ERRO_SIMILAR" /archive/`
2. **Aplicar** solução documentada
3. **Evitar** vícios conhecidos
4. **Testar** ferramenta diretamente

### Check-list Rápido:
- [ ] Ollama via API, não CLI
- [ ] Timeout >= 300s para operações pesadas
- [ ] Matar processos zumbis antes de criar novos
- [ ] Verificar se já existe antes de criar
- [ ] Um banco de dados unificado

## 📊 ESTATÍSTICAS DO RESGATE

| Métrica | Valor | Impacto |
|---------|-------|---------|
| Bugs críticos documentados | 5 | Alto |
| Vulnerabilidades corrigidas | 3 | Crítico |
| Tempo economizado | 58+ min | Crítico |
| Configurações otimizadas | 7 | Alto |
| Vícios identificados | 4 | Médio |

## 🔗 LINKS INTERNOS

- **Conhecimentos Completos**: [CONHECIMENTOS_RESGATADOS_ARCHIVE.md](./CONHECIMENTOS_RESGATADOS_ARCHIVE.md)
- **Estrutura do Archive**: [ESTRUTURA_ARCHIVE.md](./ESTRUTURA_ARCHIVE.md)
- **Padrões de Busca**: [BUSCA_ARCHIVE_PATTERNS.md](./BUSCA_ARCHIVE_PATTERNS.md)
- **Regras do Sistema**: [/archive/digimundo-history/docs/REGRAS.md](/Users/clubproducoes/Digimundo/archive/digimundo-history/docs/REGRAS.md)

---
**ÍNDICE CRIADO**: 23 de Setembro de 2025
**STATUS**: Conhecimento integrado e acessível
DIGIMUNDO PRESENTE (com memória indexada)