from flask import Flask, request, jsonify, send_from_directory
from pathlib import Path
import hashlib
import uuid

app = Flask(__name__)
UPLOAD_DIR = Path(__file__).parent / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

MAX_UPLOAD_BYTES = 256 * 1024
ALLOWED_EXTENSIONS = {".txt"}
UPLOAD_INDEX = {}

def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def validate_upload(filename: str, data: bytes):
    if not filename:
        return False, "missing filename"
    if Path(filename).suffix.lower() not in ALLOWED_EXTENSIONS:
        return False, "only .txt training files are allowed"
    if len(data) == 0:
        return False, "empty files are not allowed"
    if len(data) > MAX_UPLOAD_BYTES:
        return False, "file too large"
    try:
        data.decode("utf-8")
    except UnicodeDecodeError:
        return False, "training file must be UTF-8 text"
    return True, "ok"

@app.get("/")
def index():
    return jsonify({
        "lab": "Web Security Day 9",
        "max_upload_bytes": MAX_UPLOAD_BYTES,
        "allowed_extensions": sorted(ALLOWED_EXTENSIONS),
        "routes": ["/upload", "/files/<id>"],
    })

@app.post("/upload")
def upload():
    if "file" not in request.files:
        return jsonify({"error": "file field is required"}), 400

    incoming = request.files["file"]
    original_name = incoming.filename or ""
    data = incoming.read(MAX_UPLOAD_BYTES + 1)

    valid, reason = validate_upload(original_name, data)
    if not valid:
        return jsonify({"error": reason}), 400

    file_id = uuid.uuid4().hex
    stored_name = f"{file_id}.txt"
    (UPLOAD_DIR / stored_name).write_bytes(data)

    digest = sha256_bytes(data)
    UPLOAD_INDEX[file_id] = {
        "original_name": original_name,
        "stored_name": stored_name,
        "size": len(data),
        "sha256": digest,
    }

    return jsonify({
        "id": file_id,
        "original_name": original_name,
        "size": len(data),
        "sha256": digest,
    }), 201

@app.get("/files/<file_id>")
def get_file(file_id: str):
    record = UPLOAD_INDEX.get(file_id)
    if record is None:
        return jsonify({"error": "unknown file id"}), 404

    return send_from_directory(
        UPLOAD_DIR,
        record["stored_name"],
        mimetype="text/plain; charset=utf-8",
        as_attachment=True,
        download_name=record["original_name"],
    )

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
