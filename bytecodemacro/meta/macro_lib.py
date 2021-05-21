import bytecodemacro.bytecodecompiler.Runner as runner
import bytecodemacro.uncompile.main as main
from types import FunctionType

def macro(mac_mod):
    def ret(f):
        tups = main.main_tups(f.__code__)
        new_func = mac_mod(tups)
        string = main.tups_to_str(new_func)
        code = runner.string_to_code(string, one_obj=True)
        return FunctionType(code, globals())
    return ret

#this takes a string and compiles it to cpyasm tups
    #relies on no return statements being sent
def byte_compile(string): #need to pass the state inside the funcdtion with like variables and that
    obj = compile(string, "string", "exec") #here
    tups = main.main_tups(obj)
    tups = tups[1:-3] #removes define and load_const None return_value end
    return tups

#for when you have a new definition
def byte_compile_obj(string):
    obj = compile(string, "string", "exec")
    tups = main.main_tups(obj)
    return tups

#only works with one object
def execute_tups(tups):
    string = main.tups_to_str(tups)
    code = runner.stirng_to_code(string, one_obj=True)
    exec(code)

#get unused_var name, pass the original functions tuples and the new tuples generated
    #quite slow but ehhhhhh i really can't be bothered rn
def unused_var(old_tups, new_tups, test="v1", am=1):
    for n in old_tups + new_tups:
        if len(n) == 2:
            inst, arg = n
            if arg == test: return unused_var(old_tups, new_tups, "v" + str(am+1), am+1)
    return test

#do something about ret.append() repteaed all the time
    #maybe use goto?

#maybe add unused jump name
