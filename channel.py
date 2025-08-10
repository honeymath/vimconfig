import configparser
import os
import socket

# 读取配置文件
config_path = os.path.join(os.path.dirname(__file__), 'config.ini')
config = configparser.ConfigParser()
config.read(config_path)

# ===== 初始化外部 TCP 服务器连接 =====
servers = []
for section in config.sections():
    if section.startswith("server:"):
        if config.getboolean(section, "enabled", fallback=True):
            servers.append({
                "name": section.split(":", 1)[1],
                "host": config.get(section, "host"),
                "port": config.getint(section, "port"),
            })

print("servers",servers)
tcp_sockets = {}
for srv in servers:
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((srv["host"], srv["port"]))
        tcp_sockets[srv["name"]] = sock
        print(f"Connected to external server {srv['name']} at {srv['host']}:{srv['port']}")
    except Exception as e:
        print(f"Failed to connect to server {srv['name']}: {e}")

# ===== 初始化本地 TCP 服务（可选） =====
try:
    local_server_sock = None
    if config.getboolean("local_server", "enabled", fallback=False):
        host = config.get("local_server", "host", fallback="0.0.0.0")
        port = config.getint("local_server", "port", fallback=7777)
        max_clients = config.getint("local_server", "max_clients", fallback=5)
        local_server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        local_server_sock.bind((host, port))
        local_server_sock.listen(max_clients)
        print(f"Local TCP server listening on {host}:{port}")
except Exception as e:
    print(f"Failed to local TCP {host}:{port} since ", e)

# ===== 初始化 Unix socket =====
unix_sock_path_base = config.get("unix_socket", "path", fallback="/tmp/vim_channel_")
temp = sys.argv[1]
unix_sock_path = f"~/Documents/{temp}.sock"# the file name completely determined by
unix_sock_path = os.path.expanduser(unix_sock_path)
print("Trying path at", unix_sock_path)
if os.path.exists(unix_sock_path):
    os.remove(unix_sock_path)

unix_sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
unix_sock.bind(unix_sock_path)
unix_sock.listen(1)
print(f"Unix socket listening at {unix_sock_path}")

# ===== 主循环（示例） =====
try:
    import threading
    import sys
    import select

#ai: I am editing this part, 
# I am thinking everytime tasks has append a task, then call worker to activate py3 from inside and try to execute the tasks...
    tasks = {}  # {task_id: {"sock": sock, "request": 原始数据}}

    def send_task(task_id):
        print("REQUEST_CONTROL") ## pring this to vim worker so it can establish the receiver
#end

    def listen_unix():
        while True:
            conn, _ = unix_sock.accept()
            with conn:
                data = conn.recv(4096)
                if not data:
                    continue
#ai: Now this part has to be edited, this part is the processed data, and have to send back, have to check based on its id and our record, decide how to send it back
            try:
                import json
                msg = json.loads(data.decode())
                task_id = msg.get("task_id")
                if task_id and task_id in tasks:
                    sock = tasks[task_id]["sock"]
                    sock.sendall(json.dumps(msg).encode() + b"\n")
                    del tasks[task_id]
                    print(f"[UnixSock] Sent result for task {task_id} back to external client")
                else:
                    print(f"[UnixSock] Unknown or missing task_id: {task_id}")
            except Exception as e:
                print(f"[UnixSock] Failed to process data: {e}")
#end
    def listen_external():
        while True:
            if not tcp_sockets:
                continue
            rlist, _, _ = select.select(tcp_sockets.values(), [], [], 1)
            for sock in rlist:
                try:
                    data = sock.recv(4096)
                    if data:
                        print(f"{data.decode().strip()}")
#see: I have added this part
                        tasks[sock] = data
#ai: but I think I also have to store the uuid?
                try:
                    import json
                    msg = json.loads(data.decode())
                    task_id = msg.get("task_id")
                    if task_id:
                        tasks[task_id] = {"sock": sock, "request": msg}
                        print(f"[External] Stored task {task_id} from {sock.getpeername()}")
                    else:
                        print("[External] Missing task_id in message")
                except Exception as e:
                    print(f"[External] Failed to parse message: {e}")
#end
#end
                except Exception as e:
                    print(f"External server error: {e}", file=sys.stderr)

    def listen_local_server():
        if not local_server_sock:
            return
        while True:
            conn, addr = local_server_sock.accept()
            with conn:
                data = conn.recv(4096)
                if not data:
                    continue
                print(f"{data.decode().strip()}")

    def listen_stdin():
        while True:
            line = sys.stdin.readline()
            if not line:
                continue
            if line.strip().lower() == "exit":
                raise KeyboardInterrupt

    # 启动多线程
    threading.Thread(target=listen_unix, daemon=True).start()
    threading.Thread(target=listen_external, daemon=True).start()
    threading.Thread(target=listen_local_server, daemon=True).start()
    threading.Thread(target=listen_stdin, daemon=True).start()

    # 主线程空转保持存活
    while True:
        pass
except KeyboardInterrupt:
    print("Shutting down...")
finally:
    # 清理资源
    for sock in tcp_sockets.values():
        sock.close()
    if local_server_sock:
        local_server_sock.close()
    unix_sock.close()
    if os.path.exists(unix_sock_path):
        os.remove(unix_sock_path)
