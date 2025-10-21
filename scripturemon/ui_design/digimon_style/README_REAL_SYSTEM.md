# SCRIPTUREMON UI - Sistema REAL

## Funcionalidades REAIS

### Dados em Tempo Real:
- **Análises em progresso**: Lidas de `workspace/outputs/*/2_logs/checkpoint.json`
- **Estatísticas**: 
  - Total de análises
  - 2 rodando, 0 completas
  - 133 análises individuais completadas
  - 7.7 horas processadas

### Botões FUNCIONAIS:

1. **Nova Análise** → Abre `/Applications/Analyze Screenplay.app`
2. **Continuar Análise** → Retoma do checkpoint com `python3 analyze_all_specialists.py --resume`
3. **Ver Resultados** → Abre pasta `1_individuais` no Finder
4. **Ver Consolidados** → Abre pasta `3_consolidados` no Finder

### API Endpoints:

**Dados:**
- GET /api/analyses/list
- GET /api/system/stats

**Ações:**
- POST /api/action/new-analysis
- POST /api/action/continue-analysis/<id>
- POST /api/action/open-results/<id>
- POST /api/action/open-consolidated/<id>

## Como Funciona

O sistema REAL:
- 24 specialists × 13 autores = 312 análises por roteiro
- Checkpoint automático a cada análise
- Tempo: ~30-35 horas por roteiro
- Gera HTMLs individuais e consolidados

Sem placeholders, sem invenções. Tudo é REAL.
