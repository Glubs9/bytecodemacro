#this file takes a list of tuples (with mnenoic instructions) and converts it to a bytes.
    #it also contains code to write out a file with a header that is a relic of when this was a
    #different project

import dis
import marshal
import bytecodemacro.bytecodecompiler.Header as Header

#compiles out a byte string into a bytes
def Compile(BytesStr):
    ret = []
    for n in BytesStr:
        ret += [dis.opmap[n[0]], n[1]]
    return bytes(ret)

#writes a code object out to a pyc file
def Out(fname, obj):
    fout = open(fname, "wb+")
    fout.write(Header.Header())
    marshal.dump(obj, fout)
