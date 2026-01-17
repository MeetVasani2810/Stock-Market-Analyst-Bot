"""
Keepalive module to prevent the bot from sleeping on hosting platforms.
"""
import threading
import os
from http.server import HTTPServer, BaseHTTPRequestHandler

class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"OK")
    
    # Supress logs to avoid cluttering console
    def log_message(self, format, *args):
        pass

def start_server():
    try:
        # Render provides PORT env var. Default to 8080 if not set.
        port = int(os.environ.get("PORT", 8080))
        server = HTTPServer(("0.0.0.0", port), HealthCheckHandler)
        print(f"🌍 Health check server listening on port {port}")
        server.serve_forever()
    except Exception as e:
        print(f"❌ Failed to start health check server: {e}")

def start_keepalive():
    """
    Starts a background thread running a dummy HTTP server.
    This satisfies Render's requirement for Web Services to bind to a port.
    """
    t = threading.Thread(target=start_server, daemon=True)
    t.start()

