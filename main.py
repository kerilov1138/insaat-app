import flet as ft
import threading
import http.server
import socketserver
import os
import time
import socket

def get_free_port():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 0))
    port = s.getsockname()[1]
    s.close()
    return port

# Global port
PORT = get_free_port()

def run_server():
    dist_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dist')
    if not os.path.exists(dist_dir):
        print(f"Error: {dist_dir} does not exist.")
        return

    # Serve dist directory
    os.chdir(dist_dir)
    Handler = http.server.SimpleHTTPRequestHandler
    # Suppress logs to keep console clean
    # Handler.log_message = lambda *args: None 
    
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Server started at port {PORT}")
        httpd.serve_forever()


try:
    from flet import WebView
except ImportError:
    WebView = None

def main(page: ft.Page):
    page.title = "İnşaat Asistanı"
    page.padding = 0
    page.bgcolor = "#0f172a" 
    
    if WebView:
        wv = WebView(
            url=f"http://localhost:{PORT}/index.html",
            expand=True,
            on_web_resource_error=lambda e: print("Web Resource Error:", e.description)
        )
        page.add(wv)
    else:
        page.add(ft.Text("HATA: Bu sistemde WebView desteklenmiyor veya Flet sürümü eski. Android üzerinde çalışacaktır.", color="red"))


if __name__ == "__main__":
    t = threading.Thread(target=run_server, daemon=True)
    t.start()
    time.sleep(1) # Wait for server
    ft.app(target=main)
