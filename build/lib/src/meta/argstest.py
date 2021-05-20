from macro_lib import macro

#this file tests the capabilities for the macro library to pass arguments

def trace(tups):
    for n in tups: print(n)
    return tups

@macro(trace)
def test(a):
    print("a passed as " + str(a))
    return a
print(test(3))
