#this file exists to modularize access to the dis library for the uncompile package
    #as this is called only once it is mostly unecersarry but I am keeping it here to keep my
    #architecture clean

import dis

#gets the string output of dis from the py_object supplied
def get_str(py_object): #this function is too straightforward to comment any further detail, please
                            #read the documentation for dis if you want to know more
    tmp = dis.Bytecode(py_object)
    return tmp.dis()
