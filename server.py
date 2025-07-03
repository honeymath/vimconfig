#!/usr/bin/env python3
import socket
import os
import json
import uuid
import threading
import signal
import sys

SOCKET_PATH = os.path.join(os.path.dirname(__file__), "vimsocket")

class VimSocketServer:
    def __init__(self, socket_path=SOCKET_PATH):
        self.socket_path = socket_path
        self.sock = None
        self.running = False

    def cleanup_socket_file(self):
        if os.path.exists(self.socket_path):
            try:
                os.unlink(self.socket_path)
            except Exception as e:
                print(f"Failed to remove existing socket: {e}")
                raise

    def start(self):
        self.cleanup_socket_file()
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
#        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.sock.bind(self.socket_path)
#        self.sock.bind(("127.0.0.1",8765))
        self.sock.listen(1)
        self.running = True
        print(f"VimSocketServer listening at {self.socket_path}")
        
        threading.Thread(target=self.accept_loop, daemon=True).start()

    def accept_loop(self):
        while self.running:
            conn, _ = self.sock.accept()
            print(f"Client connected with conn={conn.fileno()} and conn= {conn}")
            threading.Thread(target=self.handle_client, args=(conn,), daemon=True).start()

    def handle_client(self, conn):
        import time
        time.sleep(2)
        self.send_task(conn, "run_python_vim_script", "helloworld", {"mode": "test"})
        try:
            buffer = ""
            while self.running:
                data = conn.recv(4096)
                if not data:
                    break
                buffer += data.decode()
                while "\n" in buffer:
                    line, buffer = buffer.split("\n", 1)
                    self.handle_response(conn, line)
        finally:
            conn.close()
            print("Client disconnected.")

    def handle_response(self, conn, line):
        try:
            msg = json.loads(line)
            print(f"Received from {conn.fileno()}: {json.dumps(msg, indent=2)}")
        except json.JSONDecodeError as e:
            print(f"Invalid JSON from {conn.fileno()}: {e}")

    def send_task(self, conn, command, target, args):

        task_id = str(uuid.uuid4())
        data = {
            "command": command,
            "target": target,
            "args": args,
            "task_id": task_id
        }
        line = json.dumps([0,data]) + "\n"
        conn.sendall(line.encode())
        print("Sending line:", repr(line))
        print(f"Sent task {task_id} -> {target}")
        return task_id

    def stop(self):
        self.running = False
        if self.sock:
            self.sock.close()
        self.cleanup_socket_file()
        print("Server stopped cleanly.")

def main():
    server = VimSocketServer()

    def cleanup(*_):
        server.stop()
        sys.exit(0)

    signal.signal(signal.SIGINT, cleanup)
    signal.signal(signal.SIGTERM, cleanup)

    server.start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        cleanup()

if __name__ == "__main__":
    main()
