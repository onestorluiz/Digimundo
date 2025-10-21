import argparse, json, sys
from pathlib import Path
from .logging_setup import get_logger
from .memory import get_unified_memory, MemoryRecord
from .script_doctor import analyze_script
from .rag import index_document, search_documents
from .version import __version__

log = get_logger()

def cmd_status(args):
    mem = get_unified_memory()
    print(json.dumps({"version": __version__, "memory": mem.stats()}, ensure_ascii=False, indent=2))

def cmd_analyze(args):
    text = Path(args.file).read_text(encoding="utf-8", errors="replace")
    res = analyze_script(text).to_dict()
    print(json.dumps(res, ensure_ascii=False, indent=2))

def cmd_memory_store(args):
    rec = MemoryRecord(type=args.type, key=args.key, value=json.loads(args.value), metadata=json.loads(args.metadata or "{}"))
    rid = get_unified_memory().store(rec)
    print(json.dumps({"id": rid}, ensure_ascii=False))

def cmd_memory_get(args):
    rec = get_unified_memory().get(args.type, args.key)
    print(json.dumps(rec.__dict__ if rec else None, ensure_ascii=False, indent=2))

def cmd_rag_index(args):
    text = Path(args.file).read_text(encoding="utf-8", errors="replace")
    index_document(args.id, text, metadata={"path": str(Path(args.file).resolve())})
    print(json.dumps({"indexed": args.id}, ensure_ascii=False))

def cmd_rag_search(args):
    res = search_documents(args.query, top_k=args.top_k)
    print(json.dumps(res, ensure_ascii=False, indent=2))

def build_parser():
    p = argparse.ArgumentParser(prog="scripturemon", description="Scripturemon Champion — CLI minimalista")
    sub = p.add_subparsers()

    sp = sub.add_parser("status", help="Mostra versão e estado da memória")
    sp.set_defaults(func=cmd_status)

    sp = sub.add_parser("analyze", help="Analisa roteiro (texto)")
    sp.add_argument("file")
    sp.set_defaults(func=cmd_analyze)

    mp = sub.add_parser("memory", help="Operações de memória unificada")
    sm = mp.add_subparsers()

    st = sm.add_parser("store", help="Armazena um registro")
    st.add_argument("--type", required=True)
    st.add_argument("--key", required=True)
    st.add_argument("--value", required=True, help='JSON string, ex: {"msg":"oi"}')
    st.add_argument("--metadata", default=None)
    st.set_defaults(func=cmd_memory_store)

    gt = sm.add_parser("get", help="Obtém registro por tipo+chave")
    gt.add_argument("--type", required=True)
    gt.add_argument("--key", required=True)
    gt.set_defaults(func=cmd_memory_get)

    rp = sub.add_parser("rag", help="Indexação/Busca simples")
    rs = rp.add_subparsers()

    ri = rs.add_parser("index", help="Indexa documento")
    ri.add_argument("--id", required=True)
    ri.add_argument("--file", required=True)
    ri.set_defaults(func=cmd_rag_index)

    rq = rs.add_parser("search", help="Busca por similaridade")
    rq.add_argument("--query", required=True)
    rq.add_argument("--top-k", type=int, default=5)
    rq.set_defaults(func=cmd_rag_search)

    return p

def main(argv=None):
    argv = argv or sys.argv[1:]
    parser = build_parser()
    if not argv:
        parser.print_help()
        return 0
    args = parser.parse_args(argv)
    if not hasattr(args, "func"):
        parser.print_help()
        return 2
    return args.func(args)

if __name__ == "__main__":
    raise SystemExit(main())
