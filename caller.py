#caller.py

import json
import importlib.util
import sys
import os

tasks = {}

#ai: please try to write the codes
def process_commands(socket):
    
    file_path = os.path.dirname(os.path.abspath(__file__))
    socket_path = os.path.join(file_path, socket)

    if not os.path.exists(socket_path):
        print(f"[Caller] Unix socket not found: {socket_path}")
        return

    try:
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        sock.connect(socket_path)
        print(f"[Caller] Connected to {socket_path}")
    except Exception as e:
        print(f"[Caller] Failed to connect: {e}")
        return

    # Step 1: 接收任务数据
    try:
        raw_data = sock.recv(65536)  # 假设任务数据一次发完
        if not raw_data:
            print("[Caller] No data received")
            sock.close()
            return
        msgs = json.loads(raw_data.decode())
    except Exception as e:
        print(f"[Caller] Invalid JSON: {e}")
        sock.close()
        return

    # Step 2: 存任务
    if not isinstance(msgs, dict) or "tasks" not in msgs:
        print("[Caller] Invalid tasks format")
        sock.close()
        return

    for tid, request in msgs["tasks"].items():
        tasks[tid] = request

    # Step 3: 处理任务
    for tid, request in list(tasks.items()):
        print(f"[Caller] Processing task {tid}")
        result_json = handle_external_message(request)
        try:
            sock.sendall(result_json.encode() + b"\n")
            print(f"[Caller] Sent result for task {tid}")
        except Exception as e:
            print(f"[Caller] Failed to send result for {tid}: {e}")
        del tasks[tid]

    sock.close()
    print("[Caller] Finished all tasks")
#end


def handle_external_message(msg):

    target = msg.get("target")
    args = msg.get("args", {})
    task_id = msg.get("task_id")

    if not target:
        return json.dumps({"success": False, "error": "Missing target", "task_id": task_id})

    tool_path = os.path.join(os.path.dirname(__file__), "tools", f"{target}.py")
    if not os.path.exists(tool_path):
        return json.dumps({"success": False, "error": f"Tool '{target}' not found", "task_id": task_id})

    try:
        spec = importlib.util.spec_from_file_location(target, tool_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        if hasattr(module, "handler"):
#ai:when handle this module.handler, need a wrapper pls, need to know its errout and printout and all infos! Consider includes a wrapper? need stdout, etc, please double check the tools/function_caller.py
            import io
            import sys
            import traceback
            from contextlib import redirect_stdout, redirect_stderr

            stdout_buffer = io.StringIO()
            stderr_buffer = io.StringIO()

            try:
                with redirect_stdout(stdout_buffer), redirect_stderr(stderr_buffer):
                    result_data = module.handler(**args)
                result = {
                    "success": True,
                    "result": result_data,
                    "stdout": stdout_buffer.getvalue(),
                    "stderr": stderr_buffer.getvalue(),
                    "task_id": task_id,
                    "error": ""
                }
            except Exception:
                result = {
                    "success": False,
                    "result": "",
                    "stdout": stdout_buffer.getvalue(),
                    "stderr": stderr_buffer.getvalue(),
                    "task_id": task_id,
                    "error": traceback.format_exc()
                }
            return json.dumps(result)
#end


