#the header for the python bytecode, (probably doesn't need to be it's own file)

import importlib.util

def Header():
    """
    this function returns the header to be inserted at the top of the bytecode file
    """ 
    return importlib.util.MAGIC_NUMBER + b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    #the header is made of two parts, first is a magic number, unqiue to each python installation,
    #and second is a timestamp for when the file was made. For clarity I have written this as all
    #zeros
    #the rest of the bytecode file is a serialized (through the marshall library) python CodeObject
    #object. The documentation for this is intentionally vague but the (currently) working code
    #should be in and explained in the compiler
