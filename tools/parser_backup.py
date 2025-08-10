from defaultstack import DefaultStack
from collections import defaultdict
class Node:
    def __init__(self, type, content=[], metadata={}):
        self.type = type
        self.children = []
        self.content = content 
        self.metadata = defaultdict(list)
        self.add_metadata(metadata)
    def new_context_child(self,metadata={},type='context'):
        self.children.append(Node(type=type, metadata=metadata))
    def borrow_child(self):
        return self.children.pop()
    def giveback_child(self,child):
        self.children.append(child)
    def new_non_context_child(self, type='', metadata={}): 
        child = Node(type=type, metadata=metadata)
        child.new_context_child() # appending a context child
        self.children.append(child) # appending a new child
        return child
    def add_metadata(self, metadata):
        lastchild = self.children[-1]
        for k, v in metadata.items():
            lastchild.metadata[k].append(v)
    def add_inline_children(self,type, line, groups):
        child = self.new_non_context_child(type='inline')
        for k,v in groups.items():
            child.new_non_context_child(type=type)
stack = DefaultStack(Node)
state = ""
# 🐾 编译模式 the block escape meta can be combined
import re
from patterns import META,BLOCK_PATTERNS, ONELINE_PATTERNS, INLINE_PATTERNS
compiled_escape = re.compile(patterns.ESCAPE_PATTERN)
compiled_block = {k: re.compile(v) for k, v in patterns.BLOCK_PATTERNS.items()}
compiled_oneline = {k: re.compile(v) for k, v in patterns.ONELINE_PATTERNS.items()}
compiled_inline = {k: re.compile(v) for k, v in patterns.INLINE_PATTERNS.items()}
# 🐾 辅助函数
def handle_block_match(type,metadata, line):
    global state
    if k in META:
        stack[-1].add_metadata(metadata={type:metadata})
        return
    oldstate,state = state,type
    if state == 'end':
        stack.pop()
    elif state == 'watch':
        stack.append(stack[-1].new_non_context_child(type='watch', metadata={type:metadata}))
    elif state == oldstate:
        stack[-1].new_context_child(metadata={type:metadata})
    else: 
        stack.append(stack[-1].new_non_context_child(type=state, metadata={type:metadata}))

def reverse_handle_block_match(type, metadata, line):
    global state
    if type in META:
        stack[-1].add_metadata(metadata={type:metadata})
        return
    oldstate, state = state, type
    if state == 'end':
        stack.append(stack[-1].new_non_context_child(type='end', metadata={type:metadata}))
    elif state == 'watch':
        stack[-1].type = state
        stack[-1].add_metadata(metadata={type:metadata})
        stack.pop()
    elif state == oldstate or oldstate == 'end':
        stack[-1].new_context_child(metadata={type:metadata})
    else:
        giveme = stack[-1].borrow_child() # borrow the last child
        stack[-1].type = oldstate
        stack.pop()
        stack[-1].giveback_child(giveme) # give back the last child

def parse(line,
    runner = {
        "CONTENT": lambda(_,__,___): stack[-1].children[-1].content.append(line),
        "BLOCK": lambda(type,metadata,___): handle_block_match(type=type,line=line, metadata=metadata),
        "ONELINE": lambda(type,metas,___): stack[-1].new_non_context_child(metadata={type: metas["prompt"]}, type=type, groups=metas["groups"]),
        "INLINE": lambda(_,groups,___): stack[-1].add_inline_children(type="ai", line=line, groups=groups),
        }):
    TYPE, type, metadata, stripline = match(line)
    return runner[TYPE](type, metadata, stripline)
# 🐾 主函数骨架
def match(line):#only parse one line
    line = line.rstrip('\n')
    if compiled_escape.match(line):#escape
        stack[-1].children[-1].content.append(line)
        return "CONTENT", "", "", ""
    for k, regex in compiled_block.items():
        if(m:= regex.search(line)):
            return "BLOCK" , k, {k:m.group(1)},""
    prompt,type,groups = "", "",[]
    for k, regex in compiled_oneline.items():#oneline match, matching groups 1.
        if(m:= regex.search(line)):
            restline = m.group(1)
            prompt = m.group(2)
            line = restline
            type = k
    regex = compiled_inline.get("ai")
    if (mm := regex.search(line)):
        groups = list(mm.groupdict().values())
    metas = {"prompt":prompt,"groups":groups}
    if type:
        return "ONELINE", type, metas, line
    elif groups:
        return "INLINE", type, metas, line
    else:
        return "CONTENT", "", {}, line
