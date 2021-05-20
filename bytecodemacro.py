import src.meta.macro_lib as macro_lib
#this file should expose the macro_lib for easy use?

def macro(n):
    return macro_lib.macro(n)
def byte_compile(n):
    return macro_lib.byte_compile(n)
def byte_compile_obj(n):
    return macro_lib.byte_compile_obj(n)
def execute_tups(n):
    return macro_lib.execute_tups(n)
def unused_var(n1,n2):
    return macro_lib.unused_var(n1,n2)
