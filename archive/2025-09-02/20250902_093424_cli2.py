from __future__ import annotations
import argparse, sys
try:
    from apps.scripturemon.entrypoints import (status_main, doctor_main, chat_main, analyze_main, compress_main)
except Exception as e:
    def status_main(): print(f"[ERR] entrypoints indisponíveis: {e}", file=sys.stderr); return 2
    def doctor_main(): print("[WARN] doctor indisponível"); return 0
    def chat_main():  print("[WARN] chat indisponível"); return 0
    def analyze_main(path:str): print("[WARN] analyze indisponível"); return 0
    def compress_main(path:str): print("[WARN] compress indisponível"); return 0

def main(argv=None)->int:
    ap = argparse.ArgumentParser(prog="scripturemon", add_help=True)
    sub = ap.add_subparsers(dest="cmd")
    sub.add_parser("help",    help="mostrar ajuda e sair")
    sub.add_parser("status",  help="checagens rápidas")
    sub.add_parser("doctor",  help="diagnóstico detalhado")
    pa = sub.add_parser("analyze",  help="analisar roteiro/livro");   pa.add_argument("path")
    pc = sub.add_parser("compress", help="aplicar DigiLang/compactação"); pc.add_argument("path")
    sub.add_parser("chat",    help="abrir chat interativo (modelo leve)")
    args = ap.parse_args(argv)
    if args.cmd in (None, "help"): ap.print_help(); return 0
    if args.cmd == "status":  return int(status_main() or 0)
    if args.cmd == "doctor":  return int(doctor_main() or 0)
    if args.cmd == "analyze": return int(analyze_main(args.path) or 0)
    if args.cmd == "compress":return int(compress_main(args.path) or 0)
    if args.cmd == "chat":    chat_main(); return 0
    ap.print_help(); return 0

if __name__ == "__main__":
    raise SystemExit(main())