"""
Simple API interface for the Real Food Score algorithm.

Usage:
    python api.py                    # Start server on port 8000
    curl localhost:8000/score?name=Test&ingredients=chicken,rice,salt
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json
from scoring import RealFoodScorer


class ScoreHandler(BaseHTTPRequestHandler):
    scorer = RealFoodScorer()

    def do_GET(self):
        parsed = urlparse(self.path)

        if parsed.path == "/score":
            params = parse_qs(parsed.query)
            name = params.get("name", ["Unknown Product"])[0]
            ingredients = params.get("ingredients", [""])[0]

            if not ingredients:
                self.send_error(400, "Missing 'ingredients' parameter")
                return

            result = self.scorer.score_product(name, ingredients)

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(result, indent=2).encode())

        elif parsed.path == "/health":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"status": "ok"}')

        else:
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(b"""
            <html>
            <head><title>Real Food Score API</title></head>
            <body>
                <h1>Real Food Score API</h1>
                <p>Score food products against realfood.gov guidelines.</p>
                <h2>Endpoints</h2>
                <ul>
                    <li><code>GET /score?name=Product&ingredients=a,b,c</code></li>
                    <li><code>GET /health</code></li>
                </ul>
                <h2>Try it</h2>
                <form action="/score" method="get">
                    <label>Product: <input name="name" value="Test Product"></label><br><br>
                    <label>Ingredients: <input name="ingredients" size="50" value="chicken, rice, olive oil, salt"></label><br><br>
                    <button type="submit">Score</button>
                </form>
            </body>
            </html>
            """)

    def log_message(self, format, *args):
        print(f"[API] {args[0]}")


def run_server(port=8000):
    server = HTTPServer(("", port), ScoreHandler)
    print(f"Real Food Score API running at http://localhost:{port}")
    print("Try: http://localhost:{port}/score?name=Test&ingredients=eggs,butter,salt")
    server.serve_forever()


if __name__ == "__main__":
    run_server()
