from flask import Flask, request, jsonify

app = Flask(__name__)

# Harmless in-memory training data.
USERS = {
    1: {"name": "student", "role": "user", "note": "Student training profile"},
    2: {"name": "analyst", "role": "user", "note": "Analyst training profile"},
    99: {"name": "admin-demo", "role": "admin", "note": "Administrator training profile"},
}

def current_user():
    """Training-only identity selector. This is NOT real authentication."""
    raw = request.headers.get("X-Training-User")
    if raw is None or not raw.isdigit():
        return None
    return USERS.get(int(raw))

@app.get("/")
def index():
    return jsonify({
        "lab": "Web Security Day 6",
        "message": "Use X-Training-User: 1, 2, or 99 with the local endpoints.",
        "warning": "The header is only a lab identity selector, not real authentication."
    })

@app.get("/me")
def me():
    user = current_user()
    if user is None:
        return jsonify({"error": "training identity required"}), 401
    return jsonify(user)

@app.get("/profiles/<int:profile_id>")
def profile(profile_id):
    user = current_user()
    if user is None:
        return jsonify({"error": "training identity required"}), 401

    # Object-level authorization: a normal user can read only their own profile.
    if user["role"] != "admin" and USERS.get(profile_id) is not user:
        return jsonify({"error": "forbidden"}), 403

    profile_data = USERS.get(profile_id)
    if profile_data is None:
        return jsonify({"error": "profile not found"}), 404

    return jsonify(profile_data)

@app.get("/admin/report")
def admin_report():
    user = current_user()
    if user is None:
        return jsonify({"error": "training identity required"}), 401

    # Function-level authorization.
    if user["role"] != "admin":
        return jsonify({"error": "admin role required"}), 403

    return jsonify({
        "report": "Harmless local admin report",
        "user_count": len(USERS)
    })

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
