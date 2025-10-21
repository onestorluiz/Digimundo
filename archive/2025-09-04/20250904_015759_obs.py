import json, time, os
LOG=os.path.join(os.environ.get("SCRIPTUREMON_HOME","."),"/Users/clubproducoes/Digimundo/scripturemon-validation","runtime","logs","obs.jsonl")
os.makedirs(os.path.dirname(LOG), exist_ok=True)
def log_obs(payload:dict):
    payload=dict(payload); payload["ts"]=time.time()
    with open(LOG,"a",encoding="utf-8") as f: f.write(json.dumps(payload, ensure_ascii=False)+"\n")