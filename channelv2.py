import os
import sys
import json
import socket
import threading
import select

# 全局任务表 {task_id: {"sock": socket_obj, "request": 原始JSON}}
tasks = {}

# 配置
UNIX_SOCKET_PATH = "/tmp/vim_channel.sock"  # Unix socket 路径
LOCAL_TCP_HOST = "127.0.0.1"
LOCAL_TCP_PORT = 9001  # 给本地 HTTP 页用的 TCP 服务
EXTERNAL_SERVERS = [("127.0.0.1", 8000)]  # 外部 TCP 服务器列表

# 发送启动 caller 的信号（需要根据你的 Vim 环境实现）
def send_task_signal():
    print("[Signal] Would trigger Vim worker to start caller here.")

# 批量派发任务给 caller
def send_task(caller_sock):
    if not tasks:
        print("[Dispatcher] No tasks to send.")
        return
    payload = {"tasks": {tid: info["request"] for tid, info in tasks.items()}}
    caller_sock.sendall(json.dumps(payload).encode() + b"\n")
    print(f"[Dispatcher] Sent {len(tasks)} tasks to caller.")

# 外部 TCP 监听线程
def listen_external():
    tcp_sockets = []
    # 主动连接外部服务器
    for host, port in EXTERNAL_SERVERS:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((host, port))
            tcp_sockets.append(s)
            print(f"[External] Connected to {host}:{port}")
        except Exception as e:
            print(f"[External] Failed to connect {host}:{port} - {e}")
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
                    print(f"[External] Stored task {task_id}")
                    send_task_signal()
                else:
                    print("[External] Missing task_id in message")
            except Exception as e:
                print(f"[External] Error: {e}")

# 本地 TCP 监听线程（给 HTTP 页用）
def listen_local_server():
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind((LOCAL_TCP_HOST, LOCAL_TCP_PORT))
    srv.listen(5)
    print(f"[LocalTCP] Listening on {LOCAL_TCP_HOST}:{LOCAL_TCP_PORT}")
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
                    print(f"[LocalTCP] Stored task {task_id}")
                    send_task_signal()
                else:
                    print("[LocalTCP] Missing task_id")
            except Exception as e:
                print(f"[LocalTCP] Error: {e}")

# Unix socket 监听线程（caller 连接）
def listen_unix():
    if os.path.exists(UNIX_SOCKET_PATH):
        os.remove(UNIX_SOCKET_PATH)
    srv = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    srv.bind(UNIX_SOCKET_PATH)
    srv.listen(1)
    print(f"[UnixSock] Listening on {UNIX_SOCKET_PATH}")
    while True:
        conn, _ = srv.accept()
        with conn:
            print("[UnixSock] Caller connected, sending tasks...")
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
                        print(f"[UnixSock] Sent result for {task_id} back to origin")
                    else:
                        print(f"[UnixSock] Unknown or missing task_id: {task_id}")
                except Exception as e:
                    print(f"[UnixSock] Failed to process data: {e}")

# stdin 监听线程
def listen_stdin():
    while True:
        line = sys.stdin.readline()
        if not line:
            continue
        if line.strip().lower() == "exit":
            raise KeyboardInterrupt
        print(f"[STDIN] {line.strip()}")

if __name__ == "__main__":
    threading.Thread(target=listen_external, daemon=True).start()
    threading.Thread(target=listen_local_server, daemon=True).start()
    threading.Thread(target=listen_unix, daemon=True).start()
    threading.Thread(target=listen_stdin, daemon=True).start()
    print("[Main] channelv2.py started. Press Ctrl+C to stop.")
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("[Main] Stopping...")