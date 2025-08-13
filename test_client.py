import socketio

sio = socketio.Client()

@sio.on("connect")
def on_connect():
    print("[test_client] Connected to server")
    # 连接后立即发送 x 事件
    sio.emit("x", {"msg": "hello from test_client"})

@sio.on("disconnect")
def on_disconnect():
    print("[test_client] Disconnected from server")

sio.connect("http://0.0.0.0:8765")
sio.wait()