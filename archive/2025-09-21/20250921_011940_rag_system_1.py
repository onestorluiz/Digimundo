# RAG seguro — sem eval/exec. Exporta a mesma API do módulo novo.
from scripturemon_champion.rag import index_document, search_documents

# Mantém compat com chamadas antigas que tentavam usar eval:
def safe_literal_eval(expr: str):
    import ast
    return ast.literal_eval(expr)
