#caller.py

import json
import importlib.util
import sys

#ai: Here read the unix socket address form the first argument 
socket = sys.argv[1]

#ai: In this part , the logic of obtain command from socket, the output is a json
def obtain_commands(socket):
#Here from the socket to read the data
    try:
        msgs = json.loads(raw_data.decode())
    except Exception as e:
        return json.dumps({"success": False, "error": f"Invalid JSON: {e}"})
    pass
# the return should be a dictionary of tasks
#end

# Here we should also have some managers to call the tasks each each


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
#ai:when handle this module.handler, need a wrapper pls, need to know its errout and printout and all infos!
            result = module.handler(**args)
#end
            return json.dumps({"success": True, "result": result, "task_id": task_id})
        else:
            return json.dumps({"success": False, "error": "No handler() in tool", "task_id": task_id})

    except Exception as e:
        return json.dumps({"success": False, "error": str(e), "task_id": task_id})
