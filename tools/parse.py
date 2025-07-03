#parse the input into a tree.
import re

syntax = "#"
tree = {"__lines__":[]}
stack = [tree]

keywords = {
        "ai":"ai:",
        "see":"see:",
        "watch":"watch:",
        "end":"end",
        }

inline_regex = {
        "ai":"__",
        "see":"[[]]",
        }

with open("test.md", "r") as f:
    lines = f.readlines()

for line in lines:
    ## first, recognize syntax format
    ## priority 1 check if the first , make inline flag false, get the syntax
    # priority 2, match #syntax$, make inline flag true, get the tyntax
    # if pir1 or pri2 is matcherd, then based on syntax 
        # see mode: when stacks has odd number of elements; aimode: with even.
        ## see mode, mathch '#watch:' and '#ai:' or '#see:'
        ## ai mode, the watch is thesame as see
        ## end mode, then popstack. note the end must be no inline flag.
        ## if the inline flag is true, then finish the node, and continue
    # priority 3, match inline syntax by regex. depends on the mode, match inline syntax, quickly creates nodes and append.
        ## in see mode, only match ai syntax __
        ## in ai mode, only match see syntax [[]]
    # if no match happend,
        # current stack [-1].__lines__ += line


## after parsing, check if the stack is only have one element, the tree. and return the tree
