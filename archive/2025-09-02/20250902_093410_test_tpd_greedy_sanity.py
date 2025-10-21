import sys
sys.path.append('.')
import tiktoken
from src.digilang.tpd_greedy import greedy_submodular_select, score_candidates

# corpus toy: ids = [1,2,3, 1,2,3, 1,2,  1,2,3]
def test_greedy_prefers_longer_ngram():
    ids = [10,11,12, 10,11,12, 10,11, 10,11,12]
    # candidates: (10,11), (10,11,12)
    cands = [((10,11), 3, (2-1)*3), ((10,11,12), 3, (3-1)*3)]
    sel = greedy_submodular_select(ids, cands, K=1, max_cands=10)
    assert list(sel.keys())[0] == (10,11,12)
    print("✅ Greedy prefers longer n-gram test passed")

if __name__ == "__main__":
    test_greedy_prefers_longer_ngram()