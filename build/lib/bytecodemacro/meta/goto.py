#this is an example use case of the macros library to implement gotos in python
#only reason this is not in it's own folder is to make importing easier
from macro_lib import macro

def goto(tups):
    ret = []
    for n in tups:
        inst, arg = n
        if inst == "LOAD_CONST" and len(arg) > 6 and arg[1:5] == "goto":
            ret.append(("JUMP_ABSOLUTE", arg[6:-1]))
        elif inst == "LOAD_CONST" and len(arg) > 2 and arg[-2] == ":":
            ret.append(("LABEL", arg[1:-2]))
        else:
            ret.append(n)
    return ret

@macro(goto)
def f():
    n = 0
    while n < 10:
        if n > 5:
            _ = "goto exit"
        print(n)
        n+=1
    _ = "exit:"
f()
