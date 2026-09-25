from http.server import BaseHTTPRequestHandler, HTTPServer

ALLOWED_ORIGIN = "http://127.0.0.1:8000"

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", ALLOWED_ORIGIN)
        self.end_headers()
        self.wfile.write(b'{"message":"CORS training response"}')

HTTPServer(("127.0.0.1", 9000), Handler).serve_forever()
