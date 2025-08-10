import os
import sys
import json
import socket
import threading
import select
import configparser

# channel.py
# 全局任务表 {task_id: {"sock": socket_obj, "request": 原始JSON}}
tasks = {}


config_path = os.path.join(os.path.dirname(__file__), 'config.ini')
config = configparser.ConfigParser()
config.read(config_path)

# ===== 初始化外部 TCP 服务器连接 =====
servers = []
EXTERNAL_SERVERS = servers
for section in config.sections():
    if section.startswith("server:"):
        if config.getboolean(section, "enabled", fallback=True):
            servers.append({
                "name": section.split(":", 1)[1],
                "host": config.get(section, "host"),
                "port": config.getint(section, "port"),
            })

# 发送启动 caller 的信号（需要根据你的 Vim 环境实现）
def send_task_signal():
    print("[Signal] Would trigger Vim worker to start caller here.", flush = True)

# 批量派发任务给 caller
def send_task(caller_sock):
    if not tasks:
        print("[Dispatcher] No tasks to send.", flush = True)
        return
    payload = {"tasks": {tid: info["request"] for tid, info in tasks.items()}}
    caller_sock.sendall(json.dumps(payload).encode() + b"\n")
    print(f"[Dispatcher] Sent {len(tasks)} tasks to caller.", flush = True)

# 外部 TCP 监听线程
def listen_external():
    tcp_sockets = []
    # 主动连接外部服务器
    for host, port in EXTERNAL_SERVERS:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((host, port))
            tcp_sockets.append(s)
            print(f"[External] Connected to {host}:{port}", flush = True)
        except Exception as e:
            print(f"[External] Failed to connect {host}:{port} - {e}", flush = True)
    while True:
        if not tcp_sockets:
            continue
        rlist, _, _ = select.select(tcp_sockets, [], [], 1)
        for sock in rlist:
            try:
                data = sock.recv(4096)
                if not data:
                    continue
                msg = json.loads(data.decode())
                task_id = msg.get("task_id")
                if task_id:
                    tasks[task_id] = {"sock": sock, "request": msg}
                    print(f"[External] Stored task {task_id}", flush = True)
                    send_task_signal()
                else:
                    print("[External] Missing task_id in message", flush = True)
            except Exception as e:
                print(f"[External] Error: {e}", flush = True)

# 本地 TCP 监听线程（给 HTTP 页用）
def listen_local_server():
    if config.getboolean("local_server", "enabled", fallback=False):
        LOCAL_TCP_HOST = config.get("local_server", "host", fallback="0.0.0.0")
        LOCAL_TCP_PORT = config.getint("local_server", "port", fallback=7777)
        max_clients = config.getint("local_server", "max_clients", fallback=5)
    else:
        return ## local server not enabled.
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind((LOCAL_TCP_HOST, LOCAL_TCP_PORT))
    srv.listen(5)
    print(f"[LocalTCP] Listening on {LOCAL_TCP_HOST}:{LOCAL_TCP_PORT}", flush = True)
    while True:
        conn, addr = srv.accept()
        with conn:
            try:
                data = conn.recv(4096)
                if not data:
                    continue
                msg = json.loads(data.decode())
                task_id = msg.get("task_id")
                if task_id:
                    tasks[task_id] = {"sock": conn, "request": msg}
                    print(f"[LocalTCP] Stored task {task_id}", flush = True)
                    send_task_signal()
                else:
                    print("[LocalTCP] Missing task_id", flush = True)
            except Exception as e:
                print(f"[LocalTCP] Error: {e}", flush = True)

# Unix socket 监听线程（caller 连接）
def listen_unix():
    unix_sock_path_base = config.get("unix_socket", "path", fallback="/tmp/vim_channel_")
    temp = sys.argv[1]
    UNIX_SOCK_PATH = f"~/Documents/{temp}.sock"# the file name completely determined by
    UNIX_SOCK_PATH = os.path.expanduser(UNIX_SOCK_PATH)
    print("Trying path at", unix_sock_path, flush = True)
    if os.path.exists(UNIX_SOCKET_PATH):
        os.remove(UNIX_SOCKET_PATH)
    srv = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    srv.bind(UNIX_SOCKET_PATH)
    srv.listen(1)
    print(f"[UnixSock] Listening on {UNIX_SOCKET_PATH}", flush = True)
    while True:
        conn, _ = srv.accept()
        with conn:
            print("[UnixSock] Caller connected, sending tasks...", flush = True)
            send_task(conn)
            while True:
                data = conn.recv(4096)
                if not data:
                    break
                try:
                    msg = json.loads(data.decode())
                    task_id = msg.get("task_id")
                    if task_id and task_id in tasks:
                        sock = tasks[task_id]["sock"]
                        sock.sendall(json.dumps(msg).encode() + b"\n")
                        del tasks[task_id]
                        print(f"[UnixSock] Sent result for {task_id} back to origin", flush = True)
                    else:
                        print(f"[UnixSock] Unknown or missing task_id: {task_id}", flush = True)
                except Exception as e:
                    print(f"[UnixSock] Failed to process data: {e}", flush = True)

# stdin 监听线程
def listen_stdin():
    while True:
        line = sys.stdin.readline()
        if not line:
            continue
        if line.strip().lower() == "exit":
            raise KeyboardInterrupt
        print(f"[STDIN] {line.strip()}", flush = True)

if __name__ == "__main__":
    threading.Thread(target=listen_external, daemon=True).start()
    threading.Thread(target=listen_local_server, daemon=True).start()
    threading.Thread(target=listen_unix, daemon=True).start()
    threading.Thread(target=listen_stdin, daemon=True).start()
    print("[Main] channelv2.py started. Press Ctrl+C to stop.", flush = True)
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("[Main] Stopping...", flush = True)
