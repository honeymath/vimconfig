import socket
import threading
import json
import uuid
import os

class Client:
    def __init__(self, conn, client_id, server):
        self.conn = conn
        self.client_id = client_id
        self.server = server
        self.buffer = ""
        self.running = True
        self.task_results = {}  # task_id -> result
        self.task_locks = {}    # task_id -> threading.Event

        # 注册 client
        self.server.clients[client_id] = self
        print(f"Client {client_id} registered.")

        # 启动接收线程
        self.recv_thread = threading.Thread(target=self.recv_loop, daemon=True)
        self.recv_thread.start()

        ### the following is a testing
        # Example task to test the server
        #import time
        #time.sleep(2)
        #print(self.send_task("run_python_vim_script", "helloworld", {"mode": "test"}))

    def send_task(self, command, target, args, task_id=None):
        if not task_id:
            task_id = str(uuid.uuid4())
        if task_id in self.task_locks:
            raise ValueError(f"Task ID {task_id} is already in use!")

        event = threading.Event()
        self.task_locks[task_id] = event

        msg = {
            "command": command,
            "target": target,
            "args": args,
            "task_id": task_id
        }
        line = json.dumps([0,msg]) + "\n"
        self.conn.sendall(line.encode())

        print(f"Task {task_id} sent to {self.client_id}")

        event.wait()

        result = self.task_results.pop(task_id, None)
        self.task_locks.pop(task_id, None)
        return result

    def recv_loop(self):
        try:
            while self.running:
                data = self.conn.recv(4096)
                if not data:
                    break
                self.buffer += data.decode()
                while '\n' in self.buffer:
                    line, self.buffer = self.buffer.split('\n', 1)
                    self.handle_response(line)
        except Exception as e:
            print(f"Error in recv_loop of {self.client_id}: {e}")
        finally:
            self.close()

    def handle_response(self, line):
        try:
            msg = json.loads(line)
            task_id = msg.get("task_id")
            if task_id and task_id in self.task_locks:
                self.task_results[task_id] = msg
                self.task_locks[task_id].set()
            else:
                print(f"Unexpected or unknown task_id: {task_id}")
        except Exception as e:
            print(f"Failed to handle response: {e}")

    def close(self):
        if self.running:
            self.running = False
            try:
                self.conn.close()
            except:
                pass
            if self.client_id in self.server.clients:
                del self.server.clients[self.client_id]
                print(f"Client {self.client_id} unregistered.")

class VimSocketServer:
    def __init__(self, socket_path=None):
        if not socket_path:
            socket_path = os.path.join(os.path.dirname(__file__), "vimsocket")
        self.socket_path = socket_path
        self.sock = None
        self.clients = {}
        self.next_client_id = 1
        self.running = True

    def start(self):
        if os.path.exists(self.socket_path):
            os.unlink(self.socket_path)
#        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#        self.sock.bind(self.socket_path)
        self.sock.bind(('0.0.0.0', 8765))
        self.sock.listen()
        print(f"Second server listening at {self.socket_path}")

        while self.running:
            conn, _ = self.sock.accept()
            client_id = f"client-{self.next_client_id}"
            self.next_client_id += 1
            Client(conn, client_id, self)

    def stop(self):
        self.running = False
        if self.sock:
            self.sock.close()
        if os.path.exists(self.socket_path):
            os.unlink(self.socket_path)
        print("Second server stopped.")

server = VimSocketServer()

if __name__ == "__main__":
    try:
        server.start()
    except KeyboardInterrupt:
        server.stop()
