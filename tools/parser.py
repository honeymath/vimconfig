import re
from collections import defaultdict
import json
# 🌟 Node 数据结构
class Node:
    def __init__(self, type="", content=[], metadata={},index=0):
        ## so adding index will take care when stack poping out.
        self.type = type
        self.children = []
        self.content = content if content else []
        self.metadata = defaultdict(list)
        self.index = index
        if metadata:
            self.add_metadata(metadata)

    def reverse(self):
        self.children.reverse()
        self.content.reverse()
        for key in self.metadata:
            self.metadata[key].reverse()
        for child in self.children:
            child.reverse()

    def to_dict(self):
        fucker = {}
        if self.type:
            fucker['type']= self.type
        if self.content:
            fucker['content'] = self.content
        if self.children:
            fucker['children'] = [child.to_dict() for child in self.children]
        for k, v in self.metadata.items():
            if v and v[0]:
                fucker[f'm.{k}'] = v[-1]
        return fucker

    def to_json(self, indent=2):
        return json.dumps(self.to_dict(), indent=indent)
    
    def add_metadata(self, metadata):
        if not isinstance(self.metadata, defaultdict):
            print("YOU SUPER FUCKER!!! ")
        try:
            for k, v in metadata.items():
                self.metadata[k].append(v)
        except Exception as e:
            print("Fuck the whole world!")
            print("Is default faught:", isinstance(self.metadata,defaultdict))
            raise e

    def new_context_child(self, metadata=None, type='context'):
        child = Node(type=type, metadata=metadata)
        self.children.append(child)
        return child

    def new_non_context_child(self, type='', metadata=None):
        child = Node(type=type, metadata=metadata)
        self.children.append(child)
        return child

    def borrow_child(self):
        childrenlist = [self.children.pop()]
        while childrenlist[-1].type!= "context" or (self.children and self.children[-1].type!="context"):
            childrenlist.append(self.children.pop())
        return childrenlist

    def giveback_child(self, child):
        self.children.append(child)

    def add_inline_children(self, type=None, line='',  prompt= ''):
        child = self.new_context_child(type='oneline')
        meta = {}
        if type:
            meta[type] = prompt
        child.add_metadata(meta)
        child.content.append(line)
        self.new_context_child()  

    def eat_child(self, child):
        if child.type != 'context':
            raise ValueError("Child must be of type 'context' to be eaten.")
        self.children[-1].content.extend(child.content)
        super_fucker = {rinima:bi for rinima,bi in child.metadata.items()}
        self.children[-1].add_metadata(super_fucker)

    def kidnap_children(self, children):
        self.children.extend(children)

    def update(self, node):
        self.eat_child(node.children[0])
        node.children = node.children[1:]  
        while node.children and node.children[0].type != self.type:
            self.kidnap_children([node.children[0]])
            node.children = node.children[1:]  # Remove the first child
        if node.children and node.children[0].type == self.type:
            self.kidnap_children(node.children[0].children)
            node.children = node.children[1:]

# 🌟 DefaultStack 按小主设计
class DefaultStack:
    def __init__(self, default_factory, callback_index=-float('inf'), callback_function=None):
        self._data = []
        self._history = []
        self.default_factory = default_factory
        self.callback_index = callback_index
        self.callback_function = callback_function

    def push(self, value):
        self._data.append(value)

    def append(self, value):
        self._data.append(value)

    def pop(self):
        if not self._data:
            self.generate()
        if self.len() == self.callback_index:
            if self.callback_function:
                self.callback_function(stack=self)
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
    def __init__(self, mode='normal', callback_index=-float('inf'), callback_function=None):
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
        self.stack = DefaultStack(Node,callback_index=callback_index, callback_function=callback_function)
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

    def handle_block_match(self, type, metadata, line):
        if type in self.META:
            self.stack[-1].children[-1].add_metadata({type: metadata})
            return
        old_state, self.state = self.state, type
        if self.state == 'end':
            self.stack.pop()
            self.state = self.stack[-1].type ## state reverse.
            self.stack[-1].new_context_child(metadata={type: metadata})
        elif self.state == 'watch':
            self.stack.append(self.stack[-1].new_non_context_child(type='watch'))
            self.stack[-1].new_context_child() ### added for fogic
            self.stack[-1].children[-1].add_metadata({type: metadata})
        elif self.state == old_state:
            self.stack[-1].new_context_child(metadata={type: metadata})
        else:
            self.stack.append(self.stack[-1].new_non_context_child(type=self.state))
            self.stack[-1].new_context_child() ### added for fogic
            self.stack[-1].children[-1].add_metadata({type: metadata})

    def reverse_handle_block_match(self, type, metadata, line):
        if type in self.META:
            self.stack[-1].children[-1].add_metadata({type: metadata})
            return
        old_state, self.state = self.state, type
        #from now on, the selfstate is the current type
        if self.state == 'end': ## it has ignore the previous fuck
            self.stack.append(self.stack[-1].new_non_context_child(type='end', metadata={}))
            self.stack[-1].new_context_child() ### added for fogic
            return
        elif self.state == 'watch':
            self.stack[-1].type = self.state
            self.stack[-1].children[-1].add_metadata({type: metadata})
            self.stack.pop()
            self.stack[-1].new_context_child(metadata={})## everytime pop, create a context, without fucking metadata.
            self.state = self.stack[-1].type  # remembers the state
            return
        ##from now on ,the coming state must be ai or see.
        Orphanage = []
        while old_state!='' and old_state != 'end' and self.state != old_state:
            Orphanage.extend(self.stack[-1].borrow_child())
            self.stack.pop()
            old_state = self.stack[-1].type
        self.stack[-1].kidnap_children(Orphanage)  
        self.stack[-1].children[-1].add_metadata({type: metadata})
        self.stack[-1].new_context_child(metadata={})## remember no fucking metadata
        self.stack[-1].type = self.state

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
            metas = {"prompt": prompt}
            return "ONELINE", type_, metas, restline

        return "CONTENT", "", {}, line

    def parse(self, line):
        TYPE, type_, metadata, restline = self.match(line)
        if TYPE == "CONTENT":
            if self.stack[-1].children:
                self.stack[-1].children[-1].content.append(line)
            else:
                raise Exception("FUCKER your mother!")
        elif TYPE == "BLOCK":
            if self.mode == 'reverse':
                self.reverse_handle_block_match(type_, metadata[type_], line)
            else:
                self.handle_block_match(type_, metadata[type_], line)
        elif TYPE == "ONELINE":
            self.stack[-1].add_inline_children(type=type_, line=restline, prompt=metadata["prompt"])
        return TYPE, type_, metadata, restline


def get_element_near_cursor(history,future):
    if not future[0]:
        print(f"You have no fucking future!")
        return Node()
    elif not future[0].children:
        print(f"You have no children!")
        return Node()
    elif future[0].children[0].type == "context":
        rinima = future[0].children[0].content
        if rinima:
            return future[0].children[0]
        else:
            return future[0].children[1] if len(future[0].children) > 1 else future[0].children[0]



if __name__ == '__main__':
    test_cases = [
        "#ai:First ai block",
        "Content line 1",
        "Content line 2 with inactiva inline __ ",
        "ai:Active line 3 with final mark #ai:do prompt",
        "#ai:Empty Line",
        "Active line 4 with inline _________ ___and___ ___a___bove should have empty content #see:some see",
        "Normal Content line 5",
        "Normal Content line 6",
            "#see: inner block",
                "Content line 7",
                "Content line 8",
                "active line 9 with inline __ and final mark #ai:caution",
            "#end",
        "#end",
    ]

    cursor = 12


### The future parser running.
    parser = Parser(mode='normal')
    parser.set_syntax_chars(comment_char='#', escape_char='##')

    parser.stack[-1].new_context_child(metadata={})  # This is SOF the init line mother fucker!!!!
    for i, line in enumerate(test_cases[cursor:]):
        TYPE, type_, metadata, restline = parser.parse(line)

### The history parser
    resrap = Parser(mode='reverse')
    resrap.set_syntax_chars(comment_char='#', escape_char='##')
    resrap.stack[-1].new_context_child(metadata={})  # This is EOF. this is glue structure.
    for i, line in enumerate(test_cases[cursor-1::-1]):
        TYPE, type_, metadata, restline = resrap.parse(line)
    resrap.reverse_handle_block_match('', {}, '')  # this is SOF the init line

### Obtain history and future
    history = resrap.stack._history
    future = parser.stack._history
    freedom = None
    counter = 0
    for ind, regret in enumerate(history):
        print(f"History {ind}: {regret.to_json(indent=2)}")
        print("-" * 40)

    for ind, hope in enumerate(future):
        print(f"Future {ind}: {hope.to_json(indent=2)}")
        print("-" * 40)


### The following is to get the cursor near the position 
    current_element = get_element_near_cursor(history, future);
    if current_element.type == "context":
        print(f"Cursor at {json.dumps(current_element.content, indent = 2)}")
    else:
        print(f"Cursor at {current_element.to_json(indent=2)}")

### the following function combines the history and future to print out the entire tree, can be used for the output.

    huhu = history[::-1]
    for hope in future:
        while hope.children:
            regret = huhu.pop()
            regret.reverse()
            if freedom:
                regret.giveback_child(freedom)
                regret.new_context_child(metadata={}) ## using to absorb fuck.
            regret.update(hope)
            freedom = regret
            print(f"freedom: {freedom.to_json(indent = 2)}")
            print("-"*40)
