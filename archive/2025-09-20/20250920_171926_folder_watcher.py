import time, os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from ..processing.pipeline import process_pdf
from ...config import load_config

_cfg = load_config()

class PDFHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory and event.src_path.lower().endswith(".pdf"):
            try:
                path = event.src_path
                if "2_roteiros_mestres" in path:
                    t = "roteiro_mestre"
                elif "3_roteiros_criador" in path:
                    t = "roteiro_criador"
                else:
                    t = "teoria_roteiro"
                process_pdf(path, doc_type=t)
                print(f"Processado: {path}")
            except Exception as e:
                print(f"Falha ao processar {event.src_path}: {e}")

def main():
    obs = Observer()
    handler = PDFHandler()
    for p in _cfg.watcher.watch_paths:
        os.makedirs(p, exist_ok=True)
        obs.schedule(handler, p, recursive=True)
    obs.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        obs.stop()
    obs.join()

if __name__ == "__main__":
    main()
