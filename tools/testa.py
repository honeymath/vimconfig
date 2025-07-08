from parser import Parser, get_element_near_cursor
import json

lines = [
    "#see:should be ignored",
    "#ai: Plan",
    "#see: Start",
    "#ai: Plan",
    "Step 1",
    "#ai: More Thoughts",
    "Step 2",
    "#ai: Final Decision",
    "Step 3",
    "#end",
    "Other test",
    "#end",
    "Test",
    "#end",
    "Other content..."
    "#end",
]
cursor = 7  # 光标行的位置
level = 2
# 1. 向前回溯
resrap = Parser(mode='reverse')
resrap.stack.scale = -1
resrap.set_syntax_chars(comment_char='#', escape_char='##')
resrap.stack[-1].new_context_child(metadata={})

badcursor = cursor - 1
while resrap.stack.len() > -level and badcursor >= 0:
    resrap.parse(lines[badcursor])
    badcursor -= 1

resrap.reverse_handle_block_match('', {}, '')  # glue line

# 2. 状态传递
parser = Parser(mode='normal')
for index, regret in enumerate(resrap.stack._history):
    parser.stack[-1 - index].type = regret.type
parser.state = parser.stack[-1].type
parser.set_syntax_chars(comment_char='#', escape_char='##')
parser.stack[-1].new_context_child(metadata={}) ## SOF

# 3. 向后拼接
goodcursor = cursor
while parser.stack.len() > -level-1 and goodcursor < len(lines):
    parser.parse(lines[goodcursor])
    goodcursor += 1

# 4. 合并历史和未来（包含辅助变量 fala）
history = resrap.stack._history
future = parser.stack._history
fala = None
for i in range(level+1):
    history[i].reverse()
    if fala:
        history[i].giveback_child(fala)
        history[i].new_context_child(metadata={})
    history[i].update(future[i])
    fala = history[i]

# 5. 输出最终结构
print("Test data:"
      )
for line in lines:
    print(line)
print("Final Result:")
print(fala.to_json(indent=2))
