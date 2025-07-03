import vim

def handler(**args):
    result = {
        "message": "Hello World Executed",
        "received_args": args
    }
    print("Hello from Vim tool!")
    print(f"Args received: {args}")
    return result