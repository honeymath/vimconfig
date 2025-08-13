def handler(**args):
    msg = "Hello World"
    print(msg)
    return {"message": msg, "args": args}