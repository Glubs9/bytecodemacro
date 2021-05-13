from macro_lib import macro
#to test the argument handling of the macro library more rigorously

def add_arg(tups):
    ret = tups[:1]
    ret.append(("ADD_ARG", "a")) #adds extra argument a
    for n in tups[1:]: #could do with a list comprehension or map but this is easier to understand
        inst, arg = n
        if inst == "LOAD_NAME" and arg == "a":
            #replacing load_name with load_fast cause arguments have to be load_fast but the interpreter parses all mentions of a as load_name
            ret.append(("LOAD_FAST", "a")) 
        else:
            ret.append(n)
    return ret

@macro(add_arg)
def test(b):
    print("b passed as " + str(b))
    print("a passed as " + str(a))

test(3, 4)
