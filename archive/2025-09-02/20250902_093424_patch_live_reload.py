# -*- coding: utf-8 -*-
from __future__ import annotations
from pathlib import Path
import re, sys, html
from scripts.ui_prefs import get_live

INJECT_ID = "script-live-refresh"

def _template(default_refresh:str)->str:
    # default_refresh: e.g., "off", "10s", "1m"
    default_refresh = (default_refresh or "off").strip()
    return '''
<script id="script-live-refresh">
(function(){
  try {
    const qs = new URLSearchParams((location.search||"").replace(/^\\?/,""));
    const r = qs.get("refresh") || qs.get("r") || "";
    const norm = (s)=> String(s||"").trim().toLowerCase();
    const toMs = (x)=>{
      if(!x) return 0;
      if(/^\\d+$/.test(x)) return parseInt(x,10)*1000;
      const m = String(x).match(/^(\\d+)\\s*(ms|s|sec|secs|seconds|m|min|mins|minutes)?$/i);
      if(!m) return 0;
      const v = parseInt(m[1],10); const u=(m[2]||"s").toLowerCase();
      if(u.startsWith("ms")) return v;
      if(u.startsWith("m")) return v*60*1000;
      return v*1000;
    };
    const DEFAULT = ''' + (("'" + default_refresh + "'") if True else "'off'") + ''';
    const chosen = norm(r || DEFAULT);
    const ms = toMs(chosen);
    if(ms>0){
      console.log("[live] auto-refresh in", ms, "ms");
      setTimeout(()=>{ location.reload(); }, ms);
      // badge simples no canto
      const b=document.createElement("div");
      b.setAttribute("style","position:fixed;right:8px;bottom:8px;background:rgba(0,0,0,.6);color:#fff;padding:4px 8px;border-radius:6px;font:12px system-ui,Arial");
      b.textContent="LIVE: "+(ms>=60000?(Math.round(ms/600)/100+"m"):(ms>=1000?(Math.round(ms/100)/10+"s"):(ms+"ms")));
      document.body.appendChild(b);
    }
  } catch(e){ console.warn("[live] inject error", e); }
})();
</script>
'''

def _inject_or_replace(path:Path, default_refresh:str)->bool:
    if not path.exists(): return False
    s = path.read_text(encoding="utf-8", errors="ignore")
    # remove bloco antigo (se existir)
    s = re.sub(r'<script[^>]+id=["\']%s["\'][\\s\\S]*?</script>' % INJECT_ID, "", s, flags=re.I)
    # injeta antes de </body>
    tmpl = _template(default_refresh)
    if "</body>" in s.lower():
        idx = s.lower().rfind("</body>")
        s = s[:idx] + tmpl + s[idx:]
    else:
        s = s + "\n" + tmpl
    path.write_text(s, encoding="utf-8")
    return True

def main():
    default_refresh = get_live()
    changed=False
    for p in (Path("reports/index.html"), Path("reports/ultimate_panel.html")):
        if p.exists():
            if _inject_or_replace(p, default_refresh):
                print("[UPDATED] live reload ->", p, "default:", default_refresh)
                changed=True
        else:
            print("[SKIP] missing", p)
    if not changed:
        print("[OK] live reload present (default:", default_refresh, ")")

if __name__=="__main__": main()