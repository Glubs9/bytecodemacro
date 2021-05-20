#!/usr/bin/env python3

import marshal
import sys
import os

#my code imports
import bytecodemacro.bytecodecompiler.Read as Read
import bytecodemacro.bytecodecompiler.Parse as Parse
import bytecodemacro.bytecodecompiler.PreProcess as PreProcess
import bytecodemacro.bytecodecompiler.CodeContext as CodeContext
import bytecodemacro.bytecodecompiler.Compile as Compile

#useful for macros
def string_to_code(string, one_obj=False):
    read = Read.read_str(string)
    all_objs = [[Parse.get_args(n)] for n in Parse.split(read)] #objects are mapped to array so that we can use the pass by reference nature of the array to handle objects referencing other objects
    [PreProcess.PreProcess(n[0], all_objs) for n in all_objs] 
    for n in all_objs:
        n[0] = n[0].MakePyObj()
    if one_obj:
        if len(n) != 1: raise Exception("one_obj true but more than one object passed")
        return n[0]
    else:
        return next(n[0] for n in all_objs if n[0].co_name.upper() == "MAIN") #gets the object named main and returns it

#takes a file from sys.argv, compiles it and outputs a pyc file
def main():
    fname = sys.argv[1]
    oname, _ = os.path.splitext(fname)
    oname += ".pyc"
    Compile.Out(oname, string_to_code(open(fname, "r").read()))

#main() #uncomment outline to handle files
