#this is an attempt to build a c style for loop in python

from macro_lib import macro, byte_compile

def split(string_in):
    return string_in.split(";")

def cloop(tups):
    ret = []
    for_iterator = []
    checker = []
    for n in tups:
        if len(n) > 2: #fix later
            ret.append(n)
            continue
        inst, arg = n
        if arg == "_": continue #just cause my code is bad lmao
        elif inst == "LOAD_CONST" and len(arg) > 3 and arg[1:4] == "for":
            definition, check, iterator = tuple(split(arg[5:-1]))
            ret += byte_compile(definition)
            ret.append(("LABEL", "for"))
            for_iterator = byte_compile(iterator)
            checker = byte_compile(check)[:-1] #pops the result of comparison
        elif inst == "LOAD_CONST" and arg == '"end"':
            ret += for_iterator
            ret += checker
            ret.append(("POP_JUMP_IF_TRUE", "for"))
        else:
            ret.append(n)
    return ret

@macro(cloop)
def test(a):
    _ = "for c = 0;c < 10;c+=1"
    print(c)
    _ = "end"
test(10)
