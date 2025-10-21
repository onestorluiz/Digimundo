from src.digilang.tpd_greedy_lazy import greedy_lazy
from collections import Counter

def test_lazy_prefers_longer_when_frequent():
    # ids com repetição (10,11,12) > (10,11)
    ids=[10,11,12, 10,11,12, 10,11, 10,11,12]
    counter=Counter({(10,11):3, (10,11,12):3})
    sel=greedy_lazy(ids, counter, K=1, time_budget_s=1.0)
    assert list(sel.keys())[0]==(10,11,12)