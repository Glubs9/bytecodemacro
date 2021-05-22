#this file describes the wrapper used to access the dis library
    #this file is unecersarry and should be removed at a later date

import dis

#gets the string output of dis from the py_object supplied
def get_str(py_object):
    tmp = dis.Bytecode(py_object)
    return tmp.dis()
