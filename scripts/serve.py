"""The walkthrough page: live source from the code folder beside the notes, comments saved to comments.jsonl.

    python3 serve.py <code folder> [port]        # notes and comments live in <code folder>/.walkthrough
"""

import json
import sys
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

HERE = Path(__file__).parent
ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
PORT = int(sys.argv[2]) if len(sys.argv) > 2 else 8090
DATA = ROOT / ".walkthrough"
COMMENTS = DATA / "comments.jsonl"


def data() -> dict:
    notes = json.loads((DATA / "notes.json").read_text())
    for repo in notes["repos"]:
        for f in repo["files"]:
            path = ROOT / f["path"]
            f["source"] = path.read_text().splitlines() if path.exists() else ["(file not found)"]
    notes["comments"] = [json.loads(l) for l in COMMENTS.read_text().splitlines() if l.strip()] if COMMENTS.exists() else []
    return notes


class Handler(BaseHTTPRequestHandler):
    def send(self, body: bytes, kind: str, status: int = 200):
        self.send_response(status)
        self.send_header("Content-Type", kind)
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/api/data":
            return self.send(json.dumps(data()).encode(), "application/json")
        if self.path in ("/", "/index.html"):
            return self.send((HERE / "index.html").read_bytes(), "text/html; charset=utf-8")
        self.send(b"not found", "text/plain", 404)

    def do_POST(self):
        if self.path != "/api/comment":
            return self.send(b"not found", "text/plain", 404)
        body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        entry = {"at": time.strftime("%H:%M"), "who": "Me", "block": body["block"], "text": body["text"].strip()}
        if entry["text"]:
            with COMMENTS.open("a") as out:
                out.write(json.dumps(entry) + "\n")
        self.send(b'{"ok": true}', "application/json")

    def log_message(self, *args):
        pass


if __name__ == "__main__":
    print(f"http://localhost:{PORT}", flush=True)
    ThreadingHTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
