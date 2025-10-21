from app.processing.chunking import smart_chunk

def test_smart_chunk_basic():
    text = " ".join(["palavra"]*2000)
    chunks = smart_chunk([text], target_tokens=500, overlap_tokens=100)
    assert len(chunks) > 2
