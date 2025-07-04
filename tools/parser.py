import re
import patterns

# 🐾 初始化
root = {'type': 'root', 'header': '', 'children': [], 'content': [], 'metadata': {}}
stack = [root]

# 🐾 编译模式
compiled_escape = re.compile(patterns.ESCAPE_PATTERN)
compiled_block = {k: re.compile(v) for k, v in patterns.BLOCK_PATTERNS.items()}
compiled_meta = {k: re.compile(v) for k, v in patterns.META_PATTERNS.items()}
compiled_oneline = {k: re.compile(v) for k, v in patterns.ONELINE_PATTERNS.items()}
compiled_inline = {k: re.compile(v) for k, v in patterns.INLINE_PATTERNS.items()}


# 🐾 主函数骨架
def parse(lines,extra_end_callback=None):
    for line in lines:
        line = line.rstrip('\n')
        
        # 检查 escape
        if compiled_escape.match(line):
            stack[-1]['content'].append(line.lstrip(patterns.escape_char).strip())  ## what ? why not just append line, why strip ?
            continue
        
        # 检查 end
        if compiled_block.get('end') and compiled_block['end'].match(line):
            if len(stack) > 1:
                stack.pop()
            else:
                print("⚠️ 多余的 end 被忽略") ## no, here just do some callback. I have added a extra_end_callback parameter to parse function.
            continue
        
        # 检查 block
        matched = False
        for k, regex in compiled_block.items():
            if k == 'end':
                continue
            m = regex.match(line)
            if m:
                # TODO: 新建 node 并入栈（watch 特殊处理）
                matched = True
                break
        if matched:
            continue
        
        # 检查 metadata
        for k, regex in compiled_meta.items():
            m = regex.match(line)
            if m:
                # TODO: 更新当前 node metadata
                matched = True
                break
        if matched:
            continue

        # 检查 oneline block
        for k, regex in compiled_oneline.items():
            m = regex.search(line)
            if m:
                # TODO: 新建 oneline node，直接挂到当前栈顶
                matched = True
                break
        if matched:
            continue
        
        
        # 检查 inline
        # TODO: 根据当前模式检查 inline 匹配并生成子 node
        
        # 普通内容
        stack[-1]['content'].append(line)
    
    if len(stack) > 1:
        print("⚠️ 有未闭合的块")
    return root

# 🐾 示例入口
def main():
    with open('test.md', 'r') as f:
        lines = f.readlines()
    tree = parse(lines)
    print(tree)

if __name__ == '__main__':
    main()
