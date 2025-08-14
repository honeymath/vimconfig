import configparser
import signal
import json
import os
import socket
import sys
import socketio
import threading
from wsgiref import simple_server

# === The tasks collection
tasks = {}
# === 读取配置 ===
config_path = os.path.join(os.path.dirname(__file__), 'config.ini')
config = configparser.ConfigParser()
config.read(config_path)

# 外部 TCP 服务器
servers = []
for section in config.sections():
    if section.startswith("server:"):
        if config.getboolean(section, "enabled", fallback=True):
            servers.append({
                "name": section.split(":", 1)[1],
                "host": config.get(section, "host"),
                "port": config.getint(section, "port", fallback=0),
            })

# now we have to make client to connect to those remote socket servers, using socketio
def push_task(data,callback):
    import uuid
    task_id = str(uuid.uuid4())
    data["task_id"] = task_id
    # store the socket reference and request data in tasks dict
    tasks[task_id] = {"sock": callback, "request": data}  # ensure data is JSON serializable, replace the sock to callback fuckers.
    send_task_signal()  # notify worker to fetch this task

def send_task_signal():
    print("X", flush = True)## send fucking X to notify the worker to call fucker to receive fuck.
remote_sios = []
for srv in servers:
    try:
        sio_client = socketio.Client()

        @sio_client.event
        def connect():
            print(f"[Remote:{srv['name']}] connected")

        @sio_client.event
        def disconnect():
            print(f"[Remote:{srv['name']}] disconnected")

        @sio_client.event
        def message(data):
            print(f"[Remote:{srv['name']}] message: {data}")
#ai: just right here in the message , have to write down the logic to put to the fucking workflow and call the fucker by print X
            push_task(
                data=data,
                callback=lambda x: sio_client.emit("result", x)
            )
#end

        url = f"{srv['host']}"+(f":{srv['port']}" if int(srv['port'])>0 else "")
        print(f"Fucking connecting to {url}")
        sio_client.connect(url)
        remote_sios.append(sio_client)
    except Exception as e:
        print(f"[Remote:{srv['name']}] connection failed: {e}")
## The following is the unix socket
import socket

unix_enabled = config.getboolean("unix_socket", "enabled", fallback=False)
unix_sock_path = None

if unix_enabled:
    base_path = config.get("unix_socket", "path", fallback="~/")
    temp_id = sys.argv[1] if len(sys.argv) > 1 else ""
    unix_sock_path = os.path.expanduser(os.path.join(base_path, f"{temp_id}.sock"))
    if os.path.exists(unix_sock_path):
        os.remove(unix_sock_path)
    print(f"[channel_v5] Unix socket path: {unix_sock_path}")

    def send_task(conn):
        try:
            tasks_without_sock = {i:tasks[i]["request"] for i in tasks}
            data = tasks_without_sock.dump.encode("utf-8")
            conn.sendall(data + b"\n")
            print(f"[UnixSock] Sent {len(data)} bytes of task data", flush=True)
        except Exception as e:
            print(f"[UnixSock] Failed to send tasks: {e}", flush=True)

    def handle_unix_client(conn):
        try:
            print("[UnixSock] Caller connected, sending tasks...", flush = True)
            send_task(conn)
            buffer = b""
            while True:
                part = conn.recv(4096)
                if not part:
                    break  # connection closed
                buffer += part
                while b"\n" in buffer:
                    line, buffer = buffer.split(b"\n", 1)
                    try:
                        msg_text = line.decode("utf-8", errors='ignore').strip()
                        msg = json.loads(msg_text)
                    except json.JSONDecodeError:
                        print(f"[UnixSock] Invalid JSON: {line!r}")
                        continue
                    except Exception as e:
                        print(f"[UnixSock] Decode error: {e} | raw: {line!r}")
                        continue
                    task_id = msg.get("task_id")
                    if task_id and task_id in tasks:
                        suck = tasks[task_id]["sock"]
                        suck(line + b"\n")#fuck all suck all
                        del tasks[task_id]
                        print(f"[UnixSock] Sent result for {task_id} back to origin", flush = True)
                    else:
                        print(f"[UnixSock] the task id can not be identified.")
        except Exception as e:
            print(f"[External] Error: {e}", flush = True)
            print(f"[channel_v5] Unix socket message: {line}")
        finally:
            conn.close()

    def unix_socket_server():
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as server_sock:
            server_sock.bind(unix_sock_path)
            server_sock.listen(1)
            print(f"[channel_v5] Unix socket server listening at {unix_sock_path}")
            while True:
                conn, _ = server_sock.accept()
                threading.Thread(target=handle_unix_client, args=(conn,), daemon=True).start()

    threading.Thread(target=unix_socket_server, daemon=True).start()

# finally 本地 Socket.IO 服务替代 TCP 客户端连接, longiveity
from flask import Flask
from flask_socketio import SocketIO

local_server_enabled = config.getboolean("local_server", "enabled", fallback=False)
local_server_sock = None
def key_listener():
     for line in sys.stdin:
         if line.strip() == "x":
             # 向当前进程发送 Ctrl+C 信号
             print(f"kill {os.getpid()}")
             os._exit(0)
#             os.kill(os.getpid(), signal.SIGTERM)
#             os.kill(os.getpid(), signal.SIGINT)
 
listener_thread = threading.Thread(target=key_listener, daemon=True)
listener_thread.start()

if local_server_enabled:
    host = config.get("local_server", "host", fallback="127.0.0.1")
    port = config.getint("local_server", "port", fallback=5001)
    app_flask = Flask(__name__)
    socketio_flask = SocketIO(app_flask, cors_allowed_origins="*")

    @socketio_flask.on('connect')
    def handle_connect():
        print(f"[channel_v5] Local Socket.IO client connected")

#ai: am I right?
    from flask import request

    @socketio_flask.on('message')
    def message(data):
        sid = request.sid
        push_task(data=data, callback=lambda x: socketio_flask.emit("result", x, to=sid))
#end
    socketio_flask.run(app_flask, host=host, port=port,allow_unsafe_werkzeug=True)

