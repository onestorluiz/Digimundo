from scripturemon_champion.rag import index_document, search_documents
def safe_literal_eval(expr: str):
    import ast; return ast.literal_eval(expr)
