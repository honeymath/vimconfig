#caller.py

import json
import importlib.util

def handle_external_message(raw_data):
    try:
        msg = json.loads(raw_data.decode())
    except Exception as e:
        return json.dumps({"success": False, "error": f"Invalid JSON: {e}"})

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
            result = module.handler(**args)
            return json.dumps({"success": True, "result": result, "task_id": task_id})
        else:
            return json.dumps({"success": False, "error": "No handler() in tool", "task_id": task_id})

    except Exception as e:
        return json.dumps({"success": False, "error": str(e), "task_id": task_id})
