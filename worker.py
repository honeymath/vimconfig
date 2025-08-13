import multiprocessing
import socketio
import configparser
import os
import time
import importlib

def run_channel_v3():
    os.system(f"python3 {os.path.join(os.path.dirname(__file__), 'channel_v3.py')} testid")

if __name__ == "__main__":
    config_path = os.path.join(os.path.dirname(__file__), "config.ini")
    config = configparser.ConfigParser()
    config.read(config_path)
    host = config.get("server", "host", fallback="0.0.0.0")
    port = config.getint("server", "port", fallback=8765)

    p = multiprocessing.Process(target=run_channel_v3)
    p.start()
    time.sleep(2)  # 等待 server 启动

    sio = socketio.Client()

    @sio.on("connect")
    def on_connect():
        print("[worker] Connected to channel_v3")

    @sio.on("disconnect")
    def on_disconnect():
        print("[worker] Disconnected from channel_v3")

    @sio.on("x")
    def on_x(data):
        print(f"[worker] Received 'x' event: {data}")
        try:
            color_module = importlib.import_module("color")
            if hasattr(color_module, "handler"):
                result = color_module.handler()
                print(f"[worker] color.py handler() result: {result}")
            else:
                print("[worker] No handler() found in color.py")
        except Exception as e:
            print(f"[worker] Error calling color.py: {e}")

    sio.connect(f"http://{host}:{port}")
    sio.wait()