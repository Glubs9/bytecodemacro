#this file takes a list of tuples (with mnenoic instructions) and converts it to a bytes.
    #it also contains code to write out a file with a header that is a relic of when this was a
    #different project

import dis

#compiles out a byte string into a bytes
def Compile(BytesStr):
    ret = []
    for n in BytesStr:
        ret += [dis.opmap[n[0]], n[1]]
    return bytes(ret)
