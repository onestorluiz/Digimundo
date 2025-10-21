from collections import defaultdict, deque
def topo_sort(deps: dict[str, list[str]]) -> list[str]:
    indeg = {u: 0 for u in deps}; adj=defaultdict(list)
    for u, ds in deps.items():
        for d in ds:
            indeg[u]+=1; adj[d].append(u)
        if u not in adj: adj[u]=adj[u]
    q=deque([u for u,d in indeg.items() if d==0]); order=[]
    while q:
        x=q.popleft(); order.append(x)
        for v in adj[x]:
            indeg[v]-=1
            if indeg[v]==0: q.append(v)
    if len(order)!=len(deps): raise ValueError('Ciclo detectado no grafo de dependências')
    return order
