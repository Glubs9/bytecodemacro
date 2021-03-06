#this file describes the api that the user can access through the bytecode macro library

import bytecodemacro.bytecodecompiler.Runner as runner
import bytecodemacro.uncompile.main as main
from types import FunctionType

#this is the main entry point for the api. It's a curried function that takes two functions and uses
    #the first to modify the seconds bytecode and returns the newly created function from that.
def macro(mac_mod):
    def ret(f):
        tups = main.main_tups(f.__code__) #gets tuple representation from passed function
        new_func = mac_mod(tups) #modifies the tuples with the passed macro
        code = runner.string_to_code(new_func, one_obj=True) #convert it back to python code object
        return FunctionType(code, f.__globals__) #returns code object as a function (might have a bug)
    return ret

#this takes a string and compiles it to bytecode tuples
    #relies on no return statements being sent
    #only works with single statements
    #very buggy, would not recommend useing 
def byte_compile(string): #need to pass the state inside the function with like variables and that
    obj = compile(string, "string", "single") #here
    tups = main.main_tups(obj)
    tups = tups[1:-3] #removes define and load_const None return_value end
    return tups

#this function is currently unused and untested
    #it is the same as byte_compile except it returns the definie and return_value statement
    #for when you have a new definition created in the string
def byte_compile_obj(string):
    obj = compile(string, "string", "exec")
    tups = main.main_tups(obj)
    return tups

#this function takes some tuples, compiles them and then runs thme
    #only works with one object
def execute_tups(tups):
    string = main.tups_to_str(tups)
    code = runner.stirng_to_code(string, one_obj=True)
    exec(code)

#this function takes two lists of tuples and returns a new variable name that is unused in both of the lists
    #quite slow and could be optimized later but this is good enough for now
def unused_var(old_tups, new_tups, test="v1", am=1):
    for n in old_tups + new_tups: #might be able to change to just passing one array of tuples
        if len(n) == 2:
            inst, arg = n
            if arg == test: return unused_var(old_tups, new_tups, "v" + str(am+1), am+1) #here is the source of inefficiency
    return test

#maybe add unused jump name
    #same as unused_var except for jump names
    #haven't had to need so far but if I do I will add this
