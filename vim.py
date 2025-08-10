# vim.py - Monkey patch of Vim API for external execution
_callback_to_worker = None

def set_callback(cb):
    global _callback_to_worker
    _callback_to_worker = cb

class _Window:
    @property
    def cursor(self):
        if not _callback_to_worker:
            raise RuntimeError("Vim callback not set")
        return _callback_to_worker("get_cursor", {})

class _Current:
    @property
    def buffer(self):
        if not _callback_to_worker:
            raise RuntimeError("Vim callback not set")
        return _callback_to_worker("get_buffer", {})
    window = _Window()

current = _Current()

def eval(expr):
    if not _callback_to_worker:
        raise RuntimeError("Vim callback not set")
    return _callback_to_worker("eval", {"expr": expr})

def command(cmd):
    if not _callback_to_worker:
        raise RuntimeError("Vim callback not set")
    return _callback_to_worker("command", {"cmd": cmd})