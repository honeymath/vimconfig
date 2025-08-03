import re
from collections import defaultdict
import json
# 🌟 Node 数据结构
MODIFIABLE_KEYS = {'ai','python','kcuf','note','cao'}
UNMODIFIABLE_KEYS = {'see','watch'} 
class Node:
    def __init__(self, type="", content=[], metadata={},index=0, parent = None):
        ## so adding index will take care when stack poping out.
        self.type = type
        self.children = []
        self.content = content if content else []
        self.metadata = defaultdict(list)
        self.index = index
        self.emails = None
        self.parent = parent 
        if metadata:
            self.add_metadata(metadata)
    def brothers(self):
#        print("The element you care is")
#        print("--"*50)
#        print(self.to_json(indent=2))
        if not self.parent:
            return [self], 0
#        print("The fucking parent is")
#        print("--"*50)
#        print(self.parent.to_json(indent=2))
        brothers = self.parent.children
#        print("--"*50)
#        print("--"*50)
#        print(f"Brothers: {brothers.to_json(indent=2)}")
#        print(f"Brothers: {[x.type for x in brothers]}")
        self_index = brothers.index(self)
        return brothers, self_index

    def ancestry(self, ignore_brother = ['note','context'], accepted_type = ['kcuf'], accepted_meta = ['python'], representative = True):
        if self.type in accepted_type:
#            print(f"     {self.type} acc")
            for kid in self.children:
                if self.type in set(kid.metadata.keys()) and kid.metadata[self.type][-1] in accepted_meta:
#                    print(f"     {self.type} finds in keys")
                    return self.children[0].content
                else:
#                    print(f"     {self.type} does not find in keys")
#                    print(f"     the keys:{set(kid.metadata.keys())}")
#                    print(f"     {self.type} in {set(kid.metadata.keys())} value is {self.type in set(kid.metadata.keys())}")
#                    print(f"     the vlues:{kid.metadata[self.type]}")
#                    print(f"     {kid.metadata[self.type][-1]} in {accepted_meta} value is {kid.metadata[self.type] in accepted_meta}")
                    return [] # if the metadata does not match.
#        else:
#            print(f"     {self.type} not acc")
        if not representative and self.type in ignore_brother:
#            print(f"     rep {self.type} ign")
            return []
#        print(f"     rep {self.type} processing...")
        collected_ancestry = []
        if representative:
#            print("Representative is runned")
            if self.parent: 
#                print("Now call parent ancestry")
                collected_ancestry += self.parent.ancestry(ignore_brother = ignore_brother, accepted_type = accepted_type, accepted_meta = accepted_meta, representative = True)

            brothers, index = self.brothers()
            older_brothers = brothers[:index]
            helper = [x.type for x in older_brothers]
#            print(f"Fund older brothers{helper}, my position is at {index} in the brothers list.")
            for bro in older_brothers:
#                print("Find brothers, now do brothers")
                collected_ancestry += bro.ancestry(ignore_brother=ignore_brother, accepted_type = accepted_type,  accepted_meta = accepted_meta, representative = False) 
        else:
#            print("Non-representative is runned type is", self.type)
#            if "start_cursor" in self.metadata.keys():
#                print(f"Start cursor is {self.metadata['start_cursor'][-1]}")
#            if "end_cursor" in self.metadata.keys():
#                print(f"End cursor is {self.metadata['end_cursor'][-1]}")
            for kid in self.children:
                collected_ancestry += kid.ancestry(ignore_brother=ignore_brother, accepted_type = accepted_type, accepted_meta = accepted_meta,  representative = False)
        print(f"Running finished, now return {collected_ancestry}") 
        return collected_ancestry

    def modifiable(self):
#        if self.metadata['ai']:
        if set(self.metadata.keys()).intersection(MODIFIABLE_KEYS):
            return True
#        if self.metadata['see'] or self.metadata['watch']:
        if set(self.metadata.keys()).intersection(UNMODIFIABLE_KEYS):
            return False
        if not self.parent:
            return False
        if self.parent.type == 'ai':
            return True
        return False

    def append_content(self,line):
        self.content.append(line)
    def reverse(self):
        self.children.reverse()
        self.content.reverse()
        for key in self.metadata:
            self.metadata[key].reverse()
        for child in self.children:
            child.reverse()
    def to_dict(self, prefix='', callback=None):
        output_dic = {}
        ignore_meta = ['scale','end','path','regex']
        for k, v in self.metadata.items():
            if k not in ignore_meta and v and v[0]: # temply give all
                if k == 'ai':
                    output_dic[f'ai_instruction'] = v[-1]
                elif k == 'see':
                    output_dic[f'ai_instruction(do not modify block)'] = v[-1]
                elif k == 'watch':
                    output_dic[f'ai_instruction(do not modify block)'] = v[-1]
                else:
                    output_dic[f'm.{k}'] = v[-1]
        modifiable = self.modifiable()
        output_dic['modifiable'] = modifiable
        if modifiable:
            if self.metadata['path']:
                path_entry=self.metadata['path'][-1]
                path_entry = [x for x in path_entry]  # deep copy
                #output_dic['path'] = str(path_entry)
                inf_counter = 0
                for i in path_entry:
                    if i == float('inf') or i == -float('inf'):
                        inf_counter += 1
                path_entry[0:inf_counter] = [inf_counter]
                output_dic['block_path'] = prefix+( '/'.join([str(x) for x in path_entry]))
                if callable(callback):
                    callback(output_dic['block_path'])
        if self.type:
            output_dic['type']= self.type
        output_dic['parent'] = self.parent.type if self.parent else "NONE"
        
        if self.content:
            output_dic['content'] = '\n'.join(self.content)
        if self.children:
            output_dic['children'] = [child.to_dict(prefix=prefix,callback=callback) for child in self.children]
        return output_dic
    def to_json(self, indent=2, prefix = "", callback = None):
        return json.dumps(self.to_dict(prefix=prefix,callback=callback), indent=indent )
    
    def add_metadata(self, metadata):
        if not isinstance(self.metadata, defaultdict):
            raise Exception("The metadata of this node is not defaultdict, please do not modify medatada without calling add_metadata! ")
        for k, v in metadata.items():
            self.metadata[k].append(v)

    def new_context_child(self, metadata=None, type='context', silent = False):
        ### handle the notify the last chldren
        if self.children and not silent:
            self.children[-1].handle_end_signal()
        ### the above finish the notification
        child = Node(type=type, metadata=metadata, parent=self)
        ### handle the path
        if self.metadata['scale']:
            the_scale = self.metadata['scale'][-1]
        else:
            raise Exception(' The scale is not given')

        if self.metadata['path']:
            the_path = [x for x in self.metadata['path'][-1]] ## deep copy
            number_children = len(self.children)
            address = number_children * the_scale
            if self.emails and not callable(self.emails) and address in self.emails:
                child.emails = self.emails[address]
                #print(f"Child emails: {child.emails}")
                #print("Initial calling of email.")
                child.reply_email()
            the_path.append(address)
            #the_path.append(number_children*the_scale)
            child.add_metadata({'path':the_path})
            child.add_metadata({'scale':the_scale})
        else:
            raise Exception('The path is not here! ')
        ###
        self.children.append(child)
        return child

    def new_non_context_child(self, type='', metadata=None):
        ### handle the notify the last chldren
        if self.children:
            self.children[-1].handle_end_signal()
        ### the above finish the notification
        child = Node(type=type, metadata=metadata, parent=self)
        ### handle the path
        if self.metadata['scale']:
            the_scale = self.metadata['scale'][-1]
            #print(f"Child emails: {child.emails}")
        else:
            raise Exception(' The scale is not given')

        if self.metadata['path']:
            the_path = [x for x in self.metadata['path'][-1]] ## deep copy
            number_children = len(self.children)
            address = number_children * the_scale
            if self.emails and address in self.emails:
                child.emails = self.emails[address]
            the_path.append(address)
            child.add_metadata({'path':the_path})
            child.add_metadata({'scale':the_scale})
        else:
            raise Exception('The path is not here! ')
        ###
        self.children.append(child)
        return child

    def borrow_child(self):
        childrenlist = [self.children.pop()]
        while childrenlist[-1].type!= "context" or (self.children and self.children[-1].type!="context"):
            childrenlist.append(self.children.pop())
        return childrenlist

    def giveback_child(self, child):
        child.parent = self
        self.children.append(child)

    def add_inline_children(self, type=None, line='',  prompt= '', regex=None):
        child = self.new_context_child(type='oneline')
        meta = {}
        if type:
            meta[type] = prompt
        if regex:
            meta['regex'] = regex.pattern
        child.add_metadata(meta)
        child.content.append(line)
        self.new_context_child()  

    def extend_metadata(self,child):
#        print("-- Before updating meta data --")
#        print(json.dumps(self.metadata,indent = 2))
#        print("--children meta data --")
#        print(json.dumps(child.metadata,indent=2))
#        print("-- Before updating --")
        for k,v in child.metadata.items():
            self.metadata[k].extend(v)
#        print("-- After updating meta data --")
#        print(json.dumps(self.metadata,indent = 2))
#        print("-- After updating --")

    def eat_child(self, child):
        if child.type != 'context':
            raise ValueError("Child must be of type 'context' to be eaten.")
        self.children[-1].content.extend(child.content)
        self.children[-1].extend_metadata(child)

    def kidnap_children(self, children):
        for c in children:
            c.parent = self
        self.children.extend(children)

    def have_children(self):
        return bool(self.children)

    def update(self, node):
        self.extend_metadata(node)## add on Aug 3 , 2025 to fuck it
        self.eat_child(node.children[0])
        node.children = node.children[1:]  
        while node.children and node.children[0].type != self.type:
            self.kidnap_children([node.children[0]])
            node.children = node.children[1:]  # Remove the first child
        if node.children and node.children[0].type == self.type:
            self.kidnap_children(node.children[0].children)
            node.children = node.children[1:]

    def on_pop(self):
        self.children[-1].handle_end_signal()  # Notify the last child that it will be popped soon.

    def reply_email(self):
        if callable(self.emails):
            self.emails(self)
            #print("Email has been called")

    def handle_end_signal(self):
        self.reply_email() 
#            print(f"Emails: {self.emails}")
        ## this is only supposed to be called by the context node

# 🌟 DefaultStack 按小主设计
class DefaultStack:
    def __init__(self, default_factory, callback_index=-float('inf'), callback_function=None, scale = 1):
        self._data = []
        self._history = []
        self.default_factory = default_factory
        self.callback_index = callback_index
        self.callback_function = callback_function
        self.scale = scale # this is to scale the path
        self.emails = {}



    def append(self, value):
        #path = self.getpath()
        #value.add_metadata({'path': path})
        self._data.append(value)

    def pop(self, silent=False):
        if not self._data:
            self.generate()
        if not silent:
            self._data[-1].on_pop() ## notify the element it will be pop soon. prepare
        if self.len() == self.callback_index:
            if self.callback_function:
                self.callback_function(stack=self)
        return self._data.pop()

#    def getpath(self):
#        history_number = len(self._history)
        # Finish the logic of getting path
#        temp_path = [self.scale*float('inf')] * (history_number)
#        for i in self._data:
#            temp_path.append(len(i.children))
        # have to use deepcopy to avoid 
#        temp_path = [x * self.scale for x in temp_path]
        return temp_path

    def generate(self):
        new_value = self.default_factory()
        history_number = len(self._history)
        new_value.add_metadata({'path': [self.scale * float('inf')] * history_number})
        if history_number in self.emails:
            new_value.emails = self.emails[history_number]
        new_value.add_metadata({'scale': self.scale})
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
    def __init__(self, mode='normal', callback_function=None):
        self.comment_char = '```'
        self.comment_tail_char = '' # the comment tail char is used when of the form <!--xxx-->
        self.comment_char_pairs = [] # a future design, can put multiple comment chars
        self.escape_char = '>'
        self.META = ['name', 'date']
        self.SELF_NESTABLE_KEYS = ['watch','note','cao','kcuf']# define the self nestable keys
        self.END_KEYS = ['end','fuck','oac'] # the end keys are used to end the current context, and pop the stack.
        self.SELF_ISOLATED_KEYS = ['python'] # the isolated keys refuses cousins of the same type.
        self.snippet_char = '```' ###
        self.patterns = {
            'ai': 'ai:(.*?)',
            'see': 'see:(.*?)',
            'watch': 'watch:(.*?)',
            'note': 'note:(.*?)',
            'cao': 'cao:(.*?)',
            'oac': 'oac()',
            'name': 'name:(.*?)',
            'date': 'date:(.*?)',
            'end': 'end()',
        }
        self.compile_patterns()
        self.stack = DefaultStack(Node)
        self.state = ""
        self.mode = mode  # 'normal' or 'reverse'


    def set_syntax_chars(self, comment_char=None, escape_char=None, comment_tail_char = None, snippet_char = None,comment_char_pairs = None):
        if comment_char is not None:
            self.comment_char = comment_char
        if comment_tail_char is not None:
            self.comment_tail_char = comment_tail_char
        if escape_char is not None:
            self.escape_char = escape_char
        if comment_char_pairs is not None:
            self.comment_char_pairs = comment_char_pairs
        if snippet_char is not None:
            self.snippet_char = snippet_char
        self.compile_patterns()

    def compile_patterns(self):
        #self.snippet_char 
        self.ESCAPE_PATTERN = re.compile(rf'^{self.escape_char}.*$')
        if not self.comment_char_pairs:
            self.BLOCK_PATTERNS = {k: re.compile(rf'^{self.comment_char}{v}{self.comment_tail_char}$') for k, v in self.patterns.items()}
            self.ONELINE_PATTERNS = {k: re.compile(rf'^(.*?){self.comment_char}{v}{self.comment_tail_char}$') for k, v in self.patterns.items() if k not in self.META}
        if self.snippet_char:
            self.BLOCK_PATTERNS["kcuf"] = re.compile(rf'^{self.snippet_char}(.+)$')
            self.BLOCK_PATTERNS["fuck"] = re.compile(rf'^{self.snippet_char}()$')
#        print(self.BLOCK_PATTERNS)

    def handle_block_match(self, type, metadata, line, cursor = None): ## add cursor option for tracking
        if type in self.META:
            self.stack[-1].children[-1].add_metadata({type: metadata})
            return
        old_state, self.state = self.state, type
        if self.state in self.END_KEYS: #== 'end':
            poop = self.stack.pop()
            if cursor is not None:
                poop.add_metadata({'end_cursor': cursor})
            print(f"End detected! Stack poped, endcorsor is {cursor},poop is {poop.to_json(indent=2)}")
            self.state = self.stack[-1].type ## state reverse.
#            print(f"End detected! Stack poped, current length {self.stack.len()}, Status transferd to:{self.state}") 
            self.stack[-1].new_context_child(metadata={type: metadata})
        elif self.state in self.SELF_NESTABLE_KEYS: #== 'watch':
            self.stack.append(self.stack[-1].new_non_context_child(type=self.state))
            self.stack[-1].add_metadata({'start_cursor': cursor})
            self.stack[-1].new_context_child() ### added for fogic
            self.stack[-1].children[-1].add_metadata({type: metadata})
        elif self.state == old_state:
            self.stack[-1].new_context_child(metadata={type: metadata})
        else:
            self.stack.append(self.stack[-1].new_non_context_child(type=self.state))
            self.stack[-1].new_context_child() ### added for fogic
            self.stack[-1].children[-1].add_metadata({type: metadata})
            if cursor is not None:
                self.stack[-1].add_metadata({'start_cursor': cursor})

    def reverse_handle_block_match(self, type, metadata, line, cursor = None): ## add cursor option for tracking
        if type in self.META:
            self.stack[-1].children[-1].add_metadata({type: metadata})
            return
        old_state, self.state = self.state, type
        #from now on, the selfstate is the current type
        if self.state in self.END_KEYS:# == 'end': ## it has ignore the previous 
            self.stack.append(self.stack[-1].new_non_context_child(type=self.state, metadata={}))
            self.stack[-1].new_context_child() ### added for fogic
            if cursor is not None:
                self.stack[-1].add_metadata({'end_cursor': cursor})
            return
        elif self.state in self.SELF_NESTABLE_KEYS:# == 'watch':
            self.stack[-1].type = self.state
            self.stack[-1].children[-1].add_metadata({type: metadata})
            poop = self.stack.pop()
            if cursor is not None:
                poop.add_metadata({'start_cursor': cursor})
            self.stack[-1].new_context_child(metadata={})## everytime pop, create a context, without metadata.
            self.state = self.stack[-1].type  # remembers the state
            return
        ##from now on ,the coming state must be ai or see.
        Orphanage = []
        while old_state!='' and old_state not in self.END_KEYS and self.state != old_state:
            Orphanage.extend(self.stack[-1].borrow_child())
            self.stack.pop(silent=True)  # Pop the last element without notifying it
            old_state = self.stack[-1].type
        self.stack[-1].kidnap_children(Orphanage)  
        self.stack[-1].children[-1].add_metadata({type: metadata}) ### what? confuse? type:meta
        self.stack[-1].new_context_child(metadata={})## remember no  metadata
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
        saved_regex = None ## this is a to save the regex that mathing the oneline patterns

        for k, regex in self.ONELINE_PATTERNS.items():
            if (m := regex.search(line)):
                saved_regex = regex
                restline = m.group(1)
                prompt = m.group(2)
                type_ = k
                break

        if type_:
            metas = {"prompt": prompt,"regex": saved_regex}
            return "ONELINE", type_, metas, restline

        return "CONTENT", "", {}, line

    def parse(self, line, cursor = None): ## add cursor option for tracking positions
        TYPE, type_, metadata, restline = self.match(line)
        print(f"Parsing line: {line}")
        print(f"TYPE: {TYPE}, type_: {type_}, metadata: {metadata}, restline: {restline}")
        if TYPE == "CONTENT":
            if self.stack[-1].children:
                self.stack[-1].children[-1].append_content(line)
            else:
                raise Exception("Unexpected, the last element does not have content children")
        elif TYPE == "BLOCK":
            if self.mode == 'reverse':
                self.reverse_handle_block_match(type_, metadata[type_], line, cursor=cursor)
            else:
                self.handle_block_match(type_, metadata[type_], line, cursor=cursor)
        elif TYPE == "ONELINE":
            self.stack[-1].add_inline_children(type=type_, line=restline, prompt=metadata["prompt"], regex = metadata["regex"])
        return TYPE, type_, metadata, restline


def get_element_near_cursor(history,future):
    """
    if not future[0]:
        print(f"This element has not future elements.")
        return Node()
    elif not future[0].children:
        print(f"You have no children!")
        return Node()
    elif future[0].children[0].type == "context" or future[0].children[0].type == "oneline":
        # Aug 3th: I don't know why return the future element, 
        rinima = future[0].children[0].content
        if rinima:
            return future[0].children[0]
        else:
            return future[0].children[1] if len(future[0].children) > 1 else future[0].children[0]
    """
        # Now I will return the history, let me say the history must have fucking children
    return history[0].children[0]
        



if __name__ == '__main__':
    test_cases = [
        "Content 0",
        "<!--ai: block start-->",
            "```python",
            "print('This is a python code block')",
            "```",
            "```python",
            "print('This is a second python code block')",
            "```",
            "<!--see: see block-->",
                "<!--ai: AI block again-->",
                    "<!--see:second see block-->",
                        "Content line 2 #ai: mark inline", 
                        "Content 3",
                        "<!--watch: watch block-->",
                        "Content of watch",
                            "<!--watch: watch inside watch-->",
                            "Inside watch block",
                            "<!--end-->",
                        "<!--end-->",
                    "<!--see:chanlenge-->",
                        "Another see block",
                    "<!--end-->",
                    "Content4",
                "<!--ai:chanlange again-->",
                    "Again again",
                "<!--end-->",
                "Content5. SUPPOSE LAST ONE",
                "```fucker",
                "fefe",
                "```",
                "FUCK",
                "```python",
                "print('This is a python code block')",
                "fuck()",
                "```",
            "<!--end-->",
            "Content6",
        "<!--end-->",
        ]


    test_cases = [
        "<!--ai: can you see me-->",
        "<!--ai:  second block-->",
        "koooo",
        "<!--note:-->",
        "```python",
        "def hello_world():",
        '    print("Hello, world!")',
        "```",
        "",
        "<!--note:-->",
        "```python",
        "def another_function():",
        '    return "This is another function"',
        "```",
        "<!--end-->",
        "<!--end-->",
        "",
        "<!--see:another-->",
        "This is a noter test",
        "<!--end-->",
        "<!--end-->",
    ]
    test_cases = [
        "<!--note:NO0-->",
        "```python",
        "print('ffffff')",
        "print('ffffff')",
        "```",
        "<!--note:ignorefuck-->",
        "```python",
        "print('iiiiiii')",
        "```",
        "<!--end-->",
        "<!--note:NO1-->",
        "```python",
        "print('eeee')",
        "```",
        "rinima",
        "<!--note:NO2-->",
        "nimabibi",
        "caonimabi",
        "```python",
        "print('uuuuuuuu')",
        "```",
        "<!--end-->",
        "```python",
        "print('pppppppp')",
        "```",
        "<!--end-->",
        "<!--end-->",
#        "<!--end-->",
#        "<!--end-->",
    ]
    cursor = 16
## Now let us design the testing data
    test_cases = [
        "<!--watch: supposed to be processed, grand older brother-->",
        "```python",
            "1",
        "```",
        "<!--end-->",
        "<!--note:non-representative ancestor siblings, grand older brother-->",
            "This part is ancestor siblisngs suppoedd to be ignore as well",
            "```python",
                "x",
            "```",
        "<!--end-->",
        "<!--note:representative ancestors, direct grand parent-->",
            "```python",
                "2",
            "```",
            "<!--note:non-representative siblings, older uncle-->",
                "This part is suppoedd to be ignore",
                "```python",
                    "x",
                "```",
            "<!--end-->",
            "```python",
                "3",
            "```",
            "<!--note:representative siblinsgs, direct parent-->",
                "```python",
                    "4",
                "```",
                "Cursor position",
                "```python",
                    "x",
                "```",
            "<!--end-->",
            "<!--note:the smaller brothers, should ignore -->",
                "This part should be non-provessed",
                "```python",
                    "x",
                "```",
            "<!--end-->",
        "<!--end-->",
    ]
    cursor = 28
    test_casesa = [
        "<!--note:NO0-->",
        "<!--cao:nimabi-->",
        "print('ffffff')",
        "print('ffffff')",
        "<!--oac-->",
        "<!--cao:nimabi-->",
        "print('iiiiiii')",
        "<!--oac-->",
        "<!--note:NO1-->",
        "<!--cao:nimabi-->",
        "print('eeee')",
        "<!--oac-->",
        "rinima",
        "<!--note:NO2-->",
        "caonimabi",
        "<!--cao:nimabi-->",
        "print('uuuuuuuu')",
        "<!--oac-->",
        "nimashishabi",
        "<!--end-->",
        "<!--end-->",
        "<!--end-->",
    ]
    test_casesa = [
        "<!--watch:NO0-->",
        "<!--cao:nimabi-->",
        "print('ffffff')",
        "print('ffffff')",
        "<!--oac-->",
        "<!--cao:nimabi-->",
        "print('iiiiiii')",
        "<!--oac-->",
        "<!--watch:NO1-->",
        "<!--cao:nimabi-->",
        "print('eeee')",
        "<!--oac-->",
        "rinima",
        "<!--watch:NO2-->",
        "caonimabi",
        "<!--cao:nimabi-->",
        "print('uuuuuuuu')",
        "<!--oac-->",
        "nimashishabi",
        "<!--end-->",
        "<!--end-->",
        "<!--end-->",
    ]
    cursora = 18
    test_casesi = [
        "<!--watch:caonima-1-->",
        "<!--watch:caonima0-->",
        "Kuangcaonimabi",
        "<!--watch:caonima1-->",
        "Caonimacaonima",
        "<!--watch:caonima2-->",
        "nitamadeshishabi",
        "<!--end-->",
        "shabishabishabi",
        "<!--end-->",
        "<!--end-->",
        "<!--end-->",
    ]
    cursori = 8
#   cursor = 7
#    cursor = 0


### The history parser
    resrap = Parser(mode='reverse')
    resrap.stack.scale = -1
#    resrap.stack.emails = {0:{-3:"rinima!!!rinima!!!"},1:{-3:"line one "}}  # This is to test the email system.
#    resrap.set_syntax_chars(comment_char='#', escape_char='##')
    resrap.set_syntax_chars(comment_char='<!--', comment_tail_char='-->' ,escape_char='>>', snippet_char = '```')
    resrap.stack[-1].new_context_child(metadata={})  # This is EOF. this is glue structure.
    badcursor = cursor-1
    #while resrap.stack.len() > -3 and badcursor >=0:
    while badcursor >=0:
        line = test_cases[badcursor]
        
        resrap.parse(line, cursor=badcursor)
#        print(line)
#        print(resrap.stack.len())
#        print(resrap.stack._data)
#        print(len(resrap.stack._data))
#        print(resrap.stack._history)
#        print(len(resrap.stack._history))
#        print("-"*40)
        badcursor -= 1
    resrap.reverse_handle_block_match('', {}, '')  # this is SOF the init line.

#    for i, line in enumerate(test_cases[cursor-1::-1]):
#        TYPE, type_, metadata, restline = resrap.parse(line)
#    resrap.reverse_handle_block_match('', {}, '')  # this is SOF the init line


### begining transmission status
    parser = Parser(mode='normal')
    for index,regret in enumerate(resrap.stack._history):
        parser.stack[-1-index].type = regret.type
    parser.state = parser.stack[-1].type  # remember the state
####### Transmisssion finished. 
#    parser.set_syntax_chars(comment_char='#', escape_char='##', snippet_char='```')
    parser.set_syntax_chars(comment_char='<!--', comment_tail_char='-->' ,escape_char='>>', snippet_char = '```')
    goodcursor = cursor
    print(f"king parser state is {parser.state}")
    parser.stack[-1].new_context_child(metadata={})  # This is SOF the init line mother !!!!
    print(f"After king parser state is {parser.state}")
### We trasmit the state to the future parser
#    while parser.stack.len()>-3 and goodcursor < len(test_cases):
    while goodcursor < len(test_cases):
        line = test_cases[goodcursor]
        TYPE, type_, metadata, restline = parser.parse(line, cursor = goodcursor)
        print(f"line:{line}")
        print("    ", [x.type for x in parser.stack._history])
        print(f"    history length: {len(parser.stack._history)}")
        print("    ", [x.type for x in parser.stack._data])
        print(f"    future length: {len(parser.stack._data)}")
        print(f"    total length: {parser.stack.len()}")
        print(f"    Current Status: {parser.state}")
        
        goodcursor += 1





#    parser.stack[-1].new_context_child(metadata={})  # This is SOF the init line mother !!!!
#    for i, line in enumerate(test_cases[cursor:]):
#        TYPE, type_, metadata, restline = parser.parse(line)

#    print("Finished finding the future, now finding the histoy")

###


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

    fala = None
    for i in range(len(history)):
        history[i].reverse()
        if fala:
            history[i].giveback_child(fala)
            history[i].new_context_child(metadata={})
        if future[i].have_children(): # this is to fuck
            history[i].update(future[i])
        fala = history[i]
    print(f"Final Result:{history[-1].to_json(indent=2)}")
    
    print(f"Get the current elemenert brothers")
    bronima, inda = current_element.brothers()
    print(f"Brothers: {[x.type for x in bronima]}, index: {inda}")
    print("-" * 40)
    print("Ancestry is ")
    print("-" * 40)
    ance = current_element.ancestry(ignore_brother=['note','context'], accepted_type=['kcuf'], accepted_meta=['python'], representative=True)
    print(f"Ancestry: {json.dumps(ance, indent=2)}")




### the following is previous sasa when status is not given hava value
"""
    huhu = history[::-1]
    for hope in future:
        while hope.children:
            regret = huhu.pop()
            regret.reverse()
            if freedom:
                regret.giveback_child(freedom)
                regret.new_context_child(metadata={}) ## using to absorb .
            regret.update(hope)
            freedom = regret
            print(f"freedom: {freedom.to_json(indent = 2)}")
            print("-"*40)
"""
