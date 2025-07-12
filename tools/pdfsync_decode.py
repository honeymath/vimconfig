import subprocess

def handler(**data):
    msg = data
    page = msg.get('pageNumber')
    x = msg.get('pageX_pdf')
    y = msg.get('pageY_pdf')
    pdf_file = msg.get('filestamp')

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
            return {"execute": f':e +{line_num} {tex_file}'}
        else:
            return {"error": f"无法解析 Synctex 输出: texfile or line_num is missing, tex_file={tex_file}, line_num={line_num}, data={data}"}
    else:
        return {"error": f"缺少必要的参数: page, x, y, pdf_file, data={data}"}
#                print(f':e +{line_num} {tex_file}', flush=True)
            # 或者直接调用 vim
            # subprocess.run(['vim', f'+{line_num}', tex_file])

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

