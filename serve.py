import http.server
import socketserver
import webbrowser
import os
import sys

PORT = 8080
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_GET(self):
        # Gracefully handle favicon requests with 204 No Content
        if self.path == '/favicon.ico':
            self.send_response(204)
            self.end_headers()
            return
        try:
            super().do_GET()
        except (ConnectionResetError, ConnectionAbortedError, BrokenPipeError):
            pass

    def copyfile(self, source, outputfile):
        """Silently handle browser closing connection mid-stream (e.g. seeking audio or page refresh)"""
        try:
            super().copyfile(source, outputfile)
        except (ConnectionResetError, ConnectionAbortedError, BrokenPipeError):
            pass

    def end_headers(self):
        self.send_header('Accept-Ranges', 'bytes')
        self.send_header('Cache-Control', 'no-cache')
        super().end_headers()

    def log_message(self, format, *args):
        # Clean log output without polluting the console
        sys.stdout.write(f"[{self.log_date_time_string()}] {format % args}\n")

class ThreadingServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True
    allow_reuse_address = True

    def handle_error(self, request, client_address):
        """Ignore client disconnect errors (WinError 10053 / 10054 / BrokenPipe) caused by F5/seeking"""
        exc_type, _, _ = sys.exc_info()
        if exc_type in (ConnectionResetError, ConnectionAbortedError, BrokenPipeError):
            return
        super().handle_error(request, client_address)

def main():
    os.chdir(DIRECTORY)
    with ThreadingServer(("", PORT), QuietHandler) as httpd:
        print(f"🚀 Esco AV Interview Simulation server running at: http://localhost:{PORT}")
        print("💡 Đang phục vụ tại http://localhost:8080 - Bấm Ctrl+C để dừng.")
        try:
            webbrowser.open(f"http://localhost:{PORT}")
        except Exception:
            pass
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Server stopped.")

if __name__ == "__main__":
    main()
