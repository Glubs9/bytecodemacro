#this file describes the functions that handle code objects when they are used in the uncompile library

import types

#this function gets all the code objects from the constants array of another code object
    #this is useful for when a file is compiled and it contains many code objects, it may not be necersarry in the current iteration of the library
    #update to add inner function and class support (idk about classes i just haven't tested it)
        #as this does not handle functions with inner functions which would need a full tree search rather than this iteration
def get_objects(obj): 
    ret = [n for n in obj.co_consts if isinstance(n, types.CodeType)]
    return [obj] + ret #the ret list does not contain the object by itself unless the function is recursive
                            #this function might cause errors with recursive functions

#this function gets all of the argument names from an object
def arg_names(obj):
    return [obj.co_varnames[n] for n in range(obj.co_argcount)] #python code objects store arguments as the first n (where n is co_argcount) varnames

#this function takes a code object and it's bytecode tuple representation and outputs the header
#define and add_arg statements and the end statement to make it properly structured
def add_definitions(obj, tuples):
    out = [("DEFINE", "main" if obj.co_name == "<module>" else obj.co_name)]
    out += [("ADD_ARG", n) for n in arg_names(obj)]
    out += tuples
    out += [("END", "0")]
    return out
