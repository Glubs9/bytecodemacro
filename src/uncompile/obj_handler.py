import types

#update to add inner function and class support (idk about classes i just haven't tested it)
def get_objects(obj): 
    ret = [n for n in obj.co_consts if isinstance(n, types.CodeType)]
    return [obj] + ret

def var_names(obj):
    return [obj.co_varnames[n] for n in range(obj.co_argcount)]

def add_definitions(obj, tuples): #tuples have already been pre processed
    out = [("DEFINE", "main" if obj.co_name == "<module>" else obj.co_name)]
    out += [("ADD_ARG", n) for n in var_names(obj)]
    out += tuples
    out += [("END", "0")]
    return out
