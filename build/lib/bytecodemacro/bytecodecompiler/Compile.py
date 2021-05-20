import dis
import marshal
import bytecodemacro.bytecodecompiler.Header as Header

def Compile(BytesStr):
    ret = []
    for n in BytesStr:
        ret += [dis.opmap[n[0]], n[1]]
    return bytes(ret)

def Out(fname, obj):
    fout = open(fname, "wb+")
    fout.write(Header.Header())
    marshal.dump(obj, fout)
