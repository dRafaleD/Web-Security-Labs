from http.server import BaseHTTPRequestHandler, HTTPServer

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.send_header(
            "Set-Cookie",
            "training_session=demo123; HttpOnly; SameSite=Lax"
        )
        self.end_headers()
        self.wfile.write(b"Harmless cookie lab\n")

HTTPServer(("127.0.0.1", 8000), Handler).serve_forever()
