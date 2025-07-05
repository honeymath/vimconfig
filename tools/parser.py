import re
from collections import defaultdict
import json
# 🌟 Node 数据结构
class Node:
    def __init__(self, type, content=None, metadata=None):
        self.type = type
        self.children = []
        self.content = content if content else []
        self.metadata = defaultdict(list)
        if metadata:
            self.add_metadata(metadata)

    def to_dict(self):
        return {
            'type': self.type,
            'content': self.content,
            'metadata': dict(self.metadata),
            'children': [child.to_dict() for child in self.children]
        }

    def to_json(self, indent=2):
        return json.dumps(self.to_dict(), indent=indent)
    
    def add_metadata(self, metadata):
        for k, v in metadata.items():
            self.metadata[k].append(v)

    def new_context_child(self, metadata=None, type='context'):
        child = Node(type=type, metadata=metadata)
        self.children.append(child)
        return child

    def new_non_context_child(self, type='', metadata=None):
        child = Node(type=type, metadata=metadata)
        child.new_context_child()
        self.children.append(child)
        return child

    def borrow_child(self):
        return self.children.pop()

    def giveback_child(self, child):
        self.children.append(child)

    def add_inline_children(self, type, line, groups):
        child = self.new_non_context_child(type='inline')
        for group in groups:
            child.new_non_context_child(type=type, metadata={'group': group})

    def eat_child(self, child):
        if child.type != 'context':
            raise Exception('who is your daddy!')
        self.children[-1].content.extend(child.content)
        for k, v_list in child.metadata.items():
            self.children[-1].metadata[k].extend(v_list)

    def kidnap_children(self, children):
        self.children.extend(children)

    def update(self, node):
        self.children[-1].eat_child(node.children[0])
        self.children[-1].kidnap_children(node.children[1:])

# 🌟 DefaultStack 按小主设计
class DefaultStack:
    def __init__(self, default_factory):
        self._data = []
        self._history = []
        self.default_factory = default_factory

    def push(self, value):
        self._data.append(value)

    def append(self, value):
        self._data.append(value)

    def pop(self):
        if not self._data:
            self.generate()
        return self._data.pop()

    def generate(self):
        new_value = self.default_factory()
        self._history.append(new_value)
        self._data.insert(0, new_value)

    def __getitem__(self, index):
        if index >= 0:
            raise IndexError("Index must be negative for DefaultStack.")
        if index < -1000:
            raise IndexError("Index too negative, please use a reasonable negative index.")
        while -index > len(self._data):
            self.generate()
        return self._data[index]

    def len(self):
        """Returns the true length of the stack, excluding history."""
        return len(self._data) - len(self._history)
    def __len__(self):
        truelen = len(self._data) - len(self._history)
        if truelen < 0:
            print(f"[WARNING]Actual length {truelen} invalid, returning abs value; use .length() for true len")
            return -truelen
        return truelen

    def __repr__(self):
        return f"DefaultStack({self._data} - {self._history})"

# 🌟 Parser 主逻辑
class Parser:
    def __init__(self, mode='normal'):
        self.comment_char = '```'
        self.escape_char = '>'
        self.META = ['name', 'date']
        self.patterns = {
            'ai': 'ai:(.*?)$',
            'see': 'see:(.*?)$',
            'watch': 'watch:(.*?)$',
            'name': 'name:(.*?)$',
            'date': 'date:(.*?)$',
            'end': 'end()$',
        }
        self.compile_patterns()
        self.stack = DefaultStack(lambda: Node(type='root'))
        self.state = ""
        self.mode = mode  # 'normal' or 'reverse'


    def set_syntax_chars(self, comment_char=None, escape_char=None):
        if comment_char is not None:
            self.comment_char = comment_char
        if escape_char is not None:
            self.escape_char = escape_char
        self.compile_patterns()

    def compile_patterns(self):
        self.ESCAPE_PATTERN = re.compile(rf'^{self.escape_char}.*$')
        self.BLOCK_PATTERNS = {k: re.compile(rf'^{self.comment_char}{v}') for k, v in self.patterns.items()}
        self.ONELINE_PATTERNS = {k: re.compile(rf'^(.*?){self.comment_char}{v}') for k, v in self.patterns.items() if k not in self.META}
        self.INLINE_PATTERNS = {'ai': re.compile(r'([.,;!?]|\\s)(_{2,})([.,;!?]|\\s)')}

    def handle_block_match(self, type, metadata, line):
        if type in self.META:
            self.stack[-1].add_metadata({type: metadata})
            return
        old_state, self.state = self.state, type
        if self.state == 'end':
            self.stack.pop()
        elif self.state == 'watch':
            self.stack.append(self.stack[-1].new_non_context_child(type='watch', metadata={type: metadata}))
        elif self.state == old_state:
            self.stack[-1].new_context_child(metadata={type: metadata})
        else:
            self.stack.append(self.stack[-1].new_non_context_child(type=self.state, metadata={type: metadata}))

    def reverse_handle_block_match(self, type, metadata, line):
        if type in self.META:
            self.stack[-1].add_metadata({type: metadata})
            return
        old_state, self.state = self.state, type
        if self.state == 'end':
            self.stack.append(self.stack[-1].new_non_context_child(type='end', metadata={type: metadata}))
        elif self.state == 'watch':
            self.stack[-1].type = self.state
            self.stack[-1].add_metadata({type: metadata})
            self.stack.pop()
        elif self.state == old_state or old_state == 'end':
            self.stack[-1].new_context_child(metadata={type: metadata})
        else:
            giveme = self.stack[-1].borrow_child()
            self.stack[-1].type = old_state
            self.stack.pop()
            self.stack[-1].giveback_child(giveme)

    def match(self, line):
        line = line.rstrip('\n')
        if self.ESCAPE_PATTERN.match(line):
            return "CONTENT", "", {}, line

        for k, regex in self.BLOCK_PATTERNS.items():
            if (m := regex.search(line)):
                return "BLOCK", k, {k: m.group(1)}, ""

        prompt, type_, groups = "", "", []
        restline = line

        for k, regex in self.ONELINE_PATTERNS.items():
            if (m := regex.search(line)):
                restline = m.group(1)
                prompt = m.group(2)
                type_ = k
                break

        if type_:
            regex = self.INLINE_PATTERNS.get("ai")
            if regex and (mm := regex.search(restline)):
                groups = [mm.group(2)]
            metas = {"prompt": prompt, "groups": groups}
            return "ONELINE", type_, metas, restline

        regex = self.INLINE_PATTERNS.get("ai")
        if regex and (mm := regex.search(line)):
            groups = [mm.group(2)]
            metas = {"groups": groups}
            return "INLINE", "", metas, line

        return "CONTENT", "", {}, line

    def parse(self, line):
        TYPE, type_, metadata, restline = self.match(line)
        if TYPE == "CONTENT":
            if self.stack[-1].children:
                self.stack[-1].children[-1].content.append(line)
            else:
                self.stack[-1].content.append(line)
        elif TYPE == "BLOCK":
            if self.mode == 'reverse':
                self.reverse_handle_block_match(type_, metadata[type_], line)
            else:
                self.handle_block_match(type_, metadata[type_], line)
        elif TYPE == "ONELINE":
            child = self.stack[-1].new_non_context_child(type=type_, metadata={type_: metadata["prompt"]})
            for g in metadata["groups"]:
                child.new_non_context_child(type="ai", metadata={"group": g})
        elif TYPE == "INLINE":
            self.stack[-1].add_inline_children(type="ai", line=line, groups=metadata["groups"])
        return TYPE, type_, metadata, restline

if __name__ == '__main__':
    parser = Parser(mode='normal')
    parser.set_syntax_chars(comment_char='#', escape_char='##')
    test_cases = [
            "##Escape test",
            "#ai: one",
            "#date:2025-01-01",
            "#name:good",
            "#watch: causion",
            "#end",
            "#ai: one again",
            "#see: two",
            "#end",
            "#ai:one again again",
            "#end",
    ]

    for i, line in enumerate(test_cases, 1):
        print(f"Test {i}: {line}")
        TYPE, type_, metadata, restline = parser.parse(line)
        print(f"  Type: {TYPE}\n Block Type: {type_}\n Metadata: {metadata}\n Rest Line: '{restline}'")
        print(f"  Stack depth: {parser.stack.len()}")
        print(f"  Current node type: {parser.stack[-1].type}")
        print("-" * 40)
    if (l:=parser.stack.len() >=0):
        print(parser.stack[-l].to_json(indent=2))
