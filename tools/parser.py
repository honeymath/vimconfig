import re
from collections import defaultdict
import json
# 🌟 Node 数据结构
class Node:
    def __init__(self, type="", content=[], metadata={}):
        self.type = type
        self.children = []
        self.content = content if content else []
        self.metadata = defaultdict(list)
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
        return self.children.pop()

    def giveback_child(self, child):
        self.children.append(child)

    def add_inline_children(self, type, line, groups):
        child = self.new_non_context_child(type='inline')
        for group in groups:
            child.new_non_context_child(type=type, metadata={'group': group})

    def eat_child(self, child):
        if child.type != 'context':
            return
#            raise Exception('who is your daddy!')
        self.children[-1].content.extend(child.content)
        super_fucker = {rinima:bi for rinima,bi in child.metadata.items()}
        self.children[-1].add_metadata(super_fucker)
#        for k, v_list in child.metadata.items():
#            self.children[-1].metadata[k].extend(v_list)

    def kidnap_children(self, children):
        self.children.extend(children)

    def update(self, node):
        self.eat_child(node.children[0])
        for child in node.children[1:]:
            if self.type == child.type:
                self.kidnap_children(child.children)
            else:
                self.kidnap_children([child])

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
        self.stack = DefaultStack(Node)
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
            Orphanage.append(self.stack[-1].borrow_child())
            self.stack.pop()
            old_state = self.stack[-1].type
        self.stack[-1].kidnap_children(Orphanage)  
        self.stack[-1].children[-1].add_metadata({type: metadata})
        self.stack[-1].new_context_child(metadata={})## remember no fucking metadata
        self.stack[-1].type = self.state
        ### now modify the state based on the old state of courses.
            ## have to remember the state but do not use the remembered state to cover the state.
                 ## if the remembered state is end, there is nothing to do because safe to escape.
                 ## if the remembered state is the same the current state, there is nothing to do. 
                 ## if the remembered state is different from the current state, it have to collapse

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
                raise Exception("FUCKER your mother!")
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
    resrap = Parser(mode='reverse')
    parser.set_syntax_chars(comment_char='#', escape_char='##')
    resrap.set_syntax_chars(comment_char='#', escape_char='##')
    test_cases = [
        "tag0",
        "#ai:1",
        "tag1",
        "#see:2",
        "tag2",
        "#ai:3",
        "fuck0",
        "fuck1",
        "ai:f2",
        "fuck3",
        "fuck4",
        "#ai:f5",
        "fuck6",
        "fuck7",
        "fuck8",
        "fuck9",
        "#end",
        "rinima1",
        "#end",
        "rinima2",
        "#end",
        "rinima3",
    ]
#    test_cases = test_cases[::-1]  # Reverse the test cases for reverse mode

    cursor = 14
    parser.stack[-1].new_context_child(metadata={})  # This is SOF the init line mother fucker!!!!
    for i, line in enumerate(test_cases[cursor:]):
#        print(f"Test {i}: {line}")
        TYPE, type_, metadata, restline = parser.parse(line)
#        print(f"  Type: {TYPE}\n Block Type: {type_}\n Metadata: {metadata}\n Rest Line: '{restline}'")
#        print(f"  Stack depth: {parser.stack.len()}")
#        print(f"  Current node type: {parser.stack[-1].type}")
#        print("-" * 40)
#    parser.reverse_handle_block_match('', {}, '')# this is the init line
    resrap.stack[-1].new_context_child(metadata={})  # This is EOF. this is glue structure.
    for i, line in enumerate(test_cases[cursor-1::-1]):
        TYPE, type_, metadata, restline = resrap.parse(line)
    resrap.reverse_handle_block_match('', {}, '')  # this is SOF the init line
#    if (l:=parser.stack.len() >=0):
#        print(parser.stack[-l].to_json(indent=2))
#    else:
#        for ind,x in enumerate(parser.stack._history):
#            print(f"History {ind}: {x.to_json(indent=2)}")
#            print("-"*40)
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

#    print(f"History 0: {history[0].to_json(indent=2)}")
#    print("-" * 40)
#    print(f"Future 0: {future[0].to_json(indent=2)}")
#    print("-" * 40)


### fucker test of combining treee fuckkkkk
#    history[0].reverse()  # Reverse the first node
#    history[0].update(future[0])  # Update it with the first future node
#    freedom = history[0]
#    print(f"Combined history and future: {freedom.to_json(indent=2)}")
###    







    for regret,hope in list(zip(history,future)):
        print("current",counter)
        counter+=1
        regret.reverse()### fucking reverse it!!!
        if freedom:
            regret.giveback_child(freedom)
            regret.new_context_child(metadata={})## add glue back
#       print("--" * 40)
#       print("regret", regret.to_json(indent=2))
#       print("--" * 40)
#       print("hope", hope.to_json(indent=2))
#        for child in regret.children:
#            print(child.to_json(indent=2))
        regret.update(hope)
        freedom = regret
        print("current freedom", freedom.to_json(indent=2))
        print("-" * 40)
#    print(freedom.to_json(indent=2))

