import random
def _dirichlet(alphas):
    vals=[random.gammavariate(max(a,0.1),1.0) for a in alphas]
    s=sum(vals) or 1.0
    return [v/s for v in vals]
def mix(outputs:list[dict])->dict:
    # outputs: [{name,text,evi,mem,coh,cites[]}...]
    alphas=[]
    for o in outputs:
        e=o.get("evi",0.3); m=o.get("mem",0.3); c=o.get("coh",0.3); cit=len(o.get("cites",[]))
        a = 0.3 + 1.2*e + 0.8*m + 0.6*c + 0.15*cit
        alphas.append(a if a>0 else 0.1)
    ws=_dirichlet(alphas)
    paras=[(o.get("name","m"), (o.get("text") or "").split("\n\n")) for o in outputs]
    mixed=[]
    for i in range(max(len(p[1]) for p in paras)):
        pool=[]
        for w,(n,pp) in zip(ws, paras):
            if i<len(pp): pool.append((w, pp[i]))
        pool.sort(key=lambda x: x[0], reverse=True)
        for w,t in pool[:2]:
            import random
            if random.random() < min(1.0, w*1.5):
                mixed.append(t)
    return {"text":"\n\n".join(mixed), "weights":ws}