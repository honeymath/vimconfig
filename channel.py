import configparser
import signal
import json
import os
import socket
import sys
import socketio
import threading
from wsgiref import simple_server
import importlib

ai_traffic = threading.Event()
ai_traffic.set()
local_traffic = threading.Event()
local_traffic.set()
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


def run_task(data):
#    print(f"task received{json.dumps(data,indent=4)}", flush = True)
    print(f"[    {data.keys()}    ]", flush = True)
    print(f"    { 'command' in data}     ", flush = True)
    if data["command"] != "run_python_vim_script":
        raise Exception(f"Warning: we have to make sure data[command] is run_python_vim_script, bbut the command is {data['command']}")
        return {}
    tools_path = os.path.join(os.path.dirname(__file__), 'tools')
    results = {}
    target = data.get('target')
    args = data.get('args')

    if not target:
        data.update({'success': False, 'error': 'No target specified'})
        return data

    script_path = os.path.join(tools_path, f'{target}.py')
    if not os.path.exists(script_path):
        data.update({'success': False, 'error': f'Script not found: {script_path}'})
        return data

#    print(f'Executing script: {script_path} with args: {args}', flush=True)
#    print(f'Tools_path = {tools_path}', flush=True)


    sys.path.insert(0, tools_path)
    try:
        function_caller = importlib.import_module('function_caller')
        module = importlib.import_module(target)
        handler = getattr(module, 'handler')
        result = function_caller.call_function(handler, args)
        data.update({'success': True, 'result': result})
        return data
    except Exception as e:
        print(f' An error occurred while executing the script: {e}', flush=True)
        data.update({'success': False, 'error': str(e)})
        return data
    return data


for srv in servers:
    try:
        sio_client = socketio.Client()

        #@sio.on('server_forward')
        @sio_client.event
        def server_forward(data):
            print(f"收到 server_forward 消息:, {data}", flush=True)
            result = run_task(data) ## only get the result, not need to send back to anywhere
#            print(f"执行结果: {result}", flush=True)
#            print("X",flush=True)

        @sio_client.event
        def task(data):
            print("Receive task, run \n", flush = True)
            ai_traffic.clear()
            print("COMcall SendToWorker('{}')", flush = True)# actively clear the traffic please
            local_traffic.wait()# wait until it shut shit off.
            run_task(data)
            ai_traffic.set()
            sio_client.emit("task_result",data)        
    
        @sio_client.event
        def connect():
            print(f"[Remote:{srv['name']}] connected")

        @sio_client.event
        def disconnect():
            print(f"[Remote:{srv['name']}] disconnected")

        @sio_client.event
        def message(data):
            print(f"[Remote:{srv['name']}] message: {data}")
            push_task(
                data=data,
                callback=lambda x: sio_client.emit("result", x)
            )

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
    while True:
        line = ""
        while line == "":
            ai_traffic.wait()
            local_traffic.clear()
            line = input().strip()
            print(f"FUCK[{line}]", flush=True)
            local_traffic.set()
        print(f"FUCKNONTRIVIAL[{line}]", flush = True)
        data = json.loads(line)
        if data:
            run_task(data)
#    lines = []
#    for line in sys.stdin:
#        ai_traffic.wait()
#        line = line.strip()
#        if not line:
#            continue
#        lines.append(line)
#        try:
#            raw_json = '\n'.join(lines)
#            #print(f"Received json: {raw_json}", flush=True)
#            data = json.loads(raw_json)
#            run_task(data)
#            lines.clear()
#        except json.JSONDecodeError:
#            print("[WARNING]CAN NOT DECODE")
            # Wait for more lines until JSON is complete
#            continue
#         print(f"Reciva:{line}",flush=True)
#         if line.strip() == "x":
#            # 向当前进程发送 Ctrl+C 信号
#             print(f"kill {os.getpid()}")
#             os._exit(0)
#             os.kill(os.getpid(), signal.SIGTERM)
#             os.kill(os.getpid(), signal.SIGINT)
 
listener_thread = threading.Thread(target=key_listener, daemon=True)
listener_thread.start() # must disable fucking key listener

if local_server_enabled:
    host = config.get("local_server", "host", fallback="127.0.0.1")
    port = config.getint("local_server", "port", fallback=5001)
    app_flask = Flask(__name__)
    from socketapp import socketio as socketio_flask # 导入socketio
#    socketio_flask = SocketIO(app_flask, cors_allowed_origins="*")
    socketio_flask.init_app(app_flask, cors_allowed_origins="*")  # 初始化 SocketIO

    try:
        from services.syncpdf_remote.send_socket_message_to_pdfjs import pdf_routes
        from services.syncpdf_remote.register_server_event import register_socketio_handlers
        app_flask.register_blueprint(pdf_routes)
        register_socketio_handlers(socketio_flask)  # 注册 SocketIO 事件处理器
    except ImportError:
        print("[Warning]pdf_routes not found, skipping PDF routes registration.")
        warnings.append("[Warning]pdf_routes not found, skipping PDF routes registration.")

    @socketio_flask.on('pdf_control_receive')
    def handle_my_event(data):
        print("FUCKING RECEIVA THE DATA",flush=True)
        msg = {
            "command": "run_python_vim_script",
            "target": "pdfsync_decode",
            "args": data,
#            "task_id": task_id # no taskid since not expected to get return of it
        }
        run_task(msg) ## only get the result, not need to send back to anywhere
#        socketio.emit('server_forward',  msg)

    @socketio_flask.on('connect')
    def handle_connect():
        print(f"[channel_v5] Local Socket.IO client connected")

    from flask import request

    @socketio_flask.on('message')
    def message(data):
        sid = request.sid
        push_task(data=data, callback=lambda x: socketio_flask.emit("result", x, to=sid))
    socketio_flask.run(app_flask, host=host, port=port,allow_unsafe_werkzeug=True)

