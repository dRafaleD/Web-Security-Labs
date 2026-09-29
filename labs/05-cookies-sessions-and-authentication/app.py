from flask import Flask, redirect, request, session

app = Flask(__name__)

# Training-only key for a local lab.
# Never hard-code real production secrets like this.
app.secret_key = "local-training-secret"

app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=False,  # Local HTTP lab only
)

@app.get("/")
def index():
    if session.get("user"):
        return (
            "Logged in as student. "
            '<a href="/profile">Profile</a> | '
            '<a href="/logout">Logout</a>'
        )

    return """
    <h1>Local Session Lab</h1>
    <form method="post" action="/login">
      <input name="username" value="student">
      <button type="submit">Training Login</button>
    </form>
    """

@app.post("/login")
def login():
    if request.form.get("username") == "student":
        session.clear()
        session["user"] = "student"
        session["role"] = "user"
        return redirect("/profile")

    return "Invalid training user", 401

@app.get("/profile")
def profile():
    if not session.get("user"):
        return "Not authenticated", 401

    return f"Profile for {session['user']} (role={session['role']})"

@app.get("/admin")
def admin():
    if not session.get("user"):
        return "Not authenticated", 401

    if session.get("role") != "admin":
        return "Authenticated but not authorized", 403

    return "Admin area"

@app.get("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
