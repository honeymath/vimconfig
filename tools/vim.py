import json
def command(text):
    print(f"COM{text}", flush = True)
def eval(text):
    print(f"VAL{text}", flush = True)
    return json.loads(input())

