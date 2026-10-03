from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
DB = ":memory:"

def init_db():
    db = sqlite3.connect(DB)
    db.execute("CREATE TABLE products (id INTEGER PRIMARY KEY, name TEXT, category TEXT, price INTEGER)")
    db.executemany(
        "INSERT INTO products VALUES (?, ?, ?, ?)",
        [
            (1, "Keyboard", "hardware", 1200),
            (2, "Mouse", "hardware", 700),
            (3, "Python Book", "books", 450),
            (4, "Linux Book", "books", 500),
        ],
    )
    db.commit()
    return db

db = init_db()

@app.get("/unsafe-search")
def unsafe_search():
    q = request.args.get("q", "")
    # Deliberately vulnerable LOCAL training example.
    sql = f"SELECT id, name, category, price FROM products WHERE name LIKE '%{q}%'"
    try:
        rows = db.execute(sql).fetchall()
        return jsonify({"query": sql, "results": rows})
    except sqlite3.Error as exc:
        return jsonify({"query": sql, "error": str(exc)}), 400

@app.get("/safe-search")
def safe_search():
    q = request.args.get("q", "")
    sql = "SELECT id, name, category, price FROM products WHERE name LIKE ?"
    rows = db.execute(sql, (f"%{q}%",)).fetchall()
    return jsonify({"query_template": sql, "results": rows})

@app.get("/product")
def product():
    raw_id = request.args.get("id", "")
    try:
        product_id = int(raw_id)
    except ValueError:
        return jsonify({"error": "id must be an integer"}), 400

    row = db.execute(
        "SELECT id, name, category, price FROM products WHERE id = ?",
        (product_id,),
    ).fetchone()

    if row is None:
        return jsonify({"error": "not found"}), 404
    return jsonify({"product": row})

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
