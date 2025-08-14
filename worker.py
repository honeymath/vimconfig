import multiprocessing
import socketio
import configparser
import os
import time
import importlib


#ai: I want to run a background service process for this program, and able to capture its stderr and stdout, whwat should I do , the following seems not correct
import subprocess
import threading

p = subprocess.Popen(
    ["python", os.path.join(os.path.dirname(__file__), "channel.py"), "d"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)

def read_stream(stream, name):
    for line in iter(stream.readline, ''):
        print(f"[{name}] {line}", end='')

threading.Thread(target=read_stream, args=(p.stdout, "STDOUT"), daemon=True).start()
threading.Thread(target=read_stream, args=(p.stderr, "STDERR"), daemon=True).start()


time.sleep(6)  # 等待 server 启动
#p.stdin.write("x\n")
#p.stdin.flush()
p.stdout.flush()
p.terminate()
p.kill()
time.sleep(2)
p.stdout.flush()


time.sleep(3)  # 等待 server 启动
p.stdout.flush()
#end
