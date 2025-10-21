# 🧪 Tests - Scripturemon

Scripts de teste e validação do sistema.

---

## 📋 Arquivos de Teste

### 1. test_personalized_prompts.py

**Propósito**: Testa prompts personalizados FASE 2

**O que faz**:
- Testa um único autor específico
- Valida que prompts personalizados estão ativos
- Gera análise de teste

**Uso**:
```bash
python3 test_personalized_prompts.py
```

**Status**: ✅ FASE 2 validado em produção

---

### 2. test_theory_path.py

**Propósito**: Valida caminhos dos livros de teoria

**O que faz**:
- Verifica se livros de teoria existem
- Testa indexação de chunks
- Valida deep context mode

**Uso**:
```bash
python3 test_theory_path.py
```

**Status**: ✅ Deep Context validado em produção

---

## 🎯 Como Usar

### Testes Rápidos

**Testar sistema completo** (recomendado):
```bash
cd /Users/clubproducoes/Digimundo/scripturemon
python3 analyze.py "inputs/examples/Te Encontro em Mim .pdf" --authors dialogue --deep
```

**Testar autor específico**:
```bash
python3 tests/test_personalized_prompts.py
```

**Validar teoria**:
```bash
python3 tests/test_theory_path.py
```

---

## ✅ Testes de Produção

Sistema FASE 3 validado com:
- 12/13 autores testados
- Scores reais: 15.5-18.0/10
- Tempo médio: 5-7 min/autor
- Deep Context: 128k tokens ativo
- FASE 2 Prompts: Personalizados por autor

Ver `VALIDACAO_COMPLETA_12_AUTORES.md` para resultados completos.

---

**Última Atualização**: 10 de Outubro 2025
