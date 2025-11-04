import http.server
import socketserver
import os

PORT = 8000
Handler = http.server.SimpleHTTPRequestHandler
socketserver.TCPServer.allow_reuse_address = True

try:
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Serving HTTP on port {PORT} from directory: {os.getcwd()}")
        print(f"Access your files at http://localhost:{PORT}/")
        print("Press Ctrl+C to stop the server.")
        httpd.serve_forever()
except OSError as e:
    print(f"Error: Could not start server on port {PORT}. It might be in use.")
    print(f"Details: {e}")
    print("Please ensure no other program is using port 8000, or try a different port.")
except KeyboardInterrupt: print("\nServer stopped by user.")
except Exception as e: print(f"An unexpected error occurred: {e}")