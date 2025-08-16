import subprocess
import os
import sys
import json




def handler(**data):
    tool_path = os.path.dirname(__file__)
    FILE_MAP_PATH = os.path.join(tool_path, "../static/file_map.json")
    REVERSE_MAP_PATH = os.path.join(tool_path, "../static/reverse_map.json")
    with open(FILE_MAP_PATH, "r", encoding="utf-8") as f:
        file_map = json.load(f)
    with open(REVERSE_MAP_PATH, "r", encoding="utf-8") as f:
        reverse_map = json.load(f)
    msg = data
    page = msg.get('pageNumber')
    x = msg.get('pageX_pdf')
    y = msg.get('pageY_pdf')
    pdf_file = msg.get('filestamp')

#    print(f"THE HANDLER FUNCTION pdfsync_decode.py with {data}", flush=True)
#    print(f"page: {page}, x: {x}, y: {y}, pdf_file: {pdf_file}", flush=True)
#    print(f"The maps path are {FILE_MAP_PATH} and {REVERSE_MAP_PATH}", flush=True)
#    print(f"File map keys: {list(file_map.keys())[:5]}...", flush=True)
#    print(f"Reverse map keys: {list(reverse_map.keys())[:5]}...", flush=True)
    
    page = str(page)

    if page not in reverse_map:
        raise Exception(f"Cannot identify page {page} in the reverse map")

    page_details = reverse_map[page]
    all_y = sorted(map(float, page_details.keys()))

    nexty = None
    for val in all_y:
        if val > y:
            nexty = val
            break
    if nexty is None:
        raise Exception(f"No y-coordinate greater than {y} found for page {page}")

    line_details = page_details[str(nexty)]
    all_x = sorted(map(float, line_details.keys()))

    nextx = None
    for val in all_x:
        if val > x:
            nextx = val
            break
    if nextx is None:
        nextx = all_x[-1]

    fileindex, line = line_details[str(nextx)]

##    print(f"Filekeys: {file_map.keys()}")
    fileindex = str(fileindex)
    if fileindex not in file_map:
        raise Exception(f"Not able to find the file index {fileindex} in the file map")

    filepath = os.path.normpath(os.path.expanduser(file_map[fileindex])).strip()
    print(f"E +{line} {filepath}", flush=True)
    return filepath, line







if __name__ == "__main__":
    if len(sys.argv) != 4:
        print(f"Usage: {sys.argv[0]} <page> <x> <y>")
        sys.exit(1)

    try:
        page_arg = str(sys.argv[1])
        x_arg = float(sys.argv[2])
        y_arg = float(sys.argv[3])
    except ValueError:
        print("x and y must be numbers")
        sys.exit(1)

    result_path, result_line = handler(pageNumber = page_arg, pageX_pdf = x_arg, pageY_pdf = y_arg,filestamp = "")
    print(result_path, result_line)
#end
        
        
        



"""
    if page and x and y and pdf_file:
        synctex_cmd = ['synctex', 'edit', '-o', f'{page}:{x}:{y}:{pdf_file}']
        result = subprocess.run(synctex_cmd, check=True, stdout=subprocess.PIPE, text=True)
        for line in result.stdout.strip().splitlines():
            if line.startswith('Input:'):
                tex_file = line.split(':', 1)[1].strip()
            elif line.startswith('Line:'):
                line_num = line.split(':', 1)[1].strip()
        if tex_file and line_num:
            import vim
            vim.command(f':e +{line_num} {tex_file}')
            vim.vars['exec'] = f'e +{line_num} {tex_file}'
            return {"execute": f':e +{line_num} {tex_file}'}
        else:
            return {"error": f"无法解析 Synctex 输出: texfile or line_num is missing, tex_file={tex_file}, line_num={line_num}, data={data}"}
    else:
        return {"error": f"缺少必要的参数: page, x, y, pdf_file, data={data}"}
#                print(f':e +{line_num} {tex_file}', flush=True)
            # 或者直接调用 vim
            # subprocess.run(['vim', f'+{line_num}', tex_file])
"""
#def on_server_forward(data):
#    print("收到 server_forward 消息:", data)
#    msg = data.get('msg', {})
#    page = msg.get('pageNumber')
#    x = msg.get('pageX_pdf')
#    y = msg.get('pageY_pdf')
#    pdf_file = msg.get('filestamp')
#    if page and x and y and pdf_file:
#        cmd = ['synctex', 'edit', '-o', f'{page}:{x}:{y}:{pdf_file}']
#        try:
#            result = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, text=True)
#            output = result.stdout.strip()
#            print("SyncTeX 返回:", output)
#            with open('synctex_output.txt', 'w') as f:
#                f.write(output)
#            # 可以自动打开编辑器
##            if output:
##                parts = output.split(':')
##                tex_file = parts[0]
##                line_num = parts[1]
##                print(f"打开编辑器: {tex_file} 行 {line_num}")
#        except Exception as e:
#            print("Synctex 调用失败:", e)
#
#if __name__ == '__main__':
#    try:
#        sio.connect('http://localhost:5001')
#        sio.wait()  # 阻塞在这里，持续监听
#    except Exception as e:
#        print("连接失败:", e)

