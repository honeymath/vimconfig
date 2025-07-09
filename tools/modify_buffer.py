
from parser import Parser
from collections import defaultdict
import json

cursor = -1

def set_marker(position, marker):
#    print(f"Set maker at position {position} with marker '{marker}' has been called.")
#    print(f"Set maker at position {position} with marker '{marker}' has been called.\n"*40)
    #return ## I am testing
    import vim
    line, col = position, 0
    bufnum = vim.current.buffer.number
    cmd = f"call setpos(\"'{marker}\", [{bufnum}, {line + 1}, {col + 1}, 0])"
    vim.command(cmd)
    

def modifiable(node):
#    if node.type == 'see' or node.type == 'watch' or node.metadata.get('see', False) or node.metadata.get('watch', False):
    if node.parent.type == 'see' or node.parent.type == 'watch':
       return False
    else:
       return True

def get_current_buffer():
    import vim
    # ✨ 输入数据
    
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

    #return lines
    return vim.current.buffer  # 获取当前缓冲区的所有行

def get_position_by_marker(marker):
    #position = 8
    #return position
    ## commenting above lines.
    import vim
    _,line_number,colum,_ = vim.eval(f"getpos(\"'{marker}\")")  # getpos returns [bufnum, lnum, col, off]
    line_number = int(line_number) - 1  # Vim 行号从1开始，Python从0开始
    return line_number

def separate_keys(key_list):## keylist is a list of address
    modify_keys = []
    negative_modify_keys = []
    for k in key_list:
        key_parts = [int(x) for x in k.split('/')]
        if key_parts[1] >= 0:
            modify_keys.append(tuple(key_parts))
        elif key_parts[1] < 0:
            negative_modify_keys.append(tuple(key_parts))
        
        if key_parts == [0,0]: ## this in make sure the 0,0 both appear in positive and negative part.
            negative_modify_keys.append(tuple(key_parts))
    return modify_keys, negative_modify_keys

def generate_emails_by_keys(modified_keys):
    arealist = defaultdict(list)
    nodelist = {}

    def handle_key(key,node):
        arealist[key].append(cursor)
        nodelist[key] = node
        print("A node detected")
        print(node.metadata)
        print("metadata printed")
    ## now generate the emails 
    emails = {}
    for keyma in modified_keys: ## each tuple
        key = list(keyma)
        the_mail = emails
        for k in key[:-1]:
            if k in the_mail:
                the_mail = the_mail[k]
            else:
                fuck = {}
                the_mail[k]=fuck
                the_mail = fuck
        the_mail[key[-1]] = lambda selfish, k=keyma: handle_key(k,selfish)
    return arealist,nodelist,emails





         

def handler(**args):
    global cursor ## this is used to follow the processing process
    level = 1
    lines = get_current_buffer()

    # ✉️ 构造邮件列表
    if args.get("to") is None:
        return "No recipient specified."
    if args.get("content") is None:
        return "No content specified."
    if args.get("marker") is None:
        return "Marker has to be specified."

    to = args["to"]
    content = args["content"]
    marker = args["marker"]
    input_email_list = {to: content}

    modified_keys, negative_modify_keys = separate_keys(input_email_list.keys())
    
    current_position = get_position_by_marker(marker)
    if current_position < 0:
        return "The marker can not be found. Please run reading the buffer again"

    negative_arealist, negative_nodelist, negative_emails = generate_emails_by_keys(negative_modify_keys)

    
    resrap = Parser(mode='reverse')
    resrap.stack.scale = -1
    resrap.set_syntax_chars(comment_char='#', escape_char='##')
    resrap.stack.emails = negative_emails
### Start processing

    cursor = current_position - 1

    resrap.stack[-1].new_context_child(metadata={})

    while resrap.stack.len() > -level and cursor >= 0:
        resrap.parse(lines[cursor])
        cursor -= 1

    resrap.reverse_handle_block_match('', {}, '')  # glue line

    
    
    
### Start status transfer
    parser = Parser(mode='normal')
    parser.set_syntax_chars(comment_char='#', escape_char='##')  # set the syntax
    arealist,nodelist,emails = generate_emails_by_keys(modified_keys) # set emails
    parser.stack.emails = emails
    
    for index, regret in enumerate(resrap.stack._history):
        parser.stack[-1 - index].type = regret.type
    parser.state = parser.stack[-1].type


    cursor = current_position
    parser.stack[-1].new_context_child(metadata={}) ## SOF, initialize
    while parser.stack.len() > -level-1 and cursor < len(lines):
        parser.parse(lines[cursor])
        cursor += 1

### Obtain history and future
    history = resrap.stack._history
    future = parser.stack._history



### Now deal witht the area and combine them.
## known arealist, and negative_arealist

    total_results = {}
    if (0,0) in arealist:
        if (0,0) not in negative_arealist:
            raise Exception("If (0,0) in arealist, it should also appear in historical bad arealist")
        smid,start = negative_arealist[(0,0)]
        emid, end = arealist[(0,0)]
        if smid + 1 != emid:
            print(f"start,smid,emid,end: {start,smid,emid,end}")
            raise Exception("The end of (0,0) or start of (0,0) does not match the cursor.")
        total_results[(0,0)] = [start, end]

    for k,v in arealist.items():
        if k == (0,0):
            continue
        total_results[k] = v
    for k,v in negative_arealist.items():
        if k == (0,0):
            continue
        if k in total_results:
            raise Exception(f"How come a negative key appear in total results?")
        total_results[k] = [v[1],v[0]] ## reverse because it is in history

##### The total results should be able to listed. then the 


### next give the sorted modify area.

    modify_area = {}

    for k,v in total_results.items():
        x,y = v
        if x == y:
            modify_area[k] = [x,y+1]
        else:
            modify_area[k] = [x+1,y]


    sorted_list = sorted(modify_area.items(), key=lambda item: item[1][0], reverse=True)
### apply the modification

    processed_keys = set() ## record the processed key  list(str)
    refused_keys = set() ## record the refused key list(str)

   
    if (0,0) in negative_nodelist:
        negative_nodelist[(0,0)].content.extend(nodelist[(0,0)].content) ## merge the content of 0,0


    total_nodelist = {}
    total_nodelist.update(nodelist)
    total_nodelist.update(negative_nodelist) ## note, the negative has priority.

        

    super_nodelist = {}

#    print("Lines before the modification")
#    print(json.dumps(lines, indent=2))
    for key, content_area in sorted_list:
        superkey = '/'.join([str(x) for x in list(key)])
        processed_keys.add(superkey)
        super_nodelist[superkey] = total_nodelist[key]
        content = input_email_list[superkey].split('\n')
    #    content = modify_list[key].split('\n')
        start, end = content_area
        if modifiable(total_nodelist[key]):
            lines[start:end] = content
        else:
            refused_keys.add(superkey)
            print(f"Modification for {superkey} is not allowed due to its properties.")

#    print("Lines after the modification")
#    print(json.dumps(lines, indent=2))

### Get those unprocessed emails
    all_keys = set(input_email_list.keys())
    unprocessed_keys = all_keys - processed_keys



    
    unprocessed_emails = {k:v for k, v in input_email_list.items() if k in unprocessed_keys}
    
    print(f"Processed keys: {processed_keys}")
    print(f"Unprocessed keys: {unprocessed_keys}")
    print(f"Refused keys: {refused_keys}")
    print(f"Original input email list: {json.dumps(input_email_list, indent=2)}")
    print(f"Total nodelist: {super_nodelist}")
    processed_emails = {k:{'replced_content':input_email_list[k], 'deleted_content':super_nodelist[k].to_dict()} for k in processed_keys-refused_keys}

    refused_emails = {k:v for k, v in input_email_list.items() if k in refused_keys}

# 1, when modify the 0,0, we have to reset the marker. easy, 
    if (0,0) in total_results:
        start,end = total_results[(0,0)]
        set_marker(position = (start+end)//2, marker=marker)


    
    return {
        "unprocessed_emails": unprocessed_emails,
        "processed_emails": processed_emails,
        "refused_emails": refused_emails,
        "marker": marker,
    }

if __name__ == "__main__":
    print(json.dumps(handler(to="1/0", content="This is a test email.\nIt has multiple lines.", marker="X"),indent=2))
