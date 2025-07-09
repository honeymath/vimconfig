from parser import Parser, get_element_near_cursor
import json
from collections import defaultdict
import vim

def get_current_buffer():
    # ✨ 输入数据
    """
    lines = [
        "#see:should be ignored",
        "#ai: Plan A",
        "#see: Start",
        "#ai: Plan B",
        "Step 1",
        "#ai: More Thoughts",
        "Step 2",
        "#ai: Final Decision",
        "Step 3",
        "Continue step 3",
        "Another thing#ai:just jump",
        "Step4",
        "#end",
        "Other test",
        "#end",
        "Test",
        "Testa!",
        "#end",
        "Other content..."
        "#end",
    ]
    """
#### the 
    import vim
    return vim.current.buffer
#    return list(vim.current.buffer)
    #return lines

def get_position_by_marker(marker):
#    position = 8
#    return position
    import vim
    pos = vim.eval(f"getpos(\"'{marker}\")")  # getpos returns [bufnum, lnum, col, off]
    line_number = int(pos[1]) - 1  # Vim 行号从1开始，Python从0开始
    return line_number

    # ✨ 模拟获取光标位
def get_current_cursor_position():
#    """获取当前光标位置"""
#    cursor = 7  # 光标落在 "Step B1" 这一行
#    marker = 'a' 
#    return cursor,marker # mimicking using vim to marker.
    import vim
    # 1. 获取当前光标位置（0-based）
    cursor = vim.current.window.cursor[0] - 1

    ## test the following later
    # 2. 获取所有已设置的 mark 列表（包含 ['markname', bufnr, lnum, col, ...]）
    marks = vim.eval("getmarklist(bufnr('%'))")

    used_marks = {entry['mark'] for entry in marks if entry['mark'].isalpha() and entry['mark'].islower()}
    # 3. 在 A-Z 中找一个没用的 mark 名
    for c in map(chr, range(ord('a'), ord('z') + 1)):
        if c not in used_marks:
            marker = c
            if len(used_marks) > 24: # if this marker is the only left marker
                next_letter = chr((ord(c) - ord('a') + 1) % 26 + ord('a'))  # 循环使用 'a' 到 'z'
                vim.command(f"delmarks {next_letter}")  # predelete the next one.
            break
    else:
        # 万一全满了，就 fallback 用 'a'
        marker = 'a'
    
    vim.command(f"execute 'normal! m{marker}'")
    return cursor, marker

def handler(**args):
    level = 1 ## looking for only 1 extra level
    if "marker" in args:
        marker = args["marker"]
        cursor = get_position_by_marker(marker)
    else:
        cursor,marker = get_current_cursor_position()
    lines = get_current_buffer()
    ## going backwards 
    badcursor=cursor-1
    resrap = Parser(mode='reverse')
    resrap.stack.scale = -1
    resrap.set_syntax_chars(comment_char='#', escape_char='##')
    resrap.stack[-1].new_context_child(metadata={}) #initialize
    while resrap.stack.len() > -level and badcursor >= 0:
        resrap.parse(lines[badcursor])
        badcursor -= 1
    resrap.reverse_handle_block_match('', {}, '')  #SOF




    # status tranfer 
    parser = Parser(mode='normal')
    for index, regret in enumerate(resrap.stack._history):
        parser.stack[-1 - index].type = regret.type
    parser.state = parser.stack[-1].type
    parser.set_syntax_chars(comment_char='#', escape_char='##')

    ## now going forward
    goodcursor = cursor
    parser.stack[-1].new_context_child(metadata={}) ## SOF
    while parser.stack.len() > -level-1 and goodcursor < len(lines):
        parser.parse(lines[goodcursor])
        goodcursor += 1

    ## now combine history and future
    history = resrap.stack._history
    future = parser.stack._history


    ### debug
    #for i in range(len(history)):
    #    print(f"History {i}: {history[i]}")
    #    print("-" * 40)

    #for i in range(len(future)):
    #    print(f"Future {i}: {future[i]}")
    #    print("-" * 40)
    ### debug

    ## printing element near the cursor
    current_element = get_element_near_cursor(history, future);

    ## Finnaly, get the element
    fala = None
    for i in range(level+1):
        if i >= len(history):
            break ### protect, safe.
        history[i].reverse()
        if fala:
            history[i].giveback_child(fala)
            history[i].new_context_child(metadata={})
        history[i].update(future[i])
        fala = history[i]
    return {"current": current_element.to_dict(), "annotated_context": fala.to_dict(), "marker":marker, "scanned_context":lines[badcursor:goodcursor]}

if __name__ == "__main__":
    result = handler() 
    print(json.dumps(result, indent=2))
