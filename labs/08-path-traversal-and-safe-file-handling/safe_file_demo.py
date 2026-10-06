from flask import Flask, request, send_from_directory, abort
from pathlib import Path

app = Flask(__name__)

BASE_DIR = Path(__file__).parent / "files"
BASE_DIR.mkdir(exist_ok=True)

(BASE_DIR / "public.txt").write_text("Public training file\n", encoding="utf-8")
(BASE_DIR / "guide.txt").write_text("Safe file handling lab\n", encoding="utf-8")

ALLOWED_FILES = {
    "public": "public.txt",
    "guide": "guide.txt",
}

@app.get("/")
def index():
    return {
        "lab": "Web Security Day 8",
        "routes": [
            "/unsafe?file=public.txt",
            "/safe?name=public",
            "/download?name=guide",
        ],
    }

@app.get("/unsafe")
def unsafe():
    requested = request.args.get("file", "")
    candidate = BASE_DIR / requested

    if not candidate.exists() or not candidate.is_file():
        abort(404)

    return candidate.read_text(encoding="utf-8", errors="replace")

@app.get("/safe")
def safe():
    name = request.args.get("name", "")
    filename = ALLOWED_FILES.get(name)
    if filename is None:
        return {"error": "unknown file key"}, 400

    return (BASE_DIR / filename).read_text(encoding="utf-8")

@app.get("/download")
def download():
    name = request.args.get("name", "")
    filename = ALLOWED_FILES.get(name)
    if filename is None:
        return {"error": "unknown file key"}, 400

    return send_from_directory(BASE_DIR, filename, as_attachment=True)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
