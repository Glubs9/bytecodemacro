#this file describes the functions that handle code objects when they are used in the uncompile library

import types

#this function gets all the code objects from the constants array of another code object
    #this is useful for when a file is compiled and it contains many code objects, it may not be necersarry anymore
    #update to add inner function and class support (idk about classes i just haven't tested it)
def get_objects(obj): 
    ret = [n for n in obj.co_consts if isinstance(n, types.CodeType)]
    return [obj] + ret

#this function gets all of the argument names from an object
def arg_names(obj):
    return [obj.co_varnames[n] for n in range(obj.co_argcount)]

#this function takes a code object and it's bytecode tuple representation and outputs the header
#define and add_arg statements and the end statement to make it properly structured
def add_definitions(obj, tuples):
    out = [("DEFINE", "main" if obj.co_name == "<module>" else obj.co_name)]
    out += [("ADD_ARG", n) for n in arg_names(obj)]
    out += tuples
    out += [("END", "0")]
    return out
