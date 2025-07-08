from parser import Parser, get_element_near_cursor
import json

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
## optional: Set up emails:
## The first number 2 means the number of ../, for example, to access ../../1/2, you write 2/1/2. To access  3/2 you write 0/3/2, to access 0/0, you write 0/0/0  the 
## the email system can let the parser call fucntions while running. Used for GPT to modify the vim buffer area.

## todo list: Given a dictionary of path "a/b/c", dynamic create the function parser, and send to the.

## The output is a list, of the position, and a list of changing. the change will happen at the end.


### If the parser is running with empty email, it will just return the result. If the parser is running with emails, it will return the original and the result for each one. 

### Also, there should be a python file store the state. Have to have the request ID.....


### tasks.
# Task1: reformat the path json as a label directly used to receive emails.
# reformat m.ai and m.see as Can/Can not Modify this area, user said:
# Task2: Create function to translate the email list into start and end part list.
# Task 3: Given the list of range and text, modify the original input.

#dic defaultdict.


#lamnda c: dic[email].append(cursor)

## Create a state python to just store the state dictionary of vim's and also have a method to register a papa. 

#modify_list = {2:{0:"replace1"}, 0:{1:"replace2"}}

modify_list = {(2,0): "replace1", (0,1): "replace2", (0,2):"replacejump"}

from collections import defaultdict



results = defaultdict(list)
goodcursor = 0

function_list = {k: lambda c,k=k: results[k].append(goodcursor) for k in modify_list.keys()} ## use k=k to bind the variable k to the lambda function, otherwise it will always use the last value of k in the loop.


### print I have test calling

#for k, v in function_list.items():
#    goodcursor += 1
#    v("rinima")
#    print("Here is the output\n"*10)
#    print(results)
#    print("Above\n"*10)

### The fucking output
##results = {(0,1):[1,2]}
### I am expecting
## results = {(2,0):[2], (0,1):[1]}

###

emails_to_send = {}

def set_email(email, value, emails_to_send):
    if len(email) == 1:
        emails_to_send[email[0]] = value
    else:
        if email[0] not in emails_to_send or not isinstance(emails_to_send[email[0]], dict):
            emails_to_send[email[0]] = {}
        set_email(email[1:], value, emails_to_send[email[0]])
emails_to_send = {}
for k, v in function_list.items():
    set_email(list(k), v, emails_to_send)

print("Email has been prepared")
print(emails_to_send)
print("function_list")
print(function_list)


### Now emails_to_send should be a email list that can be send with the full function list.

## the variable to return is a results( the path to the [initial line number, end line number]) and the modify list , the path to  the content to modify. for later use.


for k,v in function_list.items():
    caocao = list(k)
    set_email(caocao, v, emails_to_send)

## now emails_to_send is the required emaillist?

def hand(content):
    print("You fucking bullshit\n"*10)
    print(content)
    print("You fucking bullshit\n"*10)

parser.stack.emails = emails_to_send  ## seding the emaill to future parser, don't forgot the history parser.
#parser.stack.emails = {2:{0:hand},0:{1:hand}}
### the above are email






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


## Optional, debugging output

#for ind, regret in enumerate(history):
#    print(f"History {ind}: {regret.to_json(indent=2)}")
#    print("-" * 40)

#for ind, hope in enumerate(future):
#    print(f"Future {ind}: {hope.to_json(indent=2)}")
#    print("-" * 40)

# 6. 获取光标位置的元素
print("Element near the cursor")
current_element = get_element_near_cursor(history, future);
if current_element.type == "context":
    print(f"Cursor at {json.dumps(current_element.content, indent = 2)}")
else:
    print(f"Cursor at {current_element.to_json(indent=2)}")

#####
fala = None
for i in range(level+1):
    history[i].reverse()
    if fala:
        history[i].giveback_child(fala)
        history[i].new_context_child(metadata={})
    history[i].update(future[i])
    fala = history[i]
#    print(f"-"*20, f"Level {i} fala:","-"*20)
#    print(fala.to_json(indent=2))

# 5. 输出最终结构
print("Test data:"
      )
for line in lines:
    print(line)
print("Final Result:")
print(fala.to_json(indent=2))

## Out put for the results of modifiying list for buffer to modify

print("The list for lines and modifying content:")
print(results)


modify_area = defaultdict(list)

for k,v in results.items():
    x,y = v
    if x == y:
        modify_area[k] = [x,y+1]
    else:
        modify_area[k] = [x+1,y]

    
# next sort the values in modify area and make sure there is no overlap.

sorted_list = sorted(modify_area.items(), key=lambda item: item[1][0], reverse=True)

print(sorted_list)


### Lines before modification

print("The lines before modification")
print(json.dumps(lines,indent = 2))

for key, content_area in sorted_list:
    content = modify_list[key].split('\n')
    start, end = content_area
    lines[start:end] = content

print("The lines after modification")
print(json.dumps(lines, indent=2))
    



#7 Some other, giving the change to the buffer according to the list.





