import socketio
import subprocess

# 创建客户端实例
sio = socketio.Client()

@sio.event
def connect():
#    print("已连接到服务器")
#    print("已连接到服务器",flush=True)
    pass

@sio.event
def disconnect():
    pass
#    print("与服务器断开连接")

@sio.on('server_forward')
def on_server_forward(data):
#    print("收到 server_forward 消息:", data, flush=True)
    msg = data.get('msg', {})
    page = msg.get('pageNumber')
    x = msg.get('pageX_pdf')
    y = msg.get('pageY_pdf')
    pdf_file = msg.get('filestamp')

    if page and x and y and pdf_file:
        synctex_cmd = ['synctex', 'edit', '-o', f'{page}:{x}:{y}:{pdf_file}']
        try:
            result = subprocess.run(synctex_cmd, check=True, stdout=subprocess.PIPE, text=True)
            for line in result.stdout.strip().splitlines():
                if line.startswith('Input:'):
                    tex_file = line.split(':', 1)[1].strip()
                elif line.startswith('Line:'):
                    line_num = line.split(':', 1)[1].strip()
            if tex_file and line_num:
                print(f':e +{line_num} {tex_file}', flush=True)
                # 或者直接调用 vim
                # subprocess.run(['vim', f'+{line_num}', tex_file])
        except Exception as e:
            pass  # 安静忽略错误，按主人要求

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
if __name__ == '__main__':
    try:
        sio.connect('http://localhost:5001')
        sio.wait()  # 阻塞在这里，持续监听
    except Exception as e:
        print("连接失败:", e)

