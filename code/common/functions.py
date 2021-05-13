from functools import reduce 
def bind(f):
    def ret(li):
        nonlocal f
        return list(reduce(lambda n,m:n+m, map(f, li)))
    return ret

def compose(inp, *fs):
    for n in fs:
        inp = n(inp)
    return inp
