import re
import patterns
from defaultstack import DefaultStack
class Node:
    def __init__(self, type, content=[], metadata=[]):
        self.type = type
        self.children = []
        self.content = content 
        self.metadata = metadata
stack = DefaultStack(Node)
state = ""
# 🐾 编译模式 the block escape meta can be combined
compiled_escape = re.compile(patterns.ESCAPE_PATTERN)
compiled_block = {k: re.compile(v) for k, v in patterns.BLOCK_PATTERNS.items()}
compiled_meta = {k: re.compile(v) for k, v in patterns.META_PATTERNS.items()}
compiled_oneline = {k: re.compile(v) for k, v in patterns.ONELINE_PATTERNS.items()}
compiled_inline = {k: re.compile(v) for k, v in patterns.INLINE_PATTERNS.items()}
# 🐾 辅助函数
def handle_block_match(k, m):
    oldstate,state = state,k
    if state == 'end':
        stack.pop()
    elif state == 'watch':
        stack.push(Node(type='watch', metadata=m.groupdict()))
    elif state == oldstate:
        stack[-1]['children'].append(Node(type='context', metadata=m.groupdict()))
    else: 
        stack.push(Node(type='watch'),metadata=m.groupdict())

def reverse_handle_block_match(k, m):
    oldstate, state = state, k
    if state == 'end':
        stack.push(Node(type='end', metadata=m.groupdict()))
    elif state == 'watch':
        stack[-1].type = 'watch'
        ### then I have to write the metadata
        stack.pop()
    elif state == oldstate or oldstate == 'end':
        stack[-1]['children'].append(Node(type='context', metadata=m.groupdict()))
        return
    else:
        giveme = stack[-1]['children'].pop()
        stack[-1].type = oldstate
        stack.pop()
        stack[-1]['children'].append(giveme) ## need mathematical proof stack[-1] always exists.

# 🐾 主函数骨架
def parse(line):#only parse one line
    line = line.rstrip('\n')
    if compiled_escape.match(line):#escape
        stack[-1].children[-1].content.append(line)
        return
    for k, regex in compiled_block.items():#block match and meta, need matching groups 1.
        if(m:= regex.search(line)):
            handle_block_match(k, m.group(1), stack)
            return
    for k, regex in compiled_oneline.items():#oneline match, matching groups 1.
        if(m:= regex.search(line)):
            stack[-1].children.append(Node(type=k, metadata={k:m.group(1)}))# oneline match
            return
    for match in compiled_inline["ai"].match.groups(line): ## only match ai, not others.
        stack[-1].children[-1].content.append(Node(type="ai"))
    stack[-1].children[-1].content.append(line)#non-match
