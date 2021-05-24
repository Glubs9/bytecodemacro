from bytecodemacro import macro

#basically function composition as syntax
def join(tuples):
    ret = []
    joining = False
    for n in tuples:
        inst, arg = n
        if inst == "LOAD_CONST" and len(arg) > 5 and arg == "join":
            joining = True
        elif inst == "LOAD_CONST" and arg == "end":
            joining = False
        elif joining and (inst == "POP_TOP" or inst[:5] == "STORE"): #remove operations that pop from stack
            continue
        elif joining and inst == "CALL_FUNCTION": #add extra arg to call_function
            ret.append((inst, int(arg)+1))
        else:
            ret.append(n)
    for n in ret: print(n)
    return ret

def range_list(start, end):
    return list(range(start, end))

def sum_list(li):
    return sum(li)

def mult_two(n):
    return n*2

@macro(join)
def test():
    _ = "join"
    n = 3
    range_list(6)
    sum_list()
    mult_two()
    print()
    _ = "end"
test()
