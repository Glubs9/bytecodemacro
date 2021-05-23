#this file takes the unrefined tuples from parse and returns the tuples properly pre_processed of 2 length tuples
    #the entry point for this file is the function pre_proccess (at the bottom of the file)

from functools import reduce, partial
from bytecodemacro.common.functional import compose, bind

#this function tests if an instruciton loads a code object
test_str = "<code object " #not the most rigorous check but I think it will work for now
def is_load_object(v):
    return v[0] == "LOAD_CONST" and v[2][:len(test_str)] == test_str

jump_statements = {"POP_JUMP_IF_TRUE", "POP_JUMP_IF_FALSE", "JUMP_IF_NOT_EXC_MATCH", "JUMP_IF_TRUE_OR_POP", "JUMP_IF_FALSE_OR_POP", "JUMP_ABSOLUTE", "SETUP_WITH", "JUMP_FORWARD", "FOR_ITER", "SETUP_FNIALLY"}

from bytecodemacro.uncompile.parse_dis import find_next_whitespace #this is placed here because it is only used by handle_third arg
#this function takes in an un_processed tuple with potentially a third argument, converts that
#argument to the modified bytecode syntax and returns it
    #todo: handle extended_arg instruction (i think we just delete it tbh, idk i've never seen it in compiled python)
def handle_third_arg(v):
    if len(v) == 1: return [(v[0], '0')]
    elif len(v) == 2: return [v]
    inst = v[0]
    if inst in {"SETUP_WITH", "JUMP_FORWARD", "FOR_ITER", "SETUP_FNIALLY"}:
        _, arg = v[2].split() #v[2] == "to x" where x is the absolute jump position
        return [(inst, arg)]
    elif inst in jump_statements:
        raise Exception("these should only be 2 long")
    elif is_load_object(v):
        #if this is load_const with <code object test at>
        #replace with load_object
        arg = v[2][13:] #gets the name of the object
        arg = arg[:find_next_whitespace(arg)]
        inst = "LOAD_OBJECT" #not techincally a python bytecode thing but it is in the modified bytecode
        return [(inst, arg)]
    elif inst in {"LOAD_CONST", "LOAD_NAME", "LOAD_GLOBAL", "LOAD_FAST", "STORE_FAST", "DELETE_FAST", "LOAD_ATTR", "LOAD_CLOSURE", "LOAD_DEREF", "LOAD_CLASSDEREF", "DELETE_DEREF", "LOAD_METHOD", "STORE_NAME", "STORE_ATTR", "STORE_GLOBAL", "STORE_DEREF", "DELETE_NAME", "DELETE_ATTR", "DELETE_GLOBAL", "IMPORT_NAME", "IMPORT_FROM", "COMPARE_OP"}:
        return [(inst, v[2])]#need to double check each one of the load_statements to make sure am parsing properly but i'm pretty sure this works

#takes in the pre_processed lines and adds labels to where the jump statements jump (as jump statement jump by line number not label in bytecode)
def handle_jumps(lines):
    jump_lines = set()
    for v in lines: #could be done with a set comprehension but this is clearer
        inst, arg = v
        if inst in jump_statements: 
            jump_lines.add(int(arg)) #found a place where the jump jumps to and adds it to the set
    ret = []
    for i in range(len(lines)):
        if i*2 in jump_lines: #i*2 because the jump statements are made by counting bytes not liens
            ret.append(("LABEL", str(i*2))) #the label is named like this so I don't have to change the jump statements
        ret.append(lines[i])
    return ret

#this function returns an empty list if the line is empty, but is identity for non_empty lines
    #this function is called in a bind, so in the bind it removes the empty lines
def remove_empty(line):
    if line[0] == '' and len(line) == 1: return []
    return [line]

#strings are given with ' ' but my cpyasm only works with " " so this function replaces any instances of the ' in the line passed
    #this can cause some issues when passing strings from macro_lib so it needs to be fixed later
def handle_strings(v):
    inst, arg = v
    if arg[0] == "'":
        arg = '"' + arg[1:-1] + '"'
    return (inst, arg)

#if the line passed is a load_global replace with a load_name
    #i'm not 100% on what this does but i'm pretty sure it fixed some bug somewhere
    #take a look at this in the future
def remove_globals(v):
    inst, arg = v
    if inst == "LOAD_GLOBAL":
        inst = "LOAD_NAME"
    return (inst, arg)

#for debugging, it is not currently used but it's really annoying to write again all over the shop so we live it like this for now
def trace(msg):
    def ret(n):
        print(msg + ": " + str(n))
        return n
    return ret

#this is the main entry point for the file
#it takes in a list of instructions, as returned by parse and returns a pre+processed and properly
#structured verison of those bytecode. 
    #note: this function does not handle the object structure (define, add_arg, end) which is handled in obj_handler.py
def pre_process(instructions):
    return compose(
        partial(bind, remove_empty),
        partial(bind, handle_third_arg),
        partial(map, handle_strings), 
        partial(map, remove_globals), 
        list, #this is because map does not reutrn a list but an iterable but handle_jumps requires a list
        handle_jumps
    )(instructions)
