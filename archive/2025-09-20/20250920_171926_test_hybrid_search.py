from app.retrieval.hybrid import HybridRetriever

def test_hybrid_search_empty_index():
    retr = HybridRetriever("empty_test")
    out = retr.search("teste")
    assert isinstance(out, list)
