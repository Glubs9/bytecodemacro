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
    objs = obj_handler.get_objects(obj) #get all objects from passed obj (mostly unecersarry in the current iteration of the library)
    dis_strs = [dis_wrapper.get_str(n) for n in objs] #converts them all to strings from the output of dis.dis()
    parsed = [parse_dis.parse(n) for n in dis_strs] #parses the converted strings
    pre_processed = [pre_process.pre_process(n) for n in parsed] #pre processes the parsed strings
    out_tuples = [obj_handler.add_definitions(objs[n], pre_processed[n]) for n in range(len(pre_processed))] #converts them to properly formatted tuples to be sent to the user
    out_tuples = list(reduce(lambda l1,l2: l1+l2, out_tuples)) #joins all objects tuples together into one list
    return out_tuples #returns the tuples
