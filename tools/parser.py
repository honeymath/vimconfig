import re
from collections import defaultdict
import json
# 🌟 Node 数据结构
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

    def modifiable(self):
        if self.metadata['ai']:
            return True
        if self.metadata['see'] or self.metadata['watch']:
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
#see: try try try miao
    def to_dict(self):
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
                output_dic['block_path'] = ( '/'.join([str(x) for x in path_entry]))
        if self.type:
            output_dic['type']= self.type
        output_dic['parent'] = self.parent.type if self.parent else "NONE"
        
        if self.content:
            output_dic['content'] = '\n'.join(self.content)
        if self.children:
            output_dic['children'] = [child.to_dict() for child in self.children]
        return output_dic
#end
    def to_json(self, indent=2):
        return json.dumps(self.to_dict(), indent=indent)
    
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

    def update(self, node):
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

    def handle_block_match(self, type, metadata, line):
        if type in self.META:
            self.stack[-1].children[-1].add_metadata({type: metadata})
            return
        old_state, self.state = self.state, type
        if self.state == 'end':
            self.stack.pop()
            self.state = self.stack[-1].type ## state reverse.
#            print(f"End detected! Stack poped, current length {self.stack.len()}, Status transferd to:{self.state}") 
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
        if self.state == 'end': ## it has ignore the previous 
            self.stack.append(self.stack[-1].new_non_context_child(type='end', metadata={}))
            self.stack[-1].new_context_child() ### added for fogic
            return
        elif self.state == 'watch':
            self.stack[-1].type = self.state
            self.stack[-1].children[-1].add_metadata({type: metadata})
            self.stack.pop()
            self.stack[-1].new_context_child(metadata={})## everytime pop, create a context, without metadata.
            self.state = self.stack[-1].type  # remembers the state
            return
        ##from now on ,the coming state must be ai or see.
        Orphanage = []
        while old_state!='' and old_state != 'end' and self.state != old_state:
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

    def parse(self, line):
        TYPE, type_, metadata, restline = self.match(line)
        if TYPE == "CONTENT":
            if self.stack[-1].children:
                self.stack[-1].children[-1].append_content(line)
            else:
                raise Exception("Unexpected, the last element does not have content children")
        elif TYPE == "BLOCK":
            if self.mode == 'reverse':
                self.reverse_handle_block_match(type_, metadata[type_], line)
            else:
                self.handle_block_match(type_, metadata[type_], line)
        elif TYPE == "ONELINE":
            self.stack[-1].add_inline_children(type=type_, line=restline, prompt=metadata["prompt"], regex = metadata["regex"])
        return TYPE, type_, metadata, restline


def get_element_near_cursor(history,future):
    if not future[0]:
        print(f"This element has not future elements.")
        return Node()
    elif not future[0].children:
        print(f"You have no children!")
        return Node()
    elif future[0].children[0].type == "context" or future[0].children[0].type == "oneline":
        rinima = future[0].children[0].content
#        print(f"Rinima is {rinima}")
#        print(f"Future[0]{future[0].to_json(indent=2)}")
        if rinima:
            return future[0].children[0]
        else:
            return future[0].children[1] if len(future[0].children) > 1 else future[0].children[0]
#    print(future[0].children[0].to_json(indent=2))



if __name__ == '__main__':
    test_cases = [
        "Content 0",
        "#ai: block start",
            "#see: see block",
                "#ai: AI block again",
                    "#see:second see block",
                        "Content line 2 #ai: mark inline", 
                        "Content 3",
                    "#see:chanlenge",
                        "Another see block",
                    "#end",
                    "Content4",
                "#ai:chanlange again",
                    "Again again",
                "#end",
                "Content5. SUPPOSE LAST ONE",
            "#end",
            "Content6",
        "#end",
        ]
    cursor = 5
#    cursor = 0


### The history parser
    resrap = Parser(mode='reverse')
    resrap.stack.scale = -1
#    resrap.stack.emails = {0:{-3:"rinima!!!rinima!!!"},1:{-3:"line one "}}  # This is to test the email system.
    resrap.set_syntax_chars(comment_char='#', escape_char='##')
    resrap.stack[-1].new_context_child(metadata={})  # This is EOF. this is glue structure.
    badcursor = cursor-1
    while resrap.stack.len() > -2 and badcursor >=0:
        line = test_cases[badcursor]
        
        resrap.parse(line)
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
    parser.set_syntax_chars(comment_char='#', escape_char='##')
    goodcursor = cursor
    print(f"king parser state is {parser.state}")
    parser.stack[-1].new_context_child(metadata={})  # This is SOF the init line mother !!!!
    print(f"After king parser state is {parser.state}")
### We trasmit the state to the future parser
    while parser.stack.len()>-3 and goodcursor < len(test_cases):
        line = test_cases[goodcursor]
        TYPE, type_, metadata, restline = parser.parse(line)
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

"""
fala = None
for i in range(3):
    history[i].reverse()
    if fala:
        history[i].giveback_child(fala)
        history[i].new_context_child(metadata={})
    history[i].update(future[i])
    fala = history[i]
print(f"Final Result:{history[2].to_json(indent=2)}")
"""




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
