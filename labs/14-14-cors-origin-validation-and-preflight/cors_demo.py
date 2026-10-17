from http.server import BaseHTTPRequestHandler, HTTPServer
ALLOWED = {"http://localhost:3000"}
class Handler(BaseHTTPRequestHandler):
    def headers_cors(self):
        origin = self.headers.get("Origin")
        if origin in ALLOWED:
            self.send_header("Access-Control-Allow-Origin", origin)
            self.send_header("Vary", "Origin")
            self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
            self.send_header("Access-Control-Allow-Headers", "Content-Type")
    def do_OPTIONS(self):
        self.send_response(204)
        self.headers_cors()
        self.end_headers()
    def do_GET(self):
        self.send_response(200)
        self.headers_cors()
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Local CORS lab")
HTTPServer(("127.0.0.1", 8081), Handler).serve_forever()
