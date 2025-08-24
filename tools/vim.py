import json
def command(text):
    print(f"COM{text}", flush = True)
def eval(text):
#    print("X",flush = True)
#    print(f"COMcall SendToWorker('fuck')", flush = True)
    print(f"VAL{text}", flush = True)
    line = ""
    while line == "":
        print("fucking read", flush = True)
        line = input().strip()
    print(f"I jump out, because the line value is now [{line}]", flush = True)
    return json.loads(line)

