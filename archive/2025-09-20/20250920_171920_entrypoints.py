from __future__ import annotations
import os, json, sys
SAFE_MODEL = os.environ.get("SCRIPTUREMON_DEFAULT_MODEL","llama3.1:8b")
def status_main():
    ok=True
    try:
        from apps.scripturemon.memory_unification import get_unified_memory
        u=get_unified_memory(); u.store_unified_memory("ping", source="cli", memory_type="general", importance=0.1); u.retrieve_unified_memory("ping",limit=1)
        print("UnifiedMemory: OK")
    except Exception as e:
        ok=False; print(f"UnifiedMemory: FAIL ({e})")
    print(f"Ollama:        {os.environ.get('SCRIPTUREMON_DEFAULT_MODEL', SAFE_MODEL)}")
    return 0 if ok else 1
def doctor_main():
    print("Doctor: checagens estendidas…"); return status_main()
def chat_main():
    from apps.scripturemon.chat import ScripturemonChat
    ScripturemonChat().start_interactive()
def analyze_main(path:str):
    from apps.scripturemon.scripturemon_brain import ScripturemonBrain
    print(json.dumps(ScripturemonBrain().analyze_script(path), ensure_ascii=False, indent=2))
def compress_main(path:str):
    try:
        from src.digilang.encoder import DigiLangEncoder
        txt=open(path,"r",encoding="utf-8",errors="ignore").read()
        enc=DigiLangEncoder(); comp, ratio = enc.encode(txt)
        print(json.dumps({"ratio":ratio,"preview":comp[:400]}, ensure_ascii=False, indent=2))
    except Exception as e:
        print(f"[WARN] compressor indisponível: {e}"); return 1