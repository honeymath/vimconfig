## this file is a testing of worker mimicking


import subprocess
import time

## change the following code to python

def generate_uuid():
"""
    let chars = '0123456789abcdefghijklmnopqrstuvwxyz'
let s:t = localtime()
let s:shortts = ''
while s:t > 0
    let s:shortts = chars[s:t % 36] . s:shortts
    let s:t = s:t / 36
endwhile
"""
    import time
    import random
    chars = '0123456789abcdefghijklmnopqrstuvwxyz'
    s_t = int(time.time())
    shortts = ''
    while s_t > 0:
        shortts = chars[s_t % 36] + shortts
        s_t //= 36
    return shortts 
    
uuid = ""

def run_worker():
    global uuid
    uuid = generate_uuid()
    ## I want to run subprocess.run(["python3", "channelv3.py", uuid]), but also need a wrapper to simutaneously get its stdout and stderr, the code should be:
    import subprocess
    import sys
    import os
    import threading
    import io
    from contextlib import redirect_stdout, redirect_stderr
    stdout_buffer = io.StringIO()
    stderr_buffer = io.StringIO()
    #threading??  the target, channelv3.py I wanna run is a service, so should run as a thread, while the stdout and stderr should be captured, like an event call whenever it flushes, I should get it

def call_caller():
    global uuid
    ## 
    import caller
    caller.process_command(uuid)
    

