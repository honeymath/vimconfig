#ai: I want a socketio version of it, it has to use socketio to send messaged
from socketapp import socketio, Response
import uuid
import time

RESPONSE_TIMEOUT = 30  # seconds

class Client:
    def __init__(self, sid, server):
        self.sid = sid
        self.timestamp = int(time.time())
        self.server = server
        self.responses = {}  # task_id -> Response
        self.server.clients[sid] = self
        print(f"Client {sid} registered.")

    def send_task(self, command, target, args):
        resp = Response()
        self.responses[resp.uuid] = resp

        msg = {
            "task_id": resp.uuid,
            "command": command,
            "target": target,
            "args": args,
        }
        socketio.emit("task", msg, room=self.sid)
        print(f"Task {resp.uuid} sent to {self.sid}")

        if not resp.event.wait(RESPONSE_TIMEOUT):
            self.responses.pop(resp.uuid, None)
            raise TimeoutError(f"Task {resp.uuid} timed out waiting for response")

        return resp.result

    def handle_response(self, data):
        task_id = data.get("task_id")
        if task_id in self.responses:
            resp = self.responses.pop(task_id)
            resp.result = data
            resp.unlock()
        else:
            print(f"Unknown task_id {task_id} from {self.sid}")

class VimSocketServer:
    def __init__(self):
        self.clients = {}

    def start(self):
        pass

    def get_client(self, sid):
        return self.clients.get(sid)

server = VimSocketServer()

from flask import request

@socketio.on("connect")
def on_connect(auth):
    sid = str(request.sid)
    print(f"The {sid} connected.")
    return True

@socketio.on("client")
def put_client(*fucks, **args):
    sid = str(request.sid)
    Client(sid, server)

@socketio.on("disconnect")
def on_disconnect():
    sid = str(request.sid)
    if sid in server.clients:
        del server.clients[sid]
        print(f"Client {sid} disconnected.")

@socketio.on("task_result")
def on_task_result(data):
    sid = str(request.sid)
    client = server.get_client(sid)
    if client:
        client.handle_response(data)
#end
