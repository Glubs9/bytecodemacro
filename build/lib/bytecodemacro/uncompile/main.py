import bytecodemacro.uncompile.dis_wrapper as dis_wrapper
import bytecodemacro.uncompile.parse_dis as parse_dis
import bytecodemacro.uncompile.pre_process as pre_process
import bytecodemacro.uncompile.obj_handler as obj_handler
import sys as sys
import os as os
from functools import reduce

#this is done in multiple steps for dbeugging and clarity
    #takes an object and returns tuples containing each instruction
def main_tups(obj):
    objs = obj_handler.get_objects(obj)
    dis_strs = [dis_wrapper.get_str(n) for n in objs]
    parsed = [parse_dis.parse(n) for n in dis_strs]
    pre_processed = [pre_process.pre_process(n) for n in parsed]
    out_tuples = [obj_handler.add_definitions(objs[n], pre_processed[n]) for n in range(len(pre_processed))]
    out_tuples = list(reduce(lambda l1,l2: l1+l2, out_tuples))
    return out_tuples #not actually objects but lists of tuples with object information

#although this probably should be in a separate file it was unecersarry and useful to expose
def tups_to_str(tuples):
    out = ""
    for v in tuples:
        for i in v:
            out += i + " "
        out = out[:-1] #remove the extra space
        out += "\n"
    out = out[:-1] #remove extra new line
    return out

def main(): #takes object and returns string of cpyasm file
    fname = sys.argv[1]
    oname, _ = os.path.splitext(fname)
    oname += ".cpyasm"

    fc = open(fname, "r").read()
    obj = compile(fc, fname, "exec")

    tups = main_tups(obj)
    out_str = tups_to_str(tups)

    open(oname, "w").write(out_str)
