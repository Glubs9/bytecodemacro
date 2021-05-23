#this file takes a string returned by the dis wrapper and parses it into tuples
    #these tuples are not pre processed and as such are not always only 2 long and also does not
    #contain information that the objects hold
#the entry point for this file is def parse(obj_str):

#given a string return the position of the next whitespace
def find_next_whitespace(string):
    pos = 0
    for n in string:
        if n == " ": return pos
        pos+=1
    raise Exception("find next whitespace called without any whitespace")

#given a string return the position of the next non_whitespace
def find_non_whitespace(string):
    pos = 0
    for n in string:
        if n != " ": return pos
        pos += 1
    raise Exception("find non whitespace called with only whitespace")

#this function takes in a line from the dis string and splits it into it's arguments
    #including the third argument which is the dis library printing what the third arguments literal is
    #i.e: 0         load_const 0 ("hello world") could be a line that gets passed
def split_line(line):
    useable = line[16:] #removes the line numbers and pointer things
    if len(useable) < 25: return (useable,) #useable must be only one instruction
    w = find_next_whitespace(useable) #could replace with useable.index(" ")
    inst = useable[:w]
    arg = useable[w:]
    nw = find_non_whitespace(arg)
    arg = arg[nw:]
    if "(" not in arg:
        return (inst, arg)
    n = arg.index("(")
    n2 = list(reversed(arg)).index(")")-1 #searching from the back of the list just in case the arg is a string with a bracket in it
    arg_val = arg[n+1:n2]
    arg_num = arg[:n-1]
    return (inst, arg_num, arg_val) #might not need to return arg_num but whatever

#takes in the string returned by the dis and returns the un processed tuples from the string
def parse(obj_str):
    lines = obj_str.split("\n")
    args = [split_line(n) for n in lines]
    return args
