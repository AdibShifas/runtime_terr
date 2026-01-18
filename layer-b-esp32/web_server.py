import socket
import json
import network
import time
import errno

class WebServer:
    def __init__(self):
        self.events_queue = []
        self.html_content = ""
        try:
            with open("remote.html", "r") as f:
                self.html_content = f.read()
            print("[WebServer] Loaded remote.html")
        except:
            print("[WebServer] Error loading remote.html")

    def start(self, port=80):
        addr = socket.getaddrinfo('0.0.0.0', port)[0][-1]
        self.s = socket.socket()
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.setblocking(False) # Non-blocking
        self.s.bind(addr)
        self.s.listen(5)
        print('[WebServer] Listening on', addr)

    def handle_request(self):
        try:
            cl, addr = self.s.accept()
            cl.settimeout(1.0) # Short timeout
            # print('[WebServer] Client connected from', addr)
            request = cl.recv(1024)
            req_str = request.decode('utf-8')
            
            # Simple Parsing
            method, path, _ = req_str.split(' ', 2)
            
            response = ""
            
            # --- ROUTING ---
            
            if path == "/":
                response = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n" + self.html_content
            
            elif path.startswith("/drive") and method == "POST":
                # Parse Body for JSON
                body = req_str.split("\r\n\r\n")[-1]
                try:
                    data = json.loads(body)
                    # TODO: Pass 'data' to Motor Control
                    # print("Drive:", data)
                    response = "HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n{}"
                except:
                    response = "HTTP/1.1 400 Bad Request\r\n\r\n"
                    
            elif path.startswith("/detect"):
                # Format: /detect?type=saw_human
                if "type=" in path:
                    evt_type = path.split("type=")[1].split(" ")[0]
                    print(f"[EventBridge] Received: {evt_type}")
                    self.events_queue.append(evt_type)
                    response = "HTTP/1.1 200 OK\r\n\r\n"
                else:
                    response = "HTTP/1.1 400 Bad Request\r\n\r\n"

            elif path == "/poll_events":
                # Drain queue
                payload = {"events": self.events_queue}
                self.events_queue = [] # specific user session logic ignored for simplicity
                response = "HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n" + json.dumps(payload)

            else:
                response = "HTTP/1.1 404 Not Found\r\n\r\n"
            
            cl.send(response.encode('utf-8'))
            cl.close()
            
        except OSError as e:
            if e.args[0] == errno.EAGAIN:
                return # No connection
            # print(e)
            pass
        except Exception as e:
            print("[WebServer] Error:", e)
            pass
