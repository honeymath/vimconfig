from parser import Parser, get_element_near_cursor
from collections import defaultdict
import json

def set_email(email, value, emails_to_send):
    if len(email) == 1:
        emails_to_send[email[0]] = value
    else:
        if email[0] not in emails_to_send or not isinstance(emails_to_send[email[0]], dict):
            emails_to_send[email[0]] = {}
        set_email(email[1:], value, emails_to_send[email[0]])

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
#### the 

input_email_list = {"2/0": "replace1", "0/1": "replace2", "0/2": "replacejump","0/-2": "Addind start context", "0/-1": "Step 1 advanced", "0/0": "Step 2 advanced"}

modify_keys = []
negative_modify_keys = []

for k in input_email_list.keys():
    key_parts = [int(x) for x in k.split('/')]
    if key_parts[1] >= 0:
        modify_keys.append(tuple(key_parts))
    elif key_parts[1] < 0:
        negative_modify_keys.append(tuple(key_parts))
    
    if key_parts == [0,0]: ## this in make sure the 0,0 both appear in positive and negative part.
        negative_modify_keys.append(tuple(key_parts))


print("Modified keys:", modify_keys)
print("Negative modified keys:", negative_modify_keys)
## the following is an example of modified list
#modify_list = {(2,0): "replace1", (0,1): "replace2", (0,2):"replacejump"}





# 1. 向前回溯
badcursor=cursor-1
resrap = Parser(mode='reverse')
resrap.stack.scale = -1
resrap.set_syntax_chars(comment_char='#', escape_char='##')
## set up emails
badresults = defaultdict(list)
function_list = {k: lambda c,k=k: badresults[k].append(badcursor) for k in negative_modify_keys}
## the new request
# 1. after appending to the results to the time being. each time verify the self and obtain some datum, and also update some properties. 


emails_to_send = {}
for k,v in function_list.items():
    caocao = list(k)
    set_email(caocao, v, emails_to_send)
resrap.stack.emails = emails_to_send  
## finishing set up emails
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

#modify_keys = []
#negative_modify_keys = []


#modify_list = {(2,0): "replace1", (0,1): "replace2", (0,2):"replacejump"}



## set up emails
results = defaultdict(list)
function_list = {k: lambda c,k=k: results[k].append(goodcursor) for k in modify_keys}
emails_to_send = {}
for k,v in function_list.items():
    caocao = list(k)
    set_email(caocao, v, emails_to_send)
parser.stack.emails = emails_to_send  
## finishing set up emails






for index, regret in enumerate(resrap.stack._history):
    parser.stack[-1 - index].type = regret.type
parser.state = parser.stack[-1].type
parser.set_syntax_chars(comment_char='#', escape_char='##')

# 3. 向后拼接



goodcursor = cursor
parser.stack[-1].new_context_child(metadata={}) ## SOF
while parser.stack.len() > -level-1 and goodcursor < len(lines):
    print(f"Current cursor position", goodcursor, "with line:", lines[goodcursor])
    parser.parse(lines[goodcursor])
    print(f"The parser has been runned")

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
print(badresults)

#### Now combine the history results and future 

total_results = {}
if (0,0) in results:
    if (0,0) not in badresults:
        raise Exception("If (0,0) in results, it should also appear in historical bad results")
    smid,start = badresults[(0,0)]
    emid, end = results[(0,0)]
    if smid + 1 != emid:
        print(f"start,smid,emid,end: {start,smid,emid,end}")
        raise Exception("The end of (0,0) or start of (0,0) does not match the cursor.")
    total_results[(0,0)] = [start, end]

for k,v in results.items():
    if k == (0,0):
        continue
    total_results[k] = v
for k,v in badresults.items():
    if k == (0,0):
        continue
    if k in total_results:
        raise Exception(f"How come a negative key appear in total results?")
    total_results[k] = [v[1],v[0]] ## reverse because it is in history

## update finishi

#print(total_results)
    


modify_area = defaultdict(list)

for k,v in total_results.items():
    x,y = v
    if x == y:
        modify_area[k] = [x,y+1]
    else:
        modify_area[k] = [x+1,y]

    
# next sort the values in modify area and make sure there is no overlap.

sorted_list = sorted(modify_area.items(), key=lambda item: item[1][0], reverse=True)

print("The sorted list for modifying area:")
print(sorted_list)
print("End of the sorted list of modifying area")


### Lines before modification

print("The lines before modification")
print(json.dumps(lines,indent = 2))

for key, content_area in sorted_list:
    superkey = '/'.join([str(x) for x in list(key)])
    content = input_email_list[superkey].split('\n')
#    content = modify_list[key].split('\n')
    start, end = content_area
    lines[start:end] = content

print("The lines after modification")
print(json.dumps(lines, indent=2))
    



##### 
print("The good results")
print(results)
print("The bad results")
print(badresults)

### from here and finish the logic of bad results



#7 Some other, giving the change to the buffer according to the list.





