import bytecodemacro as p

def test(tups):
    print(tups)
    return tups

@p.macro(test)
def a():
    print("hello world")
a()
