import configparser
import os
import socket
import uuid

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
local_server_sock = None
if config.getboolean("local_server", "enabled", fallback=False):
    host = config.get("local_server", "host", fallback="0.0.0.0")
    port = config.getint("local_server", "port", fallback=7777)
    max_clients = config.getint("local_server", "max_clients", fallback=5)
    local_server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    local_server_sock.bind((host, port))
    local_server_sock.listen(max_clients)
    print(f"Local TCP server listening on {host}:{port}")

# ===== 初始化 Unix socket =====
unix_sock_path_base = config.get("unix_socket", "path", fallback="/tmp/vim_channel_")
unix_sock_path = f"{unix_sock_path_base}{uuid.uuid4().hex}.sock"
if os.path.exists(unix_sock_path):
    os.remove(unix_sock_path)

unix_sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
unix_sock.bind(unix_sock_path)
unix_sock.listen(1)
print(f"Unix socket listening at {unix_sock_path}")

# ===== 主循环（示例） =====
try:
    while True:
        conn, _ = unix_sock.accept()
        with conn:
            data = conn.recv(4096)
            if not data:
                continue
            print(f"Received from Vim: {data.decode().strip()}")
            conn.sendall(b"ack\n")
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
