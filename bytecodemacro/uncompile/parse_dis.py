#given a string return the position of the next whitespace
def find_next_whitespace(string):
    pos = 0
    for n in string:
        if n == " ": return pos
        pos+=1
    raise Exception("find next whitespace called without any whitespace")

def find_non_whitespace(string):
    pos = 0
    for n in string:
        if n != " ": return pos
        pos += 1
    raise Exception("find non whitespace called with only whitespace")

#we might want to save line >>s here so that we can create labels
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
    n2 = arg.index(")")
    arg_val = arg[n+1:n2]
    arg_num = arg[:n-1]
    return (inst, arg_num, arg_val) #might not need to return arg_num but whatever

#should return a list of tuples, one with arg name and the other with argument
def parse(obj_str):
    lines = obj_str.split("\n")
    args = [split_line(n) for n in lines] #could map but this is more pythonic
    return args
