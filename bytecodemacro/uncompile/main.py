#this file describes the api for the uncompile library
    #it also contains some unecersarry code (in the main function) from when this was a different
    #project which should be removed at a later date

import bytecodemacro.uncompile.dis_wrapper as dis_wrapper
import bytecodemacro.uncompile.parse_dis as parse_dis
import bytecodemacro.uncompile.pre_process as pre_process
import bytecodemacro.uncompile.obj_handler as obj_handler
from functools import reduce

#this function takes in a python code object and returns the bytecode tuple representation
    #this is done in multiple steps for dbeugging and clarity
def main_tups(obj):
    objs = obj_handler.get_objects(obj)
    dis_strs = [dis_wrapper.get_str(n) for n in objs]
    parsed = [parse_dis.parse(n) for n in dis_strs]
    pre_processed = [pre_process.pre_process(n) for n in parsed]
    out_tuples = [obj_handler.add_definitions(objs[n], pre_processed[n]) for n in range(len(pre_processed))]
    out_tuples = list(reduce(lambda l1,l2: l1+l2, out_tuples))
    return out_tuples #not actually objects but lists of tuples with object information
