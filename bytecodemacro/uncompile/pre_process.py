from functools import reduce

def bind(f):
    def ret(li):
        return reduce(lambda n1,n2: n1+n2, map(f, li))
    return ret

def compose(inp, *fs):
    for n in fs:
        inp = n(inp)
    return inp

test_str = "<code object " #not the most rigorous check but I think it will work for now
def is_load_object(v):
    return v[0] == "LOAD_CONST" and v[2][:len(test_str)] == test_str

jump_statements = {"POP_JUMP_IF_TRUE", "POP_JUMP_IF_FALSE", "JUMP_IF_NOT_EXC_MATCH", "JUMP_IF_TRUE_OR_POP", "JUMP_IF_FALSE_OR_POP", "JUMP_ABSOLUTE", "SETUP_WITH", "JUMP_FORWARD", "FOR_ITER", "SETUP_FNIALLY"}

from bytecodemacro.uncompile.parse_dis import find_next_whitespace
#todo: handle extended_arg instruction (i think we just delete it tbh, idk i've never seen it in compiled python)
def handle_third_arg(v):
    if len(v) == 1: return [(v[0], '0')]
    elif len(v) == 2: return [v]
    inst = v[0]
    if inst in {"SETUP_WITH", "JUMP_FORWARD", "FOR_ITER", "SETUP_FNIALLY"}:
        _, arg = v[2].split() #v[2] == "to __" where __ is the absolute jump position
        return [(inst, arg)]
    elif inst in jump_statements:
        raise Exception("these should only be 2 long")
    elif is_load_object(v):
        #if this is load_const with <code object test at>
        #replace with load_object
        arg = v[2][13:] #gets the name of the object
        arg = arg[:find_next_whitespace(arg)]
        inst = "LOAD_OBJECT" #not techincally a python bytecode thing but it is in cpyasm
        return [(inst, arg)] #not handling right now for dbeugging purposes
    elif inst in {"LOAD_CONST", "LOAD_NAME", "LOAD_GLOBAL", "LOAD_FAST", "STORE_FAST", "DELETE_FAST", "LOAD_ATTR", "LOAD_CLOSURE", "LOAD_DEREF", "LOAD_CLASSDEREF", "DELETE_DEREF", "LOAD_METHOD", "STORE_NAME", "STORE_ATTR", "STORE_GLOBAL", "STORE_DEREF", "DELETE_NAME", "DELETE_ATTR", "DELETE_GLOBAL", "IMPORT_NAME", "IMPORT_FROM", "COMPARE_OP"}:
        #need to double check each one to make sure am parsing properly
        return [(inst, v[2])]

#finds places where jumps go to and adds labels to those places
    #this is elegant :)
def handle_jumps(lines):
    jump_lines = set()
    for v in lines: #could be done with a set comprehension but this is clearer
        inst, arg = v
        if inst in jump_statements: 
            jump_lines.add(int(arg))
    ret = []
    for i in range(len(lines)):
        if i*2 in jump_lines: #i*2 because the jump statements are made by counting bytes not liens
            ret.append(("LABEL", str(i*2)))
        ret.append(lines[i])
    return ret

def remove_empty(line):
    if line[0] == '' and len(line) == 1: return []
    return [line]

#strings are given with ' ' but my cpyasm only works with " "
def handle_strings(v):
    inst, arg = v
    if arg[0] == "'":
        arg = '"' + arg[1:-1] + '"'
    return (inst, arg)

def remove_globals(v):
    inst, arg = v
    if inst == "LOAD_GLOBAL":
        inst = "LOAD_NAME"
    return (inst, arg)

#for debugging
def trace(msg):
    def ret(n):
        print(msg + ": " + str(n))
        return n
    return ret

def pre_process(instructions):
    return compose(instructions, 
        bind(remove_empty),
        bind(handle_third_arg),
        lambda n: map(handle_strings, n),
        lambda n: map(remove_globals, n), #this is just cause i'm too lazy to handle globals ec dee
        list,
        handle_jumps
    )
