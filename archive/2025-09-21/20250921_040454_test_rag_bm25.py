from scripturemon_champion.rag import index_document, search_documents
def test_bm25_search_basic():
    index_document('a','o sol brilha sobre o rio e o vento sopra leve')
    index_document('b','noite escura cai sobre a cidade silenciosa')
    index_document('c','vento forte no alto da montanha escura')
    res = search_documents('vento escura', top_k=3)
    ids = [r['doc_id'] for r in res]
    assert 'c' in ids and 'b' in ids
