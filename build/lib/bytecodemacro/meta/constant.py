from macro_lib import macro

def constant(tups_in):
    ret = []
    constants = {}
    for n in tups_in:
        inst, arg = n
        if inst == "LOAD_CONST" and len(arg) > 6 and arg[1:6] == "const":
            var_name, val = arg[7:-1].split(" ")
            if var_name not in constants:
                constants[var_name] = val
            else:
                raise Exception("tried to redefine a constant")
        elif arg in constants:
            ret.append(("LOAD_CONST", constants[var_name]))
        else:
            ret.append(n)
    return ret

@macro(constant)
def test():
    _ = "const x 15" #note: x is only available in this scope
    print(x)
    x = 100
    print(x) #15 because x is constant set to 15
    #_ = "const x 100" #error because you cannot redefine a constant

test()
