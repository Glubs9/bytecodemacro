from bytecodemacro import macro

#basically function composition as syntax
    #note: this function is very rubbish and doesn't return anything. probs could but this is cool enough as is
def join(tuples):
    ret = []
    joining = False
    for n in tuples:
        inst, arg = n
        if inst == "LOAD_CONST" and arg == '"join"':
            joining = True
        elif inst == "LOAD_CONST" and arg == '"end"':
            joining = False
        elif joining and (inst == "POP_TOP" or inst[:5] == "STORE"): #remove operations that pop from stack
            continue
        elif joining and inst == "CALL_FUNCTION": #add extra arg to call_function
            ret.append((inst, str(int(arg)+1)))
        elif joining and inst == "LOAD_NAME":
            ret.append(n)
            ret.append(("ROT_TWO", "0"))
        else:
            ret.append(n)
    return ret

def mult_two(n):
    return n*2

@macro(join)
def test():
    _ = "join"
    n = 3
    range(6)
    sum()
    mult_two()
    print() #should print 24 because (3+4+5)*2 == 24
    _ = "end"
test()
